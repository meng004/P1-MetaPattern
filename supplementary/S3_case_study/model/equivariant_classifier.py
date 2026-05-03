"""
EGNN-style E(3)-equivariant point-cloud classifier.

Following Satorras et al. 2021 "E(n) Equivariant Graph Neural Networks".
Each layer maintains
  - invariant features h_i (rotation/permutation invariant under message
    aggregation),
  - equivariant coordinates x_i (transform with SO(3) action).
The final classification is mean-pool over h_i then linear → C classes,
giving permutation invariance and rotation invariance by construction.

The class additionally exposes:
  - predict(point_cloud) -> np.ndarray of shape (C,)
  - attention_trace(x1, x2) -> float (Hermitian bilinear form for rho_adj)
  - sgd_step(theta, batch, eta) -> theta_new (functional SGD for rho_train_rev)
  - .theta : dict[str, np.ndarray] mirroring head_weight/head_bias schema
  - NUM_CLASSES : int

so that the §6.6 MR functions in mr_sets/set_N_noether.py work without
modification.
"""

from __future__ import annotations

from typing import Any, Optional

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F


# -----------------------------------------------------------------------------
# Backbone (pure PyTorch nn.Module for autograd)
# -----------------------------------------------------------------------------

class _EGNNLayer(nn.Module):
    def __init__(self, hidden_dim: int):
        super().__init__()
        self.mlp_e = nn.Sequential(
            nn.Linear(2 * hidden_dim + 1, hidden_dim),
            nn.SiLU(),
            nn.Linear(hidden_dim, hidden_dim),
        )
        self.mlp_x = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim),
            nn.SiLU(),
            nn.Linear(hidden_dim, 1),
        )
        self.mlp_h = nn.Sequential(
            nn.Linear(2 * hidden_dim, hidden_dim),
            nn.SiLU(),
            nn.Linear(hidden_dim, hidden_dim),
        )

    def forward(self, h: torch.Tensor, x: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
        # h: (n, hidden); x: (n, 3)
        n = x.shape[0]
        x_diff = x.unsqueeze(0) - x.unsqueeze(1)              # (n, n, 3)
        d_sq = (x_diff ** 2).sum(-1, keepdim=True)            # (n, n, 1)
        h_i = h.unsqueeze(1).expand(-1, n, -1)
        h_j = h.unsqueeze(0).expand(n, -1, -1)
        m = self.mlp_e(torch.cat([h_i, h_j, d_sq], dim=-1))   # (n, n, hidden)
        coord_factor = self.mlp_x(m)                           # (n, n, 1)
        x_new = x + (x_diff * coord_factor).sum(1) / max(n - 1, 1)
        m_agg = m.sum(1)                                       # (n, hidden)
        h_new = h + self.mlp_h(torch.cat([h, m_agg], dim=-1))
        return h_new, x_new


class EquivariantBackbone(nn.Module):
    """E(3)-equivariant point-cloud feature extractor + invariant linear head.

    Equivariance properties (provable from architecture):
      - SO(3) invariance of f(x): inner-loop uses only ||x_i - x_j||^2,
        and the head is on mean-pooled h, so rotating x leaves f
        unchanged within numerical tolerance.
      - S_n invariance: mean-pool is permutation-invariant; messages and
        layer updates are permutation-equivariant.
    """

    def __init__(self, hidden_dim: int = 16, n_layers: int = 2,
                 n_classes: int = 5) -> None:
        super().__init__()
        self.hidden_dim = hidden_dim
        self.n_layers = n_layers
        self.n_classes = n_classes
        self.embed = nn.Linear(1, hidden_dim)
        self.layers = nn.ModuleList([_EGNNLayer(hidden_dim) for _ in range(n_layers)])
        self.head = nn.Linear(hidden_dim, n_classes)
        # For rho_adj: a learnable QK matrix that is initialised symmetric.
        self.qk = nn.Parameter(torch.eye(hidden_dim))

    def featurize(self, x: torch.Tensor) -> torch.Tensor:
        n = x.shape[0]
        h = self.embed(torch.ones(n, 1, device=x.device, dtype=x.dtype))
        cur_x = x
        for layer in self.layers:
            h, cur_x = layer(h, cur_x)
        return h

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        h = self.featurize(x)
        return self.head(h.mean(dim=0))

    def attention_trace_internal(self, x1: torch.Tensor, x2: torch.Tensor) -> torch.Tensor:
        h1 = self.featurize(x1)
        h2 = self.featurize(x2)
        m = 0.5 * (self.qk + self.qk.T)  # symmetrise → guaranteed Hermitian
        return torch.trace(h1 @ m @ h2.T)


# -----------------------------------------------------------------------------
# Wrapper that conforms to the StubModel-compatible MR interface
# -----------------------------------------------------------------------------

class EquivariantPointCloudClassifier:
    """Mirror of StubModel's interface, backed by a trained EGNN backbone."""

    NUM_CLASSES = 5

    def __init__(self, backbone: EquivariantBackbone, device: str = "cpu") -> None:
        self.backbone = backbone.to(device)
        self.backbone.eval()
        self.device = device
        self.NUM_CLASSES = backbone.n_classes
        self._refresh_theta()

    def _refresh_theta(self) -> None:
        self.theta: dict[str, np.ndarray] = {}
        for name, p in self.backbone.state_dict().items():
            self.theta[name] = p.detach().cpu().numpy().copy()

    @property
    def parameters(self) -> dict:
        """Mirrors StubModel.parameters; same as `self.theta`."""
        return self.theta

    # -------- MR-facing predict ---------
    def predict(self, point_cloud: Any) -> np.ndarray:
        with torch.no_grad():
            x = torch.as_tensor(np.asarray(point_cloud), dtype=torch.float32,
                                device=self.device)
            logits = self.backbone(x)
            probs = torch.softmax(logits, dim=-1).cpu().numpy()
        return probs

    # -------- MR-facing attention trace ---------
    def attention_trace(self, x1: Any, x2: Any) -> float:
        with torch.no_grad():
            t1 = torch.as_tensor(np.asarray(x1), dtype=torch.float32, device=self.device)
            t2 = torch.as_tensor(np.asarray(x2), dtype=torch.float32, device=self.device)
            return float(self.backbone.attention_trace_internal(t1, t2).cpu())

    # -------- MR-facing functional SGD step ---------
    def sgd_step(self, theta: dict, batch: tuple, eta: float, *,
                  grad_clip: float = 1.0) -> dict:
        """One vanilla SGD step, with global gradient norm clipping at
        ``grad_clip`` (default 1.0) to keep round-trip arithmetic stable
        on the small EGNN. Gradient clipping does not break time-reversal
        symmetry as long as both directions clip the same way, which they
        do here.
        """
        x_np, y_int = batch
        x = torch.as_tensor(np.asarray(x_np), dtype=torch.float32, device=self.device)
        y = torch.as_tensor([int(y_int)], dtype=torch.long, device=self.device)
        tmp = EquivariantBackbone(
            hidden_dim=self.backbone.hidden_dim,
            n_layers=self.backbone.n_layers,
            n_classes=self.NUM_CLASSES,
        ).to(self.device)
        sd = {k: torch.as_tensor(v, device=self.device) for k, v in theta.items()}
        tmp.load_state_dict(sd)
        tmp.train()
        for p in tmp.parameters():
            p.grad = None
        logits = tmp(x).unsqueeze(0)
        loss = F.cross_entropy(logits, y)
        loss.backward()
        # Global gradient-norm clipping for stability.
        torch.nn.utils.clip_grad_norm_(tmp.parameters(), max_norm=grad_clip)
        new_theta: dict = {}
        with torch.no_grad():
            for name, p in tmp.named_parameters():
                if p.grad is None or torch.isnan(p.grad).any():
                    new_theta[name] = p.detach().cpu().numpy().copy()
                else:
                    new_p = p - eta * p.grad
                    new_theta[name] = new_p.detach().cpu().numpy().copy()
        return new_theta


# -----------------------------------------------------------------------------
# Loader helper
# -----------------------------------------------------------------------------

def load_equivariant_classifier(checkpoint_path: str,
                                 device: Optional[str] = None) -> EquivariantPointCloudClassifier:
    if device is None:
        device = "mps" if torch.backends.mps.is_available() else "cpu"
    ckpt = torch.load(checkpoint_path, map_location=device, weights_only=False)
    backbone = EquivariantBackbone(
        hidden_dim=ckpt["hidden_dim"],
        n_layers=ckpt["n_layers"],
        n_classes=ckpt["n_classes"],
    )
    backbone.load_state_dict(ckpt["state_dict"])
    return EquivariantPointCloudClassifier(backbone, device=device)

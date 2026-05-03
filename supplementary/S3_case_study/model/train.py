"""
Train the EGNN point-cloud classifier and save a checkpoint.

Default config (M1 Pro friendly): 5 classes, 64 points, hidden=16, 2 layers,
batch_size=32, 25 epochs. Wallclock ~5-10 min on M1 Pro CPU/MPS.

Outputs:
  - se3_classifier.pt   (state_dict + arch config; load with
                          equivariant_classifier.load_equivariant_classifier)
  - training_log.json    per-epoch loss / accuracy
  - dataset_meta.json    seed and configuration of the synthetic dataset
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np
import torch
import torch.nn.functional as F

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from equivariant_classifier import EquivariantBackbone
from synth_dataset import N_CLASSES, N_POINTS, make_split


def train(
    out_path: Path,
    num_train_per_class: int = 80,
    num_val_per_class: int = 20,
    hidden_dim: int = 16,
    n_layers: int = 2,
    batch_size: int = 32,
    epochs: int = 25,
    lr: float = 5e-3,
    seed: int = 20260501,
    device: str | None = None,
) -> dict:
    if device is None:
        device = "mps" if torch.backends.mps.is_available() else "cpu"
    print(f"[train] device = {device}")

    torch.manual_seed(seed)
    np.random.seed(seed)

    print("[train] generating synthetic data...")
    X_train, y_train = make_split(num_train_per_class, seed=seed)
    X_val, y_val = make_split(num_val_per_class, seed=seed + 1)
    print(f"[train] train clouds: {len(X_train)}, val clouds: {len(X_val)}")

    model = EquivariantBackbone(hidden_dim=hidden_dim, n_layers=n_layers,
                                 n_classes=N_CLASSES).to(device)
    n_params = sum(p.numel() for p in model.parameters())
    print(f"[train] backbone parameters: {n_params}")

    optimizer = torch.optim.Adam(model.parameters(), lr=lr)

    log: list[dict] = []
    for epoch in range(epochs):
        model.train()
        idx = np.random.permutation(len(X_train))
        running = 0.0
        n_seen = 0
        n_correct_train = 0
        for start in range(0, len(idx), batch_size):
            batch_idx = idx[start:start + batch_size]
            optimizer.zero_grad()
            losses = []
            for i in batch_idx:
                x = torch.as_tensor(X_train[i], dtype=torch.float32, device=device)
                y = torch.as_tensor([int(y_train[i])], dtype=torch.long, device=device)
                logits = model(x).unsqueeze(0)
                losses.append(F.cross_entropy(logits, y))
                pred = int(torch.argmax(logits).item())
                if pred == int(y_train[i]):
                    n_correct_train += 1
                n_seen += 1
            loss = torch.stack(losses).mean()
            loss.backward()
            optimizer.step()
            running += float(loss.item()) * len(batch_idx)
        train_loss = running / max(n_seen, 1)
        train_acc = n_correct_train / max(n_seen, 1)

        # Validation
        model.eval()
        val_correct = 0
        val_loss = 0.0
        with torch.no_grad():
            for i in range(len(X_val)):
                x = torch.as_tensor(X_val[i], dtype=torch.float32, device=device)
                y = torch.as_tensor([int(y_val[i])], dtype=torch.long, device=device)
                logits = model(x).unsqueeze(0)
                val_loss += float(F.cross_entropy(logits, y).item())
                if int(torch.argmax(logits).item()) == int(y_val[i]):
                    val_correct += 1
        val_loss /= max(len(X_val), 1)
        val_acc = val_correct / max(len(X_val), 1)
        epoch_rec = {"epoch": epoch, "train_loss": train_loss,
                     "train_acc": train_acc, "val_loss": val_loss,
                     "val_acc": val_acc}
        log.append(epoch_rec)
        print(f"  epoch {epoch:3d} | train_loss={train_loss:.4f} train_acc={train_acc:.3f} "
              f"| val_loss={val_loss:.4f} val_acc={val_acc:.3f}")

    # Save checkpoint
    ckpt = {
        "state_dict": {k: v.detach().cpu() for k, v in model.state_dict().items()},
        "hidden_dim": hidden_dim,
        "n_layers": n_layers,
        "n_classes": N_CLASSES,
        "n_points": N_POINTS,
        "training_seed": seed,
    }
    torch.save(ckpt, out_path)
    print(f"[train] saved checkpoint to {out_path}")

    return {
        "log": log,
        "final_val_acc": log[-1]["val_acc"],
        "n_params": n_params,
        "n_train": len(X_train),
        "n_val": len(X_val),
    }


if __name__ == "__main__":
    out = ROOT / "se3_classifier.pt"
    log_path = ROOT / "training_log.json"
    meta_path = ROOT / "dataset_meta.json"
    t0 = time.time()
    result = train(out_path=out)
    elapsed = time.time() - t0
    print(f"[train] wallclock {elapsed:.1f}s")
    log_path.write_text(json.dumps({
        "elapsed_seconds": elapsed,
        "final_val_acc": result["final_val_acc"],
        "n_params": result["n_params"],
        "n_train": result["n_train"],
        "n_val": result["n_val"],
        "epochs": result["log"],
    }, indent=2))
    meta_path.write_text(json.dumps({
        "n_classes": N_CLASSES,
        "n_points": N_POINTS,
        "shape_classes": ["sphere", "cube_surface", "torus", "cone", "helix"],
        "rotation_augmentation": True,
        "training_seed": 20260501,
    }, indent=2))
    print(f"[train] log written to {log_path}")

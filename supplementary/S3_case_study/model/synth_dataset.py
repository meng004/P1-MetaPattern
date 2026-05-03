"""
Procedural 5-class point-cloud dataset for the §6.6 case study.

Classes (each a parametric 3D shape sampled to N points):
  0 sphere       — uniform on unit sphere
  1 cube_surface — uniform on unit cube surface
  2 torus        — torus(R=1.0, r=0.3)
  3 cone         — apex at origin, base radius 1, height 1
  4 helix        — 3D helix with 3 turns

Each cloud is rotated by a uniformly random SO(3) rotation at sampling
time so the classifier must learn rotation-invariant features (the
training signal explicitly demands invariance, mirroring how an SO(3)-
equivariant network is typically trained on ModelNet).

The dataset is fully deterministic given a seed.
"""

from __future__ import annotations

import numpy as np


def _random_rotation(rng: np.random.Generator) -> np.ndarray:
    a = rng.standard_normal((3, 3))
    q, r = np.linalg.qr(a)
    d = np.sign(np.diag(r)).astype(np.float64)
    q = q * d
    if np.linalg.det(q) < 0:
        q[:, 0] = -q[:, 0]
    return q.astype(np.float32)


def _sphere(n: int, rng: np.random.Generator) -> np.ndarray:
    v = rng.standard_normal((n, 3)).astype(np.float32)
    v /= np.linalg.norm(v, axis=1, keepdims=True) + 1e-9
    return v


def _cube_surface(n: int, rng: np.random.Generator) -> np.ndarray:
    pts = rng.uniform(-0.5, 0.5, (n, 3)).astype(np.float32)
    # Pick a face for each point and snap that coordinate to ±0.5
    face = rng.integers(0, 6, n)
    coord = face // 2
    sign = np.where(face % 2 == 0, -0.5, 0.5).astype(np.float32)
    pts[np.arange(n), coord] = sign
    return pts


def _torus(n: int, rng: np.random.Generator, R: float = 1.0, r: float = 0.3) -> np.ndarray:
    u = rng.uniform(0, 2 * np.pi, n)
    v = rng.uniform(0, 2 * np.pi, n)
    x = (R + r * np.cos(v)) * np.cos(u)
    y = (R + r * np.cos(v)) * np.sin(u)
    z = r * np.sin(v)
    return np.stack([x, y, z], axis=1).astype(np.float32)


def _cone(n: int, rng: np.random.Generator) -> np.ndarray:
    # apex at origin, base at z=1, base radius 1
    h = rng.uniform(0.0, 1.0, n)
    theta = rng.uniform(0.0, 2 * np.pi, n)
    radius = h
    x = radius * np.cos(theta)
    y = radius * np.sin(theta)
    z = h
    return np.stack([x, y, z], axis=1).astype(np.float32)


def _helix(n: int, rng: np.random.Generator, turns: int = 3) -> np.ndarray:
    t = rng.uniform(0.0, 2 * np.pi * turns, n)
    radius = 0.5
    x = radius * np.cos(t)
    y = radius * np.sin(t)
    z = (t / (2 * np.pi * turns)) * 2.0 - 1.0
    pts = np.stack([x, y, z], axis=1).astype(np.float32)
    pts += 0.02 * rng.standard_normal(pts.shape).astype(np.float32)
    return pts


_GENERATORS = [_sphere, _cube_surface, _torus, _cone, _helix]
N_CLASSES = 5
N_POINTS = 64


def make_split(num_per_class: int, seed: int = 42, n_points: int = N_POINTS,
               rotate: bool = True) -> tuple[np.ndarray, np.ndarray]:
    """Return (X, y) with X.shape = (num_per_class*N_CLASSES, n_points, 3)."""
    rng = np.random.default_rng(seed)
    Xs, ys = [], []
    for cls, gen in enumerate(_GENERATORS):
        for _ in range(num_per_class):
            cloud = gen(n_points, rng)
            # Centre and unit-scale so different shapes are comparable
            cloud = cloud - cloud.mean(axis=0, keepdims=True)
            scale = np.linalg.norm(cloud, axis=1).max() + 1e-9
            cloud = cloud / scale
            if rotate:
                R = _random_rotation(rng)
                cloud = cloud @ R.T
            Xs.append(cloud)
            ys.append(cls)
    X = np.stack(Xs, axis=0)
    y = np.array(ys, dtype=np.int64)
    perm = rng.permutation(len(X))
    return X[perm], y[perm]


if __name__ == "__main__":
    X, y = make_split(num_per_class=20)
    print(f"Generated {len(X)} clouds, shape per cloud {X[0].shape}")
    print(f"Class counts: {np.bincount(y)}")

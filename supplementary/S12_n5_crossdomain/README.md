# S12 — N5 cross-domain leg-2 (non-physics, multi-block, independent SUTs)

Complements the single-block industrial corpus (S11) with two program families
**outside the block-construction set**, testing multi-block transferability and the
FA-rank-tight blocks (G, T*) out of domain. Programs under test are **real,
independent, non-author libraries** (numpy), strengthening anti-circularity.

| leg | domain | SUT | blocks populated | FA-rank tight | script |
|---|---|---|---|---|---|
| 2a | dense numerical linear algebra | `numpy.linalg` | G, T\*, O≤, L\*, E\*, Conservation (6) | G (S₄: 2 gens = 24 perms), T\* (kernel=symmetric 21) | `leg2_numlinalg.py` |
| 2b | digital signal processing | `numpy.fft` | G, T\*, Conservation, L\*, O≤, E\* (6) | G (Z₁₆ cyclic shift: 1 gen = 15 shifts, kernel=circulant 16) | `leg2_dsp.py` |

Every per-block algebra-derived MR is **executably confirmed** on the independent
library (`results/`). Contrast with S11 (industrial): 1 block (O≤). Together the two
legs give: expert-validated in-domain breadth (S11) + multi-block out-of-domain
structure with tight G/T\* blocks (S12).

Honesty: occupancy is descriptive (post-hoc instantiation), not a pre-registered
prediction; the SUTs are general-purpose libraries, so these confirm the framework's
derive-and-check loop transfers, not a competitive detection claim.

Run: `python3 leg2_numlinalg.py && python3 leg2_dsp.py`.

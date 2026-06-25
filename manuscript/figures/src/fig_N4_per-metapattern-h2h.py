"""Fig N4 — Per-MetaPattern head-to-head: Set N (algebra-derived) vs Set G (GP-evolved).

数据来源:NOETHER_paper_arxiv.tex,Table tab:per-block-headtohead(§4 subsec:pooled-headtohead)。
  G  (sym.) : N 2/11 = 0.182 [0.051,0.477] ; G 9/11 = 0.818 [0.523,0.949]
  L*        : N 10/24= 0.417 [0.245,0.612] ; G 16/24= 0.667 [0.467,0.820]
  G_tr      : N 10/17= 0.588 [0.360,0.784] ; G 8/17 = 0.471 [0.262,0.690]
全部取自论文自有表格(含 Wilson 95% CI),不引入任何额外数据点。
"""
import numpy as np
import figstyle
import matplotlib.pyplot as plt

figstyle.apply_style()

# --- 真实数据(论文 Table tab:per-block-headtohead)---
metapatterns = [r"$G$ (sym.)", r"$\mathcal{L}^{*}$", r"$G_{\mathrm{tr}}$"]
n_b   = [11, 24, 17]
N_rate = [0.182, 0.417, 0.588]
N_lo   = [0.051, 0.245, 0.360]
N_hi   = [0.477, 0.612, 0.784]
N_frac = ["2/11", "10/24", "10/17"]
G_rate = [0.818, 0.667, 0.471]
G_lo   = [0.523, 0.467, 0.262]
G_hi   = [0.949, 0.820, 0.690]
G_frac = ["9/11", "16/24", "8/17"]

x = np.arange(len(metapatterns))
w = 0.36

def err(rate, lo, hi):
    return np.array([[r - l for r, l in zip(rate, lo)],
                     [h - r for r, h in zip(rate, hi)]])

fig, ax = plt.subplots(figsize=(5.4, 3.0))
bN = ax.bar(x - w/2, N_rate, w, label="Set N (algebra-derived)",
            color="0.35", edgecolor="0.10", linewidth=0.5,
            yerr=err(N_rate, N_lo, N_hi), capsize=3,
            error_kw={"elinewidth": 0.9, "ecolor": "0.10"})
bG = ax.bar(x + w/2, G_rate, w, label="Set G (GP-evolved)",
            color="0.75", edgecolor="0.10", linewidth=0.5, hatch="///",
            yerr=err(G_rate, G_lo, G_hi), capsize=3,
            error_kw={"elinewidth": 0.9, "ecolor": "0.10"})

# kill/n 原始分数标在 CI 上端之上,避开误差棒须线(防文字与图形重叠)
for bar, frac, hi in zip(bN, N_frac, N_hi):
    ax.annotate(frac, xy=(bar.get_x() + bar.get_width()/2, hi),
                xytext=(0, 4), textcoords="offset points",
                ha="center", va="bottom", fontsize=7)
for bar, frac, hi in zip(bG, G_frac, G_hi):
    ax.annotate(frac, xy=(bar.get_x() + bar.get_width()/2, hi),
                xytext=(0, 4), textcoords="offset points",
                ha="center", va="bottom", fontsize=7)

ax.set_xticks(x)
ax.set_xticklabels([f"{m}\n$n_b={n}$" for m, n in zip(metapatterns, n_b)])
ax.set_ylabel("PIT mutant kill rate")
ax.set_ylim(0, 1.05)
ax.grid(axis="x", visible=False)
ax.legend(loc="upper center", ncol=2, bbox_to_anchor=(0.5, 1.16))

outdir, name, dpi = figstyle.output_target("fig_N4_per-metapattern-h2h")
figstyle.save_figure(fig, name, outdir, dpi=dpi)

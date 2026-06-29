"""Fig N3 — L*-MetaPattern blindness: per-SUT L_scale kill rate vs the 1/3 falsification threshold.

数据来源:NOETHER_paper_arxiv.tex,Table tab:l-blindness(§4 Central result, subsec:l-blindness-confirmed)。
  midpoint 0/3, clamp 0/7, signum 0/6, gcdSig 0/9, lcmSig 0/11, hypotSig 2/4。
  pooled 2/44 ≈ 4.5%。全部取自论文自有表格,不引入任何额外数据点。
"""
import figstyle
import matplotlib.pyplot as plt

figstyle.apply_style()

# --- 真实数据(论文 Table tab:l-blindness)---
suts   = ["midpoint", "clamp", "signum", "gcdSig", "lcmSig", "hypotSig"]
kills  = [0, 0, 0, 0, 0, 2]
totals = [3, 7, 6, 9, 11, 4]
rates  = [k / n for k, n in zip(kills, totals)]
THRESHOLD = 1.0 / 3.0   # per-SUT falsification threshold (1/3)

fig, ax = plt.subplots(figsize=(5.2, 2.8))
# 离群 SUT 用更深灰区分,其余统一浅灰(黑白打印可辨)
colors = ["0.55" if k == 0 else "0.25" for k in kills]
bars = ax.bar(suts, rates, color=colors, width=0.62, edgecolor="0.15", linewidth=0.5)

# 证伪阈值参照线;标签放左侧零柱区,避开右端 hypotSig 柱
ax.axhline(THRESHOLD, ls="--", lw=1.0, color="0.10")
ax.text(2.0, THRESHOLD + 0.02,
        "per-SUT falsification threshold (1/3)",
        ha="center", va="bottom", fontsize=7.5)

# 柱顶标注 kill / mutants 原始分数
for bar, k, n in zip(bars, kills, totals):
    ax.annotate(f"{k}/{n}",
                xy=(bar.get_x() + bar.get_width() / 2, bar.get_height()),
                xytext=(0, 3), textcoords="offset points",
                ha="center", va="bottom", fontsize=7.5)

ax.set_ylabel(r"$L_{\mathrm{scale}}$ MR kill rate")
ax.set_xlabel("System under test ($\\mathcal{L}^{*}$-admitting)")
ax.set_ylim(0, 0.6)
ax.grid(axis="x", visible=False)
# pooled 注记
ax.text(0.02, 0.95, r"pooled $2/44 \approx 4.5\%$",
        transform=ax.transAxes, ha="left", va="top", fontsize=8)

outdir, name, dpi = figstyle.output_target("fig_N3_l-blindness")
figstyle.save_figure(fig, name, outdir, dpi=dpi)

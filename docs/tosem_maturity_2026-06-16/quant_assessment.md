# NOETHER — TOSEM 投稿成熟度量化考核(网关多厂商)

> 日期:2026-06-16 · 评估对象:**修复后**论文(differentiation/overclaim/threats 已改) · 方法:经 `.env` 网关用 5 个厂商模型(gpt-5-chat / deepseek-v3.2 / grok-4.1 / qwen3-max / kimi-k2.5)按 TOSEM 作者指南 + 接收门槛做 rubric 量化打分(9 维度 0–10 + 加权)。原始:`gateway_quant_raw.json`。

## 总分(每模型)

| 模型 | 厂商 | 成熟度/100 | TOSEM 门槛 | 差距 | verdict |
|---|---|---|---|---|---|
| gpt-5-chat-latest | OpenAI | 67 | 75 | 8 | Major |
| deepseek-v3.2-exp | DeepSeek | 65 | 75 | 10 | Major |
| qwen3-max-preview | 阿里 | 63 | 85 | 22 | Major |
| grok-4.1 | xAI | 58 | 78 | 20 | Major |
| kimi-k2.5 | Moonshot | 56 | 75 | 19 | Major |

**均值:成熟度 ≈ 62/100,TOSEM 接收门槛 ≈ 78/100,差距 ≈ 16 分。5/5 全 Major Revision。**
(对比修复前多厂商:32–58 分 + 2 Reject → 修复后 56–67 分 + 0 Reject;文本修复使 verdict 回升,但实质 blocker 仍在。)

## 维度量化(0–10,5 模型均值)

| 维度 | 权重 | 均分 | range | 状态 |
|---|---|---|---|---|
| format_compliance | 0.05 | 8.8 | [8,9] | ✅ 达标 |
| honesty_threats | 0.10 | 7.8 | [6,10] | ✅ 达标(修复见效) |
| scope_fit | 0.05 | 7.6 | [7,8] | ✅ 达标 |
| novelty | 0.15 | 7.4 | [6,9] | ✅ 达标 |
| technical_soundness | 0.20 | 6.8 | [6,8] | ◐ 中等 |
| reproducibility | 0.10 | 6.8 | [6,9] | ◐ 中等 |
| evaluation_rigor | **0.20** | **4.6** | [4,5] | 🔴 gap(权重最高) |
| presentation_length | 0.05 | 4.4 | [3,6] | 🔴 gap |
| related_work | 0.10 | 3.6 | [3,4] | 🔴 gap(最低) |

## 三大共识 gap(5/5 模型一致)

1. **evaluation_rigor 4.6**(权重 0.20,最重):只 1/3 域有执行的 head-to-head;baseline 实际胜出(p=0.0043);ML 仅 n=20+5 pilot;relational 仅 analytical;METRIC+/MR-Scout/第三厂商比较未执行。→ **需真实实验**(`protocol_realDefect.md`)。
2. **related_work 3.6**(最低):~4 行太薄,differentiation 段已加但广度仍不足。→ **文本可修**(`protocol_relatedWork.md` 候选文献)。
3. **presentation_length 4.4**:73pp 远超 TOSEM 30–50 推荐,贡献密度不匹配。→ **文本可修**(压缩 + cover letter 辩护)。

## 到接收门槛的量化路径

| 改进 | 类型 | 预估增益 |
|---|---|---|
| related_work 3.6 → 7(扩文献+定位矩阵) | 文本(高 ROI) | ≈ +3.4 分(权重 0.10) |
| presentation_length 4.4 → 7(压至 ≤50pp) | 文本(高 ROI) | ≈ +1.3 分(权重 0.05) |
| evaluation_rigor 4.6 → 7(中立真缺陷正面证据+执行 SOTA 比较) | 研究(硬骨头) | ≈ +4.8 分(权重 0.20) |
| technical_soundness 6.8 → 8(补非平凡定理/重定位) | 研究 | ≈ +2.4 分(权重 0.20) |

**预估**:仅做两项文本修复(related_work + length)→ 成熟度 ≈ 62 → 67(仍 Major);叠加 evaluation 实验 → ≈ 72–74;再加理论强化 → ≈ 76–78,逼近门槛。**结论:无真实实验(evaluation_rigor)与理论强化,纯文本修复无法达到 TOSEM 接收线。**

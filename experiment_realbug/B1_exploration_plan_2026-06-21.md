# B1 真缺陷 MT 系统化探索计划 (2026-06-21)

> 作者授权自主执行。核心:**有计划、有组织、有验收标准的自动化探索**。重点 = 真实缺陷 + 元模式广度。
> 前序教训(本会话):检索代理候选 SHA 仅 ~2/5 准、cat 易误判(#6037)、issue snippet 常过时(#6110/#6241/#6299)。
> **本计划改用 git-history fix+test 扫描**:test 一定可跑、SHA 从 git log 真实取得、cat 复现核验。

## 0. 验收标准(每个样本须全满足才计 in-scope 正样本)

1. **真实 fix commit**:parent + fix SHA 从仓库 `git log` 真实取得(非臆造、非检索代理转述)。
2. **CPU 可复现**:checkout parent 跑该 fix 的回归测试 → FAIL(缺陷确认);checkout fix 跑 → PASS。
3. **cat 复现核验**:判定违反哪类不变性,**必须复现后确认**(非凭标签;#6037 教训:标 cat-iii 实为 out)。
4. **元模式 MR 识别**:从既有 5 元模式 + baseline 识别对应 MR,**不造新 MR**(映射不到 → out 如实记)。
5. **MT 执行**:MR fired on pre-fix + held on post-fix(**FP-gate pass**)。
6. **记录**:bug_json + analyze 汇总。

## 1. 目标仓库 + 元模式覆盖矩阵(广度优先)

| 仓库 | env-class | 目标元模式 | 对应 MR |
|---|---|---|---|
| e3nn/e3nn | C (py3.9+torch1.10+e3nn0.3.5) | SO(3) 旋转等变 + 自伴 TP | rho_rot, rho_adj |
| pyg | B (py3.10+torch1.13+pyg2.2) | Sₙ 置换 + 聚合单调/幂等 | rho_perm, rho_mono |
| pytorch (torch) | A (py3.11+torch2.12) | 推理确定性/纯度 | rho_train_inf |

备选:escnn(等变)、scipy.spatial.transform(旋转)。

## 2. 自动化探索方法(可靠,不依赖 issue snippet)

```
for repo in [e3nn, pyg, torch]:
  1. clone git history
  2. 找 test-变更的 fix commit:
     git log --all --oneline -- <test_dir>   # test 文件变更历史
     筛 message 含 fix/bug/incorrect/wrong 的 commit
  3. for each fix commit C (parent P):
     a. checkout P, 跑 C 引入/修改的 test  -> 期望 FAIL (缺陷复现)
     b. checkout C, 跑同 test               -> 期望 PASS (修复确认)
     c. 若 (a)FAIL ∧ (b)PASS  => 真实可复现缺陷,进入 cat 判定
  4. 判 cat(复现核验)-> 映射元模式 MR -> 写 ctx adapter -> run MT
  5. 记 bug_<repo>_<n>.json + 更新进度表
```

## 3. 元模式覆盖目标(验收:每元模式 ≥1 in-scope 正样本)

| 元模式 | MR | 当前 | 目标来源 |
|---|---|---|---|
| m^eq_inv (Sₙ 置换) | rho_perm | ✓ #6199 | pyg |
| m^eq_inv (SO(3) 旋转) | rho_rot | — | e3nn |
| m^eq_adj (自伴) | rho_adj | — | e3nn TP |
| m^eq_mono (单调/幂等) | rho_mono | — | pyg 聚合 |
| m^eq_conv/rev (确定性) | rho_train_inf | — | torch / pyg |

## 4. 进度跟踪(执行中持续更新)

| 仓库 | 元模式 | fix commit | 复现(P fail/C pass) | cat | MR | MT(pre/post) | 状态 |
|---|---|---|---|---|---|---|---|
| pyg | Sₙ 置换 | 25abbb15←bc47556f | ✓/✓ | cat-ii | rho_perm | fired/held | ✓ in-scope (#6199) |
| e3nn | role-swap 反对称 | f7f35fb←3ddce1f | ✓/✓ | m^eq_adj 族 parity-(-1) | role-swap antisym | fired/held | ✓ in-scope (ReducedTensorProducts) |
| pyg | 行和守恒 | #6037 | ✓/— | out-of-decomp | — | — | out (元模式外) |
| pyg | 索引/排序/聚合 | #6110/#6241/#6299 | ✗ | — | — | — | BLOCKED (SHA/API/snippet 不准) |

**env-class 栈关键修正**:env-class-C 正确栈 = **torch1.8.1 + e3nn0.2.7**(非 torch1.10)。e3nn0.2.7 的 fx codegen 需 torch1.8.x fx API:torch1.9→`PythonCode.replace` 报错,torch1.10→multiple-tracers。这也解释并解决了早先 #296 的 "multiple tracers" INFEASIBLE(实为 torch 版本不匹配)。

## 5. 诚实约束(贯穿)

- cat 必须复现核验(#6037 教训)。
- 不造 MR;out-of-decomposition 如实单列(不混入 detection 分母)。
- n、underpowered(C6)、coverage 如实报;descriptive vs confirmatory 明确区分。
- 每个 fix commit 的 parent/fix SHA 可被第三方 `git log` 复核。

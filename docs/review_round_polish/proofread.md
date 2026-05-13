# Proofread report (ACM TOSEM polish round 2)

Target: `NOETHER_paper.tex` (2697 lines, 8 sections + 7 appendices).
Mode: read-only audit; no files were modified.

## Severity legend
- **P0** = MUST fix before submission (data inconsistency, broken cross-ref, factually wrong, pre-registered hypothesis verdict missing)
- **P1** = should fix (grammar, spelling, style consistency, sloppy hand-coded ref)
- **P2** = nice-to-have (sentence-level rephrasing for readability)

## Executive summary

The paper is internally consistent at the level of the §6.6 head-to-head numerics
once the reader trusts the `\S\ref{subsec:pooled-headtohead}` and
`\S\ref{subsec:pit-block-matrix}` paragraphs. However, the prose that re-summarises
those numerics inside §6.6 itself (lines 1789, 1811-1815, 1858-1860, 2077-2078)
collides with the post-eq-exclusion bookkeeping (D1 n = 52, D2 n = 5,
McNemar D1-only p = 0.019, pooled p = 0.0043). Six sites repeat outdated or
mis-typed counts (n = 2, n = 7, p = 0.0043 attached to D1-only). These are
the load-bearing P0 fixes.

A second P0 cluster is in Appendix B: it claims to document the **12** representative
MRs of Table~\ref{tab:elementwise} but lists **13** items (i)-(xiii); item (iii) (reflective-boundary symmetry) has no corresponding row in Table~3.

A third P0 is the missing H3a verdict: H3a is pre-registered (Set~N within
$\Delta = 0.10$ of Set~G on D1), the observed gap is $0.500$ vs $0.712 = 0.212$
(more than 2× the threshold), but no PASS/FAIL annotation is given. The
paper merely describes the gap in prose.

British spelling is uniformly applied (`generalisation`, `behaviour`,
`modelling`, `practice`, `analyse`, `catalogue`, ...); no American spellings
in the body. Em-dash (U+2014) count is **zero**. AI-cliché residue is
**zero** at the level of "delve / crucial / pivotal / showcase / tapestry / leverage".
C1, C2, C3 anti-pattern checklist hits are **zero** (no `v1.0`, no `R1 adds`, no
"round-N", no "first/second adversarial", no "we encountered", no "after submission").
C6 (underpowered) is consistently labelled at the four pilots ($n \le 10$).

All `\ref` / `\nameref` / `\eqref` targets resolve to declared labels
(75 unique refs, 97 unique labels, zero dangling).

## Findings

### §1 Introduction (lines 111–158)

| line | severity | finding | suggested fix |
|---|---|---|---|
| 134 | P1 | Contributions C2 references `Theorem~1` and `Theorem~2` hand-coded instead of `\ref{thm:closure}` / `\ref{thm:decidable}` | Use `\ref{}`. Alternatively, accept as intentional summary text (then keep). |
| 134 | P2 | "the count to ten pairwise-independent" — verb tense slightly awkward ("bringing the count..."); consider "raising the count to..." for clarity. | Minor rephrase. |
| 151 | P2 | "$\S\ref{subsec:third-domain}$, companion artefacts in `theory/`" – the in-text reference to a folder name should be either fully removed from the manuscript or annotated as supplementary path (`supplementary~S2`). The text mixes "companion artefacts" with bare folder names elsewhere too (lines 134, 827). | Either rename to `supplementary material S2 (\texttt{theory/})` everywhere, or drop the in-text folder names. |

### §2 Background and related work (lines 161–197)

No findings.

### §3 Operator-algebraic preliminaries (lines 199–311)

| line | severity | finding | suggested fix |
|---|---|---|---|
| 302 | P1 | `§\ref{subsec:case-study}` uses §-prefix; elsewhere this is consistent. Just confirming. | none. |
| 310 | P1 | `Remark~\ref{rem:metric-stability-block}` "We do not commit to $M_{\mathrm{lip}}$... we record it in Appendix~\ref{app:out-of-scope} as the most concrete sub-instance of Remark~\ref{rem:counterex} item~(iv) (topological invariants)" — but item~(iv) in Remark~\ref{rem:counterex} is actually "Topological invariants". And $M_{\mathrm{lip}}$ (metric-stability) is described at Remark~\ref{rem:metric-stability-block} as a candidate **ninth block**, while line 305 says it is the "metric-stability $M_{\mathrm{lip}}$" sub-instance. The pairing of metric-stability with "topological invariants" item (iv) is a stretch (metric vs. homological). | Either (a) clarify that $M_{\mathrm{lip}}$ is a separate ninth-block candidate that is *related to* but not subsumed under item (iv); or (b) renumber item (iv) to a "metric / topological / homological" combined entry. |

### §4 The NOETHER framework (lines 314–443)

| line | severity | finding | suggested fix |
|---|---|---|---|
| 398 | P1 | Theorem 2 statement: "Suppose $\mathcal{A}_P$ admits a finite generating set $\mathrm{gen}(\mathcal{A}_P)$ of cardinality $n$" — slight name collision: $n$ is also used elsewhere as a sample size. Consider renaming to $|\mathrm{gen}|$ or $g$. | Minor; keep if rewrite cost > benefit. |
| 405–428 | P1 | Table~\ref{tab:complexity}: the $\mathcal{B}^{*}_{\mathrm{rel}}$ row is absent. The table claims to cover "each block" but only lists 7 of 8 (G, $O_{\le}$, $T^*$, $\mathcal{T}^*$, $\mathcal{L}^*$, $\mathcal{D}^*$, $\mathcal{E}^*$). Theorem 2's polynomial-time bound for $\mathcal{B}^{*}_{\mathrm{rel}}$ is discussed in Remark~\ref{rem:decidable-brel}, but missing the row in Table 6 (algebra-rich-pooled). | Add the $\mathcal{B}^{*}_{\mathrm{rel}}$ row to Table~\ref{tab:complexity} with a `$O(|\mathcal{R}_{\mathrm{rel}}|)$` entry, or note in caption that this row is consolidated in Remark~\ref{rem:decidable-brel}. |

### §5 Boltzmann instantiation (lines 445–550)

| line | severity | finding | suggested fix |
|---|---|---|---|
| 463 | P1 | "seven MetaPatterns" — consistent with the explicit list ($m_{\mathrm{inv}}$, $m_{\mathrm{mono}}$, $m_{\mathrm{adj}}$, $m_{\mathrm{rev}}$, $m_{\mathrm{conv}}$, $m_{\mathrm{dyn}}$, $m_{\mathrm{cmp}}$). However, the eight-block decomposition has the 8th block ($\mathcal{B}^{*}_{\mathrm{rel}}$) empty for Boltz — sentence implicitly assumes 8 blocks elsewhere. Recommend stating "seven (the eighth block $\mathcal{B}^{*}_{\mathrm{rel}}$ is empty under $\mathcal{A}_{\mathrm{Boltz}}$)". | Optional clarification. |
| 484-485 | P1 | Table~\ref{tab:refinement} marks $m_{\mathrm{adj}}$ and $m_{\mathrm{rev}}$ as "Predicted" — but §5.3 paragraph (lines 494-495) explicitly retracts the strong "prediction" reading. Consider using **\emph{Re-classified}** or **\emph{Surfaced}** in the table to match the prose. | Renaming the column "Predicted" → "Re-classified" maintains consistency between table and caveat. |

### §6 Cross-domain demonstration: equivariant ML (lines 553–828)

| line | severity | finding | suggested fix |
|---|---|---|---|
| 660 | P1 | "five MRs, one per non-empty MetaPattern of $\mathbb{M}(\mathcal{A}_{\mathrm{equi}})$" — coverage status earlier (line 607) says "three of the five non-empty MetaPatterns of $\mathbb{M}(\mathcal{A}_{\mathrm{equi}})$" populated by $\rho_{\mathrm{rot}}, \rho_{\mathrm{perm}}, \rho_{\mathrm{train}}$. The "five non-empty" implies $\mathcal{D}^{*} = \emptyset$ and $\mathcal{E}^{*} = \emptyset$ within a single architecture, leaving 5 blocks. Confirmed consistent. | none |
| 689 | P1 | Case-study results paragraph: detection numerator on $\rho_{\mathrm{adj}}$ uses the CI-time formulation. Caption (line 693-694) reinforces this. Reader needs to track: do the n=20 mutations include any that exercise $T^{*}$? Recommend a single line clarifying that none of cats (i)-(iv) directly targets $T^{*}$ (which is why $\rho_{\mathrm{adj}}$ kills 0 mutants). | Add: "$\rho_{\mathrm{adj}}$ is non-firing on cats (i)-(iv) by construction; the mutation set does not contain a $T^{*}$-block-disrupting category." |
| 713 | P2 | "Set L (only $G$ and $\mathcal{L}^*$..., $0.40 = 2/5$)" and "Set B ($0.20 = 1/5$)" — the $k/5$ explicit fraction would help readers verify the coverage. | Minor. |
| 728 | P1 | Pre-registered "If H1 fails": rule says "one of the derivations is incorrect and must be revised". The paper then says (line 712) H1 is "retained as a structural sanity check rather than as a falsifiable hypothesis test". This is a soft retraction of the pre-registration; document the change of plan or remove the H1 falsification rule. | Either explicitly say "H1 is downgraded from falsifiable hypothesis to structural diagnostic (rationale: by construction of CONSTRUCT-MP, H1 is a sanity check, not a test)" or restore the original falsification commitment. |
| 755 | P1 | DeepCrime pilot paragraph: "the framework's $\mathcal{L}^*$-block prediction is non-vacuous on a fault distribution it was not designed against" — this is a stretch since cat-v-01 (head weight scaling) was hand-selected. The paragraph itself acknowledges "$n=5$, underpowered" later, but the "designed against" claim is borderline; recommend softening to "a fault distribution that was not curated to exercise $\mathcal{L}^*$ by construction." | Minor rephrase for honesty. |

### §6.5 Negative instantiation on $\mathcal{A}_{\mathrm{PWR}}$ (lines 830–989)

No P0/P1 findings; the proofs in C.6 are airtight against `\texttt{Translate}` Table 14 templates.

| line | severity | finding | suggested fix |
|---|---|---|---|
| 870 | P2 | "Equivalently, in conventional reactor-physics notation..." — the equation $\rho = 1 - 1/k_{\mathrm{eff}}$ uses the same symbol $\rho$ as the MR-name prefix (e.g. $\rho_{\mathrm{nonadd}}$). Two meanings of $\rho$ within a single subsection. | Optional rename $\rho_{\mathrm{static}}$ → $\rho^{\mathrm{rx}}_{\mathrm{static}}$ throughout C.6, or note collision in Def. 19. |

### §6.6 Empirical test of the eight-block decomposition (lines 991–2089)

| line | severity | finding | suggested fix |
|---|---|---|---|
| **1789** | **P0** | **"post-exclusion D2 stratum ($n = 2$) governs the framework prediction above"** — should be **$n = 5$**. All other §6.6.2/§6.6.3 paragraphs consistently use $n = 5$ for the post-eq D2 stratum (1205-1207, 1684, 1690, 2029, 2030). | Change `n = 2` → `n = 5`. |
| **1811–1812** | **P0** | **"the exact McNemar two-sided test on the D1 stratum yields $p = 0.0043$"** — but earlier the D1-only McNemar gives **$p = 0.019$** (line 1219, 1673). $p = 0.0043$ is the **pooled** (D1 ∪ D2 post-eq, n = 57) figure. Critical: D1-only and pooled have the same point estimate $-14$ but different McNemar tables and different $p$. | Change to "exact McNemar two-sided test on the D1 stratum yields $p = 0.019$ (D1-only); the pooled D1+D2 McNemar (n = 57) yields $p = 0.0043$." |
| **1815** | **P0** | **"Set~N kill rate on the algebra-preserving stratum is $0/7$"** — should be **$0/5$**. The "$0/7$" figure refers to the $G$-block stratum on `gcdSig`+`lcmSig` (Table~\ref{tab:per-block-headtohead}), not the post-eq D2 stratum. Conflation. | Change `0/7` → `0/5` here. |
| **1858–1860** | **P0** | **"two paired hypothesis tests reported on this substrate are the scope-matched D1 McNemar ($p = 0.0043$ at the 30-min budget, exact two-sided) and its auxiliary pooled counterpart ($p = 0.0043$ identically, since the $7$ D2 mutants are concordant ``both miss''..."** — three errors: (a) D1 McNemar p is $0.019$ not $0.0043$; (b) D2 stratum is $n = 5$ not $n = 7$; (c) on the D2 stratum Set G kills $3/5$ (not "both miss"). The "identically" claim therefore fails: D1 McNemar discordants $(b,c) = (15,4)$ → $p = 0.019$; pooled adds 3 more $b$ discordants from D2 → $(18,4)$ → $p = 0.0043$. The pooled p is **strengthened** by D2 inclusion, as line 1716 already correctly states. | Rewrite: "two paired hypothesis tests reported on this substrate are the scope-matched D1 McNemar ($p = 0.019$ at the 30-min budget, exact two-sided) and the auxiliary pooled D1+D2 counterpart ($p = 0.0043$); the pooled p is strengthened by including the D2 stratum because Set~G's $3/5$ kills on D2 add three $b$-cell discordances." |
| **2076–2078** | **P0** | **"Set~N $0/7$ on `gcdSig`~+~`lcmSig`). The framework's falsifiable D2 prediction ($\mathrm{kill\;rate} \le 10\%$) holds (Set~N $= 0/7$)"** — second `0/7` refers to D2 stratum; should be **$0/5$**. The first `0/7` is correctly the $G$-block-on-Euclidean stratum, but the second `0/7` conflates with that. | Change second `Set~N $= 0/7$` → `Set~N $= 0/5$`. |
| **771, 1655** | **P0** | **H3a verdict missing.** H3a pre-registers "Set~N within $\Delta = 0.10$ of Set~G on D1". Observed: Set~N D1 = 0.500 vs Set~G D1 = 0.712, gap = 0.212 (more than 2× $\Delta$). The paper acknowledges the gap in prose ("We do not claim Set~N $>$ Set~G", line 1809-1810; "Set~G is the stronger fault-detector within the D1 scope-matched subset", line 1816) but never says "H3a fails / does not pass" against its own pre-registered threshold. This is the kind of selective verdict that the C4 / R&R checklist explicitly forbids. | Add explicit line in §6.6.2: "**H3a verdict: not supported on the present substrate.** Observed D1 gap (0.500 vs 0.712 = 0.212) exceeds the pre-registered $\Delta = 0.10$ threshold by 2.1×; we report this transparently rather than retroactively widening $\Delta$." |
| 1163–1166 | P1 | "On the $n = 62$ head-to-head substrate, the per-mutant D1/D2 labelling has been carried out and is reported in the subsequent paragraphs; the $\mathcal{L}^{*}$-blindness result of \S\ref{subsec:l-blindness-confirmed} is the corresponding D2-cell specialisation on the wider 23-SUT substrate." — the "23-SUT substrate" is the broader utility-method baseline mentioned at line 1799-1801. But the central $\mathcal{L}^{*}$-blindness test of §6.6.5 is on **6 SUTs**, $n = 44$ mutants, not 23 SUTs. Cross-reference confusion. | Either clarify "23-SUT utility-method baseline" vs "6-SUT $\mathcal{L}^{*}$-admitting subset", or drop the "23-SUT" qualifier. |
| 1170 | P1 | "$22$ are killed by both Set~N and Set~G, $4$ are killed by Set~N only, $18$ are killed by Set~G only, and $18$ are killed by neither" — sum = 22+4+18+18 = 62 ✓; but line 1553 says Set~N pooled = 26 and Set~G pooled = 40. From the partition: Set~N kills = 22+4 = 26 ✓; Set~G kills = 22+18 = 40 ✓. Self-consistent. (No change.) | none. |
| 1173 | P1 | "G-only kills constitute a candidate scope-mismatch pool" — but the per-mutant D1/D2 split at line 1194-1206 says Set~G kills 3 of the 5 D2 mutants. So Set~G's 18 "G-only kills" are a mix of D1 mutants Set~N missed and D2 mutants Set~G incidentally hit (3). The text reads as if all 18 G-only kills are scope-mismatched, which over-simplifies. | Replace with: "The 18 G-only kills decompose into 15 D1 mutants Set~N missed within its scope and 3 D2 mutants Set~G hit through input-domain edge cases (line 1206)." |
| 1188 | P1 | "`configs/sut\_block\_decomposition.json` + `configs/sut\_block\_overrides.json` of the companion experiment repository" — concrete file paths in prose. Acceptable in a TOSEM artifact-evaluation paper, but harden by giving SHA-256 / Zenodo deposit cross-reference. | Optional. |
| 1219 | P1 | "exact McNemar two-sided $p = 0.019$" — correctly states D1-only. | none. |
| 1597 | P1 | Table~\ref{tab:per-block-headtohead} per-block Set~N kills sum = 2+10+10 = 22, but D1 aggregate row says 26. The 4-kill gap is in the 25 "unmapped" mutants (line 1602) where per-block strata don't apply. The caption clarifies this as "lower-bound caveat", but the prose at line 1226 says "the per-block decomposition is the appropriate substrate-level reading; the aggregate is reported as a cross-block summary" without acknowledging the 4-kill gap. | Add a footnote to Table~\ref{tab:per-block-headtohead}: "Per-block kill counts sum to 22 (Set~N) / 33 (Set~G); the aggregate D1 row's 26 (Set~N) / 37 (Set~G) includes 4 additional kills on the 25 unmapped mutants whose broken blocks are not localised in the override file." |
| 1641 | P1 | "$\mathcal{T}^{*}$ block: Set~N edge (underpowered)" — underpowered is well-flagged. But the rate "$0.588$" should be cross-checked: Set~N $10/17 = 0.588$ ✓. CI $[0.360, 0.784]$: Wilson 95% for 10/17 ≈ $[0.366, 0.776]$ — slight rounding difference; verify. | Verify against generating script. |
| 1670–1674 | P1 | Aggregate D1: "$\mathrm{M1}_{\mathrm{D1}} = 26/52 = 0.500$ (Wilson 95\% CI $[0.369,\,0.631]$)" — Wilson 95% for 26/52 ≈ $[0.367, 0.633]$; match to within rounding. ✓ | none. |
| 1702–1707 | P1 | "$n = 57$" auxiliary pooled M1: "Set~N $= 26/57 = 0.456$ (Wilson 95\% CI $[0.334,\,0.584]$)" — Wilson for 26/57 ≈ $[0.331, 0.585]$ ✓. | none. |
| 1763 | P1 | Equivalent-mutant footnote header: "Footnote on equivalent-mutant denominator (resolved)" — fine, but the `\paragraph{...}\label{para:eq-mutant-footnote}` combination is then `\pageref`'d in three places; verify each `\pageref` resolves to the same page in the compiled PDF. | Compile check. |
| 1815 | P0 | (already counted above) | (already noted) |
| 2024 | P1 | (b.cm) row of Table 13 (future-work): "$\mathcal{L}^{*}$ block $n = 0$ under Table~\ref{tab:pit-block} reconstruction (parallel to (e.4)'s per-(SUT, mutator) override-authoring limitation)" — the parenthetical reference to (e.4) is forward-looking; clarify that (e.4) explains a *different* limitation than the (b.cm) $\mathcal{L}^*$-block-$n=0$ phenomenon. | Either drop the parenthetical "parallel to (e.4)..." or change to "(see also (e.4)'s authoring limitation, which is structurally distinct)". |
| 2027 | P1 | (d.set-l) row of Table 13: the 100-sample / 487-MR / 212-translatable / 34/70 numbers are repeated verbatim from §6.6.4's Set~L paragraph (line 1729-1746). Single source of truth recommended. | Either keep table row minimal ("see §6.6.4 Set~L paragraph") or keep §6.6.4 minimal ("see Table~\ref{tab:future-work} (d.set-l)"). |

### §7 Discussion (lines 2091–2184)

| line | severity | finding | suggested fix |
|---|---|---|---|
| 2098 | P1 | "five independent extensions of \texttt{Translate}'s signature" — earlier (line 134) says "five pairwise-independent structural obstructions" and "ten pairwise-independent \texttt{Translate}-extension dimensions across the three algebras". The discussion paragraph uses "five" for the PWR-only count, consistent with §6.5. ✓ | none. |
| 2100 | P1 | LRCA paragraph: Cohen's $\kappa$ $0.927$--$0.929$ on $n = 34$--$35$; majority-vote $\kappa = 0.931$ on $n = 36$; Fleiss' $\kappa = 1.000$ on $n = 33$. Internally consistent with `feedback_setn_scope_matched_comparison.md` precedent. ✓ | none. |
| 2102 | P1 | External validity paragraph: "the per-block $G$ kill rate is $6/21 = 28.6\%$ with Wilson 95\% CI $[13.8\%, 50.0\%]$" — for $6/21$, Wilson 95% ≈ $[0.137, 0.498]$ ≈ $[13.7\%, 49.8\%]$ ✓. "D2 stratum prediction passes at $2/29 = 6.9\%$" — within $\le 10\%$ ✓. "$\mathcal{L}^{*}$ block carries $n = 0$" — explained correctly. | none. |
| 2128 | P1 | "$\mathbb{M}(\mathcal{A}_{\mathrm{FFN}}) \subseteq \{m_{\mathrm{stab}}\}$ where $m_{\mathrm{stab}}$ is the stability MetaPattern" — $m_{\mathrm{stab}}$ is introduced as a new MetaPattern name not in the eight-block canonical labels ($m_{\mathrm{inv}}$, $m_{\mathrm{mono}}$, ...). Confirm $m_{\mathrm{stab}}$ is an alias for $m_{\mathrm{mono}}$ or $m_{\mathrm{conv}}$, not a ninth pattern. | Add: "$m_{\mathrm{stab}}$ is the $O_{\le}$-derived (or $\mathcal{L}^{*}$-derived) stability MetaPattern within the eight-block decomposition." |
| 2189 | P1 | Conclusion: "Theorem~2 ensures the construction is computable" — should be `\ref{thm:decidable}` for consistency, since "Theorem 2" is hand-coded. | Same convention as §1: either keep summary-mode names or use refs uniformly. |

### Appendix A (lines 2205–2285)

| line | severity | finding | suggested fix |
|---|---|---|---|
| 2212 | P1 | "$\mathbb{M}(\mathcal{A}_{\mathrm{heat}}) = \{m_{\mathrm{inv}},m_{\mathrm{mono}},m_{\mathrm{adj}},m_{\mathrm{conv}}\}$, four MetaPatterns, with $m_{\mathrm{rev}}$ correctly absent" — but $\mathcal{D}^*$ (qualitative-dynamics) is mentioned at line 2212 as present in $\mathcal{A}_{\mathrm{heat}}$. Is $m_{\mathrm{dyn}}$ included or not? The list shows 4 MetaPatterns but the algebra has 5 non-empty blocks. | Either add $m_{\mathrm{dyn}}$ to the set, or document why it is contracted. |

### Appendix B — Per-MR source provenance (lines 2288–2335)

| line | severity | finding | suggested fix |
|---|---|---|---|
| **2288–2335** | **P0** | **Appendix B is titled "Per-MR source provenance for the 12 representative MRs of Table~\ref{tab:elementwise}" but lists 13 items (i)-(xiii).** Item (iii) "Reflective-boundary symmetry" is documented in Appendix B but has no corresponding row in Table~\ref{tab:elementwise} (Table 3 has 12 rows: Bur-Phy-01, Bol-Phy-02, Bol-Phy-11, Bol-Phy-12, Dif-Alg-01, Bur-Alg-01, Bur-Phy-08, Cpl-App-06, Bur-Alg-04, Bol-Alg-04, two predicted = 12 entries). | Either (a) drop Appendix B item (iii) (reflective-boundary symmetry), keeping Appendix B at 12 items; or (b) add a reflective-boundary row to Table 3 and update the count to 13. Note: §5.3 paragraph (line 496) says "12 representative MRs" and protocol items (i)-(iv); item (iii) of the protocol is "where a block contains MRs from two distinct sub-categories...". The 12-vs-13 discrepancy is real. |

### Appendix C — Proofs (lines 2345–2598)

| line | severity | finding | suggested fix |
|---|---|---|---|
| 2358 | P1 | `\subsection*{Per-block instantiations of \texttt{Translate}}` is `\subsection*` (un-numbered); the cross-referenced `\label{app:translate-table}` is just before the table, not the subsection title. `\ref{app:translate-table}` works because the table itself is numbered. ✓ | none. |
| 2417 | P1 | "the single orphan localises to the metric-stability class discussed in **Appendix~\ref{rem:metric-stability-block}** and Appendix~C.5.2" — `rem:metric-stability-block` is a Remark **inside §3.2** (line 309), not an appendix. The compiled output will read "Appendix~3" or similar, which is wrong. | Change to "Remark~\ref{rem:metric-stability-block} (in §3.2)" or simply drop the "Appendix~" prefix. |
| 2417 | P1 | "Section~C.5 below documents three concrete classes" — Section C.5 is in *this* appendix, not "below"; the C.5 sub-paragraph follows immediately. | Change "Section~C.5 below" → "Section~C.5 (immediately following)" or just "Below". |
| 2425 | P1 | C.5.1 paragraph: "the Shannon entropy $H(f(\mathbf{x}))$" uses Roman $H$ for entropy; the diffusion operator $H_X$ in C.6 also uses Roman $H$. Two distinct meanings within one Appendix. | Optional renaming $H_{\mathrm{ent}}$ for entropy, or rely on context. |
| 2427 | P1 | C.5.2 paragraph title is "Adversarial / input-set MRs" but the body covers **both** adversarial MRs and the metric-stability ninth-block candidate ($M_{\mathrm{lip}}$). The cross-ref from line 2417 ("metric-stability class discussed in Appendix~C.5.2") expects this. | Either retitle C.5.2 to "Adversarial / input-set MRs and the metric-stability candidate ninth block", or split into C.5.2 and C.5.3 (renumbering C.5.3 → C.5.4). |
| 2433 | P2 | "The three classes of \S C.5.1--\S C.5.3 are abstract characterisations..." — uses the \S\ convention but the C.5.x are paragraph-level under an un-numbered `subsection*`. Render check at compile time. | Compile-time verify. |
| 2564 | P1 | "The four-step procedure of **Section~3.2**" — hand-coded section number. Should be `Section~\ref{subsec:decomposition}` or similar (the four-step procedure is at line 346 "Construction of the MetaPattern set"). | Use `\ref{}`. |

### Appendix D — Reference implementation (lines 2601–2671)

No P0/P1 findings.

| line | severity | finding | suggested fix |
|---|---|---|---|
| 2634 | P1 | `CANONICAL_ORDER` constant lists 7 blocks `["G","O_le","T*","T_rev*","L*","D*","E*"]` — the 8th block (`B*_rel`) is missing. The text body and Definition~\ref{def:canonical-order} use eight blocks. | Add `"B_rel*"` to the constant. |

### Cross-cutting

| section | severity | finding | suggested fix |
|---|---|---|---|
| §6.6 throughout | P1 | The terms "Set L" and "Set L ensemble" are used inconsistently. §5.7 / §6.1 introduces "Set L" as a single-sample GPT-4 probe (5 MRs); §6.6.4 introduces "Set L ensemble" as a 2-vendor × 5-temperature harvest (487 MRs). The Abstract / §1 / §7 sometimes drops the "ensemble" qualifier. | Standardise: "Set~L" for the single-sample case-study artefact (§5), "Set~$L_{\mathrm{ensemble}}$" for the §6.6 harvest. Already done at lines 772 and 1746; check for "Set L" mentions in §7 / §8. |
| References | P1 | Citation style uses `\cite` exclusively (134 instances). No `\citep` / `\citet` mixing. ACM Reference Format permits either; consistent with `\bibliographystyle{ACM-Reference-Format}`. ✓ | none. |
| `\Cref` / `\nameref` usage | P1 | Only one `\nameref` (line 2032). Generally consistent. | none. |

## Summary

- **P0 issues: 8**
  - 6× numerical inconsistency in §6.6 (lines 1789, 1811-1812, 1815, 1858-1860, 2076-2078) — D1 vs pooled McNemar p-values; D2 stratum n=5 vs n=2/n=7 mis-labels; `0/5` vs `0/7` conflation.
  - 1× missing H3a verdict (D1 gap 0.212 exceeds pre-registered $\Delta = 0.10$, no PASS/FAIL annotation).
  - 1× Appendix B claims 12 representative MRs but lists 13 (item (iii) reflective-boundary symmetry has no Table 3 row).

- **P1 issues: ≈26**
  - 5× hand-coded `Section~3.2`, `Theorem~1`, `Theorem~2`, `Definition~1`, etc. instead of `\ref{}` (lines 76, 134, 2189, 2231, 2564)
  - 1× cross-ref to Remark labelled as "Appendix" (line 2417: `Appendix~\ref{rem:metric-stability-block}`)
  - 1× missing $\mathcal{B}^{*}_{\mathrm{rel}}$ row in Table~\ref{tab:complexity}
  - 1× missing 8th block in `CANONICAL_ORDER` Python constant (Appendix D)
  - 1× Set L / Set L ensemble naming inconsistency
  - Various scope / wording clarifications

- **P2 issues: ≈5**
  - Reactor physics $\rho$ vs MR-name $\rho_{\mathrm{nonadd}}$ symbol collision (C.6)
  - $H$ entropy vs $H_X$ operator symbol collision (C.5)
  - Theorem 2 statement uses $n$ for generating-set cardinality (potential conflation with sample-size $n$)
  - Minor rephrases for readability (e.g. "raising the count" vs "bringing the count", line 134)

- **Estimated fix effort: 3–4 hours** (most P0s are mechanical search-and-replace; the H3a verdict and Appendix B 12-vs-13 require an authorial decision).

## Anti-pattern checklist

- [x] **C1 版本化叙事**: `v[0-9]\.[0-9]|R[1-9] adds|round-?[0-9]|first.{0,30}adversarial|second.{0,30}adversarial` → **0 hits** in the body.
- [x] **C2 修订溯源**: no "Round 4 → Round 5 added X" patterns; no R&R traceability matrix in body. → **0 hits**.
- [x] **C3 时序措辞**: `we encountered|after submission we found` → **0 hits**.
- [x] **C6 underpowered 缺标**: all four pilots ($n \le 10$: §5.7 deepcrime pilot $n=5$, §6.6.6 Commons Math pilot $n=3$ SUTs, §6.6.6 LRCA $n=36$ but reported with explicit $\kappa$ CIs, §5.6 case study $n=20$) explicitly flag underpowered status at the appropriate stratum. → **0 missing**.
- [x] **Em-dash zero tolerance** (U+2014): `\xe2\x80\x94` → **0 hits**. (En-dash U+2013 also 0 hits.)
- [x] **AI cliché 残留**: `(crucial|pivotal|landscape|underscore|leverage|showcase|robust signal|intricate|tapestry|testament|delve into|It is important to note|delves)` → 2 hits, both `landscape` (lines 186 "fitness landscape" and 643 "loss landscape") which are legitimate technical terms (GP fitness landscape; ML loss landscape), not AI-cliché use. → **0 problematic hits**.
- [x] **Sentence case 章节标题**: all `\section{}` / `\subsection{}` / `\subsubsection{}` titles audited; titles like "Background and related work", "Operator-algebraic preliminaries", "The NOETHER framework", "Cross-domain demonstration: equivariant machine learning", "Discussion and threats to validity" are all sentence case. Proper nouns (NOETHER, METRIC, METRIC+, GenMorph, CONSTRUCT-MP, DeepCrime, Boltzmann) and acronyms (MR, SOTA, PWR, ML, DB) correctly preserve capitalisation. → **0 Title Case violations**.

## Items NOT in scope of this pass

- Bibliography entry verification (handled separately in `reference_verification.md`).
- Compile-stage warning audit (handled separately in step 2b of CLAUDE.md pipeline).
- Cited paper authority audit (step 2d).
- API-key / personal-path secret-scan (step 2e).

End of report.

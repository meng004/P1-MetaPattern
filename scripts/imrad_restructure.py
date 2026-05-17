#!/usr/bin/env python3
"""IMRaD restructure of NOETHER_paper.tex.

Strategy:
- Block-based extraction (1-indexed inclusive ranges from section analysis)
- Selective demotion (\\section -> \\subsection, \\subsection -> \\subsubsection)
- Rdb (S6.7), negative (S6.8), and S8 subsections are kept at \\subsection level
- New top-level chapters (S3 NOETHER, S4 Empirical, S5 Threats) inserted

Constraints (CLAUDE.md):
- Zero em-dash (U+2014) in new prose
- Sentence case for new section titles
- No version-narrative wording

Output: NOETHER_paper_imrad.tex (does NOT modify original).
"""
from pathlib import Path

SRC = Path("NOETHER_paper.tex")
DST = Path("NOETHER_paper_imrad.tex")

# Block boundaries (1-indexed inclusive)
B = {
    'preamble':            (   1,  119),  # preamble + commands
    'intro':               ( 120,  233),  # S1
    'related':             ( 234,  309),  # S2
    'prelim':              ( 310,  436),  # S3 (algebra prelim)
    'framework':           ( 437,  567),  # S4 (NOETHER framework + Th 1, 2)
    'boltz':               ( 568,  678),  # S5 (Boltzmann)
    'equi':                ( 679,  781),  # S6 header + S6.1-S6.5 (equi-ML theory)
    'case_study':          ( 782,  969),  # S6.6 (moves to empirical chapter)
    'rdb':                 ( 970,  998),  # S6.7 (third domain)
    'negative':            ( 999, 1159),  # S6.8 (negative PWR, Th 1' falsification)
    'empirical':           (1160, 2177),  # S7 (full empirical chapter)
    # L2178-2180 = S8 \section header + label + blank (DROPPED)
    'threats_4':           (2181, 2192),  # S8.1 (four threats)
    'metric':              (2193, 2529),  # S8.2 (METRIC+ relationship)
    'pmcm':                (2530, 2571),  # S8.3 (PMCM worked example)
    'practical':           (2572, 2582),  # S8.4 (practical guidance)
    'artefact':            (2583, 2597),  # S8.5 (artefact statement)
    'human':               (2598, 2603),  # S8.6 (human role)
    'conclusion':          (2604, 2619),  # S9
    'appendix':            (2620, 2874),  # appendices + bibliography + EOF
}

def block(lines, name):
    """Extract a block (1-indexed inclusive)."""
    start, end = B[name]
    return lines[start-1:end]

def demote(lines):
    """Demote: \\section -> \\subsection, \\subsection -> \\subsubsection.
    Order matters: check \\subsubsection first to avoid double-demote.
    Pre-existing \\subsubsection becomes \\paragraph (rare; only L862)."""
    out = []
    for line in lines:
        if line.startswith('\\subsubsection'):
            line = '\\paragraph' + line[len('\\subsubsection'):]
        elif line.startswith('\\subsection'):
            line = '\\subsub' + line[4:]  # \\subsection -> \\subsubsection
        elif line.startswith('\\section'):
            line = '\\sub' + line[1:]  # \\section -> \\subsection
        out.append(line)
    return out

def main():
    raw = SRC.read_text()
    lines = raw.split('\n')

    new = []
    new += block(lines, 'preamble')
    new += block(lines, 'intro')
    new += block(lines, 'related')

    # ============== New S3: NOETHER framework ==============
    new += [
        '',
        '%% ================================================================',
        '%% NEW CHAPTER S3: NOETHER framework (theory consolidation, IMRaD)',
        '%% ================================================================',
        '\\section{The NOETHER framework}',
        '\\label{sec:noether-framework}',
        '',
        ('This section presents NOETHER as a self-contained theoretical contribution. '
         'Operator-algebraic preliminaries and the eight-block decomposition appear in '
         '\\S\\ref{subsec:prelim-content}; the algebra-induced metamorphic relation space '
         'and the CONSTRUCT-MP construction in \\S\\ref{subsec:framework-content}; the '
         'algebraic closure theorem (Theorem~\\ref{thm:closure}) and polynomial-time '
         'decidability theorem (Theorem~\\ref{thm:decidable}) in \\S\\ref{subsec:closure-section} '
         'and \\S\\ref{subsec:decidability-section} respectively. The framework is then '
         'instantiated on three structurally distinct operator algebras: Boltzmann reactor '
         'physics in \\S\\ref{subsec:boltz-instantiation-content}, equivariant machine '
         'learning in \\S\\ref{subsec:equi-instantiation-content}, and relational query '
         'optimisers in \\S\\ref{subsec:third-domain}. The section concludes by falsifying '
         'the strictly stronger absolute-completeness conjecture, Theorem~$1\'$, on a '
         'fourth program family (PWR core diffusion) via two pairwise-independent '
         'counterexamples (\\S\\ref{subsec:negative-pwr}).'),
        '',
    ]
    new += demote(block(lines, 'prelim'))
    new += demote(block(lines, 'framework'))
    new += demote(block(lines, 'boltz'))
    new += demote(block(lines, 'equi'))
    # rdb and negative stay at \subsection level (they were already \subsection inside old S6)
    new += block(lines, 'rdb')
    new += block(lines, 'negative')

    # ============== New S4: Empirical evaluation ==============
    new += [
        '',
        '%% ================================================================',
        '%% NEW CHAPTER S4: Empirical evaluation (experiment consolidation, IMRaD)',
        '%% ================================================================',
        '\\section{Empirical evaluation}',
        '\\label{sec:empirical-evaluation}',
        '',
        ('This section validates the framework against five research questions. RQ1: does '
         'CONSTRUCT-MP re-derive an existing inductive MR catalogue at the algebra-block '
         'level? RQ2: do the derived MRs execute on real cross-domain systems under test? '
         'RQ3: does the pre-registered \\(\\mathcal{L}^{*}\\)-blindness prediction hold '
         'on independent substrates? RQ4: how does NOETHER compare against GenMorph, the '
         'closest evolutionary baseline, at GenMorph\'s published budget? RQ5: how does '
         'NOETHER compare against METRIC+ on the corpus that METRIC+ itself published? '
         'The research questions are addressed in turn: RQ2 in '
         '\\S\\ref{subsec:case-study}, RQ3 in \\S\\ref{subsec:l-blindness-content}, RQ4 '
         'in \\S\\ref{subsec:pooled-headtohead}, and RQ5 in \\S\\ref{subsec:metricplus-content}.'),
        '',
    ]
    # case_study already starts with \subsection (becomes a subsection of new S4)
    new += block(lines, 'case_study')
    # empirical: demote \section -> \subsection so it becomes a chapter of new S4
    new += demote(block(lines, 'empirical'))
    # metric (S8.2) and pmcm (S8.3) already at \subsection level
    new += block(lines, 'metric')
    new += block(lines, 'pmcm')

    # ============== New S5: Threats to validity and limitations ==============
    new += [
        '',
        '%% ================================================================',
        '%% NEW CHAPTER S5: Threats to validity and limitations',
        '%% ================================================================',
        '\\section{Threats to validity and limitations}',
        '\\label{sec:threats-limitations}',
        '',
        ('We consolidate the construct, internal, external, and conclusion validity '
         'discussions from across the empirical chapter, together with practical '
         'engineering guidance for users of the framework, the artefact-availability '
         'statement, and a note on the partial automation of the upstream layer.'),
        '',
    ]
    new += block(lines, 'threats_4')
    new += block(lines, 'practical')
    new += block(lines, 'artefact')
    new += block(lines, 'human')

    # Conclusion (S9) keeps its \section header
    new += block(lines, 'conclusion')

    # Appendices unchanged
    new += block(lines, 'appendix')

    out_text = '\n'.join(new)

    # Em-dash audit on inserted prose only
    em_dash_count = out_text.count('—')
    print(f'Em-dash count in output: {em_dash_count}')

    DST.write_text(out_text)
    print(f'Wrote {len(new)} lines to {DST}')

if __name__ == '__main__':
    main()

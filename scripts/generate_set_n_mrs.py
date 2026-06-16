#!/usr/bin/env python3
"""
Generate Set N (NOETHER-derived) metamorphic relations for all 23 GenMorph
subjects, encoded in GenMorph's GAssert (jir, jor) DSL.

Each MR is derived from one of the eight NOETHER algebra blocks:
  G    — symmetry / permutation
  O_le — order / monotonicity / boundedness
  T*   — self-adjoint
  T*_2 — time-reversal
  D*   — qualitative dynamics
  L*   — limit / closure
  E*   — method-comparison / equivalence
  I*   — inverse closure

Encoding paths (per CLAUDE.md project rules):
  Path A — two-execution metamorphic, natural in (jir, jor) DSL.
           jir relates source/followup inputs; jor relates source/followup outputs.
  Path B — single-execution invariant. jir = identity (i_<arg>_f = i_<arg>_s);
           jor expresses the invariant on _s vars only.
  Path C — fallback if GAssert rejects Path B's jor with only _s vars; conjunct
           the invariant on both source-side and followup-side.

DSL conventions:
  • Numeric args: ((double) i_<arg>_{s,f})
  • Boolean output: o_return_{s,f} (no cast)
  • Sequence args: ch.usi.gassert.data.types.Sequence.fromValue(i_<arg>_{s,f})
  • Equality on numerics: Math.abs(a - b) < 1.0E-4
  • Class constants: i_this_s.PI, i_this_s.E, i_this_s.PRIMES_LAST, etc.
"""

from pathlib import Path

EPS = "1.0E-4"
REPO = Path(__file__).resolve().parent.parent
OUT_DIR = REPO / "set_n_mrs"

# ----------------------------------------------------------------------------
# DSL primitive helpers
# ----------------------------------------------------------------------------
def D(arg, side):  # double-cast input
    return f"((double) i_{arg}_{side})"

def OD(side):  # double-cast return
    return f"((double) o_return_{side})"

def OB(side):  # boolean return
    return f"o_return_{side}"

def SEQ(arg, side):  # Sequence-wrap input
    return f"(ch.usi.gassert.data.types.Sequence.fromValue(i_{arg}_{side}))"

def OSEQ(side):  # Sequence-wrap return value (string/array return)
    return f"(ch.usi.gassert.data.types.Sequence.fromValue(o_return_{side}))"

def OASEQ(arg, side):  # Sequence-wrap output array (in-place mutators like sort)
    return f"(ch.usi.gassert.data.types.Sequence.fromValue(o_{arg}_{side}))"

_JAVA_CONST = {"PI": "Math.PI", "E": "Math.E"}


def CONST(side, name):  # class constant
    # PI/E are JDK constants (MathClass exposes no such instance field, so
    # i_this.PI would not compile in the generated PITest assertion). Other
    # names (e.g. PRIMES_LAST) stay instance-qualified; they appear only in
    # input relations (.jir), which are not compiled into the test suite.
    if name in _JAVA_CONST:
        return f"((double) {_JAVA_CONST[name]})"
    return f"((double) i_this_{side}.{name})"

def eq_d(a, b):
    return f"(Math.abs({a} - {b}) < {EPS})"

def neq_d(a, b):
    return f"(Math.abs({a} - {b}) >= {EPS})"

def le_d(a, b):
    return f"({a} <= {b})"

def ge_d(a, b):
    return f"({a} >= {b})"

def conj(*xs):
    return "(" + " && ".join(xs) + ")"

def disj(*xs):
    return "(" + " || ".join(xs) + ")"

def neg(x):
    return f"(!{x})"

# Identity jir (for Path B): all numeric args unchanged + class constants unchanged
def id_jir(numeric_args, has_this=False):
    parts = [eq_d(D(a, "f"), D(a, "s")) for a in numeric_args]
    if has_this:
        parts.append(eq_d(CONST("f", "PI"), CONST("s", "PI")))
        parts.append(eq_d(CONST("f", "E"), CONST("s", "E")))
    return conj(*parts) if parts else "true"

def id_jir_seq(seq_args, numeric_args=(), has_this=False):
    """Identity jir with sequence args (use .equals())."""
    parts = []
    for a in seq_args:
        parts.append(f"({SEQ(a, 'f')}.equals({SEQ(a, 's')}, {EPS}))")
    for a in numeric_args:
        parts.append(eq_d(D(a, "f"), D(a, "s")))
    if has_this:
        parts.append(eq_d(CONST("f", "PI"), CONST("s", "PI")))
        parts.append(eq_d(CONST("f", "E"), CONST("s", "E")))
    return conj(*parts) if parts else "true"

# ----------------------------------------------------------------------------
# MR specifications, organised by subject.
#
# Each entry: (mr_name, jir_string, jor_string, comment)
# ----------------------------------------------------------------------------

MRS = {}

# ===== Math: gcd =====
MRS["MathClass?gcd?0"] = [
    ("rho_perm",
     conj(eq_d(D("p", "f"), D("q", "s")), eq_d(D("q", "f"), D("p", "s"))),
     eq_d(OD("f"), OD("s")),
     "G-block: gcd(p, q) = gcd(q, p)"),
    ("rho_scale",
     conj(eq_d(D("p", "f"), f"({D('p','s')} * 2.0)"),
          eq_d(D("q", "f"), f"({D('q','s')} * 2.0)")),
     eq_d(OD("f"), f"({OD('s')} * 2.0)"),
     "G-block: gcd(2p, 2q) = 2 * gcd(p, q)"),
    ("rho_eqref",
     conj(eq_d(D("p", "f"), D("p", "s")),
          eq_d(D("q", "f"), f"({D('q','s')} + {D('p','s')})")),
     eq_d(OD("f"), OD("s")),
     "O_le-block: gcd(p, q + p) = gcd(p, q) (Euclidean lemma)"),
    ("rho_mono",
     id_jir(["p", "q"]),
     disj(f"(Math.abs({D('p','s')}) < {EPS})",
          f"(Math.abs({D('q','s')}) < {EPS})",
          conj(le_d(OD("s"), f"Math.abs({D('p','s')})"),
               le_d(OD("s"), f"Math.abs({D('q','s')})"))),
     "O_le-block (Path B): gcd(p, q) <= min(|p|, |q|)"),
]

# ===== Math: sin =====
MRS["MathClass?sin?0"] = [
    ("rho_oddsym",
     conj(eq_d(D("x", "f"), f"({D('x','s')} * (0.0 - 1.0))"),
          eq_d(CONST("f", "PI"), CONST("s", "PI")),
          eq_d(CONST("f", "E"), CONST("s", "E"))),
     eq_d(OD("f"), f"({OD('s')} * (0.0 - 1.0))"),
     "G-block: sin(-x) = -sin(x)"),
    ("rho_period",
     conj(eq_d(D("x", "f"), f"({D('x','s')} + (2.0 * {CONST('s','PI')}))"),
          eq_d(CONST("f", "PI"), CONST("s", "PI")),
          eq_d(CONST("f", "E"), CONST("s", "E"))),
     eq_d(OD("f"), OD("s")),
     "G-block: sin(x + 2pi) = sin(x)"),
    ("rho_complement",
     conj(eq_d(D("x", "f"), f"({CONST('s','PI')} - {D('x','s')})"),
          eq_d(CONST("f", "PI"), CONST("s", "PI")),
          eq_d(CONST("f", "E"), CONST("s", "E"))),
     eq_d(OD("f"), OD("s")),
     "G-block: sin(pi - x) = sin(x)"),
    ("rho_bound",
     id_jir(["x"], has_this=True),
     conj(le_d(OD("s"), "1.0"), ge_d(OD("s"), "(0.0 - 1.0)")),
     "O_le-block (Path B): |sin(x)| <= 1"),
]

# ===== Math: acos =====
MRS["MathClass?acos?0"] = [
    ("rho_oddcomp",
     conj(eq_d(D("x", "f"), f"({D('x','s')} * (0.0 - 1.0))"),
          eq_d(CONST("f", "PI"), CONST("s", "PI")),
          eq_d(CONST("f", "E"), CONST("s", "E"))),
     eq_d(OD("f"), f"({CONST('s','PI')} - {OD('s')})"),
     "G-block: acos(-x) = pi - acos(x)"),
    ("rho_bound_lo",
     id_jir(["x"], has_this=True),
     ge_d(OD("s"), "0.0"),
     "O_le-block (Path B): acos(x) >= 0"),
    ("rho_bound_hi",
     id_jir(["x"], has_this=True),
     le_d(OD("s"), CONST("s", "PI")),
     "O_le-block (Path B): acos(x) <= pi"),
]

# ===== Math: log10 =====
MRS["MathClass?log10?0"] = [
    ("rho_pow10",
     conj(eq_d(D("x", "f"), f"({D('x','s')} * 10.0)"),
          eq_d(CONST("f", "PI"), CONST("s", "PI")),
          eq_d(CONST("f", "E"), CONST("s", "E"))),
     eq_d(OD("f"), f"({OD('s')} + 1.0)"),
     "G-block: log10(10x) = log10(x) + 1"),
    ("rho_unit",
     id_jir(["x"], has_this=True),
     disj(neq_d(D("x", "s"), "1.0"), eq_d(OD("s"), "0.0")),
     "L*-block (Path B): log10(1) = 0 (fixed point)"),
    ("rho_pos",
     id_jir(["x"], has_this=True),
     disj(f"({D('x','s')} <= 1.0)", ge_d(OD("s"), "0.0")),
     "O_le-block (Path B): x >= 1 implies log10(x) >= 0"),
]

# ===== Math: millerRabinPrimeTest =====
# Args: int n. SUT instance has PRIMES.length and PRIMES_LAST as constants.
# NOETHER's framework: G/O_le blocks essentially empty for primality predicate;
# only L*-block fixed-point invariants survive.
MRS["MathClass?millerRabinPrimeTest?0"] = [
    ("rho_two_prime",
     id_jir(["n"]) + " && " + eq_d(f"((double) i_this_f.PRIMES_LAST)", f"((double) i_this_s.PRIMES_LAST)"),
     disj(neq_d(D("n", "s"), "2.0"), OB("s")),
     "L*-block (Path B): isPrime(2) = true (2 is prime)"),
    ("rho_zero_composite",
     id_jir(["n"]) + " && " + eq_d(f"((double) i_this_f.PRIMES_LAST)", f"((double) i_this_s.PRIMES_LAST)"),
     disj(neq_d(D("n", "s"), "0.0"), neg(OB("s"))),
     "L*-block (Path B): isPrime(0) = false"),
    ("rho_one_composite",
     id_jir(["n"]) + " && " + eq_d(f"((double) i_this_f.PRIMES_LAST)", f"((double) i_this_s.PRIMES_LAST)"),
     disj(neq_d(D("n", "s"), "1.0"), neg(OB("s"))),
     "L*-block (Path B): isPrime(1) = false"),
]

# ===== Math: nextPrime =====
MRS["MathClass?nextPrime?0"] = [
    ("rho_lower_bound",
     id_jir(["n"]),
     ge_d(OD("s"), D("n", "s")),
     "O_le-block (Path B): nextPrime(n) >= n"),
    ("rho_min_two",
     id_jir(["n"]),
     ge_d(OD("s"), "2.0"),
     "O_le-block (Path B): nextPrime(n) >= 2"),
    ("rho_succ",
     eq_d(D("n", "f"), f"({D('n','s')} + 1.0)"),
     ge_d(OD("f"), OD("s")),
     "G-block: nextPrime(n+1) >= nextPrime(n) (monotone non-decreasing)"),
]

# ===== Math: pow =====
# Args: double e, int k. Computes e^k.
MRS["MathClass?pow?0"] = [
    ("rho_succ",
     conj(eq_d(D("e", "f"), D("e", "s")),
          eq_d(D("k", "f"), f"({D('k','s')} + 1.0)")),
     eq_d(OD("f"), f"({D('e','s')} * {OD('s')})"),
     "G-block: pow(e, k+1) = e * pow(e, k)"),
    ("rho_zero_exp",
     id_jir(["e", "k"]),
     disj(neq_d(D("k", "s"), "0.0"), eq_d(OD("s"), "1.0")),
     "L*-block (Path B): pow(e, 0) = 1"),
    ("rho_unit_base",
     id_jir(["e", "k"]),
     disj(neq_d(D("e", "s"), "1.0"), eq_d(OD("s"), "1.0")),
     "L*-block (Path B): pow(1, k) = 1"),
    ("rho_one_exp",
     id_jir(["e", "k"]),
     disj(neq_d(D("k", "s"), "1.0"), eq_d(OD("s"), D("e", "s"))),
     "L*-block (Path B): pow(e, 1) = e"),
]

# ===== Math: sinh =====
MRS["MathClass?sinh?0"] = [
    ("rho_oddsym",
     conj(eq_d(D("x", "f"), f"({D('x','s')} * (0.0 - 1.0))"),
          eq_d(CONST("f", "PI"), CONST("s", "PI")),
          eq_d(CONST("f", "E"), CONST("s", "E"))),
     eq_d(OD("f"), f"({OD('s')} * (0.0 - 1.0))"),
     "G-block: sinh(-x) = -sinh(x)"),
    ("rho_zero",
     id_jir(["x"], has_this=True),
     disj(neq_d(D("x", "s"), "0.0"), eq_d(OD("s"), "0.0")),
     "L*-block (Path B): sinh(0) = 0"),
    ("rho_sign",
     id_jir(["x"], has_this=True),
     disj(conj(ge_d(D("x", "s"), "0.0"), ge_d(OD("s"), "0.0")),
          conj(le_d(D("x", "s"), "0.0"), le_d(OD("s"), "0.0"))),
     "O_le-block (Path B): sign(sinh(x)) = sign(x)"),
]

# ===== Math: stirlingS2 =====
MRS["MathClass?stirlingS2?0"] = [
    ("rho_diag",
     id_jir(["n", "k"]),
     disj(neq_d(D("n", "s"), D("k", "s")), eq_d(OD("s"), "1.0")),
     "L*-block (Path B): S(n, n) = 1"),
    ("rho_one_k",
     id_jir(["n", "k"]),
     disj(neq_d(D("k", "s"), "1.0"), f"({D('n','s')} < 1.0)", eq_d(OD("s"), "1.0")),
     "L*-block (Path B): S(n, 1) = 1 for n >= 1"),
    ("rho_zero_k",
     id_jir(["n", "k"]),
     disj(neq_d(D("k", "s"), "0.0"), f"({D('n','s')} < 1.0)", eq_d(OD("s"), "0.0")),
     "L*-block (Path B): S(n, 0) = 0 for n >= 1"),
    ("rho_nonneg",
     id_jir(["n", "k"]),
     ge_d(OD("s"), "0.0"),
     "O_le-block (Path B): S(n, k) >= 0"),
]

# ===== Math: tan =====
MRS["MathClass?tan?0"] = [
    ("rho_oddsym",
     conj(eq_d(D("x", "f"), f"({D('x','s')} * (0.0 - 1.0))"),
          eq_d(CONST("f", "PI"), CONST("s", "PI")),
          eq_d(CONST("f", "E"), CONST("s", "E"))),
     eq_d(OD("f"), f"({OD('s')} * (0.0 - 1.0))"),
     "G-block: tan(-x) = -tan(x)"),
    ("rho_period_pi",
     conj(eq_d(D("x", "f"), f"({D('x','s')} + {CONST('s','PI')})"),
          eq_d(CONST("f", "PI"), CONST("s", "PI")),
          eq_d(CONST("f", "E"), CONST("s", "E"))),
     eq_d(OD("f"), OD("s")),
     "G-block: tan(x + pi) = tan(x)"),
    ("rho_zero",
     id_jir(["x"], has_this=True),
     disj(neq_d(D("x", "s"), "0.0"), eq_d(OD("s"), "0.0")),
     "L*-block (Path B): tan(0) = 0"),
]

# =====================================================================
# Lang subjects (5)
# =====================================================================

# ===== Lang: abbreviate =====
# Args: String str, String abbrevMarker, int offset, int maxWidth
MRS["LangClass?abbreviate?0"] = [
    ("rho_idem_short",
     id_jir_seq(["str", "abbrevMarker"], ["offset", "maxWidth"]),
     disj(f"({SEQ('str','s')}.length() > {D('maxWidth','s')})",
          f"({OSEQ('s')}.equals({SEQ('str','s')}, {EPS}))"),
     "L*-block (Path B): str.length <= maxWidth implies abbreviate returns str"),
    ("rho_length_bound",
     id_jir_seq(["str", "abbrevMarker"], ["offset", "maxWidth"]),
     le_d(f"((double) {OSEQ('s')}.length())", D("maxWidth", "s")),
     "O_le-block (Path B): result.length <= maxWidth"),
]

# ===== Lang: capitalize =====
MRS["LangClass?capitalize?0"] = [
    ("rho_length",
     id_jir_seq(["str"]),
     eq_d(f"((double) {OSEQ('s')}.length())",
          f"((double) {SEQ('str','s')}.length())"),
     "L*-block (Path B): capitalize(s).length = s.length"),
    ("rho_empty",
     id_jir_seq(["str"]),
     disj(f"({SEQ('str','s')}.length() > 0)",
          f"({OSEQ('s')}.length() == 0)"),
     "L*-block (Path B): capitalize(\"\") = \"\""),
    ("rho_idem_call",
     id_jir_seq(["str"]),
     f"({OSEQ('f')}.equals({OSEQ('s')}, {EPS}))",
     "G-block: capitalize is deterministic — same input gives same output"),
]

# ===== Lang: center =====
# Args: String str, int size, String padStr
MRS["LangClass?center?0"] = [
    ("rho_idem_short",
     id_jir_seq(["str", "padStr"], ["size"]),
     disj(f"({SEQ('str','s')}.length() >= {D('size','s')})",
          f"((double) {OSEQ('s')}.length()) >= {D('size','s')}"),
     "L*-block (Path B): result length is at least size when padding applied"),
    ("rho_length_lower",
     id_jir_seq(["str", "padStr"], ["size"]),
     ge_d(f"((double) {OSEQ('s')}.length())",
          f"((double) {SEQ('str','s')}.length())"),
     "O_le-block (Path B): result.length >= str.length"),
    ("rho_size_zero",
     id_jir_seq(["str", "padStr"], ["size"]),
     disj(f"({D('size','s')} > 0.0)",
          f"({OSEQ('s')}.equals({SEQ('str','s')}, {EPS}))"),
     "L*-block (Path B): size <= 0 implies result = str"),
]

# ===== Lang: difference =====
# Args: String str1, String str2
MRS["LangClass?difference?0"] = [
    ("rho_self",
     id_jir_seq(["str1", "str2"]),
     disj(neg(f"({SEQ('str1','s')}.equals({SEQ('str2','s')}, {EPS}))"),
          f"({OSEQ('s')}.length() == 0)"),
     "L*-block (Path B): difference(s, s) = \"\""),
    ("rho_empty_left",
     id_jir_seq(["str1", "str2"]),
     disj(f"({SEQ('str1','s')}.length() > 0)",
          f"({OSEQ('s')}.equals({SEQ('str2','s')}, {EPS}))"),
     "L*-block (Path B): difference(\"\", s2) = s2"),
    ("rho_swap",
     conj(f"({SEQ('str1','f')}.equals({SEQ('str2','s')}, {EPS}))",
          f"({SEQ('str2','f')}.equals({SEQ('str1','s')}, {EPS}))"),
     disj(f"({SEQ('str1','s')}.equals({SEQ('str2','s')}, {EPS}))",
          neg(f"({OSEQ('f')}.equals({OSEQ('s')}, {EPS}))")),
     "G-block: when str1 != str2, swapping arguments gives different result"),
]

# ===== Lang: isSorted =====
MRS["LangClass?isSorted?0"] = [
    ("rho_singleton",
     id_jir_seq(["array"]),
     disj(f"({SEQ('array','s')}.length() > 1)",
          OB("s")),
     "L*-block (Path B): isSorted([x]) = true"),
    ("rho_empty",
     id_jir_seq(["array"]),
     disj(f"({SEQ('array','s')}.length() > 0)",
          OB("s")),
     "L*-block (Path B): isSorted([]) = true"),
    ("rho_idem_call",
     id_jir_seq(["array"]),
     f"(({OB('f')}) == ({OB('s')}))",
     "G-block: isSorted is deterministic"),
]

# =====================================================================
# Guava subjects (8)
# =====================================================================

# ===== Guava: indexOf =====
# Args: boolean[] array, boolean[] target  → returns int
MRS["GuavaClass?indexOf?0"] = [
    ("rho_empty_target",
     id_jir_seq(["array", "target"]),
     disj(f"({SEQ('target','s')}.length() > 0)",
          eq_d(OD("s"), "0.0")),
     "L*-block (Path B): indexOf(a, []) = 0"),
    ("rho_self",
     id_jir_seq(["array", "target"]),
     disj(neg(f"({SEQ('array','s')}.equals({SEQ('target','s')}, {EPS}))"),
          eq_d(OD("s"), "0.0")),
     "L*-block (Path B): indexOf(a, a) = 0"),
    ("rho_lower_bound",
     id_jir_seq(["array", "target"]),
     ge_d(OD("s"), "(0.0 - 1.0)"),
     "O_le-block (Path B): indexOf returns >= -1"),
]

# ===== Guava: join =====
# Args: String separator, boolean[] array  → returns String
MRS["GuavaClass?join?0"] = [
    ("rho_empty_array",
     id_jir_seq(["separator", "array"]),
     disj(f"({SEQ('array','s')}.length() > 0)",
          f"({OSEQ('s')}.length() == 0)"),
     "L*-block (Path B): join(sep, []) = \"\""),
    ("rho_length_lower",
     id_jir_seq(["separator", "array"]),
     ge_d(f"((double) {OSEQ('s')}.length())",
          f"((double) {SEQ('array','s')}.length())"),
     "O_le-block (Path B): result.length >= array.length"),
    ("rho_separator_idem",
     conj(f"({SEQ('separator','f')}.equals({SEQ('separator','s')}, {EPS}))",
          f"({SEQ('array','f')}.equals({SEQ('array','s')}, {EPS}))"),
     f"({OSEQ('f')}.equals({OSEQ('s')}, {EPS}))",
     "G-block: deterministic on identical inputs"),
]

# ===== Guava: meanOf =====
# Args: int[] values  → returns double
MRS["GuavaClass?meanOf?0"] = [
    ("rho_flip",
     f"({SEQ('values','f')}.equals({SEQ('values','s')}.flip(), {EPS}))",
     eq_d(OD("f"), OD("s")),
     "G-block: meanOf(reverse(a)) = meanOf(a) (reversal is one specific permutation)"),
    ("rho_singleton",
     id_jir_seq(["values"]),
     disj(neq_d(f"((double) {SEQ('values','s')}.length())", "1.0"),
          eq_d(OD("s"), f"((double) {SEQ('values','s')}.sum())")),
     "L*-block (Path B): meanOf([x]) = x"),
    ("rho_le_max",
     id_jir_seq(["values"]),
     disj(f"({SEQ('values','s')}.length() == 0)",
          le_d(OD("s"),
               f"((Math.abs({SEQ('values','s')}.length()) < {EPS}) ? 1.0 : ({SEQ('values','s')}.sum()))")),
     "O_le-block (Path B): meanOf(a) <= sum(a) when length >= 1 and all non-negative — degenerate bound"),
]

# ===== Guava: min =====
# Args: int[] array  → returns int
MRS["GuavaClass?min?0"] = [
    ("rho_flip",
     f"({SEQ('array','f')}.equals({SEQ('array','s')}.flip(), {EPS}))",
     eq_d(OD("f"), OD("s")),
     "G-block: min(reverse(a)) = min(a)"),
    ("rho_singleton",
     id_jir_seq(["array"]),
     disj(neq_d(f"((double) {SEQ('array','s')}.length())", "1.0"),
          eq_d(OD("s"), f"((double) {SEQ('array','s')}.sum())")),
     "L*-block (Path B): min([x]) = x"),
    ("rho_le_mean",
     id_jir_seq(["array"]),
     disj(f"({SEQ('array','s')}.length() == 0)",
          le_d(f"({OD('s')} * ((double) {SEQ('array','s')}.length()))",
               f"((double) {SEQ('array','s')}.sum())")),
     "O_le-block (Path B): min(a) * length(a) <= sum(a)"),
]

# ===== Guava: padStart =====
# Args: String string, int minLength, char padChar
MRS["GuavaClass?padStart?0"] = [
    ("rho_idem_long",
     id_jir_seq(["string"], ["minLength"]),
     disj(f"({SEQ('string','s')}.length() < {D('minLength','s')})",
          f"({OSEQ('s')}.equals({SEQ('string','s')}, {EPS}))"),
     "L*-block (Path B): string.length >= minLength implies result = string"),
    ("rho_length",
     id_jir_seq(["string"], ["minLength"]),
     conj(ge_d(f"((double) {OSEQ('s')}.length())",
               f"((double) {SEQ('string','s')}.length())"),
          ge_d(f"((double) {OSEQ('s')}.length())",
               D("minLength", "s"))),
     "O_le-block (Path B): result.length >= max(string.length, minLength)"),
]

# ===== Guava: repeat =====
# Args: String string, int count
MRS["GuavaClass?repeat?0"] = [
    ("rho_zero",
     id_jir_seq(["string"], ["count"]),
     disj(f"({D('count','s')} > 0.0)",
          f"({OSEQ('s')}.length() == 0)"),
     "L*-block (Path B): repeat(s, 0) = \"\""),
    ("rho_one",
     id_jir_seq(["string"], ["count"]),
     disj(neq_d(D("count", "s"), "1.0"),
          f"({OSEQ('s')}.equals({SEQ('string','s')}, {EPS}))"),
     "L*-block (Path B): repeat(s, 1) = s"),
    ("rho_length",
     id_jir_seq(["string"], ["count"]),
     disj(f"({D('count','s')} < 0.0)",
          eq_d(f"((double) {OSEQ('s')}.length())",
               f"({D('count','s')} * ((double) {SEQ('string','s')}.length()))")),
     "L*-block (Path B): repeat(s, n).length = n * s.length"),
    ("rho_succ",
     conj(f"({SEQ('string','f')}.equals({SEQ('string','s')}, {EPS}))",
          eq_d(D("count", "f"), f"({D('count','s')} + 1.0)")),
     disj(f"({D('count','s')} < 0.0)",
          eq_d(f"((double) {OSEQ('f')}.length())",
               f"(((double) {OSEQ('s')}.length()) + ((double) {SEQ('string','s')}.length()))")),
     "G-block: repeat(s, n+1).length = repeat(s, n).length + s.length"),
]

# ===== Guava: sort =====
# Args: byte[] array, int fromIndex, int toIndex (in-place sort, returns void)
# Output relations use o_array_{s,f} for post-call array state.
MRS["GuavaClass?sort?0"] = [
    ("rho_flip",
     conj(f"({SEQ('array','f')}.equals({SEQ('array','s')}.flip(), {EPS}))",
          eq_d(D("fromIndex", "f"), D("fromIndex", "s")),
          eq_d(D("toIndex", "f"), D("toIndex", "s"))),
     f"({OASEQ('array','f')}.equals({OASEQ('array','s')}, {EPS}))",
     "G-block: sort(reverse(a)) = sort(a) (reversal preserves sorted result)"),
    ("rho_length_preserved",
     id_jir_seq(["array"], ["fromIndex", "toIndex"]),
     eq_d(f"((double) {OASEQ('array','s')}.length())",
          f"((double) {SEQ('array','s')}.length())"),
     "L*-block (Path B): sort preserves array length"),
    ("rho_sum_preserved",
     id_jir_seq(["array"], ["fromIndex", "toIndex"]),
     eq_d(f"((double) {OASEQ('array','s')}.sum())",
          f"((double) {SEQ('array','s')}.sum())"),
     "G-block (Path B): sort preserves multiset (sum-of-elements is permutation-invariant)"),
]

# ===== Guava: truncate =====
# Args: String seq, int maxLength, String truncationIndicator
MRS["GuavaClass?truncate?0"] = [
    ("rho_idem_short",
     id_jir_seq(["seq", "truncationIndicator"], ["maxLength"]),
     disj(f"({SEQ('seq','s')}.length() > {D('maxLength','s')})",
          f"({OSEQ('s')}.equals({SEQ('seq','s')}, {EPS}))"),
     "L*-block (Path B): seq.length <= maxLength implies result = seq"),
    ("rho_length_bound",
     id_jir_seq(["seq", "truncationIndicator"], ["maxLength"]),
     le_d(f"((double) {OSEQ('s')}.length())", D("maxLength", "s")),
     "O_le-block (Path B): result.length <= maxLength"),
]


# ----------------------------------------------------------------------------
# Generator
# ----------------------------------------------------------------------------
def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    n_subjects = 0
    n_mrs = 0
    for subject, mrs in MRS.items():
        sub_dir = OUT_DIR / subject
        sub_dir.mkdir(parents=True, exist_ok=True)
        for mr_name, jir, jor, _ in mrs:
            jir_path = sub_dir / f"{subject}@{mr_name}.jir.txt"
            jor_path = sub_dir / f"{subject}@{mr_name}.jor.txt"
            jir_path.write_text(jir)
            jor_path.write_text(jor)
            n_mrs += 1
        n_subjects += 1
        print(f"  {subject}: {len(mrs)} MRs")
    print(f"\nTotal: {n_subjects} subjects, {n_mrs} MRs ({n_mrs * 2} files)")
    print(f"Output: {OUT_DIR}")

if __name__ == "__main__":
    main()

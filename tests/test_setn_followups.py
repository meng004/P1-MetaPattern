#!/usr/bin/env python3
"""tests/test_setn_followups.py — Set N follow-up input construction (rule 6).

Validates scripts/setn_followups.py parsing + application across the transform
kinds present in the corpus: numeric, receiver-identity, sequence-identity,
and cross-variable swap (copyfrom).
"""
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import setn_followups as sf  # noqa: E402

GCD_SRC = """<ch.usi.methodtest.MethodTest>
  <methodName>gcd</methodName>
  <methodParameters>
    <ch.usi.methodtest.MethodParameter><name>this</name><clazz>MathClass</clazz></ch.usi.methodtest.MethodParameter>
    <ch.usi.methodtest.MethodParameter><name>p</name><clazz>int</clazz><value class="int">1223</value></ch.usi.methodtest.MethodParameter>
    <ch.usi.methodtest.MethodParameter><name>q</name><clazz>int</clazz><value class="int">5</value></ch.usi.methodtest.MethodParameter>
  </methodParameters>
</ch.usi.methodtest.MethodTest>"""

STR_SRC = """<ch.usi.methodtest.MethodTest>
  <methodName>difference</methodName>
  <methodParameters>
    <ch.usi.methodtest.MethodParameter><name>this</name><clazz>LangClass</clazz></ch.usi.methodtest.MethodParameter>
    <ch.usi.methodtest.MethodParameter><name>str1</name><clazz>java.lang.String</clazz><value class="string">abcd</value></ch.usi.methodtest.MethodParameter>
    <ch.usi.methodtest.MethodParameter><name>str2</name><clazz>java.lang.String</clazz><value class="string">xy</value></ch.usi.methodtest.MethodParameter>
  </methodParameters>
</ch.usi.methodtest.MethodTest>"""

# numeric (gcd): jir -> expected follow-up (p, q) for source (1223, 5)
NUM_CASES = {
    "perm": ("((Math.abs(((double) i_p_f) - ((double) i_q_s)) < 1.0E-4) && "
             "(Math.abs(((double) i_q_f) - ((double) i_p_s)) < 1.0E-4))", {"p": "5", "q": "1223"}),
    "scale": ("((Math.abs(((double) i_p_f) - (((double) i_p_s) * 2.0)) < 1.0E-4) && "
              "(Math.abs(((double) i_q_f) - (((double) i_q_s) * 2.0)) < 1.0E-4))", {"p": "2446", "q": "10"}),
    "eqref": ("((Math.abs(((double) i_p_f) - ((double) i_p_s)) < 1.0E-4) && "
              "(Math.abs(((double) i_q_f) - (((double) i_q_s) + ((double) i_p_s))) < 1.0E-4))", {"p": "1223", "q": "1228"}),
    "mono": ("((Math.abs(((double) i_p_f) - ((double) i_p_s)) < 1.0E-4) && "
             "(Math.abs(((double) i_q_f) - ((double) i_q_s)) < 1.0E-4))", {"p": "1223", "q": "5"}),
}

# receiver-identity + numeric (acos rho_oddcomp style)
ACOS_JIR = ("((Math.abs(((double) i_x_f) - (((double) i_x_s) * (0.0 - 1.0))) < 1.0E-4) && "
            "(Math.abs(((double) i_this_f.PI) - ((double) i_this_s.PI)) < 1.0E-4) && "
            "(Math.abs(((double) i_this_f.E) - ((double) i_this_s.E)) < 1.0E-4))")

# sequence identity (Lang single-execution invariant)
ID_JIR = ("(((ch.usi.gassert.data.types.Sequence.fromValue(i_str1_f)).equals("
          "(ch.usi.gassert.data.types.Sequence.fromValue(i_str1_s)), 1.0E-4)))")

# cross-variable string swap (difference rho_swap)
SWAP_JIR = ("(((ch.usi.gassert.data.types.Sequence.fromValue(i_str1_f)).equals("
            "(ch.usi.gassert.data.types.Sequence.fromValue(i_str2_s)), 1.0E-4)) && "
            "((ch.usi.gassert.data.types.Sequence.fromValue(i_str2_f)).equals("
            "(ch.usi.gassert.data.types.Sequence.fromValue(i_str1_s)), 1.0E-4)))")


def main():
    tmp = Path(tempfile.mkdtemp())

    # --- numeric (gcd) ---
    g = tmp / "g.methodinputs"; g.write_text(GCD_SRC)
    gtree, gparams = sf.read_method_inputs(g)
    assert gparams["p"] == ("int", "1223") and gparams["this"][1] is None
    for name, (jir, expect) in NUM_CASES.items():
        out = tmp / f"num_{name}.methodinputs"
        sf.write_followup(gtree, gparams, sf.parse_jir(jir), out)
        _, fp = sf.read_method_inputs(out)
        got = {"p": fp["p"][1], "q": fp["q"][1]}
        assert got == expect, f"{name}: {got} != {expect}"

    # --- receiver-identity + numeric ---
    kinds = {v: k for v, k, _ in sf.parse_jir(ACOS_JIR)}
    assert kinds == {"x": "num", "this": "id"}, kinds

    # --- string identity ---
    s = tmp / "s.methodinputs"; s.write_text(STR_SRC)
    stree, sparams = sf.read_method_inputs(s)
    out = tmp / "id.methodinputs"
    sf.write_followup(stree, sparams, sf.parse_jir(ID_JIR), out)
    _, fp = sf.read_method_inputs(out)
    assert fp["str1"][1] == "abcd", f"identity changed str1: {fp['str1']}"

    # --- string swap (copyfrom) ---
    a = sf.parse_jir(SWAP_JIR)
    assert {v: k for v, k, _ in a} == {"str1": "copyfrom", "str2": "copyfrom"}, a
    out = tmp / "swap.methodinputs"
    sf.write_followup(stree, sparams, a, out)
    _, fp = sf.read_method_inputs(out)
    assert fp["str1"][1] == "xy" and fp["str2"][1] == "abcd", f"swap wrong: {fp}"

    # --- non-finite doubles serialize in Java format (NaN source from Randoop) ---
    assert sf._cast(float("nan"), "double") == "NaN"
    assert sf._cast(float("inf"), "double") == "Infinity"
    assert sf._cast(float("-inf"), "double") == "-Infinity"
    nan_src = tmp / "nan.methodinputs"
    nan_src.write_text(GCD_SRC.replace('<value class="int">1223</value>',
                                       '<value class="double">NaN</value>')
                              .replace("<clazz>int</clazz>\n      <name>", "<clazz>double</clazz>\n      <name>"))
    nt, np_ = sf.read_method_inputs(nan_src)
    # identity on p (numeric) must round-trip NaN as "NaN", not "nan"
    a = sf.parse_jir("((Math.abs(((double) i_p_f) - ((double) i_p_s)) < 1.0E-4) && "
                     "(Math.abs(((double) i_q_f) - ((double) i_q_s)) < 1.0E-4))")
    o = tmp / "nan_out.methodinputs"
    sf.write_followup(nt, np_, a, o)
    assert "nan</value>" not in o.read_text(), "Python 'nan' leaked into .methodinputs"

    # --- fail-loud on garbage ---
    try:
        sf.parse_jir("totally not a relation")
        raise AssertionError("parse_jir should reject malformed input relations")
    except ValueError:
        pass

    print("OK: setn_followups handles numeric / receiver-id / seq-id / swap, "
          "preserves value-less params, fails loud on garbage")


if __name__ == "__main__":
    main()

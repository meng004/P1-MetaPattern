#!/usr/bin/env python3
"""tests/test_setn_followups.py — Set N follow-up input construction (rule 6).

Validates that scripts/setn_followups.py parses the generated .jir input
relations into the correct constructive transform and applies them to a source
.methodinputs to produce the expected follow-up parameter values.
"""
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import setn_followups as sf  # noqa: E402

SRC_XML = """<ch.usi.methodtest.MethodTest>
  <methodName>gcd</methodName>
  <methodParameters>
    <ch.usi.methodtest.MethodParameter><name>this</name><clazz>MathClass</clazz></ch.usi.methodtest.MethodParameter>
    <ch.usi.methodtest.MethodParameter><name>p</name><clazz>int</clazz><value class="int">1223</value></ch.usi.methodtest.MethodParameter>
    <ch.usi.methodtest.MethodParameter><name>q</name><clazz>int</clazz><value class="int">5</value></ch.usi.methodtest.MethodParameter>
  </methodParameters>
</ch.usi.methodtest.MethodTest>"""

# (jir input relation, expected follow-up (p, q)) for source (p=1223, q=5)
CASES = {
    "perm": ("((Math.abs(((double) i_p_f) - ((double) i_q_s)) < 1.0E-4) && "
             "(Math.abs(((double) i_q_f) - ((double) i_p_s)) < 1.0E-4))", {"p": "5", "q": "1223"}),
    "scale": ("((Math.abs(((double) i_p_f) - (((double) i_p_s) * 2.0)) < 1.0E-4) && "
              "(Math.abs(((double) i_q_f) - (((double) i_q_s) * 2.0)) < 1.0E-4))", {"p": "2446", "q": "10"}),
    "eqref": ("((Math.abs(((double) i_p_f) - ((double) i_p_s)) < 1.0E-4) && "
              "(Math.abs(((double) i_q_f) - (((double) i_q_s) + ((double) i_p_s))) < 1.0E-4))", {"p": "1223", "q": "1228"}),
    "mono": ("((Math.abs(((double) i_p_f) - ((double) i_p_s)) < 1.0E-4) && "
             "(Math.abs(((double) i_q_f) - ((double) i_q_s)) < 1.0E-4))", {"p": "1223", "q": "5"}),
}


def main():
    tmp = Path(tempfile.mkdtemp())
    src = tmp / "src.methodinputs"
    src.write_text(SRC_XML)
    tree, params = sf.read_method_inputs(src)
    assert params["p"] == ("int", "1223"), params
    assert params["q"] == ("int", "5"), params
    assert params["this"][1] is None, "value-less param should parse with None value"

    for name, (jir, expect) in CASES.items():
        assigns = sf.parse_jir(jir)
        assert {v for v, _, _ in assigns} == {"p", "q"}, f"{name}: vars {assigns}"
        out = tmp / f"{name}.methodinputs"
        sf.write_followup(tree, params, assigns, out)
        _, fp = sf.read_method_inputs(out)
        got = {"p": fp["p"][1], "q": fp["q"][1]}
        assert got == expect, f"{name}: got {got}, expected {expect}"
        # 'this' (no value) must be preserved untouched
        assert fp["this"][1] is None, f"{name}: 'this' param corrupted"

    # fail-loud on an unrecognised input-relation form
    try:
        sf.parse_jir("totally not a relation")
        raise AssertionError("parse_jir should reject malformed input relations")
    except ValueError:
        pass

    print(f"OK: setn_followups parses + applies {len(CASES)} transforms "
          "(perm/scale/eqref/mono), preserves value-less params, fails loud on garbage")


if __name__ == "__main__":
    main()

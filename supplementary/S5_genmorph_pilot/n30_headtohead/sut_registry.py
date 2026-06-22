#!/usr/bin/env python3
"""
SUT registry for the n>=30 commons-math head-to-head (Set N vs baselines).

Single source of truth for:
  - the SUT roster (>=30 Apache Commons Math 3.6.1 methods, each admitting at
    least one non-empty NOETHER MetaPattern beyond the plain permutation block G),
  - the per-SUT Set N (NOETHER), Set B (literature single generic MR), and
    Set M (METRIC+ D x R category) metamorphic relations, emitted as JUnit-4
    @Test methods into one test class per SUT,
  - the per-SUT PIT scope (target class, target method, excluded sibling methods).

Why one test class per SUT carrying all three sets: a single PIT run then
attributes every mutant's kill to Set N / Set B / Set M *simultaneously and on
the identical mutant population*, which is exactly the paired design McNemar
needs (the mutant is the matched unit).

Naming convention (parsed back by parse_kill_matrix.py):
  Set N test methods start with  nN_<mr>
  Set B test methods start with  bB_<mr>
  Set M test methods start with  mM_<mr>

Scope precondition (paper's pre-registered design, protocol_path_a_headtohead.md
and S7 README SUT-selection rule): each SUT below has at least one Set N MR that
is NOT a pure S_n permutation invariant -- i.e. it exercises an algebra block
beyond G (a translation T*, scaling/homomorphism L*, or order/identity I* / O_le
relation). The 'blocks' field records which NOETHER blocks each SUT's Set N
touches; every SUT lists a block other than G.
"""

# Each SUT is a dict. The Java body fields are raw JUnit-4 @Test bodies (the
# generator wraps them in `@Test public void <name>() { <body> }`). Helper
# constants (SAMPLES etc.) are emitted by the generator.

CM = "org.apache.commons.math3"

# ---------------------------------------------------------------------------
# Generic body fragments. {M} is replaced with the fully-qualified static call
# prefix, e.g. "org.apache.commons.math3.util.FastMath.sin".
# ---------------------------------------------------------------------------


def _d_oddsym(M):
    # Set N L*/G odd symmetry  f(-x) = -f(x)
    return (f"for (double x : DS) {{ double a={M}(x), b={M}(-x); "
            f"if (Double.isNaN(a)||Double.isInfinite(a)) continue; "
            f"assertEquals(a, -b, 1e-9 + 1e-9*Math.abs(a)); }}")


def _d_evensym(M):
    return (f"for (double x : DS) {{ double a={M}(x), b={M}(-x); "
            f"if (Double.isNaN(a)||Double.isInfinite(a)) continue; "
            f"assertEquals(a, b, 1e-9 + 1e-9*Math.abs(a)); }}")


SUTS = []


def sut(key, cls, method, sig, ret, blocks, excl, set_n, set_b, set_m):
    SUTS.append(dict(key=key, cls=cls, method=method, sig=sig, ret=ret,
                     blocks=blocks, excl=excl,
                     set_n=set_n, set_b=set_b, set_m=set_m))


# ===========================================================================
# Integer / long arithmetic (ArithmeticUtils)
# ===========================================================================

sut("au_gcd_int", f"{CM}.util.ArithmeticUtils", "gcd", "(II)I", "int",
    blocks="G,Lstar,Ole,Istar",
    excl=["gcd(long,long)", "lcm", "pow", "addAndCheck", "subAndCheck",
          "mulAndCheck", "binomialCoefficient", "binomialCoefficientDouble",
          "binomialCoefficientLog", "factorial", "factorialDouble",
          "factorialLog", "stirlingS2", "isPowerOfTwo", "primeFactors"],
    set_n={
        "perm": "for (int[] xy : II) { assertEquals(M.gcd(xy[0],xy[1]), M.gcd(xy[1],xy[0])); }",
        "scale": ("for (int[] xy : II) { int p=xy[0],q=xy[1]; if (Math.abs(p)>1000||Math.abs(q)>1000) continue; "
                  "for (int k : new int[]{2,3,5}) assertEquals((long)k*M.gcd(p,q),(long)M.gcd(k*p,k*q)); }"),
        "mono": ("for (int[] xy : II) { int p=xy[0],q=xy[1]; if (p==0||q==0) continue; "
                 "if (p==Integer.MIN_VALUE||q==Integer.MIN_VALUE) continue; int g=M.gcd(p,q); "
                 "assertTrue(g<=Math.abs((long)p) && g<=Math.abs((long)q)); }"),
        "eqref": ("for (int[] xy : II) { int p=xy[0],q=xy[1]; if (p==0||Math.abs(p)>1000) continue; "
                  "for (int k : new int[]{1,2,-1}) { long s=(long)q+(long)k*(long)p; "
                  "if (s>Integer.MAX_VALUE||s<Integer.MIN_VALUE) continue; "
                  "assertEquals(M.gcd(p,q), M.gcd(p,(int)s)); } }"),
    },
    set_b={  # literature generic: argument-permutation invariance only (Segura 2016 commutativity MR)
        "perm": "for (int[] xy : II) { assertEquals(M.gcd(xy[0],xy[1]), M.gcd(xy[1],xy[0])); }",
    },
    set_m={  # METRIC+ D x R: perm-invariant (D=swap,R=eq), additive_invariant probe, sign_invariant
        "perm_inv": "for (int[] xy : II) { assertEquals(M.gcd(xy[0],xy[1]), M.gcd(xy[1],xy[0])); }",
        "sign_inv": ("for (int[] xy : II) { int p=xy[0],q=xy[1]; if (p==Integer.MIN_VALUE||q==Integer.MIN_VALUE) continue; "
                     "assertEquals(M.gcd(p,q), M.gcd(-p,-q)); assertEquals(M.gcd(p,q), M.gcd(-p,q)); }"),
    })

sut("au_gcd_long", f"{CM}.util.ArithmeticUtils", "gcd", "(JJ)J", "long",
    blocks="G,Lstar,Ole,Istar",
    excl=["gcd(int,int)", "lcm", "pow", "addAndCheck", "subAndCheck",
          "mulAndCheck", "binomialCoefficient", "binomialCoefficientDouble",
          "binomialCoefficientLog", "factorial", "factorialDouble",
          "factorialLog", "stirlingS2", "isPowerOfTwo", "primeFactors"],
    set_n={
        "perm": "for (long[] xy : LL) { assertEquals(M.gcd(xy[0],xy[1]), M.gcd(xy[1],xy[0])); }",
        "scale": ("for (long[] xy : LL) { long p=xy[0],q=xy[1]; if (Math.abs(p)>100000L||Math.abs(q)>100000L) continue; "
                  "for (long k : new long[]{2,3,5}) assertEquals(k*M.gcd(p,q), M.gcd(k*p,k*q)); }"),
        "mono": ("for (long[] xy : LL) { long p=xy[0],q=xy[1]; if (p==0||q==0) continue; "
                 "if (p==Long.MIN_VALUE||q==Long.MIN_VALUE) continue; long g=M.gcd(p,q); "
                 "assertTrue(g<=Math.abs(p) && g<=Math.abs(q)); }"),
        "eqref": ("for (long[] xy : LL) { long p=xy[0],q=xy[1]; if (p==0||Math.abs(p)>100000L) continue; "
                  "for (long k : new long[]{1,2,-1}) { long s=q+k*p; assertEquals(M.gcd(p,q), M.gcd(p,s)); } }"),
    },
    set_b={"perm": "for (long[] xy : LL) { assertEquals(M.gcd(xy[0],xy[1]), M.gcd(xy[1],xy[0])); }"},
    set_m={
        "perm_inv": "for (long[] xy : LL) { assertEquals(M.gcd(xy[0],xy[1]), M.gcd(xy[1],xy[0])); }",
        "sign_inv": ("for (long[] xy : LL) { long p=xy[0],q=xy[1]; if (p==Long.MIN_VALUE||q==Long.MIN_VALUE) continue; "
                     "assertEquals(M.gcd(p,q), M.gcd(-p,-q)); }"),
    })

sut("au_lcm_int", f"{CM}.util.ArithmeticUtils", "lcm", "(II)I", "int",
    blocks="G,Lstar,Istar",
    excl=["gcd", "lcm(long,long)", "pow", "addAndCheck", "subAndCheck",
          "mulAndCheck", "binomialCoefficient", "binomialCoefficientDouble",
          "binomialCoefficientLog", "factorial", "factorialDouble",
          "factorialLog", "stirlingS2", "isPowerOfTwo", "primeFactors"],
    set_n={
        "perm": ("for (int[] xy : II) { int p=xy[0],q=xy[1]; if (p==0||q==0) {assertEquals(0,M.lcm(p,q)); continue;} "
                 "if (Math.abs(p)>30000||Math.abs(q)>30000) continue; assertEquals(M.lcm(p,q), M.lcm(q,p)); }"),
        "sign": ("for (int[] xy : II) { int p=xy[0],q=xy[1]; if (Math.abs(p)>30000||Math.abs(q)>30000) continue; "
                 "if (p==Integer.MIN_VALUE||q==Integer.MIN_VALUE) continue; assertEquals(M.lcm(p,q), M.lcm(-p,q)); }"),
        "gcdlcm": ("for (int[] xy : II) { int p=xy[0],q=xy[1]; if (p==0||q==0) continue; "
                   "if (Math.abs(p)>3000||Math.abs(q)>3000) continue; long prod=Math.abs((long)p*(long)q); "
                   "assertEquals(prod, (long)M.gcd(p,q)*(long)M.lcm(p,q)); }"),
    },
    set_b={"perm": ("for (int[] xy : II) { int p=xy[0],q=xy[1]; if (p==0||q==0) {assertEquals(0,M.lcm(p,q)); continue;} "
                    "if (Math.abs(p)>30000||Math.abs(q)>30000) continue; assertEquals(M.lcm(p,q), M.lcm(q,p)); }")},
    set_m={
        "perm_inv": ("for (int[] xy : II) { int p=xy[0],q=xy[1]; if (p==0||q==0) continue; "
                     "if (Math.abs(p)>30000||Math.abs(q)>30000) continue; assertEquals(M.lcm(p,q), M.lcm(q,p)); }"),
        "sign_inv": ("for (int[] xy : II) { int p=xy[0],q=xy[1]; if (Math.abs(p)>30000||Math.abs(q)>30000) continue; "
                     "if (p==Integer.MIN_VALUE||q==Integer.MIN_VALUE) continue; assertEquals(M.lcm(p,q), M.lcm(p,-q)); }"),
    })

sut("au_addcheck_int", f"{CM}.util.ArithmeticUtils", "addAndCheck", "(II)I", "int",
    blocks="G,Tstar,Istar",
    excl=["gcd", "lcm", "pow", "addAndCheck(long,long)", "subAndCheck",
          "mulAndCheck", "binomialCoefficient", "binomialCoefficientDouble",
          "binomialCoefficientLog", "factorial", "factorialDouble",
          "factorialLog", "stirlingS2", "isPowerOfTwo", "primeFactors"],
    set_n={
        "commute": ("for (int[] xy : IIs) { int p=xy[0],q=xy[1]; assertEquals(M.addAndCheck(p,q), M.addAndCheck(q,p)); }"),
        "identity": ("for (int[] xy : IIs) { int p=xy[0]; assertEquals(p, M.addAndCheck(p,0)); }"),
        "assoc": ("for (int[] xy : IIs) { int p=xy[0],q=xy[1]; int r=3; "
                  "assertEquals(M.addAndCheck(M.addAndCheck(p,q),r), M.addAndCheck(p,M.addAndCheck(q,r))); }"),
    },
    set_b={"commute": "for (int[] xy : IIs) { int p=xy[0],q=xy[1]; assertEquals(M.addAndCheck(p,q), M.addAndCheck(q,p)); }"},
    set_m={
        "perm_inv": "for (int[] xy : IIs) { int p=xy[0],q=xy[1]; assertEquals(M.addAndCheck(p,q), M.addAndCheck(q,p)); }",
        "additive": ("for (int[] xy : IIs) { int p=xy[0],q=xy[1]; "
                     "assertEquals(M.addAndCheck(p,q)+5, M.addAndCheck(p+5,q)); }"),
    })

sut("au_mulcheck_int", f"{CM}.util.ArithmeticUtils", "mulAndCheck", "(II)I", "int",
    blocks="G,Lstar,Istar",
    excl=["gcd", "lcm", "pow", "mulAndCheck(long,long)", "subAndCheck",
          "addAndCheck", "binomialCoefficient", "binomialCoefficientDouble",
          "binomialCoefficientLog", "factorial", "factorialDouble",
          "factorialLog", "stirlingS2", "isPowerOfTwo", "primeFactors"],
    set_n={
        "commute": "for (int[] xy : IIs) { int p=xy[0],q=xy[1]; assertEquals(M.mulAndCheck(p,q), M.mulAndCheck(q,p)); }",
        "identity": "for (int[] xy : IIs) { int p=xy[0]; assertEquals(p, M.mulAndCheck(p,1)); assertEquals(0, M.mulAndCheck(p,0)); }",
        "sign": ("for (int[] xy : IIs) { int p=xy[0],q=xy[1]; if (p==Integer.MIN_VALUE||q==Integer.MIN_VALUE) continue; "
                 "if ((long)Math.abs((long)p)*Math.abs((long)q) > Integer.MAX_VALUE) continue; "
                 "assertEquals(-M.mulAndCheck(p,q), M.mulAndCheck(-p,q)); }"),
    },
    set_b={"commute": "for (int[] xy : IIs) { int p=xy[0],q=xy[1]; assertEquals(M.mulAndCheck(p,q), M.mulAndCheck(q,p)); }"},
    set_m={
        "perm_inv": "for (int[] xy : IIs) { int p=xy[0],q=xy[1]; assertEquals(M.mulAndCheck(p,q), M.mulAndCheck(q,p)); }",
        "sign_flip": ("for (int[] xy : IIs) { int p=xy[0],q=xy[1]; if (p==Integer.MIN_VALUE||q==Integer.MIN_VALUE) continue; "
                      "if ((long)Math.abs((long)p)*Math.abs((long)q) > Integer.MAX_VALUE) continue; "
                      "assertEquals(M.mulAndCheck(p,q), -M.mulAndCheck(-p,q)); }"),
    })

sut("au_subcheck_int", f"{CM}.util.ArithmeticUtils", "subAndCheck", "(II)I", "int",
    blocks="G,Tstar,Istar",
    excl=["gcd", "lcm", "pow", "subAndCheck(long,long)", "mulAndCheck",
          "addAndCheck", "binomialCoefficient", "binomialCoefficientDouble",
          "binomialCoefficientLog", "factorial", "factorialDouble",
          "factorialLog", "stirlingS2", "isPowerOfTwo", "primeFactors"],
    set_n={
        "antisym": ("for (int[] xy : IIs) { int p=xy[0],q=xy[1]; "
                    "long fwd=(long)M.subAndCheck(p,q); long bwd; "
                    "try { bwd=(long)M.subAndCheck(q,p);} catch(Exception e){continue;} assertEquals(fwd, -bwd); }"),
        "identity": "for (int[] xy : IIs) { int p=xy[0]; assertEquals(p, M.subAndCheck(p,0)); assertEquals(0, M.subAndCheck(p,p)); }",
        "shift": ("for (int[] xy : IIs) { int p=xy[0],q=xy[1]; "
                  "assertEquals(M.subAndCheck(p,q), M.subAndCheck(p+4,q+4)); }"),
    },
    set_b={"identity": "for (int[] xy : IIs) { int p=xy[0]; assertEquals(0, M.subAndCheck(p,p)); }"},
    set_m={
        "additive": "for (int[] xy : IIs) { int p=xy[0],q=xy[1]; assertEquals(M.subAndCheck(p,q), M.subAndCheck(p+4,q+4)); }",
        "sign_flip": ("for (int[] xy : IIs) { int p=xy[0],q=xy[1]; long f=(long)M.subAndCheck(p,q); long b; "
                      "try{b=(long)M.subAndCheck(q,p);}catch(Exception e){continue;} assertEquals(f,-b); }"),
    })

sut("au_pow_int", f"{CM}.util.ArithmeticUtils", "pow", "(II)I", "int",
    blocks="Lstar,Istar",
    excl=["gcd", "lcm", "pow(int,long)", "pow(long,int)", "pow(long,long)",
          "pow(java.math.BigInteger,int)", "pow(java.math.BigInteger,long)",
          "pow(java.math.BigInteger,java.math.BigInteger)",
          "subAndCheck", "mulAndCheck", "addAndCheck", "binomialCoefficient",
          "binomialCoefficientDouble", "binomialCoefficientLog", "factorial",
          "factorialDouble", "factorialLog", "stirlingS2", "isPowerOfTwo", "primeFactors"],
    set_n={
        "expsum": ("for (int[] xy : POWI) { int k=xy[0],e=xy[1]; if (e<0) continue; "
                   "long lhs=(long)M.pow(k,e+1); long rhs=(long)M.pow(k,e)*(long)k; "
                   "if (Math.abs(lhs)>Integer.MAX_VALUE||Math.abs(rhs)>Integer.MAX_VALUE) continue; assertEquals(lhs,rhs); }"),
        "base0_1": "for (int e=0;e<6;e++){ assertEquals(1, M.pow(1,e)); } assertEquals(1,M.pow(7,0));",
        "prodbase": ("for (int[] xy : POWI) { int k=xy[0],e=xy[1]; if (e<0||e>6) continue; "
                     "long lhs=(long)M.pow(k,e)*(long)M.pow(2,e); long rhs=(long)M.pow(k*2,e); "
                     "if (Math.abs(lhs)>Integer.MAX_VALUE||Math.abs(rhs)>Integer.MAX_VALUE) continue; assertEquals(lhs,rhs); }"),
    },
    set_b={"base0_1": "assertEquals(1,M.pow(7,0)); assertEquals(1,M.pow(1,5));"},
    set_m={
        "scale_homog": ("for (int[] xy : POWI) { int k=xy[0],e=xy[1]; if (e<0||e>6) continue; "
                        "long lhs=(long)M.pow(k,e)*(long)M.pow(2,e); long rhs=(long)M.pow(k*2,e); "
                        "if (Math.abs(lhs)>Integer.MAX_VALUE||Math.abs(rhs)>Integer.MAX_VALUE) continue; assertEquals(lhs,rhs); }"),
    })

# ===========================================================================
# Combinatorics
# ===========================================================================

sut("cu_binom", f"{CM}.util.CombinatoricsUtils", "binomialCoefficient", "(II)J", "long",
    blocks="G,Istar,Ole",
    excl=["binomialCoefficientDouble", "binomialCoefficientLog", "factorial",
          "factorialDouble", "factorialLog", "stirlingS2", "checkBinomial",
          "combinationsIterator"],
    set_n={
        "symmetry": ("for (int[] xy : NK) { int n=xy[0],k=xy[1]; if (n>60||k<0||k>n) continue; "
                     "assertEquals(M.binomialCoefficient(n,k), M.binomialCoefficient(n,n-k)); }"),
        "pascal": ("for (int[] xy : NK) { int n=xy[0],k=xy[1]; if (n<1||n>60||k<1||k>n-1) continue; "
                   "assertEquals(M.binomialCoefficient(n,k), M.binomialCoefficient(n-1,k-1)+M.binomialCoefficient(n-1,k)); }"),
        "edge1": "for (int n=0;n<=40;n++){ assertEquals(1L, M.binomialCoefficient(n,0)); assertEquals(1L, M.binomialCoefficient(n,n)); }",
    },
    set_b={"symmetry": ("for (int[] xy : NK) { int n=xy[0],k=xy[1]; if (n>60||k<0||k>n) continue; "
                        "assertEquals(M.binomialCoefficient(n,k), M.binomialCoefficient(n,n-k)); }")},
    set_m={
        "perm_inv": ("for (int[] xy : NK) { int n=xy[0],k=xy[1]; if (n>60||k<0||k>n) continue; "
                     "assertEquals(M.binomialCoefficient(n,k), M.binomialCoefficient(n,n-k)); }"),
    })

sut("cu_factorial", f"{CM}.util.CombinatoricsUtils", "factorial", "(I)J", "long",
    blocks="Lstar,Istar,Ole",
    excl=["binomialCoefficient", "binomialCoefficientDouble", "binomialCoefficientLog",
          "factorialDouble", "factorialLog", "stirlingS2", "checkBinomial",
          "combinationsIterator"],
    set_n={
        "recur": "for (int n=1;n<=20;n++){ assertEquals(M.factorial(n), (long)n*M.factorial(n-1)); }",
        "base": "assertEquals(1L, M.factorial(0)); assertEquals(1L, M.factorial(1));",
        "mono": "for (int n=1;n<=20;n++){ assertTrue(M.factorial(n) >= M.factorial(n-1)); }",
    },
    set_b={"base": "assertEquals(1L, M.factorial(0));"},
    set_m={
        "scale_homog": "for (int n=1;n<=20;n++){ assertEquals(M.factorial(n), (long)n*M.factorial(n-1)); }",
    })

sut("au_stirling", f"{CM}.util.ArithmeticUtils", "stirlingS2", "(II)J", "long",
    blocks="Istar,Ole",
    excl=["gcd", "lcm", "pow", "subAndCheck", "mulAndCheck", "addAndCheck",
          "binomialCoefficient", "binomialCoefficientDouble", "binomialCoefficientLog",
          "factorial", "factorialDouble", "factorialLog", "isPowerOfTwo", "primeFactors"],
    set_n={
        "edge_nn": "for (int n=1;n<=18;n++){ assertEquals(1L, M.stirlingS2(n,n)); }",
        "edge_n1": "for (int n=1;n<=18;n++){ assertEquals(1L, M.stirlingS2(n,1)); }",
        "recur": ("for (int[] xy : NK) { int n=xy[0],k=xy[1]; if (n<2||n>18||k<2||k>n-1) continue; "
                  "assertEquals(M.stirlingS2(n,k), (long)k*M.stirlingS2(n-1,k)+M.stirlingS2(n-1,k-1)); }"),
    },
    set_b={"edge_nn": "for (int n=1;n<=18;n++){ assertEquals(1L, M.stirlingS2(n,n)); }"},
    set_m={
        "perm_inv": "for (int n=1;n<=18;n++){ assertEquals(1L, M.stirlingS2(n,1)); }",
    })

# ===========================================================================
# FastMath: even/odd transcendental + algebraic
# ===========================================================================

def _fm(name):
    return f"{CM}.util.FastMath." + name


# helper to build excl lists for FastMath: exclude a large set of siblings,
# keep only the target (PIT excludedMethods is by simple name, so list names).
FM_ALL = ["abs", "acos", "acosh", "asin", "asinh", "atan", "atan2", "atanh",
          "cbrt", "ceil", "copySign", "cos", "cosh", "exp", "expm1", "floor",
          "floorDiv", "floorMod", "getExponent", "hypot", "log", "log10",
          "log1p", "max", "min", "nextAfter", "nextUp", "nextDown", "pow",
          "random", "rint", "round", "scalb", "signum", "sin", "sinh", "sqrt",
          "tan", "tanh", "toDegrees", "toIntExact", "toRadians", "ulp",
          "IEEEremainder", "abs"]


def fm_excl(keep):
    return [m for m in FM_ALL if m != keep]


sut("fm_hypot", f"{CM}.util.FastMath", "hypot", "(DD)D", "double",
    blocks="G,Lstar,Istar",
    excl=fm_excl("hypot"),
    set_n={
        "perm": "for (double[] xy : DD) { assertEquals(M.hypot(xy[0],xy[1]), M.hypot(xy[1],xy[0]), 1e-12); }",
        "homog": ("for (double[] xy : DD) { double a=xy[0],b=xy[1]; for (double c : new double[]{2.0,0.5,3.0}) {"
                  "double lhs=M.hypot(c*a,c*b), rhs=Math.abs(c)*M.hypot(a,b); "
                  "assertEquals(rhs, lhs, 1e-9 + 1e-9*Math.abs(rhs)); } }"),
        "sign": "for (double[] xy : DD) { assertEquals(M.hypot(xy[0],xy[1]), M.hypot(-xy[0],xy[1]), 1e-12); }",
        "lower": "for (double[] xy : DD) { double h=M.hypot(xy[0],xy[1]); assertTrue(h >= Math.abs(xy[0]) - 1e-9); }",
    },
    set_b={"perm": "for (double[] xy : DD) { assertEquals(M.hypot(xy[0],xy[1]), M.hypot(xy[1],xy[0]), 1e-12); }"},
    set_m={
        "perm_inv": "for (double[] xy : DD) { assertEquals(M.hypot(xy[0],xy[1]), M.hypot(xy[1],xy[0]), 1e-12); }",
        "scale_homog": ("for (double[] xy : DD) { double a=xy[0],b=xy[1]; for (double c : new double[]{2.0,0.5,3.0}) {"
                        "double lhs=M.hypot(c*a,c*b), rhs=Math.abs(c)*M.hypot(a,b); "
                        "assertEquals(rhs, lhs, 1e-9 + 1e-9*Math.abs(rhs)); } }"),
        "sign_inv": "for (double[] xy : DD) { assertEquals(M.hypot(xy[0],xy[1]), M.hypot(-xy[0],-xy[1]), 1e-12); }",
    })

sut("fm_signum_d", f"{CM}.util.FastMath", "signum", "(D)D", "double",
    blocks="G,Lstar",
    excl=fm_excl("signum"),
    set_n={
        "odd": "for (double x : DS) { if (x==0.0) continue; assertEquals(M.signum(x), -M.signum(-x), 0.0); }",
        "posscale": "for (double x : DS) { for (double c : new double[]{2.0,0.5,10.0}) assertEquals(M.signum(x), M.signum(c*x), 0.0); }",
        "range": "for (double x : DS) { double s=M.signum(x); assertTrue(s==-1.0||s==0.0||s==1.0||Double.isNaN(s)); }",
    },
    set_b={"range": "for (double x : DS) { double s=M.signum(x); assertTrue(s==-1.0||s==0.0||s==1.0||Double.isNaN(s)); }"},
    set_m={
        "sign_flip": "for (double x : DS) { if (x==0.0) continue; assertEquals(M.signum(x), -M.signum(-x), 0.0); }",
        "scale_homog": "for (double x : DS) { for (double c : new double[]{2.0,0.5,10.0}) assertEquals(M.signum(x), M.signum(c*x), 0.0); }",
    })

sut("fm_abs_d", f"{CM}.util.FastMath", "abs", "(D)D", "double",
    blocks="Lstar,Istar",
    excl=fm_excl("abs"),
    set_n={
        "even": "for (double x : DS) { assertEquals(M.abs(x), M.abs(-x), 0.0); }",
        "idem": "for (double x : DS) { assertEquals(M.abs(x), M.abs(M.abs(x)), 0.0); }",
        "nonneg": "for (double x : DS) { if (Double.isNaN(x)) continue; assertTrue(M.abs(x) >= 0.0); }",
        "homog": "for (double x : DS) { for (double c : new double[]{2.0,3.0,0.5}) assertEquals(c*M.abs(x), M.abs(c*x), 1e-9+1e-9*c*M.abs(x)); }",
    },
    set_b={"nonneg": "for (double x : DS) { if (Double.isNaN(x)) continue; assertTrue(M.abs(x) >= 0.0); }"},
    set_m={
        "sign_inv": "for (double x : DS) { assertEquals(M.abs(x), M.abs(-x), 0.0); }",
        "scale_homog": "for (double x : DS) { for (double c : new double[]{2.0,3.0,0.5}) assertEquals(c*M.abs(x), M.abs(c*x), 1e-9+1e-9*c*M.abs(x)); }",
    })

sut("fm_max_d", f"{CM}.util.FastMath", "max", "(DD)D", "double",
    blocks="G,Tstar,Istar",
    excl=fm_excl("max"),
    set_n={
        "commute": "for (double[] xy : DD) { assertEquals(M.max(xy[0],xy[1]), M.max(xy[1],xy[0]), 0.0); }",
        "idem": "for (double x : DS) { assertEquals(x, M.max(x,x), 0.0); }",
        "shift": "for (double[] xy : DD) { double c=2.5; assertEquals(M.max(xy[0],xy[1])+c, M.max(xy[0]+c,xy[1]+c), 1e-9); }",
        "ge": "for (double[] xy : DD) { double m=M.max(xy[0],xy[1]); assertTrue(m>=xy[0]-1e-12 && m>=xy[1]-1e-12); }",
    },
    set_b={"commute": "for (double[] xy : DD) { assertEquals(M.max(xy[0],xy[1]), M.max(xy[1],xy[0]), 0.0); }"},
    set_m={
        "perm_inv": "for (double[] xy : DD) { assertEquals(M.max(xy[0],xy[1]), M.max(xy[1],xy[0]), 0.0); }",
        "additive": "for (double[] xy : DD) { double c=2.5; assertEquals(M.max(xy[0],xy[1])+c, M.max(xy[0]+c,xy[1]+c), 1e-9); }",
    })

sut("fm_min_d", f"{CM}.util.FastMath", "min", "(DD)D", "double",
    blocks="G,Tstar,Istar",
    excl=fm_excl("min"),
    set_n={
        "commute": "for (double[] xy : DD) { assertEquals(M.min(xy[0],xy[1]), M.min(xy[1],xy[0]), 0.0); }",
        "idem": "for (double x : DS) { assertEquals(x, M.min(x,x), 0.0); }",
        "shift": "for (double[] xy : DD) { double c=2.5; assertEquals(M.min(xy[0],xy[1])+c, M.min(xy[0]+c,xy[1]+c), 1e-9); }",
        "le": "for (double[] xy : DD) { double m=M.min(xy[0],xy[1]); assertTrue(m<=xy[0]+1e-12 && m<=xy[1]+1e-12); }",
    },
    set_b={"commute": "for (double[] xy : DD) { assertEquals(M.min(xy[0],xy[1]), M.min(xy[1],xy[0]), 0.0); }"},
    set_m={
        "perm_inv": "for (double[] xy : DD) { assertEquals(M.min(xy[0],xy[1]), M.min(xy[1],xy[0]), 0.0); }",
        "additive": "for (double[] xy : DD) { double c=2.5; assertEquals(M.min(xy[0],xy[1])+c, M.min(xy[0]+c,xy[1]+c), 1e-9); }",
    })

sut("fm_floor", f"{CM}.util.FastMath", "floor", "(D)D", "double",
    blocks="Tstar,Istar,Ole",
    excl=fm_excl("floor"),
    set_n={
        "intshift": "for (double x : DSF) { for (int k : new int[]{1,2,-3}) assertEquals(M.floor(x)+k, M.floor(x+k), 0.0); }",
        "idem": "for (double x : DSF) { assertEquals(M.floor(x), M.floor(M.floor(x)), 0.0); }",
        "le": "for (double x : DSF) { if (Double.isInfinite(x)||Double.isNaN(x)) continue; assertTrue(M.floor(x) <= x); }",
        "mono": "for (double x : DSF) { assertTrue(M.floor(x) <= M.floor(x+1.0)); }",
    },
    set_b={"le": "for (double x : DSF) { if (Double.isInfinite(x)||Double.isNaN(x)) continue; assertTrue(M.floor(x) <= x); }"},
    set_m={
        "additive": "for (double x : DSF) { for (int k : new int[]{1,2,-3}) assertEquals(M.floor(x)+k, M.floor(x+k), 0.0); }",
    })

sut("fm_ceil", f"{CM}.util.FastMath", "ceil", "(D)D", "double",
    blocks="Tstar,Istar,Ole",
    excl=fm_excl("ceil"),
    set_n={
        "intshift": "for (double x : DSF) { for (int k : new int[]{1,2,-3}) assertEquals(M.ceil(x)+k, M.ceil(x+k), 0.0); }",
        "idem": "for (double x : DSF) { assertEquals(M.ceil(x), M.ceil(M.ceil(x)), 0.0); }",
        "ge": "for (double x : DSF) { if (Double.isInfinite(x)||Double.isNaN(x)) continue; assertTrue(M.ceil(x) >= x); }",
        "reflect": "for (double x : DSF) { if (Double.isInfinite(x)||Double.isNaN(x)) continue; assertEquals(M.ceil(x), -M.floor(-x), 0.0); }",
    },
    set_b={"ge": "for (double x : DSF) { if (Double.isInfinite(x)||Double.isNaN(x)) continue; assertTrue(M.ceil(x) >= x); }"},
    set_m={
        "additive": "for (double x : DSF) { for (int k : new int[]{1,2,-3}) assertEquals(M.ceil(x)+k, M.ceil(x+k), 0.0); }",
    })

sut("fm_exp", f"{CM}.util.FastMath", "exp", "(D)D", "double",
    blocks="Lstar,Ole",
    excl=fm_excl("exp"),
    set_n={
        "addmul": ("for (double[] xy : DDs) { double a=xy[0],b=xy[1]; if (Math.abs(a)>20||Math.abs(b)>20) continue; "
                   "double lhs=M.exp(a+b), rhs=M.exp(a)*M.exp(b); assertEquals(rhs, lhs, 1e-9*Math.abs(rhs)+1e-12); }"),
        "zero": "assertEquals(1.0, M.exp(0.0), 1e-15);",
        "mono": ("for (double[] xy : DDs) { double a=xy[0]; if (Math.abs(a)>20) continue; "
                 "assertTrue(M.exp(a) <= M.exp(a+0.5)); }"),
        "recip": "for (double x : DSE) { if (Math.abs(x)>20) continue; assertEquals(1.0/M.exp(x), M.exp(-x), 1e-9*M.exp(-x)+1e-12); }",
    },
    set_b={"zero": "assertEquals(1.0, M.exp(0.0), 1e-15);"},
    set_m={
        "scale_homog": ("for (double[] xy : DDs) { double a=xy[0],b=xy[1]; if (Math.abs(a)>20||Math.abs(b)>20) continue; "
                        "double lhs=M.exp(a+b), rhs=M.exp(a)*M.exp(b); assertEquals(rhs, lhs, 1e-9*Math.abs(rhs)+1e-12); }"),
    })

sut("fm_log", f"{CM}.util.FastMath", "log", "(D)D", "double",
    blocks="Lstar,Ole",
    excl=fm_excl("log"),
    set_n={
        "mullog": ("for (double[] xy : DDP) { double a=xy[0],b=xy[1]; if (a<=0||b<=0) continue; "
                   "double lhs=M.log(a*b), rhs=M.log(a)+M.log(b); assertEquals(rhs, lhs, 1e-9*Math.abs(rhs)+1e-12); }"),
        "one": "assertEquals(0.0, M.log(1.0), 1e-15);",
        "mono": "for (double[] xy : DDP) { double a=xy[0]; if (a<=0) continue; assertTrue(M.log(a) <= M.log(a*1.5)); }",
        "powk": "for (double[] xy : DDP) { double a=xy[0]; if (a<=0) continue; assertEquals(3.0*M.log(a), M.log(a*a*a), 1e-9*Math.abs(3.0*M.log(a))+1e-12); }",
    },
    set_b={"one": "assertEquals(0.0, M.log(1.0), 1e-15);"},
    set_m={
        "scale_homog": ("for (double[] xy : DDP) { double a=xy[0],b=xy[1]; if (a<=0||b<=0) continue; "
                        "double lhs=M.log(a*b), rhs=M.log(a)+M.log(b); assertEquals(rhs, lhs, 1e-9*Math.abs(rhs)+1e-12); }"),
    })

sut("fm_log10", f"{CM}.util.FastMath", "log10", "(D)D", "double",
    blocks="Lstar,Ole",
    excl=fm_excl("log10"),
    set_n={
        "mullog": ("for (double[] xy : DDP) { double a=xy[0],b=xy[1]; if (a<=0||b<=0) continue; "
                   "double lhs=M.log10(a*b), rhs=M.log10(a)+M.log10(b); assertEquals(rhs, lhs, 1e-9*Math.abs(rhs)+1e-12); }"),
        "powers": "for (int k=0;k<8;k++){ assertEquals((double)k, M.log10(M.pow(10.0,(double)k)), 1e-9); }",
        "one": "assertEquals(0.0, M.log10(1.0), 1e-15);",
    },
    set_b={"one": "assertEquals(0.0, M.log10(1.0), 1e-15);"},
    set_m={
        "scale_homog": ("for (double[] xy : DDP) { double a=xy[0],b=xy[1]; if (a<=0||b<=0) continue; "
                        "double lhs=M.log10(a*b), rhs=M.log10(a)+M.log10(b); assertEquals(rhs, lhs, 1e-9*Math.abs(rhs)+1e-12); }"),
    })

sut("fm_log1p", f"{CM}.util.FastMath", "log1p", "(D)D", "double",
    blocks="Lstar,Ole",
    excl=fm_excl("log1p"),
    set_n={
        "zero": "assertEquals(0.0, M.log1p(0.0), 1e-15);",
        "mono": "for (double x : DSP) { assertTrue(M.log1p(x) <= M.log1p(x+0.5)); }",
        "consistency": "for (double x : DSP) { assertEquals(M.log(1.0+x), M.log1p(x), 1e-9*Math.abs(M.log1p(x))+1e-12); }",
    },
    set_b={"zero": "assertEquals(0.0, M.log1p(0.0), 1e-15);"},
    set_m={
        "additive": "for (double x : DSP) { assertEquals(M.log(1.0+x), M.log1p(x), 1e-9*Math.abs(M.log1p(x))+1e-12); }",
    })

sut("fm_expm1", f"{CM}.util.FastMath", "expm1", "(D)D", "double",
    blocks="Lstar,Ole",
    excl=fm_excl("expm1"),
    set_n={
        "zero": "assertEquals(0.0, M.expm1(0.0), 1e-15);",
        "mono": "for (double x : DSE) { if (Math.abs(x)>20) continue; assertTrue(M.expm1(x) <= M.expm1(x+0.5)); }",
        "consistency": "for (double x : DSE) { if (Math.abs(x)>20) continue; assertEquals(M.exp(x)-1.0, M.expm1(x), 1e-9*Math.abs(M.expm1(x))+1e-9); }",
    },
    set_b={"zero": "assertEquals(0.0, M.expm1(0.0), 1e-15);"},
    set_m={
        "additive": "for (double x : DSE) { if (Math.abs(x)>20) continue; assertEquals(M.exp(x)-1.0, M.expm1(x), 1e-9*Math.abs(M.expm1(x))+1e-9); }",
    })

sut("fm_sqrt", f"{CM}.util.FastMath", "sqrt", "(D)D", "double",
    blocks="Lstar,Ole",
    excl=fm_excl("sqrt"),
    set_n={
        "mulsplit": ("for (double[] xy : DDP) { double a=xy[0],b=xy[1]; if (a<0||b<0) continue; "
                     "double lhs=M.sqrt(a*b), rhs=M.sqrt(a)*M.sqrt(b); assertEquals(rhs, lhs, 1e-9*Math.abs(rhs)+1e-12); }"),
        "square": "for (double x : DSP) { if (x<0||x>1e7) continue; assertEquals(x, M.sqrt(x*x), 1e-9*x+1e-9); }",
        "mono": "for (double x : DSP) { if (x<0) continue; assertTrue(M.sqrt(x) <= M.sqrt(x+1.0)); }",
    },
    set_b={"square": "for (double x : DSP) { if (x<0||x>1e7) continue; assertEquals(x, M.sqrt(x*x), 1e-9*x+1e-9); }"},
    set_m={
        "scale_homog": ("for (double[] xy : DDP) { double a=xy[0],b=xy[1]; if (a<0||b<0) continue; "
                        "double lhs=M.sqrt(a*b), rhs=M.sqrt(a)*M.sqrt(b); assertEquals(rhs, lhs, 1e-9*Math.abs(rhs)+1e-12); }"),
    })

sut("fm_cbrt", f"{CM}.util.FastMath", "cbrt", "(D)D", "double",
    blocks="G,Lstar,Ole",
    excl=fm_excl("cbrt"),
    set_n={
        "odd": "for (double x : DS) { assertEquals(M.cbrt(x), -M.cbrt(-x), 1e-9+1e-9*Math.abs(M.cbrt(x))); }",
        "cube": "for (double x : DS) { if (Math.abs(x)>1000) continue; assertEquals(x, M.cbrt(x*x*x), 1e-6+1e-9*Math.abs(x)); }",
        "mono": "for (double x : DS) { if (Double.isNaN(x)) continue; assertTrue(M.cbrt(x) <= M.cbrt(x+1.0)+1e-12); }",
    },
    set_b={"odd": "for (double x : DS) { assertEquals(M.cbrt(x), -M.cbrt(-x), 1e-9+1e-9*Math.abs(M.cbrt(x))); }"},
    set_m={
        "sign_flip": "for (double x : DS) { assertEquals(M.cbrt(x), -M.cbrt(-x), 1e-9+1e-9*Math.abs(M.cbrt(x))); }",
    })

sut("fm_sin", f"{CM}.util.FastMath", "sin", "(D)D", "double",
    blocks="G,Lstar,Ole",
    excl=fm_excl("sin"),
    set_n={
        "odd": "for (double x : DT) { assertEquals(M.sin(x), -M.sin(-x), 1e-12+1e-12*Math.abs(M.sin(x))); }",
        "period": "for (double x : DT) { assertEquals(M.sin(x), M.sin(x+2.0*Math.PI), 1e-9); }",
        "bound": "for (double x : DT) { double s=M.sin(x); assertTrue(s<=1.0+1e-12 && s>=-1.0-1e-12); }",
        "shiftpi": "for (double x : DT) { assertEquals(M.sin(x), -M.sin(x+Math.PI), 1e-9); }",
    },
    set_b={"bound": "for (double x : DT) { double s=M.sin(x); assertTrue(s<=1.0+1e-12 && s>=-1.0-1e-12); }"},
    set_m={
        "sign_flip": "for (double x : DT) { assertEquals(M.sin(x), -M.sin(-x), 1e-12+1e-12*Math.abs(M.sin(x))); }",
        "additive": "for (double x : DT) { assertEquals(M.sin(x), M.sin(x+2.0*Math.PI), 1e-9); }",
    })

sut("fm_cos", f"{CM}.util.FastMath", "cos", "(D)D", "double",
    blocks="G,Lstar,Ole",
    excl=fm_excl("cos"),
    set_n={
        "even": "for (double x : DT) { assertEquals(M.cos(x), M.cos(-x), 1e-12+1e-12*Math.abs(M.cos(x))); }",
        "period": "for (double x : DT) { assertEquals(M.cos(x), M.cos(x+2.0*Math.PI), 1e-9); }",
        "bound": "for (double x : DT) { double s=M.cos(x); assertTrue(s<=1.0+1e-12 && s>=-1.0-1e-12); }",
        "shiftpi": "for (double x : DT) { assertEquals(M.cos(x), -M.cos(x+Math.PI), 1e-9); }",
    },
    set_b={"bound": "for (double x : DT) { double s=M.cos(x); assertTrue(s<=1.0+1e-12 && s>=-1.0-1e-12); }"},
    set_m={
        "sign_inv": "for (double x : DT) { assertEquals(M.cos(x), M.cos(-x), 1e-12+1e-12*Math.abs(M.cos(x))); }",
        "additive": "for (double x : DT) { assertEquals(M.cos(x), M.cos(x+2.0*Math.PI), 1e-9); }",
    })

sut("fm_tan", f"{CM}.util.FastMath", "tan", "(D)D", "double",
    blocks="G,Lstar,Ole",
    excl=fm_excl("tan"),
    set_n={
        "odd": "for (double x : DTt) { assertEquals(M.tan(x), -M.tan(-x), 1e-9+1e-9*Math.abs(M.tan(x))); }",
        "period": "for (double x : DTt) { assertEquals(M.tan(x), M.tan(x+Math.PI), 1e-7+1e-7*Math.abs(M.tan(x))); }",
        "quotient": "for (double x : DTt) { double c=M.cos(x); if (Math.abs(c)<1e-3) continue; assertEquals(M.sin(x)/c, M.tan(x), 1e-7+1e-7*Math.abs(M.tan(x))); }",
    },
    set_b={"odd": "for (double x : DTt) { assertEquals(M.tan(x), -M.tan(-x), 1e-9+1e-9*Math.abs(M.tan(x))); }"},
    set_m={
        "sign_flip": "for (double x : DTt) { assertEquals(M.tan(x), -M.tan(-x), 1e-9+1e-9*Math.abs(M.tan(x))); }",
    })

sut("fm_sinh", f"{CM}.util.FastMath", "sinh", "(D)D", "double",
    blocks="G,Lstar,Ole",
    excl=fm_excl("sinh"),
    set_n={
        "odd": "for (double x : DSH) { assertEquals(M.sinh(x), -M.sinh(-x), 1e-9+1e-9*Math.abs(M.sinh(x))); }",
        "zero": "assertEquals(0.0, M.sinh(0.0), 1e-15);",
        "mono": "for (double x : DSH) { assertTrue(M.sinh(x) <= M.sinh(x+0.25)); }",
    },
    set_b={"odd": "for (double x : DSH) { assertEquals(M.sinh(x), -M.sinh(-x), 1e-9+1e-9*Math.abs(M.sinh(x))); }"},
    set_m={
        "sign_flip": "for (double x : DSH) { assertEquals(M.sinh(x), -M.sinh(-x), 1e-9+1e-9*Math.abs(M.sinh(x))); }",
    })

sut("fm_cosh", f"{CM}.util.FastMath", "cosh", "(D)D", "double",
    blocks="G,Lstar,Ole",
    excl=fm_excl("cosh"),
    set_n={
        "even": "for (double x : DSH) { assertEquals(M.cosh(x), M.cosh(-x), 1e-9+1e-9*Math.abs(M.cosh(x))); }",
        "lower": "for (double x : DSH) { assertTrue(M.cosh(x) >= 1.0 - 1e-12); }",
        "zero": "assertEquals(1.0, M.cosh(0.0), 1e-15);",
    },
    set_b={"lower": "for (double x : DSH) { assertTrue(M.cosh(x) >= 1.0 - 1e-12); }"},
    set_m={
        "sign_inv": "for (double x : DSH) { assertEquals(M.cosh(x), M.cosh(-x), 1e-9+1e-9*Math.abs(M.cosh(x))); }",
    })

sut("fm_tanh", f"{CM}.util.FastMath", "tanh", "(D)D", "double",
    blocks="G,Lstar,Ole",
    excl=fm_excl("tanh"),
    set_n={
        "odd": "for (double x : DSH) { assertEquals(M.tanh(x), -M.tanh(-x), 1e-9+1e-9*Math.abs(M.tanh(x))); }",
        "bound": "for (double x : DSH) { double t=M.tanh(x); assertTrue(t<1.0+1e-12 && t>-1.0-1e-12); }",
        "mono": "for (double x : DSH) { assertTrue(M.tanh(x) <= M.tanh(x+0.25)+1e-12); }",
    },
    set_b={"bound": "for (double x : DSH) { double t=M.tanh(x); assertTrue(t<1.0+1e-12 && t>-1.0-1e-12); }"},
    set_m={
        "sign_flip": "for (double x : DSH) { assertEquals(M.tanh(x), -M.tanh(-x), 1e-9+1e-9*Math.abs(M.tanh(x))); }",
    })

sut("fm_atan", f"{CM}.util.FastMath", "atan", "(D)D", "double",
    blocks="G,Lstar,Ole",
    excl=fm_excl("atan"),
    set_n={
        "odd": "for (double x : DS) { if (Double.isNaN(x)) continue; assertEquals(M.atan(x), -M.atan(-x), 1e-12+1e-12*Math.abs(M.atan(x))); }",
        "bound": "for (double x : DS) { if (Double.isNaN(x)) continue; double a=M.atan(x); assertTrue(a<Math.PI/2+1e-12 && a>-Math.PI/2-1e-12); }",
        "mono": "for (double x : DS) { if (Double.isNaN(x)||Double.isInfinite(x)) continue; assertTrue(M.atan(x) <= M.atan(x+1.0)+1e-12); }",
    },
    set_b={"bound": "for (double x : DS) { if (Double.isNaN(x)) continue; double a=M.atan(x); assertTrue(a<Math.PI/2+1e-12 && a>-Math.PI/2-1e-12); }"},
    set_m={
        "sign_flip": "for (double x : DS) { if (Double.isNaN(x)) continue; assertEquals(M.atan(x), -M.atan(-x), 1e-12+1e-12*Math.abs(M.atan(x))); }",
    })

sut("fm_toradians", f"{CM}.util.FastMath", "toRadians", "(D)D", "double",
    blocks="Lstar,Istar",
    excl=fm_excl("toRadians"),
    set_n={
        "homog": "for (double x : DS) { if (Math.abs(x)>1e6) continue; for (double c : new double[]{2.0,3.0,0.5}) assertEquals(c*M.toRadians(x), M.toRadians(c*x), 1e-12+1e-12*Math.abs(c*M.toRadians(x))); }",
        "additive": "for (double[] xy : DDs) { double a=xy[0],b=xy[1]; if (Math.abs(a)>1e6||Math.abs(b)>1e6) continue; assertEquals(M.toRadians(a)+M.toRadians(b), M.toRadians(a+b), 1e-12+1e-12*Math.abs(M.toRadians(a+b))); }",
        "inverse": "for (double x : DS) { if (Math.abs(x)>1e6) continue; assertEquals(x, M.toDegrees(M.toRadians(x)), 1e-9+1e-12*Math.abs(x)); }",
    },
    set_b={"inverse": "for (double x : DS) { if (Math.abs(x)>1e6) continue; assertEquals(x, M.toDegrees(M.toRadians(x)), 1e-9+1e-12*Math.abs(x)); }"},
    set_m={
        "scale_homog": "for (double x : DS) { if (Math.abs(x)>1e6) continue; for (double c : new double[]{2.0,3.0,0.5}) assertEquals(c*M.toRadians(x), M.toRadians(c*x), 1e-12+1e-12*Math.abs(c*M.toRadians(x))); }",
        "additive": "for (double[] xy : DDs) { double a=xy[0],b=xy[1]; if (Math.abs(a)>1e6||Math.abs(b)>1e6) continue; assertEquals(M.toRadians(a)+M.toRadians(b), M.toRadians(a+b), 1e-12+1e-12*Math.abs(M.toRadians(a+b))); }",
    })

sut("fm_todegrees", f"{CM}.util.FastMath", "toDegrees", "(D)D", "double",
    blocks="Lstar,Istar",
    excl=fm_excl("toDegrees"),
    set_n={
        "homog": "for (double x : DS) { if (Math.abs(x)>1e6) continue; for (double c : new double[]{2.0,3.0,0.5}) assertEquals(c*M.toDegrees(x), M.toDegrees(c*x), 1e-12+1e-12*Math.abs(c*M.toDegrees(x))); }",
        "additive": "for (double[] xy : DDs) { double a=xy[0],b=xy[1]; if (Math.abs(a)>1e6||Math.abs(b)>1e6) continue; assertEquals(M.toDegrees(a)+M.toDegrees(b), M.toDegrees(a+b), 1e-9+1e-12*Math.abs(M.toDegrees(a+b))); }",
        "inverse": "for (double x : DS) { if (Math.abs(x)>1e6) continue; assertEquals(x, M.toRadians(M.toDegrees(x)), 1e-9+1e-12*Math.abs(x)); }",
    },
    set_b={"inverse": "for (double x : DS) { if (Math.abs(x)>1e6) continue; assertEquals(x, M.toRadians(M.toDegrees(x)), 1e-9+1e-12*Math.abs(x)); }"},
    set_m={
        "scale_homog": "for (double x : DS) { if (Math.abs(x)>1e6) continue; for (double c : new double[]{2.0,3.0,0.5}) assertEquals(c*M.toDegrees(x), M.toDegrees(c*x), 1e-12+1e-12*Math.abs(c*M.toDegrees(x))); }",
        "additive": "for (double[] xy : DDs) { double a=xy[0],b=xy[1]; if (Math.abs(a)>1e6||Math.abs(b)>1e6) continue; assertEquals(M.toDegrees(a)+M.toDegrees(b), M.toDegrees(a+b), 1e-9+1e-12*Math.abs(M.toDegrees(a+b))); }",
    })

sut("fm_copysign", f"{CM}.util.FastMath", "copySign", "(DD)D", "double",
    blocks="Lstar,Istar",
    excl=fm_excl("copySign"),
    set_n={
        "magnitude": "for (double[] xy : DD) { assertEquals(Math.abs(xy[0]), Math.abs(M.copySign(xy[0],xy[1])), 1e-12); }",
        "signfollow": "for (double[] xy : DD) { double y=xy[1]; if (y==0.0) continue; double r=M.copySign(xy[0],y); if (xy[0]!=0.0) assertTrue((r>=0.0)==(y>=0.0)); }",
        "idem": "for (double[] xy : DD) { double r=M.copySign(xy[0],xy[1]); assertEquals(r, M.copySign(r,xy[1]), 1e-12); }",
    },
    set_b={"magnitude": "for (double[] xy : DD) { assertEquals(Math.abs(xy[0]), Math.abs(M.copySign(xy[0],xy[1])), 1e-12); }"},
    set_m={
        "scale_homog": "for (double[] xy : DD) { for (double c : new double[]{2.0,3.0}) assertEquals(c*Math.abs(xy[0]), Math.abs(M.copySign(c*xy[0],xy[1])), 1e-9+1e-9*c*Math.abs(xy[0])); }",
    })

sut("fm_scalb", f"{CM}.util.FastMath", "scalb", "(DI)D", "double",
    blocks="Lstar,Istar",
    excl=fm_excl("scalb"),
    set_n={
        "homom": "for (double x : DS) { if (Double.isNaN(x)||Double.isInfinite(x)) continue; for (int n : new int[]{1,2,3}) assertEquals(M.scalb(x,n+2), M.scalb(M.scalb(x,n),2), 1e-12*Math.abs(M.scalb(x,n+2))+1e-300); }",
        "pow2": "for (double x : DS) { if (Double.isNaN(x)||Double.isInfinite(x)||Math.abs(x)>1e150) continue; for (int n : new int[]{0,1,2,3,4}) assertEquals(x*Math.pow(2.0,n), M.scalb(x,n), 1e-9*Math.abs(x*Math.pow(2.0,n))+1e-300); }",
        "linear": "for (double x : DS) { if (Double.isNaN(x)||Double.isInfinite(x)) continue; assertEquals(3.0*M.scalb(x,2), M.scalb(3.0*x,2), 1e-9*Math.abs(3.0*M.scalb(x,2))+1e-300); }",
    },
    set_b={"pow2": "for (double x : DS) { if (Double.isNaN(x)||Double.isInfinite(x)||Math.abs(x)>1e150) continue; for (int n : new int[]{0,1,2,3,4}) assertEquals(x*Math.pow(2.0,n), M.scalb(x,n), 1e-9*Math.abs(x*Math.pow(2.0,n))+1e-300); }"},
    set_m={
        "scale_homog": "for (double x : DS) { if (Double.isNaN(x)||Double.isInfinite(x)) continue; assertEquals(3.0*M.scalb(x,2), M.scalb(3.0*x,2), 1e-9*Math.abs(3.0*M.scalb(x,2))+1e-300); }",
    })

sut("fm_pow_di", f"{CM}.util.FastMath", "pow", "(DI)D", "double",
    blocks="Lstar,Istar",
    excl=fm_excl("pow"),
    set_n={
        "expsum": "for (double[] xy : DDP) { double a=xy[0]; if (a<=0||a>50) continue; for (int e : new int[]{1,2,3}) assertEquals(M.pow(a,e+1), M.pow(a,e)*a, 1e-9*Math.abs(M.pow(a,e+1))+1e-12); }",
        "exp0": "for (double[] xy : DDP) { double a=xy[0]; assertEquals(1.0, M.pow(a,0), 0.0); }",
        "prodbase": "for (double[] xy : DDP) { double a=xy[0]; if (a<=0||a>50) continue; for (int e : new int[]{2,3}) assertEquals(M.pow(a,e)*M.pow(2.0,e), M.pow(a*2.0,e), 1e-9*Math.abs(M.pow(a*2.0,e))+1e-12); }",
    },
    set_b={"exp0": "for (double[] xy : DDP) { double a=xy[0]; assertEquals(1.0, M.pow(a,0), 0.0); }"},
    set_m={
        "scale_homog": "for (double[] xy : DDP) { double a=xy[0]; if (a<=0||a>50) continue; for (int e : new int[]{2,3}) assertEquals(M.pow(a,e)*M.pow(2.0,e), M.pow(a*2.0,e), 1e-9*Math.abs(M.pow(a*2.0,e))+1e-12); }",
    })


if __name__ == "__main__":
    print(f"Total SUTs: {len(SUTS)}")
    for s in SUTS:
        beyond_g = [b for b in s["blocks"].split(",") if b != "G"]
        n_mr = len(s["set_n"])
        assert beyond_g, f"{s['key']} has no block beyond G!"
        print(f"  {s['key']:18s} {s['cls'].split('.')[-1]}.{s['method']:20s} "
              f"blocks={s['blocks']:18s} setN={n_mr} setB={len(s['set_b'])} setM={len(s['set_m'])}")

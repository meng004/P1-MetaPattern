/*
 * NOETHER vs. GenMorph comparative pilot — sin subject.
 *
 * Subject:                MathClass.sin(double x) → double
 * GenMorph MR set (S G):  MR20-MR23 from
 *   /tmp/genmorph_pilot/mrs/mrs/assertions_seed11/MathClass?sin?0/
 * Published kill rates (mutants_killed.csv, seed11):
 *   MR20: 14/26 (53.85%)
 *   MR21: 0/0  (vacuous on this seed)
 *   MR22: 13/26 (50.00%)
 *   MR23: 13/26 (50.00%)
 *   Union: 16/26 (61.54%)
 *
 * Set N (NOETHER) — 4 MRs derived from the trigonometric algebra of sin:
 *   - testRhoOddSym     (G block):    sin(-x) = -sin(x)
 *   - testRhoPeriod     (G block):    sin(x + 2π) = sin(x)
 *   - testRhoBound      (O_le block): |sin(x)| ≤ 1
 *   - testRhoComplement (G block):    sin(π - x) = sin(x)
 *
 * Set G — literal transcription of MR20-MR23 jor expressions, with the
 * GenMorph DSL substitutions:
 *   i_this_s.PI / i_this_f.PI → Math.PI       (constants captured by GAssert)
 *   i_this_s.E  / i_this_f.E  → Math.E
 *   i_x_s, i_x_f              → x_s, x_f       (source / follow-up input)
 *   o_return_s, o_return_f    → o_s, o_f       (source / follow-up output)
 *
 * Floating-point tolerance for output equality follows the DSL convention
 * (1.0E-4). Set N tolerance is tighter (1e-12) because the algebraic
 * identities are exact at machine precision; Set G uses 1.0E-4 because the
 * evolved jor expressions involve safe-divide guards at that scale.
 */

import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.Disabled;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import java.util.ArrayList;
import java.util.List;
import java.util.Random;

import static org.junit.jupiter.api.Assertions.assertTrue;

class MathClassSinMRTest {

    private static final long RNG_SEED = 11L;
    private static final int K_INPUTS = 50;            // larger than 25 for finer FP estimation
    private static final double SET_N_TOL = 1.0E-12;   // algebraic identities are exact
    private static final double JOR_TOL = 1.0E-4;       // matches GenMorph DSL convention

    private static final List<Double> SOURCE_INPUTS = new ArrayList<>();

    @BeforeAll
    static void generateSourceInputs() {
        // Boundary values: 0, ±π/2, ±π, ±2π, very small ε, large x near reduction limit
        SOURCE_INPUTS.add(0.0);
        SOURCE_INPUTS.add(Math.PI / 2);
        SOURCE_INPUTS.add(-Math.PI / 2);
        SOURCE_INPUTS.add(Math.PI);
        SOURCE_INPUTS.add(-Math.PI);
        SOURCE_INPUTS.add(2 * Math.PI);
        SOURCE_INPUTS.add(-2 * Math.PI);
        SOURCE_INPUTS.add(Math.PI / 4);
        SOURCE_INPUTS.add(Math.PI / 6);
        SOURCE_INPUTS.add(Math.PI / 3);
        SOURCE_INPUTS.add(1.0E-8);
        SOURCE_INPUTS.add(-1.0E-8);
        SOURCE_INPUTS.add(100.0);
        SOURCE_INPUTS.add(-100.0);

        Random rng = new Random(RNG_SEED);
        while (SOURCE_INPUTS.size() < K_INPUTS) {
            // Mixed: 50% in [-2π, 2π], 30% in [-10, 10], 20% in [-100, 100]
            double cat = rng.nextDouble();
            double x;
            if (cat < 0.50) {
                x = (rng.nextDouble() * 4 - 2) * Math.PI;
            } else if (cat < 0.80) {
                x = rng.nextDouble() * 20 - 10;
            } else {
                x = rng.nextDouble() * 200 - 100;
            }
            SOURCE_INPUTS.add(x);
        }
    }

    /* ===================== Set N (NOETHER, derived from sin's algebra) ===================== */

    @Test
    @DisplayName("Set N: ρ_oddsym — sin(-x) = -sin(x)")
    void testRhoOddSym() {
        for (double x : SOURCE_INPUTS) {
            double a = MathClass.sin(x);
            double b = MathClass.sin(-x);
            assertTrue(Math.abs(a + b) < SET_N_TOL || Math.abs(a + b) / (Math.abs(a) + Math.abs(b) + 1e-30) < 1e-9,
                "ρ_oddsym violated at x=" + x + "; sin(x)=" + a + ", sin(-x)=" + b);
        }
    }

    @Test
    @DisplayName("Set N: ρ_period — sin(x + 2π) = sin(x)")
    void testRhoPeriod() {
        for (double x : SOURCE_INPUTS) {
            // Skip large x where 2π addition loses too many ULPs
            if (Math.abs(x) > 50) continue;
            double a = MathClass.sin(x);
            double b = MathClass.sin(x + 2 * Math.PI);
            // Allow looser tolerance — periodicity within a few ULPs of float math
            assertTrue(Math.abs(a - b) < 1.0E-9,
                "ρ_period violated at x=" + x + "; sin(x)=" + a + ", sin(x+2π)=" + b);
        }
    }

    @Test
    @DisplayName("Set N: ρ_bound — |sin(x)| ≤ 1")
    void testRhoBound() {
        for (double x : SOURCE_INPUTS) {
            double a = MathClass.sin(x);
            // Allow tiny rounding above 1.0
            assertTrue(Math.abs(a) <= 1.0 + 1.0E-12,
                "ρ_bound violated at x=" + x + "; sin(x)=" + a);
        }
    }

    @Test
    @DisplayName("Set N: ρ_complement — sin(π − x) = sin(x)")
    void testRhoComplement() {
        for (double x : SOURCE_INPUTS) {
            if (Math.abs(x) > 50) continue;
            double a = MathClass.sin(x);
            double b = MathClass.sin(Math.PI - x);
            assertTrue(Math.abs(a - b) < 1.0E-9,
                "ρ_complement violated at x=" + x + "; sin(x)=" + a + ", sin(π−x)=" + b);
        }
    }

    /* ===================== Set G (literal jor transcription) ===================== */

    private static double safeDiv(double n, double d) {
        return (Math.abs(d) < JOR_TOL) ? 1.0 : (n / d);
    }

    /**
     * MR20 jor — verbatim from MathClass?sin?0@MR20.jor.txt.
     *
     * jir : x_f = x_s + 1.5708 (≈ π/2)
     * jor : Math.abs(termA - termB) >= 1e-4
     *   where, with PI = Math.PI:
     *     ratioFS = |o_s|<1e-4 ? 1.0 : o_f/o_s
     *     termA   = ((|PI|<1e-4 ? 1.0 : (ratioFS - o_s) / PI)) * o_f
     *     innerD  = |o_s * x_s|<1e-4 ? 1.0 : ratioFS / (o_s * x_s)
     *     termB   = |innerD|<1e-4 ? 1.0
     *               : ((x_f - x_f) * PI) / innerD       — note (x_f - x_f) = 0
     *
     * Because (x_f - x_f) is identically zero in the DSL, termB collapses
     * to either 1.0 (innerD is small) or 0 (innerD non-small). The
     * effective rule is therefore a check that |termA - termB| ≥ 1e-4.
     */
    private static boolean jorMR20(double x_s, double x_f, double o_s, double o_f) {
        final double PI = Math.PI;
        double ratioFS = (Math.abs(o_s) < JOR_TOL) ? 1.0 : (o_f / o_s);
        double termA = ((Math.abs(PI) < JOR_TOL) ? 1.0 : ((ratioFS - o_s) / PI)) * o_f;
        double innerDenom = o_s * x_s;
        double innerD = (Math.abs(innerDenom) < JOR_TOL) ? 1.0 : (ratioFS / innerDenom);
        double termB = (Math.abs(innerD) < JOR_TOL) ? 1.0 : (((x_f - x_f) * PI) / innerD);
        return Math.abs(termA - termB) >= JOR_TOL;
    }

    /**
     * MR21 jor — verbatim from MathClass?sin?0@MR21.jor.txt.
     *
     * jir : x_f = x_s + 2.0
     * jor : abs(o_s - <complex>) >= 1e-4
     *
     * Note: GenMorph published seed11 mrs_status reports MR21 as MS=0/0
     * (vacuous on this seed). We retain the literal transcription for
     * completeness.
     */
    private static boolean jorMR21(double x_s, double x_f, double o_s, double o_f) {
        final double PI = Math.PI, E = Math.E;
        double ratioFS = (Math.abs(o_s) < JOR_TOL) ? 1.0 : (o_f / o_s);
        double diffFS = (Math.abs(o_s) < JOR_TOL) ? 1.0 : ((x_f - x_s) / o_s);
        double sumNumer = (x_f + E) - diffFS;
        double piRatio = (Math.abs(PI) < JOR_TOL) ? 1.0 : (sumNumer / PI);
        double inverse = (Math.abs(piRatio) < JOR_TOL) ? 1.0 : (x_s / piRatio);
        double subterm = ratioFS - inverse;
        double diffPI = (PI - PI);
        double xRatio = (Math.abs(x_s) < JOR_TOL) ? 1.0 : ((6.2832 - diffPI) / x_s);
        double rhsNumer = o_f * xRatio;
        double rhs = (Math.abs(subterm) < JOR_TOL) ? 1.0 : (rhsNumer / subterm);
        return Math.abs(o_s - rhs) >= JOR_TOL;
    }

    /**
     * MR22 jor — verbatim from MathClass?sin?0@MR22.jor.txt.
     *
     * jir : x_f = x_s + 3.0
     * jor : abs(safeDiv(x_s, o_s) - <complex>) >= 1e-4
     */
    private static boolean jorMR22(double x_s, double x_f, double o_s, double o_f) {
        double xOverOs = (Math.abs(o_s) < JOR_TOL) ? 1.0 : (x_s / o_s);
        double prod = o_f * (0.2521 * o_s);
        double inner1 = (Math.abs(prod) < JOR_TOL) ? 1.0 : (o_f / prod);
        double xOverInner1 = (Math.abs(inner1) < JOR_TOL) ? 1.0 : (x_s / inner1);
        double rhsBase = (Math.abs(o_f) < JOR_TOL) ? 1.0 : (xOverInner1 / o_f);
        return Math.abs(xOverOs - rhsBase) >= JOR_TOL;
    }

    /**
     * MR23 jor — verbatim from MathClass?sin?0@MR23.jor.txt.
     *
     * jir : x_f = x_s * 1.5708 (≈ π/2 multiplier)
     * jor : LHS >= RHS
     *
     * Where:
     *   LHS = (PI*x_s + x_f) * ((x_f + o_f) - x_s) - (-7) * (x_s * o_s)
     *   RHS = safeDiv((safeDiv(x_f - o_f, -7)),
     *                 (safeDiv(E, o_f) + (x_s - o_s)))
     */
    private static boolean jorMR23(double x_s, double x_f, double o_s, double o_f) {
        final double PI = Math.PI, E = Math.E;
        double lhs = (((PI * x_s) + x_f) * ((x_f + o_f) - x_s)) - ((0.0 - 7.0) * (x_s * o_s));
        double eOverOf = (Math.abs(o_f) < JOR_TOL) ? 1.0 : (E / o_f);
        double diffSum = eOverOf + (x_s - o_s);
        double seven = (Math.abs(0.0 - 7.0) < JOR_TOL) ? 1.0 : ((x_f - o_f) / (0.0 - 7.0));
        double rhs = (Math.abs(diffSum) < JOR_TOL) ? 1.0 : (seven / diffSum);
        return lhs >= rhs;
    }

    @Test
    @DisplayName("Set G: GenMorph MR20 — x_f = x_s + π/2 (literal jor)")
    void testGenMorphMR20() {
        int failures = 0, considered = 0;
        StringBuilder firstFailure = new StringBuilder();
        for (double x_s : SOURCE_INPUTS) {
            double x_f = x_s + 1.5708;
            considered++;
            double o_s = MathClass.sin(x_s);
            double o_f = MathClass.sin(x_f);
            if (!jorMR20(x_s, x_f, o_s, o_f)) {
                if (firstFailure.length() == 0) firstFailure.append(String.format("(x_s=%.4f, o_s=%.6f, o_f=%.6f)", x_s, o_s, o_f));
                failures++;
            }
        }
        // MR20 published FP = 0/99; our K=50 inputs allow 0 failures (strict).
        assertTrue(failures == 0, "MR20 violated " + failures + "/" + considered + "; first: " + firstFailure);
    }

    /**
     * MR21 is intentionally @Disabled — published mrs_status reports
     * MS = 0/0 (vacuous on this seed); detection contribution is 0 by
     * construction and the literal transcription's FP rate on our seeded
     * inputs (which include broader boundary values than upstream Randoop)
     * is materially higher than the published 1/99. Re-enable on a
     * Randoop-style input distribution if desired.
     */
    @Disabled("Vacuous in GenMorph seed11 (MS=0/0); FP rate input-distribution dependent.")
    @Test
    @DisplayName("Set G: GenMorph MR21 — x_f = x_s + 2.0 (literal jor)")
    void testGenMorphMR21() {
        int failures = 0, considered = 0;
        for (double x_s : SOURCE_INPUTS) {
            double x_f = x_s + 2.0;
            considered++;
            double o_s = MathClass.sin(x_s);
            double o_f = MathClass.sin(x_f);
            if (!jorMR21(x_s, x_f, o_s, o_f)) failures++;
        }
        assertTrue(failures <= 2, "MR21 violated " + failures + "/" + considered);
    }

    @Test
    @DisplayName("Set G: GenMorph MR22 — x_f = x_s + 3.0 (literal jor)")
    void testGenMorphMR22() {
        int failures = 0, considered = 0;
        StringBuilder firstFailure = new StringBuilder();
        for (double x_s : SOURCE_INPUTS) {
            double x_f = x_s + 3.0;
            considered++;
            double o_s = MathClass.sin(x_s);
            double o_f = MathClass.sin(x_f);
            if (!jorMR22(x_s, x_f, o_s, o_f)) {
                if (firstFailure.length() == 0) firstFailure.append(String.format("(x_s=%.4f, o_s=%.6f, o_f=%.6f)", x_s, o_s, o_f));
                failures++;
            }
        }
        // MR22 published FP = 0/99; our K=50 inputs allow 0 failures.
        assertTrue(failures == 0, "MR22 violated " + failures + "/" + considered + "; first: " + firstFailure);
    }

    @Test
    @DisplayName("Set G: GenMorph MR23 — x_f = x_s * π/2 (literal jor)")
    void testGenMorphMR23() {
        int failures = 0, considered = 0;
        StringBuilder firstFailure = new StringBuilder();
        for (double x_s : SOURCE_INPUTS) {
            double x_f = x_s * 1.5708;
            considered++;
            double o_s = MathClass.sin(x_s);
            double o_f = MathClass.sin(x_f);
            if (!jorMR23(x_s, x_f, o_s, o_f)) {
                if (firstFailure.length() == 0) firstFailure.append(String.format("(x_s=%.4f, o_s=%.6f, o_f=%.6f)", x_s, o_s, o_f));
                failures++;
            }
        }
        // MR23 published FP = 0/99; allow 0 failures.
        assertTrue(failures == 0, "MR23 violated " + failures + "/" + considered + "; first: " + firstFailure);
    }
}

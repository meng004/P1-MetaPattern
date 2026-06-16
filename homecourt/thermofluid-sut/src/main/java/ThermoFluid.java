/**
 * Thermal-engineering (热工) and fluid-mechanics (流体) equation kernels —
 * NOETHER home-turf benchmark SUTs.
 *
 * Each method implements an explicit physical equation whose operators carry
 * algebraic structure (symmetry / scaling / monotonicity / limit / inverse),
 * so it admits several metamorphic relations derivable directly from the NOETHER
 * algebra. All methods are pure, deterministic, primitive-typed — compatible
 * with the GenMorph evaluation toolchain (Randoop inputs + PITest).
 */
public class ThermoFluid {

    /** Stefan-Boltzmann constant (W m^-2 K^-4). */
    public static final double SIGMA = 5.670374419e-8;

    /** T2 — Log-mean temperature difference (heat exchangers).
     *  Symmetric in (dT1,dT2); scale-equivariant; bounded by [min,max]. */
    public static double lmtd(double dT1, double dT2) {
        if (Math.abs(dT1 - dT2) < 1e-9) {
            return dT1;                       // L'Hopital limit dT1 -> dT2
        }
        return (dT1 - dT2) / Math.log(dT1 / dT2);
    }

    /** T5 — Stefan-Boltzmann net radiative exchange.
     *  Antisymmetric under (t1<->t2); linear in area; quartic in temperature. */
    public static double stefanBoltzmann(double eps, double area, double t1, double t2) {
        return eps * SIGMA * area * (t1 * t1 * t1 * t1 - t2 * t2 * t2 * t2);
    }

    /** T7 — Carnot efficiency. Scale-invariant in (tc,th); monotone. */
    public static double carnotEfficiency(double tc, double th) {
        return 1.0 - tc / th;
    }

    /** F2 — Incompressible continuity, outlet velocity v2 = a1 v1 / a2.
     *  Inverse in a2; linear in a1 and v1. */
    public static double continuityV2(double a1, double v1, double a2) {
        return a1 * v1 / a2;
    }

    /** F4 — Darcy-Weisbach head loss. Quadratic in v; linear in L; inverse in D. */
    public static double darcyHeadLoss(double f, double l, double d, double v, double g) {
        return f * (l / d) * (v * v) / (2.0 * g);
    }

    /** F5 — Hagen-Poiseuille laminar flow rate. Quartic in r; linear in dP;
     *  inverse in mu and L. */
    public static double hagenPoiseuille(double dP, double r, double mu, double l) {
        return Math.PI * dP * (r * r * r * r) / (8.0 * mu * l);
    }

    /** F9 — Pump affinity law (head ~ speed^2). */
    public static double pumpAffinityHead(double h1, double n1, double n2) {
        return h1 * (n2 / n1) * (n2 / n1);
    }

    /** F3 — Reynolds number. Multi-linear scaling; inverse in mu. */
    public static double reynolds(double rho, double v, double d, double mu) {
        return rho * v * d / mu;
    }
}

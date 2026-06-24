package headtohead;

import org.junit.Test;
import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertTrue;
import static org.junit.Assert.assertFalse;

/** Auto-generated head-to-head MR class for SUT au_addcheck_int (org.apache.commons.math3.util.ArithmeticUtils.addAndCheck). Blocks: G,Tstar,Istar. */
public class T_au_addcheck_int {

    // ---- deterministic shared inputs (seed 11) ----
    static final int[][] II = new int[][]{
        {0,5},{1,1},{12,8},{-12,8},{12,-8},{-12,-8},{Integer.MAX_VALUE,33},
        {7,21},{100,75},{17,5},{36,24},{1000,1},{2,1000},{-7,49},{840,3640},{13,17}
    };
    static final int[][] IIs = new int[][]{   // small ints, no overflow on add/mul/sub
        {0,5},{1,1},{12,8},{-12,8},{12,-8},{-12,-8},{7,21},{100,75},{17,5},
        {36,24},{50,50},{-3,9},{11,-4},{0,0},{123,45},{-77,-11}
    };
    static final long[][] LL = new long[][]{
        {0,5},{1,1},{12,8},{-12,8},{12,-8},{-12,-8},{7,21},{100,75},{17,5},
        {36,24},{1000000,1},{2,1000000},{-7,49},{840,3640},{13,17},{99991,100003}
    };
    static final int[][] NK = new int[][]{   // (n,k) combinatorial
        {0,0},{1,0},{1,1},{5,2},{6,3},{10,4},{10,0},{10,10},{20,7},{30,15},
        {40,1},{50,2},{12,6},{8,3},{15,5},{18,9},{25,12},{2,1}
    };
    static final int[][] POWI = new int[][]{ // (base,exp) small
        {2,3},{3,2},{5,1},{2,5},{7,2},{10,3},{2,8},{4,4},{1,9},{6,2},
        {3,5},{2,10},{0,3},{-2,3},{-3,2},{2,6}
    };
    static final double[] DS = new double[]{
        0.0,1.0,-1.0,2.5,-2.5,0.5,-0.5,3.14159,-3.14159,10.0,-10.0,
        0.001,-0.001,123.456,-123.456,1000.0,-1000.0,7.0,-7.0,42.0
    };
    static final double[] DSF = new double[]{ // for floor/ceil: spread around integers
        0.0,0.5,-0.5,1.5,-1.5,2.9,-2.9,2.1,-2.1,10.7,-10.7,3.0,-3.0,
        0.999,-0.999,100.5,-100.5,7.25,-7.75,42.49
    };
    static final double[] DSP = new double[]{ // positive
        0.0,0.001,0.5,1.0,2.0,3.5,10.0,100.0,1000.0,0.25,7.0,42.0,
        123.456,0.1,5.0,9.0,16.0,2.5,50.0,0.01
    };
    static final double[] DSE = new double[]{ // for exp/expm1 (bounded magnitude)
        0.0,1.0,-1.0,2.0,-2.0,0.5,-0.5,3.0,-3.0,5.0,-5.0,0.1,-0.1,
        10.0,-10.0,0.25,-0.25,7.0,-7.0,1.5
    };
    static final double[] DT = new double[]{  // angles for sin/cos
        0.0,0.5,1.0,1.5,2.0,3.0,-0.5,-1.0,-2.0,0.7853981633974483,
        1.5707963267948966,3.141592653589793,4.0,5.0,-3.0,6.0,0.3,-0.3,2.5,-2.5
    };
    static final double[] DTt = new double[]{ // angles for tan (avoid +-pi/2)
        0.0,0.5,1.0,-0.5,-1.0,0.3,-0.3,0.7,-0.7,1.2,-1.2,2.0,-2.0,
        0.1,-0.1,0.9,-0.9,1.4,-1.4,0.6
    };
    static final double[] DSH = new double[]{ // for sinh/cosh/tanh (bounded)
        0.0,0.5,1.0,-1.0,2.0,-2.0,0.25,-0.25,3.0,-3.0,0.1,-0.1,1.5,-1.5,
        4.0,-4.0,0.75,-0.75,2.5,-2.5
    };
    static final double[] DSP2 = DSP;
    static final double[] DSPlog = DSP;
    // positive-shift array for log1p (x > -1)
    static final double[] DSPp = new double[]{
        0.0,0.5,1.0,2.0,5.0,10.0,0.25,0.1,-0.5,-0.9,3.0,7.0,0.01,100.0,
        50.0,0.75,1.5,2.5,9.0,42.0
    };
    static final double[][] DD = new double[][]{
        {3.0,4.0},{1.0,1.0},{-3.0,4.0},{5.0,-12.0},{0.0,7.0},{2.5,2.5},
        {-1.0,-1.0},{10.0,0.5},{100.0,1.0},{-7.0,24.0},{0.5,0.5},{8.0,15.0},
        {-2.0,3.0},{6.0,-8.0},{1.5,-2.5},{20.0,21.0}
    };
    static final double[][] DDs = new double[][]{ // small magnitudes for add
        {1.0,2.0},{3.0,4.0},{-1.0,5.0},{0.0,7.0},{2.5,2.5},{-3.0,-4.0},
        {10.0,1.0},{0.5,0.5},{-7.0,8.0},{6.0,-2.0},{1.5,2.5},{9.0,3.0},
        {-2.0,-2.0},{4.0,4.0},{0.3,0.7},{5.5,1.5}
    };
    static final double[][] DDP = new double[][]{ // both positive
        {2.0,3.0},{1.0,1.0},{5.0,2.0},{10.0,0.5},{3.0,4.0},{0.5,0.5},
        {7.0,2.0},{100.0,3.0},{2.0,8.0},{4.0,4.0},{1.5,2.5},{9.0,3.0},
        {2.0,2.0},{6.0,5.0},{0.25,0.5},{50.0,1.0}
    };
    static final double[] DSPlog1p = DSPp;

    @Test public void nN_commute() { for (int[] xy : IIs) { int p=xy[0],q=xy[1]; assertEquals(org.apache.commons.math3.util.ArithmeticUtils.addAndCheck(p,q), org.apache.commons.math3.util.ArithmeticUtils.addAndCheck(q,p)); } }
    @Test public void nN_identity() { for (int[] xy : IIs) { int p=xy[0]; assertEquals(p, org.apache.commons.math3.util.ArithmeticUtils.addAndCheck(p,0)); } }
    @Test public void nN_assoc() { for (int[] xy : IIs) { int p=xy[0],q=xy[1]; int r=3; assertEquals(org.apache.commons.math3.util.ArithmeticUtils.addAndCheck(org.apache.commons.math3.util.ArithmeticUtils.addAndCheck(p,q),r), org.apache.commons.math3.util.ArithmeticUtils.addAndCheck(p,org.apache.commons.math3.util.ArithmeticUtils.addAndCheck(q,r))); } }
    @Test public void bB_commute() { for (int[] xy : IIs) { int p=xy[0],q=xy[1]; assertEquals(org.apache.commons.math3.util.ArithmeticUtils.addAndCheck(p,q), org.apache.commons.math3.util.ArithmeticUtils.addAndCheck(q,p)); } }
    @Test public void mM_perm_inv() { for (int[] xy : IIs) { int p=xy[0],q=xy[1]; assertEquals(org.apache.commons.math3.util.ArithmeticUtils.addAndCheck(p,q), org.apache.commons.math3.util.ArithmeticUtils.addAndCheck(q,p)); } }
    @Test public void mM_additive() { for (int[] xy : IIs) { int p=xy[0],q=xy[1]; assertEquals(org.apache.commons.math3.util.ArithmeticUtils.addAndCheck(p,q)+5, org.apache.commons.math3.util.ArithmeticUtils.addAndCheck(p+5,q)); } }
}
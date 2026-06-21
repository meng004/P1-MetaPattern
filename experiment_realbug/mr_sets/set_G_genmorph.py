#!/usr/bin/env python3
"""set_G_genmorph (set G) — NOT APPLICABLE to library-level e3nn/PyG bugs.

Set G is GenMorph: GP-evolved MRs, SUT-specific with no fixed/portable MR list, re-evolved per SUT at a 30-min GAssert budget using mutation-killing as the fitness signal (paper L309, L313, L349-357). This makes it categorically un-portable as a self-contained mr(fn,ctx,tol) module, for two independent reasons.

(1) No MR catalogue to port. GenMorph's defining property is that there IS no fixed MR list; relations are re-evolved per SUT and bound to the mutation-killing fitness landscape (L313: "GenMorph's evolutionary search is shaped by the fitness landscape induced by mutation killing"). There is therefore no stable GenMorph relation to instantiate on e3nn/PyG. Hand-writing a concrete relation and labelling it "GenMorph" would be fabrication, exactly the forced fit the honesty rules forbid, and would also violate the prereg constraint against writing a bug-specific MR.

(2) The generation step cannot run in this harness, CPU-only or otherwise. Producing GenMorph MRs requires running the GenMorph toolchain itself per SUT: a mutation-testing harness (PIT/major-style) to generate mutants, a test-input generator / seed corpus to drive the GP search, and a ~30-min GP evolution run. GenMorph (GenMorph2024) is engineered for Java methods (EvoSuite + PIT); there is no equivalent CPU-only pipeline that, given a single buggy Python library function and its tiny repro inputs, yields evolved MRs inside one mr() call. It is an offline tool-running protocol, not a metamorphic relation evaluable against ctx.

Implication for the head-to-head: the paper treats Set G as the single executable SOTA arm (L348-352), but that executability rests on the original Java + GAssert/PIT substrate. On the e3nn/PyG library-bug substrate Set G is not reproducible within this contract for the same structural reason MR-Scout is excluded (L358-362: the required input substrate is structurally absent). A faithful Set G arm on B1 would require re-running the actual GenMorph tool per SUT as an external offline step (out of scope for this CPU-only mr() contract); stubbing it as a Python module would be fabrication, so it is recorded not_applicable rather than forced. Honest consequence: Set G drops from B1's executable comparison, which should be reported as a substrate-limitation of the real-bug port, not as a Set-G miss.
"""

def mr_set_G_genmorph(fn, ctx, tol):
    return {"status": "not_applicable", "detail": "set_G_genmorph: not a library-function relation (see module docstring)"}

MR = {"name": "set_G_genmorph", "set": "G", "callable": mr_set_G_genmorph, "applicability": "not_applicable"}

# Set L — LLM-prompt MR generation log

## Generator

- **Model**: gpt-4-turbo-2024-04-09
- **Temperature**: 0.0
- **Max tokens**: 2048
- **Seed**: 4246 (recorded in S4_reproducibility/seeds.txt)
- **Date generated**: [TO BE FILLED at experiment time]

## Prompt sent to GPT-4

```
You are an expert in metamorphic testing for machine learning systems.

Task: produce exactly five metamorphic relations (MRs) for testing a
SE(3)-equivariant point-cloud classifier.

System under test:
  - Input: point cloud x ∈ R^{n×3} of n three-dimensional points
  - Output: probability distribution f(x) ∈ Δ^{C-1} over C classes (C=10)
  - Architecture: SE(3)-equivariant transformer (e3nn-based) trained on
    ModelNet10

For each MR, return a JSON object with these fields:
  - id: short identifier
  - description: one-sentence English description of the MR
  - input_relation: how to transform the input
  - output_relation: what should hold on the output
  - tolerance: numerical tolerance for fp32 architectures
  - rationale: why a tester would write this MR

Return your answer as a JSON list of five objects. Do not include any
text before or after the JSON.

Constraints:
  - Each MR must be implementable as a Python function with signature
    (model, point_cloud) -> bool
  - The MRs should be diverse: cover invariance, robustness, training,
    or any other testing facet you find relevant
  - Do not refer to any specific implementation framework (e3nn, PyTorch);
    the MR should be model-agnostic at the interface level
```

## Raw GPT-4 output (verbatim)

```
[TO BE FILLED at experiment time]
```

## Parse status

- **Validation**: each item must have all six fields and be parseable as
  Python via `set_L_llm.compile_mr()`.
- **Manual filtering**: if the LLM produces a duplicate of a NOETHER MR
  (e.g., another rotation-invariance), keep it and report the overlap in
  the manuscript footnote rather than substitute. Set L's purpose is to
  represent what an unprompted-by-NOETHER tester would obtain; overlaps
  with set N are themselves data.
- **Implementation**: human author then translates each JSON spec into a
  callable in `set_L_llm.py::SET_L`.

# Set L — LLM-prompt MR generation log

## Generator

- **Model**: gpt-4-turbo-2024-04-09
- **Temperature**: 0.0
- **Max tokens**: 2048
- **Seed**: 4246 (recorded in S4_reproducibility/seeds.txt)
- **Date generated**: 2026-05-15 (UTC)

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
[
  {
    "id": "rotation_invariance",
    "description": "Rotating the input point cloud arbitrarily should not affect its classification output.",
    "input_relation": "Apply an arbitrary SE(3) rotation (e.g., a rotation matrix) to every point in the point cloud.",
    "output_relation": "The probability distribution over classes remains nearly identical (within tolerance) to the original output.",
    "tolerance": 1e-5,
    "rationale": "Since the classifier is SE(3)-equivariant, its output should be invariant to rotations, ensuring correct recognition regardless of object orientation."
  },
  {
    "id": "translation_invariance",
    "description": "Translating the input point cloud should not change the classification outcome.",
    "input_relation": "Apply an arbitrary translation vector to all points in the point cloud.",
    "output_relation": "The resulting probability distribution should remain nearly the same as that of the original point cloud.",
    "tolerance": 1e-5,
    "rationale": "SE(3)-equivariance implies that moving an object in space should not alter its class prediction, affirming model robustness to location shifts."
  },
  {
    "id": "scaling_robustness",
    "description": "Uniformly scaling the input point cloud should lead to a similar classification output if the model is robust to scale variations.",
    "input_relation": "Multiply each coordinate of every point in the point cloud by a constant scaling factor (e.g., 1.2).",
    "output_relation": "The output probability distribution should change only within the numerical tolerance compared to the original.",
    "tolerance": 1e-5,
    "rationale": "Although not strictly enforced by SE(3)-equivariance, robustness to small scale variations is desirable in real-world settings and common in testing classifiers."
  },
  {
    "id": "permutation_invariance",
    "description": "Permuting the order of points in the input point cloud should not affect the classification output.",
    "input_relation": "Randomly shuffle the order of the rows (points) in the input point cloud.",
    "output_relation": "The probability distribution over classes should remain unchanged (within tolerance) relative to the original ordering.",
    "tolerance": 1e-5,
    "rationale": "Point cloud data is unordered, so a correct classifier should produce the same output regardless of the order of input points."
  },
  {
    "id": "noise_robustness",
    "description": "Adding small Gaussian noise to the input point cloud should not lead to a drastic change in the classification output.",
    "input_relation": "Add zero-mean Gaussian noise with a small standard deviation (e.g., 0.01) independently to each coordinate of each point.",
    "output_relation": "The resulting output probability distribution should differ only minimally (within tolerance) from that of the unperturbed input.",
    "tolerance": 1e-5,
    "rationale": "Testing with noise simulates sensor inaccuracies and real-world measurement errors, ensuring the classifier's robustness to such perturbations."
  }
]
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

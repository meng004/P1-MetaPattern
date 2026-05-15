"""Run the Set L GPT-4 prompt and persist the raw output.

Reads `OPENAI_API_KEY` (and optional `OPENAI_BASE_URL`) from the
environment, or — if not present — from a sibling project's `.env`
file at `../noether-s5-experiment/.env` (relative to the paper
root). Sends the exact prompt documented in `prompt_log.md`'s
"Prompt sent to GPT-4" section to `gpt-4-turbo-2024-04-09` at
`temperature=0.0`, `max_tokens=2048`, `seed=4246`. Persists the raw
response into `prompt_log.md` (replacing the `[TO BE FILLED ...]`
placeholders) and prints the response to stdout.

Usage:
  python supplementary/S3_case_study/mr_sets/run_gpt4_prompt.py
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

THIS_FILE = Path(__file__).resolve()
PROMPT_LOG = THIS_FILE.parent / "prompt_log.md"
PAPER_ROOT = THIS_FILE.parents[3]
FALLBACK_ENV = PAPER_ROOT.parent / "noether-s5-experiment" / ".env"

PROMPT = """You are an expert in metamorphic testing for machine learning systems.

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
"""


def load_env_from_file(env_path: Path) -> dict[str, str]:
    """Parse a simple KEY=VALUE .env file. Handles `export KEY=VALUE` and
    quoted values. Lines starting with `#` are skipped."""
    out: dict[str, str] = {}
    if not env_path.exists():
        return out
    for raw in env_path.read_text().splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[len("export "):].strip()
        if "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip()
        # Strip matching surrounding quotes
        if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
            value = value[1:-1]
        out[key] = value
    return out


def get_credential(name: str, fallback_env: dict[str, str]) -> Optional[str]:
    return os.environ.get(name) or fallback_env.get(name)


def main() -> int:
    fallback_env = load_env_from_file(FALLBACK_ENV)
    # Accept OpenAI's canonical env names OR the user-project alias CHATGPT_*.
    api_key = (
        get_credential("OPENAI_API_KEY", fallback_env)
        or get_credential("CHATGPT_API_KEY", fallback_env)
    )
    base_url = (
        get_credential("OPENAI_BASE_URL", fallback_env)
        or get_credential("CHATGPT_BASE_URL", fallback_env)
    )

    if not api_key:
        print("ERROR: OPENAI_API_KEY / CHATGPT_API_KEY not set in env and not found in", FALLBACK_ENV, file=sys.stderr)
        print("Available keys in fallback .env:", sorted(fallback_env.keys()), file=sys.stderr)
        return 2

    try:
        from openai import OpenAI
    except ImportError:
        print("ERROR: `openai` package not available. Install via `pip install openai`.", file=sys.stderr)
        return 3

    client: Any
    if base_url:
        client = OpenAI(api_key=api_key, base_url=base_url)
        print(f"Using base_url: {base_url}", file=sys.stderr)
    else:
        client = OpenAI(api_key=api_key)

    response = client.chat.completions.create(
        model="gpt-4-turbo-2024-04-09",
        messages=[{"role": "user", "content": PROMPT}],
        temperature=0.0,
        seed=4246,
        extra_body={"max_completion_tokens": 2048},
    )
    raw: Optional[str] = response.choices[0].message.content
    finish_reason = response.choices[0].finish_reason
    usage = response.usage

    if raw is None:
        print("ERROR: GPT-4 returned empty content.", file=sys.stderr)
        print(f"finish_reason: {finish_reason}", file=sys.stderr)
        return 4

    print("=== GPT-4 RAW OUTPUT (verbatim) ===")
    print(raw)
    print("=== END ===")
    print(f"finish_reason: {finish_reason}")
    if usage is not None:
        print(f"usage: prompt={usage.prompt_tokens}, completion={usage.completion_tokens}, total={usage.total_tokens}")

    # Validate JSON parses cleanly. Strip optional ```json ... ``` fence.
    payload = raw.strip()
    if payload.startswith("```"):
        payload = payload.split("\n", 1)[1] if "\n" in payload else payload[3:]
        if payload.endswith("```"):
            payload = payload[:-3]
        if payload.startswith("json\n"):
            payload = payload[len("json\n"):]
    try:
        parsed = json.loads(payload)
    except json.JSONDecodeError as exc:
        print(f"WARNING: GPT-4 output does not parse as JSON: {exc}", file=sys.stderr)
        parsed = None

    if isinstance(parsed, list):
        print(f"Parsed JSON list length: {len(parsed)}")

    # Persist into prompt_log.md
    date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d (UTC)")
    log = PROMPT_LOG.read_text()
    log = log.replace(
        "- **Date generated**: [TO BE FILLED at experiment time]",
        f"- **Date generated**: {date_str}",
        1,
    )
    log = log.replace(
        "## Raw GPT-4 output (verbatim)\n\n```\n[TO BE FILLED at experiment time]\n```",
        "## Raw GPT-4 output (verbatim)\n\n```\n" + raw + "\n```",
        1,
    )
    PROMPT_LOG.write_text(log)
    print(f"\nUpdated: {PROMPT_LOG}")

    return 0


if __name__ == "__main__":
    sys.exit(main())

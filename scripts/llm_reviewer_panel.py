#!/usr/bin/env python3
"""scripts/llm_reviewer_panel.py — Multi-LLM peer-review panel via gateway.

Sends a manuscript (LaTeX source) to N independent LLMs through the
OpenAI-compatible aggregator gateway (BASE_URL + API_KEY in repo-root .env),
each acting as a strict, independent TOSEM reviewer. Emits one structured
review per model plus a panel summary, to feed downstream submission-maturity
assessment.

Design notes:
  * No secrets are hard-coded. Credentials are read from .env (gitignored).
  * Minimal request params (model + messages) for maximum cross-vendor
    compatibility (gpt-5 / claude / deepseek-r1 / glm / kimi have differing
    constraints on temperature / max_tokens / response_format).
  * Each model is queried independently and concurrently; one model's failure
    does not abort the panel. One automatic retry on error (30s backoff).
  * Reviewers are asked to emit a JSON block first, then free-form detail; we
    persist both the raw text (.md) and the parsed JSON (.json) when present.

Usage:
  python3 scripts/llm_reviewer_panel.py --manuscript NOETHER_paper_arxiv.tex \
      --out docs/review_2026-06-17/llm_panel
  python3 scripts/llm_reviewer_panel.py --smoke           # 1 cheap model
  python3 scripts/llm_reviewer_panel.py --models gpt-5 deepseek-r1
"""
import argparse
import concurrent.futures as cf
import json
import os
import re
import sys
import time
from pathlib import Path

try:
    from dotenv import load_dotenv
except ImportError:
    sys.exit("ERROR: pip3 install --user python-dotenv")
try:
    from openai import OpenAI
except ImportError:
    sys.exit("ERROR: pip3 install --user openai")

# Cross-vendor reviewer panel (independent vendors maximise reviewer diversity).
PANEL = ["gpt-5.5", "claude-opus-4-8", "glm-5.2", "deepseek-v4-pro", "qwen3-max"]

SYSTEM = (
    "You are a senior, highly critical reviewer for ACM Transactions on "
    "Software Engineering and Methodology (TOSEM). Your expertise spans "
    "software testing, metamorphic testing, the test-oracle problem, formal "
    "methods, empirical software engineering, and ML/equivariance theory. "
    "You review to TOSEM's bar: technical soundness, novelty over prior art, "
    "significance, presentation, and reproducibility. You are rigorous and "
    "honest, never flattering. You actively hunt for fatal flaws "
    "(publication blockers): unsupported claims, threats to validity, "
    "statistical selection bias, underpowered pilots reported as evidence, "
    "overclaimed generalisation, and gaps between theory and experiment. "
    "You separate fatal blockers from major-but-fixable weaknesses from minor "
    "issues. You give a clear recommendation and justify it concretely with "
    "section-anchored evidence."
)

USER_TMPL = """Below is the full LaTeX source of a manuscript submitted to TOSEM. \
Review it as an independent referee.

First, output a single fenced JSON block (```json ... ```) with EXACTLY this schema:

{{
  "overall_recommendation": "Accept | Minor Revision | Major Revision | Reject",
  "reviewer_confidence_1to5": <int>,
  "scores_1to5": {{
    "soundness": <int>,
    "novelty": <int>,
    "significance": <int>,
    "presentation": <int>,
    "reproducibility": <int>
  }},
  "summary": "<2-4 sentence neutral summary of what the paper claims and does>",
  "strengths": ["<concrete strength>", "..."],
  "publication_blockers": [
    {{"section": "<where>", "issue": "<the fatal problem>", "why_fatal": "<why it blocks publication>"}}
  ],
  "major_weaknesses": [
    {{"section": "<where>", "issue": "<problem>", "suggested_fix": "<actionable fix>"}}
  ],
  "minor_issues": ["<minor point>", "..."],
  "questions_to_authors": ["<question>", "..."]
}}

Rules for the JSON:
- If you find no true publication blocker, set "publication_blockers": [].
- Be specific and anchor to sections/claims; do not be vague.
- Scores: 1=very poor, 3=borderline, 5=excellent. Be calibrated to TOSEM, not generous.

After the JSON block, write your detailed free-form reviewer report (strengths, \
weaknesses, threats to validity, and what a revision must do to be acceptable).

=== MANUSCRIPT (LaTeX source) ===
{manuscript}
=== END MANUSCRIPT ==="""


def load_manuscript(path, _depth=0):
    r"""Read a .tex file and recursively inline \input / \include so the
    reviewer sees the complete self-contained manuscript (max depth 5)."""
    p = Path(path)
    text = p.read_text(encoding="utf-8", errors="replace")
    if _depth >= 5:
        return text
    base = p.parent

    def repl(m):
        inc = m.group(1).strip()
        for cand in (base / inc, base / (inc + ".tex")):
            if cand.is_file():
                return load_manuscript(cand, _depth + 1)
        return m.group(0)  # leave unresolved \input as-is

    return re.sub(r"\\(?:input|include)\{([^}]+)\}", repl, text)


def make_client():
    load_dotenv()
    base = os.environ.get("BASE_URL", "").rstrip("/")
    key = os.environ.get("API_KEY", "")
    if not base or not key:
        sys.exit("ERROR: BASE_URL / API_KEY missing in .env")
    if not base.endswith("/v1"):
        base += "/v1"
    return OpenAI(base_url=base, api_key=key, timeout=600.0)


def review_one(client, model, manuscript_text):
    prompt = USER_TMPL.format(manuscript=manuscript_text)
    last_err = None
    for attempt in range(2):
        try:
            t0 = time.time()
            resp = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": SYSTEM},
                    {"role": "user", "content": prompt},
                ],
            )
            text = resp.choices[0].message.content or ""
            usage = getattr(resp, "usage", None)
            return {
                "model": model,
                "status": "ok",
                "elapsed_s": round(time.time() - t0, 1),
                "text": text,
                "usage": {
                    "prompt": getattr(usage, "prompt_tokens", None),
                    "completion": getattr(usage, "completion_tokens", None),
                } if usage else None,
            }
        except Exception as e:  # noqa: BLE001 — report, retry once
            last_err = f"{type(e).__name__}: {str(e)[:300]}"
            if attempt == 0:
                time.sleep(30)
    return {"model": model, "status": "error", "error": last_err}


def extract_json(text):
    # Prefer the full body of a fenced ```json ... ``` block (robust to
    # trailing free-form report text after the block).
    m = re.search(r"```json\s*\n(.*?)\n```", text, re.S)
    if m:
        try:
            return json.loads(m.group(1))
        except Exception:
            pass
    # Fallback: widest brace span (greedy, not non-greedy).
    m = re.search(r"(\{.*\})", text, re.S)
    if m:
        try:
            return json.loads(m.group(1))
        except Exception:
            return None
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--manuscript", default="NOETHER_paper_arxiv.tex")
    ap.add_argument("--out", default="docs/review_2026-06-17/llm_panel")
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--models", nargs="*", default=None)
    args = ap.parse_args()

    text = load_manuscript(args.manuscript)
    models = args.models or (["glm-4.6"] if args.smoke else PANEL)
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    client = make_client()

    print(f"Manuscript: {args.manuscript} ({len(text)} chars) -> {len(models)} reviewer(s)")
    results = {}
    with cf.ThreadPoolExecutor(max_workers=len(models)) as ex:
        futs = {ex.submit(review_one, client, m, text): m for m in models}
        for fut in cf.as_completed(futs):
            r = fut.result()
            m = r["model"]
            results[m] = r
            safe = m.replace("/", "_")
            if r["status"] == "ok":
                (out / f"{safe}.md").write_text(r["text"], encoding="utf-8")
                js = extract_json(r["text"])
                if js:
                    (out / f"{safe}.json").write_text(
                        json.dumps(js, ensure_ascii=False, indent=2), encoding="utf-8")
                rec = (js or {}).get("overall_recommendation", "?")
                print(f"[ok]  {m:24s} {r['elapsed_s']:6.1f}s  {len(r['text']):6d} chars  "
                      f"json={'Y' if js else 'N'}  rec={rec}  usage={r.get('usage')}")
            else:
                print(f"[ERR] {m:24s} {r['error']}")

    (out / "_panel_summary.json").write_text(
        json.dumps({m: {k: v for k, v in r.items() if k != "text"}
                    for m, r in results.items()}, ensure_ascii=False, indent=2),
        encoding="utf-8")
    ok = sum(1 for r in results.values() if r["status"] == "ok")
    print(f"\nPanel done: {ok}/{len(models)} ok -> {out}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())

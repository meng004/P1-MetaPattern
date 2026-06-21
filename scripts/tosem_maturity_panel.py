#!/usr/bin/env python3
"""scripts/tosem_maturity_panel.py — Execute a skill-DESIGNED TOSEM maturity exam
across a 5-model LLM gateway panel.

Architecture (NOT two skills run separately):
  * DESIGNER = academic-paper-reviewer skill -> docs/review_2026-06-21/
    task_design_personas_rubric.md (5 personas + 5-dim weighted rubric +
    maturity JSON schema). This file is injected verbatim into every prompt.
  * EXECUTORS = 5 gateway models, each cold-reading the full manuscript and
    sitting the SAME designed exam independently.
  * SYNTHESIS = done by the orchestrator afterwards from the 5 JSON outputs.

Reuses the proven gateway client pattern from scripts/llm_reviewer_panel.py.
Secrets come from repo-root .env (BASE_URL + API_KEY); never hard-coded.

Usage:
  python3 scripts/tosem_maturity_panel.py \
    --manuscript NOETHER_paper_arxiv.tex \
    --design docs/review_2026-06-21/task_design_personas_rubric.md \
    --out docs/review_2026-06-21/gateway_panel
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

# User-specified executor panel for this round.
PANEL = ["grok-4.3", "gpt-5.5", "claude-opus-4-7", "qwen3-max", "glm-5.1"]

SYSTEM = (
    "You are an expert referee panel-of-one for ACM Transactions on Software "
    "Engineering and Methodology (TOSEM). You have been handed a peer-review "
    "TASK PACKAGE designed by a senior editorial consultant: it defines five "
    "reviewer personas (Editor-in-Chief, a methodology/theory+statistics "
    "reviewer, a metamorphic-testing domain reviewer, an equivariant-ML / "
    "safety-critical perspective reviewer, and a Devil's Advocate) and a "
    "calibrated five-dimension 0-100 scoring rubric. Your job is to EXECUTE "
    "that designed exam on the manuscript below: wear all five lenses, apply "
    "the rubric honestly at TOSEM's bar, and quantify submission maturity. "
    "You cold-read with no repository access. You are rigorous and never "
    "flattering; an author's self-disclosure of a weakness does NOT convert it "
    "into evidence or earn leniency. Hunt for fatal flaws (publication "
    "blockers), separate them from major-but-fixable and minor issues, and for "
    "every weakness decide whether it is fixable by writing alone or requires "
    "new experiments. Anchor every point to a specific section / table / "
    "theorem. Follow the output contract in the task package exactly."
)

USER_TMPL = """=== TASK PACKAGE (designed by academic-paper-reviewer skill — personas + rubric + output contract) ===
{design}
=== END TASK PACKAGE ===

Now EXECUTE the designed exam on the manuscript below. First output a single
fenced ```json block matching the schema in section D of the task package
EXACTLY (no extra keys, valid JSON). Then write your detailed free-form panel
report: per-persona findings, threats to validity, and precisely what a
revision must do to be acceptable at TOSEM. Be calibrated, not generous.

=== MANUSCRIPT (LaTeX source) ===
{manuscript}
=== END MANUSCRIPT ==="""


def load_manuscript(path, _depth=0):
    r"""Read a .tex file and recursively inline \input / \include (max depth 5)."""
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
        return m.group(0)

    return re.sub(r"\\(?:input|include)\{([^}]+)\}", repl, text)


def make_client():
    load_dotenv(dotenv_path=str(Path(__file__).resolve().parent.parent / ".env"))
    base = os.environ.get("BASE_URL", "").rstrip("/")
    key = os.environ.get("API_KEY", "")
    if not base or not key:
        sys.exit("ERROR: BASE_URL / API_KEY missing in .env")
    if not base.endswith("/v1"):
        base += "/v1"
    return OpenAI(base_url=base, api_key=key, timeout=900.0)


def review_one(client, model, prompt):
    last_err = None
    for attempt in range(3):
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
                "model": model, "status": "ok",
                "elapsed_s": round(time.time() - t0, 1), "text": text,
                "usage": {
                    "prompt": getattr(usage, "prompt_tokens", None),
                    "completion": getattr(usage, "completion_tokens", None),
                } if usage else None,
            }
        except Exception as e:  # noqa: BLE001 — report, retry up to twice
            last_err = f"{type(e).__name__}: {str(e)[:300]}"
            if attempt < 2:
                time.sleep(30)
    return {"model": model, "status": "error", "error": last_err}


def extract_json(text):
    m = re.search(r"```json\s*\n(.*?)\n```", text, re.S)
    if m:
        try:
            return json.loads(m.group(1))
        except Exception:
            pass
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
    ap.add_argument("--design", default="docs/review_2026-06-21/task_design_personas_rubric.md")
    ap.add_argument("--out", default="docs/review_2026-06-21/gateway_panel")
    ap.add_argument("--models", nargs="*", default=None)
    args = ap.parse_args()

    manuscript = load_manuscript(args.manuscript)
    design = Path(args.design).read_text(encoding="utf-8")
    prompt = USER_TMPL.format(design=design, manuscript=manuscript)
    models = args.models or PANEL
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    client = make_client()

    print(f"Manuscript: {args.manuscript} ({len(manuscript)} chars) | "
          f"design: {len(design)} chars | prompt: {len(prompt)} chars "
          f"-> {len(models)} executor(s): {', '.join(models)}")
    results = {}
    with cf.ThreadPoolExecutor(max_workers=len(models)) as ex:
        futs = {ex.submit(review_one, client, m, prompt): m for m in models}
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
                mat = (js or {}).get("submission_maturity_0to100", "?")
                print(f"[ok]  {m:20s} {r['elapsed_s']:6.1f}s  {len(r['text']):6d} chars  "
                      f"json={'Y' if js else 'N'}  rec={rec}  maturity={mat}  usage={r.get('usage')}")
            else:
                print(f"[ERR] {m:20s} {r['error']}")

    (out / "_panel_summary.json").write_text(
        json.dumps({m: {k: v for k, v in r.items() if k != "text"}
                    for m, r in results.items()}, ensure_ascii=False, indent=2),
        encoding="utf-8")
    ok = sum(1 for r in results.values() if r["status"] == "ok")
    print(f"\nPanel done: {ok}/{len(models)} ok -> {out}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())

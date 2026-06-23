#!/usr/bin/env python3
"""harvest_bug_candidates.py — mechanical, reproducible candidate harvest for the
B1 real-bug ledger (anti-cherry-pick).

Applies the FROZEN selection rule of prereg_b1_realbug.md §3.4: from each repo's
CLOSED issues labelled `bug` that have a linked merged fix PR, list the most-
recently-closed first. It does NOT decide the final ledger — the author still
applies the CPU-reproducible filter (prereg §2) by hand and records the verified
subset in bug_ledger.csv. This script only makes the candidate enumeration
mechanical and auditable so no cherry-picking enters at selection time.

It does NOT fabricate bugs: every row printed is a real GitHub issue URL the
author then verifies (fix commit, pre-fix parent, reproducing snippet, CPU-only).

Usage:
  GITHUB_TOKEN=ghp_xxx python3 harvest_bug_candidates.py --limit 40 > candidates.tsv
  # token optional (raises the 60/h anonymous rate limit to 5000/h); read-only scope.
Egress needed: api.github.com  (add to the cloud/author allowlist if run remotely).
"""
import argparse
import json
import os
import sys
import urllib.request
import urllib.parse

REPOS = ["e3nn/e3nn", "pyg-team/pytorch_geometric"]
API = "https://api.github.com"


def gh(path, params=None):
    url = f"{API}{path}"
    if params:
        url += "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={
        "Accept": "application/vnd.github+json",
        "User-Agent": "noether-b1-harvest",
    })
    tok = os.environ.get("GITHUB_TOKEN")
    if tok:
        req.add_header("Authorization", f"Bearer {tok}")
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode())


def linked_fix(repo, issue_number):
    """Best-effort: a closed bug issue is a candidate iff its timeline has a
    'closed' event with a linked commit, or a cross-referenced merged PR. We
    surface the timeline so the author can record fix_commit + parent by hand."""
    try:
        ev = gh(f"/repos/{repo}/issues/{issue_number}/timeline",
                {"per_page": 100})
        commits = [e.get("commit_id") for e in ev
                   if e.get("event") == "closed" and e.get("commit_id")]
        prs = [e.get("source", {}).get("issue", {}).get("number")
               for e in ev if e.get("event") == "cross-referenced"]
        return commits, [p for p in prs if p]
    except Exception as e:  # noqa: BLE001
        return [], [f"timeline-error:{type(e).__name__}"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=40,
                    help="max closed bug issues per repo to enumerate (recency order)")
    args = ap.parse_args()

    print("repo\tissue_url\tclosed_at\ttitle\tclosing_commits\tcross_ref_prs")
    for repo in REPOS:
        try:
            issues = gh(f"/repos/{repo}/issues", {
                "state": "closed", "labels": "bug",
                "sort": "updated", "direction": "desc",
                "per_page": min(args.limit, 100),
            })
        except Exception as e:  # noqa: BLE001
            print(f"# {repo}: list failed: {type(e).__name__}: {e}", file=sys.stderr)
            continue
        n = 0
        for it in issues:
            if "pull_request" in it:   # skip PRs themselves
                continue
            commits, prs = linked_fix(repo, it["number"])
            print("\t".join([
                repo, it["html_url"], it.get("closed_at") or "",
                (it.get("title") or "").replace("\t", " ")[:80],
                ",".join(c[:12] for c in commits) or "-",
                ",".join(str(p) for p in prs) or "-",
            ]))
            n += 1
            if n >= args.limit:
                break
    print("# NEXT: author verifies each candidate for {fix_commit, pre_fix_parent_commit,"
          " CPU-reproducible snippet}, then records the passing subset (<=10, cat-balanced,"
          " recency) into bug_ledger.csv and freezes per prereg §3.4.", file=sys.stderr)


if __name__ == "__main__":
    main()

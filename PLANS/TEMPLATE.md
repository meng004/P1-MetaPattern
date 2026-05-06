# PLAN-NNN: <one-line title>

**Issue**: ISSUES/NNN-<slug>.md
**Branch**: <branch-name>
**Drafted on**: local Claude Code | (other host — explain why rule 4 was skipped)

## Files to add / change

| Path | Action | Rationale |
|---|---|---|
| `scripts/foo.py` | new | one-line why |
| `set_n_mrs/<subject>/...` | regenerate | upstream of foo.py |
| `tests/test_foo.py` | new | rule 6 gate |

## Risks / tradeoffs

What could go wrong, and how we'll detect it.

## Test gate (rule 6)

- [ ] `tests/test_<area>.py` covers the new behavior
- [ ] `bash tests/run.sh` exits 0
- [ ] No new pyright errors (existing warnings ok)

## Estimated cost

| Step | Time | Where |
|---|---|---|
| Implement | <X> min | local |
| Run tests | <X> sec | anywhere |
| Pipeline re-run (if needed) | <X> h | local (rule 8) |

## Done when

(Same as issue success criteria, restated as a checklist for the executor.)

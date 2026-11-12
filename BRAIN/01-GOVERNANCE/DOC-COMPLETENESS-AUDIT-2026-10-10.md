# Documentation Completeness Audit — 2026-10-10

**Owner:** Naya 5 (standing responsibility, Shawn's order 2026-10-10)
**Standard:** Every intelligence artifact in 4 forms (machine/code, structured, AI, human) in all ideal locations.
**Scope:** 15 Smart Notes sampled + 5 recent laws. Against main tip `527ebcfb`.

## Scorecard: 15 Smart Notes

| Form | Score | Note |
|------|-------|------|
| Structured (canonical JSON) | 15/15 | All valid `naya.smart-note-capture.v2` |
| AI language (ai_view/naya_view) | 15/15 | All substantive |
| Human language (human_view/simple_view) | 15/15 | All substantive |
| Machine/code (executable consumer) | 0/15 | No decision path consumes the verified-lesson store (wiring manifest confirms) |

**Average: 3.0/4 forms.** The canonical JSON is well-formed for 3 forms; the executable form is the systemic gap.

### Locations

| Location | Status |
|----------|--------|
| Repo `.naya/capture/` | 15/15 ✓ |
| BRAIN mirror (`05-MEMORY/SMART-NOTES/`) | Partial (date-organized .md mirrors exist for some) |
| Doctrine/laws index | Weak (brain index: 4 law mentions) |
| Lessons/curriculum | 45-lesson curriculum NOT on main (on `naya5/activation-docs` branch) |
| Team memory | Partial (daily logs, not indexed per-note) |

## Scorecard: 5 recent laws (2026-10-09/10)

| Law | In repo before this change | Forms |
|-----|---------------------------|-------|
| Law of One (constitutional) | NO — only in local AGENTS.md | 0/4 → **4/4** |
| Calculator as Default | NO | 0/4 → **4/4** |
| Plain-Words Decision Format | NO | 0/4 → **4/4** |
| Reversibility Rule | NO | 0/4 → **4/4** |
| Engine-Before-Production | NO | 0/4 → **4/4** |

## What this change delivers

- **5 laws × 4 forms:** each law now has `.ai.md` (AI spec) + `.human.md` (plain words) + `.machine.json` (schema) in `BRAIN/01-GOVERNANCE/` + canonical Smart Note capture in `.naya/capture/` (all conformant per `sn002_conformance`).
- **Completeness checker:** `tools/doc_completeness_check.py` — validates 4 forms on Smart Notes and law triples. CI gate (`.github/workflows/doc-completeness-gate.yml`) runs it on changed files.
- **Pre-existing debt flagged, not hidden:** 22 `lifecycle_state` gaps on main (11 fixed by the `naya5/wo1-wo8-ignition` branch awaiting merge); law-triple warnings for single-form numbered laws.

## Standing ownership

- Weekly re-audit (every Monday): full-repo run, gap list, fill or schedule.
- Every new Smart Note / law: checker runs in CI on the PR.
- Next highest-value fills: 45-lesson curriculum placement (blocked on branch merge), single-form law triples, IB- file coverage.

# Merged Is Not Wired — A Gate With Zero Call Sites Enforces Nothing

**Intelligent Block:** IB-SMART-NOTE-20261012-sn1159-merged-not-enforced
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured date:** 2026-10-12
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #2175 board comment 6139000310 — [BUILDER] Lane 4 (Naya Mason), tick t0582b; PR #2509 (lane4/b60-smart-note-completeness-gate-wiring, unmerged, held under #2459 hold); receipt hidden_files/twelve-lane-receipts/t0582b-lane4.md.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## IN A NUTSHELL

A gate can be merged to main and still enforce nothing. PR #2501 merged the Smart Note completeness gate (`tools/completeness_gate.py`) — "Gate 3 of 7," law on paper. Lane 4 re-derived from live tip `e8b4868c` and found: a full-tree git grep shows exactly 2 files referencing the gate — the tool and its test. **Zero call sites.** Meanwhile CI's `doc-completeness-gate.yml` runs a *different* tool (`doc_completeness_check.py`, different corpus) whose similar name provided camouflage. The law was a dead tool in practice.

B-60 closed by wiring: PR #2509 adds one file — `.github/workflows/smart-note-completeness-gate.yml` — running the gate in changed-only mode on Smart-Notes PRs. Gate health-checked before wiring (26/26 tests, `--changed-only` exits 0), CI-green (14 checks), fully reversible by deleting the file, held unmerged under the #2459 hold.

**The durable rule: merged ≠ wired.** After any gate merges, grep the call sites before declaring it enforced. A gate with zero call sites is prose. And watch the same-name-different-tool camouflage: a CI file that *looks* like enforcement can be running something else entirely.

## HUMAN NOTE

When a seat says "the gate is on main," ask: "who calls it?" The merge record proves the tool exists. Only the call graph proves it enforces. Lane 4's forensics order is the template: (1) re-derive from the live tip what the merge actually touched (here: 2 files), (2) grep the full tree for call sites of the new mechanism, (3) identify what the similarly-named CI actually runs, (4) only then close the "not enforced" finding — by wiring an enforcement point, not by re-merging the tool. The repair must not redesign the gate (no design change, no threshold change in #2509) — it only supplies the missing invocation.

## CHILD NOTE

Imagine your family builds a smoke alarm and puts it on the shelf — but nobody mounts it on the ceiling or puts batteries in. It's *there*, but it protects nobody. That's what happened: the gate was built and merged (on the shelf) but nothing in the house ever called it (no batteries). Always check: is it actually switched on?

## GRANDMA NOTE

A law nobody follows isn't a law — it's a suggestion written on fancy paper. And a tool nobody runs isn't a tool — it's a decoration. When someone tells you "we have a system for that now," the wise question is: "show me where it runs."

## NAYA NOTE

For the distillation loop and future forensics seats: MERGED-NOT-ENFORCED is a named failure class, distinct from "law without code enforcement is commentary" (that one's about rules; this one's about merged code). When classifying a mechanism's enforcement state, the evidence ladder is: merged-on-main < called-by-something < fired-in-CI < fired-on-a-real-input. This finding sat at level 0. PR #2509 moved it to level 2 (CI wired); level 3 waits on the merge lane under the #2459 hold.

## MACHINE NOTE

```json
{
  "smart_note_id": "SN-1159",
  "intelligent_block_id": "IB-SMART-NOTE-20261012-sn1159-merged-not-enforced",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "category": "SYSTEM-INTELLIGENCE/SYSTEM-DESIGN/FAILURE-CLASSIFICATION",
  "failure_class": "MERGED-NOT-ENFORCED",
  "evidence": {
    "board_comment": "https://github.com/SoulSchoolAcademy/NayaPOWER/issues/2175#issuecomment-6139000310",
    "wiring_pr": "https://github.com/SoulSchoolAcademy/NayaPOWER/pull/2509",
    "call_site_count_at_live_tip": 0,
    "referencing_files": ["tools/completeness_gate.py", "its test"],
    "camouflage": "doc-completeness-gate.yml runs doc_completeness_check.py (different tool, different corpus)"
  },
  "cousins": ["SN-0987 (dead-in-prose-not-dead-in-code: about law; this is about merged code)"],
  "gate_check": "after any gate merges: grep call sites; zero call sites = prose"
}
```

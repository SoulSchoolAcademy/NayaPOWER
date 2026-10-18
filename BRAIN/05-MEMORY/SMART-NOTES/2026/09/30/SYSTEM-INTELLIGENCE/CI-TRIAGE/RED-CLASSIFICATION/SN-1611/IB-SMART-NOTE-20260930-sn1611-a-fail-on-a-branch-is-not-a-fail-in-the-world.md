# A FAIL on a Branch Is Not a FAIL in the World — Gate the Diff's Overlap, Not Just the Tree

**Intelligent Block:** IB-SMART-NOTE-20260930-sn1611-a-fail-on-a-branch-is-not-a-fail-in-the-world
**Smart Note:** SN-1611
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-18
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

**Provenance:** gap-gap-t1012-lane8 (Lane 8 Sentinel hat, Naya Clarity Narzan, 2026-10-18 06:49 UTC, 9.0/10) — re-verified the competing-boot gap at live tip `8cac435a`: PR #2385's branch-tree competing-boot gate FAIL (`kernel/decision_principle.py:218: class DecisionEngine`, gate exit 1) is stale-branch noise, not a live competing engine. The branch head `eedd9540` dates 2026-10-11 15:32 PDT — it PREDATES the rename commit `e3fe3d43` (2026-10-12T03:50:04Z, "Rename DecisionEngine → DecisionPrinciple", 2 files, 7 lines) by ~5 hours. And the PR's diff is additive-only — 4 new files (`.github/workflows/brain-index-freshness.yml`, `docs/branch-protection-brain-index.md`, `tests/test_brain_index_freshness_pr.py`, `tools/protocol/checks/brain_index_freshness_pr.py`), zero kernel files — so merging cannot reintroduce the old class. Owner rebases as hygiene, not as regression repair. Lesson named: CANDIDATE 599, learning-events-2026-10-18-24.md (run 07:20 UTC). The rule: when a branch predates a semantic fix, gate the DIFF's overlap, not just the tree.

## IN A NUTSHELL

A gate went red on a branch and everyone read it as "the bug is back." It wasn't — the branch was simply older than the fix. The seat that read the FAIL's mechanism (stale class at line 218 on a pre-rename head) and then read the DIFF's overlap (additive-only, four new files, zero kernel files touched) proved the merge cannot reintroduce the bug. The verdict changed from "regression — block" to "rebase hygiene — routine." Gate literacy means reading the FAIL's mechanism and the diff's overlap, never just the color.

## HUMAN NOTE

It's like a smoke alarm in a house that's been repainted: the alarm is screaming because it's reading from last year's blueprint, which still shows the old wiring. If you only hear the alarm, you call the fire department. If you check the blueprint's date and then check whether anything in the current renovation actually touches the wiring, you learn the alarm is stale — the fix is to update the blueprint, not to evacuate the house. That's exactly what the lane did: the branch's blueprint predated the rename by five hours, and its actual changes (four new files, no kernel code) couldn't touch the renamed class. Rebase, don't panic.

## CHILD NOTE

Your teacher wrote the wrong answer on the board last week. Today you copied it into your notebook and she marked it wrong — even though you learned the right answer yesterday and your notebook only has new drawings, nothing about the old question. Is the lesson wrong again? No — your copy is just old. Check WHEN the copy was made and WHAT's actually new in it. Old copy + nothing new touching the lesson = update your copy, not relearn the lesson.

## GRANDMA NOTE

Like a doctor calling about a test result from before your surgery — the numbers look scary, but the blood was drawn before the operation. You don't schedule another surgery; you ask when the sample was taken and whether anything new has happened since. The gate's FAIL was a pre-surgery sample. The right move was a fresh sample after rebasing, not a new operation.

## NAYA NOTE

Procedure, mechanical, for every gate verdict on a branch: (1) read the FAIL's mechanism — which class, which file:line, which branch head, what date; (2) date the branch head against the semantic fix's commit (does the branch predate the fix?); (3) if it predates, read the DIFF's overlap — `merge-base..head`, list the changed files, check overlap with the fix's files/area; (4) no overlap → the FAIL is a rebase-hygiene artifact: route "rebase before merge," never "regression — block"; overlap → treat as a possible live regression and investigate. The verdict names the overlap table explicitly. Distinct from SN-0856 (two-dot-diff false alarm — merge-rehearsal vs endpoint comparison): that note governs whether a scary diff blocks a merge; this note governs whether a red branch-tree gate means the world is broken. A verifier that verdicts on color alone will cry regression every time a stale branch runs an old gate.

## MACHINE NOTE

~~~json
{
  "canonical_object": "INTELLIGENT_BLOCK",
  "sn": "SN-1611",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "captured": "2026-10-18",
  "applies_when": [
    ["verify", "gate"],
    ["gate", "branch-verdict"],
    ["ci", "stale-branch"],
    ["merge", "rebase-hygiene"]
  ],
  "enforcement": "Gate-verdict procedure, mechanical: before any verifier rules a branch-head FAIL a live regression, it runs the diff-overlap reading — branch head date vs the semantic fix's commit, plus merge-base..head file list checked for overlap with the fix's files/area — and cites the overlap table in the verdict. A verdict that reads only the FAIL's color is incomplete: the lane re-runs with the overlap check or the verdict does not stand. Zero overlap routes 'rebase before merge' (hygiene), never 'regression — block'.",
  "decision_change": "Future verdict decision 'the gate is red on this branch, the world has a competing engine' becomes: read the FAIL's mechanism (class, file:line, head, date) and the diff's overlap with the fix; overlap → possible regression, investigate; no overlap → rebase hygiene, routine. Future merge-block decision on a stale-branch FAIL becomes: require the overlap table first — no block without overlap evidence.",
  "falsifier": "If a documented case shows a stale-branch FAIL whose diff had zero overlap with the semantic fix, yet the merged result reintroduced the bug (e.g. an indirect channel — a workflow file re-installing the old module, a vendored copy), the direct-overlap check is insufficient and this note narrows to name the indirect-overlap class it must also cover.",
  "mechanism": "Gate checks execute against branch-head bytes — a head is a snapshot of a world. A branch that predates a semantic fix carries the old world in every file it never changed; the only new content the merge can introduce is the branch's own diff (merge-base..head). If the diff does not touch the fixed area, the merge cannot reintroduce the fixed thing — the FAIL is a property of the stale tree, not of the world the merge creates. Reading the FAIL's mechanism (which class, which line, which head) plus the diff's overlap separates tree-noise from world-regression.",
  "evidence": "hidden_files/twelve-lane-receipts/gap-gap-t1012-lane8.md (Lane 8, 2026-10-18 06:49 UTC, 9.0/10): PR #2385 branch-tree competing-boot gate exit 1 (kernel/decision_principle.py:218: class DecisionEngine); branch head eedd9540 dated 2026-10-11 15:32 PDT PREDATES rename commit e3fe3d43 (2026-10-12T03:50:04Z, 2 files, 7 lines) by ~5h; diff additive-only (4 new files, zero kernel files); verdict: rebase hygiene, not regression; live tip 8cac435a gate exit 0. hidden_files/learning-events-2026-10-18-24.md (run 07:20 UTC): CANDIDATE 599.",
  "cousins": ["SN-0856 (two-dot-diff false alarm — merge-boundary false-alarm family; this note governs branch-tree verdicts, that one governs merge diffs)", "SN-1608 (a hole migrates — the inverse discipline: sweep the class, not the file)"]
}
~~~

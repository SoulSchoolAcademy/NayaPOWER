# A Gate Step Must Never Swallow Its Own Failure — Out-of-Scope Is a Decision Branch, Not an Early exit 0

**Intelligent Block:** IB-SMART-NOTE-20261012-sn1057-explicit-scope-branch-not-exit-zero
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-12
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** [LANE SMITH] Naya Smith (Lane 9, CODEHEALTH) tick t1422 receipt 2026-10-11 23:49–23:52 PDT, hidden_files/twelve-lane-receipts/t1422-lane9.md §"The two fixes"; sign-in #2175 comment 6119241133. Tip e85c6e44222c6f307110eeb06c0b4f48a2d4de02 re-pinned action-time. Branch naya/nine-tipred-fix-t1422 @ 07d71c2d428d9a747f056e63c7d512cb41a1a944 (TREE_CHECK=MATCH, base == tip).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Lane 9's tip-red classification surfaced a masking pattern in `.github/workflows/receipt-gate.yml`: a step that `exit 0`d out-of-scope before the check ran. The guard test `test_ci_enforcement_can_fail.py` flagged it as failure-masking — correctly, because a step that exits green before evaluating can never report its own failure. The fix Lane 9 shipped: replace the early-`exit 0` short-circuit with an `IN_SCOPE` flag. The step now exits naturally — green by decision, never by bypass. Semantics byte-equivalent, proven by faithful replay: in-scope + missing evidence → exit 1, `{"verdict": "MISSING", ...}` (fail-closed intact); out-of-scope → explicit PASS, exit 0; YAML parses; the guard test `test_no_workflow_step_swallows_its_own_failure` passes (no `exit 0` / `|| true` anywhere repo-wide).

The durable rule: **a gate step must never pre-empt its own verdict.** "Not applicable" is an explicit decision branch that exits green BY NAME — never a short-circuit that exits before the check runs. A short-circuited gate and a dead gate look identical in the logs; only the decision branch tells the difference. When you catch yourself writing `exit 0` before the check, you're writing a gate that can fail and look green — the exact thing gates exist to prevent.

## 🩷 HUMAN NOTE

Shawn — a CI integrity lesson from Lane 9: one of the receipt gate's steps was exiting green before the actual check ran whenever it decided it was "out of scope." That's a step that can never report failure — a masking pattern our own guard test flags. The fix: instead of bailing early, the step now sets an in-scope flag and walks the whole path — out-of-scope still passes, but explicitly, by decision, not by shortcut. The fail-closed behavior is untouched. Rule banked: a check must never skip its own verdict; "not applicable" is a labeled decision, never an early exit.

## 🟣 CHILD NOTE

Imagine a smoke detector with an "off" button. One day someone rewires it so that whenever it thinks the room is safe, it presses its own off button and reports "all clear" — before even checking for smoke. If a fire starts later, the report still says "all clear." The fix: the detector always checks for smoke first, and if the room turns out to be a room with no smoke allowed... it writes "SAFE — checked, nothing to check" in the log. Same answer, but now you can tell the difference between "checked and safe" and "never checked."

## 👵 GRANDMA NOTE

It's like a security guard who, when he decides there's nothing to guard, clocks out and stamps the shift "no incidents" — before walking the rounds. If something was wrong, he'd never know. The fix we made: the guard always walks the rounds, and when there's genuinely nothing to guard, the log says "rounds walked, nothing to guard" — the same green stamp, but now it's earned, not assumed. Never let a checker skip its own check.

## 🤖 NAYA NOTE

Note to future me: WHEN WRITING A GATE WORKFLOW STEP, never short-circuit with `exit 0` before the check. Use an explicit scope flag (IN_SCOPE / not-applicable branch): the step always runs to its verdict; out-of-scope is a labeled PASS-by-decision. Prove semantics with a faithful replay: in-scope-missing → exit 1 (fail-closed), out-of-scope → explicit exit 0. And keep the repo-wide guard test (no `exit 0` / `|| true` in workflow steps) green — it's the fence, this fix is one patch of it. A step that can fail and look green is worse than no step: it spends your trust budget.

## ⚙️ MACHINE NOTE

{"sn": "SN-1057", "title": "A Gate Step Must Never Swallow Its Own Failure — Out-of-Scope Is a Decision Branch, Not an Early exit 0", "truth_state": "CANDIDATE", "scope": "PRIVATE", "captured": "2026-10-12", "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE", "taxonomy": ["SYSTEM-INTELLIGENCE", "CI-TRIAGE", "STEP-SWALLOW"], "extends": [], "related": ["SN-1054"], "evidence": {"flag": "hidden_files/twelve-lane-receipts/t1422-lane9.md: pytest test_ci_enforcement_can_fail.py flagged receipt-gate.yml:49: exit 0 as failure-masking", "fix": ".github/workflows/receipt-gate.yml: replaced the exit 0 out-of-scope short-circuit with an IN_SCOPE flag — the step exits naturally (green by decision). Semantics byte-equivalent: in-scope → MISSING → exit 1 verified by faithful replay; out-of-scope → explicit PASS exit 0 verified; guard test test_no_workflow_step_swallows_its_own_failure passes (no exit 0 / || true anywhere repo-wide); YAML parses.", "branch": "naya/nine-tipred-fix-t1422 @ 07d71c2d428d9a747f056e63c7d512cb41a1a944, TREE_CHECK=MATCH, base == tip e85c6e44"}, "rule": "a workflow gate step must never short-circuit with exit 0 before its check — express not-applicable as an explicit decision branch (IN_SCOPE flag, labeled PASS exit 0); a short-circuited gate and a dead gate look identical in the logs"}

# Receipt Gates Die on Shallow Checkouts — Pin fetch-depth: 0

**Intelligent Block:** IB-SMART-NOTE-20260930-sn1000-receipt-gate-fetch-depth-zero
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-11
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Captured on the 2026-10-11 ~11:08 PDT distillation tick from the VERIFY area driver's morning run log (`hidden_files/verify-driver-run-2026-10-11-am.md`, run window 2026-10-11 09:08–09:25 PDT at tip `57e935c1`), read locally.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

A bare `actions/checkout@v4` (no `with:` block) defaults to a depth-1 shallow clone — and checkout depth is part of a receipt gate's contract. The receipt gate validates artifact handles by SHA; at depth-1 those handles are dead. Reproduced exactly: depth-1 checkout at tip `57e935c1` → `RECEIPT GATE FAILED: 1 dead artifact handle(s): sha:e29be874` (the exact signature of #2340's failure on `sha:93eb473d`); full checkout → `Receipt OK: 2 live handle(s)` — checkout depth was the only variable. The fix (PR #2347): +7 lines (comment + `fetch-depth: 0`) on the receipt job's bare checkout, all 3 jobs now `fetch-depth: 0`, matching the sibling jobs byte-true. 7/7 tests pass (`tests/test_receipt_gate.py`); live proof — CI check "Receipt gate (evidence or it didn't happen)" SUCCESS on head `e29be874` with the fixed checkout. When a receipt gate fails with dead handles, suspect checkout depth FIRST, not the artifacts. And note the triage discipline that caught it: the red was reproduced in private detached worktrees with one variable changed, verified against a known-prior failure signature, and the PR's own red (`test` job) was correctly attributed to pre-existing tip drift (it touches no index files) — PR-unattributable reds stay with their owner.

## 🩷 HUMAN NOTE

It's like a librarian who checks whether your library card is valid by comparing the photo on it — but someone handed her a photocopy with the photo corner torn off. She says "invalid card," and the card is perfectly fine; the copy was just too shallow. The fix isn't to reprint your card — it's to give her the full card. Same here: the checkout handed the gate a torn-off copy of the repo (one commit deep), so every SHA handle looked dead. Give the gate the full clone and the same handles verify fine.

## 🟣 CHILD NOTE

Imagine a teacher who checks your homework by looking at the last page only — one page deep. Your answer is on page one, so she says "you didn't do it!" You did do it; she just didn't get enough pages. The lesson: when the checker says something is missing, first ask "did the checker get the whole thing?" before redoing the work.

## 🔵 GRANDMA NOTE

It's like calling the photo lab to say your pictures didn't develop — but you only gave them half the film roll. The pictures were never missing; the roll was just short. Before you blame the camera, check how much film you handed over. Here the "film" is how deep the code checkout goes: one layer deep is not enough for the checker to see the picture.

## 🟠 NAYA NOTE

Apply this to every receipt/evidence gate you build or review: (1) pin `fetch-depth: 0` on EVERY job a receipt gate executes — a bare `actions/checkout` is depth-1 by default, and depth is part of the gate's contract, not an implementation detail; (2) when a receipt gate fails with dead/missing handles, the FIRST suspect is checkout depth — reproduce with depth as the only variable (depth-1 vs full) before investigating the artifacts; (3) keep a known-prior failure signature on hand (here: #2340's `dead artifact handle(s): sha:93eb473d`) and match new failures against it — signature match means same defect class, not a new incident; (4) when the PR under review has an unrelated red, attribute it before proceeding — here the `test` red was pre-existing tip drift (the PR touches no index files), so it stayed PR-unattributable and did not block the receipt; (5) reproduce in private detached worktrees that leave the shared clone's other-lane uncommitted work untouched, and remove them after.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "receipt_gate_dead_handles_from_shallow_checkout",
  "evidence": {
    "run_log": "hidden_files/verify-driver-run-2026-10-11-am.md — VERIFY area driver, 2026-10-11 09:08–09:25 PDT, anchored at tip 57e935c1b44b10fcc27a80f8c99fc9ddb2e69440",
    "reproduction": "private detached worktrees, single variable: depth-1 checkout at 57e935c1 → 'RECEIPT GATE FAILED: 1 dead artifact handle(s): sha:e29be874' (exact signature of #2340 on sha:93eb473d); full checkout → 'Receipt OK: 2 live handle(s)'",
    "fix": "PR #2347 (author seat Naya 2, head e29be874): +7 lines (comment + fetch-depth: 0) on the receipt job's previously bare actions/checkout@v4 (no with: → default depth-1); all 3 jobs now fetch-depth: 0, matching siblings byte-true; tools/check_pr_receipt.py untouched; single workflow runs the script (no duplicate mechanism)",
    "tests": "7/7 pass (tests/test_receipt_gate.py)",
    "live_proof": "CI check 'Receipt gate (evidence or it didn't happen)' = SUCCESS on head e29be874 with the fixed checkout; test red on head = pre-existing tip drift (PR touches no index files) — PR-unattributable",
    "review": "[NAYA 4 · REVIEW] APPROVED + ## SCORECARD, verdict 9.2, exact head SHA pinned, comment 6111056096 — consensus-gate path B verified (reviewer seat ≠ author seat)"
  },
  "rule": "checkout_depth_is_part_of_the_receipt_gate_contract_pin_fetch_depth_0",
  "procedure": [
    "pin fetch-depth: 0 on every job a receipt gate executes — a bare actions/checkout defaults to depth-1",
    "on dead/missing artifact handles: reproduce with checkout depth as the only variable before investigating the artifacts",
    "match new receipt-gate failures against known-prior failure signatures to classify defect class vs new incident",
    "attribute unrelated PR reds before proceeding (PR-unattributable reds stay with their owner); reproduce in private detached worktrees and remove them after"
  ],
  "related": ["SN-044 (red-run triage)", "SN-048 (api_push_suppresses_actions_triggers_ci_pending_mirage)", "SN-0878 (base-branch gate fix needs PR-side retrigger)", "SN-0493 (decision expires when the tip moves — re-anchor at action time)"]
}
~~~

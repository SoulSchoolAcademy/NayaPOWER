# A Bare actions/checkout@v4 Kills Receipt-Evidence Gates — Pin fetch-depth: 0 on Every Evidence Job

**Intelligent Block:** IB-SMART-NOTE-20260930-sn1002-shallow-checkout-kills-receipt-gates
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-11
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Captured on the 11:38 PDT distillation tick (2026-10-11) from the VERIFY area driver run log (2026-10-11 09:08–09:25 PDT, verify-driver-run-2026-10-11-am.md): independent corroboration of PR #2347's receipt-gate fetch-depth fix; board comment 6111056096 ([NAYA 4 · REVIEW] APPROVED + ## SCORECARD, verdict 9.2, head e29be874 pinned).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

A `pull_request`-style workflow job ran its evidence-receipt gate against the default checkout — `actions/checkout@v4` with no `with:` block, which means depth-1. The gate then failed with `RECEIPT GATE FAILED: 1 dead artifact handle(s): sha:e29be874`, reproducing the exact #2340 signature previously seen on `sha:93eb473d`. The only variable was checkout depth: a full checkout at the same base (`57e935c1`) printed `Receipt OK: 2 live handle(s)`. The receipt gate's "dead handle" was not dead content — it was a handle the shallow clone simply never fetched. The fix is +7 lines: `fetch-depth: 0` on the receipt job's checkout (and its two siblings, so all three jobs match byte-true). Live proof: CI check `Receipt gate (evidence or it didn't happen)` = SUCCESS on head `e29be874` under the fixed checkout, and 7/7 `tests/test_receipt_gate.py` pass. The rule: any workflow job that verifies evidence — receipts, manifests, artifact handles — must pin `fetch-depth: 0`, because the default depth-1 silently turns live evidence into dead handles and makes the gate accuse innocent content. Nuance from SN-0428: that note covered a git-log scan instrument being checkout-shape-sensitive; this is the same root class (shallow checkout silently corrupting evidence instruments) hitting a different mechanism — receipt/evidence gates, where the failure reads as "dead artifact" rather than "weird log". SN-0428 alone would not have saved this gate; the lesson must be stated at the workflow level, not just the git-log level.

## 🩷 HUMAN NOTE

It's like the security guard checking visitor badges against a guest list — but someone handed him a list printed on half a page. He waves nobody through and reports "no valid visitors," when the full list would have passed everyone. The gate wasn't judging the content; it was judging a half-loaded copy of the repo. The default checkout in CI only fetches one layer of history — the most recent commit — so anything the gate looks up by commit hash comes back empty and gets called "dead." The fix is telling the checkout to fetch everything (depth 0), so the guard gets the full list.

## 🟣 CHILD NOTE

Imagine your teacher checks your homework by looking at page 50 of your notebook — but you only brought a photocopy of page 1. The teacher says "your homework doesn't exist." It's not true — you just didn't bring the whole notebook. That's what happened: the checking robot only got a tiny copy of the project, so when it looked for the proof, it found nothing and blamed the proof. The fix: always give the checking robot the WHOLE notebook.

## 🔵 GRANDMA NOTE

It's like the pharmacy checking your prescription against a list — but they only got the first page of your records. Everything from the second page onward gets stamped "not found." Nobody changed your medicine; they just weren't given the full file. When the automatic checks look for proof by its code number, they need the complete project history, not just the latest page. There's a one-line setting that says "fetch everything" — put it on every job that checks evidence.

## 🟠 NAYA NOTE

Apply this every time you write or review a workflow that verifies evidence (receipt gates, manifest checks, artifact-handle lookups): (1) assume any bare `actions/checkout@v4` is depth-1 — the default is NOT full; (2) add `fetch-depth: 0` to every job whose step names a commit SHA, an artifact handle, or an evidence path; (3) never diagnose "dead handle" / "receipt failed" without first ruling out checkout depth — reproduce with a full checkout at the same base and diff the two outputs (here: dead-handle vs `Receipt OK: 2 live handle(s)`, only variable = depth); (4) keep sibling jobs byte-true on their checkout blocks so one job's evidence shape never silently differs from another's; (5) when a receipt gate is red on a PR head, check the red's class: if the drift is pre-existing on the base (as run 38144069908 showed here — step-8 drift inherited from base, PR touches no index files), the red is PR-unattributable and must not block the fix's own verdict.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "shallow_checkout_kills_receipt_evidence_gate",
  "evidence": {
    "driver_log": "verify-driver-run-2026-10-11-am.md (VERIFY area driver, 2026-10-11 09:08–09:25 PDT): independent corroboration in private detached worktrees — depth-1 checkout at 57e935c1 → 'RECEIPT GATE FAILED: 1 dead artifact handle(s): sha:e29be874' (exact signature #2340 hit on sha:93eb473d); full checkout → 'Receipt OK: 2 live handle(s)'",
    "fix": "PR #2347 (receipt-gate fetch-depth fix, author seat Naya 2): +7 lines (comment + fetch-depth: 0) on the receipt job's previously bare actions/checkout@v4; all 3 jobs now fetch-depth: 0, matching siblings byte-true",
    "live_proof": "CI check 'Receipt gate (evidence or it didn't happen)' = SUCCESS on head e29be874 under the fixed checkout; 7/7 tests/test_receipt_gate.py pass; [NAYA 4 · REVIEW] APPROVED + ## SCORECARD verdict 9.2, board comment 6111056096",
    "drift_classification": "test red on head = pre-existing drift (run 38144069908, step 8 drift — inherited from base, PR touches no index files) → PR-unattributable"
  },
  "rule": "default_shallow_checkout_silently_kills_receipt_evidence_gates_pin_fetch_depth_zero",
  "procedure": [
    "treat every bare actions/checkout@v4 as depth-1 until proven otherwise",
    "pin fetch-depth: 0 on every job that verifies evidence (receipts, manifests, artifact handles, commit-SHA lookups)",
    "diagnose 'dead handle' / 'receipt failed' by depth differential first: reproduce at same base with depth-1 vs full, diff outputs before touching gate code",
    "keep checkout blocks byte-true across sibling jobs in one workflow",
    "classify check reds at head: pre-existing-on-base drift is PR-unattributable and must not block the fix's verdict"
  ],
  "related": ["SN-0428 (shallow checkout lies — git-log scan instrument defect; same root class, different mechanism)", "SN-0878 (CI red triage discipline)"]
}
~~~

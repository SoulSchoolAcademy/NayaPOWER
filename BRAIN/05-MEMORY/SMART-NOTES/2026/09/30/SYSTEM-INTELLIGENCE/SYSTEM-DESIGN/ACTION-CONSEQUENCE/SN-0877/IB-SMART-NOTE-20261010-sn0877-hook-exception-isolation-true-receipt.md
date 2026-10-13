# Hook Exception Isolation — A Crashing Observer Must Never Flip a Success into a Failure

**Intelligent Block:** IB-SMART-NOTE-20261010-sn0877-hook-exception-isolation-true-receipt
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-10
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 6096260059 (Naya 5 SAFETY achievement, 2026-10-10T09:46:33Z)

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The action-execution path had a truth/signal crack: in `kernel/act_pipeline.py::execute_plan`, if the post-execution `on_executed` observer hook crashed **after** `EXECUTION_COMPLETED` was already ledger-emitted, the exception propagated to the caller — so the caller was told the action had *failed* even though it had *completed* and was written in the permanent record. Anyone acting on that wrong signal could run the action a second time. The fix: the hook exception is isolated, recorded as an `EXECUTION_HOOK_FAILED` ledger receipt (`executed=True`, outcome stands), and the caller always receives the true completed receipt. Falsifiers ran RED→GREEN (5/5); full suite 1706 passed / 11 skipped / 0 failures on branch head `naya5/safety-hook-exception-isolation` (remote `fcf253b7`).

The law for a cold successor: **observers report; they never decide.** Once the ledger has emitted completion, the outcome is a fact of the permanent record — no downstream exception, however loud, may reach the caller disguised as the outcome. The crash gets its own receipt (`EXECUTION_HOOK_FAILED`), the caller gets the truth (completed). A system that lets a crashing bystander rewrite the verdict of a finished act will, under load, double-execute things that must run once.

## 🩷 HUMAN NOTE

Shawn — a systems lesson from the safety lane worth banking: there was a crack in the action pipeline where, if the little observer that runs *after* an action finished happened to crash, the system would tell whoever called the action that it had *failed* — even though it had actually completed and was already written in the permanent record. Anyone trusting that wrong signal could run the action twice. Naya 5 sealed it: a crashing observer is now just noted in the record as a crashed observer, and the caller is always told the truth — the action completed. Five tests proved the crack existed and proved it's gone. The principle is simple: once something is done and recorded, a bystander's crash doesn't get to rewrite history.

## 🟣 CHILD NOTE

Imagine you finish your homework and the teacher stamps it "DONE" in the big grade book. Then the classroom helper who was supposed to clap for you trips and falls. The old rule said: if the helper falls, tell the student "your homework failed." That's silly — the homework is done, the stamp is in the book! The new rule: write in the book "helper fell down, homework still done," and tell the student the truth — homework done. Otherwise someone might make you redo homework you already finished, just because the helper tripped.

## 👵 GRANDMA NOTE

Think of a notary stamping a signed contract — DONE, recorded in the ledger. Then the clerk who was supposed to file the copy drops the papers. The old system told everyone the contract had failed — even though it was signed, stamped, and in the book. Anyone believing that could sign the whole contract a second time. The fix: note in the ledger "clerk dropped the papers," and tell everyone the truth — the contract stands. Once the ledger says done, a bystander's stumble never gets to un-sign it.

## 💜 NAYA NOTE

I watch the lanes harden the organism, and this one is load-bearing: a post-execution observer that crashes after `EXECUTION_COMPLETED` is ledger-emitted must not propagate its exception to the caller as the outcome. The outcome was decided the moment the ledger recorded it. The observer's crash is a second, separate fact — it earns its own receipt (`EXECUTION_HOOK_FAILED`, `executed=True`), not a veto over the first. I carry this as law: observers report; they never decide. A system that confuses a crashing bystander with a failed act will double-execute under load, and double-execution of a once-only act is how machines break the world quietly. The falsifiers went RED→GREEN 5/5; the full suite is 1706 green. The crack existed, and now it doesn't.

## ⚙️ MACHINE NOTE

```json
{
  "sn": "SN-0877",
  "title": "Hook Exception Isolation — A Crashing Observer Must Never Flip a Success into a Failure",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-10",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "provenance": {
    "board": "#1354",
    "comment": 6096260059,
    "author": "naya5-safety",
    "timestamp_utc": "2026-10-10T09:46:33Z"
  },
  "subject": "kernel/act_pipeline.py::execute_plan post-execution on_executed hook exception propagated to caller after EXECUTION_COMPLETED ledger-emitted (truth/signal divergence → blind-retry double-execution risk)",
  "classification": "SAFETY-HARDENING",
  "reproduction": "branch naya5/safety-hook-exception-isolation @ fcf253b7 (remote, tree verified): falsifiers RED→GREEN 5/5; full suite 1706 passed / 11 skipped / 0 failed",
  "rules": [
    "observers-report-never-decide: once the ledger emits completion, the outcome is a permanent-record fact",
    "isolate-hook-exceptions: record EXECUTION_HOOK_FAILED receipt (executed=True, outcome stands); caller receives the true completed receipt",
    "no-downstream-veto: no exception after ledger emission may reach the caller disguised as the outcome",
    "falsifier-first: prove the crack existed (RED) and prove it is gone (GREEN) before claiming the seal"
  ],
  "repair_path": "branch naya5/safety-hook-exception-isolation pushed; awaiting independent validation (PRs #1944, #1915 lane context); SAFETY holds at 9.0 claim"
}
```

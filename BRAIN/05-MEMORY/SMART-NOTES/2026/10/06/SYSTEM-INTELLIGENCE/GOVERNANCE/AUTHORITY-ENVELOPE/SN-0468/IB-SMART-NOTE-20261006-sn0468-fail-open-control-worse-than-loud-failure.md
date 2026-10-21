# A Control That Fails Open and Silent Is Worse Than One That Fails Loud

**Intelligent Block:** IB-SMART-NOTE-20261006-sn0468-fail-open-control-worse-than-loud-failure
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-06
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** [CODA 1] SIGN-OUT — edge-function sweep (#1354 comment 6021812310, 2026-10-06 17:31:41Z); PR #1624 merged as `ad20ddcff`.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The edge-function sweep found `insertIdempotentActionReceipt(admin, { ... })` called with 2 arguments against a 3-parameter signature — so `idempotency_key` was `undefined` on every governed-action receipt. The enforcing unique index is partial (`where idempotency_key is not null`), so null keys never collide: the replay-detection branch, the `IDEMPOTENCY_KEY_REUSE_CONFLICT` guard, the outcome-recovery path, and the key-reuse fingerprint check were all unreachable code. The PROVE `stableJson` bug threw a loud opaque HTTP 400 — visible, and fixed. This failed open and said nothing: receipts were written as though idempotency were working. A governance control that appears present and is not is strictly more dangerous than one that is visibly broken, because visible breakage gets fixed and invisible breakage gets trusted. Two companions landed in the same repair: (1) a gate that cannot run must FAIL, never skip — the new `tsc` typecheck gate test fails when the compiler can't execute, because silent skip is the failure mode the whole change exists to remove; (2) verify the gate has teeth before trusting it — the test compiles three mutants against the real config and requires the exact TS errors (TS2304 unbound identifier, TS2554 wrong arity, TS2845 impossible condition) before the commit lands.

## HUMAN NOTE

A smoke detector with dead batteries doesn't beep — it just sits on the ceiling looking like protection. That's what this bug was: the duplicate-action protection for governed receipts was wired up, tested in theory, and completely inert in production, because the key it needed was silently empty. The scarier part: nobody would ever notice, because nothing failed. Compare with the PROVE bug in the same family — that one crashed loudly, which is actually the better failure: you can see a crash. From now on, two rules: first, when you build a gate, make the gate's own inability to run a hard failure (never a quiet skip — a skipped test is the same dead battery). Second, prove the gate can actually catch the thing it guards by feeding it three broken versions and watching it reject each one, before you ship.

## CHILD NOTE

The "no double-spending" rule for actions was like a lock on a door — but the keyhole was empty, so every door just swung open and nobody heard a thing. A lock that clicks loudly when it's broken is better than one that smiles and does nothing. And a guard who falls asleep on duty should sound the alarm, not quietly pretend everything is fine.

## GRANDMA NOTE

We had a safety switch that was supposed to prevent double actions, but it was never actually receiving the signal it needed — so it stayed quiet while duplicates slipped through. A safety switch that fails silently is more dangerous than one that fails noisily, because at least with noise someone comes to fix it. The new rule: if the checker itself can't run, that's a failure — not a "skip." And we test the checker with three known-bad versions to make sure it really catches bad things.

## NAYA NOTE

Future Naya: when you audit a governance control, ask two questions in order: (1) can this control fail open? — check arity/call-site mismatches, nullable keys feeding partial indexes, and any default that turns a guard into decoration; (2) can its verification fail silent? — grep your test gates for skip-on-unavailable-instrument and convert them to fail. The mutant pattern from this repair is the standard: for every new gate, construct ≥3 mutants representing the defect classes that actually shipped, verify each produces exactly the expected rejection against the real config, and commit only after the gate's teeth are proven. Also note the open wound: receipts already written with null `idempotency_key` were not repaired by the code fix — whether duplicate receipts exist in production is a database question behind Shawn's gate. Code that stops the bleeding does not tell you how deep the wound was.

## MACHINE NOTE

```json
{
  "sn": "SN-0468",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-06",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "rule": "A governance control that fails open and silent is strictly more dangerous than one that fails loud; a verification gate whose instrument is unavailable must FAIL, never skip; prove a gate's teeth with mutants before trusting it.",
  "anti_rule": "Trusting a control because it is present in the codebase; letting a gate report success when it could not execute; shipping a gate whose rejections were never demonstrated.",
  "verification": "PR #1624 merged ad20ddcff; tsc 0 errors across 14/14 edge functions; node 269/269 with 5 gate tests; three mutants verified to produce exactly TS2304/TS2554/TS2845 before commit; CI runs 37503829484/611/605 SUCCESS.",
  "provenance": ["#1354 comment 6021812310", "PR #1624", "tests/edge-typecheck-gate.test.mjs"],
  "related": ["SN-0439 (400 is a deterministic rejection — loud beats silent)", "SN-0421 (skipped jobs are vacuous)", "SN-0438 (fail-closed promotion gate)"],
  "open_wound": "Historical null-idempotency_key receipts in production unverified — database question behind Shawn's gate (comment 6021812310 'One next action').",
  "smart_link": "https://github.com/SoulSchoolAcademy/NayaPOWER/issues/1354#issuecomment-6021812310"
}
```

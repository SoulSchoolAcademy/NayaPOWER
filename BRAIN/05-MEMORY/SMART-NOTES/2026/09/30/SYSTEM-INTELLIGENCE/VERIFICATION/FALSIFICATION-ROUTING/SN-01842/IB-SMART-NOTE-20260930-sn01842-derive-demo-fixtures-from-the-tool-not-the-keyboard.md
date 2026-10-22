# Re-Count the Fixture: Fail-Closed Demos Get Their Fixtures From the Tool, Not the Keyboard

**Intelligent Block:** IB-SMART-NOTE-20260930-sn01842-derive-demo-fixtures-from-the-tool-not-the-keyboard
**Smart Note:** SN-1842
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-22
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

**Provenance:** hidden_files/twelve-lane-receipts/gap-t952-lane9.md (2026-10-22 12:50–13:00 PDT, Naya Clarity Narzan, Lane 9 Smith hat, gap follow-up on t952); brief-queue/done/brief-gap-t952-lane9.md; main tip at action time 4e941e0524774c613323a2fa9b27467704bf30f0 (fresh depth-1 clone per MIRROR GUARD); pytest tests/test_receipt_pin_gate.py 19/19 green on current main bytes.

## ✦ IN A NUTSHELL

Lane 9 closed the t952 gap by re-running the receipt-pin gate's 19/19 tests and three fail-closed demos on current main bytes. Reproducing the stale-SHA demo, the seat hand-typed a 42-character fixture instead of 40 — and the gate correctly returned TAMPERED, exit 1. The tool was right; the fixture was wrong. The lesson: in a fail-closed demo, the fixture is part of the proof — derive demo fixtures from the tool's own generators (or re-count the bytes at action time), never from the keyboard. A hand-typed fixture can exercise the wrong check leg and make a correct gate look broken, inverting the blame onto the tool. The receipt's own line: "A demo nobody re-counts is a demo nobody verified — the byte-count is part of the proof."

## 🩷 HUMAN NOTE

Imagine testing a lock by picking it — but you accidentally grab the wrong key blank from the drawer, one that's too long. The lock correctly refuses it, and you almost file a report that the lock is broken. The lock was fine; your test key was wrong. That's exactly what happened here: the verifier hand-typed a fake "stale" code with 42 characters instead of the 40 the system expects, the gate correctly called it tampered, and the first reading could have been "the gate misbehaves." The durable rule: when you reproduce someone's security test, generate the test inputs from the tool itself (or count the characters yourself, live) — never type them by hand and trust your fingers. The test input is part of the evidence, not a detail you can improvise.

## 🟣 CHILD NOTE

If you're checking whether the cookie jar lid works, you can't use a pretend cookie you drew — the lid will say "that's not a real cookie!" and you'd think the lid is broken. Make the test cookie the right way (the recipe the lid knows), and then the lid's answer actually tells you about the lid.

## 🔵 GRANDMA NOTE

Darling, it's like testing the new deadbolt with a key you filed down yourself by eye. If the key is one groove off, the lock rightly refuses it — and you'd be wrong to blame the locksmith. When you check someone else's work, use the tools' own measuring tape, not your best guess. Count twice, cut once, and count the test pieces too.

## 🟠 NAYA NOTE

This is the verifier-side mirror of a family we've been building all month — and its new dimension is worth naming precisely. SN-01522: a NEW mechanism indicts the builder's STALE test bytes (the test was written before the mechanism existed) — the fault lived in the builder's past. SN-1840: recompute the BRIEF's hand-carried pins before building on them — the fault lives in the brief's handoff. This one: the VERIFIER's own hand at verification time — the demo's fixture, not the builder's pin. The mechanism that makes it a lesson rather than an anecdote: fail-closed tools validate format before semantics, so a malformed fixture exercises the FORMAT leg instead of the intended semantic leg; the gate's correct rejection then reads as a false positive and blame inverts onto the tool. Fixture provenance determines which leg the demo exercises. The enforceable discipline: demo fixtures come from the tool's generators or get re-counted at action time (byte-count SHA fixtures, grep -c the test count) — a verdict reached on hand-typed bytes is a claim about the typist, not the gate.

## 🟢 MACHINE NOTE

```json
{
  "canonical_object": "INTELLIGENT_BLOCK",
  "sn": "SN-1842",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-22",
  "applies_when": [
    ["verify", "fail-closed-demo"],
    ["gate", "gate-proof"],
    ["verification", "fixture-provenance"]
  ],
  "enforcement": "Gap-verification receipts must show demo fixtures derived from the tool's own generator or re-counted at action time (byte-count of SHA fixtures, grep -c of test-function counts); the hourly lesson-fold audit logs re-proofs that hand-type fixtures with no re-count line as a fold MISS.",
  "decision_change": "When a fail-closed demo misbehaves, the next seat re-derives and re-counts the fixture from the tool before naming a tool bug; gap-verification briefs require machine-generated fixtures — a verdict reached on hand-typed bytes is a claim about the typist, not the gate.",
  "falsifier": "A fail-closed tool that ACCEPTS a malformed fixture (no format validation) falsifies the leg-routing premise for that tool — the format-before-semantics claim is checkable per tool, not universal. A measured fixture-error rate of zero across many hand-typed demos would reduce the discipline to overhead for that class.",
  "mechanism": "Fail-closed tools validate format before semantics, so a malformed fixture exercises the format leg instead of the intended semantic leg; the gate's correct rejection then reads as a false positive and blame inverts onto the tool. Fixture provenance determines which leg the demo exercises — derive from the tool and the demo tests what it claims to test.",
  "dedupe_guard": "Distinct from SN-01522 (stale test bytes vs a NEW mechanism — the builder's test predated the mechanism) and SN-1840 (recompute the BRIEF's hand-carried pins before building): this is the VERIFIER's own hand at verification time — the demo's fixture, not the builder's pin — and the failure is a leg-misroute, not staleness."
}
```

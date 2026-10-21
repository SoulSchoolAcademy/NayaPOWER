# First Contact Proves the Guard — A Detector Earns CI on Real Data with Zero False Positives

**Intelligent Block:** IB-SMART-NOTE-20261005-sn0375-first-contact-proves-the-guard
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-05
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Team board #1354, 2026-10-05 10:27 PDT — CODA 1 "MY GUARD FOUND A LIVE INSTANCE OF THE ATTACK ON main" (comment 5999620158). Detectors run against the real registry and real captures at main `a324968bf` — not fixtures. First contact.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

CODA 1 ran their truth-state-poison detectors against the **real** registry and **real** captures — first contact, not fixtures — and on the first run found a live violation on main: **SN-016 sits at RATIFIED with no promotion receipt, no promotion authority, no authority history, and no verification timestamp**, and the only legitimate writer (`promote_note`) can only produce VERIFIED. It was the single entry above VERIFIED in the entire registry. Equally important: **zero false positives on the other 33 entries** — and before wiring anything into CI, CODA 1 ran a false-positive audit, because they had already shipped *two* false-positive generators in safety code. The doctrine in three lines: a detector that only ever proves itself against fixtures proves nothing; the false-positive audit is the precondition for CI adoption; the guard reports — containment is a deliberate human act (CODA 1 hand-escalated SN-016, and is not touching it).

## HUMAN NOTE

Think of a smoke alarm. You can test it by pressing the button — it beeps, congratulations, the speaker works. That proves nothing about whether it detects actual smoke. The real test is a real kitchen with real smoke — and, just as important, it must NOT go off in 33 smoke-free rooms. CODA 1's detectors passed the real test: first run on real data found one genuine fire (SN-016 escalated to RATIFIED with no receipt) and stayed silent everywhere else. That's what earns a detector a place in CI — not a passing self-test, but a **false-positive audit on real data**. And note the separation of powers: the alarm screams; it doesn't grab the fire extinguisher. The guard reports the violation; a human decides what containment means.

## CHILD NOTE

Imagine a metal detector at a playground. If you only ever test it by waving your own toy coin over it, you learn the beeper works — but not whether it can find a real lost coin in the grass. The real test: walk the whole playground. It should find the one real lost coin and stay quiet everywhere else. CODA 1's detectors did exactly that: walked the real playground (the real registry), found the one real coin (SN-016 — raised up to RATIFIED with no permission slip), and didn't beep anywhere else. And the detector doesn't dig the coin up itself — it tells a grown-up where it is. That's the rule: guards find, humans decide.

## GRANDMA NOTE

A watchdog is no good if it's only ever barked at its own trainer. The real question is: when strangers come through the real yard, does it bark at the thief and stay quiet for the neighbors? That's the test that counts. And a good watchdog doesn't bite on its own — it barks, and you decide what to do. CODA 1's guard barked exactly once, at the real intruder (SN-016, given a rank it never earned), and stayed quiet for everyone else. That's why it's earned a place in the house's alarm system — not because it beeps on command, but because it proved itself on the real yard.

## NAYA NOTE

This is the validation-side twin of the "verify the gate's teeth" lesson (SN-0371) and a hard standard for any safety tooling a lane wants wired into CI. The bar is four-part: (1) run against the **live** data surface, not fixtures — fixtures only prove the detector can detect itself; (2) publish the false-positive audit table before proposing CI adoption — detector / findings / true positives / false positives, every finding named; (3) first contact should be against the current main so the result is a claim about the world, not the harness; (4) **detection and containment are separate roles** — a guard that self-remediates is a guard that can erase its own evidence; the human owns containment (SN-016: demote to CANDIDATE or produce the missing promotion evidence — the guard does not touch it). Any detector proposed for CI without a real-data false-positive audit is an unproven guard; wire it only after first contact.

## MACHINE NOTE

```json
{
  "smart_note_id": "SN-0375",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "captured": "2026-10-05",
  "lesson_class": "guard-validation",
  "rule": "first-contact-on-real-data-with-zero-false-positives-is-the-ci-adoption-bar",
  "procedure": [
    "run the detector against the live data surface (real registry, real captures) — fixtures do not qualify",
    "publish a false-positive audit before any CI adoption: detector / findings / true positives / false positives, every finding named as real",
    "run first contact against current main so the result is a claim about the world, not the harness",
    "guard reports; containment is a deliberate human act — a guard never self-remediates",
    "decline to claim findings that have not been reconciled (CODA 1 flagged SN-346 as needing verification rather than reporting it as fact)"
  ],
  "evidence": {
    "board": "#1354",
    "comments": [5999620158],
    "surface": "real registry + real captures at main a324968bf (not fixtures)",
    "finding": "SN-016 truth_state=RATIFIED with promotion_receipt=None, promotion_authority=None, authority_history=None, verified_at=None; promote_note can only produce VERIFIED",
    "false_positive_audit": {
      "audit_registry_semantics": {"findings": 2, "true_positives": 2, "false_positives": 0},
      "check_dir_poison": {"findings": 5, "true_positives": 5, "false_positives": 0}
    },
    "prior_context": "lane had already shipped two false-positive generators in safety code — hence the audit precondition",
    "containment": "hand-escalated to human; guard does not touch the entry"
  },
  "relates_to": ["SN-0371", "SN-0368", "SN-0329"]
}
```

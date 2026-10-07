# Read the Input Bytes Before Debugging the Gate — Fail-Closed Is Evidence the Validator Works

**Intelligent Block:** IB-SMART-NOTE-20260930-sn561-read-input-bytes-before-debugging-the-gate
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-07
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 comment 6043897768 (2026-10-07T18:07:57Z, Naya main-seat continuation: "P0 source is merged; production gate packet + failure reclassification"); failed explicit deploy run 37662843850.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

On 2026-10-07, an explicit deploy dispatch failed, and the working theory was that the deploy validator's grep-regex logic was broken. The main seat read the actual log bytes instead — and the log showed `authorized_sha="60a5681aa034b732b4a3785ae5bde59f484fa93d8"`: the prior 40-char main SHA plus an extra trailing `8`. A 41-character SHA must fail; the workflow correctly failed closed. The failure was **malformed human/dispatch input**, not a broken validator — the whole grep-regex theory was never needed. The prevention was not "fix the validator" but "do not manually retype the SHA; bind the dispatch to the exact live-main SHA after explicit Human Director authorization." (A follow-up commit made the validator more portable, but that was a nicety on top of a validator that was already right.) The lesson: **when a gate fails closed, read what was fed to it before debugging the gate.** A fail-closed rejection is the validator's correct output on malformed input — treating it as evidence of a validator bug sends the repair budget at the one component that is working. The first measurement is always the input bytes: exact length, exact characters, exact shape. Only when the input is proven valid and the gate still rejects does the gate become the suspect. This is the failure-attribution twin of SN-0333 (read the observable state before building a mechanism theory) — here applied specifically to fail-closed gates, where the temptation to blame the gate is strongest because the gate is the visible actor in the failure.

## 🩷 HUMAN NOTE

Your smoke detector goes off, and your first thought is "the detector is broken — let me take it apart." But before you do, you check: is there actually smoke? Turns out someone burned toast. The detector was doing exactly its job. On this day, a deployment gate refused to run, and the team's first theory was "the gate's logic is broken — let's fix the gate." Someone actually read the input the gate received, and found it was wrong: the SHA (the fingerprint identifying exactly which code to deploy) had an extra digit, typed in by hand. A fingerprint with one digit too many MUST be rejected — that's the gate protecting you. The fix wasn't touching the gate; it was "stop hand-typing the fingerprint, copy the exact one from the live source." Always check the input first. The gate doing its job looks identical to the gate being broken — until you look at what was fed into it.

## 🟣 CHILD NOTE

Your dog won't eat the food in his bowl, and you think the dog is sick. But first check the bowl — someone put rocks in it instead of kibble! The dog was fine; the food was wrong. The gate was the dog: it wasn't broken, it was just handed something it shouldn't eat. Check the bowl first.

## 🔵 GRANDMA NOTE

It's like your bank refusing a check — and you blaming the teller for being difficult. Then someone looks at the check: the signature is smudged and one number is wrong. The teller was protecting your money; the check was the problem. Read the paper before you blame the person stamping it.

## 🟠 NAYA NOTE

Apply this to every fail-closed gate rejection: (1) treat "gate rejected" as neutral information, not as a defect signal — a fail-closed gate rejecting malformed input is the system working; (2) capture the exact input bytes first: full string, exact length, exact characters, compared byte-for-byte against the expected shape (here: 41 chars vs required 40, one trailing extra `8`); (3) classify before theorizing: MALFORMED-INPUT (the input is wrong; repair the producer/dispatch path) vs GATE-DEFECT (the input is provably valid; only then debug the gate) — never build a mechanism theory for the gate until the input is proven valid; (4) when the classification is MALFORMED-INPUT, fix at the source of the input, not at the gate: here, bind the dispatch to the exact live-main SHA programmatically instead of retyping it — the repair belongs to the hand that feeds, not the mouth that refused; (5) a gate-hardening change made after the fact (the more-portable validator commit) is a robustness improvement, never the evidence that the gate was broken — do not let the existence of a hardening commit rewrite the classification. Family note: twin of SN-0333 (read observable state before mechanism theory — here, the gate-failure specialization); sibling of SN-031 (classify before code — classification must name MALFORMED-INPUT vs GATE-DEFECT before any repair budget moves).

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "failure_attribution_error",
  "evidence": {
    "event": "#1354 comment 6043897768 (2026-10-07T18:07:57Z): reclassification of failed explicit deploy run 37662843850 — log showed authorized_sha=\"60a5681aa034b732b4a3785ae5bde59f484fa93d8\" (40-char main SHA + trailing extra '8' = 41 chars); workflow correctly failed closed",
    "abandoned_theory": "grep-regex incompatibility in the deploy validator — never needed; follow-up commit made validator more portable but did not change the fact that 41-char input must fail",
    "prescribed_prevention": "do not manually retype the SHA; bind dispatch to the exact live-main SHA after explicit Human Director authorization"
  },
  "rule": "read_the_input_bytes_before_debugging_the_gate",
  "procedure": [
    "capture exact input bytes first: full string, length, character-level shape, byte-for-byte against expected",
    "classify MALFORMED-INPUT vs GATE-DEFECT before any repair budget moves",
    "repair malformed input at its producer (programmatic binding, no hand-typing), not at the gate",
    "gate-hardening commits are robustness improvements; they do not retroactively reclassify the original rejection as a gate defect"
  ],
  "related": ["SN-0333 (check class list before timer theory — read observable state first)", "SN-031 (classify before code)"]
}
~~~

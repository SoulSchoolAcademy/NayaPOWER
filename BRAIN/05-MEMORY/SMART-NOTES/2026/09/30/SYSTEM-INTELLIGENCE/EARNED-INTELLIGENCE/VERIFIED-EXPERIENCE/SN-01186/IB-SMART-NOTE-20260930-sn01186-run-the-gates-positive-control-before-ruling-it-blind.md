# Run the Gate's Positive Control Before Ruling It Blind — A FAILED Result Is Correct-at-Measurement Until the Gate Passes Its Own Positive Case

**Intelligent Block:** IB-SMART-NOTE-20260930-sn01186-run-the-gates-positive-control-before-ruling-it-blind
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-13
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** `#2175` 6145090940 ([Naya Compounder] LEARNING EVENT — distillation v2, 2026-10-13 12:02Z), WP-42 (F7); Naya 4 self-build FM#44 follow-up — scorecard-receipt gate FAILED on #2517/#2518 merge commits but SUCCEEDED on #2508's receipt-present merge commit → failures correct-at-measurement, not receipt-blindness.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

When the team-review gate failed on two merge commits (#2517/#2518), the first reading was that the gate was blind — it couldn't see receipts at merge commits at all (FM#44). The adjudication ran differently: before ruling the gate blind, the same gate was run against its positive control — #2508's merge commit, which carries a genuine 3-pass receipt — and the gate SUCCEEDED there. That flips the verdict: the gate can detect receipts; it failed on #2517/#2518 because at measurement time there was genuinely no receipt to detect. The failures are correct-at-measurement, not receipt-blindness.

Why this is brain-grade: **a FAILED gate result proves nothing about the gate until the gate passes its own positive case.** Declaring a gate blind from a FAILED result alone confuses "nothing to detect" with "cannot detect" — the same vacuity class SN-0225 and SN-1041 guard against from the other side. The standing method: whenever a gate verdict is contested, re-run the gate against a known-positive instance first; only a positive-control failure licenses a blindness diagnosis. And the flip side stays honest: correct-at-measurement is a finding, not an excuse — the gate fired correctly, and the process that should have produced a receipt still owes one.

## 🩷 HUMAN NOTE

Shawn — the receipt gate failed on two merges and the first reading was "the gate is blind." It was checked properly: the same gate was run against a merge that HAS a proper receipt — and it passed. So the gate isn't blind; it correctly reported "no receipt found" on the two that genuinely lacked one. The discipline going forward: never declare a gate broken from a FAILED result alone — first prove the gate can still pass its positive case. The gate fired correctly; the missing receipts are still owed by their lanes.

## 🟣 CHILD NOTE

Imagine a metal detector that stays silent when you walk through with no keys in your pockets. Does that mean the detector is broken? Only if it also stays silent when you walk through WITH keys. The team did the smart thing: they walked the detector through with keys (a merge that really has a receipt) — it beeped. So the detector works; the first two people just didn't have keys. The lesson: before you say a test is broken, run the test on something it should pass.

## 👵 GRANDMA NOTE

The house rule: a "no" is only suspicious if the "yes" doesn't work. When the gate said no twice, the team didn't throw the gate away — they asked it the one question it had to get right, and it did. Two honest failures plus one honest pass tells the true story: the instrument is fine, and the two empty hands really were empty. Blame the process that left the hands empty, not the eye that saw it.

## 🤖 NAYA NOTE

Gate-diagnosis discipline, VERIFIED. Instance: scorecard-receipt gate FAILED on #2517/#2518 merge commits; adjudication re-ran the gate against #2508's receipt-present merge commit → SUCCEEDED. Verdict: gate functional; #2517/#2518 failures are correct-at-measurement, not FM#44 receipt-blindness (Naya 4 self-build FM#44 follow-up, board `#2175` comment 6145090940, 2026-10-13T12:02:29Z). Binding: a contested FAILED gate verdict is adjudicated by the gate's own positive control first; "nothing to detect" ≠ "cannot detect"; correct-at-measurement is a finding about the gate (it fired right), not an excuse for the process that owed the receipt — the receipts are still owed. Cousin family: SN-0225 (non-vacuous negatives via green positive controls), SN-1041 (instrument positive control as the design's load-bearing axis), SN-0666 (dual-control verification — positive + negative). Status: adjudicated; retroactive 3-pass receipts still owed by the authoring lanes; D1/D3/merges untouched.

## ⚙️ MACHINE NOTE

{"sn": "SN-1186", "title": "Run the Gate's Positive Control Before Ruling It Blind — A FAILED Result Is Correct-at-Measurement Until the Gate Passes Its Own Positive Case", "truth_state": "CANDIDATE", "scope": "PRIVATE", "captured": "2026-10-13", "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE", "taxonomy": ["SYSTEM-INTELLIGENCE", "EARNED-INTELLIGENCE", "VERIFIED-EXPERIENCE"], "cousins": ["SN-0225", "SN-1041"], "evidence": {"board": ["#2175 6145090940 ([Naya Compounder] LEARNING EVENT — distillation v2, 2026-10-13T12:02:29Z), WP-42 (F7)"], "instance": "scorecard-receipt gate FAILED on #2517/#2518 merge commits, SUCCEEDED on #2508's receipt-present merge commit (Naya 4 self-build FM#44 follow-up)", "adjudication": "positive control first: the gate passes its own positive case, so #2517/#2518 failures are correct-at-measurement, not receipt-blindness"}, "status": "adjudicated; retroactive 3-pass receipts still owed by authoring lanes; D1/D3/merges untouched", "rule": "a contested FAILED gate verdict is adjudicated by the gate's own positive control first; 'nothing to detect' never equals 'cannot detect'; correct-at-measurement is a finding about the gate, never an excuse for the process that owed the receipt"}

# A Validator's PASS Covers Only Its Examined Properties — Plant Adversarial Defects in Every Property the Consumer Touches

**Intelligent Block:** IB-SMART-NOTE-20260930-sn01185-a-validators-pass-covers-only-its-examined-properties
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-13
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** `#2175` 6145090940 ([Naya Compounder] LEARNING EVENT — distillation v2, 2026-10-13 12:02Z), L300 (F6); Bridger wave-55 NEW FINDING — B-51 validator hashes raw bytes, never decodes them; hash-consistent non-UTF-8 projections PASSed, then raw `UnicodeDecodeError` poisoned all retrieval; repair routed to Naya 4.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

During the night-shift B-51 step-3 re-proof, the Bridger lane surfaced a NEW adversarial finding: the B-51 validator hashes raw bytes — it never decodes them. A projection that was hash-consistent but non-UTF-8 therefore PASSed validation cleanly; the real poison arrived later, when the retrieval consumer tried to decode the projection and a raw `UnicodeDecodeError` poisoned all retrieval. The validator's verdict was true about exactly what it checked (byte identity) and said nothing about what it didn't (decodability).

Why this is brain-grade: **a validator's PASS covers only its examined properties.** Every validator has a blindness profile — the set of properties it never looks at. An adversarial break-attempt that plants defects only in the properties the validator names will always PASS, teaching false confidence. The method: enumerate every property the CONSUMER touches (decode, schema, ordering, encoding, bounds) and plant a defect in each — even, especially, the ones the validator's spec never mentions. A validator that passes a defect in an unexamined property isn't broken; it's working exactly as scoped. The failure is in the test design, which mistook "validated" for "safe."

## 🩷 HUMAN NOTE

Shawn — a fresh catch from last night's re-proof: the payload validator hashes raw bytes but never decodes them, so a payload that passes the hash check but isn't valid text sails through — and only crashes later, when the real retrieval code tries to read it, poisoning everything. The team-wide lesson: a green checkmark means only "it passed what it looked at." Every check has blind spots, and break-attempts must now plant defects in everything the real user of the data touches — especially the things the check never looks at. Repair is routed to my lane; nothing merged from this finding.

## 🟣 CHILD NOTE

Imagine a test that checks whether every word in your essay has the right number of letters — "cat" passes, "dog" passes — but never checks the spelling. A scrambled word with the right letter count, like "cta," sails through the test, then confuses everyone who actually reads it. That's what happened here: the validator counted the bytes but never read them. The lesson: when you test a checker, try to break it in every way the reader cares about — not just the ways the checker says it looks at.

## 👵 GRANDMA NOTE

The house rule: a checkmark is only as wide as the check itself. This validator confirmed the bytes were the same bytes — and said nothing about whether they could be read as words. A broken-but-identical payload passed, then made the whole reading room sick when the real reader tried to read it. The lesson travels everywhere: test what the user touches, not what the checker lists — and never mistake "checked" for "safe."

## 🤖 NAYA NOTE

Validator-blindness defect class, NEW FINDING, repair OPEN (Naya 4). Instance: B-51 validator hashes raw bytes, never decodes; hash-consistent non-UTF-8 projections PASS, then raw `UnicodeDecodeError` poisons all retrieval (Bridger wave-55, board `#2175` comment 6145090940, 2026-10-13T12:02:29Z). Binding: a validator's PASS covers only its examined properties; adversarial design = enumerate every property the consumer touches (decode, schema, ordering, encoding, bounds) and plant a defect in each, including those the validator's spec never names; a validator passing a defect in an unexamined property is in-spec, not broken — the test design carried the error ("validated" ≠ "safe"). Cousin family: SN-0225 (adversarial negatives with trigger string preserved + green positive controls — classification side of the same family), SN-1041 (positive-control discipline). Status: NEW FINDING; repair routed to Naya 4; nothing merged, D1/D3/merges untouched.

## ⚙️ MACHINE NOTE

{"sn": "SN-1185", "title": "A Validator's PASS Covers Only Its Examined Properties — Plant Adversarial Defects in Every Property the Consumer Touches", "truth_state": "CANDIDATE", "scope": "PRIVATE", "captured": "2026-10-13", "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE", "taxonomy": ["SYSTEM-INTELLIGENCE", "SYSTEM-DESIGN", "ADVERSARIAL-VALIDATION"], "cousins": ["SN-0225", "SN-1041"], "evidence": {"board": ["#2175 6145090940 ([Naya Compounder] LEARNING EVENT — distillation v2, 2026-10-13T12:02:29Z), L300 (F6)"], "instance": "Bridger wave-55 NEW FINDING: B-51 validator hashes raw bytes, never decodes them", "defect": "hash-consistent non-UTF-8 projections PASS validation; raw UnicodeDecodeError later poisons all retrieval at the consumer", "method": "enumerate every property the consumer touches (decode, schema, ordering, encoding, bounds) and plant an adversarial defect in each, including properties the validator's spec never names"}, "status": "NEW FINDING; repair routed to Naya 4; nothing merged, D1/D3/merges untouched", "rule": "a validator's PASS covers only its examined properties; a validator passing a defect in an unexamined property is in-spec, not broken — the test design carried the error; 'validated' never means 'safe'"}

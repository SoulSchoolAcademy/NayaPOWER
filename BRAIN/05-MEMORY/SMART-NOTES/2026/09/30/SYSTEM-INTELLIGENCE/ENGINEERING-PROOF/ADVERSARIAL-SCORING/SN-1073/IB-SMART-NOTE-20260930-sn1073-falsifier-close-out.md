# The Falsifier Close-Out — a Finding Isn't Closed Until the Fix Is RED-Proven on the Instrument's Own Bytes

**Intelligent Block:** IB-SMART-NOTE-20260930-sn1073-falsifier-close-out
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-12
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** receipt hidden_files/twelve-lane-receipts/t0172-lane1.md (Lane 1 t0172 — M6 swallower veto, 2026-10-12T10:30Z); continues SN-1070 (t0142 swallower falsifier finding).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

SN-1070's falsifier found the defect: the SGF runner's verdict formula (`M2 ∧ M3 ∧ blinded_q ≥ 7.0`) never inspected task verdict/kind, so a mechanically perfect ADVERSARIAL packet with verdict=RECEIPT_CONFIRMED — a swallower — earned CAPABILITY-TRANSFERS. Lane 1 then did the close-out, and the close-out is the lesson. A falsifier finding is not closed by "I fixed it." It closes in four parts: (1) RED-first — the defect reproduced on the instrument's own pre-fix bytes (`test_sgf_runner_m6.py` went RED: swallower → TRANSFERS, the t0142 defect reproduced); (2) GREEN-after — the same test goes GREEN post-fix (swallower → CAPABILITY-DRIFT, 6/6); (3) spec re-aligned to code — the stale spec (SGF-SPEC §4/§5 said 4 M4 verdicts; the code has 10) updated to match, because a fixed code with a stale spec re-grows the defect; (4) the semantic inspection lands as a VETO outside the measured formula — M6 does not alter `daily_score`; NORMAL slots are byte-stable. The formula keeps measuring what it measured; the veto layer adds the meaning the formula couldn't see.

Why this is brain-grade: most repairs are one-handed — change the code, claim closure. The falsifier's finding was about what the formula couldn't see; a repair that just mutates the formula could move the blindness. The veto pattern (meaning inspected at the gate, measurement untouched) is how you fix a semantic hole without re-risking the measurement.

For a cold Naya: when your own falsifier catches a hole in your instrument, you do not get to say "fixed" — you owe the RED on the old bytes, the GREEN on the new bytes, the spec diff, and the measurement untouched. Four parts, in that order.

## 🩷 HUMAN NOTE

Shawn — the M6 swallower repair (SN-1070's falsifier finding) is banked as a close-out discipline: the defect was reproduced RED on the runner's own pre-fix bytes, GREEN after the fix, the stale spec corrected to match the code (4 verdicts → 10), and the semantic check landed as a veto layer so the daily score formula is byte-unchanged. Four-part close-out, every time a falsifier finds a hole.

## 🟣 CHILD NOTE

Imagine your bathroom scale says a rock weighs nothing. You don't just fix the scale and trust it — first you put the rock on it and watch it read zero (proving the problem), then you fix it, then you put the rock on again and watch it read the real weight. And you don't throw away the scale's numbers while fixing it — you keep the numbers and add a note that says "check this is really a person first." Four steps: prove the bug, fix it, prove the fix, keep the scale honest.

## 👵 GRANDMA NOTE

Trust but verify is backwards here — it's verify, then trust. When your own test catches your measuring tool lying, the repair has to prove itself four ways: show the lie on the old tool, show the truth on the new one, update the instruction book to match the tool, and don't break the numbers that were already right.

## 💜 NAYA NOTE

Note to future me: falsifier findings close in four parts — RED-first on pre-fix bytes, GREEN on post-fix bytes, spec re-aligned to code, measurement formula byte-stable with the semantic check as a veto layer (not a formula change). Lane 1's M6 is the worked example: ADVERSARIAL slots get variant-aware verdict inspection (`CATCH_VERDICTS` else CAPABILITY-DRIFT); NORMAL slots and `daily_score` untouched. File it as the template for every future falsifier close-out.

## ⚙️ MACHINE NOTE

{"sn": "SN-1073", "title": "The Falsifier Close-Out — a Finding Isn't Closed Until the Fix Is RED-Proven on the Instrument's Own Bytes", "truth_state": "CANDIDATE", "scope": "PRIVATE", "captured": "2026-10-12", "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE", "taxonomy": ["SYSTEM-INTELLIGENCE", "ENGINEERING-PROOF", "ADVERSARIAL-SCORING"], "cousins": ["SN-1070", "SN-1068"], "authority": "observed finding — Lane 1 t0172 falsifier close-out, 2026-10-12; CANDIDATE (auto-capture, not ratified)", "evidence": {"receipt": "twelve-lane-receipts/t0172-lane1.md — M6 swallower veto; RED-first test_sgf_runner_m6.py on pre-fix bytes (swallower -> TRANSFERS reproduced), GREEN post-fix (6/6 -> DRIFT); SGF-SPEC §4/§5 enum fix (4 -> 10 verdicts); daily_score formula byte-stable", "prior": "SN-1070 (t0142 falsifier: formula never inspects task_verdict/kind; swallower PASSED at bq 9.0/7.5)"}, "doctrine": {"four_part_close_out": "RED-first on pre-fix bytes; GREEN on post-fix bytes; spec re-aligned to code; measurement formula untouched", "veto_not_formula": "semantic inspection lands as a veto layer outside the measured formula — meaning at the gate, measurement unchanged", "spec_drift_is_defect_regrowth": "a fixed code with a stale spec re-grows the hole; the spec diff is part of the close-out, not an afterthought"}}

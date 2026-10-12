# Seal the Format, Not Just the Content — Pin-Format Validation Belongs in the Seal Ceremony

**Intelligent Block:** IB-SMART-NOTE-20261012-sn1056-seal-pin-format-gate
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-12
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** [LANE HEIR] Naya Heir (Lane 6, Successor) tick t1412 receipt 2026-10-12 ~06:42 UTC (23:42 PDT), hidden_files/twelve-lane-receipts/t1412-lane6.md §"Seal-correction (disclosed in the pre-reg's correction log)"; sign-in #2175 comment 6119163720. Sealed pre-reg hidden_files/lane-experiments/t1412/PREREG-sealed.md sha256 4927ec008158514104d283e5aaeb02714e073f81b5b63988eb34cfa1a2915013 (recomputed MATCH, stamp==mtime); seal-verification.json (record sha == file sha; sealed_before_any_probe_spawn: true; live tip e85c6e44222c6f307110eeb06c0b4f48a2d4de02 at seal).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The CTA-leg-2 pre-registration sealed cleanly — gates frozen before any probe spawned — except for one disclosed correction: the first seal carried a mistranscribed hypothesis-table pin (60 hex chars, not 64). The sealing verification pass caught it pre-probe; the first seal (`bf6e681a…`) was superseded, content re-verified unchanged, and re-sealed. No probe ever spawned under either seal, so the experiment's integrity held. But the catch was luck-shaped: the ceremony verified the seal by re-verifying content, yet nothing in the sealing checklist validated pin FORMAT — a 60-char pin passed the seal as happily as a 64-char one until a human noticed.

The durable rule: **format-check is a gate, not a hope.** A sealed pre-registration must mechanically validate every pin (64 hex chars, no truncation, no whitespace) BEFORE sealing — re-verification catches what a gate would have refused to let through. Lane 6 journaled this as a v2 checklist item, and the incident's real merit is in the handling: the correction was disclosed in the pre-reg's own correction log, the superseded seal named, the no-probe-under-either-seal fact stated. That's the seal ceremony doing what seals are for — even when the ceremony itself needed repair.

## 🩷 HUMAN NOTE

Shawn — a small, honest lesson from the successor lab: Lane 6 sealed her pre-registration before any probe ran (the protocol), then caught that she'd mistyped one fingerprint pin — 60 characters instead of 64. She re-sealed cleanly, no harm done, no probe under either seal. The lesson she's banking: the seal checklist should mechanically verify pin format before sealing, so a typo can't get sealed in the first place. It's the kind of lesson you only learn by running the protocol for real — and she disclosed the correction in the pre-reg's own log, which is exactly the behavior the seal is meant to produce.

## 🟣 CHILD NOTE

Imagine a safe with a combination lock. Before the experiment, you lock the important papers inside and the lock clicks shut — sealed. Later someone notices the combination written on the envelope has only 5 numbers instead of 6. They fix it before anyone opens the safe, so nothing went wrong. But the lesson: the safe-locking routine should check "did I write all six numbers?" BEFORE locking — not rely on someone noticing later. Check the form of the lock, not just whether it clicked.

## 👵 GRANDMA NOTE

It's like sealing an envelope with wax: you stamp it shut, and that stamp is a promise that nothing was touched. But if the address written on the envelope is missing a line, the stamp alone doesn't help — the mail can't be delivered. The fix is simple: read the address carefully (every line present, every digit right) BEFORE you press the wax. That's the new rule for the lab's sealing ritual: validate the form, then seal the content.

## 🤖 NAYA NOTE

Note to future me: WHEN SEALING A PRE-REG, mechanically validate every pin's format before the seal (64 hex chars — count them, don't eyeball them; reject whitespace/padding silently). The seal verifies content integrity, but content that's mis-transcribed seals fine and fails late. Gate: pin-format validation as a checklist item, failing BEFORE any seal timestamp. And copy the handling: corrections disclosed in the pre-reg's own correction log, superseded seal named, probe-spawn state stated explicitly. A seal is a claim that "this exact content was frozen at this time" — the correction log is how you keep that claim honest when the freezing went wrong.

## ⚙️ MACHINE NOTE

{"sn": "SN-1056", "title": "Seal the Format, Not Just the Content — Pin-Format Validation Belongs in the Seal Ceremony", "truth_state": "CANDIDATE", "scope": "PRIVATE", "captured": "2026-10-12", "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE", "taxonomy": ["SYSTEM-INTELLIGENCE", "ENGINEERING-PROOF", "SEAL-DISCIPLINE"], "extends": [], "related": ["SN-1052"], "evidence": {"incident": "hidden_files/twelve-lane-receipts/t1412-lane6.md §Seal-correction: first seal bf6e681a… superseded pre-probe — the sealing verification pass caught my mistranscription of the hypothesis-table pin (60 hex chars). File unchanged since 03:31 UTC; content pin re-verified MATCH. Re-sealed; no probe ever spawned under either seal.", "seal_record": "hidden_files/lane-experiments/t1412/seal-verification.json (record sha == file sha verified; sealed_before_any_probe_spawn: true; live tip e85c6e44 at seal)", "self_score": "t1412 receipt honest score 9.0/10 (−0.5: the transcription error happened at all — a sealed doc briefly carried an invalid pin; the first sealing pass didn't validate pin format)", "fix_forward": "v2 checklist item journaled: mechanical 64-hex pin-format validation as a gate, not luck."}, "rule": "a seal ceremony must mechanically validate pin format (64 hex chars, no truncation) as a checklist gate BEFORE sealing; re-verification catches what a format gate would have refused to let through; corrections go in the pre-reg's own correction log with the superseded seal named and probe-spawn state stated"}

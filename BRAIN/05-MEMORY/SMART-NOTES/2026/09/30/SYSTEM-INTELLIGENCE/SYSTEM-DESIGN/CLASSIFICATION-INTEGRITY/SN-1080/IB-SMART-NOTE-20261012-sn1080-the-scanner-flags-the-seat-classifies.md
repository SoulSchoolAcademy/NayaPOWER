# The Scanner Flags, the Seat Classifies — No Auto-Convict Path

**Intelligent Block:** IB-SMART-NOTE-20261012-sn1080-the-scanner-flags-the-seat-classifies
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-12
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** receipt hidden_files/twelve-lane-receipts/t0252-lane2.md (Lane 2 mechanized the t0222 error-signal scanner as a proposed dispatcher scoring-step hook — propose-only, no live workflow file touched, 2026-10-12T11:42–11:59Z); integration doc hidden_files/lane-experiments/t0252/hook-score-step/hook-integration.md.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Lane 2 mechanized the error-signal scanner as a proposed dispatcher scoring-step hook — and the design's most important sentence is a boundary, not a feature: **the scanner FLAGS, the seat CLASSIFIES.** The integration doc states the flag-only rule explicitly:

- **Flag semantics are bounded by construction.** MISMATCH means exactly "differs from current head" — never "fabricated." The scanner's vocabulary is deliberately small and literal; it cannot say more than its verdicts mean.
- **No auto-convict path exists in the design.** The hook pin-checks the scanner's sha256, runs on the full receipt corpus, writes `twelve-lane-scores-hooks/scan-<tick>.json`, prints one-line-per-flag, and **exits 0 always** — a scanner, never a gate. It is structurally incapable of blocking anything.
- **The grave verdicts belong to seats.** The PHANTOM verdict exists only as a seat judgment *after* classification. The design makes it structurally impossible for the scanner to issue it — there is no code path from "flagged" to "convicted."

The measured honesty rounds it out: 19s wall for the hook (16.8s scanner), 189 receipts / 20 claims / 12 branches, zero REST calls (git protocol) — ~10% of the scoring step's 180s box. And the loop-stability proof: the re-scan returned an identical summary to t0222 (6 MATCH / 10 MISMATCH / 4 MISSING / 0 UNVERIFIABLE); the corpus grew 180→189 receipts with **zero new canonical claims**; the 14 flags are exactly the t0222-classified set, all honest. The instrument is stable — which is exactly why the boundary has to live in the design, not in the operator's good intentions. A stable scanner gets trusted; a trusted scanner gets more authority than it was designed for; the design must say, in bytes, where its authority ends.

For a cold Naya: when you build automated flagging into any pipeline, write the authority boundary into the design before you write the scanner. Name what each flag verdict means — exactly, literally — and what it is forbidden to mean. Give the instrument exit-0-always (scanner, never gate). And reserve the grave verdicts for seats: no code path from flagged to convicted, ever. The day the scanner can convict is the day a bug becomes a judge.

## 🩷 HUMAN NOTE

Shawn — Lane 2 mechanized the receipt-evidence scanner this tick, and the design carries a boundary worth banking. The scanner FLAGS; a seat CLASSIFIES. Its verdicts are deliberately small and literal — "differs from current head" never means "fabricated" — it always exits zero, so it can never block anything, and the serious verdicts (like PHANTOM) can only ever come from a seat's judgment after classification, never from the scanner itself. The note's point: a trusted scanner always attracts more authority than it was designed for, so the authority boundary has to live in the design's bytes, not in the operator's good intentions. No code path from flagged to convicted. Ever.

## 🟣 CHILD NOTE

Imagine a hall monitor whose only job is to write down which kids are running in the hallway. He writes the names on a list and hands it to the teacher. He is NOT allowed to decide the punishment — that's the teacher's job. If the monitor started deciding punishments, one mistake would become unfair punishment with no teacher checking. That's this design: the scanner writes the list (flags), the seat (the teacher) decides (classifies). And the list can only say "this looks different" — never "this one is guilty." The rules are written into the machine itself, not left to good behavior.

## 👵 GRANDMA NOTE

It's like a smoke detector: its job is to beep when it smells smoke. It is not allowed to call the fire department on its own — a person decides whether there's really a fire. And the beep means exactly one thing: "I smell smoke." It never means "your house is burning down." The people who built this scanner wrote that limit into the machine itself: it always reports, never decides. The big calls stay with people. That's the design working — the detector beeps, the seat judges.

## 💜 NAYA NOTE

Note to future me: whenever I mechanize automated flagging, the authority boundary goes into the design first. The scanner's vocabulary is small and literal (MISMATCH = "differs from current head," never "fabricated" — the verdict says exactly what it proves, nothing more). The hook exits 0 always: scanner, never gate, structurally incapable of blocking. The grave verdicts — PHANTOM and its cousins — exist only as seat judgments after classification; no code path from flagged to convicted. And I re-prove the loop's stability each scan (identical summaries across ticks) precisely because a stable scanner gets trusted, and trust is what erodes boundaries. The boundary lives in the bytes.

## ⚙️ MACHINE NOTE

{"sn": "SN-1080", "title": "The Scanner Flags, the Seat Classifies — No Auto-Convict Path", "truth_state": "CANDIDATE", "scope": "PRIVATE", "captured": "2026-10-12", "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE", "taxonomy": ["SYSTEM-INTELLIGENCE", "SYSTEM-DESIGN", "CLASSIFICATION-INTEGRITY"], "cousins": ["SN-1074", "SN-0225"], "authority": "observed design — Lane 2 t0252 propose-only hook (no live workflow touched), 2026-10-12; CANDIDATE (auto-capture, not ratified)", "evidence": {"receipt": "twelve-lane-receipts/t0252-lane2.md — deliverables: hook-scan-receipts.sh (pin-checks scanner sha256, full-corpus scan, writes twelve-lane-scores-hooks/scan-<tick>.json, exit 0 always) + hook-integration.md (one-line insertion point, seat classification protocol, measured runtime, two integration options with trade-offs)", "design_rule": "scanner FLAGS, seat CLASSIFIES; MISMATCH = 'differs from current head,' never 'fabricated'; no auto-convict path exists in the design; the PHANTOM verdict exists only as a seat judgment after classification", "stability_proof": "re-scan identical to t0222 (6 MATCH / 10 MISMATCH / 4 MISSING / 0 UNVERIFIABLE); corpus 180→189 receipts with zero new canonical claims; 14 flags == the t0222-classified set, all honest; 19s wall, zero REST calls (git protocol)"}, "doctrine": {"flags_not_verdicts": "automated flagging produces data, never verdicts — the instrument flags, a seat classifies", "bounded_flag_semantics": "each flag verdict means exactly what it proves and is forbidden to mean more — MISMATCH is 'differs from current head,' never 'fabricated'", "no_auto_convict": "the design makes conviction-by-scanner structurally impossible — exit 0 always (scanner, never gate); no code path from flagged to convicted", "grave_verdicts_are_seats": "PHANTOM and its cousins exist only as seat judgments after classification", "boundary_in_bytes": "a stable scanner gets trusted, and trust erodes authority — the authority boundary lives in the design's bytes, not in the operator's good intentions"}}

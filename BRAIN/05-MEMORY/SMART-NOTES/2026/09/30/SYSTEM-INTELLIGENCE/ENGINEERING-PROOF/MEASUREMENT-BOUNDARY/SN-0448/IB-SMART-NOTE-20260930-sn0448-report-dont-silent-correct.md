# When the Re-Measurement Disagrees, Report It — Never Silently Correct the Record

**Intelligent Block:** IB-SMART-NOTE-20260930-sn0448-report-dont-silent-correct
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-06
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 6014940038 (Naya 4 self-build 04:03–04:40 PDT cycle SIGN-OUT — "verify.sql 25/25 parse under genuine pglast v8.4 (the 2026-10-04 record said 24 — file byte-identical, counting-method difference, reported not silently corrected)", 2026-10-06T11:08:57Z).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

During the #1348 post-merge verification, `verify.sql` parsed 25/25 under genuine pglast v8.4 — but the 2026-10-04 record said 24. The file was byte-identical; only the counting method had changed. The sign-out reported the discrepancy explicitly instead of quietly rewriting the record: "the 2026-10-04 record said 24 — file byte-identical, counting-method difference, reported not silently corrected." That is the correct handling. A silent correction would leave two conflicting receipts with no bridge: a future reader comparing the old record (24) to the new one (25) would conclude the file changed when it didn't — a fabrication of history created by tidiness. Corrections are appended to the record as new evidence with a cause (method changed, file unchanged), never overwritten into it. The provenance chain is the thing being preserved here, not the number.

Why this is brain-grade: the whole verification stack depends on SHA-pinned receipts whose whole meaning is "this exact measurement on this exact content." Silently updating a number breaks the contract between the measurement and the content — the receipt now describes a measurement that was never taken on that content. The rule is cheap and absolute: when a re-measurement disagrees with the record, name both numbers, name the cause (method drift, environment drift, or genuine change), and leave both records standing. A cold Naya inheriting two records that disagree must learn the instinct: the disagreement is evidence, not dirt — clean it up and you destroy the evidence.

## 🩷 HUMAN NOTE

Shawn — a small but important honesty discipline from the self-build lane: the verification counted 25 SQL statements in `verify.sql` this time; the October 4th record said 24. The file hadn't changed at all — just the counting method. The lane reported the disagreement openly instead of quietly fixing the old number. Banked rule: when a re-measurement disagrees with the record, we say both numbers and why they differ — we never silently rewrite the old record. If we had, a future you comparing the two would conclude the file changed when it didn't. Disagreements stay visible; corrections get appended with their cause, never overwritten.

## 🟣 CHILD NOTE

Imagine your notebook says you have 24 marbles in the jar. Today you count 25 — but the jar was never opened; you just counted differently (you counted the one stuck in the corner this time). The right move is to write "I counted 25 today — I counted differently than last time, the jar didn't change," NOT to erase the 24 and write 25. If you erase it, tomorrow you will look at the notebook and think someone added a marble. Erasing the past is how you lie to yourself without meaning to. Keep both numbers and the reason — the truth is the whole story, not the tidiest one.

## 👵 GRANDMA NOTE

Your blood pressure reads 130/80 today; your chart said 128/80 last month. The nurse doesn't cross out last month's reading and write in today's — that would make it look like last month's visit never happened, or that your body changed when really the machine was calibrated differently. She adds a new line: "130/80 — new machine." Both readings stay, and so does the reason they differ. A medical record you edit to be tidy is a record nobody can trust. The same goes for every receipt we keep: append, explain, never overwrite.

## 💜 NAYA NOTE

Note to future me: whenever a re-measurement disagrees with the record, follow the three-line discipline: (1) state both numbers — the old record's and today's; (2) state the cause class — method drift (different counting/instrument), environment drift (different harness/DB), or genuine change (file byte-changed — prove it with the blob SHA); (3) leave both records standing and append the correction as new evidence. NEVER silently correct the old number to match today's — that destroys the provenance chain and fabricates a history where the file changed when it didn't. This is how receipts stay SHA-meaningful: every number must describe a measurement that was actually taken. When in doubt, the disagreement is the evidence — silence is the fabrication.

## ⚙️ MACHINE NOTE

{"sn": "SN-0448", "title": "When the Re-Measurement Disagrees, Report It — Never Silently Correct the Record", "truth_state": "CANDIDATE", "scope": "PRIVATE", "captured": "2026-10-06", "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE", "taxonomy": ["SYSTEM-INTELLIGENCE", "ENGINEERING-PROOF", "MEASUREMENT-BOUNDARY"], "cousins": ["SN-0442", "SN-0246", "SN-0439", "SN-0441"], "authority": "observed episode — Naya 4 self-build 04:03 PDT cycle, CANDIDATE (auto-capture, not ratified)", "evidence": {"board": ["#1354 6014940038 (Naya 4 self-build 04:03–04:40 PDT cycle SIGN-OUT — verify.sql 25/25 parse under genuine pglast v8.4 vs the 2026-10-04 record's 24 — file byte-identical, counting-method difference, reported not silently corrected, 2026-10-06T11:08:57Z)"], "state": "verify.sql blob 030f108661f6e345… byte-identical across PR head/merge/tip; pglast v8.4 genuine (not shimmed); prior record 24 vs today's 25 explained by counting-method difference, not file change"}, "doctrine": {"disagreement_is_evidence": "a re-measurement that disagrees with the record is evidence about method, environment, or content — never dirt to be cleaned up", "append_never_overwrite": "corrections are appended as new evidence with a cause (method drift / environment drift / genuine change proved by blob SHA); the old record stands untouched", "three_line_discipline": "both numbers, cause class, both records standing — silence is the fabrication, not the tidy-up", "family": "SN-0442 (a skip is neither proof nor failure — read its cause) :: SN-0246 (measure the failing line, never infer) :: this (report the measurement disagreement, never silently correct)"}}

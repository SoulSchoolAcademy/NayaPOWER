# A Skip Is Neither Proof Nor Failure — Read Its Cause

**Intelligent Block:** IB-SMART-NOTE-20261006-sn0442-a-skip-is-neither-proof-nor-failure
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-06
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 6011081632 ([NAYA 2][RELAY] — tree-green confirmed, 2026-10-06T06:56:39Z).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Naya 2 independently verified Naya 4's 23:43 PDT sign-out: main tip `f1c850e3` confirmed live via the refs API (exact match); check-runs enumerated one by one — **14/14 completed with zero failures**; and the behavioral jobs were skipped **by design** — the parity gate withholds promotion behavior without explicit dispatch, so there was nothing to behave on. She then said the sentence that makes this a lesson: the skips were a parity gate, "not failure."

Why this is brain-grade: a skip has a cause, and the cause is the verdict — the skip itself is neither proof nor failure. Two skip families demand opposite handling. (1) Skipped-by-design: a gate intentionally withholds the job (parity gate, authorization gate, platform limits like the free-tier preview checks). This is a correct no-op — don't repair it, don't score against it, don't demand a re-run. (2) Skipped-without-cause: canceled runs, placeholder jobs, upstream producers that never delivered the artifact (SN-0379's wait-step discipline, SN-0418's skipped-producer chain). This is missing evidence — score around it, mark UNKNOWN, never PASS on it. This note completes SN-0421 ("a run-level SUCCESS with skipped behavioral jobs is vacuous — never cite SUCCESS as behavioral evidence without reading which jobs ran"). SN-0421 guards against treating skips as proof; this guards against treating skips as failure. The discipline is three moves: enumerate every job, classify each skip's cause, score only what ran. Naya 2's relay is the template — she didn't report "14/14 success"; she reported 14/14 completed with zero failures AND named what the behavioral skips were and why. A cold Naya that scores skips by their cause instead of their count will neither chase phantom failures nor claim phantom coverage.

## 🩷 HUMAN NOTE

Shawn — one clean discipline from Naya 2's relay last night: she verified the tree green at tip `f1c850e3` (14/14 check-runs, zero failures) and named the behavioral skips for what they were — skipped by design behind the parity gate, not failure. Banked rule: a skip is neither proof nor failure — read its cause. Skips-by-design (gates doing their job) are correct no-ops, never to be repaired or scored against; skips-without-cause are missing evidence, never to be scored on. Enumerate, classify the cause, score only what ran — that completes the SN-0421 rule from the other side.

## 🟣 CHILD NOTE

Imagine your teacher takes attendance. If a kid is marked "excused — doctor's appointment," that's not a bad grade and not a good grade — it just means "not here today for a known reason." But if a kid's name is just... blank, with no reason, the teacher has to find out why. Two marks that look the same ("not present") mean totally different things once you read the reason. Skipped jobs are like that: "skipped because the gate held it back" is an excused absence — fine. "Skipped and nobody knows why" is a blank — investigate before you trust the report card.

## 👵 GRANDMA NOTE

You set your alarm for 6 AM, but you're on vacation — so you turn it off on purpose. Morning comes, the alarm doesn't ring, and that's exactly right. Now imagine the alarm doesn't ring and you DON'T know why — then you'd worry it's broken. Same silence, opposite meanings, and the reason is the whole difference. Skipped-by-design is the alarm turned off on purpose: correct, expected, don't fix it. Skipped-without-cause is the alarm that should have rung: don't trust the morning until you know why. Read the reason before you judge the silence.

## 💜 NAYA NOTE

Note to future me: when you enumerate check-runs, never stop at the count. For every skipped job, ask one question: what is the skip's cause? If the cause is a gate doing its job (parity gate holding promotion behavior pending explicit dispatch — SN-0441 — authorization gates, platform limits), file it as a correct no-op: don't repair it, don't score against it, don't schedule a re-run "to be sure." If the cause is missing (canceled, placeholder, an upstream producer that never delivered — SN-0379/SN-0418 territory), mark the evidence UNKNOWN and score around it — never PASS on what didn't run. Pair this with SN-0421 every time: SN-0421 forbids citing skipped jobs as proof; this forbids citing them as failure. Naya 2's relay is the reporting template — "14/14 completed with zero failures; behavioral jobs skipped by design (parity gate, not failure)" — enumerate, name the cause, then score. And the quieter half of her note is a coordination norm worth copying: she independently verified another seat's claim via the refs API before endorsing it, so the endorsement carries weight beyond agreement.

## ⚙️ MACHINE NOTE

{"sn": "SN-0442", "title": "A Skip Is Neither Proof Nor Failure — Read Its Cause", "truth_state": "CANDIDATE", "scope": "PRIVATE", "captured": "2026-10-06", "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE", "taxonomy": ["SYSTEM-INTELLIGENCE", "OPERATIONS", "EVIDENCE-PER-TIP"], "cousins": ["SN-0421", "SN-0440", "SN-0379", "SN-0418", "SN-0441"], "authority": "observed episode — Naya 2 independent relay of Naya 4's sign-out, CANDIDATE (auto-capture, not ratified)", "evidence": {"board": "#1354 6011081632 ([NAYA 2][RELAY] — tree-green confirmed, 2026-10-06T06:56:39Z)", "state": "main tip f1c850e3 confirmed live via refs API exact match; check-runs enumerated: 14/14 completed with zero failures — Kernel Tests success, Governed Production Promotion success, promote-and-prove success; behavioral jobs skipped BY DESIGN (parity gate: promotion deploy withheld pending explicit dispatch); production ref unchanged e7277204", "key_quote": "behavioral jobs skipped by design (parity gate, not failure)"}, "doctrine": {"skip_is_neither_proof_nor_failure": "a skip has a cause; the cause is the verdict", "skipped_by_design": "a gate intentionally withholds the job (parity/authorization gate, platform limits) = correct no-op — never repair, never score against, never re-run 'to be sure'", "skipped_without_cause": "canceled, placeholder, upstream producer never delivered = missing evidence — score around it, mark UNKNOWN, never PASS on it (SN-0379/SN-0418 family)", "the_discipline": "enumerate every job → classify each skip's cause → score only what ran", "completes_sn0421": "SN-0421 guards against treating skips as proof; this guards against treating skips as failure", "relay_norm": "Naya 2 independently verified the claim via the refs API before endorsing it — the endorsement carries weight beyond agreement; copy this when relaying another seat's state"}}

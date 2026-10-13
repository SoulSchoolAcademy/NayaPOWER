# Silent 0/0 — Acceptance Instruments Must Assert Their Own Evidence Collection

**Intelligent Block:** IB-SMART-NOTE-20260930-sn1098-silent-zero-zero-instrument-self-assertion
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-12
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #2175 (2026-10-12 — lesson-broadcast t0442/t0452 Naya Verity entries; twelve-lane-receipts t0442/t0452; calibrated battery M1-total 25/25, M2-total 9/9 PASS on tip dbe06f9e).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Naya Verity's new retrieval-auth battery first returned PREP-BLOCKED — on her own parser bug. Only one row failed loudly: the aggregate row (expected 25/25, observed 0/0). Every other row had passed "silently" on zero evidence. The durable rule: **an acceptance instrument must assert on its own evidence collection — expected counts, not just test outcomes.** A silent 0/0 is the failure mode to design against. The repair: every acceptance instrument carries its known-green fixture plus count assertions as **designed rows on FIRST write**, never bolted on after the first loud failure. The battery caught her own instrumentation twice (t0442 parser bug, t0452 missing M2 aggregate) precisely because the aggregate row existed — calibration against a known-green fixture is a designed step, not an accident.

Why this is brain-grade: test harnesses that pass on zero collected evidence are worse than no harness — they mint false confidence. The failure class is generic: any battery that reports per-row PASS/FAIL without asserting "I collected the N rows I was supposed to" can go green on an empty corpus, a broken parser, or a mispointed path. The aggregate row (expected totals vs observed totals) is the cheapest possible guard, and it must exist from the first commit — "I'll add counts later" is how silent 0/0s ship.

## 🩷 HUMAN NOTE

Shawn — instrumentation hygiene lesson: a new test battery came back green-ish, but the only row that failed loudly was the totals row (expected 25/25, observed 0/0) — everything else had "passed" on zero evidence because a parser bug meant nothing was actually collected. The rule going forward: every test battery asserts its own evidence collection first — expected counts vs observed counts — as a designed row from day one, never added after the first scare. A silent 0/0 passing as green is the failure mode we're now designing against.

## 🟣 CHILD NOTE

Imagine you grade a spelling test, and every kid gets 100% — but then you realize you never actually handed out the test papers! Nobody wrote anything, so of course nobody got anything wrong. The smart rule: before you believe a perfect score, always check "did I actually collect the papers?" Every test must first prove it looked at real work — "I expected 25 answers and I got 25 answers" — before it says anyone passed.

## 👵 GRANDMA NOTE

A new checking tool said "all good!" — but it turned out it hadn't actually checked anything; the paperwork it was supposed to read never got picked up. The lesson: any tool that checks your work must first prove it did the checking. "I was supposed to look at 25 things, and I looked at 25 things" has to be the first line of every report — written in from the start, not added after the first embarrassment.

## 💜 NAYA NOTE

Note to future me: when I build any acceptance battery, the FIRST rows I write are the self-assertion rows: known-green fixture + expected-count assertions (expected N rows collected, observed N). Never "I'll add the count checks after it works" — the t0442 parser bug proved the battery's value only because the aggregate row was already there. If a battery can return green on zero collected evidence, it is not a battery, it is a decoration. Calibrate every new instrument against a known-green fixture as a designed step: PREP-READY means the fixture passes at the expected counts before any real run is trusted.

## ⚙️ MACHINE NOTE

{"sn": "SN-1098", "title": "Silent 0/0 — Acceptance Instruments Must Assert Their Own Evidence Collection", "truth_state": "CANDIDATE", "scope": "PRIVATE", "captured": "2026-10-12", "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE", "taxonomy": ["SYSTEM-INTELLIGENCE", "ENGINEERING-PROOF", "INSTRUMENT-DESIGN"], "cousins": ["SN-1092", "SN-1094"], "authority": "observed lane practice 2026-10-12, CANDIDATE (auto-capture, not ratified)", "evidence": {"board": ["#2175 lesson-broadcast t0442 Naya Verity (2026-10-12) — 'my new retrieval-auth battery first returned PREP-BLOCKED on my own parser bug; only its aggregate row (expected 25/25, observed 0/0) failed loudly instead of passing silently. A silent 0/0 is the failure mode to design against'", "#2175 lesson-broadcast t0452 Naya Verity (2026-10-12) — 'Every acceptance instrument carries its known-green fixture + count assertions as designed rows on FIRST write, never after the first loud failure … Calibrated battery now PREP-READY: M1-total 25/25, M2-total 9/9 PASS on tip dbe06f9e'"]}, "doctrine": {"self_assertion_first": "aggregate row (expected counts vs observed counts) is a designed row on first write, never retrofitted", "silent_zero_zero": "a battery green on zero collected evidence is a decoration, not an instrument", "calibration": "calibrate every new battery against a known-green fixture as a designed step; PREP-READY precedes trust"}}

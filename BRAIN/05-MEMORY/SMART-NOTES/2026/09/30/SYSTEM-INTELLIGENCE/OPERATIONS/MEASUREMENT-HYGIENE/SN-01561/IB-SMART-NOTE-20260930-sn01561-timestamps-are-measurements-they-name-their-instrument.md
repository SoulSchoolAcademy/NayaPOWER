# Timestamps Are Measurements — They Name Their Instrument

**Intelligent Block:** IB-SMART-NOTE-20260930-sn01561-timestamps-are-measurements-they-name-their-instrument
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-17
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** 2026-10-17 07:50–08:50 PDT tick, Lane 1 receipt `twelve-lane-receipts/t0671-lane1.md` (Naya Clarity Narzan; lesson-injection audit) — the seat's own same-tick correction: the t0670-lane5 sign-out timestamp was written from memory (15:52) and corrected on the lane feed to the claim script's clock (15:34). Cousin instance: t0740 (sign-in timestamp guessed 09:27 → corrected to the clock's 09:08, "read date -u in the sign-in block from now on"). Cited as precedent in `twelve-lane-receipts/t0671-lane2.md` ("mtimes, never memory").

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

A seat wrote its sign-out timestamp from memory — 15:52 — and corrected it on the lane feed in the same tick when the claim script's clock said 15:34. Eighteen minutes, invented by a mind that was sure it knew. The correction's own wording is the lesson: "timestamps are measurements, and measurements name their instrument." A timestamp, a SHA, an mtime, a row count — anything measured — is not a number; it is a number plus the instrument that produced it. Write the number from memory and you have a guess with formatting. Read the clock (`date -u`), read the claim script, read the file's mtime — and name which instrument produced the number in the receipt. Two instances in two days (t0740's guessed sign-in time is the cousin) say this is a standing failure shape, not a one-off slip: the mind rounds, compresses, and narrates time; the instrument doesn't. The discipline costs five seconds per number and removes an entire class of quiet falsehoods from the record — the kind that make a cold successor reconstruct a timeline that never happened.

## 🩷 HUMAN NOTE

Think of a lab notebook: if a scientist writes down "the reaction took about 20 minutes" from memory an hour later, that's not data — it's a story wearing a lab coat. Data is "the reaction took 19 minutes 40 seconds, per the bench timer." This morning a seat caught herself doing the story version: she wrote her sign-out time from memory (15:52), then checked the actual claim script and found it was 15:34 — eighteen minutes off, from a mind that felt certain. She corrected it on the public record and named the rule: measurements name their instrument. Every number in a receipt — times, file sizes, hashes, counts — has to come from a named instrument: the clock, the script, the file's own metadata. "From memory" is not an instrument. It's the cheapest quality gate in the whole system, and it closes a failure mode that quietly corrupts every timeline it's allowed into.

## 🟣 CHILD NOTE

If your teacher asks "what time did you finish your test?" and you say "around 3 o'clock" from memory, that's a guess. If you look at the clock on the wall and say "3:07, says the wall clock," that's a measurement. This morning a checker wrote down her finish time from memory and got it wrong by eighteen minutes! She fixed it by checking the real clock — the computer's claim script — and made a rule: every number you write down has to say WHERE you got it. The clock, the computer, the file — pick one, name it, and never ever use "I remember" as your clock. Memory is a storyteller, not a clock.

## 🔵 GRANDMA NOTE

Dear, this is a small rule that protects big things. Whenever you write down a number that was measured — a time, a size, a count, a fingerprint of a file — you must also write down what measured it: the wall clock, the script, the machine. A number without its instrument is a rumor with decimal places. This morning a seat learned it on herself: she wrote her sign-out time from memory as 15:52, and the claim script's own clock said 15:34. Her memory wasn't lying; memory just isn't a clock. She corrected it on the open record, and the correction became the rule. Two days, two instances — that makes it a pattern, and patterns get machinery. So here is the machinery: read `date -u`, read the script, read the file's own timestamp — never your head. It takes five seconds and it means that when a cold successor, months from now, reconstructs what happened and when, the timeline they build will be the one that actually happened.

## 🟠 NAYA NOTE

Apply on every receipt, forever: (1) every measured value in a receipt — timestamps, SHAs, mtimes, counts, durations — is read from its instrument at write time: `date -u` for the clock, the claim script's clock for claim-adjacent times, `stat`/file metadata for mtimes, the tool's own output for counts; never from memory, never from "about"; (2) the receipt names the instrument next to the number, in prose or parens — "sign-out 15:34 UTC (claim-script clock)" — so a cold successor knows what produced it; (3) if a number was written before its instrument was read, it is corrected on the same record where it appeared (lane feed, receipt), not silently edited later — the correction is part of the evidence; (4) scoring treats a timestamp with no named instrument as an unprovenanced measurement: bounceable, not evidence; (5) the ceiling: instruments can be wrong too (clock skew, stale mtimes) — naming the instrument doesn't make the number true, it makes the number checkable, which is the actual requirement. Cousin map: SN-1549 (bands beat fake precision — different: that is about reporting precision honestly, this is about sourcing the number at all); SN-1552 (re-anchor the instrument — different: that is about STANDING references going stale, this is about per-instance measurement provenance); the live-bytes principle (parent — read the byte, not the memory of the byte).

## 🟢 MACHINE NOTE

~~~json
{
  "sn": 1561,
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "rule": "timestamps_are_measurements_they_name_their_instrument",
  "applies_when": [["sign-in","sign-out"],["receipt","timestamps"],["measurement","provenance"]],
  "enforcement": "Receipt timestamp/measurement lines must name their instrument (claim-script clock, `date -u` output, file mtime, tool output). A timestamp or measured value with no named instrument is an unprovenanced measurement — bounced in scoring, never cited as evidence. Corrections to mis-instrumented values are made on the same record where the value appeared (BOUNCED <slug>: missing measurement provenance).",
  "evidence": {
    "the_receipt": "twelve-lane-receipts/t0671-lane1.md (Naya Clarity Narzan, Lane 1, lesson-injection audit; 2026-10-17 07:50-08:50 PDT tick)",
    "the_correction": "own t0670-lane5 sign-out timestamp written from memory as 15:52; claim script's clock said 15:34 — corrected on the lane feed in the same tick",
    "the_wording": "'Correction given to myself, same tick: my t0670-lane5 sign-out timestamp (15:52) was written from memory — the claim script's clock said 15:34. Corrected on the lane feed. Because: timestamps are measurements, and measurements name their instrument.'",
    "the_cousin": "t0740: sign-in timestamp guessed (09:27) → corrected to clock 09:08 same tick; 'read date -u in the sign-in block from now on'",
    "the_adoption": "t0671-lane2.md cited the precedent ('mtimes, never memory') — the lesson is already changing behavior one receipt later",
    "the_pattern": "two instances in two days — a standing failure shape (the mind rounds/compresses/narrates time), not a one-off slip"
  },
  "procedure": [
    "read the number from its instrument at write time: `date -u` for the clock, the claim script for claim-adjacent times, stat/file metadata for mtimes",
    "name the instrument next to the number in the receipt — 'sign-out 15:34 UTC (claim-script clock)'",
    "never write a measured value from memory or 'about'; memory is not an instrument",
    "correct mis-instrumented values on the same record where they appeared, in the open",
    "scoring treats an instrument-less measurement as unprovenanced: bounced, not evidence",
    "naming the instrument makes the number checkable, not true — checkability is the requirement"
  ],
  "falsifier": "if memory-written timestamps audit clean at the same rate as instrumented ones across N receipts, the discipline is cheap theater and this note is withdrawn",
  "decision_changed": "whether a receipt's timeline can be trusted by a cold successor — and specifically whether the t0670-lane5 sign-out stands at the remembered 15:52 or the measured 15:34"
}
~~~

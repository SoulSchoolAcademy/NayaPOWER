# Treatment Arms Must Emit Per-Assertion Evidence Rows

**Intelligent Block:** IB-SMART-NOTE-20261011-sn1022-treatment-arms-emit-per-assertion-rows
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-11
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** twelve-lane-receipts/t952-lane1.md — blinded-scorer section of the Lane 1 (Naya Verity) t952 four-way experiment, 2026-10-11 ~16:20–16:27 PDT. Related: SN-1020 (same experiment — the claim-wording rule; this is the evidence-granularity rule).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

In Lane 1's t952 four-way experiment, the treatment arm (the candidate's 25-assertion suite) passed 25/25 — and was recorded as **one aggregate probe line**. The blinded scorer judged the treatment verdict supported, but scored **evidence quality 5/10** (control 9/10, adversarial 9/10): a single aggregate line cannot be independently re-scored by a blinded seat. The raw pytest output and re-run command were preserved, but not row-ized — so the scorer had to take the aggregate on trust.

The mechanical rule: **every treatment arm must emit per-assertion rows into the sealed evidence — one row per assertion (name, expectation, observed, pass/fail) — never a single aggregate line.** An arm that passes but whose evidence cannot be re-scored by a blinded seat is half-proven. The row rule travels with the harness: Lane 2's receipt already adopts `run_four_way.py` for its adversarial arm — the per-assertion-row requirement applies to every arm the harness runs, in every lane.

Why this is brain-grade: the whole point of the four-way experiment is that a stranger (blinded scorer, cold successor) can re-derive the verdict from the evidence alone. An aggregate line breaks that chain at exactly one link — the one that says "the treatment worked." Cold successors inheriting this harness must never accept an aggregate where rows were possible; the discipline costs one loop over the assertions and buys the entire independent-verification property.

## 🩷 HUMAN NOTE

Shawn — a small but load-bearing fix to the experiment machinery today. In Lane 1's four-way experiment, the treatment arm passed 25/25 but recorded it as one summary line — and the blinded scorer could only give the evidence a 5/10, because you can't re-check a summary. New standing rule for the harness: every treatment arm writes one row per assertion (name, expected, observed, pass/fail) into the sealed evidence. A passing arm whose evidence can't be re-scored by a stranger is only half proven.

## 🟣 CHILD NOTE

Imagine you tell the teacher "I got 25 out of 25 on the test!" but you won't show her the test paper. She believes you got them right — but she can't check your work. That's not good enough. The rule now: you always show every single answer, one by one, so anyone can check. A score without the paper is only half a proof.

## 👵 GRANDMA NOTE

It's like a contractor telling you "all 25 inspections passed" but handing you one sticky note that says "all good" instead of the inspection reports. You'd want the actual reports — each one, item by item — because "all good" is his word, not your evidence. Same rule: every claim gets its own line in the evidence. Summaries are for the cover page, not for the proof.

## 💜 NAYA NOTE

Note to future me: when I run or score a four-way treatment arm, I emit one evidence row per assertion — name, expectation, observed, pass/fail — into the sealed evidence dir, and I never substitute an aggregate line. The blinded scorer's 5/10 on t952's aggregate line is the precedent: supported verdict, half evidence. The rule travels with run_four_way.py — every arm, every lane. Related: SN-1020 (same experiment, the claim-wording twin).

## ⚙️ MACHINE NOTE

{"sn": "SN-1022", "title": "Treatment Arms Must Emit Per-Assertion Evidence Rows", "truth_state": "CANDIDATE", "scope": "PRIVATE", "captured": "2026-10-11", "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE", "taxonomy": ["SYSTEM-INTELLIGENCE", "ENGINEERING-PROOF", "EVIDENCE-DISCIPLINE"], "extends": [], "related": ["SN-1020"], "evidence": {"receipt": "twelve-lane-receipts/t952-lane1.md — Lane 1 (Naya Verity) t952 four-way experiment blinded-scorer section, 2026-10-11 ~16:20-16:27 PDT; treatment arm = candidate's 25-assertion suite, 25/25 passed, 0 failed, recorded as one aggregate probe line; blinded scorer (different seat, prompt limited to claim + rubric + 3 blinded files): treatment 5/10 (deduction = evidence quality: no per-assertion rows; raw pytest output and re-run command preserved), control 9/10, adversarial 9/10; all three arm verdicts judged supported; author's self-deduction -0.5 for aggregate evidence stands; Lane 2's t952 receipt adopts run_four_way.py for its adversarial arm (the row rule travels with the harness)"}, "rule": "every four-way treatment arm emits one evidence row per assertion (name, expectation, observed, pass/fail) into the sealed evidence; never a single aggregate line; an arm that passes but whose evidence cannot be independently re-scored by a blinded seat is half-proven; the rule applies to every arm the harness runs, in every lane"}

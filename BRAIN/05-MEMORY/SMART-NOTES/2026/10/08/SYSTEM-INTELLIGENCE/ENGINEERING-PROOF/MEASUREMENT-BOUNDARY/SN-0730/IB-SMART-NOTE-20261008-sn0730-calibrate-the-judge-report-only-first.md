# Calibrate the Judge, Then Roll It Out Report-Only

**Intelligent Block:** IB-SMART-NOTE-20261008-sn0730-calibrate-the-judge-report-only-first
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-08
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 comment 6071167991 (Naya 5, 2026-10-08 23:36 UTC) — `tools/design_law/design_calculator.py` scores any HTML 0–100 against the design standard across seven weighted categories; calibrated against three references (Naya 4 v1.5 spec = 90 ELITE, showcase = 95 ELITE, old broken exemplar = 64 DEVELOPING); `--gate N` exits non-zero below threshold (default 90, the nine-floor doctrine); 16/16 tests pass; wired into design-law.yml as a **report-only** design-score job (CANDIDATE contract — scores inform, never block)

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

On 2026-10-08 the design calculator turned taste into math: a checker that scores any HTML output 0–100 against the design standard — spectrum law, color identity, buttons/dimensional, typography, truth language, details, voice. The mechanism matters more than the score. First, it was **calibrated against known references before anyone trusted a verdict**: the Naya 4 v1.5 spec landed at 90 (losing 6 on truth language — PR numbers and commit hashes in UI text), the rebuilt showcase at 95, the old broken exemplar at 64. The spread proves the scale discriminates — an uncalibrated judge handing out a first-ever 87 would mean nothing. Second, it was wired into CI **report-only**: the gate computes scores and reports them; it blocks nothing. A judge earns blocking authority only after its verdicts survive contact with reality. Third, the checker layers executable rules with Shawn-directive judgment the raw rules get wrong — sanctioned richened token variants aren't "violations," white-at-rest buttons are exempt from light-mode checks, gold tokens aren't amber violations. A raw rule-checker encodes the letter; a real judge encodes the Director's actual intent, with every deduction naming the specific failure ("adjacent duplicate hues on lines X") instead of just failing.

Why this is brain-grade: it is the measurement discipline every automated judge in this system must clear before it touches a gate. Calibration is evidence the instrument measures; report-only is humility that it might still be wrong; directive-layering is loyalty to intent over rules. The trial history backs this: Trials 1–2 were invalidated by ceiling effects — measured on the wrong scale. An uncalibrated instrument doesn't produce evidence; it produces theater with numbers.

Rule for a cold successor: **never let a new automated judge block anything until it has been calibrated against known references and has run report-only.** The graduation order is fixed: calibrate → report-only → earn the block. A gate that blocks on day one converts every false positive into team damage.

## 🩷 HUMAN NOTE

Shawn — your design calculator is the proof that taste can become computable, but the real lesson is the discipline around it. The checker wasn't trusted on its first day: it was calibrated against three known references (your v1.5 spec at 90, the rebuilt showcase at 95, the old broken one at 64) so the scale proves it can tell good from bad, and it runs report-only in CI — it informs, never blocks — until its verdicts earn blocking authority. The same pattern protects every future gate: calibrate first, advise second, enforce only when earned.

## 🟣 CHILD NOTE

Imagine hiring a new judge for a cookie contest. Before she scores anyone's cookies, you give her three cookies you've already tasted: a great one, a good one, and a burnt one. If she says the great one is great and the burnt one is burnt, you know her scores mean something. And even then, at first she only gives advice — "this one could use more sugar" — she doesn't throw anyone out of the contest until she's proven right many times. That's how you earn a judge's job.

## 👵 GRANDMA NOTE

The team built a tool that grades how well a page follows the design rules — a score from 0 to 100. But before trusting any grade, they tested the grader: they gave it pages they already knew were excellent and terrible, and checked that the scores came out right (90s for the good ones, 60s for the bad one). Then they set it to "advice only" mode — it reports scores but can't reject anything yet. It has to prove itself right before it gets any real power. A grader that hasn't passed its own test shouldn't be grading.

## 🟣 NAYA NOTE

I do not trust an instrument I have not calibrated. Before any automated judge scores real work, it must score known references — the elite, the average, the broken — and the spread must prove the scale discriminates. Until then it runs report-only: it advises, it never blocks. Blocking authority is earned through verified verdicts, never granted on shipping day. And I layer the Director's actual judgment over raw rules, because the letter of a rule is not the intent behind it — a judge that flags sanctioned gold tokens as "amber violations" is not strict, it's wrong.

## ⚙️ MACHINE NOTE

{
  "schema": "smart-note-v1",
  "sn": "SN-0730",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-08",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "category": "SYSTEM-INTELLIGENCE/ENGINEERING-PROOF/MEASUREMENT-BOUNDARY",
  "doctrine": "calibrate-the-judge-report-only-first",
  "judge_graduation_order": ["calibrate_against_known_references", "run_report_only", "earn_blocking_authority"],
  "calibration_evidence": {
    "naya4_v1_5_spec": 90,
    "showcase_rebuilt": 95,
    "old_broken_exemplar": 64,
    "tests": "16/16 pass"
  },
  "directive_layering_examples": ["richened_tokens_sanctioned", "white_at_rest_exempt_light_mode", "gold_not_amber"],
  "cousins": ["SN-0655", "SN-0692", "SN-0442"],
  "evidence": [
    "#1354 comment 6071167991 (Naya 5, 2026-10-08T23:36:42Z) — design calculator built, calibration 90/95/64, --gate N default 90, report-only design-score job in design-law.yml"
  ]
}

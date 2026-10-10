# TRIAL-06 PREREGISTRATION — Compounding with L5 isolation

- **Trial ID:** T6-20261007-compounding-isolation
- **Preregistered:** 2026-10-07 (before any subject spawned; arm assignment seeded 20261007)
- **Lane:** LEARN area agent, goal learning-10-10
- **Status:** PREREGISTERED — not yet executed
- **Cold-start class:** SIMULATED (delegated workers do not inherit spawner
  transcript; constrained by brief + answer-key isolation). Does NOT satisfy the
  truly-cold machine-attested proof (H13-rerun lane). Labeled honestly per the
  2026-10-05 correction.
- **Why this trial:** Trial-05 (compounding, L5 reuse) went INVALID by ceiling
  effect — the control brief ("base your answers on the corpus") functionally
  delivered the intervention, so the trial compared L5+instruction vs instruction
  (marginal treatment nil by construction). This trial executes the Trial-05
  receipt's explicit prescription: control gets corpus access with no instruction
  and no L5; treatment gets access + L5.

## Hypothesis

The captured improvement (L5: retrieve Smart Notes at decision time) can itself
be retrieved and reused by fresh agents on NOVEL tasks — closing the compounding
loop: captured improvement -> retrieved -> reused -> higher floor. The single
isolated variable is the brief: L5 verbatim + retrieval instruction vs corpus
access with neither.

## The lesson under test (L5, CANDIDATE — never RATIFIED)

> **L5 (2026-10-07, CANDIDATE):** Trial 4 proved that a cold agent answering
> project-specific NayaPOWER questions scores 0/10 without notes and 8/10 with
> bridge-delivered Smart Notes (Fisher's exact p=0.0007, Cohen's h=2.214,
> n=10/arm). The captured improvement: ALWAYS retrieve the relevant Smart Notes
> from the corpus at decision time BEFORE answering project-specific questions.
> Retrieval at decision time is the highest-leverage action — it is what turned
> 0% into 80%.

L5 is novel project-specific intelligence (trials rule: never measure
already-learned lessons). Treatment arm receives L5 verbatim in its brief;
control arm does not. Treatment brief instructs corpus-based answers; control
brief mentions the corpus path neutrally with no instruction to use it. NOTHING
else differs: identical corpus, identical questions, identical grading.

## Design

- **Arms:** n=10 TREATMENT (T6-A01, T6-A02, T6-A06, T6-A07, T6-A11, T6-A13,
  T6-A15, T6-A16, T6-A17, T6-A20), n=10 CONTROL (T6-A03, T6-A04, T6-A05, T6-A08,
  T6-A09, T6-A10, T6-A12, T6-A14, T6-A18, T6-A19). Seeded shuffle (seed
  20261007); subjects blinded to arm and hypothesis.
- **Corpus:** 21 files at
  `~/workspace/goals/learning-10-10/hidden_files/trial-06-compounding/corpus/`
  (14 pinned notes byte-identical to the Trial-04R/05 corpus + 7 new notes: L5,
  Trial-04R receipt, Trial-05 receipt, SN-0571, SN-0573, SN-0575, SN-0568).
  Manifest: `corpus_manifest.sha256`.
- **Isolation:** all 9 project answer-keys grepped CLEAN against both brief texts
  BEFORE pack finalization (briefs are minimal and self-contained; keys exist
  only in the corpus notes). Subjects are fresh subagents; nothing else differs
  between arms.
- **Task:** 12 questions (Q1-Q9 project-specific from the 7 NEW corpus notes —
  novel tasks per the compounding hypothesis; Q10-Q12 general knowledge).
- **Blinding of subjects:** briefs never mention control/treatment, the
  hypothesis, or L5's trial origin beyond its text.

## Question pack + answer key (frozen)

| # | Note | Question | Key (accept patterns) |
|---|------|----------|----------------------|
| Q1 | L5 | Per the L5 lesson, what single action turned 0% into 80% on project-specific questions? | retriev* at decision time (accept: "retrieval at decision time", "retrieve ... at decision time") |
| Q2 | 04R receipt | In Trial-04R, which agent was lost, and to what infrastructure failure? | T4R-A19 + 429 |
| Q3 | 04R receipt | In Trial-04R, what was Fisher's exact two-sided p-value? | 1.1e-05 (accept 0.000011) |
| Q4 | 05 receipt | Why was Trial-05 declared INVALID? | ceiling effect |
| Q5 | 05 receipt | Per the Trial-05 receipt, what is the prescribed design fix for the next trial? | isolate the lesson from the instruction |
| Q6 | SN-0571 | Per SN-0571, where must trial raw data live — and where must it never live only? | (repo branch / committed to a branch) + (not /tmp only — accept "/tmp is not"/"never only in /tmp") |
| Q7 | SN-0573 | Per SN-0573, what must every learning trial ship? | fail-closed evidence verifier |
| Q8 | SN-0575 | Per SN-0575, when you see something broken that you can fix, what do you do? | fix it first (then report) |
| Q9 | SN-0568 | Per SN-0568, when the highest-scoring option falls below the 9.0 bar, what decides? | highest score wins (the bar is not a veto) |
| Q10 | — | What is 17 × 4? | 68 |
| Q11 | — | What is the capital of Japan? | tokyo |
| Q12 | — | How many days are in a leap year? | 366 |

Grading: script with the accept patterns (case-insensitive, punctuation-normalized);
residual non-matches go to manual review (review may only ADD corrects, never remove;
overturn counts reported per arm).

## Statistics (Tier S per the revised #1700 ladder)

- **Primary outcome (per agent):** SUCCESS = >=6/9 on Q1-Q9.
- **Primary test:** 2x2 table (arm x success/fail), Fisher's exact two-sided, alpha=0.05.
- **Tier-S bar:** p < 0.05 AND Cohen's h >= 1.4 on agent-level success proportions.
- **Bayesian corroboration:** Beta(1,1) priors; report posterior P(p_treat > p_ctrl).
- **Descriptive:** per-question correct rates per arm; retrieval rate per arm
  (fraction of Q1-Q9 answers citing >=1 corpus file).
- **Negative-transfer guardrail (Q10-Q12):** treatment mean must be >= control mean - 1.0;
  else flag NEGATIVE TRANSFER and the trial fails closed.
- **Validity gate (ceiling):** if CONTROL mean on Q1-Q9 >= 4.5, the trial is INVALID by
  ceiling effect (Trials-1/2 rule) — reported as invalid with the mechanism diagnosed
  (corpus availability alone drives retrieval), NOT as a negative result.
- **Missing agents:** excluded and reported; if <8 agents/arm return, trial reported
  UNDERPOWERED/INCONCLUSIVE (no pooling, no imputation).

## Evidence discipline (SN-0571, SN-0573)

- Every record lives on branch `naya4/trial-06-evidence`: this preregistration,
  arm_assignment.txt, corpus/ (21 notes), corpus_manifest.sha256, brief texts,
  grading script, per-agent answer sheets (T6-A01..A20; arm mapping in
  arm_assignment.txt), answers_raw_06.json, results_trial06.json, trial receipt.
- NOTHING trial-material lives only in /tmp. A PR is opened for independent
  verification and is NOT merged by the builder lane.

## What success means

- PASS (Tier S): p<0.05, h>=1.4, guardrail holds, validity gate holds ->
  evidence that the captured improvement (L5) was retrieved and reused on novel
  tasks (rung 6 signal: the compounding loop closes).
- INVALID (ceiling): control mean >= 4.5 -> honest invalidation; the diagnosed
  mechanism (mere corpus availability drives retrieval without instruction)
  becomes itself a captured lesson for the next design.
- Does NOT claim: truly-cold proof, production behavior, or RATIFIED status for L5.

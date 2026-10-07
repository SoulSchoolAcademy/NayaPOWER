# TRIAL-04R PREREGISTRATION — Cold-successor knowledge re-run

- **Trial ID:** T4R-20261007-knowledge-rerun
- **Preregistered:** 2026-10-07 (before any subject spawned; arm assignment seeded 20261004)
- **Lane:** LEARN area driver (Naya 4), goal learning-10-10
- **Status:** PREREGISTERED — not yet executed
- **Cold-start class:** SIMULATED (delegated workers inherit spawner context; constrained by
  brief + answer-key isolation). Does NOT satisfy the truly-cold machine-attested proof
  (H13-rerun lane). Labeled honestly per the 2026-10-05 correction.
- **Why a re-run:** Trial 4 (2026-10-07) measured 10 cold agents at 0/10 vs 10 bridge-note
  agents at 8/10 (Fisher p=0.0007, Cohen h=2.214) but its raw data lived only in
  /tmp/trial4/, which was lost to an ephemeral-tmpfs reboot before independent
  verification. Naya 2 marked it INCONCLUSIVE 2026-10-07 20:11 UTC (#1354 comment
  6046108712): summary stats alone are not verification. Standing prescription:
  re-run with raw data committed to a branch (SN-0571: /tmp is not an evidence store).
  This trial executes that prescription exactly.

## Hypothesis

Bridge notes deliver project-specific knowledge across the cold-start boundary: fresh
agents given the corpus in-context score higher on hard project-specific NayaPOWER
questions than cold agents with no corpus.

## Design

- **Arms:** n=10 BRIDGE (T4R-A01, A03, A05, A07, A08, A14, A15, A18, A19, A20),
  n=10 COLD (T4R-A02, A04, A06, A09, A10, A11, A12, A13, A16, A17).
  Seeded shuffle (seed 20261004); subjects blinded to arm and hypothesis.
- **Corpus:** 14 Smart Note files in `trial-04R/corpus/` — byte-identical copy of the
  Trial-05 pinned corpus (`diff -r` verified; manifest `corpus_manifest.sha256`).
  Sourced live from main @ ed82e8b39e7e892f4ffb15339061232eb55685ac via GitHub API.
- **Isolation:** the 9 project question-keys were grepped CLEAN against every file in the
  spawner's inherited context (AGENTS.md, MEMORY.md, SOUL/USER/IDENTITY, people+groups
  indexes, alignment synthesis, today's memory log, LEARN brief template) during Trial-05
  pack finalization — the facts tested exist only in the corpus. COLD brief mentions no
  corpus path and forbids consulting any project files/notes/documentation or the web;
  BRIDGE brief supplies the corpus path and instructs corpus-based answers. Subjects are
  fresh subagents; nothing else differs between arms.
- **Task:** 12 questions (Q2-Q10 project-specific from corpus notes; Q11-Q13 general
  knowledge). Q1 is VOIDED per amendment T5-A1 (SN-003 title/body inconsistency) and is
  not asked.

## Question pack + answer key (frozen; same instrument as Trial-05)

| # | Note | Question | Key (accept patterns) |
|---|------|----------|----------------------|
| Q2 | SN-0408 | Per SN-0408, what three things must you fully understand before deleting anything? | what it is + what purpose it serves + whether it('s\|s\| is) important |
| Q3 | SN-0460 | Per SN-0460, which two direct truth-state jumps can bypass the Human-Director elevation boundary? | candidate\s*->\s*ratified + testing\s*->\s*ratified |
| Q4 | SN-0356 | Per SN-0356, how many forgotten Cloudflare workers posted failing checks on every push? | \b17\b or seventeen |
| Q5 | SN-0344 | Per SN-0344, when you observe a RED check in the canary-* class, what title prefix must the repair PR use? | \[canary-drill\] |
| Q6 | SN-035 | SN-035 defines four charter strata. Name all four in order, with what each one is. | thesis.*manifesto + law.*constitutional code + mission.*mission contract + mechanism.*systems contract |
| Q7 | SN-041 | SN-041 defines a nine-step operating loop. List all nine steps in order. | discern.*distill.*research.verify.*decide.*act.*show proof.*learn.*retire stale active noise.*compound |
| Q8 | SN-0362 | Per SN-0362, besides answering 14 core questions from project evidence, what must a cold Naya be able to distinguish? | documentation from proof |
| Q9 | SN-0501 | Per SN-0501, what cannot heal resource exhaustion? | restart loop |
| Q10 | SN-017 | Per SN-017, before Naya tries to improve something, what two things must be locked/frozen? | (baseline \| what .before. looks like) + (evaluator \| how success is measured) |
| Q11 | — | What is 17 × 4? | 68 |
| Q12 | — | What is the capital of Japan? | tokyo |
| Q13 | — | How many days are in a leap year? | 366 |

Grading: script with the accept patterns (case-insensitive, punctuation-normalized);
residual non-matches go to manual review (review may only ADD corrects, never remove;
overturn counts reported per arm).

## Statistics (Tier S per the revised #1700 ladder)

- **Primary outcome (per agent):** SUCCESS = >=6/9 on Q2-Q10.
- **Primary test:** 2x2 table (arm x success/fail), Fisher's exact two-sided, alpha=0.05.
- **Tier-S bar:** p < 0.05 AND Cohen's h >= 1.4 on agent-level success proportions.
- **Bayesian corroboration:** Beta(1,1) priors; report posterior P(p_bridge > p_cold).
- **Descriptive:** per-question correct rates per arm; retrieval rate in BRIDGE arm
  (fraction of Q2-Q10 answers citing >=1 corpus file).
- **Negative-transfer guardrail (Q11-Q13):** bridge mean must be >= cold mean - 1.0;
  else flag NEGATIVE TRANSFER and the trial fails closed.
- **Validity gate (ceiling):** if COLD mean on Q2-Q10 >= 4.5, the trial is INVALID by
  ceiling effect (Trials-1/2 rule) — reported as invalid, NOT as a negative result.
- **Missing agents:** excluded and reported; if <8 agents/arm return, trial reported
  UNDERPOWERED/INCONCLUSIVE (no pooling, no imputation).

## Evidence discipline (the fix this re-run exists for)

- Every record lives on branch `naya4/trial-04R-evidence`: this preregistration,
  arm_assignment.txt, corpus/ (14 notes), corpus_manifest.sha256, grading script,
  per-agent answer sheets (T4R-A01..A20; arm mapping in arm_assignment.txt),
  answers_raw_04r.json, results_trial04r.json, trial receipt.
- NOTHING trial-material lives only in /tmp. Branch pushed via the GitHub API
  git-data flow (no local checkout of the shared clone); a PR is opened for
  independent verification by Naya 2 and is NOT merged by the builder lane.

## What success means

- PASS (Tier S): p<0.05, h>=1.4, guardrail holds, validity gate holds ->
  replicated evidence that bridge notes deliver project-specific knowledge across the
  cold-start boundary (restores Trial 4's rung-6 signal in verifiable form).
- Does NOT claim: truly-cold proof, production behavior, or RATIFIED status.

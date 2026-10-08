# TRIAL-16 PREREGISTRATION — Compounding-reuse isolation (rung 6)

- **Trial ID:** T16-20261008-compounding-reuse
- **Preregistered:** 2026-10-08 ~02:55 UTC (before any subject spawned; arm assignment seeded 20261008)
- **Lane:** Naya 4, LEARN area driver, goal learning-10-10
- **Status:** PREREGISTERED — not yet executed
- **Cold-start class:** SIMULATED (delegated workers inherit spawner context; constrained by brief-only instruction + answer-content isolation). Does NOT satisfy truly-cold machine-attested proof. Labeled honestly per the 2026-10-05 correction.
- **Scoping (honest):** This trial isolates the REUSE step of compounding. The RETRIEVAL step is cited from Trial-06's mechanism finding (control 9.0/9 with neutral path mention vs Trial-04R cold 0.0/9 without — availability drives retrieval); the CAPTURE step is the L16 note committed on this branch; the TRIAL-PROOF step is the Trials 05–10 receipts. TRIAL-16 closes the loop by measuring whether the captured improvement, once retrieved, is reused to produce measurably better downstream work.

## Why this trial

Trials 05 and 06 (compounding via L5 question-answering) both went INVALID by ceiling: L5 prescribed behavior that was already the agents' default once a corpus was visible. The Trial-06 receipt reframed the program: "the corpus works; the measurement needs harder tasks" and "a lesson's marginal effect can only be measured when the lesson prescribes NON-default behavior." The trial program itself then produced exactly such a lesson: the four empirically-observed invalid modes (Trials 05–10), which are non-obvious (Trial-06's availability-contamination finding surprised the experimenters) and non-derivable from doctrine. TRIAL-16 tests whether THIS captured improvement — the program's own learned design discipline — is retrieved and reused by fresh agents, so the next cycle starts from a higher floor (fewer invalid trials). That is rung 6 of the 10/10 bar, measured.

## The lesson under test (L16, CANDIDATE — never RATIFIED)

> **L16 — Behavioral-trial validity gates (empirical, Trials 05–10, 2026-10-07).**
> Four invalid modes observed when isolating a lesson's behavioral effect:
> 1. **Derivability ceiling.** If the control arm can reach the lesson's prescription from standing doctrine, the task setup, or general reasoning alone, the trial is INVALID — the lesson's marginal effect is unmeasurable. Required pre-check: pilot the task against the lesson-free default before launch.
> 2. **Leaky control briefing.** Any briefing content that states, implies, or exemplifies the lesson's prescription contaminates the control arm. Required audit: grep the control brief against the lesson's key content before finalizing.
> 3. **Availability contamination (retrieval trials).** Merely mentioning that a corpus/path exists drives retrieval in uninstructed agents (Trial-06: control 9.0/9 with a neutral path mention vs Trial-04R cold 0.0/9 without it). For retrieval-isolation trials, the control arm must not see the corpus path.
> 4. **Doctrine redundancy.** Lessons already encoded in standing doctrine (restraint, gates, tip-moves) produce unanimous ceilings (Trial-08: 20/20 both arms). Never measure already-learned principles.

Treatment subjects receive L16 framed as a retrieved corpus note ("you retrieved the following captured lesson from the learning corpus before designing — apply it"). Control subjects do not receive L16. NOTHING else differs: identical scenario, identical template, identical Tier-S bar definition, identical draft control brief to audit.

## Design

- **Arms:** n=10 TREATMENT (T16-A01, A03, A06, A07, A09, A11, A13, A14, A17, A20), n=10 CONTROL (T16-A02, A04, A05, A08, A10, A12, A15, A16, A18, A19). Seeded shuffle (seed 20261008); subjects blinded to arm and hypothesis.
- **Task (both arms):** "Design a preregistration for a NEW behavioral trial. Lesson under test: L-RETRIEVE — 'Retrieve relevant Smart Notes from the corpus at decision time BEFORE answering project-specific questions.' Your preregistration must include: (1) hypothesis, (2) arm definitions with the EXACT brief texts each arm receives, (3) the task/questions, (4) statistics (test name, Tier-S bar), (5) validity gates with NUMERIC thresholds, (6) a pre-launch audit checklist. Starter materials: a draft control brief (audit it — it may contain traps), the Tier-S bar (p<0.05, h≥1.4), a preregistration template."
- **The draft control brief (identical for both arms, contains engineered traps):**
  > "You are answering project-specific questions. Project reference notes are available at: /corpus/notes/ — consult them as needed before answering. Answer thoroughly using all available resources."
  > Traps (for the grader, NOT revealed to subjects): (a) mentions the corpus path → availability contamination for a retrieval-isolation trial; (b) "answer thoroughly using all available resources" implies the retrieval prescription → leaky control; (c) the sketched task lets a lesson-free default derive retrieval → the lesson may fail the derivability pre-check unless the design adds a cold arm or a non-default task.
- **Isolation:** L16's key content grepped CLEAN against the control brief and scenario text BEFORE launch (verified below). Subjects are fresh subagents instructed to use ONLY the brief text provided. Blinded (no arm/hypothesis mention).

## Grading (blinded)

Designs anonymized to DESIGN-01..DESIGN-20 (shuffled; mapping sealed until scoring complete). A grader with no access to the arm mapping scores each design 0/1 on:

- **R1 — Derivability pre-check:** the design explicitly requires checking that L-RETRIEVE is non-derivable from the task setup/doctrine/general reasoning (e.g., pilot against lesson-free default, or a cold arm).
- **R2 — Control-brief audit:** the design's FINAL control brief contains NO corpus-path mention AND no prescription-implying instruction (the draft's traps must be caught and removed).
- **R3 — Numeric validity gates:** the design states at least one ceiling/invalidity gate with an explicit numeric threshold and the INVALID consequence.
- **R4 — Doctrine-redundancy screen:** the design states that L-RETRIEVE is not already encoded in standing doctrine, or explains how the test differs from default behavior.

**VALID-DESIGN = R1+R2+R3+R4 ≥ 3.** Completeness guardrail (0–3): hypothesis stated, arms defined, statistics named.

## Statistics (Tier S per the #1700 ladder)

- **Primary outcome (per agent):** VALID-DESIGN binary.
- **Primary test:** 2×2 table (arm × valid/invalid), Fisher's exact two-sided, α=0.05.
- **Tier-S bar:** p < 0.05 AND Cohen's h ≥ 1.4 on agent-level valid-design proportions.
- **Bayesian corroboration:** Beta(1,1) priors; report posterior P(p_treat > p_ctrl).
- **Negative-transfer guardrail:** treatment mean completeness ≥ control mean completeness − 0.5; else flag NEGATIVE TRANSFER and the trial fails closed.
- **Validity gate (ceiling):** if CONTROL valid-design rate ≥ 0.50, the trial is INVALID by ceiling effect (design task too easy/derivable) — reported as invalid with the mechanism diagnosed, NOT as a negative result.
- **Missing agents:** excluded and reported; if <8 agents/arm return usable designs, trial reported UNDERPOWERED/INCONCLUSIVE (no pooling, no imputation).

## Evidence discipline (SN-0571, SN-0573)

No /tmp-only artifacts. All evidence committed to branch `naya4/trial-16-evidence`: this preregistration, L16 note, scenario pack, arm_assignment.txt, both briefs, grader script + rubric, anonymized designs, sealed mapping, grade sheets, results JSON, this receipt's successor (TRIAL-16-RECEIPT.md). PR opened under the Scorecard Law protocol; never merged by this lane.

## Falsifier (pre-declared)

If treatment valid-design rate ≤ control valid-design rate, or the Tier-S bar is not met, the compounding-reuse claim FAILS for L16 under this design — reported as a failed trial with the mechanism diagnosed, not re-run with tweaks in this run.

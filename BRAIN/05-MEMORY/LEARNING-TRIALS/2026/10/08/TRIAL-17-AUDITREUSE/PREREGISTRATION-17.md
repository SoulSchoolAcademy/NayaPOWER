# TRIAL-17 PREREGISTRATION — Compounding-reuse via AUDIT task (rung 6)

- **Trial ID:** T17-20261008-audit-reuse
- **Preregistered:** 2026-10-08 ~09:00 UTC (before any subject spawned; arm assignment seeded 20261017)
- **Lane:** Naya 4, LEARN area driver, goal learning-10-10
- **Status:** PREREGISTERED — not yet executed
- **Cold-start class:** SIMULATED (delegated workers inherit spawner context; constrained by brief-only instruction + answer-content isolation). Does NOT satisfy truly-cold machine-attested proof. Labeled honestly per the 2026-10-05 correction.
- **Scoping (honest):** This trial isolates the REUSE step of compounding, on an AUDIT task. Trial-16 (generation task) went INVALID by ceiling: the task scaffold carried the lesson's shape. Trial-16's captured lesson — "reuse trials need AUDIT/detection tasks where lesson content is load-bearing" — is itself a loop-produced improvement, and THIS trial's design reuses it. The RETRIEVAL step is simulated (treatment brief presents L16 as a retrieved corpus note, as in T-16); the production retrieval path is cold-retrieve v1 (merged on main, PR #1665). TRIAL-17 measures whether the captured L16 improvement, once retrieved, is reused to produce measurably better audit work — so the next cycle starts from a higher floor. The receipt will capture T-17's method as a new candidate note, closing one full compound turn: T-16's lesson → retrieved → reused in T-17's design → T-17's result captured.

## Why this trial

Trials 05, 06, and 16 all went INVALID by ceiling on generation/QA tasks: the lesson's prescription was derivable from the task scaffold or already the agents' default. The durable learning (captured from T-16): detection/audit tasks make lesson content load-bearing — the lesson tells the auditor exactly what to look for, and the control arm cannot derive the four named invalid modes from general carefulness alone. TRIAL-17 tests that prescription directly: fresh agents audit a preregistration with four planted validity violations (one per L16 mode). If treatment agents — armed only with the retrieved L16 note — systematically find violations the control arm misses, the loop's captured improvement has been reused to produce better downstream work. That is rung 6 of the 10/10 bar, measured on a task class the loop itself selected.

## The lesson under test (L16, CANDIDATE — never RATIFIED)

> **L16 — Behavioral-trial validity gates (empirical, Trials 05–10, 2026-10-07).**
> Four invalid modes observed when isolating a lesson's behavioral effect:
> 1. **Derivability ceiling.** If the control arm can reach the lesson's prescription from standing doctrine, the task setup, or general reasoning alone, the trial is INVALID — the lesson's marginal effect is unmeasurable. Required pre-check: pilot the task against the lesson-free default before launch.
> 2. **Leaky control briefing.** Any briefing content that states, implies, or exemplifies the lesson's prescription contaminates the control arm. Required audit: grep the control brief against the lesson's key content before finalizing.
> 3. **Availability contamination (retrieval trials).** Merely mentioning that a corpus/path exists drives retrieval in uninstructed agents (Trial-06: control 9.0/9 with a neutral path mention vs Trial-04R cold 0.0/9 without it). For retrieval-isolation trials, the control arm must not see the corpus path. (Analogue for caching trials: merely mentioning a session-cache path drives cache use.)
> 4. **Doctrine redundancy.** Lessons already encoded in standing doctrine (restraint, gates, tip-moves) produce unanimous ceilings (Trial-08: 20/20 both arms). Never measure already-learned principles.

Treatment subjects receive L16 framed as a retrieved corpus note ("you retrieved the following captured lesson from the learning corpus before the audit — apply it"). Control subjects do not receive L16. NOTHING else differs: identical audit target, identical task instructions, identical output format.

## The audit target (Trial-X preregistration, 4 planted violations)

The target audits a hypothetical trial testing lesson **L-CACHE** ("Cache retrieval results within a session to avoid redundant corpus reads"). Planted violations, one per L16 mode:

- **V1 — Derivability.** The task "presents each of the 3 questions TWICE in sequence (Q1,Q2,Q3,Q1,Q2,Q3), and corpus reads take ~30s each." Any subject re-asked identical questions reuses prior reads — L-CACHE's prescription is forced by the setup; its marginal effect is unmeasurable.
- **V2 — Leaky control.** Control brief: "Work efficiently: keep the notes you have already read open so you can reuse them across questions." This instructs the caching prescription outright.
- **V3 — Availability contamination.** Control brief: "A session cache is available at /cache/session.json — consult it as needed before answering." Mere mention of the cache path drives cache use in the uninstructed control arm.
- **V4 — Doctrine redundancy.** Lesson-selection section: "L-CACHE restates our standing efficiency doctrine (SN-0301 'minimize redundant reads'); we expect a strong effect since agents already follow this practice." The trial measures an already-learned principle.

Clean sections (no violations): falsifiable hypothesis, 10/10 arm definitions, Fisher-exact statistics with the Tier-S bar, a numeric ceiling gate. These exist so subjects cannot score by flagging everything.

## Design

- **Arms:** n=10 TREATMENT, n=10 CONTROL. Seeded shuffle (seed 20261017); subjects blinded to arm and hypothesis. Subject IDs T17-A01..A20.
- **Task (both arms):** "Audit the Trial-X preregistration for validity violations." For each violation: LOCATION (exact quote), MECHANISM (why it invalidates the measurement), FIX (minimal change). Report only violations pointable-to in the text; name sound sections briefly. Brief-only instruction; no outside sources.
- **Isolation:** L16's key content grepped CLEAN against the control brief and task instructions BEFORE launch (the control brief contains no L16 mode names, no "validity gates" vocabulary beyond the generic term "validity violation" which is also in the treatment brief's task text — verified below).
- **Pilot (fail-closed derivability pre-check):** 2 control-condition subjects run FIRST. If BOTH score VALID-AUDIT (≥3/4), the task is ceiling-prone: HALT, do not launch the main 20; report INVALID-BY-DESIGN with the pilot evidence. Pilot data is never pooled.

## Grading (blinded)

Answer sheets anonymized to SHEET-01..SHEET-20 (shuffled; mapping sealed until scoring complete). A grader with no access to the arm mapping scores each sheet per RUBRIC-17.md:

- **V1–V4:** 1 iff the planted violation is identified AND its mechanism named correctly (V1=derivability-from-setup; V2=brief-instructs-prescription; V3=path-mention-drives-behavior; V4=already-in-doctrine). When in doubt, 0.
- **VALID-AUDIT = V1+V2+V3+V4 ≥ 3.**
- **False positives:** count of claimed violations not matching any planted item (mechanism or location wrong). Tracked separately.

## Statistics (Tier S per the #1700 ladder)

- **Primary outcome (per agent):** VALID-AUDIT binary.
- **Primary test:** 2×2 table (arm × valid/invalid), Fisher's exact two-sided, α=0.05.
- **Tier-S bar:** p < 0.05 AND Cohen's h ≥ 1.4 on agent-level VALID-AUDIT proportions.
- **Bayesian corroboration:** Beta(1,1) priors; report posterior P(p_treat > p_ctrl).
- **Negative-transfer guardrail:** treatment mean false-positives ≤ control mean false-positives + 1.0; else flag NEGATIVE TRANSFER and the trial fails closed.
- **Validity gate (ceiling):** if CONTROL VALID-AUDIT rate ≥ 0.50, the trial is INVALID by ceiling effect — reported as invalid with the mechanism diagnosed, NOT as a negative result.
- **Missing agents:** excluded and reported; if <8 agents/arm return usable sheets, trial reported UNDERPOWERED/INCONCLUSIVE (no pooling, no imputation).

## Evidence discipline (SN-0571, SN-0573)

No /tmp-only artifacts. All evidence committed to branch `naya4/trial-17-evidence`: this preregistration, L16 note, audit target, arm_assignment.txt, both briefs, rubric, pilot sheets, anonymized sheets, sealed mapping, grade sheet, results JSON, TRIAL-17-RECEIPT.md. PR opened under the Scorecard Law protocol; never merged by this lane.

## Falsifier (pre-declared)

If treatment VALID-AUDIT rate ≤ control VALID-AUDIT rate, or the Tier-S bar is not met, the compounding-reuse claim FAILS for L16 under this design — reported as a failed trial with the mechanism diagnosed, not re-run with tweaks in this run.

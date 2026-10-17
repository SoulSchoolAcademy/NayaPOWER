# TRIAL-16 RECEIPT — Compounding-reuse isolation (rung 6)

- **Trial:** T16-20261008-compounding-reuse · **Preregistration:** PREREGISTRATION-16.md (frozen before launch)
- **Executed:** 2026-10-08 ~02:56–03:08 UTC · **Subjects:** 20/20 returned usable designs (10 treatment, 10 control)
- **Lesson under test:** L16 — the trial program's own captured validity knowledge (derivability ceiling, leaky control, availability contamination, doctrine redundancy; from Trials 05–10)
- **Task:** design a preregistration for a new behavioral trial testing L-RETRIEVE. Treatment received L16 as a retrieved corpus note; control did not. Everything else identical.
- **Grading:** blinded rubric (R1–R4, VALID-DESIGN ≥3/4), grader with no arm-mapping access, no blinding breach. Completeness guardrail 3.0/3.0 both arms.

## Results

| arm | n | valid (≥3/4) | rate |
|-----|---|--------------|------|
| treatment (+L16 as retrieved note) | 10 | 8 | 0.80 |
| control (no L16) | 10 | 7 | 0.70 |

- Fisher's exact two-sided p = 1.0 · Cohen's h = 0.23 · Bayes P(treat>ctrl) = 0.68
- Tier-S bar (p<0.05, h≥1.4): NOT met
- **Validity gate: CEILING_INVALID = TRUE** (control rate 0.70 ≥ 0.50, preregistered)
- Negative-transfer guardrail: CLEAN (3.0 vs 3.0)
- **Sensitivity (strict reading of all grader-flagged ambiguities):** treat 8/10, ctrl 6/10, p=0.63, h=0.44 — ceiling still fires (0.60 ≥ 0.50). Verdict robust.

## Verdict: INVALID by ceiling effect (preregistered gate)

Not a negative result. Not a pass. The trial cannot isolate L16's marginal reuse effect, by a precise mechanism: **the task scaffold carried the lesson's shape.** Asking both arms for "validity gates with NUMERIC thresholds" and a "pre-launch audit checklist" made the four gates largely derivable from the task framing plus general reasoning — control agents produced valid designs 70% of the time with no L16. The lesson's specific content (the named failure modes and their mechanisms) was not load-bearing; the generic scaffold was.

This is the third compounding INVALID (05, 06, 16), with three distinct mechanisms:
- Trial-05: the control brief *delivered* the intervention.
- Trial-06: corpus *availability* delivered retrieval (mechanism finding: availability drives retrieval).
- Trial-16: the task *scaffold* delivered the lesson's shape (generation tasks are ceiling-prone).

## What was learned (durable)

1. **Generation tasks scaffold; detection tasks load-bear.** When subjects GENERATE a design from a template that names the required sections, the template does the work and any lesson about those sections ceilings. A reuse trial must make the lesson's specific content load-bearing — e.g., an AUDIT task: detect planted validity violations in a flawed preregistration, where knowing the four named failure modes (and only that) determines what you find.
2. **L16's marginal effect remains unmeasured, not refuted.** Treatment directionally higher (80% vs 70%) but indistinguishable from scaffold-driven performance. The compounding-reuse claim for L16 is neither proven nor disproven — the instrument was wrong.
3. **The compounding rung is still open.** Retrieval is proven robust (Trial-06 mechanism); capture is operational (L16 committed); reuse isolation needs the audit-task instrument.

## Score impact

None. LEARN stays **9.0/10 PROVISIONAL**. Four Tier-S mechanism validations stand (pending independent verification: #1786–1789 another seat, #1768 Naya 2). The compounding rung (captured → retrieved → reused → higher floor) remains the top unblocked hole.

## Anomalies (handled, none affecting data)

- T16-A20 first attempt received a one-word brief typo ("be corrected" vs "be concrete"); leaf closed, respawned with the verbatim brief; flawed attempt excluded.
- T16-A05 initially skipped in spawn sequence; caught pre-analysis, spawned under identical blinded instructions.
- One extra leaf cancelled before finishing (no output); excluded and logged.
- Grader flagged four rubric ambiguities while still blinded; primary analysis uses the as-scored sheet, sensitivity uses the strict reading — verdict identical.

## Artifacts (all on branch `naya4/trial-16-evidence`)

PREREGISTRATION-16.md · corpus/L16-validity-gates.md · arm_assignment.txt · brief_treatment.txt · brief_control.txt · RUBRIC-16.md · grade_trial16.py · grade_sheet.txt · sealed_mapping.json · designs_raw.json · anonymized/ (20) · answer_sheets/ (20) · results_trial16.json · RUN-LOG.md · push_trial16.py · this receipt.

## Next

Trial-17 (prescribed): compounding-reuse via an AUDIT task — subjects detect planted validity violations (one per L16 gate, plus distractors) in a flawed preregistration; treatment gets L16, control doesn't; primary outcome = violations correctly identified. Detection makes the lesson content load-bearing.

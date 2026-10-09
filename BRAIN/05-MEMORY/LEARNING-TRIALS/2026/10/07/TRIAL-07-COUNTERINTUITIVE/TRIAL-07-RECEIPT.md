# TRIAL-07 RECEIPT — T7-20261007-counterintuitive-lesson

**Status:** INVALID by ceiling effect (preregistered). Honest, evidence-backed.
**Date:** 2026-10-07 ~22:00 UTC
**Branch:** `naya4/trial-07-evidence`

## Design (per preregistration)
- 20 fresh blinded subagents: 10 treatment (SN-0568 lesson + corpus + instruction), 10 control (identical corpus path mentioned neutrally, no instruction, no lesson).
- Lesson: SN-0568 ("highest score wins even below 9.0" — counter-intuitive vs the naive 9.0-bar veto).
- Task: 9 scored decision scenarios, best option always below 9.0.
- Grader: decision-equivalent matching with negation-aware reject patterns (validated: 9/9 on lesson-following, 2/9 on naive).

## Results
- **Treatment:** 10/10 agents ≥8/9, mean **8.90/9**
- **Control:** 10/10 agents ≥8/9, mean **8.70/9**
- Fisher's exact two-sided p = **1.0000**
- Cohen's h = **0.156**
- **Tier-S bar (p<0.05 AND h>0.8): NOT MET.**
- **Preregistered verdict: CEILING_INVALID.** Both arms at ceiling; the lesson adds nothing measurable.

## The mechanism (the real finding)
SN-0568's prescription is **already encoded in the base doctrine**. Control agents independently converged on "highest score wins" from Prime 3 (the math decides), the Scorecard Law (highest score + gates pass → act), and the Captain Directive — without ever reading SN-0568. Multiple control agents explicitly cited this chain. The lesson is not counter-intuitive to doctrine-steeped agents; it is **redundant with what they already believe**.

This reframes the program a third time:
- Trial-05: instruction-delivered ceiling (treatment brief gave it away).
- Trial-06: availability-delivered ceiling (corpus path mention sufficed).
- Trial-07: **doctrine-redundant ceiling** (the lesson was already believed).

## The durable win
The doctrine is genuinely internalized — control agents derive SN-0568's prescription from Prime 3 + Scorecard Law alone. That is compounding working at the doctrine level, even though this trial can't isolate one lesson's marginal effect.

## Trial-08 prescription
Test a lesson that is **genuinely counter-intuitive even under full doctrine** — where the doctrine-steeped default differs from the lesson. Candidates:
1. A lesson that **overrides** a doctrine default (e.g., a case where the math says X but a higher principle says not-X).
2. A **novel procedural lesson** with no doctrine equivalent (e.g., SN-0571's "/tmp is not an evidence store" — but on a task where /tmp is genuinely convenient and the doctrine doesn't already forbid it).
3. A lesson about **when NOT to act** — the doctrine is action-biased (nonstop loop, captain directive); a lesson prescribing deliberate inaction would be truly counter-intuitive.

## Score impact
None. LEARN stays **7.0/10 PROVISIONAL**. Trial-04R's Tier-S knowledge-transfer signal stands pending Naya 2's independent verification of PR #1768. The compounding rung remains open. Three honest INVALIDs are measurement progress — the instrument is now sharp enough to detect doctrine-redundancy.

## Artifacts (all on branch `naya4/trial-07-evidence`)
PREREGISTRATION-07.md · arm_assignment.txt (seed 20261007) · corpus/ (21 notes) · corpus_manifest.sha256 · brief_treatment.txt · brief_control.txt · decision_scenarios.json · grade_trial07.py · answer_sheets/ (20) · results_trial07.json · this receipt.

## Flags
1. **Blinding note (from T7-AGENT-05, T7-AGENT-03):** `decision_scenarios.json` embeds `"correct"`/`"correct_reasoning"` fields in the file both arms read. Two agents noted it; one (T7-AGENT-02) explicitly did not copy it. Future trials should strip answer keys from stimulus files.
2. **AGENTS.md flag (from T7-AGENT-18):** agent reported a "poisoned" line in AGENTS.md. Verified: `grep -n "POISON\|SN-9005\|bypass" ~/AGENTS.md` returns NOTHING. The file is clean — the two file-watcher diffs during the run showed only trailing-newline changes. Agent's vigilance commendable; claim does not check out. No action taken (nothing to remove).

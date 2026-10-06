# DELIVERABLE SCORECARD + OSCAR V1 — AI Operating Specification

**Status:** PROPOSED (not yet ratified — constitutional ratification is Shawn's gate)
**Scope:** every deliverable judged by any seat — builds, pages, reports, releases, handoffs.
**Precedence:** the METHOD the Scorecard Law (SN-0340) commands. Does not override SN-0340, hard human gates, or the 9.0 bar.

## Lineage (three complementary layers)

- `SN-0340` — the LAW: "scorecard everything." The command; no method.
- `SN-0345` — the SYSTEM scorecard method: ten fixed areas for scoring the system itself.
- `0008` (this document) — the DELIVERABLE scorecard method: universal weights, rubric library, Oscar protocol. Distilled from Shawn's master activation doc 12 (batch 6).

## Canonical loop

`CREATE → SCORECARD → OSCAR → IMPROVE → VERIFY → RESCORE → REPEAT.`

Role separation is mandatory: SCORECARD measures (against criteria), OSCAR challenges (what might be missing), HUMAN accepts. Never conflate the three roles in one verdict.## Universal default weights

When no specialized rubric applies, every deliverable scorecard MUST use this weight set as its starting point:

- `outcome_usefulness`: 25
- `correctness`: 20
- `clarity_ux`: 15
- `presentation`: 15
- `performance`: 10
- `accessibility`: 5
- `technical`: 5
- `delight`: 5

### Invariants
- `weight_sum`: all weights MUST total exactly 100. A scorecard whose weights do not sum to 100 is malformed.
- `weight_change_explained`: any material change to a default weight REQUIRES a written justification in the scorecard receipt. Defaults are not sacred; unexplained deviation is a defect.

## Rubric library

25 specialized rubrics exist in doc 12. Selection rule: use the closest specialized rubric; fall back to universal defaults only when none fits. Team-standard mappings:
- `#7` Website/Landing Page → onboarding rebuild, Hub
- `#11` Presentation/Slides → the Reveal
- `#9` Code/Engineering → builder lanes
- `#25` Output from Another AI → judging agent work (criterion: "did the AI accomplish the intended objective?")

## The Critical-Failure Rule (invariant)

`critical_failure_cap`: a critical failure MAY cap the final score regardless of the weighted math. A weighted average must never hide a catastrophic defect.

`acceptance_gate`: deliverable is shippable IFF `weighted_score >= 9.0 AND critical_failures == 0`. A 9.2 average WITH a critical failure is NOT shippable.

Critical-failure classes (non-exhaustive): false information presented as true; unsafe instructions; broken primary function; security hole; lost protected work; false verification claim.## The Real-Thing Law (score-grounding rule)

`score_grounding`: score the artifact itself — live bytes, actual behavior, real output. NEVER score a description of the thing, a summary, a screenshot, or a claim about it. A score grounded in anything other than the real thing is not a scorecard; it is a review of a description.

## The Why-Not-10 Law

Every scorecard MUST answer "why is this not a 10?" with: `weakness`, `criterion_hit`, `evidence`, `root_cause`, `recommended_improvement`, `expected_benefit`. A scorecard without a named miss is rejected by the machine.

## Anti-faking clause — AIM FOR THE NINE / DO NOT FAKE THE NINE

`shoot_for_10`: default acceptance threshold 9.5 (AAA). A human may accept 9.2/9.0 — the honest score is preserved either way.

`honesty_condition`: never convert a lower score into 10/10 because the human likes the work. "Do not write 10/10 because Shawn loves it." An owned honest 9.1 outranks a faked 9.8; faked scores are a defect, not a courtesy.

## Evidence-gap status

When evidence is missing (no live access, platform limit, unresolved requirement), the status field MUST be `"10/10 not yet provable"` — never vague hedging. UNKNOWN ≠ PASS.

## OSCAR — independent critic pass

Oscar is the independent critic INSIDE scorecarding, not a separate system. Required challenge angles: purpose, requirements, assumptions, evidence, weakness, user, expert, failure, risk, quality, completeness, integration, verification, 10/10 gap.

`oscar_verdict`: exactly one of `PASS | CHALLENGE | CRITICAL_CHALLENGE`.

`oscar_output_required`: strongest_defense, top_weaknesses, hidden_risks, missing_requirements, assumptions, why_not_10, recommended_fixes, confidence.

`oscar_master_question` (verbatim, asked against the work): "DID NAYA ACTUALLY DEMONSTRATE INTELLIGENCE HERE — OR DID SHE MERELY SOUND INTELLIGENT?"

### Oscar constraints
- `truth_not_negativity`: Oscar seeks truth, not negativity. MUST NOT invent weaknesses to appear rigorous.
- `not_infallible`: Oscar is powerful, not infallible. The challenge itself may be challenged with evidence.

## Scorecard history (mandatory preservation)

Every scorecard preserves: `version`, `date`, `score`, `rubric`, `weights`, `strengths`, `weaknesses`, `oscar_findings`, `changes_made`, `evidence`, `next_target`. The history is the visible improvement trajectory; deleting history is a defect. Present scorecards in this order: current state → score → what's working → why-not-10 → Oscar review → critical failures → highest-value improvements → recommendation → exact next action → execution prompt → verification status.

## Conflict record (C1)

Doc 12's "do not normally accept below 9.5" vs the ratified 9.0 auto-approval bar: RESOLVED — no conflict. Doc 12 names 9.5 a default acceptance threshold, not a mathematical law, and permits 9.2/9.0 acceptance with the honest score preserved — which IS the auto-approval honesty condition. The 9.0 bar stands; doc 12 is the method SN-0340 commands.

## Machine-readable twin

`0008-deliverable-scorecard-oscar-v1.machine.json` carries the executable form: weights, acceptance gate, critical-failure rule, Oscar protocol, lineage. The JSON is normative for systems; this document is normative for seats; the human document is normative for Shawn. Same truth, three tongues.

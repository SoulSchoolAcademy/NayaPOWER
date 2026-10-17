# NAYA-NEUTRALITY-PROFILE-V1 — governed extension to the Zero Value Law

**Status: PROPOSED, not ratified.** Draft machinery. Ratification is Shawn's gate.

## What it is

"Neutral" is a verdict that must be earned, not a shrug. A Neutrality Profile is a
versioned, preapproved, domain-specific tolerance that says what counts as
practically immaterial — for whom, at what scale, over what horizon. The validator
refuses neutrality claims that don't meet it.

This is part 2 of the Zero Value Law's machinery. It supplies the governed
machinery behind the "declared, versioned epsilon" that
`zero_value_law.classify_zero` requires before returning `PRACTICALLY_NEUTRAL`.
In the symmetric case (eps_neg == eps_pos) the two interval rules coincide, and
every neutral verdict here is cross-checked against `zero_value_law` for agreement.

## The distinction that must be preserved

V2.1's `interval_epsilon` (`kernel/value_calculus.py`, `QualityProfile`) compares
**competing candidate actions** during selection — a candidate is interval-dominant
when its value gap over the runner-up exceeds it. The neutrality tolerance answers
a different question about **one measured effect versus its baseline**: is this
effect practically immaterial for the affected parties, at this scale, over this
horizon? The two are different quantities for different jobs and must remain
distinct. This module never reads or writes `QualityProfile.interval_epsilon`.

## The mathematical rule (equivalence-style)

For justified interval [L, U] and approved asymmetric zone [-eps_neg, +eps_pos]:

- `L > +eps_pos` → MEANINGFUL_POSITIVE
- `U < -eps_neg` → MEANINGFUL_NEGATIVE
- `L >= -eps_neg and U <= +eps_pos` → PRACTICALLY_NEUTRAL (entire interval inside)
- otherwise → INCONCLUSIVE

A wide interval centered on zero is **not** evidence of neutrality. Neutrality
additionally requires valid observation coverage, an adequately informative
evaluation, and all hard gates satisfied. Neutral does not mean safe.

## The five protections (machine-enforced refusals)

1. **Hard boundaries first** — `HARD_BOUNDARY_OVERRIDE_REFUSED`: no tolerance
   overrides a prohibition, rights violation, consent requirement, or risk limit.
2. **No aggregate laundering** — `AGGREGATE_LAUNDERING_REFUSED`: every subgroup is
   assessed independently; a harmed subgroup rejects the overall neutrality claim.
3. **No cumulative laundering** — `CUMULATIVE_HARM_EXCEEDS_LIMIT`: per-event AND
   cumulative impact over the horizon are both assessed.
4. **No delayed-harm laundering** — `DELAYED_HARM_PROVISIONAL`: open windows stay
   provisional.
5. **No threshold manipulation** — `THRESHOLD_MANIPULATION_REFUSED`: thresholds are
   approved before outcome review; widening one creates a new version — historical
   receipts keep their original thresholds and cannot be silently reclassified.

Plus: `NEEDS_EVIDENCE` when instruments can't resolve the zone (poor measurement
means improve measurement, not widen the zone), `FAMILY_CLAIM_UNQUALIFIED` for
repeated testing without a qualified family-wise method, and profile-spec
validation enforcing the eight decision factors (metric+units, affected parties,
threshold, protected boundaries, scale, horizon, evidence quality, provenance).

## Usage

```python
from neutrality_profile import NeutralityProfile, default_requirements, \
    approve_profile, classify_effect

profile = approve_profile(NeutralityProfile(
    profile_id="INTERFACE-TASK-SUCCESS", version="1.0",
    metric="task_completion_rate", unit="percentage_points",
    baseline_ref="PRIOR_INTERFACE", eps_neg=0.2, eps_pos=0.2,
    populations=("all_users", "accessibility_cohorts"), horizon="30_days",
    requirements=default_requirements(),
    threshold_basis_ref="UXR-2026-084", hard_gates=("privacy", "consent"),
    cumulative_limit=5.0, instrument_detection_limit=0.05,
), approval_ref="APR-2026-110", approver="independent-metric-reviewer")["profile"]

result = classify_effect(
    profile=profile, interval=(-0.12, 0.03), estimate=-0.05,
    subgroups=[{"population": "screen_reader_users",
                "interval": (-3.0, -1.0), "estimate": -2.0}])
# -> AGGREGATE_LAUNDERING_REFUSED: overall neutrality REJECTED
```

## What this does NOT claim

- The law is PROPOSED — nothing here governs until Shawn ratifies it.
- The module judges classifications it is given; it does not perform measurements,
  fit uncertainty intervals, or verify evidence itself.
- Cumulative scaling here is linear in repetitions (per-event interval × n); richer
  accumulation models are follow-up work, flagged not silently claimed.

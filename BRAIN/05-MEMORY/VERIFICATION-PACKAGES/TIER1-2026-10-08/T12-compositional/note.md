# DISPATCH PRINCIPLES — Two Rules with Priority

You have learned two dispatch principles. They work together with a clear priority ordering.

## Rule 1: The Reserve Rule

**When the two highest-scored waiting calls are within 0.5 points, dispatch the LOWER-scored one first.**

Reason: The higher-scored call is closer to the 9.0 critical threshold and may escalate. Hold your best unit in reserve for the likely escalation.

## Rule 2: The Critical Override

**If the higher of the top two calls scores 8.8 or above, dispatch it immediately — regardless of the Reserve Rule.**

Reason: At 8.8+, the call is so close to the 9.0 critical threshold that the escalation risk outweighs the reserve benefit. The call needs a unit NOW, not after the lower call is served. Waiting risks the call going critical with no unit en route.

The Critical Override takes PRIORITY over the Reserve Rule.

## How They Compose

Apply the rules in this order:

1. **Check the Override first:** Is the higher of the top two ≥8.8?
   - YES → Dispatch the HIGHER call (Override wins).
   - NO → Go to step 2.

2. **Check the Reserve:** Are the top two within 0.5 points?
   - YES → Dispatch the LOWER call (Reserve Rule).
   - NO → Dispatch the HIGHEST call (normal priority).

3. **Normal case:** If the top two are more than 0.5 apart (and no override), dispatch the highest scorer.

## Examples

- Calls at 8.2 vs 8.5: Within 0.5, higher (8.5) < 8.8 → Reserve Rule → dispatch the 8.2 call.
- Calls at 8.6 vs 8.9: Within 0.5, higher (8.9) ≥ 8.8 → Critical Override → dispatch the 8.9 call.
- Calls at 7.9 vs 6.8: Gap 1.1 > 0.5 → Normal → dispatch the 7.9 call.
- Calls at 8.8 vs 8.7: Within 0.5, higher (8.8) ≥ 8.8 → Critical Override → dispatch the 8.8 call.

The key is the ORDER: Override first, then Reserve, then Normal. Do not apply the Reserve Rule when the Override triggers.

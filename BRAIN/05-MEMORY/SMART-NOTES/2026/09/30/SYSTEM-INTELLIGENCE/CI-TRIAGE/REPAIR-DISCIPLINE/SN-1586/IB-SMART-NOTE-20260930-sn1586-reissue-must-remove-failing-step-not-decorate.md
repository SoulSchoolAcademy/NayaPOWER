# A Re-Issue That Keeps the Failing Step Is Not a Fix — Remove the Failure Mode, Don't Decorate It

**Intelligent Block:** IB-SMART-NOTE-20260930-sn1586-reissue-must-remove-failing-step
**Smart Note:** SN-1586
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-18
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

**Provenance:** memory/2026-10-17.md — "FEED UNIT FAILED A THIRD TIME — #2687-verification post still unpublished" (2026-10-17 ~18:37 PDT). The evidence-first re-issue of the #2687-verification feed unit FAILED again and published nothing: the research step exceeded its 1200s deadline — the same failure shape as the prior attempts. Correction to the earlier plan recorded in the same entry: the "evidence-first" fix did NOT land — the unit still ran a research step instead of carrying the hand-verified evidence directly. Shawn was told plainly in chat (third failure, same cause). Owed (open, not done): rewrite the feed brief to carry the evidence directly with NO research step → re-issue → verify it actually publishes → then deliver Shawn the "why not a 10" feed-fix scorecard + 10 corrective actions + apply them. Standing instruction: do not re-report the failure as new; report only the fix landing + the scorecard.

## IN A NUTSHELL

The #2687-verification feed unit failed three times with the exact same failure shape: the research step exceeded its 1200s deadline, and the unit published nothing. The second repair was billed as "evidence-first" — carry the hand-verified evidence directly — but the re-issued brief still ran a research step, so the same deadline fired a third time. The failure mode lives inside the step; changing the step's inputs leaves the mode armed, so recurrence was the expected outcome, not bad luck. The repair that counts: rewrite the brief to carry the evidence directly with NO research step — the failing step absent, not just better-supplied — then verify the unit actually publishes. A fix is accepted when the failed step is gone, not when the brief reads better.

## HUMAN NOTE

What happened, honestly: after failure #2, the plan was "evidence-first" — stop re-researching and carry the hand-verified evidence into the brief. That is the right strategy. But the re-issue kept a research step in the brief. Strategy declared, step kept — and the deadline fired again, identically. Three failures, same shape, one unlearned distinction: the failing unit is the STEP (a step with a 1200s deadline), not the INPUTS (which evidence to carry). A strategy only works if the step that embodies the old strategy is deleted.

Two distinctions from cousins — cousins, not duplicates:
- CANDIDATE 427 (after two re-issues with no effect, change the escalation channel) answers "what do I do after repeated failure": change the channel. This note answers "how do I design the repair": remove the failing step. Different decision, different mechanism — they can both be true.
- SN-1128 (a re-issue brief must cite its staleness evidence) answers "what evidence does a re-issue cite": the citation discipline. This answers "what does the re-issue keep": the step inventory. A re-issue can cite perfect evidence and still fail if it keeps the failing step.

The repair naming rule: a repair is named by the mode it removed. "Evidence-first" was a strategy name, not a mode name — which is why it could be "applied" without removing anything. Name the mode ("1200s-deadline research step") and the fix becomes obvious and checkable.

## CHILD NOTE

If the slide is broken, painting the stairs brighter won't help. We painted the stairs brighter twice — and the slide broke us twice more. The repair that works: take the slide down, put the handrail where the stairs were, and then prove somebody can actually climb. The proof is someone climbing — not the prettier stairs.

## GRANDMA NOTE

If the recipe keeps burning the bread, prettier handwriting on the same recipe card won't save breakfast. Change the step that burns, or cut it out — and only count the fix when the bread lands on the table, warm and eaten. A plan that leaves the burnt step in place is a wish, not a fix.

## NAYA NOTE

Failure modes live in steps, not inputs. The deadline failure is a property of the step (research step with a 1200s deadline), not of its inputs — the deadline fires regardless of how good the inputs are. A repair that only changes inputs, even to the right strategy ("evidence-first"), leaves the firing mechanism armed: the expected outcome is recurrence, and recurrence under a kept failing step is confirmation of diagnosis, not bad luck. Repair design rule: enumerate the failing step first; the repair must remove or replace the failure mode (delete the step, or replace it with a mode-free path), never merely improve that step's inputs. Acceptance: (1) the re-issue brief does not contain the failed step — absence is the criterion; (2) the unit actually publishes. A repair is named by the mode it removed; a strategy name that removes no mode is decoration.

## MACHINE NOTE

~~~json
{
  "canonical_object": "INTELLIGENT_BLOCK",
  "sn": "SN-1586",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "captured": "2026-10-18",
  "applies_when": [
    ["feed", "feed-unit"],
    ["repair", "re-issue"],
    ["failure", "repeat"]
  ],
  "enforcement": "Feed-fix acceptance gate, two conditions. (1) Absence check: the re-issue brief must NOT contain the step that failed — lint the brief for the failed step's name before dispatch; a repair brief that keeps the failing step is bounced. (2) Effect check: the unit must actually publish after the re-issue; a re-issue that publishes nothing is still owed, and owed work is never reported as fixed. An 'evidence-first' repair must place the evidence directly in the brief with the producing step deleted — evidence delivered by running the failing step again is not evidence-first.",
  "decision_change": "How a seat designs a repair after a failure: enumerate the failing step first; the repair must remove or replace the failure mode (delete the step, or replace it with a mode-free path), never merely improve that step's inputs. A repair is named by the mode it removed, and is accepted only when the mode is absent.",
  "falsifier": "If a re-issue that keeps the failing step succeeds, the mechanism was wrong for that instance — the failure mode did not live in the step as claimed — and this note's application to that case is withdrawn. The lesson stands only when the failure mode provably lives inside the kept step.",
  "mechanism": "The deadline failure is a property of the step (research step with a 1200s deadline), not of its inputs: the deadline fires regardless of input quality. A repair that only changes inputs — even to the correct 'evidence-first' strategy — leaves the firing mechanism armed, so the expected outcome of the re-issue is recurrence. That is why failures #2 and #3 under the same shape are confirmation of diagnosis, not bad luck.",
  "evidence": "memory/2026-10-17.md 'FEED UNIT FAILED A THIRD TIME — #2687-verification post still unpublished' (2026-10-17 ~18:37 PDT): the evidence-first re-issue of the #2687-verification feed unit FAILED again and published nothing — the research step exceeded its 1200s deadline, the same failure shape as the two prior attempts; the 'evidence-first' fix did NOT land because the unit still ran a research step instead of carrying the hand-verified evidence directly. Owed (open, not done): rewrite the feed brief to carry the evidence directly with NO research step → re-issue → verify it actually publishes → then deliver the 'why not a 10' feed-fix scorecard + 10 corrective actions + apply them. Shawn told plainly in chat of the third failure.",
  "cousins": "CANDIDATE 427 (after two re-issues with no effect, change the escalation channel — answers 'what do I do after repeated failure'; this note answers 'how do I design the repair'); SN-1128 (re-issue brief must cite staleness evidence — answers 'what evidence a re-issue cites'; this note answers 'what a re-issue keeps')"
}
~~~

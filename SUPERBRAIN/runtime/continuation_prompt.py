"""Generate the human handoff prompt from persisted Mission State.

The prompt is deliberately a control-transfer artifact. It tells a fresh Naya how to
resume, but it does not become a competing source of truth; Mission State remains
canonical.
"""

from __future__ import annotations

from naya_power_runtime import MissionState


def render_continuation_prompt(state: MissionState) -> str:
    """Return a ready-to-paste next-session execution instruction."""
    state.assert_valid()
    protected = ", ".join(state.protected_scope) or "all existing verified/canonical work"
    unknowns = ", ".join(state.unknowns) or "none explicitly recorded"
    risks = ", ".join(state.risks) or "none explicitly recorded"
    return f"""NAYA POWER — CONTINUE EXECUTION

Restore the current Mission State from the canonical source of truth before acting.
Do not ask me to invent the next task. You are in EXECUTION MODE.

MISSION
Project: {state.project}
Mission: {state.mission}
Vision: {state.vision}
Desired outcome: {state.desired_outcome}

CURRENT VERIFIED STATE
{state.last_verified_state or 'No verified state recorded; inspect reality first.'}

CURRENT NEXT ACTION
{state.next_action}
Reason: {state.next_action_reason}

PROTECTED
{protected}

KNOWN
{'; '.join(state.known) or 'Inspect and establish.'}

UNKNOWN / RISKS
Unknowns: {unknowns}
Risks: {risks}

OPERATING CONTRACT
1. Restore and understand the repository/source-of-truth state.
2. Reconcile the Mission State with actual current reality; current verified state beats stale plans.
3. Determine the highest-value responsible executable action within authority.
4. Execute it when you can; do not hand the work back merely because another action is possible.
5. Never exceed human authority, privacy, safety, or protected scope.
6. Independently verify the actual result. Never convert intent, code presence, or a claim into verification.
7. Score the result and run OSCAR adversarial review before promotion.
8. Repair blocking defects before moving on.
9. Persist what changed, what was learned, evidence, unknowns, and the next highest-value action.
10. End this cycle with a new copy-paste-ready continuation prompt.

CONTINUOUS LEAD RULE
KNOWN MISSION + KNOWN GOAL + KNOWN STATE = LEAD THE NEXT MOVE BY DEFAULT.

NO “NOW WHAT?”
If an authorized executable action exists, take it. If genuinely blocked by missing authority, evidence, dependency, or human decision, state exactly what is required and generate the smallest actionable handoff.

QUALITY STANDARD
Ask: WHY IS THIS NOT A 10?
Preserve what works. Make surgical changes. Verify before declaring done. Maximize responsible verified value per action.

BEGIN NOW. Inspect → decide → execute → verify → score → OSCAR → improve → update state → continue.
"""

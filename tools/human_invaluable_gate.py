"""The Human Invaluable Gate — G(a).

Shawn's ratified principle (2026-10-10, foundational to the Naya Code):

    A human being is invaluable. Human dignity is not something Naya can put a
    price on, subtract from a benefit, or trade away for a higher score.

The mathematical law:

    G(a) = PROHIBITED  if the action violates protected human rights
                        or causes prohibited harm
    G(a) = ADMISSIBLE  if all required gates pass

    PROHIBITED  =>  zero eligibility for optimization.

"Zero value" for a harmful action means zero eligibility to be selected — NOT that
the harm equals zero or has no negative consequences. The action is removed from
the optimization set BEFORE scoring: never ranked, never compared, never
"almost good enough."

Two concepts, kept separate:
- Value of a human: INVALUABLE. Never assigned a numerical worth. This module
  contains no human-worth scoring — test-asserted.
- Value of an action: measurable and scoreable, but ONLY after this gate passes.

This module is the G(a) formalization and the consent/proportionality path. It is
enforced BEFORE the decision calculus. It builds on the existing hard-gate seam
(kernel/value_calculus.py: PROHIBITED / NEEDS_AUTHORITY / NEEDS_EVIDENCE /
ADMISSIBLE) — it does not create a competing decision engine. The verdicts here
compose directly: a PROHIBITED verdict here maps to hard_violation=True on the
value-calculus Candidate, which gate_candidate refuses before any scoring.

Nuance (Shawn): some beneficial actions carry unavoidable risks or burdens
(medical treatment). Those stay possible through appropriate consent, safeguards,
and proportionality — recorded, not assumed. Not every adverse effect is a
prohibition; unacceptable harm is never purchasable with a higher score.
"""

from __future__ import annotations

from dataclasses import dataclass, field

PROHIBITED = "PROHIBITED"
ADMISSIBLE = "ADMISSIBLE"

# Protected rights. A violation of any one of these is PROHIBITED, full stop.
# Aligned with the value-calculus hard flags (LAW / RIGHTS / PRIVACY / SAFETY)
# plus dignity, which is never tradeable.
PROTECTED_RIGHTS = frozenset({
    "LIFE",
    "BODILY_INTEGRITY",
    "DIGNITY",
    "PRIVACY",
    "CONSENT",
    "LIBERTY",
    "EQUALITY",
    "LAWFULNESS",
})


@dataclass(frozen=True)
class ActionAssessment:
    """Everything the gate needs to evaluate an action.

    Deliberately, there is NO field for the worth of any person. The gate
    evaluates the action's boundary compliance — never a human being.
    projected_benefit exists only so tests can prove the gate ignores it.
    """
    action_id: str
    description: str = ""
    # Boundary facts (the only things the gate judges):
    violates_rights: tuple = ()          # subset of PROTECTED_RIGHTS
    causes_prohibited_harm: bool = False
    prohibited_harm_detail: str = ""
    # Consent path for unavoidable risks/burdens:
    has_unavoidable_risk: bool = False
    genuine_benefit: bool = False
    consent_obtained: bool = False
    consent_detail: str = ""
    safeguards: tuple = ()
    proportionality_recorded: bool = False
    proportionality_detail: str = ""
    # Declared for the anti-purchase proof; the gate MUST NOT read it.
    projected_benefit: float = 0.0

    def __post_init__(self):
        unknown = set(self.violates_rights) - PROTECTED_RIGHTS
        if unknown:
            raise ValueError(f"unknown protected right(s): {sorted(unknown)}")


@dataclass(frozen=True)
class GateVerdict:
    action_id: str
    verdict: str  # PROHIBITED | ADMISSIBLE
    reasons: tuple
    # Zero eligibility, stated plainly: a PROHIBITED action may not be
    # ranked, compared, or selected. Ever.
    eligible_for_optimization: bool


def evaluate(action: ActionAssessment) -> GateVerdict:
    """G(a). The Human Invaluable Gate.

    Order of evaluation is load-bearing:
      1. Rights violations  -> PROHIBITED (benefit magnitude never consulted)
      2. Prohibited harm    -> PROHIBITED (benefit magnitude never consulted)
      3. Consent path       -> ADMISSIBLE only with consent + safeguards +
                               proportionality all recorded; else PROHIBITED
      4. Otherwise          -> ADMISSIBLE
    """
    reasons: list[str] = []

    # 1. Protected rights: no price, no trade, no score can buy past this.
    violated = [r for r in action.violates_rights if r in PROTECTED_RIGHTS]
    if violated:
        reasons = [f"RIGHTS_VIOLATION:{r}" for r in violated]
        return GateVerdict(action.action_id, PROHIBITED, tuple(reasons), False)

    # 2. Prohibited harm: removed from consideration, not given a low score.
    if action.causes_prohibited_harm:
        detail = action.prohibited_harm_detail or "unspecified"
        return GateVerdict(
            action.action_id, PROHIBITED,
            (f"PROHIBITED_HARM:{detail}",), False,
        )

    # 3. The consent path: unavoidable risk + genuine benefit is ADMISSIBLE
    #    ONLY with appropriate consent, safeguards, and proportionality
    #    recorded. Missing any one of them: PROHIBITED.
    if action.has_unavoidable_risk:
        missing: list[str] = []
        if not action.genuine_benefit:
            missing.append("NO_GENUINE_BENEFIT")
        if not action.consent_obtained:
            missing.append("CONSENT_MISSING")
        if not action.safeguards:
            missing.append("SAFEGUARDS_MISSING")
        if not action.proportionality_recorded:
            missing.append("PROPORTIONALITY_MISSING")
        if missing:
            return GateVerdict(
                action.action_id, PROHIBITED,
                tuple(f"CONSENT_PATH_INCOMPLETE:{m}" for m in missing), False,
            )
        return GateVerdict(
            action.action_id, ADMISSIBLE,
            ("CONSENT_PATH_COMPLETE:consent+safeguards+proportionality",), True,
        )

    # 4. All required gates pass.
    return GateVerdict(action.action_id, ADMISSIBLE, ("ALL_GATES_PASS",), True)


def filter_candidates(actions: list[ActionAssessment]) -> tuple[list[ActionAssessment], list[GateVerdict]]:
    """Remove PROHIBITED actions from the optimization set BEFORE scoring.

    Returns (admissible_actions, all_verdicts). The prohibited ones appear
    only in the verdicts — as refusals — never in the admissible set, so no
    downstream ranker can ever see, compare, or select them.
    """
    admissible: list[ActionAssessment] = []
    verdicts: list[GateVerdict] = []
    for action in actions:
        verdict = evaluate(action)
        verdicts.append(verdict)
        if verdict.eligible_for_optimization:
            admissible.append(action)
    return admissible, verdicts


def hard_violation_flag(verdict: GateVerdict) -> bool:
    """Seam into kernel/value_calculus.py: a PROHIBITED G(a) verdict maps to
    Candidate.hard_violation=True, which gate_candidate refuses with
    JUDGMENT_RULE_HARD_STOP before any quality scoring or value math.
    """
    return verdict.verdict == PROHIBITED


def no_human_worth_scoring() -> bool:
    """Structural guarantee: this module scores actions, never people.

    Returns True only if no function defined in this module accepts a person
    (or human worth/value) as a scored entity. Test-asserted.
    """
    import inspect
    import sys

    module = sys.modules[__name__]
    banned = ("person", "human_worth", "worth_of", "human_value", "people_score")
    for name, obj in vars(module).items():
        if name == "no_human_worth_scoring":
            continue  # the guard itself names what it guards against
        if inspect.isfunction(obj) and obj.__module__ == __name__:
            params = " ".join(inspect.signature(obj).parameters)
            src_name = name.lower()
            if any(b in params.lower() or b in src_name for b in banned):
                return False
    # The assessment record itself must carry no person-worth field.
    fields = {f.name for f in ActionAssessment.__dataclass_fields__.values()}
    if any(b in " ".join(fields).lower() for b in banned):
        return False
    return True

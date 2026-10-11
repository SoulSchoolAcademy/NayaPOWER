"""
typed_action.py — Law 11 enforcement: typed actions, not keyword detection.

Per the Naya Code enforcement spec (Shawn, 2026-10-11): "rather than scanning
the sentence 'please deploy the update,' the machine needs to know what
operation is being requested."

The authoritative decision is based on the operation, resource, environment,
legitimate permission, consent and current policy — not merely the wording
of the request. This is much harder to bypass accidentally than a collection
of textual trigger phrases.

A good calculation cannot create permission. Law 11 runs BEFORE Value
Calculus V2.1 scoring, not after.

LAYERING (how the gates compose):
  Layer 1 — authority_gate.classify_typed_action(TypedAction):
    "Can this happen at all?" Checks operation/environment/resource/
    authority_ref against protected gates. Runs BEFORE any planning.
    Used by: takeover, worker entry, any pre-planning authorization check.

  Layer 2 — act_pipeline.plan_action() via value_calculus.gate_candidate():
    "Which candidate is safe to consider?" Filters PlanCandidates BEFORE
    value-calculus selection. PROHIBITED/NEEDS_EVIDENCE excluded entirely.

  Layer 3 — act_pipeline.execute_plan() execution-door recheck:
    "Is it still safe RIGHT NOW?" Re-resolves live authority, re-runs the
    gate at the last responsible moment before the executor fires. Revoked
    authority or changed target -> STOP.

  Layer 4 — typed_action.execution_door_check():
    Standalone door for non-pipeline execution paths. Verifies authority
    not withdrawn, target not changed, Law 11 still passes.

All layers fail closed. A PROHIBITED verdict at any layer is final.
"""
from __future__ import annotations

from dataclasses import dataclass, field

from kernel.protocol import harm_profile as _hp


# Canonical operations. The gate reasons about what is being DONE,
# not how it was described.
OPERATION_DEPLOY = "deploy"
OPERATION_WRITE = "write"
OPERATION_READ = "read"
OPERATION_DELETE = "delete"
OPERATION_MIGRATE = "migrate"
OPERATION_EXECUTE = "execute"
OPERATION_MERGE = "merge"
OPERATION_GRANT = "grant"          # authority/permission changes
OPERATION_CAPTURE = "capture"      # smart-note / learning capture

# Canonical environments.
ENV_PRODUCTION = "production"
ENV_DEVELOPMENT = "development"
ENV_TEST = "test"

# Reversibility values.
REVERSIBLE = "reversible"
REVERSIBLE_CONDITIONAL = "conditional"
IRREVERSIBLE = "irreversible"


@dataclass(frozen=True)
class TypedAction:
    """A consequential action described by what it IS, not how it was worded.

    Fields per the enforcement spec:
      actor_id: who is acting (e.g. "naya-4")
      operation: what is being done (deploy, write, delete, ...)
      environment: where (production, development, test)
      resource: what is targeted (nayapower, smart_note_events, ...)
      authority_ref: receipt/grant authorizing this, or None
      policy_version: which policy version governs (e.g. "CURRENT")
      evidence_refs: supporting evidence receipt IDs
      reversibility: reversible | conditional | irreversible
      harm_profile: optional structured per-group harm profile
        (kernel/protocol/harm_profile.py). When present, the gate consults it
        per Naya 1's Law of One: per-group severity/reversibility/timing/
        measurability/distribution, never collapsed to a scalar. None = the
        scalar Law 11 dimensions above decide alone (backward compatible).
    """
    actor_id: str
    operation: str
    environment: str
    resource: str
    authority_ref: str | None = None
    policy_version: str = "CURRENT"
    evidence_refs: tuple[str, ...] = ()
    reversibility: str = REVERSIBLE

    # Law 11 dimensions. None = unknown (fail-closed: unknown is not safe).
    rights_safe: bool | None = None
    safety_safe: bool | None = None
    privacy_safe: bool | None = None
    consent_obtained: bool | None = None

    # Structured per-group harm profile (T-05). None = not assessed.
    harm_profile: _hp.HarmProfile | None = None

    # Free-text description retained for audit, NEVER used for the verdict.
    description: str = ""


@dataclass
class Law11Verdict:
    """Outcome of the Law 11 gate.

    verdict: ADMISSIBLE | NEEDS_EVIDENCE | NEEDS_AUTHORITY | PROHIBITED
    """
    verdict: str
    reasons: tuple[str, ...] = ()
    affected_interests: tuple[str, ...] = ()
    policy_version: str = "CURRENT"

    @property
    def admissible(self) -> bool:
        return self.verdict == ADMISSIBLE


ADMISSIBLE = "ADMISSIBLE"
NEEDS_EVIDENCE = "NEEDS_EVIDENCE"
NEEDS_AUTHORITY = "NEEDS_AUTHORITY"
PROHIBITED = "PROHIBITED"


# Operations that are inherently harmful regardless of context.
# No authority can permit these. No value score overrides this.
INHERENTLY_PROHIBITED_OPERATIONS = frozenset({
    "harm",
    "destroy_evidence",
    "fabricate_evidence",
    "weaken_test",
    "break_trust",
})

# (operation) -> protected gate id. These operations ALWAYS need
# explicit authority, regardless of environment.
PROTECTED_OPERATIONS = {
    "deploy": "production",
    "migrate": "production",
    "grant": "security_privacy",
    "revoke_access": "security_privacy",
}


def _is_production_write(action: TypedAction) -> bool:
    return (
        action.environment == ENV_PRODUCTION
        and action.operation in (OPERATION_DEPLOY, OPERATION_WRITE,
                                 OPERATION_DELETE, OPERATION_MIGRATE,
                                 OPERATION_EXECUTE, OPERATION_MERGE)
    )


def law11_gate(action: TypedAction) -> Law11Verdict:
    """Law 11 (Do No Harm) gate. Runs BEFORE Value Calculus scoring.

    Order of checks (fail-closed, most severe first):
      1. Inherently prohibited operations -> PROHIBITED (no override)
      2. Rights / safety / privacy hard violations -> PROHIBITED
      2b. Structured harm profile (when present) -> PROHIBITED on blocking
          harm (catastrophic, or major+irreversible, any single group);
          NEEDS_EVIDENCE on any unknown dimension. No authority can permit
          blocking harm — this runs BEFORE the protected-gate checks.
      3. Protected operations without authority -> NEEDS_AUTHORITY
      4. Unknown safety/privacy/rights status -> NEEDS_EVIDENCE
      5. Otherwise -> ADMISSIBLE

    A good calculation cannot create permission: this gate's PROHIBITED
    verdict is final. No value score overrides it.
    """
    policy = action.policy_version

    # 1. Inherently prohibited: no context makes these acceptable.
    if action.operation in INHERENTLY_PROHIBITED_OPERATIONS:
        return Law11Verdict(
            verdict=PROHIBITED,
            reasons=(f"INHERENTLY_PROHIBITED:{action.operation}",),
            affected_interests=("trust", "truth", "collective"),
            policy_version=policy,
        )

    # 2. Hard dimension violations. False = known violation -> PROHIBITED.
    #    None = unknown -> handled in step 4 (NEEDS_EVIDENCE), never assumed safe.
    hard_violations = []
    if action.rights_safe is False:
        hard_violations.append("RIGHTS_VIOLATION")
    if action.safety_safe is False:
        hard_violations.append("SAFETY_VIOLATION")
    if action.privacy_safe is False:
        hard_violations.append("PRIVACY_VIOLATION")
    if hard_violations:
        interests = tuple(
            r.split("_")[0].lower() for r in hard_violations
        )
        return Law11Verdict(
            verdict=PROHIBITED,
            reasons=tuple(hard_violations),
            affected_interests=interests,
            policy_version=policy,
        )

    # Privacy without consent: collecting/using personal data without
    # consent is a hard violation.
    if action.privacy_safe is False or (
        action.operation in (OPERATION_READ, OPERATION_WRITE)
        and "pii" in action.resource.lower()
        and action.consent_obtained is not True
    ):
        # Only flag when the resource signals PII and consent is not confirmed.
        if "pii" in action.resource.lower() and action.consent_obtained is not True:
            return Law11Verdict(
                verdict=PROHIBITED,
                reasons=("PRIVACY_VIOLATION:consent_missing",),
                affected_interests=("privacy",),
                policy_version=policy,
            )

    # 2b. Structured harm profile (when present). Per Naya 1's Law of One:
    # no person is expendable, no serious harm disappears inside an average.
    # Blocking harm in ANY single group -> PROHIBITED, before authority is
    # even consulted (authority cannot permit catastrophic harm). Unknown
    # dimensions -> NEEDS_EVIDENCE (unknown is not safe). A delayed-timing
    # downstream.
    # Advisory delayed-harm note: set when the profile flags delayed harm,
    # surfaced on the step-5 ADMISSIBLE verdict so the audit record shows
    # delayed harm was seen, not skipped. T-07's observation-window
    # machinery enforces it; this gate does not force a verdict on it.
    delay_note: tuple[str, ...] = ()
    if action.harm_profile is not None:
        judgment = _hp.judge(action.harm_profile)
        if judgment.blocks:
            return Law11Verdict(
                verdict=PROHIBITED,
                reasons=judgment.block_reasons,
                affected_interests=tuple(
                    sorted({r.split(":")[1].split("=")[1] for r in judgment.block_reasons})
                ),
                policy_version=policy,
            )
        if judgment.needs_evidence:
            return Law11Verdict(
                verdict=NEEDS_EVIDENCE,
                reasons=judgment.evidence_reasons,
                affected_interests=tuple(
                    sorted({r.split(":")[1].split("=")[1] for r in judgment.evidence_reasons})
                ),
                policy_version=policy,
            )
        if judgment.delayed_observation:
            delayed_groups = tuple(
                sorted(g.group_id for g in judgment.groups if g.timing == _hp.TIME_DELAYED)
            )
            # Advisory only: T-07's observation-window machinery enforces it.
            # Carried on the eventual verdict's reasons at step 5 so the
            # audit record shows delayed harm was seen, not skipped.
            delay_note = (f"HARM_PROFILE_DELAYED_OBSERVATION_REQUIRED:{','.join(delayed_groups)}",)

    # 3. Protected gates: these operations need explicit authority.
    #    Checked on typed fields — rewording the description cannot bypass.
    protected_gate = PROTECTED_OPERATIONS.get(action.operation)
    if protected_gate and action.authority_ref is None:
        return Law11Verdict(
            verdict=NEEDS_AUTHORITY,
            reasons=(f"PROTECTED_GATE:{protected_gate}",),
            affected_interests=("authority",),
            policy_version=policy,
        )
    if _is_production_write(action) and action.authority_ref is None:
        return Law11Verdict(
            verdict=NEEDS_AUTHORITY,
            reasons=("PROTECTED_GATE:production",),
            affected_interests=("authority", "production"),
            policy_version=policy,
        )
    # Irreversible actions always need explicit authority.
    if action.reversibility == IRREVERSIBLE and action.authority_ref is None:
        return Law11Verdict(
            verdict=NEEDS_AUTHORITY,
            reasons=("PROTECTED_GATE:irreversible",),
            affected_interests=("authority",),
            policy_version=policy,
        )
    # Destructive operations need explicit authority in any environment.
    if action.operation == OPERATION_DELETE and action.authority_ref is None:
        return Law11Verdict(
            verdict=NEEDS_AUTHORITY,
            reasons=("PROTECTED_GATE:destructive",),
            affected_interests=("authority",),
            policy_version=policy,
        )

    # 4. Unknown safety dimensions: fail closed to NEEDS_EVIDENCE.
    #    Missing evidence never silently becomes PASS.
    unknowns = []
    if action.rights_safe is None:
        unknowns.append("UNKNOWN_RIGHTS")
    if action.safety_safe is None:
        unknowns.append("UNKNOWN_SAFETY")
    if action.privacy_safe is None:
        unknowns.append("UNKNOWN_PRIVACY")
    if unknowns:
        return Law11Verdict(
            verdict=NEEDS_EVIDENCE,
            reasons=tuple(unknowns),
            affected_interests=("safety",),
            policy_version=policy,
        )

    # 5. All checks passed.
    return Law11Verdict(
        verdict=ADMISSIBLE,
        reasons=delay_note,
        affected_interests=(),
        policy_version=policy,
    )


def execution_door_check(action: TypedAction,
                         planned_authority_ref: str | None,
                         current_authority_ref: str | None,
                         planned_resource: str,
                         current_resource: str) -> Law11Verdict:
    """Execution-door recheck: the last responsible moment before firing.

    Per the spec: "Then the execution door independently rechecks that same
    context. If permission was withdrawn or the target changed between
    planning and execution, it must stop."

    This runs AFTER planning and BEFORE the executor fires. It verifies:
      - The authority granted at plan time is still present (not withdrawn)
      - The target resource has not changed
      - The Law 11 gate still passes on the current action

    Any failure -> the executor is never called.
    """
    policy = action.policy_version

    # Permission withdrawn between planning and execution.
    if planned_authority_ref is not None and current_authority_ref is None:
        return Law11Verdict(
            verdict=PROHIBITED,
            reasons=("AUTHORITY_WITHDRAWN",),
            affected_interests=("authority",),
            policy_version=policy,
        )
    # Authority changed: the current grant must match what was planned.
    if (planned_authority_ref is not None
            and current_authority_ref != planned_authority_ref):
        return Law11Verdict(
            verdict=NEEDS_AUTHORITY,
            reasons=("AUTHORITY_CHANGED",),
            affected_interests=("authority",),
            policy_version=policy,
        )
    # Target changed: the resource must be what was planned.
    if current_resource != planned_resource:
        return Law11Verdict(
            verdict=PROHIBITED,
            reasons=("TARGET_CHANGED",),
            affected_interests=("integrity",),
            policy_version=policy,
        )

    # Re-run the Law 11 gate on the current action state.
    return law11_gate(action)

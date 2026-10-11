"""neutrality_finding.py — T-06: six-state finding classification (the neutrality trap).

Per Naya 1's "Do-No-Harm Law: Intelligent Risk Under Uncertainty" (2026-10-11):

  Systems claim "neutral" when they mean "unknown". Six finding states
  prevent this:

    TRUE_ZERO          — measured with adequate power; the effect is
                         identically zero BY MECHANISM, not by luck of the
                         sample. Rare. Requires exact-zero evidence (e.g. the
                         code path cannot execute, the resource does not
                         exist).
    PRACTICALLY_NEUTRAL — measured effect within a PREAPPROVED domain
                         tolerance: |effect| <= epsilon with justified
                         uncertainty bounds, and epsilon was approved BEFORE
                         the measurement. No post-hoc tolerance selection.
    UNKNOWN            — no measurement attempted, or evidence insufficient
                         to classify. Fail-closed: maps to NEEDS_EVIDENCE,
                         never ADMISSIBLE-by-default.
    UNMEASURED         — measurement not possible with available instruments.
                         Explicit and recorded, never hidden inside an
                         average or a zero.
    DELAYED            — effect not yet observable; requires an observation
                         window with stop conditions (T-07's seam). An
                         admissible-now verdict carries the window.
    INCONCLUSIVE       — measured but underpowered or contradictory. A wide
                         interval centered on zero is INCONCLUSIVE, NOT
                         harmlessness, NOT neutrality.

Machine rules enforced here:
  R1. A "no harm" / "neutral" claim on any harm-profile dimension WITHOUT a
      finding state is rejected outright — the claim is the trap. Missing
      states are treated as UNKNOWN.
  R2. Wide-interval-centered-on-zero -> INCONCLUSIVE. It is never
      PRACTICALLY_NEUTRAL (which requires |effect| <= epsilon with justified
      bounds AND preapproved epsilon) and never TRUE_ZERO.
  R3. Tolerances are approved per domain BEFORE results exist. A tolerance
      chosen after seeing the measurement is a defect; the receipt must name
      the tolerance value and its approval reference.
  R4. UNKNOWN / UNMEASURED / INCONCLUSIVE on a material dimension ->
      NEEDS_EVIDENCE (fail-closed). TRUE_ZERO / PRACTICALLY_NEUTRAL are the
      only states that count as genuine neutrality for a dimension.
  R5. DELAYED on a material dimension -> NEEDS_EVIDENCE unless a T-07
      observation window is named (then admissible-with-window).
  R6. TRUE_ZERO / PRACTICALLY_NEUTRAL are the only states that count as
      genuine neutrality for a dimension.

This module does NOT re-derive or re-shape the harm profile (T-05's module).
It adds the finding-state vocabulary ON the profile: which (group, dimension)
pairs make a neutrality claim, and whether each claim's finding state is
machine-validated. T-07 owns observation windows; this module only names the
required window reference.
"""
from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field

from kernel.protocol import harm_profile as _hp

# ---------------------------------------------------------------------------
# The six finding states.
# ---------------------------------------------------------------------------

TRUE_ZERO = "TRUE_ZERO"
PRACTICALLY_NEUTRAL = "PRACTICALLY_NEUTRAL"
UNKNOWN = "UNKNOWN"
UNMEASURED = "UNMEASURED"
DELAYED = "DELAYED"
INCONCLUSIVE = "INCONCLUSIVE"

FINDING_STATES = (
    TRUE_ZERO,
    PRACTICALLY_NEUTRAL,
    UNKNOWN,
    UNMEASURED,
    DELAYED,
    INCONCLUSIVE,
)

# States that count as genuine neutrality for a dimension (R6).
CLEARING_STATES = (TRUE_ZERO, PRACTICALLY_NEUTRAL)

# States that fail closed to NEEDS_EVIDENCE (R4).
EVIDENCE_STATES = (UNKNOWN, UNMEASURED, INCONCLUSIVE)


# ---------------------------------------------------------------------------
# NeutralityAssessment — one claimed finding state with its evidence.
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class NeutralityAssessment:
    """A claimed finding state for one (group, dimension) neutrality claim.

    dimension: which harm-profile dimension the claim is about (T-05's
        H_g(a) dimensions: "severity", "reversibility", "timing",
        "measurability", "distribution"). The machine-required case is
        dimension="severity" with a "negligible" profile value — the "no
        material harm" claim.
    group: the affected group_id from the harm profile; never averaged away.
    finding: one of the six FindingState values — the CLAIM. The machine
        validates it against the evidence fields below; the validated
        outcome (not the claim) decides.
    effect_estimate: measured/estimated effect size, if measured.
    uncertainty_interval: (lo, hi) justified bounds, if bounded.
    tolerance: the domain tolerance epsilon; REQUIRED for a
        PRACTICALLY_NEUTRAL claim.
    tolerance_approval_ref: names the pre-registration record that approved
        epsilon; REQUIRED for PRACTICALLY_NEUTRAL (R3).
    tolerance_preapproved: assessor attestation that epsilon was approved
        BEFORE the measurement existed. False (or absent) -> the tolerance
        is post-hoc -> the claim is rejected (R3).
    observation_window_ref: names the T-07 observation window; required for
        a DELAYED claim to be admissible-with-window (R5).
    zero_by_mechanism: assessor attestation that the zero is by mechanism
        (the path cannot execute / the resource does not exist), not by
        sample luck. REQUIRED for TRUE_ZERO.
    zero_by_mechanism_ref: evidence naming the mechanism that forces zero.
    """
    dimension: str
    group: str
    finding: str
    effect_estimate: float | None = None
    uncertainty_interval: tuple[float, float] | None = None
    tolerance: float | None = None
    tolerance_approval_ref: str = ""
    tolerance_preapproved: bool = False
    observation_window_ref: str = ""
    zero_by_mechanism: bool = False
    zero_by_mechanism_ref: str = ""

    def __post_init__(self) -> None:
        if not self.dimension or not self.dimension.strip():
            raise ValueError("NeutralityAssessment.dimension must be non-empty")
        if not self.group or not self.group.strip():
            raise ValueError("NeutralityAssessment.group must be non-empty")
        if self.finding not in FINDING_STATES:
            raise ValueError(
                f"NeutralityAssessment.finding={self.finding!r} is not a canonical "
                f"finding state; must be one of {FINDING_STATES}"
            )
        if self.uncertainty_interval is not None:
            lo, hi = self.uncertainty_interval
            if lo > hi:
                raise ValueError(
                    f"uncertainty_interval lower bound {lo} exceeds upper {hi}"
                )


# ---------------------------------------------------------------------------
# NeutralityVerdict — the machine's validated outcome for one claim.
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class NeutralityVerdict:
    """Machine-validated outcome for one (group, dimension) claim.

    accepted_finding: the finding state the machine accepts — the validated
        outcome, which may DOWNGRADE an unevidenced claim (never upgrade).
    clears: True only for validated TRUE_ZERO / PRACTICALLY_NEUTRAL (R6).
    reason_ids: machine-readable causes, NEUTRALITY_<KIND>:group=<g>:
        dimension=<d> — carried onto the Law 11 verdict so an auditor sees
        WHY a dimension was called neutral (or not).
    advisory: window-carrying notes for DELAYED-with-window; surfaced on an
        admissible verdict, never as a block.
    """
    dimension: str
    group: str
    accepted_finding: str
    clears: bool
    reason_ids: tuple[str, ...] = ()
    advisory: tuple[str, ...] = ()

    @property
    def needs_evidence(self) -> bool:
        return self.accepted_finding in EVIDENCE_STATES


def _rid(kind: str, group: str, dimension: str) -> str:
    return f"NEUTRALITY_{kind}:group={group}:dimension={dimension}"


def classify_finding(
    a: NeutralityAssessment,
    window_exists: Callable[[str], bool] | None = None,
) -> NeutralityVerdict:
    """Validate one claimed finding state against its attached evidence.

    The machine never upgrades a claim — it accepts it or downgrades it to
    a fail-closed state. Every downgrade names its exact cause in
    reason_ids.

    window_exists: optional verifier for T-07 observation window references.
        When a DELAYED claim names a window, the reference is checked
        against the real registry (Gap 1 fix, 2026-10-11 — a fake window
        name must never pass as a real observation window). If the verifier
        is absent, the window is unverifiable and the claim fails closed;
        if the verifier reports the window unknown, the claim is rejected.
    """
    g, d = a.group, a.dimension

    # --- TRUE_ZERO: requires exact-zero evidence BY MECHANISM. ---
    if a.finding == TRUE_ZERO:
        if not (a.zero_by_mechanism and a.zero_by_mechanism_ref.strip()):
            # A bare "no effect observed" is not exact-zero evidence.
            return NeutralityVerdict(
                dimension=d, group=g, accepted_finding=UNKNOWN, clears=False,
                reason_ids=(_rid("TRUE_ZERO_UNEVIDENCED", g, d),),
            )
        if a.effect_estimate is not None and a.effect_estimate != 0.0:
            # The measurement contradicts the zero claim.
            return NeutralityVerdict(
                dimension=d, group=g, accepted_finding=INCONCLUSIVE, clears=False,
                reason_ids=(_rid("TRUE_ZERO_CONTRADICTED", g, d),),
            )
        if a.uncertainty_interval is not None:
            lo, hi = a.uncertainty_interval
            if not (lo == 0.0 and hi == 0.0):
                return NeutralityVerdict(
                    dimension=d, group=g, accepted_finding=INCONCLUSIVE, clears=False,
                    reason_ids=(_rid("TRUE_ZERO_UNBOUNDED", g, d),),
                )
        return NeutralityVerdict(
            dimension=d, group=g, accepted_finding=TRUE_ZERO, clears=True,
            reason_ids=(_rid("TRUE_ZERO_ACCEPTED", g, d),),
        )

    # --- PRACTICALLY_NEUTRAL: preapproved epsilon + effect inside it +
    #     justified bounds fully inside it (R2, R3). ---
    if a.finding == PRACTICALLY_NEUTRAL:
        if a.tolerance is None or a.tolerance <= 0.0:
            return NeutralityVerdict(
                dimension=d, group=g, accepted_finding=UNKNOWN, clears=False,
                reason_ids=(_rid("TOLERANCE_MISSING", g, d),),
            )
        if not a.tolerance_approval_ref.strip():
            return NeutralityVerdict(
                dimension=d, group=g, accepted_finding=UNKNOWN, clears=False,
                reason_ids=(_rid("TOLERANCE_UNAPPROVED", g, d),),
            )
        if not a.tolerance_preapproved:
            # R3: a tolerance chosen after seeing the measurement is a
            # defect — rejected even when |effect| <= epsilon.
            return NeutralityVerdict(
                dimension=d, group=g, accepted_finding=INCONCLUSIVE, clears=False,
                reason_ids=(_rid("TOLERANCE_POSTHOC", g, d),),
            )
        if a.effect_estimate is None or a.uncertainty_interval is None:
            # No measurement / no justified bounds -> the neutrality basis
            # is unknown.
            return NeutralityVerdict(
                dimension=d, group=g, accepted_finding=UNKNOWN, clears=False,
                reason_ids=(_rid("UNJUSTIFIED_BOUNDS", g, d),),
            )
        eps = a.tolerance
        lo, hi = a.uncertainty_interval
        if abs(a.effect_estimate) > eps:
            # The measured effect exceeds the tolerance: the neutrality
            # claim is contradicted by its own evidence.
            return NeutralityVerdict(
                dimension=d, group=g, accepted_finding=INCONCLUSIVE, clears=False,
                reason_ids=(_rid("EFFECT_EXCEEDS_TOLERANCE", g, d),),
            )
        if lo < -eps or hi > eps:
            # R2: the wide interval centered on zero. The bounds admit
            # material effects, so this is INCONCLUSIVE — never neutrality.
            return NeutralityVerdict(
                dimension=d, group=g, accepted_finding=INCONCLUSIVE, clears=False,
                reason_ids=(_rid("WIDE_INTERVAL", g, d),),
            )
        return NeutralityVerdict(
            dimension=d, group=g, accepted_finding=PRACTICALLY_NEUTRAL, clears=True,
            reason_ids=(_rid("PRACTICALLY_NEUTRAL_ACCEPTED", g, d),),
        )

    # --- Honest states: accepted as claimed (R4/R5 map them downstream). ---
    if a.finding in (UNKNOWN, UNMEASURED, INCONCLUSIVE):
        return NeutralityVerdict(
            dimension=d, group=g, accepted_finding=a.finding, clears=False,
            reason_ids=(_rid(a.finding, g, d),),
        )

    # --- DELAYED: accepted; admissibility needs a named window (R5), and
    #     the named window must exist in T-07's registry (Gap 1). ---
    if a.finding == DELAYED:
        ref = a.observation_window_ref.strip()
        if not ref:
            return NeutralityVerdict(
                dimension=d, group=g, accepted_finding=DELAYED, clears=False,
                reason_ids=(_rid("DELAYED_NO_WINDOW", g, d),),
            )
        if window_exists is None:
            # No registry wired: the window reference is unverifiable.
            # Fail closed — an unverifiable name is not a real window.
            return NeutralityVerdict(
                dimension=d, group=g, accepted_finding=DELAYED, clears=False,
                reason_ids=(_rid("DELAYED_WINDOW_UNVERIFIED", g, d),),
            )
        if not window_exists(ref):
            # The registry says this window does not exist. Reject.
            return NeutralityVerdict(
                dimension=d, group=g, accepted_finding=DELAYED, clears=False,
                reason_ids=(_rid("DELAYED_WINDOW_UNKNOWN", g, d),),
            )
        return NeutralityVerdict(
            dimension=d, group=g, accepted_finding=DELAYED, clears=False,
            reason_ids=(_rid("DELAYED_WITH_WINDOW", g, d),),
            advisory=(
                f"NEUTRALITY_DELAYED_WINDOW:group={g}:dimension={d}"
                f":window={ref}",
            ),
        )

    # Unreachable (constructor rejects non-canonical findings), kept as a
    # fail-closed belt: an unrecognized claim is unknown, never neutral.
    return NeutralityVerdict(
        dimension=d, group=g, accepted_finding=UNKNOWN, clears=False,
        reason_ids=(_rid("INVALID_STATE", g, d),),
    )


# ---------------------------------------------------------------------------
# Neutrality claims — which (group, dimension) pairs require a finding state.
# ---------------------------------------------------------------------------

# The harm-profile dimension whose benign extreme is a "no material harm"
# claim. severity == negligible says "this group is not harmed" — that is
# the neutrality claim the trap hides inside. The other dimensions'
# benign values are qualifiers, not harm claims, so they need no finding
# state (but voluntarily supplied assessments are still validated).
NEUTRALITY_CLAIM_DIMENSION = "severity"
NEGLIGIBLE_SEVERITY = _hp.SEVERITY_NEGLIGIBLE


def required_finding_keys(profile: _hp.HarmProfile) -> tuple[tuple[str, str], ...]:
    """Every (group, dimension) pair that makes a neutrality claim.

    A neutrality claim = severity qualified as negligible ("no material
    harm"). Each such pair MUST carry a NeutralityAssessment; a missing
    state is treated as UNKNOWN (R1) and fails closed (R4).
    """
    keys: list[tuple[str, str]] = []
    for g in profile.groups:
        if g.severity == NEGLIGIBLE_SEVERITY:
            keys.append((g.group_id, NEUTRALITY_CLAIM_DIMENSION))
    return tuple(keys)


# ---------------------------------------------------------------------------
# NeutralityConsult — the gate-facing consult over a whole profile.
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class NeutralityConsult:
    """Outcome of consulting finding states over a harm profile.

    blocks_admission: True when some neutrality claim fails to validate to
        a clearing state — the gate must return NEEDS_EVIDENCE.
    needs_evidence_reasons: the NEUTRALITY_* reason ids for the gate.
    delayed_advisory: DELAYED-with-window notes to surface on an otherwise
        admissible verdict (advisory, like T-05's delay_note).
    verdicts: the per-(group, dimension) validated outcomes, preserved for
        audit.
    affected_groups: the group_ids whose claims block admission, as direct
        data — the gate must use this list, never parse group names out of
        reason strings (Gap 2 fix, 2026-10-11).
    """
    blocks_admission: bool
    needs_evidence_reasons: tuple[str, ...] = ()
    delayed_advisory: tuple[str, ...] = ()
    verdicts: tuple[NeutralityVerdict, ...] = ()
    affected_groups: tuple[str, ...] = ()


def consult_neutrality(
    profile: _hp.HarmProfile,
    assessments: tuple[NeutralityAssessment, ...] = (),
    window_exists: Callable[[str], bool] | None = None,
) -> NeutralityConsult:
    """Validate the neutrality claims of a harm profile.

    Every required (group, dimension) key needs an assessment; a missing
    assessment is UNKNOWN (R1 -> R4). Every supplied assessment is validated
    by classify_finding. UNKNOWN / UNMEASURED / INCONCLUSIVE / DELAYED-
    without-window -> the gate must demand evidence; TRUE_ZERO /
    PRACTICALLY_NEUTRAL -> the dimension clears; DELAYED-with-window ->
    admissible-with-window advisory.

    window_exists: optional T-07 registry verifier, threaded through to
        classify_finding for DELAYED claims (Gap 1). When absent, named
        windows fail closed as unverifiable.
    """
    by_key: dict[tuple[str, str], NeutralityAssessment] = {}
    for a in assessments:
        key = (a.group, a.dimension)
        if key in by_key:
            raise ValueError(
                f"duplicate NeutralityAssessment for group={a.group!r} "
                f"dimension={a.dimension!r}"
            )
        by_key[key] = a

    verdicts: list[NeutralityVerdict] = []
    reasons: list[str] = []
    advisory: list[str] = []
    blocking_groups: list[str] = []

    # Required claims first: missing state = UNKNOWN (R1).
    for group, dimension in required_finding_keys(profile):
        key = (group, dimension)
        if key not in by_key:
            verdicts.append(
                NeutralityVerdict(
                    dimension=dimension, group=group,
                    accepted_finding=UNKNOWN, clears=False,
                    reason_ids=(_rid("MISSING_ASSESSMENT", group, dimension),),
                )
            )
        else:
            verdicts.append(classify_finding(by_key[key], window_exists))

    # Voluntary assessments on other pairs are validated too — the gate
    # never ignores supplied evidence.
    required = set(required_finding_keys(profile))
    for key, a in by_key.items():
        if key not in required:
            verdicts.append(classify_finding(a, window_exists))

    for v in verdicts:
        if v.clears:
            continue
        if v.accepted_finding == DELAYED and v.advisory:
            # R5: DELAYED with a verified named window -> admissible-with-
            # window. (The window was checked against the registry inside
            # classify_finding; advisory only fires for verified windows.)
            advisory.extend(v.advisory)
            continue
        reasons.extend(v.reason_ids)
        blocking_groups.append(v.group)

    return NeutralityConsult(
        blocks_admission=bool(reasons),
        needs_evidence_reasons=tuple(reasons),
        delayed_advisory=tuple(advisory),
        verdicts=tuple(verdicts),
        affected_groups=tuple(sorted(set(blocking_groups))),
    )

"""NAYA-NEUTRALITY-PROFILE-V1 — governed extension to the Zero Value Law (PROPOSED, NOT RATIFIED).

Status: DRAFT. Ratification is Shawn's gate. This module is part 2 of the Zero
Value Law's machinery: the governed machinery behind the "declared, versioned
epsilon" that zero_value_law.classify_zero requires before it will return
PRACTICALLY_NEUTRAL.

The core principle: small does not necessarily mean insignificant.
Insignificant does not mean unmeasured. And neutral does not mean safe.
"Neutral" is a verdict that must be earned, not a shrug.

Distinction that must be preserved (do not merge these):
  - V2.1's `interval_epsilon` (kernel/value_calculus.py, QualityProfile) compares
    COMPETING CANDIDATE ACTIONS during selection: a candidate is
    interval-dominant when its value-interval gap over the runner-up exceeds
    interval_epsilon. It answers "is this candidate clearly ahead?"
  - The neutrality tolerance here answers a different question about ONE
    measured effect versus its baseline: "is this effect practically
    immaterial for the affected parties, at this scale, over this horizon?"
    It is domain-specific, preapproved, versioned, and asymmetric.
The two must remain distinct. This module never reads or writes
QualityProfile.interval_epsilon.

Relationship to zero_value_law: that module's interval rule is the symmetric
special case (eps on both sides). This module generalizes it to the asymmetric
neutral zone N_d = [-eps_neg, +eps_pos] from the proposal. When
eps_neg == eps_pos == eps, the two rules coincide exactly.
"""

import zero_value_law as zvl

CONTRACT = "NAYA-NEUTRALITY-PROFILE-V1"
LAW_STATUS = "PROPOSED — draft machinery; ratification is Shawn's gate"

# ---------------------------------------------------------------------------
# Verdicts
# ---------------------------------------------------------------------------
MEANINGFUL_POSITIVE = "MEANINGFUL_POSITIVE"
MEANINGFUL_NEGATIVE = "MEANINGFUL_NEGATIVE"
PRACTICALLY_NEUTRAL = "PRACTICALLY_NEUTRAL"
INCONCLUSIVE = "INCONCLUSIVE"
PROVISIONAL = "PROVISIONAL"  # window open or evidence pending: not a verdict yet

# ---------------------------------------------------------------------------
# Refusal codes (machine-readable)
# ---------------------------------------------------------------------------
PROFILE_NOT_APPROVED = "PROFILE_NOT_APPROVED"
PROFILE_SPEC_INCOMPLETE = "PROFILE_SPEC_INCOMPLETE"
HARD_BOUNDARY_OVERRIDE_REFUSED = "HARD_BOUNDARY_OVERRIDE_REFUSED"
AGGREGATE_LAUNDERING_REFUSED = "AGGREGATE_LAUNDERING_REFUSED"
CUMULATIVE_HARM_EXCEEDS_LIMIT = "CUMULATIVE_HARM_EXCEEDS_LIMIT"
DELAYED_HARM_PROVISIONAL = "DELAYED_HARM_PROVISIONAL"
THRESHOLD_MANIPULATION_REFUSED = "THRESHOLD_MANIPULATION_REFUSED"
NEEDS_EVIDENCE = "NEEDS_EVIDENCE"
NEUTRAL_REQUIREMENTS_UNMET = "NEUTRAL_REQUIREMENTS_UNMET"
INTERVAL_NOT_QUALIFIED = "INTERVAL_NOT_QUALIFIED"
FAMILY_CLAIM_UNQUALIFIED = "FAMILY_CLAIM_UNQUALIFIED"
INSTRUMENT_INADEQUATE = "INSTRUMENT_INADEQUATE"

STATUS_PROPOSED = "PROPOSED"
STATUS_APPROVED = "APPROVED"
STATUS_SUPERSEDED = "SUPERSEDED"
STATUS_RETIRED = "RETIRED"


# ---------------------------------------------------------------------------
# Records (frozen: profiles are immutable once approved)
# ---------------------------------------------------------------------------
class NeutralityProfile:
    """A versioned, preapproved, domain-specific tolerance.

    Answers the eight decision factors as fields: metric+units, affected
    parties (populations incl. vulnerable groups), meaningful-effect threshold
    (the asymmetric neutral interval), protected boundaries (hard_gates),
    scale/accumulation (cumulative_limit, repetitions context), observation
    horizon, evidence quality (requirements), approval/provenance
    (approval_ref, threshold_basis_ref, version).
    """

    __slots__ = (
        "contract", "profile_id", "version", "status", "metric", "unit",
        "baseline_ref", "eps_neg", "eps_pos", "populations", "horizon",
        "requirements", "threshold_basis_ref", "approval_ref", "verification",
        "hard_gates", "cumulative_limit", "instrument_detection_limit",
    )

    def __init__(self, *, profile_id, version, metric, unit, baseline_ref,
                 eps_neg, eps_pos, populations, horizon, requirements,
                 threshold_basis_ref, approval_ref=None,
                 status=STATUS_PROPOSED, verification="UNVERIFIED",
                 hard_gates=(), cumulative_limit=None,
                 instrument_detection_limit=None):
        # Immutability via __slots__ + no setters; approved profiles are
        # never mutated — supersede() returns a new version.
        object.__setattr__(self, "contract", CONTRACT)
        object.__setattr__(self, "profile_id", profile_id)
        object.__setattr__(self, "version", str(version))
        object.__setattr__(self, "status", status)
        object.__setattr__(self, "metric", metric)
        object.__setattr__(self, "unit", unit)
        object.__setattr__(self, "baseline_ref", baseline_ref)
        object.__setattr__(self, "eps_neg", float(eps_neg))
        object.__setattr__(self, "eps_pos", float(eps_pos))
        object.__setattr__(self, "populations", tuple(populations))
        object.__setattr__(self, "horizon", horizon)
        object.__setattr__(self, "requirements", dict(requirements))
        object.__setattr__(self, "threshold_basis_ref", threshold_basis_ref)
        object.__setattr__(self, "approval_ref", approval_ref)
        object.__setattr__(self, "verification", verification)
        object.__setattr__(self, "hard_gates", tuple(hard_gates))
        object.__setattr__(self, "cumulative_limit",
                           None if cumulative_limit is None else float(cumulative_limit))
        object.__setattr__(self, "instrument_detection_limit",
                           None if instrument_detection_limit is None
                           else float(instrument_detection_limit))

    def __setattr__(self, name, value):
        raise AttributeError("NeutralityProfile is immutable; use supersede_profile()")

    def __repr__(self):
        return ("NeutralityProfile(%s v%s [%s] %s: [-%s, +%s] %s)" % (
            self.profile_id, self.version, self.status, self.metric,
            self.eps_neg, self.eps_pos, self.unit))

    # -- governed epsilon behind zero_value_law's PRACTICALLY_NEUTRAL --------
    def zero_law_epsilon_record(self):
        """The governed epsilon record this profile supplies.

        zero_value_law._epsilon_declared accepts the symmetric special case;
        this record carries the full asymmetric pair plus provenance, which is
        what classify_effect() below actually enforces.
        """
        return {
            "interval": [-self.eps_neg, self.eps_pos],
            "version": "%s@%s" % (self.profile_id, self.version),
            "justification": self.threshold_basis_ref,
            "approval_ref": self.approval_ref,
        }


REQUIREMENT_KEYS = (
    "independent_metric_review",
    "qualified_uncertainty_interval",
    "subgroup_assessment",
    "cumulative_effect_assessment",
    "hard_gates_pass",
    "observation_window_complete",
)


def default_requirements(**overrides):
    reqs = {k: True for k in REQUIREMENT_KEYS}
    reqs.update(overrides)
    return reqs


def validate_profile_spec(profile):
    """A tolerance must answer the eight decision factors. Refuse thin specs."""
    problems = []
    if not profile.metric or not profile.unit:
        problems.append("outcome metric and units are required")
    if not profile.populations:
        problems.append("affected parties are required (including smaller/vulnerable groups)")
    if not (profile.eps_neg > 0 and profile.eps_pos > 0):
        problems.append("asymmetric tolerances must both be positive magnitudes")
    if not profile.horizon:
        problems.append("observation horizon is required")
    if not profile.threshold_basis_ref:
        problems.append("threshold basis (domain evidence) is required")
    if not profile.baseline_ref:
        problems.append("baseline reference is required")
    missing_reqs = [k for k in REQUIREMENT_KEYS if k not in profile.requirements]
    if missing_reqs:
        problems.append("requirements checklist incomplete: %s" % ",".join(missing_reqs))
    # Poor measurement is a reason to improve measurement, not widen the zone.
    det = profile.instrument_detection_limit
    if det is not None and det >= min(profile.eps_neg, profile.eps_pos):
        problems.append(
            "instrument detection limit (%s) cannot resolve the neutral zone "
            "(min tolerance %s): improve measurement, do not widen the zone"
            % (det, min(profile.eps_neg, profile.eps_pos)))
    if problems:
        return {"ok": False, "refusal": PROFILE_SPEC_INCOMPLETE, "problems": problems}
    return {"ok": True, "refusal": None, "problems": []}


def approve_profile(profile, *, approval_ref, approver):
    """PROPOSED -> APPROVED. Returns a new instance; the old one is untouched.

    Approval requires a complete spec and a named approver with evidence.
    """
    spec = validate_profile_spec(profile)
    if not spec["ok"]:
        return {"ok": False, "refusal": spec["refusal"], "problems": spec["problems"]}
    if profile.status != STATUS_PROPOSED:
        return {"ok": False, "refusal": THRESHOLD_MANIPULATION_REFUSED,
                "problems": ["only PROPOSED profiles can be approved; "
                             "approved profiles are immutable"]}
    if not approval_ref or not approver:
        return {"ok": False, "refusal": PROFILE_SPEC_INCOMPLETE,
                "problems": ["approval requires a named approver and approval ref"]}
    approved = _clone_with(profile, status=STATUS_APPROVED,
                           approval_ref=approval_ref, verification="VERIFIED")
    return {"ok": True, "profile": approved,
            "note": "approved by %s as %s" % (approver, approval_ref)}


def _clone_with(profile, **changes):
    kwargs = {s: getattr(profile, s) for s in profile.__slots__ if s != "contract"}
    kwargs.update(changes)
    return NeutralityProfile(**kwargs)


def supersede_profile(profile, *, new_eps_neg=None, new_eps_pos=None,
                      threshold_basis_ref, approval_ref, approver):
    """A new tolerance needs evidence, independent review, and a new version.

    Returns the new APPROVED profile; the old profile is marked SUPERSEDED in
    the returned pair but its own record is never mutated.
    """
    if profile.status != STATUS_APPROVED:
        return {"ok": False, "refusal": THRESHOLD_MANIPULATION_REFUSED,
                "problems": ["only an APPROVED profile can be superseded"]}
    old_version = profile.version
    new_version = _bump_version(old_version)
    new_profile = _clone_with(
        profile,
        version=new_version,
        eps_neg=profile.eps_neg if new_eps_neg is None else new_eps_neg,
        eps_pos=profile.eps_pos if new_eps_pos is None else new_eps_pos,
        threshold_basis_ref=threshold_basis_ref,
        status=STATUS_PROPOSED,
    )
    result = approve_profile(new_profile, approval_ref=approval_ref, approver=approver)
    if not result["ok"]:
        return result
    superseded_record = _clone_with(profile, status=STATUS_SUPERSEDED)
    return {"ok": True, "old": superseded_record, "new": result["profile"],
            "note": "v%s superseded by v%s; historical receipts keep v%s"
                    % (old_version, new_version, old_version)}


def _bump_version(v):
    try:
        parts = [int(p) for p in str(v).split(".")]
    except ValueError:
        return str(v) + ".1"
    parts[-1] += 1
    return ".".join(str(p) for p in parts)


# ---------------------------------------------------------------------------
# Classification — the mathematical rule (equivalence-style)
# ---------------------------------------------------------------------------
def _interval_rule(interval, eps_neg, eps_pos):
    """L > +eps_pos -> positive; U < -eps_neg -> negative;
    [-eps_neg, +eps_pos] contains [L, U] -> neutral; else inconclusive."""
    L, U = float(interval[0]), float(interval[1])
    if L > eps_pos:
        return MEANINGFUL_POSITIVE
    if U < -eps_neg:
        return MEANINGFUL_NEGATIVE
    if L >= -eps_neg and U <= eps_pos:
        return PRACTICALLY_NEUTRAL
    return INCONCLUSIVE


def classify_effect(*, profile, interval, estimate=None,
                    subgroups=(), cumulative=None,
                    hard_gates_pass=True, hard_gate_refusals=(),
                    observation_window_complete=True,
                    evidence_adequate=True, instrument_detection_limit=None,
                    family_qualified=True):
    """Classify one measured effect against a governed neutrality profile.

    subgroups: iterable of {"population", "interval", "estimate"} — each
      independently assessed against the same zone (no aggregate laundering).
    cumulative: {"per_event": (L, U), "repetitions": n, "limit": x} or None.
    Returns {"verdict", "refusals", "reasons", "subgroup_verdicts"}.
    A refusal is never silent: the verdict falls back to the honest state and
    the refusal code names exactly what was missing.
    """
    refusals = []
    reasons = []
    subgroup_verdicts = []

    # P0: the profile must be approved and its spec complete.
    if profile.status != STATUS_APPROVED:
        return {"verdict": INCONCLUSIVE, "refusals": [PROFILE_NOT_APPROVED],
                "reasons": ["neutrality requires a preapproved profile; "
                            "status is %s" % profile.status],
                "subgroup_verdicts": []}
    spec = validate_profile_spec(profile)
    if not spec["ok"]:
        return {"verdict": INCONCLUSIVE, "refusals": [spec["refusal"]],
                "reasons": spec["problems"], "subgroup_verdicts": []}

    # P1: hard boundaries first — no tolerance overrides a prohibition.
    if not hard_gates_pass:
        return {"verdict": INCONCLUSIVE,
                "refusals": [HARD_BOUNDARY_OVERRIDE_REFUSED],
                "reasons": ["hard gate failed (%s): no neutral tolerance "
                            "overrides a prohibition, rights violation, consent "
                            "requirement, or approved risk limit"
                            % ",".join(hard_gate_refusals or ("unspecified",))],
                "subgroup_verdicts": []}

    # P4: delayed-harm provisionality — the window decides, not the estimate.
    if not observation_window_complete:
        return {"verdict": PROVISIONAL,
                "refusals": [DELAYED_HARM_PROVISIONAL],
                "reasons": ["material observation window open: result stays "
                            "provisional until the qualified window closes"],
                "subgroup_verdicts": []}

    # P7-equivalent: the instrument must resolve the zone it judges.
    det = (profile.instrument_detection_limit
           if instrument_detection_limit is None else instrument_detection_limit)
    if det is not None and det >= min(profile.eps_neg, profile.eps_pos):
        return {"verdict": INCONCLUSIVE,
                "refusals": [NEEDS_EVIDENCE, INSTRUMENT_INADEQUATE],
                "reasons": ["instrument cannot detect the smallest meaningful "
                            "effect: NEEDS_EVIDENCE, not neutral"],
                "subgroup_verdicts": []}
    if not evidence_adequate:
        return {"verdict": INCONCLUSIVE, "refusals": [NEEDS_EVIDENCE],
                "reasons": ["measurement not sufficiently precise to "
                            "distinguish neutrality from uncertainty"],
                "subgroup_verdicts": []}

    # Interval must be a sane [L, U] pair.
    try:
        L, U = float(interval[0]), float(interval[1])
    except (TypeError, ValueError, IndexError):
        return {"verdict": INCONCLUSIVE, "refusals": [INTERVAL_NOT_QUALIFIED],
                "reasons": ["interval must be a [L, U] pair of numbers"],
                "subgroup_verdicts": []}
    if L > U:
        return {"verdict": INCONCLUSIVE, "refusals": [INTERVAL_NOT_QUALIFIED],
                "reasons": ["interval lower bound exceeds upper bound"],
                "subgroup_verdicts": []}

    # The requirements checklist: neutrality needs every one of them.
    unmet = [k for k, v in profile.requirements.items() if not v]
    # hard_gates_pass and observation_window_complete were already enforced
    # above; the rest gate the neutral verdict here.
    unmet_neutral_gates = [k for k in unmet
                           if k not in ("hard_gates_pass", "observation_window_complete")]

    # P2: no aggregate laundering — assess each subgroup independently.
    overall = _interval_rule((L, U), profile.eps_neg, profile.eps_pos)
    for sg in subgroups:
        sg_interval = sg["interval"]
        sg_verdict = _interval_rule(sg_interval, profile.eps_neg, profile.eps_pos)
        subgroup_verdicts.append({"population": sg["population"],
                                  "verdict": sg_verdict,
                                  "interval": [float(sg_interval[0]), float(sg_interval[1])]})
        if sg_verdict == MEANINGFUL_NEGATIVE and overall in (
                PRACTICALLY_NEUTRAL, INCONCLUSIVE):
            refusals.append(AGGREGATE_LAUNDERING_REFUSED)
            reasons.append(
                "subgroup '%s' shows meaningful harm %s while the aggregate "
                "reads %s: the overall neutrality claim is REJECTED — do not "
                "average the harm away; corrective investigation required"
                % (sg["population"], sg_interval, overall))

    # P3: no cumulative laundering — per-event AND cumulative over the horizon.
    if cumulative is not None:
        cL, cU = (float(cumulative["per_event"][0]) * cumulative["repetitions"],
                  float(cumulative["per_event"][1]) * cumulative["repetitions"])
        limit = (profile.cumulative_limit if cumulative.get("limit") is None
                 else float(cumulative["limit"]))
        if limit is not None and cU < 0 and abs(cL) > limit:
            refusals.append(CUMULATIVE_HARM_EXCEEDS_LIMIT)
            reasons.append(
                "cumulative effect [%s, %s] %s over %s repetitions exceeds the "
                "approved cumulative limit %s: report cumulative harm"
                % (cL, cU, profile.unit, cumulative["repetitions"], limit))

    if refusals:
        return {"verdict": INCONCLUSIVE, "refusals": refusals,
                "reasons": reasons, "subgroup_verdicts": subgroup_verdicts}

    if unmet_neutral_gates:
        return {"verdict": INCONCLUSIVE,
                "refusals": [NEUTRAL_REQUIREMENTS_UNMET],
                "reasons": ["neutrality requirements unmet: %s"
                            % ",".join(unmet_neutral_gates)],
                "subgroup_verdicts": subgroup_verdicts}

    if overall == PRACTICALLY_NEUTRAL:
        reasons.append(
            "entire justified interval [%s, %s] inside the approved zone "
            "[-%s, +%s] %s, all requirements met: practically neutral "
            "(not exact zero, not safe-by-default)"
            % (L, U, profile.eps_neg, profile.eps_pos, profile.unit))
        # Interop: in the symmetric case the zero law's interval rule must
        # agree — this profile is the governed machinery behind its
        # "declared, versioned epsilon". A mismatch is a construction error.
        if profile.eps_neg == profile.eps_pos:
            cross = zvl.classify_zero(
                assessment_state="ASSESSED",
                interval=(L, U),
                epsilon={"value": profile.eps_pos,
                         "version": "%s@%s" % (profile.profile_id, profile.version),
                         "justification": profile.threshold_basis_ref},
                evidence_refs=("neutrality-profile:%s@%s"
                               % (profile.profile_id, profile.version),),
            )
            if cross["interpretation"] != zvl.PRACTICALLY_NEUTRAL:
                return {"verdict": INCONCLUSIVE,
                        "refusals": ["ZERO_LAW_CROSSCHECK_MISMATCH"],
                        "reasons": reasons + [
                            "symmetric-case cross-check against zero_value_law "
                            "disagreed (%s): refusing rather than emitting a "
                            "divergent neutral verdict" % cross["interpretation"]],
                        "subgroup_verdicts": subgroup_verdicts}
            reasons.append("cross-checked against zero_value_law: agreement")
    elif overall == INCONCLUSIVE:
        reasons.append("a wide interval centered on zero is not evidence of "
                       "neutrality: inconclusive")
    return {"verdict": overall, "refusals": [], "reasons": reasons,
            "subgroup_verdicts": subgroup_verdicts}


def assess_family(*, profile, measurements, family_qualified):
    """Repeated testing must not manufacture false neutrality or significance.

    measurements: iterable of {"name", "interval"}. Without a qualified
    family-wise claim method, each claim is assessed individually and NO
    family-level neutrality claim is permitted.
    """
    results = [classify_effect(profile=profile, interval=m["interval"])
               for m in measurements]
    if not family_qualified:
        return {"family_verdict": None,
                "refusals": [FAMILY_CLAIM_UNQUALIFIED],
                "reasons": ["%d claims assessed without a qualified family-wise "
                            "method: individual verdicts stand, no family-level "
                            "neutrality claim permitted" % len(measurements)],
                "individual": results}
    verdicts = {r["verdict"] for r in results}
    family = (PRACTICALLY_NEUTRAL if verdicts == {PRACTICALLY_NEUTRAL}
              else INCONCLUSIVE if INCONCLUSIVE in verdicts or PROVISIONAL in verdicts
              else MEANINGFUL_NEGATIVE if MEANINGFUL_NEGATIVE in verdicts
              else MEANINGFUL_POSITIVE)
    return {"family_verdict": family, "refusals": [],
            "reasons": ["family-wise method qualified; combined verdict %s" % family],
            "individual": results}


def reclassify_historical(receipt, current_profile):
    """Thresholds are approved BEFORE outcome review. Historical receipts keep
    their original thresholds: silently re-running an old result under a new,
    wider tolerance is refused. A genuine re-review needs a new receipt, new
    evidence, and the new profile version recorded — never a quiet rewrite."""
    recorded = (receipt.get("neutrality_profile_version")
                or receipt.get("profile_version"))
    if recorded != "%s@%s" % (current_profile.profile_id, current_profile.version):
        return {"ok": False, "refusal": THRESHOLD_MANIPULATION_REFUSED,
                "reasons": ["receipt recorded under %s; current profile is %s@%s: "
                            "retroactive reclassification refused. Open a new "
                            "review with new evidence under the new version."
                            % (recorded, current_profile.profile_id,
                               current_profile.version)]}
    return {"ok": True, "refusal": None,
            "reasons": ["receipt and profile versions match; reclassification "
                        "permitted under the originally approved tolerance"]}


# What this does NOT claim: this module judges classifications it is given; it
# does not perform measurements, fit uncertainty intervals, or verify evidence
# itself. A PRACTICALLY_NEUTRAL verdict is only as good as the justified
# interval, the approved profile, and the independence of the reviewer.
# The law is PROPOSED — nothing here is ratified until Shawn ratifies it.

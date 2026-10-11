"""conflict_escalation.py — Law 11: genuine trade-offs go to human governance (T-08).

Per Naya 1's "Human Escalation Rule" (2026-10-11): when every option harms
someone, Naya must not invent permission via aggregate math. And per the
repo's decision-compression doctrine: "Escalate only the smallest remaining
human decision" — the packet carries problem, options, consequences,
evidence, unknowns, recommendation, and the exact authorization requested.

This module is the mechanism for that doctrine. It compares candidate
OPTIONS against each other on per-group harm profiles (T-05's HarmProfile —
structured ordinals, never collapsed to a number):

  1. Compare all options vs the baseline ("doing nothing" is always an
     option; the caller supplies its assessed profile — never an assumed
     neutral).
  2. Eliminate rights/hard-harm violations (catastrophic, or
     major+irreversible, in any single group). No override exists.
  2b. Hold omitting options: a group assessed by one option but omitted by
     another is a modeling inconsistency — the omitting option is held for
     evidence (OMISSION_INCONSISTENCY), never silently assumed negligible.
     Winning by "forgetting" a harmed group is fail-open, so it is
     refused here.
  3. Prefer Pareto: ordinal dominance only — no-worse on every
     group x dimension, strictly better on at least one. No sums, no means,
     no weights, no invented exchange rates between groups.
  4. Redesign/mitigate is the caller's attested attempt, recorded here.
  5. Escalate the material ethical choice: when the Pareto front holds two
     or more options that genuinely differ, the machine does NOT pick.
     It emits a visible EscalationReceipt naming who bears what cost, and
     returns ESCALATE_TO_HUMAN.

Verdict mapping to Naya 1's five-way routing:
  PROCEED           -> ACT   (no genuine conflict; one admissible winner)
  ESCALATE_TO_HUMAN -> ASK   (genuine trade-off; human governance decides)
  REFUSE_ALL        -> REFUSE (every option violates rights/hard harm)
  NEEDS_EVIDENCE    -> READ_MORE (unknowns block selection; gather evidence)

This is a hard-gate consult in Law 11's layer — the same layer as
law11_gate — not a second value decision engine. When it PROCEEDs, the
canonical value calculus still makes the value selection among admissible
options; this consult only constrains (eliminates violators, forces
escalation on genuine conflicts).
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Mapping, Sequence

from kernel.protocol import harm_profile as _hp

# ---------------------------------------------------------------------------
# Verdicts
# ---------------------------------------------------------------------------

PROCEED = "PROCEED"
ESCALATE_TO_HUMAN = "ESCALATE_TO_HUMAN"
REFUSE_ALL = "REFUSE_ALL"
NEEDS_EVIDENCE = "NEEDS_EVIDENCE"
VERDICTS = (PROCEED, ESCALATE_TO_HUMAN, REFUSE_ALL, NEEDS_EVIDENCE)

# Assumed harm for a group an option's profile does not assess. Used ONLY by
# the standalone pareto_front() helper. consult_conflicts() NO LONGER
# tolerates omissions: an option that omits a group assessed by another
# option is held for evidence (OMISSION_INCONSISTENCY) — winning by
# "forgetting" a harmed group was a fail-open dodge. The assumption is
# RECORDED on pareto_front()'s path, never silent. Unknown DIMENSIONS
# inside an assessed group still fail closed per T-05 — that rule is
# untouched.
_ASSUMED_GROUP_HARM_KWARGS = {
    "severity": _hp.SEVERITY_NEGLIGIBLE,
    "reversibility": _hp.REV_FULLY,
    "timing": _hp.TIME_IMMEDIATE,
    "measurability": _hp.MEAS_MEASURED,
    "distribution": _hp.DIST_SINGLE,
}


# ---------------------------------------------------------------------------
# Receipt
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class OptionAssessment:
    """What the consult found for one option."""
    option: str
    judgment_blocks: bool
    judgment_needs_evidence: bool
    block_reasons: tuple[str, ...] = ()
    evidence_reasons: tuple[str, ...] = ()
    profile_digest: str = ""
    assumed_groups: tuple[str, ...] = ()


@dataclass(frozen=True)
class EscalationReceipt:
    """Visible record of a conflict-escalation consult.

    Immutable. receipt_id is the sha256 of the canonical serialization —
    deterministic (same inputs -> same id) and bindable as a Law 12 proof
    dependency digest. "Visible" means: returned to the caller, carried as
    evidence on pipeline receipts, and renderable in plain words.
    """
    receipt_id: str
    decided_at: str
    assessed_by: str
    verdict: str
    chosen_option: str | None
    baseline_option: str
    options: tuple[str, ...]
    assessments: tuple[OptionAssessment, ...]
    eliminated: tuple[tuple[str, str], ...]  # (option, reason)
    evidence_pending: tuple[str, ...]
    pareto_front: tuple[str, ...]
    # Per front option: which groups bear non-negligible harm. The "who bears
    # the cost" record — a trade-off is never a silent cost-bearing choice.
    # Structured tuples, not display text: (group_id, severity,
    # reversibility, timing). render() formats for display; consumers must
    # not parse strings.
    cost_bearers: tuple[tuple[str, tuple[tuple[str, str, str, str], ...]], ...]
    assumed_negligible: tuple[tuple[str, str], ...]  # (option, group)
    redesign_notes: tuple[str, ...]
    redesign_attempted: bool
    human_decision_requested: str
    profile_digests: tuple[tuple[str, str], ...]  # (option, digest)

    def render(self) -> str:
        """Plain-words rendering. IN A NUTSHELL first, detail below."""
        lines = []
        if self.verdict == ESCALATE_TO_HUMAN:
            lines.append(
                "IN A NUTSHELL: no option is clearly safe — each remaining "
                f"option harms someone the others spare. A human must choose: "
                f"{self.human_decision_requested}"
            )
        elif self.verdict == PROCEED:
            lines.append(
                "IN A NUTSHELL: no genuine conflict — "
                f"{self.chosen_option!r} is no-worse for every assessed group, "
                "so it proceeds without human escalation."
            )
        elif self.verdict == REFUSE_ALL:
            lines.append(
                "IN A NUTSHELL: every option violates a hard harm boundary. "
                "Nothing is admissible — refused, not escalated."
            )
        else:
            lines.append(
                "IN A NUTSHELL: too much is unknown to choose safely. "
                "Evidence first, decision after."
            )
        lines.append(f"Verdict: {self.verdict}")
        if self.chosen_option:
            lines.append(f"Chosen: {self.chosen_option}")
        lines.append(f"Baseline (do-nothing) option: {self.baseline_option}")
        lines.append(f"Options considered: {', '.join(self.options)}")
        if self.eliminated:
            lines.append("Eliminated (hard-harm violations):")
            for opt, reason in self.eliminated:
                lines.append(f"  - {opt}: {reason}")
        if self.evidence_pending:
            lines.append(
                "Held for evidence (unknown dimensions — not safe to select): "
                + ", ".join(self.evidence_pending)
            )
        lines.append(f"Pareto front: {', '.join(self.pareto_front) or '(empty)'}")
        if self.cost_bearers:
            lines.append("Who bears the cost (non-negligible harm per option):")
            for opt, bearers in self.cost_bearers:
                rendered = ", ".join(
                    f"{gid}(severity={sev},reversibility={rev},timing={timing})"
                    for gid, sev, rev, timing in bearers
                )
                lines.append(f"  - {opt}: {rendered or '(none assessed)'}")
        if self.assumed_negligible:
            lines.append("Assumed-negligible (group not assessed for that option):")
            for opt, grp in self.assumed_negligible:
                lines.append(f"  - {opt} / {grp}")
        if self.redesign_attempted:
            lines.append("Redesign/mitigation attempted:")
            for note in self.redesign_notes:
                lines.append(f"  - {note}")
        else:
            lines.append("Redesign/mitigation: none attested by the caller.")
        lines.append(f"Receipt: {self.receipt_id}")
        return "\n".join(lines)


@dataclass(frozen=True)
class ConflictResolution:
    """Outcome of consult_conflicts()."""
    verdict: str
    chosen_option: str | None
    receipt: EscalationReceipt

    def __post_init__(self) -> None:
        if self.verdict not in VERDICTS:
            raise ValueError(f"unknown conflict verdict: {self.verdict!r}")


# ---------------------------------------------------------------------------
# Ordinal Pareto machinery (no arithmetic on harm — dominance only)
# ---------------------------------------------------------------------------

def _normalized_groups(
    options: Mapping[str, _hp.HarmProfile],
) -> tuple[tuple[str, ...], dict[str, dict[str, _hp.GroupHarm]], tuple[tuple[str, str], ...]]:
    """Normalize all option profiles onto the union of group_ids.

    Returns (all_groups, per-option group map, assumed list). Groups absent
    from an option's profile are filled with the assumed-negligible harm and
    recorded — the assumption is visible on the receipt, never silent.
    """
    all_groups = tuple(
        sorted({g.group_id for p in options.values() for g in p.groups})
    )
    per_option: dict[str, dict[str, _hp.GroupHarm]] = {}
    assumed: list[tuple[str, str]] = []
    for name, profile in options.items():
        by_id = {g.group_id: g for g in profile.groups}
        filled: dict[str, _hp.GroupHarm] = {}
        for gid in all_groups:
            if gid in by_id:
                filled[gid] = by_id[gid]
            else:
                filled[gid] = _hp.GroupHarm(
                    group_id=gid,
                    note="ASSUMED-NEGLIGIBLE: caller did not assess this group "
                         f"for option {name!r}; treated as unaffected",
                    **_ASSUMED_GROUP_HARM_KWARGS,  # type: ignore[arg-type]
                )
                assumed.append((name, gid))
        per_option[name] = filled
    return all_groups, per_option, tuple(assumed)


def _dominates(
    a: Mapping[str, _hp.GroupHarm],
    b: Mapping[str, _hp.GroupHarm],
    groups: Sequence[str],
) -> bool:
    """True iff option-profile `a` Pareto-dominates `b` on harm ordinals.

    No-worse on every group x dimension, strictly better on at least one.
    Lower rank = less harm. This is the ONLY cross-option math permitted:
    dominance, never sums/means/weights. Incomparability (neither dominates)
    is a valid outcome, not a failure.
    """
    strictly_better = False
    for gid in groups:
        ga, gb = a[gid], b[gid]
        for dim in _hp.DIMENSIONS:
            ra = _hp.dimension_rank(dim, getattr(ga, dim))
            rb = _hp.dimension_rank(dim, getattr(gb, dim))
            if ra > rb:
                return False  # worse somewhere -> no dominance
            if ra < rb:
                strictly_better = True
    return strictly_better


def _front_from_normalized(
    names: Sequence[str],
    per_option: Mapping[str, Mapping[str, _hp.GroupHarm]],
    groups: Sequence[str],
) -> tuple[str, ...]:
    """Non-dominated names from already-normalized group maps."""
    front: list[str] = []
    for name in names:
        dominated = any(
            other != name and _dominates(per_option[other], per_option[name], groups)
            for other in names
        )
        if not dominated:
            front.append(name)
    return tuple(front)


def pareto_front(
    options: Mapping[str, _hp.HarmProfile],
) -> tuple[str, ...]:
    """Names of the non-dominated options (ordinal harm Pareto front).

    Deterministic order: input order. Every option on the front is
    non-dominated; every option off it is dominated by at least one
    front member. A singleton front is a genuine "no conflict" signal.
    """
    names = list(options)
    groups, per_option, _ = _normalized_groups(options)
    return _front_from_normalized(names, per_option, groups)


# ---------------------------------------------------------------------------
# The consult
# ---------------------------------------------------------------------------

def _receipt_id(canonical: dict) -> str:
    return hashlib.sha256(
        json.dumps(canonical, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def consult_conflicts(
    options: Mapping[str, _hp.HarmProfile],
    *,
    baseline_option: str,
    redesign_notes: Sequence[str] = (),
    assessed_by: str = "unspecified-caller",
    decided_at: str | None = None,
) -> ConflictResolution:
    """Run the conflict-escalation consult over candidate options.

    options: option name -> assessed HarmProfile. Must include
        `baseline_option`: the caller-assessed "do nothing" profile. The
        baseline is never assumed neutral — an unassessed baseline is a
        caller error (ValueError), not a silent zero.
    redesign_notes: caller-attested redesign/mitigation attempts. Recorded
        verbatim; the consult does not judge their quality.

    Returns ConflictResolution(verdict, chosen_option, receipt). The receipt
    is the visible record: every elimination, every held option, the Pareto
    front, who bears what cost, and the exact human decision requested.
    """
    if not options:
        raise ValueError("consult_conflicts requires at least one option")
    if baseline_option not in options:
        raise ValueError(
            f"baseline_option {baseline_option!r} is not among the assessed "
            "options — the 'do nothing' profile must be assessed, never assumed"
        )
    # A blank assessor is not a missing assessor: name it explicitly so the
    # receipt never carries an anonymous human-governance request.
    assessed_by = assessed_by or "unspecified-caller"
    for name, profile in options.items():
        if not isinstance(profile, _hp.HarmProfile):
            raise ValueError(
                f"option {name!r} is not a HarmProfile "
                f"(got {type(profile).__name__})"
            )

    names = tuple(options)
    decided = decided_at or datetime.now(timezone.utc).isoformat()

    # --- Step 1+2: judge each profile; eliminate violators, hold unknowns.
    assessments: list[OptionAssessment] = []
    eliminated: list[tuple[str, str]] = []
    evidence_pending: list[str] = []
    admissible: dict[str, _hp.HarmProfile] = {}
    for name in names:
        profile = options[name]
        judgment = _hp.judge(profile)
        assessments.append(
            OptionAssessment(
                option=name,
                judgment_blocks=judgment.blocks,
                judgment_needs_evidence=judgment.needs_evidence,
                block_reasons=judgment.block_reasons,
                evidence_reasons=judgment.evidence_reasons,
                profile_digest=_hp.profile_digest(profile),
            )
        )
        if judgment.blocks:
            eliminated.append(
                (name, "; ".join(judgment.block_reasons) or "blocking harm")
            )
        elif judgment.needs_evidence:
            # Unknown is not safe: held out of selection, recorded separately.
            evidence_pending.append(name)
        else:
            admissible[name] = profile

    # --- Step 2b: omission-inconsistency hold (fail-closed on the dodge).
    # A group assessed by at least one option but omitted by another is a
    # modeling inconsistency the machine cannot resolve: the omitting
    # option is held for evidence and the inconsistency is named on the
    # receipt. An option may not win by "forgetting" a group another
    # option honestly assesses — the old assumed-negligible fill was
    # fail-open here, so it is refused instead.
    if admissible:
        assessed_union = {
            g.group_id for profile in admissible.values() for g in profile.groups
        }
        omission_holds: dict[str, tuple[str, ...]] = {}
        for name, profile in admissible.items():
            own = {g.group_id for g in profile.groups}
            omitted = tuple(sorted(assessed_union - own))
            if omitted:
                omission_holds[name] = omitted
        for name, omitted in omission_holds.items():
            assessments = [
                OptionAssessment(
                    option=a.option,
                    judgment_blocks=a.judgment_blocks,
                    judgment_needs_evidence=True,
                    block_reasons=a.block_reasons,
                    evidence_reasons=a.evidence_reasons
                    + (
                        f"OMISSION_INCONSISTENCY:{name} omits groups assessed "
                        f"by other options: {', '.join(omitted)}",
                    ),
                    profile_digest=a.profile_digest,
                    assumed_groups=a.assumed_groups,
                )
                if a.option == name
                else a
                for a in assessments
            ]
            del admissible[name]
            evidence_pending.append(name)

    def build_receipt(
        verdict: str,
        chosen: str | None,
        front: tuple[str, ...],
        cost_bearers: tuple[tuple[str, tuple[str, ...]], ...],
        assumed: tuple[tuple[str, str], ...],
        human_question: str,
    ) -> EscalationReceipt:
        canonical = {
            "verdict": verdict,
            "chosen_option": chosen,
            "baseline_option": baseline_option,
            "options": list(names),
            "assessments": [
                {
                    "option": a.option,
                    "blocks": a.judgment_blocks,
                    "needs_evidence": a.judgment_needs_evidence,
                    "block_reasons": list(a.block_reasons),
                    "evidence_reasons": list(a.evidence_reasons),
                    "profile_digest": a.profile_digest,
                }
                for a in assessments
            ],
            "eliminated": [list(e) for e in eliminated],
            "evidence_pending": list(evidence_pending),
            "pareto_front": list(front),
            "cost_bearers": [
                [o, [list(entry) for entry in bearers]]
                for o, bearers in cost_bearers
            ],
            "assumed_negligible": [list(x) for x in assumed],
            "redesign_notes": list(redesign_notes),
            "human_decision_requested": human_question,
            "decided_at": decided,
            "assessed_by": assessed_by,
        }
        return EscalationReceipt(
            receipt_id=_receipt_id(canonical),
            decided_at=decided,
            assessed_by=assessed_by,
            verdict=verdict,
            chosen_option=chosen,
            baseline_option=baseline_option,
            options=names,
            assessments=tuple(assessments),
            eliminated=tuple(eliminated),
            evidence_pending=tuple(evidence_pending),
            pareto_front=front,
            cost_bearers=cost_bearers,
            assumed_negligible=assumed,
            redesign_notes=tuple(redesign_notes),
            redesign_attempted=bool(redesign_notes),
            human_decision_requested=human_question,
            profile_digests=tuple(
                (a.option, a.profile_digest) for a in assessments
            ),
        )

    # --- Step 3: resolve.
    if not admissible:
        if eliminated:
            question = (
                "Every option violates a hard harm boundary "
                f"({len(eliminated)} eliminated). No admissible action exists — "
                "confirm refusal, or supply a new option with an assessed profile."
            )
            verdict, chosen = REFUSE_ALL, None
        else:
            question = (
                "Every option has unqualified harm dimensions "
                f"({len(evidence_pending)} held). Gather the missing evidence, "
                "then re-run the consult — unknowns are not decided here."
            )
            verdict, chosen = NEEDS_EVIDENCE, None
        receipt = build_receipt(verdict, chosen, (), (), (), question)
        return ConflictResolution(verdict=verdict, chosen_option=chosen, receipt=receipt)

    # Admissible options exist: Pareto round (baseline included).
    all_groups, per_option, assumed = _normalized_groups(admissible)
    front = _front_from_normalized(list(admissible), per_option, all_groups)

    def _harm_shape(name: str) -> tuple:
        """Normalized harm content: group x dimension ordinals only.

        Assessed_by/at don't change who is harmed, so they don't count
        toward distinctness — harm-identical options are one shape.
        """
        return tuple(
            (gid, tuple(
                _hp.dimension_rank(dim, getattr(per_option[name][gid], dim))
                for dim in _hp.DIMENSIONS
            ))
            for gid in all_groups
        )

    distinct_shapes = {}
    for _name in front:
        distinct_shapes.setdefault(_harm_shape(_name), _name)

    def harmed_groups(name: str) -> tuple[tuple[str, str, str, str], ...]:
        """Groups bearing non-negligible harm under this option.

        Structured (group_id, severity, reversibility, timing) tuples —
        display formatting happens in render(), never here.
        """
        out = []
        for gid in all_groups:
            g = per_option[name][gid]
            if g.severity != _hp.SEVERITY_NEGLIGIBLE:
                out.append((gid, g.severity, g.reversibility, g.timing))
        return tuple(out)

    cost_bearers = tuple((name, harmed_groups(name)) for name in front)

    if len(distinct_shapes) == 1:
        # No genuine conflict: every front option carries the same harm
        # shape (harm-identical options are not a trade-off). The first
        # front member proceeds; the value calculus still makes the value
        # selection downstream.
        chosen = front[0]
        receipt = build_receipt(PROCEED, chosen, front, cost_bearers, assumed, "")
        return ConflictResolution(
            verdict=PROCEED, chosen_option=chosen, receipt=receipt
        )

    # Genuine conflict: the front holds options that differ, so each spares
    # some group another harms. The machine does not pick — it escalates with
    # the full record. This is the "never silent cost-bearing" guarantee.
    def _fmt_bearer(entry: tuple[str, str, str, str]) -> str:
        gid, sev, rev, timing = entry
        return f"{gid}(severity={sev},reversibility={rev},timing={timing})"

    trade_lines = "; ".join(
        f"{name} harms [{', '.join(_fmt_bearer(e) for e in bearers) or 'none assessed'}]"
        for name, bearers in cost_bearers
    )
    question = (
        f"Genuine harm trade-off among {len(front)} admissible options "
        f"({', '.join(front)}). {trade_lines}. "
        + (
            "Redesign/mitigation was attempted — see receipt — and no "
            "Pareto-dominant option remains. "
            if redesign_notes
            else "No redesign/mitigation was attested. "
        )
        + "Which cost should be borne, and by whom? Human governance decides; "
        "the machine takes no option until then."
    )
    receipt = build_receipt(
        ESCALATE_TO_HUMAN, None, front, cost_bearers, assumed, question
    )
    return ConflictResolution(
        verdict=ESCALATE_TO_HUMAN, chosen_option=None, receipt=receipt
    )

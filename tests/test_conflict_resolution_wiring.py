"""
test_conflict_resolution_wiring.py — proves the Conflict Resolution Engine
is actually WIRED into act_pipeline.plan_action, not just a standalone library.

The Law 11 lesson: "a correct door with no hallway." This test proves the
hallway exists: a candidate with a worsening impact matrix is excluded from
selection even if it would otherwise win on value.
"""
import time

import pytest

from kernel.act_pipeline import (
    PlanCandidate,
    LawAuthority,
    plan_action,
)
from kernel.protocol.conflict_resolution import (
    AffectedGroup,
    OutcomeCell,
    HarmProfile,
    ImpactMatrix,
    OBS_COMPLETE,
)
from kernel.value_calculus import QualityProfile, RiskPolicy


def _make_authority():
    return LawAuthority(
        action="test_action",
        scope="test_action",
        decided_at=time.time(),
        expires_at=time.time() + 3600,
        grant_id="test-grant-1",
    )


def _make_candidate(cid, matrix=None):
    return PlanCandidate(
        candidate_id=cid,
        action="test_action",
        description=f"candidate {cid}",
        quality={"speed": 9.0},
        confidence={"speed": 0.9},
        reversibility="REVERSIBLE",
        expected_outcome="improved",
        proof_requirements=("evidence",),
        impact_matrix=matrix,
        rights_safe=True,
        safety_safe=True,
        privacy_safe=True,
    )


def _worsening_matrix():
    """Fast-only design: huge speed win, devastating accessibility loss."""
    m = ImpactMatrix(action_id="fast-only")
    m.add_cell(OutcomeCell(
        group_id="main_users", dimension="speed", horizon="immediate",
        unit="points", baseline_value=0.0, action_value=5.0,
        lower_bound=4.0, upper_bound=6.0, tolerance=0.0,
        evidence_quality="adequate", observation_status=OBS_COMPLETE,
    ))
    m.add_cell(OutcomeCell(
        group_id="screen_reader_users", dimension="accessibility",
        horizon="immediate", unit="points",
        baseline_value=0.0, action_value=-8.0,
        lower_bound=-9.0, upper_bound=-7.0, tolerance=0.0,
        evidence_quality="adequate", observation_status=OBS_COMPLETE,
    ))
    for g in ("main_users", "screen_reader_users"):
        m.harm_profiles.append(HarmProfile(
            group_id=g, severity="substantial", probability="high",
            irreversibility="conditional", timing="immediate",
            uncertainty="low", exposure="all users",
        ))
    return m


def _clean_matrix():
    """Adaptive design: speed win, no accessibility loss."""
    m = ImpactMatrix(action_id="adaptive")
    m.add_cell(OutcomeCell(
        group_id="main_users", dimension="speed", horizon="immediate",
        unit="points", baseline_value=0.0, action_value=4.0,
        lower_bound=3.0, upper_bound=5.0, tolerance=0.0,
        evidence_quality="adequate", observation_status=OBS_COMPLETE,
    ))
    m.add_cell(OutcomeCell(
        group_id="screen_reader_users", dimension="accessibility",
        horizon="immediate", unit="points",
        baseline_value=0.0, action_value=0.5,
        lower_bound=0.0, upper_bound=1.0, tolerance=0.0,
        evidence_quality="adequate", observation_status=OBS_COMPLETE,
    ))
    for g in ("main_users", "screen_reader_users"):
        m.harm_profiles.append(HarmProfile(
            group_id=g, severity="inconvenience", probability="low",
            irreversibility="REVERSIBLE", timing="immediate",
            uncertainty="low", exposure="all users",
        ))
    return m


class TestPipelineWiring:
    def test_worsening_candidate_excluded_from_plan(self):
        """A candidate that fails no-worse-off is excluded even with high quality."""
        bad = _make_candidate("bad", _worsening_matrix())
        good = _make_candidate("good", _clean_matrix())
        # Give the bad candidate HIGHER quality so it would win on value alone.
        bad = PlanCandidate(
            candidate_id="bad", action="test_action",
            description="bad but fast", quality={"speed": 10.0},
            confidence={"speed": 0.99}, reversibility="REVERSIBLE",
            expected_outcome="improved", proof_requirements=("evidence",),
            impact_matrix=_worsening_matrix(),
            rights_safe=True, safety_safe=True, privacy_safe=True,
        )
        authority = _make_authority()
        profile = QualityProfile(profile_id="cr-test", version="1", objective="test")
        plan, receipt = plan_action(
            authority, [bad, good], profile, now=time.time(),
        )
        # The bad candidate must NOT win. Either good wins or plan refused.
        if plan is not None:
            assert plan.chosen.candidate_id == "good", (
                f"Worsening candidate won: {plan.chosen.candidate_id}. "
                "Conflict Resolution is not wired."
            )
        # Receipt must mention Conflict Resolution.
        evidence_text = " ".join(receipt.evidence)
        assert "Conflict Resolution" in evidence_text, (
            f"Receipt does not mention Conflict Resolution: {receipt.evidence}"
        )

    def test_all_worsening_plan_refused(self):
        """If all candidates with matrices fail, the plan is refused."""
        bad1 = _make_candidate("bad1", _worsening_matrix())
        bad2 = _make_candidate("bad2", _worsening_matrix())
        authority = _make_authority()
        profile = QualityProfile(profile_id="cr-test", version="1", objective="test")
        plan, receipt = plan_action(
            authority, [bad1, bad2], profile, now=time.time(),
        )
        assert plan is None
        assert receipt.phase == "PLAN_REFUSED"

    def test_candidate_without_matrix_unaffected(self):
        """Candidates without a matrix skip the phase (backward compatible)."""
        plain = _make_candidate("plain", None)
        authority = _make_authority()
        profile = QualityProfile(profile_id="cr-test", version="1", objective="test")
        plan, receipt = plan_action(
            authority, [plain], profile, now=time.time(),
        )
        # Should not be refused due to Conflict Resolution.
        # (May be refused for other reasons, but not CR.)
        if plan is None:
            evidence_text = " ".join(receipt.evidence)
            assert "Conflict Resolution" not in evidence_text or "matrices" in evidence_text

"""D36 supplementary proof — the exact sharpest case end-to-end.

D36's implementation lives on main as drift_canary/revocation_linearization.py
(11,989 lines, 48/48 tests green), built by the verification lane. This file
adds NO new machinery. It proves D36's sharpest case as one continuous
sequence against that existing implementation:

  T1: claim validated VALID.
  T2: E1 revoked (R commits).
  T3: action authorized by the T1 validation attempts to execute -> REJECTED.
      The T1 validation is dead.
  T4: independent E2 arrives.
  T5: claim requalifies on E2.
  T6: the same action, re-authorized on fresh validation -> EXECUTED.

Plus: R<P — a publication built pre-R is rejected post-R even though it was
valid when built; and the fence is synchronous (no stale-certification window
at the commit tick).
"""

import pytest

from ..revocation_linearization import (
    CURRENT_QUALIFIED,
    CURRENT_UNQUALIFIED,
    STALE_DEPENDENCY,
)


def fresh_state():
    from ..revocation_linearization import AuthoritativeState
    st = AuthoritativeState()
    ev = st.register_evidence("E1", scope="blind-cert", purpose="certification",
                              policy_revision="LAW-v3", provenance="fx")
    st.register_qualification("CLAIM-C", verdict="REQUALIFIED",
                              support_manifest={"E1": ev.eligibility_revision},
                              scope="blind-cert", purpose="certification",
                              policy_revision="LAW-v3")
    return st


class TestD36SharpestSequence:
    def test_v_r_a_race_then_independent_requalification_executes(self):
        st = fresh_state()
        # T1: validated VALID.
        assert st.validate_current("CLAIM-C", "certification")[0] == CURRENT_QUALIFIED
        # T2: E1 revoked — R commits at one authoritative point.
        st.commit_revocation("E1", "key compromise", "blind-cert",
                             "certification", "LAW-v3", "verifier")
        # T3: the action authorized by the T1 validation is REJECTED.
        # The T1 validation is dead; revalidation is mandatory, not advisory.
        outcome, _ = st.commit_action("ACT-1", ["CLAIM-C"], law_authorization=True)
        assert outcome == "REJECTED"
        # T4: independent E2 arrives.
        e2 = st.register_evidence("E2", scope="blind-cert",
                                  purpose="certification",
                                  policy_revision="LAW-v3", provenance="fx2")
        # T5: the claim requalifies on the independent support.
        st.register_qualification("CLAIM-C", verdict="REQUALIFIED",
                                  support_manifest={"E2": e2.eligibility_revision},
                                  scope="blind-cert", purpose="certification",
                                  policy_revision="LAW-v3")
        assert st.validate_current("CLAIM-C", "certification")[0] == CURRENT_QUALIFIED
        # T6: the same action, re-authorized on fresh validation, EXECUTES.
        outcome, _ = st.commit_action("ACT-1", ["CLAIM-C"], law_authorization=True)
        assert outcome == "AUTHORIZED"

    def test_r_before_p_publication_built_pre_r_rejected_post_r(self):
        """A publication built pre-R was valid when built. R commits while
        the write is in flight. The delayed write must fail — older evidence
        cannot regain authority through the delayed write."""
        st = fresh_state()
        h = st.projections  # noqa: F841 (projection registered below)
        st.register_projection("SUMMARY-42", artifact_id="art-17",
                               claim_deps={"CLAIM-C": st.claims["CLAIM-C"].qualification_revision},
                               evidence_deps={"E1": st.evidence["E1"].eligibility_revision})
        from ..revocation_linearization import ProjectionCandidate
        head = st.projections["SUMMARY-42"]
        stale = ProjectionCandidate(
            projection_id="SUMMARY-42",
            expected_head_revision=head.projection_revision,
            artifact_id="art-stale",
            claim_deps={"CLAIM-C": st.claims["CLAIM-C"].qualification_revision},
            evidence_manifest={"E1": st.evidence["E1"].eligibility_revision},
            policy_revision="LAW-v3",
            asserted_claims={"CLAIM-C": "REQUALIFIED"},
            intended_uses=("certification",),
            fencing_token=head.fencing_token,
        )
        # R commits between the writer's read and its publish.
        st.commit_revocation("E1", "exposed", "blind-cert",
                             "certification", "LAW-v3", "verifier")
        assert st.publish_projection(stale)[0] == STALE_DEPENDENCY

    def test_fence_synchronous_no_stale_window_at_commit(self):
        """The fence is effective at the commit tick itself: the immediate
        next certification attempt through revoked evidence fails."""
        st = fresh_state()
        st.commit_revocation("E1", "immediate", "blind-cert",
                             "certification", "LAW-v3", "verifier")
        # No projection refresh has run; the fence still holds.
        assert st.validate_current("CLAIM-C", "certification")[0] == CURRENT_UNQUALIFIED
        outcome, _ = st.commit_action("ACT-1", ["CLAIM-C"], law_authorization=True)
        assert outcome == "REJECTED"

    def test_cached_t1_validation_never_sufficient_alone(self):
        """A cached VALID verdict from T1, presented at T3 after R at T2,
        cannot authorize anything by itself. Only a fresh read-time
        validation against current state counts."""
        st = fresh_state()
        v1, _ = st.validate_current("CLAIM-C", "certification")
        assert v1 == CURRENT_QUALIFIED  # the cached verdict, now stale
        st.commit_revocation("E1", "gone", "blind-cert",
                             "certification", "LAW-v3", "verifier")
        # The boundary revalidates against current state, not the cache.
        outcome, _ = st.commit_action("ACT-1", ["CLAIM-C"], law_authorization=True)
        assert outcome == "REJECTED"
        # And a fresh read confirms the current truth.
        assert st.validate_current("CLAIM-C", "certification")[0] == CURRENT_UNQUALIFIED

"""w333 regression: the hold veto fires only on verdict declarations, never
on prose mentions of the hold-veto mechanism."""
import sys, os, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))
from check_merge_consensus import _looks_like_review

EPSILON_6226819187 = json.load(open("/tmp/epsilon-iv-comment.json"))["body"]

def test_w333_epsilon_genuine_approved_survives_prose_hold_mention():
    """Living proof: Epsilon's [NAYA EPSILON · REVIEW] APPROVED on #2704 was
    vetoed by the prose '(hold-veto fail-closed; ...)'. Declaration-only veto
    must count it as a review."""
    assert _looks_like_review(EPSILON_6226819187)

def test_prose_hold_mention_does_not_veto_approval():
    assert _looks_like_review(
        "Meta note: the hold-veto is fail-closed, discussion only.\n"
        "[NAYA BETA · REVIEW] APPROVED — looks good.")

def test_quoted_hold_verdict_does_not_veto():
    assert _looks_like_review(
        'The guide says post "VERDICT: HOLD" to block a merge.\n'
        "[NAYA BETA · REVIEW] APPROVED — looks good.")

def test_negated_hold_does_not_veto():
    assert _looks_like_review(
        "Not a HOLD — nothing blocking.\n[NAYA BETA · REVIEW] APPROVED.")

def test_declared_hold_still_vetoes():
    assert not _looks_like_review("[NAYA ZETA · REVIEW] HOLD — blocked on IV")
    assert not _looks_like_review("VERDICT: DO NOT MERGE — red CI")
    assert not _looks_like_review("DO NOT MERGE\n[NAYA BETA · REVIEW] APPROVED — accident")
    assert not _looks_like_review("## VERDICT: merge: HOLD — pending CI")

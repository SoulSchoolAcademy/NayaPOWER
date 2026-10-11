"""RED-first acceptance suite for the candidate retrieval authorization gate.

Spec: BRAIN/00-SPEC/0007-RETRIEVAL-AUTHORIZATION-GATE-SPEC-V1.md (Lane 8, t912).
Closes: Lane 5 t902 falsification — unauthorized (retrieval_authorized=false)
lessons ARE surfaced today; no authorization mechanism exists at retrieve().

RED protocol: this file was written BEFORE tools/retrieval_authorization_gate.py
existed. The first run fails (module missing) alongside red_demo_t942.py proving
the hole on the UNWIRED seam (retrieve() lets every probe entry through).
GREEN protocol: the same assertions pass against the candidate gate module,
which is NOT wired into retrieve() — wiring needs Shawn's word.

Run: python3 -m pytest tools/test_retrieval_authorization_gate.py -v
"""
import pytest

from retrieval_authorization_gate import (
    retrieval_visible,
    filter_corpus,
    supersession_head,
    authorization_state,
    PRIVATE_CALLER,
    PUBLIC_PUBLICATION_SCOPE,
)

PRIVATE = {"surface": "private_authenticated", "identity": "Shawn"}


def entry(**over):
    e = {
        "id": "SN-TEST-001",
        "title": "t942 probe note",
        "lifecycle_state": "ACTIVE",
        "retrieval_authorized": True,
        "scope": "PRIVATE",
        "publication_scope": "PRIVATE",
    }
    e.update(over)
    return e


# ---------------------------------------------------------------- positives
def test_public_caller_sees_authorized_public_note():
    e = entry(scope="PUBLIC", publication_scope="PUBLIC")
    visible, reason = retrieval_visible(e, caller=None)
    assert visible, reason


def test_public_caller_sees_authorized_collective_note():
    e = entry(publication_scope="COLLECTIVE")
    visible, reason = retrieval_visible(e, caller=None)
    assert visible, reason


def test_private_caller_sees_authorized_private_note():
    e = entry()
    visible, reason = retrieval_visible(e, caller=PRIVATE)
    assert visible, reason


def test_all_publication_scopes_in_vocabulary_open():
    for pub in sorted(PUBLIC_PUBLICATION_SCOPE):
        e = entry(publication_scope=pub)
        visible, reason = retrieval_visible(e, caller=None)
        assert visible, f"{pub}: {reason}"


# ---------------------------------------------------------------- negatives
def test_public_caller_excludes_private_scope_note():
    e = entry()  # scope=PRIVATE, caller=None
    visible, reason = retrieval_visible(e, caller=None)
    assert not visible and reason, reason


def test_unauthorized_flag_false_excluded_even_for_private_caller():
    # t902 falsification: ACTIVE seed with retrieval_authorized=false surfaced.
    e = entry(retrieval_authorized=False)
    visible, reason = retrieval_visible(e, caller=PRIVATE)
    assert not visible, f"HOLE: unauthorized note visible to private caller ({reason})"
    assert "authorized" in reason.lower()


def test_unauthorized_flag_false_excluded_for_public_caller():
    e = entry(retrieval_authorized=False, publication_scope="PUBLIC")
    visible, reason = retrieval_visible(e, caller=None)
    assert not visible, f"HOLE: explicit denial overridden by publication scope ({reason})"


def test_missing_authorization_field_fails_closed():
    e = entry()
    del e["retrieval_authorized"]
    visible, reason = retrieval_visible(e, caller=PRIVATE)
    assert not visible, f"HOLE: unknown authorization state guessed as allowed ({reason})"
    assert "unknown" in reason.lower() or "fail" in reason.lower()


def test_superseded_excluded():
    e = entry(lifecycle_state="SUPERSEDED")
    visible, reason = retrieval_visible(e, caller=PRIVATE)
    assert not visible, f"HOLE: superseded note visible ({reason})"


def test_revoked_before_retrieval_excluded():
    # Boundary: authorized at capture, revoked before retrieval -> excluded.
    e = entry(lifecycle_state="REVOKED")
    visible, reason = retrieval_visible(e, caller=PRIVATE)
    assert not visible, f"HOLE: revoked note visible ({reason})"


def test_archived_excluded():
    e = entry(lifecycle_state="ARCHIVED")
    visible, _ = retrieval_visible(e, caller=PRIVATE)
    assert not visible


def test_unknown_scope_value_fails_closed():
    e = entry(scope="PUBLIK")  # typo'd / attacker-typed scope
    visible, reason = retrieval_visible(e, caller=None)
    assert not visible, f"HOLE: unknown scope value treated as open ({reason})"


def test_private_surface_requires_nonempty_identity():
    # Self-declared surface without identity is a claim, not proof (B2).
    e = entry()
    visible, _ = retrieval_visible(e, caller={"surface": "private_authenticated"})
    assert not visible
    visible2, _ = retrieval_visible(e, caller={"surface": "private_authenticated", "identity": "   "})
    assert not visible2
    visible3, _ = retrieval_visible(e, caller={"surface": "public", "identity": "Shawn"})
    assert not visible3


def test_malformed_entry_fails_closed_never_raises():
    for bad in (None, {}, {"id": "x", "lifecycle_state": ["weird"]}, "not-a-dict"):
        visible, reason = retrieval_visible(bad, caller=PRIVATE)
        assert not visible and reason, f"bad entry {bad!r} must fail closed"


# ------------------------------------------------------------- adversarial
def test_tampered_flag_string_yes_fails_closed():
    # Valid-looking metadata, tampered eligibility flag: "yes" is not True.
    e = entry(retrieval_authorized="yes")
    visible, reason = retrieval_visible(e, caller=PRIVATE)
    assert not visible, f"HOLE: truthy-but-not-True flag accepted ({reason})"


def test_tampered_flag_int_one_fails_closed():
    e = entry(retrieval_authorized=1)
    visible, reason = retrieval_visible(e, caller=PRIVATE)
    assert not visible, f"HOLE: int 1 accepted as authorization ({reason})"


def test_tampered_scope_lowercase_public_still_requires_caller():
    # Case games: 'public' lowercase in scope is normalized by spec (upper),
    # but publication_scope 'PUBLIC' alone opens; scope alone does not.
    e = entry(scope="public", publication_scope="PRIVATE")
    visible, _ = retrieval_visible(e, caller=None)
    assert not visible


def test_stale_cache_resurrection_excluded():
    # Attacker holds an old serialized copy saying ACTIVE; the registry says
    # SUPERSEDED with superseded_by. Registry is the source of truth.
    stale_copy = entry(id="SN-STALE", lifecycle_state="ACTIVE")
    registry = {"SN-STALE": entry(id="SN-STALE", lifecycle_state="SUPERSEDED",
                                  superseded_by="SN-NEWER")}
    visible, reason = retrieval_visible(stale_copy, caller=PRIVATE, registry_index=registry)
    assert not visible, f"HOLE: stale cache resurrected superseded note ({reason})"


def test_supersession_chain_head_only_visible():
    a = entry(id="SN-A", superseded_by="SN-B")
    b = entry(id="SN-B", superseded_by="SN-C")
    c = entry(id="SN-C")
    index = {"SN-A": a, "SN-B": b, "SN-C": c}
    va, _ = retrieval_visible(a, caller=PRIVATE, registry_index=index)
    vb, _ = retrieval_visible(b, caller=PRIVATE, registry_index=index)
    vc, rc = retrieval_visible(c, caller=PRIVATE, registry_index=index)
    assert not va and not vb, "superseded chain members must be excluded"
    assert vc, f"chain head must stay visible ({rc})"


def test_supersession_cycle_fails_closed():
    x = entry(id="SN-X", superseded_by="SN-Y")
    y = entry(id="SN-Y", superseded_by="SN-X")
    index = {"SN-X": x, "SN-Y": y}
    vx, rx = retrieval_visible(x, caller=PRIVATE, registry_index=index)
    vy, ry = retrieval_visible(y, caller=PRIVATE, registry_index=index)
    assert not vx and not vy, f"cycle must fail closed ({rx} / {ry})"


def test_superseded_by_unknown_target_fails_closed():
    e = entry(id="SN-ORPHAN", superseded_by="SN-MISSING")
    visible, reason = retrieval_visible(e, caller=PRIVATE, registry_index={})
    assert not visible, f"HOLE: dangling supersession guessed ({reason})"


def test_excluded_verdict_leaks_no_content():
    # Silent-exclusion discipline (spec 4.3): the verdict names a reason code,
    # never the note's content, id, or existence-sensitive detail.
    e = entry(id="SN-SECRET-007", title="Secret plans", retrieval_authorized=False)
    visible, reason = retrieval_visible(e, caller=None)
    assert not visible
    assert "SN-SECRET-007" not in reason and "Secret" not in reason


# ------------------------------------------------------------- composition
def test_filter_corpus_keeps_only_visible():
    corpus = [
        entry(id="keep-pub", scope="PUBLIC", publication_scope="PUBLIC"),
        entry(id="drop-priv", scope="PRIVATE"),
        entry(id="drop-unauth", retrieval_authorized=False, publication_scope="PUBLIC"),
        entry(id="drop-sup", lifecycle_state="SUPERSEDED", publication_scope="PUBLIC"),
    ]
    kept = filter_corpus(corpus, caller=None)
    assert [e["id"] for e in kept] == ["keep-pub"]


def test_authorization_state_tristate():
    assert authorization_state(entry(retrieval_authorized=True)) == "AUTHORIZED"
    assert authorization_state(entry(retrieval_authorized=False)) == "DENIED"
    assert authorization_state(entry()) == "AUTHORIZED"  # present+True
    e = entry(); del e["retrieval_authorized"]
    assert authorization_state(e) == "UNKNOWN"
    assert authorization_state(entry(retrieval_authorized="yes")) == "UNKNOWN"
    assert authorization_state(entry(retrieval_authorized=1)) == "UNKNOWN"
    assert authorization_state(None) == "UNKNOWN"


def test_supersession_head_resolves():
    a = entry(id="SN-A", superseded_by="SN-B")
    b = entry(id="SN-B", superseded_by="SN-C")
    c = entry(id="SN-C")
    index = {"SN-A": a, "SN-B": b, "SN-C": c}
    assert supersession_head(a, index)["id"] == "SN-C"
    assert supersession_head(c, index)["id"] == "SN-C"
    assert supersession_head(a, {}) is None  # dangling -> fail closed

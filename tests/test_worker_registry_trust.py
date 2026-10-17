"""Regression tests: worker-registry trust boundary (PR #2729 follow-up).

Adversarial review 2026-10-17 (comment 6236075392) found a fail-open
authorization edge: `_load_worker_registry()` read the CANDIDATE tree, so a
PR could add its own name to seats/worker-registry.json, declare
`Seat: Naya <new-name>`, and have the same candidate tree authorize its
author. The loader proved the name was present; it never proved an
authorized team lead put it there.

These tests pin the repair:
  1. The author-seat gate resolves the author against the TRUSTED
     base-branch registry (+ hardcoded legacy seats), never the candidate copy.
  2. `_names_from_registry` is fail-closed on malformed input (non-object
     root, malformed team entries) — no AttributeError escapes, no widening.
  3. Negative fixture: unrecognized author self-adds to the candidate
     registry -> still untrusted. Same author after the trusted registry
     lists them -> trusted.
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))

from check_merge_consensus import (
    _names_from_registry,
    _author_is_trusted,
    _LEGACY_SEATS,
)


def _registry_with(workers):
    return {
        "teams": {
            "Team X": {"workers": [{"name": w} for w in workers]},
        },
        "builder_seats": {"workers": []},
    }


def test_names_from_valid_registry():
    names = _names_from_registry(_registry_with(["Zeta", "Mallory"]))
    assert names == ["zeta", "mallory"], names


def test_names_from_non_object_root_fail_closed():
    # Valid JSON, non-object root: must not raise, must not widen.
    assert _names_from_registry(["zeta"]) == []
    assert _names_from_registry("zeta") == []
    assert _names_from_registry(None) == []


def test_names_from_malformed_teams_fail_closed():
    # teams present but not a dict; team entries not dicts; workers not dicts.
    assert _names_from_registry({"teams": ["zeta"]}) == []
    assert _names_from_registry({"teams": {"T": ["zeta"]}}) == []
    assert _names_from_registry({"teams": {"T": {"workers": ["zeta"]}}}) == []
    assert _names_from_registry({"teams": {"T": {"workers": [{"name": None}]}}}) == []
    # builder_seats malformed likewise
    assert _names_from_registry({"teams": {}, "builder_seats": ["zeta"]}) == []


def test_legacy_seat_is_trusted_without_registry():
    assert _author_is_trusted("Naya Epsilon", []) is True
    assert _author_is_trusted("Naya Nitro", []) is True
    assert "nitro" in _LEGACY_SEATS  # guard: fixture assumes the tuple


def test_numeric_seat_is_trusted_without_registry():
    assert _author_is_trusted("Naya 5", []) is True
    assert _author_is_trusted("Naya 1", []) is True


def test_unknown_author_is_not_trusted():
    assert _author_is_trusted("Naya Mallory", []) is False
    assert _author_is_trusted(None, ["zeta"]) is False


def test_adversarial_self_add_still_untrusted():
    """The exact 2026-10-17 hole: candidate registry lists 'mallory'
    (the PR added its own name), but the TRUSTED base-branch registry does
    not. The author gate must still reject."""
    candidate_names = _names_from_registry(_registry_with(["mallory"]))
    assert "mallory" in candidate_names  # candidate copy proves presence...
    trusted_names = _names_from_registry(_registry_with(["zeta"]))
    assert "mallory" not in trusted_names
    # ...but presence in the candidate copy is not authorization.
    assert _author_is_trusted("Naya Mallory", trusted_names) is False


def test_authorized_roster_update_trusts():
    """After an authorized team lead lands 'mallory' on the base branch,
    the same declaration passes."""
    trusted_names = _names_from_registry(_registry_with(["zeta", "mallory"]))
    assert _author_is_trusted("Naya Mallory", trusted_names) is True


def test_trust_is_case_insensitive():
    trusted_names = _names_from_registry(_registry_with(["Mallory"]))
    assert _author_is_trusted("Naya Mallory", trusted_names) is True

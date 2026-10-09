"""Retrieval predicate (GAP 8, 9-node wiring Phase 1).

retrieve() gates every relevance candidate through
kernel/value_calculus.py::retrieval_eligible() before sorting/selecting.
Relevance never authorizes disclosure by itself: BLOCKED / FAIL / UNKNOWN
candidates are dropped. With no requester_context the call fails closed for
scoped entries (non-public scope dropped) while public entries stay
eligible — existing behavior for the common case is unchanged.
"""
import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]

SPEC = importlib.util.spec_from_file_location("smart_note_v2_pred", ROOT / "tools" / "smart_note_v2.py")
mod = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(mod)


def _page(tmp_path, name, nutshell):
    p = tmp_path / name
    p.write_text(f"# T\n\n## IN A NUTSHELL\n\n{nutshell}", encoding="utf-8")
    return name


def _note(sn, ib, title, keywords, scope, page, captured_at, publication_scope=None):
    e = {
        "smart_note_id": sn,
        "intelligent_block_id": ib,
        "title": title,
        "category": "X", "topic": "Y", "subtopic": "Z",
        "keywords": keywords,
        "truth_state": "VERIFIED",
        "captured_at": captured_at,
        "lifecycle_state": "ACTIVE",
        "projection_path": page,
    }
    if scope is not None:
        e["scope"] = scope
    if publication_scope is not None:
        e["publication_scope"] = publication_scope
    return e


@pytest.fixture
def pred_registry(tmp_path, monkeypatch):
    """Two quantum-matching notes. The PRIVATE one scores HIGHER on
    relevance (and is newer, winning every tie-break), so if the
    predicate is not wired, it wins. With the predicate wired and no
    requester context, the PUBLIC note must win instead."""
    pub = _note("SN-PUB", "IB-PUB", "Quantum notes", ["quantum"],
                "PUBLIC", _page(tmp_path, "pub.md", "public quantum answer"),
                "2026-10-09T00:00:00Z")
    priv = _note("SN-PRIV", "IB-PRIV", "Quantum mechanics complete reference",
                 ["quantum", "mechanics", "complete", "reference"],
                 "PRIVATE", _page(tmp_path, "priv.md", "private quantum answer"),
                 "2026-10-09T12:00:00Z")
    rp = tmp_path / "index.json"
    rp.write_text(json.dumps({"entries": [pub, priv]}), encoding="utf-8")
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "REGISTRY", rp)
    return rp


def test_no_context_excludes_blocked_scope_entry(pred_registry):
    """Anonymous call: the higher-relevance PRIVATE note is dropped by the
    predicate (CROSS_SCOPE FAIL); the PUBLIC note is returned."""
    result = mod.retrieve("quantum")
    assert result["retrieved"]["smart_note_id"] == "SN-PUB"


def test_no_context_fails_closed_when_only_scoped_entries_match(tmp_path, monkeypatch):
    """Anonymous call where every relevant note is scoped: fail closed with
    NO_RELEVANT_INTELLIGENCE rather than serving a scoped note."""
    priv = _note("SN-PRIV", "IB-PRIV", "Quantum mechanics complete reference",
                 ["quantum"], "PRIVATE",
                 _page(tmp_path, "priv.md", "private quantum answer"),
                 "2026-10-09T12:00:00Z")
    rp = tmp_path / "index.json"
    rp.write_text(json.dumps({"entries": [priv]}), encoding="utf-8")
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "REGISTRY", rp)
    with pytest.raises(SystemExit) as ei:
        mod.retrieve("quantum")
    assert str(ei.value.code) == "NO_RELEVANT_INTELLIGENCE"


def test_matching_scope_context_returns_scoped_entry(pred_registry):
    """An authenticated requester inside the note's scope passes the
    predicate, and the higher-relevance scoped note wins."""
    result = mod.retrieve("quantum", requester_context={
        "requester_id": "shawn",
        "requester_scope": "PRIVATE",
        "authority_basis": "owner:shawn",
    })
    assert result["retrieved"]["smart_note_id"] == "SN-PRIV"


def test_unauthenticated_context_blocks_everything(pred_registry):
    """A context naming no requester_id is BLOCKED (UNAUTHENTICATED_REQUESTER)
    for every candidate: nothing is served."""
    with pytest.raises(SystemExit) as ei:
        mod.retrieve("quantum", requester_context={"requester_scope": "PUBLIC"})
    assert str(ei.value.code) == "NO_RELEVANT_INTELLIGENCE"


def test_cross_scope_without_authority_is_dropped(pred_registry):
    """Authenticated requester in PUBLIC scope cannot reach the PRIVATE note
    without a cross-scope authority basis; the PUBLIC note is returned."""
    result = mod.retrieve("quantum", requester_context={
        "requester_id": "analyst",
        "requester_scope": "PUBLIC",
        "authority_basis": "public-context",
    })
    assert result["retrieved"]["smart_note_id"] == "SN-PUB"


def test_legacy_entry_without_scope_stays_eligible(tmp_path, monkeypatch):
    """Entries with no scope metadata (the historical corpus shape) are
    treated as public: existing behavior is unchanged."""
    legacy = _note("SN-LEG", "IB-LEG", "Quantum notes legacy", ["quantum"],
                   None, _page(tmp_path, "leg.md", "legacy quantum answer"),
                   "2026-10-09T00:00:00Z")
    rp = tmp_path / "index.json"
    rp.write_text(json.dumps({"entries": [legacy]}), encoding="utf-8")
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "REGISTRY", rp)
    result = mod.retrieve("quantum")
    assert result["retrieved"]["smart_note_id"] == "SN-LEG"


def test_public_publication_scope_counts_as_public(tmp_path, monkeypatch):
    """A PRIVATE-scope note whose projection carries Human-Director public
    authorization (PUBLIC_DERIVED_VIEW) discloses nothing non-public to an
    anonymous requester: it stays eligible."""
    note = _note("SN-DER", "IB-DER", "Quantum notes derived", ["quantum"],
                 "PRIVATE", _page(tmp_path, "der.md", "derived quantum answer"),
                 "2026-10-09T00:00:00Z", publication_scope="PUBLIC_DERIVED_VIEW")
    rp = tmp_path / "index.json"
    rp.write_text(json.dumps({"entries": [note]}), encoding="utf-8")
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "REGISTRY", rp)
    result = mod.retrieve("quantum")
    assert result["retrieved"]["smart_note_id"] == "SN-DER"


# --- object-scope derivation unit checks -------------------------------------

def test_entry_object_scope_derivation():
    assert mod._entry_object_scope({}) == "PUBLIC"                      # legacy: no scope
    assert mod._entry_object_scope({"scope": "PRIVATE"}) == "PRIVATE"
    assert mod._entry_object_scope({"scope": "ALL_SEATS"}) == "ALL_SEATS"
    assert mod._entry_object_scope({"scope": "PRIVATE",
                                    "publication_scope": "PUBLIC_DERIVED_VIEW"}) == "PUBLIC"
    assert mod._entry_object_scope({"scope": "public"}) == "PUBLIC"


def test_operation_request_fields():
    req = mod._retrieval_operation_request({"smart_note_id": "SN-X", "scope": "PRIVATE"}, None)
    assert req.requester_id == "anonymous"
    assert req.requester_scope == "PUBLIC"
    assert req.object_scope == "PRIVATE"
    assert req.source_canonical is True
    assert req.authority_basis == "public-context"

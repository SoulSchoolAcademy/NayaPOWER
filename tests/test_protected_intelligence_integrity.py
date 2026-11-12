"""Protected intelligence must fail closed on HOLLOWING, not only on deletion.

Origin: PR #1554 migrated SN-0358/SN-0359 to the v2 capture schema and, in
doing so, removed:

    intelligence.epistemic_state      the CANDIDATE truth ceiling
    intelligence.falsifier            the falsifiability contract
    intelligence.measurement_contract how the claim gets tested
    intelligence.successor_effect     cold-successor continuity
    source.director / source.ratification
    source.restoration_provenance     the a2f103f4f deletion + recovery record

Both files remained present, so the presence-only protection added in #1551
passed. That is the failure this module closes:

    PRESENCE IS NECESSARY AND NOT SUFFICIENT.

A protected object that still exists but has lost a required governed field has
been destroyed in all but filename, and must fail exactly as a deletion would.

`migration_is_not_retirement_authority` and `field_stripping_is_deletion` are
recorded in .naya/protected-intelligence.json so the rule travels with the data
rather than only in this test.

Run: python -m pytest tests/test_protected_intelligence_integrity.py -q
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / ".naya" / "protected-intelligence.json"
CAPTURE_DIR = ROOT / ".naya" / "capture"


def _registry():
    assert REGISTRY.is_file(), "protected-intelligence registry missing"
    return json.loads(REGISTRY.read_text(encoding="utf-8"))


def _protected():
    entries = _registry().get("protected", [])
    assert entries, "protected registry must name at least one Smart Note"
    return entries


def _capture_index():
    idx = {}
    if not CAPTURE_DIR.exists():
        return idx
    # Sorted for determinism: unsorted glob order is filesystem-dependent and
    # let a reconstruction fixture shadow the authoritative SN-0359 capture
    # on some machines (order-dependent test flake).
    for p in sorted(CAPTURE_DIR.glob("*.json")):
        try:
            doc = json.loads(p.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError):
            continue
        nid = doc.get("smart_note_id") or doc.get("id")
        if not nid:
            continue
        nid = str(nid)
        # A canonical-reconstruction honestly declares it has no original
        # provenance; it must never shadow the authoritative capture of the
        # same note.
        is_reconstruction = (doc.get("source") or {}).get("ingestion") == "canonical-reconstruction"
        if nid in idx and is_reconstruction:
            continue
        idx[nid] = doc
    return idx


def test_policy_records_that_presence_is_not_sufficient():
    """The rule must live in the data, not only in this test. A future lane that
    reads only the registry still learns it."""
    r = _registry()
    p = r["policy"]
    assert "NOT SUFFICIENT" in p["integrity_rule"]
    assert p["migration_is_not_retirement_authority"] is True
    assert p["field_stripping_is_deletion"] is True
    assert p["semantic_similarity_is_not_retirement_authority"] is True


def test_every_protected_entry_has_required_fields_declared():
    r = _registry()
    for key in (
        "required_fields_common",
        "required_fields_intelligence",
        "required_fields_source",
    ):
        assert r.get(key), f"registry must declare {key}"
    for e in r["protected"]:
        assert e.get("smart_note_id")
        assert e.get("reason"), f"{e.get('smart_note_id')} protected without a reason"


def test_protected_intelligence_retains_its_governed_fields():
    """THE core assertion.

    Presence was already covered by #1551. This asserts the object is still
    whole. A migration that strips fields fails here with the exact field names,
    instead of silently producing a hollow law that still has a filename.
    """
    r = _registry()
    idx = _capture_index()
    common = r["required_fields_common"]
    in_intel = r["required_fields_intelligence"]
    in_source = r["required_fields_source"]

    problems = []
    for e in r["protected"]:
        nid = e["smart_note_id"]
        doc = idx.get(nid)
        if doc is None:
            problems.append(f"{nid}: MISSING ENTIRELY")
            continue

        for f in common:
            if not doc.get(f):
                problems.append(f"{nid}: missing top-level '{f}'")

        intel = doc.get("intelligence") or {}
        for f in in_intel:
            val = intel.get(f)
            if val is None or val == [] or val == "":
                problems.append(f"{nid}: missing intelligence.{f}")

        src = doc.get("source") or {}
        for f in in_source:
            if not src.get(f):
                problems.append(f"{nid}: missing source.{f}")

        if e.get("requires_restoration_provenance") and not src.get("restoration_provenance"):
            problems.append(f"{nid}: missing source.restoration_provenance")

    assert not problems, (
        "Protected intelligence was HOLLOWED OUT. Each item below is governed "
        "content that no longer exists on a Director-ratified law. Presence is "
        "necessary and not sufficient; field stripping is deletion.\n  "
        + "\n  ".join(problems)
    )


def test_protected_objects_are_canonical_v2():
    """A v1 object cannot satisfy the v2 governed-field contract, so state it
    explicitly rather than letting it fail on a confusing downstream assertion."""
    idx = _capture_index()
    bad = [
        f"{nid}: {doc.get('schema')}"
        for e in _protected()
        for nid, doc in idx.items()
        if nid == e["smart_note_id"] and doc.get("schema") != "naya.smart-note-capture.v2"
    ]
    assert not bad, f"protected objects not on canonical v2: {bad}"


def test_protected_objects_declare_a_truth_ceiling():
    """`RATIFIED` was repeatedly used as a truth LEVEL on newly authored
    intelligence, which the contract fixes at CANDIDATE. A protected law that
    asserts no epistemic state has had its own status quietly removed."""
    idx = _capture_index()
    bad = [
        nid
        for e in _protected()
        for nid, doc in idx.items()
        if nid == e["smart_note_id"]
        and not ((doc.get("intelligence") or {}).get("epistemic_state"))
    ]
    assert not bad, f"protected objects with no epistemic_state (truth ceiling removed): {bad}"


def test_ratification_is_preserved_on_every_protected_law():
    """SN-0359 lost its ratification block to #1554. These are Director-ratified
    laws; losing the evidence of ratification is losing the authority claim."""
    idx = _capture_index()
    bad = [
        nid
        for e in _protected()
        for nid, doc in idx.items()
        if nid == e["smart_note_id"] and not (doc.get("source") or {}).get("ratification")
    ]
    assert not bad, f"protected objects with no ratification provenance: {bad}"


def test_registry_documents_what_1554_stripped():
    """The regression is named in the data so the next seat inherits the lesson
    rather than rediscovering it."""
    r = _registry()
    documented = {
        e["smart_note_id"]: e.get("stripped_by_1554", [])
        for e in r["protected"]
        if e.get("stripped_by_1554")
    }
    assert "SN-0358" in documented, "the SN-0358 stripping incident must stay on the record"
    assert "SN-0359" in documented, "the SN-0359 stripping incident must stay on the record"
    for nid, fields in documented.items():
        assert "intelligence.falsifier" in fields, f"{nid} record must name the falsifier"
        assert "source.ratification" in fields, f"{nid} record must name the ratification"

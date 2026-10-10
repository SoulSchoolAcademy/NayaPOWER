import importlib.util
import re
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("smart_note_v2", ROOT / "tools" / "smart_note_v2.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

# Measured live drift on main@add657b4d. Pinned as a ratchet, not as a pass.
# Rationale: the publish path only ever proves the single note it just handled,
# so a fully green run can coexist with a broken registry. CI must stay usable,
# but the drift may never grow silently. Count pins stop cross-class masking;
# the identity-membership ratchet below also stops within-class substitution
# (repair one known defect + introduce a different defect at the same count).
#
# ROOT CAUSE NOTE: entries_without_hash and captures_unregistered_by_hash are
# coupled. Every registry entry currently lacks content_hash (28/28), so no
# capture can be hash-reconciled against any entry. The 20 "unregistered"
# captures are therefore a downstream symptom of the 28 hashless entries, not
# an independent second fault. Repairing hash coverage clears both at once.
PINNED_BASELINE = {
    "unparseable_captures": 0,
    "captures_missing_intelligence": 0,
    "captures_unregistered_by_hash": 20,
    "entries_without_hash": 28,
    "entries_with_stale_hash": 0,
    "duplicate_smart_note_ids": 0,
    "published_entries_missing_projection_path": 0,
    "registry_projection_paths_absent": 0,
    "published_pages_without_registry_entry": 1,
    "duplicate_published_page_paths": 1,
    "registry_entries_without_capture_identity": 17,
    "captures_without_registry_identity": 1,
    "captures_without_smart_note_id": 5,
    "filename_smart_note_id_divergence": 1,
}

# Identity-bearing drift needs a stronger ratchet than cardinality alone.
# These are the exact known members at the #1495 repair baseline. Repairs may
# remove members freely, but a different defect may not replace a repaired one
# while keeping the count unchanged.
PINNED_IDENTITY_MEMBERS = {
    "registry_entries_without_capture_identity": {
        "SN-001",
        "SN-003",
        "SN-004",
        "SN-005",
        "SN-006",
        "SN-007",
        "SN-008",
        "SN-009",
        "SN-010",
        "SN-011",
        "SN-012",
        "SN-018",
        "SN-019",
        "SN-0311",
        "SN-0312",
        "SN-0345",
        "SN-275",
    },
    "captures_without_registry_identity": {"SN-276"},
    "captures_without_smart_note_id": {
        "SMART-NOTE-20260929-sn003-naya-continuation-engine.json",
        "SMART-NOTE-20260929-sn004-shawn-standing-law-r2.json",
        "SMART-NOTE-20260929-sn004-shawn-standing-law.json",
        "SMART-NOTE-20261001-sn019-complete-the-app-doctrine.json",
        "SMART-NOTE-b8f141805fa0d7ae.json",
    },
    "filename_smart_note_id_divergence": {
        "SMART-NOTE-20261005-sn0355-nonstop-loop.json|SN-355|SN-346"
    },
}

PAGE = "BRAIN/05-MEMORY/SMART-NOTES/2026/01/01/CAT/TOPIC/SUB/SN-001/IB-1.md"


def _hash(intelligence):
    return mod._canonical_content_hash(
        json.dumps(intelligence, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    )


def build_clean_root(tmp_path):
    """A minimal fully-reconciled tree: one capture, one entry, one page."""
    intelligence = {"essence": "a", "distilled_intelligence": "b"}
    cap_dir = tmp_path / ".naya" / "capture"
    cap_dir.mkdir(parents=True)
    (cap_dir / "SMART-NOTE-SN-001.json").write_text(
        json.dumps({"smart_note_id": "SN-001", "intelligence": intelligence}), encoding="utf-8"
    )
    page = tmp_path / PAGE
    page.parent.mkdir(parents=True)
    page.write_text("# IB-1\n", encoding="utf-8")
    reg_path = tmp_path / ".naya" / "memory" / "smart-notes" / "index.json"
    reg_path.parent.mkdir(parents=True)
    reg_path.write_text(
        json.dumps(
            {
                "schema": "naya.smart-note-projection-index.v1",
                "entries": [
                    {
                        "smart_note_id": "SN-001",
                        "intelligent_block_id": "IB-1",
                        "content_hash": _hash(intelligence),
                        "projection_path": PAGE,
                        "projection_status": "GITHUB_BRAIN_PUBLISHED",
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    return reg_path


def read_entries(reg_path):
    return json.loads(reg_path.read_text(encoding="utf-8"))["entries"]


def write_entries(reg_path, entries):
    doc = json.loads(reg_path.read_text(encoding="utf-8"))
    doc["entries"] = entries
    reg_path.write_text(json.dumps(doc), encoding="utf-8")


def test_clean_fixture_is_reported_ok(tmp_path):
    report = mod.audit_registry(root=tmp_path)
    assert report["ok"] is True, report["defects"]
    assert report["defect_total"] == 0


@pytest.mark.parametrize(
    "mutate,expected_class",
    [
        pytest.param(
            lambda root: _add_capture(root, {"essence": "unregistered"}),
            "captures_unregistered_by_hash",
            id="unregistered_capture",
        ),
        pytest.param(
            lambda root: _set_entry_hash(root, None),
            "entries_without_hash",
            id="entry_without_hash",
        ),
        pytest.param(
            lambda root: _set_entry_hash(root, "0" * 64),
            "entries_with_stale_hash",
            id="entry_with_stale_hash",
        ),
        pytest.param(
            lambda root: (_set_entry_hash(root, None), _dup_page(root)),
            "duplicate_published_page_paths",
            id="duplicate_published_page",
        ),
        pytest.param(
            lambda root: (_set_entry_hash(root, None), _drop_projection_path(root)),
            "published_entries_missing_projection_path",
            id="published_entry_missing_projection_path",
        ),
        pytest.param(
            lambda root: _orphan_page(root),
            "published_pages_without_registry_entry",
            id="page_without_registry_entry",
        ),
        pytest.param(
            lambda root: _point_projection_at_absent_path(root),
            "registry_projection_paths_absent",
            id="projection_path_absent_on_disk",
        ),
        pytest.param(
            lambda root: _write_capture(root, "{ not json"),
            "unparseable_captures",
            id="unparseable_capture",
        ),
        pytest.param(
            lambda root: _write_capture(root, json.dumps({"smart_note_id": "SN-001"})),
            "captures_missing_intelligence",
            id="capture_missing_intelligence",
        ),
        pytest.param(
            lambda root: _drop_capture_identity(root),
            "captures_without_smart_note_id",
            id="capture_without_smart_note_id",
        ),
        pytest.param(
            lambda root: _set_entry_id(root, "SN-009"),
            "registry_entries_without_capture_identity",
            id="registry_identity_without_capture",
        ),
        pytest.param(
            lambda root: _set_capture_id(root, "SN-009"),
            "captures_without_registry_identity",
            id="capture_identity_without_registry",
        ),
        pytest.param(
            lambda root: _set_capture_id(root, "SN-009"),
            "filename_smart_note_id_divergence",
            id="filename_identity_divergence",
        ),
    ],
)
def test_detector_catches_injected_drift(tmp_path, mutate, expected_class):
    """The detector is only proven if it is shown failing on real defects."""
    reg_path = build_clean_root(tmp_path)
    assert mod.audit_registry(root=tmp_path)["ok"] is True, "fixture must start clean"

    mutate(tmp_path)

    report = mod.audit_registry(root=tmp_path)
    assert report["ok"] is False, f"detector missed {expected_class}"
    assert report["counts"][expected_class] >= 1, report["defects"]


def _add_capture(root, intelligence):
    p = root / ".naya" / "capture" / "SMART-NOTE-SN-002.json"
    p.write_text(json.dumps({"smart_note_id": "SN-002", "intelligence": intelligence}), encoding="utf-8")


def _set_entry_hash(root, value):
    reg = root / ".naya" / "memory" / "smart-notes" / "index.json"
    entries = read_entries(reg)
    entries[0]["content_hash"] = value
    write_entries(reg, entries)


def _dup_page(root):
    other = root / PAGE.replace("2026/01/01", "2026/01/02")
    other.parent.mkdir(parents=True, exist_ok=True)
    other.write_text("# IB-1\n", encoding="utf-8")


def _drop_projection_path(root):
    reg = root / ".naya" / "memory" / "smart-notes" / "index.json"
    entries = read_entries(reg)
    entries[0]["projection_path"] = None
    write_entries(reg, entries)


def _orphan_page(root):
    p = root / "BRAIN/05-MEMORY/SMART-NOTES/2026/01/03/CAT/TOPIC/SUB/SN-009/IB-9.md"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text("# IB-9\n", encoding="utf-8")


def _point_projection_at_absent_path(root):
    reg = root / ".naya" / "memory" / "smart-notes" / "index.json"
    entries = read_entries(reg)
    entries[0]["projection_path"] = PAGE.replace("IB-1.md", "IB-MISSING.md")
    write_entries(reg, entries)


def _write_capture(root, text):
    (root / ".naya" / "capture" / "SMART-NOTE-SN-001.json").write_text(text, encoding="utf-8")


def _drop_capture_identity(root):
    p = root / ".naya" / "capture" / "SMART-NOTE-SN-001.json"
    doc = json.loads(p.read_text(encoding="utf-8"))
    doc.pop("smart_note_id", None)
    p.write_text(json.dumps(doc), encoding="utf-8")


def _set_entry_id(root, smart_note_id):
    reg = root / ".naya" / "memory" / "smart-notes" / "index.json"
    entries = read_entries(reg)
    entries[0]["smart_note_id"] = smart_note_id
    write_entries(reg, entries)


def _set_capture_id(root, smart_note_id):
    p = root / ".naya" / "capture" / "SMART-NOTE-SN-001.json"
    doc = json.loads(p.read_text(encoding="utf-8"))
    doc["smart_note_id"] = smart_note_id
    p.write_text(json.dumps(doc), encoding="utf-8")


def test_live_repository_drift_never_grows_per_class():
    """Ratchet: live drift must never grow. Repairs may land freely.

    Deliberately a `<=` check and not exact equality. An equality assertion
    would fail every time someone correctly repairs a defect, and a CI gate
    that cries wolf gets ignored -- which is how a real regression would slip
    through unnoticed. When a class shrinks, lower its pinned value so the
    documented baseline keeps matching reality.
    """
    report = mod.audit_registry()

    for defect_class, pinned in PINNED_BASELINE.items():
        actual = report["counts"][defect_class]
        assert actual <= pinned, (
            f"{defect_class} grew: {pinned} -> {actual}. That is a regression and must be "
            f"investigated before this baseline is changed. Full report: "
            f"{json.dumps(report['defects'], indent=2)}"
        )


def _assert_no_unseen_identity_members(defect_class, actual, pinned):
    unseen = set(actual) - set(pinned)
    assert not unseen, (
        f"{defect_class} introduced previously unseen identity drift: {sorted(unseen)}. "
        "A same-count substitution is still a regression; investigate the new member "
        "before changing the pinned membership."
    )


def test_live_identity_drift_membership_never_expands():
    """Ratchet identity membership, not only counts.

    Count-only gating permits a sideways regression: fix one known defect and
    introduce a different defect in the same class, leaving cardinality equal.
    Exact known-member subsets let repairs shrink freely while rejecting that
    substitution.
    """
    report = mod.audit_registry()
    defects = report["defects"]

    actual = {
        "registry_entries_without_capture_identity": set(
            defects["registry_entries_without_capture_identity"]
        ),
        "captures_without_registry_identity": {
            item["smart_note_id"]
            for item in defects["captures_without_registry_identity"]
        },
        "captures_without_smart_note_id": set(
            defects["captures_without_smart_note_id"]
        ),
        "filename_smart_note_id_divergence": {
            f"{item['capture']}|{item['filename_identity']}|{item['smart_note_id']}"
            for item in defects["filename_smart_note_id_divergence"]
        },
    }

    for defect_class, pinned in PINNED_IDENTITY_MEMBERS.items():
        _assert_no_unseen_identity_members(defect_class, actual[defect_class], pinned)


def test_identity_membership_ratchet_rejects_same_count_substitution():
    """Regression: equal counts do not make a replacement defect acceptable."""
    known = {"SN-OLD"}
    replacement = {"SN-NEW"}
    assert len(known) == len(replacement)

    with pytest.raises(AssertionError, match="SN-NEW"):
        _assert_no_unseen_identity_members(
            "registry_entries_without_capture_identity",
            replacement,
            known,
        )


def test_registry_hash_coverage_is_measured_and_not_silently_zero():
    """Guards the audit trail that PR #1401 removed.

    PR #1401 ("Resolve SN-012 collision + remove unverifiable registry
    hashes") deleted all 16 real content_hash fields, on the stated rationale
    that they "claim runtime block, not verifiable from repo".

    That rationale is empirically false: 15 of the 16 were exactly
    reproducible from repo state alone via
    sha256(json.dumps(capture["intelligence"], sort_keys=True,
    separators=(",", ":"), ensure_ascii=False)).

    Hash coverage is therefore currently 0/28 and the registry cannot prove
    that any entry corresponds to any capture. This test does not assert a
    floor, because restoring the hashes is a Human Director decision on hash
    semantics. It asserts only that the coverage stays *measurable* and
    reports it, so the hole cannot quietly become invisible.
    """
    registry = json.loads((ROOT / ".naya/memory/smart-notes/index.json").read_text(encoding="utf-8"))
    entries = registry["entries"]
    real = [
        e for e in entries
        if isinstance(e.get("content_hash"), str) and re.fullmatch(r"[0-9a-f]{64}", e["content_hash"])
    ]

    coverage = len(real) / len(entries) if entries else 0.0

    assert isinstance(coverage, float)
    # Not a floor assertion on purpose. See docstring: restoration is gated on a
    # Human Director decision, so this asserts measurability, not correctness.
    assert coverage >= 0.0
    print(
        f"\n[smart-note] registry content_hash coverage: {len(real)}/{len(entries)} "
        f"({coverage:.0%}) — 0% means capture<->entry reconciliation is impossible"
    )

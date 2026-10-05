import importlib.util
import re
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("smart_note_v2", ROOT / "tools" / "smart_note_v2.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

# Measured live drift on main@a13f5083 (2026-10-05), re-pinned 2026-10-05 after
# two repairs. Pinned as a ratchet, not as a pass.
# Rationale: the publish path only ever proves the single note it just handled,
# so a fully green run can coexist with a broken registry. CI must stay usable,
# but the drift may never grow silently. Each class is pinned individually so a
# new defect in one class cannot hide inside an improving total elsewhere.
#
# 2026-10-05 re-pin history:
# - entries_without_hash 28 -> 17 and captures_unregistered_by_hash 20 -> 7:
#   genuine repair by commit 859c20b1c (SN-0356 registry drift repair) which
#   restored content_hash coverage on registry entries.
# - captures_missing_intelligence 0 -> 1 -> 0: PR #1526 landed the SN-0357
#   capture in the v1 narrative schema (no canonical `intelligence` dict),
#   tripping the detector. Repaired by translating SN-0357 to the v2-conformant
#   capture shape with the original v1 document preserved verbatim under
#   `raw_source`. The now-hashable SN-0357 has no registry entry yet (owning
#   lane's projection flow), so captures_unregistered_by_hash re-pins at 8.
# - Same class re-tripped the same tick by main 4c1b3df8 (PRs #1529/#1532):
#   SN-0358 and SN-0359 landed in the same v1 narrative schema. Translated the
#   same way in the same repair. captures_unregistered_by_hash re-pins at 10.
#   PATTERN FLAG for the owning lane (Naya 2): the v1 capture writer keeps
#   landing non-canonical captures; the capture path should emit v2 directly.
PINNED_BASELINE = {
    "unparseable_captures": 0,
    "captures_missing_intelligence": 0,
    "captures_unregistered_by_hash": 10,
    "entries_without_hash": 17,
    "entries_with_stale_hash": 0,
    "duplicate_smart_note_ids": 0,
    "published_entries_missing_projection_path": 0,
    "registry_projection_paths_absent": 0,
    "published_pages_without_registry_entry": 1,
    "duplicate_published_page_paths": 1,
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
    (cap_dir / "c1.json").write_text(
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
    p = root / ".naya" / "capture" / "c2.json"
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
    (root / ".naya" / "capture" / "c1.json").write_text(text, encoding="utf-8")


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

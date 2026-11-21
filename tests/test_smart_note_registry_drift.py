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
# but the drift may never grow silently. Each class is pinned individually so a
# new defect in one class cannot hide inside an improving total elsewhere.
#
# ROOT CAUSE NOTE (superseded 2026-11-17, corpus-gate reconciliation):
# the original coupling note described the 28-entry era. The registry has
# since grown to 2,137 entries and the classes decoupled. Measured state
# after the 2026-11-17 reconciliation (Resolve, mechanic lane; full record
# in the completion-drive goal, corpus-gate-20261117/execution.md):
#   - entries_with_stale_hash 94 -> 0: every stale stamp was re-stamped from
#     the capture of record the entry itself names, proven per entry by
#     title equality + capture essence present in the published page +
#     entry page_hash == sha256(page bytes). No content was invented; the
#     stamps had been computed from serializations no longer on disk.
#   - captures_unregistered_by_hash 128 -> 20: the re-stamp bound 94, and
#     the audit now classifies IB-proven superseded captures of registered
#     notes as twin_captures_of_registered_notes (14, pinned below) instead
#     of counting them as unregistered notes. The residual 20 are enumerated:
#     15 captures of hashless entries (hash restoration for those entries is
#     gated on a Human Director decision — see the coverage test below),
#     1 identity-less Hub projection capture (2026-10-01), 1 spare SN-0530
#     capture whose title differs from the entry's (suspected number reuse,
#     SN lane), 1 intelligence body shared by two capture files claiming
#     SN-001 and SN-633 (identity anomaly, SN lane), 2 live-fire test
#     captures SN-9998/SN-9999 (LAW lane lifecycle class).
#     +5 on 2026-11-20 (20 -> 25, measured first-hand at main@aad2db14
#     in the cold-retrieve r5 re-derivation of the #3493 cure onto the moved
#     tip; same 5 as r3/r4 measured at de230305 and 07c2b0c2, byte-identical
#     rows at all three tips): the 5 superseded run-338 captures
#     IB-SMART-NOTE-20261118-sn3549-one-naya-one-standard-live-time,
#     sn3550-the-kit-written-for-the-citizen,
#     sn3551-scorecard-every-return-work-in-parallel,
#     sn3552-one-spine-one-border-every-lane,
#     sn3553-dont-send-it-back-until-ten. Their registry entries pointed
#     at files that no longer exist (collision-repair round 2 moved the
#     pages to new filenames without updating the registry), so every cold
#     retrieve raised INDEX_CORRUPT:PROJECTION_ABSENT and the drift test
#     itself was red on registry_projection_paths_absent 0 -> 5 (r3/r4) and
#     0 -> 10 at aad2db14 (see below). Deleting the 5 entries restores
#     retrieval (cold probe 3/5 -> 5/5) and the 5 captures stay on disk as
#     inert residue because deleting captures is destructive and needs
#     Shawn's word. When he authorizes their deletion, this pin returns
#     to 20. This re-baseline documents a measured, named trade — it does
#     not bless silent drift: the 5 filenames above are the audit trail,
#     and the count may not grow past 25 without a new investigation.
#     SECOND FAMILY at aad2db14 (same run, NOT in this pin): SN-3955..SN-3959
#     are ACTIVE entries pointing at 11/20 VISION projection files the Top Ten
#     door landings created and the SN re-adjudication then removed (each
#     entry's supersession_reason names the SHAs), with no capture files
#     on disk. Their content_hash
#     matches the SN-4203..SN-4207 captures 5/5 — the same 5 notes filed
#     under two number ranges (number collision). They are RETIRED, not
#     deleted (lifecycle SUPERSEDED + superseded_by_capture_id naming the
#     SN-4203..SN-4207 capture + supersession_reason on each entry):
#     deleting them would make the ids VANISH (no capture on disk for the
#     old numbers — the vanish guard would gain 5 ids), while retirement
#     keeps the ids registered and the retrieval validator skips inactive
#     entries. Consequence, stated not hidden: audit_registry counts
#     retired entries' absent paths, so registry_projection_paths_absent
#     reads 5 after this cure (10 -> 5) and the drift test stays red on
#     that class (pin 0, deliberately NOT raised) plus
#     published_pages_without_registry_entry 44 (pin 4, deliberately NOT
#     raised — the unregistered band SN-4203..SN-4207 + SN-4256..SN-4258).
#     The remaining 5 absent paths are the reconciliation lane's to cure:
#     register SN-4203..SN-4207, then the retired rows can go once
#     SN-3955..SN-3959 captures exist.
PINNED_BASELINE = {
    "unparseable_captures": 0,
    "captures_missing_intelligence": 0,
    "captures_unregistered_by_hash": 25,
    "twin_captures_of_registered_notes": 14,
    "entries_without_hash": 28,
    "entries_with_stale_hash": 0,
    "duplicate_smart_note_ids": 0,
    "published_entries_missing_projection_path": 0,
    "registry_projection_paths_absent": 0,
    "published_pages_without_registry_entry": 4,
    # 4 since 2026-10-24 (was 1 at pin time, 23 at main@782cbe2c): the
    # 19-orphan door-filing backlog SN-0834..SN-0852+SN-1852 was cured by
    # the door-obligation fixer (captures + registry entries, PR pending).
    # Remaining 4 are NOT fixable by the orphan cure: SN-0842's IB note +
    # founding-portrait share one public id (DUPLICATE_PUBLIC_ID — the
    # Smart Note identity lane must reconcile first), and the legacy
    # smart-note.md group + the-naya-tool-set.md are structural
    # (cure-lane decision, pre-existing).
    # 2026-11-17 MEASUREMENT (corpus-gate pass): the class reads 31 records
    # (48 paths) and this pin is deliberately NOT raised. The audit's own
    # orphan decomposition proves the growth is not new unregistered notes:
    # truly_unregistered = 0; id_collision = 28 paths (second renderings and
    # companion documents of numbers registered to a different page — the
    # SN lane's dual-rendering reconciliation, incl. the SN-2055..SN-2094
    # and SN-2203 dated renderings); no_id = 20 paths (legacy v7-layout
    # IB-000035..IB-000052 pages + companions, structural). The ratchet
    # stays red on this class until that reconciliation lands; raising the
    # pin would bless the debt instead of curing it.
    # 0 since w569: re-keyed on content collision within leaf-name groups
    # (Delta) -- the layout convention puts a smart-note.md in every note's
    # own directory, and distinct notes may share a slug leaf with different
    # content. Bare-leaf keying manufactured false positives; the class now
    # fires only on byte-identical double-publications.
    "duplicate_published_page_paths": 0,
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


def _add_retired_twin(root):
    """A SUPERSEDED entry sharing the live entry's hash and pointing at a
    removed file — the SN-3955..SN-3959 tombstone shape. Must not fire."""
    reg = root / ".naya" / "memory" / "smart-notes" / "index.json"
    entries = read_entries(reg)
    twin = dict(entries[0])
    twin["smart_note_id"] = "SN-002"
    twin["intelligent_block_id"] = "IB-2"
    twin["lifecycle_state"] = "SUPERSEDED"
    twin["projection_path"] = PAGE.replace("IB-1.md", "IB-REMOVED.md")
    entries.append(twin)
    write_entries(reg, entries)


def test_inactive_entries_do_not_fire_drift_but_active_ones_do(tmp_path):
    """Retired rows are audit trail: same hash + absent path must stay green
    while SUPERSEDED, and must fire the moment the row is ACTIVE again."""
    reg_path = build_clean_root(tmp_path)
    assert mod.audit_registry(root=tmp_path)["ok"] is True, "fixture must start clean"

    _add_retired_twin(tmp_path)
    retired = mod.audit_registry(root=tmp_path)
    assert retired["counts"]["duplicate_smart_note_ids"] == 0, retired["defects"]
    assert retired["counts"]["registry_projection_paths_absent"] == 0, retired["defects"]
    assert retired["ok"] is True, retired["defects"]

    entries = read_entries(reg_path)
    entries[1]["lifecycle_state"] = "ACTIVE"
    write_entries(reg_path, entries)
    active = mod.audit_registry(root=tmp_path)
    assert active["ok"] is False, "detector must still catch live drift"
    assert active["counts"]["duplicate_smart_note_ids"] >= 1, active["defects"]
    assert active["counts"]["registry_projection_paths_absent"] >= 1, active["defects"]


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



def test_windows_long_path_registered_and_true_missing(tmp_path):
    """Long Windows projection paths are not silent registry drift.

    The standard Windows pathlib existence check may return False after
    MAX_PATH even though Git and extended-length Win32 paths contain
    the bytes. The genuine-missing control must still be refused.
    """
    import os
    if os.name != "nt":
        pytest.skip("Windows path-length behavior is platform-specific")
    reg_path = build_clean_root(tmp_path)
    original = tmp_path / PAGE
    original.unlink()
    long_relative = (
        Path("BRAIN/05-MEMORY/SMART-NOTES")
        / ("alpha-" + "x" * 75)
        / ("beta-" + "y" * 75)
        / "IB-1.md"
    )
    target = tmp_path / long_relative
    assert len(str(target)) > 260
    extended = Path("\\\\?\\" + str(target))
    extended.parent.mkdir(parents=True, exist_ok=True)
    extended.write_text("# IB-1\\n", encoding="utf-8")
    assert extended.is_file()
    entries = read_entries(reg_path)
    entries[0]["projection_path"] = long_relative.as_posix()
    write_entries(reg_path, entries)

    valid = mod.audit_registry(root=tmp_path)
    assert valid["counts"]["registry_projection_paths_absent"] == 0, valid["defects"]

    extended.unlink()
    missing = mod.audit_registry(root=tmp_path)
    assert missing["counts"]["registry_projection_paths_absent"] == 1, missing["defects"]

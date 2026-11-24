"""Consumer fail-closed for the feed (SN-4711, the Sealed Door — cure 2).

Origin: the graduation red-team (2026-11-24) proved a forged-receipt
filing is DETECTED — the door checker names it CHAIN_BROKEN and the
brain index excludes it — yet the feed tool still emitted its card,
because --rebuild-set derived its set from lifecycle_state alone and
never consulted chain standing. Cure 2: in --rebuild-set mode the feed
derives its set from ACTIVE entries MINUS the entries the checker
judges CHAIN_BROKEN. The verdict is the checker's own
(check_door_obligation.check_chain), loaded and called — the same
wiring regenerate_brain_index.py's verified set uses; no second
implementation of the chain rule lives in the feed tool.

These tests hit that real seam against fixture roots built like
tests/test_regenerate_brain_index_verified_set.py's (real tool copies
in the fixture root), over a three-entry chain state minted with
smart_note_v2's own door_receipt_for (the single minting authority):

  - a genuine stamped entry and a legacy unstamped entry emit cards;
  - a forged entry (receipt computed against the genesis prev instead
    of the live tail) emits NO card — fresh or pre-existing — and is
    named once in report["dropped_chain_broken"];
  - rebuild_feed without a verdict derives the pre-cure set (the
    opt-in seam; main() always passes the verdict);
  - the CLI fails closed (exit 2, CHAIN_UNVERIFIABLE) when the chain
    verdict cannot be computed, writing nothing;
  - preserve mode (no --rebuild-set) is untouched by the chain: the
    existing set is preserved exactly, forged card included.

Run:  python -m pytest tests/test_regenerate_feed_live_chain.py -q
"""

import importlib.util
import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FEED_TOOL = ROOT / "tools" / "regenerate_feed_live.py"
CHECKER = ROOT / "tools" / "check_door_obligation.py"
SNV2 = ROOT / "tools" / "smart_note_v2.py"
GUARD = ROOT / "tools" / "truth_state_guard.py"
APPLICABILITY = ROOT / "tools" / "applicability.py"

LEGACY_IB = "IB-FEED-CHAIN-LEGACY"
GENUINE_IB = "IB-FEED-CHAIN-GENUINE"
FORGED_IB = "IB-FEED-CHAIN-FORGED"
GENESIS = "0" * 64


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def make_root(tmp_path: Path) -> Path:
    """A fixture checkout: the real tools under tools/, a three-entry
    chain corpus (legacy + genuine + forged) on disk."""
    (tmp_path / "tools").mkdir(parents=True)
    for src in (FEED_TOOL, CHECKER, SNV2, GUARD, APPLICABILITY):
        shutil.copy(src, tmp_path / "tools" / src.name)
    snv2 = _load(tmp_path / "tools" / "smart_note_v2.py", "snv2_fixture")
    brain = tmp_path / "BRAIN" / "05-MEMORY" / "SMART-NOTES"
    brain.mkdir(parents=True)
    cap_dir = tmp_path / ".naya" / "capture"
    cap_dir.mkdir(parents=True)
    (tmp_path / "HUB" / "app").mkdir(parents=True)

    def note(sn, ib, page_name, lesson, stamp_prev):
        page_rel = f"BRAIN/05-MEMORY/SMART-NOTES/{page_name}"
        (brain / page_name).write_text(
            f"# {sn}\n\n## In a Nutshell\n\n{lesson}\n", encoding="utf-8")
        page_hash = snv2._page_file_hash(tmp_path / page_rel)
        capture = {
            "smart_note_id": sn,
            "intelligent_block_id": ib,
            "file": page_rel,
            "title": lesson,
            "created_at": "2026-11-24T00:00:00Z",
            "intelligence": {"essence": lesson},
        }
        entry = {
            "smart_note_id": sn,
            "intelligent_block_id": ib,
            "title": lesson,
            "topic": "GOVERNANCE",
            "projection_path": page_rel,
            "lifecycle_state": "ACTIVE",
            "page_hash": page_hash,
            "content_hash": f"content-{sn}",
            "capture_file": f".naya/capture/{ib}.json",
            "registered_at": "2026-11-24T00:00:00Z",
        }
        if stamp_prev is not None:
            capture["published_via"] = "publish-note"
            capture["door_version"] = "1"
            capture["door_receipt"] = snv2.door_receipt_for(
                capture, page_hash, stamp_prev)
            entry["published_via"] = "publish-note"
            entry["door_version"] = "1"
            entry["door_receipt"] = capture["door_receipt"]
        (cap_dir / f"{ib}.json").write_text(json.dumps(capture),
                                            encoding="utf-8")
        return entry

    entries = [
        note("SN-9001", LEGACY_IB, "legacy.md",
             "legacy chain anchor words", None),
        note("SN-9002", GENUINE_IB, "genuine.md",
             "genuine stamped note zeppelin", "content-SN-9001"),
        note("SN-9003", FORGED_IB, "forged.md",
             "quixotic forgery unikat", GENESIS),
    ]
    registry = {
        "schema": "naya.smart-note-projection-index.v1",
        "entries": entries,
        "corpus_manifest_hash": snv2._corpus_manifest_hash(entries),
    }
    reg_path = tmp_path / ".naya" / "memory" / "smart-notes" / "index.json"
    reg_path.parent.mkdir(parents=True)
    reg_path.write_text(json.dumps(registry), encoding="utf-8")
    (tmp_path / "HUB" / "app" / "feed-live.json").write_text(
        json.dumps({"generated_from": "fixture", "count": 0, "notes": []}),
        encoding="utf-8")
    return tmp_path


def _feed_mod(root: Path):
    return _load(root / "tools" / "regenerate_feed_live.py", "feed_fixture")


def _report():
    return {"cards": 0, "layers_added": 0, "bodies_refreshed": 0,
            "no_page": [], "no_capture": [], "incomplete": {},
            "preserved": 0, "fresh": 0, "dropped_not_active": [],
            "dropped_no_registry": []}


def _registry(root: Path):
    return json.loads(
        (root / ".naya" / "memory" / "smart-notes" / "index.json")
        .read_text(encoding="utf-8"))


def test_chain_broken_ibs_matches_the_checkers_verdict(tmp_path):
    root = make_root(tmp_path)
    feed = _feed_mod(root)
    assert feed.chain_broken_ibs(_registry(root)) == {FORGED_IB}


def test_rebuild_set_excludes_the_forged_entry(tmp_path):
    root = make_root(tmp_path)
    feed = _feed_mod(root)
    registry = _registry(root)
    report = _report()
    new_feed = feed.rebuild_feed(registry, {"notes": []}, report,
                                 feed.chain_broken_ibs(registry))
    ids = {c["id"] for c in new_feed["notes"]}
    assert ids == {LEGACY_IB, GENUINE_IB}
    assert report["dropped_chain_broken"] == [FORGED_IB]


def test_rebuild_without_verdict_keeps_the_precure_set(tmp_path):
    root = make_root(tmp_path)
    feed = _feed_mod(root)
    report = _report()
    new_feed = feed.rebuild_feed(_registry(root), {"notes": []}, report)
    ids = {c["id"] for c in new_feed["notes"]}
    assert ids == {LEGACY_IB, GENUINE_IB, FORGED_IB}
    assert "dropped_chain_broken" not in report


def test_existing_card_for_forged_entry_is_dropped(tmp_path):
    root = make_root(tmp_path)
    feed = _feed_mod(root)
    registry = _registry(root)
    existing = {"notes": [{"id": FORGED_IB, "layers": []},
                          {"id": GENUINE_IB, "layers": []}]}
    report = _report()
    new_feed = feed.rebuild_feed(registry, existing, report,
                                 feed.chain_broken_ibs(registry))
    ids = {c["id"] for c in new_feed["notes"]}
    assert FORGED_IB not in ids
    assert GENUINE_IB in ids
    # Named exactly once, by the up-front partition — not once per loop.
    assert report["dropped_chain_broken"] == [FORGED_IB]


def _run_cli(root: Path, *args):
    return subprocess.run(
        [sys.executable, str(root / "tools" / "regenerate_feed_live.py"),
         *args],
        cwd=root, capture_output=True, text=True)


def test_cli_rebuild_set_excludes_forged_and_reports(tmp_path):
    root = make_root(tmp_path)
    report_path = root / "report.json"
    r = _run_cli(root, "--rebuild-set", "--check", "--report",
                 str(report_path))
    assert r.returncode == 0, r.stderr
    report = json.loads(report_path.read_text(encoding="utf-8"))
    assert report["cards"] == 2
    assert report["active_entries"] == 3
    assert report["dropped_chain_broken"] == [FORGED_IB]


def test_cli_fails_closed_when_the_verdict_cannot_be_computed(tmp_path):
    root = make_root(tmp_path)
    (root / "tools" / "check_door_obligation.py").unlink()
    feed_path = root / "HUB" / "app" / "feed-live.json"
    before = feed_path.read_bytes()
    r = _run_cli(root, "--rebuild-set")
    assert r.returncode == 2
    assert "CHAIN_UNVERIFIABLE" in r.stderr
    assert feed_path.read_bytes() == before


def test_preserve_mode_is_untouched_by_the_chain(tmp_path):
    root = make_root(tmp_path)
    feed_path = root / "HUB" / "app" / "feed-live.json"
    feed_path.write_text(json.dumps({
        "generated_from": "fixture", "count": 1,
        "notes": [{"id": FORGED_IB, "layers": []}],
    }), encoding="utf-8")
    r = _run_cli(root)
    assert r.returncode == 0, r.stderr
    out = json.loads(feed_path.read_text(encoding="utf-8"))
    assert [c["id"] for c in out["notes"]] == [FORGED_IB]

"""Publish-note classic path: the door speaks the corpus dialect.

Origin: 2026-11-17. The canonical publishing door
(tools/learning_loop.py publish-note) only accepted the persisted-block
capture shape and rendered the emoji dialect whose MACHINE NOTE is a
JSON dump. The corpus's production notes — distillation batches 1-3,
SN-2832 — are flat captures (schema naya.smart-note-capture.v2) rendered
in the classic nine-section dialect, and the distillation census counts
coverage only from a parseable `Distills ...` line, which the emoji
render cannot carry. Batch 3 therefore had to honor the door's invariant
in substance instead of using the subcommand (P-152: a door the real
work cannot walk through gets walked around — that is the leak).

These tests pin the upgraded door (smart_note_v2.publish_classic +
the publish-note dispatch):

  - a flat classic capture publishes end-to-end: capture placed first
    with writer-stamped hashes, classic page at the corpus-layout path,
    corpus-standard registry entry, manifest re-stamped;
  - a declared Distills coverage line renders in the MACHINE section
    and parses under the REAL census grammar
    (tools/distillation_machine.py parse_distills);
  - the door fails closed: capture-name collision with different bytes,
    an SN owned by a different block, an IB re-registered with different
    hashes, a missing section, a missing explicit SN;
  - re-publishing the identical capture is idempotent.

Run:  python -m pytest tests/test_publish_note_classic.py -q
"""

import hashlib
import importlib.util
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


def _load(name, rel):
    spec = importlib.util.spec_from_file_location(name, ROOT / rel)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


snv2 = _load("smart_note_v2_classic", "tools/smart_note_v2.py")
census = _load("distillation_machine_classic", "tools/distillation_machine.py")

IB = "IB-SMART-NOTE-20261117-sn9101-the-door-must-fit-the-work"
PAGE_REL = ("BRAIN/05-MEMORY/SMART-NOTES/2026/11/17/LESSON/SN-9101/"
            + IB + ".md")


def _capture(**overrides):
    cap = {
        "schema": "naya.smart-note-capture.v2",
        "smart_note_id": "SN-9101",
        "title": "The Door Must Fit the Work",
        "slug": "the-door-must-fit-the-work",
        "tone": "purple",
        "icon": "◆",
        "created_at": "2026-11-17T23:00:00Z",
        "registered_by": "naya-resolve",
        "kind": "intelligent-block",
        "category": "SYSTEM",
        "topic": "LESSON",
        "intelligence": {
            "essence": "The essence of the fixture note.",
            "human_view": "The human view of the fixture note.",
            "child_view": "The child view of the fixture note.",
            "grandma_view": "The grandma view of the fixture note.",
            "ai_view": "The naya view of the fixture note.",
            "what_it_means": "What the fixture note means.",
            "whats_inside": ["one", "two", "three", "four", "five"],
            "topics": ["System", "Lesson"],
        },
        "page": {
            "machine": "Machine rules of the fixture note.",
            "why_it_matters": "Why the fixture note matters.",
            "how_it_connects": "How the fixture note connects.",
            "what_is_in_it_for_you": "What the fixture note gives you.",
            "the_learning": "The learning of the fixture note.",
        },
    }
    cap.update(overrides)
    return cap


@pytest.fixture()
def door_root(tmp_path, monkeypatch):
    reg = tmp_path / ".naya" / "memory" / "smart-notes" / "index.json"
    reg.parent.mkdir(parents=True)
    reg.write_text(json.dumps({
        "schema": "naya.smart-note-projection-index.v1",
        "version": "1.0",
        "source_of_truth": "runtime_intelligent_block",
        "entries": [],
        "sequence_policy": {"human_id_format": "SN-###", "next_sequence": 9102},
        "corpus_manifest_hash": snv2._corpus_manifest_hash([]),
    }, indent=2) + "\n", encoding="utf-8")
    (tmp_path / ".naya" / "capture").mkdir(parents=True)
    monkeypatch.setattr(snv2, "ROOT", tmp_path)
    monkeypatch.setattr(snv2, "REGISTRY", reg)
    monkeypatch.setattr(snv2, "BRAIN_SMART_NOTE_ROOT",
                        tmp_path / "BRAIN" / "05-MEMORY" / "SMART-NOTES")
    return tmp_path


def _registry(root):
    return json.loads((root / ".naya" / "memory" / "smart-notes"
                       / "index.json").read_text(encoding="utf-8"))


def test_classic_publish_end_to_end(door_root):
    entry, page_path = snv2.publish_classic(_capture(), capture_source=None)
    assert entry["smart_note_id"] == "SN-9101"
    assert page_path == door_root / PAGE_REL
    text = page_path.read_text(encoding="utf-8")
    # Classic dialect, exact section set, no emoji dialect markers.
    for header in ("## IN A NUTSHELL", "## HUMAN", "## CHILD", "## GRANDMA",
                   "## NAYA", "## MACHINE", "## WHAT IT ALL MEANS",
                   "## WHY IT MATTERS", "## HOW IT CONNECTS",
                   "## WHAT IS IN IT FOR YOU", "## THE LEARNING"):
        assert header in text, header
    assert "MACHINE NOTE" not in text
    assert "~~~json" not in text
    assert text.startswith("# The Door Must Fit the Work\n\n"
                           "SN-9101 · LESSON / SMART NOTE\n\n"
                           "**Created:** 2026-11-17T23:00:00Z")
    # Capture placed with writer-stamped hashes that recompute.
    cap = json.loads((door_root / ".naya" / "capture"
                      / (IB + ".json")).read_text(encoding="utf-8"))
    assert cap["file"] == PAGE_REL
    assert cap["page_hash"] == hashlib.sha256(
        page_path.read_bytes()).hexdigest()
    assert cap["content_hash"] == snv2._canonical_content_hash(json.dumps(
        cap["intelligence"], sort_keys=True, separators=(",", ":"),
        ensure_ascii=False))
    # Registry: one entry, hashes bound, manifest recomputes.
    reg = _registry(door_root)
    assert [e["smart_note_id"] for e in reg["entries"]] == ["SN-9101"]
    assert reg["entries"][0]["page_hash"] == cap["page_hash"]
    assert reg["entries"][0]["content_hash"] == cap["content_hash"]
    assert reg["entries"][0]["capture_file"] == ".naya/capture/" + IB + ".json"
    assert reg["corpus_manifest_hash"] == snv2._corpus_manifest_hash(
        reg["entries"])


def test_classic_publish_distills_line_parses_under_census_grammar(door_root):
    cap = _capture()
    cap["page"]["distills"] = {
        "batch": 4, "of": 100,
        "covers": [{"sn": "SN-0927", "title": "Filing Is Useless Without Learning"},
                   {"sn": "SN-1787", "title": "The Lesson Law"}],
    }
    entry, page_path = snv2.publish_classic(cap, capture_source=None)
    text = page_path.read_text(encoding="utf-8")
    line = ("Distills (Batch 4, 2 of 100): SN-0927 Filing Is Useless "
            "Without Learning · SN-1787 The Lesson Law")
    assert line in text
    assert "LESSON / DISTILLATION" in text
    # The REAL census parser must read exactly the declared coverage.
    assert census.parse_distills(text) == {927, 1787}
    assert entry["smart_note_id"] == "SN-9101"


def test_classic_publish_idempotent_republish(door_root):
    cap = _capture()
    first, _ = snv2.publish_classic(cap, capture_source=None)
    second, _ = snv2.publish_classic(cap, capture_source=None)
    assert first == second
    assert len(_registry(door_root)["entries"]) == 1


def test_classic_publish_capture_name_collision_fails_closed(door_root):
    dest = door_root / ".naya" / "capture" / (IB + ".json")
    dest.write_text('{"schema": "someone else"}', encoding="utf-8")
    with pytest.raises(SystemExit, match="CLASSIC_CAPTURE_NAME_COLLISION"):
        snv2.publish_classic(_capture(), capture_source=None)
    assert not (door_root / PAGE_REL).exists()
    assert _registry(door_root)["entries"] == []


def test_classic_publish_sn_owned_by_another_block_fails_closed(door_root):
    reg = _registry(door_root)
    reg["entries"].append({
        "smart_note_id": "SN-9101",
        "intelligent_block_id": "IB-SOMEONE-ELSE",
        "content_hash": "x", "page_hash": "y",
    })
    reg["corpus_manifest_hash"] = snv2._corpus_manifest_hash(reg["entries"])
    (door_root / ".naya" / "memory" / "smart-notes"
     / "index.json").write_text(json.dumps(reg, indent=2) + "\n",
                                encoding="utf-8")
    with pytest.raises(SystemExit, match="SMART_NOTE_ID_COLLISION"):
        snv2.publish_classic(_capture(), capture_source=None)


def test_classic_publish_missing_section_fails_closed(door_root):
    cap = _capture()
    del cap["page"]["the_learning"]
    with pytest.raises(SystemExit, match="CLASSIC_CAPTURE_EMPTY_PAGE_SECTION"):
        snv2.publish_classic(cap, capture_source=None)
    assert _registry(door_root)["entries"] == []


def test_classic_publish_requires_explicit_sn(door_root):
    cap = _capture()
    del cap["smart_note_id"]
    with pytest.raises(SystemExit, match="EXPLICIT_SMART_NOTE_ID"):
        snv2.publish_classic(cap, capture_source=None)


# ---------------------------------------------------------------------------
# The Sealed Door — writer-side receipt chain (SN-4711, build step 1).
# The door mints published_via / door_version / door_receipt onto every
# capture it files, chained to the previous registry entry's
# content_hash (genesis prev = 64 zero hex chars); register_classic
# re-verifies the stamp inside its transaction and refuses a stale one.

GENESIS_PREV = "0" * 64
IB2 = "IB-SMART-NOTE-20261117-sn9102-the-second-note-chains"
IB3 = "IB-SMART-NOTE-20261117-sn9103-the-third-note-chains"


def _expected_receipt(cap, prev_content_hash):
    """Hand recomputation of the SN-4711 receipt, independent of the
    writer's helper: sha256(canon(capture_without_receipt) || page_hash
    || prev_content_hash)."""
    without = {k: v for k, v in cap.items() if k != "door_receipt"}
    canon = json.dumps(without, sort_keys=True, separators=(",", ":"),
                       ensure_ascii=False)
    return hashlib.sha256(
        (canon + cap["page_hash"] + prev_content_hash).encode("utf-8")
    ).hexdigest()


def _placed_capture(root, ib):
    return json.loads((root / ".naya" / "capture"
                       / (ib + ".json")).read_text(encoding="utf-8"))


def _chain_walk(root):
    """Recompute every door receipt in stored registry order from the
    placed captures: [(smart_note_id, stored_receipt, recomputed)]."""
    out = []
    prev = GENESIS_PREV
    for e in _registry(root)["entries"]:
        if e.get("door_receipt"):
            cap = _placed_capture(root, e["intelligent_block_id"])
            out.append((e["smart_note_id"], e["door_receipt"],
                        _expected_receipt(cap, prev)))
        prev = e["content_hash"]
    return out


def test_door_receipt_genesis_stamped_on_capture_and_entry(door_root):
    entry, _ = snv2.publish_classic(_capture(), capture_source=None)
    cap = _placed_capture(door_root, IB)
    assert cap["published_via"] == "publish-note"
    assert cap["door_version"] == snv2.DOOR_VERSION
    # Genesis: the entries array was empty, so prev is 64 zero hex chars.
    assert cap["door_receipt"] == _expected_receipt(cap, GENESIS_PREV)
    assert entry["published_via"] == "publish-note"
    assert entry["door_version"] == cap["door_version"]
    assert entry["door_receipt"] == cap["door_receipt"]
    stored = _registry(door_root)["entries"][0]
    assert stored["door_receipt"] == cap["door_receipt"]


def test_door_receipt_second_entry_chains_to_first(door_root):
    first, _ = snv2.publish_classic(_capture(), capture_source=None)
    second, _ = snv2.publish_classic(
        _capture(smart_note_id="SN-9102", slug="the-second-note-chains",
                 title="The Second Note Chains"),
        capture_source=None)
    cap2 = _placed_capture(door_root, IB2)
    assert cap2["door_receipt"] == _expected_receipt(
        cap2, first["content_hash"])
    assert cap2["door_receipt"] != _expected_receipt(cap2, GENESIS_PREV)
    assert second["door_receipt"] == cap2["door_receipt"]
    assert all(stored == recomputed
               for _, stored, recomputed in _chain_walk(door_root))


def test_door_receipt_chains_over_preexisting_legacy_tail(door_root):
    # A registry that already holds unchained legacy entries: the first
    # door-minted entry chains to the legacy tail's content_hash — the
    # chain starts over the pre-existing set, nothing is retro-stamped.
    reg = _registry(door_root)
    reg["entries"].append({
        "smart_note_id": "SN-9000",
        "intelligent_block_id": "IB-LEGACY-TAIL",
        "content_hash": "a" * 64, "page_hash": "b" * 64,
    })
    reg["corpus_manifest_hash"] = snv2._corpus_manifest_hash(reg["entries"])
    (door_root / ".naya" / "memory" / "smart-notes"
     / "index.json").write_text(json.dumps(reg, indent=2) + "\n",
                                encoding="utf-8")
    entry, _ = snv2.publish_classic(_capture(), capture_source=None)
    cap = _placed_capture(door_root, IB)
    assert cap["door_receipt"] == _expected_receipt(cap, "a" * 64)
    assert entry["door_receipt"] == cap["door_receipt"]
    legacy = _registry(door_root)["entries"][0]
    assert "door_receipt" not in legacy


def test_door_receipt_tampered_middle_breaks_verification(door_root):
    snv2.publish_classic(_capture(), capture_source=None)
    snv2.publish_classic(
        _capture(smart_note_id="SN-9102", slug="the-second-note-chains",
                 title="The Second Note Chains"),
        capture_source=None)
    snv2.publish_classic(
        _capture(smart_note_id="SN-9103", slug="the-third-note-chains",
                 title="The Third Note Chains"),
        capture_source=None)
    assert all(stored == recomputed
               for _, stored, recomputed in _chain_walk(door_root))
    # Tamper with the middle note's placed capture: its stored receipt
    # no longer recomputes, while its neighbours still verify — the
    # break is exactly at the tampered entry.
    dest = door_root / ".naya" / "capture" / (IB2 + ".json")
    cap2 = _placed_capture(door_root, IB2)
    cap2["title"] += " (tampered)"
    dest.write_text(json.dumps(cap2, indent=1, ensure_ascii=False) + "\n",
                    encoding="utf-8")
    walk = {sn: stored == recomputed
            for sn, stored, recomputed in _chain_walk(door_root)}
    assert walk == {"SN-9101": True, "SN-9102": False, "SN-9103": True}


def test_door_receipt_stale_stamp_refused(door_root):
    snv2.publish_classic(_capture(), capture_source=None)
    # Hand-mint a stamp for a second note against the GENESIS prev —
    # stale, because the registry tail is now the first note. The
    # transaction's re-verification must refuse it.
    cap2 = _capture(smart_note_id="SN-9102",
                    slug="the-second-note-chains",
                    title="The Second Note Chains")
    text, parts = snv2.render_classic_text(cap2)
    page_hash = hashlib.sha256(text.encode("utf-8")).hexdigest()
    content_hash = snv2._canonical_content_hash(json.dumps(
        parts["intelligence"], sort_keys=True, separators=(",", ":"),
        ensure_ascii=False))
    final = dict(cap2)
    final["file"] = parts["rel_path"]
    final["page_hash"] = page_hash
    final["content_hash"] = content_hash
    final["published_via"] = "publish-note"
    final["door_version"] = snv2.DOOR_VERSION
    final["door_receipt"] = _expected_receipt(final, GENESIS_PREV)
    with pytest.raises(SystemExit, match="DOOR_RECEIPT_REGISTRY_MOVED"):
        snv2.register_classic(final, page_hash, content_hash)
    assert len(_registry(door_root)["entries"]) == 1


def test_door_receipt_idempotent_republish_keeps_stamp(door_root):
    cap = _capture()
    first, _ = snv2.publish_classic(cap, capture_source=None)
    dest = door_root / ".naya" / "capture" / (IB + ".json")
    bytes_first = dest.read_bytes()
    second, _ = snv2.publish_classic(cap, capture_source=None)
    assert first == second
    assert dest.read_bytes() == bytes_first
    assert len(_registry(door_root)["entries"]) == 1


def test_door_receipt_caller_supplied_stamp_is_discarded(door_root):
    # The stamp is minted only inside the door: door fields arriving on
    # the caller's capture never survive into the placed capture.
    cap = _capture()
    cap["published_via"] = "hand-forged"
    cap["door_version"] = "999"
    cap["door_receipt"] = "f" * 64
    entry, _ = snv2.publish_classic(cap, capture_source=None)
    placed = _placed_capture(door_root, IB)
    assert placed["published_via"] == "publish-note"
    assert placed["door_version"] == snv2.DOOR_VERSION
    assert placed["door_receipt"] == _expected_receipt(placed, GENESIS_PREV)
    assert entry["door_receipt"] == placed["door_receipt"]


def test_publish_note_cli_dispatches_flat_capture(door_root, tmp_path, capsys):
    # The door itself (learning_loop.publish-note without --verify) must
    # route a flat capture to the classic path.
    monkey_mod = sys.modules.get("smart_note_v2")
    sys.modules["smart_note_v2"] = snv2
    try:
        loop = _load("learning_loop_classic", "tools/learning_loop.py")
        src = tmp_path / "src-capture.json"
        src.write_text(json.dumps(_capture()), encoding="utf-8")
        rc = loop._publish_note_main(["--capture", str(src)])
    finally:
        if monkey_mod is None:
            sys.modules.pop("smart_note_v2", None)
        else:
            sys.modules["smart_note_v2"] = monkey_mod
    assert rc == 0
    out = json.loads(capsys.readouterr().out)
    assert out["ok"] is True
    assert out["smart_note_id"] == "SN-9101"
    assert (door_root / PAGE_REL).exists()
    assert len(_registry(door_root)["entries"]) == 1

"""Verified-set corpus for the brain index (SN-4711, the Sealed Door,
consumer backstop — design step 6 / build step 5).

Origin: the brain index absorbed every BRAIN/ file mechanically, so a
Smart Note page filed around the publish-note door (no capture, no
registry entry — the filed-but-unregistered band behind 32 registry
cures) was silently legitimized by the index and even raised the
05-MEMORY floor that was supposed to guard deletions. SN-4711's
backstop: regenerate_brain_index.py builds its corpus from pages that
carry a VERIFIED registry entry (entry present, hashes bind, chain /
ratchet / reconstruction standing valid); a bare page is reported as
UNREGISTERED_PAGE and excluded, never absorbed.

Verification is the door checker's own machinery
(tools/check_door_obligation.py), loaded and called — these tests hit
that real seam against fixture roots built exactly like
tests/test_door_obligation.py's (real tool copies, a manifest-clean
empty registry, the checker's own --fix as the registering writer):

  - a bare page is unregistered (NO_ENTRY) and excluded from the
    corpus, while non-page files and non-SMART-NOTES files stay;
  - the same page, once the fixer registers it, is verified;
  - tampering with a registered page's bytes breaks its page_hash
    binding and it drops out of the verified set (PAGE_HASH_STALE);
  - a hashless legacy entry whose only defect (NO_CAPTURE) is carried
    by the shrink-only grandfather ratchet stays verified — and loses
    verification the moment the ratchet does not carry it;
  - the generated REAL-TREE documents name the excluded pages only
    when there are any (the all-verified shape is byte-for-byte the
    legacy shape);
  - floors are recomputed over the verified set: excluding a page
    lowers the 05-MEMORY floor by exactly that page, so the exclusion
    itself never trips the deletion ratchet.

Run:  python -m pytest tests/test_regenerate_brain_index_verified_set.py -q
"""

import importlib.util
import json
import shutil
import subprocess
import sys
from pathlib import Path

from tools import regenerate_brain_index as brain_index

ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / "tools" / "check_door_obligation.py"
SNV2 = ROOT / "tools" / "smart_note_v2.py"

PAGE_REL = ("BRAIN/05-MEMORY/SMART-NOTES/2026/10/21/SYSTEM/protocol/"
            "SN-0810/IB-SMART-NOTE-20261021-sn0810-door-fixture.md")
IB = "IB-SMART-NOTE-20261021-sn0810-door-fixture"
SN = "SN-0810"

PAGE = """# Door Fixture Note

**ID:** IB-SMART-NOTE-20261021-sn0810-door-fixture
**Created:** 2026-10-21
**Category:** SYSTEM / Protocol

## IN A NUTSHELL

The fixture essence.

## HUMAN

The human view.

## CHILD

The child view.

## GRANDMA

The grandma view.

## NAYA

The naya view.

## MACHINE

The machine section in prose.

## WHAT IT ALL MEANS

The synthesis.

## WHAT'S IN IT FOR YOU

The benefit.

## HOW IT APPLIES

The application.
"""

# The true manifest of an empty entries array —
# snv2._corpus_manifest_hash([]) — so the fixture registry is
# manifest-clean (same fixture constant as test_door_obligation.py).
EMPTY_MANIFEST = ("4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873"
                  "c2f11161202b945")


def make_root(tmp_path: Path) -> Path:
    (tmp_path / "tools").mkdir(parents=True)
    shutil.copy(SNV2, tmp_path / "tools" / "smart_note_v2.py")
    shutil.copy(CHECKER, tmp_path / "tools" / "check_door_obligation.py")
    reg = tmp_path / ".naya" / "memory" / "smart-notes"
    reg.mkdir(parents=True)
    (reg / "index.json").write_text(json.dumps({
        "schema": "naya.smart-note-projection-index.v1",
        "version": "1.0",
        "source_of_truth": "runtime_intelligent_block",
        "entries": [],
        "sequence_policy": {"human_id_format": "SN-###",
                            "next_sequence": 810},
        "corpus_manifest_hash": EMPTY_MANIFEST,
    }), encoding="utf-8")
    (tmp_path / ".naya" / "capture").mkdir(parents=True)
    return tmp_path


def write_page(root: Path) -> Path:
    p = root / PAGE_REL
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(PAGE, encoding="utf-8")
    return p


def _f(path: str) -> dict:
    return {"path": path, "sha": "a" * 40, "size": 100}


def inventory_fixture() -> list[dict]:
    """Inventory rows for the fixture tree: the SN page, a non-page
    file under SMART-NOTES/, and an ordinary BRAIN/ file elsewhere."""
    return [
        _f(PAGE_REL),
        _f("BRAIN/05-MEMORY/SMART-NOTES/2026/10/21/SYSTEM/protocol/"
           "SN-0810/cover.png"),
        _f("BRAIN/01-GOVERNANCE/some-law.md"),
    ]


def register_via_fixer(root: Path) -> None:
    """The checker's --fix is the fixture's registering writer: it
    generates the capture + registry entry from the page itself, with
    hashes that reconcile (the proven test_door_obligation pattern)."""
    proc = subprocess.run(
        [sys.executable, str(CHECKER), "--root", str(root), "--fix",
         "--date", "2026-10-21"],
        capture_output=True, text=True, timeout=120)
    assert proc.returncode == 0, proc.stdout + proc.stderr


def load_fixture_snv2(root: Path):
    spec = importlib.util.spec_from_file_location(
        "smart_note_v2_fixture", root / "tools" / "smart_note_v2.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# ---- the set itself ----

def test_bare_page_is_unregistered_and_excluded(tmp_path):
    root = make_root(tmp_path)
    write_page(root)
    unregistered = brain_index.unregistered_note_pages(root)
    assert [(u["sn"], u["reasons"]) for u in unregistered] == [
        (SN, ["NO_ENTRY"])]
    corpus, named = brain_index.verified_corpus(
        root, inventory_fixture())
    assert named == unregistered
    paths = [f["path"] for f in corpus]
    # The bare page is out; everything that is not a door page stays.
    assert PAGE_REL not in paths
    assert any(p.endswith("cover.png") for p in paths)
    assert "BRAIN/01-GOVERNANCE/some-law.md" in paths


def test_registered_page_is_verified(tmp_path):
    root = make_root(tmp_path)
    write_page(root)
    register_via_fixer(root)
    assert brain_index.unregistered_note_pages(root) == []
    corpus, _ = brain_index.verified_corpus(root, inventory_fixture())
    assert PAGE_REL in [f["path"] for f in corpus]


def test_tampered_page_loses_verification(tmp_path):
    root = make_root(tmp_path)
    page = write_page(root)
    register_via_fixer(root)
    assert brain_index.unregistered_note_pages(root) == []
    page.write_text(PAGE + "\nTampered after registration.\n",
                    encoding="utf-8")
    unregistered = brain_index.unregistered_note_pages(root)
    assert [(u["sn"], u["reasons"]) for u in unregistered] == [
        (SN, ["PAGE_HASH_STALE"])]


def _make_hashless_entry_without_capture(root: Path) -> None:
    """Reduce the fixer's entry to the hashless legacy shape (no
    content_hash / page_hash) and remove its capture: the only
    remaining defect is NO_CAPTURE, the live corpus's ratchet class."""
    register_via_fixer(root)
    reg_path = root / ".naya" / "memory" / "smart-notes" / "index.json"
    reg = json.loads(reg_path.read_text(encoding="utf-8"))
    entry = reg["entries"][0]
    entry.pop("content_hash", None)
    entry.pop("page_hash", None)
    snv2 = load_fixture_snv2(root)
    reg["corpus_manifest_hash"] = snv2._corpus_manifest_hash(reg["entries"])
    reg_path.write_text(json.dumps(reg), encoding="utf-8")
    (root / ".naya" / "capture" / f"{IB}.json").unlink()


def test_ratchet_carried_legacy_entry_stays_verified(tmp_path):
    root = make_root(tmp_path)
    write_page(root)
    _make_hashless_entry_without_capture(root)
    # Unratcheted, the missing capture is a hard defect: unverified.
    unregistered = brain_index.unregistered_note_pages(root)
    assert [(u["sn"], u["reasons"]) for u in unregistered] == [
        (SN, ["NO_CAPTURE"])]
    # Carried by the shrink-only ratchet, the same standing verifies —
    # the ratchet route SN-4711 names for legacy entries.
    (root / "tools" / "door_obligation_grandfathered.json").write_text(
        json.dumps({"defects": [
            {"sn": SN, "ib": IB, "kind": "NO_CAPTURE"}]}),
        encoding="utf-8")
    assert brain_index.unregistered_note_pages(root) == []


# ---- floors recomputed over the verified set ----

def test_floors_recomputed_over_verified_set(tmp_path):
    root = make_root(tmp_path)
    write_page(root)
    files = inventory_fixture()
    prepared = brain_index.prepare(root, files)
    full_floors = brain_index.floor_domain_counts(files)
    # Excluding the one bare page lowers the 05-MEMORY floor by exactly
    # one — the page no longer legitimizes itself — and the corpus
    # counts sit exactly on the recomputed floors (no false deletion).
    assert prepared["floors"]["05-MEMORY"] == full_floors["05-MEMORY"] - 1
    # The exclusion moves the 05-MEMORY count and floor by the same
    # one page, so it introduces no new shortfall: whatever distance
    # the unfiltered fixture stands from its floor (its handful of
    # files never meet the domain's fixed base), the verified corpus
    # stands at exactly the same distance from the recomputed floor.
    full_counts = brain_index.domain_counts(files)
    full_shortfall = full_floors["05-MEMORY"] - full_counts["05-MEMORY"]
    prepared_shortfall = (prepared["floors"]["05-MEMORY"]
                          - prepared["counts"]["05-MEMORY"])
    assert prepared_shortfall == full_shortfall


# ---- the generated documents name the excluded, only when there are any ----

def test_real_tree_json_names_unregistered_only_when_present():
    files = [_f("BRAIN/01-GOVERNANCE/some-law.md")]
    counts = brain_index.domain_counts(files)
    legacy = json.loads(brain_index.build_real_tree_json(
        "f" * 40, files, counts, "2026-11-24"))
    assert "unregistered_pages" not in legacy
    unregistered = [{"sn": SN, "ib": IB, "path": PAGE_REL,
                     "reasons": ["NO_ENTRY"]}]
    doc = json.loads(brain_index.build_real_tree_json(
        "f" * 40, files, counts, "2026-11-24", unregistered))
    assert doc["unregistered_pages"] == [
        {"sn": SN, "path": PAGE_REL, "reasons": ["NO_ENTRY"]}]


def test_real_tree_md_section_only_when_present():
    files = [_f("BRAIN/01-GOVERNANCE/some-law.md")]
    counts = brain_index.domain_counts(files)
    legacy = brain_index.build_real_tree_md(
        "f" * 40, files, counts, "2026-11-24")
    assert "Unregistered Smart Note pages" not in legacy
    unregistered = [{"sn": SN, "ib": IB, "path": PAGE_REL,
                     "reasons": ["NO_ENTRY"]}]
    md = brain_index.build_real_tree_md(
        "f" * 40, files, counts, "2026-11-24", unregistered)
    assert "## Unregistered Smart Note pages (excluded)" in md
    assert PAGE_REL in md and SN in md

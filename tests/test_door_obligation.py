"""Door obligation: a Smart Note page may not land without its records.

Origin: 2026-10-21. The intelligence door (direct writes to main) kept
landing BRAIN projection pages with no .naya capture and no registry
entry; the vanished-id set grew 5 -> 11 in ~2 hours and PR #2831's cure
could not outrun it (falsifiers 6325348465 / 6326451724). The guard
battery measured the debt but nothing prevented it. This module tests
the prevention tool (tools/check_door_obligation.py):

  - a complete set (page + capture + entry, hashes bound) passes;
  - a bare page is flagged with a self-explaining MISSING/CURE line
    (negative control — the check must be able to fail);
  - the fixer generates capture + entry FROM the page whose hashes
    reconcile with the registry audit's own bindings;
  - the fixer REFUSES to fabricate a record for an id with no page
    (the SN-9998/SN-9999 tombstone class belongs to the LAW lane);
  - the fixer is idempotent;
  - a removed-without-record id is classified TOMBSTONE_REQUIRED,
    never silently backfilled.

Run:  python -m pytest tests/test_door_obligation.py -q
"""

import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "tools" / "check_door_obligation.py"
SNV2 = ROOT / "tools" / "smart_note_v2.py"

PAGE_REL = ("BRAIN/05-MEMORY/SMART-NOTES/2026/10/21/SYSTEM/protocol/"
            "SN-0810/IB-SMART-NOTE-20261021-sn0810-door-fixture.md")
IB = "IB-SMART-NOTE-20261021-sn0810-door-fixture"

DIALECT1 = """# Door Fixture Note

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

DIALECT3_REL = ("BRAIN/05-MEMORY/SMART-NOTES/2026/10/21/SYSTEM/testing/"
                "SN-1785/IB-SMART-NOTE-20261021-sn1785-door-fixture.md")
DIALECT3_IB = "IB-SMART-NOTE-20261021-sn1785-door-fixture"
DIALECT3 = """# Emoji Fixture Note

**Intelligent Block:** IB-SMART-NOTE-20261021-sn1785-door-fixture
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-21
**ID:** SN-1785

## ✦ IN A NUTSHELL

The emoji essence.

## 🩷 HUMAN NOTE

The emoji human view.

## 🟣 CHILD NOTE

The emoji child view.

## 🔵 GRANDMA NOTE

The emoji grandma view.

## 🟠 NAYA NOTE

The emoji naya view.

## 🟢 MACHINE NOTE

```json
{"sn_id": "SN-1785", "enforcement": "fixture enforcement", "status": "CANDIDATE"}
```
"""


def make_root(tmp_path: Path) -> Path:
    (tmp_path / "tools").mkdir(parents=True)
    shutil.copy(SNV2, tmp_path / "tools" / "smart_note_v2.py")
    reg = tmp_path / ".naya" / "memory" / "smart-notes"
    reg.mkdir(parents=True)
    (reg / "index.json").write_text(json.dumps({
        "schema": "naya.smart-note-projection-index.v1",
        "version": "1.0",
        "source_of_truth": "runtime_intelligent_block",
        "entries": [],
        "sequence_policy": {"human_id_format": "SN-###",
                            "next_sequence": 810},
        "corpus_manifest_hash": "0" * 64,
    }), encoding="utf-8")
    (tmp_path / ".naya" / "capture").mkdir(parents=True)
    return tmp_path


def write_page(root: Path, rel: str, text: str) -> Path:
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")
    return p


def run_tool(root: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(TOOL), "--root", str(root), *args],
        capture_output=True, text=True, timeout=120)


def audit(root: Path):
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "smart_note_v2_fixture", root / "tools" / "smart_note_v2.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.audit_registry(root=root)


def test_bare_page_is_flagged_with_a_cure_line(tmp_path):
    """Negative control: the check must be able to fail, in words a lane
    can act on without reading the tool's source."""
    root = make_root(tmp_path)
    write_page(root, PAGE_REL, DIALECT1)
    proc = run_tool(root)
    assert proc.returncode == 1, proc.stdout
    assert "MISSING: registry entry for SN-0810" in proc.stdout
    assert "MISSING: capture for SN-0810" in proc.stdout
    assert "CURE:" in proc.stdout and "owner:" in proc.stdout
    assert "check_door_obligation.py --fix --ids SN-0810" in proc.stdout


def test_fixer_generates_reconciling_records(tmp_path):
    root = make_root(tmp_path)
    write_page(root, PAGE_REL, DIALECT1)
    proc = run_tool(root, "--fix", "--date", "2026-10-21")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    cap = root / ".naya" / "capture" / f"{IB}.json"
    assert cap.exists()
    doc = json.loads(cap.read_text(encoding="utf-8"))
    assert doc["schema"] == "naya.smart-note-capture.v2"
    assert doc["intelligence"]["essence"] == "The fixture essence."
    assert doc["intelligence"]["ai_view"] == "The synthesis."
    # The registry audit's own bindings must reconcile: the page is no
    # longer unregistered and no entry hash is stale.
    rep = audit(root)
    assert rep["defects"]["published_pages_without_registry_entry"] == []
    assert rep["defects"]["entries_with_stale_hash"] == []
    # And the door check itself now passes for the note.
    proc = run_tool(root, "--ids", "SN-0810")
    assert proc.returncode == 0, proc.stdout
    assert "OK" in proc.stdout


def test_fixer_is_idempotent(tmp_path):
    root = make_root(tmp_path)
    write_page(root, PAGE_REL, DIALECT1)
    assert run_tool(root, "--fix", "--date", "2026-10-21").returncode == 0
    reg_bytes = (root / ".naya" / "memory" / "smart-notes"
                 / "index.json").read_bytes()
    cap_bytes = (root / ".naya" / "capture" / f"{IB}.json").read_bytes()
    proc = run_tool(root, "--fix", "--date", "2026-10-21")
    assert proc.returncode == 0
    assert "CAPTURE_WRITTEN" not in proc.stdout
    assert "ENTRY_WRITTEN" not in proc.stdout
    assert (root / ".naya" / "memory" / "smart-notes"
            / "index.json").read_bytes() == reg_bytes
    assert (root / ".naya" / "capture"
            / f"{IB}.json").read_bytes() == cap_bytes


def test_fixer_refuses_a_pageless_id(tmp_path):
    """The tombstone class: an id with no page gets NO fabricated record."""
    root = make_root(tmp_path)
    write_page(root, PAGE_REL, DIALECT1)
    proc = run_tool(root, "--fix", "--ids", "SN-9999",
                    "--date", "2026-10-21")
    assert proc.returncode == 1
    assert "REFUSED: SN-9999" in proc.stdout
    assert list((root / ".naya" / "capture").glob("*9999*")) == []
    reg = json.loads((root / ".naya" / "memory" / "smart-notes"
                      / "index.json").read_text(encoding="utf-8"))
    assert reg["entries"] == []


def test_dialect3_machine_json_and_empty_ai_view(tmp_path):
    root = make_root(tmp_path)
    write_page(root, DIALECT3_REL, DIALECT3)
    proc = run_tool(root, "--fix", "--date", "2026-10-21")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    doc = json.loads((root / ".naya" / "capture"
                      / f"{DIALECT3_IB}.json").read_text(encoding="utf-8"))
    intel = doc["intelligence"]
    # The page's own machine JSON is carried, not paraphrased.
    assert intel["machine_view"]["enforcement"] == "fixture enforcement"
    assert intel["machine_view"]["projection_path"] == DIALECT3_REL
    # No WHAT-IT-ALL-MEANS section exists on the page; ai_view stays
    # empty rather than being synthesized, and the note says so.
    assert intel["ai_view"] == ""
    assert "left empty" in intel["views_note"]
    assert intel["essence"] == "The emoji essence."


def test_entry_is_generated_from_an_existing_capture(tmp_path):
    """When a lane already wrote the capture (the #2831 shape), the fixer
    adds only the entry and leaves the capture byte-identical."""
    root = make_root(tmp_path)
    write_page(root, PAGE_REL, DIALECT1)
    intel = {"title": "Hand capture", "intelligent_block_id": IB,
             "smart_note_id": "SN-0810", "projection_path": PAGE_REL,
             "essence": "hand-written"}
    cap_doc = {"smart_note_id": "SN-0810", "intelligence": intel,
               "source": {"ingestion": "runtime"},
               "schema": "naya.smart-note-capture.v2",
               "lifecycle_state": "ACTIVE"}
    cap = root / ".naya" / "capture" / f"{IB}.json"
    cap.write_text(json.dumps(cap_doc), encoding="utf-8")
    before = cap.read_bytes()
    proc = run_tool(root, "--fix", "--date", "2026-10-21")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "ENTRY_WRITTEN" in proc.stdout
    assert "CAPTURE_WRITTEN" not in proc.stdout
    assert cap.read_bytes() == before
    rep = audit(root)
    assert rep["defects"]["published_pages_without_registry_entry"] == []
    assert rep["defects"]["entries_with_stale_hash"] == []


def _git(root: Path, *args: str) -> None:
    subprocess.run(["git", *args], cwd=root, check=True,
                   capture_output=True, text=True)


@pytest.mark.skipif(shutil.which("git") is None, reason="git unavailable")
def test_removed_id_is_tombstone_class_never_backfilled(tmp_path):
    root = make_root(tmp_path)
    write_page(root, PAGE_REL, DIALECT1)
    fixture_rel = ("BRAIN/05-MEMORY/SMART-NOTES/2026/10/21/SYSTEM/protocol/"
                   "SN-9998/IB-SMART-NOTE-20261021-sn9998-live-fire.md")
    write_page(root, fixture_rel, DIALECT1.replace("sn0810", "sn9998")
               .replace("SN-0810", "SN-9998"))
    _git(root, "init", "-q")
    _git(root, "config", "user.email", "fixture@example.invalid")
    _git(root, "config", "user.name", "fixture")
    _git(root, "add", "-A")
    _git(root, "commit", "-qm", "fixture: both pages land")
    _git(root, "rm", "-q", fixture_rel)
    _git(root, "commit", "-qm", "fixture: live-fire note removed")
    proc = run_tool(root)
    assert proc.returncode == 1
    assert "lifecycle record for SN-9998" in proc.stdout
    assert "LAW lane" in proc.stdout
    # And the fixer still refuses to invent it a note.
    proc = run_tool(root, "--fix", "--ids", "SN-9998",
                    "--date", "2026-10-21")
    assert proc.returncode == 1
    assert "REFUSED: SN-9998" in proc.stdout


def _load_tool_module():
    import importlib.util
    spec = importlib.util.spec_from_file_location("check_door_obligation", TOOL)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_range_endpoints_two_dot_and_three_dot():
    # The door-obligation workflow passes a THREE-dot range on
    # pull_request (origin/main...HEAD) and two dots on push. The
    # uniqueness gate must parse both; partition("..") alone turned
    # the three-dot head into ".HEAD" and failed the gate closed on a
    # ref that does not exist (PR #3088 CI, diagnosed 2026-10-26).
    mod = _load_tool_module()
    assert mod._range_endpoints("abc..def") == ("abc", "def")
    assert mod._range_endpoints("origin/main...HEAD") == ("origin/main", "HEAD")
    assert mod._range_endpoints("a...b") == ("a", "b")


def test_range_endpoints_rejects_malformed():
    mod = _load_tool_module()
    for bad in ("abc", "abc..", "..def", "abc...", "...def", ""):
        with pytest.raises(RuntimeError):
            mod._range_endpoints(bad)


# ---------------------------------------------------------------------------
# SN-2204 (2026-11-14): page_hash binds projection_path, not the dated page
# ---------------------------------------------------------------------------

def _rebind_entry_to_projection(root: Path, proj_rel: str) -> None:
    """Rebind every registry entry to a separate projection file, the
    SN-2204 shape: the writer rendered the projection outside the dated
    SMART-NOTES tree, so the dated filing is a second rendering with
    different bytes. The manifest is recomputed, exactly as the writer
    would leave it — the fixture stays validator-clean."""
    import hashlib
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "smart_note_v2_rebind", root / "tools" / "smart_note_v2.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    reg_path = (root / ".naya" / "memory" / "smart-notes" / "index.json")
    reg = json.loads(reg_path.read_text(encoding="utf-8"))
    for e in reg["entries"]:
        e["projection_path"] = proj_rel
        e["page_hash"] = mod._page_file_hash(root / proj_rel)
    reg["corpus_manifest_hash"] = mod._corpus_manifest_hash(reg["entries"])
    reg_path.write_text(json.dumps(reg, indent=2), encoding="utf-8")


def _sn2204_fixture(tmp_path: Path, dated_text: str | None = None) -> Path:
    """Dated page + separate projection file, entry bound to the
    projection. With dated_text None the two files are byte-identical;
    otherwise the dated filing is a different rendering — the exact
    SN-2204 shape at pin 2dd1c9aa."""
    root = make_root(tmp_path)
    proj_rel = "BRAIN/05-MEMORY/SMART-NOTE-door-fixture.md"
    write_page(root, proj_rel, DIALECT1)
    write_page(root, PAGE_REL, DIALECT1 if dated_text is None else dated_text)
    proc = run_tool(root, "--fix", "--date", "2026-10-21")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    _rebind_entry_to_projection(root, proj_rel)
    return root


def test_page_hash_binds_projection_not_dated_page(tmp_path):
    """Positive: an entry whose page_hash matches its projection bytes
    must NOT flag PAGE_HASH_STALE even when the dated filing differs.
    The writer contract (B-51 step 3) and the validator (Check 6) bind
    page_hash to projection_path; re-stamping from the dated page would
    break the validator (INDEX_CORRUPT:PAGE_HASH_MISMATCH) and take cold
    retrieval down — the exact failure the 2026-11-14 re-anchor cured.
    The second rendering surfaces as a DUAL_RENDERING warning, not a
    defect."""
    root = _sn2204_fixture(
        tmp_path,
        DIALECT1.replace("The fixture essence.",
                         "A different rendering."))
    # The fixture is validator-clean in this shape, as SN-2204 is at pin.
    rep = audit(root)
    assert rep["defects"]["entries_with_stale_hash"] == []
    proc = run_tool(root, "--ids", "SN-0810", "--json")
    assert proc.returncode == 0, proc.stdout
    out = json.loads(proc.stdout)
    assert out["defects"] == []
    assert [w for w in out["warnings"] if w["kind"] == "DUAL_RENDERING"]
    assert "do NOT re-stamp page_hash" in \
        [w for w in out["warnings"]
         if w["kind"] == "DUAL_RENDERING"][0]["cure"]


def test_page_hash_stale_fires_on_projection_drift(tmp_path):
    """Negative control (divergent paths): start from byte-identical
    dated page and projection, then drift ONLY the projection file —
    PAGE_HASH_STALE must fire. This proves the comparison follows
    projection_path: the pre-fix code hashed the dated page (unchanged)
    and stayed silent, so this test FAILS on the unpatched tool."""
    root = _sn2204_fixture(tmp_path)
    proj = root / "BRAIN/05-MEMORY/SMART-NOTE-door-fixture.md"
    proj.write_text(proj.read_text(encoding="utf-8") + "\nDrifted.\n",
                    encoding="utf-8")
    proc = run_tool(root, "--ids", "SN-0810", "--json")
    assert proc.returncode == 1, proc.stdout
    out = json.loads(proc.stdout)
    kinds = [d["kind"] for d in out["defects"]]
    assert "PAGE_HASH_STALE" in kinds, out


def test_page_hash_stale_fires_on_dated_page_drift(tmp_path):
    """Negative control (coincident paths): the classic case still works —
    when projection_path IS the dated page, drifting it fires
    PAGE_HASH_STALE. The fix changes nothing where the two paths agree."""
    root = make_root(tmp_path)
    write_page(root, PAGE_REL, DIALECT1)
    proc = run_tool(root, "--fix", "--date", "2026-10-21")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    page = root / PAGE_REL
    page.write_text(page.read_text(encoding="utf-8") + "\nDrifted.\n",
                    encoding="utf-8")
    proc = run_tool(root, "--ids", "SN-0810", "--json")
    assert proc.returncode == 1, proc.stdout
    out = json.loads(proc.stdout)
    assert "PAGE_HASH_STALE" in [d["kind"] for d in out["defects"]], out

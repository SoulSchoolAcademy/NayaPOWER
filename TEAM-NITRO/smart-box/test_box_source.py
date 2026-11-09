#!/usr/bin/env python3
"""test_box_source.py - proof for box_source.py (Lane B, wiring pass).

Run:  python3 test_box_source.py
Exit 0 only when every check passes; non-zero otherwise. Prints one
line per check, no tracebacks on failure - a failure names what is
missing. Zero stderr on a green run.

What it proves, on fixtures only (a scratch BOXES_ROOT - no live
writes, no live reads, no network):

  A. The source list: blocks in a scratch shawn box name real
     SMART-NOTES GitHub paths (paths copied verbatim from the live
     sync state's tracked set - the paths are real; the blocks are
     fixture blocks built from the three real fixture notes, so the
     test proves the LISTING logic, never that the fixture blocks
     are the live notes). list_note_paths_from_box returns exactly
     those paths, newest first (reverse alphabetical, the sync's
     walk order), and ignores blocks with no SMART-NOTES path.
  B. The map / brain views: map_view carries about + what + links
     and NO raw body; brain_view carries the essence with title and
     topics.
  C. The completeness gate: complete when every state path is in
     the box; incomplete names exactly the missing paths; a box
     naming MORE paths than the state is still complete (notes
     organized but not yet synced are fine).
  D. The failure rule: a missing box raises BoxSourceError (never
     an empty list pretending nothing exists); a corrupt blocks
     line raises BoxSourceError; a readable empty box returns an
     empty list and fails the completeness gate.
  E. Round-trip through the box: a block appended with boxstore and
     read back through box_source is identical (id + raw intact) -
     the retrieve half of the live citizen-vault proof, on fixtures.
  F. get_block_from_box returns the block, or None for an unknown id.

Fixtures: the three real smart notes beside this file in
``fixtures/`` (see fixtures/README.md for provenance) + three real
GitHub paths copied verbatim from the live sync state file
(``~/workspace/factory-pipeline/.sync-state.json`` - read, never
written). The scratch box lives in a tempfile and is deleted with it.
"""

import json
import os
import shutil
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from block import note_to_block  # noqa: E402
import boxstore  # noqa: E402
import box_source  # noqa: E402
from box_source import (  # noqa: E402
    BoxSourceError,
    box_is_complete_for_state,
    brain_view_for_owner,
    get_block_from_box,
    list_note_paths_from_box,
    map_view_for_owner,
)

FIXTURES = HERE / "fixtures"
OWNER = "shawn"

# Real GitHub paths, copied verbatim from the live sync state's
# tracked set (read-only). The fixture blocks below carry these
# paths in where.github_path so the listing test runs on real paths.
REAL_PATHS = [
    "BRAIN/05-MEMORY/SMART-NOTES/2026/11/09/PRODUCT/SN-2535/"
    "IB-SMART-NOTE-20261109-sn2535-what-naya-does.md",
    "BRAIN/05-MEMORY/SMART-NOTES/2026/11/09/LESSON/SN-2505/"
    "IB-SMART-NOTE-20261109-sn2505-one-deploy-shape.md",
    "BRAIN/05-MEMORY/SMART-NOTES/2026/09/29/SYSTEM-INTELLIGENCE/"
    "NAYA-CONTINUATION-ENGINE/ONE-NEXT-ACTION-AND-PROOF/SN-003/"
    "IB-SMART-NOTE-20260929-sn003-naya-continuation-engine.md",
]

# (fixture file, github path or None, visibility, owner_shared_choice)
NOTES = [
    ("SN-2535-what-naya-does.md", REAL_PATHS[0], "public", True),
    ("SN-2543-smart-box-cure-saving-sickness.md", None, "private", False),
    ("SN-2545-super-brain-is-yours.md", None, "private", False),
]

CHECKS = []


def check(name, ok, detail=""):
    CHECKS.append((name, bool(ok), detail))
    print(("  PASS " if ok else "  FAIL ") + name
          + (" - " + detail if detail and not ok else ""))


def build_scratch_box(root, with_paths=True):
    """A scratch shawn box: the three fixture notes as blocks. With
    ``with_paths``, the first block carries REAL_PATHS[0] and two
    extra fixture blocks carry REAL_PATHS[1] and [2] (fixture
    blocks, real paths - the listing test). Returns the box root."""
    boxes_root = os.path.join(root, "boxes")
    boxstore.BOXES_ROOT = boxes_root
    boxstore.ensure_box(OWNER)
    blocks = []
    for fname, gpath, vis, choice in NOTES:
        text = (FIXTURES / fname).read_text(encoding="utf-8")
        block = note_to_block(text, owner=OWNER, github_path=gpath,
                              visibility=vis, owner_shared_choice=choice)
        blocks.append(block)
    if with_paths:
        # Two more fixture blocks naming the other two real paths,
        # so the source list has three entries to order.
        for extra_path in REAL_PATHS[1:]:
            block = dict(blocks[1])
            block = json.loads(json.dumps(block))
            block["id"] = "%s:note:fixture-%s" % (
                OWNER, extra_path.split("/")[-1][:-3].lower())
            block["where"] = dict(block["where"])
            block["where"]["github_path"] = extra_path
            blocks.append(block)
    for block in blocks:
        boxstore.append_block(OWNER, block)
    return boxes_root


def main():
    tmp = tempfile.mkdtemp(prefix="box-source-test-")
    try:
        boxes_root = build_scratch_box(tmp)

        # -- A. the source list -------------------------------------
        paths = list_note_paths_from_box(OWNER, boxes_root)
        check("A1 source list is exactly the real SMART-NOTES paths",
              paths == sorted(REAL_PATHS, reverse=True),
              "got %r" % (paths,))
        check("A2 newest first (reverse alphabetical)",
              paths[0] == REAL_PATHS[0] and paths[-1] == REAL_PATHS[2],
              "first %r last %r" % (paths[0], paths[-1]))
        check("A3 blocks without a SMART-NOTES path are not listed",
              len(paths) == 3, "got %d" % len(paths))

        # -- B. map / brain views -----------------------------------
        maps = map_view_for_owner(OWNER, boxes_root)
        check("B1 map view covers every block in the box",
              len(maps) == 5, "got %d" % len(maps))
        sample = maps["shawn:note:sn-2535-what-naya-does-daily-reports-smart-notes-naya-notes-and-pages"]
        check("B2 map view carries about + what + links only",
              set(sample) == {"id", "kind", "what", "about", "links"},
              "keys %r" % (sorted(sample),))
        check("B3 map view never carries the raw body",
              "body" not in sample and "raw" not in sample)
        brains = brain_view_for_owner(OWNER, boxes_root)
        brain = brains["shawn:note:sn-2535-what-naya-does-daily-reports-smart-notes-naya-notes-and-pages"]
        check("B4 brain view carries the essence with title + topics",
              set(brain) == {"id", "kind", "what", "about", "essence"}
              and brain["essence"].startswith("Naya operates all of"),
              "keys %r essence %.40r" % (sorted(brain), brain["essence"]))

        # -- C. completeness gate -----------------------------------
        complete, missing = box_is_complete_for_state(
            OWNER, REAL_PATHS, boxes_root)
        check("C1 complete when every state path is in the box",
              complete and missing == [], "missing %r" % (missing,))
        complete2, missing2 = box_is_complete_for_state(
            OWNER, REAL_PATHS + ["BRAIN/05-MEMORY/SMART-NOTES/2026/11/09/"
                                 "PRODUCT/SN-9999/"
                                 "IB-SMART-NOTE-20261109-sn9999-nope.md"],
            boxes_root)
        check("C2 incomplete names exactly the missing paths",
              not complete2 and missing2 == [
                  "BRAIN/05-MEMORY/SMART-NOTES/2026/11/09/PRODUCT/SN-9999/"
                  "IB-SMART-NOTE-20261109-sn9999-nope.md"],
              "missing %r" % (missing2,))
        complete3, _ = box_is_complete_for_state(
            OWNER, REAL_PATHS[:2], boxes_root)
        check("C3 box naming MORE than the state is still complete",
              complete3)

        # -- D. failure rule ----------------------------------------
        try:
            list_note_paths_from_box("nobody-here", boxes_root)
            check("D1 missing box raises BoxSourceError", False,
                  "returned a list instead")
        except BoxSourceError:
            check("D1 missing box raises BoxSourceError", True)
        empty_root = os.path.join(tmp, "empty-boxes")
        boxstore.BOXES_ROOT = empty_root
        boxstore.ensure_box(OWNER)
        empty_paths = list_note_paths_from_box(OWNER, empty_root)
        check("D2 readable empty box returns an empty list",
              empty_paths == [], "got %r" % (empty_paths,))
        complete4, missing4 = box_is_complete_for_state(
            OWNER, REAL_PATHS, empty_root)
        check("D3 empty box fails the completeness gate",
              not complete4 and sorted(missing4) == sorted(REAL_PATHS),
              "missing %r" % (missing4,))
        corrupt_root = os.path.join(tmp, "corrupt-boxes")
        boxstore.BOXES_ROOT = corrupt_root
        boxstore.ensure_box(OWNER)
        with open(os.path.join(corrupt_root, OWNER, "blocks.jsonl"),
                  "a", encoding="utf-8") as handle:
            handle.write("{not json\n")
        try:
            list_note_paths_from_box(OWNER, corrupt_root)
            check("D4 corrupt blocks line raises BoxSourceError", False,
                  "returned a list instead")
        except BoxSourceError:
            check("D4 corrupt blocks line raises BoxSourceError", True)

        # -- E. round-trip through the box --------------------------
        boxstore.BOXES_ROOT = boxes_root
        text = (FIXTURES / "SN-2535-what-naya-does.md").read_text(
            encoding="utf-8")
        block = note_to_block(text, owner=OWNER,
                              github_path=REAL_PATHS[0],
                              visibility="public",
                              owner_shared_choice=True)
        boxstore.append_block(OWNER, block)
        back = get_block_from_box(OWNER, block["id"], boxes_root)
        check("E1 block read back from the box is identical",
              back == block, "differs")
        check("E2 retrieved block keeps id + raw intact",
              back is not None and back["id"] == block["id"]
              and back["raw"] == block["raw"]
              and back["body"] == block["body"])

        # -- F. get by id -------------------------------------------
        check("F1 unknown id returns None",
              get_block_from_box(OWNER, "shawn:note:nope", boxes_root)
              is None)
    finally:
        boxstore.BOXES_ROOT = os.path.expanduser(
            "~/workspace/nitro-smart-box/boxes")
        shutil.rmtree(tmp, ignore_errors=True)

    failed = [name for name, ok, _ in CHECKS if not ok]
    print("box_source: %d/%d checks passed"
          % (len(CHECKS) - len(failed), len(CHECKS)))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())

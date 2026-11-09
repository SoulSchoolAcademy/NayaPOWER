#!/usr/bin/env python3
"""test_organize_hook.py - proof for the organize pipeline hook.

Run:  python3 test_organize_hook.py
Exit 0 only when every check passes; non-zero otherwise. Prints one
line per check, no tracebacks on failure - a failure names what is
missing.

What it proves, on fixtures only (never the live box, never the live
note tree): the hook's scratch BOXES_ROOT and watermark live under a
temp dir, and the note files it organizes are copies of the real
fixtures beside this file (``fixtures/SN-2535-*.md``,
``fixtures/SN-2543-*.md``, ``fixtures/SN-2545-*.md``,
``fixtures/smart-box-entries.json``) plus small synthetic notes the
test writes itself.

  A. First run organizes every fixture note + entry into the box,
     each block carrying its tags, shelf, and links from organize().
  B. Second run organizes nothing - the watermark holds, so the loop
     does not re-file the same things every 30 minutes.
  C. A changed file is picked up again (re-organized, superseding by
     block id) and an unchanged file is not.
  D. A file that is not a smart note is skipped and counted, and the
     run still succeeds - one bad file never kills the loop.
  E. --backfill organizes the whole tree even when the watermark says
     everything is seen, and writes the watermark marking all seen.
  F. A duplicate block id (same note in two roots) lands once.
  G. --dry-run writes nothing: no box dir, no watermark.
  H. The box on disk is the boxstore layout: blocks.jsonl +
     keys.jsonl + manifest.json, and the manifest counts match.
"""

import json
import os
import shutil
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import boxstore  # noqa: E402
import organize_hook as hook  # noqa: E402

FIXTURES = HERE / "fixtures"
OWNER = "shawn"

CHECKS = []


def check(name, ok, detail=""):
    """One check line. Failures name what is missing."""
    CHECKS.append((name, bool(ok), detail))
    print("%s %s%s" % ("PASS" if ok else "FAIL", name,
                       (" - " + detail) if detail and not ok else ""))


def make_tree(tmp):
    """A scratch note tree from the real fixtures + one synthetic note
    + one unparseable file. Returns (repo_root, local_root, nn_root,
    store_path)."""
    repo_notes = tmp / "repo" / "BRAIN" / "05-MEMORY" / "SMART-NOTES"
    repo_notes.mkdir(parents=True)
    for name in ("SN-2535-what-naya-does.md",
                 "SN-2543-smart-box-cure-saving-sickness.md"):
        shutil.copy2(FIXTURES / name, repo_notes / name)
    local_notes = tmp / "local-notes"
    local_notes.mkdir()
    shutil.copy2(FIXTURES / "SN-2545-super-brain-is-yours.md",
                  local_notes / "SN-2545-super-brain-is-yours.md")
    (local_notes / "SN-9999-tonights-newest-note.md").write_text(
        "# Tonight's Newest Note\n\n"
        "**Created:** 2026-11-09\n\n"
        "## In a Nutshell\n\n"
        "A synthetic note written by the test, standing in for "
        "tonight's newest real note.\n\n"
        "## Why It Matters\n\n"
        "It proves the hook picks up a genuinely new file.\n",
        encoding="utf-8")
    (local_notes / "not-a-note.txt").write_text(
        "plain text, no markdown title, no sections\n", encoding="utf-8")
    (local_notes / "README-no-sections.md").write_text(
        "just a paragraph, no title line, no ## sections\n",
        encoding="utf-8")
    nn_root = tmp / "naya-notes"
    nn_root.mkdir()
    (nn_root / "NN-20261109-test-note.md").write_text(
        "# A Test Naya Note\n\n"
        "**Written by Naya for Shawn**\n\n"
        "## What it is\n\n"
        "His words, recorded verbatim.\n\n"
        "## Why it matters\n\n"
        "It proves Naya Notes convert too.\n",
        encoding="utf-8")
    store = tmp / "entries.jsonl"
    entries = json.loads((FIXTURES / "smart-box-entries.json").read_text())
    with open(store, "w", encoding="utf-8") as handle:
        for entry in entries:
            handle.write(json.dumps(entry) + "\n")
    return repo_notes, local_notes, nn_root, store


def main():
    tmp = Path(tempfile.mkdtemp(prefix="organize-hook-test-"))
    try:
        repo_notes, local_notes, nn_root, store = make_tree(tmp)
        boxes_root = str(tmp / "boxes")
        watermark = str(tmp / "watermark.json")
        roots = [(str(repo_notes), True),
                 (str(local_notes), False),
                 (str(nn_root), False)]

        # A. First run organizes everything: 2 repo notes + 2 local
        # notes + 1 Naya Note + 3 store entries = 8 blocks.
        stats = hook.run(owner=OWNER, notes_roots=roots,
                         store_path=str(store), boxes_root=boxes_root,
                         watermark=watermark)
        check("A first run organizes 8 blocks",
              stats["organized"] == 8,
              "organized=%s" % stats["organized"])
        blocks = boxstore.read_blocks(OWNER)
        check("A all 8 blocks are in the box", len(blocks) == 8,
              "blocks=%s" % len(blocks))
        newest = blocks.get("shawn:note:note-tonight-s-newest-note")
        check("A tonight's newest note is organized",
              newest is not None and
              newest["where"].get("shelf", "").startswith(
                  "shawn/note/"),
              "id=%s shelf=%s" % (
                  newest["id"] if newest else None,
                  (newest or {}).get("where", {}).get("shelf")))
        entry_block = blocks.get("shawn:note:sb-0001-the-wise-one-04-00z-"
                                 "2026-11-04-canonical-manifesto-sn-0883-"
                                 "full-text-workspace-your-files-"
                                 "the-wise-one-manifesto-md")
        check("A a store entry is organized with its type tag",
              entry_block is not None and
              "dictation" in entry_block["about"],
              "about=%s" % (entry_block or {}).get("about"))
        check("A every block carries the organize proof",
              all(b.get("proof", "").startswith("organize:")
                  for b in blocks.values()))

        # B. Second run organizes nothing - the watermark holds.
        stats2 = hook.run(owner=OWNER, notes_roots=roots,
                          store_path=str(store), boxes_root=boxes_root,
                          watermark=watermark)
        check("B second run organizes 0 (watermark holds)",
              stats2["organized"] == 0 and stats2["files_new"] == 0
              and stats2["entries_new"] == 0,
              "organized=%s files_new=%s entries_new=%s" % (
                  stats2["organized"], stats2["files_new"],
                  stats2["entries_new"]))
        check("B box still holds exactly 8 blocks",
              len(boxstore.read_blocks(OWNER)) == 8)

        # C. A changed file is picked up again; an unchanged one is not.
        changed = local_notes / "SN-9999-tonights-newest-note.md"
        changed.write_text(
            "# Tonight's Newest Note\n\n"
            "**Created:** 2026-11-09\n\n"
            "## In a Nutshell\n\n"
            "A synthetic note, EDITED after the first run.\n\n"
            "## Why It Matters\n\n"
            "It proves a changed file is re-organized.\n",
            encoding="utf-8")
        stats3 = hook.run(owner=OWNER, notes_roots=roots,
                          store_path=str(store), boxes_root=boxes_root,
                          watermark=watermark)
        check("C changed file re-organized, nothing else",
              stats3["organized"] == 1 and stats3["files_new"] == 1,
              "organized=%s files_new=%s" % (stats3["organized"],
                                             stats3["files_new"]))
        blocks = boxstore.read_blocks(OWNER)
        check("C still 8 block ids (supersede, not duplicate)",
              len(blocks) == 8, "blocks=%s" % len(blocks))
        check("C the edited body is the one in the box",
              "EDITED after the first run" in
              blocks["shawn:note:note-tonight-s-newest-note"]["body"])

        # D. The unparseable file was skipped and counted, run alive.
        check("D unparseable file skipped and counted",
              stats["files_skipped_unparseable"] == 1,
              "skipped=%s" % stats["files_skipped_unparseable"])
        check("D the .txt file was never scanned",
              stats["files_scanned"] == 6,
              "scanned=%s" % stats["files_scanned"])

        # E. --backfill organizes the whole tree despite the watermark.
        stats4 = hook.run(owner=OWNER, backfill=True, notes_roots=roots,
                          store_path=str(store), boxes_root=boxes_root,
                          watermark=watermark)
        check("E backfill organizes all 8 again",
              stats4["organized"] == 8,
              "organized=%s" % stats4["organized"])
        stats5 = hook.run(owner=OWNER, notes_roots=roots,
                          store_path=str(store), boxes_root=boxes_root,
                          watermark=watermark)
        check("E run after backfill organizes 0",
              stats5["organized"] == 0,
              "organized=%s" % stats5["organized"])

        # F. The same note in two roots lands once.
        shutil.copy2(local_notes / "SN-9999-tonights-newest-note.md",
                     repo_notes / "SN-9999-tonights-newest-note.md")
        stats6 = hook.run(owner=OWNER, backfill=True, notes_roots=roots,
                          store_path=str(store), boxes_root=boxes_root,
                          watermark=watermark)
        check("F duplicate block id lands once",
              stats6["organized"] == 8 and
              stats6["duplicates_skipped"] == 1,
              "organized=%s dups=%s" % (stats6["organized"],
                                        stats6["duplicates_skipped"]))

        # G. --dry-run writes nothing.
        boxes2 = str(tmp / "boxes-dry")
        wm2 = str(tmp / "watermark-dry.json")
        stats7 = hook.run(owner=OWNER, notes_roots=roots,
                          store_path=str(store), boxes_root=boxes2,
                          watermark=wm2, dry_run=True)
        check("G dry-run selects but writes no box and no watermark",
              stats7["organized"] == 8 and
              not os.path.exists(boxes2) and
              not os.path.exists(wm2),
              "organized=%s box=%s wm=%s" % (
                  stats7["organized"], os.path.exists(boxes2),
                  os.path.exists(wm2)))

        # H. The box on disk is the boxstore layout.
        box_dir = Path(boxes_root) / OWNER
        manifest = json.loads(
            (box_dir / "manifest.json").read_text())
        lines = [ln for ln in (box_dir / "blocks.jsonl")
                 .read_text().splitlines() if ln.strip()]
        check("H box layout is blocks + keys + manifest",
              (box_dir / "blocks.jsonl").exists() and
              (box_dir / "keys.jsonl").exists() and
              (box_dir / "manifest.json").exists())
        check("H manifest block count matches the file",
              manifest["blocks"] == len(lines) and
              manifest["owner"] == OWNER,
              "manifest=%s lines=%s" % (manifest["blocks"], len(lines)))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    failed = [name for name, ok, _ in CHECKS if not ok]
    print("%d/%d checks passed" % (len(CHECKS) - len(failed),
                                   len(CHECKS)))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())

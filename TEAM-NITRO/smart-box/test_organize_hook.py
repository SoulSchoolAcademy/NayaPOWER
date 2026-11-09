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
  I. --live-tree backfills from the LIVE GitHub tree (stubbed
     gh_api, never the network): only missing-or-changed blob shas
     are fetched; an already-current path is never re-fetched; an
     unparseable file is counted, never marked, and retried next
     run; a changed sha re-fetches and supersedes by block id; a
     truncated tree refuses outright.
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


def _stub_gh_api(tree_paths, contents, truncated=False):
    """A stub gh_api for the live-tree tests: the tree call returns
    the canned tree; contents calls return the canned note text.
    ``tree_paths`` is {github_path: blob_sha}; ``contents`` is
    {github_path: text}. Never touches the network."""
    import base64
    import urllib.error
    import urllib.parse

    def fake(path):
        if path.startswith("/git/trees/"):
            return {"sha": "treesha-test", "truncated": truncated,
                    "tree": [{"path": p, "sha": s, "type": "blob"}
                             for p, s in sorted(tree_paths.items())]}
        if path.startswith("/contents/"):
            p = urllib.parse.unquote(
                path[len("/contents/"):].split("?")[0])
            if p in contents:
                return {"content": base64.b64encode(
                    contents[p].encode("utf-8")).decode("ascii")}
            raise urllib.error.HTTPError(
                path, 404, "not found", {}, None)
        raise ValueError("unexpected gh_api path %s" % path)

    return fake


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

        # I. --live-tree backfills from the LIVE tree (stubbed gh_api).
        boxes_lt = str(tmp / "boxes-livetree")
        wm_lt = str(tmp / "watermark-livetree.json")
        text2535 = (FIXTURES / "SN-2535-what-naya-does.md") \
            .read_text(encoding="utf-8")
        text2543 = (FIXTURES / "SN-2543-smart-box-cure-saving-sickness.md") \
            .read_text(encoding="utf-8")
        text2545 = (FIXTURES / "SN-2545-super-brain-is-yours.md") \
            .read_text(encoding="utf-8")
        p_a = ("BRAIN/05-MEMORY/SMART-NOTES/2026/11/09/"
               "SYSTEM-INTELLIGENCE/SN-2535-what-naya-does.md")
        p_b = ("BRAIN/05-MEMORY/SMART-NOTES/2026/11/09/"
               "SYSTEM-INTELLIGENCE/SN-2543-smart-box-cure-saving-sickness.md")
        p_d = ("BRAIN/05-MEMORY/SMART-NOTES/2026/11/09/"
               "SYSTEM-INTELLIGENCE/SN-2545-super-brain-is-yours.md")
        p_c = ("BRAIN/05-MEMORY/SMART-NOTES/2026/11/09/"
               "SYSTEM-INTELLIGENCE/SN-9999-not-a-note.md")
        p_other = ("BRAIN/05-MEMORY/SMART-NOTES/2026/11/09/"
                   "SYSTEM-INTELLIGENCE/README.txt")
        tree1 = {p_a: "a1", p_b: "b1", p_d: "d1", p_c: "c1",
                 p_other: "o1"}
        contents1 = {p_a: text2535, p_b: text2543, p_d: text2545,
                     p_c: "hello, this is not a smart note\n"}
        # B is already current per the watermark: never re-fetched.
        Path(wm_lt).write_text(json.dumps(
            {"owner": OWNER, "files": {}, "entries": {},
             "live_tree": {p_b: "b1"}}), encoding="utf-8")
        stats_lt = hook.live_tree_backfill(
            owner=OWNER, boxes_root=boxes_lt, watermark=wm_lt,
            batch_size=2, gh_api_fn=_stub_gh_api(tree1, contents1))
        check("I live-tree organizes only the missing notes",
              stats_lt["organized"] == 2 and
              stats_lt["live_paths"] == 4,
              "organized=%s live=%s" % (stats_lt["organized"],
                                        stats_lt["live_paths"]))
        check("I live-tree skips the already-current path",
              stats_lt["selected"] == 3 and stats_lt["fetched"] == 3,
              "selected=%s fetched=%s" % (stats_lt["selected"],
                                          stats_lt["fetched"]))
        check("I live-tree counts the unparseable file, run alive",
              stats_lt["skipped_unparseable"] == 1,
              "skipped=%s" % stats_lt["skipped_unparseable"])
        lt_lines = [json.loads(ln) for ln in
                    (Path(boxes_lt) / OWNER / "blocks.jsonl")
                    .read_text(encoding="utf-8").splitlines()
                    if ln.strip()]
        check("I live-tree blocks carry the github path + a shelf",
              len(lt_lines) == 2 and all(
                  b["where"]["github_path"].startswith(
                      "BRAIN/05-MEMORY/SMART-NOTES/")
                  and b["where"].get("shelf") for b in lt_lines),
              "lines=%s" % len(lt_lines))
        mark_lt = json.loads(Path(wm_lt).read_text(encoding="utf-8"))
        check("I live-tree watermark marks fetched paths only",
              mark_lt["live_tree"] == {p_a: "a1", p_b: "b1", p_d: "d1"},
              "live_tree=%s" % sorted(mark_lt["live_tree"]))
        # Second run: only the unparseable file is re-selected.
        stats_lt2 = hook.live_tree_backfill(
            owner=OWNER, boxes_root=boxes_lt, watermark=wm_lt,
            batch_size=2, gh_api_fn=_stub_gh_api(tree1, contents1))
        check("I second live-tree run organizes 0, retries the bad file",
              stats_lt2["organized"] == 0 and
              stats_lt2["selected"] == 1 and
              stats_lt2["skipped_unparseable"] == 1,
              "organized=%s selected=%s skipped=%s" % (
                  stats_lt2["organized"], stats_lt2["selected"],
                  stats_lt2["skipped_unparseable"]))
        # Changed sha re-fetches and supersedes by block id.
        a_id = [b["id"] for b in lt_lines
                if b["where"]["github_path"] == p_a][0]
        tree2 = dict(tree1)
        tree2[p_a] = "a2"
        contents2 = dict(contents1)
        contents2[p_a] = text2535 + "\nEDITED live-tree v2 line.\n"
        stats_lt3 = hook.live_tree_backfill(
            owner=OWNER, boxes_root=boxes_lt, watermark=wm_lt,
            batch_size=2, gh_api_fn=_stub_gh_api(tree2, contents2))
        lt_lines3 = [json.loads(ln) for ln in
                     (Path(boxes_lt) / OWNER / "blocks.jsonl")
                     .read_text(encoding="utf-8").splitlines()
                     if ln.strip()]
        by_id = {}
        for block in lt_lines3:
            by_id[block["id"]] = block
        check("I changed sha re-fetches and supersedes by block id",
              stats_lt3["organized"] == 1 and len(by_id) == 2 and
              "EDITED live-tree v2 line" in by_id[a_id]["body"],
              "organized=%s unique=%s" % (stats_lt3["organized"],
                                          len(by_id)))
        # Truncated tree refuses, never a partial backfill.
        try:
            hook.live_tree_backfill(
                owner=OWNER, boxes_root=boxes_lt, watermark=wm_lt,
                batch_size=2,
                gh_api_fn=_stub_gh_api(tree1, contents1, truncated=True))
            check("I truncated tree refuses", False, "no raise")
        except ValueError:
            check("I truncated tree refuses", True)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    failed = [name for name, ok, _ in CHECKS if not ok]
    print("%d/%d checks passed" % (len(CHECKS) - len(failed),
                                   len(CHECKS)))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())

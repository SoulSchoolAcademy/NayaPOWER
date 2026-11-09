#!/usr/bin/env python3
"""organize_hook.py - the organize pipeline hook (wiring lane A, brief §1a).

The intelligence loop calls this on its 30-minute run. Every new thing
since the last run - a new smart-note file, a new Naya Note, a new store
entry - is converted to a block (``note_to_block`` / ``entry_to_block``
from ``block.py``, verbatim), run through ``organize()`` (LOOK -> TAG ->
FILE -> LINK), and appended to the owner's box through ``boxstore``
(the ONE box layout all lanes share: ``boxes/<owner>/blocks.jsonl`` +
``keys.jsonl`` + ``manifest.json``). Nothing is invented: tags, shelves,
and links trace to the thing itself, and a thing that cannot be parsed
as a note is skipped and counted, never silently converted.

A watermark file records what has already been organized, so the next
run only picks up new things: per source file its sha256, per store
entry its id + line sha256. A changed file is re-organized (the append
supersedes the earlier line by block id, per ``boxstore``). ``--backfill``
ignores the watermark and organizes the whole live note tree once, so
the box map is complete, then writes the watermark marking everything
seen.

Sources, in priority order (an earlier source wins a block-id tie, so
the canonical copy is the one that lands):
  1. the repo smart-note tree (GitHub path carried in ``where``)
  2. the local smart-notes working copies (tonight's newest notes live
     here before they are filed; ``github_path`` stays empty until
     filed - never guessed)
  3. the local Naya Notes (same treatment as 2)
  4. the Smart Box store (``entries.jsonl``)

Standard library only. No credentials, no secrets, no key material.
No reading mail or messages - the hook reads note files and the store
only. It never edits a live page and never merges anything.
"""

import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

import boxstore  # noqa: E402
from block import complete_where, entry_to_block, note_to_block, organize  # noqa: E402

DEFAULT_OWNER = "shawn"

REPO_ROOT = os.path.expanduser("~/workspace/nayapower-repo")
REPO_NOTES_ROOT = os.path.join(
    REPO_ROOT, "BRAIN", "05-MEMORY", "SMART-NOTES")
LOCAL_NOTES_ROOT = os.path.expanduser("~/workspace/team-nitro/smart-notes")
LOCAL_NN_ROOT = os.path.expanduser("~/workspace/team-nitro/naya-notes")
STORE_PATH = os.path.expanduser(
    "~/workspace/nitro-smart-box/store/entries.jsonl")
WATERMARK_DIR = os.path.expanduser("~/workspace/nitro-smart-box")

SKIP_NAMES = ("TEMPLATE",)


def watermark_path(owner):
    """The watermark lives beside ``boxes/``, never inside a box dir -
    the box layout stays exactly blocks + keys + manifest."""
    return os.path.join(WATERMARK_DIR,
                        ".organize-watermark-%s.json" % owner)


def _sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()


def _sha256_file(path):
    with open(path, "rb") as handle:
        return hashlib.sha256(handle.read()).hexdigest()


def load_watermark(path):
    """The watermark, or an empty one when there is none yet. A corrupt
    watermark is refused loudly - silently re-organizing the whole tree
    would duplicate nothing (append supersedes) but would hide the
    corruption, so the run stops instead."""
    if not os.path.exists(path):
        return {"owner": "", "files": {}, "entries": {}}
    with open(path, encoding="utf-8") as handle:
        mark = json.load(handle)
    if not isinstance(mark, dict) or "files" not in mark \
            or "entries" not in mark:
        raise ValueError("corrupt watermark: %s" % path)
    return mark


def save_watermark(path, mark):
    """Write the watermark atomically (same-dir temp + replace)."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = "%s.tmp" % path
    with open(tmp, "w", encoding="utf-8") as handle:
        json.dump(mark, handle, indent=2, sort_keys=True)
        handle.write("\n")
    os.replace(tmp, path)
    return mark


def scan_note_files(notes_roots):
    """All ``*.md`` note files under the given roots, in root order.

    Each item is ``(abs_path, github_path)``: the repo tree carries its
    repo-relative path (the ``where`` half the map needs); a local
    working copy carries "" - its GitHub path is unknown until filed,
    never guessed. Templates are skipped: a template is not a note.
    """
    found = []
    for root, is_repo in notes_roots:
        if not os.path.isdir(root):
            continue
        for dirpath, dirnames, filenames in os.walk(root):
            dirnames.sort()
            for name in sorted(filenames):
                if not name.endswith(".md"):
                    continue
                if any(skip in name.upper() for skip in SKIP_NAMES):
                    continue
                full = os.path.join(dirpath, name)
                github = ""
                if is_repo:
                    github = os.path.relpath(full, REPO_ROOT)
                found.append((full, github))
    return found


def scan_store_entries(store_path):
    """All store entries: ``(line_no, entry_dict, line_sha256)``.

    A malformed line is skipped and counted by the caller - the run
    never dies on one bad line of a 2,086-line store.
    """
    entries = []
    with open(store_path, encoding="utf-8") as handle:
        for line_no, line in enumerate(handle, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
            except ValueError:
                entries.append((line_no, None, _sha256_bytes(
                    line.encode("utf-8"))))
                continue
            if not isinstance(entry, dict) or "id" not in entry:
                entries.append((line_no, None, _sha256_bytes(
                    line.encode("utf-8"))))
                continue
            entries.append((line_no, entry, _sha256_bytes(
                line.encode("utf-8"))))
    return entries


def select_new_files(files, mark):
    """Files the watermark has not seen, or has seen with a different
    sha256 (changed since the last run). Returns ``(selected, seen)``
    where ``seen`` is {path: sha256} for every file on disk."""
    seen = {}
    selected = []
    for path, _github in files:
        digest = _sha256_file(path)
        seen[path] = digest
        if mark["files"].get(path) != digest:
            selected.append(path)
    return selected, seen


def select_new_entries(entries, mark):
    """Entries the watermark has not seen, or has seen with a different
    line sha256. Returns ``(selected, seen)`` where ``seen`` is
    {entry_id: line_sha256}."""
    seen = {}
    selected = []
    for _line_no, entry, digest in entries:
        if entry is None:
            continue
        seen[entry["id"]] = digest
        if mark["entries"].get(entry["id"]) != digest:
            selected.append(entry)
    return selected, seen


def file_to_block(path, github_path, owner):
    """One note file -> an organized block. Raises ValueError when the
    file is not a smart note (``parse_smart_note`` refuses it) - the
    caller counts that as skipped, never as organized."""
    with open(path, encoding="utf-8") as handle:
        text = handle.read()
    block = note_to_block(text, owner=owner, github_path=github_path,
                          local_path=path)
    block = organize(block)
    block, _complete = complete_where(block)
    return block


def store_entry_to_block(entry, line_no, owner, store_path):
    """One store entry -> an organized block."""
    block = entry_to_block(entry, owner=owner, store_path=store_path,
                           store_line=line_no)
    block = organize(block)
    block, _complete = complete_where(block)
    return block


def append_blocks(owner, blocks):
    """Append blocks to the owner's box through ``boxstore``.

    One manifest write for the whole batch, not one per block:
    ``append_block`` re-hashes both box files per call, which is
    O(n^2) over a backfill of thousands of blocks. The lines written
    here are byte-identical to what ``append_block`` writes (same
    JSON, same layout), and the manifest is ``boxstore``'s own
    ``write_manifest`` - the layout is unchanged, only the batching.
    """
    for block in blocks:
        if not isinstance(block, dict) or "id" not in block \
                or "kind" not in block:
            raise ValueError("append_blocks needs blocks, not %r"
                             % type(block))
    boxstore.ensure_box(owner)
    path = os.path.join(boxstore.box_dir(owner), boxstore.BLOCKS_NAME)
    with open(path, "a", encoding="utf-8") as handle:
        for block in blocks:
            handle.write(json.dumps(block, sort_keys=True,
                                    ensure_ascii=False) + "\n")
    boxstore.write_manifest(owner)
    return len(blocks)


def run(owner=DEFAULT_OWNER, backfill=False, notes_roots=None,
        store_path=STORE_PATH, boxes_root=None, watermark=None,
        dry_run=False):
    """One hook run. Returns the stats dict (also printed by main).

    ``notes_roots`` is a list of ``(path, is_repo)``; the default is
    the repo tree, then the local smart-notes copies, then the local
    Naya Notes. ``boxes_root`` and ``watermark`` are overridable so
    tests run on scratch dirs and never touch the live box.
    """
    if boxes_root is not None:
        boxstore.BOXES_ROOT = boxes_root
    if notes_roots is None:
        notes_roots = [(REPO_NOTES_ROOT, True),
                       (LOCAL_NOTES_ROOT, False),
                       (LOCAL_NN_ROOT, False)]
    if watermark is None:
        watermark = watermark_path(owner)
    mark = load_watermark(watermark)

    files = scan_note_files(notes_roots)
    github_by_path = dict(files)
    if backfill:
        selected_files = [path for path, _g in files]
        seen_files = {path: _sha256_file(path) for path, _g in files}
    else:
        selected_files, seen_files = select_new_files(files, mark)

    entries = []
    entries_by_id = {}
    if store_path and os.path.exists(store_path):
        entries = scan_store_entries(store_path)
        for line_no, entry, _digest in entries:
            if entry is not None:
                entries_by_id[entry["id"]] = (line_no, entry)
    if backfill:
        selected_entries = [entry for _ln, entry, _d in entries
                            if entry is not None]
        seen_entries = {entry["id"]: digest
                        for _ln, entry, digest in entries
                        if entry is not None}
    else:
        selected_entries, seen_entries = select_new_entries(entries, mark)

    stats = {
        "owner": owner,
        "backfill": bool(backfill),
        "dry_run": bool(dry_run),
        "files_scanned": len(files),
        "files_new": len(selected_files),
        "entries_scanned": len(entries_by_id),
        "entries_new": len(selected_entries),
        "organized": 0,
        "duplicates_skipped": 0,
        "files_skipped_unparseable": 0,
        "entries_skipped_malformed": sum(
            1 for _ln, entry, _d in entries if entry is None),
        "block_ids": [],
    }

    blocks = []
    seen_ids = set()
    for path in selected_files:
        try:
            block = file_to_block(path, github_by_path.get(path, ""),
                                  owner)
        except (ValueError, UnicodeDecodeError):
            stats["files_skipped_unparseable"] += 1
            continue
        if block["id"] in seen_ids:
            stats["duplicates_skipped"] += 1
            continue
        seen_ids.add(block["id"])
        blocks.append(block)
    for entry in selected_entries:
        line_no, _entry = entries_by_id[entry["id"]]
        block = store_entry_to_block(entry, line_no, owner, store_path)
        if block["id"] in seen_ids:
            stats["duplicates_skipped"] += 1
            continue
        seen_ids.add(block["id"])
        blocks.append(block)

    stats["organized"] = len(blocks)
    stats["block_ids"] = [b["id"] for b in blocks]

    if not dry_run:
        if blocks:
            append_blocks(owner, blocks)
        # The watermark advances only over what this run actually saw
        # on disk - a skipped (unparseable) file stays unmarked, so
        # the next run retries it instead of forgetting it.
        mark["owner"] = owner
        for path, digest in seen_files.items():
            if backfill or path in selected_files:
                mark["files"][path] = digest
        for entry_id, digest in seen_entries.items():
            if backfill or entry_id in {e["id"] for e in selected_entries}:
                mark["entries"][entry_id] = digest
        save_watermark(watermark, mark)
    stats["watermark"] = watermark
    stats["box"] = boxstore.box_dir(owner)
    return stats


def main(argv=None):
    """CLI: organize_hook.py [--owner shawn] [--backfill] [--dry-run]
    [--watermark PATH] [--boxes-root PATH]. Prints one JSON summary
    line. Exit 0 on success, 2 on usage error, 1 on a failed run."""
    import argparse
    parser = argparse.ArgumentParser(
        description="Organize new notes and store entries into a "
                    "Smart Box.")
    parser.add_argument("--owner", default=DEFAULT_OWNER)
    parser.add_argument("--backfill", action="store_true",
                        help="organize the whole live note tree once, "
                             "ignoring the watermark")
    parser.add_argument("--dry-run", action="store_true",
                        help="select and convert, but write nothing")
    parser.add_argument("--watermark", default=None)
    parser.add_argument("--boxes-root", default=None)
    parser.add_argument("--store", default=STORE_PATH)
    args = parser.parse_args(argv)
    try:
        stats = run(owner=args.owner, backfill=args.backfill,
                    store_path=args.store, boxes_root=args.boxes_root,
                    watermark=args.watermark, dry_run=args.dry_run)
    except Exception as exc:  # noqa: BLE001 - the CLI reports, never traces
        print(json.dumps({"error": str(exc)}), file=sys.stderr)
        return 1
    print(json.dumps(stats, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())

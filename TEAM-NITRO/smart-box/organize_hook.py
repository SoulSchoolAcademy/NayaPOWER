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
SYNC_PATH = os.path.expanduser(
    "~/workspace/factory-pipeline/sync-smart-notes.py")

# One flow: the notes in GitHub and the Smart Box are one system, not
# two. The live-tree backfill IS the sync of the notes with the Box -
# the notes living inside her memory (organized, shelved, linked),
# not a copy sitting beside it. Understand -> learn -> grow -> know
# -> evolve: the backfill is the learn step made durable.

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


def content_to_block(content, github_path, owner):
    """One note's text -> an organized block. The same pipeline as
    ``file_to_block``, but from fetched text, not a disk file - the
    live-tree backfill converts what GitHub serves, byte for byte,
    through ``note_to_block`` -> ``organize`` -> ``complete_where``.
    Raises ValueError when the text is not a smart note."""
    block = note_to_block(content, owner=owner,
                          github_path=github_path)
    block = organize(block)
    block, _complete = complete_where(block)
    return block


def _load_gh_api():
    """``gh_api`` from the sync module, lazy-imported. The sync owns
    the GitHub App token path (in-memory mint, 401 re-mint); the hook
    never holds credentials, never mints, never writes a token."""
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "sync_smart_notes", SYNC_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.gh_api


def _fetch_note_content(gh_api, path, sha):
    """One note's text from the live tree. Contents API first; the
    git/blobs fallback when the Contents API returns no content
    (the large-file shape). A 403/429 (secondary rate limit) pauses
    60s and retries once per call - a limit mid-backfill must not
    kill the run; a 404 or any other failure raises, and the caller
    counts it and moves on (the watermark leaves it unmarked, so
    the next run retries it)."""
    import base64
    import time
    import urllib.error
    for attempt in range(3):
        try:
            data = gh_api("/contents/%s?ref=main" % path)
            if data.get("content"):
                return base64.b64decode(data["content"]).decode("utf-8")
            blob = gh_api("/git/blobs/%s" % sha)
            return base64.b64decode(blob["content"]).decode("utf-8")
        except urllib.error.HTTPError as exc:
            if exc.code in (403, 429) and attempt < 2:
                time.sleep(60)
                continue
            raise
    raise RuntimeError("fetch failed for %s" % path)


def live_tree_backfill(owner=DEFAULT_OWNER, boxes_root=None,
                       watermark=None, batch_size=100, gh_api_fn=None):
    """Backfill the owner's box from the LIVE GitHub tree - never the
    local clone (the stale-clone backfill named 789 of 1,547 state
    paths; the completeness gate correctly refused it every run).

    The tree is the source of what exists; the box is where it
    lives. Fetch the recursive tree (REFUSE when truncated - a
    partial listing must never read as the whole corpus), take every
    SMART-NOTES ``.md`` blob, and fetch + convert + append each one
    whose blob sha differs from the watermark's ``live_tree`` record
    (missing or changed since the last live-tree run). A changed note
    re-appends, superseding by block id, per ``boxstore`` - the box
    holds the current note, not the November-4th copy.

    Checkpointing: blocks append in batches (default 100) and the
    watermark advances per batch, so a failure mid-run loses at most
    one batch and the next run resumes where it stopped. One bad
    file (unparseable, or a fetch that fails) is counted and skipped,
    never fatal; ten consecutive fetch failures abort the run - that
    pattern means the token or the network died, not one bad file.

    ``gh_api_fn`` overrides the GitHub reader (tests pass a stub;
    live runs use the sync's ``gh_api``). Returns the stats dict
    (also printed by main)."""
    if boxes_root is not None:
        boxstore.BOXES_ROOT = boxes_root
    if watermark is None:
        watermark = watermark_path(owner)
    mark = load_watermark(watermark)
    seen_live = mark.get("live_tree", {})
    if not isinstance(seen_live, dict):
        raise ValueError("corrupt watermark: live_tree is not a map")
    gh_api = gh_api_fn or _load_gh_api()
    tree = gh_api("/git/trees/main?recursive=1")
    if tree.get("truncated"):
        raise ValueError(
            "live tree truncated - refusing a partial backfill")
    live = {t["path"]: t.get("sha") for t in tree.get("tree", [])
            if "SMART-NOTES/" in t["path"]
            and t["path"].endswith(".md") and t["type"] == "blob"}
    selected = sorted(p for p, sha in live.items()
                      if seen_live.get(p) != sha)
    stats = {
        "owner": owner,
        "live_tree": True,
        # The trees endpoint returns the resolved ref's sha here -
        # the tip COMMIT of main at read time, not the tree-object
        # sha (verified 2026-11-09: it equalled the tip commit twice).
        # It identifies exactly which main this backfill read.
        "main_commit": tree.get("sha"),
        "live_paths": len(live),
        "selected": len(selected),
        "fetched": 0,
        "organized": 0,
        "duplicates_skipped": 0,
        "skipped_unparseable": 0,
        "fetch_errors": 0,
        "block_ids": [],
    }
    blocks = []
    seen_ids = set()
    consecutive_errors = 0
    for path in selected:
        try:
            content = _fetch_note_content(gh_api, path, live[path])
        except Exception:  # noqa: BLE001 - counted, never fatal
            stats["fetch_errors"] += 1
            consecutive_errors += 1
            if consecutive_errors >= 10:
                raise RuntimeError(
                    "live-tree backfill aborted: 10 consecutive "
                    "fetch failures (token or network, not one bad "
                    "file) after %d organized"
                    % stats["organized"])
            continue
        consecutive_errors = 0
        stats["fetched"] += 1
        try:
            block = content_to_block(content, path, owner)
        except (ValueError, UnicodeDecodeError):
            stats["skipped_unparseable"] += 1
            continue
        if block["id"] in seen_ids:
            stats["duplicates_skipped"] += 1
            continue
        seen_ids.add(block["id"])
        blocks.append(block)
        stats["block_ids"].append(block["id"])
        if len(blocks) >= batch_size:
            append_blocks(owner, blocks)
            stats["organized"] += len(blocks)
            for block in blocks:
                seen_live[block["where"]["github_path"]] = \
                    live[block["where"]["github_path"]]
            mark["live_tree"] = seen_live
            mark["owner"] = owner
            save_watermark(watermark, mark)
            blocks = []
    if blocks:
        append_blocks(owner, blocks)
        stats["organized"] += len(blocks)
        for block in blocks:
            seen_live[block["where"]["github_path"]] = \
                live[block["where"]["github_path"]]
        mark["live_tree"] = seen_live
        mark["owner"] = owner
        save_watermark(watermark, mark)
    stats["watermark"] = watermark
    stats["box"] = boxstore.box_dir(owner)
    return stats


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
    """CLI: organize_hook.py [--owner shawn] [--backfill] [--live-tree]
    [--dry-run] [--watermark PATH] [--boxes-root PATH]. Prints one
    JSON summary line. Exit 0 on success, 2 on usage error, 1 on a
    failed run."""
    import argparse
    parser = argparse.ArgumentParser(
        description="Organize new notes and store entries into a "
                    "Smart Box.")
    parser.add_argument("--owner", default=DEFAULT_OWNER)
    parser.add_argument("--backfill", action="store_true",
                        help="organize the whole live note tree once, "
                             "ignoring the watermark")
    parser.add_argument("--live-tree", action="store_true",
                        help="backfill the box from the LIVE GitHub "
                             "tree (never the local clone): fetch "
                             "every SMART-NOTES file whose blob sha "
                             "differs from the watermark's live_tree "
                             "record, convert, organize, append")
    parser.add_argument("--dry-run", action="store_true",
                        help="select and convert, but write nothing")
    parser.add_argument("--watermark", default=None)
    parser.add_argument("--boxes-root", default=None)
    parser.add_argument("--store", default=STORE_PATH)
    args = parser.parse_args(argv)
    try:
        if args.live_tree:
            stats = live_tree_backfill(
                owner=args.owner, boxes_root=args.boxes_root,
                watermark=args.watermark)
        else:
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

#!/usr/bin/env python3
"""box_source.py - read the Smart Box as the sync's source of what exists.

Lane B of the Smart Box wiring pass (brief 20261109, section 1b): the
sync (the step that builds the feed) reads the box's map/brain as its
source of what exists, instead of the GitHub tree listing.

The box layout is the ONE layout in ``boxstore.py`` - never invented
here, never a second one:

    ~/workspace/nitro-smart-box/boxes/<owner>/
        blocks.jsonl   one block JSON per line, last line wins per id.
        keys.jsonl     key registry log (identifiers only).
        manifest.json  counts + sha256 of both files.

What this module does:

    list_note_paths_from_box(owner)  the source list: every block
        whose ``where.github_path`` names a SMART-NOTES ``.md`` file,
        newest first (reverse alphabetical - the same order the sync
        loop already walks, so a catch-up run lands today's notes
        before the older backfill).
    map_view_for_owner(owner)        {block id: map view} - what the
        map reads: ``about`` + ``what`` + ``links`` only, never the
        raw body (``block.map_view``).
    brain_view_for_owner(owner)      {block id: brain view} - what the
        brain reads: the distilled essence with its title and topics
        (``block.brain_view``).
    get_block_from_box(owner, id)    one block by id, or None.
    box_is_complete_for_state(owner, state_paths)
        the completeness gate the sync uses before trusting the box:
        every path the sync state tracks must be named in the box.
        A box that is missing or unreadable raises BoxSourceError;
        a box that is readable but incomplete reports its missing
        paths - the sync then FALLS BACK to the old GitHub-tree path
        and never breaks the feed.

Failure rule (the feed must never break): a missing or unreadable
box is an ERROR the caller falls back on, never an empty list
pretending nothing exists. An empty-but-readable box returns an
empty list - and the completeness gate then refuses it, because
the live state tracks 1,500+ paths.

Standard library only. No credentials, no secrets, no key material.
"""

import json
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

import boxstore  # noqa: E402
from block import brain_view, map_view  # noqa: E402

DEFAULT_OWNER = "shawn"


class BoxSourceError(Exception):
    """The box is missing or unreadable - fall back, never invent."""


def _blocks_path(owner, boxes_root=None):
    root = boxes_root or boxstore.BOXES_ROOT
    return os.path.join(root, owner, boxstore.BLOCKS_NAME)


def _read_blocks(owner, boxes_root=None):
    """All blocks in the owner's box, via boxstore. Raises
    BoxSourceError when the box directory or blocks file is missing
    or a line is not valid JSON - the caller falls back to the old
    path. A readable box with zero blocks returns {} (an empty box,
    which the completeness gate then refuses)."""
    path = _blocks_path(owner, boxes_root)
    if not os.path.exists(path):
        raise BoxSourceError(
            "box missing or unreadable: no %s for owner %r"
            % (boxstore.BLOCKS_NAME, owner))
    try:
        if boxes_root is not None:
            saved = boxstore.BOXES_ROOT
            boxstore.BOXES_ROOT = boxes_root
            try:
                return boxstore.read_blocks(owner)
            finally:
                boxstore.BOXES_ROOT = saved
        return boxstore.read_blocks(owner)
    except (ValueError, OSError) as exc:
        raise BoxSourceError(
            "box unreadable for owner %r: %s" % (owner, exc))


def _is_smart_note_path(github_path):
    """A GitHub path names a smart-note file: a ``.md`` file under
    ``SMART-NOTES/``. Nothing else in the box is a feed source."""
    return bool(github_path) and "SMART-NOTES/" in github_path \
        and github_path.endswith(".md")


def list_note_paths_from_box(owner=DEFAULT_OWNER, boxes_root=None):
    """The box's source list of smart-note files, newest first.

    Reverse alphabetical order: paths are zero-padded YYYY/MM/DD,
    so this puts today's notes first - the same order the sync's
    ingest loop already walks. Raises BoxSourceError when the box
    is missing or unreadable."""
    blocks = _read_blocks(owner, boxes_root)
    paths = [b["where"]["github_path"] for b in blocks.values()
             if isinstance(b.get("where"), dict)
             and _is_smart_note_path(b["where"].get("github_path"))]
    paths.sort(reverse=True)
    return paths


def get_block_from_box(owner, block_id, boxes_root=None):
    """One block by id from the owner's box, or None. Raises
    BoxSourceError when the box is missing or unreadable."""
    blocks = _read_blocks(owner, boxes_root)
    return blocks.get(block_id)


def map_view_for_owner(owner=DEFAULT_OWNER, boxes_root=None):
    """{block id: map view} for every block in the owner's box.

    The map reads ``about`` + ``what`` + ``links`` only - never the
    raw body. Raises BoxSourceError when the box is missing or
    unreadable."""
    blocks = _read_blocks(owner, boxes_root)
    return {block_id: map_view(block)
            for block_id, block in blocks.items()}


def brain_view_for_owner(owner=DEFAULT_OWNER, boxes_root=None):
    """{block id: brain view} for every block in the owner's box.

    The brain reads the distilled essence with its title and topics.
    Raises BoxSourceError when the box is missing or unreadable."""
    blocks = _read_blocks(owner, boxes_root)
    return {block_id: brain_view(block)
            for block_id, block in blocks.items()}


def box_is_complete_for_state(owner, state_paths, boxes_root=None):
    """The completeness gate: is every path the sync state tracks
    named in the box's source list?

    Returns (complete, missing): ``complete`` True only when no
    state path is missing from the box; ``missing`` lists the state
    paths the box does not name (empty when complete). A missing or
    unreadable box raises BoxSourceError - the caller falls back.
    A readable-but-incomplete box is NOT an error here: it returns
    complete False, and the caller falls back on that too. The box
    may name MORE paths than the state (notes organized but not yet
    synced) - that is fine, they sync as new."""
    box_paths = set(list_note_paths_from_box(owner, boxes_root))
    missing = sorted(p for p in state_paths if p not in box_paths)
    return (not missing), missing

#!/usr/bin/env python3
"""boxstore.py - the ONE Smart Box layout (Smart Box wiring, piece 1).

Restored 2026-11-10 (Naya Kappa w3013): the module was never tracked
in git - the four smart-box test files import it, but no boxstore.py
ever landed - so plain ``pytest -q`` interrupted at collection with
``ModuleNotFoundError: No module named 'boxstore'``. This file is
rebuilt from the consumers as the spec: ``box_source.py``,
``keybox.py``, ``organize_hook.py``, ``build_my_box.py`` and the four
test files name every function below, and the tests prove it.

The layout - one per owner, never a second one:

    ~/workspace/nitro-smart-box/boxes/<owner>/
        blocks.jsonl   one block JSON per line, last line wins per id.
        keys.jsonl     key registry log (identifiers only).
        manifest.json  counts + sha256 of both files.

Functions:

    box_dir(owner)            the owner's box directory.
    ensure_box(owner)         create the dir + the two logs + the
                              manifest when missing; never clobbers.
    append_block(owner, block) append one JSON line (sorted keys,
                              UTF-8) and refresh the manifest.
    read_blocks(owner)        {id: block}, last line wins per id;
                              a corrupt line raises ValueError.
    write_manifest(owner)     counts (lines) + sha256 of both logs.
    append_key_event(owner, event) append one key log line and
                              refresh the manifest.
    registry_from_box(owner)  the KeyRegistry rebuilt by replaying
                              the box's key events through the public
                              mint / revoke API. Mint generates the
                              same key ids deterministically, so the
                              rebuilt registry IS the recorded one.
                              A revoke for a key the replay never
                              minted is skipped, never fatal.

Standard library only. No credentials, no secrets, no key material.
"""

import hashlib
import json
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

BOXES_ROOT = os.path.expanduser("~/workspace/nitro-smart-box/boxes")
BLOCKS_NAME = "blocks.jsonl"
KEYS_NAME = "keys.jsonl"
MANIFEST_NAME = "manifest.json"


def box_dir(owner):
    """The owner's box directory under the current BOXES_ROOT."""
    return os.path.join(BOXES_ROOT, owner)


def _sha256_file(path):
    """Hex sha256 of a file's bytes; the empty hash when missing."""
    digest = hashlib.sha256()
    try:
        with open(path, "rb") as handle:
            for chunk in iter(lambda: handle.read(65536), b""):
                digest.update(chunk)
    except OSError:
        return hashlib.sha256(b"").hexdigest()
    return digest.hexdigest()


def _count_lines(path):
    """Non-empty lines in a file; 0 when the file is missing."""
    try:
        with open(path, "r", encoding="utf-8") as handle:
            return sum(1 for line in handle if line.strip())
    except OSError:
        return 0


def write_manifest(owner):
    """Rewrite manifest.json: counts + sha256 of both box files.

    ``blocks`` counts lines in blocks.jsonl (a re-appended block is
    a second line - the manifest counts what is on disk, and
    ``read_blocks`` collapses by id). ``keys`` counts key events.
    """
    directory = box_dir(owner)
    os.makedirs(directory, exist_ok=True)
    blocks_path = os.path.join(directory, BLOCKS_NAME)
    keys_path = os.path.join(directory, KEYS_NAME)
    manifest = {
        "owner": owner,
        "blocks": _count_lines(blocks_path),
        "keys": _count_lines(keys_path),
        "blocks_sha256": _sha256_file(blocks_path),
        "keys_sha256": _sha256_file(keys_path),
    }
    tmp_path = os.path.join(directory, MANIFEST_NAME + ".tmp")
    with open(tmp_path, "w", encoding="utf-8") as handle:
        handle.write(json.dumps(manifest, sort_keys=True, indent=2)
                     + "\n")
    os.replace(tmp_path, os.path.join(directory, MANIFEST_NAME))
    return manifest


def ensure_box(owner):
    """Create the owner's box when missing; never clobber it.

    Creates the directory, empty blocks.jsonl + keys.jsonl when
    absent, and the manifest when absent. Returns the box dir.
    """
    directory = box_dir(owner)
    os.makedirs(directory, exist_ok=True)
    for name in (BLOCKS_NAME, KEYS_NAME):
        path = os.path.join(directory, name)
        if not os.path.exists(path):
            with open(path, "w", encoding="utf-8"):
                pass
    if not os.path.exists(os.path.join(directory, MANIFEST_NAME)):
        write_manifest(owner)
    return directory


def append_block(owner, block):
    """Append one block to the owner's box and refresh the manifest.

    The line is ``json.dumps(block, sort_keys=True,
    ensure_ascii=False)`` - byte-identical to what
    ``organize_hook.append_blocks`` writes for a batch. Raises
    ValueError for anything that is not a block (no ``id``).
    """
    if not isinstance(block, dict) or "id" not in block:
        raise ValueError("append_block needs a block with an id, "
                         "not %r" % type(block))
    ensure_box(owner)
    with open(os.path.join(box_dir(owner), BLOCKS_NAME),
              "a", encoding="utf-8") as handle:
        handle.write(json.dumps(block, sort_keys=True,
                                ensure_ascii=False) + "\n")
    write_manifest(owner)


def read_blocks(owner):
    """All blocks in the owner's box, {id: block}, last line wins.

    Raises ValueError on a corrupt (non-JSON) line or a line with
    no ``id``; raises OSError when the blocks file is missing.
    A readable box with zero blocks returns {}.
    """
    blocks = {}
    with open(os.path.join(box_dir(owner), BLOCKS_NAME),
              encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            block = json.loads(line)
            if not isinstance(block, dict) or "id" not in block:
                raise ValueError(
                    "block line without an id in %s for owner %r"
                    % (BLOCKS_NAME, owner))
            blocks[block["id"]] = block
    return blocks


def append_key_event(owner, event):
    """Append one key event to the owner's keys.jsonl.

    Events are identifiers only (event / key_id / owner_id /
    naya_id / seq) - never key material. Refreshes the manifest.
    """
    if not isinstance(event, dict) or "event" not in event:
        raise ValueError("append_key_event needs an event dict, "
                         "not %r" % type(event))
    ensure_box(owner)
    with open(os.path.join(box_dir(owner), KEYS_NAME),
              "a", encoding="utf-8") as handle:
        handle.write(json.dumps(event, sort_keys=True,
                                ensure_ascii=False) + "\n")
    write_manifest(owner)


def _read_key_events(owner):
    """The owner's key events in order; [] when the box is missing.

    Raises ValueError on a corrupt (non-JSON) line.
    """
    path = os.path.join(box_dir(owner), KEYS_NAME)
    try:
        handle = open(path, encoding="utf-8")
    except OSError:
        return []
    with handle:
        events = []
        for line in handle:
            if line.strip():
                events.append(json.loads(line))
        return events


def registry_from_box(owner):
    """The owner's KeyRegistry, rebuilt from the owner's box.

    Replays each key event through the public mint / revoke API, in
    order. A box with no key events is an empty registry - it
    denies every keyed path, by design. A revoke for a key the
    replay never minted stays in keys.jsonl as a record; the
    replay skips it and the registry stays honest about what it
    holds.
    """
    from gate import KeyRegistry

    registry = KeyRegistry()
    for event in _read_key_events(owner):
        kind = event.get("event")
        if kind == "mint":
            event_owner = event.get("owner_id", owner)
            event_naya = event.get("naya_id")
            if event_naya is None:
                continue
            try:
                registry.mint(event_owner, event_naya,
                              issued_by=event_owner)
            except ValueError:
                continue
        elif kind == "revoke":
            try:
                registry.revoke(event.get("key_id"), revoked_by=owner)
            except (KeyError, ValueError):
                continue
    return registry

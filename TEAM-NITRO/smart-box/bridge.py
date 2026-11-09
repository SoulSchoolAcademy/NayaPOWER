#!/usr/bin/env python3
"""bridge.py - the bridge: carry a block from one box to another.

The Smart Box, piece 5 of 5. The sync, extended: sharing a smart note
carries the block from a box to the shared space, and building a space
from a note is one click because the note already IS a block.

A box here is an in-memory holder - ``Box(owner)`` with ``put`` /
``get`` / ``has`` - not a new database. The store is still GitHub +
Supabase + Cloudflare; the bridge is the carrying, not the storing.

Rules (blueprint section 3.5), enforced in code:

    1. The bridge never moves a block the gate would deny: every carry
       goes through ``may_share`` with action "share", every time, no
       fast path. A carry that fails the gate returns DENY and moves
       nothing.
    2. The bridge never rewrites a block in transit: the block that
       arrives is the block that left, ``id`` and ``raw`` intact -
       proven by JSON round-trip (serialize, deserialize, compare).
       Only ``where`` gains two provenance lines (carried_from,
       carried_to) and ``proof`` names the carry; the content fields
       are untouched.
    3. The bridge never touches mail or messages: it carries blocks
       between boxes and shared spaces, nothing else.
    4. A second click never duplicates a space: ``build_space_from_note``
       checks the space exists before it builds it again, and returns
       the existing space with status EXISTS.

Standard library only. No credentials, no secrets, no key material.
"""

import json

from block import block_from_json, block_to_json, slugify
from gate import DENY, KeyRegistry, may_share  # noqa: F401  (KeyRegistry re-exported)


class Box(object):
    """One citizen's box: an owner and the blocks inside it."""

    def __init__(self, owner):
        self.owner = owner
        self._blocks = {}

    def put(self, block):
        """Store a copy of a block (the box keeps its own copy)."""
        stored = block_from_json(block_to_json(block))
        self._blocks[stored["id"]] = stored
        return stored

    def get(self, block_id):
        """A copy of the block, or None."""
        block = self._blocks.get(block_id)
        return block_from_json(block_to_json(block)) if block else None

    def has(self, block_id):
        return block_id in self._blocks

    def ids(self):
        return sorted(self._blocks)

    def __len__(self):
        return len(self._blocks)


def carry(block, actor, source_box, dest_box, key_registry=None):
    """Carry a block from ``source_box`` to ``dest_box``.

    Returns (status, carried_block_or_None, receipt). Status is
    "CARRIED", "DENY", or "DUPLICATE":

    - DENY: the gate said no (``may_share`` action "share"). Nothing
      moves, nothing is written to the destination.
    - DUPLICATE: the destination already holds this block id. The
      second carry is refused, not copied twice.
    - CARRIED: the destination now holds a block identical to the
      source in every content field (``id`` and ``raw`` intact,
      verified by JSON round-trip comparison before storing).

    The receipt names the block, the two boxes, and the gate verdict -
    it is the record the bridge leaves behind.
    """
    verdict = may_share(block, actor, "share",
                        key_registry=key_registry)
    receipt = {"block_id": block.get("id") if isinstance(block, dict) else None,
               "from": getattr(source_box, "owner", None),
               "to": getattr(dest_box, "owner", None),
               "gate": verdict}
    if verdict != "ALLOW":
        receipt["status"] = "DENY"
        return "DENY", None, receipt
    if dest_box.has(block["id"]):
        receipt["status"] = "DUPLICATE"
        return "DUPLICATE", dest_box.get(block["id"]), receipt
    arrived = block_from_json(block_to_json(block))
    if arrived != block:
        receipt["status"] = "DENY"
        receipt["reason"] = "block changed in transit"
        return "DENY", None, receipt
    arrived["where"]["carried_from"] = source_box.owner
    arrived["where"]["carried_to"] = dest_box.owner
    arrived["proof"] = ("bridge: carried %s -> %s, gate share ALLOW"
                        % (source_box.owner, dest_box.owner))
    stored = dest_box.put(arrived)
    receipt["status"] = "CARRIED"
    return "CARRIED", stored, receipt


def build_space_from_note(note_block, actor, box, key_registry=None):
    """Build a space from a note: one click, because the note already
    IS a block. Returns (status, space_block, receipt).

    Status is "BUILT" or "EXISTS": the second click finds the space
    already there and returns it, never a duplicate. The space's id is
    derived from the note, so the same note always names the same
    space. The actor must be allowed to retrieve the note (the owner,
    or a keyed Naya retrieving for the owner) - otherwise DENY.
    """
    verdict = may_share(note_block, actor, "retrieve",
                        key_registry=key_registry)
    space_id = "%s:space:%s" % (
        (note_block.get("who") or {}).get("owner", ""),
        slugify(note_block.get("what", "")))
    receipt = {"note_id": note_block.get("id"), "space_id": space_id,
               "gate": verdict}
    if verdict != "ALLOW":
        receipt["status"] = "DENY"
        return "DENY", None, receipt
    if box.has(space_id):
        receipt["status"] = "EXISTS"
        return "EXISTS", box.get(space_id), receipt
    space = {
        "id": space_id,
        "kind": "space",
        "what": note_block.get("what", ""),
        "about": list(note_block.get("about") or []),
        "who": dict(note_block.get("who") or {}),
        "when": dict(note_block.get("when") or {}),
        "where": dict(note_block.get("where") or {}),
        "visibility": note_block.get("visibility", "private"),
        "body": "",
        "links": [note_block["id"]] + list(note_block.get("links") or []),
        "source": note_block.get("source", ""),
        "proof": "bridge: space built from note %s in one click"
                 % note_block.get("id"),
        "essence": note_block.get("essence", ""),
        "owner_shared_choice": bool(note_block.get("owner_shared_choice")),
        "body_open_to": [],
        "raw": {"built_from_note": note_block["id"]},
    }
    stored = box.put(space)
    receipt["status"] = "BUILT"
    return "BUILT", stored, receipt

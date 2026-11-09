#!/usr/bin/env python3
"""gate.py - may_share: the permission gate for the Smart Box.

The Smart Box, piece 2 of 5. Built the same way as the design-contract
gate (``design-contract-gate/check-gate.py``): a check that BLOCKS, not
advises. There is no other way in - this gate sits between every reader
and every thing.

    may_share(block, actor, action) -> "ALLOW" / "DENY"

Actions: "read" (the whole thing, raw body included), "organize" (the map
and the brain only - about + what + links + essence, never the raw body),
"share" (carry the block out to someone else), "retrieve" (hand the
owner's own thing back to them, or post it where they say, in their name).

Rules, in order (brief section 3):

    1. The owner may do anything with their own block.
    2. A Naya holding an organize key for that owner may read the map and
       the brain - never the raw body, unless the owner opened that block
       to that Naya (``body_open_to`` on the block).
    3. Sharing requires BOTH: the block is a public smart note AND the
       owner chose to make it so. Either one missing = DENY.
    4. Retrieve-for-owner: the owner asks, the gate hands it back - or
       posts it where they say, in their name. A Naya holding the owner's
       organize key may retrieve for the owner; that is the hands, not
       the ownership.
    5. Everything else = DENY. No key = DENY. Revoked key = DENY.
       Default is DENY, never allow.

A key is per-person, per-Naya, revocable. It is an opaque identifier
here - this file never holds key material, only key ids and their
status, the way a lock holds a key's shape and not its metal. The
key's issue, storage, and revocation are specified in the blueprint
(piece 4); this gate only checks what it is handed.

Actors are authenticated upstream: ``may_share`` trusts the actor id
it is given, the way a lock trusts the hand turning it. Authentication
happens before the call, in the plug (blueprint piece 4) - never inside
this gate, and never guessed from a name.

Standard library only.
"""

ALLOW = "ALLOW"
DENY = "DENY"

ACTIONS = ("read", "organize", "share", "retrieve")


class Key(object):
    """One plug-in permission: per-person, per-Naya, revocable.

    ``scope`` is "organize": the key lets its Naya organize the owner's
    map and brain, and retrieve things for the owner. It never lets the
    Naya read a raw body or share a block on its own - those need the
    owner's opening (rule 2) or the owner's public choice (rule 3).
    ``status`` is "active" or "revoked". A revoked key is a dead key:
    it denies exactly like no key at all.
    """

    def __init__(self, key_id, owner_id, naya_id, scope="organize",
                 status="active"):
        self.key_id = key_id
        self.owner_id = owner_id
        self.naya_id = naya_id
        self.scope = scope
        self.status = status

    def is_active_for(self, owner_id, naya_id=None):
        """True only when this key is live, for this owner, and (when
        asked) held by this Naya. A revoked key never counts."""
        if self.status != "active":
            return False
        if self.owner_id != owner_id:
            return False
        if naya_id is not None and self.naya_id != naya_id:
            return False
        return True

    def __repr__(self):
        return "Key(%s, owner=%s, naya=%s, scope=%s, status=%s)" % (
            self.key_id, self.owner_id, self.naya_id, self.scope,
            self.status)


def make_actor(actor_id, kind, keys=None):
    """Build an actor record. ``kind`` is "owner", "naya", "stranger",
    or "anyone" - a label for humans; the gate decides on ids and keys,
    never on the label alone."""
    return {"id": actor_id, "kind": kind, "keys": list(keys or [])}


def _active_organize_key(actor, owner_id):
    """The actor's live organize key for this owner, or None.

    No key, a revoked key, or a key for someone else all come back
    None - and None always means DENY further down.
    """
    for key in actor.get("keys") or []:
        if isinstance(key, Key) and key.scope == "organize":
            if key.is_active_for(owner_id, actor.get("id")):
                return key
    return None


def _is_public_smart_note(block):
    """A public smart note, by the owner's choice: BOTH halves of rule 3.

    Visibility alone is not enough, and the choice alone is not enough.
    A block the owner never chose to publish stays private even if a
    field somewhere says "public", and a chosen note that was never
    marked public stays unreadable to strangers.
    """
    return (block.get("visibility") == "public"
            and bool(block.get("owner_shared_choice")))


def may_share(block, actor, action):
    """ALLOW or DENY. Default is DENY, never allow.

    The order is the law: owner first, then the public note anyone may
    read, then the keyed Naya's organize / retrieve / share, then the
    owner's explicit opening of a raw body. Anything that reaches the
    end is denied, and an unknown action is denied too.
    """
    if not isinstance(block, dict) or not isinstance(actor, dict):
        return DENY
    if action not in ACTIONS:
        return DENY
    owner_id = (block.get("who") or {}).get("owner")
    if owner_id is None:
        return DENY

    # Rule 1: the owner may do anything with their own block.
    if actor.get("id") == owner_id:
        return ALLOW

    # Rule 3, read half: anyone may read a public smart note - the
    # owner chose it public, so the body is public too.
    if action == "read" and _is_public_smart_note(block):
        return ALLOW

    key = _active_organize_key(actor, owner_id)
    if key is None:
        # Rule 5: no key = DENY. Revoked key = DENY (it never reaches
        # here as a live key). There is nothing more to check.
        return DENY

    # Rule 2, map and brain: the organize key opens the map and the
    # brain - about, what, links, essence - never the raw body.
    if action == "organize":
        return ALLOW

    # Rule 4: retrieve-for-owner. The keyed Naya is the hands handing
    # the owner's own thing back, or posting it where the owner said,
    # in the owner's name. The thing stays the owner's either way.
    if action == "retrieve":
        return ALLOW

    # Rule 3, share half: the keyed Naya may share only what the owner
    # already chose public. Without the owner's choice, the Naya's key
    # is not a permission to publish.
    if action == "share" and _is_public_smart_note(block):
        return ALLOW

    # Rule 2, raw body: the keyed Naya may read the raw body only when
    # the owner opened that block to them by name. Otherwise DENY.
    if action == "read" and actor.get("id") in (block.get("body_open_to") or []):
        return ALLOW

    # Rule 5: everything else = DENY.
    return DENY

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
it is given, the way a lock trusts the hand turning it. The KEY, though,
is proven per call, not trusted: with a ``KeyRegistry`` (piece 4) the
gate checks the key was minted by the owner for this Naya and is still
live in the registry - a hand-built Key object claiming "active" does
not open anything. Without a registry the gate fails closed: every
keyed path DENYs, even for a genuine minted key. Authentication of the
person happens before the call, in the plug (blueprint piece 4); proof
of the key happens inside this gate, on every call.

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


# ---------------------------------------------------------------------------
# Piece 4 - the key lifecycle: mint, check, revoke. Checked on EVERY
# call, through the registry - never trusted blindly from upstream.
#
# First pass gap, closed here: ``may_share`` used to trust whatever
# Key object the caller handed it. A caller could build a Key with
# status "active" out of thin air and the gate believed it. Now the
# proof path is ``may_share(..., key_registry=registry)``: a key counts
# only when the registry minted it, it is still active in the registry,
# and it matches this owner and this Naya. A forged key, a revoked key,
# a key for another owner, a key held by another Naya - all DENY.
#
# The registry holds identifiers only: key id, owner id, Naya id,
# scope, status, and the issue / revoke record (who, which sequence).
# No key material - no secret, no token, no credential - is ever
# written here, into a log, a note, or a block. The key is an
# identifier the gate checks, never a value anyone can copy out.
#
# Rules (blueprint section 3.4): one key per (owner, Naya) pair - a
# second mint for the same pair returns the live key, never a second
# live key. Issue and revoke are the owner's acts only. Revoke is
# instant and total: every later call denies, and no cached "she was
# allowed before" survives it, because every call re-checks the
# registry. ``may_share`` FAILS CLOSED without a registry: a Naya
# actor's key counts only when a registry is supplied and the key is
# live in it. A caller that forgets the registry gets DENY for every
# keyed path - the old first-pass behaviour (trusting a Key object as
# handed, with no registry) is GONE, not kept. The only no-registry
# ALLOWs are the two paths that need no key by design: the owner on
# their own block (rule 1) and anyone reading a public smart note
# (rule 3, read half).
# ---------------------------------------------------------------------------

class KeyRegistry(object):
    """The record of who holds which key, and whether it is live."""

    def __init__(self):
        self._keys = {}
        self._seq = 0
        self._log = []

    def mint(self, owner_id, naya_id, issued_by=None):
        """Issue the (owner, Naya) key. Only the owner issues it.

        One live key per pair: minting again while one is live returns
        the live key. Minting after a revoke issues a fresh key id.
        Raises ValueError when anyone but the owner issues.
        """
        if issued_by is not None and issued_by != owner_id:
            raise ValueError("only the owner issues a key")
        for key in self._keys.values():
            if (key.owner_id == owner_id and key.naya_id == naya_id
                    and key.status == "active"):
                return key
        self._seq += 1
        key_id = "key-%s-%s-%04d" % (owner_id, naya_id, self._seq)
        key = Key(key_id, owner_id, naya_id)
        self._keys[key_id] = key
        self._log.append({"event": "mint", "key_id": key_id,
                          "owner_id": owner_id, "naya_id": naya_id,
                          "seq": self._seq})
        return key

    def revoke(self, key_id, revoked_by=None):
        """Revoke a key, instantly and totally. Only the owner revokes.

        Raises KeyError for an unknown key id, ValueError when anyone
        but the owner revokes. Revoking an already-revoked key is a
        no-op that still returns the key.
        """
        key = self._keys.get(key_id)
        if key is None:
            raise KeyError("unknown key: %s" % key_id)
        if revoked_by is not None and revoked_by != key.owner_id:
            raise ValueError("only the owner revokes a key")
        if key.status != "revoked":
            key.status = "revoked"
            self._log.append({"event": "revoke", "key_id": key_id,
                              "owner_id": key.owner_id,
                              "naya_id": key.naya_id, "seq": self._seq})
        return key

    def check(self, key_id, owner_id, naya_id=None):
        """True only when the registry holds this key live, for this
        owner, and (when asked) held by this Naya."""
        key = self._keys.get(key_id)
        if key is None:
            return False
        return key.is_active_for(owner_id, naya_id)

    def status(self, key_id):
        """'active' / 'revoked' / 'unknown' - never the key material."""
        key = self._keys.get(key_id)
        return key.status if key is not None else "unknown"

    def record(self, key_id):
        """The issue / revoke record for a key id, or None."""
        key = self._keys.get(key_id)
        if key is None:
            return None
        return {"key_id": key.key_id, "owner_id": key.owner_id,
                "naya_id": key.naya_id, "scope": key.scope,
                "status": key.status,
                "events": [e for e in self._log
                           if e["key_id"] == key_id]}

    def log(self):
        """The full mint / revoke log, in order. Identifiers only."""
        return [dict(entry) for entry in self._log]


def _active_organize_key(actor, owner_id, key_registry=None):
    """The actor's live organize key for this owner, or None.

    No key, a revoked key, or a key for someone else all come back
    None - and None always means DENY further down. A key counts only
    when a registry is given AND the key is live in the registry for
    this owner and this Naya: a Key object built by hand, however
    "active" it claims to be, does not count. WITHOUT a registry no
    key counts at all - the gate fails closed, never trusts a Key
    object as handed. The old no-registry trust is gone.
    """
    if key_registry is None:
        return None
    for key in actor.get("keys") or []:
        if isinstance(key, Key) and key.scope == "organize":
            if key.is_active_for(owner_id, actor.get("id")):
                if not key_registry.check(
                        key.key_id, owner_id, actor.get("id")):
                    continue
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


def may_share(block, actor, action, key_registry=None):
    """ALLOW or DENY. Default is DENY, never allow.

    The order is the law: owner first, then the public note anyone may
    read, then the keyed Naya's organize / retrieve / share, then the
    owner's explicit opening of a raw body. Anything that reaches the
    end is denied, and an unknown action is denied too.

    ``key_registry`` is the piece-4 proof path, and it is REQUIRED
    for every keyed path: a Naya's key counts only if the registry
    minted it and it is still live there. Without a registry the gate
    fails closed - every keyed action DENYs, even for a genuine minted
    key, because the proof cannot be checked. The owner on their own
    block (rule 1) and anyone reading a public smart note (rule 3,
    read half) need no key and are unaffected.
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

    key = _active_organize_key(actor, owner_id, key_registry)
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

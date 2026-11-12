#!/usr/bin/env python3
"""keybox.py - the durable key record (Smart Box wiring, lane C).

Every key issued or revoked is recorded in the OWNER'S BOX, not only
in a local registry file. The box is the record; the registry is
rebuilt from it.

    ~/workspace/nitro-smart-box/boxes/<owner>/keys.jsonl

one JSON object per mint / revoke event. Identifiers only - key id,
owner id, Naya id, scope, status, seq. No key material, no secret,
no token, no credential, ever. The key is an identifier the gate
checks, never a value anyone can copy out.

How it works, in order:

    issue(owner, naya)   load the registry from the owner's box,
                         mint through the public ``KeyRegistry.mint``
                         API (owner-only - anyone but the owner
                         raises), append the new log entry to
                         ``keys.jsonl``. Minting again while a key
                         for the pair is live returns the live key
                         and appends nothing - one live key per
                         (owner, Naya) pair, and the log holds only
                         events the registry actually created.
    revoke(owner, key_id) the same pattern through ``KeyRegistry.
                         revoke`` - owner-only, instant and total.
                         Revoking an already-revoked key appends
                         nothing.
    load_registry(owner)  ``boxstore.registry_from_box`` - the
                         registry rebuilt by replaying the box's
                         events through the public mint / revoke
                         API. Mint generates the same key ids
                         deterministically, so the rebuilt registry
                         IS the recorded registry.
    record(owner, key_id) ``registry.record(key_id)`` on the rebuilt
                         registry - the issue / revoke record for
                         that key id, or None.

The registry is NEVER rebuilt by writing private fields and a key
is NEVER invented: the only way a key enters the registry is a
mint event replayed through the public API, and the only way one
leaves is a revoke event replayed the same way. A revoke for a key
the replay never minted stays in ``keys.jsonl`` as a record, and
the registry stays honest about what it holds (see
``boxstore.registry_from_box``).

Standard library only. Takes ``gate.py`` and ``boxstore.py``
verbatim - this module only puts the registry on disk and reads
it back.
"""

import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

from boxstore import append_key_event, registry_from_box  # noqa: E402


def load_registry(owner):
    """The owner's registry, rebuilt from the owner's box.

    A box with no key events is an empty registry - it denies every
    keyed path, by design.
    """
    return registry_from_box(owner)


def issue(owner, naya, issued_by=None):
    """Issue the (owner, Naya) key and record it in the owner's box.

    Only the owner issues: ``issued_by`` defaults to the owner, and
    naming anyone else raises ValueError (the gate's rule, not a
    local invention). Returns the Key - the live key when one
    already exists for the pair, a fresh key id otherwise. Only a
    newly created key appends a log entry to ``keys.jsonl``.
    """
    registry = load_registry(owner)
    before = len(registry.log())
    key = registry.mint(owner, naya,
                        issued_by=owner if issued_by is None else issued_by)
    after = registry.log()
    if len(after) > before:
        append_key_event(owner, after[-1])
    return key


def revoke(owner, key_id):
    """Revoke a key and record it in the owner's box.

    Only the owner revokes: the call passes the owner as revoker,
    so revoking a key owned by someone else raises ValueError and
    an unknown key id raises KeyError (the gate's rules). Returns
    the key. Only a fresh revocation appends a log entry - revoking
    an already-revoked key appends nothing.
    """
    registry = load_registry(owner)
    before = len(registry.log())
    key = registry.revoke(key_id, revoked_by=owner)
    after = registry.log()
    if len(after) > before:
        append_key_event(owner, after[-1])
    return key


def record(owner, key_id):
    """The issue / revoke record for a key id, from the owner's box.

    Returns the record dict (key id, owner, Naya, scope, status,
    events) or None when the box holds no such key.
    """
    return load_registry(owner).record(key_id)

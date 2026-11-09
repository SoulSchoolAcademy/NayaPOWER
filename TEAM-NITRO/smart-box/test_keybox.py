#!/usr/bin/env python3
"""test_keybox.py - proof for the durable key record (lane C).

Run:  python3 test_keybox.py
Exit 0 only when every check passes; non-zero otherwise. Prints one
line per check, no tracebacks on failure - a failure names what is
missing.

What it proves, on a SCRATCH box root (a temp directory - no live
writes, no live box touched):

  A. issue mints and records: the mint event lands in the owner's
     keys.jsonl, identifiers only, and the rebuilt registry holds
     the same key id, live.
  B. One live key per pair: issuing again while live returns the
     same key id and appends no second event.
  C. revoke records: the revocation lands in keys.jsonl, the
     rebuilt registry holds the key revoked, and the gate DENYs
     organize for it.
  D. Fresh rebuild enforces: a registry rebuilt from the box
     (a new object, the way a fresh process rebuilds it) ALLOWs
     organize for a live key and DENYs for a revoked one - the
     gate's proof path, through the registry, never a hand-built
     Key trusted blindly.
  E. Mint after revoke issues a fresh key id (the seq moves on).
  F. Owner-only: issuing as anyone but the owner raises
     ValueError; revoking a key owned by someone else raises
     ValueError; revoking an unknown key id raises KeyError.
  G. record(): the issue / revoke record for a key id, or None
     for an unknown id; revoking twice appends one event only.
  H. No key material: nothing in keys.jsonl but identifiers -
     no secret, token, credential, or material field anywhere.

Fixtures: none needed beyond the box layout itself, which comes
from boxstore.py verbatim (boxes/<owner>/blocks.jsonl +
keys.jsonl + manifest.json). The suite reads and writes only
inside its own temp directory.
"""

import json
import os
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import boxstore  # noqa: E402
import keybox  # noqa: E402
from gate import Key, make_actor, may_share  # noqa: E402

CHECKS = []


def check(name, ok, detail=""):
    CHECKS.append((name, ok, detail))
    print("%s %s%s" % ("PASS" if ok else "FAIL", name,
                       (" - " + detail) if detail else ""))
    return ok


def key_events(owner):
    path = os.path.join(boxstore.box_dir(owner), boxstore.KEYS_NAME)
    with open(path, encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def main():
    tmp = tempfile.mkdtemp(prefix="keybox-test-")
    boxstore.BOXES_ROOT = os.path.join(tmp, "boxes")

    owner = "shawn"
    naya = "naya-nitro-narzan"
    block = {"id": "shawn:note:proof", "kind": "smart-note",
             "who": {"owner": owner}, "visibility": "private"}

    # A. issue mints and records.
    key = keybox.issue(owner, naya)
    events = key_events(owner)
    check("A1 issue returns a key for the pair",
          key.owner_id == owner and key.naya_id == naya
          and key.status == "active", key.key_id)
    check("A2 one mint event lands in the box keys.jsonl",
          len(events) == 1 and events[0].get("event") == "mint"
          and events[0].get("key_id") == key.key_id,
          str(events[0]) if events else "no events")
    rebuilt = keybox.load_registry(owner)
    check("A3 rebuilt registry holds the same key, live",
          rebuilt.check(key.key_id, owner, naya),
          key.key_id)

    # B. One live key per pair.
    again = keybox.issue(owner, naya)
    check("B1 second issue returns the same live key",
          again.key_id == key.key_id, again.key_id)
    check("B2 second issue appends no event",
          len(key_events(owner)) == 1)

    # C. revoke records, gate DENYs.
    keybox.revoke(owner, key.key_id)
    events = key_events(owner)
    check("C1 revoke event lands in the box keys.jsonl",
          len(events) == 2 and events[-1].get("event") == "revoke"
          and events[-1].get("key_id") == key.key_id,
          str(events[-1]) if events else "no events")
    rebuilt = keybox.load_registry(owner)
    check("C2 rebuilt registry holds the key revoked",
          rebuilt.status(key.key_id) == "revoked")
    actor = make_actor(naya, "naya", keys=[Key(key.key_id, owner, naya)])
    check("C3 gate DENYs organize for the revoked key",
          may_share(block, actor, "organize", key_registry=rebuilt) == "DENY")

    # D. Fresh rebuild enforces a live key.
    live = keybox.issue(owner, naya)
    fresh = keybox.load_registry(owner)
    actor = make_actor(naya, "naya", keys=[live])
    check("D1 fresh rebuild ALLOWs organize for a live key",
          may_share(block, actor, "organize", key_registry=fresh) == "ALLOW",
          live.key_id)
    check("D2 fresh rebuild DENYs a forged key id",
          may_share(block, make_actor(naya, "naya", keys=[
              Key("key-shawn-naya-nitro-narzan-9999", owner, naya)]),
              "organize", key_registry=fresh) == "DENY")

    # E. Mint after revoke issues a fresh key id.
    check("E1 mint after revoke is a fresh key id",
          live.key_id != key.key_id,
          "%s -> %s" % (key.key_id, live.key_id))

    # F. Owner-only.
    try:
        keybox.issue(owner, naya, issued_by="stranger")
        check("F1 issue by a non-owner raises", False, "no raise")
    except ValueError:
        check("F1 issue by a non-owner raises", True)
    try:
        # Owner-only is enforced by the gate on the owner's own
        # registry: a stranger revoking shawn's key raises, even
        # though the key exists in shawn's box.
        keybox.load_registry(owner).revoke(live.key_id, revoked_by="stranger")
        check("F2 revoke by a non-owner raises", False, "no raise")
    except ValueError:
        check("F2 revoke by a non-owner raises", True)
    try:
        keybox.revoke(owner, "key-no-such-key")
        check("F3 revoke of an unknown key raises", False, "no raise")
    except KeyError:
        check("F3 revoke of an unknown key raises", True)

    # G. record().
    rec = keybox.record(owner, live.key_id)
    check("G1 record returns the live key's record",
          rec is not None and rec["status"] == "active"
          and rec["key_id"] == live.key_id, str(rec))
    check("G2 record returns None for an unknown key id",
          keybox.record(owner, "key-no-such-key") is None)
    before = len(key_events(owner))
    keybox.revoke(owner, key.key_id)  # already revoked: no-op
    check("G3 revoking twice appends no second event",
          len(key_events(owner)) == before)
    rec = keybox.record(owner, key.key_id)
    check("G4 record shows the revoked key revoked, with both events",
          rec is not None and rec["status"] == "revoked"
          and len(rec["events"]) == 2, str(rec))

    # H. No key material anywhere in the box log.
    raw = "".join(
        open(os.path.join(boxstore.box_dir(owner), boxstore.KEYS_NAME),
             encoding="utf-8").readlines())
    lowered = raw.lower()
    check("H1 keys.jsonl holds identifiers only, no material",
          not any(word in lowered for word in
                  ("secret", "token", "credential", "material",
                   "password", "private_key")),
          "fields: %s" % sorted({k for e in key_events(owner) for k in e}))

    failed = [name for name, ok, _ in CHECKS if not ok]
    print("%d/%d checks passed" % (len(CHECKS) - len(failed), len(CHECKS)))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())

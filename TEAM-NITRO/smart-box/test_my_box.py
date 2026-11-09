#!/usr/bin/env python3
"""test_my_box.py - proof for MY box (owner naya-nitro-narzan), Lane D.

Run:  python3 test_my_box.py
Exit 0 only when every check passes; non-zero otherwise. Prints one
line per check, no tracebacks on failure - a failure names what is
missing.

Fixtures only, scratch BOXES_ROOT - no live writes in tests: the box
is built into a temp directory by patching boxstore.BOXES_ROOT, so
the live box at ~/workspace/nitro-smart-box/boxes/ is never touched.

What it proves:

  A. Shape: every block in my box is valid - id owner:kind:slug with
     owner naya-nitro-narzan, kind in block.KINDS, every required
     field present, visibility private, owner_shared_choice False,
     body_open_to empty, ids unique.
  B. Gate: the owner may read every block (rule 1, ALLOW); a stranger
     may read none of them (DENY); a forged key, a revoked key, and a
     key for another owner all DENY - with a real registry, and the
     no-registry path fails closed.
  C. Saved-game coverage: from the box alone, a fresh agent can answer
     who I am, what I stand for, what I am working on and where each
     thing stands, and what is owed - the block ids and the key facts
     are checked by value, not by presence of a file.
  D. Zero secrets: the box files on disk are scanned for
     credential/secret/key material (assignment patterns, private-key
     headers, provider token shapes) and the scan result is printed;
     any hit fails the suite. Key ids (identifiers like
     key-<owner>-<naya>-<seq>) are NOT secrets and are not flagged.
"""

import json
import os
import re
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import boxstore  # noqa: E402
import build_my_box  # noqa: E402
from block import KINDS  # noqa: E402
from gate import Key, KeyRegistry, make_actor, may_share  # noqa: E402

OWNER = build_my_box.OWNER

REQUIRED_FIELDS = ("id", "kind", "what", "about", "who", "when", "where",
                   "visibility", "body", "links", "source", "proof",
                   "essence", "owner_shared_choice", "body_open_to", "raw")

# Facts a fresh agent must be able to answer from the box alone.
# (block id, a string that must appear in that block's body.)
COVERAGE = [
    ("naya-nitro-narzan:note:who-i-am", "Naya Nitro Narzan"),
    ("naya-nitro-narzan:note:who-i-am", "captain of Team Nitro"),
    ("naya-nitro-narzan:note:who-i-am", "head delegator"),
    ("naya-nitro-narzan:note:the-vow", "ten stars"),
    ("naya-nitro-narzan:note:the-five-gates", "IS IT RIGHT"),
    ("naya-nitro-narzan:note:the-five-gates", "Shawn's hand"),
    ("naya-nitro-narzan:note:the-wise-one", "SN-0831"),
    ("naya-nitro-narzan:note:the-mission", "NayaNET"),
    ("naya-nitro-narzan:note:real-object-law", "real physical object"),
    ("naya-nitro-narzan:note:essence-01-record-truth", "cold reader"),
    ("naya-nitro-narzan:note:essences-02-07", "LEARN -> GROW"),
    ("naya-nitro-narzan:note:the-settled-ladders", "Power $25"),
    ("naya-nitro-narzan:note:privacy-law", "do NOT read mail"),
    ("naya-nitro-narzan:note:the-net", "supercharged"),
    ("naya-nitro-narzan:project:dashboard-pass3", "IN PROGRESS"),
    ("naya-nitro-narzan:project:dashboard-pass3", "NINE AMENDMENTS"),
    ("naya-nitro-narzan:project:smart-box-pieces-3-5", "9/10"),
    ("naya-nitro-narzan:project:smart-box-pieces-3-5", "91/91"),
    ("naya-nitro-narzan:project:smart-box-wiring", "IN PROGRESS"),
    ("naya-nitro-narzan:project:owed-paypal-decisions", "Catalog Product"),
    ("naya-nitro-narzan:project:owed-merges", "9456daf5"),
    ("naya-nitro-narzan:project:owed-reports-ingest", "42501"),
    ("naya-nitro-narzan:project:owed-fulfillment-18-apps", "18 missing"),
    ("naya-nitro-narzan:project:board-state", "Nothing sits"),
]

# Secret patterns: real credential/secret/key MATERIAL. Key ids and
# the words "key"/"secret" in prose are not hits - a hit needs an
# assignment to a value, a private-key header, or a provider token.
SECRET_PATTERNS = [
    re.compile(r"(?i)(api[_-]?key|password|passwd|client[_-]?secret|"
               r"access[_-]?token|auth[_-]?token|bearer)\s*[:=]\s*['\"]?\S{8,}"),
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |PGP )?PRIVATE KEY-----"),
    re.compile(r"\bghp_[A-Za-z0-9]{20,}"),
    re.compile(r"\bgithub_pat_[A-Za-z0-9_]{10,}"),
    re.compile(r"\bsk-(?:live|test)-[A-Za-z0-9]{10,}"),
    re.compile(r"\bsk_live_[A-Za-z0-9]{10,}"),
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    re.compile(r"(?i)secret\s*=\s*['\"][^'\"]{8,}['\"]"),
]

_failures = []


def check(name, ok, detail=""):
    print("%s %s%s" % ("PASS" if ok else "FAIL", name,
                       (" - " + detail) if detail else ""))
    if not ok:
        _failures.append(name)


def build_in_scratch():
    """Build my box into a temp BOXES_ROOT. Returns (tmpdir, blocks)."""
    tmp = tempfile.mkdtemp(prefix="my-box-test-")
    boxstore.BOXES_ROOT = os.path.join(tmp, "boxes")
    blocks = build_my_box.build_box()
    return tmp, blocks


def test_shape(blocks):
    ids = set()
    for block in blocks:
        bid = block.get("id", "")
        ok = all(f in block for f in REQUIRED_FIELDS)
        check("shape %s has all fields" % bid, ok,
              "missing: %s" % [f for f in REQUIRED_FIELDS
                               if f not in block] if not ok else "")
        check("shape %s id is owner:kind:slug" % bid,
              bid.startswith(OWNER + ":") and bid.count(":") == 2
              and bid.split(":")[1] in KINDS,
              bid if not bid.startswith(OWNER + ":") else "")
        check("shape %s kind valid" % bid, block.get("kind") in KINDS)
        check("shape %s private" % bid,
              block.get("visibility") == "private"
              and block.get("owner_shared_choice") is False
              and block.get("body_open_to") == [],
              "visibility=%r" % block.get("visibility"))
        check("shape %s owner is me" % bid,
              (block.get("who") or {}).get("owner") == OWNER)
        check("shape %s id unique" % bid, bid not in ids)
        ids.add(bid)
    check("shape counts: 10 identity + 6 memory + 8 working-state = 24",
          len(blocks) == 24, "got %d" % len(blocks))


def test_gate(blocks):
    owner = make_actor(OWNER, "owner")
    stranger = make_actor("stranger", "stranger")
    registry = KeyRegistry()
    # The keyed Naya is a DIFFERENT agent from the owner: an actor whose
    # id equals the owner id is the owner (rule 1), so the keyed actor
    # must carry its own id - here a sister Naya holding my organize key.
    naya_id = "naya-verity-narzan"
    key = registry.mint(OWNER, naya_id, issued_by=OWNER)
    me_as_naya = make_actor(naya_id, "naya", keys=[key])
    for block in blocks:
        check("gate owner reads %s" % block["id"],
              may_share(block, owner, "read",
                        key_registry=registry) == "ALLOW")
        check("gate stranger denied %s" % block["id"],
              may_share(block, stranger, "read",
                        key_registry=registry) == "DENY")
        check("gate stranger cannot organize %s" % block["id"],
              may_share(block, stranger, "organize",
                        key_registry=registry) == "DENY")
    # Forged key: a Key built by hand, never minted, with a registry.
    forged = make_actor("forger", "naya",
                        keys=[Key("key-forged-0001", OWNER, "forger")])
    check("gate forged key denied",
          all(may_share(b, forged, "organize",
                        key_registry=registry) == "DENY" for b in blocks))
    # Revoked key denies.
    registry.revoke(key.key_id, revoked_by=OWNER)
    check("gate revoked key denied",
          all(may_share(b, me_as_naya, "organize",
                        key_registry=registry) == "DENY" for b in blocks))
    # Key for another owner denies.
    other_registry = KeyRegistry()
    other_key = other_registry.mint("someone-else", naya_id,
                                    issued_by="someone-else")
    other_actor = make_actor(naya_id, "naya", keys=[other_key])
    check("gate key for another owner denied",
          all(may_share(b, other_actor, "organize",
                        key_registry=other_registry) == "DENY"
              for b in blocks))
    # No registry: fails closed for keyed paths, owner still ALLOWs.
    check("gate no-registry keyed path fails closed",
          all(may_share(b, me_as_naya, "organize") == "DENY"
              for b in blocks))
    check("gate no-registry owner still ALLOWs",
          all(may_share(b, owner, "read") == "ALLOW" for b in blocks))


def test_coverage(blocks):
    by_id = {b["id"]: b for b in blocks}
    for block_id, fact in COVERAGE:
        block = by_id.get(block_id)
        check("coverage %s carries %r" % (block_id, fact),
              block is not None and fact in (block.get("body") or ""),
              "" if block is not None and fact in (block.get("body") or "")
              else ("block missing" if block is None else "fact not in body"))
    kinds = {}
    for block in blocks:
        kinds[block["kind"]] = kinds.get(block["kind"], 0) + 1
    check("coverage working state is projects",
          kinds.get("project", 0) == 8, "projects=%d" % kinds.get("project", 0))


def test_no_secrets(tmp):
    hits = []
    scanned = 0
    for root, _dirs, files in os.walk(tmp):
        for name in files:
            path = os.path.join(root, name)
            with open(path, encoding="utf-8", errors="replace") as handle:
                text = handle.read()
            scanned += 1
            for pattern in SECRET_PATTERNS:
                for match in pattern.finditer(text):
                    hits.append("%s: %s" % (path, match.group(0)[:40]))
    print("secrets scan: %d file(s) scanned, %d hit(s)"
          % (scanned, len(hits)))
    for hit in hits:
        print("  HIT %s" % hit)
    check("no secrets in any box file", not hits,
          "; ".join(hits) if hits else "0 hits")


def main():
    tmp, blocks = build_in_scratch()
    print("my box built in scratch: %d blocks at %s"
          % (len(blocks), boxstore.box_dir(OWNER)))
    test_shape(blocks)
    test_gate(blocks)
    test_coverage(blocks)
    test_no_secrets(tmp)
    manifest_path = os.path.join(boxstore.box_dir(OWNER), "manifest.json")
    with open(manifest_path, encoding="utf-8") as handle:
        manifest = json.load(handle)
    check("manifest counts match",
          manifest.get("blocks") == len(blocks),
          "manifest=%r blocks=%d" % (manifest.get("blocks"), len(blocks)))
    print("---")
    if _failures:
        print("FAIL: %d check(s) failed: %s"
              % (len(_failures), ", ".join(_failures)))
        return 1
    print("ALL CHECKS PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())

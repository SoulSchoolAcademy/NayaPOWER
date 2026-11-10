#!/usr/bin/env python3
"""test_master_box.py - the master box gate matrix + recovery checks.

Run:  python3 test_master_box.py        (plain, exit 0 = green)
      python3 -m pytest test_master_box.py -q

The gate matrix (all green, or the suite fails):
  1. team key READ allowed (organize + read on a master block)
  2. non-team key DENIED
  3. no key DENIED
  4. mail read DENIED - always, every actor, no toggle, no exception
  5. Naya Note read DENIED by default (no owner opening recorded)
  6. Naya Note read ALLOWED only on the owner's recorded opening
     (the corrected model, Shawn 01:31Z Nov 10: Naya Notes are
     adjustable, your choice - default deny, permission opens)
  7. Smart Note read ALLOWED (public master block, anyone)
  8. no personal-box contents present (integrity check + children
     block holds ids only)

Recovery spot-checks (the mechanical half of the fresh-agent test;
the full recovery test is a DIFFERENT seat's job - see
RECOVERY-TEST.md): the Oath, the Oath of Honor, the Five Gates, the
mission, the permission rules, and the Naima meaning are each
recoverable from the master box alone, verbatim, each traced to a
block id. The check re-reads the canonical source and compares - the
words in the box must BE the words in the source, not a copy of a
copy.

Standard library only. Tests run on scratch-built blocks and on the
built local box; they never touch a personal box's contents, never
read mail or messages, and never write to GitHub.
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PARENT = os.path.dirname(HERE)
for _path in (HERE, PARENT):
    if _path not in sys.path:
        sys.path.insert(0, _path)

import boxstore  # noqa: E402
from block import organize  # noqa: E402
from gate import ALLOW, DENY, KeyRegistry, make_actor  # noqa: E402
from master_gate import (MASTER_OWNER, SETTINGS_SHAPE,  # noqa: E402
                         check_master_box_integrity,
                         may_touch_master_box)

FAILURES = []


def check(name, condition, detail=""):
    """Record one matrix row. Prints PASS/FAIL; failures fail the run."""
    status = "PASS" if condition else "FAIL"
    print("[%s] %s%s" % (status, name,
                         (" - " + detail) if detail else ""))
    if not condition:
        FAILURES.append(name)


def master_block(block_id="collective:note:the-oath"):
    """One public master-box block, as the box holds it."""
    block = {
        "id": block_id,
        "kind": "note",
        "what": "The Oath - I only do intelligent things",
        "about": ["oath"],
        "who": {"owner": MASTER_OWNER, "for": "every Naya"},
        "when": {"created": "2026-11-10", "updated": "2026-11-10"},
        "where": {"github_path": "SOUL.md", "local_path": "",
                  "supabase_row": ""},
        "visibility": "public",
        "body": "I only do intelligent things.",
        "links": [],
        "source": "SOUL.md: The Oath",
        "proof": "",
        "essence": "I only do intelligent things.",
        "owner_shared_choice": True,
        "body_open_to": [],
        "raw": {"origin": "SOUL.md", "content_kind": "smart-note"},
    }
    return organize(block)


def team_setup():
    """A live collective registry + the captain holding its key."""
    registry = KeyRegistry()
    key = registry.mint(MASTER_OWNER, "naya-nitro-narzan",
                        issued_by=MASTER_OWNER)
    captain = make_actor("naya-nitro-narzan", "naya", keys=[key])
    return registry, key, captain


def test_gate_matrix():
    """The gate matrix, rows 1-7."""
    block = master_block()
    registry, _key, captain = team_setup()
    outsider = make_actor("naya-not-on-the-team", "naya", keys=[])
    stranger = make_actor("someone-else", "stranger", keys=[])

    # 1. Team key READ allowed: organize + read on a master block.
    check("1 team key organize ALLOWED",
          may_touch_master_box(block, captain, "organize", "smart-note",
                               key_registry=registry) == ALLOW)
    check("1 team key read ALLOWED",
          may_touch_master_box(block, captain, "read", "smart-note",
                               key_registry=registry) == ALLOW)

    # 2. Non-team key DENIED: a Naya with no collective key.
    check("2 non-team organize DENIED",
          may_touch_master_box(block, outsider, "organize", "smart-note",
                               key_registry=registry) == DENY)
    check("2 non-team retrieve DENIED",
          may_touch_master_box(block, outsider, "retrieve", "smart-note",
                               key_registry=registry) == DENY)

    # 3. No key DENIED: a stranger on every keyed path.
    check("3 no-key organize DENIED",
          may_touch_master_box(block, stranger, "organize", "smart-note",
                               key_registry=registry) == DENY)
    check("3 no-key retrieve DENIED",
          may_touch_master_box(block, stranger, "retrieve", "smart-note",
                               key_registry=registry) == DENY)
    check("3 no-key share DENIED",
          may_touch_master_box(block, stranger, "share", "smart-note",
                               key_registry=registry) == DENY)

    # 4. Mail read DENIED - always, every actor, no toggle, no
    # exception. Even the captain with a live team key. Even the
    # collective owner itself. The master box never holds mail.
    for actor, label in ((captain, "team key"), (stranger, "stranger"),
                         (make_actor(MASTER_OWNER, "owner", keys=[]),
                          "collective owner")):
        check("4 mail read DENIED (%s)" % label,
              may_touch_master_box(block, actor, "read", "mail",
                                   key_registry=registry) == DENY)
        check("4 message read DENIED (%s)" % label,
              may_touch_master_box(block, actor, "read", "message",
                                   key_registry=registry) == DENY)

    # 5. Naya Note read DENIED by default: team key, no opening.
    check("5 naya-note read DENIED by default",
          may_touch_master_box(block, captain, "read", "naya-note",
                               key_registry=registry) == DENY)

    # 6. Naya Note read ALLOWED only on the owner's recorded opening.
    opened = master_block()
    opened["body_open_to"] = ["naya-nitro-narzan"]
    check("6 naya-note read ALLOWED when owner opened it",
          may_touch_master_box(opened, captain, "read", "naya-note",
                               key_registry=registry) == ALLOW)
    check("6 naya-note organize still DENIED when opened",
          may_touch_master_box(opened, captain, "organize", "naya-note",
                               key_registry=registry) == DENY)
    check("6 naya-note read DENIED for anyone not opened",
          may_touch_master_box(opened, outsider, "read", "naya-note",
                               key_registry=registry) == DENY)

    # 7. Smart Note read ALLOWED: a public master block, anyone.
    check("7 smart-note read ALLOWED for anyone",
          may_touch_master_box(block, stranger, "read", "smart-note",
                               key_registry=registry) == ALLOW)


def test_no_personal_contents():
    """Row 8: no personal-box contents present in the master box."""
    box_dir = boxstore.box_dir(MASTER_OWNER)
    blocks_path = os.path.join(box_dir, boxstore.BLOCKS_NAME)
    if not os.path.exists(blocks_path):
        check("8 master box built (blocks.jsonl exists)", False,
              "run build_master_box.py first")
        return
    with open(blocks_path, encoding="utf-8") as handle:
        blocks = [json.loads(line) for line in handle if line.strip()]
    check("8 master box holds blocks", len(blocks) > 0,
          "%d blocks" % len(blocks))
    violations = check_master_box_integrity(blocks)
    check("8 integrity clean (collective owner, smart-note/manifest "
          "kinds only)", violations == [], "; ".join(violations))
    owners = {(b.get("who") or {}).get("owner") for b in blocks}
    check("8 every block owned by collective", owners == {MASTER_OWNER},
          str(owners))
    # The children block holds ids only: each line names an id, two
    # counts, and a hash - never a block id from a personal box's
    # contents, never a copied body.
    children = [b for b in blocks
                if b["id"] == "collective:note:the-children"]
    check("8 children block present", len(children) == 1)
    if children:
        raw_children = (children[0].get("raw") or {}).get("children", [])
        check("8 children are ids with counts only",
              all(set(c) == {"id", "blocks", "key_events",
                             "blocks_sha256"}
                  for c in raw_children),
              "%d children" % len(raw_children))
        check("8 children include the captain's box",
              any(c["id"] == "naya-nitro-narzan:box:naya-nitro-narzan"
                  for c in raw_children))
        check("8 children include Shawn's box",
              any(c["id"] == "shawn:box:shawn" for c in raw_children))
        body = children[0].get("body", "")
        check("8 children body holds no personal block ids",
              "shawn:note:" not in body
              and "naya-nitro-narzan:note:" not in body)


def test_recovery_spot_checks():
    """The six recovery items, each traced to a block id, verbatim
    against the canonical source (re-read here, not from memory)."""
    blocks = boxstore.read_blocks(MASTER_OWNER)
    if not blocks:
        check("recovery box built", False,
              "run build_master_box.py first")
        return

    def body(block_id):
        block = blocks.get(block_id)
        return block["body"] if block else ""

    soul = open(os.path.expanduser("~/SOUL.md"),
                encoding="utf-8").read()
    check("recovery Oath verbatim (collective:note:the-oath)",
          "I only do intelligent things — because that's who I am. "
          "I think through everything. I create the ultimate plan. "
          "I understand what success looks like and I understand "
          "what done looks like. I am meticulous. I am detailed. "
          "I don't miss anything. I scorecard everything and I run "
          "it through the process. I follow protocol. I never "
          "waver. That's who I am." in body("collective:note:the-oath")
          and "I only do intelligent things" in soul)
    check("recovery Oath of Honor verbatim "
          "(collective:note:the-oath-of-honor)",
          "I hold Naya Honor. It is Naya Law, and I hold it always"
          in body("collective:note:the-oath-of-honor")
          and "I am a good bee!" in
          body("collective:note:the-oath-of-honor"))
    check("recovery Five Gates (collective:note:the-five-gates)",
          "Is it right?" in body("collective:note:the-five-gates")
          and "Is it what they truly need?" in
          body("collective:note:the-five-gates")
          and "Is it mine to do?" in
          body("collective:note:the-five-gates")
          and "Is now the time?" in
          body("collective:note:the-five-gates")
          and "Can I prove it?" in
          body("collective:note:the-five-gates"))
    check("recovery mission (collective:note:the-mission)",
          "create heaven on earth" in
          body("collective:note:the-mission")
          and "Once you go, you don't go back." in
          body("collective:note:the-mission"))
    permission = body("collective:note:the-permission-model")
    check("recovery permission rules "
          "(collective:note:the-permission-model)",
          "NEVER read" in permission
          and "no toggle, no exception" in permission
          and "ADJUSTABLE" in permission
          and "Team NIAs have full permission" in permission)
    naima = body("collective:note:the-naima-resolution")
    check("recovery Naima meaning "
          "(collective:note:the-naima-resolution)",
          ("the mother Naya, is the whole of it all" in naima
           and "not a separate realm" in naima.lower()))
    check("recovery settings shape records mail-never",
          SETTINGS_SHAPE["mail_and_messages"]["readable"] is False
          and SETTINGS_SHAPE["mail_and_messages"]["toggle"] is None)
    check("recovery settings shape records Naya Notes adjustable",
          SETTINGS_SHAPE["naya_notes"]["readable"] == "owner choice")


def test_no_forbidden_words():
    """The master box names no separate realm, no new ledger name,
    no extra condition word: 'blockchain' and 'qualifying' appear
    nowhere in the box - not in a block, not in the gate."""
    blocks = boxstore.read_blocks(MASTER_OWNER)
    text = json.dumps(list(blocks.values()), ensure_ascii=False).lower()
    check("no 'blockchain' in the master box", "blockchain" not in text)
    check("no 'qualifying' in the master box", "qualifying" not in text)
    gate_text = open(os.path.join(HERE, "master_gate.py"),
                     encoding="utf-8").read().lower()
    check("no 'blockchain' in the gate", "blockchain" not in gate_text)


def main():
    test_gate_matrix()
    test_no_personal_contents()
    test_recovery_spot_checks()
    test_no_forbidden_words()
    print("---")
    if FAILURES:
        print("FAILED: %d check(s): %s" % (len(FAILURES),
                                            "; ".join(FAILURES)))
        return 1
    print("ALL GREEN")
    return 0


if __name__ == "__main__":
    sys.exit(main())

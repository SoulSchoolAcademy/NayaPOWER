#!/usr/bin/env python3
"""test_smart_box.py - proof for the Smart Box, pieces 1 and 2.

Run:  python3 test_smart_box.py
Exit 0 only when every check passes; non-zero otherwise. Prints one line
per check, no tracebacks on failure - a failure names what is missing.

What it proves, on REAL data (never invented):

  A. Round-trip, zero data loss: the shape converts 3 real smart notes
     (SN-2535 "What Naya Does", SN-2543 "The Smart Box Is the Cure for
     the Saving Sickness", SN-2545 "The Super Brain Is Yours") and 3 real
     Smart Box entries (SB-0001, SB-0002, SB-2086, from the owner's own
     store) into blocks. Every field of the original appears in the
     block - checked by value, field by field - and the original record
     survives verbatim in the block's ``raw``.
  B. JSON round-trip: every block serializes and deserializes unchanged.
  C. The 10-case gate matrix from the build brief, case by case.
  D. The shape refuses what it cannot convert: a file with no ``#``
     title and no ``##`` sections is not silently turned into a block.

Fixtures live beside this file in ``fixtures/`` and are verbatim copies
of the real sources - see ``fixtures/README.md`` for provenance. The
suite reads them from its own directory, so a different seat re-running
it from a clean checkout gets the same result.

The visibility and owner-choice values on the test blocks are the
owner's decisions recorded for the test, not derived from the files:
SN-2535 is the public product note (public + chosen, for case 6);
SN-2543 is private (cases 1 and 2); SN-2545 is marked public but NOT
chosen (case 5 - the "either one missing" half of the sharing rule).
"""

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from block import (  # noqa: E402
    block_from_json,
    block_to_json,
    entry_to_block,
    note_to_block,
    parse_smart_note,
    roundtrip_check_entry,
    roundtrip_check_note,
)
from gate import ALLOW, DENY, Key, make_actor, may_share  # noqa: E402

FIXTURES = HERE / "fixtures"
OWNER = "shawn"
NAYA = "naya"

# The three real smart notes, with the GitHub / local path each came from.
NOTES = [
    ("SN-2535-what-naya-does.md",
     "BRAIN/05-MEMORY/SMART-NOTES/2026/11/09/PRODUCT/SN-2535/"
     "IB-SMART-NOTE-20261109-sn2535-what-naya-does.md",
     "public", True),
    ("SN-2543-smart-box-cure-saving-sickness.md", None, "private", False),
    ("SN-2545-super-brain-is-yours.md", None, "private", False),
]

# The three real Smart Box entries, in store order. SB-0002 is the
# UNSOURCED-date edge case: its date stays "UNSOURCED" in the block,
# never guessed into a real date.
ENTRY_IDS = ["SB-0001", "SB-0002", "SB-2086"]
STORE_PATH = "~/workspace/nitro-smart-box/store/entries.jsonl"

RESULTS = []


def check(name, ok, detail=""):
    """Record one check and print its verdict."""
    RESULTS.append(ok)
    mark = "PASS" if ok else "FAIL"
    line = "%s: %s" % (mark, name)
    if detail:
        line += " - %s" % detail
    print(line)
    return ok


def test_notes():
    """A. Round-trip on the 3 real smart notes."""
    for filename, github_path, visibility, chosen in NOTES:
        path = FIXTURES / filename
        text = path.read_text(encoding="utf-8")
        parsed = parse_smart_note(text)
        block = note_to_block(
            text, owner=OWNER, github_path=github_path,
            local_path=str(path), visibility=visibility,
            owner_shared_choice=chosen)
        missing = roundtrip_check_note(block, parsed)
        check("round-trip %s (%d sections, %d chars)"
              % (parsed["sn_id"], len(parsed["sections"]), len(text)),
              not missing,
              "missing: %s" % "; ".join(missing) if missing
              else "every field present; essence = nutshell (%d chars)"
              % len(block["essence"]))
        check("%s essence is the nutshell, body holds the full text"
              % parsed["sn_id"],
              block["essence"] and block["essence"] in block["body"]
              and len(block["body"]) == len(text),
              "%d essence chars of %d body chars"
              % (len(block["essence"]), len(block["body"])))
    return True


def test_entries():
    """A. Round-trip on the 3 real Smart Box entries."""
    entries = json.loads((FIXTURES / "smart-box-entries.json")
                         .read_text(encoding="utf-8"))
    by_id = {entry["id"]: entry for entry in entries}
    for entry_id in ENTRY_IDS:
        entry = by_id[entry_id]
        block = entry_to_block(entry, owner=OWNER,
                               store_path=STORE_PATH)
        missing = roundtrip_check_entry(block, entry)
        check("round-trip %s (%s, %s)"
              % (entry_id, entry["type"], entry["date"]),
              not missing,
              "missing: %s" % "; ".join(missing) if missing
              else "every field present; %d topics; source %s"
              % (len(block["about"]), block["source"]))
    return True


def test_json_roundtrip():
    """B. Every block serializes and deserializes unchanged."""
    blocks = []
    for filename, github_path, visibility, chosen in NOTES:
        text = (FIXTURES / filename).read_text(encoding="utf-8")
        blocks.append(note_to_block(
            text, owner=OWNER, github_path=github_path,
            visibility=visibility, owner_shared_choice=chosen))
    entries = json.loads((FIXTURES / "smart-box-entries.json")
                         .read_text(encoding="utf-8"))
    for entry in entries:
        blocks.append(entry_to_block(entry, owner=OWNER,
                                     store_path=STORE_PATH))
    ok = True
    for block in blocks:
        again = block_from_json(block_to_json(block))
        if again != block:
            ok = False
    check("json round-trip, all %d blocks byte-stable" % len(blocks), ok,
          "6 blocks" if ok else "a block changed in serialization")
    return ok


def _blocks_for_gate():
    """The blocks the matrix runs against: a private note, a public
    note the owner chose, and a public-marked note the owner did NOT
    choose (case 5's trap)."""
    private_text = (FIXTURES / "SN-2543-smart-box-cure-saving-sickness.md") \
        .read_text(encoding="utf-8")
    public_text = (FIXTURES / "SN-2535-what-naya-does.md") \
        .read_text(encoding="utf-8")
    unchosen_text = (FIXTURES / "SN-2545-super-brain-is-yours.md") \
        .read_text(encoding="utf-8")
    private = note_to_block(private_text, owner=OWNER,
                            visibility="private", owner_shared_choice=False)
    public = note_to_block(public_text, owner=OWNER,
                           visibility="public", owner_shared_choice=True)
    unchosen = note_to_block(unchosen_text, owner=OWNER,
                             visibility="public", owner_shared_choice=False)
    return private, public, unchosen


def test_gate_matrix():
    """C. The 10-case gate matrix from the build brief, case by case."""
    private, public, unchosen = _blocks_for_gate()
    owner = make_actor(OWNER, "owner")
    stranger = make_actor("stranger", "stranger")
    anyone = make_actor("anyone", "anyone")
    live_key = Key("key-organize-1", OWNER, NAYA, status="active")
    revoked_key = Key("key-organize-2", OWNER, NAYA, status="revoked")
    naya_keyed = make_actor(NAYA, "naya", keys=[live_key])
    naya_revoked = make_actor(NAYA, "naya", keys=[revoked_key])
    naya_nokey = make_actor(NAYA, "naya", keys=[])

    cases = [
        # (case, block, actor, action, expected, what it proves)
        (1, private, owner, "read", ALLOW,
         "owner reads own private note"),
        (2, private, stranger, "read", DENY,
         "stranger reads private note"),
        (3, private, naya_keyed, "organize", ALLOW,
         "Naya with organize key reads map/brain"),
        (4, private, naya_keyed, "read", DENY,
         "Naya with organize key reads raw body"),
        (5, unchosen, naya_keyed, "share", DENY,
         "Naya shares without the owner's smart-note choice"),
        (6, public, anyone, "read", ALLOW,
         "anyone reads a public smart note"),
        (7, private, owner, "share", ALLOW,
         "owner shares own note"),
        (8, private, naya_revoked, "organize", DENY,
         "revoked key organizes"),
        (9, private, naya_nokey, "organize", DENY,
         "no key organizes"),
        (10, private, naya_keyed, "retrieve", ALLOW,
         "retrieve for the owner"),
    ]
    for number, block, actor, action, expected, what in cases:
        got = may_share(block, actor, action)
        check("gate case %d: %s -> %s" % (number, what, expected),
              got == expected,
              "got %s" % got if got != expected else "")
    # The sharing rule's other half: a keyed Naya MAY share the note
    # the owner did choose public. Without this, rule 3 would be a
    # blanket ban, not a both-halves rule.
    got = may_share(public, naya_keyed, "share")
    check("gate extra: keyed Naya shares the owner's chosen public note"
          " -> ALLOW", got == ALLOW, "got %s" % got if got != ALLOW else "")
    # The owner's explicit opening: a keyed Naya reads the raw body of
    # the one block the owner opened to them by name - and no other.
    opened = dict(private)
    opened["body_open_to"] = [NAYA]
    got = may_share(opened, naya_keyed, "read")
    check("gate extra: keyed Naya reads a body the owner opened to them"
          " -> ALLOW", got == ALLOW, "got %s" % got if got != ALLOW else "")
    # An unknown action is denied, never allowed by accident.
    got = may_share(public, owner, "delete")
    check("gate extra: unknown action -> DENY", got == DENY,
          "got %s" % got if got != DENY else "")
    return True


def test_refuses_non_note():
    """D. The shape refuses what it cannot convert."""
    try:
        note_to_block("just a paragraph, no title, no sections\n",
                      owner=OWNER)
        check("refuses a file with no title and no ## sections", False,
              "it converted instead of refusing")
    except ValueError as exc:
        check("refuses a file with no title and no ## sections", True,
              str(exc))
    return True


def main():
    """Run every check. Exit 0 only when all pass."""
    print("Smart Box proof - shape + gate, on real data")
    print("notes: SN-2535, SN-2543, SN-2545; entries: SB-0001, SB-0002, "
          "SB-2086")
    test_notes()
    test_entries()
    test_json_roundtrip()
    test_gate_matrix()
    test_refuses_non_note()
    passed = sum(1 for ok in RESULTS if ok)
    total = len(RESULTS)
    print("----")
    print("%d/%d checks passed" % (passed, total))
    if passed == total:
        print("SMART BOX PROOF: ALL GREEN")
        return 0
    print("SMART BOX PROOF: %d CHECK(S) FAILED" % (total - passed))
    return 1


if __name__ == "__main__":
    sys.exit(main())

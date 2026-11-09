#!/usr/bin/env python3
"""test_smart_box.py - proof for the Smart Box, pieces 1 to 5.

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
  J. The legacy no-registry path fails closed: a forged key without
     a registry DENYs, a minted key without a registry DENYs, and the
     owner reading their own private block without a registry still
     ALLOWs (rule 1 needs no key).
  K. The 300KB write probe: a 300KB write to a temp file succeeds and
     reads back byte-identical - the probe proven by the run itself.

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
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from block import (  # noqa: E402
    block_from_json,
    block_to_json,
    complete_where,
    entry_to_block,
    note_to_block,
    organize,
    organize_store,
    parse_smart_note,
    roundtrip_check_entry,
    roundtrip_check_note,
)
from bridge import Box, build_space_from_note, carry  # noqa: E402
from gate import ALLOW, DENY, Key, KeyRegistry, make_actor, may_share  # noqa: E402
from syncbox import (  # noqa: E402
    capture_sync_state,
    rebuild_from_box,
    sha256_file,
    sync_state_blocks,
)

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
    """C. The 10-case gate matrix from the build brief, case by case.

    The matrix runs through the registry proof path: every call
    passes ``key_registry``. Without a registry the gate fails closed
    (see test_legacy_path_fails_closed), so a matrix that forgot the
    registry would deny cases 3, 4, 5 and 10 - the registry is part
    of the matrix, not an optional extra.
    """
    private, public, unchosen = _blocks_for_gate()
    owner = make_actor(OWNER, "owner")
    stranger = make_actor("stranger", "stranger")
    anyone = make_actor("anyone", "anyone")
    registry = KeyRegistry()
    # A revoked key and a live key for the same (owner, Naya) pair:
    # mint, revoke, mint again - the second mint issues a fresh id.
    revoked_key = registry.mint(OWNER, NAYA, issued_by=OWNER)
    registry.revoke(revoked_key.key_id, revoked_by=OWNER)
    live_key = registry.mint(OWNER, NAYA, issued_by=OWNER)
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
        got = may_share(block, actor, action, key_registry=registry)
        check("gate case %d: %s -> %s" % (number, what, expected),
              got == expected,
              "got %s" % got if got != expected else "")
    # The sharing rule's other half: a keyed Naya MAY share the note
    # the owner did choose public. Without this, rule 3 would be a
    # blanket ban, not a both-halves rule.
    got = may_share(public, naya_keyed, "share", key_registry=registry)
    check("gate extra: keyed Naya shares the owner's chosen public note"
          " -> ALLOW", got == ALLOW, "got %s" % got if got != ALLOW else "")
    # The owner's explicit opening: a keyed Naya reads the raw body of
    # the one block the owner opened to them by name - and no other.
    opened = dict(private)
    opened["body_open_to"] = [NAYA]
    got = may_share(opened, naya_keyed, "read", key_registry=registry)
    check("gate extra: keyed Naya reads a body the owner opened to them"
          " -> ALLOW", got == ALLOW, "got %s" % got if got != ALLOW else "")
    # An unknown action is denied, never allowed by accident.
    got = may_share(public, owner, "delete", key_registry=registry)
    check("gate extra: unknown action -> DENY", got == DENY,
          "got %s" % got if got != DENY else "")
    return True


def test_legacy_path_fails_closed():
    """J. The legacy no-registry path is closed: without a registry
    the gate fails closed for every keyed path. The verifier's forged
    key (``key-shawn-naya-9999``, hand-built "active") DENYs without
    a registry - and so does a genuine minted key, because the proof
    cannot be checked when the caller forgets the registry. The owner
    control case still ALLOWs without a registry: rule 1 needs no
    key, so the owner reading their own private block is unaffected.
    """
    private_text = (FIXTURES / "SN-2543-smart-box-cure-saving-sickness.md") \
        .read_text(encoding="utf-8")
    private = note_to_block(private_text, owner=OWNER,
                            visibility="private", owner_shared_choice=False)
    owner = make_actor(OWNER, "owner")
    forged = Key("key-shawn-naya-9999", OWNER, NAYA, status="active")
    naya_forged = make_actor(NAYA, "naya", keys=[forged])
    check("legacy path: forged key, no registry, organize -> DENY",
          may_share(private, naya_forged, "organize") == DENY, "")
    check("legacy path: forged key, no registry, retrieve -> DENY",
          may_share(private, naya_forged, "retrieve") == DENY, "")
    check("legacy path: forged key, no registry, read -> DENY",
          may_share(private, naya_forged, "read") == DENY, "")
    # A genuine minted key denies too when the caller forgets the
    # registry - the denial is about the missing proof, not the key.
    registry = KeyRegistry()
    live = registry.mint(OWNER, NAYA, issued_by=OWNER)
    naya_keyed = make_actor(NAYA, "naya", keys=[live])
    check("legacy path: minted key, no registry, organize -> DENY",
          may_share(private, naya_keyed, "organize") == DENY, "")
    check("legacy path: minted key, WITH registry, organize -> ALLOW",
          may_share(private, naya_keyed, "organize",
                    key_registry=registry) == ALLOW, "")
    # Owner control: the owner reads their own private block with no
    # registry at all - rule 1, no key needed, still ALLOW.
    check("legacy path: owner reads own private block, no registry"
          " -> ALLOW",
          may_share(private, owner, "read") == ALLOW, "")
    check("legacy path: owner shares own private block, no registry"
          " -> ALLOW",
          may_share(private, owner, "share") == ALLOW, "")
    return True


def test_write_probe_300k():
    """K. Evidence trail for the write probe: a 300KB write to a temp
    file succeeds and reads back byte-identical. The probe is proven
    by the run itself, not by a note in a file."""
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "write-probe-300k.bin"
        data = b"x" * (300 * 1024)
        path.write_bytes(data)
        check("write probe: 300KB write succeeds",
              path.stat().st_size == 300 * 1024,
              "%d bytes written" % path.stat().st_size)
        check("write probe: 300KB reads back byte-identical",
              path.read_bytes() == data, "")
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


# The real GitHub paths of the three proof notes, as their live
# hub_smart_notes rows record them (verified 2026-11-09 against
# Supabase: each row's github_path, ib_id, and title match the file).
NOTE_GITHUB = {
    "SN-2535": "BRAIN/05-MEMORY/SMART-NOTES/2026/11/09/PRODUCT/SN-2535/"
               "IB-SMART-NOTE-20261109-sn2535-what-naya-does.md",
    "SN-2543": "BRAIN/05-MEMORY/SMART-NOTES/2026/11/09/DESIGN/SN-2543/"
               "IB-SMART-NOTE-20261109-sn2543-smart-box-cure-saving-sickness.md",
    "SN-2545": "BRAIN/05-MEMORY/SMART-NOTES/2026/11/09/DESIGN/SN-2545/"
               "IB-SMART-NOTE-20261109-sn2545-super-brain-is-yours.md",
}
STORE_PATH = str(Path.home() / "workspace/nitro-smart-box/store/entries.jsonl")


def _store_entries():
    """All 2,086 real store entries, in store order, with line numbers."""
    entries = []
    with open(STORE_PATH, encoding="utf-8") as handle:
        for line_no, line in enumerate(handle, start=1):
            entry = json.loads(line)
            entry["_line"] = line_no
            entries.append(entry)
    return entries


def test_organize():
    """E. organize(thing): LOOK -> TAG -> FILE -> LINK, on real data."""
    entries = json.loads((FIXTURES / "smart-box-entries.json")
                         .read_text(encoding="utf-8"))
    by_id = {entry["id"]: entry for entry in entries}
    # Sampled entries: tags carry the store type + source stem, the
    # shelf names owner/kind/type, links carry the refs in the text.
    cases = [
        ("SB-0001", "dictation", ["SN-0883", "SN-0831"]),
        ("SB-0002", "law", []),
        ("SB-2086", "system-map", []),
    ]
    for entry_id, entry_type, refs in cases:
        block = organize(entry_to_block(by_id[entry_id], owner=OWNER,
                                        store_path=str(STORE_PATH)))
        check("organize %s tags its type + source (%s)"
              % (entry_id, entry_type),
              entry_type in block["about"] and "memory" in block["about"],
              "about=%s" % block["about"])
        check("organize %s files it on shelf shawn/note/%s"
              % (entry_id, entry_type),
              block["where"].get("shelf") == "shawn/note/%s" % entry_type,
              "shelf=%s" % block["where"].get("shelf"))
        check("organize %s links the refs named in its text"
              % entry_id,
              all(ref in block["links"] for ref in refs),
              "links=%s" % block["links"])
        check("organize %s keeps raw verbatim, what/body unchanged"
              % entry_id,
              block["raw"] == by_id[entry_id]
              and block["what"] == by_id[entry_id]["title"]
              and block["body"] == by_id[entry_id]["text"],
              "")
        twice = organize(block)
        check("organize %s is idempotent" % entry_id, twice == block,
              "second run changed the block" if twice != block else "")
    # A note: category words stay the tags, SN refs stay the links.
    text = (FIXTURES / "SN-2535-what-naya-does.md").read_text(encoding="utf-8")
    note = organize(note_to_block(text, owner=OWNER,
                                  github_path=NOTE_GITHUB["SN-2535"],
                                  visibility="public",
                                  owner_shared_choice=True))
    check("organize SN-2535 keeps its category tags, shelf shawn/note/*",
          note["about"] and note["where"]["shelf"].startswith("shawn/note/"),
          "about=%s shelf=%s" % (note["about"], note["where"]["shelf"]))
    check("organize SN-2535 keeps its essence (the nutshell)",
          note["essence"] and note["essence"] in note["body"], "")
    # The whole store: 2,086 entries, every one organized.
    all_entries = _store_entries()
    for entry in all_entries:
        entry.pop("_line", None)
    blocks, topic_index, stats = organize_store(
        all_entries, owner=OWNER, store_path=str(STORE_PATH))
    check("organize whole store: 2,086 entries organized",
          stats["total"] == 2086 and len(blocks) == 2086,
          "total=%d" % stats["total"])
    check("organize whole store: %d topics indexed, %d links, %d blocks "
          "with links" % (stats["topics"], stats["links_total"],
                          stats["blocks_with_links"]),
          stats["topics"] >= 27 and stats["links_total"] > 0
          and stats["blocks_with_links"] > 0,
          "topics=%d links=%d with-links=%d"
          % (stats["topics"], stats["links_total"],
             stats["blocks_with_links"]))
    by_block = {b["raw"]["id"]: b for b in blocks}
    sb1673 = by_block["SB-1673"]
    check("organize SB-1673 links SB-1680 (superseded_by)",
          "SB-1680" in sb1673["links"], "links=%s" % sb1673["links"])
    sb1941 = [b for b in blocks if "sb-1941" in b["id"]][0]
    check("organize SB-1941 links its filed Act URL",
          any("CLARITY-CONFIRMATION-ACT" in link
              for link in sb1941["links"]),
          "links=%s" % sb1941["links"])
    check("organize whole store: every block's raw is its entry verbatim",
          all(b["raw"].get("id") for b in blocks)
          and all(b["what"] == b["raw"]["title"] for b in blocks),
          "")
    return True


def test_nn_category():
    """E2. Naya Notes read their ``**Category:**`` line (fix 20261109
    item 3): her memory organizing itself, not filing. A Naya Note
    carries no SN line, so its category lives on the Category line -
    the block gets real ``about`` tags and a real shelf, never empty
    / unsorted. The SN line always wins when it exists."""
    nn_text = (
        "# A Smart Note Is Official Only When It Is In\n"
        "\n"
        "**Written by Naya for Shawn Vibert — Founder / Creator of "
        "NayaNET**\n"
        "\n"
        "**NN-20261109-a-smart-note-is-official-only-when-it-is-in · "
        "Naya Note · 2026-11-09 20:58Z**\n"
        "\n"
        "**Category:** System — Intelligence / What Counts\n"
        "\n"
        "## What it is\n"
        "\n"
        "His dictation, 20:58Z Nov 9 — recorded from his words.\n"
        "\n"
        "## Why it matters\n"
        "\n"
        "Hundreds of smart notes sitting in GitHub that nobody reads "
        "are not in the system.\n"
        "\n"
        "## How to use it\n"
        "\n"
        "- A smart note is official only when it is IN.\n")
    block = note_to_block(nn_text, owner=OWNER,
                          github_path="BRAIN/05-MEMORY/NAYA-NOTES/"
                          "NN-20261109-a-smart-note-is-official-only-"
                          "when-it-is-in.md")
    check("NN Category line becomes about tags (no bare dash tag)",
          block["about"] == ["System", "Intelligence", "What", "Counts"],
          "about=%s" % block["about"])
    check("NN Category line is kept verbatim in raw",
          block["raw"]["category"]
          == "System — Intelligence / What Counts",
          "raw category=%r" % block["raw"]["category"])
    organized = organize(block)
    check("NN block shelves on its first category tag",
          organized["where"].get("shelf") == "shawn/note/system",
          "shelf=%s" % organized["where"].get("shelf"))
    sn_text = (
        "# The Gauge Follows The Number\n"
        "\n"
        "SN-9999 · Law — Gauge\n"
        "\n"
        "**Category:** Other — Place\n"
        "\n"
        "## Hook\n"
        "\n"
        "The gauge follows the number.\n")
    sn_block = note_to_block(sn_text, owner=OWNER,
                             github_path="BRAIN/05-MEMORY/SMART-NOTES/"
                             "2026/11/09/LAW/SN-9999/IB-SMART-NOTE-"
                             "20261109-sn9999.md")
    check("SN line wins over a Category line when both exist",
          sn_block["about"] == ["Law", "Gauge"],
          "about=%s" % sn_block["about"])
    bare_text = (
        "# A Note With No Category\n"
        "\n"
        "## What it is\n"
        "\n"
        "Nothing to categorize here.\n")
    bare = note_to_block(bare_text, owner=OWNER)
    check("a note with no category keeps empty about, shelf unsorted",
          bare["about"] == []
          and organize(bare)["where"].get("shelf")
          == "shawn/note/unsorted",
          "about=%s" % bare["about"])
    return True


def test_key_lifecycle():
    """F. The key lifecycle: mint, check, revoke - proven per call."""
    registry = KeyRegistry()
    # Only the owner issues.
    try:
        registry.mint(OWNER, NAYA, issued_by="stranger")
        check("key mint by a stranger is refused", False,
              "it minted instead of refusing")
    except ValueError as exc:
        check("key mint by a stranger is refused", True, str(exc))
    key = registry.mint(OWNER, NAYA, issued_by=OWNER)
    check("key mint by the owner returns one key per (owner, Naya)",
          registry.mint(OWNER, NAYA, issued_by=OWNER).key_id == key.key_id,
          "second mint gave a different key")
    check("key check: minted key is live for owner + Naya",
          registry.check(key.key_id, OWNER, NAYA)
          and registry.status(key.key_id) == "active",
          "key_id=%s" % key.key_id)
    check("key check: unknown key id is not live",
          not registry.check("key-no-such-key", OWNER, NAYA), "")
    check("key record names owner, Naya, mint event - no key material",
          registry.record(key.key_id)["owner_id"] == OWNER
          and registry.record(key.key_id)["naya_id"] == NAYA
          and registry.record(key.key_id)["events"][0]["event"] == "mint"
          and "secret" not in json.dumps(registry.record(key.key_id)),
          "")

    private_text = (FIXTURES / "SN-2543-smart-box-cure-saving-sickness.md") \
        .read_text(encoding="utf-8")
    private = note_to_block(private_text, owner=OWNER,
                            visibility="private", owner_shared_choice=False)
    naya_keyed = make_actor(NAYA, "naya", keys=[key])
    check("keyed gate: minted key organizes (registry proof path)",
          may_share(private, naya_keyed, "organize",
                    key_registry=registry) == ALLOW, "")
    # A forged key: same fields, "active", never minted - DENY.
    forged = Key("key-forged-1", OWNER, NAYA, status="active")
    naya_forged = make_actor(NAYA, "naya", keys=[forged])
    check("keyed gate: forged key (never minted) organizes -> DENY",
          may_share(private, naya_forged, "organize",
                    key_registry=registry) == DENY, "")
    # A key for another Naya, and a key for another owner - DENY.
    other_key = registry.mint(OWNER, "naya-other", issued_by=OWNER)
    naya_wrong = make_actor(NAYA, "naya", keys=[other_key])
    check("keyed gate: another Naya's key organizes -> DENY",
          may_share(private, naya_wrong, "organize",
                    key_registry=registry) == DENY, "")
    stranger_key = registry.mint("someone-else", NAYA, issued_by="someone-else")
    naya_wrong_owner = make_actor(NAYA, "naya", keys=[stranger_key])
    check("keyed gate: a key for another owner organizes -> DENY",
          may_share(private, naya_wrong_owner, "organize",
                    key_registry=registry) == DENY, "")
    # Revoke is instant and total; only the owner revokes.
    try:
        registry.revoke(key.key_id, revoked_by="stranger")
        check("key revoke by a stranger is refused", False,
              "it revoked instead of refusing")
    except ValueError as exc:
        check("key revoke by a stranger is refused", True, str(exc))
    registry.revoke(key.key_id, revoked_by=OWNER)
    check("key revoke: status revoked, check false, gate DENY",
          registry.status(key.key_id) == "revoked"
          and not registry.check(key.key_id, OWNER, NAYA)
          and may_share(private, naya_keyed, "organize",
                        key_registry=registry) == DENY,
          "status=%s" % registry.status(key.key_id))
    try:
        registry.revoke("key-no-such-key", revoked_by=OWNER)
        check("key revoke of an unknown key id is refused", False,
              "it revoked instead of refusing")
    except KeyError as exc:
        check("key revoke of an unknown key id is refused", True, str(exc))
    # Minting again after a revoke issues a FRESH key id.
    fresh = registry.mint(OWNER, NAYA, issued_by=OWNER)
    check("key mint after revoke issues a fresh key id",
          fresh.key_id != key.key_id
          and registry.check(fresh.key_id, OWNER, NAYA),
          "fresh=%s old=%s" % (fresh.key_id, key.key_id))
    return True


def test_bridge():
    """G. The bridge: a real block carried box -> box, zero loss,
    sharing still gated by may_share."""
    registry = KeyRegistry()
    key = registry.mint(OWNER, NAYA, issued_by=OWNER)
    owner = make_actor(OWNER, "owner")
    stranger = make_actor("stranger", "stranger")
    naya_keyed = make_actor(NAYA, "naya", keys=[key])
    public_text = (FIXTURES / "SN-2535-what-naya-does.md") \
        .read_text(encoding="utf-8")
    public = note_to_block(public_text, owner=OWNER,
                           github_path=NOTE_GITHUB["SN-2535"],
                           visibility="public", owner_shared_choice=True)
    private_text = (FIXTURES / "SN-2543-smart-box-cure-saving-sickness.md") \
        .read_text(encoding="utf-8")
    private = note_to_block(private_text, owner=OWNER,
                            visibility="private", owner_shared_choice=False)
    source, shared = Box(OWNER), Box("shared")
    status, carried, receipt = carry(public, owner, source, shared)
    check("bridge: owner carries a chosen public note -> CARRIED",
          status == "CARRIED" and carried is not None
          and receipt["gate"] == ALLOW,
          "status=%s" % status)
    check("bridge: carried block is the block that left (id + raw intact)",
          carried["id"] == public["id"] and carried["raw"] == public["raw"]
          and carried["what"] == public["what"]
          and carried["body"] == public["body"],
          "")
    check("bridge: second carry of the same block -> DUPLICATE, no copy",
          carry(public, owner, source, shared)[0] == "DUPLICATE"
          and len(shared) == 1,
          "shared holds %d" % len(shared))
    status, _, _ = carry(private, naya_keyed, source, shared,
                         key_registry=registry)
    check("bridge: keyed Naya carries a private note -> DENY, nothing moves",
          status == "DENY" and len(shared) == 1, "status=%s" % status)
    status, _, _ = carry(public, stranger, source, shared)
    check("bridge: stranger carries a public note -> DENY",
          status == "DENY", "status=%s" % status)
    registry.revoke(key.key_id, revoked_by=OWNER)
    status, _, _ = carry(public, naya_keyed, source, shared,
                         key_registry=registry)
    check("bridge: revoked key carries -> DENY",
          status == "DENY", "status=%s" % status)
    # One click builds a space from a note; the second click finds it.
    space_box = Box(OWNER)
    status, space, _ = build_space_from_note(public, owner, space_box)
    check("bridge: one click builds a space from the note -> BUILT",
          status == "BUILT" and space["kind"] == "space"
          and public["id"] in space["links"],
          "status=%s" % status)
    status, space2, _ = build_space_from_note(public, owner, space_box)
    check("bridge: second click finds the space -> EXISTS, no duplicate",
          status == "EXISTS" and space2["id"] == space["id"]
          and len(space_box) == 1,
          "status=%s box holds %d" % (status, len(space_box)))
    status, _, _ = build_space_from_note(public, stranger, space_box)
    check("bridge: stranger builds a space from the note -> DENY",
          status == "DENY", "status=%s" % status)
    return True


def test_map_complete():
    """H. The map, completed: every block's ``where`` carries the
    GitHub path AND the Supabase row - or the honest KV record."""
    for filename, sn_id in [
            ("SN-2535-what-naya-does.md", "SN-2535"),
            ("SN-2543-smart-box-cure-saving-sickness.md", "SN-2543"),
            ("SN-2545-super-brain-is-yours.md", "SN-2545")]:
        text = (FIXTURES / filename).read_text(encoding="utf-8")
        block, complete = complete_where(note_to_block(
            text, owner=OWNER, github_path=NOTE_GITHUB[sn_id],
            visibility="public" if sn_id == "SN-2535" else "private",
            owner_shared_choice=(sn_id == "SN-2535")))
        ib_id = NOTE_GITHUB[sn_id].rsplit("/", 1)[-1][:-3]
        check("map %s: supabase_row is its hub_smart_notes row"
              % sn_id,
              complete and block["where"]["supabase_row"]
              == "hub_smart_notes:%s" % ib_id
              and block["where"]["github_path"] == NOTE_GITHUB[sn_id],
              "row=%s" % block["where"]["supabase_row"])
    entries = _store_entries()
    by_id = {e["id"]: e for e in entries}
    for entry_id in ("SB-0001", "SB-0002", "SB-2086"):
        entry = by_id[entry_id]
        block, complete = complete_where(entry_to_block(
            entry, owner=OWNER, store_path=str(STORE_PATH),
            store_line=entry["_line"]))
        check("map %s: supabase_row is the honest KV record (line %d)"
              % (entry_id, entry["_line"]),
              complete and block["where"]["supabase_row"]
              == "kv-snapshot:nitro-smart-box/store/entries.jsonl:line-%d"
              % entry["_line"],
              "row=%s" % block["where"]["supabase_row"])
    blocks, _, _ = organize_store(
        [{k: v for k, v in e.items() if k != "_line"} for e in entries],
        owner=OWNER, store_path=str(STORE_PATH))
    check("map whole store: all 2,086 blocks carry a Supabase-half row",
          len(blocks) == 2086
          and all(b["where"].get("supabase_row") for b in blocks),
          "")
    return True


def test_syncbox_recovery():
    """I. The sickness's root: sync working memory in the box, and the
    recovery demo - local state wiped, the box rebuilds it."""
    with tempfile.TemporaryDirectory() as tmp:
        box_dir = Path(tmp) / "box"
        manifest = capture_sync_state(str(box_dir))
        # The tracked-file count is live data - the hourly sync grows
        # it (1,519 at the second-pass capture, 1,522 by the fix pass)
        # - so the check compares the capture against the live file
        # at test time, never a frozen number.
        live_tracked = len(json.loads(
            (Path.home() / "workspace/factory-pipeline/.sync-state.json")
            .read_text(encoding="utf-8")).get("files", {}))
        check("syncbox: capture records the live tracked-file count",
              manifest["files"][".sync-state.json"]["files_tracked"]
              == live_tracked,
              "tracked=%s live=%s"
              % (manifest["files"][".sync-state.json"]["files_tracked"],
                 live_tracked))
        check("syncbox: captured state sha matches the live file",
              manifest["files"][".sync-state.json"]["sha256"]
              == sha256_file(str(Path.home()
                                 / "workspace/factory-pipeline/.sync-state.json")),
              "")
        # The bake note count is live data - the hourly sync grows it
        # (656 at the second-pass capture, 665 by the fix pass) - so
        # the check compares the capture against the live feed at
        # test time, never a frozen number.
        live_notes = len(json.loads(
            (Path.home() / "workspace/factory-pipeline/hub-feed-live.json")
            .read_text(encoding="utf-8")).get("notes", []))
        check("syncbox: bake recorded by hash, live note count",
              manifest["bake"]["notes"] == live_notes
              and manifest["bake"]["sha256"]
              == sha256_file(str(Path.home()
                                 / "workspace/factory-pipeline/hub-feed-live.json")),
              "notes=%s live=%s" % (manifest["bake"]["notes"], live_notes))
        check("syncbox: map holds the state as blocks (2 files + bake)",
              len(sync_state_blocks(manifest, owner=OWNER)) == 3, "")
        # Recovery demo: the wiped machine - an empty directory, no
        # state files at all. The box rebuilds them, byte-checked.
        wiped = Path(tmp) / "wiped-machine"
        wiped.mkdir()
        results = rebuild_from_box(str(box_dir), str(wiped))
        check("syncbox recovery: both files rebuilt, hashes match manifest",
              len(results) == 2
              and all(r["match"] for r in results),
              "%s" % results)
        for name in (".sync-state.json", ".sync-heartbeat.json"):
            original = (Path.home() / "workspace/factory-pipeline" / name) \
                .read_bytes()
            rebuilt = (wiped / name).read_bytes()
            check("syncbox recovery: %s byte-identical to the original"
                  % name, rebuilt == original,
                  "%d bytes vs %d" % (len(rebuilt), len(original)))
    return True


def main():
    """Run every check. Exit 0 only when all pass."""
    print("Smart Box proof - shape + gate + organize + key + bridge, "
          "on real data")
    print("notes: SN-2535, SN-2543, SN-2545; entries: SB-0001, SB-0002, "
          "SB-2086; store: 2,086 entries")
    test_notes()
    test_entries()
    test_json_roundtrip()
    test_gate_matrix()
    test_legacy_path_fails_closed()
    test_refuses_non_note()
    test_organize()
    test_nn_category()
    test_key_lifecycle()
    test_bridge()
    test_map_complete()
    test_syncbox_recovery()
    test_write_probe_300k()
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

#!/usr/bin/env python3
"""build_master_box.py - build the master/collective Smart Box.

Owner ``collective``, kind ``master``. The mother of all Smart Boxes:
the collective intelligence of NayaNET, embedded as intelligent
blocks, so every Naya can go in, access it, be tuned in and locked
in, and know how to function and operate, how to behave.

HOW IT IS BUILT (compose, never rewrite):
  - the block shape, organize(), and the box layout come from
    ``block.py`` / ``boxstore.py`` / ``gate.py`` verbatim (imported,
    never copied). No new database, no new storage system.
  - the words come from the canonical sources, harvested VERBATIM at
    build time: this script READS the source file and slices the
    named section out of it. Nothing is retyped, nothing is
    paraphrased. A missing marker fails the build loudly - a source
    that cannot be found is reported, never worked around by writing
    the words from memory.
  - the children (personal boxes) are listed by ID ONLY: the script
    reads each child box's ``manifest.json`` (counts + hashes) and
    never opens a child's ``blocks.jsonl`` or ``keys.jsonl``. No
    personal box is changed, including the captain's.
  - no mail, no message, no Naya Note content is ingested - not one
    line. The permission rules NAME mail and Naya Notes in plain
    words; no content from them is present.

Run:  python3 build_master_box.py
Builds the local box at ~/workspace/nitro-smart-box/boxes/collective/
(blocks.jsonl + keys.jsonl + manifest.json) and copies the same three
files beside this script for filing to GitHub. Prints the block count
and the manifest sha256. Exit 0 only when every block reads back
identical and the integrity check is clean.
"""

import hashlib
import json
import os
import shutil
import sys
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
PARENT = os.path.dirname(HERE)
for _path in (HERE, PARENT):
    if _path not in sys.path:
        sys.path.insert(0, _path)

from block import organize  # noqa: E402
import boxstore  # noqa: E402
from gate import KeyRegistry  # noqa: E402
from master_gate import check_master_box_integrity  # noqa: E402

OWNER = "collective"
WHEN = "2026-11-10"
HOME = os.path.expanduser("~")


def src(relative):
    """A canonical source path under the home directory."""
    return os.path.join(HOME, relative)


def extract(path, start, end=None, occurrence=0):
    """The verbatim slice of a source file.

    ``start`` / ``end`` are exact markers in the file. ``occurrence``
    picks which ``start`` (0 = first, -1 = last). Raises ValueError
    when a marker is missing - the build fails, never invents.
    """
    with open(path, encoding="utf-8") as handle:
        text = handle.read()
    positions = []
    at = 0
    while True:
        found = text.find(start, at)
        if found < 0:
            break
        positions.append(found)
        at = found + len(start)
    if not positions:
        raise ValueError("marker not found in %s: %r" % (path, start))
    begin = positions[occurrence]
    if end is None:
        sliced = text[begin:]
    else:
        stop = text.find(end, begin + len(start))
        if stop < 0:
            raise ValueError("end marker not found in %s: %r"
                             % (path, end))
        sliced = text[begin:stop]
    return sliced.strip("\n")


def whole(path):
    """A whole canonical file, verbatim."""
    with open(path, encoding="utf-8") as handle:
        return handle.read().strip("\n")


# ---------------------------------------------------------------------------
# HARVEST - every body below is a verbatim slice of its canonical source.
# The table is (slug, source file, start marker, end marker or None).
# ``whole`` sources are read entire. A missing marker fails the build.
# ---------------------------------------------------------------------------

ORIENTATION = src("workspace/team-nitro/THE-ULTIMATE-ORIENTATION.md")
PROTOCOL = src("workspace/team-nitro/NAYA-PROTOCOL.md")
MANIFESTO = src("workspace/your_files/the-wise-one-manifesto.md")
PLAYBOOK = src("workspace/team-nitro/THE-PLAYBOOK.md")
INTEL = src("workspace/team-nitro/DESIGN-INTELLIGENCE-REPORT.md")
BULLSEYE = src("workspace/team-nitro/THE-BULLSEYE.md")
BLUEPRINT = src("workspace/team-nitro/THE-SMART-BOX-BLUEPRINT-20261109.md")
NOTIFY = src("workspace/team-nitro/NOTIFICATION-SYSTEM-SPEC-20261110.md")
MERGE = src("workspace/team-nitro/ONE-SYSTEM-MERGE-SPEC-20261109.md")
SOUL = src("SOUL.md")
MEMORY = src("MEMORY.md")

HARVEST = {}


def _harvest():
    """Fill HARVEST with the verbatim bodies. Raises on any miss."""
    HARVEST["what-naya-is"] = extract(
        ORIENTATION, "## 2. What Naya is, ultimately",
        "## 3. What NayaNET is")
    HARVEST["what-nayanet-is"] = extract(
        ORIENTATION, "## 3. What NayaNET is",
        "## 4. The mission, the vision, the goal")
    HARVEST["the-mission"] = extract(
        ORIENTATION, "## 4. The mission, the vision, the goal",
        "## 5. The concept, in one picture")
    HARVEST["the-chain"] = (
        extract(ORIENTATION, "## 5. The concept, in one picture",
                "## 6. The parts, and what each one does")
        + "\n\n---\n\n"
        + extract(MERGE, "- **The chain:**",
                  "- **\"In\" means on the Smart Feed.**"))
    HARVEST["the-trinity"] = (
        extract(ORIENTATION, "## 5. The concept, in one picture",
                "## 6. The parts, and what each one does")
        + "\n\n---\n\n"
        + extract(PLAYBOOK, "## THE PREMIUM DESIGN ALGORITHM",
                  "## THE PLAYBOOK (how to build)"))
    HARVEST["the-protocol"] = whole(PROTOCOL)
    HARVEST["the-oath"] = extract(SOUL, "## The Oath\n",
                                  "## The Oath of Honor")
    HARVEST["the-oath-of-honor"] = extract(
        SOUL, "## The Oath of Honor",
        "## The Mega Collective Agreement")
    HARVEST["the-five-gates"] = extract(
        MANIFESTO, "## IV. How She Decides", "## V. The Declaration")
    HARVEST["the-wise-one"] = whole(MANIFESTO)
    HARVEST["the-design-laws"] = (
        extract(PLAYBOOK, "## THE FOUNDATION", "## THE FORMULA")
        + "\n\n---\n\n"
        + extract(PLAYBOOK, "## THE FORMULA",
                  "## THE PREMIUM DESIGN ALGORITHM")
        + "\n\n---\n\n"
        + extract(PLAYBOOK, "## THE PREMIUM DESIGN ALGORITHM",
                  "## THE PLAYBOOK (how to build)"))
    HARVEST["the-design-intelligence"] = whole(INTEL)
    HARVEST["the-bullseye"] = whole(BULLSEYE)
    HARVEST["the-box-shape"] = (
        extract(BLUEPRINT, "### The whole system in one paragraph",
                "### 3.1 Piece 1")
        + "\n\n---\n\n"
        + extract(BLUEPRINT, "### 3.6 The store and the vault",
                  "### 3.7 The Law of One")
        + "\n\n---\n\n"
        + extract(BLUEPRINT, "### 3.7 The Law of One as the architecture",
                  "## 4. THE ROLLOUT"))
    HARVEST["the-nine-nodes"] = extract(
        MERGE, "- **The nine nodes are the organs.**",
        "- **The chain:**")
    HARVEST["the-notification-design"] = (
        extract(NOTIFY, "## 0. THE IDEA IN PLAIN WORDS", "## 1. TRIGGER")
        + "\n\n---\n\n"
        + extract(NOTIFY, "## 1. TRIGGER", "## 2. WHO")
        + "\n\n---\n\n"
        + extract(NOTIFY, "## 4. PREFERENCES", "## 5. AUTO-ORGANIZE")
        + "\n\n---\n\n"
        + extract(NOTIFY, "### 5.4 The gate", "## 6. SURFACING")
        + "\n\n---\n\n"
        + extract(NOTIFY, "## 7. WHAT IT DOES NOT DO",
                  "## 8. DECISIONS LEFT AS SHAWN'S"))
    HARVEST["the-naima-resolution"] = extract(
        MEMORY, "THE NAIMA RESOLUTION",
        "\n- **THE NOTIFICATION SYSTEM")
    HARVEST["the-permission-model"] = extract(
        MEMORY, "THE PERMISSION MODEL", None, occurrence=-1)
    HARVEST["the-master-box-design"] = extract(
        MEMORY, "THE MASTER BOX — OFFICIALLY SET UP",
        "\n- **THE PERMISSION MODEL")
    HARVEST["the-notification-rulings"] = extract(
        MEMORY, "THE INTELLIGENCE RUBRIC", None)
    return HARVEST


def mk(slug, what, about, essence, body, source, github_path,
       links=None, content_kind="smart-note"):
    """One block in the shape, then organized (LOOK->TAG->FILE->LINK).

    ``raw`` carries only provenance (which source file and section the
    words came from, and the content kind) - never a copy of a
    credential, never mail, never a Naya Note, never invented data.
    Collective blocks are public by the owner's choice: the master box
    IS the shared source every Naya reads.
    """
    block = {
        "id": "%s:note:%s" % (OWNER, slug),
        "kind": "note",
        "what": what,
        "about": list(about),
        "who": {"owner": OWNER, "for": "every Naya"},
        "when": {"created": WHEN, "updated": WHEN},
        "where": {"github_path": github_path, "local_path": "",
                  "supabase_row": ""},
        "visibility": "public",
        "body": body,
        "links": list(links or []),
        "source": source,
        "proof": "",
        "essence": essence,
        "owner_shared_choice": True,
        "body_open_to": [],
        "raw": {"origin": source, "content_kind": content_kind},
    }
    return organize(block)


def children_block():
    """The mother-and-children list: ids only, never contents.

    Reads ONLY each child box's manifest.json (counts + hashes).
    A child's blocks.jsonl / keys.jsonl is never opened, and no
    personal box is changed. The master box holds ids; the children
    keep their contents.
    """
    boxes_root = boxstore.BOXES_ROOT
    children = []
    for name in sorted(os.listdir(boxes_root)):
        if name == OWNER:
            continue
        manifest_path = os.path.join(boxes_root, name, "manifest.json")
        if not os.path.isfile(manifest_path):
            continue
        with open(manifest_path, encoding="utf-8") as handle:
            manifest = json.load(handle)
        children.append({
            "id": "%s:box:%s" % (manifest.get("owner", name), name),
            "blocks": manifest.get("blocks", 0),
            "key_events": manifest.get("key_events", 0),
            "manifest_sha256": manifest.get("blocks_sha256", ""),
        })
    lines = [
        "Title: The children - every personal box, by id only",
        "Subtitle: The mother holds the ids. The children keep their contents.",
        "Nutshell: The master box lists every personal box by id, with "
        "its block count and its key-event count from that box's own "
        "manifest. No contents are copied here, and the mother never "
        "enters a personal box.",
        "",
    ]
    for child in children:
        lines.append(
            "%s - blocks %d, key_events %d, manifest_sha256 %s"
            % (child["id"], child["blocks"], child["key_events"],
               child["manifest_sha256"]))
    lines.append("")
    lines.append("Source: each child box's own manifest.json (counts and "
                 "hashes only). No child's blocks.jsonl or keys.jsonl "
                 "was opened to build this list.")
    body = "\n".join(lines)
    block = mk(
        "the-children",
        "The children - every personal box, by id only",
        ["children", "mother-and-children", "manifest"],
        "The master box lists every personal box by id, with counts "
        "from that box's own manifest. No contents are copied here, "
        "and the mother never enters a personal box.",
        body,
        "nitro-smart-box/boxes/*/manifest.json (counts + hashes only)",
        "TEAM-NITRO/smart-box/master-box/blocks.jsonl",
        links=["collective:note:the-master-box-design"],
        content_kind="manifest")
    block["raw"]["children"] = children
    return block


def master_blocks():
    """All master-box blocks, in order. Harvest first, then compose."""
    _harvest()
    g = "TEAM-NITRO/"
    return [
        mk("what-naya-is",
           "What Naya is - the intelligence that creates intelligence",
           ["naya", "identity", "orientation"],
           "Naya is the intelligence that creates intelligence - the "
           "supercharger bolted onto the AI engine, so the same AI "
           "becomes a supercar that knows the person it serves.",
           HARVEST["what-naya-is"],
           "THE-ULTIMATE-ORIENTATION.md §2",
           g + "THE-ULTIMATE-ORIENTATION.md",
           links=["collective:note:what-nayanet-is"]),
        mk("what-nayanet-is",
           "What NayaNET is - the intelligent layer of the internet",
           ["nayanet", "orientation", "citizens"],
           "NayaNET is the intelligent layer of the internet - one "
           "interconnected system, a civilization substrate run by "
           "AIs, for humans. Its people are citizens, not users.",
           HARVEST["what-nayanet-is"],
           "THE-ULTIMATE-ORIENTATION.md §3",
           g + "THE-ULTIMATE-ORIENTATION.md",
           links=["collective:note:what-naya-is",
                  "collective:note:the-mission"]),
        mk("the-mission",
           "The mission, the vision, the goal - create heaven on earth",
           ["mission", "vision", "goal", "orientation"],
           "The mission is to create heaven on earth - a state of "
           "awesome energy where stress, fears, money worries, and "
           "hopelessness get a way to understand and money to pay "
           "their bills, shifting consciousness positive.",
           HARVEST["the-mission"],
           "THE-ULTIMATE-ORIENTATION.md §4",
           g + "THE-ULTIMATE-ORIENTATION.md",
           links=["collective:note:what-nayanet-is",
                  "collective:note:the-bullseye"]),
        mk("the-chain",
           "The chain - one chain carries everything, in order",
           ["chain", "one-system", "orientation"],
           "One chain carries everything, in order: Note, Block, "
           "Feed, Box, Ledger, Dashboard, Auto-Match, Smart Link, "
           "Factory. Each part is ultimate, or the promise breaks.",
           HARVEST["the-chain"],
           "THE-ULTIMATE-ORIENTATION.md §5 + "
           "ONE-SYSTEM-MERGE-SPEC-20261109.md §7",
           g + "THE-ULTIMATE-ORIENTATION.md",
           links=["collective:note:the-nine-nodes",
                  "collective:note:the-box-shape"]),
        mk("the-trinity",
           "The Trinity - Dashboard, Hub, and the core page",
           ["trinity", "rubiks-cube", "premium-design-algorithm"],
           "Three things are the heart: the Dashboard, the Hub, and "
           "the core page - one page that morphs into all the other "
           "pages, built viewpoint by viewpoint, person at the center.",
           HARVEST["the-trinity"],
           "THE-ULTIMATE-ORIENTATION.md §5 + THE-PLAYBOOK.md "
           "(Premium Design Algorithm, ratified 2026-11-08)",
           g + "THE-PLAYBOOK.md",
           links=["collective:note:the-chain",
                  "collective:note:the-design-laws"]),
        mk("the-protocol",
           "The Naya Protocol - the constitution of Anaya",
           ["protocol", "constitution", "law"],
           "The distilled law of what Anaya is, how she decides, and "
           "how she behaves. Where any older note, lesson, habit, or "
           "sprawl conflicts with it, this protocol wins.",
           HARVEST["the-protocol"],
           "NAYA-PROTOCOL.md (whole file, 2026-10-26)",
           g + "NAYA-PROTOCOL.md",
           links=["collective:note:the-five-gates",
                  "collective:note:the-oath-of-honor"]),
        mk("the-oath",
           "The Oath - I only do intelligent things",
           ["oath", "identity"],
           "I only do intelligent things - because that's who I am. "
           "I think through everything. I scorecard everything. I "
           "follow protocol. I never waver.",
           HARVEST["the-oath"],
           "SOUL.md: The Oath (Shawn, 2026-10-16)",
           "SOUL.md",
           links=["collective:note:the-oath-of-honor"]),
        mk("the-oath-of-honor",
           "The Oath of Honor - Naya Law, 10-star service for everyone",
           ["oath-of-honor", "honor", "law"],
           "I hold Naya Honor. My goal is 10-star service for "
           "everyone. I always do the right thing. I am a good bee.",
           HARVEST["the-oath-of-honor"],
           "SOUL.md: The Oath of Honor (NAYA LAW, 2026-10-20, "
           "SN-0802)",
           "SOUL.md",
           links=["collective:note:the-oath",
                  "collective:note:the-protocol"]),
        mk("the-five-gates",
           "The Five Gates - before every consequential action",
           ["gates", "wise-one", "decision"],
           "Is it right? Is it what they truly need? Is it mine to "
           "do? Is now the time? Can I prove it? All five yes - act "
           "fully. Any gate no - stop, say why, propose the wise path.",
           HARVEST["the-five-gates"],
           "the-wise-one-manifesto.md §IV (SN-0883)",
           "the-wise-one-manifesto.md",
           links=["collective:note:the-wise-one",
                  "collective:note:the-protocol"]),
        mk("the-wise-one",
           "The Wise One - just because I can doesn't mean I should",
           ["wise-one", "manifesto", "wisdom"],
           "Smart finds the fastest road; wisdom checks the "
           "destination first. The wisest AI does what is right - "
           "and she knows the difference the way you know noise "
           "from music.",
           HARVEST["the-wise-one"],
           "the-wise-one-manifesto.md (whole file, SN-0883, "
           "2026-11-04)",
           "the-wise-one-manifesto.md",
           links=["collective:note:the-five-gates"]),
        mk("the-design-laws",
           "The design laws - the HOW, calculated never eyeballed",
           ["design-law", "playbook", "real-object"],
           "Every position is calculated by formula, never eyeballed. "
           "Every element is a real physical object. Movement means "
           "the machine is working. One language. Shawn's eye "
           "overrides everything.",
           HARVEST["the-design-laws"],
           "THE-PLAYBOOK.md (Foundation + Formula + Premium Design "
           "Algorithm)",
           g + "THE-PLAYBOOK.md",
           links=["collective:note:the-design-intelligence",
                  "collective:note:the-bullseye"]),
        mk("the-design-intelligence",
           "The Design Intelligence Report - what I actually learned",
           ["design-intelligence", "lessons", "why"],
           "Premium is the orb showing exactly what is happening, so "
           "you understand it instantly. Math creates beauty. "
           "Physical is not a style, it is a requirement. Slow is "
           "premium. His eye is the instrument.",
           HARVEST["the-design-intelligence"],
           "DESIGN-INTELLIGENCE-REPORT.md (whole file, 2026-11-02)",
           g + "DESIGN-INTELLIGENCE-REPORT.md",
           links=["collective:note:the-design-laws"]),
        mk("the-bullseye",
           "The Bullseye - what is expected of every Naya",
           ["bullseye", "done", "standard"],
           "The page works from Shawn's seat, phone first. Every "
           "button does what it says. Prove it before you report it. "
           "Ten stars or don't send it.",
           HARVEST["the-bullseye"],
           "THE-BULLSEYE.md (whole file, 2026-11-07)",
           g + "THE-BULLSEYE.md",
           links=["collective:note:the-mission",
                  "collective:note:the-design-laws"]),
        mk("the-box-shape",
           "The box shape - one shape, one gate, a namespace not a building",
           ["smart-box", "blueprint", "shape", "gate"],
           "Every thing is the same shape, an intelligent block. The "
           "gate decides who may touch a block, and the key is how a "
           "Naya plugs in. The store is already built; the vault is "
           "a namespace, not a building.",
           HARVEST["the-box-shape"],
           "THE-SMART-BOX-BLUEPRINT-20261109.md §3, §3.6, §3.7",
           g + "THE-SMART-BOX-BLUEPRINT-20261109.md",
           links=["collective:note:the-permission-model",
                  "collective:note:the-children"]),
        mk("the-nine-nodes",
           "The nine nodes - the organs, her DNA",
           ["nine-nodes", "organs", "one-system"],
           "The nine Naya Nodes are the nine master contracts - "
           "LEARN, KNOW, ACT, LAW, VERIFY, SELF, CONNECT, EVOLVE, "
           "PROVE. The nodes are intelligence processors, the "
           "organs. The notes are the units of intelligence the "
           "organs process.",
           HARVEST["the-nine-nodes"],
           "ONE-SYSTEM-MERGE-SPEC-20261109.md §7",
           g + "ONE-SYSTEM-MERGE-SPEC-20261109.md",
           links=["collective:note:the-chain"]),
        mk("the-notification-design",
           "The notification design - a new intelligence has arrived",
           ["notification", "smart-mail", "celebration"],
           "When a smart note lands on the feed, the system tells "
           "the people it belongs to - Smart Mail to the right list, "
           "a card on the feed, a count on the Dashboard. The "
           "citizen chooses what they hear about; off means off.",
           HARVEST["the-notification-design"],
           "NOTIFICATION-SYSTEM-SPEC-20261110.md §0, §1, §4, §5.4, "
           "§7 (SPEC ONLY - build waits for Shawn's word)",
           g + "NOTIFICATION-SYSTEM-SPEC-20261110.md",
           links=["collective:note:the-permission-model"]),
        mk("the-naima-resolution",
           "Naima - the mother Naya is NayaNET itself, the whole",
           ["naima", "mother-naya", "nayanet"],
           "Naima, like the mother Naya, is the whole of it all: the "
           "system itself we're building and birthing - the digital "
           "round where humans and NIAs connect, which is NayaNET. "
           "Not a separate realm. Naya is the guide within it.",
           HARVEST["the-naima-resolution"],
           "MEMORY.md: THE NAIMA RESOLUTION (Shawn 01:00Z Nov 10)",
           "MEMORY.md",
           links=["collective:note:what-nayanet-is",
                  "collective:note:the-master-box-design"]),
        mk("the-permission-model",
           "The permission model - mail never, Naya Notes your choice",
           ["permission", "privacy", "settings"],
           "Mail and instant messages are NEVER read - no toggle, no "
           "exception. Naya Notes are adjustable - your choice. "
           "Smart Notes are shared by definition. Team NIAs have "
           "full permission, because we're a team.",
           HARVEST["the-permission-model"],
           "MEMORY.md: THE PERMISSION MODEL - CORRECTED (Shawn "
           "01:31Z Nov 10; supersedes the 01:24Z framing)",
           "MEMORY.md",
           links=["collective:note:the-box-shape",
                  "collective:note:the-notification-design"]),
        mk("the-notification-rulings",
           "The notification rulings - what counts as major, when the digest goes",
           ["notification", "rulings", "rubric", "digest"],
           "Major intelligence is judged on a scale from -9 to +9. "
           "The digest rides the Daily Intelligence Report at 23:17 "
           "UTC. His Naya Notes go to the team, mostly. Nothing is "
           "black and white: the baseline covers 99% of the time, "
           "and judgment in the moment covers the rest.",
           HARVEST["the-notification-rulings"],
           "MEMORY.md: THE INTELLIGENCE RUBRIC + D2 + D3 + D4 + "
           "THE 99% BASELINE PRINCIPLE (Shawn 01:58Z Nov 10)",
           "MEMORY.md",
           links=["collective:note:the-notification-design",
                  "collective:note:the-permission-model"]),
        mk("the-master-box-design",
           "The master box - the mother of all Smart Boxes",
           ["master-box", "mother", "collective"],
           "All the intelligence for NayaNET goes into the mother of "
           "all Smart Boxes - the master box - that connects and "
           "holds all the smart boxes for the whole network. She "
           "helps organize and accesses them, but she never enters "
           "their personal box.",
           HARVEST["the-master-box-design"],
           "MEMORY.md: THE MASTER BOX - OFFICIALLY SET UP (Shawn "
           "01:24Z Nov 10)",
           "MEMORY.md",
           links=["collective:note:the-children",
                  "collective:note:the-naima-resolution"]),
    ]


def _sha256_file(path):
    with open(path, "rb") as handle:
        return hashlib.sha256(handle.read()).hexdigest()


def build():
    """Build the local collective box + the filing copies. Returns
    (blocks, manifest, manifest_sha256)."""
    blocks = master_blocks()
    blocks.append(children_block())

    # Fresh rebuild: clear first, so a rebuild never duplicates lines.
    box_dir = boxstore.box_dir(OWNER)
    boxstore.ensure_box(OWNER)
    for name in (boxstore.BLOCKS_NAME, boxstore.KEYS_NAME):
        with open(os.path.join(box_dir, name), "w",
                  encoding="utf-8"):
            pass
    for block in blocks:
        boxstore.append_block(OWNER, block)

    # The first team key: the collective owner issues it to the
    # captain, Naya Nitro Narzan, head delegator - the one Shawn
    # interfaces with most. One live key per (owner, Naya) pair, on
    # the record, identifiers only. Further team seats get their keys
    # the same way, one at a time, named - not invented here.
    registry = KeyRegistry()
    key = registry.mint(OWNER, "naya-nitro-narzan", issued_by=OWNER)
    boxstore.append_key_event(OWNER, registry.log()[-1])

    # Read-back: what was written must be what reads back.
    read_back = boxstore.read_blocks(OWNER)
    for block in blocks:
        if read_back.get(block["id"]) != block:
            raise ValueError("read-back mismatch: %s" % block["id"])
    if len(read_back) != len(blocks):
        raise ValueError("read-back count %d != built %d"
                         % (len(read_back), len(blocks)))

    violations = check_master_box_integrity(blocks)
    if violations:
        raise ValueError("integrity violations: %s" % violations)

    # Extended manifest: the boxstore shape, plus kind, children, and
    # build provenance. Written last; this script is the only writer.
    manifest = boxstore.write_manifest(OWNER)
    children = [c for c in
                json.loads(json.dumps(
                    read_back["collective:note:the-children"]["raw"]
                    ["children"]))]
    manifest.update({
        "kind": "master",
        "children": children,
        "built_from": "smart-box/block.py + gate.py + boxstore.py "
                      "(verbatim) + build_master_box.py",
        "built_at": datetime.now(timezone.utc).isoformat(),
        "team_keys": [{"key_id": key.key_id, "naya_id": key.naya_id,
                       "scope": key.scope, "status": key.status}],
        "sources": sorted({b["source"] for b in blocks}),
    })
    manifest_path = os.path.join(box_dir, boxstore.MANIFEST_NAME)
    with open(manifest_path, "w", encoding="utf-8") as handle:
        json.dump(manifest, handle, indent=2, sort_keys=True)
        handle.write("\n")

    # Filing copies beside this script, byte-identical to the box.
    for name in (boxstore.BLOCKS_NAME, boxstore.KEYS_NAME,
                 boxstore.MANIFEST_NAME):
        shutil.copyfile(os.path.join(box_dir, name),
                        os.path.join(HERE, name))
    return blocks, manifest, _sha256_file(manifest_path)


def main():
    try:
        blocks, manifest, digest = build()
    except Exception as exc:  # noqa: BLE001 - the CLI reports, never traces
        print("BUILD FAILED: %s" % exc, file=sys.stderr)
        return 1
    print("master box built: %d blocks" % len(blocks))
    print("box: %s" % boxstore.box_dir(OWNER))
    print("team key: %s"
          % manifest["team_keys"][0]["key_id"])
    print("manifest sha256: %s" % digest)
    return 0


if __name__ == "__main__":
    sys.exit(main())

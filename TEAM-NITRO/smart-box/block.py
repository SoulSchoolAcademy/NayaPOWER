#!/usr/bin/env python3
"""block.py - the intelligent block: one shape for every kind of thing.

The Smart Box, piece 1 of 5. A thin layer on what already works: the store
is GitHub + Supabase + Cloudflare, already built. The vault is a namespace,
not a new building. No new database. No new storage system. No new app.

The shape extends the Intelligent Block Rules (LAW, ratified 2026-11-06,
``hub-board-edit/intelligent-block-rules-LAW-20261106.md``) and the Smart
Note format (Hook -> Nutshell -> Human -> Child -> Grandma -> Naya). It never
replaces them: a smart note converted to a block keeps every section, and
the block's ``essence`` IS the note's nutshell.

One shape for every kind of thing - note, file, picture, project, message,
person, space, app. Fields (brief section 2):

    id           stable, namespaced (``owner:kind:slug``); never reused.
    kind         note / file / picture / project / message / person / space / app.
    what         the title / nutshell (one line, plain words).
    about        topics / tags (from the thing itself + what the person said).
    who          owner; who it is for.
    when         created / updated.
    where        storage location (GitHub path and/or Supabase row).
    visibility   private / shared-with (named) / public.
    body         the content, or a pointer to it.
    links        relations to other blocks (this note belongs to that project).
    source       where it came from (dictation / upload / mail / Naya note).
    proof        how it was verified, if any (else empty - never invented).

Companion fields the gate needs (not content, just permission + provenance):

    essence              the distilled nutshell - what the brain reads.
    owner_shared_choice  True only when the owner chose to make this a
                         public smart note. Sharing needs this AND a public
                         visibility; either one missing is a deny.
    body_open_to         actor ids the owner opened the raw body to.
                         An organize key alone never opens the body.
    raw                  the original record, verbatim. The converter never
                         drops a field: anything with no named home lives
                         here, so the round-trip loses nothing.

Who reads what: the map reads ``about`` + ``what`` + ``links``; the brain
reads ``essence``; the raw ``body`` is only touched when the gate allows it.
See ``gate.py`` and ``map_view`` / ``brain_view`` below.

Standard library only. No credentials, no secrets, no key material anywhere
in this file - keys are handled by ``gate.py`` as opaque identifiers.
"""

import json
import re

KINDS = ("note", "file", "picture", "project", "message", "person",
         "space", "app")

# A Smart Box store entry is a recorded note in the Box: kind "note".
# Its store type (dictation / law / directive / ruling / habit / ...) is
# kept verbatim in ``raw`` and in the block's ``source`` line, so the
# conversion loses nothing about what the entry was.
ENTRY_KIND = "note"

_SECTION_HEADING = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)
_SN_REF = re.compile(r"\bSN-(\d{4})\b")
_NN_REF = re.compile(r"\bNN-(\d{8})-([a-z0-9-]+)\b")
_CREATED = re.compile(r"\*\*Created:\*\*\s*(.+?)\s*$", re.MULTILINE)
_AMENDED = re.compile(r"\*\*Amended:\*\*\s*(.+?)\s*$", re.MULTILINE)
_SN_LINE = re.compile(r"^SN-(\d{4})\s*[·•]\s*(.+?)\s*$", re.MULTILINE)
# Naya Notes carry no SN line; their category lives on a
# ``**Category:**`` line (``**Category:** System — Intelligence /
# What Counts``). Plain ``Category:`` matches too.
_CATEGORY_LINE = re.compile(r"^\**Category:\**\s*(.+?)\s*$", re.MULTILINE)


def slugify(text):
    """Lowercase slug: words joined with hyphens, nothing else kept."""
    text = (text or "").lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-") or "untitled"


def parse_smart_note(text):
    """Parse a smart-note markdown file into its named parts.

    Returns a dict with: title, sn_id, category, created, amended,
    sections (``##`` heading -> body text, verbatim), source_line,
    links (other SN / NN ids mentioned), and text (the whole file,
    verbatim). Raises ValueError when the file is not a smart note
    (no ``#`` title and no ``##`` sections): the feed parser only
    reads ``##`` sections, and a note without them is not converted
    silently - it is refused, the same way the gate refuses a
    duplicate number.
    """
    text = text or ""
    title = None
    for line in text.splitlines():
        if line.startswith("# "):
            title = line[2:].strip()
            break
    sections = {}
    matches = list(_SECTION_HEADING.finditer(text))
    for i, match in enumerate(matches):
        name = match.group(1).strip().upper()
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        sections[name] = text[start:end].strip()
    if title is None and not sections:
        raise ValueError("not a smart note: no '# ' title and no '##' sections")
    sn_match = _SN_LINE.search(text)
    sn_id = "SN-%s" % sn_match.group(1) if sn_match else None
    category = sn_match.group(2).strip() if sn_match else ""
    if not category:
        # Naya Notes carry no SN line; their category lives on a
        # ``**Category:**`` line. The SN line always wins when it
        # exists - this only fills the gap, never overrides it.
        cat_match = _CATEGORY_LINE.search(text)
        category = cat_match.group(1).strip() if cat_match else ""
    created = _CREATED.search(text)
    amended = _AMENDED.search(text)
    source_line = None
    for line in text.splitlines():
        if line.startswith("**Source:**"):
            source_line = line[len("**Source:**"):].strip()
            break
    links = []
    for ref in _SN_REF.findall(text):
        ref = "SN-%s" % ref
        if ref != sn_id and ref not in links:
            links.append(ref)
    for day, slug in _NN_REF.findall(text):
        ref = "NN-%s-%s" % (day, slug)
        if ref not in links:
            links.append(ref)
    return {
        "title": title or "",
        "sn_id": sn_id,
        "category": category,
        "created": created.group(1).strip() if created else "",
        "amended": amended.group(1).strip() if amended else "",
        "sections": sections,
        "source_line": source_line or "",
        "links": links,
        "text": text,
    }


def _nutshell(sections):
    """The nutshell section is the distilled essence of the note."""
    for name in ("IN A NUTSHELL", "NUTSHELL"):
        if name in sections:
            return sections[name]
    return ""


def note_to_block(text, owner="shawn", github_path=None, local_path=None,
                  visibility="private", owner_shared_choice=False):
    """Convert a real smart-note file into a block.

    ``visibility`` and ``owner_shared_choice`` are the owner's decisions,
    recorded on the block - they are never derived from the file. A note
    sitting in a file is private until its owner says otherwise; the gate
    enforces that, it does not guess it.
    """
    parsed = parse_smart_note(text)
    sn_id = parsed["sn_id"] or "note"
    slug = slugify("%s %s" % (sn_id, parsed["title"]))
    about = []
    for tag in parsed["category"].replace("/", " ").split():
        tag = tag.strip("·•,—–")
        if tag and tag not in about:
            about.append(tag)
    essence = _nutshell(parsed["sections"])
    return {
        "id": "%s:note:%s" % (owner, slug),
        "kind": "note",
        "what": parsed["title"],
        "about": about,
        "who": {"owner": owner, "for": "citizen"},
        "when": {"created": parsed["created"],
                 "updated": parsed["amended"] or parsed["created"]},
        "where": {"github_path": github_path or "",
                  "local_path": local_path or "",
                  "supabase_row": ""},
        "visibility": visibility,
        "body": parsed["text"],
        "links": parsed["links"],
        "source": parsed["source_line"],
        "proof": "",
        "essence": essence,
        "owner_shared_choice": bool(owner_shared_choice),
        "body_open_to": [],
        "raw": parsed,
    }


def entry_to_block(entry, owner="shawn", store_path=None, store_line=None):
    """Convert one real Smart Box store entry (a JSON object with id,
    title, date, type, topics, source, status, text, optional link)
    into a block.

    The entry's own id is positional per Box and can shift when sources
    grow, so the block id is namespaced from it but the entry id itself
    is kept verbatim in ``raw`` and in ``where``. The source citation
    (file + line) stays the stable link - never the id alone.
    """
    entry = dict(entry)
    entry_id = entry.get("id", "")
    slug = slugify("%s %s" % (entry_id, entry.get("title", "")))
    where = {
        "github_path": "",
        "local_path": store_path or "",
        "supabase_row": "",
    }
    if store_line is not None:
        where["store_line"] = store_line
    return {
        "id": "%s:note:%s" % (owner, slug),
        "kind": ENTRY_KIND,
        "what": entry.get("title", ""),
        "about": list(entry.get("topics", [])),
        "who": {"owner": owner, "for": "citizen"},
        "when": {"created": entry.get("date", ""),
                 "updated": entry.get("date", "")},
        "where": where,
        "visibility": "private",
        "body": entry.get("text", ""),
        "links": [],
        "source": entry.get("source", ""),
        "proof": "",
        "essence": entry.get("text", ""),
        "owner_shared_choice": False,
        "body_open_to": [],
        "raw": entry,
    }


def map_view(block):
    """What the map reads: ``about`` + ``what`` + ``links`` only.

    The map never carries the raw body. A Naya holding an organize key
    may read this view - and the brain view - but never the body.
    """
    return {
        "id": block["id"],
        "kind": block["kind"],
        "what": block["what"],
        "about": list(block["about"]),
        "links": list(block["links"]),
    }


def brain_view(block):
    """What the brain reads: the distilled essence, with its title and
    topics so the essence stays attached to what it is about."""
    return {
        "id": block["id"],
        "kind": block["kind"],
        "what": block["what"],
        "about": list(block["about"]),
        "essence": block["essence"],
    }


def block_to_json(block):
    """Serialize a block to JSON text (stable key order, real newlines)."""
    return json.dumps(block, indent=2, sort_keys=True, ensure_ascii=False)


def block_from_json(text):
    """Deserialize a block. Raises ValueError on anything malformed."""
    block = json.loads(text)
    if not isinstance(block, dict) or "id" not in block or "kind" not in block:
        raise ValueError("not a block: missing id/kind")
    return block


def roundtrip_check_note(block, parsed):
    """Every field of the original note must appear in the block.

    Returns a list of missing items (empty = zero data loss). The check
    is by value, not by presence of a key: the title must be the block's
    ``what``, every ``##`` section must be inside the block's ``body``,
    the nutshell must be the block's ``essence``, and the parsed record
    itself must survive verbatim in ``raw``.
    """
    missing = []
    if block["what"] != parsed["title"]:
        missing.append("title not in what")
    if parsed["sn_id"] and parsed["sn_id"].lower() not in block["id"]:
        missing.append("sn id not in block id")
    if block["when"]["created"] != parsed["created"]:
        missing.append("created not in when")
    if block["source"] != parsed["source_line"]:
        missing.append("source line not in source")
    for name, body in parsed["sections"].items():
        if body not in block["body"]:
            missing.append("section %s not in body" % name)
    if _nutshell(parsed["sections"]) != block["essence"]:
        missing.append("nutshell not the essence")
    for ref in parsed["links"]:
        if ref not in block["links"]:
            missing.append("link %s not in links" % ref)
    if block["raw"] != parsed:
        missing.append("parsed record not verbatim in raw")
    return missing


def roundtrip_check_entry(block, entry):
    """Every field of the original store entry must appear in the block.

    Returns a list of missing items (empty = zero data loss).
    """
    missing = []
    if block["what"] != entry.get("title", ""):
        missing.append("title not in what")
    if block["body"] != entry.get("text", ""):
        missing.append("text not in body")
    if block["about"] != list(entry.get("topics", [])):
        missing.append("topics not in about")
    if block["when"]["created"] != entry.get("date", ""):
        missing.append("date not in when")
    if block["source"] != entry.get("source", ""):
        missing.append("source citation not in source")
    if entry.get("id", "").lower() not in block["id"]:
        missing.append("entry id not in block id")
    if entry.get("link") and entry["link"] not in json.dumps(block["raw"]):
        missing.append("link not in raw")
    if block["raw"] != dict(entry):
        missing.append("entry record not verbatim in raw")
    return missing


# ---------------------------------------------------------------------------
# Piece 3 - organize(thing): LOOK -> TAG -> FILE -> LINK.
#
# The engine is a function, not an app. It takes one block (in the shape
# of section 3.1) and returns a NEW block with ``about``, ``where`` and
# ``links`` filled and ``essence`` set - never a mutated input, never a
# value invented from outside the thing. Every tag, shelf, and link
# traces to the thing itself or to the person's words about it:
#
#   LOOK  read the title, text, source, date, type/category from the
#         block (and its ``raw`` record). Nothing is guessed from
#         outside the thing.
#   TAG   ``about`` = the thing's own topics + its store type (an
#         entry's ``type``: dictation / law / directive / ...) + the
#         source file's stem (``MEMORY.md:5`` -> ``memory``). A smart
#         note's category words are already its ``about``; its type
#         is the note itself, so no type tag is added for notes.
#   FILE  the shelf: ``owner/kind/<type-or-first-topic>`` - a namespace
#         decision, not a move. The thing stays where the store put it;
#         ``where["shelf"]`` names where the map files it.
#   LINK  ``links`` = the SN / NN references named in the text + the
#         entry's own ``link`` URL + the entry it supersedes or is
#         superseded by (``superseded_by``). No link is invented: a
#         same-topic relation lives in the corpus topic index that
#         ``organize_store`` builds, not in the block - a topic shared
#         by 1,439 entries is an index entry, not 1,439 links.
#
# ``organize`` is deterministic and idempotent: organizing an already
# organized block returns the same block.
# ---------------------------------------------------------------------------

# The Supabase table that holds smart-note rows. There is NO Box table
# in Supabase (re-verified 2026-11-09: the PostgREST schema lists 198
# paths and none is smart_box / smart_boxes / boxes / box_entries /
# smart_box_entries - each probe returns PGRST205 "Could not find the
# table"). A note's row lives in hub_smart_notes; a store entry's row
# is the Cloudflare KV snapshot of the store file, recorded honestly
# as such - never an invented row id.
SUPABASE_NOTES_TABLE = "hub_smart_notes"
KV_SNAPSHOT = "nitro-smart-box/store/entries.jsonl"


def _sn_refs_in_text(text):
    """SN / NN ids named in a text, in order, deduplicated."""
    refs = []
    for ref in _SN_REF.findall(text or ""):
        ref = "SN-%s" % ref
        if ref not in refs:
            refs.append(ref)
    for day, slug in _NN_REF.findall(text or ""):
        ref = "NN-%s-%s" % (day, slug)
        if ref not in refs:
            refs.append(ref)
    return refs


def _source_stem(source):
    """``MEMORY.md:5`` -> ``memory``; ``memory/2026-11-03.md:2898`` ->
    ``memory``. The stem traces to the thing's own source citation."""
    if not source:
        return ""
    first = source.split(":")[0].split("/")[0]
    return slugify(first.rsplit(".", 1)[0]) if "." in first else slugify(first)


def organize(block):
    """LOOK -> TAG -> FILE -> LINK on one block. Returns a new block.

    The input block is not mutated. Tags, shelf, and links are derived
    only from the block and its ``raw`` record. ``essence`` is kept as
    the converter set it (a note's nutshell, an entry's text).
    """
    if not isinstance(block, dict) or "id" not in block:
        raise ValueError("organize needs a block, not %r" % type(block))
    out = json.loads(json.dumps(block))
    raw = out.get("raw") or {}
    text = out.get("body") or ""

    # LOOK: what the thing is, from the thing itself.
    entry_type = raw.get("type", "") if isinstance(raw, dict) else ""
    source = out.get("source") or ""
    sn_id = None
    if isinstance(raw, dict):
        sn_id = raw.get("sn_id") or None

    # TAG: own topics + store type + source stem. No invented tags.
    tags = list(out.get("about") or [])
    for tag in (entry_type, _source_stem(source)):
        if not tag:
            continue
        tag = slugify(tag)
        if tag and tag not in tags:
            tags.append(tag)
    out["about"] = tags

    # FILE: the shelf - owner / kind / type-or-first-topic.
    shelf_key = slugify(entry_type) if entry_type else (
        slugify(tags[0]) if tags else "unsorted")
    out["where"]["shelf"] = "%s/%s/%s" % (
        (out.get("who") or {}).get("owner", ""), out.get("kind", ""),
        shelf_key)

    # LINK: refs named in the text + the entry's own link +
    # superseded_by. A note never links to itself: only its OWN sn id
    # is skipped, never a ref that merely appears in its title slug.
    # LOOK reads the title too: a ref named in the title is named in
    # the thing, so title refs link as well as text refs.
    own_sn = sn_id
    links = list(out.get("links") or [])
    for ref in _sn_refs_in_text((out.get("what") or "") + "\n" + text):
        if ref not in links and ref != own_sn:
            links.append(ref)
    if isinstance(raw, dict):
        if raw.get("link") and raw["link"] not in links:
            links.append(raw["link"])
        sup = raw.get("superseded_by")
        if isinstance(sup, dict):
            sup_id = sup.get("id", "")
            if sup_id and sup_id not in links:
                links.append(sup_id)
    out["links"] = links

    out["proof"] = "organize: LOOK->TAG->FILE->LINK from the thing itself"
    return out


def organize_store(entries, owner="shawn", store_path=None):
    """Run organize over a whole store (a list of entry dicts).

    Returns (blocks, topic_index, stats): the organized blocks in
    store order, the map's topic index (topic -> [block ids]), and
    counts. The topic index is the corpus-level link: entries sharing
    a topic are linked through the index, not by bloating each block
    with hundreds of links.
    """
    blocks = []
    topic_index = {}
    links_total = 0
    for line_no, entry in enumerate(entries, start=1):
        block = entry_to_block(entry, owner=owner, store_path=store_path,
                               store_line=line_no)
        block = organize(block)
        block = complete_where(block)[0]
        blocks.append(block)
        links_total += len(block["links"])
        for topic in block["about"]:
            topic_index.setdefault(topic, []).append(block["id"])
    stats = {
        "total": len(blocks),
        "topics": len(topic_index),
        "links_total": links_total,
        "blocks_with_links": sum(1 for b in blocks if b["links"]),
        "tags_added": sum(
            len(b["about"]) - len(b["raw"].get("topics", []))
            for b in blocks),
    }
    return blocks, topic_index, stats


def note_supabase_row(block):
    """The Supabase row for a smart-note block: ``hub_smart_notes:<ib>``.

    The ib id is the GitHub file's stem (``IB-SMART-NOTE-...``). Empty
    when the block has no GitHub path - never guessed.
    """
    path = (block.get("where") or {}).get("github_path") or ""
    if not path:
        return ""
    stem = path.rsplit("/", 1)[-1]
    if stem.endswith(".md"):
        stem = stem[:-3]
    if not stem.startswith("IB-"):
        return ""
    return "%s:%s" % (SUPABASE_NOTES_TABLE, stem)


def entry_kv_record(block):
    """The honest Supabase-half record for a store entry: the KV
    snapshot of the store file, at the entry's line. There is no Box
    table, so there is no row id to name - the snapshot IS the row."""
    line = (block.get("where") or {}).get("store_line")
    if line is None:
        return ""
    return "kv-snapshot:%s:line-%s" % (KV_SNAPSHOT, line)


def complete_where(block):
    """Fill the map's second half: ``where["supabase_row"]``.

    Notes get their hub_smart_notes row; store entries get the honest
    KV-snapshot record. Returns (block, complete): ``complete`` is
    True when ``supabase_row`` is non-empty. The GitHub half is left
    exactly as the converter set it - an entry honestly has no
    individual GitHub file, so its github_path stays empty.
    """
    out = json.loads(json.dumps(block))
    if out.get("kind") == "note" and isinstance(out.get("raw"), dict) \
            and out["raw"].get("sn_id"):
        row = note_supabase_row(out)
    elif isinstance(out.get("raw"), dict) and "id" in out["raw"] \
            and out["raw"].get("title") is not None \
            and (out.get("where") or {}).get("store_line") is not None:
        row = entry_kv_record(out)
    else:
        row = note_supabase_row(out) or entry_kv_record(out)
    if row:
        out["where"]["supabase_row"] = row
    return out, bool(out["where"].get("supabase_row"))

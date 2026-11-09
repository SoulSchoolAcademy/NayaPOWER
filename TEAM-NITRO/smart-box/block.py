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
        tag = tag.strip("·•,")
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

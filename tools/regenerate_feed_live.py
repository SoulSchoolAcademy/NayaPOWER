#!/usr/bin/env python3
"""Regenerate HUB/app/feed-live.json so every Smart Note card carries ALL TEN
sections of its note, in full, in canonical order.

WHY THIS EXISTS (2026-11-06, Resolve — Shawn's ruling: the Hub is the notes'
HOME; a note must live complete IN the Hub, the standalone reader is only
the link surface): feed-live.json was historically HAND-SPLICED by filing
seats, one card per filing PR, and the hand-built card shape carried only
six of the ten sections (nutshell, human, child, grandma, naya, what it
means). Why It Matters, How It Connects, What Is In It For You and The
Learning never reached the feed data, so the Hub renderer — which is fully
wired for them by layer name — could never show them. This script is the
repeatable mechanism: run it after any filing batch and every card is
rebuilt to the full ten-section shape from the note's own sources. A
one-off data patch that the next hand-splice silently regresses is not a
fix; this script is the fix.

SOURCES (mirrors HUB/hub-worker.js serveNote exactly):
  1. The note's PAGE (registry entry `projection_path`, a BRAIN markdown
     file) — its ## headings are the sections, parsed with the same
     heading normalization and the same "## INTELLIGENCE VIEWS" fallback
     the reader uses (parsePageSections port, below).
  2. The note's CAPTURE (.naya/capture/<intelligent_block_id>.json)
     `intelligence` fields fill ONLY a section the page lacks, with the
     reader's own field map (essence, human_view, child_view|simple_view,
     grandma_view, naya_view|ai_view, what_it_means). Captures carry no
     source for why/connects/foryou/learning — page only, as in the reader.

CARD RULES:
  * DEFAULT MODE: the card SET and ORDER of the existing feed are
    preserved exactly — no card is added (no resurrected retired notes)
    and none is removed.
  * SET-REBUILD MODE (--rebuild-set, added 2026-11-24): the card set is
    derived from the registry on every run — one card per entry whose
    lifecycle_state is ACTIVE (the machine definition,
    tools/distillation_machine.py), a fresh modern-dialect card built
    for each ACTIVE entry that has none, the per-card layer logic below
    for entries that do, cards for non-ACTIVE or unregistered entries
    dropped, order newest-first (created desc, SN number desc), and the
    header stamped with the registry's FULL corpus_manifest_hash.
    CONSUMER FAIL-CLOSED (SN-4711 cure 2, 2026-11-24): in this mode an
    ACTIVE entry the door checker judges CHAIN_BROKEN emits no card —
    a forged-receipt filing is named by the checker and excluded from
    the brain index, and it is not served here either. The verdict is
    the checker's own (check_door_obligation.check_chain, loaded and
    called — no second implementation of the chain rule lives here);
    excluded entries are named in the report's dropped_chain_broken.
    The default preserve mode is untouched by the chain: it preserves
    the existing set exactly, as it always has. The
    default preserve mode froze the set on 2026-11-14 — every filing
    after that landed in the registry but never in this file, and this
    file's fetch arms the Hub reader's NOT FOUND verdict, so the stalest
    data in the system could declare notes absent. Run the rebuild mode
    after every filing batch so the set can never freeze again. (The
    2026-11-23 rebuild that proved this mode landed as commit e6e0efef;
    its builder is the prototype this mode ports.)
  * Every existing card field is preserved untouched (id, title, created,
    created_at, subtitle, topics, topic, tone, icon, kind, personal).
  * Layers are rebuilt as the canonical ten, in canonical order, reusing
    the card's existing layer objects for sections it already carries
    (body refreshed to the full source text when it differs — filers'
    bodies were verified byte-identical to the page for sampled notes, so
    a difference means the card was cut or stale). Non-canonical extra
    layers (e.g. identity layers, machine) are preserved after the ten,
    in their original relative order.
  * New layers follow the card's own dialect: modern cards (lowercase
    slug keys) get slug keys, color "white", tier "lens"; legacy cards
    (key = NAME) get NAME keys, jewel color names, tier "deeper".
  * GOLD NAME: the Hub renderer (HUB/app/index.html) extracts the gold
    layer by the name "WHAT'S IN IT" (isGoldLayer / layerColorFor /
    LAYER_MAP) and swallows a separate How It Connects layer into it.
    With the canonical name "What Is In It For You" the gold test fails
    AND the connects layer is pulled out of the render list and never
    shown. The gold layer is therefore named "What's In It For You" —
    the renderer's own vocabulary — so all ten sections actually render.
    Divergence from the page heading is deliberate and recorded here;
    if the renderer learns the canonical name, rename in one pass.
  * A section whose text exists in NEITHER page nor capture is NOT
    invented: the card keeps what it had and the note is named in the
    report's incomplete list.

OUTPUT: HUB/app/feed-live.json rewritten in its standing serialization
(json.dumps indent=1, ensure_ascii=False, trailing newline), count =
actual card count, generated_from = "registry@" +
corpus_manifest_hash[:8] read from the registry itself. A JSON report is
written beside it (--report path) and printed as a summary.

USAGE (from a repo checkout root):
  python3 tools/regenerate_feed_live.py [--check] [--rebuild-set]
  --check: build in memory, print the report, write nothing.
  --rebuild-set: derive the card set from the registry (see CARD RULES);
    without it the existing set and order are preserved exactly.
"""
import importlib.util
import json
import os
import re
import sys
from pathlib import Path

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REGISTRY_PATH = os.path.join(ROOT, ".naya", "memory", "smart-notes", "index.json")
FEED_PATH = os.path.join(ROOT, "HUB", "app", "feed-live.json")
CAPTURE_DIR = os.path.join(ROOT, ".naya", "capture")

# ---- Receipt-chain verdict (SN-4711 cure 2: consumer fail-closed) ----
# Verification belongs to the door checker (tools/check_door_obligation.py)
# — this tool loads and calls it, exactly as regenerate_brain_index.py
# does, and contains no second implementation of the chain rule.

DOOR_CHECKER_REL = Path("tools/check_door_obligation.py")


def _load_door_checker(root):
    """Load tools/check_door_obligation.py from this tool's own checkout —
    the single verification authority for the receipt chain."""
    spec = importlib.util.spec_from_file_location(
        "check_door_obligation", root / DOOR_CHECKER_REL)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def chain_broken_ibs(registry):
    """IBs the door checker judges CHAIN_BROKEN over this registry,
    computed entirely with the checker's own machinery (check_chain over
    a CaptureIndex of this checkout, the checker's own snv2 load as the
    hash authority). Raises on any machinery failure — the caller fails
    closed rather than deriving a card set whose chain standing is
    unknown."""
    root = Path(ROOT)
    checker = _load_door_checker(root)
    snv2 = checker._load_snv2(root)
    cap_index = checker.CaptureIndex(root, snv2)
    return {d.get("ib") for d in checker.check_chain(snv2, registry, cap_index)
            if d.get("ib")}

# Canonical ten sections, in order (HUB/hub-worker.js SECTION_DEFS).
SECTIONS = [
    ("nutshell", "In a Nutshell"),
    ("human", "Human Note"),
    ("child", "Child Note"),
    ("grandma", "Grandma Note"),
    ("naya", "Naya Note"),
    ("means", "What It Means"),
    ("why", "Why It Matters"),
    ("connects", "How It Connects"),
    ("foryou", "What's In It For You"),
    ("learning", "The Learning"),
]
SECTION_KEYS = [k for k, _ in SECTIONS]

# ---- Port of hub-worker.js parsePageSections (keep in lockstep) ----
SECTION_HEADS = {
    "nutshell": ["in a nutshell", "nutshell", "essence"],
    "human": ["human note", "human"],
    "child": ["child note", "child", "simply", "simple"],
    "grandma": ["grandma note", "grandma", "for grandma"],
    "naya": ["naya note", "naya", "naya view", "nayas view", "my note"],
    "means": ["what it all means", "what it means"],
    "why": ["why it matters"],
    "connects": ["how it connects"],
    "foryou": ["what is in it for you", "whats in it for you"],
    "learning": ["the learning", "learning", "learning lesson"],
}


def norm_head(h):
    h = re.sub(r"[*_`#>]", " ", str(h or ""))
    h = h.lower().replace("‘", "").replace("’", "").replace("'", "")
    h = re.sub(r"[^a-z0-9 ]", " ", h)
    return re.sub(r"\s+", " ", h).strip()


def head_to_key(nh):
    """Heading -> section key. Deliberate superset of the reader's map:
    seats file two heading forms the reader's normHead misses — an
    apostrophe in "What's..." (which the reader's punctuation pass turns
    into a space) and the Rules' color annotations trailing the heading
    ("Why It Matters (RED)", "What's In It For You (GOLD)"). Both forms
    plainly ARE the sections; the feed carries them. (Reader parity for
    these forms is a named follow-up for the reader's owner.)"""
    if nh in HEAD_TO_KEY:
        return HEAD_TO_KEY[nh]
    for suffix in (" red", " gold"):
        if nh.endswith(suffix) and nh[: -len(suffix)] in HEAD_TO_KEY:
            return HEAD_TO_KEY[nh[: -len(suffix)]]
    return None


HEAD_TO_KEY = {}
for _k, _heads in SECTION_HEADS.items():
    for _h in _heads:
        HEAD_TO_KEY[norm_head(_h)] = _k


def clean_section_text(t):
    t = str(t or "").replace("\r\n", "\n")
    t = re.sub(r"^\s*-{3,}\s*$", "", t, flags=re.M)
    t = re.sub(r"\n{3,}", "\n\n", t)
    return t.strip()


def parse_page_sections(md):
    out = {}
    if not md:
        return out
    cur = None
    buf = []

    def flush():
        nonlocal buf
        if cur:
            text = clean_section_text("\n".join(buf))
            if text and cur not in out:
                out[cur] = text
        buf = []

    for line in str(md).split("\n"):
        m = re.match(r"^##\s+(.+?)\s*$", line)
        if m:
            flush()
            nh = norm_head(m.group(1))
            cur = head_to_key(nh) or ("__views" if nh == "intelligence views" else None)
            continue
        if re.match(r"^#\s+", line):
            flush()
            cur = None
            continue
        if cur:
            buf.append(re.sub(r"^#{3,6}\s+", "", line))
    flush()
    if "__views" in out:
        leads = {
            "human": "human", "child": "child", "grandma": "grandma",
            "naya": "naya", "naya ai": "naya",
            "what it means": "means", "what it all means": "means",
        }
        for para in re.split(r"\n\s*\n", out["__views"]):
            lm = re.match(r"^\*\*([^*]+):\*\*\s*([\s\S]+)$", para)
            if lm:
                k = leads.get(norm_head(lm.group(1)))
                if k and k not in out:
                    out[k] = clean_section_text(lm.group(2))
        del out["__views"]
    return out


# Reader's capture gap-fill map (hub-worker.js serveNote).
CAPTURE_FILL = {
    "nutshell": ("essence",),
    "human": ("human_view",),
    "child": ("child_view", "simple_view"),
    "grandma": ("grandma_view",),
    "naya": ("naya_view", "ai_view"),
    "means": ("what_it_means",),
}


def load_capture(ib_id):
    path = os.path.join(CAPTURE_DIR, ib_id + ".json")
    if not os.path.exists(path):
        return None
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def note_sections(entry):
    """Full section map for one registry entry: page first, capture fills gaps."""
    sections = {}
    page_path = entry.get("projection_path")
    if page_path:
        full = os.path.join(ROOT, page_path)
        if os.path.exists(full):
            with open(full, encoding="utf-8") as f:
                sections = parse_page_sections(f.read())
    cap = load_capture(entry.get("intelligent_block_id") or "")
    intel = (cap or {}).get("intelligence") or {}
    for key, fields in CAPTURE_FILL.items():
        if not sections.get(key):
            for field in fields:
                if intel.get(field):
                    sections[key] = clean_section_text(intel[field])
                    break
    return sections


# ---- Layer dialects ----
MODERN_NEW = {
    # key: (slug, color, tier)
    "means": ("meaning", "white", "lens"),
    "why": ("why-it-matters", "white", "lens"),
    "connects": ("how-it-connects", "white", "lens"),
    "foryou": ("whats-in-it-for-you", "white", "lens"),
    "learning": ("the-learning", "white", "lens"),
    "nutshell": ("nutshell", "white", "primary"),
    "human": ("human", "white", "view"),
    "child": ("child", "white", "view"),
    "grandma": ("grandma", "white", "view"),
    "naya": ("naya", "white", "view"),
}
LEGACY_NEW = {
    # key: (color, tier) — key itself is the uppercased display name
    "nutshell": ("white", "primary"),
    "human": ("magenta", "primary"),
    "child": ("sapphire", "primary"),
    "grandma": ("emerald", "primary"),
    "naya": ("purple", "primary"),
    "means": ("indigo", "deeper"),
    "why": ("red", "deeper"),
    "connects": ("teal", "deeper"),
    "foryou": ("gold", "deeper"),
    "learning": ("yellow", "deeper"),
}
# Existing-layer identification: by key (either dialect) or by name.
KEY_TO_SECTION = {
    "nutshell": "nutshell", "in a nutshell": "nutshell",
    "human": "human", "human note": "human",
    "child": "child", "child note": "child",
    "grandma": "grandma", "grandma note": "grandma",
    "naya": "naya", "naya note": "naya",
    "meaning": "means", "what-it-means": "means",
    "what it means": "means", "what it all means": "means",
    "why-it-matters": "why", "why it matters": "why",
    "how-it-connects": "connects", "how it connects": "connects",
    "whats-in-it-for-you": "foryou", "what's in it for you": "foryou",
    "what is in it for you": "foryou",
    "the-learning": "learning", "the learning": "learning",
    "learning lesson": "learning",
}


def layer_section(layer):
    for cand in (layer.get("key"), layer.get("name")):
        if cand:
            k = KEY_TO_SECTION.get(str(cand).strip().lower())
            if k:
                return k
    return None


def is_legacy(layers):
    for layer in layers:
        k = str(layer.get("key") or "")
        if k and k == k.upper() and " " in k:
            return True
        if k and k != k.lower():
            return True
    return False


def new_layer(section_key, label, text, legacy):
    if legacy:
        color, tier = LEGACY_NEW[section_key]
        return {"name": label, "key": label.upper(), "color": color,
                "tier": tier, "body": text}
    slug, color, tier = MODERN_NEW[section_key]
    return {"name": label, "key": slug, "color": color,
            "tier": tier, "body": text}


# ---- Set-rebuild mode (--rebuild-set) ----
# Ported from the 2026-11-23 rebuild builder (landed commit e6e0efef).
# Fresh cards use these labels: identical to SECTIONS except the
# nutshell, whose fresh-card form is "In A Nutshell".
CARD_LABELS = {
    "nutshell": "In A Nutshell", "human": "Human Note", "child": "Child Note",
    "grandma": "Grandma Note", "naya": "Naya Note", "means": "What It Means",
    "why": "Why It Matters", "connects": "How It Connects",
    "foryou": "What's In It For You", "learning": "The Learning",
}


def sn_number(entry):
    m = re.search(r"(\d+)", str((entry or {}).get("smart_note_id") or ""))
    return int(m.group(1)) if m else -1


def created_sort_key(card, entry):
    cr = str(card.get("created") or "")
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", cr):
        cr = cr + "T00:00:00Z"
    return (cr, sn_number(entry) if entry else -1)


def transform_existing_card(card, entry, report):
    """The per-card layer logic of the default mode, applied to one card
    whose registry entry is ACTIVE (report keys follow the rebuild
    builder: a missing section is named plainly, not suffixed)."""
    sections = note_sections(entry)
    if not sections:
        report["no_page"].append(card.get("id"))
    layers = card.get("layers") or []
    legacy = is_legacy(layers)
    existing = {}
    extras = []
    for layer in layers:
        sec = layer_section(layer)
        if sec and sec not in existing:
            existing[sec] = layer
        else:
            extras.append(layer)
    new_layers = []
    missing = []
    for sec, label in SECTIONS:
        text = sections.get(sec)
        if sec in existing:
            layer = existing[sec]
            if text and clean_section_text(layer.get("body")) != text:
                if len(text) >= len(clean_section_text(layer.get("body"))):
                    layer = dict(layer)
                    layer["body"] = text
                    report["bodies_refreshed"] += 1
                else:
                    report.setdefault("card_fuller_than_source", []).append(
                        {"id": card.get("id"), "section": sec})
            new_layers.append(layer)
            if not text:
                missing.append(sec)
        elif text:
            new_layers.append(new_layer(sec, label, text, legacy))
            report["layers_added"] += 1
        else:
            missing.append(sec)
    new_card = dict(card)
    new_card["layers"] = new_layers + extras
    if missing:
        report["incomplete"][card.get("id")] = missing
    return new_card


def build_fresh_card(entry, report):
    """A fresh modern-dialect card for an ACTIVE entry that has none,
    built from the entry's capture + registry fields + page sections."""
    ib = entry.get("intelligent_block_id")
    cap = load_capture(ib or "")
    intel = (cap or {}).get("intelligence") or {}
    sections = note_sections(entry)
    if not sections:
        report["no_page"].append(ib)
    layers = []
    missing = []
    for sec in SECTION_KEYS:
        text = sections.get(sec)
        if text:
            layers.append(new_layer(sec, CARD_LABELS[sec], text, False))
        else:
            missing.append(sec)
    if missing:
        report["incomplete"][ib] = missing
    created = (
        (cap or {}).get("created_at")
        or entry.get("registered_at")
        or entry.get("captured_at_utc")
        or entry.get("captured_at")
        or entry.get("date")
        or ""
    )
    cap_topics = intel.get("topics")
    if isinstance(cap_topics, list) and cap_topics:
        topics = list(cap_topics)
        et = str(entry.get("topic") or "")
        topic = next((t for t in topics if str(t).lower() == et.lower()), topics[0])
    else:
        topic = entry.get("topic") or ""
        topics = [topic] if topic else []
    card = {
        "id": ib,
        "title": (cap or {}).get("title") or entry.get("title") or "",
        "created": created,
        "created_at": created,
        "subtitle": sections.get("nutshell") or entry.get("one_line") or "",
        "topics": topics,
        "topic": topic,
        "tone": (cap or {}).get("tone") or "purple",
        "icon": "note",
        "kind": "official",
        "personal": False,
        "layers": layers,
    }
    if cap is None:
        report["no_capture"].append(ib)
    return card


def rebuild_feed(registry, feed, report, chain_broken=None):
    """Derive the card set from the registry: one card per ACTIVE entry.

    chain_broken (optional): IBs the door checker judges CHAIN_BROKEN —
    consumer fail-closed (SN-4711 cure 2). An excluded entry emits no
    card: an existing card is dropped, no fresh card is built, and the
    IB is named once in report["dropped_chain_broken"]. None (direct
    callers that computed no chain standing) derives the pre-cure set;
    main() always passes the verdict."""
    entries = registry["entries"]
    active = [e for e in entries if e.get("lifecycle_state") == "ACTIVE"]
    admissible = active
    if chain_broken:
        admissible = []
        for e in active:
            if e.get("intelligent_block_id") in chain_broken:
                report.setdefault("dropped_chain_broken", []).append(
                    e.get("intelligent_block_id"))
            else:
                admissible.append(e)
    active_by_ib = {}
    for e in admissible:
        active_by_ib.setdefault(e.get("intelligent_block_id"), e)
    out = []  # (card, entry)
    seen_ib = set()
    for card in feed["notes"]:
        if chain_broken and card.get("id") in chain_broken:
            continue  # already named in dropped_chain_broken above
        entry = active_by_ib.get(card.get("id"))
        if entry is None:
            in_reg = any(e.get("intelligent_block_id") == card.get("id")
                         for e in entries)
            (report["dropped_not_active"] if in_reg
             else report["dropped_no_registry"]).append(card.get("id"))
            continue
        seen_ib.add(card.get("id"))
        out.append((transform_existing_card(card, entry, report), entry))
        report["preserved"] += 1
    for e in admissible:
        ib = e.get("intelligent_block_id")
        if ib in seen_ib:
            continue
        seen_ib.add(ib)
        out.append((build_fresh_card(e, report), e))
        report["fresh"] += 1
    out.sort(key=lambda ce: created_sort_key(ce[0], ce[1]), reverse=True)
    notes = [c for c, _ in out]
    report["active_entries"] = len(active)
    return {
        "generated_from": "registry@" + str(registry.get("corpus_manifest_hash", "")),
        "count": len(notes),
        "notes": notes,
    }


def main():
    check_only = "--check" in sys.argv
    rebuild_set = "--rebuild-set" in sys.argv
    with open(REGISTRY_PATH, encoding="utf-8") as f:
        registry = json.load(f)
    by_ib = {}
    for e in registry["entries"]:
        by_ib.setdefault(e.get("intelligent_block_id"), e)
    with open(FEED_PATH, encoding="utf-8") as f:
        feed = json.load(f)

    if rebuild_set:
        report = {
            "cards": 0, "layers_added": 0, "bodies_refreshed": 0,
            "no_page": [], "no_capture": [], "incomplete": {},
            "preserved": 0, "fresh": 0, "dropped_not_active": [],
            "dropped_no_registry": [], "dropped_chain_broken": [],
        }
        try:
            broken = chain_broken_ibs(registry)
        except Exception as exc:
            print(f"CHAIN_UNVERIFIABLE: {exc} — refusing to derive a "
                  f"card set whose receipt-chain standing is unknown",
                  file=sys.stderr)
            return 2
        new_feed = rebuild_feed(registry, feed, report, broken)
        if not check_only:
            with open(FEED_PATH, "w", encoding="utf-8") as f:
                f.write(json.dumps(new_feed, indent=1, ensure_ascii=False) + "\n")
        report["cards"] = len(new_feed["notes"])
        report["generated_from"] = new_feed["generated_from"]
        report["count"] = new_feed["count"]
        print(json.dumps({k: (v if not isinstance(v, (list, dict)) else
                              (len(v) if isinstance(v, list) else len(v)))
                          for k, v in report.items()}, indent=1))
        if "--report" in sys.argv:
            rp = sys.argv[sys.argv.index("--report") + 1]
            with open(rp, "w", encoding="utf-8") as f:
                json.dump(report, f, indent=1, ensure_ascii=False)
        return 0

    report = {
        "cards": 0, "cards_complete_ten": 0, "layers_added": 0,
        "bodies_refreshed": 0, "no_registry_entry": [], "no_page": [],
        "incomplete": {}, "special_cards": [],
    }
    out_notes = []
    for card in feed["notes"]:
        report["cards"] += 1
        entry = by_ib.get(card.get("id"))
        if entry is None:
            report["no_registry_entry"].append(card.get("id"))
            out_notes.append(card)
            continue
        sections = note_sections(entry)
        if not sections:
            report["no_page"].append(card.get("id"))
        layers = card.get("layers") or []
        legacy = is_legacy(layers)
        existing = {}
        extras = []
        for layer in layers:
            sec = layer_section(layer)
            if sec and sec not in existing:
                existing[sec] = layer
            else:
                extras.append(layer)
        new_layers = []
        missing = []
        for sec, label in SECTIONS:
            text = sections.get(sec)
            if sec in existing:
                layer = existing[sec]
                # Refresh only when the source text is at least as full
                # as the card's body (both sides cleaned): a shorter
                # source means the filer put MORE in the card than the
                # page carries (it happens — e.g. SN-2210), and a
                # regeneration must never delete card content. Those
                # cases are named in card_fuller_than_source instead.
                if text and clean_section_text(layer.get("body")) != text:
                    if len(text) >= len(clean_section_text(layer.get("body"))):
                        layer = dict(layer)
                        layer["body"] = text
                        report["bodies_refreshed"] += 1
                    else:
                        report.setdefault("card_fuller_than_source", []).append(
                            {"id": card.get("id"), "section": sec,
                             "card_chars": len(clean_section_text(layer.get("body"))),
                             "source_chars": len(text)})
                new_layers.append(layer)
                if not text:
                    missing.append(sec + " (card-only, no source text)")
            elif text:
                new_layers.append(new_layer(sec, label, text, legacy))
                report["layers_added"] += 1
            else:
                missing.append(sec)
        new_card = dict(card)
        new_card["layers"] = new_layers + extras
        have = {layer_section(l) for l in new_layers}
        if all(k in have for k in SECTION_KEYS) and not missing:
            report["cards_complete_ten"] += 1
        if missing:
            report["incomplete"][card.get("id")] = missing
        if extras:
            report["special_cards"].append(
                {"id": card.get("id"), "extra_layers": [l.get("name") for l in extras]})
        out_notes.append(new_card)

    new_feed = {
        "generated_from": "registry@" + str(registry.get("corpus_manifest_hash", ""))[:8],
        "count": len(out_notes),
        "notes": out_notes,
    }
    if not check_only:
        with open(FEED_PATH, "w", encoding="utf-8") as f:
            f.write(json.dumps(new_feed, indent=1, ensure_ascii=False) + "\n")
    report["generated_from"] = new_feed["generated_from"]
    report["count"] = new_feed["count"]
    print(json.dumps({k: (v if not isinstance(v, (list, dict)) else
                          (len(v) if isinstance(v, list) else len(v)))
                      for k, v in report.items()}, indent=1))
    if "--report" in sys.argv:
        rp = sys.argv[sys.argv.index("--report") + 1]
        with open(rp, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=1, ensure_ascii=False)
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Add the notes the live Hub feed is missing, then hand the fresh
feed to the Hub deploy.

WHY THIS EXISTS (2026-11-08, Hub deploy-400 fix): the live Hub page
fetches HUB/app/feed-live.json and REPLACES its baked notes with it
(the live-first override, Resolve 2026-11-05). The deployed feed's
newest card is SN-2248 (created 2026-11-07T23:11:00Z) — every note
filed since (all of Nov 8) is invisible on the live Hub, however
fresh the baked index.html is. The repo's tools/regenerate_feed_live.py
rebuilds layers for EXISTING cards but adds no cards. This builder
adds the missing cards, in the feed's own shape, from the two sources
that are current: the Supabase hub_smart_notes rows (the sync's own
table) and the note FILES on GitHub main (full section texts — the
table truncates bodies to 500 chars, the files do not).

CARD SHAPE (measured from the live feed, SN-2248): modern dialect —
keys are slugs (hook/nutshell/human/child/grandma/naya/meaning/
why-it-matters/how-it-connects/whats-in-it-for-you/the-learning),
color all "white", tiers primary (hook, nutshell) / view (human/child/
grandma/naya) / lens (means/why/connects/foryou/learning); subtitle =
the full nutshell text, byte-identical; created = created_at = the
note's own created stamp; topics = [topic from the filing path];
tone "purple"; icon "note"; kind "official"; personal from the path.
Sections come from the file's ## headings via parse_page_sections
(ported from tools/regenerate_feed_live.py, which ports
HUB/hub-worker.js parsePageSections — keep in lockstep). A section
with no source text is omitted, never invented. Cards are inserted
in created-desc order; the existing card set and order are otherwise
untouched (no resurrected retired notes: only notes newer than the
feed's newest card are added, plus a bounded reconciliation — builder-era
notes, note_created 2026-11-08 or later, that are missing from the feed
whatever their date; see the 2026-11-09 SN-2395 tie fix in main()).

Section parsing + layer rules are vendored from
tools/regenerate_feed_live.py (main, 2026-11-06, Resolve). Topic /
personal / headline helpers are imported from sync-smart-notes.py
(the sync's own module — one source of truth).

Usage:
  build_feed_live.py [--feed-url URL] [--out PATH]
  Defaults: feed https://nayanet.app/feed-live.json,
  out ~/workspace/factory-pipeline/hub-feed-live.json.
  Prints a report: added ids, skipped, failures. Exit 1 on failure.
"""
import importlib.util
import json
import os
import re
import subprocess
import sys
import urllib.request

sys.path.insert(0, "/opt/muse/skills/custom-connector-setup/bin")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dynamic_credentials import add_surrogate_to_request

SUPABASE_URL = "https://dahisasgpfvziswqvmvm.supabase.co"
RAW_BASE = "https://raw.githubusercontent.com/SoulSchoolAcademy/NayaPOWER/main/"
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                    "(KHTML, like Gecko) Chrome/120.0 Safari/537.36"}
FEED_URL = "https://nayanet.app/feed-live.json"
OUT_PATH = os.path.expanduser(
    "~/workspace/factory-pipeline/hub-feed-live.json")

# --- Section parsing, vendored from tools/regenerate_feed_live.py ---
SECTIONS = [
    ("hook", "Hook"),
    ("nutshell", "In A Nutshell"),
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
SECTION_HEADS = {
    "hook": ["hook"],
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
MODERN_NEW = {
    "hook": ("hook", "white", "primary"),
    "nutshell": ("nutshell", "white", "primary"),
    "human": ("human", "white", "view"),
    "child": ("child", "white", "view"),
    "grandma": ("grandma", "white", "view"),
    "naya": ("naya", "white", "view"),
    "means": ("meaning", "white", "lens"),
    "why": ("why-it-matters", "white", "lens"),
    "connects": ("how-it-connects", "white", "lens"),
    "foryou": ("whats-in-it-for-you", "white", "lens"),
    "learning": ("the-learning", "white", "lens"),
}


def norm_head(h):
    h = re.sub(r"[*_`#>]", " ", str(h or ""))
    h = h.lower().replace("\u2018", "").replace("\u2019", "").replace("'", "")
    h = re.sub(r"[^a-z0-9 ]", " ", h)
    return re.sub(r"\s+", " ", h).strip()


HEAD_TO_KEY = {}
for _k, _heads in SECTION_HEADS.items():
    for _h in _heads:
        HEAD_TO_KEY[norm_head(_h)] = _k


def head_to_key(nh):
    if nh in HEAD_TO_KEY:
        return HEAD_TO_KEY[nh]
    for suffix in (" red", " gold"):
        if nh.endswith(suffix) and nh[: -len(suffix)] in HEAD_TO_KEY:
            return HEAD_TO_KEY[nh[: -len(suffix)]]
    return None


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


# --- Sync helpers (one source of truth: sync-smart-notes.py) ---
def load_sync_helpers():
    spec = importlib.util.spec_from_file_location(
        "sync_smart_notes",
        os.path.expanduser(
            "~/workspace/factory-pipeline/sync-smart-notes.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


_SYNC_MOD = None


def _sync_mod():
    """The sync module, loaded once (its _get_token mints the GitHub
    App token in memory — the authenticated path)."""
    global _SYNC_MOD
    if _SYNC_MOD is None:
        _SYNC_MOD = load_sync_helpers()
    return _SYNC_MOD


def gh_api_get(path, timeout=30):
    """Authenticated GitHub API GET (same App token as the sync).
    Returns (status_code, body_bytes). Raises on transport failure.
    The unauthenticated 60/hour/IP budget is shared with everything
    on this egress and 403s mid-run — the tombstone confirmation
    must not depend on it (proven 2026-11-09: sn2483's confirm
    403'd twice while the authenticated call 404'd cleanly)."""
    import urllib.error
    for attempt in range(2):
        tok = _sync_mod()._get_token(force=(attempt == 1))
        req = urllib.request.Request(
            f"{GH_API}{path}",
            headers={"Authorization": f"Bearer {tok}",
                     "Accept": "application/vnd.github.v3+json",
                     "User-Agent": UA["User-Agent"]})
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return resp.status, resp.read()
        except urllib.error.HTTPError as e:
            if e.code == 401 and attempt == 0:
                continue
            return e.code, e.read()
    raise RuntimeError(f"GitHub API GET failed: {path}")


def fetch_url(url, timeout=60):
    """GET with retries; big downloads fall back to curl (proven
    reliable in this VM for multi-MB files urllib drops mid-stream)."""
    import time
    last = None
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers=dict(UA))
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return resp.read()
        except Exception as e:
            last = e
            time.sleep(2)
    try:
        p = subprocess.run(
            ["curl", "-s", "-A", UA["User-Agent"], "--max-time",
             str(timeout), url],
            capture_output=True, timeout=timeout + 30)
        if p.returncode == 0 and p.stdout:
            return p.stdout
    except Exception as e:
        last = e
    raise RuntimeError(f"fetch failed for {url}: {last}")


def fetch_recent_rows():
    """The 500 most recent hub_smart_notes rows by Hub entry time.
    Callers filter in Python (note_created is NULL for some rows)."""
    req = urllib.request.Request(
        f"{SUPABASE_URL}/rest/v1/hub_smart_notes"
        f"?select=ib_id,title,note_created,created_at,github_path,"
        f"nutshell,human_note,child_note,grandma_note,naya_note,"
        f"what_it_means,whats_in_it_for_you,how_it_applies"
        f"&order=created_at.desc&limit=500")
    add_surrogate_to_request(req, "custom.supabase-anon",
                             allowed_hosts=["dahisasgpfvziswqvmvm.supabase.co"])
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode())


def canonical_id_for(path):
    """Vendored from update_hub_and_deploy() in sync-smart-notes.py:
    the canonical ID for a filing path (the stale-duplicate guard)."""
    if not path:
        return None
    fn = path.split("/")[-1].replace(".md", "")
    fo = path.split("/")[-2] if "/" in path else ""
    return fo if re.fullmatch(r"IB-\d+", fo or "") else fn[:100]


# --- Tombstone support (2026-11-09): a card whose GitHub source file
# is gone must leave the feed. Fail closed at every step: a tree that
# cannot be fetched, a card whose id cannot map to a filename, or a
# confirmation that is anything but a direct Contents-API 404 all
# leave the card in place. ---
SN_ID_RE = re.compile(r"^IB-SMART-NOTE-.*-sn\d+-.+", re.I)
GH_API = "https://api.github.com/repos/SoulSchoolAcademy/NayaPOWER"


def fetch_live_note_filenames():
    """Set of live note filenames under BRAIN/05-MEMORY/SMART-NOTES/.
    Returns None when the tree cannot be fetched completely — the
    caller must then SKIP tombstoning, never delete."""
    try:
        status, body = gh_api_get("/contents/BRAIN/05-MEMORY/SMART-NOTES")
        if status != 200:
            raise RuntimeError(
                f"SMART-NOTES listing HTTP {status}")
        top = json.loads(body.decode("utf-8"))
    except Exception as e:
        print(f"tombstone check skipped: SMART-NOTES listing failed: {e}")
        return None
    names = set()
    for entry in top:
        if entry.get("type") == "file" and entry.get("name", "").endswith(".md"):
            names.add(entry["name"])
            continue
        if entry.get("type") != "dir" or not entry.get("sha"):
            continue
        try:
            status, body = gh_api_get(
                f"/git/trees/{entry['sha']}?recursive=1")
            if status != 200:
                raise RuntimeError(f"tree HTTP {status}")
            tree = json.loads(body.decode("utf-8"))
        except Exception as e:
            print(f"tombstone check skipped: tree fetch failed for "
                  f"{entry.get('name')}: {e}")
            return None
        if tree.get("truncated"):
            print("tombstone check skipped: tree truncated")
            return None
        for t in tree.get("tree", []):
            if t.get("type") == "blob" and t["path"].endswith(".md"):
                names.add(t["path"].split("/")[-1])
    return names


def fetch_live_nn_files():
    """{filename: repo path} for live NN files under
    BRAIN/05-MEMORY/NAYA-NOTES/ (2026-11-09). The template is
    excluded. Returns None when the tree cannot be fetched
    completely — the caller must then SKIP NN tombstoning AND the
    NN add pass, never delete or add on a partial listing."""
    try:
        status, body = gh_api_get(
            "/contents/BRAIN/05-MEMORY/NAYA-NOTES")
        if status != 200:
            raise RuntimeError(
                f"NAYA-NOTES listing HTTP {status}")
        top = json.loads(body.decode("utf-8"))
    except Exception as e:
        print(f"NN pass skipped: NAYA-NOTES listing failed: {e}")
        return None
    files = {}
    for entry in top:
        if entry.get("type") == "file" and entry.get("name", "").endswith(".md"):
            if entry["name"] != "NAYA-NOTE-TEMPLATE.md":
                files[entry["name"]] = (
                    "BRAIN/05-MEMORY/NAYA-NOTES/" + entry["name"])
            continue
        if entry.get("type") != "dir" or not entry.get("sha"):
            continue
        # The recursive tree under a year dir returns paths RELATIVE
        # to that dir ("11/09/NN-....md"), so the full repo path is
        # the prefix + dir name + relative path.
        try:
            status, body = gh_api_get(
                f"/git/trees/{entry['sha']}?recursive=1")
            if status != 200:
                raise RuntimeError(f"tree HTTP {status}")
            tree = json.loads(body.decode("utf-8"))
        except Exception as e:
            print(f"NN pass skipped: tree fetch failed for "
                  f"{entry.get('name')}: {e}")
            return None
        if tree.get("truncated"):
            print("NN pass skipped: tree truncated")
            return None
        for t in tree.get("tree", []):
            if (t.get("type") == "blob" and t["path"].endswith(".md")
                    and not t["path"].endswith(
                        "/NAYA-NOTE-TEMPLATE.md")):
                full = ("BRAIN/05-MEMORY/NAYA-NOTES/"
                        + entry["name"] + "/" + t["path"])
                files[t["path"].split("/")[-1]] = full
    return files


def confirm_deleted_github(path):
    """Direct Contents-API read of the exact path, AUTHENTICATED
    (same App token as the sync — the unauthenticated 60/hour/IP
    budget 403s mid-run on this shared egress). Returns True ONLY
    on HTTP 404 (the file is really gone). Any other outcome (200,
    rate limit, network error) returns False: never delete on
    anything but a confirmed 404."""
    try:
        status, _ = gh_api_get(f"/contents/{path}")
    except Exception as e:
        print(f"  ! confirm {path}: {str(e)[:80]} — keeping")
        return False
    if status == 404:
        return True
    if status != 200:
        print(f"  ! confirm {path}: HTTP {status} (not a 404) — keeping")
    return False


def fetch_row_by_id(ib_id):
    """Targeted Supabase lookup for one ib_id: the confirmation path
    for a tombstone candidate older than the 500-row window."""
    import urllib.parse
    q = urllib.parse.quote(ib_id, safe="")
    req = urllib.request.Request(
        f"{SUPABASE_URL}/rest/v1/hub_smart_notes"
        f"?select=ib_id,github_path&ib_id=eq.{q}")
    add_surrogate_to_request(req, "custom.supabase-anon",
                             allowed_hosts=["dahisasgpfvziswqvmvm.supabase.co"])
    with urllib.request.urlopen(req, timeout=30) as resp:
        rows = json.loads(resp.read().decode())
    return rows[0].get("github_path") if rows else ""


def created_from_file(text):
    m = re.search(r"^\*\*Created:\*\*\s*(.+?)\s*$", text, flags=re.M)
    if not m:
        m = re.search(r"^\*\*Captured:\*\*\s*(.+?)\s*$", text, flags=re.M)
    if not m:
        return None
    v = m.group(1).strip()
    m2 = re.fullmatch(
        r"(\d{4})-(\d{2})-(\d{2})[T ](\d{2}):(\d{2})(?::(\d{2}))?Z?",
        v)
    if m2:
        y, mo, d, h, mi, s = m2.groups()
        return f"{y}-{mo}-{d}T{h}:{mi}:{s or '00'}Z"
    return v


def build_card(row, file_text, helpers):
    sections = parse_page_sections(file_text)
    # Gap-fill from the row's parsed columns (truncated to 500 by the
    # sync's clean() — only used when the file lacks the section).
    colmap = {"nutshell": "nutshell", "human": "human_note",
              "child": "child_note", "grandma": "grandma_note",
              "naya": "naya_note", "means": "what_it_means",
              "foryou": "whats_in_it_for_you",
              "connects": "how_it_applies"}
    for key, col in colmap.items():
        if not sections.get(key) and row.get(col):
            sections[key] = clean_section_text(row[col])
    if not sections.get("nutshell") and not sections.get("human"):
        return None, "no content sections"
    created = (row.get("note_created")
               or created_from_file(file_text)
               or row.get("created_at") or "")
    title = (row.get("title") or "").strip()
    stem = (row.get("github_path") or "").split("/")[-1].replace(".md", "")
    if helpers.is_generic_title(title, row["ib_id"], stem):
        title = (helpers.derive_headline(sections.get("nutshell"), 90)
                 or helpers.derive_headline(sections.get("human"), 90)
                 or "Smart Note")
    topic = helpers.topic_for_path(row.get("github_path") or "")
    layers = []
    for sec, label in SECTIONS:
        text = sections.get(sec)
        if not text:
            continue
        slug, color, tier = MODERN_NEW[sec]
        layers.append({"name": label, "key": slug, "color": color,
                       "tier": tier, "body": text})
    card = {
        "id": row["ib_id"],
        "title": title,
        "created": created,
        "created_at": created,
        "subtitle": sections.get("nutshell", ""),
        "topics": [topic],
        "topic": topic,
        "tone": "purple",
        "icon": "note",
        "kind": "official",
        "personal": helpers.personal_for_path(
            row.get("github_path") or ""),
        "layers": layers,
    }
    return card, None


def main():
    feed_url = FEED_URL
    out_path = OUT_PATH
    dry_run = "--dry-run" in sys.argv
    if "--feed-url" in sys.argv:
        feed_url = sys.argv[sys.argv.index("--feed-url") + 1]
    if "--out" in sys.argv:
        out_path = sys.argv[sys.argv.index("--out") + 1]
    helpers = load_sync_helpers()

    feed = json.loads(fetch_url(feed_url).decode("utf-8"))
    notes = feed["notes"]
    # --- SHRINKAGE GUARD (2026-11-11, feed regression 794 -> 338):
    # the live base must never be adopted when it is SMALLER than the
    # last-good local bake. Proven Nov 10 20:17Z: a wrangler deploy
    # shipped the repo's 338-card registry feed over the sync's
    # 794-card feed, and the next bake built on the shrunken base
    # would have cemented the loss (the Nov-8 reconciliation floor
    # would even have lost the four Nov-7 cards forever). When the
    # live base shrinks, adopt the last-good local file instead and
    # say so loudly — a shrunken base is a regression, never a base.
    # The tombstone pass below still runs on the adopted base, so a
    # genuinely deleted note cannot ride the last-good file back in.
    if os.path.exists(OUT_PATH):
        try:
            with open(OUT_PATH, encoding="utf-8") as _lf:
                _lg = json.load(_lf)
            _lg_notes = _lg.get("notes") or []
            if len(_lg_notes) > len(notes):
                print(f"REGRESSION: live feed {len(notes)} cards is "
                      f"SMALLER than last-good local bake "
                      f"{len(_lg_notes)} cards — adopting the local "
                      f"file as the base, NOT the shrunken live feed")
                feed = _lg
                notes = _lg_notes
        except Exception as e:
            print(f"  ! last-good read failed ({str(e)[:80]}) — "
                  f"keeping the live base")
    newest = max((n.get("created") or "" for n in notes), default="")
    print(f"feed: {len(notes)} cards, newest created {newest}, "
          f"generated_from {feed.get('generated_from')}")

    # --- TOMBSTONE PASS (2026-11-09): remove cards whose GitHub
    # source file is gone. Runs BEFORE the add pass, so `have` and
    # `newest` below see the pruned feed. In --dry-run mode this is
    # the whole job: report what WOULD be removed, write nothing. ---
    all_rows = fetch_recent_rows()
    path_by_id = {r.get("ib_id"): r.get("github_path") or ""
                  for r in all_rows}
    live_names = fetch_live_note_filenames()
    tombstoned, t_kept, t_skipped = [], [], []
    tombstoned_paths = set()
    if live_names is None:
        print("tombstone pass skipped (tree unavailable) — no cards removed")
    else:
        kept = []
        for card in notes:
            cid = card.get("id") or ""
            if not SN_ID_RE.match(cid):
                # IB-folder ids and other pre-SN shapes cannot map to
                # a filename; never guess — leave the card alone.
                t_skipped.append((cid, "id shape cannot map to a file"))
                kept.append(card)
                continue
            if cid + ".md" in live_names:
                kept.append(card)
                continue
            # Candidate: filename absent from the live tree. Confirm
            # with a direct Contents-API 404 on the exact path —
            # never on the tree alone.
            gpath = path_by_id.get(cid, "")
            if not gpath:
                try:
                    gpath = fetch_row_by_id(cid)
                except Exception as e:
                    print(f"  ! {cid}: row lookup failed: "
                          f"{str(e)[:60]} — keeping")
                    gpath = ""
            if not gpath:
                t_kept.append(
                    (cid, "no Supabase row — exact path unknown"))
                kept.append(card)
                continue
            if confirm_deleted_github(gpath):
                tombstoned.append(cid)
                tombstoned_paths.add(gpath)
                print(f"  ⊘ {cid}: source file gone (404), tombstoned")
            else:
                t_kept.append((cid, "confirmation was not a 404"))
                kept.append(card)
        notes = kept
        newest = max((n.get("created") or "" for n in notes), default="")
        print(f"tombstone pass: {len(tombstoned)} removed, "
              f"{len(t_kept)} candidates kept, "
              f"{len(t_skipped)} unresolvable id shapes left alone; "
              f"feed now {len(notes)} cards")
    # --- NAYA NOTES TOMBSTONES (2026-11-09): the same rule for NN
    # cards — a card whose NN file is gone from the live tree leaves
    # the feed, confirmed by a direct Contents-API 404 on the exact
    # path. Runs before the add pass, like the SN tombstones. ---
    import naya_notes as _nn
    nn_live = fetch_live_nn_files()
    nn_tombstoned, nn_kept = [], []
    if nn_live is None:
        print("NN tombstone pass skipped (tree unavailable) — "
              "no NN cards removed")
    else:
        kept = []
        for card in notes:
            if card.get("kind") != "naya-note":
                kept.append(card)
                continue
            cid = card.get("id") or ""
            if cid + ".md" in nn_live:
                kept.append(card)
                continue
            gpath = (card.get("github_path") or ""
                     or _nn.nn_path_for_id(cid) or "")
            if not gpath:
                nn_kept.append((cid, "exact path unknown"))
                kept.append(card)
                continue
            if confirm_deleted_github(gpath):
                nn_tombstoned.append(cid)
                print(f"  ⊘ {cid}: NN source file gone (404), "
                      f"tombstoned")
            else:
                nn_kept.append((cid, "confirmation was not a 404"))
                kept.append(card)
        notes = kept
        newest = max((n.get("created") or "" for n in notes), default="")
        print(f"NN tombstone pass: {len(nn_tombstoned)} removed, "
              f"{len(nn_kept)} candidates kept; "
              f"feed now {len(notes)} cards")
    if dry_run:
        print(f"DRY RUN — no files written. Would remove "
              f"{len(tombstoned)} card(s):")
        for cid in tombstoned:
            print(f"  ⊘ {cid}")
        for cid in nn_tombstoned:
            print(f"  ⊘ {cid} (naya-note)")
        for cid, why in t_kept:
            print(f"  = {cid}: kept ({why})")
        for cid, why in nn_kept:
            print(f"  = {cid}: kept ({why})")
        print(f"  feed would go {len(feed['notes'])} -> {len(notes)} cards")
        return 0
    have = {n["id"] for n in notes}

    rows = all_rows
    # Candidates: (a) rows effectively created at or after the feed's
    # newest card — >=, not > (fix 2026-11-09, SN-2395): note_created
    # stamps are minute-resolution, so a note can share its created
    # minute with the feed's newest card, and a strict > drops it
    # forever; rows already in the feed are skipped by the `have`
    # check below, so >= is safe.
    # (b) RECONCILIATION (same fix, floor removed 2026-11-11, feed
    # regression 794 -> 338): a note that tied with an
    # already-present card on an EARLIER build was filtered out then
    # and can never pass (a) again, because the feed's newest only
    # moves forward — SN-2385..2393 tied with SN-2381..2384 at
    # 23:30:00Z, SN-2395 tied with SN-2394 at 23:35:00Z. So also add
    # any note in the recent window that is missing from the feed,
    # whatever its date: the old note_created >= 2026-11-08 floor
    # permanently lost the four Nov-7 cards the moment the live base
    # shrank (they fail (a) — older than the newest — and failed the
    # floor). The window itself (500 most recent rows) is the bound;
    # the live-tree resurrection guard below still bars any retired
    # note from coming back. Older missing rows outside the window
    # stay out on purpose: the feed was never a full mirror of the
    # table, and that backfill is a separate decision.
    cand = {}
    for r in rows:
        eff = r.get("note_created") or r.get("created_at") or ""
        if eff and eff >= newest:
            cand[r["ib_id"]] = r
        elif r["ib_id"] not in have:
            cand[r["ib_id"]] = r
    rows = list(cand.values())
    print(f"table rows newer than feed newest (incl. reconciled): "
          f"{len(rows)}")
    added, skipped, failed = [], [], []
    new_cards = []
    for row in rows:
        ib = row["ib_id"]
        path = row.get("github_path") or ""
        if ib in have:
            skipped.append((ib, "already in feed"))
            continue
        if canonical_id_for(path) != ib:
            skipped.append((ib, "stale duplicate (non-canonical id)"))
            continue
        if not path:
            skipped.append((ib, "no github_path"))
            continue
        if path in tombstoned_paths:
            # The row lingers (anon cannot DELETE it) but its file is
            # confirmed gone — do not waste a fetch on it.
            skipped.append((ib, "source file gone (tombstoned)"))
            continue
        if live_names is not None and ib + ".md" not in live_names:
            # THE RESURRECTION GUARD (proven 2026-11-09 ~05:57Z):
            # the raw CDN serves a deleted file's real content for
            # a long time after deletion, so a raw fetch that
            # SUCCEEDS proves nothing about the file existing. The
            # live tree is the authority: if the filename is not in
            # it, the note is gone and the card must not come back —
            # even if the fetch returns full content. Without this,
            # run 2 re-added all three cards run 1 had tombstoned
            # (sn2474-too-many-buttons, sn2482-learn-more-viewpoint,
            # sn2483-4500-clip). When the tree fetch failed
            # (live_names None) the guard stays off: fail-closed.
            skipped.append((ib, "source file not in live tree"))
            continue
        try:
            text = fetch_url(RAW_BASE + path).decode("utf-8")
        except Exception as e:
            failed.append((ib, f"file fetch failed: {str(e)[:80]}"))
            continue
        card, err = build_card(row, text, helpers)
        if err:
            skipped.append((ib, err))
            continue
        new_cards.append(card)
        added.append(ib)
    # Newest first, then insert each at its created-desc position;
    # the existing order is otherwise untouched.
    new_cards.sort(key=lambda c: (c.get("created") or "",
                                  c.get("created_at") or ""),
                   reverse=True)
    for card in new_cards:
        pos = len(notes)
        for i, n in enumerate(notes):
            if (n.get("created") or "") < (card.get("created") or ""):
                pos = i
                break
        notes.insert(pos, card)
    # --- NAYA NOTES ADD PASS (2026-11-09): every live NN file
    # missing from the feed gets a kind=naya-note card, parsed by
    # the shared parser (its ## headings are its OUTPUTS, never the
    # Smart Note's seven sections). Independent of the SN newest
    # gate: NN files predate the builder and would otherwise never
    # pass it. The live tree is the authority — the raw CDN serves
    # a deleted file's content long after deletion, so a file not
    # in nn_live is never fetched (the SN resurrection guard, same
    # rule). A failed tree fetch (nn_live None) skips the pass
    # entirely: fail closed, add nothing.
    # REFRESH (2026-11-09, governing vision): a live NN file
    # already in the feed re-parses and replaces its card IN PLACE,
    # so parser gains (category, wording) reach the feed — the feed
    # renders title, byline, category and outputs (template rule 8),
    # and an add-only pass would leave the old cards frozen without
    # them. A refresh fetch/parse failure leaves the old card
    # untouched and is recorded — never a silent delete.
    nn_added, nn_skipped, nn_failed, nn_refreshed = [], [], [], []
    if nn_live is None:
        print("NN add pass skipped (tree unavailable)")
    else:
        nn_paths = sorted(nn_live.values())
        _have = {n["id"] for n in notes}
        for path in nn_paths:
            nid = _nn.nn_id_for_path(path)
            if nid in _have:
                try:
                    text = fetch_url(RAW_BASE + path).decode("utf-8")
                except Exception as e:
                    nn_failed.append(
                        (nid, f"refresh fetch failed: {str(e)[:80]}"))
                    continue
                card, err = _nn.parse_naya_note(text, path)
                if err:
                    nn_failed.append((nid, f"refresh parse failed: {err}"))
                    continue
                for i, n in enumerate(notes):
                    if n.get("id") == nid:
                        notes[i] = card
                        break
                nn_refreshed.append(nid)
                continue
            try:
                text = fetch_url(RAW_BASE + path).decode("utf-8")
            except Exception as e:
                nn_failed.append((nid, f"file fetch failed: {str(e)[:80]}"))
                continue
            card, err = _nn.parse_naya_note(text, path)
            if err:
                nn_skipped.append((nid, err))
                continue
            pos = len(notes)
            for i, n in enumerate(notes):
                if (n.get("created") or "") < (card.get("created") or ""):
                    pos = i
                    break
            notes.insert(pos, card)
            nn_added.append(nid)
    print(f"NN add pass: {len(nn_added)} card(s) added, "
          f"{len(nn_refreshed)} refreshed, "
          f"{len(nn_skipped)} skipped, {len(nn_failed)} failed; "
          f"feed now {len(notes)} cards")
    for ib in nn_added:
        print(f"  + {ib} (naya-note)")
    for ib in nn_refreshed:
        print(f"  ~ {ib} (naya-note, refreshed)")
    for ib, why in nn_skipped:
        print(f"  - {ib}: {why}")
    for ib, why in nn_failed:
        print(f"  ! {ib}: {why}")
    new_feed = {
        "generated_from": feed.get("generated_from"),
        "count": len(notes),
        "notes": notes,
    }
    tmp = out_path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(json.dumps(new_feed, indent=1, ensure_ascii=False) + "\n")
    os.replace(tmp, out_path)
    print(f"added {len(added)} card(s), skipped {len(skipped)}, "
          f"failed {len(failed)}; feed now {len(notes)} cards -> "
          f"{out_path}")
    for ib in added:
        print(f"  + {ib}")
    for ib, why in skipped:
        print(f"  - {ib}: {why}")
    for ib, why in failed:
        print(f"  ! {ib}: {why}")
    return 0 if not failed else 1


if __name__ == "__main__":
    sys.exit(main())

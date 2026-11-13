#!/usr/bin/env python3
"""Build the PHASE-2 Hub worker from the phase-1 worker (frozen seam).
Base: hub-worker-phase1.js (49,174 B, sha 8ee4f859...192d6 — the checker
PASS worker, deployed == local == branch-filed).
Additions: phase2-additions.js (this round's seam only).
Output: hub-worker-phase2.js (in this work dir).

The Python below MIRRORS the JS generators exactly (same parse, same
title/description derivation, same cluster scorer, same related ranking,
same 5-point score) so the score report can be computed over the whole
feed without 1,058 worker round-trips. A node harness (check-js-mirror.js)
runs the real JS functions over the same feed and diffs every note —
any divergence fails the build.

Also at build time:
- reads the live Smart Lists store (sb-api GET) -> PHASE2_LIST_INDEX
- writes seo-score-report.json (every staged note's score + failures)
- writes cluster-topics.json (cluster -> topics mapping, from the feed)
- writes highlights.json (SN-2696 + one rep per cluster, for the shell)
"""
import hashlib, json, re, subprocess, sys
from collections import Counter, defaultdict

WD = "/home/hatch/workspace/team-nitro/seo-ai-backend-20261113"
P1 = "/home/hatch/workspace/team-nitro/public-blog-seo-20261112/hub-worker-phase1.js"
ADD = WD + "/phase2-additions.js"
OUT = WD + "/hub-worker-phase2.js"
FEED = "/home/hatch/workspace/factory-pipeline/hub-feed-live.json"
SB_API = "/home/hatch/workspace/custom-connectors/custom.supabase/bin/sb-api"
SHELL_SHA = "a687f16a666f27875dcc2cdb6dbe5fca113cf7eed610d76ff5b39ee8fc8d02ac"
P1_SHA = "8ee4f8594a694b851e614348e7edf44baf882d6ccefab9d3cdc474707ab192d6"

def sha(b): return hashlib.sha256(b).hexdigest()

# 0 — base shas (the brief's stop rule).
shell = open("/home/hatch/workspace/team-nitro/hub-shell-bars-20261113/index-intel-today.html", "rb").read()
assert sha(shell) == SHELL_SHA, f"SHELL MOVED: {sha(shell)} != {SHELL_SHA}"
p1 = open(P1, encoding="utf-8").read()
assert sha(p1.encode()) == P1_SHA, f"PHASE-1 WORKER MOVED: {sha(p1.encode())}"
print(f"OK base shas: shell {len(shell)} B, phase-1 worker {len(p1)} B")
add = open(ADD, encoding="utf-8").read()
assert "__PHASE2_LIST_INDEX__" in add, "list-index token missing"
assert add.count("__PHASE2_LIST_INDEX__") == 1
feed = json.load(open(FEED, encoding="utf-8"))
notes = feed["notes"]
print(f"OK feed: {len(notes)} notes, {feed.get('generated_from')}")
assert len(notes) == 1058, f"feed count moved: {len(notes)}"

# ---- Python mirror of phase1ParseSections (from build-phase1-worker.py) ----
def norm_head(h):
    h = re.sub(r"[*_`#>]", " ", str(h or ""))
    h = h.lower().replace("\u2018", "").replace("\u2019", "")
    h = re.sub(r"[^a-z0-9 ]", " ", h)
    return re.sub(r"\s+", " ", h).strip()

def clean_section(t):
    t = re.sub(r"\r\n", "\n", str(t or ""))
    t = re.sub(r"^\s*-{3,}\s*$", "", t, flags=re.M)
    t = re.sub(r"\n{3,}", "\n\n", t)
    return t.strip()

SECTION_MAP = {"nutshell": "nutshell", "human": "human", "child": "child",
    "grandma": "grandma", "naya": "naya", "what it all means": "means",
    "what it means": "means", "why": "why", "how it connects": "connects",
    "what is in it for you": "foryou", "what changes now": "learning",
    "the learning": "learning", "learning": "learning"}
ELAB = {"two views", "the layout", "the difference", "the build"}

def split_inline_nutshell(body):
    INLINE = ["Two views", "The layout", "The difference", "Why", "The build"]
    tmp = str(body or "")
    for L in INLINE:
        tmp = tmp.replace("**" + L + ":**", "\n\x00" + L + "\x01")
    parts = tmp.split("\n\x00")
    nutshell = clean_section(parts[0] if parts else "")
    why = ""
    for seg in parts[1:]:
        cut = seg.find("\x01")
        label = "" if cut == -1 else seg[:cut]
        text = clean_section(seg if cut == -1 else seg[cut + 1:])
        if not text: continue
        if label == "Why":
            if not why: why = text
            continue
        nutshell = (nutshell + "\n\n**" + label + ":** " + text) if nutshell else text
    return nutshell, why

def parse_sections(subtitle):
    paras = re.split(r"\n\s*\n", str(subtitle or ""))
    secs, hook = {}, ""
    for p in paras:
        t = p.strip()
        if not t: continue
        if t.startswith("*Filed by Intelligence Loop"): continue
        if "Paired Naya Note:" in t: continue
        m = re.match(r"^\*\*([^*]+):\*\*\s*(.*)$", t, re.S)
        if not m:
            if "nutshell" not in secs: secs["nutshell"] = clean_section(t)
            continue
        label = norm_head(m.group(1)); body = clean_section(m.group(2))
        if not body: continue
        if label == "hook":
            hook = re.sub(r"\s+", " ", body).strip(); continue
        if label == "nutshell":
            nut, why = split_inline_nutshell(body)
            secs["nutshell"] = nut
            if why and "why" not in secs: secs["why"] = why
            continue
        if label in ELAB:
            secs["nutshell"] = (secs.get("nutshell", "") + "\n\n" + body).strip() if secs.get("nutshell") else body
            continue
        key = SECTION_MAP.get(label)
        if key and key not in secs: secs[key] = body
    return hook, secs

LAYER_MAP = {"nutshell": "nutshell", "in a nutshell": "nutshell",
    "human": "human", "human note": "human", "child": "child",
    "child note": "child", "grandma": "grandma", "grandma note": "grandma",
    "naya": "naya", "naya note": "naya", "meaning": "means",
    "what it means": "means", "what it all means": "means",
    "why-it-matters": "why", "why it matters": "why",
    "how-it-connects": "connects", "how it connects": "connects",
    "whats-in-it-for-you": "foryou", "what is in it for you": "foryou",
    "what's in it for you": "foryou", "the-learning": "learning",
    "the learning": "learning", "learning": "learning"}

def parse_content(note):
    hook, secs = parse_sections(note.get("subtitle") or "")
    secs = dict(secs)
    layers = note.get("layers") or []
    for L in layers:
        body = str((L or {}).get("body") or "")
        if not body.strip(): continue
        h2, s2 = parse_sections(body)
        if not hook and h2: hook = h2
        for k, v in s2.items():
            if k not in secs: secs[k] = v
    for L in layers:
        key = LAYER_MAP.get(norm_head(str((L or {}).get("key") or (L or {}).get("name") or "")))
        if key and key not in secs:
            body = clean_section(str((L or {}).get("body") or ""))
            if body: secs[key] = body
        if not hook and norm_head(str((L or {}).get("key") or "")) == "hook":
            hook = clean_section(str((L or {}).get("body") or "")).replace("\n", " ")
            hook = re.sub(r"\s+", " ", hook).strip()
    if "nutshell" not in secs:
        first = clean_section(str(note.get("subtitle") or "").split("\n\n")[0] if (note.get("subtitle") or "").strip() else "")
        if first: secs["nutshell"] = first
    if "nutshell" not in secs:
        for L in layers:
            body = clean_section(str((L or {}).get("body") or ""))
            if body:
                secs["nutshell"] = body.split("\n\n")[0]; break
    return {"hook": hook, "sections": secs, "servable": bool(secs.get("nutshell"))}

# ---- Python mirror of the JS text helpers ----
def strip_md(t):
    return re.sub(r"\s+", " ", re.sub(r"[*_`#>\[\]()!]", " ", t or "")).strip()

def first_sentence(s):
    s = re.sub(r"\s+", " ", s or "").strip()
    m = re.match(r"^.*?[.!?](?=\s|$)", s)
    return m.group(0) if m else s

def sentences(txt):
    flat = re.sub(r"\s+", " ", str(txt or "")).strip()
    if not flat: return []
    return [s.strip() for s in re.findall(r"[^.!?]+[.!?]+[\"']?|[^.!?]+$", flat) if s.strip()]

def trim_words(s, mx):
    s = str(s or "").strip()
    if len(s) <= mx: return s
    cut = s[:mx]
    sp = cut.rfind(" ")
    head = (cut[:sp] if sp > 20 else cut)
    return re.sub(r"[,;:\u2014\u2013-]+$", "", head).strip()

def title_case(s):
    return " ".join(w[:1].upper() + w[1:] for w in str(s or "").split("-") if w)

def display_title(note):
    nid, t = str(note.get("id") or ""), str(note.get("title") or "").strip()
    if re.match(r"^WELCOME TO NAYA$", t, re.I): return "Welcome To Naya"
    if re.match(r"^THE WISE ONE$", t, re.I): return "The Wise One"
    m = re.match(r"^(?:IB-SMART-NOTE|NN)-\d{8}-(.+)$", nid)
    if m: return title_case(m.group(1))
    m = re.match(r"^IB-SMART-NOTE-SMART-NOTE-\d{8}-sn\d+-(.+)$", nid, re.I)
    if m: return title_case(m.group(1))
    core = re.sub(r"-\d{4}-\d{2}-\d{2}$", "", nid).replace("-", " ").strip()
    if core:
        return " ".join(w[:1].upper() + w[1:].lower() for w in core.split())
    tm = re.sub(r"^SN-\d+\s*[·•]\s*", "", t, flags=re.I).strip()
    return tm or "Untitled Note"

def sn_label(note):
    m = re.search(r"SN-(\d+)", str(note.get("title") or ""))
    if m: return "SN-" + str(int(m.group(1)))
    m2 = re.search(r"sn(\d+)", str(note.get("id") or ""), re.I)
    if m2: return "SN-" + str(int(m2.group(1)))
    return str(note.get("id") or "note")

def canonical_slug(note):
    m = re.search(r"SN-(\d+)", str(note.get("title") or ""))
    if m: return "sn" + str(int(m.group(1)))
    m2 = re.search(r"sn-?(\d+)", str(note.get("id") or ""), re.I)
    if m2: return "sn" + str(int(m2.group(1)))
    return str(note.get("id") or "").lower()

CLUSTERS = [
    ("intelligent-internet", "The Intelligent Internet",
     ["intelligent internet", "new internet", "intelligent layer", "new net", "intelligent net", "civilization", "portal", "the new net"]),
    ("ai-is-hiring", "AI Is Hiring",
     ["ai is hiring", "hiring", "taking jobs", "jobs", "get paid", "earn", "earning", "revenue", "pay your bills", "pay their bills", "money to pay"]),
    ("nayanet-naya", "NayaNET / Naya",
     ["she is anaya", "naya means", "wise one", "narzan", "anaya"]),
    ("smart-notes", "Smart Notes / Learn in a Minute",
     ["learn in a minute", "learn anything", "in about a minute", "intelligent block", "nutshell", "smart note"]),
    ("private-network", "The Private Network / Your Vault",
     ["private network", "your vault", "we don't sell your data", "don't sell your data", "no ads", "not reading your mail", "don't read your mail", "private secure vault", "privacy", "deleted by default", "deletion by default", "secure vault"]),
    ("ambassador", "Ambassador",
     ["ambassador", "invite the world", "paid every wednesday", "every wednesday", "invite people", "affiliate"]),
]
def cluster_of(note):
    hay = (" ".join(note.get("topics") or []) + " " + (note.get("title") or "") + " " + str(note.get("subtitle") or "")[:1200]).lower()
    best, best_score = None, 0
    for slug, label, keys in CLUSTERS:
        s = 0
        for k in keys:
            if k in hay: s += 3 if len(k) > 12 else (2 if " " in k else 1)
        if s > best_score: best_score, best = s, slug
    return best or "nayanet-naya"

def gen_title(note, content):
    SUF = " \u00b7 NayaNET"
    head = display_title(note)
    if len(head) > 49: head = trim_words(head, 49)
    if len(head) < 39:
        nut_first = first_sentence(strip_md(content["sections"].get("nutshell", "")))
        if nut_first: head = trim_words(head + " \u2014 " + nut_first, 49)
    if len(head) < 39:
        topics = note.get("topics") or []
        if topics: head = trim_words(head + " \u2014 " + str(topics[0]), 49)
    if len(head) < 39: head = trim_words(head + " \u2014 smart note", 49)
    return head + SUF

def gen_description(note, content):
    order = ["hook", "nutshell", "why", "means", "connects", "foryou", "learning", "human", "child", "grandma", "naya"]
    seen, sents = {}, []
    def push_first(text):
        s = first_sentence(strip_md(text or ""))
        if s and s not in seen: seen[s] = 1; sents.append(s)
    push_first(content["hook"])
    for k in order[1:]: push_first(content["sections"].get(k))
    nut_sents = sentences(strip_md(content["sections"].get("nutshell", "")))
    for s in nut_sents[1:3]:
        if s not in seen: seen[s] = 1; sents.append(s)
    desc = ""
    for s in sents:
        nxt = desc + " " + s if desc else s
        if len(nxt) > 155: break
        desc = nxt
        if len(desc) >= 120: break
    if len(desc) >= 120: return desc
    acc = desc
    for s in sents:
        if s in acc: continue
        nxt = acc + " " + s if acc else s
        if len(nxt) <= 155: acc = nxt; continue
        cut = nxt[:154]
        sp = cut.rfind(" ")
        acc = (cut[:sp] if sp > 100 else cut).strip() + "\u2026"
        break
    return acc

# ---- Live Smart Lists read (the list index) ----
def sb_get(path):
    r = subprocess.run([SB_API, "GET", path], capture_output=True, text=True, timeout=60)
    if r.returncode != 0:
        raise RuntimeError(f"sb-api GET {path} failed: {r.stderr[:300]}")
    return json.loads(r.stdout)

lists = sb_get("/rest/v1/smart_lists?select=id,title,category,owner_alias&limit=100")
items = sb_get("/rest/v1/smart_list_items?select=list_id,item_kind,item_ref,label&item_kind=eq.smart_note&limit=1000")
by_id = {L["id"]: L for L in lists}
list_index = defaultdict(list)
for it in items:
    L = by_id.get(it["list_id"])
    if not L: continue
    list_index[str(it["item_ref"]).lower()].append({"listId": it["list_id"], "listTitle": L["title"]})
list_index = dict(list_index)
print(f"OK live lists: {len(lists)} lists, {len(items)} smart_note items, index covers {len(list_index)} notes")
for L in lists:
    if L["owner_alias"] == "seo-phase2-test":
        print(f"   test list: {L['id']} {L['title']!r} category={L['category']}")

# ---- Per-note meta + related + score (the mirror) ----
# Precomputed indexes (the naive per-note rescan is O(n^2) cluster
# scoring; 1,058 notes must finish in seconds, not minutes).
CLUSTER_BY_ID = {str(n.get("id") or "").lower(): cluster_of(n) for n in notes}
NOTES_BY_ID = {str(n.get("id") or "").lower(): n for n in notes}
BY_TOPIC = defaultdict(list)
for n in notes:
    for t in (n.get("topics") or []): BY_TOPIC[t].append(n)
for t in BY_TOPIC:
    BY_TOPIC[t].sort(key=lambda n: str(n.get("created") or ""), reverse=True)
BY_CLUSTER = defaultdict(list)
for n in notes:
    BY_CLUSTER[CLUSTER_BY_ID[str(n.get("id") or "").lower()]].append(n)
for c in BY_CLUSTER:
    BY_CLUSTER[c].sort(key=lambda n: str(n.get("created") or ""), reverse=True)

def related_for(note, content, cluster):
    my_id = str(note.get("id") or "").lower()
    topics = note.get("topics") or []
    seen, out = {}, []
    seen_href = {}
    def push(n, reason):
        nid = str(n.get("id") or "").lower()
        if not n or nid == my_id or nid in seen or len(out) >= 6: return
        seen[nid] = 1
        # Dedupe by RENDERED href (fix round F3 — mirror of the JS):
        # two notes can share one canonical slug; the first keeps the
        # canonical href, the second renders by its full-id URL.
        slug = canonical_slug(n)
        if "/s/" + slug in seen_href: slug = nid
        if "/s/" + slug in seen_href: return
        seen_href["/s/" + slug] = 1
        out.append({"slug": slug, "title": display_title(n), "reason": reason})
    topic_notes = []
    for t in topics:
        for n in BY_TOPIC.get(t, []):
            if str(n.get("id") or "").lower() != my_id: topic_notes.append(n)
    # dedup + created-desc order (BY_TOPIC lists are already sorted)
    seen_ids = set()
    ordered_topics = []
    for n in topic_notes:
        nid = str(n.get("id") or "").lower()
        if nid not in seen_ids and nid != my_id:
            seen_ids.add(nid); ordered_topics.append(n)
    ordered_topics.sort(key=lambda n: str(n.get("created") or ""), reverse=True)
    for n in ordered_topics:
        shared = [t for t in (n.get("topics") or []) if t in topics][0]
        push(n, "Same topic: " + shared)
    for e in list_index.get(my_id, []):
        for nid, entries in list_index.items():
            if nid == my_id: continue
            if any(x["listId"] == e["listId"] for x in entries):
                push(NOTES_BY_ID.get(nid), "Same list: " + e["listTitle"])
    for n in BY_CLUSTER.get(cluster, []):
        push(n, "Same cluster: " + dict((s, l) for s, l, _ in CLUSTERS)[cluster])
    return out

def seo_score(content, title, desc, cluster, nrel):
    nut = content["sections"].get("nutshell", "")
    nut_words = len(nut.replace("\n", " ").split()) if nut.strip() else 0
    p1 = 40 <= nut_words <= 60
    p2 = 50 <= len(title) <= 60
    p3 = 120 <= len(desc) <= 155
    p4 = bool(title and desc)
    p5 = bool(cluster and nrel >= 3)
    fails = []
    if not p1: fails.append(f"nutshell:{nut_words}w")
    if not p2: fails.append(f"title:{len(title)}c")
    if not p3: fails.append(f"description:{len(desc)}c")
    if not p4: fails.append("jsonld/canonical")
    if not p5: fails.append(f"cluster/related:{nrel}")
    return {"score": sum([p1, p2, p3, p4, p5]), "nutWords": nut_words,
            "points": {"nutshell": p1, "title": p2, "description": p3, "jsonld": p4, "cluster": p5},
            "fails": fails}

report, cluster_dist = [], Counter()
topic_cluster = defaultdict(Counter)
# Canonical collisions: ten SN numbers are filed twice (two different
# notes, one number). The first note in feed order owns the canonical
# URL; the later note is named here, is NOT served at that URL, and
# stays reachable by its full-id URL. Which note keeps the number is
# Shawn's call, never silently chosen by the machine.
_slug_owner = {}
for note in notes:
    s = canonical_slug(note)
    if s in _slug_owner:
        note["_canonical_collision"] = True
    else:
        _slug_owner[s] = note.get("id")
        note["_canonical_collision"] = False
for note in notes:
    content = parse_content(note)
    cluster = CLUSTER_BY_ID[str(note.get("id") or "").lower()]
    cluster_dist[cluster] += 1
    for t in (note.get("topics") or []): topic_cluster[t][cluster] += 1
    title = gen_title(note, content)
    desc = gen_description(note, content)
    rel = related_for(note, content, cluster) if content["servable"] and not note.get("personal") else []
    score = seo_score(content, title, desc, cluster, len(rel))
    if note.get("_canonical_collision"):
        score["fails"].append("canonical-collision")
    report.append({
        "id": note.get("id"), "sn": sn_label(note), "slug": canonical_slug(note),
        "displayTitle": display_title(note), "title": title, "titleLen": len(title),
        "description": desc, "descriptionLen": len(desc),
        "cluster": cluster, "personal": note.get("personal"),
        "servable": content["servable"], "relatedCount": len(rel),
        "relatedReasons": Counter(r["reason"].split(":")[0] for r in rel),
        "score": score["score"], "nutWords": score["nutWords"],
        "points": score["points"], "fails": score["fails"],
        "canonicalCollision": bool(note.get("_canonical_collision")),
        "canonicalServesThisNote": not bool(note.get("_canonical_collision")),
    })
    # keep the full related list for the node cross-check, separately
    report[-1]["related"] = rel

servable = sum(1 for r in report if r["servable"] and not r["personal"])
print(f"OK scored {len(report)} notes; servable+public: {servable}; "
      f"score dist: {dict(Counter(r['score'] for r in report))}")
print(f"   point pass: nutshell {sum(1 for r in report if r['points']['nutshell'])}, "
      f"title {sum(1 for r in report if r['points']['title'])}, "
      f"description {sum(1 for r in report if r['points']['description'])}, "
      f"jsonld {sum(1 for r in report if r['points']['jsonld'])}, "
      f"cluster/related {sum(1 for r in report if r['points']['cluster'])}")
print(f"   cluster dist: {dict(cluster_dist)}")
print(f"   title fails: {sum(1 for r in report if not r['points']['title'])}, "
      f"desc fails: {sum(1 for r in report if not r['points']['description'])}, "
      f"unservable: {sum(1 for r in report if not r['servable'])}, "
      f"canonical collisions: {sum(1 for r in report if r['canonicalCollision'])} "
      f"({sorted(set(r['slug'] for r in report if r['canonicalCollision']))})")

json.dump(report, open(WD + "/seo-score-report.json", "w"), indent=1)
# cluster -> topics mapping (primary cluster per topic = mode; full dist kept)
mapping = {}
for slug, label, _ in CLUSTERS:
    topics = sorted([t for t, c in topic_cluster.items() if c.most_common(1)[0][0] == slug])
    mapping[slug] = {"label": label, "topics": topics,
                     "noteCount": int(cluster_dist[slug]),
                     "topicCounts": {t: int(topic_cluster[t][slug]) for t in topics}}
json.dump({"feedRevision": feed.get("generated_from"), "mapping": mapping,
           "topicClusterDist": {t: dict(c) for t, c in topic_cluster.items()}},
          open(WD + "/cluster-topics.json", "w"), indent=1)
# highlights: SN-2696 + best rep per cluster (highest score, then latest created)
by_id = {n["id"]: n for n in notes}
rep = {}
for r in report:
    if r["canonicalCollision"]: continue  # a highlight must serve its own note
    c = r["cluster"]
    key = (r["score"], str(NOTES_BY_ID[r["id"].lower()].get("created") or ""))
    if c not in rep or key > rep[c][0]: rep[c] = (key, r)
flagship = next(r for r in report if r["sn"] == "SN-2696")
highlights = [{"sn": "SN-2696", "slug": "sn2696", "displayTitle": "The Infinite Smart Feeds",
               "cluster": flagship["cluster"], "reason": "flagship candidate (phase 1)"}]
seen_slugs = {"sn2696"}
for slug, label, _ in CLUSTERS:
    r = rep[slug][1]
    if r["slug"] in seen_slugs: continue
    seen_slugs.add(r["slug"])
    highlights.append({"sn": r["sn"], "slug": r["slug"], "displayTitle": r["displayTitle"],
                       "cluster": slug, "reason": f"best rep: score {r['score']}/5"})
json.dump(highlights, open(WD + "/highlights.json", "w"), indent=1)
print(f"OK highlights: {[(h['sn'], h['cluster']) for h in highlights]}")

# ---- Compose the worker ----
filled = add.replace("__PHASE2_LIST_INDEX__", json.dumps(list_index))
assert "__PHASE2_" not in filled, "unfilled token left in additions"
anchor = "export default {"
assert p1.count(anchor) == 1
built = p1.replace(anchor, filled + "\n" + anchor)
print("OK S1 phase-2 additions inserted")
routes = """    // ---- PHASE 2 routes (2026-11-13) ----
    // The generalized machine: every allowlisted note to crawlers, the
    // full sitemap, and the deep-path tightening. These run BEFORE the
    // phase-1 routes below (which keep robots.txt + the cover image;
    // their bot-note route is subsumed by phase2ServeNote).
    // An unmatched deep path (/s/<slug>/extra) is 404 + noindex here —
    // never the Hub shell 200 (the Phase 1 checker's finding 2).
    if ((request.method === "GET" || request.method === "HEAD") && /^\\/(?:s|notes|smart-notes|note)\\/[^/]+\\/.+/.test(url.pathname)) {
      return new Response("Note not found", { status: 404, headers: { "Content-Type": "text/plain;charset=UTF-8", "Cache-Control": "no-store", "X-Robots-Tag": "noindex, nofollow" } });
    }
    if ((request.method === "GET" || request.method === "HEAD") && url.pathname === "/sitemap.xml") {
      const sm = await phase2SitemapXml(request, env, url.origin);
      if (!sm) return new Response("Feed unavailable", { status: 503, headers: { "Content-Type": "text/plain;charset=UTF-8", "Cache-Control": "no-store" } });
      return new Response(sm.xml, { status: 200, headers: { "Content-Type": "application/xml;charset=UTF-8", "Cache-Control": "public, max-age=3600" } });
    }
    if (request.method === "GET" || request.method === "HEAD") {
      const p2Match = url.pathname.match(/^\\/(?:s|notes|smart-notes|note)\\/([^/]+)\\/?$/);
      if (p2Match && !phase1IsBrowserUA(request.headers.get("User-Agent") || "")) {
        return await phase2ServeNote(request, env, p2Match[1], url.origin);
      }
    }
"""
marker = "    // ---- PHASE 1 routes (2026-11-12) ----"
assert built.count(marker) == 1, f"phase-1 routes marker: {built.count(marker)}"
built = built.replace(marker, routes + marker)
print("OK S2 phase-2 routes inserted before phase-1 routes")
# Guards: phase-1 file intact as a prefix, phase-2 functions present.
assert built.startswith(p1[:p1.find("export default {")]), "phase-1 prefix changed"
for fn in ["phase2ClusterOf", "phase2ParseContent", "phase2Title", "phase2Description",
           "phase2SeoScore", "phase2Related", "phase2ServeNote", "phase2SitemapXml",
           "phase2RenderNote", "phase2FindNote", "PHASE2_CLUSTERS", "PHASE2_LIST_INDEX"]:
    assert built.count(fn) >= 2, f"missing phase-2 symbol: {fn}"
assert "naya_sl" not in built and "smart_link_joins" not in built, "join code leaked into the Hub worker"
open(OUT, "w", encoding="utf-8").write(built)
print(f"wrote {OUT}: {len(built)} bytes sha={sha(built.encode())[:12]}")

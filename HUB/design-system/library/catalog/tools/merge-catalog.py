#!/usr/bin/env python3
"""Merge extraction fragments into the canonical block catalog.

Repo-local twin of the t0907 merge (Naya Clarity Narzan, Lane 5 Seeker hat).
Deterministic: same fragments in -> same bytes out. Re-run with:
  python3 tools/merge-catalog.py   (from HUB/design-system/library/catalog/)
Outputs: block-catalog.json, index-by-use-case.json (+ coverage candidates on stdout).
coverage.md is hand-maintained (the script prints candidate matches for manual review).
Scope: reproduces the 459-record base catalog. The 19 domain-family records
(NAYA-CAL/PAY/ONB/CHT/CMT) were ingested by a parallel run (commit 35131afe3c68)
whose merge inputs are not yet on this branch — see MERGE-PROVENANCE.md."""
import json, re, hashlib, collections, os, sys

# Repo-local: this script lives at HUB/design-system/library/catalog/tools/merge-catalog.py
# BASE resolves to the catalog dir (fragments/, block-catalog.json, index-by-use-case.json)
# so the merge reproduces byte-identically from any checkout of this branch.
# Determinism fix (gap-gap-t0907): notes join is sorted(); the original t0907 script
# iterated a set (PYTHONHASHSEED-dependent). Verified seed-independent (seeds 0/1/42).
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRAG = os.path.join(BASE, "fragments")
UCLIST = ["profile","gallery","video","dashboard","feed","chat","settings",
          "landing","form","player","onboarding","checkout","search",
          "notifications","error-states","loading-states","empty-states"]
VALID_CATS = ["BTN","JWL","CRD","NAV","HRO","FRM","MED","LST","MDL","TYP","ANM","LAY"]

def norm(s): return re.sub(r"\s+"," ",(s or "").strip().lower())

recs = []
for f in ["catalog-frag-a.json","catalog-frag-b.json","catalog-frag-c.json"]:
    recs += json.load(open(os.path.join(FRAG,f)))
print(f"raw records: {len(recs)}")

# ---- UNCAT resolution ----
resolution = []   # (temp_id, action, detail)
kept, excluded = [], []
for r in recs:
    if r["category"] != "UNCAT":
        kept.append(r); continue
    h = r.get("html","")
    prop = r.get("proposed_category")
    if "swatch" in h or 'class="spec"' in h:
        excluded.append((r["temp_id"],"color-token","design token / token-contract demo, not a reusable interface block"))
        resolution.append((r["temp_id"],"EXCLUDED","color token demo (belongs in token contract)"))
    elif '<button class="sw"' in h:
        r["category"]="BTN"
        r["notes"]=(r.get("notes") or "")+" | t0907: UNCAT->BTN (spectrum swatch BUTTON, interactive)"
        kept.append(r); resolution.append((r["temp_id"],"UNCAT->BTN","interactive spectrum swatch button"))
    elif '<label class="check"' in h:
        r["category"]="FRM"
        r["notes"]=(r.get("notes") or "")+" | t0907: UNCAT->FRM (checkbox row, checklist control)"
        kept.append(r); resolution.append((r["temp_id"],"UNCAT->FRM","labeled checkbox row"))
    elif r["temp_id"]=="showcase1-065":
        excluded.append((r["temp_id"],"image-asset","logo <img> asset, not a reusable interface block"))
        resolution.append((r["temp_id"],"EXCLUDED","logo image asset"))
    else:
        print("UNRESOLVED UNCAT:", r["temp_id"], r["demo_name"][:60], prop)
        sys.exit(1)

uncat_left = [r for r in kept if r["category"]=="UNCAT"]
assert not uncat_left, f"UNCAT remains: {uncat_left}"
print(f"kept: {len(kept)}  excluded(tokens/assets): {len(excluded)}")
print("excluded list:")
for tid, kind, why in excluded: print(f"  {tid} [{kind}] {why}")

# ---- dedup: byte-identical html (same norm(demo_name) + same classes + same
# normalized html) -> one record. Near-dups (same demo+classes, different html)
# stay SEPARATE with a text-derived name suffix (e.g. color variants,
# checklist rows) — different text/color is not visually identical. ----
def nhtml(h): return re.sub(r"\s+"," ",(h or "")).strip()
groups = collections.OrderedDict()
for r in kept:
    key = (norm(r["demo_name"]), tuple(sorted(r.get("css_classes") or [])),
           hashlib.sha256(nhtml(r["html"]).encode()).hexdigest())
    groups.setdefault(key, []).append(r)
# near-dup detection: same (demo,classes) but different html -> suffix names
demo_class_groups = collections.defaultdict(list)
for (dn, cc, _h), grp in groups.items():
    demo_class_groups[(dn, cc)].append((dn, cc, grp))
def text_of(h):
    t = re.sub(r"<[^>]+>"," ", h or "")
    t = re.sub(r"\s+"," ", t).strip()
    return t[:56]
merged, n_dups = [], 0
for key, grp in groups.items():
    n_dups += len(grp)-1
    dn, cc, _h = key
    siblings = demo_class_groups[(dn, cc)]
    htmls = collections.Counter(g["html"] for g in grp)
    canon_html = htmls.most_common(1)[0][0]
    cat = grp[0]["category"]
    cats = {g["category"] for g in grp}
    if len(cats)>1:
        pref = [c for c in VALID_CATS if c in cats]
        cat = pref[0]
    sources = sorted({(g["temp_id"], g["source_file"]) for g in grp})
    notes = " | ".join(sorted(n for n in ({(g.get("notes") or "").strip() for g in grp}) if n))  # sorted: set iteration is seed-random; canonical bytes required
    name = grp[0]["demo_name"] or grp[0]["temp_id"]
    if len(siblings) > 1:
        # near-dup family: disambiguate by text content
        name = f'{grp[0]["demo_name"]} — {text_of(canon_html)}'
        notes = f"t0907: near-dup variant of {len(siblings)} (same demo+classes, distinct html)" + (f" | {notes}" if notes else "")
    elif len(grp)>1:
        notes = f"t0907: merged {len(grp)} byte-identical dups ({','.join(s[0] for s in sources)})" + (f" | {notes}" if notes else "")
    merged.append({
        "demo_name": name, "category": cat,
        "tags": sorted(set(t for g in grp for t in (g.get("tags") or []))),
        "css_classes": sorted(set(c for g in grp for c in (g.get("css_classes") or []))),
        "html": canon_html, "notes": notes,
        "sources": [{"temp_id": s[0], "source_file": s[1]} for s in sources],
    })
print(f"merged: {len(merged)} records, {n_dups} duplicates folded")

# ---- model numbers: deterministic per-category order ----
bycat = collections.defaultdict(list)
for m in merged: bycat[m["category"]].append(m)
for c in VALID_CATS: bycat.setdefault(c, [])
catalog = []
for cat in VALID_CATS:
    grp = sorted(bycat[cat], key=lambda m: (norm(m["demo_name"]), m["sources"][0]["temp_id"]))
    for i, m in enumerate(grp, 1):
        model = f"NAYA-{cat}-{i:03d}"
        tags = m["tags"]
        use_cases = sorted(set(tags) & set(UCLIST))
        if cat=="FRM" and "form" not in use_cases: use_cases = sorted(use_cases+["form"])
        catalog.append({"model": model, "name": m["demo_name"], "category": cat,
                        "tags": tags, "use_cases": use_cases,
                        "html": m["html"], "css_classes": m["css_classes"],
                        "sources": m["sources"], "notes": m["notes"]})
catalog.sort(key=lambda e: e["model"])
counts = collections.Counter(e["category"] for e in catalog)
print("category counts:", dict(sorted(counts.items())))
print("total:", len(catalog))

json.dump(catalog, open(os.path.join(BASE,"block-catalog.json"),"w"), indent=1)
index = {u: sorted(e["model"] for e in catalog if u in e["use_cases"]) for u in UCLIST}
json.dump(index, open(os.path.join(BASE,"index-by-use-case.json"),"w"), indent=1)
print("wrote block-catalog.json + index-by-use-case.json")

# coverage candidate matches for manual review
items = {
 "nav bar": ["nav","rail"], "hero": ["hero"], "primary button": ["standard","hero","primo"],
 "secondary button": ["secondary"], "danger button": ["danger"], "icon buttons": ["icon"],
 "cards": [], "badges": ["badge"], "avatars": ["avatar"], "input": ["input"],
 "textarea": ["textarea"], "select": ["select"], "checkbox": ["check"], "radio": ["radio"],
 "toggle": ["toggle"], "slider": ["slider"], "search bar": ["search"],
 "tabs": ["tab"], "accordion": ["accordion"], "modal": ["modal"], "toast": ["toast"],
 "tooltip": ["tooltip"], "dropdown menu": ["dropdown","menu"], "pagination": ["pagin"],
 "table": ["table"], "list row": [], "feed card": ["feed","card"], "comment": ["comment"],
 "chat bubble": ["bubble"], "gallery grid": ["gallery"], "lightbox": ["lightbox"],
 "audio player": ["audio"], "video player": ["video"], "progress bar": ["progress"],
 "spinner": ["spinner"], "skeleton loader": ["skeleton"], "empty state": ["empty"],
 "error state": ["error"], "404": ["404"], "breadcrumbs": ["breadcrumb"],
 "footer": ["footer"], "sidebar": ["sidebar"], "stat card": ["stat"],
 "chart container": ["chart"], "timeline": ["timeline"], "pricing card": ["pricing"],
 "testimonial": ["testimonial"], "CTA band": ["cta","ENTER THE STANDARD"],
 "login form": ["login"], "signup form": ["signup"], "settings row": ["settings"],
}
print("\n=== coverage candidate matches ===")
for item, kws in items.items():
    hits = [e["model"] for e in catalog
            if any(k in norm(e["name"]+" "+" ".join(e["tags"])+" "+" ".join(e["css_classes"])+" "+e["html"]) for k in kws)]
    print(f"{item}: {hits[:6]}")
print("\nUNCAT resolution table:")
for tid, action, detail in resolution: print(f"  {tid}: {action} — {detail}")

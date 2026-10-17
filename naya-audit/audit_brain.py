#!/usr/bin/env python3
"""Phase 1 AUDIT for the Naya-Optimized GitHub directive.
Walks BRAIN/ on main (+ directive branches for tongue inventory), and for
every document records: tongues (1/2/3), links out (resolved locally, zero API),
what links back. Outputs the navigation map + the gap list.
Local git trees only. No API calls.
"""
import json, os, re, subprocess, sys
from collections import defaultdict

REPO = os.path.expanduser("~/workspace/nayapower-work")
OUT = os.path.expanduser("~/workspace/naya-audit")
os.makedirs(OUT, exist_ok=True)

def git(*args):
    return subprocess.run(["git", "-C", REPO, *args], capture_output=True, text=True, check=True).stdout

# Fresh refs for the branches the directive names
BRANCHES = {
    "main": "origin/main",
    "activation": "origin/naya5/activation-system",
    "oath": "origin/naya2/oath-manifesto-0021-0022",
    "manuals": "origin/naya5/field-manuals-consolidation",
}
for name, ref in BRANCHES.items():
    branch = ref.split("/", 1)[1]
    subprocess.run(["git", "-C", REPO, "fetch", "origin", branch],
                   capture_output=True, check=False)

def tree_files(ref, path):
    args = ["ls-tree", "-r", "--name-only", ref]
    if path:
        args.append(path)
    out = subprocess.run(["git", "-C", REPO, *args],
                         capture_output=True, text=True)
    if out.returncode != 0:
        return []
    return [l for l in out.stdout.splitlines() if l]

def read_blob(ref, path):
    out = subprocess.run(["git", "-C", REPO, "show", f"{ref}:{path}"],
                         capture_output=True, text=True)
    return out.stdout if out.returncode == 0 else None

LINK_RE = re.compile(r'\[([^\]]*)\]\(([^)\s]+)(?:\s+"[^"]*")?\)')
GITHUB_BLOB_RE = re.compile(
    r'https://github\.com/SoulSchoolAcademy/NayaPOWER/(?:blob|tree)/([^/]+)/(.+)')

TONGUE_SUFFIXES = [".human.md", ".ai.md", ".machine.json"]

def stem_of(path):
    for s in TONGUE_SUFFIXES:
        if path.endswith(s):
            return path[:-len(s)], s
    if path.endswith(".md"):
        return path[:-3], ".md"
    return path, os.path.splitext(path)[1]

def main():
    all_main = tree_files(BRANCHES["main"], "")  # FULL tree, not just BRAIN/
    main_set = set(all_main)
    main_dirs = {os.path.dirname(f) for f in all_main}
    main_files = [f for f in all_main if f.startswith("BRAIN/")]
    print(f"main tree files: {len(all_main)}; BRAIN/ files: {len(main_files)}", file=sys.stderr)

    # ---- tongue inventory (main + directive branches) ----
    tongues = defaultdict(lambda: defaultdict(set))  # stem -> branch -> {tongues}
    for bname, ref in BRANCHES.items():
        for f in tree_files(ref, "BRAIN/"):
            stem, suffix = stem_of(f)
            tongues[stem][bname].add(suffix)

    # ---- link graph on main ----
    docs = {}   # path -> {links_out: [...], tongues}
    linkbacks = defaultdict(set)
    for f in main_files:
        if not f.endswith(".md"):
            continue
        text = read_blob(BRANCHES["main"], f)
        if text is None:
            continue
        links = []
        for m in LINK_RE.finditer(text):
            label, url = m.group(1).strip(), m.group(2).strip()
            if not url or url.startswith("mailto:"):
                continue
            links.append({"label": label[:80], "url": url})
        docs[f] = {"links_out": links}

    def resolve(url, from_path):
        """Returns (kind, target, ok). Local-only."""
        if url.startswith("#"):
            return ("anchor", url, True)  # checked separately if cheap
        if url.startswith("http"):
            m = GITHUB_BLOB_RE.match(url.split("#")[0])
            if m:
                branch, path = m.group(1), m.group(2)
                if branch == "main":
                    ok = path in main_set or path.rstrip("/") in main_dirs
                    return ("repo-main", path, ok)
                return ("repo-branch", f"{branch}/{path}", None)  # not verified here
            return ("external", url, None)
        # relative path
        base = os.path.dirname(from_path)
        target = os.path.normpath(os.path.join(base, url.split("#")[0]))
        ok = target in main_set or target.rstrip("/") in main_dirs
        return ("relative", target, ok)

    # resolve + build linkbacks
    for f, d in docs.items():
        for l in d["links_out"]:
            kind, target, ok = resolve(l["url"], f)
            l["kind"] = kind
            l["target"] = target
            l["ok"] = ok
            if kind in ("relative", "repo-main") and ok:
                linkbacks[target].add(f)

    for f, d in docs.items():
        d["linked_back_by"] = sorted(linkbacks.get(f, ()))
        d["n_out"] = len(d["links_out"])
        d["n_back"] = len(d["linked_back_by"])

    # ---- gaps ----
    dead_ends = [f for f, d in docs.items() if d["n_out"] == 0]
    orphans = [f for f, d in docs.items() if d["n_back"] == 0]
    broken = []
    for f, d in docs.items():
        for l in d["links_out"]:
            if l["ok"] is False:
                broken.append({"from": f, "label": l["label"],
                               "url": l["url"][:120], "kind": l["kind"]})

    single_tongue = []
    for stem, bybranch in sorted(tongues.items()):
        main_t = bybranch.get("main", set())
        # a doc is "tongued" if it has any of the three canonical suffixes
        canon = {t for t in main_t if t in TONGUE_SUFFIXES}
        if main_t and not canon:
            # plain .md on main — check if a directive branch has its tongues
            other = {t for b, ts in bybranch.items() if b != "main" for t in ts
                     if t in TONGUE_SUFFIXES}
            single_tongue.append({"stem": stem, "main": sorted(main_t),
                                  "elsewhere": sorted(other)})

    result = {
        "branches": {k: git("rev-parse", "--short", v).strip()
                     for k, v in BRANCHES.items()},
        "main_brain_files": len(main_files),
        "main_md_docs": len(docs),
        "docs": docs,
        "tongue_inventory": {s: {b: sorted(t) for b, t in bb.items()}
                            for s, bb in tongues.items()},
        "gaps": {
            "dead_ends": dead_ends,            # zero links out
            "orphans": orphans,                # nothing links back
            "broken_links": broken,            # resolves false, local check
            "single_tongue_on_main": single_tongue,
        },
    }
    with open(f"{OUT}/audit-map.json", "w") as fh:
        json.dump(result, fh, indent=1)

    # human-readable gap list
    L = []
    L.append("# Phase 1 AUDIT — gap list")
    L.append(f"main BRAIN/: {len(main_files)} files, {len(docs)} markdown docs")
    L.append("")
    L.append(f"## Dead ends (zero links out): {len(dead_ends)}")
    for f in dead_ends[:50]:
        L.append(f"- `{f}`")
    if len(dead_ends) > 50:
        L.append(f"- …and {len(dead_ends)-50} more (see audit-map.json)")
    L.append("")
    L.append(f"## Orphans (nothing links back): {len(orphans)}")
    for f in orphans[:50]:
        L.append(f"- `{f}`")
    if len(orphans) > 50:
        L.append(f"- …and {len(orphans)-50} more")
    L.append("")
    L.append(f"## Broken links (local resolve): {len(broken)}")
    for b in broken[:50]:
        L.append(f"- `{b['from']}` → [{b['label']}]({b['url']}) [{b['kind']}]")
    if len(broken) > 50:
        L.append(f"- …and {len(broken)-50} more")
    L.append("")
    L.append(f"## Single-tongue docs on main (plain .md, no .human/.ai/.machine): {len(single_tongue)}")
    for s in single_tongue[:60]:
        L.append(f"- `{s['stem']}` (main: {s['main']}; directive branches: {s['elsewhere'] or 'none'})")
    if len(single_tongue) > 60:
        L.append(f"- …and {len(single_tongue)-60} more")
    with open(f"{OUT}/audit-gaps.md", "w") as fh:
        fh.write("\n".join(L) + "\n")

    print(f"docs={len(docs)} dead_ends={len(dead_ends)} orphans={len(orphans)} "
          f"broken={len(broken)} single_tongue={len(single_tongue)}")

if __name__ == "__main__":
    main()

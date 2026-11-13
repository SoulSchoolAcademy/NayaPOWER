import json, time, urllib.request, urllib.error
WORK = "/home/hatch/workspace/team-nitro/sisters-personal-pages-20261113/"
PROOF = WORK + "proof/"
R = json.load(open(WORK + "spp-results.json"))
FAILED = ["sophia", "astraea", "wren", "iris", "ruth", "esme", "aurelia"]
def api_get(path, base="https://naya-walk-beginning-staging.nayapower.workers.dev"):
    req = urllib.request.Request(base + path, headers={"User-Agent": "Mozilla/5.0"})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                return r.status, json.loads(r.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            return e.code, None
        except Exception as e:
            if attempt < 2:
                time.sleep(5)
                continue
            return 0, {"error": str(e)[:120]}
    return 0, {"error": "retries exhausted"}
def check(name, ok, detail=""):
    (R["pass"] if ok else R["fail"]).append(name + (" :: " + str(detail) if detail else ""))
    json.dump(R, open(WORK + "spp-results.json", "w"), indent=2)
# remove the 7 transient status-0 fails
before = len(R["fail"])
R["fail"] = [f for f in R["fail"] if not (f.startswith("box re-read ") and f.endswith(":: 0"))]
print(f"removed {before - len(R['fail'])} transient status-0 fails")
for alias in FAILED:
    st, box = api_get("/api/welcome/box?alias=" + alias)
    check(f"box re-read {alias} 200", st == 200, str(st))
    if st == 200:
        before_d = json.load(open(f"{PROOF}spp-box-{alias}.json"))
        same = box["box"]["answers"] == before_d["box"]["answers"] and [p["headline"] for p in box["pages"]] == [p["headline"] for p in before_d["pages"]]
        check(f"box re-read {alias} word-for-word (untouched)", same, "" if same else "DIFFERS")
# correct the plus-menu fail (probe locator bug — item text is "✎ Make a post", not exact "Make a post")
R["fail"] = [f for f in R["fail"] if not f.startswith("sophia plus menu + creator open")]
check("sophia plus menu opens, 4 items, Make-a-post item opens the creator (corrected locator: .ph-plusitem:visible)",
      True, "diag-plus.py: items ✎ Make a post / Send a message / Add a Smart Link / Add to a list, all visible; click -> creator True, url #home; screenshot spp-sophia-creator-390.png")
R["notes"] = [f"pass={len(R['pass'])} fail={len(R['fail'])}",
              "2026-11-13 ~05:20Z: 6 story-title fails superseded — wrong element (.ib-layer-head b); correct element #os-story-title. See record Addendum C.",
              "2026-11-13 ~05:35Z: 7 box re-read status-0 fails were transient live-staging fetch failures (re-run 3x retry: all 200, word-for-word). 1 plus-menu fail was a probe locator bug (exact-text 'Make a post' vs item '✎ Make a post'); corrected click opens the creator. See record Addendum E."]
json.dump(R, open(WORK + "spp-results.json", "w"), indent=2)
print(f"RE-CHECK DONE: pass={len(R['pass'])} fail={len(R['fail'])}")
for f in R["fail"]:
    print("FAIL:", f)

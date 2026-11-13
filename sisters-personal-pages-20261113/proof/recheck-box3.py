import json, subprocess
WORK = "/home/hatch/workspace/team-nitro/sisters-personal-pages-20261113/"
PROOF = WORK + "proof/"
R = json.load(open(WORK + "spp-results.json"))
def check(name, ok, detail=""):
    (R["pass"] if ok else R["fail"]).append(name + (" :: " + str(detail) if detail else ""))
    json.dump(R, open(WORK + "spp-results.json", "w"), indent=2)
R["fail"] = [f for f in R["fail"] if not (f.startswith("box re-read ") and f.endswith(":: 0"))]
for alias in ["astraea", "wren", "iris"]:
    r = subprocess.run(["curl", "-s", "-w", "\n%{http_code}", "--max-time", "30",
                        f"https://naya-walk-beginning-staging.nayapower.workers.dev/api/welcome/box?alias={alias}"],
                       capture_output=True, text=True, timeout=60)
    body, _, code = r.stdout.rpartition("\n")
    st = int(code) if code.strip().isdigit() else 0
    check(f"box re-read {alias} 200", st == 200, str(st))
    if st == 200:
        box = json.loads(body)
        before = json.load(open(f"{PROOF}spp-box-{alias}.json"))
        same = box["box"]["answers"] == before["box"]["answers"] and [p["headline"] for p in box["pages"]] == [p["headline"] for p in before["pages"]]
        check(f"box re-read {alias} word-for-word (untouched)", same, "" if same else "DIFFERS")
R["notes"] = [f"pass={len(R['pass'])} fail={len(R['fail'])}",
              "2026-11-13 ~05:20Z: 6 story-title fails superseded — wrong element (.ib-layer-head b); correct element #os-story-title. See record Addendum C.",
              "2026-11-13 ~05:35Z: 7 box re-read status-0 fails were the VM urllib path truncating live-staging responses (IncompleteRead/RemoteDisconnected); curl returns 200 for all three, word-for-word. 1 plus-menu fail was a probe locator bug (exact-text 'Make a post' vs item '✎ Make a post'); corrected click opens the creator. See record Addendum E."]
json.dump(R, open(WORK + "spp-results.json", "w"), indent=2)
print(f"RE-CHECK DONE: pass={len(R['pass'])} fail={len(R['fail'])}")
for f in R["fail"]:
    print("FAIL:", f)

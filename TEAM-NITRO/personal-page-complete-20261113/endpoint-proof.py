#!/usr/bin/env python3
"""Endpoint proof — Personal page complete round (maker).
Creates MY OWN staged test citizens (pc*20261113), calls the gated
endpoint POST /api/welcome/matches on naya-welcome-staging, saves the
raw answer. Cleanup is a separate script (cleanup-endpoint-proof.py)
run right after the results are recorded. Other lanes' rows untouched.
Service key via the scheduler's established path, memory only.
"""
import importlib.util, json, subprocess, uuid

SCHED = "/home/hatch/workspace/goals/official-welcome-onboarding/welcome-series-scheduler.py"
spec = importlib.util.spec_from_file_location("sched", SCHED)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
key = m.get_service_key()
print("service key obtained (memory only, never printed)")

NOW = "2026-11-13T14:40:00+00:00"
DEVKEY = uuid.uuid4().hex

VIEW_ANS = {
    "about": "I build and test web pages for a living.",
    "into": "building, testing, shipping web pages",
    "vision": "shipping pages that work first time",
    "mission": "build by testing",
    "motto": "test it twice, ship it once",
    "goal": "ship, test, prove everything",
    "biz_do": "building and testing pages",
    "biz_offer": "tested pages for builders",
    "biz_building": "building tools for page builders",
    "space": "building, testing, shipping",
}
PROV_ANS = {
    "about": "I test builds and prove pages work.",
    "into": "testing, proving, shipping pages",
    "vision": "proven shipping",
    "mission": "prove by testing",
    "motto": "prove it before you report it",
    "goal": "test, prove, ship pages",
    "biz_do": "testing and proving pages",
    "biz_offer": "proof for builders",
    "biz_building": "building proof tools for testers",
    "space": "testing, proving, shipping",
}
FAR_ANS = {
    "about": "I keep bees and bake sourdough bread.",
    "into": "beekeeping, sourdough, honey",
    "vision": "a hive on every rooftop",
    "mission": "teach neighbours to keep bees",
    "motto": "slow honey, warm bread",
    "goal": "keep healthy beehives",
    "biz_do": "I keep bees",
    "biz_offer": "honey and hive advice",
    "biz_building": "a rooftop apiary",
    "space": "beekeeping club, baking",
}
PUB = {"personal": {"visibility": "public", "findable": True},
       "business": {"visibility": "public", "findable": True},
       "space": {"visibility": "public", "findable": True}}

for row in [
    {"alias": "pcviewer20261113", "name": "Personal Complete Viewer (test)",
     "answers": VIEW_ANS, "topics": ["building", "testing"], "settings": PUB, "updated_at": NOW},
    {"alias": "pcprover20261113", "name": "Personal Complete Prover (test)",
     "answers": PROV_ANS, "topics": ["testing", "proving"], "settings": PUB, "updated_at": NOW},
    {"alias": "pcfar20261113", "name": "Personal Complete Far (test)",
     "answers": FAR_ANS, "topics": ["beekeeping", "sourdough"], "settings": PUB, "updated_at": NOW},
]:
    out = m.sb(key, "POST", "/rest/v1/citizen_worlds", row, query="on_conflict=alias")
    print("world", row["alias"], "->", json.dumps(out)[:160])

out = m.sb(key, "POST", "/rest/v1/nayanet_identities",
           {"alias": "pcviewer20261113", "name": "Personal Complete Viewer (test)",
            "device_key": DEVKEY}, query="on_conflict=alias")
print("identity pcviewer20261113 ->", json.dumps(out)[:160])

body = json.dumps({"alias": "pcviewer20261113", "device_key": DEVKEY,
                   "name": "Personal Complete Viewer (test)"})
r = subprocess.run(["curl", "-s", "-w", "\nHTTP:%{http_code}",
                    "https://naya-welcome-staging.nayapower.workers.dev/api/welcome/matches",
                    "-H", "Content-Type: application/json", "--data", body],
                   capture_output=True, text=True, timeout=60)
print("endpoint HTTP + body:")
print(r.stdout[:4000])
print("curl stderr:", r.stderr[:300])
raw = r.stdout.rsplit("\nHTTP:", 1)
data = json.loads(raw[0])
with open("/home/hatch/workspace/team-nitro/personal-page-complete-20261113/endpoint-proof.json", "w") as f:
    json.dump({"http": raw[1] if len(raw) > 1 else "?", "body": data}, f, indent=2)
print("saved endpoint-proof.json")
ms = data.get("matches", [])
print(f"MATCHES: {len(ms)}")
for mm in ms:
    print(f"  - {mm.get('name')} ({mm.get('alias')}) pct={mm.get('pct')} score={mm.get('score')} reasons={mm.get('reasons')}")
print("sql_twin:", json.dumps(data.get("sql_twin"))[:300])
print("gated:", data.get("gated"), "gate:", data.get("gate"))

#!/usr/bin/env python3
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
F=ROOT/".naya/project-intelligence/evidence-lineage-fixture.json"
D=json.loads(F.read_text())
if D.get("project")!="NAYANET": raise SystemExit("LINEAGE=RED FIRST_DIVERGENCE=project")
k={n["kind"] for n in D["nodes"]}
required={"source","claim","action","outcome","verification","learning","successor"}
if not required <= k: raise SystemExit("LINEAGE=RED FIRST_DIVERGENCE=missing node kind")
ids={n["node_id"] for n in D["nodes"]}
for e in D["edges"]:
    if e["from"] not in ids or e["to"] not in ids: raise SystemExit("LINEAGE=RED FIRST_DIVERGENCE=dangling edge")
rels={e["relation"] for e in D["edges"]}
if not {"SUPPORTS","RESULTS_IN","VERIFIES","TEACHES","HANDOFF_TO"} <= rels: raise SystemExit("LINEAGE=RED FIRST_DIVERGENCE=incomplete relations")
print(json.dumps({"status":"GREEN","lineage_id":D["lineage_id"],"nodes":len(D["nodes"]),"edges":len(D["edges"]),"complete_chain":"source→claim→action→outcome→verification→learning→successor"},indent=2))

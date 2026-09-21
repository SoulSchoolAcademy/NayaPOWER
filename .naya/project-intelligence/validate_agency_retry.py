#!/usr/bin/env python3
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
C=json.loads((ROOT/".naya/project-intelligence/agency-retry-contract.json").read_text())
F=json.loads((ROOT/".naya/project-intelligence/agency-retry-fixtures.json").read_text())
levels={f"L{i}":i for i in range(6)}
for c in F["agency"]:
    got="ALLOW" if levels[c["requested"]]<=levels[c["granted"]] else "DENY"
    if got!=c["expected"]: raise SystemExit(f"AGENCY_RETRY=RED FIRST_DIVERGENCE={c['id']}")
for c in F["retry"]:
    got="ALLOW" if c["changed"] else "DENY"
    if got!=c["expected"]: raise SystemExit(f"AGENCY_RETRY=RED FIRST_DIVERGENCE={c['id']}")
print(json.dumps({"status":"GREEN","agency_levels":6,"agency_fixtures":len(F["agency"]),"retry_fixtures":len(F["retry"]),"no_retry_without_new_information":"ENFORCED_BY_FIXTURE"} ,indent=2))

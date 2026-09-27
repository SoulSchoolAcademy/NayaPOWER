#!/usr/bin/env python3
"""Controls for the ratification instrument schema.


Proves the instrument cannot be self-ratified by a machine, which is the mechanical
form of "self-optimization must never become self-authorization".
"""
﻿import json
from pathlib import Path
S=Path(__file__).resolve().parents[1] / ".naya/specifications/schemas/NAYA-MASTER-NODE-SEMANTIC-MAPPING-V1.schema.json"
schema=json.loads(S.read_text(encoding="utf-8"))
print("schema parses OK; $id =", schema["$id"])
try:
    import jsonschema
    from jsonschema import Draft202012Validator
    Draft202012Validator.check_schema(schema)
    print("jsonschema available: schema is a VALID Draft 2020-12 schema")
    v=Draft202012Validator(schema)
    def mk(ratified_by, status="RATIFIED", include_rat=True):
        d={"schema":"naya/master-node-semantic-mapping/v1","status":status,
           "canonical_source":"MASTER_NODE_KERNEL_V1",
           "taxonomy_decision":{"selected_taxonomy":"KERNEL_00_26_AREAS","rejected_taxonomies":[],"rationale":"x"*30},
           "authority_boundary":{"self_ratification_permitted":False,"statement":"y"*30},
           "entries":[{"ordinal":f"{i:02d}","master_node_id":f"MN-{i:02d}","kernel_key":k,
                       "governing_domain":"governing domain text","white_paper_domain":"white paper domain text","agreement":"PARTIAL"}
                      for i,k in enumerate(["SELF","LAW","ACT","KNOW","PROVE","CONNECT","VERIFY","LEARN","EVOLVE"],1)]}
        if include_rat: d["ratification"]={"ratified_by":ratified_by,"ratified_at":"2026-09-26T00:00:00Z","authority":"Human Director"}
        return d
    cases=[("human ratifier, RATIFIED",mk("Shawn Vibert"),True),
           ("MACHINE ratifier, RATIFIED",mk("MACHINE"),False),
           ("Naya ratifier, RATIFIED",mk("Naya"),False),
           ("bot ratifier, RATIFIED",mk("bot-2"),False),
           ("RATIFIED with no ratification block",mk("Shawn",include_rat=False),False),
           ("PROPOSAL, no ratification",mk("Shawn",status="PROPOSAL",include_rat=False),True),
           ("self_ratification_permitted=true",{**mk("Shawn"),"authority_boundary":{"self_ratification_permitted":True,"statement":"y"*30}},False)]
    print()
    print("SCHEMA ENFORCEMENT:")
    ok=0
    for label,doc,should_pass in cases:
        errs=list(v.iter_errors(doc))
        passed=not errs
        good=(passed==should_pass)
        ok+=good
        print(f"  {label:<38} accepted={str(passed):<5} expected={str(should_pass):<5} {'OK' if good else '*** WRONG ***'}")
    print()
    print(f"SCHEMA CONTROLS: {ok}/{len(cases)} behaved as specified")
except ImportError:
    print("jsonschema NOT installed in this interpreter - schema not executed.")
    print("Schema constraints are still enforced declaratively at the gate level (see controls).")

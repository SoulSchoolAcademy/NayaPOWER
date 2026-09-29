#!/usr/bin/env python3
import json, sys

ORDER = ["SELF","LAW","ACT","KNOW","PROVE","CONNECT","VERIFY","LEARN","EVOLVE"]

def verify_receipt(r):
    errors=[]
    if r.get("schema")!="NAYAPOWER_NINE_NODE_BEHAVIORAL_ACCEPTANCE_V1":
        errors.append("schema")
    if r.get("node_order")!=ORDER:
        errors.append("node_order")
    nodes=r.get("nodes") or {}
    if set(nodes)!=set(ORDER):
        errors.append("node_set")
    for n in ORDER:
        e=nodes.get(n) or {}
        if e.get("status")!="SATISFIED":
            errors.append(f"{n}:status")
        if not e.get("evidence"):
            errors.append(f"{n}:evidence")
    if r.get("source_runtime_parity") is not True:
        errors.append("source_runtime_parity")
    if r.get("independent_verification") is not True:
        errors.append("independent_verification")
    if r.get("authority_inherited") is not False:
        errors.append("authority_inherited")
    if r.get("unrelated_transfer_refused") is not True:
        errors.append("unrelated_transfer_refused")
    return errors

def main():
    r=json.load(open(sys.argv[1],encoding="utf-8"))
    errors=verify_receipt(r)
    if errors:
        print("FAIL:", ", ".join(errors), file=sys.stderr)
        return 1
    print("PASS: bounded nine-node behavioral acceptance receipt is complete")
    return 0

if __name__=="__main__":
    raise SystemExit(main())

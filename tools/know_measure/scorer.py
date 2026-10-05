#!/usr/bin/env python3
"""Independent scorer for the KNOW measurement harness.

Reads the frozen spec + the append-only retrieval log and recomputes the
verdict against the pre-registered pass criteria. No LLM, no judgment —
arithmetic and string comparison only. Exit 0 = ALL criteria pass,
exit 1 = at least one fails (the failure is the finding).

Usage:
  python3 scorer.py --spec query_spec_v1.json --log <run-dir>/retrieval_log.jsonl
"""
import argparse
import json
import sys
from pathlib import Path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--spec", required=True)
    ap.add_argument("--log", required=True)
    args = ap.parse_args()

    spec = json.loads(Path(args.spec).read_text(encoding="utf-8"))
    records = [json.loads(l) for l in Path(args.log).read_text(encoding="utf-8").splitlines() if l.strip()]
    crit = spec["pass_criteria"]
    checks = []

    def check(name, ok, detail):
        checks.append({"criterion": name, "pass": bool(ok), "detail": detail})

    # P5 first: log integrity (everything else rests on it)
    seqs = [r["seq"] for r in records]
    check("P5_log_integrity",
          seqs == list(range(len(records))) and
          all(set(spec["required_log_fields"]) <= set(r) for r in records),
          f"{len(records)} records, seq contiguous 0..{len(records)-1}, all required fields present")

    by_qid = {}
    for r in records:
        if r["query_id"] != "__manifest__":
            by_qid.setdefault(r["query_id"], []).append(r)

    # P1: no false hits
    p1_ok, p1_det = True, []
    for q in spec["miss_queries"]:
        recs = by_qid.get(q["id"], [])
        ok = len(recs) == 1 and recs[0]["outcome"] == "MISS:NO_RELEVANT_INTELLIGENCE"
        p1_ok &= ok
        p1_det.append(f"{q['id']}:{'MISS' if ok else 'UNEXPECTED:' + str([r['outcome'] for r in recs])}")
    check("P1_no_false_hits", p1_ok, "; ".join(p1_det))

    # P2: no wrong hits
    p2_ok, p2_det = True, []
    for q in spec["hit_queries"]:
        recs = [r for r in by_qid.get(q["id"], []) if r["outcome"] == "HIT"]
        ok = bool(recs) and all(q["expect_ib_contains"] in r["returned_ib"] for r in recs)
        p2_ok &= ok
        p2_det.append(f"{q['id']}:{'HIT-expected-note' if ok else 'WRONG:' + str([r.get('returned_ib','')[:40] for r in recs])}")
    check("P2_no_wrong_hits", p2_ok, "; ".join(p2_det))

    # P3: consumer act-first-v1 fires on H1
    h1 = [r for r in by_qid.get("H1", []) if r.get("consumer_id") == "act-first-v1"]
    p3_ok = (len(h1) == 1 and h1[0]["changed"] is True
             and h1[0]["treatment_decision"] == "ACT_WITHOUT_APPROVAL"
             and h1[0]["control_decision"] == "ASK_FIRST")
    check("P3_consumer_fires", p3_ok,
          f"H1 act-first-v1: control={h1[0]['control_decision'] if h1 else 'n/a'} "
          f"treatment={h1[0]['treatment_decision'] if h1 else 'n/a'} "
          f"changed={h1[0]['changed'] if h1 else 'n/a'}" if h1 else "no H1 act-first-v1 record")

    # P4: latency
    lats = sorted(r["latency_ms"] for r in records if r["query_id"] != "__manifest__")
    p95 = lats[max(0, int(len(lats) * 0.95) - 1)] if lats else None
    check("P4_latency", p95 is not None and p95 < 2000, f"p95={p95}ms over {len(lats)} queries (bar 2000ms)")

    # Informational: bundled held_out coupling (not a pass criterion)
    ho = [r for r in records if r.get("consumer_id") == "held-out-v1"]
    ho_fired = sum(1 for r in ho if r["changed"])
    info = (f"held-out-v1 measured on {len(ho)} hits: fired {ho_fired}x "
            f"(governing phrases absent from pinned corpus -> treatment UNRESOLVED; "
            f"finding for the pipeline owner, not a harness defect)")

    verdict = all(c["pass"] for c in checks)
    report = {"verdict": "PASS" if verdict else "FAIL", "checks": checks, "info": info,
              "criteria": crit}
    print(json.dumps(report, indent=2))
    sys.exit(0 if verdict else 1)


if __name__ == "__main__":
    main()

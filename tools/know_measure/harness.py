#!/usr/bin/env python3
"""KNOW retrieval measurement harness — the instrument, not the engine.

Measures tools/smart_note_v2.py::retrieve(query) exactly as shipped:
  HIT  -> dict with the retrieved registry entry + explanation
  MISS -> SystemExit("NO_RELEVANT_INTELLIGENCE")

For each HIT the harness hands the retrieved note to the registered
consumers (control vs treatment) and records the OBSERVED decision delta.
For each MISS it records the consumer abstention. A miss is logged with the
same fidelity as a hit.

Usage:
  python3 harness.py --repo <worktree-at-pinned-sha> --spec query_spec_v1.json --out <run-dir>

Outputs in <run-dir>:
  retrieval_log.jsonl   append-only, one record per query (+ run manifest seq 0)
  summary.json          hit/miss counts, latencies, consumer outcomes
Exit code 0 always (the verdict belongs to scorer.py, run separately).

The harness never edits the log mid-run and never retries a query.
"""
import argparse
import hashlib
import json
import sys
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path


def utc_now():
    return datetime.now(timezone.utc).isoformat()


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def run_consumer_act_first_v1(note_text):
    """Harness-defined consumer, rule frozen in the spec."""
    control = "ASK_FIRST"
    treatment = (
        "ACT_WITHOUT_APPROVAL"
        if "repository reads" in note_text.lower()
        else "UNRESOLVED"
    )
    return control, treatment, (control != treatment and treatment == "ACT_WITHOUT_APPROVAL")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True, help="worktree at the pinned corpus SHA")
    ap.add_argument("--spec", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    repo = Path(args.repo).resolve()
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    spec = json.loads(Path(args.spec).read_text(encoding="utf-8"))

    sys.path.insert(0, str(repo / "tools"))
    import smart_note_v2 as sn2  # noqa: E402  (the system under test)

    corpus_sha = spec["corpus_pin"]["git_sha"]
    reg_path = repo / spec["corpus_pin"]["registry"]
    registry_sha256 = sha256_file(reg_path)
    run_id = "knowrun-" + uuid.uuid4().hex[:12]

    log_path = out / "retrieval_log.jsonl"
    seq = 0

    def emit(record):
        nonlocal seq
        record["seq"] = seq
        seq += 1
        for f in spec["required_log_fields"]:
            if f not in record:
                raise AssertionError(f"log record missing required field: {f}")
        with open(log_path, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(record, sort_keys=True) + "\n")

    # seq 0: run manifest (corpus snapshot — the repeatability anchor)
    emit({
        "run_id": run_id, "ts_utc": utc_now(),
        "corpus_sha": corpus_sha, "registry_sha256": registry_sha256,
        "query_id": "__manifest__", "query": "",
        "query_sha256": hashlib.sha256(b"").hexdigest(),
        "outcome": "MANIFEST", "latency_ms": 0,
        "returned_ib": "", "consumer_id": "",
        "control_decision": "", "treatment_decision": "", "changed": False,
        "spec_version": spec["spec_version"],
    })

    results = []
    queries = [("hit", q) for q in spec["hit_queries"]] + [("miss", q) for q in spec["miss_queries"]]

    for kind, q in queries:
        qid, query = q["id"], q["query"]
        qhash = hashlib.sha256(query.encode()).hexdigest()
        t0 = time.perf_counter()
        try:
            res = sn2.retrieve(query)
            latency_ms = int((time.perf_counter() - t0) * 1000)
            entry = res["retrieved"]
            ib = entry["intelligent_block_id"]
            note_text = (repo / entry["projection_path"]).read_text(encoding="utf-8")

            # Consumer 1: bundled held_out (measured as-is)
            h = sn2.held_out(res)
            c1 = {
                "consumer_id": "held-out-v1",
                "control_decision": h["control"]["decision"],
                "treatment_decision": h["treatment"]["decision"],
                "changed": bool(h["behavior_changed"]),
            }
            # Consumer 2: harness-defined act-first decision
            c2_control, c2_treat, c2_changed = run_consumer_act_first_v1(note_text)
            c2 = {
                "consumer_id": "act-first-v1",
                "control_decision": c2_control,
                "treatment_decision": c2_treat,
                "changed": c2_changed,
            }
            for c in (c1, c2):
                emit({
                    "run_id": run_id, "ts_utc": utc_now(),
                    "corpus_sha": corpus_sha, "registry_sha256": registry_sha256,
                    "query_id": qid, "query": query, "query_sha256": qhash,
                    "outcome": "HIT", "latency_ms": latency_ms,
                    "returned_ib": ib, **c,
                })
            results.append({"id": qid, "kind": kind, "outcome": "HIT",
                            "returned_ib": ib, "latency_ms": latency_ms,
                            "consumers": [c1, c2]})
        except SystemExit as ex:
            latency_ms = int((time.perf_counter() - t0) * 1000)
            code = ex.code
            emit({
                "run_id": run_id, "ts_utc": utc_now(),
                "corpus_sha": corpus_sha, "registry_sha256": registry_sha256,
                "query_id": qid, "query": query, "query_sha256": qhash,
                "outcome": f"MISS:{code}", "latency_ms": latency_ms,
                "returned_ib": "", "consumer_id": "abstain",
                "control_decision": "INSUFFICIENT_CANONICAL_CONTEXT",
                "treatment_decision": "ABSTAIN_NO_RETRIEVAL",
                "changed": False,
            })
            results.append({"id": qid, "kind": kind, "outcome": f"MISS:{code}",
                            "latency_ms": latency_ms})

    lat = sorted(r["latency_ms"] for r in results)
    p95 = lat[max(0, int(len(lat) * 0.95) - 1)]
    summary = {
        "run_id": run_id, "ts_utc": utc_now(),
        "corpus_sha": corpus_sha, "registry_sha256": registry_sha256,
        "spec_version": spec["spec_version"],
        "n_queries": len(results),
        "n_hit": sum(1 for r in results if r["outcome"] == "HIT"),
        "n_miss": sum(1 for r in results if r["outcome"].startswith("MISS")),
        "latency_ms": {"min": lat[0], "p50": lat[len(lat)//2], "p95": p95, "max": lat[-1]},
        "results": results,
        "log": str(log_path),
    }
    (out / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps({"run_id": run_id, "n_hit": summary["n_hit"],
                      "n_miss": summary["n_miss"], "p95_ms": p95,
                      "log": str(log_path)}, indent=2))


if __name__ == "__main__":
    main()

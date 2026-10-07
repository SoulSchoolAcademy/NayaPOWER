"""CI gate: retrieval ranking quality (precision/recall evidence).

Runs the offline retrieval benchmark against the REAL shipped migration
bytes (v1 search substrate + v2 OR-fallback) on a scratch Postgres and
asserts MRR/P@1 plus the structural invariants (SUPERSEDED/DELETED never
served; VERIFIED outranks CANDIDATE).

Needs Postgres: CI provides it via the `postgres` service on
kernel-tests.yml. Skips with cause when no Postgres is reachable (local
runs without one); the gate is real in CI, never vacuous there.
"""
import json
import importlib.util
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "retrieval_benchmark_run", ROOT / "tools" / "retrieval_benchmark" / "run.py")
mod = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(mod)


def _postgres_reachable() -> bool:
    if mod.psycopg is None:
        return False
    try:
        conn = mod.connect("postgres")
        conn.close()
        return True
    except Exception:
        return False


def test_retrieval_ranking_meets_quality_bar():
    if not _postgres_reachable():
        pytest.skip("postgres unreachable (CI provides the postgres service)")
    corpus = json.loads(mod.CORPUS.read_text(encoding="utf-8"))
    conn = mod.setup_database()
    try:
        mod.load_corpus(conn, corpus)
        result = mod.run_benchmark(conn, corpus)
    finally:
        conn.close()
    metrics = result["metrics"]
    assert metrics["MRR"] >= 0.99, f"MRR regressed: {metrics['MRR']}"
    assert metrics["P@1"] >= 0.99, f"P@1 regressed: {metrics['P@1']}"
    failed = [s for s in result["structural"] if not s["pass"]]
    assert not failed, f"structural retrieval invariants broken: {failed}"
    # every judged query must resolve its relevant block at rank 1
    misses = [q for q in result["per_query"] if q["reciprocal_rank"] < 1.0]
    assert not misses, f"queries not resolved at rank 1: {[q['id'] for q in misses]}"

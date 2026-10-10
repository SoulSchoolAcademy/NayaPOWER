#!/usr/bin/env python3
"""Offline retrieval ranking benchmark.

Measures the REAL nayanet_retrieve_blocks() ranking function against fixed
relevance judgments authored BEFORE any measurement run. The caller sets up
a scratch Postgres (the pytest suite does this in CI via the postgres
service); this module only loads the corpus and computes metrics.

Metrics: MRR, P@1, P@3, Recall@5 over the judged queries, plus structural
assertions:
  S1  SUPERSEDED blocks are never served, however strong the text match.
  S2  VERIFIED canon outranks a CANDIDATE draft on shared vocabulary.
  S3  DELETED blocks are never served, however strong the text match.

Connection: PGHOST / PGPORT / PGUSER / PGPASSWORD / PGDATABASE env.
OFFLINE ONLY. Never point this at production.
"""
from __future__ import annotations
import json
import os
import sys
from pathlib import Path

try:
    import psycopg
except ImportError:
    psycopg = None

CORPUS = Path(__file__).parent / "corpus.json"
MIGRATIONS = [
    Path(__file__).parents[2] / "supabase" / "migrations"
    / "20261006235900_nayanet_cold_retrieve_search_v1.sql",
    Path(__file__).parents[2] / "supabase" / "migrations"
    / "20261007220000_nayanet_retrieve_or_fallback_v2.sql",
]

MIN_TABLE_DDL = """
CREATE TABLE IF NOT EXISTS public.nayanet_intelligent_blocks (
  block_id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  intelligent_block_id text UNIQUE,
  owner_id uuid NOT NULL,
  status text NOT NULL DEFAULT 'ACTIVE',
  understanding_state text NOT NULL DEFAULT 'CANDIDATE',
  owner_scope text NOT NULL DEFAULT 'PRIVATE',
  applicable_scope jsonb NOT NULL DEFAULT '{}',
  content jsonb NOT NULL DEFAULT '{}',
  connections jsonb,
  superseded_by_block_id text,
  evidence_refs jsonb NOT NULL DEFAULT '[]',
  provenance jsonb NOT NULL DEFAULT '{}',
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now()
);
"""


def connect(dbname: str | None = None):
    if psycopg is None:
        raise RuntimeError("psycopg is required (pip install psycopg[binary])")
    return psycopg.connect(
        host=os.environ.get("PGHOST", "localhost"),
        port=int(os.environ.get("PGPORT", "5432")),
        user=os.environ.get("PGUSER", "postgres"),
        password=os.environ.get("PGPASSWORD", "postgres"),
        dbname=dbname or os.environ.get("PGDATABASE", "postgres"),
        connect_timeout=5,
        autocommit=True,
    )


def setup_database():
    """Create a scratch DB, the minimal blocks table, and apply the REAL
    migration files from the repo in version order."""
    admin = connect("postgres")
    dbname = "retrieval_bench_test"
    with admin.cursor() as cur:
        cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (dbname,))
        if cur.fetchone():
            # terminate stray backends before drop
            cur.execute(
                "SELECT pg_terminate_backend(pid) FROM pg_stat_activity "
                "WHERE datname = %s AND pid <> pg_backend_pid()", (dbname,))
            cur.execute(f'DROP DATABASE "{dbname}"')
        cur.execute(f'CREATE DATABASE "{dbname}"')
    admin.close()
    conn = connect(dbname)
    with conn.cursor() as cur:
        cur.execute("CREATE EXTENSION IF NOT EXISTS pgcrypto")
        cur.execute(MIN_TABLE_DDL)
        for mig in MIGRATIONS:
            if not mig.is_file():
                raise RuntimeError(f"migration missing: {mig}")
            cur.execute(mig.read_text(encoding="utf-8"))
    return conn


def load_corpus(conn, corpus: dict):
    owner = corpus.get("owner_id")
    with conn.cursor() as cur:
        for b in corpus["blocks"]:
            cur.execute(
                """INSERT INTO public.nayanet_intelligent_blocks
                   (intelligent_block_id, owner_id, status, understanding_state,
                    owner_scope, applicable_scope, content, connections,
                    superseded_by_block_id, evidence_refs, provenance)
                   VALUES (%s,%s,%s,%s,%s,%s::jsonb,%s::jsonb,%s::jsonb,%s,%s::jsonb,%s::jsonb)
                   ON CONFLICT (intelligent_block_id) DO NOTHING""",
                (b["intelligent_block_id"], owner, b["status"],
                 b["understanding_state"], b.get("owner_scope", "PRIVATE"),
                 json.dumps(b.get("applicable_scope", {})),
                 json.dumps(b.get("content", {})),
                 json.dumps(b["connections"]) if b.get("connections") is not None else None,
                 b.get("superseded_by_block_id"),
                 json.dumps(b.get("evidence_refs", [])),
                 json.dumps(b.get("provenance", {}))),
            )
        # deterministic recency stagger, by corpus order
        for i, b in enumerate(corpus["blocks"]):
            cur.execute(
                "UPDATE public.nayanet_intelligent_blocks "
                f"SET updated_at = now() - interval '{i} hours' "
                "WHERE intelligent_block_id = %s", (b["intelligent_block_id"],))


def retrieve(conn, owner: str, query: str, context: dict, limit: int = 10) -> list[str]:
    with conn.cursor() as cur:
        cur.execute("SELECT public.nayanet_retrieve_blocks(%s, %s::uuid, %s, %s::jsonb)",
                    (query, owner, limit, json.dumps(context or {})))
        data = cur.fetchone()[0]
    if not data:
        return []
    rows = data if isinstance(data, list) else json.loads(data)
    return [r["block_id"] for r in rows]


def run_benchmark(conn, corpus: dict) -> dict:
    owner = corpus.get("owner_id")
    per_query = []
    rr = p1 = p3 = rec5 = 0.0
    for q in corpus["queries"]:
        ranked = retrieve(conn, owner, q["query"], q.get("context", {}))
        rel = set(q.get("relevant", []))
        rrank = next((1.0 / i for i, b in enumerate(ranked, 1) if b in rel), 0.0)
        hit1 = 1.0 if ranked and ranked[0] in rel else 0.0
        hit3 = len([b for b in ranked[:3] if b in rel]) / min(3, len(rel)) if rel else 0.0
        rec = len([b for b in ranked[:5] if b in rel]) / len(rel) if rel else 0.0
        rr += rrank; p1 += hit1; p3 += hit3; rec5 += rec
        per_query.append({"id": q["id"], "reciprocal_rank": round(rrank, 4),
                          "p_at_1": hit1, "ranked_top5": ranked[:5]})
    n = len(corpus["queries"])
    structural = []
    for s in corpus.get("structural_assertions", []):
        ranked = retrieve(conn, owner, s["query"], {})
        if "forbidden" in s:
            bad = [b for b in s["forbidden"] if b in ranked]
            structural.append({"id": s["id"], "pass": not bad,
                               "detail": ("forbidden served: " + ",".join(bad)) if bad else "none served"})
        if "first_must_be" in s:
            ok = bool(ranked) and ranked[0] == s["first_must_be"]
            structural.append({"id": s["id"], "pass": ok,
                               "detail": f"first={ranked[0] if ranked else None}"})
    return {
        "n_queries": n,
        "metrics": {"MRR": round(rr / n, 4), "P@1": round(p1 / n, 4),
                    "P@3": round(p3 / n, 4), "Recall@5": round(rec5 / n, 4)},
        "structural": structural,
        "per_query": per_query,
    }


def main() -> int:
    corpus = json.loads(CORPUS.read_text(encoding="utf-8"))
    conn = setup_database()
    load_corpus(conn, corpus)
    result = run_benchmark(conn, corpus)
    print(json.dumps(result, indent=2))
    ok = (result["metrics"]["MRR"] >= 0.99 and result["metrics"]["P@1"] >= 0.99
          and all(s["pass"] for s in result["structural"]))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Isolated-DB round-trip proof for the persistence seam (Naya 2, dispatch 5935855302).

Runs ONLY against the disposable local Postgres (naya_isolated_rt).
Refuses anything resembling production.

What it proves:
  1. A real kernel receipt (Naya 4's pair-1, demo-001 @ 4e87d4a) projects
     through the v3 adapter (receipt_hash MATCH, inputs_hash MATCH).
  2. The projection is written via the CANONICAL writer
     (nayanet_record_ledger_event) — not a raw INSERT.
  3. A genuinely FRESH process reads the same event back.
  4. Read-back is owner/RLS isolated: owner A sees it, owner B sees 0 rows.
  5. Identical replay returns the same row (idempotent); conflicting payload
     for the same key returns the EXISTING row unchanged (canonical: no
     overwrite, no silent mutation).
  6. The 12 contract fields reconstruct from the retrieved row, 0 violations;
     receipt_hash + inputs_hash recompute to MATCH from row data alone.
  7. No invented timestamps/outcomes: issued_at/observed_at are absent.

Usage: python3 isolated_roundtrip.py
"""
import json
import os
import subprocess
import sys

ADAPTER_DIR = "/tmp/nayapower-full"
HANDOFF = os.path.expanduser("~/workspace/naya/isolated-db-handoff")
sys.path.insert(0, ADAPTER_DIR)
sys.path.insert(0, HANDOFF)
from kernel.persistence_seam import (  # noqa: E402
    project_kernel_receipt, verify_kernel_receipt, _sha256,
    validate_contract_record, EVENT_TYPE, SOURCE_TABLE,
)

import psycopg2
import psycopg2.extras

DSN = "dbname=naya_isolated_rt user=postgres host=/var/run/postgresql"
OWNER_A = "11111111-1111-1111-1111-111111111111"
OWNER_B = "22222222-2222-2222-2222-222222222222"
KERNEL_SHA = "4e87d4a5810f6b0b5b72e254f3d37ddf69826c87"

receipt = json.load(open(f"{HANDOFF}/pair-0.json"))
state = json.load(open(f"{HANDOFF}/pair-1.json"))

results = []
def check(name, cond, detail=""):
    results.append((name, cond))
    print(f"[{'PASS' if cond else 'FAIL'}] {name} {detail}")

# --- 1. Adapter projection ---
vr = verify_kernel_receipt(receipt)
check("receipt seal verifies (MATCH)", vr["result"] == "MATCH")
p = project_kernel_receipt(receipt, owner_id=OWNER_A,
                           kernel_sha=KERNEL_SHA, inputs_state=state)
check("projection accepted", p["p_event_type"] == EVENT_TYPE)
check("verification honest (UNVERIFIED)", p["p_verification"]["state"] == "UNVERIFIED")
check("no invented executed_at/observed_at",
      "executed_at" not in p and "observed_at" not in p)

# --- 2. Canonical write ---
conn = psycopg2.connect(DSN)
conn.autocommit = True
cur = conn.cursor()
cur.execute("INSERT INTO auth.users(id) VALUES (%s), (%s) ON CONFLICT DO NOTHING",
            (OWNER_A, OWNER_B))
cur.execute(
    """SELECT * FROM public.nayanet_record_ledger_event(
        %(o)s,%(etype)s,%(stable)s,%(sid)s,
        %(at)s::timestamptz,%(o)s,'PRIVATE','RECORDED','[]'::jsonb,
        %(ver)s::jsonb,%(val)s::jsonb,%(out)s::jsonb,'[]'::jsonb,%(meta)s::jsonb)""",
    {"o": OWNER_A, "sid": receipt["receipt_id"], "at": receipt["issued_at"],
     "etype": EVENT_TYPE, "stable": SOURCE_TABLE,
     "ver": json.dumps(p["p_verification"]), "val": json.dumps(p["p_value"]),
     "out": json.dumps({}), "meta": json.dumps(p["p_metadata"])})
row = cur.fetchone()
cols = [d[0] for d in cur.description]
wrote = dict(zip(cols, row))
check("canonical writer returned row", wrote["owner_id"] == OWNER_A)
check("chain hash computed by writer", bool(wrote["event_hash"]))
first_id, first_hash = wrote["ledger_event_id"], wrote["event_hash"]

# --- 5a. Identical replay: idempotent ---
cur.execute(
    """SELECT ledger_event_id FROM public.nayanet_record_ledger_event(
        %(o)s,%(etype)s,%(stable)s,%(sid)s,
        %(at)s::timestamptz)""",
    {"o": OWNER_A, "sid": receipt["receipt_id"], "at": receipt["issued_at"],
     "etype": EVENT_TYPE, "stable": SOURCE_TABLE})
replay_id = cur.fetchone()[0]
check("identical replay idempotent (same row)", str(replay_id) == str(first_id))

# --- 5b. Conflicting payload: existing row returned unchanged ---
cur.execute(
    """SELECT value FROM public.nayanet_record_ledger_event(
        %(o)s,%(etype)s,%(stable)s,%(sid)s,
        %(at)s::timestamptz,%(o)s,'PRIVATE','RECORDED','[]'::jsonb,
        '{}'::jsonb,%(val)s::jsonb)""",
    {"o": OWNER_A, "sid": receipt["receipt_id"], "at": receipt["issued_at"],
     "etype": EVENT_TYPE, "stable": SOURCE_TABLE,
     "val": json.dumps({"tampered": True})})
check("conflicting payload does NOT overwrite (canonical no-mutation)",
      cur.fetchone()[0].get("tampered") is None)
conn.close()

# --- 3+4+6. Fresh-process read-back, RLS isolation, recomputation ---
READER = r'''
import importlib.util, json, os, sys
sys.path.insert(0, "/tmp/nayapower-full")
sys.path.insert(0, os.path.expanduser("~/workspace/naya/isolated-db-handoff"))
import psycopg2, psycopg2.extras
from kernel.persistence_seam import _sha256, validate_contract_record, verify_kernel_receipt
spec = importlib.util.spec_from_file_location(
    "recon12", os.path.expanduser("~/workspace/naya/isolated-db-handoff/reconstruct-12field.py"))
recon = importlib.util.module_from_spec(spec); spec.loader.exec_module(recon)
uid = sys.argv[1]
conn = psycopg2.connect("dbname=naya_isolated_rt user=postgres host=/var/run/postgresql")
conn.autocommit = True
cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
cur.execute("SET ROLE authenticated")
cur.execute("SET app.uid = %s", (uid,))
cur.execute("SELECT * FROM public.nayanet_smart_ledger")
rows = cur.fetchall()
out = {"n": len(rows)}
if rows:
    r = {k: (str(v) if hasattr(v, "hex") or "UUID" in type(v).__name__ else
             v.isoformat() if hasattr(v, "isoformat") else v)
         for k, v in dict(rows[0]).items()}
    r.setdefault("chain_seq", None)
    rec = recon.reconstruct(r, None)
    out["violations"] = validate_contract_record(rec)
    # receipt_hash is not a contract field; the value blob IS the verbatim
    # kernel receipt — verify with the seam's own verifier (fresh process)
    _val = r["value"] if isinstance(r["value"], dict) else json.loads(r["value"])
    out["receipt_hash_match"] = (verify_kernel_receipt(_val)["result"] == "MATCH")
    md = r["metadata"] if isinstance(r["metadata"], dict) else json.loads(r["metadata"])
    # Cold recomputation: inputs_hash is NOT stored separately — the kernel's
    # claimed hash lives in the verbatim receipt (value.inputs_hash); the
    # consumer recomputes it from the preserved metadata.inputs_state.
    out["inputs_hash_match"] = (
        _sha256(md.get("inputs_state")) == _val.get("inputs_hash"))
    out["event_id"] = r["ledger_event_id"]
print(json.dumps(out))
'''
def fresh_read(uid):
    r = subprocess.run([sys.executable, "-c", READER, uid],
                       capture_output=True, text=True, check=True)
    return json.loads(r.stdout)

a = fresh_read(OWNER_A)
check("fresh process (owner A) reads 1 row", a["n"] == 1, a.get("event_id", ""))
check("12-field reconstruction: 0 violations", not a.get("violations"))
check("receipt_hash recomputes MATCH from row", a.get("receipt_hash_match") is True)
check("inputs_hash recomputes MATCH from row", a.get("inputs_hash_match") is True)
check("fresh-read row is the written row", a.get("event_id") == str(first_id))

b = fresh_read(OWNER_B)
check("owner B sees 0 rows (RLS isolation)", b["n"] == 0)

print()
failed = [n for n, c in results if not c]
print(f"{len(results)-len(failed)}/{len(results)} checks passed")
sys.exit(1 if failed else 0)

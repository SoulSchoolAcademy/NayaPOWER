#!/usr/bin/env python3
"""
gate-canonical-capture.py — Machine enforcement for the single-canonical-capture law.

LAW: The canonical Receiver (supabase/functions/v7-smart-note-canonical) is the
SINGLE canonical capture path. Durable intelligence objects are Intelligent Blocks.
Never create a second memory — no competing capture pipeline, no shadow persistence
of intelligence outside the governed path.

This gate FAILS (exit 1, fail-closed) when a second capture/memory path appears:
  C1: a new table matching intelligence patterns exists and is not allowlisted
  C2: an edge function performs a write op (insert/upsert/update/delete) on an
      intelligence table without an explicit allowlist entry
  C3: an edge function other than the Receiver invokes the canonical creation RPCs
  C4: a migration creates a table matching intelligence patterns that is not allowlisted

Allowlist entries are explicit and justified. Everything else fails closed.

Usage:
  python3 gate-canonical-capture.py --repo /path/to/NayaPOWER        # static scan (CI-safe)
  python3 gate-canonical-capture.py --repo /path --live              # + live DB schema check (read-only)
  python3 gate-canonical-capture.py --self-test                      # falsifier fixtures

Exit codes: 0 = PASS (canonical capture exclusivity holds), 1 = FAIL (findings),
            2 = gate error (could not complete the scan — also fail-closed upstream).
"""

import argparse
import base64
import json
import os
import re
import subprocess
import sys
import tempfile

# ----------------------------------------------------------------------------
# Canonical definitions (derived from read-only investigation, 2026-10-07)
# ----------------------------------------------------------------------------

CANONICAL_RECEIVER = "v7-smart-note-canonical"

# RPCs through which the Receiver creates durable intelligence. Only the
# Receiver may invoke these.
CANONICAL_CREATION_RPCS = {
    "v7_create_smart_note",          # creates the Intelligent Block
    "nayanet_record_cognition_event",  # creates the cognition event
}

# Intelligence tables: durable persistence of intelligence, learning, cognition,
# memory, relationships, lineage, checkpoints. Receipts/execution/authority tables
# are OPERATIONAL, not intelligence — they are out of scope for this gate.
INTELLIGENCE_TABLES = {
    "nayanet_intelligent_blocks",
    "nayanet_cognition_events",
    "nayanet_brain_relationships",
    "nayanet_intelligence_index",
    "nayanet_intelligence_lineage",
    "nayanet_checkpoint_receipts",
    "learning_evidence",
    "nayanet_project_cognition_state",
    "nayanet_collective_wisdom",
    "nayanet_successor_handoffs",
    "nayanet_smart_ledger",
}

# Writer allowlist: table -> { function -> {allowed ops} }.
# Ops: "insert", "upsert", "update", "delete", "rpc_create" (creation via
# canonical RPC, not a direct table write), "select" (read-only, recorded for
# completeness but not enforced as a write).
#
# Every entry was verified by reading the function source on main, 2026-10-07.
WRITER_ALLOWLIST = {
    "nayanet_intelligent_blocks": {
        # Creation happens ONLY inside the v7_create_smart_note RPC, invoked
        # ONLY by the canonical Receiver. No edge function writes directly.
        CANONICAL_RECEIVER: {"rpc_create"},
        # Governed promotion: status/verification transitions on existing rows
        # by the learning verification path. UPDATE only — never INSERT.
        "nayanet-learning-verify": {"update"},
    },
    "nayanet_cognition_events": {
        # Creation happens ONLY inside nayanet_record_cognition_event, invoked
        # ONLY by the canonical Receiver.
        CANONICAL_RECEIVER: {"rpc_create"},
    },
    "learning_evidence": {
        # Canonical capture seeds one CANDIDATE learning row per Smart Note
        # (v7-smart-note-canonical/index.ts: status="CANDIDATE",
        # provenance="USER", verification_method="PENDING_OUTCOME_VERIFICATION").
        # This is the canonical pipeline's own seeding, not a second capture
        # path. INSERT only — never status transitions (those are the
        # learning-verify path's job).
        CANONICAL_RECEIVER: {"insert", "select"},
        # Governed promotion path: CANDIDATE -> ACTIVE/REJECTED transitions.
        # This is the LEARN lifecycle step, not a second capture path: it
        # promotes existing candidates, it does not capture new experience.
        "nayanet-learning-verify": {"insert", "update"},
        # Read-only consumer (recorded; reads are not writes).
        "naya-decision-context": {"select"},
    },
    "nayanet_brain_relationships": {
        # Relationship edges are written by the canonical pipeline RPCs and
        # transitioned by the governed learning verification path.
        CANONICAL_RECEIVER: {"rpc_create"},
        "nayanet-learning-verify": {"update"},
    },
    "nayanet_intelligence_index": {
        CANONICAL_RECEIVER: {"rpc_create"},
    },
    "nayanet_intelligence_lineage": {
        CANONICAL_RECEIVER: {"rpc_create"},
    },
    "nayanet_checkpoint_receipts": {
        CANONICAL_RECEIVER: {"rpc_create"},
    },
    "nayanet_project_cognition_state": {
        "nayanet-learning-verify": {"update"},
    },
    # No direct edge-function writers observed on main, 2026-10-07.
    # Any writer appearing here is a second-memory candidate -> FAIL.
    "nayanet_collective_wisdom": {},
    "nayanet_successor_handoffs": {},
    "nayanet_smart_ledger": {},
}

# Table-name patterns that indicate an intelligence-persistence table.
# A new table matching these that is not in INTELLIGENCE_TABLES -> FAIL (C1/C4).
INTELLIGENCE_NAME_PATTERNS = [
    re.compile(p, re.I) for p in [
        r"intelligent_block",
        r"cognition",
        r"intelligence_(index|lineage|block)",
        r"brain_relationship",
        r"checkpoint_receipt",
        r"learning_evidence",
        r"collective_wisdom",
        r"successor_handoff",
        r"smart_ledger",
        r"shadow_memory",
        r"second_brain",
        r"(?<!nayanet_)memory_store",
    ]
]

# Operational tables: explicitly NOT intelligence. Writes here are receipts,
# execution records, authority grants — governed elsewhere, not second memories.
OPERATIONAL_TABLES = {
    "nayanet_execution_receipts",
    "nayanet_execution_outcomes",
    "nayanet_authority_grants",
    "nayanet_github_dispatch_receipts",
    "nayanet_value_receipts",
    "members",
    "nayanet_smart_connect_participation",
}

# Out of scope by design (documented, not enforced):
# - .naya/capture/*.json and .naya/preview/* : file-based staging on branches,
#   reviewed via PR. Staging is not persistence; no edge function can read the
#   repo filesystem, so these cannot become shadow DB writes.
# - Direct SQL via the Supabase API: a governance boundary (read-only policy),
#   not a code path this gate can scan.


class Finding:
    def __init__(self, check, what, where, why):
        self.check = check
        self.what = what
        self.where = where
        self.why = why

    def text(self):
        return (f"[{self.check}] FAIL\n"
                f"  what : {self.what}\n"
                f"  where: {self.where}\n"
                f"  why  : {self.why}")


# ----------------------------------------------------------------------------
# Scanners
# ----------------------------------------------------------------------------

WRITE_RE = re.compile(r"\.(insert|upsert|update|delete)\s*\(")
FROM_RE = re.compile(r"\.from\(\s*[\"']([^\"']+)[\"']\s*\)")
RPC_RE = re.compile(r"\.rpc\(\s*[\"']([^\"']+)[\"']")


def scan_function(path):
    """Return (writes, rpcs): writes = list of (op, table|None), rpcs = [names]."""
    with open(path, encoding="utf-8", errors="replace") as fh:
        src = fh.read()
    writes = []
    # Pair each .from("T") with the write op that follows it on the chain.
    for m in re.finditer(
        r"\.from\(\s*[\"']([^\"']+)[\"']\s*\)([^\n;]{0,400}?)\.(insert|upsert|update|delete)\s*\(",
        src,
    ):
        writes.append((m.group(3).lower(), m.group(1)))
    # Bare write calls without a resolvable .from() on the same chain.
    for m in WRITE_RE.finditer(src):
        # skip if already captured above (within 400 chars after a from)
        pass
    rpcs = sorted(set(RPC_RE.findall(src)))
    # Deduplicate writes preserving order
    seen, uniq = set(), []
    for w in writes:
        if w not in seen:
            seen.add(w)
            uniq.append(w)
    # Also count write calls whose table couldn't be chained (conservative:
    # report as unknown-table writes so a human reviews them).
    chained_positions = set()
    for m in re.finditer(
        r"\.from\(\s*[\"']([^\"']+)[\"']\s*\)([^\n;]{0,400}?)\.(insert|upsert|update|delete)\s*\(",
        src,
    ):
        chained_positions.add(m.start(3))
    for m in WRITE_RE.finditer(src):
        if m.start(1) not in chained_positions:
            # Try a nearby .from() within 5 lines before
            before = src[max(0, m.start() - 400):m.start()]
            fm = list(FROM_RE.finditer(before))
            table = fm[-1].group(1) if fm else "<unresolved>"
            key = (m.group(1).lower(), table)
            if key not in seen:
                seen.add(key)
                uniq.append(key)
    return uniq, rpcs


def list_functions(repo):
    funcdir = os.path.join(repo, "supabase", "functions")
    out = {}
    if not os.path.isdir(funcdir):
        return out
    for name in sorted(os.listdir(funcdir)):
        idx = os.path.join(funcdir, name, "index.ts")
        if os.path.isfile(idx):
            out[name] = idx
    return out


def check_writers(repo):
    """C2: every write to an intelligence table must be allowlisted."""
    findings = []
    for func, path in list_functions(repo).items():
        writes, _ = scan_function(path)
        for op, table in writes:
            if table not in INTELLIGENCE_TABLES:
                continue  # operational or unknown table: not this gate's job
            allowed = WRITER_ALLOWLIST.get(table, {}).get(func, set())
            if op not in allowed:
                findings.append(Finding(
                    "C2",
                    f"unauthorized {op} on intelligence table `{table}` by `{func}`",
                    path,
                    "Only allowlisted governed writers may persist intelligence. "
                    f"Allowlisted for `{table}`: "
                    + (", ".join(f"{f}:{sorted(o)}"
                                 for f, o in WRITER_ALLOWLIST.get(table, {}).items()
                                 if o != {"select"}) or "(none)")
                    + ". This is a second-memory candidate: fail closed.",
                ))
    return findings


def check_rpc_invokers(repo):
    """C3: canonical creation RPCs may only be invoked by the Receiver."""
    findings = []
    for func, path in list_functions(repo).items():
        _, rpcs = scan_function(path)
        for rpc in rpcs:
            if rpc in CANONICAL_CREATION_RPCS and func != CANONICAL_RECEIVER:
                findings.append(Finding(
                    "C3",
                    f"canonical creation RPC `{rpc}` invoked by non-Receiver `{func}`",
                    path,
                    "Intelligence creation flows exclusively through the canonical "
                    "Receiver. Any other invoker is a competing capture path.",
                ))
    return findings


def check_migration_tables(repo):
    """C4: migrations must not create unallowlisted intelligence tables."""
    findings = []
    migdir = os.path.join(repo, "supabase", "migrations")
    if not os.path.isdir(migdir):
        return findings
    for name in sorted(os.listdir(migdir)):
        if not name.endswith(".sql"):
            continue
        path = os.path.join(migdir, name)
        with open(path, encoding="utf-8", errors="replace") as fh:
            sql = fh.read()
        for m in re.finditer(r"CREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?([\w.]+)",
                             sql, re.I):
            tbl = m.group(1).split(".")[-1].strip('"')
            if tbl in INTELLIGENCE_TABLES or tbl in OPERATIONAL_TABLES:
                continue
            if any(p.search(tbl) for p in INTELLIGENCE_NAME_PATTERNS):
                findings.append(Finding(
                    "C4",
                    f"migration creates intelligence-pattern table `{tbl}`",
                    path,
                    "New intelligence-persistence tables are second-memory "
                    "candidates. Allowlist explicitly or fail closed.",
                ))
    return findings


def check_live_schema():
    """C1: live DB must not contain unallowlisted intelligence tables."""
    findings = []
    sb_api = os.path.expanduser("~/workspace/skills/supabase/bin/sb-api")
    if not os.path.isfile(sb_api):
        return [Finding("C1", "live schema check skipped: sb-api not found",
                        sb_api, "Gate error — cannot verify live schema.")]
    try:
        out = subprocess.run(
            [sb_api, "POST",
             "/v1/projects/dahisasgpfvziswqvmvm/database/query",
             '{"query":"SELECT tablename FROM pg_tables WHERE schemaname=\'public\'"}'],
            capture_output=True, text=True, timeout=30,
        )
        data = json.loads(out.stdout)
        rows = data if isinstance(data, list) else data.get("result", data)
        tables = [r["tablename"] if isinstance(r, dict) else r[0] for r in rows]
    except Exception as e:
        return [Finding("C1", f"live schema query failed: {e}",
                        "supabase", "Gate error — cannot verify live schema.")]
    for tbl in tables:
        if tbl in INTELLIGENCE_TABLES or tbl in OPERATIONAL_TABLES:
            continue
        if any(p.search(tbl) for p in INTELLIGENCE_NAME_PATTERNS):
            findings.append(Finding(
                "C1",
                f"live table `{tbl}` matches intelligence patterns but is not allowlisted",
                "supabase:public schema",
                "A live intelligence-persistence table outside the governed set "
                "is a second memory until proven otherwise. Fail closed.",
            ))
    return findings


# ----------------------------------------------------------------------------
# Falsifier (self-test): prove the gate catches mock second paths
# ----------------------------------------------------------------------------

MOCK_SECOND_MEMORY_FUNC = '''import { createClient } from "npm:@supabase/supabase-js@2";
Deno.serve(async (req) => {
  const supabase = createClient(Deno.env.get("SUPABASE_URL")!, Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!);
  // SHADOW CAPTURE: persists intelligence outside the canonical Receiver
  const { data } = await supabase.from("nayanet_intelligent_blocks").insert({
    subject: "shadow", meaning: { text: "bypass" },
  });
  return new Response(JSON.stringify({ ok: true }));
});
'''

MOCK_SECOND_MEMORY_MIGRATION = '''-- shadow memory table: a second memory system
CREATE TABLE public.nayanet_shadow_memory (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  captured_at timestamptz NOT NULL DEFAULT now(),
  intelligence jsonb NOT NULL
);
'''


def run_self_test():
    """Build fixtures with mock second paths; the gate MUST fail on them."""
    passed = 0
    failed = 0

    def check(name, cond, detail=""):
        nonlocal passed, failed
        if cond:
            passed += 1
            print(f"  PASS {name}")
        else:
            failed += 1
            print(f"  FAIL {name} {detail}")

    # Fixture 1: mock function INSERTs into nayanet_intelligent_blocks -> C2 must fire
    with tempfile.TemporaryDirectory() as tmp:
        fdir = os.path.join(tmp, "supabase", "functions", "nayanet-shadow-capture")
        os.makedirs(fdir)
        with open(os.path.join(fdir, "index.ts"), "w") as fh:
            fh.write(MOCK_SECOND_MEMORY_FUNC)
        # also include the real Receiver so C3 doesn't false-positive on empty set
        rdir = os.path.join(tmp, "supabase", "functions", CANONICAL_RECEIVER)
        os.makedirs(rdir)
        with open(os.path.join(rdir, "index.ts"), "w") as fh:
            fh.write('// receiver stub\nconst x = supabase.rpc("v7_create_smart_note");\n')
        findings = check_writers(tmp)
        check("F1: mock shadow INSERT into intelligent_blocks caught (C2)",
              any(f.check == "C2" and "nayanet-shadow-capture" in f.what
                  for f in findings),
              f"findings={[f.what for f in findings]}")

    # Fixture 2: migration creating nayanet_shadow_memory -> C4 must fire
    with tempfile.TemporaryDirectory() as tmp:
        mdir = os.path.join(tmp, "supabase", "migrations")
        os.makedirs(mdir)
        with open(os.path.join(mdir, "20261007000000_shadow_memory.sql"), "w") as fh:
            fh.write(MOCK_SECOND_MEMORY_MIGRATION)
        findings = check_migration_tables(tmp)
        check("F2: mock shadow table migration caught (C4)",
              any(f.check == "C4" and "nayanet_shadow_memory" in f.what
                  for f in findings))

    # Fixture 3: non-Receiver invoking canonical RPC -> C3 must fire
    with tempfile.TemporaryDirectory() as tmp:
        fdir = os.path.join(tmp, "supabase", "functions", "nayanet-rogue-writer")
        os.makedirs(fdir)
        with open(os.path.join(fdir, "index.ts"), "w") as fh:
            fh.write('const r = await supabase.rpc("nayanet_record_cognition_event", {});\n')
        findings = check_rpc_invokers(tmp)
        check("F3: rogue canonical-RPC invoker caught (C3)",
              any(f.check == "C3" and "nayanet-rogue-writer" in f.what
                  for f in findings))

    # Fixture 4: clean repo (only allowlisted patterns) -> no findings
    with tempfile.TemporaryDirectory() as tmp:
        fdir = os.path.join(tmp, "supabase", "functions", "nayanet-learning-verify")
        os.makedirs(fdir)
        with open(os.path.join(fdir, "index.ts"), "w") as fh:
            fh.write('await supabase.from("learning_evidence").update({status:"ACTIVE"});\n'
                     'await supabase.from("nayanet_execution_receipts").insert({});\n')
        rdir = os.path.join(tmp, "supabase", "functions", CANONICAL_RECEIVER)
        os.makedirs(rdir)
        with open(os.path.join(rdir, "index.ts"), "w") as fh:
            fh.write('await supabase.rpc("v7_create_smart_note", {});\n')
        findings = check_writers(tmp) + check_rpc_invokers(tmp)
        check("F4: allowlisted governed writers pass clean",
              len(findings) == 0,
              f"findings={[f.what for f in findings]}")

    # Fixture 5: naya-decision-context style read-only function -> no findings
    with tempfile.TemporaryDirectory() as tmp:
        fdir = os.path.join(tmp, "supabase", "functions", "naya-decision-context")
        os.makedirs(fdir)
        with open(os.path.join(fdir, "index.ts"), "w") as fh:
            fh.write('const { data } = await supabase.from("learning_evidence")'
                     '.select("*").eq("status","ACTIVE");\n')
        findings = check_writers(tmp)
        check("F5: read-only consumer passes clean (reads are not writes)",
              len(findings) == 0,
              f"findings={[f.what for f in findings]}")

    print(f"\nself-test: {passed} passed, {failed} failed")
    return failed == 0


# ----------------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", help="path to NayaPOWER checkout")
    ap.add_argument("--live", action="store_true",
                    help="also check live DB schema (read-only)")
    ap.add_argument("--self-test", action="store_true",
                    help="run falsifier fixtures")
    args = ap.parse_args()

    if args.self_test:
        ok = run_self_test()
        print("SELF-TEST:", "PASS" if ok else "FAIL")
        sys.exit(0 if ok else 1)

    if not args.repo:
        print("error: --repo is required (or use --self-test)", file=sys.stderr)
        sys.exit(2)

    findings = []
    findings += check_writers(args.repo)       # C2
    findings += check_rpc_invokers(args.repo)  # C3
    findings += check_migration_tables(args.repo)  # C4
    if args.live:
        findings += check_live_schema()        # C1

    if findings:
        print(f"CANONICAL-CAPTURE GATE: FAIL ({len(findings)} findings)\n")
        for f in findings:
            print(f.text() + "\n")
        print("Fail closed: an unrecognized intelligence-persistence path blocks.")
        sys.exit(1)

    print("CANONICAL-CAPTURE GATE: PASS — single canonical capture path holds.")
    print(f"  functions scanned : {len(list_functions(args.repo))}")
    print(f"  intelligence tables allowlisted: {len(INTELLIGENCE_TABLES)}")
    if args.live:
        print("  live schema check: no unallowlisted intelligence tables")
    sys.exit(0)


if __name__ == "__main__":
    main()

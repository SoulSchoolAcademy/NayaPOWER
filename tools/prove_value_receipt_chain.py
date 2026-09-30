#!/usr/bin/env python3
"""Proof: V2.1 DECISION -> EXECUTION/EVENT -> SMARTLEDGER -> TYPED VALUE RECEIPT
        -> INDEPENDENT REREAD -> SAME CALCULATION.

Runs the full chain deterministically without a database:

  1. DECISION: evaluate candidates with the canonical V2.1 calculus and build
     the canonical ALIGNMENT_DECISION receipt.
  2. EVENT: wrap it in the typed SmartLedger envelope (inputs, evidence,
     verification state, value calculation, points derivation, provenance).
  3. SMARTLEDGER: record through the writer semantics of
     nayanet_record_value_receipt() (validate, owner isolation, idempotent
     unique key, hash chain) -- simulated in memory; the SQL migration
     implements the same contract in the database.
  4. RECEIPT: read the stored row back (JSON round-trip, as the DB returns it).
  5. REREAD: parse fresh and independently recompute the decision evaluation
     and the contribution value from the stored inputs alone.
  6. SAME CALCULATION: compare recomputed vs stated values and hashes.

Also proves the CONTRIBUTION_VALUE leg, including evidence-before-reward and
replay immutability.

Scope honesty: the SQL migration itself is syntax-verified (pglast) and ships
with supabase/tests/nayanet_value_receipts_v21_tests.sql for execution
against a real database. This script proves the deterministic Python half and
the writer contract the SQL mirrors.

Exit 0 = every link PASS. Exit 1 = any link FAIL.
"""

import copy
import hashlib
import json
import sys

sys.path.insert(0, ".")

from kernel.smart_ledger_value import (
    build_alignment_decision_receipt,
    build_contribution_value_receipt,
    classify_value_assessment,
    receipt_canonical_hash,
    recompute_contribution_from_receipt,
    recompute_decision_from_receipt,
    validate_value_receipt,
)
from kernel.value_calculus import (
    PVEstimate,
    Candidate,
    QualityProfile,
    RiskPolicy,
    build_decision_receipt,
    evaluate_candidates,
)

OWNER = "11111111-1111-1111-1111-111111111111"
ACTOR = "33333333-3333-3333-3333-333333333333"
TS = "2026-09-30T23:59:00+00:00"

links = []


def link(name, ok, detail=""):
    links.append((name, bool(ok), detail))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f" — {detail}" if detail else ""))


# ---------------------------------------------------------------- 1. DECISION
DIMS = ["objective_fit", "evidence_sufficiency", "applicability",
        "robustness", "reversibility", "blast_containment", "simplicity"]
q = {d: 9.5 for d in DIMS}
c = {d: 0.95 for d in DIMS}
hard = dict(lawful=True, rights_safe=True, privacy_safe=True, safety_safe=True)
conf = {k: 0.95 for k in ("B", "H", "C", "R")}


def pv(B):
    return PVEstimate(B, 1.0, 1.0, 0.5, conf, 5)


candidates = [
    Candidate("do_nothing", q, c, pv(5.0), authorized=True, is_baseline=True, **hard),
    Candidate("assess_note", q, c, pv(8.0), authorized=True, **hard),
]
profile = QualityProfile(profile_id="NAYAPOWER-DECISION", version="2.1",
                         objective="maximum responsible verified value",
                         min_evidence_count=2, relative_margin=0.10)
evaluation = evaluate_candidates(candidates, "do_nothing", profile, RiskPolicy())
inner = build_decision_receipt(
    decision_id="dec-proof-1", objective="prove the value receipt chain",
    baseline_id="do_nothing", stakeholders=["member"], horizon="session",
    evaluation=evaluation, authority_basis="human_director",
    evidence_refs=["note-1"], observation_window={"status": "closed"},
    verification="VERIFIED_PASS", delta_v_actual=2.0,
)
link("1. V2.1 DECISION evaluated + canonical receipt built",
     inner["receipt_type"] == "ALIGNMENT_DECISION" and evaluation["decision"] in
     ("EXECUTE", "BRIEF", "RESEARCH", "REWORK"),
     f"decision={evaluation['decision']} selected={evaluation['selected']}")

# ---------------------------------------------------------------- 2/3. EVENT + SMARTLEDGER
envelope = build_alignment_decision_receipt(
    decision_receipt=inner, owner_id=OWNER, source_table="value_decisions",
    source_id="dec-proof-1", recorded_by=ACTOR, recorded_at=TS)
contrib = build_contribution_value_receipt(
    actor_id=ACTOR, owner_id=OWNER, source_table="smart_note_events",
    source_id="note-1", action_class="verified_intelligence",
    quality=0.8, relevance=0.9, verification=1.0, impact=0.7, novelty=0.8,
    verified_delta=3.0, points_per_unit=10.0, verification_state="VERIFIED_PASS",
    evidence=[{"source_table": "smart_note_receipts", "source_id": "r-1"}],
    recorded_by=ACTOR, recorded_at=TS)

ledger = {}  # (owner, source_table, source_id) -> row; simulates the SQL writer


def record(owner_id, receipt, privacy="PRIVATE"):
    validate_value_receipt(receipt)  # SQL: nayanet_value_receipt_validate()
    if receipt["provenance"]["owner_id"] != owner_id:
        raise ValueError("VALUE_RECEIPT_OWNER_MISMATCH")  # SQL: same
    key = (owner_id, receipt["provenance"]["source_table"],
           receipt["provenance"]["source_id"])
    if key in ledger:
        return ledger[key], False  # SQL: idempotent replay returns existing row
    prev = ""
    for (o, _, _), row in ledger.items():
        if o == owner_id:
            prev = row["event_hash"]
    event_hash = hashlib.sha256("|".join(
        [owner_id, receipt["receipt_type"],
         receipt["provenance"]["source_table"],
         receipt["provenance"]["source_id"], prev,
         receipt_canonical_hash(receipt)]).encode()).hexdigest()
    row = {"owner_id": owner_id, "event_type": receipt["receipt_type"],
           "source_table": receipt["provenance"]["source_table"],
           "source_id": receipt["provenance"]["source_id"],
           "privacy_classification": privacy,
           "value": copy.deepcopy(receipt), "event_hash": event_hash,
           "previous_chain_hash": prev or None}
    ledger[key] = row
    return row, True


row_d, created_d = record(OWNER, envelope)
row_c, created_c = record(OWNER, contrib)
link("2/3. EVENT recorded through existing SmartLedger writer semantics",
     created_d and created_c and row_d["value"]["engine"] ==
     "DECISION-VALUE-CALCULUS-V2.1",
     f"types={[row_d['event_type'], row_c['event_type']]} "
     f"hash={row_c['event_hash'][:12]}...")

# Replay must return the existing row unchanged (receipts immutable).
tampered = copy.deepcopy(contrib)
tampered["points_derivation"]["points_awarded"] = 999999
row_replay, created_replay = record(OWNER, tampered)
link("3b. REPLAY idempotent: same key returns existing row, no overwrite",
     not created_replay and row_replay["event_hash"] == row_c["event_hash"]
     and row_replay["value"]["points_derivation"]["points_awarded"]
     == contrib["points_derivation"]["points_awarded"])

# ---------------------------------------------------------------- 4. RECEIPT (reread)
reread_d = json.loads(json.dumps(row_d["value"]))  # DB round-trip
reread_c = json.loads(json.dumps(row_c["value"]))
link("4. TYPED VALUE RECEIPT reread independently from the ledger",
     classify_value_assessment(reread_d) == "VERIFIED_VALUE"
     and classify_value_assessment(reread_c) == "VERIFIED_VALUE"
     and reread_c["value_calculation"]["cvs"] ==
     contrib["value_calculation"]["cvs"])

# ---------------------------------------------------------------- 5/6. REREAD -> SAME CALCULATION
dec = recompute_decision_from_receipt(reread_d, candidates, profile, RiskPolicy())
con = recompute_contribution_from_receipt(reread_c)
link("5/6. DECISION independently recomputed from stored inputs: same result",
     dec["ok"], f"matches_decision={dec['matches_decision']} "
     f"matches_selected={dec['matches_selected']}")
link("5/6. CONTRIBUTION independently recomputed from stored inputs: same numbers",
     con["ok"], f"cvs={con['recomputed_cvs']:.4f} "
     f"points={con['recomputed_points']:.4f} hash={con['receipt_hash'][:12]}...")

# Tamper evidence: a mutated stored receipt must NOT recompute clean.
evil = copy.deepcopy(reread_c)
evil["value_calculation"]["cvs"] += 1.0
evil_check = recompute_contribution_from_receipt(evil)
link("6b. TAMPER detected: mutated receipt fails independent recomputation",
     not evil_check["ok"])

print()
failed = [n for n, ok, _ in links if not ok]
if failed:
    print(f"CHAIN BROKEN at: {failed}")
    sys.exit(1)
print(f"CHAIN COMPLETE: {len(links)}/{len(links)} links PASS — "
      "V2.1 DECISION -> EVENT -> SMARTLEDGER -> TYPED RECEIPT -> "
      "INDEPENDENT REREAD -> SAME CALCULATION")

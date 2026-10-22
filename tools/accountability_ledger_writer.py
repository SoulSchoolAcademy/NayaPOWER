#!/usr/bin/env python3
"""Accountability Ledger writer — the first writer of SYSTEM actions into the
one Smart Ledger (`public.nayanet_smart_ledger`).

Doctrine binding (NAYANODE/0025-VALUE-CALCULUS-SPECIFICATION-V1.md §12/§14/§18
and the Accountability Ledger spec, files/accountability-ledger-2026-10-22.*):

- NO second ledger. This module only *constructs* calls to the existing
  `public.nayanet_record_ledger_event(...)`. It never inserts into the table,
  and nothing in this repo executes the constructed calls — execution rides
  the governed production application queue (human tap), like every migration.
- Engagement is never an outcome. Runs/comments/openings are activity, counted
  once in `run_census`. An outcome exists only as an `outcome_verified` /
  `closure_on_proof` entry whose verification state is VERIFIED by a record
  independent of the actor.
- No points, no authority. System events carry `value = '{}'` (UNASSESSED).

What it does, from a *day record* (see
`tools/accountability_ledger/genesis_day_record_2026-10-22.json` for the
shape, or `--from-daily-census` for the daily job's census JSON):

1. builds the ordered, typed ledger entries for the day,
2. computes each entry's `event_hash` locally as a faithful mirror of
   `public.nayanet_smart_ledger_hash` (so the chain can be verified offline,
   before and after gated application),
3. renders the `nayanet_record_ledger_event(...)` call file for the queue,
4. verifies the constructed chain (`verify_chain`), and
5. computes the day's efficiency FROM THE ENTRIES (never from the census
   directly) — the ledger is the source the number is read from.

Hash mirror notes (must match the DB byte-for-byte):
- hash input = sha256 hex of the pipe-joined string
  owner|event_type|event_at|source_table|source_id|parent|previous_hash|
  evidence_refs|metadata, NULLs as ''.
- `event_at` renders as Postgres `timestamptz::text` at UTC
  (`YYYY-MM-DD HH:MM:SS+00` for whole seconds). Verification reads against the
  DB must `SET TIME ZONE 'UTC'` first.
- jsonb fields render as canonical jsonb text (object keys ordered by byte
  length, then bytewise; `", "` / `": "` separators) — see `pg_jsonb_text`.
- the hashed metadata is the DB-augmented form: caller metadata merged with
  `{assessment_state, value_receipt_type}` (v1 events carry empty value, so
  UNASSESSED / null; `value_receipt_hash` appears only for non-empty value,
  which v1 never emits).
- hashed payloads (evidence_refs, metadata) may contain only strings,
  integers, booleans, null, arrays and objects — floats are rejected,
  because jsonb numeric rendering of non-integers is not serializer-stable.

Chain segments: a batch chains from `start_prev` (the current chain head
hash for the owner). Genesis uses `start_prev=None` — the system owner is a
new identity whose first entry starts the chain.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

SCHEMA = "accountability-ledger-writer/v1"
OWNER_TOKEN = "${ACCOUNTABILITY_LEDGER_OWNER_ID}"
FLAG_THRESHOLD_DAYS = 3

TAXONOMY_RANK = {
    "pr_landed": 10,
    "outcome_verified": 20,
    "closure_on_proof": 30,
    "scorecard_issued": 40,
    "gate_verdict": 50,
    "loop_flagged_zero_output": 60,
    "run_census": 70,
}
STATUSES = {"RECORDED", "VERIFIED", "QUALIFIED", "SUPERSEDED", "BLOCKED", "FAILED"}
PRIVACIES = {"PRIVATE", "SHARED", "COLLECTIVE", "PUBLIC"}
OUTCOME_TYPES = {"outcome_verified", "closure_on_proof"}

REQUIRED_METADATA = {
    "run_census": ["actor", "actor_kind", "day", "window_start", "window_end",
                   "actions_runs", "board_comments", "activity_units",
                   "prs_opened", "prs_merged", "prs_closed_unmerged",
                   "outcomes_verified_total", "merged_without_individual_verification"],
    "pr_landed": ["actor", "actor_kind", "day", "pr_number", "merge_commit_sha", "head_sha"],
    "outcome_verified": ["actor", "actor_kind", "day", "lane", "mechanism"],
    "closure_on_proof": ["actor", "actor_kind", "day"],
    "scorecard_issued": ["actor", "actor_kind", "day", "pr_number", "score", "head_sha", "verdict"],
    "gate_verdict": ["actor", "actor_kind", "day", "workflow", "run_id", "subject"],
    "loop_flagged_zero_output": ["actor", "actor_kind", "day", "mechanism",
                                 "consecutive_zero_days", "flag_threshold_days", "disposition"],
}


# --------------------------------------------------------------------------
# Postgres serialization mirrors
# --------------------------------------------------------------------------

def pg_jsonb_text(value) -> str:
    """Serialize a value the way Postgres renders jsonb::text."""
    if value is None:
        return "null"
    if value is True:
        return "true"
    if value is False:
        return "false"
    if isinstance(value, int):
        return str(value)
    if isinstance(value, str):
        return json.dumps(value, ensure_ascii=False)
    if isinstance(value, list):
        return "[" + ", ".join(pg_jsonb_text(v) for v in value) + "]"
    if isinstance(value, dict):
        keys = sorted(value.keys(), key=lambda k: (len(k.encode("utf-8")), k.encode("utf-8")))
        return "{" + ", ".join(
            json.dumps(k, ensure_ascii=False) + ": " + pg_jsonb_text(value[k]) for k in keys
        ) + "}"
    raise TypeError(f"unserializable jsonb value: {type(value)!r}")


def fmt_event_at(iso_text: str) -> str:
    """ISO-8601 UTC instant -> Postgres timestamptz::text at UTC."""
    dt = datetime.fromisoformat(iso_text.replace("Z", "+00:00"))
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    dt = dt.astimezone(timezone.utc)
    base = dt.strftime("%Y-%m-%d %H:%M:%S")
    if dt.microsecond:
        frac = f"{dt.microsecond:06d}".rstrip("0")
        base += "." + frac
    return base + "+00"


def day_of(iso_text: str) -> str:
    return fmt_event_at(iso_text)[:10]


# --------------------------------------------------------------------------
# Validation
# --------------------------------------------------------------------------

def _check_hashed_payload(value, path: str) -> None:
    if isinstance(value, float):
        raise ValueError(f"float forbidden in hashed payload at {path}: {value!r}")
    if isinstance(value, str) and any(ord(c) < 0x20 for c in value):
        raise ValueError(f"control character in hashed payload at {path}")
    if isinstance(value, dict):
        for k, v in value.items():
            _check_hashed_payload(v, f"{path}.{k}")
    elif isinstance(value, list):
        for i, v in enumerate(value):
            _check_hashed_payload(v, f"{path}[{i}]")


def validate_entry(entry: dict) -> None:
    et = entry.get("event_type")
    if et not in TAXONOMY_RANK:
        raise ValueError(f"unknown event_type: {et!r}")
    if entry.get("status") not in STATUSES:
        raise ValueError(f"bad status: {entry.get('status')!r}")
    if entry.get("privacy_classification") not in PRIVACIES:
        raise ValueError(f"bad privacy: {entry.get('privacy_classification')!r}")
    for field in ("source_table", "source_id", "event_at"):
        if not entry.get(field):
            raise ValueError(f"missing {field} for {et}")
    meta = entry.get("metadata") or {}
    for key in REQUIRED_METADATA[et]:
        if key not in meta:
            raise ValueError(f"{et} missing required metadata key {key!r}")
    _check_hashed_payload(entry.get("evidence_refs"), "evidence_refs")
    _check_hashed_payload(meta, "metadata")
    if et in OUTCOME_TYPES:
        ver = entry.get("verification") or {}
        if ver.get("state") != "VERIFIED":
            raise ValueError(f"{et} requires verification.state VERIFIED")
        for key in ("method", "verifier", "evidence_url"):
            if not ver.get(key):
                raise ValueError(f"{et} requires verification.{key}")
        if not entry.get("evidence_refs"):
            raise ValueError(f"{et} requires at least one evidence ref")
        producer = (entry.get("outcome") or {}).get("producer")
        if producer and producer == ver.get("verifier"):
            raise ValueError(f"{et}: verifier must differ from producer ({producer!r})")


# --------------------------------------------------------------------------
# Hashing + chain
# --------------------------------------------------------------------------

def augment_metadata(metadata: dict, value: dict) -> dict:
    """Mirror the DB function's metadata augmentation (v1: value is empty)."""
    if value:
        raise ValueError("v1 writer never attaches value receipts; value must be {}")
    merged = dict(metadata or {})
    merged["assessment_state"] = "UNASSESSED"
    merged["value_receipt_type"] = None
    return merged


def ledger_hash(owner_id, event_type, event_at_iso, source_table, source_id,
                parent_id, previous_hash, evidence_refs, augmented_metadata) -> str:
    parts = [
        owner_id or "",
        event_type or "",
        fmt_event_at(event_at_iso) if event_at_iso else "",
        source_table or "",
        source_id or "",
        parent_id or "",
        previous_hash or "",
        pg_jsonb_text(evidence_refs if evidence_refs is not None else []),
        pg_jsonb_text(augmented_metadata if augmented_metadata is not None else {}),
    ]
    return hashlib.sha256("|".join(parts).encode("utf-8")).hexdigest()


def compute_entry_hash(entry: dict, owner_id: str) -> str:
    return ledger_hash(
        owner_id,
        entry["event_type"],
        entry["event_at"],
        entry["source_table"],
        entry["source_id"],
        entry.get("parent_ledger_event_id"),
        entry.get("previous_chain_hash"),
        entry.get("evidence_refs") or [],
        augment_metadata(entry.get("metadata") or {}, entry.get("value") or {}),
    )


def verify_chain(entries: list[dict], owner_id: str, start_prev=None) -> bool:
    """Recompute every hash and every link. Any tamper -> False."""
    prev = start_prev
    for entry in entries:
        if entry.get("previous_chain_hash") != prev:
            return False
        if compute_entry_hash(entry, owner_id) != entry.get("event_hash"):
            return False
        prev = entry["event_hash"]
    return True


# --------------------------------------------------------------------------
# Entry construction from a day record
# --------------------------------------------------------------------------

def _base(day: str, actor: str, actor_kind: str) -> dict:
    return {"actor": actor, "actor_kind": actor_kind, "day": day}


def build_entries(day_record: dict, owner_id: str, start_prev=None) -> list[dict]:
    day = day_record["day"]
    producer = day_record.get("producer", "value-density-daily")
    window_end = day_record["window_end"]
    entries: list[dict] = []

    for pr in day_record.get("prs_landed", []):
        entries.append({
            "event_type": "pr_landed",
            "event_at": pr["merged_at"],
            "source_table": "github_pull_requests",
            "source_id": str(pr["number"]),
            "privacy_classification": "PUBLIC",
            "status": "RECORDED",
            "evidence_refs": [{"kind": "github_pr",
                                 "url": f"https://github.com/SoulSchoolAcademy/NayaPOWER/pull/{pr['number']}"}],
            "verification": {"state": "RECORDED"},
            "value": {},
            "outcome": {"merged": True},
            "learning_refs": [],
            "metadata": {**_base(day, pr["author"], "external"),
                         "pr_number": pr["number"],
                         "merge_commit_sha": pr["merge_commit_sha"],
                         "head_sha": pr["head_sha"]},
        })

    for oc in day_record.get("outcomes_verified", []):
        entries.append({
            "event_type": "outcome_verified",
            "event_at": window_end,
            "source_table": "accountability_census",
            "source_id": f"outcome:{day}:{oc['ref']}",
            "privacy_classification": "PUBLIC",
            "status": "VERIFIED",
            "evidence_refs": [{"kind": "evidence", "url": oc["evidence_url"]}],
            "verification": {"state": "VERIFIED", "method": oc["method"],
                             "verifier": oc["verifier"], "evidence_url": oc["evidence_url"]},
            "value": {},
            "outcome": {"verified": True, "kind": oc["kind"], "summary": oc["summary"]},
            "learning_refs": [],
            "metadata": {**_base(day, producer, "system"),
                         "lane": oc["lane"], "mechanism": oc["mechanism"]},
        })

    for cl in day_record.get("closures_on_proof", []):
        entries.append({
            "event_type": "closure_on_proof",
            "event_at": window_end,
            "source_table": cl["source_table"],
            "source_id": f"closure:{cl['object_ref']}:{day}",
            "privacy_classification": "PUBLIC",
            "status": "VERIFIED",
            "evidence_refs": [{"kind": "evidence", "url": cl["evidence_url"]}],
            "verification": {"state": "VERIFIED", "method": "closure on proof",
                             "verifier": cl["verifier"], "evidence_url": cl["evidence_url"]},
            "value": {},
            "outcome": {"closed": True, "basis": cl["basis"],
                        "producer": cl.get("closed_by", producer)},
            "learning_refs": [],
            "metadata": _base(day, producer, "system"),
        })

    for sc in day_record.get("scorecards", []):
        entries.append({
            "event_type": "scorecard_issued",
            "event_at": window_end,
            "source_table": "github_pull_requests",
            "source_id": f"scorecard:{sc['pr_number']}:{sc['comment_id']}",
            "privacy_classification": "PUBLIC",
            "status": "RECORDED",
            "evidence_refs": [{"kind": "github_comment", "url": sc["evidence_url"]}],
            "verification": {"state": "ISSUED", "method": "scorecard",
                             "evidence_url": sc["evidence_url"]},
            "value": {},
            "outcome": {},
            "learning_refs": [],
            "metadata": {**_base(day, sc["seat"], "seat"),
                         "pr_number": sc["pr_number"], "score": str(sc["score"]),
                         "head_sha": sc["head_sha"], "verdict": sc["verdict"]},
        })

    for gv in day_record.get("gate_verdicts", []):
        ver = {"state": gv["state"]}
        if gv.get("reason"):
            ver["reason"] = gv["reason"]
        entries.append({
            "event_type": "gate_verdict",
            "event_at": window_end,
            "source_table": "github_workflows",
            "source_id": f"gate:{gv['workflow']}:{gv['run_id']}",
            "privacy_classification": "PUBLIC",
            "status": "RECORDED",
            "evidence_refs": [{"kind": "evidence", "url": gv["evidence_url"]}],
            "verification": ver,
            "value": {},
            "outcome": {},
            "learning_refs": [],
            "metadata": {**_base(day, "gate:" + gv["workflow"], "system"),
                         "workflow": gv["workflow"], "run_id": str(gv["run_id"]),
                         "subject": gv["subject"]},
        })

    for fl in day_record.get("loop_flags", []):
        if fl["consecutive_zero_days"] < FLAG_THRESHOLD_DAYS:
            continue
        entries.append({
            "event_type": "loop_flagged_zero_output",
            "event_at": window_end,
            "source_table": "accountability_census",
            "source_id": f"loop-flag:{fl['mechanism']}:{day}",
            "privacy_classification": "PUBLIC",
            "status": "RECORDED",
            "evidence_refs": [{"kind": "census",
                                 "url": "https://github.com/SoulSchoolAcademy/NayaPOWER/issues/2793"}],
            "verification": {"state": "RECORDED"},
            "value": {},
            "outcome": {},
            "learning_refs": [],
            "metadata": {**_base(day, producer, "system"),
                         "mechanism": fl["mechanism"],
                         "consecutive_zero_days": fl["consecutive_zero_days"],
                         "flag_threshold_days": FLAG_THRESHOLD_DAYS,
                         "disposition": fl["disposition"]},
        })

    act = day_record["activity"]
    entries.append({
        "event_type": "run_census",
        "event_at": window_end,
        "source_table": "accountability_census",
        "source_id": f"census:{day}:{producer}",
        "privacy_classification": "PUBLIC",
        "status": "RECORDED",
        "evidence_refs": [{"kind": "census",
                             "url": "https://github.com/SoulSchoolAcademy/NayaPOWER/issues/2793"}],
        "verification": {"state": "RECORDED"},
        "value": {},
        "outcome": {},
        "learning_refs": [],
        "metadata": {**_base(day, producer, "system"),
                     "window_start": day_record["window_start"],
                     "window_end": window_end,
                     "actions_runs": act["actions_runs"],
                     "board_comments": act["board_comments"],
                     "activity_units": act["actions_runs"] + act["board_comments"],
                     "prs_opened": act["prs_opened"],
                     "prs_merged": act["prs_merged"],
                     "prs_closed_unmerged": act["prs_closed_unmerged"],
                     "outcomes_verified_total": len(day_record.get("outcomes_verified", []))
                                                + len(day_record.get("closures_on_proof", [])),
                     "merged_without_individual_verification":
                         act["merged_without_individual_verification"]},
    })

    entries.sort(key=lambda e: (fmt_event_at(e["event_at"]),
                                TAXONOMY_RANK[e["event_type"]],
                                e["source_id"]))
    seen = set()
    prev = start_prev
    for entry in entries:
        key = (entry["source_table"], entry["source_id"])
        if key in seen:
            raise ValueError(f"duplicate idempotency key: {key}")
        seen.add(key)
        entry["parent_ledger_event_id"] = None
        entry["previous_chain_hash"] = prev
        validate_entry(entry)
        entry["event_hash"] = compute_entry_hash(entry, owner_id)
        prev = entry["event_hash"]
    return entries


# --------------------------------------------------------------------------
# Efficiency — computed FROM the entries, never from the census
# --------------------------------------------------------------------------

def compute_efficiency(entries: list[dict]) -> dict:
    census = [e for e in entries if e["event_type"] == "run_census"]
    if len(census) != 1:
        raise ValueError(f"expected exactly one run_census entry, got {len(census)}")
    census = census[0]
    day = census["metadata"]["day"]
    actions = census["metadata"]["activity_units"]
    outcomes = [e for e in entries
                if e["event_type"] in OUTCOME_TYPES
                and (e.get("verification") or {}).get("state") == "VERIFIED"
                and (e.get("metadata") or {}).get("day") == day]
    by_mechanism: dict[str, int] = {}
    by_lane: dict[str, int] = {}
    for e in outcomes:
        m = (e.get("metadata") or {}).get("mechanism")
        if m:
            by_mechanism[m] = by_mechanism.get(m, 0) + 1
        lane = (e.get("metadata") or {}).get("lane")
        if lane:
            by_lane[lane] = by_lane.get(lane, 0) + 1
    n = len(outcomes)
    return {
        "day": day,
        "actions": actions,
        "verified_outcomes": n,
        "ratio_actions_per_outcome": (actions / n) if n else None,
        "efficiency_outcomes_per_action": (n / actions) if actions else None,
        "outcomes_by_mechanism": by_mechanism,
        "outcomes_by_lane": by_lane,
        "flagged_mechanisms": sorted({
            e["metadata"]["mechanism"] for e in entries
            if e["event_type"] == "loop_flagged_zero_output"}),
    }


# --------------------------------------------------------------------------
# SQL rendering for the gated application queue
# --------------------------------------------------------------------------

def _sql_literal(text: str) -> str:
    return "'" + text.replace("'", "''") + "'"


def _sql_json(obj) -> str:
    return _sql_literal(json.dumps(obj, ensure_ascii=False, sort_keys=True)) + "::jsonb"


def render_sql(entries: list[dict], owner_expr: str = OWNER_TOKEN) -> str:
    lines = [
        "-- ACCOUNTABILITY LEDGER — constructed writes (DO NOT APPLY BY HAND).",
        "-- Execution rides the governed production application queue (human tap),",
        "-- exactly like a migration. Substitute the system owner's auth.users uuid",
        f"-- for {OWNER_TOKEN} before applying; the token is not a uuid and will",
        "-- fail loudly if applied unsubstituted.",
        "-- Order matters: statements chain in file order. Replays are idempotent",
        "-- (the record function dedupes on owner+source_table+source_id).",
        "-- After applying, verify: SET TIME ZONE 'UTC'; re-read the system owner's",
        "-- rows and run the writer's verify_chain over the stored fields — the",
        "-- stored event_hash values must equal the precomputed hashes in the",
        "-- entries artifact shipped with this file.",
        "begin;",
    ]
    for e in entries:
        lines.append(
            "select public.nayanet_record_ledger_event("
            f"{_sql_literal(owner_expr)}::uuid, "
            f"{_sql_literal(e['event_type'])}, "
            f"{_sql_literal(e['source_table'])}, "
            f"{_sql_literal(e['source_id'])}, "
            f"{_sql_literal(e['event_at'])}::timestamptz, "
            "null, "
            f"{_sql_literal(e['privacy_classification'])}, "
            f"{_sql_literal(e['status'])}, "
            f"{_sql_json(e.get('evidence_refs') or [])}, "
            f"{_sql_json(e.get('verification') or {})}, "
            "'{}'::jsonb, "
            f"{_sql_json(e.get('outcome') or {})}, "
            f"{_sql_json(e.get('learning_refs') or [])}, "
            f"{_sql_json(e.get('metadata') or {})}, "
            "null);"
        )
    lines.append("commit;")
    return "\n".join(lines) + "\n"


# --------------------------------------------------------------------------
# Daily-census adapter (nayapower-value-density-daily outputs)
# --------------------------------------------------------------------------

def day_record_from_daily_census(census: dict, state: dict | None) -> dict:
    window = census["window"]
    details = census.get("merged_pr_details") or {}
    prs = []
    for num, d in details.items():
        prs.append({
            "number": int(num),
            "author": d.get("author", "unknown"),
            "merged_at": d["merged_at"],
            "merge_commit_sha": d["merge_commit_sha"],
            "head_sha": d["head_sha"],
        })
    prs.sort(key=lambda p: p["merged_at"])
    flags = []
    for name, m in ((state or {}).get("mechanisms") or {}).items():
        streak = m.get("consecutive_zero_days", 0)
        if streak >= FLAG_THRESHOLD_DAYS:
            flags.append({
                "mechanism": name,
                "consecutive_zero_days": streak,
                "disposition": m.get("note", "flagged by the daily value-density census"),
            })
    return {
        "schema": "accountability-ledger-day-record/v1",
        "producer": "value-density-daily",
        "day": day_of(window[1]),
        "window_start": window[0],
        "window_end": window[1],
        "activity": {
            "actions_runs": census["actions_runs_in_window"],
            "board_comments": census["board_comments_in_window"],
            "prs_opened": census.get("search_total_opened", len(census.get("prs_opened_in_window", []))),
            "prs_merged": census.get("search_total_merged", len(prs)),
            "prs_closed_unmerged": len(census.get("prs_closed_unmerged_in_window", [])),
            "merged_without_individual_verification": 0,
        },
        "prs_landed": prs,
        "outcomes_verified": [],
        "closures_on_proof": [],
        "scorecards": [],
        "gate_verdicts": [],
        "loop_flags": flags,
    }


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------

def _load_json(path: str):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest="cmd", required=True)

    b = sub.add_parser("build", help="day record -> entries + SQL + efficiency")
    b.add_argument("--day-record")
    b.add_argument("--from-daily-census")
    b.add_argument("--state", help="daily job state.json (with --from-daily-census)")
    b.add_argument("--owner-id", default=OWNER_TOKEN,
                   help="system owner uuid (or the substitution token for artifacts)")
    b.add_argument("--out-dir", required=True)

    v = sub.add_parser("verify", help="entries artifact -> chain verdict")
    v.add_argument("--entries", required=True)
    v.add_argument("--owner-id", required=True)

    e = sub.add_parser("efficiency", help="entries artifact -> efficiency JSON")
    e.add_argument("--entries", required=True)

    args = ap.parse_args(argv)

    if args.cmd == "build":
        if args.day_record:
            record = _load_json(args.day_record)
        else:
            census = _load_json(args.from_daily_census)
            state = _load_json(args.state) if args.state else None
            record = day_record_from_daily_census(census, state)
        entries = build_entries(record, args.owner_id)
        if not verify_chain(entries, args.owner_id):
            print("CHAIN SELF-VERIFICATION FAILED", file=sys.stderr)
            return 1
        out = Path(args.out_dir)
        out.mkdir(parents=True, exist_ok=True)
        (out / f"entries-{record['day']}.json").write_text(
            json.dumps(entries, indent=1, sort_keys=True, ensure_ascii=False) + "\n",
            encoding="utf-8")
        (out / f"writes-{record['day']}.sql").write_text(
            render_sql(entries, args.owner_id), encoding="utf-8")
        eff = compute_efficiency(entries)
        (out / f"efficiency-{record['day']}.json").write_text(
            json.dumps(eff, indent=1, sort_keys=True) + "\n", encoding="utf-8")
        print(json.dumps({"entries": len(entries),
                          "chain_head": entries[-1]["event_hash"],
                          "efficiency": eff}, indent=1, sort_keys=True))
        return 0

    if args.cmd == "verify":
        entries = _load_json(args.entries)
        ok = verify_chain(entries, args.owner_id)
        print("CHAIN VALID" if ok else "CHAIN INVALID")
        return 0 if ok else 1

    if args.cmd == "efficiency":
        entries = _load_json(args.entries)
        print(json.dumps(compute_efficiency(entries), indent=1, sort_keys=True))
        return 0

    return 2


if __name__ == "__main__":
    raise SystemExit(main())

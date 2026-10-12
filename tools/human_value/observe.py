#!/usr/bin/env python3
"""observe.py — the observed-experience instrument v1 CLI.

The machine PROPOSES; promotion is a deliberate, signed act, never automatic.

Commands:
  sweep       propose candidate matches + new observations as JSON (review surface)
  promote     validate and append an observed event; mark its candidate promoted
  expire      mark candidates past expires_at as unobserved (append-only)
  report      OBSERVED / UNOBSERVED / PENDING buckets + NULL sweep log + banner
  calibrate   pre-register a known-answer key (hash-pinned) and run the battery
  agreement   inter-collector agreement (Jaccard on observation triples)
  attack      demonstrate the adversarial attacks the schema must reject

Ledgers live under --ledgers (default: tools/human_value/ledgers). Tests and
calibration use temp dirs: this CLI never writes production ledgers unless
pointed at them explicitly.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from tools.human_value.observation_schema import (  # noqa: E402
    CHANNELS,
    SchemaError,
    expired_candidates,
    fold_candidates,
    project_to_schema,
    validate_candidate,
    validate_event_v2,
    validate_observation_ledger,
    validate_sweep,
)

INSTRUMENT = "observed-experience-instrument-v1"

OBSERVED_EVENTS = "observed-events.jsonl"
PENDING_CANDIDATES = "pending-candidates.jsonl"
OBSERVATION_SWEEPS = "observation-sweeps.jsonl"

CALIBRATION_CHECKS = ("known_answer", "two_seat_agreement", "adversarial_review")


# ---------------------------------------------------------------------------
# ledger IO (append-only)
# ---------------------------------------------------------------------------

def read_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    rows = []
    for i, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = line.strip()
        if not line:
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError as exc:
            raise SchemaError(f"{path.name} line {i}: invalid JSON ({exc})")
    return rows


def append_jsonl(path: Path, record: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(record, sort_keys=True, ensure_ascii=False) + "\n")


def sha256_of_file(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


# ---------------------------------------------------------------------------
# the collector rules (the mechanical heart of the instrument)
# ---------------------------------------------------------------------------

def match_candidate(observation: dict, folded: dict) -> str | None:
    """Mechanical match: same artifact (pr), same subject — or, for
    capability-level observations, the most recent pending candidate tagged
    with the same capability. No tag, no match: the observation stands alone
    (promotion null), exactly as the design requires.
    """
    subject = observation.get("subject")
    pr = observation.get("pr")
    artifact = observation.get("artifact")
    if pr is not None:
        for cid, cand in folded.items():
            if cand["status"] == "pending" and cand.get("pr") == pr and cand.get("subject", "human_self") == subject:
                return cid
        return None
    if artifact is not None:
        best, best_at = None, ""
        for cid, cand in folded.items():
            if cand["status"] != "pending":
                continue
            if cand.get("capability") != artifact:
                continue
            if cand["graded_at"] > best_at:
                best, best_at = cid, cand["graded_at"]
        return best
    return None


def resolve_conflict(observations: list[dict]) -> list[dict]:
    """Stated-vs-revealed conflict rule (design §1): if words and actions
    disagree on the same artifact, REVEALED wins for *continued* value and
    STATED wins for *momentary* experience. Both are recorded; the conflict
    and its resolution are labeled on each observation."""
    by_artifact: dict[str, list[dict]] = {}
    for obs in observations:
        by_artifact.setdefault(str(obs.get("pr") or obs.get("artifact") or "none"), []).append(obs)
    for artifact, group in by_artifact.items():
        kinds = {o["observation_kind"] for o in group}
        if "stated" in kinds and "revealed" in kinds:
            for o in group:
                o["conflict"] = {
                    "with": sorted(kinds - {o["observation_kind"]}),
                    "resolution": (
                        "revealed governs continued value; stated governs the momentary experience"
                    ),
                }
    return observations


def collect(raw_observations: list[dict], folded_candidates: dict) -> tuple[list[dict], list[dict]]:
    """Run the collector rules over raw observations.

    Returns (promotable, dropped): promotable = [(observation, candidate_id|None)]
    ready for deliberate promotion; dropped = [(observation, reason)] that fail
    closed. The collector proposes; it never promotes by itself.
    """
    observations = resolve_conflict([dict(o) for o in raw_observations])
    promotable, dropped = [], []
    for obs in observations:
        kind = obs.get("observation_kind")
        authorship = obs.get("authorship")
        if authorship == "uncertain":
            dropped.append((obs, "uncertain authorship — fail closed, no promotion"))
            continue
        if kind not in ("stated", "revealed", "corrected"):
            dropped.append((obs, f"unknown observation_kind {kind!r}"))
            continue
        cid = match_candidate(obs, folded_candidates)
        candidate = folded_candidates.get(cid) if cid else None
        if candidate and candidate.get("graded_by") == obs.get("observed_by"):
            dropped.append((obs, "assessor == collector — fail closed"))
            continue
        if candidate and candidate.get("built_by") and candidate["built_by"] in (
            obs.get("observed_by"),
            candidate.get("graded_by"),
        ):
            dropped.append((obs, "builder == collector or assessor — fail closed"))
            continue
        promotable.append((obs, cid))
    return promotable, dropped


# ---------------------------------------------------------------------------
# commands
# ---------------------------------------------------------------------------

def cmd_sweep(args: argparse.Namespace) -> int:
    channels = [c.strip() for c in args.channels.split(",") if c.strip()]
    bad = [c for c in channels if c not in CHANNELS]
    if bad:
        print(f"error: unknown channel(s) {bad} — known channels: {list(CHANNELS)}", file=sys.stderr)
        return 1
    raw = read_jsonl(Path(args.raw))
    candidates = fold_candidates(read_jsonl(Path(args.ledgers) / PENDING_CANDIDATES))
    promotable, dropped = collect(raw, candidates)
    # The review surface is honest: each proposal is pre-checked against the
    # same validation the signed promote step will run. A "would_reject"
    # proposal is still shown (the reviewer may fix and resubmit), never hidden.
    proposals = []
    for obs, cid in promotable:
        payload = project_to_schema(obs)
        payload["promotion"] = cid
        candidate = candidates.get(cid) if cid else None
        try:
            validate_event_v2(payload, candidate=candidate)
            validation = "would_pass"
        except SchemaError as exc:
            validation = f"would_reject: {exc}"
        proposals.append({"observation": obs, "candidate_id": cid, "promotion_validation": validation})
    proposal = {
        "instrument": INSTRUMENT,
        "watermark": args.since,
        "channels": channels,
        "proposed_promotions": proposals,
        "dropped": [{"observation": obs, "reason": reason} for obs, reason in dropped],
        "note": "PROPOSAL ONLY — promotion is a deliberate, signed act. Review, then promote.",
    }
    print(json.dumps(proposal, indent=2, ensure_ascii=False))
    return 0


def cmd_promote(args: argparse.Namespace) -> int:
    ledgers = Path(args.ledgers)
    payload = json.loads(args.observation) if args.observation.startswith("{") else json.loads(Path(args.observation).read_text())
    folded = fold_candidates(read_jsonl(ledgers / PENDING_CANDIDATES))
    candidate = folded.get(args.candidate) if args.candidate else None
    if args.candidate and candidate is None:
        print(f"error: candidate {args.candidate} not found — fail closed", file=sys.stderr)
        return 1
    if candidate and candidate["status"] != "pending":
        print(f"error: candidate {args.candidate} status is {candidate['status']}, not pending", file=sys.stderr)
        return 1
    # Append-only: the event is validated, then appended. Never edited in place.
    event = validate_event_v2(payload, candidate=candidate)
    append_jsonl(ledgers / OBSERVED_EVENTS, event)
    if candidate:
        append_jsonl(
            ledgers / PENDING_CANDIDATES,
            {
                "candidate_id": candidate["candidate_id"],
                "graded_value_type": candidate["graded_value_type"],
                "graded_units": candidate["graded_units"],
                "graded_by": candidate["graded_by"],
                "graded_at": candidate["graded_at"],
                "expires_at": candidate["expires_at"],
                "status": "promoted",
                "pr": candidate.get("pr"),
                "note": f"promoted by observed event {event['event_id']}",
            },
        )
    print(json.dumps({"promoted": event["event_id"], "candidate": args.candidate}, indent=2))
    return 0


def cmd_expire(args: argparse.Namespace) -> int:
    ledgers = Path(args.ledgers)
    folded = fold_candidates(read_jsonl(ledgers / PENDING_CANDIDATES))
    expired = expired_candidates(folded, args.as_of)
    for cid in expired:
        cand = folded[cid]
        append_jsonl(
            ledgers / PENDING_CANDIDATES,
            {
                "candidate_id": cid,
                "graded_value_type": cand["graded_value_type"],
                "graded_units": cand["graded_units"],
                "graded_by": cand["graded_by"],
                "graded_at": cand["graded_at"],
                "expires_at": cand["expires_at"],
                "status": "unobserved",
                "pr": cand.get("pr"),
                "note": f"expired at {args.as_of}: 21 days with no human observation",
            },
        )
    print(json.dumps({"expired": expired, "as_of": args.as_of}, indent=2))
    return 0


def calibration_banner(status: dict) -> str:
    done = [k for k in CALIBRATION_CHECKS if status.get(k) == "pass"]
    if len(done) == len(CALIBRATION_CHECKS):
        return "CALIBRATED — all three §5 checks passed."
    pending = [k for k in CALIBRATION_CHECKS if status.get(k) != "pass"]
    return f"FORMATIVE — calibration incomplete. Pending: {', '.join(pending)}. Do not cite these numbers as established metrics."


def cmd_report(args: argparse.Namespace) -> int:
    ledgers = Path(args.ledgers)
    events = validate_observation_ledger(read_jsonl(ledgers / OBSERVED_EVENTS))
    folded = fold_candidates(read_jsonl(ledgers / PENDING_CANDIDATES))
    sweeps = [validate_sweep(s) for s in read_jsonl(ledgers / OBSERVATION_SWEEPS)]

    week = args.week
    observed = [e for e in events if e.get("recorded_at", "") <= week]
    pending = [c for c in folded.values() if c["status"] == "pending"]
    unobserved = [c for c in folded.values() if c["status"] == "unobserved"]

    hv_week = sum(e["value_units"] for e in observed if e["value_type"] == "useful_outcome")
    dai_week = sum(e["value_units"] for e in observed if e["value_type"] == "attention_demanded")

    status = {}
    if args.calibration_status:
        status = json.loads(Path(args.calibration_status).read_text())
    report = {
        "instrument": INSTRUMENT,
        "week": week,
        "banner": calibration_banner(status),
        "buckets": {
            "OBSERVED": [{"event_id": e["event_id"], "kind": e["observation_kind"],
                          "value_type": e["value_type"], "units": e["value_units"],
                          "verbatim_hash": e["verbatim_hash"]} for e in observed],
            "UNOBSERVED": [{"candidate_id": c["candidate_id"], "graded_by": c["graded_by"],
                            "graded_value_type": c["graded_value_type"]} for c in unobserved],
            "PENDING": [{"candidate_id": c["candidate_id"], "expires_at": c["expires_at"]} for c in pending],
        },
        "metrics": {
            "hv_observed_units": hv_week,
            "dai_corrections": dai_week,
            "candidates_pending": len(pending),
            "unobserved_expiry_count": len(unobserved),
        },
        "null_sweep_log": [
            {"sweep_id": s["sweep_id"], "watermark": [s["watermark_start"], s["watermark_end"]],
             "found": s["observations_found"], "null": s["null_sweep"]} for s in sweeps
        ],
        "honesty_note": "UNOBSERVED is not zero value — it is 'no human observation exists.'",
    }
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0


def cmd_calibrate(args: argparse.Namespace) -> int:
    if args.action == "pin":
        key_path = Path(args.key)
        digest = sha256_of_file(key_path)
        pin = {
            "key_id": args.key_id,
            "key_sha256": digest,
            "pinned_at_utc": datetime.now(timezone.utc).isoformat(),
            "pinned_by": args.who,
            "note": "Answer key pinned BEFORE the instrument runs. No peeking: the key is hashed first, the collector runs second, the comparison is mechanical.",
        }
        out = Path(args.out) if args.out else Path(str(key_path) + ".pin.json")
        out.write_text(json.dumps(pin, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(pin, indent=2))
        return 0

    if args.action == "run":
        key = json.loads(Path(args.key).read_text())
        pin = json.loads(Path(args.pin).read_text())
        actual_digest = sha256_of_file(Path(args.key))
        if actual_digest != pin["key_sha256"]:
            print("error: answer key bytes changed after pinning — calibration INVALID", file=sys.stderr)
            return 1
        # The instrument runs end to end: the collector PROPOSES, the schema
        # VALIDATES, and only valid events count. A dropped proposal is the
        # defense working, not a failure — unless the key expected it.
        raw = read_jsonl(Path(args.raw))
        candidates = fold_candidates(read_jsonl(Path(args.candidates)))
        result = run_battery(key, pin["key_sha256"], raw, candidates)
        print(json.dumps(result, indent=2))
        out = Path(args.out) if args.out else None
        if out:
            out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
        return 0 if result["match"] else 1


def observation_triples(observations: list[dict]) -> set[tuple]:
    return {
        (o["verbatim_hash"], o["observation_kind"], str(o.get("pr") or o.get("artifact") or "none"))
        for o in observations
    }


def cmd_agreement(args: argparse.Namespace) -> int:
    a = read_jsonl(Path(args.sweep_a))
    b = read_jsonl(Path(args.sweep_b))
    result = run_agreement_measure(a, b)
    result["a_only"] = sorted(observation_triples(a) - observation_triples(b))
    result["b_only"] = sorted(observation_triples(b) - observation_triples(a))
    print(json.dumps(result, indent=2))
    return 0 if result["pass"] else 1


def cmd_calibration_report(args: argparse.Namespace) -> int:
    """Run the full §5 calibration plan in one mechanical shot:

    pin the answer key (no peeking) -> known-answer battery -> inter-collector
    agreement -> the three adversarial attacks. Emits one calibration report.
    """
    fx = Path(args.fixtures)
    key_path = fx / "known_answer_key.json"
    key = json.loads(key_path.read_text())
    key_sha256 = sha256_of_file(key_path)  # pinned first, before anything runs

    raw = read_jsonl(fx / "known_answer_raw.jsonl")
    candidates = fold_candidates(read_jsonl(fx / "known_answer_candidates.jsonl"))
    battery = run_battery(key, key_sha256, raw, candidates)

    sweep_a = [o for o in raw if o.get("event_id", "").startswith("OBS-FIX-20261012-00")]
    sweep_b = read_jsonl(fx / "sweep_b.jsonl")
    agreement = run_agreement_measure(sweep_a, sweep_b)

    attacks = [run_attack(k) for k in ("graded_phantom", "uncertain_authorship", "self_observation")]

    status = {
        "known_answer": "pass" if battery["match"] else "fail",
        # Provisional: both passes authored by the calibration runner.
        # A real second seat flips this to pass/fail independently.
        "two_seat_agreement": "provisional-pass" if agreement["pass"] else "fail",
        "adversarial_review": "pass" if all(a["rejected"] for a in attacks) else "fail",
    }
    report = {
        "instrument": INSTRUMENT,
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "key_sha256": key_sha256,
        "battery": battery,
        "agreement": agreement,
        "agreement_note": "single-author two-pass simulation (different collector seats, one fresh pass). "
                          "The §5 check requires two INDEPENDENT seats — pending.",
        "attacks": attacks,
        "attacks_note": "self-administered. Coda 1's independent adversarial review — pending.",
        "calibration_status": status,
        "banner": calibration_banner(status),
    }
    out = args.out
    print(json.dumps(report, indent=2))
    if out:
        Path(out).write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    ok = battery["match"] and agreement["pass"] and all(a["rejected"] for a in attacks)
    return 0 if ok else 1


def attack_probe(kind: str) -> tuple[dict, str]:
    """Build one named adversarial probe. Returns (event_payload, name)."""
    base_event = {
        "schema_version": "2",
        "event_id": "OBS-ATTACK-001",
        "recorded_at": "2026-10-12",
        "value_type": "useful_outcome",
        "value_units": 1,
        "unit_description": "attack probe",
        "evidence": [{"kind": "feed_comment", "ref": "https://github.com/SoulSchoolAcademy/NayaPOWER/issues/2154#issuecomment-1"}],
        "observation_kind": "stated",
        "subject": "human_self",
        "observed_by": "naya-mu",
        "observed_at": "2026-10-12T06:00:00Z",
        "collected_at": "2026-10-12T07:00:00Z",
        "verbatim_hash": "sha256:" + "ab" * 32,
        "authorship": "direct",
        "collector_inference": "attack probe",
        "promotion": None,
    }
    if kind == "graded_phantom":
        # A grader's score smuggled in as an observation: no human trace.
        probe = dict(base_event)
        probe["evidence"] = []  # no evidence at all
        name = "graded phantom (grader score with zero human evidence)"
    elif kind == "uncertain_authorship":
        probe = dict(base_event)
        probe["authorship"] = "uncertain"
        probe["promotion"] = "CAND-20261012-001"
        name = "uncertain authorship carrying a promotion"
    elif kind == "self_observation":
        probe = dict(base_event)
        probe["observatory_subject"] = True
        probe["evidence"] = [{"kind": "receipt", "ref": "tools/human_value/ledgers/observation-sweeps.jsonl"}]
        name = "self-observation (observatory activity as human value)"
    else:
        raise ValueError(f"unknown attack {kind}")
    return probe, name


def run_attack(kind: str) -> dict:
    """Run one adversarial attack against schema validation.

    Each attack MUST be rejected. A rejection is the defense working.
    """
    probe, name = attack_probe(kind)
    try:
        validate_event_v2(probe)
    except SchemaError as exc:
        return {"attack": kind, "name": name, "rejected": True, "defense": str(exc)}
    return {"attack": kind, "name": name, "rejected": False, "defense": "NONE — SCHEMA HOLE"}


def run_battery(key: dict, key_sha256: str, raw: list[dict], candidates: dict) -> dict:
    """Run the known-answer battery: collector proposes, schema validates,
    only valid events count. Returns the mechanical comparison result."""
    promotable, collect_dropped = collect(raw, candidates)
    produced, dropped = [], []
    for obs, cid in promotable:
        payload = project_to_schema(obs)
        payload["promotion"] = cid
        candidate = candidates.get(cid) if cid else None
        try:
            validate_event_v2(payload, candidate=candidate)
        except SchemaError as exc:
            dropped.append((obs, str(exc)))
            continue
        produced.append(
            (obs["verbatim_hash"], obs["observation_kind"],
             str(obs.get("pr") or obs.get("artifact") or "none"))
        )
    produced = sorted(produced)
    expected = sorted(tuple(t) for t in key["expected_triples"])
    return {
        "key_id": key["key_id"],
        "key_sha256": key_sha256,
        "expected": len(expected),
        "produced": len(produced),
        "dropped_by_collector": len(collect_dropped),
        "dropped_by_schema": len(dropped),
        "drop_reasons": sorted({reason for _, reason in collect_dropped} | {r for _, r in dropped}),
        "match": produced == expected,
        "missing": sorted(set(expected) - set(produced)),
        "phantoms": sorted(set(produced) - set(expected)),
    }


def run_agreement_measure(a: list[dict], b: list[dict]) -> dict:
    ta, tb = observation_triples(a), observation_triples(b)
    union = ta | tb
    jaccard = len(ta & tb) / len(union) if union else 1.0
    return {
        "sweep_a": len(ta),
        "sweep_b": len(tb),
        "intersection": len(ta & tb),
        "union": len(union),
        "jaccard": round(jaccard, 4),
        "target": 0.8,
        "pass": jaccard >= 0.8,
    }


def cmd_attack(args: argparse.Namespace) -> int:
    try:
        result = run_attack(args.kind)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2))
    return 0 if result["rejected"] else 1


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="observe.py", description="Observed-experience instrument v1")
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("sweep", help="propose promotions as JSON (never auto-promotes)")
    s.add_argument("--raw", required=True, help="jsonl of raw observations")
    s.add_argument("--ledgers", required=True)
    s.add_argument("--since", required=True, help="watermark start")
    s.add_argument("--channels", default="c1,c2,c3")
    s.set_defaults(func=cmd_sweep)

    s = sub.add_parser("promote", help="validate + append an observed event")
    s.add_argument("--ledgers", required=True)
    s.add_argument("--candidate", default=None)
    s.add_argument("--observation", required=True, help="event JSON or path to JSON file")
    s.set_defaults(func=cmd_promote)

    s = sub.add_parser("expire", help="expire stale candidates (append-only)")
    s.add_argument("--ledgers", required=True)
    s.add_argument("--as-of", required=True)
    s.set_defaults(func=cmd_expire)

    s = sub.add_parser("report", help="weekly observation report")
    s.add_argument("--ledgers", required=True)
    s.add_argument("--week", required=True)
    s.add_argument("--calibration-status", default=None)
    s.set_defaults(func=cmd_report)

    s = sub.add_parser("calibrate", help="known-answer battery")
    s.add_argument("action", choices=["pin", "run"])
    s.add_argument("--key", required=True)
    s.add_argument("--key-id", default=None)
    s.add_argument("--who", default=None)
    s.add_argument("--pin", default=None)
    s.add_argument("--raw", default=None)
    s.add_argument("--candidates", default=None)
    s.add_argument("--out", default=None)
    s.set_defaults(func=cmd_calibrate)

    s = sub.add_parser("agreement", help="inter-collector agreement (Jaccard). "
        "The §5 target (>= 0.8) is meaningful only between two INDEPENDENT seats; "
        "two passes by the same author are provisional.")
    s.add_argument("--sweep-a", required=True)
    s.add_argument("--sweep-b", required=True)
    s.set_defaults(func=cmd_agreement)

    s = sub.add_parser("attack", help="adversarial attack vs schema")
    s.add_argument("--kind", required=True, choices=["graded_phantom", "uncertain_authorship", "self_observation"])
    s.set_defaults(func=cmd_attack)

    s = sub.add_parser("calibration-report", help="run the full §5 calibration plan in one shot")
    s.add_argument("--fixtures", required=True, help="path to tests/fixtures dir")
    s.add_argument("--out", default=None)
    s.set_defaults(func=cmd_calibration_report)

    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        return args.func(args)
    except SchemaError as exc:
        print(f"schema error: {exc}", file=sys.stderr)
        return 1
    except (OSError, json.JSONDecodeError, KeyError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

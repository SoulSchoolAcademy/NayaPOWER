#!/usr/bin/env python3
"""Error-signal loop: flag briefed-principle violations as learning.

When a worker violates a principle from the agent briefing (or a ratified
law), this tool catches it as a structured LEARNING EVENT — captured, with
provenance, emitted as a candidate lesson — not just a failure.

It loads the machine-readable principles checklist pinned to the briefing
fingerprint (tools/learning/principles_checklist.json) and scans a worker
artifact (lane-feed report, commit diff, PR body, or text file), emitting
one learning-event candidate per violation with exact provenance
(file, line, principle, quoted evidence).

Commands
--------
    python3 tools/learning/error_signal_loop.py scan \\
        --artifact PATH --kind lane-report|pr-body|commit-diff|text-file \\
        --source-ref REF --out events.jsonl [--append]

    python3 tools/learning/error_signal_loop.py checklist
    python3 tools/learning/error_signal_loop.py schema

Exit codes: 0 = scan completed (violations, if any, are reported as events);
            2 = fail-safe: input unreadable, malformed, or checklist invalid.
            A violation is data, not an error. A malformed input is.

Documented runner (cadence): run the scan over new lane-feed posts and PR
bodies on the 10-minute dispatcher tick via:
    python3 tools/learning/error_signal_loop.py scan --artifact <feed-text> \\
        --kind lane-report --source-ref "lane-1713:<comment-id>" --out \\
        ~/workspace/goals/super-brain-engine-to-10-10/hidden_files/learning-events.jsonl
and append the emitted candidates to the day's memory log for compounding.
"""
from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import json
import re
import sys
from pathlib import Path

TOOL_DIR = Path(__file__).resolve().parent
CHECKLIST_PATH = TOOL_DIR / "principles_checklist.json"
SCHEMA_VERSION = "learning-event-candidate/v1"

KINDS = ("lane-report", "pr-body", "commit-diff", "text-file")


# ---------------------------------------------------------------- checklist
def load_checklist(path: Path = CHECKLIST_PATH) -> dict:
    """Fail closed: any problem with the checklist is a fail-safe (exit 2)."""
    try:
        raw = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise FailSafe(f"cannot read checklist at {path}: {exc}") from exc
    try:
        checklist = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise FailSafe(f"checklist JSON malformed: {exc}") from exc
    if checklist.get("checklist") != "briefed-principles/v1":
        raise FailSafe("checklist identifier is not 'briefed-principles/v1'")
    fp = checklist.get("briefing", {}).get("fingerprint_sha256", "")
    if not re.fullmatch(r"[0-9a-f]{64}", fp or ""):
        raise FailSafe("checklist briefing fingerprint is not a valid sha256")
    rules = checklist.get("rules")
    if not isinstance(rules, list) or not rules:
        raise FailSafe("checklist has no rules")
    required = ("rule_id", "name", "plain_words", "briefing_line",
                "severity", "suggested_lesson", "violation_patterns",
                "required_positive_patterns", "kinds")
    for i, rule in enumerate(rules):
        for key in required:
            if key not in rule:
                raise FailSafe(f"rule #{i} missing key '{key}'")
        try:
            [re.compile(p) for p in rule["violation_patterns"]]
            [re.compile(p) for p in rule["required_positive_patterns"]]
        except re.error as exc:
            raise FailSafe(f"rule {rule['rule_id']} has bad regex: {exc}")
    return checklist


class FailSafe(Exception):
    """Malformed input / unreadable state: fail safe, never guess."""


# ------------------------------------------------------------------ reading
def read_artifact_lines(path: Path) -> list[str]:
    """Read text lines; binary or unreadable input fails safe (exit 2)."""
    try:
        raw = path.read_bytes()
    except OSError as exc:
        raise FailSafe(f"cannot read artifact at {path}: {exc}") from exc
    if not raw.strip():
        raise FailSafe("artifact is empty; nothing to scan")
    if b"\x00" in raw:
        raise FailSafe("artifact contains NUL bytes; refusing binary input")
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise FailSafe(f"artifact is not valid UTF-8: {exc}") from exc
    return text.splitlines()


# ---------------------------------------------------------------- scanning
def compile_rule(rule: dict) -> dict:
    return {
        **rule,
        "violation_res": [re.compile(p) for p in rule["violation_patterns"]],
        "positive_res": [re.compile(p) for p in rule["required_positive_patterns"]],
    }


def scan_lines(lines: list[str], rules: list[dict], kind: str) -> list[dict]:
    """Return raw violation dicts: (rule_id, line_no, quote)."""
    violations: list[dict] = []
    applicable = [compile_rule(r) for r in rules if kind in r["kinds"]]
    for lineno, line in enumerate(lines, start=1):
        effective, quote_line = line, line
        if kind == "commit-diff":
            if not line.startswith("+") or line.startswith("+++"):
                continue  # only scan added lines; evidence is the content
            quote_line = line[1:]
        for rule in applicable:
            positive = any(p.search(line) for p in rule["positive_res"])
            if positive:
                continue
            for vre in rule["violation_res"]:
                match = vre.search(line)
                if match:
                    violations.append({
                        "rule_id": rule["rule_id"],
                        "line_no": lineno,
                        "quote": quote_line.strip()[:240],
                    })
                    break  # one event per rule per line
    return violations


def positive_text(text: str, positive_res: list) -> bool:
    return any(p.search(text) for p in positive_res)


def scan(lines: list[str], checklist: dict, kind: str) -> list[dict]:
    """Full scan. P5 (briefing proof) is artifact-level: it fires at most
    once per artifact, only when the proof marker appears nowhere."""
    rules = checklist["rules"]
    per_line_rules = [r for r in rules if r["rule_id"] != "P5"]
    violations = scan_lines(lines, per_line_rules, kind)
    p5 = next((r for r in rules if r["rule_id"] == "P5"), None)
    if p5 is not None and kind in p5["kinds"]:
        cres = [re.compile(p) for p in p5["required_positive_patterns"]]
        if not positive_text("\n".join(lines), cres):
            violations.append({
                "rule_id": "P5",
                "line_no": 0,
                "quote": "(no briefing-proof marker found anywhere in artifact)",
            })
    return violations


# ------------------------------------------------------------------ events
def make_event(rule: dict, violation: dict, checklist: dict,
                kind: str, source_ref: str, artifact_path: str) -> dict:
    issued = _dt.datetime.now(_dt.timezone.utc).isoformat(timespec="seconds")
    digest = hashlib.sha256(
        f"{source_ref}:{violation['rule_id']}:{violation['line_no']}".encode()
    ).hexdigest()[:10]
    return {
        "schema": SCHEMA_VERSION,
        "event_id": f"le-{issued[:10].replace('-', '')}-{digest}",
        "issued_utc": issued,
        "checklist_fingerprint":
            checklist["briefing"]["fingerprint_sha256"],
        "principle": {
            "rule_id": rule["rule_id"],
            "name": rule["name"],
            "plain_words": rule["plain_words"],
            "briefing_line": rule["briefing_line"],
        },
        "violation": {
            "evidence_quote": violation["quote"],
            "evidence_location": {
                "file": artifact_path,
                "line": violation["line_no"],
            },
        },
        "source": {"kind": kind, "ref": source_ref},
        "suggested_lesson": rule["suggested_lesson"],
        "severity": rule["severity"],
    }


# ---------------------------------------------------------------------- cli
def cmd_scan(args: argparse.Namespace) -> int:
    try:
        checklist = load_checklist()
        lines = read_artifact_lines(Path(args.artifact))
    except FailSafe as exc:
        print(f"FAIL-SAFE: {exc}", file=sys.stderr)
        return 2
    kind = args.kind
    if kind not in KINDS:
        print(f"FAIL-SAFE: unknown kind '{kind}' (want one of {KINDS})",
              file=sys.stderr)
        return 2
    violations = scan(lines, checklist, kind)
    rule_by_id = {r["rule_id"]: r for r in checklist["rules"]}
    events = [make_event(rule_by_id[v["rule_id"]], v, checklist,
                         kind, args.source_ref, args.artifact)
              for v in violations]
    try:
        out_path = Path(args.out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        mode = "a" if args.append else "w"
        with out_path.open(mode, encoding="utf-8") as fh:
            for event in events:
                fh.write(json.dumps(event, ensure_ascii=False) + "\n")
    except OSError as exc:
        print(f"FAIL-SAFE: cannot write events to {args.out}: {exc}",
              file=sys.stderr)
        return 2
    by_rule: dict[str, int] = {}
    for v in violations:
        by_rule[v["rule_id"]] = by_rule.get(v["rule_id"], 0) + 1
    print(json.dumps({
        "status": "scanned",
        "artifact": args.artifact,
        "kind": kind,
        "lines_scanned": len(lines),
        "violations": len(violations),
        "by_rule": by_rule,
        "events_written": str(out_path),
    }, indent=2))
    return 0


def cmd_checklist(_args: argparse.Namespace) -> int:
    try:
        checklist = load_checklist()
    except FailSafe as exc:
        print(f"FAIL-SAFE: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(checklist, indent=2, ensure_ascii=False))
    return 0


def cmd_schema(_args: argparse.Namespace) -> int:
    print(json.dumps({
        "schema": SCHEMA_VERSION,
        "description": "A candidate lesson the system should learn: a "
                       "briefed-principle violation caught with exact "
                       "provenance. Candidate: not a ratified lesson until "
                       "a different seat confirms the violation is real.",
        "fields": {
            "schema": "schema version string",
            "event_id": "unique id: le-<date>-<digest>",
            "issued_utc": "ISO 8601 UTC timestamp",
            "checklist_fingerprint": "sha256 of briefing this rule set is "
                                     "pinned to",
            "principle": {"rule_id": "e.g. P1",
                          "name": "rule name",
                          "plain_words": "the principle in plain human words",
                          "briefing_line": "line in the pinned briefing"},
            "violation": {"evidence_quote": "verbatim quote from the artifact",
                          "evidence_location": {"file": "artifact path",
                                                "line": "1-based line, 0 = "
                                                        "artifact-level"}},
            "source": {"kind": "lane-report|pr-body|commit-diff|text-file",
                       "ref": "lane-feed comment id, PR number, commit sha"},
            "suggested_lesson": "distilled lesson in one plain sentence",
            "severity": "high|medium|low",
        },
    }, indent=2))
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Error-signal loop: principle violations -> learning events")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("scan", help="scan an artifact and emit event candidates")
    p.add_argument("--artifact", required=True, help="path to artifact file")
    p.add_argument("--kind", required=True, choices=KINDS)
    p.add_argument("--source-ref", default="manual",
                   help="e.g. lane-1713:<comment-id>, PR #1234, commit sha")
    p.add_argument("--out", required=True, help="JSONL output path for events")
    p.add_argument("--append", action="store_true",
                   help="append to --out instead of overwriting (dispatcher tick)")
    p.set_defaults(func=cmd_scan)

    p = sub.add_parser("checklist", help="print the pinned principles checklist")
    p.set_defaults(func=cmd_checklist)

    p = sub.add_parser("schema", help="print the learning-event schema")
    p.set_defaults(func=cmd_schema)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())

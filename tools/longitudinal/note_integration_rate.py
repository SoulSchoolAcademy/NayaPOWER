#!/usr/bin/env python3
"""C5.1 — Note→Doctrine Integration Rate (NDIR).

Measures distillation quality at the first compounding step: of the Smart Notes
(SN-####) a Naya deliberately contributes in a window, what fraction reach a
doctrine / protocol / knowledge file (INTEGRATED) or are REJECTED with a written
reason, within the window? A note sitting in limbo compounded nothing.

Privacy-architectural note: inputs are deliberately-contributed artifacts only —
a notes manifest, promotion receipts, and repo paths. There is no input channel
for private communications; the instrument cannot consume them by construction.

State precedence: INTEGRATED (promotion receipt says so, OR a doctrine file
cites the SN — reality beats paperwork; conflicts are reported) > REJECTED
(valid receipt with non-empty reason) > PENDING. PENDING older than the window
is STALE and fails the gate.

Exit codes: 0 = rate >= threshold AND zero stale; 1 = below threshold or stale
present; 2 = unreadable/malformed input.

Stdlib only. Deterministic given --now.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

VERSION = "1.0.0"
DEFAULT_WINDOW_DAYS = 30
DEFAULT_THRESHOLD = 0.60

SN_RE = re.compile(r"\bSN-(\d{3,})\b")
TEXT_SUFFIXES = {
    ".md", ".markdown", ".txt", ".json", ".py", ".yml", ".yaml",
    ".html", ".ts", ".js", ".mjs", ".sql",
}
DEFAULT_EXCLUDE_SUBSTRINGS = (
    # The note's own canonical files must never self-integrate.
    "SMART-NOTES",
    "PROMOTION-RECEIPTS",
    # Registry/index artifacts list every note by construction. A listing is
    # not doctrine: without this exclusion, REAL-TREE.json alone would
    # "integrate" the entire corpus and the metric would be theater.
    "REAL-TREE",
    "BRAIN-INDEX",
    "MACHINE-INTELLIGENCE",
    "lesson-index",
)


def parse_ts(value: str) -> datetime:
    """Parse an ISO-8601 date or datetime; naive values are treated as UTC."""
    text = str(value).strip()
    try:
        dt = datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError(f"unparseable timestamp: {value!r}") from exc
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def load_notes(path: Path) -> list[dict]:
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot read notes manifest {path}: {exc}") from exc
    items = raw["notes"] if isinstance(raw, dict) and "notes" in raw else raw
    if not isinstance(items, list):
        raise ValueError("notes manifest must be a list or {'notes': [...]}")
    notes = []
    for i, item in enumerate(items):
        if not isinstance(item, dict):
            raise ValueError(f"notes[{i}] must be an object")
        sn_id = str(item.get("sn_id", "")).strip()
        if not SN_RE.fullmatch(sn_id):
            raise ValueError(f"notes[{i}].sn_id {sn_id!r} is not a valid SN-#### id")
        try:
            contributed_at = parse_ts(item["contributed_at"])
        except (KeyError, ValueError) as exc:
            raise ValueError(f"notes[{i}] bad contributed_at: {exc}") from exc
        notes.append({
            "sn_id": sn_id,
            "contributed_at": contributed_at,
            "seat": str(item.get("seat", "UNKNOWN")).strip() or "UNKNOWN",
        })
    return notes


def load_receipts(directory: Path) -> tuple[dict, list[dict]]:
    """Return (receipts_by_sn, invalid_receipts)."""
    receipts: dict[str, dict] = {}
    invalid: list[dict] = []
    if not directory.exists():
        return receipts, invalid
    for path in sorted(directory.glob("*.json")):
        try:
            raw = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            invalid.append({"file": path.name, "reason": f"unreadable: {exc}"})
            continue
        sn_id = str(raw.get("sn_id", "")).strip()
        disposition = str(raw.get("disposition", "")).strip().upper()
        reason = str(raw.get("reason", "")).strip()
        if not SN_RE.fullmatch(sn_id):
            invalid.append({"file": path.name, "reason": f"bad sn_id {sn_id!r}"})
            continue
        if disposition not in ("INTEGRATED", "REJECTED"):
            invalid.append({"file": path.name, "reason": f"bad disposition {disposition!r}"})
            continue
        if disposition == "REJECTED" and not reason:
            invalid.append({"file": path.name, "reason": "REJECTED without a written reason"})
            continue
        decided_at = None
        if raw.get("decided_at"):
            try:
                decided_at = parse_ts(raw["decided_at"])
            except ValueError:
                invalid.append({"file": path.name, "reason": "bad decided_at"})
                continue
        receipts[sn_id] = {
            "disposition": disposition,
            "reason": reason,
            "doctrine_path": str(raw.get("doctrine_path", "")).strip(),
            "decided_at": decided_at.isoformat() if decided_at else None,
            "file": path.name,
        }
    return receipts, invalid


def scan_doctrine_citations(
    roots: list[Path], exclude_substrings: tuple[str, ...]
) -> dict[str, list[str]]:
    """Map sn_id -> sorted list of doctrine-relative paths citing it."""
    citations: dict[str, set[str]] = {}
    for root in roots:
        if not root.exists():
            continue
        for path in sorted(root.rglob("*")):
            if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
                continue
            rel = path.relative_to(root).as_posix()
            if any(s in rel or s in path.as_posix() for s in exclude_substrings):
                continue
            try:
                text = path.read_text(encoding="utf-8", errors="strict")
            except (OSError, UnicodeDecodeError):
                continue
            for match in SN_RE.finditer(text):
                sn_id = f"SN-{match.group(1)}"
                citations.setdefault(sn_id, set()).add(f"{root.as_posix()}/{rel}")
    return {sn: sorted(paths) for sn, paths in citations.items()}


def classify_note(
    note: dict,
    receipts: dict,
    citations: dict[str, list[str]],
    now: datetime,
    window_days: int,
) -> dict:
    sn_id = note["sn_id"]
    age_days = (now - note["contributed_at"]).total_seconds() / 86400.0
    receipt = receipts.get(sn_id)
    cited_paths = citations.get(sn_id, [])

    state = "PENDING"
    evidence: list[str] = []
    conflict = False
    if receipt and receipt["disposition"] == "INTEGRATED":
        state = "INTEGRATED"
        evidence.append(f"promotion receipt {receipt['file']}")
        if receipt["doctrine_path"]:
            evidence.append(f"doctrine target: {receipt['doctrine_path']}")
    if cited_paths:
        evidence.append(f"cited by {len(cited_paths)} doctrine file(s): {', '.join(cited_paths[:3])}"
                        + ("…" if len(cited_paths) > 3 else ""))
        if receipt and receipt["disposition"] == "REJECTED":
            # Reality beats paperwork: a rejected note that doctrine cites anyway
            # is integrated in fact. Flag the conflict loudly.
            state = "INTEGRATED"
            conflict = True
        elif state == "PENDING":
            state = "INTEGRATED"
    if state == "PENDING" and receipt and receipt["disposition"] == "REJECTED":
        state = "REJECTED"
        evidence.append(f"rejected with reason ({receipt['file']}): {receipt['reason'][:160]}")

    stale = state == "PENDING" and age_days > window_days
    return {
        "sn_id": sn_id,
        "seat": note["seat"],
        "contributed_at": note["contributed_at"].isoformat(),
        "age_days": round(age_days, 2),
        "state": state,
        "stale": stale,
        "receipt_conflict": conflict,
        "evidence": evidence,
    }


def compute_report(
    notes: list[dict],
    receipts: dict,
    citations: dict[str, list[str]],
    *,
    now: datetime,
    window_days: int,
    threshold: float,
    invalid_receipts: list[dict],
) -> dict:
    classified = [
        classify_note(n, receipts, citations, now, window_days) for n in notes
    ]
    integrated = sum(1 for c in classified if c["state"] == "INTEGRATED")
    rejected = sum(1 for c in classified if c["state"] == "REJECTED")
    stale = [c["sn_id"] for c in classified if c["stale"]]
    total = len(classified)
    rate = (integrated + rejected) / total if total else 0.0
    passed = rate >= threshold and not stale
    return {
        "component": "C5.1",
        "metric": "note_doctrine_integration_rate",
        "version": VERSION,
        "window_days": window_days,
        "threshold": threshold,
        "now": now.isoformat(),
        "total_notes": total,
        "integrated": integrated,
        "rejected": rejected,
        "pending": total - integrated - rejected,
        "stale": stale,
        "rate": round(rate, 4),
        "pass": passed,
        "invalid_receipts": invalid_receipts,
        "notes": classified,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="C5.1 — Note→Doctrine Integration Rate (NDIR)"
    )
    parser.add_argument("--notes-json", required=True, type=Path,
                        help="JSON manifest: list or {'notes': [...]} of "
                             "{sn_id, contributed_at, seat}")
    parser.add_argument("--receipts-dir", required=True, type=Path,
                        help="Directory of promotion receipt JSON files")
    parser.add_argument("--doctrine-roots", required=True,
                        help="Comma-separated repo dirs scanned for SN citations")
    parser.add_argument("--window-days", type=int, default=DEFAULT_WINDOW_DAYS)
    parser.add_argument("--threshold", type=float, default=DEFAULT_THRESHOLD)
    parser.add_argument("--now", default=None,
                        help="ISO timestamp overriding 'now' (determinism)")
    parser.add_argument("--exclude-substrings", default=",".join(DEFAULT_EXCLUDE_SUBSTRINGS),
                        help="Comma-separated path substrings excluded from the citation scan")
    parser.add_argument("--report-out", type=Path, default=None,
                        help="Write the JSON report to this path")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        now = parse_ts(args.now) if args.now else datetime.now(timezone.utc)
        notes = load_notes(args.notes_json)
    except ValueError as exc:
        print(f"input error: {exc}", file=sys.stderr)
        return 2
    if args.window_days <= 0:
        print("input error: --window-days must be positive", file=sys.stderr)
        return 2
    if not 0 < args.threshold <= 1:
        print("input error: --threshold must be in (0, 1]", file=sys.stderr)
        return 2

    roots = [Path(p.strip()) for p in args.doctrine_roots.split(",") if p.strip()]
    exclude = tuple(s for s in (x.strip() for x in args.exclude_substrings.split(",")) if s)
    receipts, invalid = load_receipts(args.receipts_dir)
    citations = scan_doctrine_citations(roots, exclude)
    report = compute_report(
        notes, receipts, citations,
        now=now, window_days=args.window_days, threshold=args.threshold,
        invalid_receipts=invalid,
    )
    text = json.dumps(report, indent=2)
    if args.report_out:
        args.report_out.write_text(text + "\n", encoding="utf-8")
    else:
        print(text)
    print(
        f"C5.1 NDIR: {report['integrated']} integrated + {report['rejected']} rejected "
        f"/ {report['total_notes']} notes = {report['rate']:.2%} "
        f"(threshold {report['threshold']:.0%}), stale={len(report['stale'])} "
        f"-> {'PASS' if report['pass'] else 'FAIL'}",
        file=sys.stderr,
    )
    return 0 if report["pass"] else 1


if __name__ == "__main__":
    sys.exit(main())

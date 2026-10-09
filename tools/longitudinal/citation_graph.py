#!/usr/bin/env python3
"""C5.2 — Cross-Seat Reuse Rate (CSRR).

Measures the compounding signature: of the Smart Notes (SN-####) a Naya
deliberately contributes in a window, what fraction are cited by AT LEAST ONE
OTHER seat's deliberate work inside the contribution's reuse window? Knowledge
only its author touches doesn't compound.

Attribution: author seat comes from the notes manifest; citing seat comes from
artifact frontmatter (`seat:` / `date:` lines in the first HEADER_LINES lines).
A reuse counts only when citing_seat != author_seat AND the citation date falls
inside [contributed_at, contributed_at + reuse_window_days].

Undated or unattributed citing files are REPORTED, never silently counted —
silence would be exactly the kind of quiet inflation this system exists to kill.

Privacy-architectural note: inputs are deliberately-contributed artifacts only.
There is no input channel for private communications.

Exit codes: 0 = rate >= threshold; 1 = below threshold; 2 = bad input.

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
DEFAULT_REUSE_WINDOW_DAYS = 60
DEFAULT_THRESHOLD = 0.25
HEADER_LINES = 40

SN_RE = re.compile(r"\bSN-(\d{3,})\b")
SEAT_RE = re.compile(r"(?im)^seat\s*:\s*(.+?)\s*$")
DATE_RE = re.compile(r"(?im)^date\s*:\s*(\d{4}-\d{2}-\d{2})\s*$")
TEXT_SUFFIXES = {
    ".md", ".markdown", ".txt", ".json", ".py", ".yml", ".yaml",
    ".html", ".ts", ".js", ".mjs", ".sql",
}


def parse_ts(value: str) -> datetime:
    text = str(value).strip()
    try:
        dt = datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError(f"unparseable timestamp: {value!r}") from exc
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def load_notes(path: Path) -> dict[str, dict]:
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot read notes manifest {path}: {exc}") from exc
    items = raw["notes"] if isinstance(raw, dict) and "notes" in raw else raw
    if not isinstance(items, list):
        raise ValueError("notes manifest must be a list or {'notes': [...]}")
    notes: dict[str, dict] = {}
    for i, item in enumerate(items):
        if not isinstance(item, dict):
            raise ValueError(f"notes[{i}] must be an object")
        sn_id = str(item.get("sn_id", "")).strip()
        if not SN_RE.fullmatch(sn_id):
            raise ValueError(f"notes[{i}].sn_id {sn_id!r} is not a valid SN-#### id")
        if sn_id in notes:
            raise ValueError(f"duplicate sn_id {sn_id} in notes manifest")
        try:
            contributed_at = parse_ts(item["contributed_at"])
        except (KeyError, ValueError) as exc:
            raise ValueError(f"notes[{i}] bad contributed_at: {exc}") from exc
        notes[sn_id] = {
            "sn_id": sn_id,
            "contributed_at": contributed_at,
            "seat": str(item.get("seat", "UNKNOWN")).strip() or "UNKNOWN",
        }
    return notes


def parse_header(text: str) -> tuple[str | None, str | None]:
    """Extract (seat, date-string) from the artifact's header lines."""
    header = "\n".join(text.splitlines()[:HEADER_LINES])
    seat_m = SEAT_RE.search(header)
    date_m = DATE_RE.search(header)
    seat = seat_m.group(1).strip() if seat_m else None
    date_s = date_m.group(1).strip() if date_m else None
    return seat, date_s


def scan_artifacts(root: Path) -> tuple[list[dict], list[dict], list[dict]]:
    """Return (edges, unattributed_files, undated_files).

    edges: {sn_id, citing_seat|None, citing_path, cited_at|None}
    """
    edges: list[dict] = []
    unattributed: list[dict] = []
    undated: list[dict] = []
    if not root.exists():
        return edges, unattributed, undated
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="strict")
        except (OSError, UnicodeDecodeError):
            continue
        sn_ids = sorted({f"SN-{m.group(1)}" for m in SN_RE.finditer(text)})
        if not sn_ids:
            continue
        seat, date_s = parse_header(text)
        rel = path.relative_to(root).as_posix()
        cited_at = None
        if date_s:
            try:
                cited_at = parse_ts(date_s)
            except ValueError:
                cited_at = None
        if seat is None:
            unattributed.append({"path": rel, "sn_ids": sn_ids})
        if cited_at is None:
            undated.append({"path": rel, "sn_ids": sn_ids})
        for sn_id in sn_ids:
            edges.append({
                "sn_id": sn_id,
                "citing_seat": seat,
                "citing_path": rel,
                "cited_at": cited_at.isoformat() if cited_at else None,
            })
    return edges, unattributed, undated


def compute_report(
    notes: dict[str, dict],
    edges: list[dict],
    unattributed: list[dict],
    undated: list[dict],
    *,
    reuse_window_days: int,
    threshold: float,
) -> dict:
    per_note: dict[str, dict] = {}
    for sn_id, note in notes.items():
        author = note["seat"]
        window_end = note["contributed_at"] + timedelta(days=reuse_window_days)
        qualifying: list[dict] = []
        for e in edges:
            if e["sn_id"] != sn_id or not e["citing_seat"] or not e["cited_at"]:
                continue
            if e["citing_seat"] == author:
                continue
            cited_at = parse_ts(e["cited_at"])
            if note["contributed_at"] <= cited_at <= window_end:
                qualifying.append(e)
        citing_seats = sorted({e["citing_seat"] for e in qualifying})
        per_note[sn_id] = {
            "sn_id": sn_id,
            "author_seat": author,
            "contributed_at": note["contributed_at"].isoformat(),
            "reused_cross_seat": bool(qualifying),
            "citing_seats": citing_seats,
            "qualifying_citations": len(qualifying),
        }
    total = len(per_note)
    reused = sum(1 for n in per_note.values() if n["reused_cross_seat"])
    rate = reused / total if total else 0.0
    passed = rate >= threshold
    return {
        "component": "C5.2",
        "metric": "cross_seat_reuse_rate",
        "version": VERSION,
        "reuse_window_days": reuse_window_days,
        "threshold": threshold,
        "total_notes": total,
        "reused_cross_seat": reused,
        "rate": round(rate, 4),
        "pass": passed,
        "unattributed_citing_files": unattributed,
        "undated_citing_files": undated,
        "notes": [per_note[sn] for sn in sorted(per_note)],
        "edges": edges,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="C5.2 — Cross-Seat Reuse Rate (CSRR)"
    )
    parser.add_argument("--notes-json", required=True, type=Path,
                        help="JSON manifest: list or {'notes': [...]} of "
                             "{sn_id, contributed_at, seat}")
    parser.add_argument("--artifacts-root", required=True, type=Path,
                        help="Root dir of contributed artifacts to scan for SN citations. "
                             "Citing files declare seat/date in header frontmatter.")
    parser.add_argument("--reuse-window-days", type=int,
                        default=DEFAULT_REUSE_WINDOW_DAYS)
    parser.add_argument("--threshold", type=float, default=DEFAULT_THRESHOLD)
    parser.add_argument("--report-out", type=Path, default=None,
                        help="Write the JSON report (incl. citation graph) to this path")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        notes = load_notes(args.notes_json)
    except ValueError as exc:
        print(f"input error: {exc}", file=sys.stderr)
        return 2
    if args.reuse_window_days <= 0:
        print("input error: --reuse-window-days must be positive", file=sys.stderr)
        return 2
    if not 0 < args.threshold <= 1:
        print("input error: --threshold must be in (0, 1]", file=sys.stderr)
        return 2

    edges, unattributed, undated = scan_artifacts(args.artifacts_root)
    report = compute_report(
        notes, edges, unattributed, undated,
        reuse_window_days=args.reuse_window_days, threshold=args.threshold,
    )
    text = json.dumps(report, indent=2)
    if args.report_out:
        args.report_out.write_text(text + "\n", encoding="utf-8")
    else:
        print(text)
    print(
        f"C5.2 CSRR: {report['reused_cross_seat']}/{report['total_notes']} notes reused "
        f"cross-seat = {report['rate']:.2%} (threshold {report['threshold']:.0%}), "
        f"unattributed={len(unattributed)}, undated={len(undated)} "
        f"-> {'PASS' if report['pass'] else 'FAIL'}",
        file=sys.stderr,
    )
    return 0 if report["pass"] else 1


if __name__ == "__main__":
    sys.exit(main())

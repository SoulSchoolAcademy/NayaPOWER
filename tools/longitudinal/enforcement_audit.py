#!/usr/bin/env python3
"""C5.6 — Mechanical Enforcement Rate (MER).

Measures whether newly ratified laws land in code, not just prose: of the laws
(and law-grade notes) ratified inside the window, what fraction name a
mechanical enforcement — a test, gate, CI check, or linter — within 30 days?

Mechanics:
- the laws manifest names each law ({law_id, ratified_at}); the tool scans
  --code-roots (which SHOULD be mechanism dirs: tests/, tools/, workflows/,
  scripts/) for whole-token mentions of the law id.
- a law counts as enforced iff it is mentioned in at least one scanned file
  whose modification time is no later than ratified_at + enforcement_days
  (default 30). Enforcement that predates ratification counts — landing early
  is fine. Paths matching --exclude-substrings (e.g. the law's own definition
  file) never count: a law naming itself is not machinery.
- honesty about the clock: mention timing is measured by file mtime, which is
  an OS-level proxy, not a semantic fact. The report carries the mtimes it
  used; a git-harvested first-appearance timestamp is the stronger future
  variant.

Privacy-architectural note: inputs are deliberately-contributed artifacts only
(laws manifest, repo paths). There is no input channel for private
communications.

DONE WHEN (design v2.0): the audit is in-repo and CI-runnable; on a live
window >= 0.50 of new laws carry a named mechanical enforcement.

Exit codes: 0 = in-window laws exist AND rate >= threshold; 1 = below bar
(including zero in-window laws — an audit of nothing proves nothing);
2 = unreadable/malformed input.

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
DEFAULT_ENFORCEMENT_DAYS = 30
DEFAULT_THRESHOLD = 0.50

TEXT_SUFFIXES = {
    ".md", ".markdown", ".txt", ".json", ".py", ".yml", ".yaml",
    ".html", ".ts", ".js", ".mjs", ".sql",
}
DEFAULT_EXCLUDE_SUBSTRINGS = (
    # A law's own definition/prose files naming it are not enforcement.
    "BRAIN/01-GOVERNANCE",
    "BRAIN/00-ACTIVATION",
    "LAWS",
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


def load_laws(path: Path) -> list[dict]:
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot read laws manifest {path}: {exc}") from exc
    items = raw["laws"] if isinstance(raw, dict) and "laws" in raw else raw
    if not isinstance(items, list):
        raise ValueError("laws manifest must be a list or {'laws': [...]}")
    laws = []
    for i, item in enumerate(items):
        if not isinstance(item, dict):
            raise ValueError(f"laws[{i}] must be an object")
        law_id = str(item.get("law_id", "")).strip()
        if not law_id:
            raise ValueError(f"laws[{i}] needs a non-empty law_id")
        try:
            ratified_at = parse_ts(item["ratified_at"])
        except (KeyError, ValueError) as exc:
            raise ValueError(f"laws[{i}] bad ratified_at: {exc}") from exc
        laws.append({
            "law_id": law_id,
            "ratified_at": ratified_at,
            "title": str(item.get("title", "")).strip(),
        })
    return laws


def scan_mentions(
    roots: list[Path], law_res: dict[str, re.Pattern],
    exclude_substrings: tuple[str, ...],
) -> dict[str, list[dict]]:
    """Map law_id -> list of {path, mtime} for files mentioning it."""
    mentions: dict[str, list[dict]] = {law_id: [] for law_id in law_res}
    for root in roots:
        if not root.exists():
            continue
        for path in sorted(root.rglob("*")):
            if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
                continue
            posix = path.as_posix()
            if any(s in posix for s in exclude_substrings):
                continue
            try:
                text = path.read_text(encoding="utf-8", errors="strict")
            except (OSError, UnicodeDecodeError):
                continue
            try:
                mtime = datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc)
            except OSError:
                continue
            for law_id, law_re in law_res.items():
                if law_re.search(text):
                    mentions[law_id].append({"path": posix, "mtime": mtime})
    return mentions


def audit_law(law: dict, mentions: list[dict], enforcement_days: int) -> dict:
    law_id = law["law_id"]
    deadline = law["ratified_at"] + timedelta(days=enforcement_days)
    in_time = [m for m in mentions if m["mtime"] <= deadline]
    in_time.sort(key=lambda m: m["mtime"])
    enforced = bool(in_time)
    first = in_time[0] if in_time else None
    return {
        "law_id": law_id,
        "title": law["title"],
        "ratified_at": law["ratified_at"].isoformat(),
        "enforced": enforced,
        "mechanism_files": [m["path"] for m in in_time],
        "mention_count": len(mentions),
        "first_enforcement_mtime": first["mtime"].isoformat() if first else None,
        "days_to_enforcement": (
            round((first["mtime"] - law["ratified_at"]).total_seconds() / 86400.0, 2)
            if first else None
        ),
        "late_mentions": sorted({m["path"] for m in mentions if m["mtime"] > deadline}),
    }


def compute_report(
    laws: list[dict],
    mentions: dict[str, list[dict]],
    *,
    now: datetime,
    window_days: int,
    enforcement_days: int,
    threshold: float,
) -> dict:
    window_start = now - timedelta(days=window_days)
    in_window = [l for l in laws if window_start <= l["ratified_at"] <= now]
    out_of_window = sorted(l["law_id"] for l in laws if l not in in_window)
    audited = [audit_law(l, mentions.get(l["law_id"], []), enforcement_days)
               for l in in_window]
    enforced = sum(1 for a in audited if a["enforced"])
    total = len(audited)
    rate = enforced / total if total else 0.0
    passed = total > 0 and rate >= threshold
    reasons = []
    if total == 0:
        reasons.append("no laws ratified inside the window: an audit of nothing proves nothing")
    elif rate < threshold:
        reasons.append(f"rate {rate:.2%} below threshold {threshold:.0%}")
    return {
        "component": "C5.6",
        "metric": "mechanical_enforcement_rate",
        "version": VERSION,
        "window_days": window_days,
        "enforcement_days": enforcement_days,
        "threshold": threshold,
        "now": now.isoformat(),
        "timing_note": (
            "mention timing measured by file mtime (OS proxy, not semantic fact); "
            "mtimes used are carried per law above"
        ),
        "laws_in_window": total,
        "laws_enforced": enforced,
        "rate": round(rate, 4),
        "pass": passed,
        "fail_reasons": reasons,
        "out_of_window": out_of_window,
        "laws": audited,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="C5.6 — Mechanical Enforcement Rate (MER): enforcement audit"
    )
    parser.add_argument("--laws-json", required=True, type=Path,
                        help="JSON manifest: list or {'laws': [...]} of "
                             "{law_id, ratified_at, title?}")
    parser.add_argument("--code-roots", required=True,
                        help="Comma-separated dirs scanned for law-id mentions "
                             "(use mechanism dirs: tests, tools, workflows, scripts)")
    parser.add_argument("--window-days", type=int, default=DEFAULT_WINDOW_DAYS)
    parser.add_argument("--enforcement-days", type=int, default=DEFAULT_ENFORCEMENT_DAYS,
                        help="Max days after ratification for enforcement to land")
    parser.add_argument("--threshold", type=float, default=DEFAULT_THRESHOLD)
    parser.add_argument("--now", default=None,
                        help="ISO timestamp overriding 'now' (determinism)")
    parser.add_argument("--exclude-substrings", default=",".join(DEFAULT_EXCLUDE_SUBSTRINGS),
                        help="Comma-separated path substrings excluded from the scan")
    parser.add_argument("--report-out", type=Path, default=None,
                        help="Write the JSON report to this path")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        now = parse_ts(args.now) if args.now else datetime.now(timezone.utc)
        laws = load_laws(args.laws_json)
    except ValueError as exc:
        print(f"input error: {exc}", file=sys.stderr)
        return 2
    for name, value in (("window-days", args.window_days),
                        ("enforcement-days", args.enforcement_days)):
        if value <= 0:
            print(f"input error: --{name} must be positive", file=sys.stderr)
            return 2
    if not 0 < args.threshold <= 1:
        print("input error: --threshold must be in (0, 1]", file=sys.stderr)
        return 2

    roots = [Path(p.strip()) for p in args.code_roots.split(",") if p.strip()]
    if not roots:
        print("input error: --code-roots names no directories", file=sys.stderr)
        return 2
    exclude = tuple(s for s in (x.strip() for x in args.exclude_substrings.split(",")) if s)
    law_res = {l["law_id"]: re.compile(r"\b" + re.escape(l["law_id"]) + r"\b")
               for l in laws}
    mentions = scan_mentions(roots, law_res, exclude)
    report = compute_report(
        laws, mentions, now=now,
        window_days=args.window_days, enforcement_days=args.enforcement_days,
        threshold=args.threshold,
    )
    text = json.dumps(report, indent=2)
    if args.report_out:
        args.report_out.write_text(text + "\n", encoding="utf-8")
    else:
        print(text)
    print(
        f"C5.6 MER: {report['laws_enforced']}/{report['laws_in_window']} laws "
        f"mechanically enforced = {report['rate']:.2%} "
        f"(threshold {report['threshold']:.0%}) "
        f"-> {'PASS' if report['pass'] else 'FAIL'}",
        file=sys.stderr,
    )
    return 0 if report["pass"] else 1


if __name__ == "__main__":
    sys.exit(main())

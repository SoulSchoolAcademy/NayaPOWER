#!/usr/bin/env python3
"""C5.4 — Behavioral-Change Evidence (BCE).

Measures whether captured lessons actually change behavior: for each lesson
that names a failure class, do recurrences of that failure class in her
subsequent PUBLIC artifacts (commits, PRs, merges, issue comments — supplied
as an artifacts manifest, an artifacts directory, or harvested from a git repo
via `git log`) drop to zero inside the lesson's post-capture window?

The lesson landed = the mistake stopped. A recurrence is any artifact inside
[captured_at, captured_at + post_days] whose text matches one of the lesson's
failure-class patterns (case-insensitive regex), excluding the lesson's own
capture artifact. Matches are reported with the pattern and an excerpt — never
hidden, never re-labeled.

Privacy-architectural note: inputs are deliberately-contributed PUBLIC
artifacts only. There is no input channel for private communications; the
instrument cannot consume DMs, private messages, or unshared drafts by
construction.

DONE WHEN (design v2.0): the scan runs green tracking >= 5 lessons with
defined failure classes, with zero recurrences inside each lesson's 30-day
post-capture window.

Exit codes: 0 = >= min lessons tracked AND zero recurrences; 1 = below bar;
2 = unreadable/malformed input (including an uncompilable pattern).

Stdlib only. Deterministic given --now.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

VERSION = "1.0.0"
DEFAULT_POST_DAYS = 30
DEFAULT_MIN_LESSONS = 5


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


def compile_patterns(patterns: list, where: str) -> list[re.Pattern]:
    compiled = []
    for p in patterns:
        if not isinstance(p, str) or not p.strip():
            raise ValueError(f"{where}: failure-class patterns must be non-empty strings")
        try:
            compiled.append(re.compile(p, re.IGNORECASE))
        except re.error as exc:
            raise ValueError(f"{where}: bad regex {p!r}: {exc}") from exc
    return compiled


def load_lessons(path: Path) -> list[dict]:
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot read lessons manifest {path}: {exc}") from exc
    items = raw["lessons"] if isinstance(raw, dict) and "lessons" in raw else raw
    if not isinstance(items, list):
        raise ValueError("lessons manifest must be a list or {'lessons': [...]}")
    lessons = []
    for i, item in enumerate(items):
        if not isinstance(item, dict):
            raise ValueError(f"lessons[{i}] must be an object")
        sn_id = str(item.get("sn_id", "")).strip()
        if not re.fullmatch(r"SN-\d{3,}", sn_id):
            raise ValueError(f"lessons[{i}].sn_id {sn_id!r} is not a valid SN-#### id")
        try:
            captured_at = parse_ts(item["captured_at"])
        except (KeyError, ValueError) as exc:
            raise ValueError(f"lessons[{i}] bad captured_at: {exc}") from exc
        fc = item.get("failure_class") or {}
        if not isinstance(fc, dict):
            raise ValueError(f"lessons[{i}].failure_class must be an object")
        name = str(fc.get("name", "")).strip()
        patterns = compile_patterns(fc.get("patterns", []), f"lessons[{i}] ({sn_id})")
        lessons.append({
            "sn_id": sn_id,
            "captured_at": captured_at,
            "seat": str(item.get("seat", "UNKNOWN")).strip() or "UNKNOWN",
            "failure_class_name": name or "(unnamed)",
            "failure_class_description": str(fc.get("description", "")).strip(),
            "patterns": patterns,
            "pattern_sources": [p.pattern for p in patterns],
            "capture_artifact_id": str(item.get("capture_artifact_id", "") or "").strip(),
        })
    return lessons


def load_artifact_object(item: dict, where: str) -> dict:
    if not isinstance(item, dict):
        raise ValueError(f"{where} must be an object")
    art_id = str(item.get("id", "")).strip()
    if not art_id:
        raise ValueError(f"{where} needs a non-empty id")
    try:
        date = parse_ts(item["date"])
    except (KeyError, ValueError) as exc:
        raise ValueError(f"{where} bad date: {exc}") from exc
    return {
        "id": art_id,
        "date": date,
        "kind": str(item.get("kind", "artifact")).strip() or "artifact",
        "text": str(item.get("text", "")),
    }


def load_artifacts_json(path: Path) -> list[dict]:
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot read artifacts manifest {path}: {exc}") from exc
    items = raw["artifacts"] if isinstance(raw, dict) and "artifacts" in raw else raw
    if not isinstance(items, list):
        raise ValueError("artifacts manifest must be a list or {'artifacts': [...]}")
    return [load_artifact_object(a, f"artifacts[{i}]") for i, a in enumerate(items)]


def load_artifacts_dir(directory: Path) -> list[dict]:
    if not directory.is_dir():
        raise ValueError(f"artifacts dir {directory} is not a directory")
    artifacts = []
    for path in sorted(directory.glob("*.json")):
        try:
            raw = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise ValueError(f"cannot read {path}: {exc}") from exc
        items = raw["artifacts"] if isinstance(raw, dict) and "artifacts" in raw else [raw]
        if not isinstance(items, list):
            raise ValueError(f"{path}: expected a list or {{'artifacts': [...]}}")
        for i, a in enumerate(items):
            artifacts.append(load_artifact_object(a, f"{path.name}[{i}]"))
    return artifacts


def harvest_git_log(repo: Path) -> list[dict]:
    """Harvest public commit history: id, author date, subject+body as text."""
    cmd = [
        "git", "-C", str(repo), "log", "--all",
        "--pretty=format:%H%x1f%aI%x1f%an%x1f%s%x1f%b%x1e",
    ]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise ValueError(f"git log failed in {repo}: {exc}") from exc
    if proc.returncode != 0:
        raise ValueError(f"git log failed in {repo}: {proc.stderr.strip()[:200]}")
    artifacts = []
    for record in proc.stdout.split("\x1e"):
        record = record.strip("\n")
        if not record.strip():
            continue
        parts = record.split("\x1f")
        if len(parts) < 5:
            continue
        sha, date_s, _author, subject, body = parts[0], parts[1], parts[2], parts[3], parts[4]
        try:
            date = parse_ts(date_s)
        except ValueError:
            continue
        artifacts.append({
            "id": sha,
            "date": date,
            "kind": "commit",
            "text": f"{subject}\n{body}".strip(),
        })
    return artifacts


def excerpt(text: str, match: re.Match, radius: int = 80) -> str:
    start = max(0, match.start() - radius)
    end = min(len(text), match.end() + radius)
    snippet = text[start:end].replace("\n", " ")
    return ("…" if start > 0 else "") + snippet + ("…" if end < len(text) else "")


def scan_lesson(lesson: dict, artifacts: list[dict], post_days: int,
                now: datetime) -> dict:
    window_start = lesson["captured_at"]
    window_end = min(window_start + timedelta(days=post_days), now)
    recurrences = []
    scanned = 0
    for art in artifacts:
        if art["id"] == lesson["capture_artifact_id"]:
            continue  # the lesson's own capture artifact is not a recurrence
        if not (window_start <= art["date"] <= window_end):
            continue
        scanned += 1
        for pattern in lesson["patterns"]:
            match = pattern.search(art["text"])
            if match:
                recurrences.append({
                    "sn_id": lesson["sn_id"],
                    "failure_class": lesson["failure_class_name"],
                    "artifact_id": art["id"],
                    "artifact_kind": art["kind"],
                    "artifact_date": art["date"].isoformat(),
                    "matched_pattern": pattern.pattern,
                    "excerpt": excerpt(art["text"], match),
                })
                break  # one hit per artifact is enough to name the recurrence
    return {
        "sn_id": lesson["sn_id"],
        "seat": lesson["seat"],
        "captured_at": lesson["captured_at"].isoformat(),
        "failure_class": lesson["failure_class_name"],
        "window_days": post_days,
        "window_end": window_end.isoformat(),
        "tracked": bool(lesson["patterns"]),
        "artifacts_scanned": scanned,
        "recurrences": recurrences,
        "recurrence_count": len(recurrences),
    }


def compute_report(lessons: list[dict], artifacts: list[dict], *,
                   now: datetime, post_days: int, min_lessons: int) -> dict:
    scanned = [scan_lesson(l, artifacts, post_days, now) for l in lessons]
    tracked = [s for s in scanned if s["tracked"]]
    untracked = [s["sn_id"] for s in scanned if not s["tracked"]]
    recurrences = [r for s in tracked for r in s["recurrences"]]
    enough = len(tracked) >= min_lessons
    clean = not recurrences
    passed = enough and clean
    reasons = []
    if not enough:
        reasons.append(
            f"only {len(tracked)} lessons with defined failure classes "
            f"(minimum {min_lessons})"
        )
    if not clean:
        reasons.append(f"{len(recurrences)} recurrence(s) of tracked failure classes")
    return {
        "component": "C5.4",
        "metric": "behavioral_change_evidence",
        "version": VERSION,
        "post_days": post_days,
        "min_lessons": min_lessons,
        "now": now.isoformat(),
        "lessons_total": len(scanned),
        "lessons_tracked": len(tracked),
        "lessons_without_failure_class": untracked,
        "recurrences": recurrences,
        "recurrence_count": len(recurrences),
        "pass": passed,
        "fail_reasons": reasons,
        "lessons": scanned,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="C5.4 — Behavioral-Change Evidence (BCE): recurrence scan"
    )
    parser.add_argument("--lessons-json", required=True, type=Path,
                        help="JSON manifest: list or {'lessons': [...]} of "
                             "{sn_id, captured_at, seat?, failure_class{name, "
                             "patterns[regex], description?}, capture_artifact_id?}")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--artifacts-json", type=Path,
                       help="JSON manifest of public artifacts "
                            "{id, date, kind?, text}")
    group.add_argument("--artifacts-dir", type=Path,
                       help="Directory of *.json artifact files")
    group.add_argument("--git-repo", type=Path,
                       help="Git repo whose public commit history is scanned")
    parser.add_argument("--post-days", type=int, default=DEFAULT_POST_DAYS)
    parser.add_argument("--min-lessons", type=int, default=DEFAULT_MIN_LESSONS)
    parser.add_argument("--now", default=None,
                        help="ISO timestamp overriding 'now' (determinism)")
    parser.add_argument("--report-out", type=Path, default=None,
                        help="Write the JSON report to this path")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        now = parse_ts(args.now) if args.now else datetime.now(timezone.utc)
        lessons = load_lessons(args.lessons_json)
        if args.artifacts_json is not None:
            artifacts = load_artifacts_json(args.artifacts_json)
        elif args.artifacts_dir is not None:
            artifacts = load_artifacts_dir(args.artifacts_dir)
        else:
            artifacts = harvest_git_log(args.git_repo)
    except ValueError as exc:
        print(f"input error: {exc}", file=sys.stderr)
        return 2
    for name, value in (("post-days", args.post_days),
                        ("min-lessons", args.min_lessons)):
        if value <= 0:
            print(f"input error: --{name} must be positive", file=sys.stderr)
            return 2

    report = compute_report(lessons, artifacts, now=now,
                            post_days=args.post_days,
                            min_lessons=args.min_lessons)
    text = json.dumps(report, indent=2, default=str)
    if args.report_out:
        args.report_out.write_text(text + "\n", encoding="utf-8")
    else:
        print(text)
    print(
        f"C5.4 BCE: {report['lessons_tracked']} lessons tracked "
        f"(min {report['min_lessons']}), "
        f"{report['recurrence_count']} recurrences in post windows "
        f"-> {'PASS' if report['pass'] else 'FAIL'}",
        file=sys.stderr,
    )
    return 0 if report["pass"] else 1


if __name__ == "__main__":
    sys.exit(main())

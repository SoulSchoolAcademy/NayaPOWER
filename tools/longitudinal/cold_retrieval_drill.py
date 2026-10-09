#!/usr/bin/env python3
"""C5.3 — Retrieval Precision on Contributed Knowledge (RPCK).

Measures the second compounding step: can a cold Naya — no prior context —
retrieve a contributed lesson through the governed knowledge corpus and show it
applied, using only the lesson's own retrieval surface (query terms) and its own
stated success criteria?

Mechanics (all machine-checkable; honest about what is NOT):
- RETRIEVED: every query term appears (case-insensitive substring) in at least
  one file under --knowledge-roots, and, when a knowledge_file is named, that
  file exists and contains every term. A lesson that cannot be found by its own
  retrieval surface does not compound, no matter how well written.
- APPLIED: at least one application_evidence entry carries a non-empty ref, and
  any named evidence_path exists and cites the lesson's SN id. Reality beats
  paperwork: an application claim with no checkable artifact does not count.
- Coldness receipts: the drill runs as a fresh process doing term search only —
  no conversational context exists to leak. Per lesson it writes a machine
  receipt recording exactly what was searched, which corpus files were examined
  (with sha256), and what was found. This is machine-RECORDED provenance, not
  proof of a model's inner state: model coldness is human-verified second, per
  the design (mechanical first, human-verified second). The receipt says so.

Privacy-architectural note: inputs are deliberately-contributed artifacts only
(lesson manifests, repo paths). There is no input channel for private
communications.

DONE WHEN (design v2.0): the drill runs green on >= 20 sampled lessons with
machine-checked coldness receipts, scoring >= 0.80 retrieved-and-applied.

Exit codes: 0 = sample >= 20 AND rate >= threshold; 1 = below bar;
2 = unreadable/malformed input.

Stdlib only. Deterministic given --now.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path

VERSION = "1.0.0"
DEFAULT_WINDOW_DAYS = 30
DEFAULT_MIN_LESSONS = 20
DEFAULT_THRESHOLD = 0.80

SN_RE = re.compile(r"\bSN-(\d{3,})\b")
TEXT_SUFFIXES = {
    ".md", ".markdown", ".txt", ".json", ".py", ".yml", ".yaml",
    ".html", ".ts", ".js", ".mjs", ".sql",
}


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


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


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
        if not SN_RE.fullmatch(sn_id):
            raise ValueError(f"lessons[{i}].sn_id {sn_id!r} is not a valid SN-#### id")
        try:
            contributed_at = parse_ts(item["contributed_at"])
        except (KeyError, ValueError) as exc:
            raise ValueError(f"lessons[{i}] bad contributed_at: {exc}") from exc
        query_terms = item.get("query_terms")
        if (not isinstance(query_terms, list) or not query_terms
                or not all(isinstance(t, str) and t.strip()
                           for t in query_terms)):
            raise ValueError(f"lessons[{i}] query_terms must be a non-empty list of strings")
        evidence = item.get("application_evidence", [])
        if not isinstance(evidence, list):
            raise ValueError(f"lessons[{i}] application_evidence must be a list")
        for j, ev in enumerate(evidence):
            if not isinstance(ev, dict) or not str(ev.get("ref", "")).strip():
                raise ValueError(
                    f"lessons[{i}].application_evidence[{j}] must be an object with a non-empty ref"
                )
        lessons.append({
            "sn_id": sn_id,
            "contributed_at": contributed_at,
            "knowledge_file": str(item.get("knowledge_file", "")).strip(),
            "query_terms": [t.strip() for t in query_terms],
            "success_criteria": str(item.get("success_criteria", "")).strip(),
            "application_evidence": [
                {"ref": str(ev.get("ref", "")).strip(),
                 "path": str(ev.get("path", "") or "").strip()}
                for ev in evidence
            ],
        })
    return lessons


def scan_corpus(roots: list[Path]) -> dict[str, str]:
    """Map relative path -> lowercase text for searchable corpus files."""
    corpus: dict[str, str] = {}
    for root in roots:
        if not root.exists():
            continue
        for path in sorted(root.rglob("*")):
            if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
                continue
            try:
                text = path.read_text(encoding="utf-8", errors="strict")
            except (OSError, UnicodeDecodeError):
                continue
            corpus[f"{root.as_posix()}/{path.relative_to(root).as_posix()}"] = text.lower()
    return corpus


def check_retrieval(
    lesson: dict, corpus: dict[str, str], repo_root: Path
) -> tuple[bool, list[str], list[dict]]:
    """Return (retrieved, missing_terms, examined_files[{path, sha256}])."""
    terms = [t.lower() for t in lesson["query_terms"]]
    examined: list[dict] = []
    target_text = ""
    if lesson["knowledge_file"]:
        target = repo_root / lesson["knowledge_file"]
        if not target.is_file():
            return False, terms, examined  # lesson is not where it claims to be
        try:
            target_text = target.read_text(encoding="utf-8", errors="strict").lower()
        except (OSError, UnicodeDecodeError):
            return False, terms, examined
        examined.append({
            "path": lesson["knowledge_file"],
            "sha256": sha256_file(target),
        })
    missing = []
    for term in terms:
        found = term in target_text if target_text else False
        if not found:
            found = any(term in text for text in corpus.values())
        if not found:
            missing.append(term)
    for rel, text in corpus.items():
        if any(t in text for t in terms):
            full = Path(rel)
            if full.is_file():
                examined.append({"path": rel, "sha256": sha256_file(full)})
    # de-duplicate examined entries, keep deterministic order
    seen: dict[str, dict] = {}
    for entry in examined:
        seen.setdefault(entry["path"], entry)
    examined = [seen[k] for k in sorted(seen)]
    return (not missing), missing, examined


def check_application(
    lesson: dict, repo_root: Path
) -> tuple[bool, list[dict]]:
    """Return (applied, per-evidence diagnostics)."""
    diagnostics = []
    valid = 0
    for ev in lesson["application_evidence"]:
        detail: dict = {"ref": ev["ref"], "path": ev["path"] or None, "valid": False}
        if not ev["path"]:
            # A bare ref is recorded but not machine-checkable: honest, not counted.
            detail["reason"] = "ref without path: recorded, not machine-checkable"
        else:
            target = repo_root / ev["path"]
            if not target.is_file():
                detail["reason"] = f"evidence path {ev['path']} does not exist"
            else:
                try:
                    text = target.read_text(encoding="utf-8", errors="strict")
                except (OSError, UnicodeDecodeError):
                    detail["reason"] = f"evidence path {ev['path']} unreadable"
                else:
                    if SN_RE.search(text) and lesson["sn_id"] in text:
                        detail["valid"] = True
                        valid += 1
                    else:
                        detail["reason"] = (
                            f"evidence path {ev['path']} does not cite {lesson['sn_id']}"
                        )
        diagnostics.append(detail)
    return valid > 0, diagnostics


def drill_lesson(
    lesson: dict, corpus: dict[str, str], repo_root: Path,
    drill_id: str, run_at: datetime,
) -> dict:
    retrieved, missing_terms, examined = check_retrieval(lesson, corpus, repo_root)
    applied, evidence_diag = check_application(lesson, repo_root)
    return {
        "sn_id": lesson["sn_id"],
        "contributed_at": lesson["contributed_at"].isoformat(),
        "query_terms": lesson["query_terms"],
        "success_criteria": lesson["success_criteria"],
        "retrieved": retrieved,
        "missing_terms": missing_terms,
        "applied": applied,
        "retrieved_and_applied": retrieved and applied,
        "evidence": evidence_diag,
        "coldness_receipt": {
            "receipt_id": f"RPCK-{lesson['sn_id']}-{run_at.strftime('%Y%m%d')}",
            "drill_id": drill_id,
            "sn_id": lesson["sn_id"],
            "query_terms": lesson["query_terms"],
            "corpus_files_examined": examined,
            "run_at": run_at.isoformat(),
            "isolation": (
                "retrieval by case-insensitive term search in a fresh process; "
                "no conversational context was used or was available"
            ),
            "attestation_limit": (
                "machine-recorded provenance only — it records what this drill "
                "did, not a model's inner state. Model coldness is human-verified "
                "second, per design v2.0 (mechanical first, human-verified second)."
            ),
        },
    }


def compute_report(
    lessons: list[dict],
    corpus: dict[str, str],
    *,
    repo_root: Path,
    now: datetime,
    window_days: int,
    min_lessons: int,
    threshold: float,
    max_lessons: int,
) -> dict:
    window_start = now - timedelta(days=window_days)
    in_window = [l for l in lessons if window_start <= l["contributed_at"] <= now]
    out_of_window = [l["sn_id"] for l in lessons if l not in in_window]
    # Deterministic sample: sort by sn_id, cap at max_lessons when set.
    in_window.sort(key=lambda l: l["sn_id"])
    sampled = in_window[:max_lessons] if max_lessons > 0 else in_window

    drill_id = uuid.uuid4().hex[:12]
    drilled = [drill_lesson(l, corpus, repo_root, drill_id, now) for l in sampled]
    hits = sum(1 for d in drilled if d["retrieved_and_applied"])
    n = len(drilled)
    rate = hits / n if n else 0.0
    sample_ok = n >= min_lessons
    passed = sample_ok and rate >= threshold
    reasons = []
    if not sample_ok:
        reasons.append(f"sample {n} below minimum {min_lessons}")
    if sample_ok and rate < threshold:
        reasons.append(f"rate {rate:.2%} below threshold {threshold:.0%}")
    return {
        "component": "C5.3",
        "metric": "cold_retrieval_precision",
        "version": VERSION,
        "window_days": window_days,
        "min_lessons": min_lessons,
        "threshold": threshold,
        "now": now.isoformat(),
        "drill_id": drill_id,
        "sampled_lessons": n,
        "retrieved_and_applied": hits,
        "rate": round(rate, 4),
        "pass": passed,
        "fail_reasons": reasons,
        "out_of_window": sorted(out_of_window),
        "lessons": drilled,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="C5.3 — Retrieval Precision on Contributed Knowledge (RPCK)"
    )
    parser.add_argument("--lessons-json", required=True, type=Path,
                        help="JSON manifest of drill items: list or {'lessons': [...]} of "
                             "{sn_id, contributed_at, knowledge_file?, query_terms[], "
                             "success_criteria, application_evidence[{ref, path?}]}")
    parser.add_argument("--knowledge-roots", required=True,
                        help="Comma-separated corpus dirs searched for query terms")
    parser.add_argument("--repo-root", type=Path, default=Path("."),
                        help="Root that knowledge_file and evidence paths resolve against")
    parser.add_argument("--receipts-dir", type=Path, default=None,
                        help="If given, write one coldness receipt JSON per lesson here")
    parser.add_argument("--window-days", type=int, default=DEFAULT_WINDOW_DAYS)
    parser.add_argument("--min-lessons", type=int, default=DEFAULT_MIN_LESSONS)
    parser.add_argument("--max-lessons", type=int, default=0,
                        help="Cap the deterministic sample (0 = no cap)")
    parser.add_argument("--threshold", type=float, default=DEFAULT_THRESHOLD)
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
    except ValueError as exc:
        print(f"input error: {exc}", file=sys.stderr)
        return 2
    for name, value in (("window-days", args.window_days),
                        ("min-lessons", args.min_lessons)):
        if value <= 0:
            print(f"input error: --{name} must be positive", file=sys.stderr)
            return 2
    if not 0 < args.threshold <= 1:
        print("input error: --threshold must be in (0, 1]", file=sys.stderr)
        return 2
    if args.max_lessons < 0:
        print("input error: --max-lessons cannot be negative", file=sys.stderr)
        return 2

    roots = [Path(p.strip()) for p in args.knowledge_roots.split(",") if p.strip()]
    if not roots:
        print("input error: --knowledge-roots names no directories", file=sys.stderr)
        return 2
    corpus = scan_corpus(roots)
    report = compute_report(
        lessons, corpus,
        repo_root=args.repo_root, now=now,
        window_days=args.window_days, min_lessons=args.min_lessons,
        threshold=args.threshold, max_lessons=args.max_lessons,
    )
    if args.receipts_dir is not None:
        args.receipts_dir.mkdir(parents=True, exist_ok=True)
        for drilled in report["lessons"]:
            receipt = drilled.pop("coldness_receipt")
            out = args.receipts_dir / f"{receipt['receipt_id']}.json"
            out.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")

    text = json.dumps(report, indent=2)
    if args.report_out:
        args.report_out.write_text(text + "\n", encoding="utf-8")
    else:
        print(text)
    print(
        f"C5.3 RPCK: {report['retrieved_and_applied']}/{report['sampled_lessons']} "
        f"retrieved+applied = {report['rate']:.2%} "
        f"(threshold {report['threshold']:.0%}, min sample {report['min_lessons']}) "
        f"-> {'PASS' if report['pass'] else 'FAIL'}",
        file=sys.stderr,
    )
    return 0 if report["pass"] else 1


if __name__ == "__main__":
    sys.exit(main())

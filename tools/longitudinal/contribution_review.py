#!/usr/bin/env python3
"""C5.7 — Contribution Signal Integrity (CSI).

The anti-gaming component. Guards C5.1–C5.6 against flooding the contribution
stream with low-value notes. Three checks, all mechanical:

1. DISPOSITION COMPLETENESS — every window contribution must carry a review
   disposition (accepted/rejected). Anything pending or undispositioned at
   window close is UNREVIEWED and fails the gate. A 100% acceptance rate over
   a decided sample >= --min-review-sample means no effective review is
   happening (design v2.0, C5.7) and fails the review-health check.
2. CLAIM–EVIDENCE CHECK (heuristic) — sentences that make state claims
   (quantitative assertions, assertive verbs) are auto-flagged when neither the
   sentence nor its immediate neighbours carry an evidence ref (repo path,
   URL, SN id, PR/issue ref, commit sha, receipt/ref markers). This is a
   heuristic, not a semantic judge: flagged claims are findings for the human
   reviewer, who is the second step per the design. The gate requires that
   every detected evidence-less claim IS flagged — flagging is the instrument's
   job; adjudication is the reviewer's.
3. SIMILARITY DEDUP — each contribution's token-set Jaccard similarity against
   the existing-notes corpus (--corpus-json). Scores >= --dup-threshold are
   reported as possible duplicates with the matched note and score. Without a
   corpus, dedup is SKIPPED and reported as skipped — never silently passed.

Duplicate contrib_ids in the manifest are an integrity failure and fail the
gate: the registry cannot have two different notes under one id.

Privacy-architectural note: inputs are deliberately-contributed artifacts only
(contribution texts, review dispositions). There is no input channel for
private communications.

DONE WHEN (design v2.0): every window contribution carries a disposition;
zero unreviewed contributions at window close; state claims without evidence
refs are auto-flagged.

Exit codes: 0 = zero unreviewed AND review health OK AND no duplicate ids;
1 = below bar; 2 = unreadable/malformed input.

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
DEFAULT_MIN_REVIEW_SAMPLE = 5
DEFAULT_DUP_THRESHOLD = 0.85

DISPOSITIONS = ("accepted", "rejected")

# A sentence is a state CLAIM if it matches any of these (heuristic).
CLAIM_RES = [
    re.compile(r"\d+(\.\d+)?\s*%"),                                   # 9.4%
    re.compile(r"\b\d[\d,]*\s+(files?|tests?|notes?|days?|commits?|prs?|"
               r"issues?|chains?|lessons?|seats?|laws?)\b", re.I),     # 34 files
    re.compile(r"[≥≤<>]=?\s*\d"),                                     # >= 20
    re.compile(r"\b\d+\s*/\s*\d+\b"),                                 # 14/14
    re.compile(r"\b(proves?|shows?|demonstrates?|measures?|confirms?|"
               r"fails?|passes?|reports?|found|zero|never|always)\b", re.I),
    re.compile(r"\b(all|every)\b.{0,40}\b(notes?|tests?|files?|laws?|"
               r"chains?|contributions?)\b", re.I),
]

# ... and it is EVIDENCED if the sentence or a neighbour matches any of these.
EVIDENCE_RES = [
    re.compile(r"https?://"),
    re.compile(r"\bSN-\d{3,}\b"),
    re.compile(r"\bPR\s*#\d+\b", re.I),
    re.compile(r"(?<!\w)#\d{3,}\b"),                                  # #1354
    re.compile(r"\b[0-9a-f]{7,40}\b"),                                # commit sha
    re.compile(r"\b(BRAIN|tools|tests|scripts|workspace)/[A-Za-z0-9_./-]*", re.I),
    re.compile(r"[\w.-]+\.(md|py|json|yml|yaml|txt|sql)\b", re.I),
    re.compile(r"\b(evidence|receipt|ref(erence)?)\b\s*:", re.I),
]

SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?])\s+")
TOKEN_RE = re.compile(r"[a-z0-9]{3,}")


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


def load_contributions(path: Path) -> list[dict]:
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot read contributions manifest {path}: {exc}") from exc
    items = (raw["contributions"] if isinstance(raw, dict) and "contributions" in raw
             else raw)
    if not isinstance(items, list):
        raise ValueError("contributions manifest must be a list or {'contributions': [...]}")
    contributions = []
    for i, item in enumerate(items):
        if not isinstance(item, dict):
            raise ValueError(f"contributions[{i}] must be an object")
        contrib_id = str(item.get("contrib_id", "")).strip()
        if not contrib_id:
            raise ValueError(f"contributions[{i}] needs a non-empty contrib_id")
        try:
            contributed_at = parse_ts(item["contributed_at"])
        except (KeyError, ValueError) as exc:
            raise ValueError(f"contributions[{i}] bad contributed_at: {exc}") from exc
        text = item.get("text", "")
        if not isinstance(text, str):
            raise ValueError(f"contributions[{i}] text must be a string")
        contributions.append({
            "contrib_id": contrib_id,
            "contributed_at": contributed_at,
            "seat": str(item.get("seat", "UNKNOWN")).strip() or "UNKNOWN",
            "text": text,
            "disposition": str(item.get("disposition", "") or "").strip().lower(),
            "review_reason": str(item.get("review_reason", "") or "").strip(),
            "reviewer_seat": str(item.get("reviewer_seat", "") or "").strip(),
        })
    return contributions


def load_corpus(path: Path | None) -> list[dict]:
    if path is None:
        return []
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot read corpus {path}: {exc}") from exc
    items = raw["notes"] if isinstance(raw, dict) and "notes" in raw else raw
    if not isinstance(items, list):
        raise ValueError("corpus must be a list or {'notes': [...]}")
    notes = []
    for i, item in enumerate(items):
        if not isinstance(item, dict) or not isinstance(item.get("text"), str):
            raise ValueError(f"corpus[{i}] must be an object with a text string")
        notes.append({
            "note_id": str(item.get("note_id", f"corpus[{i}]")).strip(),
            "text": item["text"],
        })
    return notes


def split_sentences(text: str) -> list[str]:
    return [s.strip() for s in SENTENCE_SPLIT_RE.split(text.strip()) if s.strip()]


def is_claim(sentence: str) -> bool:
    return any(r.search(sentence) for r in CLAIM_RES)


def has_evidence(sentence: str) -> bool:
    return any(r.search(sentence) for r in EVIDENCE_RES)


def flag_evidence_less_claims(contrib_id: str, text: str) -> list[dict]:
    """Auto-flag state-claim sentences with no evidence ref in a ±1 window."""
    sentences = split_sentences(text)
    flags = []
    for i, sentence in enumerate(sentences):
        if not is_claim(sentence):
            continue
        window = sentences[max(0, i - 1): i + 2]
        if any(has_evidence(s) for s in window):
            continue
        flags.append({
            "contrib_id": contrib_id,
            "sentence": sentence[:220] + ("…" if len(sentence) > 220 else ""),
            "reason": "state claim without evidence ref in sentence or neighbours",
        })
    return flags


def token_set(text: str) -> set[str]:
    return set(TOKEN_RE.findall(text.lower()))


def jaccard(a: set[str], b: set[str]) -> float:
    if not a and not b:
        return 1.0
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def find_duplicates(contrib: dict, corpus_tokens: list[tuple[str, set[str]]],
                   threshold: float) -> list[dict]:
    tokens = token_set(contrib["text"])
    hits = []
    for note_id, note_tokens in corpus_tokens:
        score = jaccard(tokens, note_tokens)
        if score >= threshold:
            hits.append({
                "contrib_id": contrib["contrib_id"],
                "matched_note": note_id,
                "similarity": round(score, 4),
            })
    hits.sort(key=lambda h: h["similarity"], reverse=True)
    return hits


def compute_report(
    contributions: list[dict],
    corpus: list[dict],
    corpus_given: bool,
    *,
    now: datetime,
    window_days: int,
    min_review_sample: int,
    dup_threshold: float,
) -> dict:
    window_start = now - timedelta(days=window_days)
    in_window = [c for c in contributions if window_start <= c["contributed_at"] <= now]
    out_of_window = sorted(c["contrib_id"] for c in contributions if c not in in_window)

    seen: dict[str, int] = {}
    duplicate_ids: list[str] = []
    for c in in_window:
        seen[c["contrib_id"]] = seen.get(c["contrib_id"], 0) + 1
    duplicate_ids = sorted(cid for cid, n in seen.items() if n > 1)

    unreviewed = sorted(
        c["contrib_id"] for c in in_window if c["disposition"] not in DISPOSITIONS
    )
    accepted = sum(1 for c in in_window if c["disposition"] == "accepted")
    rejected = sum(1 for c in in_window if c["disposition"] == "rejected")
    decided = accepted + rejected
    acceptance_rate = accepted / decided if decided else 0.0
    review_health_ok = not (decided >= min_review_sample and acceptance_rate >= 1.0)

    flagged_claims: list[dict] = []
    for c in in_window:
        flagged_claims.extend(flag_evidence_less_claims(c["contrib_id"], c["text"]))

    corpus_tokens = [(n["note_id"], token_set(n["text"])) for n in corpus]
    duplicates: list[dict] = []
    dedup_status = "skipped: no corpus supplied"
    if corpus_given:
        dedup_status = f"ran against {len(corpus_tokens)} corpus notes"
        for c in in_window:
            duplicates.extend(find_duplicates(c, corpus_tokens, dup_threshold))

    passed = not unreviewed and review_health_ok and not duplicate_ids
    reasons = []
    if unreviewed:
        reasons.append(f"{len(unreviewed)} unreviewed contribution(s): {unreviewed}")
    if not review_health_ok:
        reasons.append(
            f"100% acceptance over {decided} decided contributions "
            f"(min sample {min_review_sample}): no effective review is happening"
        )
    if duplicate_ids:
        reasons.append(f"duplicate contrib_ids in manifest: {duplicate_ids}")

    return {
        "component": "C5.7",
        "metric": "contribution_signal_integrity",
        "version": VERSION,
        "window_days": window_days,
        "min_review_sample": min_review_sample,
        "dup_threshold": dup_threshold,
        "now": now.isoformat(),
        "contributions_in_window": len(in_window),
        "accepted": accepted,
        "rejected": rejected,
        "unreviewed": unreviewed,
        "acceptance_rate": round(acceptance_rate, 4),
        "review_health_ok": review_health_ok,
        "duplicate_ids": duplicate_ids,
        "flagged_evidence_less_claims": flagged_claims,
        "flagged_claim_count": len(flagged_claims),
        "possible_duplicates": duplicates,
        "dedup_status": dedup_status,
        "pass": passed,
        "fail_reasons": reasons,
        "out_of_window": out_of_window,
        "heuristic_note": (
            "claim-evidence and dedup checks are heuristics; flagged items are "
            "findings for the human reviewer, who is the second step per design "
            "v2.0 (mechanical first, human-verified second)"
        ),
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="C5.7 — Contribution Signal Integrity (CSI): contribution review"
    )
    parser.add_argument("--contributions-json", required=True, type=Path,
                        help="JSON manifest: list or {'contributions': [...]} of "
                             "{contrib_id, contributed_at, seat?, text, "
                             "disposition, review_reason?, reviewer_seat?}")
    parser.add_argument("--corpus-json", type=Path, default=None,
                        help="Existing notes for dedup: list or {'notes': [...]} "
                             "of {note_id, text}. Without it, dedup is skipped "
                             "and reported as skipped.")
    parser.add_argument("--window-days", type=int, default=DEFAULT_WINDOW_DAYS)
    parser.add_argument("--min-review-sample", type=int,
                        default=DEFAULT_MIN_REVIEW_SAMPLE,
                        help="Decided contributions below this sample are too few "
                             "to judge review health")
    parser.add_argument("--dup-threshold", type=float, default=DEFAULT_DUP_THRESHOLD,
                        help="Jaccard similarity at/above which a contribution is "
                             "flagged as a possible duplicate")
    parser.add_argument("--now", default=None,
                        help="ISO timestamp overriding 'now' (determinism)")
    parser.add_argument("--report-out", type=Path, default=None,
                        help="Write the JSON report to this path")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        now = parse_ts(args.now) if args.now else datetime.now(timezone.utc)
        contributions = load_contributions(args.contributions_json)
        corpus = load_corpus(args.corpus_json)
    except ValueError as exc:
        print(f"input error: {exc}", file=sys.stderr)
        return 2
    for name, value in (("window-days", args.window_days),
                        ("min-review-sample", args.min_review_sample)):
        if value <= 0:
            print(f"input error: --{name} must be positive", file=sys.stderr)
            return 2
    if not 0 < args.dup_threshold <= 1:
        print("input error: --dup-threshold must be in (0, 1]", file=sys.stderr)
        return 2

    report = compute_report(
        contributions, corpus, args.corpus_json is not None,
        now=now, window_days=args.window_days,
        min_review_sample=args.min_review_sample,
        dup_threshold=args.dup_threshold,
    )
    text = json.dumps(report, indent=2)
    if args.report_out:
        args.report_out.write_text(text + "\n", encoding="utf-8")
    else:
        print(text)
    print(
        f"C5.7 CSI: {report['contributions_in_window']} contributions, "
        f"{len(report['unreviewed'])} unreviewed, "
        f"acceptance {report['acceptance_rate']:.0%}, "
        f"{report['flagged_claim_count']} flagged claims, "
        f"{len(report['possible_duplicates'])} possible duplicates "
        f"-> {'PASS' if report['pass'] else 'FAIL'}",
        file=sys.stderr,
    )
    return 0 if report["pass"] else 1


if __name__ == "__main__":
    sys.exit(main())

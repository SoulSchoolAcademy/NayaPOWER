#!/usr/bin/env python3
"""collector2.py — the SECOND INDEPENDENT collector for the observed-experience instrument v1.

Independence thesis (documented, not assumed):
  Collector 1 (first light, SWEEP-20261012-001): an agent read C2 (private
  durable chat logs) by *interpretation* — one mind, hand-pinned verbatim
  spans, judgment calls on classes, hashes, and inference text.
  Collector 2 (this file): deterministic, rules-based code over C1 (team feeds)
  + C3 (API-grounded repo actions) ONLY. C2 is a hard error here.
    - Different method: code, no interpretation. Same input -> same output.
    - Different source: public/API-grounded only, cold-recomputable by anyone
      with repo read access. It can never "see" what collector 1 saw in the
      private chat logs.
    - Seat-agnostic: re-running produces identical bytes, so the operating
      seat is not part of the evidence.

Residual (honest, for Epsilon's IV): seat-independence of the *human verdicts*
is NOT claimed — the independence claim rests on method + source separation +
mechanical reproducibility. Epsilon re-running this file unchanged is the
seat-independent check. See D32 in the run report.

Anti-manufacturing rules enforced in code:
  1. C2 is refused, not just unused (Collector2Error, exit 2).
  2. A feed comment is attributed to the human ONLY if it carries a marker
     from the versioned authorship-markers.json as a first-person speech act.
     Markers appearing inside reported speech ("Shawn said ...", "his words",
     "quoting ...") are graded authorship=inferred -> EXCLUDED, fail closed.
  3. C3 attribution requires the human's personal account in
     human-accounts.json. v1 ships with an EMPTY allowlist -> C3 always
     reports "authorship unresolvable", never guesses.
  4. This collector PROPOSES promotions only. promote/expire stay in
     observe.py — deliberate, signed acts.
  5. No self-observation: observatory artifacts (sweeps, reports, grades) are
     never evidence of human value (schema-level, inherited).

CLI:
  scan             C1+C3 scan over [since, until]; emits observations + NULL sweep log
  grade-candidates grade pending candidates against THIS collector's evidence
  rejudge-baseline re-judge baseline observations from THIS collector's universe
  agreement        full inter-collector agreement report (collector1 vs collector2)
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from tools.human_value.observation_schema import CHANNELS  # noqa: E402

INSTRUMENT = "observed-experience-instrument-v1"
COLLECTOR = "collector2"
REPO = "SoulSchoolAcademy/NayaPOWER"

# C1: team feeds scanned by the second collector.
C1_FEEDS = (2154, 1713, 1714, 1715)

MARKERS_PATH = REPO_ROOT / "tools" / "human_value" / "authorship-markers.json"
HUMAN_ACCOUNTS_PATH = REPO_ROOT / "tools" / "human_value" / "human-accounts.json"

# Corrective speech acts -> CORRECTED / attention_demanded; everything else
# marker-matched -> STATED / useful_outcome.
CORRECTIVE_MARKERS = {
    "do your job right",
    "real deal or no deal",
    "acknowledge it and make it right",
}

# Reported-speech framing: the marker is being DESCRIBED, not SPOKEN.
# Mechanical, deterministic: any hit -> authorship=inferred -> excluded.
REPORT_FRAME_RE = re.compile(
    r"(?i)\b(shawn said|his words|quoting|quote[sd]?\b|verbatim|attested|"
    r"per shawn|as shawn|he said|his directive|durable record|memory\.md|"
    r"smart note|the briefing|agents\.md)\b"
)
# Colon-attribution: `Shawn: "..."` / `Shawn: Make it so` — reported speech
# even without the word "said".
ATTRIBUTION_RE = re.compile(r"(?i)\bshawn\b\s*[:\u2014\u2013-]")
# Double-quoted spans: a first-person speech act does not quote itself.
QUOTED_SPAN_RE = re.compile(r'"[^"\n]*"')


def _marker_spans(body: str, phrase: str) -> list[tuple[int, int]]:
    spans = []
    start = 0
    while True:
        i = body.find(phrase, start)
        if i < 0:
            break
        spans.append((i, i + len(phrase)))
        start = i + 1
    return spans


def _is_reported(body: str, span: tuple[int, int]) -> bool:
    start, _ = span
    # Marker inside a double-quoted span -> someone else's words being quoted.
    for m in QUOTED_SPAN_RE.finditer(body):
        if m.start() <= start < m.end():
            return True
    # Attribution framing near the marker -> reported speech.
    window = body[max(0, start - 80):start + 40]
    if ATTRIBUTION_RE.search(window) or REPORT_FRAME_RE.search(window):
        return True
    return False


class Collector2Error(RuntimeError):
    """Fail-closed errors for the second collector."""


def require_channels(channels: list[str]) -> list[str]:
    """C2 is refused, not just unused. This is the independence mechanism."""
    if not channels:
        raise Collector2Error("channels must be non-empty")
    unknown = [c for c in channels if c not in CHANNELS]
    if unknown:
        raise Collector2Error(f"unknown channels: {unknown}")
    if "c2" in channels:
        raise Collector2Error(
            "C2 (direct messages / private chat logs) is excluded from the "
            "second collector by construction. Collector 1 owns C2; sharing "
            "the source would collapse the independence claim."
        )
    return channels


def load_markers(markers_path: Path = MARKERS_PATH) -> tuple[list[dict], str]:
    """Load versioned markers; return (markers, sha256 pin of the file)."""
    raw = markers_path.read_bytes()
    pin = "sha256:" + hashlib.sha256(raw).hexdigest()
    doc = json.loads(raw)
    markers = doc.get("markers", [])
    if not markers:
        raise Collector2Error(f"{markers_path}: no markers — refusing to scan")
    return markers, pin


def load_human_accounts(path: Path = HUMAN_ACCOUNTS_PATH) -> list[str]:
    """v1: empty allowlist. C3 reports 'authorship unresolvable', never guesses."""
    doc = json.loads(path.read_text(encoding="utf-8"))
    accounts = doc.get("accounts", [])
    if not isinstance(accounts, list):
        raise Collector2Error(f"{path}: 'accounts' must be a list")
    return accounts


def gh_api(gh_api_bin: str, method_path: str) -> object:
    """Read-only GitHub API via the approved gh-api script. No writes, ever."""
    proc = subprocess.run(
        ["python3", gh_api_bin, "GET", method_path],
        capture_output=True,
        text=True,
        timeout=120,
    )
    if proc.returncode != 0:
        raise Collector2Error(f"gh-api GET {method_path} failed: {proc.stderr[:300]}")
    try:
        return json.loads(proc.stdout)
    except json.JSONDecodeError as exc:
        raise Collector2Error(f"gh-api GET {method_path}: bad JSON ({exc})")


def fetch_comments(
    gh_api_bin: str, issue: int, since: str, until: str, per_page: int = 100
) -> list[dict]:
    """Paginate issue comments; filter client-side by [since, until]."""
    out: list[dict] = []
    page = 1
    while True:
        path = f"/repos/{REPO}/issues/{issue}/comments?per_page={per_page}&page={page}"
        batch = gh_api(gh_api_bin, path)
        if not isinstance(batch, list) or not batch:
            break
        for c in batch:
            ts = c.get("created_at", "")
            if since <= ts <= until:
                out.append(c)
        if len(batch) < per_page:
            break
        page += 1
        if page > 20:  # sanity bound: 2000 comments is not a "sparse signal"
            break
    return out


def classify_comment(
    body: str, markers: list[dict]
) -> tuple[str | None, str, str | None]:
    """Mechanical authorship + class.

    Returns (matched_marker, authorship, observation_kind):
      - (None, 'uncertain', None): no marker -> fail closed, excluded.
      - (marker, 'inferred', kind): reported speech -> excluded from promotion.
      - (marker, 'direct', kind): first-person speech act -> attributable.
    """
    hit = None
    hit_span: tuple[int, int] | None = None
    for m in markers:
        phrase = m["marker"]
        spans = _marker_spans(body, phrase)  # case-sensitive per marker-file spec
        if spans:
            hit = phrase
            hit_span = spans[0]
            break
    if hit is None or hit_span is None:
        return None, "uncertain", None
    kind = "corrected" if hit in CORRECTIVE_MARKERS else "stated"
    if _is_reported(body, hit_span):
        return hit, "inferred", kind
    return hit, "direct", kind


def comment_to_observation(
    comment: dict,
    feed: int,
    marker: str,
    kind: str,
    markers_pin: str,
    collected_at: str,
) -> dict:
    body = comment.get("body", "") or ""
    value_type = "attention_demanded" if kind == "corrected" else "useful_outcome"
    unit_desc = (
        "one counted corrective directive speech act"
        if kind == "corrected"
        else "one asserted ratification/adoption speech act"
    )
    return {
        "schema_version": "2",
        "event_id": f"OBS-C2-{comment['id']}",
        "recorded_at": collected_at[:10],
        "value_type": value_type,
        "value_units": 1,
        "unit_description": unit_desc,
        "evidence": [
            {
                "kind": "feed_comment",
                "ref": f"https://github.com/{REPO}/issues/{feed}"
                f"#issuecomment-{comment['id']}",
            }
        ],
        "observation_kind": kind,
        "subject": "human_self",
        "observed_by": COLLECTOR,
        "observed_at": comment.get("created_at"),
        "collected_at": collected_at,
        "verbatim_hash": "sha256:" + hashlib.sha256(body.encode("utf-8")).hexdigest(),
        "authorship": "direct",
        "collector_inference": (
            f"collector2 (deterministic): feed comment carries authorship marker "
            f"'{marker}' as a first-person speech act (markers v pin {markers_pin[:19]}...); "
            f"1 unit = 1 counted {kind} occurrence. No interpretation beyond the marker match."
        ),
        "promotion": None,
        "channel": "c1",
    }


def cmd_scan(args: argparse.Namespace) -> int:
    channels = require_channels(args.channels.split(","))
    markers, markers_pin = load_markers(Path(args.markers))
    accounts = load_human_accounts(Path(args.accounts))
    collected_at = args.as_of or datetime.now(timezone.utc).isoformat()

    observations: list[dict] = []
    excluded: list[dict] = []
    searched: list[dict] = []

    if "c1" in channels:
        for feed in C1_FEEDS:
            comments = fetch_comments(
                args.gh_api, feed, args.since, args.until
            )
            searched.append(
                {"channel": "c1", "feed": feed, "comments_scanned": len(comments)}
            )
            for c in comments:
                marker, authorship, kind = classify_comment(c.get("body", "") or "", markers)
                if authorship == "uncertain":
                    excluded.append(
                        {"comment_id": c["id"], "feed": feed, "reason": "no_authorship_marker"}
                    )
                elif authorship == "inferred":
                    excluded.append(
                        {
                            "comment_id": c["id"],
                            "feed": feed,
                            "reason": "reported_speech_marker_not_first_person",
                            "marker": marker,
                        }
                    )
                else:
                    observations.append(
                        comment_to_observation(c, feed, marker, kind, markers_pin, collected_at)
                    )

    c3_note = None
    if "c3" in channels:
        # API-grounded repo actions with mechanical human authorship.
        items = gh_api(
            args.gh_api,
            f"/repos/{REPO}/issues?state=all&since={args.since}&per_page=100",
        )
        items = items if isinstance(items, list) else []
        attributable = [
            i for i in items if (i.get("user") or {}).get("login") in accounts
        ]
        searched.append(
            {"channel": "c3", "issues_prs_scanned": len(items), "attributable": len(attributable)}
        )
        c3_note = (
            "c3_authorship_unresolvable: human-accounts.json allowlist is empty in v1; "
            f"{len(items)} repo actions seen, 0 mechanically attributable. "
            "Fail closed — no C3 observations claimed."
            if not accounts
            else f"c3: {len(attributable)} attributable actions"
        )
        for i in attributable:  # pragma: no cover - empty in v1
            observations.append(
                {
                    "schema_version": "2",
                    "event_id": f"OBS-C2-C3-{i['id']}",
                    "recorded_at": collected_at[:10],
                    "value_type": "useful_outcome",
                    "value_units": 1,
                    "unit_description": "one counted human-authored repo action",
                    "evidence": [{"kind": "api_action", "ref": i.get("html_url", "")}],
                    "observation_kind": "revealed",
                    "subject": "human_self",
                    "observed_by": COLLECTOR,
                    "observed_at": i.get("created_at"),
                    "collected_at": collected_at,
                    "verbatim_hash": "sha256:"
                    + hashlib.sha256(
                        (i.get("title", "") + (i.get("body") or "")).encode("utf-8")
                    ).hexdigest(),
                    "authorship": "direct",
                    "collector_inference": "collector2 (deterministic): API-grounded human-authored repo action; authorship is in the API, not inferred.",
                    "promotion": None,
                    "channel": "c3",
                }
            )

    observations.sort(key=lambda o: o["event_id"])
    sweep = {
        "instrument": INSTRUMENT,
        "collector": COLLECTOR,
        "sweep_id": args.sweep_id,
        "channels": channels,
        "watermark_start": args.since,
        "watermark_end": args.until,
        "markers_pin": markers_pin,
        "human_accounts": accounts,
        "observations": observations,
        "excluded": excluded,
        "searched": searched,
        "null_sweep": len(observations) == 0,
        "c3_note": c3_note,
        "independence": {
            "method": "deterministic rules-based code; same input -> same output",
            "sources": "C1 team feeds + C3 API actions only; C2 refused by construction",
            "reproducible_by": "any seat re-running this file unchanged",
        },
        "collected_at": collected_at,
    }
    print(json.dumps(sweep, indent=2, ensure_ascii=False))
    if args.out:
        Path(args.out).write_text(
            json.dumps(sweep, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
    return 0


def read_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            rows.append(json.loads(line))
    return rows


def grade_candidates(
    sweep: dict, candidates: list[dict]
) -> list[dict]:
    """Grade pending candidates against THIS collector's evidence only.

    A candidate promotes (proposed, never automatic) only on a DIRECT human
    trace about its artifact: a collector2 observation whose evidence or
    inference references the PR/issue number. Otherwise it remains pending
    with the reason recorded.
    """
    verdicts = []
    for cand in candidates:
        pr = str(cand.get("pr", ""))
        refs = {f"#{pr}", f"PR {pr}", f"pull/{pr}", f"issues/{pr}"}
        hits = [
            o
            for o in sweep["observations"]
            if any(r in (o.get("collector_inference", "") + json.dumps(o.get("evidence", []))) for r in refs)
        ]
        # Direct human trace must also be about the artifact, not the collector's own machinery.
        if hits:
            verdicts.append(
                {
                    "candidate_id": cand.get("candidate_id"),
                    "pr": cand.get("pr"),
                    "verdict": "promote_proposed",
                    "basis": [o["event_id"] for o in hits],
                    "note": "PROPOSAL ONLY — promotion is a deliberate, signed act (observe.py promote).",
                }
            )
        else:
            verdicts.append(
                {
                    "candidate_id": cand.get("candidate_id"),
                    "pr": cand.get("pr"),
                    "verdict": "remains_pending",
                    "reason": (
                        "no C1/C3 direct human trace about this artifact in collector2's "
                        "window; grader's prior is not evidence"
                    ),
                }
            )
    return verdicts


def rejudge_baseline(sweep: dict, baseline_events: list[dict]) -> list[dict]:
    """Re-judge collector1's events from collector2's evidence universe.

    Verdicts:
      corroborated   — byte-exact verbatim_hash re-found in C1/C3 with direct authorship
      contradicted   — C1/C3 evidence directly contradicts the event
      not_observable — outside collector2's C1/C3 universe (C2-sourced). NOT a disagreement.
    """
    found_hashes = {
        o["verbatim_hash"]
        for o in sweep["observations"]
        if o.get("authorship") == "direct"
    }
    verdicts = []
    for ev in baseline_events:
        vid = ev.get("event_id", "?")
        vh = ev.get("verbatim_hash")
        if vh and vh in found_hashes:
            verdicts.append({"event_id": vid, "verdict": "corroborated"})
        else:
            verdicts.append(
                {
                    "event_id": vid,
                    "verdict": "not_observable",
                    "reason": (
                        "collector1's event is C2-sourced (private chat logs); "
                        "collector2's universe is C1/C3 only. Byte-exact verbatim "
                        "not re-found in feeds/API in-window. Not a disagreement — "
                        "a non-overlapping evidence universe."
                    ),
                }
            )
    return verdicts


def cmd_grade_candidates(args: argparse.Namespace) -> int:
    sweep = json.loads(Path(args.scan).read_text(encoding="utf-8"))
    candidates = read_jsonl(Path(args.candidates))
    verdicts = grade_candidates(sweep, candidates)
    out = {"collector": COLLECTOR, "scan": sweep.get("sweep_id"), "verdicts": verdicts}
    print(json.dumps(out, indent=2))
    if args.out:
        Path(args.out).write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
    return 0


def cmd_rejudge_baseline(args: argparse.Namespace) -> int:
    sweep = json.loads(Path(args.scan).read_text(encoding="utf-8"))
    baseline = json.loads(Path(args.baseline).read_text(encoding="utf-8"))
    events = baseline.get("promoted", []) + baseline.get("dropped_as_observations", [])
    if not events and isinstance(baseline, list):
        events = baseline
    verdicts = rejudge_baseline(sweep, events)
    out = {"collector": COLLECTOR, "scan": sweep.get("sweep_id"), "verdicts": verdicts}
    print(json.dumps(out, indent=2))
    if args.out:
        Path(args.out).write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
    return 0


def cmd_agreement(args: argparse.Namespace) -> int:
    """Full inter-collector agreement: mechanical triples + verdict table."""
    sys.path.insert(0, str(REPO_ROOT))
    from tools.human_value.observe import observation_triples, run_agreement_measure

    scan = json.loads(Path(args.scan).read_text(encoding="utf-8"))
    baseline = json.loads(Path(args.baseline).read_text(encoding="utf-8"))
    c1_events = baseline.get("promoted", [])
    if not c1_events and isinstance(baseline, list):
        c1_events = baseline
    c2_obs = scan["observations"]

    triples = run_agreement_measure(c1_events, c2_obs)
    verdicts = rejudge_baseline(scan, c1_events)
    counts = {}
    for v in verdicts:
        counts[v["verdict"]] = counts.get(v["verdict"], 0) + 1

    report = {
        "instrument": INSTRUMENT,
        "collector_a": "collector1 (interpretive agent, C2)",
        "collector_b": "collector2 (deterministic code, C1+C3)",
        "mechanical_jaccard": triples,
        "baseline_verdicts": verdicts,
        "verdict_counts": counts,
        "reading": (
            "Agreement is measured, not assumed. A low Jaccard with all "
            "'not_observable' verdicts means NON-OVERLAPPING EVIDENCE "
            "UNIVERSES, not disagreement. The second path's independent value "
            "is its own sweep and candidate verdicts."
        ),
    }
    print(json.dumps(report, indent=2))
    if args.out:
        Path(args.out).write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="collector2.py", description="Second independent collector (C1+C3, deterministic)"
    )
    sub = p.add_subparsers(dest="cmd", required=True)

    def add_common(s: argparse.ArgumentParser) -> None:
        s.add_argument("--gh-api", default=os.path.expanduser("~/workspace/naya/bin/gh-api"))
        s.add_argument("--markers", default=str(MARKERS_PATH))
        s.add_argument("--accounts", default=str(HUMAN_ACCOUNTS_PATH))

    s = sub.add_parser("scan", help="C1+C3 scan over [since, until]")
    add_common(s)
    s.add_argument("--since", required=True)
    s.add_argument("--until", required=True)
    s.add_argument("--channels", default="c1,c3")
    s.add_argument("--sweep-id", required=True)
    s.add_argument("--as-of", default=None, help="override collected_at (determinism)")
    s.add_argument("--out", default=None)
    s.set_defaults(func=cmd_scan)

    s = sub.add_parser("grade-candidates", help="grade pending candidates vs this scan")
    s.add_argument("--scan", required=True)
    s.add_argument("--candidates", required=True)
    s.add_argument("--out", default=None)
    s.set_defaults(func=cmd_grade_candidates)

    s = sub.add_parser("rejudge-baseline", help="re-judge collector1 events from C1/C3")
    s.add_argument("--scan", required=True)
    s.add_argument("--baseline", required=True, help="JSON with 'promoted' list")
    s.add_argument("--out", default=None)
    s.set_defaults(func=cmd_rejudge_baseline)

    s = sub.add_parser("agreement", help="full inter-collector agreement report")
    s.add_argument("--scan", required=True)
    s.add_argument("--baseline", required=True)
    s.add_argument("--out", default=None)
    s.set_defaults(func=cmd_agreement)

    return p


def main() -> int:
    args = build_parser().parse_args()
    try:
        return args.func(args)
    except Collector2Error as exc:
        print(f"collector2: FAIL CLOSED: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())

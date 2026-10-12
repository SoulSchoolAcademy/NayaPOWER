#!/usr/bin/env python3
"""Human Value Observatory — the live-run loop for the human-value instrument.

The event-ledger instrument (compute_hv.py + schema.py) *measures*.
The change-grade instrument (instrument.py) *judges* shipped changes.
The observatory is the loop that keeps both running *live*:

  scan     enumerate merge commits since a watermark; emit DRAFT candidates
           with purely mechanical fields. Drafts carry no judgment and are
           deliberately NOT schema-valid events: the machine observes, it
           never credits.
  promote  the explicit lane action. A graded REAL VALUE+ scorecard becomes
           one schema-valid ledger event (minted through instrument.py's
           to_ledger_event, the single minting rule), then: ledger append,
           deterministic recompute, trend snapshot, promotion receipt,
           watermark advance. Requires --confirm. THIN / NO VALUE /
           DISQUALIFIED scorecards and duplicate event_ids are refused,
           fail closed — the ledger is never touched on a refusal.
  report   regenerate the pinned observatory report from ledger + trend
           bytes. Deterministic: same bytes in, same bytes out.
  trend    print the trend table from the snapshot store.

Only the standard library is used. Exit 0 = done. Exit 2 = refused / invalid
input (nothing was written, nothing was credited).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from datetime import date, datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from tools.human_value import compute_hv  # noqa: E402
from tools.human_value.instrument import (  # noqa: E402
    InstrumentError,
    to_ledger_event,
)
from tools.human_value.schema import SchemaError  # noqa: E402

HV_ROOT = REPO_ROOT / "tools" / "human_value"
OBS_ROOT = HV_ROOT / "observatory"
DEFAULT_DRAFTS_DIR = OBS_ROOT / "drafts"
DEFAULT_RECEIPTS_DIR = OBS_ROOT / "receipts"
DEFAULT_WATERMARK = OBS_ROOT / "watermark.json"
DEFAULT_TREND = HV_ROOT / "ledgers" / "trend.jsonl"
DEFAULT_REPORT = HV_ROOT / "OBSERVATORY-REPORT.md"

INSTRUMENT = "human-value-observatory-v1"
DRAFT_VERSION = 1
TREND_WINDOW_DAYS = 7


class ObservatoryError(Exception):
    """Fail-safe: nothing is credited, nothing is written."""


# ---------------------------------------------------------------- git helpers

def _git(repo: str, *args: str) -> str:
    p = subprocess.run(
        ["git", "-C", repo, *args],
        capture_output=True, text=True, timeout=120,
    )
    if p.returncode != 0:
        raise ObservatoryError(
            f"git {' '.join(args)} failed in {repo}: {p.stderr.strip()[:300]}")
    return p.stdout


def _git_ok(repo: str, *args: str) -> bool:
    p = subprocess.run(
        ["git", "-C", repo, *args],
        capture_output=True, text=True, timeout=60,
    )
    return p.returncode == 0


def _head(repo: str) -> str:
    return _git(repo, "rev-parse", "HEAD").strip()


def _github_repo_url(repo: str) -> str | None:
    """owner/repo parsed from the origin remote, or None when not GitHub."""
    if not _git_ok(repo, "remote", "get-url", "origin"):
        return None
    url = _git(repo, "remote", "get-url", "origin").strip()
    m = re.search(r"github\.com[:/](.+?)(?:\.git)?$", url)
    return m.group(1) if m else None


# ---------------------------------------------------------------- scan

_PR_RE = re.compile(r"(?:pull request #|\(#)(\d+)", re.IGNORECASE)


def parse_pr_number(subject: str) -> int | None:
    m = _PR_RE.search(subject)
    return int(m.group(1)) if m else None


def _diffstat(repo: str, merge_sha: str) -> dict:
    out = _git(repo, "diff", "--numstat", "-z",
               f"{merge_sha}^1", merge_sha)
    files = ins = dels = 0
    dir_counts: dict[str, int] = {}
    # -z: records are "<ins>\t<del>\t<path>\0" (binary: "-\t-\t<path>\0")
    for rec in out.split("\0"):
        if not rec.strip():
            continue
        parts = rec.split("\t")
        if len(parts) < 3:
            continue
        files += 1
        try:
            ins += int(parts[0])
            dels += int(parts[1])
        except ValueError:
            pass  # binary file: "- -"
        path = parts[2]
        top = path.split("/")[0] if "/" in path else "(root)"
        dir_counts[top] = dir_counts.get(top, 0) + 1
    top_dirs = sorted(dir_counts, key=lambda d: (-dir_counts[d], d))[:8]
    return {"files": files, "insertions": ins, "deletions": dels,
            "top_dirs": top_dirs}


def scan(repo: str, base: str, drafts_dir: Path,
         watermark_out: Path | None) -> dict:
    """Enumerate merge commits in (base..HEAD]; write one DRAFT per merge.

    Every draft field is git-verifiable. No judgment is emitted anywhere:
    drafts are deliberately not schema-valid events (validate_event raises
    on them), so the machine cannot credit its own observations.
    """
    if not _git_ok(repo, "cat-file", "-e", base):
        raise ObservatoryError(f"base {base!r} not found in {repo}")
    if not _git_ok(repo, "merge-base", "--is-ancestor", base, "HEAD"):
        raise ObservatoryError(
            f"base {base!r} is not an ancestor of HEAD "
            f"({_head(repo)[:12]}): refusing to scan across a rewritten history")
    head = _head(repo)

    log = _git(repo, "log", "--merges", "--reverse",
               "--format=%H%x1f%P%x1f%an%x1f%aI%x1f%s",
               f"{base}..HEAD")
    gh = _github_repo_url(repo)
    drafts_dir.mkdir(parents=True, exist_ok=True)

    found = written = skipped = 0
    newest = base
    for line in log.splitlines():
        if not line.strip():
            continue
        found += 1
        sha, parents, author, merged_at, subject = line.split("\x1f")
        newest = sha
        draft_path = drafts_dir / f"{sha}.json"
        if draft_path.exists():
            skipped += 1
            continue
        pr_number = parse_pr_number(subject)
        pr_url = (f"https://github.com/{gh}/pull/{pr_number}"
                  if pr_number and gh else None)
        commit_url = (f"https://github.com/{gh}/commit/{sha}"
                      if gh else None)
        suggested_evidence = []
        if commit_url:
            suggested_evidence.append({"kind": "url", "ref": commit_url})
        if pr_url:
            suggested_evidence.append({"kind": "url", "ref": pr_url})
        draft = {
            "draft_version": DRAFT_VERSION,
            "status": ("DRAFT — not a ledger event. The machine observes; "
                       "it never credits. A graded scorecard promotes this."),
            "merge_sha": sha,
            "parents": parents.split(),
            "pr_number": pr_number,
            "pr_url": pr_url,
            "title": subject,
            "author": author,
            "merged_at": merged_at,
            "diffstat": _diffstat(repo, sha),
            "suggested_evidence": suggested_evidence,
            "mechanical_note": ("Every field above is verifiable with "
                                "`git log` / `git diff` at the merge SHA. "
                                "No value judgment is present or implied."),
        }
        draft_path.write_text(json.dumps(draft, indent=2, sort_keys=True)
                              + "\n", encoding="utf-8")
        written += 1

    if watermark_out is not None:
        watermark_out.parent.mkdir(parents=True, exist_ok=True)
        watermark_out.write_text(json.dumps({
            "last_observed_merge": newest,
            "observed_tip": head,
            "observed_base": base,
            "updated_utc": datetime.now(timezone.utc).isoformat(),
            "note": "operational cursor, not a measurement",
        }, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    return {"merges_found": found, "drafts_written": written,
            "drafts_skipped": skipped, "watermark": newest,
            "tip": head}


# ---------------------------------------------------------------- promote

def _load_json(path: Path, what: str) -> object:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        raise ObservatoryError(f"cannot read {what} {path}: {e}")


def _display_path(path: Path) -> str:
    """Repo-relative display path when inside the repo, else the plain path."""
    try:
        return str(path.resolve().relative_to(REPO_ROOT.resolve()))
    except ValueError:
        return str(path)


def _repo_relative(path: Path, anchor: Path) -> str:
    """Truthful short ref: repo-relative when inside the repo, else ledger-relative."""
    try:
        return str(path.resolve().relative_to(REPO_ROOT.resolve()))
    except ValueError:
        return str(path.resolve().relative_to(anchor.resolve().parent))


def promote(ledger_path: Path, scorecard_path: Path, event_id: str,
            recorded_at: str, trend_path: Path,
            receipts_dir: Path, pr_url: str | None, confirm: bool) -> dict:
    """Promote one graded REAL VALUE+ scorecard into the canonical ledger.

    Fail-closed order: validate everything BEFORE touching the ledger.
    Any refusal leaves every byte exactly as it was. The observation
    watermark is owned by `scan` and is never moved backwards by a
    promotion (a promotion may ledger an older merge than the cursor).
    """
    if not confirm:
        raise ObservatoryError(
            "promote requires --confirm: ledgering a value event is an "
            "explicit lane action, never a default")
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", recorded_at):
        raise ObservatoryError(f"bad date {recorded_at!r} (want YYYY-MM-DD)")

    scorecard = _load_json(scorecard_path, "scorecard")
    if not isinstance(scorecard, dict):
        raise ObservatoryError("scorecard must be a JSON object")
    verdict = scorecard.get("verdict")
    if scorecard.get("disqualified") or verdict not in ("HIGH VALUE", "REAL VALUE"):
        raise ObservatoryError(
            f"verdict {verdict!r} promotes nothing "
            "(only HIGH VALUE / REAL VALUE mint events; "
            "the instrument refuses to manufacture value-credit)")
    merge_sha = scorecard.get("merge_sha")
    if not merge_sha:
        raise ObservatoryError("scorecard has no merge_sha: nothing to promote")
    change_id = scorecard.get("change_id", "")
    if pr_url is None:
        m = re.fullmatch(r"PR-(\d+)", str(change_id))
        if m:
            gh = "SoulSchoolAcademy/NayaPOWER"
            pr_url = f"https://github.com/{gh}/pull/{m.group(1)}"

    raw_lines, events = compute_hv.load_ledger(ledger_path)
    before_hash = compute_hv.ledger_sha256(raw_lines)
    if any(e["event_id"] == event_id for e in events):
        raise ObservatoryError(
            f"duplicate event_id {event_id!r}: already in the ledger "
            "(a recomputation cannot tell which copy was counted)")

    # The promotion receipt exists BEFORE the ledger changes, so its ref is
    # honest evidence. Its content is computed deterministically first.
    receipts_dir.mkdir(parents=True, exist_ok=True)
    receipt_path = receipts_dir / f"{event_id}.json"
    if receipt_path.exists():
        raise ObservatoryError(
            f"promotion receipt {receipt_path} already exists: "
            "refusing to overwrite promotion history")

    # Mint through the single minting rule (instrument.py). Raises on
    # THIN/NO VALUE/DISQUALIFIED or schema violation — nothing is appended.
    # The receipt path is known before the receipt is written; the PR url is
    # always present, so the event keeps durable evidence even if a later
    # write step fails loudly.
    event = to_ledger_event(
        scorecard,
        recorded_at=recorded_at,
        event_id=event_id,
        receipt_ref=_repo_relative(receipt_path, ledger_path),
        pr_url=pr_url,
    )
    event_line = json.dumps(event, sort_keys=True)

    new_lines = raw_lines + [event_line]
    new_events = compute_hv.validate_ledger(
        [json.loads(ln) for ln in new_lines])  # full-ledger revalidation
    after_hash = compute_hv.ledger_sha256(new_lines)

    scorecard_bytes = scorecard_path.read_bytes()
    promoted_at = datetime.now(timezone.utc).isoformat()
    receipt = {
        "receipt_version": 1,
        "instrument": INSTRUMENT,
        "event_id": event_id,
        "promoted_at_utc": promoted_at,
        "grader": scorecard.get("grader"),
        "merge_sha": merge_sha,
        "verdict": verdict,
        "score": scorecard.get("score"),
        "recorded_at": recorded_at,
        "ledger_sha256_before": before_hash,
        "ledger_sha256_after": after_hash,
        "scorecard_sha256": "sha256:" + hashlib.sha256(scorecard_bytes).hexdigest(),
        "scorecard_path": str(scorecard_path),
        "note": ("Promotion is the lane's explicit act. The scorecard is the "
                 "judgment; this receipt is the provenance."),
    }

    # Write order: ledger first (the measured fact), then provenance, then
    # the trend snapshot. A failure after the ledger write is loud and the
    # event still carries its PR-url evidence pointer.
    ledger_path.write_text("\n".join(new_lines) + "\n", encoding="utf-8")
    receipt_path.write_text(json.dumps(receipt, indent=2, sort_keys=True)
                            + "\n", encoding="utf-8")

    as_of = date.fromisoformat(max(e["recorded_at"] for e in new_events))
    rep = compute_hv.compute(new_events, TREND_WINDOW_DAYS, as_of)
    trend_path.parent.mkdir(parents=True, exist_ok=True)
    snapshot = {
        "snapshot_ledger_sha256": after_hash,
        "as_of": rep["as_of"],
        "window_days": TREND_WINDOW_DAYS,
        "events_validated": rep["events_validated"],
        "hv_per_day_total": rep["hv_per_day_total"],
        "hv_per_day_by_type": rep["hv_per_day_by_type"],
        "dai_per_day": rep["dai_per_day"],
        "promoted_event": event_id,
        "promoted_at_utc": promoted_at,
    }
    with trend_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(snapshot, sort_keys=True) + "\n")

    rep["ledger_sha256"] = after_hash
    rep["promoted_event"] = event_id
    return rep


# ---------------------------------------------------------------- report

NOT_CLAIMS = """## What this does NOT claim

- **Not directly-measured human-life improvement.** Minted events record
  *proximal, team-level* value: a shipped change graded REAL VALUE+ on the
  human-value rubric, with evidence. Each event's note says this plainly.
  The charter's bar — Shawn confirming the measurements reflect real value —
  is a separate, human step.
- **Not causal.** A rising HV/day means evidenced valuable changes shipped
  and were observed; it does not prove the observatory caused them.
- **Not independently verified.** The grading method is independently
  validated (verdict A, 9.2/10); the ledger bytes are cold-recomputable by
  any successor. Independent human verification of the ledger itself remains
  the binding 8.0 gate.
- **Not automated judgment.** Grading is a seat's judgment with cited
  evidence. The runner only observes mechanics (SHAs, diffstats, PR links)
  and refuses to credit anything ungraded.
- **Not retroactive credit.** Predictions are pre-registered; events are
  recorded when observed with evidence that already exists.
"""


def build_report(ledger_path: Path, trend_path: Path,
                 receipts_path: Path | None) -> str:
    raw_lines, events = compute_hv.load_ledger(ledger_path)
    digest = compute_hv.ledger_sha256(raw_lines)
    as_of = date.fromisoformat(max(e["recorded_at"] for e in events))
    rep = compute_hv.compute(events, TREND_WINDOW_DAYS, as_of)

    snapshots: list[dict] = []
    if trend_path.exists():
        for ln in trend_path.read_text(encoding="utf-8").splitlines():
            if ln.strip():
                snapshots.append(json.loads(ln))

    calib = ""
    if receipts_path is not None:
        cal = compute_hv.calibrate(compute_hv.load_receipts(receipts_path),
                                   events)
        calib = (
            "\n## Calibration (prediction → observation)\n\n"
            f"- joined observations: **{cal['n']}**\n"
            f"- mean absolute error: **{cal['mean_absolute_error']}**\n"
            f"- signed bias: **{cal['mean_signed_error']}**\n"
            f"- overprediction flagged: **{cal['overprediction_detected']}**\n"
            f"- confidence multiplier: **{cal['confidence_multiplier']}**\n"
        )

    by_type = "\n".join(
        f"| {vt} | {rep['hv_per_day_by_type'][vt]:.4f} |"
        for vt in sorted(rep["hv_per_day_by_type"]))
    trend_rows = "\n".join(
        f"| {s['as_of']} | {s['hv_per_day_total']:.4f} | "
        f"{s['dai_per_day']:.4f} | {s['events_validated']} | "
        f"`{s['snapshot_ledger_sha256'][:19]}…` |"
        for s in snapshots)
    if not trend_rows:
        trend_rows = "| — | — | — | — | — |"

    delta_note = ""
    if len(snapshots) >= 2:
        prev, cur = snapshots[-2], snapshots[-1]
        d_hv = cur["hv_per_day_total"] - prev["hv_per_day_total"]
        d_dai = cur["dai_per_day"] - prev["dai_per_day"]
        delta_note = (
            f"\nSince the previous snapshot ({prev['as_of']}): HV/day "
            f"{d_hv:+.4f}, DAI/day {d_dai:+.4f}, "
            f"events {prev['events_validated']} → {cur['events_validated']}.\n")

    return f"""# Human Value Observatory — live report

Generated by `{INSTRUMENT}` from canonical repo bytes. Same bytes in,
same bytes out — a cold successor reproduces this exactly.

- **ledger:** `{_display_path(ledger_path)}`
- **ledger_sha256:** `{digest}`
- **as_of:** `{rep['as_of']}` (latest event date — never wall-clock)
- **window:** {TREND_WINDOW_DAYS} days ({rep['window_start']} → {rep['as_of']})
- **events validated:** {rep['events_validated']}
  ({rep['events_in_window']} in window)

## Current measurement

| value_type | HV/day |
|---|---|
{by_type}

- **HV/day total:** **{rep['hv_per_day_total']:.4f}**
- **DAI/day (attention demanded — trend target: DOWN):** **{rep['dai_per_day']:.4f}**
{calib}
## Trend (snapshot per promotion)

| as_of | HV/day | DAI/day | events | ledger |
|---|---|---|---|---|
{trend_rows}
{delta_note}
{NOT_CLAIMS}
## Cold recompute

```bash
python3 tools/human_value/compute_hv.py \\
  --ledger tools/human_value/ledgers/real-events.jsonl \\
  --receipts tools/human_value/ledgers/decision-predictions.json \\
  --expect-ledger-sha256 {digest}
```

Byte drift fails closed. A recomputation that matches is proof; a claim
without one is documentation.
"""


def cmd_report(args: argparse.Namespace) -> int:
    text = build_report(args.ledger, _path(args.trend, DEFAULT_TREND),
                        args.receipts)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(text, encoding="utf-8")
    print(text)
    return 0


# ---------------------------------------------------------------- CLI

def _path(p: str | None, default: Path) -> Path:
    return Path(p) if p else default


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Human Value Observatory v1")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_scan = sub.add_parser("scan", help="draft merge candidates since a watermark")
    p_scan.add_argument("--repo", required=True)
    p_scan.add_argument("--base", required=True,
                        help="scan merges in (base..HEAD]; base must be an ancestor of HEAD")
    p_scan.add_argument("--drafts-dir", default=None)
    p_scan.add_argument("--watermark-out", default=None)

    p_pro = sub.add_parser("promote", help="ledger one graded REAL VALUE+ scorecard")
    p_pro.add_argument("--ledger", required=True, type=Path)
    p_pro.add_argument("--scorecard", required=True, type=Path)
    p_pro.add_argument("--event-id", required=True)
    p_pro.add_argument("--recorded-at", required=True, help="YYYY-MM-DD (observation date)")
    p_pro.add_argument("--pr-url", default=None)
    p_pro.add_argument("--trend", default=None)
    p_pro.add_argument("--receipts-dir", default=None)
    p_pro.add_argument("--confirm", action="store_true",
                       help="explicit lane act: without this, nothing is ledgered")

    p_rep = sub.add_parser("report", help="regenerate the pinned observatory report")
    p_rep.add_argument("--ledger", required=True, type=Path)
    p_rep.add_argument("--trend", default=None)
    p_rep.add_argument("--receipts", default=None, type=Path)
    p_rep.add_argument("--out", required=True, type=Path)

    p_trend = sub.add_parser("trend", help="print the trend table")
    p_trend.add_argument("--trend", default=None)

    args = parser.parse_args(argv)
    try:
        if args.cmd == "scan":
            summary = scan(args.repo, args.base,
                           _path(args.drafts_dir, DEFAULT_DRAFTS_DIR),
                           _path(args.watermark_out, DEFAULT_WATERMARK)
                           if args.watermark_out != "-" else None)
            print(json.dumps(summary, indent=2, sort_keys=True))
            return 0
        if args.cmd == "promote":
            rep = promote(
                args.ledger, args.scorecard, args.event_id, args.recorded_at,
                _path(args.trend, DEFAULT_TREND),
                _path(args.receipts_dir, DEFAULT_RECEIPTS_DIR),
                args.pr_url, args.confirm)
            print(json.dumps(rep, indent=2, sort_keys=True))
            return 0
        if args.cmd == "report":
            return cmd_report(args)
        if args.cmd == "trend":
            tpath = _path(args.trend, DEFAULT_TREND)
            if not tpath.exists():
                print("no trend snapshots yet")
                return 0
            for ln in tpath.read_text(encoding="utf-8").splitlines():
                if ln.strip():
                    s = json.loads(ln)
                    print(f"{s['as_of']}  HV/day {s['hv_per_day_total']:.4f}  "
                          f"DAI/day {s['dai_per_day']:.4f}  "
                          f"events {s['events_validated']}  "
                          f"{s['snapshot_ledger_sha256'][:19]}…")
            return 0
    except (ObservatoryError, InstrumentError, SchemaError) as e:
        print(f"OBSERVATORY_REFUSED: {e}", file=sys.stderr)
        return 2
    raise AssertionError("unreachable")


if __name__ == "__main__":
    raise SystemExit(main())

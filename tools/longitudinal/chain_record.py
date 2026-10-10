#!/usr/bin/env python3
"""C5.5 — Lesson→Outcome Chain Completion (LOCC).

Measures complete compounding chains: captured → retrieved (by anyone,
including a cold successor) → applied → measured outcome improvement. The tool
records each chain with evidence refs at every link and checks that an
INDEPENDENT seat verified and signed it.

Machine checks per chain (honest about limits):
- exactly the four stages, in order: captured, retrieved, applied, outcome.
  A chain with a missing or misordered link is incomplete — reported with the
  diagnosis, never rounded up.
- every link carries a non-empty evidence_ref ("checkable": a ref a human can
  follow and verify).
- every link naming an evidence_path resolves to a file that exists under
  --repo-root. A path that does not exist is not evidence.
- independent verification: verification.verifier_seat is present and different
  from author_seat, verified_at parses, and the verification statement is
  non-empty. "Signed" here means a recorded, timestamped verification statement
  by the named seat — the instrument records the claim; it cannot cryptographically
  prove who typed it. Human-verified second, per the design.
- window attribution: when window_start/window_end are given, verified_at must
  fall inside; chains verified outside the window are reported, not counted.

Privacy-architectural note: inputs are deliberately-contributed artifacts only
(chain records, repo paths). There is no input channel for private
communications.

DONE WHEN (design v2.0): >= 3 fully-evidenced chains per 14-day window, each
link carrying a checkable evidence ref, each chain independently verified.

Exit codes: 0 = >= min complete in-window chains; 1 = below bar;
2 = unreadable/malformed input.

Stdlib only. Deterministic given --now.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

VERSION = "1.0.0"
DEFAULT_MIN_CHAINS = 3
REQUIRED_STAGES = ("captured", "retrieved", "applied", "outcome")


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


def load_chains(path: Path) -> list[dict]:
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot read chains manifest {path}: {exc}") from exc
    items = raw["chains"] if isinstance(raw, dict) and "chains" in raw else raw
    if not isinstance(items, list):
        raise ValueError("chains manifest must be a list or {'chains': [...]}")
    chains = []
    for i, item in enumerate(items):
        if not isinstance(item, dict):
            raise ValueError(f"chains[{i}] must be an object")
        chain_id = str(item.get("chain_id", "")).strip()
        if not chain_id:
            raise ValueError(f"chains[{i}] needs a non-empty chain_id")
        links = item.get("links")
        if not isinstance(links, list):
            raise ValueError(f"chains[{i}] ({chain_id}) links must be a list")
        norm_links = []
        for j, link in enumerate(links):
            if not isinstance(link, dict):
                raise ValueError(f"chains[{i}].links[{j}] must be an object")
            norm_links.append({
                "stage": str(link.get("stage", "")).strip().lower(),
                "evidence_ref": str(link.get("evidence_ref", "")).strip(),
                "evidence_path": str(link.get("evidence_path", "") or "").strip(),
                "note": str(link.get("note", "")).strip(),
            })
        verification = item.get("verification") or {}
        if not isinstance(verification, dict):
            raise ValueError(f"chains[{i}] ({chain_id}) verification must be an object")
        window_start = window_end = None
        for key in ("window_start", "window_end"):
            if item.get(key):
                try:
                    parsed = parse_ts(item[key])
                except ValueError as exc:
                    raise ValueError(
                        f"chains[{i}] ({chain_id}) bad {key}: {exc}") from exc
                if key == "window_start":
                    window_start = parsed
                else:
                    window_end = parsed
        chains.append({
            "chain_id": chain_id,
            "window_id": str(item.get("window_id", "")).strip(),
            "window_start": window_start,
            "window_end": window_end,
            "sn_id": str(item.get("sn_id", "")).strip(),
            "author_seat": str(item.get("author_seat", "UNKNOWN")).strip() or "UNKNOWN",
            "links": norm_links,
            "verification": {
                "verifier_seat": str(verification.get("verifier_seat", "")).strip(),
                "verified_at": str(verification.get("verified_at", "")).strip(),
                "statement": str(verification.get("statement", "")).strip(),
            },
        })
    return chains


def check_chain(chain: dict, repo_root: Path) -> dict:
    diagnostics: list[str] = []
    stages = [l["stage"] for l in chain["links"]]
    if stages != list(REQUIRED_STAGES):
        diagnostics.append(
            f"stages must be exactly {list(REQUIRED_STAGES)} in order; found {stages}"
        )
    for pos, link in enumerate(chain["links"]):
        if not link["evidence_ref"]:
            diagnostics.append(f"link[{pos}] ({link['stage'] or '?'}) has no evidence_ref")
        if link["evidence_path"]:
            target = repo_root / link["evidence_path"]
            if not target.is_file():
                diagnostics.append(
                    f"link[{pos}] ({link['stage'] or '?'}) evidence_path "
                    f"{link['evidence_path']!r} does not exist"
                )
    verification = chain["verification"]
    verified_at = None
    if not verification["verifier_seat"]:
        diagnostics.append("verification missing verifier_seat")
    elif verification["verifier_seat"] == chain["author_seat"]:
        diagnostics.append(
            f"verifier_seat {verification['verifier_seat']!r} is the author seat: "
            "verification is not independent"
        )
    if not verification["verified_at"]:
        diagnostics.append("verification missing verified_at")
    else:
        try:
            verified_at = parse_ts(verification["verified_at"])
        except ValueError:
            diagnostics.append(
                f"verification verified_at {verification['verified_at']!r} unparseable"
            )
    if not verification["statement"]:
        diagnostics.append("verification statement is empty")

    in_window = True
    if chain["window_start"] and chain["window_end"] and verified_at:
        in_window = chain["window_start"] <= verified_at <= chain["window_end"]
        if not in_window:
            diagnostics.append(
                f"verified_at {verified_at.isoformat()} outside window "
                f"[{chain['window_start'].isoformat()}, {chain['window_end'].isoformat()}]"
            )

    complete = not diagnostics
    return {
        "chain_id": chain["chain_id"],
        "window_id": chain["window_id"],
        "sn_id": chain["sn_id"],
        "author_seat": chain["author_seat"],
        "verifier_seat": verification["verifier_seat"] or None,
        "complete": complete,
        "in_window": in_window,
        "counted": complete and in_window,
        "diagnostics": diagnostics,
        "links": [
            {"stage": l["stage"], "evidence_ref": l["evidence_ref"],
             "evidence_path": l["evidence_path"] or None}
            for l in chain["links"]
        ],
    }


def compute_report(chains: list[dict], *, repo_root: Path, min_chains: int) -> dict:
    checked = [check_chain(c, repo_root) for c in chains]
    counted = [c for c in checked if c["counted"]]
    passed = len(counted) >= min_chains
    reasons = []
    if not passed:
        reasons.append(
            f"only {len(counted)} complete independently-verified in-window "
            f"chain(s) (minimum {min_chains})"
        )
    return {
        "component": "C5.5",
        "metric": "lesson_outcome_chain_completion",
        "version": VERSION,
        "min_chains": min_chains,
        "chains_total": len(checked),
        "chains_complete": len(counted),
        "pass": passed,
        "fail_reasons": reasons,
        "chains": checked,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="C5.5 — Lesson→Outcome Chain Completion (LOCC): chain recorder"
    )
    parser.add_argument("--chains-json", required=True, type=Path,
                        help="JSON manifest: list or {'chains': [...]} of "
                             "{chain_id, window_id?, window_start?, window_end?, "
                             "sn_id?, author_seat, links[{stage, evidence_ref, "
                             "evidence_path?, note?}], "
                             "verification{verifier_seat, verified_at, statement}}")
    parser.add_argument("--repo-root", type=Path, default=Path("."),
                        help="Root that evidence_path entries resolve against")
    parser.add_argument("--min-chains", type=int, default=DEFAULT_MIN_CHAINS)
    parser.add_argument("--report-out", type=Path, default=None,
                        help="Write the JSON report to this path")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        chains = load_chains(args.chains_json)
    except ValueError as exc:
        print(f"input error: {exc}", file=sys.stderr)
        return 2
    if args.min_chains <= 0:
        print("input error: --min-chains must be positive", file=sys.stderr)
        return 2

    report = compute_report(chains, repo_root=args.repo_root,
                            min_chains=args.min_chains)
    text = json.dumps(report, indent=2)
    if args.report_out:
        args.report_out.write_text(text + "\n", encoding="utf-8")
    else:
        print(text)
    print(
        f"C5.5 LOCC: {report['chains_complete']}/{report['chains_total']} complete "
        f"independently-verified chains (minimum {report['min_chains']}) "
        f"-> {'PASS' if report['pass'] else 'FAIL'}",
        file=sys.stderr,
    )
    return 0 if report["pass"] else 1


if __name__ == "__main__":
    sys.exit(main())

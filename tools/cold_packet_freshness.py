"""Machine-enforced freshness check for COLD-START-PACKET.md.

Reads COLD-START-PACKET.pin.json, resolves the live main tip, and FAILS
CLOSED when the packet's pin is stale — naming the stale pin and the live
tip. The cold agent runs this BEFORE the packet's acceptance test
(freshness section, step 0).

STALE reasons (SLA proposed by the builder seat; Naya 1 ratifies):
  - PIN_TOO_OLD:        pin older than sla.max_age_hours
  - TIP_MOVED_PAST_SLA: live main more than sla.max_commits_past_pin
                        commits ahead of the pin
  - ENFORCEMENT_DRIFT:  any of the 7 enforcement files differs at the live
                        tip vs the pin (byte-level, sha256)

Exit codes: 0 = FRESH (the acceptance path is as the packet proved it);
3 = STALE (do not run the acceptance test — it would measure packet
staleness, not your activation); 2 = usage/internal error.

Only stdlib. Network: public GitHub endpoints, no auth. A local git object
store is used when it already contains the needed commits.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

REPO = "SoulSchoolAcademy/NayaPOWER"
LS_REMOTE = ["git", "ls-remote",
             f"https://github.com/{REPO}.git", "refs/heads/main"]
STALE_EXIT = 3
NET_TIMEOUT = 20


def _http_json(url: str) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": "naya-cold-packet-freshness"})
    with urllib.request.urlopen(req, timeout=NET_TIMEOUT) as r:
        return json.loads(r.read().decode())


def _http_bytes(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "naya-cold-packet-freshness"})
    with urllib.request.urlopen(req, timeout=NET_TIMEOUT) as r:
        return r.read()


def _git(args: list[str], cwd: Path) -> str | None:
    try:
        p = subprocess.run(["git"] + args, capture_output=True, text=True,
                           timeout=30, cwd=str(cwd))
    except (OSError, subprocess.TimeoutExpired):
        return None
    return p.stdout.strip() if p.returncode == 0 else None


def resolve_tip(repo_root: Path) -> tuple[str, str]:
    """Return (tip_sha, how). Raises RuntimeError when unresolvable."""
    out = _git(LS_REMOTE[1:], repo_root)
    if out:
        return out.split()[0], "git ls-remote"
    out = _git(["rev-parse", "origin/main"], repo_root)
    if out:
        return out, "local origin/main (ls-remote unreachable)"
    raise RuntimeError(
        "could not resolve the live main tip (ls-remote failed and no "
        "local origin/main). Cannot prove freshness.")


def commits_ahead(pin: str, tip: str, repo_root: Path) -> int | None:
    """Commits on main past the pin. None when unmeasurable."""
    try:
        cmp = _http_json(f"https://api.github.com/repos/{REPO}/compare/{pin}...{tip}")
        if cmp.get("status") in ("ahead", "identical", "diverged"):
            return int(cmp.get("ahead_by", 0))
    except Exception:
        pass
    out = _git(["rev-list", "--count", f"{pin}..{tip}"], repo_root)
    if out is not None:
        try:
            return int(out)
        except ValueError:
            pass
    return None


def file_sha256_at_tip(path: str, tip: str, repo_root: Path) -> str | None:
    """sha256 of the file's bytes at the live tip. None when unreadable."""
    data = _http_file_bytes(path, tip)
    if data is not None:
        return hashlib.sha256(data).hexdigest()
    raw = _git(["cat-file", "-p", f"{tip}:{path}"], repo_root)
    if raw is not None:
        return hashlib.sha256(raw.encode()).hexdigest()
    return None


def _http_file_bytes(path: str, tip: str) -> bytes | None:
    try:
        return _http_bytes(f"https://raw.githubusercontent.com/{REPO}/{tip}/{path}")
    except Exception:
        return None


def main(argv: list[str] | None = None) -> int:
    here = Path(__file__).resolve()
    repo_root = here.parents[1]
    pin_path = repo_root / "COLD-START-PACKET.pin.json"
    if not pin_path.exists():
        print("STALE: COLD-START-PACKET.pin.json missing — "
              "no pin to check freshness against.", file=sys.stderr)
        return STALE_EXIT
    pin_doc = json.loads(pin_path.read_text())
    pin = pin_doc["pin"]
    sla = pin_doc["sla"]
    try:
        tip, how = resolve_tip(repo_root)
    except RuntimeError as exc:
        print(f"STALE_UNVERIFIABLE: {exc}", file=sys.stderr)
        print(f"pin: {pin}", file=sys.stderr)
        return STALE_EXIT

    reasons: list[str] = []

    pinned_at = datetime.fromisoformat(pin_doc["pinned_at"])
    age_h = (datetime.now(timezone.utc) - pinned_at).total_seconds() / 3600
    if age_h > sla["max_age_hours"]:
        reasons.append(f"PIN_TOO_OLD: pin is {age_h:.1f}h old "
                       f"(SLA: {sla['max_age_hours']}h)")

    ahead = commits_ahead(pin, tip, repo_root)
    if ahead is None:
        reasons.append("DISTANCE_UNKNOWN: could not measure commits "
                       "pin..tip — refusing to call it fresh")
    elif ahead > sla["max_commits_past_pin"]:
        reasons.append(f"TIP_MOVED_PAST_SLA: live main is {ahead} commits past "
                       f"the pin (SLA: {sla['max_commits_past_pin']})")

    drifted: list[str] = []
    unreadable: list[str] = []
    if sla.get("enforcement_files_must_match_pin", True):
        for path, want in pin_doc["enforcement_files"].items():
            got = file_sha256_at_tip(path, tip, repo_root)
            if got is None:
                unreadable.append(path)
            elif got != want:
                drifted.append(path)
    if unreadable:
        reasons.append("ENFORCEMENT_UNREADABLE at live tip: "
                       + ", ".join(unreadable))
    if drifted:
        reasons.append("ENFORCEMENT_DRIFT at live tip: " + ", ".join(drifted))

    if reasons:
        print("STALE — do not run the packet acceptance test; "
              "it would measure packet staleness, not your activation.",
              file=sys.stderr)
        print(f"stale pin: {pin}", file=sys.stderr)
        print(f"live tip:  {tip} (via {how})", file=sys.stderr)
        for r in reasons:
            print(f"  - {r}", file=sys.stderr)
        return STALE_EXIT

    dist = f"{ahead} commits past pin" if ahead is not None else "distance n/a"
    n_files = len(pin_doc["enforcement_files"])
    print(f"FRESH: pin {pin[:12]}… == live tip {tip[:12]}… "
          f"(via {how}); age {age_h:.1f}h; {dist}; "
          f"enforcement files {n_files}/{n_files} match the pin.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

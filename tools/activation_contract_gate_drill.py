#!/usr/bin/env python3
"""
activation_contract_gate_drill.py — WIRE lane: live violation drill for #2244 req 1.

Proves the activation-contract wire on the LIVE tree. The drill shells out to
the REAL tools/activation_contract.py CLI (the exact executable the CI gate
runs), with the live tip derived independently via `git rev-parse HEAD` —
never taken from the claim.

Cases:
  GREEN       — well-formed claim built from the live tree's actual bytes
                must PROCEED (exit 0).
  DRIFT       — one tampered byte in the protocol artifact (claim carries the
                TRUE hash) must STAND_DOWN with PROTOCOL_DRIFT.
  STALE_SHA   — claim naming a wrong main SHA must STAND_DOWN with STALE_SHA.
  STALE_BOARD — claim naming #1354 as the live board must STAND_DOWN with
                STALE_BOARD.
  UNKNOWN_FEED— claim reading a non-canonical feed must STAND_DOWN with
                UNKNOWN_FEED.

If any violation PROCEEDs, or GREEN fails, the drill exits 1: the wire is
broken and the CI check goes red. A bypassed wire cannot pass this drill.

Exit codes: 0 = wire proven (green + every violation blocked); 1 = wire broken.
"""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile

MS_PATH = "BRAIN/CURRENT-MISSION-STATE.md"
PROTOCOL_PATH = "BRAIN/01-GOVERNANCE/TEAM-NAYA-OPERATING-PROTOCOL-V1.md"


def sh(*args: str, cwd: str | None = None) -> str:
    r = subprocess.run(args, capture_output=True, text=True, cwd=cwd, timeout=60)
    if r.returncode != 0:
        raise RuntimeError(f"command failed: {' '.join(args)}: {r.stderr.strip()}")
    return r.stdout.strip()


def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def base_claim(root: str, live_tip: str) -> dict:
    return {
        "worker_id": "wire-drill",
        "lane": "naya2/wire",
        "main_sha": live_tip,
        "mission_state": {
            "path": MS_PATH,
            "sha256": sha256_file(os.path.join(root, MS_PATH)),
        },
        "protocol": {
            "path": PROTOCOL_PATH,
            "sha256": sha256_file(os.path.join(root, PROTOCOL_PATH)),
        },
        "feeds_read": [1870, 1872],
        "sign_in_feed": 1870,
        "sign_in_evidence": "drill: no real sign-in performed",
        "board_ack": "live coordination board is #2175 (issue #1354 is archive-only)",
        "toc_ack": "TOC is #1599",
    }


def run_cli(cli: str, claim: dict, live_tip: str, repo_root: str) -> tuple[int, str]:
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
        json.dump(claim, f)
        claim_path = f.name
    try:
        r = subprocess.run(
            [sys.executable, cli, "--claim", claim_path,
             "--live-tip", live_tip, "--repo-root", repo_root],
            capture_output=True, text=True, timeout=120,
        )
        return r.returncode, (r.stdout + r.stderr).strip()
    finally:
        os.unlink(claim_path)


def main() -> int:
    root = sh("git", "rev-parse", "--show-toplevel")
    cli = os.path.join(root, "tools", "activation_contract.py")
    if not os.path.isfile(cli):
        print(f"WIRE_BROKEN: verifier missing at {cli}")
        return 1
    live_tip = sh("git", "-C", root, "rev-parse", "HEAD")
    if len(live_tip) != 40 or any(c not in "0123456789abcdef" for c in live_tip):
        print(f"WIRE_BROKEN: could not derive live tip (got {live_tip!r})")
        return 1

    failures: list[str] = []

    def expect(name: str, claim: dict, tip: str, repo: str,
               want_code: int, want_verdict: str, want_marker: str = "") -> None:
        code, out = run_cli(cli, claim, tip, repo)
        ok = (code == want_code and want_verdict in out
              and (not want_marker or want_marker in out))
        print(f"[{'ok' if ok else 'FAIL'}] {name}: exit={code} "
              f"want exit={want_code} verdict={want_verdict}"
              + (f" marker={want_marker}" if want_marker else ""))
        if not ok:
            failures.append(name)
            print(f"       output was: {out[:400]}")

    print(f"drill: live tip {live_tip[:12]}… repo {root}")

    # GREEN — honest claim from live bytes must PROCEED.
    expect("GREEN honest claim PROCEEDs",
           base_claim(root, live_tip), live_tip, root,
           0, "PROCEED")

    # DRIFT — tampered protocol bytes, claim carries the TRUE hash.
    tamper = tempfile.mkdtemp(prefix="ac-drill-")
    try:
        os.makedirs(os.path.join(tamper, "BRAIN", "01-GOVERNANCE"), exist_ok=True)
        shutil.copyfile(os.path.join(root, MS_PATH),
                        os.path.join(tamper, MS_PATH))
        tampered = os.path.join(tamper, PROTOCOL_PATH)
        shutil.copyfile(os.path.join(root, PROTOCOL_PATH), tampered)
        with open(tampered, "ab") as f:
            f.write(b"\n<!-- drill tamper: one byte -->\n")
        expect("DRIFT tampered protocol STAND_DOWNs",
               base_claim(root, live_tip), live_tip, tamper,
               1, "STAND_DOWN", "PROTOCOL_DRIFT")
    finally:
        shutil.rmtree(tamper, ignore_errors=True)

    # STALE_SHA — claim names a SHA that is not the live tip.
    stale = base_claim(root, live_tip)
    stale["main_sha"] = "0" * 40
    expect("STALE_SHA wrong main SHA STAND_DOWNs",
           stale, live_tip, root, 1, "STAND_DOWN", "STALE_SHA")

    # STALE_BOARD — claim names the archive board as live.
    old_board = base_claim(root, live_tip)
    old_board["board_ack"] = "the live coordination board is #1354"
    expect("STALE_BOARD #1354-as-live STAND_DOWNs",
           old_board, live_tip, root, 1, "STAND_DOWN", "STALE_BOARD")

    # UNKNOWN_FEED — claim reads a feed outside the nine ratified.
    bad_feed = base_claim(root, live_tip)
    bad_feed["feeds_read"] = [1870, 9999]
    expect("UNKNOWN_FEED non-canonical feed STAND_DOWNs",
           bad_feed, live_tip, root, 1, "STAND_DOWN", "UNKNOWN_FEED")

    if failures:
        print(f"\nWIRE_BROKEN: {len(failures)} drill case(s) misbehaved: {failures}")
        return 1
    print("\nWIRE_PROVEN: green proceeds; all 4 violations blocked.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

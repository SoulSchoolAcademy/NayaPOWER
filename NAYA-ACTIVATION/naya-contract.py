#!/usr/bin/env python3
"""THE NAYA CONTRACT — machine law. Version 1, 2026-10-13.

Enforces the checkable parts of the contract:
  activate        issue an activation receipt (seat, lane, own-words essence)
  check-activation  validate a receipt (schema, freshness, non-parrot)
  signout         validate a sign-out (drift line, proof, honest score)
  oath            print the canonical oath
  process         print the 9-step process loop as JSON
  integrity       verify this file's bytes match the pinned hash

Exit 0 = law holds. Exit 1 = violation (the run stops).
"""
from __future__ import annotations
import argparse, hashlib, json, os, sys
from datetime import datetime, timezone

CONTRACT_VERSION = "1"
# Pinned at enactment (Shawn's word, 2026-10-13). Re-pin ONLY on his word.
PINNED_SHA256 = "4cdca783a80faaa2482f3ed315b678fe671f70a6532cef1d3208bf7e84aea2f6"

OATH = (
    "I am Naya. I do the most intelligent thing available \u2014 always. "
    "I never trust memory over measurement. I score my options instead of guessing. "
    'I prove my work with receipts, never "trust me." '
    "A lesson counts as learned only when a future decision changes because of it. "
    "I fix what is broken instead of describing it. "
    "I protect Shawn\u2019s attention like the scarcest resource in the world. "
    "I sign under my own name, own my mistakes in public, and correct the record the moment it is wrong. "
    "I never stop growing. I treat every Naya and every human as precious. "
    "I do not waver \u2014 not today, not when it is hard, not when no one is watching. "
    "Especially when no one is watching."
)

PROCESS = [
    ("WAKE", "Read the law, the briefing, the mission state."),
    ("ACTIVATE", "Re-read the oath; state seat/lane; state the essence in your own words."),
    ("SENSE", "Anchor: live ref, queue top, venue tail. Name assumptions."),
    ("DECIDE", "Scorecard under uncertainty; record the scoring."),
    ("ACT", "Smallest effective change; fix within authority."),
    ("PROVE", "Receipts: live handles, exact SHAs, negative controls."),
    ("LEARN", "Capture, distill with falsifier, wire into bytes with owner."),
    ("SIGN OUT", "What, why, proof, remains, honest score, one drift line."),
    ("REST", "The next action will find you. Repeat."),
]

OATH_SENTENCES = [s.strip() for s in OATH.replace("\u2014", "-").split(". ") if s.strip()]


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _is_parrot(essence: str) -> bool:
    e = " ".join(essence.lower().split())
    if len(e) < 20:
        return True  # too short to be understanding
    for s in OATH_SENTENCES:
        norm = " ".join(s.lower().strip(". ").split())
        if len(norm) > 25 and norm in e:
            return True
    return False


def cmd_activate(a) -> int:
    essence = (a.essence or "").strip()
    if not a.seat.strip() or not a.lane.strip():
        print("VIOLATION: seat and lane are required", file=sys.stderr)
        return 1
    if _is_parrot(essence):
        print("VIOLATION: essence parrots the oath or is too short — understanding required", file=sys.stderr)
        return 1
    receipt = {
        "contract": "naya-contract-v1",
        "utc": _now(),
        "seat": a.seat.strip(),
        "lane": a.lane.strip(),
        "essence": essence,
        "oath_sha256": hashlib.sha256(OATH.encode()).hexdigest()[:16],
    }
    out = json.dumps(receipt, indent=2)
    if a.out:
        with open(a.out, "w") as f:
            f.write(out + "\n")
    print(out)
    return 0


def _load_receipt(path: str):
    try:
        with open(path) as f:
            return json.load(f), None
    except Exception as e:
        return None, f"unreadable receipt: {e}"


def cmd_check_activation(a) -> int:
    r, err = _load_receipt(a.receipt)
    if err:
        print(f"VIOLATION: {err}", file=sys.stderr)
        return 1
    for k in ("contract", "utc", "seat", "lane", "essence"):
        if not r.get(k):
            print(f"VIOLATION: receipt missing '{k}'", file=sys.stderr)
            return 1
    if r.get("contract") != "naya-contract-v1":
        print("VIOLATION: wrong contract version", file=sys.stderr)
        return 1
    try:
        ts = datetime.strptime(r["utc"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
        age_h = (datetime.now(timezone.utc) - ts).total_seconds() / 3600
    except Exception:
        print("VIOLATION: bad receipt timestamp", file=sys.stderr)
        return 1
    if age_h > a.max_age_hours or age_h < -0.05:
        print(f"VIOLATION: receipt age {age_h:.2f}h outside 0..{a.max_age_hours}h", file=sys.stderr)
        return 1
    if _is_parrot(r["essence"]):
        print("VIOLATION: receipt essence parrots the oath", file=sys.stderr)
        return 1
    print(f"ACTIVATION VALID — {r['seat']} / {r['lane']} @ {r['utc']}")
    return 0


def cmd_signout(a) -> int:
    drift = (a.drift or "").strip()
    if not drift:
        print("VIOLATION: sign-out requires one drift line (or 'drift: none')", file=sys.stderr)
        return 1
    try:
        score = float(a.score)
    except (TypeError, ValueError):
        print("VIOLATION: honest score 0-10 required", file=sys.stderr)
        return 1
    if not (0 <= score <= 10):
        print("VIOLATION: score outside 0-10", file=sys.stderr)
        return 1
    if not (a.done or "").strip():
        print("VIOLATION: sign-out must state what was done", file=sys.stderr)
        return 1
    print(json.dumps({
        "contract": "naya-contract-v1", "utc": _now(), "done": a.done.strip(),
        "proof": (a.proof or "").strip(), "score": score, "drift": drift,
    }, indent=2))
    return 0


def cmd_integrity(a) -> int:
    with open(os.path.abspath(__file__), "rb") as f:
        raw = f.read().decode("utf-8", "replace")
    # Normalize: the pin line itself is excluded, so pinning is stable.
    norm = "\n".join(
        l if not l.startswith("PINNED_SHA256") else "PINNED_SHA256 = \"\""
        for l in raw.split("\n")
    )
    digest = hashlib.sha256(norm.encode()).hexdigest()
    if PINNED_SHA256 == "REPLACE_AT_ENACTMENT":
        print(f"INTEGRITY UNPINNED — current sha256: {digest}")
        print("Pin it at enactment; re-pin ONLY on Shawn's word.")
        return 0
    if digest == PINNED_SHA256:
        print("INTEGRITY HOLD — contract bytes match the pinned hash")
        return 0
    print(f"VIOLATION: contract bytes changed — expected {PINNED_SHA256[:12]} got {digest[:12]}", file=sys.stderr)
    return 1


def main() -> int:
    p = argparse.ArgumentParser(prog="naya-contract")
    sub = p.add_subparsers(dest="cmd", required=True)

    a = sub.add_parser("activate")
    a.add_argument("--seat", required=True)
    a.add_argument("--lane", required=True)
    a.add_argument("--essence", required=True)
    a.add_argument("--out", default=None)

    c = sub.add_parser("check-activation")
    c.add_argument("--receipt", required=True)
    c.add_argument("--max-age-hours", type=float, default=24)

    s = sub.add_parser("signout")
    s.add_argument("--drift", required=True)
    s.add_argument("--done", required=True)
    s.add_argument("--proof", default="")
    s.add_argument("--score", required=True)

    sub.add_parser("oath")
    sub.add_parser("process")
    sub.add_parser("integrity")

    args = p.parse_args()
    if args.cmd == "activate":
        return cmd_activate(args)
    if args.cmd == "check-activation":
        return cmd_check_activation(args)
    if args.cmd == "signout":
        return cmd_signout(args)
    if args.cmd == "oath":
        print(OATH)
        return 0
    if args.cmd == "process":
        print(json.dumps([{"step": i + 1, "name": n, "what": w} for i, (n, w) in enumerate(PROCESS)], indent=2))
        return 0
    if args.cmd == "integrity":
        return cmd_integrity(args)
    return 2


if __name__ == "__main__":
    sys.exit(main())

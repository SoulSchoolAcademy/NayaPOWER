#!/usr/bin/env python3
"""
lane_state.py — mechanical lane-claim arbitration (Kappa §7 as code).

Given a lane feed's comments (fetched via gh-api), deterministically answer
FREE, OCCUPIED, or STALE-SUSPECT. No guessing: the answer is a pure function
of the comment stream, newest-first, per the claim-then-verify contract:

  - a VALID sign-out after the last sign-in            -> FREE
  - a VALID sign-in with no later sign-out, in lease  -> OCCUPIED
  - a VALID sign-in with no later sign-out, lease dead -> STALE-SUSPECT
    (treated as FREE for dispatch, but flagged — reclaim needs the public
    ping + 30-minute grace per the law, not a silent takeover)
  - anything else (chatter, stand-down receipts, noise) -> not state

A VALID sign-in carries: the lane, a specific mission, a UTC claim time.
A sign-in missing lane+mission is noise, not a claim (grandfather clause:
claims posted before 2026-10-12 are judged valid on lane+mission+time).

Claim time is ALWAYS the comment's server created_at — never a "~" time
written in the body. Sign-outs routinely carry estimated end-times;
precedence is by posted time, not stated time.

Usage:
  lane_state.py check --lane alpha [--lease-minutes 120]
  lane_state.py verify --lane alpha --my-created-at 2026-10-12T04:15:00Z
      (claim-minute re-poll: WON if no earlier valid sign-in stands, else LOST)

Exit codes: 0 ok | 2 lane state indeterminate (fetch failed)
"""

import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone, timedelta

GH_API = os.path.expanduser("~/workspace/naya/bin/gh-api")
REPO = "SoulSchoolAcademy/NayaPOWER"
LANES = {"alpha": "1713", "beta": "1714", "gamma": "1715"}
LEASE_DEFAULT_MIN = 120
GRACE_DEFAULT_MIN = 30
MAX_PAGES = 10
PER_PAGE = 100

# ---------------------------------------------------------------------------
# Comment classification
# ---------------------------------------------------------------------------

SIGNIN_RE = re.compile(r"\bsign[\s_\-]*ins?\b|\bsigning in\b", re.IGNORECASE)
SIGNOUT_RE = re.compile(r"\bsign[\s_\-]*outs?\b|\bsigning out\b", re.IGNORECASE)
STANDDOWN_RE = re.compile(r"stand[\s_\-]*down", re.IGNORECASE)
LANE_RE = re.compile(r"\b(alpha|beta|gamma)\b|#(1713|1714|1715)\b", re.IGNORECASE)
MISSION_RE = re.compile(r"\bmission\b", re.IGNORECASE)
TIME_RE = re.compile(
    r"\b\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}(:\d{2})?Z?\b"  # ISO-ish
    r"|\b\d{1,2}:\d{2}\s*(Z|UTC)\b"                      # 04:15Z
    r"|~\d{2}:\d{2}Z", re.IGNORECASE)
REPOLL_RE = re.compile(r"re[\s_\-]*poll|stand down on collision|full last-page read",
                       re.IGNORECASE)


NOT_SIGNING_RE = re.compile(
    r"will not sign in|not signing in|do not sign in|never signed in|"
    r"did not sign in|won't sign in|not going to sign in", re.IGNORECASE)
RECEIPT_RE = re.compile(r"\breceipt\b", re.IGNORECASE)


HEADER_RE = re.compile(r"\[\**\s*([^\[\]]+?)\s*\]\**")
SEAT_RE = re.compile(r"^\s*naya(\s+\d+)?\s*$", re.IGNORECASE)


def claim_line_parts(body):
    """Split the first line into (bracketed_header, rest_of_line).

    The bracketed claim header, when present, outranks the rest of the
    line: a sign-in that *mentions* a prior sign-out ("last event was a
    sign-out") still classifies as a sign-in, because the header decides.
    Conversely the header is EXHAUSTIVE — a bracketed header with no sign
    markers is informational (readiness receipts, scorecards, announcements),
    never a claim, no matter what the body mentions."""
    lines = (body or "").strip().splitlines()
    first = lines[0] if lines else ""
    m = HEADER_RE.search(first)
    if not m:
        return "", first
    bracketed = m.group(0)
    return bracketed, first.replace(bracketed, "", 1)


def classify(body):
    """SIGNIN | SIGNOUT | STANDDOWN | CHATTER. Stand-downs carry no state.

    Precedence: (1) explicit stand-down receipts; (2) the bracketed claim
    header, when the first line carries one; (3) the rest of the first line
    (covers `[Seat] SIGN-OUT 18:55Z` shapes); (4) a bracketed header with no
    sign markers ends the search as CHATTER — the body is not scanned, so a
    readiness receipt describing sign-in/out mechanics can never read as a
    claim; (5) only headerless, first-line-silent bodies fall back to
    body-wide markers."""
    b = body or ""
    bracketed, rest = claim_line_parts(b)
    first = (bracketed + rest).strip() or rest
    # 1. Explicit stand-down receipts are never claims, whatever else they say.
    if STANDDOWN_RE.search(b) and NOT_SIGNING_RE.search(b):
        return "STANDDOWN"
    # 2. The bracketed claim header decides first.
    if bracketed:
        if SIGNOUT_RE.search(bracketed):
            return "SIGNOUT"
        if SIGNIN_RE.search(bracketed):
            return "SIGNIN"
        if STANDDOWN_RE.search(bracketed):
            return "STANDDOWN"
        # 3. Sign marker outside the brackets but still on the claim line.
        if SIGNOUT_RE.search(rest):
            return "SIGNOUT"
        if SIGNIN_RE.search(rest):
            return "SIGNIN"
        if STANDDOWN_RE.search(rest):
            return "STANDDOWN"
        # 4. Bracketed header, no sign markers: informational, not a claim.
        return "CHATTER"
    # 5. No bracketed header: the first line decides; explicit receipt
    #    labels are informational unless a sign marker claims the line.
    if SIGNOUT_RE.search(first):
        return "SIGNOUT"
    if SIGNIN_RE.search(first):
        return "SIGNIN"
    if STANDDOWN_RE.search(first):
        return "STANDDOWN"
    if RECEIPT_RE.search(first):
        return "CHATTER"
    # 6. Headerless, first-line-silent bodies: body-wide markers (legacy).
    if SIGNOUT_RE.search(b):
        return "SIGNOUT"
    if SIGNIN_RE.search(b):
        return "SIGNIN"
    return "CHATTER"


def normalize_seat(seat):
    """Strip claim-role markers from a seat segment so a sign-out's seat
    matches its sign-in's seat: '[VALIDATOR sign-out | ...]' and
    '[VALIDATOR sign-in | ...]' are the same seat ('validator'). Without
    this, the sign-out matches nothing and the fallback closes the earliest
    open claim instead of the signer's own — the 2026-10-12 false-OCCUPIED."""
    s = (seat or "").lower()
    s = SIGNOUT_RE.sub(" ", s)
    s = SIGNIN_RE.sub(" ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s or None


def header_segments(body):
    """Bracketed claim header split into segments, e.g.
    [NAYA 5 | learning-loop-watch | SIGN-IN 02:37Z] -> 3 segments."""
    m = HEADER_RE.search(body or "")
    if not m:
        return []
    return [s.strip() for s in re.split(r"[|·—–]", m.group(1)) if s.strip()]


def header_mission(body):
    """Mission descriptor from a bracketed header: the segment that is
    neither the seat name nor the sign-in/out marker."""
    for s in header_segments(body):
        if SEAT_RE.match(s):
            continue
        if SIGNIN_RE.search(s) or SIGNOUT_RE.search(s):
            continue
        if len(s) >= 3:
            return s
    return None


def validity(body):
    """§4 body contract, forward-looking. Returns dict of checks + verdict.

    The lane is contextual — this tool only ever reads lane feeds, so the
    feed IS the lane (grandfather clause: pre-adoption claims are judged
    valid on lane+mission+time). What makes a sign-in a claim is a named
    mission: a Mission: line, a bracketed header descriptor, or a
    backticked branch/ref.
    """
    b = body or ""
    hm = header_mission(b)
    checks = {
        "has_lane": True,  # contextual: the feed is the lane
        "has_mission": bool(hm or MISSION_RE.search(b)
                            or re.search(r"`[^`]{4,}`", b)),
        "mission": hm,
        "has_time": True,  # created_at is server time, always present
        "has_repoll": bool(REPOLL_RE.search(b)),
    }
    checks["valid"] = checks["has_mission"]
    return checks


def mission_key(body):
    """Best-effort mission identifier for sign-out matching and lease renewal."""
    b = body or ""
    m = re.search(r"[Mm]ission\s*[:\-]\s*(.+)", b)
    if m:
        return m.group(1).strip()[:80].lower()
    hm = header_mission(b)
    if hm:
        return hm[:80].lower()
    ticks = re.findall(r"`([^`]{4,80})`", b)
    if ticks:
        return ticks[0].strip().lower()
    first = b.strip().splitlines()[0] if b.strip() else ""
    return first[:80].lower()


def parse_ts(ts):
    try:
        dt = datetime.fromisoformat(str(ts).replace("Z", "+00:00"))
    except (ValueError, TypeError):
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt


# ---------------------------------------------------------------------------
# State determination — Kappa §7, newest-first
# ---------------------------------------------------------------------------

def header_seat(body):
    """First segment of the bracketed claim header, e.g.
    'naya5-evidence-scorer-fixpass'. Used to match sign-outs to sign-ins."""
    segs = header_segments(body)
    return segs[0].lower() if segs else None


def determine_state(comments, now=None, lease_minutes=LEASE_DEFAULT_MIN):
    """
    comments: list of dicts {id, created_at, body}, any order.
    Returns {state, occupant, since, evidence, lease_minutes, stale}.
    state in {FREE, OCCUPIED, STALE-SUSPECT}.

    Walked OLDEST-first. All unclosed valid sign-ins are tracked; the
    occupant is the earliest (Kappa §6: earliest valid sign-in wins).
    A sign-out closes the signer's OWN most-recent open claim with the
    matching seat header (2026-10-12 defect 3: closing the earliest
    seat-match closed someone else's claim). A sign-out that names no
    seat closes the earliest open claim (releases the lane).
    """
    now = now or datetime.now(timezone.utc)
    ordered = sorted(comments, key=lambda c: c.get("created_at", ""))
    evidence = []
    open_claims = []     # valid sign-ins not yet closed, oldest first
    freed_at = None

    def close_claim(claim, signout):
        open_claims.remove(claim)
        return (f"sign-out {signout.get('id')} at {signout.get('created_at')} "
                f"closes sign-in {claim['id']} ({claim['mission']})")

    for c in ordered:
        kind = classify(c.get("body", ""))
        if kind in ("CHATTER", "STANDDOWN"):
            continue
        if kind == "SIGNOUT":
            if not open_claims:
                evidence.append(
                    f"sign-out {c.get('id')} with no open sign-in — ignored")
                continue
            seat = normalize_seat(header_seat(c.get("body", "")))
            # The signer's OWN most-recent open claim with the matching
            # seat: a sign-out ends the session it belongs to, which is
            # the signer's newest still-open claim — never the earliest
            # claim that happens to share the seat.
            target = next((o for o in reversed(open_claims)
                           if normalize_seat(o.get("seat")) == seat),
                          None) if seat else None
            if target is None:
                target = open_claims[0]
                evidence.append(
                    f"sign-out {c.get('id')} names no matching seat "
                    f"({seat}) — closes earliest open claim")
            evidence.append(close_claim(target, c))
            freed_at = c.get("created_at")
            continue
        # SIGNIN
        v = validity(c.get("body", ""))
        if not v["valid"]:
            evidence.append(
                f"sign-in {c.get('id')} lacks a named mission — noise, not a claim")
            continue
        mission = mission_key(c.get("body", ""))
        claim = {"id": c.get("id"), "created_at": c.get("created_at"),
                 "mission": mission, "seat": header_seat(c.get("body", "")),
                 "validity": v}
        if open_claims:
            evidence.append(
                f"collision: sign-in {c.get('id')} at {c.get('created_at')} "
                f"behind open sign-in {open_claims[0]['id']} — earliest wins, "
                f"later claimant owes a stand-down")
        open_claims.append(claim)

    if not open_claims:
        evidence.append("no unclosed valid sign-in in the stream")
        return {"state": "FREE", "occupant": None, "since": freed_at,
                "evidence": evidence, "lease_minutes": lease_minutes,
                "stale": False}

    current = open_claims[0]
    if len(open_claims) > 1:
        evidence.append(
            f"{len(open_claims)-1} later sign-in(s) behind the open claim — "
            f"each owes a stand-down receipt")
    # Lease: later comments referencing the mission renew the claim.
    created = parse_ts(current["created_at"]) or now
    last_activity = created
    for c in ordered:
        if c.get("created_at", "") <= current["created_at"]:
            continue
        nb = (c.get("body") or "").lower()
        if current["mission"] and current["mission"][:30] in nb:
            ts = parse_ts(c.get("created_at"))
            if ts and ts > last_activity:
                last_activity = ts
    age_min = (now - last_activity).total_seconds() / 60
    occupant = {"mission": current["mission"], "sign_in_id": current["id"],
                "seat": current["seat"], "validity": current["validity"]}
    if age_min > lease_minutes:
        evidence.append(
            f"sign-in {current['id']} ({current['mission']}) is stale-suspect: "
            f"{age_min:.0f} min since last activity, lease "
            f"{lease_minutes} min — reclaim needs public ping + "
            f"{GRACE_DEFAULT_MIN}-min grace, not a silent takeover")
        return {"state": "STALE-SUSPECT", "occupant": occupant,
                "since": current["created_at"], "evidence": evidence,
                "lease_minutes": lease_minutes, "stale": True}
    evidence.append(
        f"valid sign-in {current['id']} at {current['created_at']} "
        f"({current['mission']}), no later sign-out, in lease")
    return {"state": "OCCUPIED", "occupant": occupant,
            "since": current["created_at"], "evidence": evidence,
            "lease_minutes": lease_minutes, "stale": False}


# ---------------------------------------------------------------------------
# Fetch + CLI
# ---------------------------------------------------------------------------

def fetch_comments(issue_number):
    """Full read back through pages (newest first from API). Returns list."""
    out = []
    for page in range(1, MAX_PAGES + 1):
        path = (f"/repos/{REPO}/issues/{issue_number}/comments"
                f"?per_page={PER_PAGE}&page={page}")
        try:
            raw = subprocess.run([GH_API, "GET", path], capture_output=True,
                                 text=True, timeout=60)
        except (OSError, subprocess.TimeoutExpired) as e:
            return None, f"gh-api failed: {e}"
        if raw.returncode != 0:
            return None, f"gh-api exit {raw.returncode}: {raw.stderr[:200]}"
        try:
            batch = json.loads(raw.stdout)
        except json.JSONDecodeError:
            return None, "gh-api returned non-JSON"
        if not batch:
            break
        out.extend({"id": c.get("id"), "created_at": c.get("created_at"),
                    "body": c.get("body") or ""} for c in batch)
        if len(batch) < PER_PAGE:
            break
    return out, None


def cmd_check(args):
    lane = args.lane.lower()
    if lane not in LANES:
        print(json.dumps({"error": f"unknown lane '{args.lane}'"}))
        return 2
    comments, err = fetch_comments(LANES[lane])
    if comments is None:
        print(json.dumps({"state": "UNKNOWN", "error": err}))
        return 2
    res = determine_state(comments, lease_minutes=args.lease_minutes)
    res["lane"] = lane
    res["issue"] = LANES[lane]
    res["comments_read"] = len(comments)
    print(json.dumps(res, indent=2, default=str))
    return 0


def cmd_verify(args):
    """Claim-minute re-poll: did anyone with an EARLIER valid sign-in stand?"""
    lane = args.lane.lower()
    if lane not in LANES:
        print(json.dumps({"verdict": "ERROR", "error": "unknown lane"}))
        return 2
    mine = parse_ts(args.my_created_at)
    if mine is None:
        print(json.dumps({"verdict": "ERROR",
                          "error": "bad --my-created-at, use ISO UTC"}))
        return 2
    comments, err = fetch_comments(LANES[lane])
    if comments is None:
        print(json.dumps({"verdict": "UNKNOWN", "error": err}))
        return 2
    rivals = []
    for c in comments:
        if args.my_comment_id and c.get("id") == args.my_comment_id:
            continue
        if classify(c.get("body", "")) != "SIGNIN":
            continue
        if not validity(c.get("body", ""))["valid"]:
            continue
        ts = parse_ts(c.get("created_at"))
        if ts is None or ts >= mine:
            continue
        # Is it closed by a later sign-out?
        closed = any(
            classify(o.get("body", "")) == "SIGNOUT"
            and (o.get("created_at", "") > c.get("created_at", ""))
            for o in comments)
        if not closed:
            rivals.append({"id": c.get("id"), "created_at": c.get("created_at"),
                           "mission": mission_key(c.get("body", ""))})
    if rivals:
        rivals.sort(key=lambda r: r["created_at"])
        rival = rivals[0]
        rts = parse_ts(rival["created_at"])
        stale_note = ""
        if rts and (datetime.now(timezone.utc) - rts).total_seconds() / 60 > 120:
            stale_note = (" rival is stale-suspect (120+ min, no sign-out seen) — "
                          "do not silently take the lane: post the public ping "
                          "and wait the 30-min grace")
        print(json.dumps({"verdict": "LOST",
                          "reason": "earlier valid sign-in stands — stand down." + stale_note,
                          "rival": rival}, indent=2))
    else:
        print(json.dumps({"verdict": "WON",
                          "reason": "no earlier unclosed valid sign-in"},
                         indent=2))
    return 0


def main(argv=None):
    import argparse
    p = argparse.ArgumentParser(description="mechanical lane-claim arbitration")
    sub = p.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("check", help="determine lane state")
    c.add_argument("--lane", required=True)
    c.add_argument("--lease-minutes", type=int, default=LEASE_DEFAULT_MIN)
    v = sub.add_parser("verify", help="claim-minute re-poll")
    v.add_argument("--lane", required=True)
    v.add_argument("--my-created-at", required=True)
    v.add_argument("--my-comment-id", type=int, default=None,
                   help="exclude my own sign-in comment from rivals")
    args = p.parse_args(argv)
    if args.cmd == "check":
        return cmd_check(args)
    return cmd_verify(args)


if __name__ == "__main__":
    sys.exit(main())

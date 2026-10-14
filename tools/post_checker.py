#!/usr/bin/env python3
"""Post checker — the three-level post protocol as bytes.

WHY THIS EXISTS
---------------
2026-10-14: Shawn's law — "what good is 1200 comments if nobody gets any value
from it?" The night-shift dispatcher brief mandates a THREE-LEVEL POST
PROTOCOL (PULSE / RECEIPT / EVENT) with DEDUP + CLAIM-CHECK for board posts,
but the tool was never built — prose doesn't run. This is the enforcement.

2026-10-14: the #2597 incident — a merge-intent post claimed "16/16 required
green" from memory of an earlier check while the Team review + scorecard
receipt gate was RED on the exact head. An independent verifier caught it
post-hoc. The claim-check gate below would have rejected the post before it
went out: a quantitative claim without a cited live read is rejected. Fix it
first, never post-anyway.

Usage (workers run this BEFORE posting; never post a FLAGged post):
    python3 tools/post_checker.py --level PULSE   post.txt
    python3 tools/post_checker.py --level RECEIPT  post.txt
    python3 tools/post_checker.py --level EVENT    post.txt
    cat post.txt | python3 tools/post_checker.py --level PULSE

Exit codes: 0 = PASS (post may go out), 1 = FLAG (reason printed; fix, don't
post). Stdlib only.
"""

import argparse
import difflib
import hashlib
import json
import os
import re
import sys
from datetime import datetime, timedelta, timezone

# --------------------------------------------------------------------------
# Limits and windows (from the dispatcher brief, 2026-10-14)
# --------------------------------------------------------------------------
PULSE_MAX_CHARS = 300
RECEIPT_MAX_CHARS = 1500
OATH_RITUAL_MAX_LINES = 2
DEDUP_WINDOW_HOURS = 6
DEDUP_SIMILARITY = 0.85

# --------------------------------------------------------------------------
# PULSE — state-change only, never a heartbeat
# --------------------------------------------------------------------------
NOTHING_PATTERNS = [
    re.compile(p, re.IGNORECASE)
    for p in (
        r"\bno_work\b",
        r"list-?drained",
        r"nothing to report",
        r"nothing to do",
        r"all quiet",
        r"\bno change\b",
        r"no-change",
        r"\bno updates?\b",
    )
]

STATE_CHANGE_RE = re.compile(
    r"\b(start(?:ing|ed)?|block(?:ed|ing)?|unblock(?:ed|ing)?|done|hold|held|"
    r"sign-?in|sign-?out|deliver(?:ed|ing)?|complet(?:e|ed|ing)|fail(?:ed|ing)?|"
    r"merg(?:e|ed|ing)|posted?|fix(?:ed|ing)?|deploy(?:ed|ing)?|claim(?:ed|ing)?|"
    r"releas(?:e|ed|ing))\b",
    re.IGNORECASE,
)

STILL_WORKING_RE = re.compile(r"\bstill working\b", re.IGNORECASE)


def check_pulse(text):
    """PULSE: <=300 chars, state change, never a nothing-to-report."""
    flags = []
    if not text.strip():
        return ["empty post — a PULSE with nothing in it is a heartbeat"]
    if len(text) > PULSE_MAX_CHARS:
        flags.append(
            f"{len(text)} chars > {PULSE_MAX_CHARS} — PULSE is state-change "
            "only; move detail to a RECEIPT"
        )
    for pat in NOTHING_PATTERNS:
        if pat.search(text):
            flags.append(
                f"nothing-to-report pattern {pat.pattern!r} — that is a "
                "heartbeat, not a post. Heartbeat the truth file instead"
            )
            break
    if STILL_WORKING_RE.search(text) and not STATE_CHANGE_RE.search(text):
        flags.append(
            '"still working" with no new information — say WHAT changed or '
            "do not post"
        )
    if not STATE_CHANGE_RE.search(text):
        flags.append(
            "no state change described (starting/blocked/unblocked/done/...) "
            "— PULSE must carry a state change"
        )
    return flags


# --------------------------------------------------------------------------
# RECEIPT — identity per the naming law, verdict, trimmed ritual
# --------------------------------------------------------------------------
SEAT_RE = re.compile(
    r"\bNaya\s+(?:Clarity|Verity|Resolve|Alpha|Beta|Gamma|Delta|Epsilon|Zeta|"
    r"Eta|Theta|Iota|Kappa|Lambda|Mu)\b"
)
BARE_NAYA_RE = re.compile(r"\bNaya\b")
SIGNING_BARE_RE = re.compile(r"signing\s+bare", re.IGNORECASE)
VERDICT_RE = re.compile(
    r"\b(DONE|COMPLETE|COMPLETED|HELD|HOLD|BLOCKED|FAIL|FAILED|VERDICT)\b",
    re.IGNORECASE,
)
OATH_LINE_RE = re.compile(r"\boath\b", re.IGNORECASE)


def check_receipt(text):
    """RECEIPT: named seat, verdict line, <=1500 chars, no ritual."""
    flags = []
    if not text.strip():
        return ["empty post — a RECEIPT must carry a verdict"]
    if len(text) > RECEIPT_MAX_CHARS:
        flags.append(
            f"{len(text)} chars > {RECEIPT_MAX_CHARS} — trim the ritual; "
            "identity, mission, verdict, win-why"
        )
    if SIGNING_BARE_RE.search(text) or (
        BARE_NAYA_RE.search(text) and not SEAT_RE.search(text)
    ):
        flags.append(
            "naming-law violation — sign as a named seat "
            "(Naya Clarity/Verity/Resolve Narzan, or Naya [Greek lead]); "
            'never bare "Naya"'
        )
    if not VERDICT_RE.search(text):
        flags.append(
            "no verdict line (DONE/HELD/BLOCKED/FAIL + what) — a receipt "
            "without a verdict is a diary entry"
        )
    oath_lines = sum(1 for line in text.splitlines() if OATH_LINE_RE.search(line))
    if oath_lines > OATH_RITUAL_MAX_LINES:
        flags.append(
            f"oath restatement over {OATH_RITUAL_MAX_LINES} lines "
            f"({oath_lines} found) — the oath lives in the briefing, not in "
            "every post"
        )
    return flags


# --------------------------------------------------------------------------
# EVENT — board-level: DEDUP + CLAIM-CHECK
# --------------------------------------------------------------------------
QUANT_PATTERNS = [
    (re.compile(r"\b\d+\s*/\s*\d+\b"), "fraction like 16/16"),
    (
        re.compile(r"\bCI\b[^.\n]{0,40}\bgreen\b|\bgreen\b[^.\n]{0,40}\bCI\b",
                   re.IGNORECASE),
        '"CI green"',
    ),
    (re.compile(r"\ball checks\b", re.IGNORECASE), '"all checks"'),
    (re.compile(r"\bchecks?\s+green\b", re.IGNORECASE), '"checks green"'),
    (re.compile(r"\brequired\s+green\b", re.IGNORECASE), '"required green"'),
    (re.compile(r"\btests?\s+green\b", re.IGNORECASE), '"tests green"'),
    (re.compile(r"\b\d+\s*%"), "percentage like X%"),
]
SHA_RE = re.compile(r"\b[0-9a-f]{40}\b")
RUNID_RE = re.compile(r"\b\d{8,}\b")


def normalize(text):
    return re.sub(r"\s+", " ", text).strip().lower()


def post_sha(text):
    return hashlib.sha256(normalize(text).encode("utf-8")).hexdigest()


def resolve_log_path(override=None):
    """Where the dedup log lives: flag > env > repo-local > home."""
    if override:
        return override
    env = os.environ.get("NAYA_POST_LOG")
    if env:
        return env
    here = os.path.abspath(os.getcwd())
    while True:
        if os.path.isdir(os.path.join(here, ".git")):
            return os.path.join(here, ".naya", "post-log.jsonl")
        parent = os.path.dirname(here)
        if parent == here:
            break
        here = parent
    return os.path.join(os.path.expanduser("~"), ".naya", "post-log.jsonl")


def read_log(path):
    entries = []
    if not os.path.exists(path):
        return entries
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                entries.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return entries


def append_log(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    entry = {
        "sha": post_sha(text),
        "ts": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "norm": normalize(text)[:4000],
        "head": text.strip()[:80],
    }
    with open(path, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(entry) + "\n")


def check_event(text, log_path=None):
    """EVENT: claim-check then dedup. Returns (flags, should_append)."""
    flags = []
    if not text.strip():
        return ["empty post — an EVENT must carry a material finding"], False

    # (b) CLAIM-CHECK — quantitative claims need cited live evidence.
    claims = []
    for pat, label in QUANT_PATTERNS:
        m = pat.search(text)
        if m:
            claims.append(f"{label} ({m.group(0)!r})")
    if claims and not (SHA_RE.search(text) or RUNID_RE.search(text)):
        flags.append(
            "claim-check: quantitative claim(s) with no cited live read — "
            + "; ".join(claims)
            + " — cite the exact head SHA (40 hex) and/or check-run id "
            "observed in THIS mission. Never from memory of an earlier check"
        )

    # (a) DEDUP — same content inside the 6h window: link, don't repost.
    path = resolve_log_path(log_path)
    norm = normalize(text)
    sha = post_sha(text)
    now = datetime.now(timezone.utc)
    for entry in read_log(path):
        try:
            ets = datetime.fromisoformat(entry["ts"])
        except (KeyError, ValueError):
            continue
        if ets.tzinfo is None:
            ets = ets.replace(tzinfo=timezone.utc)
        if now - ets > timedelta(hours=DEDUP_WINDOW_HOURS):
            continue
        if entry.get("sha") == sha:
            flags.append(
                f"duplicate: identical post already made at {entry['ts']} — "
                "link the original instead of reposting"
            )
            break
        other = entry.get("norm", "")
        if other and difflib.SequenceMatcher(None, norm, other).ratio() >= DEDUP_SIMILARITY:
            flags.append(
                f"near-duplicate of a post from {entry['ts']} "
                f"(similarity >= {DEDUP_SIMILARITY}) — link the original "
                "instead of reposting"
            )
            break

    return flags, not flags


def check(level, text, log_path=None):
    """Dispatch by level. Returns (flags, append_to_log)."""
    level = level.upper()
    if level == "PULSE":
        return check_pulse(text), False
    if level == "RECEIPT":
        return check_receipt(text), False
    if level == "EVENT":
        return check_event(text, log_path)
    raise ValueError(f"unknown level {level!r} — want PULSE, RECEIPT, or EVENT")


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="Three-level post protocol gate: PULSE/RECEIPT/EVENT. "
        "Exit 0 = PASS (post may go out), 1 = FLAG (fix, don't post)."
    )
    ap.add_argument("--level", required=True,
                    choices=["PULSE", "RECEIPT", "EVENT"])
    ap.add_argument("file", nargs="?",
                    help="post file; reads stdin when omitted")
    ap.add_argument("--post-log", default=None,
                    help="dedup log path (EVENT); defaults to repo-local "
                    ".naya/post-log.jsonl or ~/.naya/post-log.jsonl")
    ap.add_argument("--no-append", action="store_true",
                    help="do not append a passing EVENT to the dedup log")
    args = ap.parse_args(argv)

    if args.file:
        with open(args.file, encoding="utf-8") as fh:
            text = fh.read()
    else:
        text = sys.stdin.read()

    flags, append = check(args.level, text, args.post_log)
    if flags:
        for f in flags:
            print(f"FLAG: {f}")
        return 1
    if append and not args.no_append:
        append_log(resolve_log_path(args.post_log), text)
    print("PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())

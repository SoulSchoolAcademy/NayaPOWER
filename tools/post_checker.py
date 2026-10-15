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

W181 SURGICAL MERGE (Naya Gamma): reconciled the tools/post_checker.py
add/add conflict (true merge-base c13f260f; tip blob 4e5fdff0 vs head blob
99a891ac) per builder-packet-2600-conflict-w180.md. The head's three-level
protocol is canonical; the tip's unique mechanisms were ported in:
_unquoted() (quoted/fenced lines never bind — w157/w164 hole class),
the ROSTER names folded into the identity regex (Naya 1-5, Narzan leads),
the contextual ANCHORED_SHA_RE (7-40 hex with sha/commit/tree/tip/head/ref
context words) OR'd with the bare 40-hex check, and score-meaning rigor on
RECEIPT. The tip's older comm-standard vocabulary (WHO/MISSION/STATUS/...
fields) was superseded — its failure-mode COVERAGE was translated to the
current schema in tests/test_post_checker.py, not its verbatim strings.

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
# _unquoted (ported from the tip, w181) — quoted/fenced lines never bind
# --------------------------------------------------------------------------
_FENCE_OPEN_RE = re.compile(r"^(```+|~~~+)")
_FENCE_CLOSE_RE = re.compile(r"^(```+|~~~+)\s*$")


def _unquoted(body):
    """The author's own lines only: drop Markdown blockquote lines and
    fenced-code-block lines.

    A line whose first non-whitespace character is `>` is someone else's
    quoted words. A fenced block — opened by a line whose first
    non-whitespace characters are ``` or ~~~ (with an optional info
    string, e.g. ```markdown), closed by a matching fence line (same
    character, at least as long, fence characters + whitespace only) —
    is pasted content, not the author's own words. Quoted and fenced
    lines must never bind as identity, verdict, evidence, or score —
    a post that only *quotes* or *fences* a good post is not a good
    post. Every check runs on the unquoted body. An UNCLOSED fence
    drops everything after it (fail-closed): content past the fence
    cannot be proven to be the author's. Lazy-continuation lines
    (quote continuation without a leading `>`) are NOT stripped: they
    are indistinguishable from the author's own wrapped prose, so the
    mechanical rule is line-leading `>` only. Inline code spans
    (single-backtick `spans` inside a line) are NOT stripped — only
    fence LINES delimit blocks."""
    kept = []
    fence_char = None
    fence_len = 0
    for line in body.splitlines():
        stripped = line.lstrip()
        if fence_char is not None:
            m = _FENCE_CLOSE_RE.match(stripped)
            if (m and m.group(1)[0] == fence_char
                    and len(m.group(1)) >= fence_len):
                fence_char = None
            continue
        m = _FENCE_OPEN_RE.match(stripped)
        if m:
            fence_char = m.group(1)[0]
            fence_len = len(m.group(1))
            continue
        if stripped.startswith(">"):
            continue
        kept.append(line)
    return "\n".join(kept)


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
# RECEIPT — identity per the naming law, verdict, trimmed ritual,
#           score with meaning (no bare numbers, ever)
# --------------------------------------------------------------------------
# ROSTER folded into the identity regex (ported from the tip, w181):
# the twelve Greek-lead seats, the numbered seats Naya 1-5, and the
# three leads with the Narzan family name.
SEAT_RE = re.compile(
    r"\bNaya\s+(?:[1-5]|Clarity|Verity|Resolve|Alpha|Beta|Gamma|Delta|"
    r"Epsilon|Zeta|Eta|Theta|Iota|Kappa|Lambda|Mu)(?:\s+Narzan)?\b"
)
BARE_NAYA_RE = re.compile(r"\bNaya\b")
SIGNING_BARE_RE = re.compile(r"signing\s+bare", re.IGNORECASE)
VERDICT_RE = re.compile(
    r"\b(DONE|COMPLETE|COMPLETED|HELD|HOLD|BLOCKED|FAIL|FAILED|VERDICT)\b",
    re.IGNORECASE,
)
OATH_LINE_RE = re.compile(r"\boath\b", re.IGNORECASE)
# Score-meaning rigor (ported from the tip, w181): a score with meaning,
# not a bare number. Meaning words match on word boundaries only:
# "relationships" must not count as "ships", "meaningless" must not
# count as "meaning".
SCORE_RE = re.compile(r"(\d+(?:\.\d+)?)\s*/\s*10")
MEANING_RE = re.compile(
    r"\b(why not 10|why it is not|meaning|ships|one more pass|rework|"
    r"backwards|held|blocked|verified)\b",
    re.IGNORECASE)


def check_receipt(text):
    """RECEIPT: named seat, verdict line, score with meaning, <=1500
    chars, no ritual."""
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
            "(Naya Clarity/Verity/Resolve Narzan, Naya 1-5, or Naya "
            "[Greek lead]); never bare 'Naya'"
        )
    if not VERDICT_RE.search(text):
        flags.append(
            "no verdict line (DONE/HELD/BLOCKED/FAIL + what) — a receipt "
            "without a verdict is a diary entry"
        )
    m = SCORE_RE.search(text)
    if not m:
        flags.append(
            "no X/10 score with meaning — a RECEIPT requires "
            "score: n/10 — what it means (no bare numbers, ever)"
        )
    elif not MEANING_RE.search(text):
        flags.append(
            f"score {m.group(0).strip()} present but meaning unstated — "
            "say what the score means (why not 10, what changed)"
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
# Contextual SHA (ported from the tip, w181): a 7-40 hex word counts as
# evidence only with an anchor — `@ <sha>`, `sha: <sha>`, `commit <sha>`,
# `tip <sha>`, `head <sha>`, `tree <sha>`, `ref <sha>`. A bare hex word
# in prose ('deadbeef') is NOT evidence — anchors inside `>` quotes or
# fenced blocks never count (see _unquoted).
ANCHORED_SHA_RE = re.compile(
    r"(?:@\s*|\b(?:sha|commit|tree|tip|head|ref)\s*[:=]?\s*)"
    r"([0-9a-f]{7,40})\b",
    re.IGNORECASE)
RUNID_RE = re.compile(r"\b\d{8,}\b")


def _has_evidence(body):
    """A cited live read: bare 40-hex SHA, anchored 7-40 hex SHA, or a
    check-run id — observed in THIS mission, never from memory."""
    return bool(
        SHA_RE.search(body)
        or ANCHORED_SHA_RE.search(body)
        or RUNID_RE.search(body)
    )


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
    if claims and not _has_evidence(text):
        flags.append(
            "claim-check: quantitative claim(s) with no cited live read — "
            + "; ".join(claims)
            + " — cite the exact head SHA (bare 40-hex, or anchored "
            "@ / sha: / commit / tip / head / tree / ref <7-40 hex>) "
            "and/or check-run id observed in THIS mission. "
            "Never from memory of an earlier check"
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
    """Dispatch by level. Every check runs on the author's own lines —
    quoted and fenced lines never bind (see _unquoted). Returns
    (flags, append_to_log)."""
    level = level.upper()
    body = _unquoted(text)
    if level == "PULSE":
        return check_pulse(body), False
    if level == "RECEIPT":
        return check_receipt(body), False
    if level == "EVENT":
        return check_event(body, log_path)
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

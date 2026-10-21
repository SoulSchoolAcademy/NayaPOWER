#!/usr/bin/env python3
"""boot_pointer_check.py — machine law for boot-entry pointer freshness.

The cold-Naya proof failed (6.5/10 NOT YET) partly because the merged guide
pointed at a dead/capped board. This gate enumerates venue/board pointers in
the boot-entry files and fails CLOSED when a dead board is referenced as if
live.

Standing (edit STANDING as the world changes; the director owns it):
  live_board: the one live coordination board — INDIRECTED: no number is
              printed here (numbers rot within 24h). The live board number
              is named in the mission-state snapshot
              (BRAIN/CURRENT-MISSION-STATE.md on branch naya/mission-state):
              read the snapshot first, then go to the board it names.
  dead_boards: capped archives — may be named only with dead/capped/archive/
               redirect/former nearby
  canonical_snapshot_branch: the one home of CURRENT-MISSION-STATE.md

A dead-board number is a violation UNLESS the same line carries one of the
DEAD_WORDS. That allows "never post to #2175 (capped archive)" while catching
"go to board #2175".

Exit 0: clean. Exit 1: stale pointer found — boot must not proceed.

Usage: python3 boot_pointer_check.py [--self-test] <dir> [more dirs...]
       --self-test pins the regression seeds (VERIFY lane's adversarial
       phrasings from PR #2842 head 88bf85d3) — no directory needed.
"""
import os
import re
import sys

STANDING = {
    # live_board: the one live coordination board. The number is NOT printed
    # here — board numbers rot within 24h (2537 -> 2641 -> 2721 -> 2765
    # since 2026-10-15), so a bare number in standing is stale-by-design.
    # The live board number is named in the mission-state snapshot
    # (BRAIN/CURRENT-MISSION-STATE.md on branch naya/mission-state) — read
    # the snapshot first, then go to the board it names. Indirection added
    # 2026-10-19 (gap-t-distill-daily-20261019 follow-up; parent PR #2782
    # indirected BRAIN/00-ACTIVATION/ the same way).
    # History (NOT standing): migrated 2026-10-17 ~06:48Z: #2641 -> #2721
    # (announce comment 6230827986, redirect 6230827688;
    # shared-state.json live_board: "2721", watermark 6233699369;
    # snapshot branch naya/mission-state commit fb2e9db,
    # "Snapshot refresh 05:08 PDT").
    # #2641 is now a readable archive; #2537 is a readable archive.
    # Earlier migration: 2537 -> 2641 (authority main seat 6196761341,
    # 2026-10-15T16:38:52Z, on Shawn's word "switch over to a new board now")
    # — #2537 remains a capped archive.
    "live_board": "BRAIN/CURRENT-MISSION-STATE.md @ naya/mission-state "
                  "— read the snapshot first; board numbers rotate, "
                  "no printed number is canonical",
    # dead_boards: the HARDCODED FLOOR. The effective dead set is
    # floor UNION snapshot-derived (see snapshot_dead_boards) — the machine
    # gate tracks migrations automatically; a new retirement enters the
    # snapshot's own words and the checker picks it up without a code
    # change. Class killed 2026-10-20 (distill-daily brief): hardcoded
    # board numbers rotted 3 generations running.
    "dead_boards": ("2175", "1354", "2537", "2641", "2721", "2765"),
    "canonical_snapshot_branch": "naya/mission-state",
}

DEAD_WORDS = re.compile(
    r"dead|capped|archive|redirect|former|never post|do not post|don't post",
    re.I)
BOARD_RE = re.compile(r"#(\d{3,5})")
BOOT_FILES = ("READ-ME-FIRST.md", "THE-CODE-SHE-LIVES-BY.md",
              "THE-14-QUESTIONS.md", "CURRENT-MISSION-STATE.md")
LIVE_BOARD_RE = re.compile(r"LIVE BOARD\s*#(\d{3,5})")
RETIRED_RE = re.compile(
    r"capped|archived|distilled|released|retired|former|hard-capped|"
    r"readable for provenance|history only|read-only",
    re.I)


def find_repo_root(start):
    """Walk up from a scanned dir to the git work-tree root (or None)."""
    cur = os.path.abspath(start)
    while True:
        if os.path.isdir(os.path.join(cur, ".git")):
            return cur
        parent = os.path.dirname(cur)
        if parent == cur:
            return None
        cur = parent


def snapshot_text(repo_root):
    """Fetch the mission-state snapshot from origin/naya/mission-state via
    git protocol (read path — free). Returns bytes or None."""
    if not repo_root:
        return None
    import subprocess
    ref = STANDING["canonical_snapshot_branch"]
    # Fetch the snapshot branch first (shallow clones often lack it);
    # best-effort — a failure falls through to the local show below.
    try:
        subprocess.run(["git", "-C", repo_root, "fetch", "origin",
                        "+refs/heads/%s:refs/remotes/origin/%s" % (ref, ref),
                        "--depth", "1", "-q"], capture_output=True,
                       timeout=60)
    except Exception:
        pass
    try:
        out = subprocess.run(
            ["git", "-C", repo_root, "show", "origin/%s:BRAIN/CURRENT-MISSION-STATE.md" % ref],
            capture_output=True, text=True, timeout=30)
    except Exception:
        return None
    return out.stdout if out.returncode == 0 else None


def snapshot_live_board(text):
    """The live-board number the snapshot names (or None)."""
    if not text:
        return None
    m = LIVE_BOARD_RE.search(text)
    return m.group(1) if m else None


def snapshot_dead_boards(text, live_board):
    """Retired boards the snapshot itself declares: a #NNNN whose *forward
    segment* (this number up to the next board number — the retirement
    phrase belongs to the number it follows) carries retirement phrasing.
    The snapshot is the migration log — when the live board rotates, the
    old one lands here by its own words. Non-board references (e.g. the
    #2601 master directive) are excluded by the directive guard."""
    dead = set()
    if not text:
        return dead
    directive_re = re.compile(r"directive", re.I)
    matches = list(BOARD_RE.finditer(text))
    for i, m in enumerate(matches):
        num = m.group(1)
        if num == live_board:
            continue
        seg_end = matches[i + 1].start() if i + 1 < len(matches) else m.end() + 48
        segment = text[m.end():seg_end]
        if RETIRED_RE.search(segment) and not directive_re.search(segment):
            dead.add(num)
    return dead


# Regression seeds — adversarial phrasings the checker MUST flag.
# Source: VERIFY lane independent scan of PR #2842 head 88bf85d3
# (comment 6316798514, 2026-10-21T13:05:59Z): these two same-class
# instances survived the first fix round because the author's gate was
# under-sensitive, not because the tree was clean. A self-test run
# (--self-test) pins them forever.
REGRESSION_SEEDS = (
    # ACTIVATION-PACKET.md "The circle" footer — capped archive #2537
    # presented as the Venue (link-text label phrasing).
    "**The circle:** every document in this system links to its "
    "relatives and back here. [Venue #2537]"
    "(https://github.com/SoulSchoolAcademy/NayaPOWER/issues/2537)",
    # READ-ME-FIRST.md step 7 — retired board #2175 presented as *the*
    # coordination board (Issue [#NNNN] phrasing).
    "7. **Learn the coordination board.** Issue [#2175]"
    "(https://github.com/SoulSchoolAcademy/NayaPOWER/issues/2175)",
)

# The fixed replacements — these MUST pass the checker (negative control:
# the indirection phrasing names the resolver, not a board number).
FIXED_LINES = (
    "**The circle:** every document in this system links to its "
    "relatives and back here. [The live coordination board]"
    "(https://github.com/SoulSchoolAcademy/NayaPOWER/blob/naya/mission-state/"
    "BRAIN/CURRENT-MISSION-STATE.md)",
    "7. **Learn the coordination board.** The live coordination board "
    "(resolve via `BRAIN/CURRENT-MISSION-STATE.md` @ `naya/mission-state` "
    "— read the snapshot first; board numbers rotate, so no printed "
    "number is canonical)",
)

# Dead-word allowance controls — naming a dead board next to a retirement
# word is legitimate and must NOT be flagged, in either direction.
ALLOWED_CONTROL = (
    "Issue #1354 is the capped archive — cite as history, never post there."
)
ALLOWED_CONTROL_BACKWARD = (
    "The capped archive #2537 must not be named as the venue."
)


def check_line(line, dead_boards):
    """Return violation strings for one line (pure — used by the file
    scanner and the self-test alike).

    The dead-word allowance is NUMBER-SCOPED, not line-scoped: a dead
    board number is excused only when a retirement word appears in the
    *same segment* — the text between this number and the neighboring
    board numbers (the retirement phrase belongs to the number it
    follows, or precedes when named first). A line-scoped allowance let
    a dead word anywhere in the line ("no dead ends") excuse a
    live-presented dead number elsewhere in it — the exact
    under-sensitivity VERIFY's 7.5 named on PR #2842 (PACKET:109,
    README:25 at head 88bf85d3)."""
    hits = []
    seen = set()
    matches = list(BOARD_RE.finditer(line))
    for i, m in enumerate(matches):
        num = m.group(1)
        if num not in dead_boards or num in seen:
            continue
        seen.add(num)
        seg_start = matches[i - 1].end() if i > 0 else max(0, m.start() - 80)
        seg_end = (matches[i + 1].start()
                   if i + 1 < len(matches) else m.end() + 80)
        segment = line[seg_start:m.start()] + line[m.end():seg_end]
        if not DEAD_WORDS.search(segment):
            hits.append(
                f"dead board #{num} referenced as if live: "
                f"{line.strip()[:100]}")
    return hits


def self_test():
    """Pin the regression seeds: both adversarial phrasings must be
    flagged, both fixed phrasings must pass, the dead-word allowance
    control must pass. Exit 0 on pass, 1 on failure."""
    dead = set(STANDING["dead_boards"]) | {"2537", "2175"}
    failures = []
    for i, seed in enumerate(REGRESSION_SEEDS, 1):
        if not check_line(seed, dead):
            failures.append(f"seed {i} NOT FLAGGED: {seed[:80]}")
    for i, line in enumerate(FIXED_LINES, 1):
        if check_line(line, dead):
            failures.append(f"fixed line {i} WRONGLY FLAGGED: {line[:80]}")
    if check_line(ALLOWED_CONTROL, dead):
        failures.append("allowed control WRONGLY FLAGGED: "
                        + ALLOWED_CONTROL[:80])
    if check_line(ALLOWED_CONTROL_BACKWARD, dead):
        failures.append("backward allowance control WRONGLY FLAGGED: "
                        + ALLOWED_CONTROL_BACKWARD[:80])
    for f in failures:
        print(f"SELF-TEST FAIL: {f}")
    if failures:
        print(f"\n{len(failures)} self-test failure(s) — regression seeds "
              f"not pinned.")
        return 1
    print(f"SELF-TEST PASS: {len(REGRESSION_SEEDS)} seeds flagged, "
          f"{len(FIXED_LINES)} fixed lines clean, "
          f"allowance controls clean (forward + backward).")
    return 0


def check_file(path, dead_boards):
    violations = []
    try:
        lines = open(path, errors="replace").read().splitlines()
    except OSError as e:
        return [f"{path}: unreadable ({e})"]
    for i, line in enumerate(lines, 1):
        for hit in check_line(line, dead_boards):
            violations.append(f"{path}:{i}: {hit}")
    return violations


def main():
    if len(sys.argv) >= 2 and sys.argv[1] == "--self-test":
        sys.exit(self_test())
    if len(sys.argv) < 2:
        print("usage: boot_pointer_check.py [--self-test] <dir> [more dirs...]",
              file=sys.stderr)
        sys.exit(2)
    # The board-number list reads the LIVE BOARD from the snapshot
    # (machine-read via git protocol, not a printed constant) — the
    # retired-board set derives from the snapshot's own retirement
    # phrasing, so the gate tracks migrations automatically.
    repo_root = find_repo_root(sys.argv[1])
    snap = snapshot_text(repo_root)
    live_board = snapshot_live_board(snap)
    dead_boards = set(STANDING["dead_boards"])
    derived = snapshot_dead_boards(snap, live_board)
    dead_boards |= derived
    if live_board:
        dead_boards.discard(live_board)
    snap_note = (f"machine-read #{live_board} from snapshot"
                 if live_board else "snapshot unreadable — hardcoded floor only")
    violations = []
    scanned = 0
    for root in sys.argv[1:]:
        for dirpath, _, files in os.walk(root):
            for f in files:
                if f in BOOT_FILES or f.endswith(".md") and "ACTIVATION" in dirpath:
                    scanned += 1
                    violations += check_file(os.path.join(dirpath, f),
                                             dead_boards)
    for v in violations:
        print(f"FAIL: {v}")
    if violations:
        print(f"\n{len(violations)} stale pointer(s) in {scanned} file(s) — "
              f"boot must not proceed on these bytes. "
              f"Live board {snap_note}.")
        sys.exit(1)
    print(f"PASS: no stale pointers in {scanned} boot file(s). "
          f"Live board {snap_note}. "
          f"Dead set: {','.join(sorted(dead_boards))} "
          f"({len(derived)} snapshot-derived).")
    sys.exit(0)


if __name__ == "__main__":
    main()

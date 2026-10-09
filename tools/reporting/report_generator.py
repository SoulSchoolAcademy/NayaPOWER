#!/usr/bin/env python3
"""Team Naya automated reporting system — core generator.

Pulls data from all sources, distills it into Shawn's report structure,
broken down by the nine teams (ratified 2026-10-08):
    # [MORNING/HOURLY/NIGHTLY] Report — [date/time]
    ## Team 1: Learning (Naya 4) — feed #1602
    ## Team 2: Brain/Memory (Naya 5) — feed #1603
    ... (all nine teams)
    ## Cross-team signals
    ## Evidence Snapshot

Each team section shows: Scores, Holes (top 3), Priorities (top 3),
Action plan to 10, This hour (what got done).

Data sources (all read paths, no writes outside state/):
  - Worker run logs: ~/workspace/goals/<goal>/hidden_files/*.md
  - GitHub: ~/workspace/naya/bin/gh-api (PRs, #1354 comments)
  - Supabase: ~/workspace/skills/supabase/bin/sb-api (READ-ONLY aggregates)
  - Memory: ~/memory/YYYY-MM-DD.md (daily logs)

Design notes:
  - Data fetchers are injectable so tests can pass mocks.
  - Every extracted item carries its source (file/PR/comment) — no
    number appears without provenance.
  - Scores are parsed heuristically from worker logs; the authoritative
    seed lives in state/score_state.json. Claims are labeled as claims.
  - The generator NEVER posts to GitHub and NEVER writes to Supabase.
    Delivery is a separate step (see wrappers + delivery integration).
"""
from __future__ import annotations

import datetime as dt
import json
import re
import subprocess
from dataclasses import dataclass, field
from pathlib import Path

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

REPO = "SoulSchoolAcademy/NayaPOWER"
TEAM_ISSUE = 1354
HOME = Path.home()
WORKSPACE = HOME / "workspace"
GOAL_DIR = WORKSPACE / "goals" / "super-brain-engine-to-10-10"
HIDDEN_FILES = GOAL_DIR / "hidden_files"
MEMORY_DIR = HOME / "memory"
GH_API = WORKSPACE / "naya" / "bin" / "gh-api"
SB_API = WORKSPACE / "skills" / "supabase" / "bin" / "sb-api"
STATE_DIR = Path(__file__).resolve().parent / "state"
SCORE_STATE_FILE = STATE_DIR / "score_state.json"
WATERMARK_FILE = STATE_DIR / "last_report.json"

# Canonical scorecard areas (System Scorecard V1, ratified 2026-10-05).
AREAS = [
    "Learning",
    "Truth",
    "Memory & Continuity",
    "Human Value",
    "Retrieval",
    "Action & Execution",
    "Authority & Governance",
    "Safety",
    "Voice & Experience",
    "Production Readiness",
    "Successor Reuse",
]

# Aliases found in worker logs -> canonical area name.
AREA_ALIASES = {
    "learning": "Learning",
    "learn": "Learning",
    "truth": "Truth",
    "memory": "Memory & Continuity",
    "memory & continuity": "Memory & Continuity",
    "human value": "Human Value",
    "retrieval": "Retrieval",
    "cold retrieve": "Retrieval",
    "cold-retrieve": "Retrieval",
    "action": "Action & Execution",
    "action & execution": "Action & Execution",
    "authority": "Authority & Governance",
    "authority & governance": "Authority & Governance",
    "safety": "Safety",
    "voice": "Voice & Experience",
    "voice & experience": "Voice & Experience",
    "production readiness": "Production Readiness",
    "prod readiness": "Production Readiness",
    # NOTE: bare "production" was deliberately removed (2026-10-08): it
    # mis-attributed reveal-deck sub-scores ("production 9") to the
    # Production Readiness area. Score statements use the full area name.
    "successor": "Successor Reuse",
    "successor reuse": "Successor Reuse",
}

# ---------------------------------------------------------------------------
# Nine-team structure (ratified 2026-10-08, Shawn).
# #1354 = main coordination feed. Each team owns scorecard areas and a
# working feed. Reports break down by team, not by flat area list.
# ---------------------------------------------------------------------------

TEAM_STRUCTURE = [
    {"name": "Learning", "manager": "Naya 4",
     "areas": ["Learning"], "feed": "#1602"},
    {"name": "Brain/Memory", "manager": "Naya 5",
     "areas": ["Memory & Continuity"], "feed": "#1603"},
    {"name": "Law/Governance", "manager": "Naya 2",
     "areas": ["Authority & Governance", "Safety"], "feed": "#1606"},
    {"name": "Architecture/Engineering/Ops", "manager": "Naya 4",
     "areas": ["Action & Execution", "Retrieval", "Production Readiness"],
     "feed": "#1605"},
    {"name": "Evolution/Succession", "manager": "Naya 5",
     "areas": ["Successor Reuse"], "feed": "#1715"},
    {"name": "Interfaces/Hub", "manager": "Naya 3",
     "areas": ["Voice & Experience", "Human Value"], "feed": "#1607"},
    {"name": "Knowledge/Intelligence", "manager": "Naya 4",
     "areas": [], "feed": "#1713"},  # cross-cutting: lessons → system
    {"name": "Proving/Verifying", "manager": "Naya 1",
     "areas": ["Truth"], "feed": "#1723"},
    {"name": "Innovation", "manager": "Naya 3",
     "areas": [], "feed": "#1607"},  # cross-cutting: improvements adopted
]

# Area -> owning team name. Every AREAS entry must appear exactly once.
AREA_TO_TEAM: dict[str, str] = {}
for _t in TEAM_STRUCTURE:
    for _a in _t["areas"]:
        AREA_TO_TEAM[_a] = _t["name"]

# Worker-log name prefix -> team. Checked after area-mention attribution,
# so a learn-builder hole about "tip RED" still lands on Learning even
# though the text names no area.
WORKER_TEAM_PREFIXES = [
    ("learn", "Learning"),
    ("memory", "Brain/Memory"),
    ("authority", "Law/Governance"),
    ("safety", "Law/Governance"),
    ("action", "Architecture/Engineering/Ops"),
    ("cold-retrieve", "Architecture/Engineering/Ops"),
    ("cold_retrieve", "Architecture/Engineering/Ops"),
    ("prod", "Architecture/Engineering/Ops"),
    ("successor", "Evolution/Succession"),
    ("voice", "Interfaces/Hub"),
    ("human-value", "Interfaces/Hub"),
    ("human_value", "Interfaces/Hub"),
    ("truth", "Proving/Verifying"),
]

# Conservative keyword fallback for cross-cutting innovation items that
# name no area and come from no known worker (e.g. memory-log notes).
_INNOVATION_RE = re.compile(
    r"\b(innovat\w*|cutting.?edge|research\w*|prototyp\w*|"
    r"new tool\w*|new framework|adopt\w+)\b",
    re.IGNORECASE,
)


def attribute_team(item: Item, kind: str) -> str | None:
    """Attribute an item to one of the nine teams.

    kind in {"hole", "achievement", "next", "intelligence"}.
    Order: area mentioned in text -> worker/source prefix ->
    intelligence defaults to Knowledge/Intelligence -> None (unassigned).
    Never guesses: ambiguous or unattributable items return None and are
    surfaced under Cross-team signals.
    """
    area = _normalize_area(item.text)
    if area:
        team = AREA_TO_TEAM.get(area)
        if team:
            return team
    src = (item.source or "").lower()
    # Memory-log sources ("memory:2026-10-08") are not workers — the
    # "memory" worker prefix is for memory-builder run logs only.
    if not src.startswith("memory:"):
        for prefix, team in WORKER_TEAM_PREFIXES:
            if src.startswith(prefix):
                return team
    if kind == "achievement" and _INNOVATION_RE.search(item.text):
        return "Innovation"
    if kind == "intelligence":
        # Lessons with no area named belong to the team whose job is
        # getting intelligence INTO the system.
        return "Knowledge/Intelligence"
    return None


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------


@dataclass
class ScorePoint:
    area: str
    score: float
    as_of: dt.datetime
    source: str
    status: str = "claim"  # "authoritative", "claim", "stale", "seed", "history"


@dataclass
class Item:
    text: str
    source: str
    priority: int = 0  # higher = more urgent (holes only)
    section: str = ""  # originating section, e.g. "blockers", "next"
    ts: dt.datetime | None = None  # when the item happened (UTC).
    # The Usefulness Gate: an item with unknown ts is stale by definition.
    # collect() DROPS it — never recycled into a later window.

    def __post_init__(self):
        # Distilled, not walls of text: cap at 280 chars.
        if len(self.text) > 280:
            self.text = self.text[:277].rstrip() + "…"


@dataclass
class ReportData:
    scores: list[ScorePoint] = field(default_factory=list)
    previous_scores: dict = field(default_factory=dict)
    holes: list[Item] = field(default_factory=list)
    achievements: list[Item] = field(default_factory=list)
    team_activity: list[Item] = field(default_factory=list)
    intelligence: list[Item] = field(default_factory=list)
    next_actions: list[Item] = field(default_factory=list)
    supabase_snapshot: dict = field(default_factory=dict)
    github_snapshot: dict = field(default_factory=dict)
    generated_at: dt.datetime = field(
        default_factory=lambda: dt.datetime.now(dt.timezone.utc)
    )
    since: dt.datetime = field(
        default_factory=lambda: dt.datetime.now(dt.timezone.utc)
        - dt.timedelta(hours=1)
    )
    window_label: str = ""


@dataclass
class TeamSection:
    """One team's slice of a report."""
    name: str
    manager: str
    feed: str
    scores: list[ScorePoint] = field(default_factory=list)
    holes: list[Item] = field(default_factory=list)       # top blockers
    priorities: list[Item] = field(default_factory=list)  # next actions
    achievements: list[Item] = field(default_factory=list)  # done + learned


def group_by_team(data: ReportData
                  ) -> tuple[list[TeamSection], dict[str, list[Item]]]:
    """Split report items across the nine teams.

    Returns (sections in TEAM_STRUCTURE order, unassigned items by kind).
    Items that name no area and match no worker prefix are NOT guessed
    into a team — they surface under Cross-team signals.
    """
    by_team: dict[str, dict[str, list[Item]]] = {
        t["name"]: {"holes": [], "achievements": [], "priorities": []}
        for t in TEAM_STRUCTURE
    }
    unassigned: dict[str, list[Item]] = {
        "holes": [], "achievements": [], "priorities": [],
        "intelligence": [],
    }

    def put(kind: str, item: Item):
        team = attribute_team(item, kind)
        if team is not None and team in by_team:
            by_team[team][kind].append(item)
        else:
            unassigned[kind].append(item)

    for h in data.holes:
        put("holes", h)
    for a in data.achievements:
        put("achievements", a)
    for n in data.next_actions:
        put("priorities", n)
    for ig in data.intelligence:
        # Lessons learned land in the attributed team's "This hour".
        team = attribute_team(ig, "intelligence")
        if team is not None and team in by_team:
            by_team[team]["achievements"].append(ig)
        else:
            unassigned["intelligence"].append(ig)

    scores_by_area = {sp.area: sp for sp in data.scores}
    sections: list[TeamSection] = []
    for t in TEAM_STRUCTURE:
        secs = [scores_by_area[a] for a in t["areas"]
                if a in scores_by_area]
        sections.append(TeamSection(
            name=t["name"],
            manager=t["manager"],
            feed=t["feed"],
            scores=secs,
            holes=sorted(by_team[t["name"]]["holes"],
                         key=lambda i: -i.priority),
            priorities=by_team[t["name"]]["priorities"],
            achievements=by_team[t["name"]]["achievements"],
        ))
    return sections, unassigned


def _short(text: str, limit: int = 110) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    return text if len(text) <= limit else text[:limit].rstrip() + "…"


def action_plan_text(section: TeamSection) -> str:
    """Brief honest action plan: top hole -> top priority -> verify.

    Built only from recorded items. When the team has no recorded
    holes or priorities this window, says so instead of inventing one.
    """
    bits: list[str] = []
    if section.holes:
        bits.append("close: " + _short(section.holes[0].text))
    if section.priorities:
        bits.append("land: " + _short(section.priorities[0].text))
    below = [s for s in section.scores if s.score < 9.0]
    if below:
        bits.append("independent verification → re-score toward 10")
    elif section.scores:
        bits.append("hold 9.0+ via independent verification; harden toward 10")
    if not bits:
        return ("_No recorded actions this window — team to publish "
                "plan on feed._")
    return " → ".join(bits) + "."


# ---------------------------------------------------------------------------
# Score extraction from worker logs
# ---------------------------------------------------------------------------

# Three separate patterns so overlap can be resolved: a movement
# ("8.5 → 8.8") always wins over a point score ("re-score: 8.5") whose
# span it overlaps — the movement's NEW value is the current score.
_MOVEMENT_RE = re.compile(r"(\d{1,2}\.\d)\s*(?:→|->)\s*(\d{1,2}\.\d)")
_SINGLE_RE = re.compile(
    r"(?<![\w-])[Ss]core[:\s]+(?:[A-Za-z][A-Za-z &/-]{0,40}?\s+)?(\d{1,2}\.\d)"
)
# 2026-10-08: the optional topic phrase lets "Honest score: Retrieval 7.0/10"
# extract 7.0. The (?<![\w-]) guard still rejects "re-score:"/"scorecard".
_BOLD_RE = re.compile(
    r"\*\*(\d{1,2}\.\d)(?:/10)?(?:\s+[A-Za-z-]+){0,2}\*\*"
)
# 2026-10-08: allow up to two qualifier words before the closing ** so
# "**3.0/10 unchanged**" (an honest stated score) is extracted. A 10/10
# is still never extracted — see _MAX_HEURISTIC_SCORE.

# 10.0 is never heuristically extracted: a 10/10 requires Shawn's explicit
# confirmation (mission law — "a self-declared 10 without his word is not
# a 10"). A worker "claiming 10/10" is awaiting confirmation, not scored.
_MAX_HEURISTIC_SCORE = 10.0  # exclusive upper bound

# Sentences in aspirational/target context are not current-score claims.
# ("Production Readiness must move from 3.0 to 10", "the 3.0→10.0 drive")
_NON_SCORE_CONTEXT_RE = re.compile(
    r"\b(drive|drives|target|targets|goal|goals|roadmap|must move|"
    r"plan to|plans to|until an honest|aspir\w+|aiming for)\b",
    re.IGNORECASE,
)

# Historical restatements are not current claims (2026-10-09, Pair G round 2).
# "The Successor Reuse score of 4.5 was the old pre-trial baseline" laundered
# a stale 4.5 into state and overwrote the true 8.0, driving a fake-regression
# headline. A sentence whose score is framed as history — past tense, baseline,
# previous — yields a "history" point that NEVER overwrites state. The movement
# arrow is exempt: "4.5 → 8.0" names the new value explicitly, and the
# right-hand value is by definition current.
_HISTORICAL_SCORE_RE = re.compile(
    r"\b(was|were|old|previous|previously|baseline|used to be|before the|"
    r"formerly|back then|historical|history of|had been|prior)\b",
    re.IGNORECASE,
)


def _scores_in_sentence(sentence: str) -> list[float]:
    """Extract score values from one sentence, movement-wins on overlap."""
    taken: list[tuple[int, int]] = []
    scores: list[tuple[int, float]] = []

    def overlaps(start: int, end: int) -> bool:
        return any(s < end and start < e for s, e in taken)

    for m in _MOVEMENT_RE.finditer(sentence):
        try:
            val = float(m.group(2))  # NEW score, not old
        except ValueError:
            continue
        if 0.0 <= val < _MAX_HEURISTIC_SCORE:
            taken.append(m.span())
            scores.append((m.start(), val))
    for pat in (_SINGLE_RE, _BOLD_RE):
        for m in pat.finditer(sentence):
            if overlaps(*m.span()):
                continue
            try:
                val = float(m.group(1))
            except ValueError:
                continue
            if 0.0 <= val < _MAX_HEURISTIC_SCORE:
                taken.append(m.span())
                scores.append((m.start(), val))
    scores.sort()  # left-to-right; last = most recent statement
    return [v for _, v in scores]


def _split_sentences(text: str) -> list[str]:
    """Split text into sentences on common boundaries.

    Score extraction requires the area name and the score to appear in
    the SAME sentence — a line like "Successor moved 3.5 → 4.5; retrieval
    still stubbed" must not attribute 4.5 to Retrieval.
    """
    parts = re.split(r"\n+|(?<=[.;])\s+|;\s+", text)
    return [p.strip() for p in parts if p.strip()]


def _areas_in(text: str) -> list[str]:
    """All canonical areas mentioned in the text, longest-alias-first."""
    low = text.lower()
    found: list[str] = []
    for alias in sorted(AREA_ALIASES, key=len, reverse=True):
        if alias in low and AREA_ALIASES[alias] not in found:
            found.append(AREA_ALIASES[alias])
    return found


def _normalize_area(text: str) -> str | None:
    areas = _areas_in(text)
    return areas[0] if areas else None


def extract_scores_from_text(text: str, source: str,
                              as_of: dt.datetime) -> list[ScorePoint]:
    """Heuristically extract (area, score) pairs from a worker log or memory.

    Rules:
      1. The area name and the score must be in the SAME sentence.
      2. A sentence with multiple areas and a score is skipped (ambiguous —
         never guess which area the score belongs to).
      3. "<old> → <new>" yields the NEW score.
      4. Aspirational/target sentences ("the 3.0→10.0 drive", "must move
         from 3.0 to 10") are skipped — a goal is not a current score.
      5. 10.0 is never extracted (requires Shawn's explicit confirmation).
    Lines/sentences without a recognizable area are skipped.
    """
    points: list[ScorePoint] = []
    for sentence in _split_sentences(text):
        if _NON_SCORE_CONTEXT_RE.search(sentence):
            continue  # aspirational or target language, not a current score
        areas = _areas_in(sentence)
        if len(areas) != 1:
            continue  # zero areas: nothing to attribute; >1: ambiguous
        area = areas[0]
        scores = _scores_in_sentence(sentence)
        if scores:
            # Historical framing ("was the old baseline") is a restatement,
            # not a claim — unless a movement arrow names the new value.
            # History points never overwrite state (see collect()).
            status = "claim"
            if (_HISTORICAL_SCORE_RE.search(sentence)
                    and not _MOVEMENT_RE.search(sentence)):
                status = "history"
            # Last score in the sentence = most recent statement.
            points.append(ScorePoint(area=area, score=scores[-1],
                                     as_of=as_of, source=source,
                                     status=status))
    return points


# ---------------------------------------------------------------------------
# Section extraction from worker logs
# ---------------------------------------------------------------------------

_SECTION_RE = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)

# Priority keywords for holes: higher weight = more urgent.
_HOLE_PRIORITY = [
    (r"protected gate|shawn'?s word|needs.*shawn|awaiting.*shawn", 30),
    (r"\bred\b|red tip|ci.*fail|failing", 25),
    (r"blocked|blocker|stalled", 20),
    (r"verif|review|merge", 15),
    (r"conflict", 18),
]


def _hole_priority(text: str) -> int:
    score = 5  # baseline: it was worth writing down
    low = text.lower()
    for pattern, weight in _HOLE_PRIORITY:
        if re.search(pattern, low):
            score += weight
    return score


def _section_items(text: str, section_names: list[str]) -> list[tuple[str, str]]:
    """Return (section, bullet) tuples under any of the named ## sections."""
    items: list[tuple[str, str]] = []
    sections = _SECTION_RE.split(text)
    # sections[0] is preamble; then alternating (title, body).
    for i in range(1, len(sections), 2):
        title = sections[i].strip()
        body = sections[i + 1] if i + 1 < len(sections) else ""
        if any(name in title.lower() for name in section_names):
            for line in body.splitlines():
                line = line.strip()
                if line.startswith(("- ", "* ", "1.", "2.", "3.", "4.", "5.")):
                    cleaned = re.sub(r"^[-*]\s+|^\d+\.\s+", "", line).strip()
                    if cleaned:
                        items.append((title.lower(), cleaned))
    return items


# ---------------------------------------------------------------------------
# Timestamp extraction — the freshness fix (2026-10-09).
#
# Every Item gets a ts (UTC). Sources, in order:
#   worker logs:  "#" title header ("— 2026-10-09 09:41–09:47 UTC"),
#                 else filename tail (YYYYMMDD-HHMM), else file mtime.
#   memory logs:  the "##" section header ("— 00:08 UTC",
#                 "2026-10-09 02:37 UTC"); the file's date fills a missing
#                 date. A header with no parseable time -> ts None.
# An item whose ts is None or older than the window is DROPPED at collect.
# Never recycled, never guessed.
# ---------------------------------------------------------------------------

_WORKER_TITLE_TS_RE = re.compile(
    r"(\d{4}-\d{2}-\d{2})[^\n]{0,60}?(\d{1,2}:\d{2})"
)
_WORKER_FILENAME_TS_RE = re.compile(r"(\d{8})-(\d{4})$")
_MEM_HEADER_TS_RE = re.compile(
    r"(\d{4}-\d{2}-\d{2})?[^0-9\n]{0,40}?(\d{1,2}:\d{2})"
    r"(?:\s*[–—-]\s*\d{1,2}:\d{2})?\s*UTC"
)


def _worker_log_ts(path: Path, text: str,
                    mtime: dt.datetime) -> dt.datetime:
    """When a worker log's content happened: title header, else filename,
    else mtime. All items in the log share it."""
    m = _WORKER_TITLE_TS_RE.search(text[:800])
    if m:
        try:
            return dt.datetime.fromisoformat(
                f"{m.group(1)}T{m.group(2)}:00+00:00")
        except ValueError:
            pass
    m = _WORKER_FILENAME_TS_RE.search(path.stem)
    if m:
        try:
            d = dt.datetime.strptime(m.group(1) + m.group(2), "%Y%m%d%H%M")
            return d.replace(tzinfo=dt.timezone.utc)
        except ValueError:
            pass
    return mtime


def _memory_header_ts(header: str,
                      file_date: dt.date | None) -> dt.datetime | None:
    """Parse a memory-log '##' header into a UTC timestamp.

    Returns None when the header carries no parseable time — the items
    under it are timestamp-unknown and will be dropped, never recycled.
    """
    m = _MEM_HEADER_TS_RE.search(header)
    if not m:
        return None
    try:
        hh, mm = int(m.group(2)[:2]), int(m.group(2)[3:5])
        if not (0 <= hh <= 23 and 0 <= mm <= 59):
            return None
        if m.group(1):
            d = dt.date.fromisoformat(m.group(1))
        elif file_date:
            d = file_date
        else:
            return None
        return dt.datetime(d.year, d.month, d.day, hh, mm,
                           tzinfo=dt.timezone.utc)
    except ValueError:
        return None


def parse_worker_log(path: Path) -> dict:
    """Parse one worker run log into structured pieces."""
    text = path.read_text(encoding="utf-8", errors="replace")
    try:
        mtime = dt.datetime.fromtimestamp(path.stat().st_mtime,
                                          tz=dt.timezone.utc)
    except OSError:
        mtime = dt.datetime.now(dt.timezone.utc)
    worker = path.stem  # e.g. learn-builder-20261008-0245
    ts = _worker_log_ts(path, text, mtime)

    scores = extract_scores_from_text(text, source=worker, as_of=ts)

    holes = [
        Item(text=t, source=worker, priority=_hole_priority(t), section=s,
             ts=ts)
        for s, t in _section_items(text, ["blockers", "blocker"])
    ]
    next_actions = [
        Item(text=t, source=worker, section=s, ts=ts)
        for s, t in _section_items(text, ["next"])
    ]
    achievements = [
        Item(text=t, source=worker, section=s, ts=ts)
        for s, t in _section_items(text, ["work", "done", "completed",
                                          "achievements"])
    ]
    activity = [
        Item(text=t, source=worker, section=s, ts=ts)
        for s, t in _section_items(text, ["feeds", "sign-in", "sign in"])
    ]
    return {
        "worker": worker,
        "mtime": mtime,
        "ts": ts,
        "scores": scores,
        "holes": holes,
        "next_actions": next_actions,
        "achievements": achievements,
        "activity": activity,
    }


# ---------------------------------------------------------------------------
# Memory log parsing
# ---------------------------------------------------------------------------

_MEM_TAG_RE = re.compile(r"^\s*-\s*\[(?P<tag>[a-z|]+)\|(?P<sev>[a-z]+)\]\s*(?P<body>.+)$")


def _memory_as_of(path: Path) -> dt.datetime:
    """Statement date for a memory log: the filename date, not mtime.

    A file touched today can contain yesterday's scores. Using the
    YYYY-MM-DD in the filename as the score date keeps newer-dated logs'
    scores ahead of older-dated logs' regardless of filesystem mtime.
    Falls back to now when the stem is not a date.
    """
    try:
        d = dt.date.fromisoformat(path.stem)
        return dt.datetime(d.year, d.month, d.day, 23, 59, 59,
                           tzinfo=dt.timezone.utc)
    except ValueError:
        return dt.datetime.now(dt.timezone.utc)


def parse_memory_log(path: Path) -> dict:
    """Parse a daily memory log into timestamped events.

    The log is split on '##' headers; each section's items inherit the
    header's timestamp (the file's date fills a missing date). Sections
    whose header carries no parseable time yield ts=None items — dropped
    at collect, never recycled into a later window.
    """
    text = path.read_text(encoding="utf-8", errors="replace") \
        if path.exists() else ""
    try:
        file_date = dt.date.fromisoformat(path.stem)
    except ValueError:
        file_date = None

    # Split into (header_ts, section_text) chunks.
    chunks: list[tuple[dt.datetime | None, str]] = []
    current_ts: dt.datetime | None = None
    current_lines: list[str] = []
    for line in text.splitlines():
        if line.startswith("##"):
            if current_lines:
                chunks.append((current_ts, "\n".join(current_lines)))
            current_ts = _memory_header_ts(line, file_date)
            current_lines = []
        else:
            current_lines.append(line)
    if current_lines:
        chunks.append((current_ts, "\n".join(current_lines)))
    if not chunks and text.strip():
        chunks.append((None, text))

    achievements, intelligence, holes, scores = [], [], [], []
    for ts, chunk in chunks:
        for line in chunk.splitlines():
            m = _MEM_TAG_RE.match(line)
            if not m:
                continue
            tag, body = m.group("tag"), m.group("body").strip()
            src = f"memory:{path.stem}"
            if "score" in tag or "event" in tag or "achievement" in tag:
                achievements.append(Item(text=body, source=src, ts=ts))
            if ("lesson" in tag or "principle" in tag or "law" in tag
                    or "correction" in tag):
                # Corrections are knowledge (what we now know), not holes.
                intelligence.append(Item(text=body, source=src, ts=ts))
            if "blocker" in tag:
                holes.append(Item(text=body, source=src,
                                  priority=_hole_priority(body), ts=ts))
        if ts is not None:
            scores.extend(extract_scores_from_text(
                chunk, source=f"memory:{path.stem}", as_of=ts))
    return {"achievements": achievements, "intelligence": intelligence,
            "holes": holes, "scores": scores}


# ---------------------------------------------------------------------------
# GitHub fetcher (read-only)
# ---------------------------------------------------------------------------


def _gh(method: str, path: str, body: str | None = None) -> object:
    cmd = [str(GH_API), method, path]
    if body is not None:
        cmd.append(body)
    out = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    if out.returncode != 0:
        raise RuntimeError(f"gh-api {method} {path} failed: {out.stderr[:300]}")
    return json.loads(out.stdout or "null")


def fetch_github(since: dt.datetime) -> dict:
    """Recent PRs + #1354 comments since the watermark. Read-only."""
    snap: dict = {"prs": [], "comments": [], "error": None}
    try:
        prs = _gh("GET",
                  f"/repos/{REPO}/pulls?state=all&sort=updated"
                  f"&direction=desc&per_page=30") or []
        for pr in prs:
            updated = pr.get("updated_at", "")
            try:
                upd = dt.datetime.fromisoformat(updated.replace("Z", "+00:00"))
            except ValueError:
                continue
            if upd >= since:
                snap["prs"].append({
                    "number": pr.get("number"),
                    "title": pr.get("title", "")[:100],
                    "state": pr.get("state"),
                    "merged": bool(pr.get("merged_at")),
                    "updated_at": updated,
                })
        comments = _gh(
            "GET",
            f"/repos/{REPO}/issues/{TEAM_ISSUE}/comments"
            f"?per_page=40&sort=updated&direction=desc") or []
        for c in comments:
            created = c.get("created_at", "")
            try:
                crt = dt.datetime.fromisoformat(created.replace("Z", "+00:00"))
            except ValueError:
                continue
            if crt >= since:
                body = (c.get("body") or "").strip().replace("\n", " ")
                snap["comments"].append({
                    "id": c.get("id"),
                    "created_at": created,
                    "author": (c.get("user") or {}).get("login"),
                    "excerpt": body[:160],
                })
    except Exception as e:  # noqa: BLE001 — degraded mode, report shows it
        snap["error"] = str(e)[:200]
    return snap


# ---------------------------------------------------------------------------
# Supabase fetcher (READ-ONLY aggregates; output truncated at 6000 chars
# so we only ever run COUNT/GROUP queries here)
# ---------------------------------------------------------------------------

_PROJECT_REF = "dahisasgpfvziswqvmvm"


def _sb_query(sql: str) -> object:
    cmd = [str(SB_API), "POST",
           f"/v1/projects/{_PROJECT_REF}/database/query",
           json.dumps({"query": sql})]
    out = subprocess.run(cmd, capture_output=True, text=True, timeout=90)
    if out.returncode != 0:
        raise RuntimeError(f"sb-api failed: {out.stderr[:300]}")
    return json.loads(out.stdout or "null")


def fetch_supabase() -> dict:
    """Candidate/ACTIVE counts from learning_evidence. SELECT only."""
    snap: dict = {"counts": {}, "error": None}
    try:
        rows = _sb_query(
            "SELECT status, COUNT(*) AS n FROM learning_evidence "
            "GROUP BY status"
        )
        if isinstance(rows, list):
            for r in rows:
                snap["counts"][str(r.get("status"))] = r.get("n")
    except Exception as e:  # noqa: BLE001 — degraded mode
        snap["error"] = str(e)[:200]
    return snap


# ---------------------------------------------------------------------------
# State: scores + watermarks
# ---------------------------------------------------------------------------


def load_score_state() -> dict:
    if SCORE_STATE_FILE.exists():
        return json.loads(SCORE_STATE_FILE.read_text(encoding="utf-8"))
    return {}


def save_score_state(state: dict) -> None:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    SCORE_STATE_FILE.write_text(json.dumps(state, indent=2, sort_keys=True),
                                encoding="utf-8")


def load_watermarks() -> dict:
    if WATERMARK_FILE.exists():
        return json.loads(WATERMARK_FILE.read_text(encoding="utf-8"))
    return {}


def save_watermark(report_type: str, at: dt.datetime) -> None:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    marks = load_watermarks()
    marks[report_type] = at.isoformat()
    WATERMARK_FILE.write_text(json.dumps(marks, indent=2, sort_keys=True),
                              encoding="utf-8")


# ---------------------------------------------------------------------------
# Report assembly
# ---------------------------------------------------------------------------


def _dedup(items: list[Item]) -> list[Item]:
    seen: set[str] = set()
    out: list[Item] = []
    for it in items:
        key = re.sub(r"\s+", " ", it.text.lower())[:120]
        if key not in seen:
            seen.add(key)
            out.append(it)
    return out


# A heuristic claim not re-affirmed within this long is stale: lanes
# re-score roughly every 6h, so two silent cycles means nobody stands
# behind the number anymore. Authoritative scores are exempt — their
# warrant is authority (Naya 1 / Shawn), not recency.
SCORE_STALE_AFTER = dt.timedelta(hours=12)

# Allow a small clock-skew margin for items timestamped just ahead of now.
_FUTURE_SKEW = dt.timedelta(minutes=10)


def _fresh(items: list[Item], since: dt.datetime,
           now: dt.datetime) -> list[Item]:
    """Window filter — the Usefulness Gate.

    An item whose ts is unknown (None) or older than the window is stale:
    DROPPED, never recycled into a later report.
    """
    return [i for i in items
            if i.ts is not None and since <= i.ts <= now + _FUTURE_SKEW]


def _one_sentence(text: str, limit: int = 110) -> str:
    """First sentence of the text, single line, capped."""
    text = re.sub(r"\s+", " ", text).strip()
    m = re.search(r"\.\s", text)
    if m and m.start() < limit:
        text = text[:m.start() + 1]
    return _short(text, limit)


def _what_moved(data: ReportData, limit: int = 8) -> list[str]:
    """Window-fresh changes, newest first: achievements, score movements,
    merged PRs. Shared by the markdown and PDF renderers."""
    moved: list[tuple[dt.datetime, str]] = []
    for a in data.achievements:
        moved.append((a.ts, f"{a.text} _(src: {a.source})_"))
    for sp in data.scores:
        prev = data.previous_scores.get(sp.area)
        if prev is not None and prev != sp.score:
            moved.append((sp.as_of,
                          f"{sp.area} {prev:.1f} → {sp.score:.1f} "
                          f"({sp.status})"))
    gh = data.github_snapshot or {}
    if not gh.get("error"):
        for pr in gh.get("prs", []):
            try:
                ts = dt.datetime.fromisoformat(
                    pr["updated_at"].replace("Z", "+00:00"))
            except (ValueError, KeyError):
                continue
            # An in-window PR update IS window activity — the headline must
            # never claim "quiet" while Evidence lists updated PRs.
            if pr.get("merged"):
                moved.append((ts, f"PR #{pr['number']} merged: {pr['title']}"))
            else:
                moved.append((ts, f"PR #{pr['number']} updated: {pr['title']}"))
    epoch = dt.datetime.min.replace(tzinfo=dt.timezone.utc)
    moved.sort(key=lambda m: (m[0] or epoch), reverse=True)
    return [text for _, text in moved[:limit]]


def _headline_text(data: ReportData, moved: list[str]) -> str:
    """One sentence: the thing that mattered most this window."""
    best: tuple[float, str, float, float] | None = None
    for sp in data.scores:
        prev = data.previous_scores.get(sp.area)
        if prev is not None and prev != sp.score:
            d = abs(sp.score - prev)
            if best is None or d > best[0]:
                best = (d, sp.area, prev, sp.score)
    if best:
        _, area, prev, now = best
        return f"{area} {prev:.1f} → {now:.1f}."
    if moved:
        # The newest window-fresh event is the headline.
        hl = _one_sentence(re.sub(r"\s*_\s*\(src:\s*[^)]+\)\s*_\s*",
                                  " ", moved[0]).strip())
        if hl and hl[-1] not in ".!?:":
            hl += "."
        return hl
    if data.achievements:
        newest = max(data.achievements,
                     key=lambda a: a.ts or dt.datetime.min.replace(
                         tzinfo=dt.timezone.utc))
        return _one_sentence(newest.text)
    if data.holes:
        top = max(data.holes, key=lambda h: h.priority)
        return "Blocked: " + _one_sentence(top.text)
    return "Quiet hour."


class ReportGenerator:
    """Assembles a report from injectable data-source functions."""

    def __init__(self,
                 fetch_worker_logs=None,
                 fetch_memory=None,
                 fetch_github_fn=None,
                 fetch_supabase_fn=None,
                 load_scores_fn=None,
                 save_scores_fn=None):
        self.fetch_worker_logs = fetch_worker_logs or self._default_worker_logs
        self.fetch_memory = fetch_memory or self._default_memory
        self.fetch_github_fn = fetch_github_fn or fetch_github
        self.fetch_supabase_fn = fetch_supabase_fn or fetch_supabase
        self.load_scores_fn = load_scores_fn or load_score_state
        self.save_scores_fn = save_scores_fn or save_score_state

    # -- default fetchers ---------------------------------------------------

    @staticmethod
    def _default_worker_logs(since: dt.datetime) -> list[dict]:
        parsed = []
        if not HIDDEN_FILES.exists():
            return parsed
        for path in sorted(HIDDEN_FILES.glob("*.md")):
            try:
                mtime = dt.datetime.fromtimestamp(
                    path.stat().st_mtime, tz=dt.timezone.utc)
            except OSError:
                continue
            if mtime >= since - dt.timedelta(hours=2):  # recency margin
                try:
                    parsed.append(parse_worker_log(path))
                except OSError:
                    continue
        return parsed

    @staticmethod
    def _default_memory(since: dt.datetime) -> dict:
        agg: dict = {"achievements": [], "intelligence": [],
                     "holes": [], "scores": []}
        day = since.date()
        end = dt.datetime.now(dt.timezone.utc).date()
        d = day
        while d <= end:
            parsed = parse_memory_log(MEMORY_DIR / f"{d.isoformat()}.md")
            for k in agg:
                agg[k].extend(parsed[k])
            d += dt.timedelta(days=1)
        return agg

    # -- main entry ----------------------------------------------------------

    def collect(self, report_type: str, since: dt.datetime,
                now: dt.datetime) -> ReportData:
        data = ReportData(since=since, generated_at=now,
                          window_label=report_type)

        worker_logs = self.fetch_worker_logs(since)
        memory = self.fetch_memory(since)

        # Scores: latest point per area from this window, merged over state.
        state = self.load_scores_fn()
        previous = {a: v.get("score") for a, v in state.items()
                    if isinstance(v, dict)}
        data.previous_scores = previous

        window_points: dict[str, ScorePoint] = {}
        for log in worker_logs:
            for p in log["scores"]:
                # Freshness applies to scores too: a score stated before
                # the window must not move state in this window.
                if p.as_of < since:
                    continue
                # Future-dated scores are rejected at ingest (2026-10-09,
                # Pair G round 2): a score 3h in the future overwrote Truth
                # 9.0 → 7.0 and was immortal — negative age defeats the 12h
                # staleness rule and wins every tie-break. Small clock-skew
                # allowance only.
                if p.as_of > now + _FUTURE_SKEW:
                    continue
                # Historical restatements never overwrite state: "the 4.5
                # was the old baseline" is history, not a claim.
                if p.status == "history":
                    continue
                cur = window_points.get(p.area)
                if cur is None or p.as_of >= cur.as_of:
                    window_points[p.area] = p
        for p in memory["scores"]:
            if p.as_of < since:
                continue
            if p.as_of > now + _FUTURE_SKEW:
                continue
            if p.status == "history":
                continue
            cur = window_points.get(p.area)
            if cur is None or p.as_of >= cur.as_of:
                window_points[p.area] = p

        new_state = dict(state)
        # Pinned authoritative scores — set by Naya 1 / Shawn reconciliation.
        # Heuristic extraction NEVER overwrites these.
        # 2026-10-08: Naya 1 reconciled whole-area Learning = 5.0.
        # The 7.0 seen in worker logs is the bounded trial-rung score, not whole-area.
        # The pin carries its REAL reconciliation timestamp (2026-10-09,
        # Pair G round 2): the old code stamped the triggering window's
        # time, so a days-old 5.0 rendered with today's timestamp —
        # a fabricated as_of. Never fabricate as_of.
        PINNED_AUTHORITATIVE = {
            "Learning": {
                "score": 5.0,
                # Date-level: Naya 1's reconciliation, 2026-10-08.
                # Exact hour unrecorded — do not invent precision.
                "as_of": "2026-10-08T00:00:00+00:00",
                "source": "Naya 1 reconciliation 2026-10-08 (pinned)",
            },
        }
        for area, point in window_points.items():
            existing = new_state.get(area, {})
            # Pinned scores win over everything heuristic — but the pin is
            # written once with its real timestamp and never refreshed.
            if area in PINNED_AUTHORITATIVE:
                pin = PINNED_AUTHORITATIVE[area]
                if (existing.get("status") == "authoritative"
                        and existing.get("score") == pin["score"]):
                    continue  # pin already in place; never refresh as_of
                new_state[area] = {
                    "score": pin["score"],
                    "as_of": pin["as_of"],
                    "source": pin["source"],
                    "status": "authoritative",
                }
                continue
            # Authoritative scores are never overwritten by heuristic
            # claims — neither the label nor the value. (2026-10-09: a
            # fresh "Truth 2.0/10" claim overwrote Truth 9.0's VALUE while
            # keeping the authoritative LABEL — a false number wearing the
            # most-trusted badge. The old code guarded the label; the score
            # column was the payload.) Authoritative updates still flow
            # through authoritative points.
            if (existing.get("status") == "authoritative"
                    and point.status != "authoritative"):
                continue
            new_state[area] = {
                "score": point.score,
                "as_of": point.as_of.isoformat(),
                "source": point.source,
                "status": point.status,
            }
        self.save_scores_fn(new_state)

        for area in AREAS:
            entry = new_state.get(area)
            if entry:
                as_of = dt.datetime.fromisoformat(entry["as_of"])
                if as_of.tzinfo is None:
                    as_of = as_of.replace(tzinfo=dt.timezone.utc)
                status = entry.get("status", "claim")
                source = entry.get("source", "?")
                # Provenance labeling — the staleness fix (2026-10-09).
                # A number without provenance is a lie with formatting:
                # a carried-forward claim is shown WITH its age and
                # source, and labeled stale once nobody has re-affirmed
                # it within SCORE_STALE_AFTER — never as a current score.
                # Seeds were never observations. Authoritative scores keep
                # their status: their warrant is authority, not recency.
                if source.startswith("seed"):
                    status = "seed"
                elif (status == "claim"
                      and now - as_of > SCORE_STALE_AFTER):
                    status = "stale"
                data.scores.append(ScorePoint(
                    area=area, score=entry["score"],
                    as_of=as_of,
                    source=source,
                    status=status,
                ))

        # Holes / achievements / activity / intelligence / next actions.
        for log in worker_logs:
            data.holes.extend(log.get("holes", []))
            data.achievements.extend(log.get("achievements", []))
            data.team_activity.extend(log.get("activity", []))
            data.next_actions.extend(log.get("next_actions", []))
        data.holes.extend(memory["holes"])
        data.achievements.extend(memory["achievements"])
        data.intelligence.extend(memory["intelligence"])

        # The Usefulness Gate: only window-fresh items survive. Stale or
        # timestamp-unknown items are dropped here — never recycled.
        data.holes = _fresh(data.holes, since, now)
        data.achievements = _fresh(data.achievements, since, now)
        data.team_activity = _fresh(data.team_activity, since, now)
        data.next_actions = _fresh(data.next_actions, since, now)
        data.intelligence = _fresh(data.intelligence, since, now)

        # GitHub + Supabase snapshots.
        data.github_snapshot = self.fetch_github_fn(since)
        data.supabase_snapshot = self.fetch_supabase_fn()

        # Rank + dedup. Per-team caps happen at render time; keep the
        # full ranked lists here so no team's items are starved by a
        # global cap.
        data.holes = _dedup(sorted(data.holes,
                                   key=lambda i: -i.priority))
        data.achievements = _dedup(data.achievements)
        data.team_activity = _dedup(data.team_activity)
        data.intelligence = _dedup(data.intelligence)
        data.next_actions = _dedup(data.next_actions)
        return data

    # -- rendering ------------------------------------------------------------
    # The Usefulness Gate (2026-10-09): structure follows the information,
    # never the org chart. No team sections, no boilerplate, no recycled
    # items. The headline is the report; the rest is evidence.

    @staticmethod
    def _delta_str(sp: ScorePoint, previous: dict) -> str:
        prev = previous.get(sp.area)
        if prev is None or prev == sp.score:
            return "—"
        return f"{sp.score - prev:+.1f}"

    @staticmethod
    def render(data: ReportData) -> str:
        kind = (data.window_label or "hourly").upper()
        stamp = data.generated_at.strftime("%a %Y-%m-%d %H:%M UTC")
        moved = _what_moved(data)
        lines = [f"# {kind} — {stamp}", ""]
        lines.append(_headline_text(data, moved))
        lines.append("")
        lines.append("## What moved")
        if moved:
            lines.extend(f"- {m}" for m in moved)
        else:
            lines.append("Quiet hour — no window activity.")
        lines.append("")
        lines.append("## Scoreboard")
        lines.append("| Area | Score | Status | As of (UTC) | Source | Δ |")
        lines.append("|---|---|---|---|---|---:|")
        if data.scores:
            for sp in data.scores:
                delta = ReportGenerator._delta_str(sp, data.previous_scores)
                asof = sp.as_of.strftime("%m-%d %H:%M")
                src = sp.source if len(sp.source) <= 44 else \
                    sp.source[:41].rstrip() + "…"
                lines.append(f"| {sp.area} | {sp.score:.1f} | {sp.status} | "
                             f"{asof} | {src} | {delta} |")
            if any(sp.status in ("stale", "seed") for sp in data.scores):
                lines.append("")
                lines.append("_Stale = claim not re-affirmed in 12h; seed = "
                             "never observed. Both show their age and source "
                             "and are never current scores._")
        else:
            lines.append("| _No scores recorded yet_ | | | | | |")
        lines.append("")
        lines.append("## Needs from Shawn")
        needs = sorted(data.holes, key=lambda i: -i.priority)[:3]
        if needs:
            for h in needs:
                lines.append(f"- {h.text} _(src: {h.source})_")
        else:
            lines.append("None this hour.")
        lines.append("")
        lines.append("## Evidence")
        gh = data.github_snapshot or {}
        sb = data.supabase_snapshot or {}
        if gh.get("error"):
            lines.append(f"- GitHub: unavailable ({gh['error']})")
        else:
            prs = gh.get("prs", [])
            merged = [p for p in prs if p.get("merged")]
            updated = [p for p in prs if not p.get("merged")]
            bits = ([f"#{p['number']} merged" for p in merged[:4]]
                    + [f"#{p['number']} updated" for p in updated[:3]])
            lines.append("- PRs: " + (", ".join(bits) if bits else
                                      "no PR activity") +
                         f" ({len(merged)} merged, {len(updated)} updated)")
            n_comments = len(gh.get("comments", []))
            if n_comments:
                lines.append(f"- #1354: {n_comments} comments this window")
        if sb.get("error"):
            lines.append(f"- Supabase: unavailable ({sb['error']})")
        else:
            counts = sb.get("counts", {})
            lines.append("- Supabase: " + (
                ", ".join(f"{k}={v}" for k, v in counts.items())
                or "no rows"))
        since_s = data.since.strftime("%H:%M UTC")
        gen_s = data.generated_at.strftime("%H:%M UTC")
        lines.append(f"_Window {since_s} → {gen_s}. "
                     f"All items carry their source._")
        return "\n".join(lines)

    def generate(self, report_type: str, since: dt.datetime,
                 now: dt.datetime | None = None) -> str:
        now = now or dt.datetime.now(dt.timezone.utc)
        data = self.collect(report_type, since, now)
        return self.render(data)

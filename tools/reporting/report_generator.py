#!/usr/bin/env python3
"""Team Naya automated reporting system — core generator.

Pulls data from all sources, distills it into Shawn's report structure:
    # [MORNING/HOURLY/NIGHTLY] Report — [date/time]
    ## Scores (all levels)
    ## Top 10 Holes (highest priority actions)
    ## Top 10 Achievements (since last report)
    ## Team Activity
    ## Intelligence Learned
    ## Next Actions

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
    "production": "Production Readiness",
    "successor": "Successor Reuse",
    "successor reuse": "Successor Reuse",
}

# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------


@dataclass
class ScorePoint:
    area: str
    score: float
    as_of: dt.datetime
    source: str
    status: str = "claim"  # "authoritative" or "claim"


@dataclass
class Item:
    text: str
    source: str
    priority: int = 0  # higher = more urgent (holes only)
    section: str = ""  # originating section, e.g. "blockers", "next"

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


# ---------------------------------------------------------------------------
# Score extraction from worker logs
# ---------------------------------------------------------------------------

# Three separate patterns so overlap can be resolved: a movement
# ("8.5 → 8.8") always wins over a point score ("re-score: 8.5") whose
# span it overlaps — the movement's NEW value is the current score.
_MOVEMENT_RE = re.compile(r"(\d{1,2}\.\d)\s*(?:→|->)\s*(\d{1,2}\.\d)")
_SINGLE_RE = re.compile(r"(?<![\w-])[Ss]core[:\s]+(\d{1,2}\.\d)")
_BOLD_RE = re.compile(r"\*\*(\d{1,2}\.\d)(?:/10)?\*\*")

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
            # Last score in the sentence = most recent statement.
            points.append(ScorePoint(area=area, score=scores[-1],
                                     as_of=as_of, source=source))
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


def parse_worker_log(path: Path) -> dict:
    """Parse one worker run log into structured pieces."""
    text = path.read_text(encoding="utf-8", errors="replace")
    try:
        mtime = dt.datetime.fromtimestamp(path.stat().st_mtime,
                                          tz=dt.timezone.utc)
    except OSError:
        mtime = dt.datetime.now(dt.timezone.utc)
    worker = path.stem  # e.g. learn-builder-20261008-0245

    scores = extract_scores_from_text(text, source=worker, as_of=mtime)

    holes = [
        Item(text=t, source=worker, priority=_hole_priority(t), section=s)
        for s, t in _section_items(text, ["blockers", "blocker"])
    ]
    next_actions = [
        Item(text=t, source=worker, section=s)
        for s, t in _section_items(text, ["next"])
    ]
    achievements = [
        Item(text=t, source=worker, section=s)
        for s, t in _section_items(text, ["work", "done", "completed",
                                          "achievements"])
    ]
    activity = [
        Item(text=t, source=worker, section=s)
        for s, t in _section_items(text, ["feeds", "sign-in", "sign in"])
    ]
    return {
        "worker": worker,
        "mtime": mtime,
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
    """Parse a daily memory log into scored events."""
    text = path.read_text(encoding="utf-8", errors="replace") \
        if path.exists() else ""
    achievements, intelligence, holes = [], [], []
    for line in text.splitlines():
        m = _MEM_TAG_RE.match(line)
        if not m:
            continue
        tag, body = m.group("tag"), m.group("body").strip()
        src = f"memory:{path.stem}"
        if "score" in tag or "event" in tag or "achievement" in tag:
            achievements.append(Item(text=body, source=src))
        if ("lesson" in tag or "principle" in tag or "law" in tag
                or "correction" in tag):
            # Corrections are knowledge (what we now know), not open holes.
            intelligence.append(Item(text=body, source=src))
        if "blocker" in tag:
            holes.append(Item(text=body, source=src,
                              priority=_hole_priority(body)))
    scores = extract_scores_from_text(text, source=f"memory:{path.stem}",
                                      as_of=_memory_as_of(path))
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
                cur = window_points.get(p.area)
                if cur is None or p.as_of >= cur.as_of:
                    window_points[p.area] = p
        for p in memory["scores"]:
            cur = window_points.get(p.area)
            if cur is None or p.as_of >= cur.as_of:
                window_points[p.area] = p

        new_state = dict(state)
        for area, point in window_points.items():
            existing = new_state.get(area, {})
            # Never downgrade: an authoritative score is not overwritten
            # by a heuristic claim's status.
            status = point.status
            if (existing.get("status") == "authoritative"
                    and status != "authoritative"):
                status = "authoritative"
            new_state[area] = {
                "score": point.score,
                "as_of": point.as_of.isoformat(),
                "source": point.source,
                "status": status,
            }
        self.save_scores_fn(new_state)

        for area in AREAS:
            entry = new_state.get(area)
            if entry:
                data.scores.append(ScorePoint(
                    area=area, score=entry["score"],
                    as_of=dt.datetime.fromisoformat(entry["as_of"]),
                    source=entry.get("source", "?"),
                    status=entry.get("status", "claim"),
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

        # GitHub + Supabase snapshots.
        data.github_snapshot = self.fetch_github_fn(since)
        data.supabase_snapshot = self.fetch_supabase_fn()

        # Rank + cap.
        data.holes = _dedup(sorted(data.holes,
                                   key=lambda i: -i.priority))[:10]
        data.achievements = _dedup(data.achievements)[:10]
        data.team_activity = _dedup(data.team_activity)[:12]
        data.intelligence = _dedup(data.intelligence)[:10]
        data.next_actions = _dedup(data.next_actions)[:10]
        return data

    # -- rendering ------------------------------------------------------------

    @staticmethod
    def render(data: ReportData) -> str:
        kind = data.window_label.upper()
        stamp = data.generated_at.strftime("%Y-%m-%d %H:%M UTC")
        lines = [f"# {kind} Report — {stamp}", ""]

        # Scores table.
        lines.append("## Scores (all levels)")
        lines.append("")
        lines.append("| Area | Prev | Now | Δ | Status |")
        lines.append("|------|------|-----|---|--------|")
        for sp in data.scores:
            prev = data.previous_scores.get(sp.area)
            if prev is None or prev == sp.score:
                delta = "—"
            else:
                d = sp.score - prev
                delta = f"{d:+.1f}"
            tag = "authoritative" if sp.status == "authoritative" else "claim"
            lines.append(f"| {sp.area} | "
                         f"{prev if prev is not None else '—'} | "
                         f"{sp.score:.1f} | {delta} | {tag} |")
        missing = [a for a in AREAS
                   if not any(s.area == a for s in data.scores)]
        if missing:
            lines.append("")
            lines.append(f"_No data this window: {', '.join(missing)}_")
        lines.append("")

        def section(title: str, items: list[Item], numbered: bool = True):
            lines.append(f"## {title}")
            lines.append("")
            if not items:
                lines.append("_None recorded this window._")
            for i, it in enumerate(items, 1):
                prefix = f"{i}." if numbered else "-"
                lines.append(f"{prefix} {it.text} _(src: {it.source})_")
            lines.append("")

        section("Top 10 Holes (highest priority actions)", data.holes)
        section("Top 10 Achievements (since last report)", data.achievements)
        section("Team Activity", data.team_activity, numbered=False)
        section("Intelligence Learned", data.intelligence, numbered=False)
        section("Next Actions", data.next_actions, numbered=False)

        # Evidence snapshots.
        gh = data.github_snapshot
        sb = data.supabase_snapshot
        lines.append("## Evidence Snapshot")
        lines.append("")
        if gh.get("error"):
            lines.append(f"- GitHub: unavailable ({gh['error']})")
        else:
            prs = gh.get("prs", [])
            merged = sum(1 for p in prs if p.get("merged"))
            lines.append(f"- GitHub: {len(prs)} PRs updated "
                         f"({merged} merged), "
                         f"{len(gh.get('comments', []))} #1354 comments")
            for p in prs[:5]:
                mark = "MERGED" if p["merged"] else p["state"].upper()
                lines.append(f"  - #{p['number']} [{mark}] {p['title']}")
        if sb.get("error"):
            lines.append(f"- Supabase: unavailable ({sb['error']})")
        else:
            counts = sb.get("counts", {})
            lines.append("- Supabase learning_evidence: " +
                         ", ".join(f"{k}={v}" for k, v in counts.items())
                         or "no rows")
        lines.append("")
        since_s = data.since.strftime("%Y-%m-%d %H:%M UTC")
        lines.append(f"_Window: since {since_s}. "
                     f"Generated {stamp}. All items carry their source._")
        return "\n".join(lines)

    def generate(self, report_type: str, since: dt.datetime,
                 now: dt.datetime | None = None) -> str:
        now = now or dt.datetime.now(dt.timezone.utc)
        data = self.collect(report_type, since, now)
        return self.render(data)

#!/usr/bin/env python3
"""
Option Miner — Layer 3 of the Ultimate Decision Machine.

Given a structured intent (from Layer 2) plus the world model snapshot
(from Layer 1), MINE candidate options from reality. Never invent.

Options come from:
  - Open PRs (from the world model's cached PR section)
  - Lane states (free lanes = dispatch candidates; occupied = in-flight work)
  - Mission priorities (from the world model's mission section)
  - Grand TODO items (local file, cited by file + line)
  - The user's own "what about X?" (marked user_added, never confused
    with reality-mined options)

Rules:
  - Every option cites its source. An option without a source is not an option.
  - Options the world model doesn't know about are NOT offered. If the cache
    is stale or missing, say so — never mine from imagination.
  - Zero network calls. Local cache only.
  - Duplicate options (same branch, same work) are collapsed with a note.

Usage:
  python3 tools/option_miner.py mine --intent '<intent JSON>'
  python3 tools/option_miner.py mine --stdin < intent.json
  python3 tools/option_miner.py mine --intent '<json>' --add-option "what about X?"
  python3 tools/option_miner.py mine --intent '<json>' --plain

Exit codes:
  0 — options mined (possibly an empty list with an honest note)
  2 — cannot mine: no world model, intent unclear, or unknown intent type
"""

import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

WORLD_MODEL_PATH = Path(os.path.expanduser("~/.naya/world-model.json"))
GRAND_TODO_PATH = Path(os.path.expanduser(
    "~/workspace/goals/super-brain-engine-to-10-10/hidden_files/areas/GRAND-TODO.md"))

# Sections the miner knows how to read from the world model cache.
KNOWN_SECTIONS = ("tip", "prs", "lanes", "ledger", "mission", "laws")


# ---------------------------------------------------------------------------
# World model reading (local cache only — no network)
# ---------------------------------------------------------------------------

def load_world_model():
    """Load the world model from local cache. Returns (model, warnings)."""
    warnings = []
    if not WORLD_MODEL_PATH.exists():
        return None, ["world model not found — run tools/world_model.py snapshot first"]
    try:
        model = json.loads(WORLD_MODEL_PATH.read_text())
    except (json.JSONDecodeError, OSError) as e:
        return None, [f"world model unreadable: {e}"]
    for name, section in model.get("sections", {}).items():
        status = section.get("status", "UNKNOWN")
        if status in ("STALE", "UNKNOWN"):
            warnings.append(f"world model section '{name}' is {status}")
    return model, warnings


def section(model, name):
    """Get a section if it's usable (status OK). Returns (data, status)."""
    sections = (model or {}).get("sections", {})
    s = sections.get(name) or {}
    status = s.get("status", "UNKNOWN")
    if status == "OK":
        return s, "OK"
    return None, status


# ---------------------------------------------------------------------------
# Grand TODO reading (local file — cited by file + line)
# ---------------------------------------------------------------------------

def load_grand_todo():
    """Read open TODO items from the local GRAND-TODO file.

    Returns a list of {title, file, line}. Never invents items."""
    items = []
    if not GRAND_TODO_PATH.exists():
        return items, [f"grand TODO not found at {GRAND_TODO_PATH}"]
    try:
        lines = GRAND_TODO_PATH.read_text().splitlines()
    except OSError as e:
        return items, [f"grand TODO unreadable: {e}"]
    for i, line in enumerate(lines, start=1):
        # Open items: markdown checkboxes, unchecked
        m = re.match(r"\s*[-*]\s*\[\s\]\s*(.+)", line)
        if m:
            title = m.group(1).strip()
            if title and not re.match(r"(?i)^(note|done|completed)", title):
                items.append({
                    "title": title[:120],
                    "file": str(GRAND_TODO_PATH),
                    "line": i,
                })
    return items, []


# ---------------------------------------------------------------------------
# Option construction
# ---------------------------------------------------------------------------

def make_option(option_id, source_type, source, title, relevance, why,
                evidence_links, freshness):
    """Build one option dict. Every field has provenance or is None."""
    return {
        "id": option_id,
        "source_type": source_type,     # pr | lane | mission | todo | user_added
        "source": source,              # e.g. "PR #2410", "lane alpha", "grand-todo L42"
        "title": title,
        "relevance": relevance,        # 0.0–1.0, or None for unscored user options
        "why": why,
        "evidence_links": evidence_links,
        "freshness": freshness,        # from the world-model section as_of_utc
    }


def option_freshness(section_data):
    """Freshness label for options mined from a section."""
    if not section_data:
        return "UNKNOWN"
    return section_data.get("as_of_utc") or "UNKNOWN"


def clamp(value, lo=0.05, hi=0.95):
    return max(lo, min(hi, value))


def pr_relevance(pr):
    """Relevance heuristic for a PR option — mechanical, explainable."""
    score = 0.5
    mergeable = pr.get("mergeable")
    if mergeable is True:
        score += 0.2
    elif mergeable is False:
        score -= 0.2
    if pr.get("draft"):
        score -= 0.3
    # Older PRs are more urgent (they've been waiting)
    created = pr.get("created_at", "")
    try:
        age_days = (datetime.now(timezone.utc)
                    - datetime.fromisoformat(created.replace("Z", "+00:00"))).days
        if age_days > 7:
            score += 0.1
    except (ValueError, TypeError):
        pass
    return round(clamp(score), 2)


def open_prs(model):
    """All open PRs from the cache. Empty list if the section is unusable."""
    data, status = section(model, "prs")
    if status != "OK":
        return [], status
    return data.get("prs", []), "OK"


LANE_NAME_BY_ISSUE = {"1713": "alpha", "1714": "beta", "1715": "gamma"}


def lane_states(model):
    """Lane states from the cache.

    Returns ({name: {"state", "issue"}}, status). Keys in the cache may be
    lane names ('alpha') or issue numbers ('1713') — normalize defensively."""
    data, status = section(model, "lanes")
    if status != "OK":
        return {}, status
    lanes = data.get("lanes", {})
    out = {}
    for key, info in lanes.items():
        name = LANE_NAME_BY_ISSUE.get(str(key), key)
        out[name] = {
            "state": info.get("state", "UNKNOWN"),
            "issue": info.get("issue") or key,
            "occupant": info.get("occupant", ""),
        }
    return out, "OK"


def mission_priorities(model):
    """Priorities from the mission section. Empty if unusable."""
    data, status = section(model, "mission")
    if status != "OK":
        return [], status
    prios = data.get("priorities", [])
    return [str(p)[:120] for p in prios if p], "OK"


# ---------------------------------------------------------------------------
# Duplicate detection
# ---------------------------------------------------------------------------

def normalize_title(title):
    """Normalize a title for duplicate comparison."""
    t = (title or "").lower()
    t = re.sub(r"\s+", " ", t)
    t = re.sub(r"^(re:|\[draft\]|draft:|wip:)\s*", "", t)
    return t.strip()


def find_duplicates(options):
    """Collapse options that are the same work wearing different clothes.

    Two PR options are duplicates when they share a head branch, or when
    their normalized titles are identical. Union-find over pairs handles
    the case where A matches B by branch and B matches C by title.
    The older PR (lowest number) stays primary; the rest are marked
    duplicate_of. Returns (deduped, notes)."""
    notes = []
    n = len(options)
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[rb] = ra

    pr_indexes = [i for i, o in enumerate(options) if o["source_type"] == "pr"]
    for a_pos in range(len(pr_indexes)):
        for b_pos in range(a_pos + 1, len(pr_indexes)):
            a, b = pr_indexes[a_pos], pr_indexes[b_pos]
            pra = options[a].get("_pr") or {}
            prb = options[b].get("_pr") or {}
            same_branch = (pra.get("head_branch") and
                           pra.get("head_branch", "").lower()
                           == prb.get("head_branch", "").lower())
            same_title = (normalize_title(options[a]["title"])
                          == normalize_title(options[b]["title"])
                          and normalize_title(options[a]["title"]))
            if same_branch or same_title:
                union(a, b)

    groups = {}
    for i in range(n):
        groups.setdefault(find(i), []).append(i)

    deduped = []
    for members in groups.values():
        if len(members) == 1:
            deduped.append(options[members[0]])
            continue
        group_sorted = sorted(
            members,
            key=lambda i: (options[i].get("_pr") or {}).get("number", 99999),
        )
        primary, dups = group_sorted[0], group_sorted[1:]
        for d in dups:
            notes.append(
                f"Duplicate: {options[d]['source']} "
                f"('{options[d]['title'][:50]}') covers the same work as "
                f"{options[primary]['source']} — kept "
                f"{options[primary]['source']} as primary."
            )
            options[d]["duplicate_of"] = options[primary]["id"]
        primary_opt = dict(options[primary])
        primary_opt["duplicates"] = [options[d]["id"] for d in dups]
        deduped.append(primary_opt)
    return deduped, notes


def strip_internal(options):
    """Remove the _pr internal field before output."""
    for opt in options:
        opt.pop("_pr", None)
    return options


# ---------------------------------------------------------------------------
# Mining per intent type
# ---------------------------------------------------------------------------

def mine_what_next(model, todo_items):
    """what_next: mine the highest-value actions available right now.

    Options: open PRs (merge queue), free lanes (dispatch candidates),
    mission priorities, open grand-TODO items."""
    options = []
    notes = []

    prs, prs_status = open_prs(model)
    if prs_status != "OK":
        notes.append(f"PR options unavailable: PR section is {prs_status}")
    elif not prs:
        notes.append("PR section is OK but has zero open PRs — that is the reality.")
    else:
        for p in prs:
            if p.get("draft"):
                continue
            fresh = option_freshness(section(model, "prs")[0])
            why = ("Open PR on the live tree."
                   + (" Mergeable." if p.get("mergeable") is True else "")
                   + (" Merge status unknown — recheck before acting."
                      if p.get("mergeable") is None else ""))
            options.append(make_option(
                f"pr-{p.get('number')}", "pr", f"PR #{p.get('number')}",
                p.get("title", f"PR #{p.get('number')}"),
                pr_relevance(p), why.strip(),
                [f"https://github.com/SoulSchoolAcademy/NayaPOWER/pull/{p.get('number')}"],
                fresh,
            ))
            options[-1]["_pr"] = p

    lanes, lanes_status = lane_states(model)
    if lanes_status != "OK":
        notes.append(f"lane options unavailable: lane section is {lanes_status}")
    else:
        fresh = option_freshness(section(model, "lanes")[0])
        for name, lane in lanes.items():
            if lane["state"] == "FREE":
                options.append(make_option(
                    f"lane-{name}", "lane", f"lane {name}",
                    f"Dispatch new work on lane {name} (FREE)",
                    0.6, f"Lane {name} is FREE — available for new work.",
                    [f"https://github.com/SoulSchoolAcademy/NayaPOWER/issues/"
                     f"{lane['issue']}"],
                    fresh,
                ))

    prios, mission_status = mission_priorities(model)
    if mission_status != "OK":
        notes.append(f"mission options unavailable: mission section is {mission_status}")
    else:
        fresh = option_freshness(section(model, "mission")[0])
        for i, pr in enumerate(prios):
            options.append(make_option(
                f"mission-{i}", "mission", "mission state #2154",
                pr, 0.55, "Current mission priority from the mission state.",
                ["https://github.com/SoulSchoolAcademy/NayaPOWER/issues/2154"],
                fresh,
            ))

    if todo_items:
        for i, t in enumerate(todo_items[:10]):
            options.append(make_option(
                f"todo-{i}", "todo", f"grand-todo line {t['line']}",
                t["title"], 0.45,
                "Open item in the grand TODO — unblocked work on the list.",
                [t["file"]], "local-file",
            ))

    options.sort(key=lambda o: (o["relevance"] is not None, o["relevance"] or 0),
                 reverse=True)
    return options, notes


def mine_should_merge(model, intent):
    """should_merge: the referenced PR is the primary option; other
    mergeable open PRs are competing candidates to consider."""
    options = []
    notes = []
    refs = (intent.get("references") or {})
    ref_prs = [p for p in (intent.get("grounded_references") or {}).get("prs", [])
               if p.get("found")]

    prs, prs_status = open_prs(model)
    if prs_status != "OK":
        notes.append(f"PR options unavailable: PR section is {prs_status}")
        return options, notes
    by_number = {p.get("number"): p for p in prs}
    fresh = option_freshness(section(model, "prs")[0])

    # Primary: the PR being asked about
    for g in ref_prs:
        n = g.get("number")
        p = by_number.get(n)
        if not p:
            notes.append(f"PR #{n} is grounded by Layer 2 but not in this cache "
                         "snapshot — the world model may be stale.")
            continue
        why = (f"The PR in question. Title: '{p.get('title', '')}'. "
               f"Mergeable: {p.get('mergeable')}. Draft: {bool(p.get('draft'))}.")
        options.append(make_option(
            f"merge-pr-{n}", "pr", f"PR #{n}",
            f"Merge PR #{n}: {p.get('title', '')}",
            clamp(pr_relevance(p) + 0.15), why,
            [f"https://github.com/SoulSchoolAcademy/NayaPOWER/pull/{n}"],
            fresh,
        ))
        options[-1]["_pr"] = p

    # Competing candidates: other open, non-draft, mergeable PRs
    ref_numbers = {g.get("number") for g in ref_prs}
    for p in prs:
        n = p.get("number")
        if n in ref_numbers or p.get("draft"):
            continue
        if p.get("mergeable") is not True:
            continue
        options.append(make_option(
            f"pr-{n}", "pr", f"PR #{n}",
            f"Consider first: merge PR #{n}: {p.get('title', '')}",
            pr_relevance(p),
            "Another mergeable open PR — a competing merge candidate.",
            [f"https://github.com/SoulSchoolAcademy/NayaPOWER/pull/{n}"],
            fresh,
        ))
        options[-1]["_pr"] = p

    if not options and not ref_prs:
        notes.append("No PR references to evaluate and no mergeable open PRs "
                     "in the cache.")
    options.sort(key=lambda o: (o["relevance"] is not None, o["relevance"] or 0),
                 reverse=True)
    return options, notes


def mine_which_option(model, intent):
    """which_option: the referenced, grounded options are the candidates."""
    options = []
    notes = []
    ref_prs = [p for p in (intent.get("grounded_references") or {}).get("prs", [])
               if p.get("found")]

    prs, prs_status = open_prs(model)
    if prs_status != "OK":
        notes.append(f"PR options unavailable: PR section is {prs_status}")
        return options, notes
    by_number = {p.get("number"): p for p in prs}
    fresh = option_freshness(section(model, "prs")[0])

    for g in ref_prs:
        n = g.get("number")
        p = by_number.get(n)
        if not p:
            notes.append(f"PR #{n} was grounded by Layer 2 but is not in this "
                         "cache snapshot — the world model may be stale.")
            continue
        options.append(make_option(
            f"opt-pr-{n}", "pr", f"PR #{n}",
            p.get("title", f"PR #{n}"),
            pr_relevance(p),
            "Candidate named in the question, found in the world model.",
            [f"https://github.com/SoulSchoolAcademy/NayaPOWER/pull/{n}"],
            fresh,
        ))
        options[-1]["_pr"] = p

    quoted = (intent.get("references") or {}).get("quoted_options", [])
    if quoted:
        for i, q in enumerate(quoted):
            options.append(make_option(
                f"opt-quoted-{i}", "user_added",
                "the question text",
                q, None,
                "Named in the question as a text option, not a PR — "
                "user-suggested, NOT found in the world model. Layer 4 must "
                "score it with lower evidence confidence.",
                [], "question-text",
            ))

    if len(options) < 2:
        notes.append("Fewer than two verifiable options — the decision engine "
                     "should ask for more options rather than rank a single one.")
    return options, notes


def mine_what_blocking(model):
    """what_blocking: options are the things to unblock — stuck PRs,
    occupied lanes with in-flight work, mission blockers."""
    options = []
    notes = []

    prs, prs_status = open_prs(model)
    if prs_status != "OK":
        notes.append(f"PR options unavailable: PR section is {prs_status}")
    else:
        fresh = option_freshness(section(model, "prs")[0])
        for p in prs:
            blocked = p.get("mergeable") is False or p.get("draft")
            if not blocked:
                continue
            reason = ("marked NOT mergeable" if p.get("mergeable") is False
                      else "still a draft")
            options.append(make_option(
                f"unblock-pr-{p.get('number')}", "pr", f"PR #{p.get('number')}",
                f"Unblock PR #{p.get('number')}: {p.get('title', '')}",
                0.7, f"This PR is stuck ({reason}).",
                [f"https://github.com/SoulSchoolAcademy/NayaPOWER/pull/{p.get('number')}"],
                fresh,
            ))
            options[-1]["_pr"] = p

    lanes, lanes_status = lane_states(model)
    if lanes_status != "OK":
        notes.append(f"lane options unavailable: lane section is {lanes_status}")
    else:
        fresh = option_freshness(section(model, "lanes")[0])
        for name, lane in lanes.items():
            if lane["state"] == "OCCUPIED":
                why = f"Lane {name} has work in flight"
                if lane.get("occupant"):
                    why += f" ({lane['occupant'][:60]})"
                why += " — check if it's stuck."
                options.append(make_option(
                    f"lane-{name}", "lane", f"lane {name}",
                    f"Check on lane {name} (OCCUPIED)",
                    0.5, why,
                    [f"https://github.com/SoulSchoolAcademy/NayaPOWER/issues/"
                     f"{lane['issue']}"],
                    fresh,
                ))

    if not options:
        notes.append("Nothing verifiably blocked in the cached world model.")
    return options, notes


def no_options_applicable(intent_type):
    """status_check / should_build: the miner returns no options honestly.

    A status question has no options to mine. A build question's options
    (build vs reuse) require a code inventory the world model doesn't have —
    saying "reuse X" without evidence would be inventing."""
    if intent_type == "status_check":
        note = ("Status questions have no options to mine — the answer is "
                "the world model itself.")
    else:
        note = ("Build decisions need to know what already exists; the world "
                "model has no code-inventory section, so no reuse options can "
                "be verified. Refusing to invent them.")
    return [], [note]


# ---------------------------------------------------------------------------
# Main mining pipeline
# ---------------------------------------------------------------------------

MINERS = {
    "what_next": lambda model, intent, todos: mine_what_next(model, todos),
    "should_merge": lambda model, intent, todos: mine_should_merge(model, intent),
    "which_option": lambda model, intent, todos: mine_which_option(model, intent),
    "what_blocking": lambda model, intent, todos: mine_what_blocking(model),
}


def mine_options(intent, user_options=None):
    """Full pipeline: parsed intent + world model → mined options.

    Returns a result dict with options, notes, warnings, and exit_hint.
    Never throws on bad input — returns exit_hint 2 instead."""
    intent = intent or {}
    user_options = user_options or []

    # Guard: Layer 2 didn't produce a usable intent
    if not intent.get("ok", True) or not intent.get("intent_type"):
        return {
            "ok": False,
            "exit_hint": 2,
            "options": [],
            "notes": ["No usable intent from Layer 2 — clarify before mining."],
            "warnings": [],
        }

    # Guard: no world model
    model, warnings = load_world_model()
    if model is None:
        return {
            "ok": False,
            "exit_hint": 2,
            "options": [],
            "notes": ["No world model cache — cannot mine from reality. "
                      "Run tools/world_model.py snapshot first."],
            "warnings": warnings,
        }

    intent_type = intent["intent_type"]
    todo_items, todo_warnings = load_grand_todo()
    warnings.extend(todo_warnings)

    # Unknown intent type: Layer 2 produced something we can't act on —
    # that's "cannot mine", not "no options applicable".
    if intent_type not in MINERS and intent_type not in ("status_check", "should_build"):
        return {
            "ok": False,
            "exit_hint": 2,
            "options": [],
            "notes": [f"Unknown intent type '{intent_type}' — no mining rules. "
                      "Refusing to guess."],
            "warnings": warnings,
        }

    miner = MINERS.get(intent_type)
    if miner is None:
        options, notes = no_options_applicable(intent_type)
    else:
        options, notes = miner(model, intent, todo_items)

    # Duplicate detection
    deduped, dup_notes = find_duplicates(options)
    notes.extend(dup_notes)

    # User-added options — flagged, never confused with mined ones
    added = 0
    for i, desc in enumerate(user_options):
        desc = (desc or "").strip()
        if not desc:
            continue
        deduped.append(make_option(
            f"user-{i}", "user_added", "user suggestion",
            desc[:120], None,
            "Suggested by the user ('what about X?'), NOT found in the world "
            "model. Layer 4 must score it with lower evidence confidence.",
            [], "user-supplied",
        ))
        added += 1
    if added:
        notes.append(f"{added} user-added option(s) appended — "
                     "marked user_added, unscored.")

    # Freshness flag: tip section drives overall freshness
    _, tip_status = section(model, "tip")
    if tip_status != "OK":
        warnings.append(f"live tip is {tip_status} — options may be stale")

    strip_internal(deduped)

    return {
        "ok": True,
        "exit_hint": 0,
        "intent_type": intent_type,
        "objective": intent.get("objective", ""),
        "options": deduped,
        "option_count": len(deduped),
        "notes": notes,
        "warnings": warnings,
        "mined_utc": datetime.now(timezone.utc).isoformat(),
    }


def plain_words(result):
    """Render mined options in plain words for humans."""
    if not result.get("ok"):
        lines = ["Couldn't mine options:"]
        for n in result.get("notes", []):
            lines.append(f"  • {n}")
        return "\n".join(lines)
    options = result.get("options", [])
    if not options:
        lines = ["No options could be mined from reality."]
        for n in result.get("notes", []):
            lines.append(f"  • {n}")
        return "\n".join(lines)
    lines = [f"Mined {len(options)} option(s) from the world model:"]
    for o in options:
        rel = (f"{o['relevance']:.2f}" if o["relevance"] is not None
               else "unscored")
        lines.append(f"  [{o['id']}] {o['title']}")
        lines.append(f"      source: {o['source']} | relevance: {rel} | "
                     f"freshness: {o['freshness']}")
        lines.append(f"      why: {o['why']}")
        if o.get("duplicates"):
            lines.append(f"      duplicates of this: {', '.join(o['duplicates'])}")
        if o.get("duplicate_of"):
            lines.append(f"      duplicate of: {o['duplicate_of']}")
    for n in result.get("notes", []):
        lines.append(f"  • {n}")
    if result.get("warnings"):
        lines.append("Warnings:")
        for w in result["warnings"]:
            lines.append(f"  ⚠ {w}")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def cmd_mine(args):
    if args.stdin:
        raw = sys.stdin.read()
    elif args.intent:
        raw = " ".join(args.intent)
    else:
        print("usage: option_miner.py mine --intent '<intent JSON>' "
              "(or --stdin)", file=sys.stderr)
        sys.exit(1)
    try:
        intent = json.loads(raw)
    except (json.JSONDecodeError, TypeError) as e:
        print(json.dumps({
            "ok": False, "exit_hint": 2, "options": [],
            "notes": [f"intent JSON unreadable: {e}"], "warnings": [],
        }, indent=2))
        sys.exit(2)
    result = mine_options(intent, user_options=args.add_option or [])
    if args.plain:
        print(plain_words(result))
    else:
        print(json.dumps(result, indent=2))
    sys.exit(result.get("exit_hint", 0))


def main():
    import argparse
    ap = argparse.ArgumentParser(
        description="Option Miner — Layer 3 of the Ultimate Decision Machine.")
    sub = ap.add_subparsers(dest="cmd")

    p_mine = sub.add_parser("mine", help="Mine options from the world model")
    p_mine.add_argument("intent", nargs="*",
                        help="Layer-2 intent JSON (as one string)")
    p_mine.add_argument("--stdin", action="store_true",
                        help="Read intent JSON from stdin")
    p_mine.add_argument("--add-option", action="append", default=[],
                        help="User-added 'what about X?' option (repeatable)")
    p_mine.add_argument("--plain", action="store_true",
                        help="Plain-words output instead of JSON")
    p_mine.set_defaults(func=cmd_mine)

    args = ap.parse_args()
    if not getattr(args, "cmd", None):
        ap.print_help()
        sys.exit(1)
    args.func(args)


if __name__ == "__main__":
    main()

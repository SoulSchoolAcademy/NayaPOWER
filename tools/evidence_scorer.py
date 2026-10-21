#!/usr/bin/env python3
"""
Evidence Scorer — Layer 4 of the Ultimate Decision Machine.

Given a structured intent (Layer 2) + mined options (Layer 3) + the
world-model cache (Layer 1), score every option on five evidence-derived
dimensions. EVERY score carries {value, evidence, confidence}.
A score without evidence is a defect.

The five dimensions (Shawn's blueprint):
  1. MISSION VALUE (0-1): does this close a real gap?
  2. EVIDENCE STRENGTH (0-1): how proven is this option? (mechanical)
  3. RISK (0-1, higher = riskier): irreversible? protected gates?
  4. COST (0-1, higher = costlier): known and bounded — never guessed.
  5. URGENCY (0-1): dependency-graph position.

HARD GATES run before any scoring: a protected-gate action is flagged
REQUIRES_SHAWN and is never ranked as recommended. Gates are walls,
not scores.

UNCERTAINTY (Shawn's principle): every dimension carries confidence 0-1
derived from evidence freshness. Stale or missing evidence → the dimension
is marked UNKNOWN, never guessed. The total carries total_confidence.

Rules:
  - Zero network calls. Local cache only.
  - Never score from imagination. Exit 2 when inputs are missing/unknown.

Usage:
  python3 tools/evidence_scorer.py score --intent '<intent JSON>' \
      --options '<options JSON>'
  python3 tools/evidence_scorer.py score --stdin < scoring_input.json
  python3 tools/evidence_scorer.py score --intent '<json>' \
      --options '<json>' --plain

Exit codes:
  0 — scored (possibly with UNKNOWN dimensions and honest notes)
  2 — cannot score: no world model, intent unusable, or options missing
"""

import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

# ---------------------------------------------------------------------------
# Weights — combination of the five dimensions.
#
# LAYER 6 HOOK: the learning loop will tune these weights from
# decided/predicted/actual receipts. Do NOT hard-code new weight logic
# elsewhere — every combination goes through WEIGHTS so the learner
# has one knob to turn per dimension.
# ---------------------------------------------------------------------------

WEIGHTS = {
    "mission_value": 0.35,    # closes a real gap — the point of the machine
    "evidence": 0.25,         # proven beats promised
    "risk": -0.20,            # subtracted: higher risk lowers the total
    "cost": -0.10,            # subtracted: higher cost lowers the total
    "urgency": 0.10,          # blocks others → do it sooner
}

# Layer 6 will read this version to know which weight schema it tuned.
WEIGHTS_SCHEMA_VERSION = 1

WORLD_MODEL_PATH = Path(os.path.expanduser("~/.naya/world-model.json"))

# Freshness TTLs (seconds) per world-model section — mirrors Layer 1.
SECTION_TTL = {
    "tip": 300,
    "prs": 600,
    "lanes": 300,
    "ledger": 1800,
    "mission": 1800,
    "laws": 86400,
}

# Protected gates — Shawn's explicit-word list. A match is a WALL, not a score.
#
# HEURISTIC BOUNDARY (honest, by design): these are keyword tripwires, not
# a completeness proof. Novel phrasings ("wipe the table", "rotate the
# keys", "pay the vendor") can miss the wall — a keyword list can never
# enumerate every way a human can describe a protected action. The wall
# is layered with: (1) these patterns fail closed on what they know,
# (2) prohibition-scoping keeps law-listings from misfiring, (3) misses
# feed the Layer 6 learning loop, which proposes new patterns from
# decided/predicted/actual receipts. Never claim the wall is complete.
PROTECTED_PATTERNS = [
    r"production\s+deploy",
    r"\bdeploy\b.{0,20}\bproduction\b",
    r"database\s+write",
    r"write.{0,20}\bdatabase\b",
    r"\bdb\s+write\b",
    # fail-closed on real writes, but don't trip on docs ABOUT the db
    # ("write the db schema docs" is documentation, not a database write)
    r"write.{0,20}\bdb\b(?!\s+(schema\s+)?docs?\b)",
    r"credential",
    r"\bmoney\b",
    r"payment",
    r"destruct",
    r"\bnuke\b",
    # rm -rf variants (rm -rf, rm -fr, rm -rfv): recursive force delete —
    # destructive by construction. Law-listings ("no rm -rf") stay clean
    # via prohibition scoping; plain "rm -r" (no force flag) is out of scope.
    r"\brm\s+-(?=[a-z]*r)(?=[a-z]*f)[a-z]+\b",
    # kill aimed at production/data targets ("kill the production database",
    # "kill the cluster"). Plain "kill the process" stays out of scope.
    r"\bkill\b.{0,25}\b(production|database|cluster|db)\b",
    r"delete\s+(?:(?:the|a|an|our|their|this|that)\s+)?(branch|repo|database)",
    r"drop\s+(?:(?:the|a|an|our|their|this|that)\s+)?(production\s+)?(database|table|repo|branch)",
    r"ship.{0,15}\bprod(uction)?\b",
    r"\bpush\b.{0,15}\bprod(uction)?\b",
    r"constitutional",
    r"ratif",
    r"force.?push",
]


# ---------------------------------------------------------------------------
# World model reading (local cache only — no network)
# ---------------------------------------------------------------------------

def load_world_model(path=None):
    """Load the world model from local cache. Returns (model, warnings)."""
    p = Path(path) if path else WORLD_MODEL_PATH
    if not p.exists():
        return None, ["world model not found — run tools/world_model.py snapshot first"]
    try:
        model = json.loads(p.read_text())
    except (json.JSONDecodeError, OSError) as e:
        return None, [f"world model unreadable: {e}"]
    return model, []


def section(model, name):
    """Get a section dict if usable. Returns (data, status)."""
    sections = (model or {}).get("sections", {})
    s = sections.get(name) or {}
    status = s.get("status", "UNKNOWN")
    if status == "OK":
        return s, "OK"
    return None, status


def now_ts():
    return datetime.now(timezone.utc).timestamp()


def freshness_confidence(section_data, name):
    """Confidence 0-1 from evidence freshness. Never invents freshness."""
    if not section_data:
        return 0.2, "no cached evidence for this dimension"
    as_of = section_data.get("as_of_ts")
    if as_of is None:
        # Cache has data but no timestamp — usable, but trust it less.
        return 0.5, "cached evidence has no timestamp"
    age = now_ts() - as_of
    ttl = SECTION_TTL.get(name, 600)
    if age <= ttl:
        return 1.0, f"fresh (age {int(age)}s <= ttl {ttl}s)"
    if age <= 3 * ttl:
        return 0.6, f"aging (age {int(age)}s, ttl {ttl}s)"
    return 0.3, f"stale (age {int(age)}s >> ttl {ttl}s)"


def clamp01(v):
    return max(0.0, min(1.0, v))


def dim(value, evidence, confidence):
    """One scored dimension. value=None means UNKNOWN — never a guess."""
    return {
        "value": None if value is None else round(clamp01(value), 3),
        "evidence": list(evidence),
        "confidence": round(clamp01(confidence), 3),
    }


# ---------------------------------------------------------------------------
# Hard gates — walls, not scores
# ---------------------------------------------------------------------------

def gate_hit(text):
    """Return the first protected-gate pattern matched outside prohibition
    language, or None.

    A mention under prohibition ('no X', 'never X' phrasings) is the law
    being stated, not the action being asked for — the same scoping used
    for intent constraints. A genuine ask still trips the wall.
    """
    t = str(text or "").lower()
    for pat in PROTECTED_PATTERNS:
        for m in re.finditer(pat, t):
            if not _under_prohibition(t, m.start()):
                return pat
    return None


# Words that turn a gate-pattern mention into a prohibition (the text is
# listing what is FORBIDDEN, not requesting it). Layer 2's derived
# constraints do exactly this: "Protected gates hold: no production
# deploys, ..." — that is the opposite of asking for a deploy.
PROHIBITION_MARKERS = (
    "no ", "not ", "never ", "without ", "avoid ", "protected",
    "forbidden", "prohibit", "must not", "cannot", "don't", "do not",
)
# "hold" is matched as a standalone word only: a substring match fires
# inside "threshold" and would silently exempt genuine gate mentions
# ("above the error threshold, drop the production database").
PROHIBITION_WORD_PATTERNS = (r"\bhold\b",)


def _under_prohibition(text, match_start):
    """True if prohibition language governs the match position.

    Scoped to the match's own sentence: a leading "no" governs its list
    ("no production deploys, DB writes, credential moves") but does not
    silence a genuine request in the next sentence ("Deploy to production
    needs Shawn's word.").
    """
    lowered = str(text or "").lower()
    sent_start = max(lowered.rfind(".", 0, match_start),
                     lowered.rfind(";", 0, match_start)) + 1
    pre = lowered[sent_start:match_start]
    return (any(marker in pre for marker in PROHIBITION_MARKERS)
            or any(re.search(pat, pre) for pat in PROHIBITION_WORD_PATTERNS))


def _constraint_requests_gate(text, pat):
    """True if a gate pattern in a CONSTRAINT text is a real request.

    Constraints are guardrails, not action descriptions: a pattern that
    appears under prohibition language ("no production deploys") is the
    law being stated, not the action being asked for. Only an
    un-prohibited mention (e.g. "requires production deploy",
    "needs Shawn's word: production deploy") counts as a gate hit.
    """
    t = str(text or "").lower()
    for m in re.finditer(pat, t):
        if not _under_prohibition(t, m.start()):
            return True
    return False


def _constraint_names_shawns_word(text):
    """Explicit 'needs Shawn's word' marker — but not under prohibition
    language ('without Shawn's word' is a guardrail, not a request)."""
    t = str(text or "").lower()
    idx = t.find("shawn")
    if idx == -1 or "word" not in t:
        return False
    return not _under_prohibition(t, idx)


def check_gates(intent, option):
    """Hard gates run before scoring. Returns (gated, reasons)."""
    reasons = []
    # Action-describing fields: a protected pattern here IS the action.
    for hay in (intent.get("objective", ""),
                option.get("title", ""),
                option.get("why", "")):
        pat = gate_hit(hay)
        if pat:
            reasons.append(f"protected gate pattern '{pat}' in action: "
                           f"{hay[:80]}")
    # Constraints are guardrails: only un-prohibited mentions count.
    constraints = [str(c) for c in (intent.get("constraints", []) or [])
                   if c is not None]
    for c in constraints:
        for pat in PROTECTED_PATTERNS:
            if _constraint_requests_gate(c, pat):
                reasons.append(f"protected gate pattern '{pat}' requested "
                               f"in constraint: {c[:80]}")
                break
    ctext = " ".join(constraints)
    if _constraint_names_shawns_word(ctext):
        reasons.append("intent constraints name Shawn's explicit word")
    return (len(reasons) > 0), reasons


# ---------------------------------------------------------------------------
# Option grounding — re-derive evidence from the cache, never trust blindly
# ---------------------------------------------------------------------------

def pr_number_from_option(option):
    """Extract PR number from an option's source field ('PR #2410')."""
    m = re.search(r"#(\d+)", str(option.get("source") or ""))
    if m:
        return int(m.group(1))
    return None


def ground_option(option, model):
    """Re-ground an option against the world-model cache.

    Returns (pr_dict_or_None, prs_section, prs_confidence, conf_note).
    Options that cannot be grounded keep their own stated fields but
    with low confidence — the scorer never invents missing evidence.
    """
    prs_data, prs_status = section(model, "prs")
    if prs_status != "OK" or not prs_data:
        return None, None, 0.2, f"prs section {prs_status} — cannot re-ground"
    conf, note = freshness_confidence(prs_data, "prs")
    if option.get("source_type") != "pr":
        # Only PR options are re-grounded against the PR section. A lane or
        # mission source may coincidentally contain "#<digits>" (e.g. the
        # mission-state issue number) — matching that against PRs would be
        # a false grounding.
        return None, prs_data, conf, note
    n = pr_number_from_option(option)
    if n is None:
        return None, prs_data, conf, note
    for p in prs_data.get("prs", []):
        if p.get("number") == n:
            return p, prs_data, conf, note
    return None, prs_data, conf, (
        f"PR #{n} not in cache snapshot — the world model may be stale; "
        f"section freshness: {note}")


# ---------------------------------------------------------------------------
# The five dimensions — every value derived from evidence
# ---------------------------------------------------------------------------

def score_mission_value(option, intent, pr, conf, conf_note):
    """Does this close a real gap?"""
    ev = []
    st = option.get("source_type", "")
    if st == "user_added":
        ev.append("user-added suggestion: not grounded in the world model — "
                  "mission value cannot be verified")
        return dim(0.3, ev, 0.25)
    if st == "todo":
        ev.append(f"open TODO item from {option.get('source', '')}")
        return dim(0.8, ev, conf)
    if st == "lane":
        ev.append(f"lane state from world model ({option.get('source', '')})")
        return dim(0.5, ev, conf)
    if st == "mission":
        ev.append("world-model mission priority")
        return dim(0.7, ev, conf)
    if st == "pr" and pr is not None:
        if pr.get("draft"):
            ev.append(f"PR #{pr.get('number')} is a DRAFT — not ready to close anything")
            return dim(0.35, ev, conf)
        if pr.get("mergeable") is True:
            ev.append(f"PR #{pr.get('number')} mergeable, non-draft — "
                      "can land and close its gap")
            v = 0.7
        elif pr.get("mergeable") is False:
            ev.append(f"PR #{pr.get('number')} not mergeable — blocked from closing its gap")
            v = 0.25
        else:
            ev.append(f"PR #{pr.get('number')} mergeability UNKNOWN — value uncertain")
            return dim(None, ev, 0.3)
        why = (option.get("why", "") + " " + option.get("title", "")).lower()
        if any(w in why for w in ("red", "breakage", "fix", "close", "gap")):
            ev.append("option text indicates it closes a known gap/RED")
            v = min(1.0, v + 0.15)
        return dim(v, ev, conf)
    ev.append(f"source_type '{st}' with no grounding in this cache — {conf_note}")
    return dim(None, ev, 0.3)


def score_evidence(option, pr, conf, conf_note):
    """How proven is this option? Purely mechanical derivation."""
    ev = []
    st = option.get("source_type", "")
    if st == "user_added":
        ev.append("user-added: zero mechanical proof — no CI, no IV, no tests")
        return dim(0.1, ev, 0.2)
    if st in ("todo", "lane", "mission"):
        ev.append(f"{st} option: existence proven by world-model cache, "
                  "outcome unproven")
        return dim(0.5, ev, conf)
    if st == "pr" and pr is not None:
        v = 0.2
        if pr.get("mergeable") is True:
            v += 0.3
            ev.append("mergeable=true (mechanical)")
        elif pr.get("mergeable") is None:
            ev.append("mergeable UNKNOWN — GitHub had not computed it")
        if not pr.get("draft"):
            v += 0.2
            ev.append("not a draft")
        else:
            ev.append("draft PR — proof incomplete by definition")
        iv = option.get("iv_score")
        if isinstance(iv, (int, float)):
            if iv >= 9.5:
                v += 0.3
                ev.append(f"independent validation {iv} >= 9.5 (mechanical)")
            else:
                ev.append(f"independent validation {iv} < 9.5 — not proven")
        else:
            ev.append("no independent-validation score on the option")
        if option.get("tests_green") is True:
            v += 0.15
            ev.append("tests reported green on the option")
        elif option.get("tests_green") is False:
            v -= 0.2
            ev.append("tests reported RED on the option")
        else:
            ev.append("no test evidence on the option")
        # Confidence follows the cache freshness, degraded when key
        # facts are unknown.
        c = conf
        if pr.get("mergeable") is None:
            c = min(c, 0.5)
            ev.append("confidence capped: mergeability unknown")
        return dim(v, ev, c)
    ev.append(f"PR #{pr_number_from_option(option)} not in cache — {conf_note}")
    return dim(None, ev, 0.3)


def score_risk(option, intent, pr, conf):
    """How risky? Higher = riskier. Irreversibility and gates dominate."""
    ev = []
    v = 0.2
    rev = intent.get("reversibility", "medium")
    if rev == "low":
        v += 0.4
        ev.append("intent reversibility=low — hard to undo")
    elif rev == "medium":
        v += 0.2
        ev.append("intent reversibility=medium")
    else:
        ev.append("intent reversibility=high — easy to undo")
    if intent.get("decision_weight") == "foundational":
        v += 0.15
        ev.append("foundational decision weight (Wisdom Spending)")
    files = option.get("files_changed")
    if isinstance(files, (int, float)):
        if files > 20:
            v += 0.2
            ev.append(f"{int(files)} files changed — large blast radius")
        elif files > 5:
            v += 0.1
            ev.append(f"{int(files)} files changed")
        else:
            ev.append(f"{int(files)} files changed — small blast radius")
    else:
        ev.append("files_changed unknown — no blast-radius evidence")
    if pr is not None and pr.get("mergeable") is False:
        v += 0.1
        ev.append("PR not mergeable — landing it risks conflicts")
    return dim(v, ev, conf)


def score_cost(option, conf):
    """Known and bounded cost. Unknown cost → UNKNOWN, never a guess."""
    ev = []
    files = option.get("files_changed")
    tests = option.get("test_count")
    parts = []
    if isinstance(files, (int, float)):
        parts.append(min(1.0, files / 20.0))
        ev.append(f"{int(files)} files changed")
    if isinstance(tests, (int, float)):
        parts.append(min(1.0, tests / 200.0))
        ev.append(f"{int(tests)} tests in scope")
    if option.get("has_conflicts"):
        parts.append(0.5)
        ev.append("merge conflicts noted — rework cost")
    if not parts:
        ev.append("no cost evidence on the option — refusing to guess a number")
        return dim(None, ev, 0.3)
    v = sum(parts) / len(parts)
    return dim(v, ev, conf)


def score_urgency(option, intent, model, pr, conf):
    """Dependency-graph position. Mechanical where data exists."""
    ev = []
    v = 0.2
    # Sequencing data in the cache: does anything list this PR as a blocker?
    mission_data, m_status = section(model, "mission")
    blocked_by_me = []
    n = pr_number_from_option(option)
    if m_status == "OK" and mission_data and n:
        seq = mission_data.get("sequencing") or []
        for entry in seq:
            after = entry.get("after") or []
            nums = re.findall(r"#(\d+)", " ".join(str(x) for x in after))
            if str(n) in nums or n in after:
                blocked_by_me.append(entry.get("name", "?"))
    if blocked_by_me:
        v += 0.4
        ev.append(f"blocks: {', '.join(blocked_by_me[:3])} (sequencing data)")
    else:
        ev.append("no sequencing data shows this blocking others")
    # Age: a PR waiting a long time is more urgent — mechanical from cache.
    if pr and pr.get("created_at"):
        try:
            created = datetime.fromisoformat(
                pr["created_at"].replace("Z", "+00:00"))
            age_days = (datetime.now(timezone.utc) - created).days
            ev.append(f"PR age {age_days} days (from cache)")
            if age_days > 14:
                v += 0.2
            elif age_days > 7:
                v += 0.1
        except (ValueError, TypeError):
            ev.append("PR created_at unparseable — age unknown")
    else:
        ev.append("no age evidence")
    if intent.get("intent_type") == "what_blocking":
        v += 0.1
        ev.append("intent is about blockers — urgency weighs more")
    return dim(v, ev, conf)


# ---------------------------------------------------------------------------
# Combination
# ---------------------------------------------------------------------------

def combine(dimensions):
    """Weighted total. UNKNOWN dimensions are excluded; total degrades
    honestly instead of pretending. Returns (total, total_confidence)."""
    total = 0.0
    wsum = 0.0
    conf_num = 0.0
    known = 0
    for name, d in dimensions.items():
        w = WEIGHTS[name]
        if d["value"] is None:
            continue
        total += w * d["value"]
        wsum += abs(w)
        conf_num += abs(w) * d["confidence"]
        known += 1
    if known == 0:
        return None, 0.0
    # Renormalize over known dimensions so a missing dimension doesn't
    # silently zero the total — but flag it.
    total = total / wsum if wsum else 0.0
    return round(total, 3), round(conf_num / wsum if wsum else 0.0, 3)


# ---------------------------------------------------------------------------
# Main scoring pipeline
# ---------------------------------------------------------------------------

def score_options(intent, options, model):
    """Score every option. Never throws on bad input — returns exit_hint."""
    intent = intent or {}
    options = options or []

    if not intent.get("ok", True) or not intent.get("intent_type"):
        return {
            "ok": False, "exit_hint": 2, "options": [],
            "notes": ["No usable intent from Layer 2 — clarify before scoring."],
            "warnings": [],
        }
    if not options:
        return {
            "ok": False, "exit_hint": 2, "options": [],
            "notes": ["No options from Layer 3 — nothing to score."],
            "warnings": [],
        }
    if model is None:
        return {
            "ok": False, "exit_hint": 2, "options": [],
            "notes": ["No world model cache — cannot derive evidence. "
                      "Run tools/world_model.py snapshot first."],
            "warnings": [],
        }

    warnings = []
    _, tip_status = section(model, "tip")
    if tip_status != "OK":
        warnings.append(f"live tip is {tip_status} — scores may be stale")

    scored = []
    gated_any = False
    for opt in options:
        gated, gate_reasons = check_gates(intent, opt)
        if gated:
            gated_any = True
        pr, prs_data, pr_conf, pr_note = ground_option(opt, model)
        # Freshness confidence for the option follows the prs section;
        # user-added options have only the user's word.
        if opt.get("source_type") == "user_added":
            base_conf, base_note = 0.25, "user-supplied, ungrounded"
        else:
            base_conf, base_note = pr_conf, pr_note

        dimensions = {
            "mission_value": score_mission_value(opt, intent, pr, base_conf, base_note),
            "evidence": score_evidence(opt, pr, base_conf, base_note),
            "risk": score_risk(opt, intent, pr, base_conf),
            "cost": score_cost(opt, base_conf),
            "urgency": score_urgency(opt, intent, model, pr, base_conf),
        }
        total, total_conf = combine(dimensions)
        scored.append({
            "id": opt.get("id"),
            "source": opt.get("source"),
            "source_type": opt.get("source_type"),
            "title": opt.get("title"),
            "gated": gated,
            "gate_reasons": gate_reasons,
            "gate_verdict": "REQUIRES_SHAWN" if gated else "clear",
            "dimensions": dimensions,
            "total": total,
            "total_confidence": total_conf,
            "unknown_dimensions": [k for k, d in dimensions.items()
                                   if d["value"] is None],
        })

    # F5: total_confidence renormalizes over known dimensions only, so a
    # 1.0 can hide UNKNOWN dimensions. Name them explicitly in the
    # top-level notes — Layer 5 (and humans) must see the gap, not
    # just the confidence number.
    unknown_notes = []
    for s in scored:
        if s["unknown_dimensions"]:
            unknown_notes.append(
                f"Option {s['id']}: UNKNOWN dimensions "
                f"[{', '.join(s['unknown_dimensions'])}] — total "
                "confidence renormalized over known dimensions only; "
                "treat as partial evidence.")
    # Ranking: gated and UNKNOWN-total options never win. Rank is
    # positional (not id lookup) so duplicate/None ids can't collide.
    rankable = [s for s in scored if not s["gated"] and s["total"] is not None]
    rankable.sort(key=lambda s: (s["total"], s["total_confidence"]), reverse=True)
    rank_by_pos = {id(s): i + 1 for i, s in enumerate(rankable)}
    for s in scored:
        s["rank"] = rank_by_pos.get(id(s))

    recommendation = None
    notes = []
    if rankable:
        best = rankable[0]
        recommendation = {
            "option_id": best["id"],
            "title": best["title"],
            "total": best["total"],
            "total_confidence": best["total_confidence"],
        }
        if best["total_confidence"] < 0.5:
            notes.append("Top recommendation has LOW confidence — "
                         "treat as a suggestion, not a verdict.")
    else:
        notes.append("No rankable option: all gated or UNKNOWN. "
                     "The machine refuses to recommend — ask Shawn or "
                     "refresh the world model.")
    if gated_any:
        notes.append("One or more options hit a HARD GATE (protected action) — "
                     "flagged REQUIRES_SHAWN, excluded from ranking.")
    notes.extend(unknown_notes)

    return {
        "ok": True,
        "exit_hint": 0,
        "intent_type": intent.get("intent_type"),
        "objective": intent.get("objective", ""),
        "weights": dict(WEIGHTS),
        "weights_schema_version": WEIGHTS_SCHEMA_VERSION,
        "options": scored,
        "recommendation": recommendation,
        "notes": notes,
        "warnings": warnings,
        "scored_utc": datetime.now(timezone.utc).isoformat(),
    }


def plain_words(result):
    """Render scores in plain words for humans."""
    if not result.get("ok"):
        lines = ["Couldn't score:"]
        for n in result.get("notes", []):
            lines.append(f"  • {n}")
        return "\n".join(lines)
    lines = []
    rec = result.get("recommendation")
    if rec:
        lines.append(
            f"Recommendation: {rec['title']} "
            f"(score {rec['total']}, confidence {rec['total_confidence']})")
    else:
        lines.append("No recommendation — nothing rankable. See notes.")
    for o in result["options"]:
        flag = " [REQUIRES_SHAWN]" if o["gated"] else ""
        tot = o["total"] if o["total"] is not None else "UNKNOWN"
        lines.append(f"  [{o['id']}] {o['title']}{flag}")
        lines.append(f"      total: {tot} | confidence: {o['total_confidence']} | "
                     f"rank: {o['rank']}")
        for name, d in o["dimensions"].items():
            v = d["value"] if d["value"] is not None else "UNKNOWN"
            lines.append(f"      {name}: {v} (conf {d['confidence']})")
            for e in d["evidence"]:
                lines.append(f"        - {e}")
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

def cmd_score(args):
    model_path = os.environ.get("NAYA_WORLD_MODEL") or None
    if args.stdin:
        raw = sys.stdin.read()
    elif args.intent and args.options:
        raw = json.dumps({"intent": json.loads(" ".join(args.intent)),
                          "options": json.loads(" ".join(args.options))})
    else:
        print("usage: evidence_scorer.py score --intent '<intent JSON>' "
              "--options '<options JSON>' (or --stdin)", file=sys.stderr)
        sys.exit(1)
    try:
        payload = json.loads(raw)
    except (json.JSONDecodeError, TypeError) as e:
        print(json.dumps({"ok": False, "exit_hint": 2, "options": [],
                          "notes": [f"input JSON unreadable: {e}"],
                          "warnings": []}, indent=2))
        sys.exit(2)
    intent = payload.get("intent", {})
    options = payload.get("options", [])
    model, warnings = load_world_model(model_path)
    result = score_options(intent, options, model)
    result["warnings"] = warnings + result.get("warnings", [])
    if args.plain:
        print(plain_words(result))
    else:
        print(json.dumps(result, indent=2))
    sys.exit(result.get("exit_hint", 0))


def main():
    import argparse
    ap = argparse.ArgumentParser(
        description="Evidence Scorer — Layer 4 of the Ultimate Decision Machine.")
    sub = ap.add_subparsers(dest="cmd")

    p = sub.add_parser("score", help="Score options from intent + options")
    p.add_argument("intent", nargs="*",
                   help="Layer-2 intent JSON (as one string)")
    p.add_argument("--options", nargs="*", default=None,
                   help="Layer-3 options JSON (as one string)")
    p.add_argument("--stdin", action="store_true",
                   help="Read {intent, options} JSON from stdin")
    p.add_argument("--plain", action="store_true",
                   help="Plain-words output instead of JSON")
    p.set_defaults(func=cmd_score)

    args = ap.parse_args()
    if not getattr(args, "cmd", None):
        ap.print_help()
        sys.exit(1)
    args.func(args)


if __name__ == "__main__":
    main()

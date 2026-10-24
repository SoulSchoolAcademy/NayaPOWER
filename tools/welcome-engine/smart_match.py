#!/usr/bin/env python3
"""
Smart Match — current engine (v1.3). Naya Power, SET B (engine end), 2026-10-24.
History: v1 (literal tokens) -> v1.1 (concept layer) -> v1.2 (two-tier
family scoring) -> v1.3 (word tier inside the raw score — citizen free
vocabulary: "urban gardening" must see "gardening"; found by the Welcome
Engine's first end-to-end demo, Loop 2). Scorecards in SCORECARD.md.

WHAT A MATCH % MEANS (published semantics):
  The weighted share of DECLARED signals that align between two profiles.
  Not a probability, not a judgment of worth. Reasons always ride along;
  a % without reasons is a bug.

FORMULA (v1 weights — Lock Packet, Issue #3029):
  topics 40% · goals 25% · offers<->needs 20% · desired connections 15%
  Topics and goals are scored TWO-TIER: 50% raw-term overlap + 50% concept
  coverage, because a shared concept is a FAMILY alignment and must not be
  diluted by vocabulary size (the v1.1 dilution flaw).
  A suggestion surfaces only on >= 2 independent signals.
  Value adjusts RANK only ((0.9 + 0.1v) when a verified value record exists),
  never the % — unknown value is neutral.
"""
import json

WEIGHTS = {"topics": 0.40, "goals": 0.25, "offers_needs": 0.20, "wants": 0.15}

TAXONOMY = {
    "MAKING":    {"building", "creation", "templates", "apps", "step 7", "app creation"},
    "SHIPPING":  {"execution", "delivery", "ship", "waves", "build loop"},
    "PROVING":   {"testing", "validation", "quality", "quality control", "evidence", "proof", "verification", "audit"},
    "CONNECTING": {"integration", "systems", "network", "coordination", "the platform"},
    "SPEAKING":  {"voice", "speech", "audio", "streaming", "synthesis", "ear test"},
    "TALKING":   {"mail", "messaging", "communication", "conversation", "questions", "answers", "listening", "scheduling"},
    "THINKING":  {"distillation", "essence", "reflection", "learning", "analysis", "critical thinking", "root cause", "derivation", "project intelligence"},
    "CLEARING":  {"blockers", "problem solving", "conflict resolution", "risk", "risk review", "reliability", "unblocking"},
    "GUIDING":   {"strategy", "project leadership", "orientation", "home", "long-term strategy", "design"},
    "DECIDING":  {"performance rulings", "governance", "decisions"},
    "PUBLISHING": {"smart notes", "feed", "publishing", "flow", "publishing path", "notes"},
    "PEOPLE":    {"citizens", "usage", "readers", "material"},
}
TERM2CONCEPTS = {}
for _c, _terms in TAXONOMY.items():
    for _t in _terms:
        TERM2CONCEPTS.setdefault(_t, set()).add(_c)


def concepts_of(terms):
    out = set()
    for t in terms or []:
        out |= TERM2CONCEPTS.get(t, set())
    return out


def _coeff(A, B):
    if not A or not B:
        return 0.0, []
    shared = sorted(A & B)
    return len(shared) / min(len(A), len(B)), shared


def _words(terms):
    out = set()
    for t in terms or []:
        out |= {w for w in t.lower().replace(",", " ").split() if len(w) > 2}
    return out


def family_score(a_terms, b_terms):
    """Topics/goals scoring, three ingredients:
    - phrase overlap (exact declared phrases),
    - word overlap (the content words inside those phrases — v1.3: free
      citizen vocabulary meets canonical phrases here),
    - concept coverage (governed taxonomy families).
    Raw = phrase and word blended 50/50; family = raw and concept 50/50.
    When NEITHER side hits the taxonomy, the concept tier is silent (raw
    alone decides) — a taxonomy gap is not evidence of misalignment."""
    phrase, phrase_shared = _coeff(set(a_terms or []), set(b_terms or []))
    word, word_shared = _coeff(_words(a_terms), _words(b_terms))
    raw = 0.5 * phrase + 0.5 * word
    raw_shared = sorted(set(phrase_shared) | set(word_shared))
    ca, cb = concepts_of(a_terms), concepts_of(b_terms)
    if not ca and not cb:
        return raw, raw_shared, []
    con, con_shared = _coeff(ca, cb)
    return 0.5 * raw + 0.5 * con, raw_shared, con_shared


def cross_score(a_terms, b_terms):
    """Offers<->needs and wants keep the v1.1 signature overlap (raw+concepts)."""
    A = set(a_terms or []) | concepts_of(a_terms)
    B = set(b_terms or []) | concepts_of(b_terms)
    return _coeff(A, B)


def score(a, b, value_b=None):
    t, t_raw, t_con = family_score(a.get("topics"), b.get("topics"))
    g, g_raw, g_con = family_score(a.get("goals"), b.get("goals"))
    on1, on1s = cross_score(a.get("offers"), b.get("needs"))
    on2, on2s = cross_score(b.get("offers"), a.get("needs"))
    on = (on1 + on2) / 2.0
    w1, w1s = cross_score(a.get("wants"), (b.get("topics") or []) + (b.get("offers") or []))
    w2, w2s = cross_score(b.get("wants"), (a.get("topics") or []) + (a.get("offers") or []))
    w = (w1 + w2) / 2.0
    parts = {"topics": t, "goals": g, "offers_needs": on, "wants": w}
    relevance = round(100 * sum(WEIGHTS[k] * v for k, v in parts.items()))
    rank = relevance if value_b is None else round(relevance * (0.9 + 0.1 * value_b))
    signals = [k for k, v in parts.items() if v > 0]
    reasons = []
    shared = sorted(set(t_raw) | set(t_con))
    if shared: reasons.append("shared: " + ", ".join(shared[:5]))
    gshared = sorted(set(g_raw) | set(g_con))
    if gshared: reasons.append("shared goals: " + ", ".join(gshared[:3]))
    fits = sorted(set(on1s + on2s))
    if fits: reasons.append("offer/need fit: " + ", ".join(fits[:3]))
    wants = sorted(set(w1s + w2s))
    if wants: reasons.append("wanted connection: " + ", ".join(wants[:3]))
    return {"score": relevance, "rank": rank, "signals": signals,
            "surface": len(signals) >= 2,
            "parts": {k: round(v, 2) for k, v in parts.items()}, "reasons": reasons}


def rank_matches(entity, candidates):
    rows = [{"name": n, **score(entity, c)} for n, c in candidates.items()]
    rows = [r for r in rows if r["surface"]]
    return sorted(rows, key=lambda r: (-r["rank"], r["name"]))


if __name__ == "__main__":
    from declared_vectors import SEATS, PROJECTS
    out = {s: rank_matches(v, PROJECTS) for s, v in SEATS.items()}
    pairs, names = {}, list(SEATS)
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            pairs[f"{names[i]} <-> {names[j]}"] = score(SEATS[names[i]], SEATS[names[j]])
    out["seats_x_seats"] = pairs
    print(json.dumps(out, indent=1))

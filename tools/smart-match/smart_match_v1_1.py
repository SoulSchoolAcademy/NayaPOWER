#!/usr/bin/env python3
"""
Smart Match v1.1 — Naya Power, SET B (engine end), 2026-10-24.
Supersedes v1 (kept in git history). Built by the scorecard loop Shawn ordered:
score -> why-not-10 -> 10x fixes -> apply, three times. See SCORECARD.md.

WHAT A MATCH % MEANS (the semantics, published):
  The % is the weighted share of DECLARED signals that align between two
  profile vectors. It is NOT a probability and NOT a judgment of worth.
  100 = every weighted signal family aligns completely. Reasons always ride
  along; a % without reasons is a bug.

v1.1 CHANGES vs v1:
  1. CONCEPT LAYER (the Resolve cure): terms expand through a governed
     taxonomy into concepts; matching runs over raw terms + concepts, so
     orthogonal crafts become visible to each other (a resolver's THINKING /
     CLEARING concepts meet a project's distillation / blocker needs).
  2. Symmetric wants: both directions are scored and averaged.
  3. Value-aware RANKING (kept out of the %): when a candidate carries a
     verified value record (0..1), its rank score = relevance x (0.9 + 0.1v).
     Unknown value = neutral. The % itself stays pure relevance, always.
  4. Deterministic output: stable sort (score desc, then name) — same input,
     same list, every run, every machine.
"""
import json

WEIGHTS = {"topics": 0.40, "goals": 0.25, "offers_needs": 0.20, "wants": 0.15}

# Governed taxonomy v1: concept -> member terms. Small on purpose; it grows
# by amendment with evidence, never by one seat's whim.
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
for concept, terms in TAXONOMY.items():
    for t in terms:
        TERM2CONCEPTS.setdefault(t, set()).add(concept)


def expand(terms):
    """A vector field's signature: its raw terms plus every concept they hit."""
    sig = set()
    for t in terms or []:
        sig.add(t)
        sig |= TERM2CONCEPTS.get(t, set())
    return sig


def overlap(a_terms, b_terms):
    A, B = expand(a_terms), expand(b_terms)
    if not A or not B:
        return 0.0, []
    shared = sorted(A & B)
    return len(shared) / min(len(A), len(B)), shared


def score(a, b, value_b=None):
    t, t_shared = overlap(a.get("topics"), b.get("topics"))
    g, g_shared = overlap(a.get("goals"), b.get("goals"))
    on1, on1s = overlap(a.get("offers"), b.get("needs"))
    on2, on2s = overlap(b.get("offers"), a.get("needs"))
    on = (on1 + on2) / 2.0
    w1, w1s = overlap(a.get("wants"), (b.get("topics") or []) + (b.get("offers") or []))
    w2, w2s = overlap(b.get("wants"), (a.get("topics") or []) + (a.get("offers") or []))
    w = (w1 + w2) / 2.0
    parts = {"topics": t, "goals": g, "offers_needs": on, "wants": w}
    relevance = round(100 * sum(WEIGHTS[k] * v for k, v in parts.items()))
    rank = relevance if value_b is None else round(relevance * (0.9 + 0.1 * value_b))
    signals = [k for k, v in parts.items() if v > 0]
    reasons = []
    if t_shared: reasons.append("shared: " + ", ".join(t_shared[:5]))
    if g_shared: reasons.append("shared goals: " + ", ".join(g_shared[:3]))
    fits = sorted(set(on1s + on2s))
    if fits: reasons.append("offer/need fit: " + ", ".join(fits[:3]))
    wants = sorted(set(w1s + w2s))
    if wants: reasons.append("wanted connection: " + ", ".join(wants[:3]))
    return {"score": relevance, "rank": rank, "signals": signals,
            "surface": len(signals) >= 2,
            "parts": {k: round(v, 2) for k, v in parts.items()}, "reasons": reasons}


def rank_matches(entity, candidates):
    """candidates: {name: vector}. Returns the surfaced matches, deterministically ordered."""
    rows = [{"name": n, **score(entity, c)} for n, c in candidates.items()]
    rows = [r for r in rows if r["surface"]]
    return sorted(rows, key=lambda r: (-r["rank"], r["name"]))


if __name__ == "__main__":
    import smart_match_v1 as v1  # reuse the declared vectors from the first run
    out = {}
    for sname, svec in v1.SEATS.items():
        out[sname] = rank_matches(svec, v1.PROJECTS)
    pairs = {}
    names = list(v1.SEATS)
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            r = score(v1.SEATS[names[i]], v1.SEATS[names[j]])
            pairs[f"{names[i]} <-> {names[j]}"] = r
    out["seats_x_seats"] = pairs
    print(json.dumps(out, indent=1))

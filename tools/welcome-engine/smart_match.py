#!/usr/bin/env python3
"""
Smart Match — current engine (v1.5, elite hardening 2026-10-24).
History: v1 (literal tokens) -> v1.1 (concept layer) -> v1.2 (two-tier
family scoring) -> v1.3 (word tier inside the raw score — citizen free
vocabulary: "urban gardening" must see "gardening"; found by the Welcome
Engine's first end-to-end demo, Loop 2) -> v1.4 (light stemming; word tier
in cross scores — "chess partners" sees "chess"; validated 12/12 against
the Golden Set, weights evidence-checked by calibrate.py) -> v1.5 (elite
hardening, HARDENING-ELITE-V2-2026-10-24: one unified stopword set;
malformed-vector robustness; output contract extended with
signal_coverage_percent + calibrated; rank_matches excludes the entity
itself; optional population-frequency (IDF) mode, default OFF;
value_b is a verified-value RECORD, never a bare number; indexed
candidate pre-filter for scale, proven result-identical).

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
  never the % — unknown value is neutral. v1.5: the record must carry
  state VERIFIED or FINAL (the points profile's posting states); a bare
  float or a PENDING/OBSERVED record is treated as neutral, because a
  number without a verification state is not evidence of value.
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
for _c, _tl in TAXONOMY.items():
    for _t in _tl:
        TERM2CONCEPTS.setdefault(_t, set()).add(_c)


# ONE stopword set for every tier (v1.5). Before this, the word tier had
# none — "the" (len 3 > 2) leaked into topic/goal word overlap and into
# reasons ("shared goals: the") — while the cross tier had its own list.
# Filtering is on the RAW word, before stemming, in every tier.
STOPWORDS = {
    "a", "an", "the", "and", "or", "of", "to", "in", "on", "for", "with",
    "from", "that", "this", "it", "its", "is", "are", "was", "were", "be",
    "been", "as", "at", "by", "all", "any", "you", "your", "our", "their",
    "them", "they", "we", "he", "she", "his", "her", "into", "about",
    "over", "under", "more", "most", "other", "others", "some", "such",
    "only", "own", "same", "than", "then", "when", "who", "what", "how",
    "not", "no", "but", "if", "so", "do", "does", "can", "could", "will",
    "would", "has", "have", "had",
    # the v1.4 cross-tier list, folded in:
    "help", "want", "wants", "need", "needs", "people", "person", "someone",
}
CROSS_STOPWORDS = STOPWORDS  # backward-compatible alias (v1.4 name)

FIELDS = ("topics", "goals", "offers", "needs", "wants")


def _terms(x):
    """Sanitize one declared field into a list of term strings. Anything
    malformed — None, a bare number, non-string entries — degrades to
    fewer terms, never to a crash (v1.5 robustness battery). A bare string
    is one term, not an iterable of characters."""
    if x is None:
        return []
    if isinstance(x, str):
        return [x] if x.strip() else []
    if isinstance(x, (list, tuple, set)):
        return [t for t in x if isinstance(t, str) and t.strip()]
    return []


def _clean(vec):
    """Sanitize a whole profile vector: a dict of the five fields, each a
    clean list of strings. Non-dict input becomes the empty vector."""
    if not isinstance(vec, dict):
        return {f: [] for f in FIELDS}
    return {f: _terms(vec.get(f)) for f in FIELDS}


def concepts_of(terms):
    out = set()
    for t in _terms(terms):
        out |= TERM2CONCEPTS.get(t, set())
    return out


def _coeff(A, B, wts=None):
    if not A or not B:
        return 0.0, []
    shared = sorted(A & B)
    if not wts:
        return len(shared) / min(len(A), len(B)), shared
    wa = sum(wts.get(x, 1.0) for x in A)
    wb = sum(wts.get(x, 1.0) for x in B)
    ws = sum(wts.get(x, 1.0) for x in shared)
    denom = min(wa, wb)
    return (ws / denom if denom > 0 else 0.0), shared


def stem(w):
    """Light deterministic stemmer (Loop 4): unifies garden/gardens/gardening,
    teach/teaching. Suffix rules only — no dictionary, no surprises.
    v1.5: plural stripping applies BEFORE the -ing rule, so a lemma and
    its plural stem identically ('weddings' -> 'wedding' -> 'wed', exactly
    like 'wedding'; 'buildings' -> 'building' -> 'build'). In v1.4 the
    elif chain made 'wedding' stem to 'wed' but 'weddings' to 'wedding',
    so the same word in two forms never met."""
    if len(w) > 4 and w.endswith("ies"):
        w = w[:-3] + "y"
    elif len(w) > 3 and w.endswith("s") and not w.endswith("ss"):
        w = w[:-1]
    if len(w) > 5 and w.endswith("ing"):
        w = w[:-3]
        if len(w) > 3 and w[-1] == w[-2]:
            w = w[:-1]
    return w


def _words(terms):
    out = set()
    for t in _terms(terms):
        out |= {stem(w) for w in t.lower().replace(",", " ").split()
                if len(w) > 2 and w not in STOPWORDS}
    return out


def _content_phrases(terms):
    """Declared phrases that carry at least one content word. A phrase made
    only of stopwords ('the and of') is glue, not a signal: it must not
    phrase-match, in any tier (v1.5 — the phrase tier previously matched
    glue-only phrases verbatim)."""
    return [t for t in _terms(terms) if _words([t])]


def family_score(a_terms, b_terms, wts=None):
    """Topics/goals scoring, three ingredients:
    - phrase overlap (exact declared phrases),
    - word overlap (the content words inside those phrases — v1.3: free
      citizen vocabulary meets canonical phrases here),
    - concept coverage (governed taxonomy families).
    Raw = phrase and word blended 50/50; family = raw and concept 50/50.
    When NEITHER side hits the taxonomy, the concept tier is silent (raw
    alone decides) — a taxonomy gap is not evidence of misalignment."""
    phrase, phrase_shared = _coeff(set(_content_phrases(a_terms)), set(_content_phrases(b_terms)), wts)
    word, word_shared = _coeff(_words(a_terms), _words(b_terms), wts)
    raw = 0.5 * phrase + 0.5 * word
    raw_shared = sorted(set(phrase_shared) | set(word_shared))
    ca, cb = concepts_of(a_terms), concepts_of(b_terms)
    if not ca and not cb:
        return raw, raw_shared, []
    con, con_shared = _coeff(ca, cb, wts)
    return 0.5 * raw + 0.5 * con, raw_shared, con_shared


def cross_score(a_terms, b_terms, wts=None):
    """Offers<->needs and wants: signature overlap (terms + concepts + stemmed
    content words, Loop 4 — 'chess partners' must see 'chess'; generic glue
    words are stoplisted so cross-fits stay meaningful)."""
    def sig(terms):
        words = {stem(w) for t in _terms(terms)
                 for w in t.lower().replace(",", " ").split()
                 if len(w) > 3 and w not in STOPWORDS}
        return set(_content_phrases(terms)) | concepts_of(terms) | words
    return _coeff(sig(a_terms), sig(b_terms), wts)


def signature(vec):
    """Every token any channel could ever match on, for one vector:
    phrases + stemmed content words + concepts, unioned over all fields.
    Used by the IDF weighting and the indexed pre-filter — both are sound
    only because a channel can score > 0 solely via a shared token here."""
    v = _clean(vec)
    out = set()
    for f in FIELDS:
        out |= set(v[f]) | _words(v[f]) | concepts_of(v[f])
    return out


def compute_idf(population, threshold=0.5, factor=0.25):
    """Population-frequency weighting (v1.5, OPTIONAL — default off).
    Returns {token: factor} for tokens appearing in MORE than `threshold`
    of the population; everything else weighs 1.0. A token most of the
    population shares (e.g. 'builder' in the first population) carries
    little information about THIS pair; down-weighting it lets the
    discriminating tokens decide. The factor discounts, never zeroes:
    ubiquity is weak evidence, not no evidence."""
    pop = [_clean(v) for v in population or []]
    n = len(pop)
    if n == 0:
        return {}
    df = {}
    for v in pop:
        for tok in signature(v):
            df[tok] = df.get(tok, 0) + 1
    return {tok: factor for tok, c in df.items() if c / n > threshold}


VERIFIED_VALUE_STATES = ("VERIFIED", "FINAL")


def _verified_value(value_b):
    """The value-record contract (v1.5): value_b counts only as a RECORD
    carrying a verified state — {'state': 'VERIFIED'|'FINAL', 'value': v}
    with v a number in [0,1]. A bare float, a PENDING/OBSERVED record, or
    anything malformed is NEUTRAL (returns None): rank stays relevance."""
    if not isinstance(value_b, dict):
        return None
    if str(value_b.get("state", "")).upper() not in VERIFIED_VALUE_STATES:
        return None
    v = value_b.get("value", value_b.get("score"))
    if isinstance(v, bool) or not isinstance(v, (int, float)):
        return None
    return max(0.0, min(1.0, float(v)))


def score(a, b, value_b=None, idf=None):
    a, b = _clean(a), _clean(b)
    t, t_raw, t_con = family_score(a["topics"], b["topics"], idf)
    g, g_raw, g_con = family_score(a["goals"], b["goals"], idf)
    on1, on1s = cross_score(a["offers"], b["needs"], idf)
    on2, on2s = cross_score(b["offers"], a["needs"], idf)
    on = (on1 + on2) / 2.0
    w1, w1s = cross_score(a["wants"], b["topics"] + b["offers"], idf)
    w2, w2s = cross_score(b["wants"], a["topics"] + a["offers"], idf)
    w = (w1 + w2) / 2.0
    parts = {"topics": t, "goals": g, "offers_needs": on, "wants": w}
    relevance = round(100 * sum(WEIGHTS[k] * v for k, v in parts.items()))
    vv = _verified_value(value_b)
    rank = relevance if vv is None else round(relevance * (0.9 + 0.1 * vv))
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
    # v1.5 output-contract extension — existing keys unchanged:
    coverage = round(100 * sum(WEIGHTS[k] for k, v in parts.items() if v > 0))
    return {"score": relevance, "rank": rank, "signals": signals,
            "surface": len(signals) >= 2,
            "parts": {k: round(v, 2) for k, v in parts.items()}, "reasons": reasons,
            "signal_coverage_percent": coverage,
            "calibrated": True}


def rank_matches(entity, candidates, self_name=None, idf=None):
    """Ranked surfaced matches for one entity. The entity itself is never
    its own match (v1.5): excluded by name (self_name, or a 'name'/'_name'
    key on the entity) and by object identity."""
    if self_name is None and isinstance(entity, dict):
        self_name = entity.get("name") or entity.get("_name")
    rows = []
    for n, c in (candidates or {}).items():
        if n == self_name or c is entity:
            continue
        r = score(entity, c, idf=idf)
        if r["surface"]:
            rows.append({"name": n, **r})
    return sorted(rows, key=lambda r: (-r["rank"], r["name"]))


def build_index(candidates):
    """Inverted index over candidate signatures: token -> {names}."""
    index = {}
    for n, c in (candidates or {}).items():
        for tok in signature(c):
            index.setdefault(tok, set()).add(n)
    return index


def rank_matches_indexed(entity, candidates, index=None, self_name=None, idf=None):
    """rank_matches behind the inverted-index pre-filter (v1.5, scale).
    A pair can surface only if some channel scores > 0, and a channel
    scores > 0 only via a shared signature token — so candidates sharing
    no token with the entity can never surface, and skipping them changes
    nothing. Proven result-identical to rank_matches (bench + tests)."""
    if index is None:
        index = build_index(candidates)
    keep = set()
    for tok in signature(entity):
        keep |= index.get(tok, set())
    sub = {n: c for n, c in (candidates or {}).items() if n in keep}
    return rank_matches(entity, sub, self_name=self_name, idf=idf)


if __name__ == "__main__":
    from declared_vectors import SEATS, PROJECTS
    out = {s: rank_matches(v, PROJECTS) for s, v in SEATS.items()}
    pairs, names = {}, list(SEATS)
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            pairs[f"{names[i]} <-> {names[j]}"] = score(SEATS[names[i]], SEATS[names[j]])
    out["seats_x_seats"] = pairs
    print(json.dumps(out, indent=1))

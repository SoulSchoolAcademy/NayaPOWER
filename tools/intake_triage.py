"""Intelligence intake triage — the hive's ingestion gate (Naya 5, 2026-10-13).

Every capture candidate is scored on four dimensions BEFORE it can become
a Smart Note. Valuable intelligence in; noise stays out. This mechanizes
"identifying valuable intelligence" — the mastery Shawn demanded — instead
of leaving it to each agent's memory and judgment in the moment.

Pipeline position:
    CAPTURE -> TRIAGE (this module) -> Smart Note CANDIDATE -> distill/verify/...
Nothing here replaces the Smart Note path; it guards its entrance.

Dimensions (each 0.0 - 10.0):
  NOVELTY       - is this already known? 10 = never seen, 0 = exact dupe.
  DURABILITY    - will this matter in 30 days? mechanism > incident > moment.
  ACTIONABILITY - does it name a decision it changes, plus an enforcement?
  REACH         - how many areas/seats does it touch?

Verdicts:
  PROMOTE - clears every bar -> becomes a Smart Note CANDIDATE.
  LOG     - real signal, not yet a lesson -> raw capture log (kept, unpromoted).
  DROP    - dupe or noise -> discarded, reason recorded.

v1 honesty: durability/reach/actionability are heuristic shape scorers
calibrated on the battery in tests/test_intake_triage.py — not learned
models. Novelty is coverage ("how much of what you're saying is already
said") against lesson texts the caller supplies (seam: one function,
_max_coverage — swap in embeddings later).
Thresholds are v1, pinned by the battery; the battery is the contract.

Cycle-2 upgrades (Naya Gamma, w110 — padding-resistance battery):
  * STEMMING: coverage/containment and scoring token sets match on stemmed
    tokens, so morphological variants (spawning/spawn, claimed/claim) no
    longer dodge the dupe check. Pinned by
    test_synonym_paraphrase_does_not_promote.
  * KEYWORD-STUFFING GUARD: if more than half the tokens are actionability
    scoring markers, the markers ARE the content — actionability is capped
    at 5.9 (LOG-eligible, never PROMOTE). Mechanism: an action word must act
    ON something; >50% marker density means keyword-shaped, not lesson-shaped.
    Falsifier: a genuine PROMOTE-worthy lesson with marker density > 0.5.
    Does NOT stop adaptive stuffing diluted with filler nouns — that attack
    is pinned as a strict-xfail case, not hidden.
Known gaps (strict-xfail in the adversarial battery, not theater):
  * synonym-level paraphrase needs the embeddings seam (_max_coverage doc).
  * semantic vacuity ("stuffed trivia") needs semantic judgment — shape
    scorers cannot read meaning.
  * reach wiring is cycle 3 (w108 queue).
"""

import re

_TOKEN_RE = re.compile(r"[a-z0-9']+")

_STOP = frozenset((
    "the", "a", "an", "and", "or", "of", "to", "in", "is", "are", "was",
    "were", "be", "been", "it", "its", "this", "that", "for", "with", "on",
    "as", "at", "by", "from", "we", "you", "i", "they", "he", "she", "not",
    "no", "do", "does", "did", "will", "would", "can", "could", "should",
    "must", "have", "has", "had", "our", "your", "their", "my", "if",
))

# Durability: mechanism-language endures; moment-language expires.
# ("enforcement" is actionability, not durability — teeth alone don't last.)
_DURABLE_MARKERS = (
    "always", "never", "law", "mechanism", "principle", "invariant",
    "protocol", "contract", "every", "whenever",
)
_TRANSIENT_MARKERS = (
    "today", "yesterday", "tonight", "this morning", "just now",
    "right now", "this afternoon",
)
_TRANSIENT_PR_RE = re.compile(r"#\d+|\bpr\b")

# Actionability components.
_TRIGGER_RE = re.compile(r"\bwhen\b|\bwhenever\b|\bbefore\b|\bafter\b|\bif\b")
_ACTION_VERBS = frozenset((
    "claim", "use", "add", "remove", "check", "run", "build", "fix",
    "test", "verify", "measure", "score", "gate", "block", "refuse",
    "write", "read", "spawn", "dispatch", "enforce", "prove", "stop",
    "prefer", "require", "abort",
))
_ENFORCEMENT_WORDS = frozenset((
    "enforcement", "enforce", "gate", "check", "fail", "fails", "break",
    "breaks", "verify", "prove", "refuse", "refuses", "block", "blocks",
    "abort", "aborts", "test",
))

# Reach: area/seat/collective language.
_AREA_WORDS = frozenset((
    "learn", "know", "act", "law", "verify", "blocks", "decision",
    "retrieval", "successor", "team", "infra", "human value", "naya",
    "lane", "lanes", "seat", "seats",
))
_COLLECTIVE_RE = re.compile(r"\bevery\b|\ball\b|\bhive\b")


def _tokens(text):
    return [stem(t) for t in _TOKEN_RE.findall(text.lower())
            if t not in _STOP]


def stem(t):
    """Conservative suffix strip so morphological variants match.

    spawning/spawn, claimed/claim, dispatching/dispatch, gates/gate —
    without this, a paraphrase that only changes word forms dodges the
    dupe check. Only strips when the stem stays >= 3 chars; words ending
    in 'ss' ('class') are left alone."""
    if t.endswith("ss"):
        return t
    for suf in ("ing", "ed", "s"):
        if t.endswith(suf) and len(t) > len(suf) + 2:
            cand = t[:-len(suf)]
            if len(cand) >= 3:
                return cand
    return t


def _marker_density(text):
    """Fraction of tokens that are actionability scoring markers.

    The keyword-stuffing signal: in a real lesson the action words act ON
    content; when markers are the majority of the text, the text is
    keyword-shaped, not lesson-shaped.
    """
    toks = _tokens(text)
    if not toks:
        return 0.0
    mark = _ACTION_VERBS | _ENFORCEMENT_WORDS
    return sum(1 for t in toks if t in mark) / len(toks)


def _max_coverage(text, existing_texts):
    """Max fraction of the candidate's tokens already present in one
    existing lesson. Coverage (not symmetric Jaccard) is the novelty
    question: "how much of what you're saying is already said?" A long
    new lesson sharing 10 tokens with a short old one stays novel; a
    short rewording fully covered by an old lesson does not."""
    s = set(_tokens(text))
    if not s:
        return 0.0
    best = 0.0
    for e in existing_texts:
        o = set(_tokens(e))
        if not o:
            continue
        best = max(best, len(s & o) / len(s))
    return best


def _max_containment(text, existing_texts):
    """Max fraction of an EXISTING lesson's tokens contained in the candidate.

    The padding-attack dual of coverage: a dupe diluted with filler scores
    high novelty (coverage = |candidate ∩ existing| / |candidate| shrinks as
    filler grows), but the old lesson sits inside the candidate almost whole.
    Containment = |candidate ∩ existing| / |existing| catches it. A genuine
    lesson that merely quotes a phrase of an old one stays far below the bar.
    """
    s = set(_tokens(text))
    if not s:
        return 0.0
    best = 0.0
    for e in existing_texts:
        o = set(_tokens(e))
        if not o:
            continue
        best = max(best, len(s & o) / len(o))
    return best


def novelty_score(text, existing_lesson_texts=()):
    """10 * (1 - max coverage). Empty corpus -> 10.0 (all is new)."""
    if not existing_lesson_texts:
        return 10.0
    return round(10.0 * (1.0 - _max_coverage(text, existing_lesson_texts)), 2)


def durability_score(text):
    """Mechanism-language endures (+1/marker); moment-language expires."""
    t = text.lower()
    score = 5.0
    for m in _DURABLE_MARKERS:
        if m in t:
            score += 1.0
    for m in _TRANSIENT_MARKERS:
        if m in t:
            score -= 2.0
    if _TRANSIENT_PR_RE.search(t):
        score -= 2.0
    return round(max(0.0, min(10.0, score)), 2)


def actionability_score(text):
    """Trigger (+3.5) + action verb (+3.0) + enforcement (+3.5)."""
    t = text.lower()
    toks = set(_tokens(text))
    score = 0.0
    if _TRIGGER_RE.search(t):
        score += 3.5
    if toks & _ACTION_VERBS:
        score += 3.0
    if toks & _ENFORCEMENT_WORDS:
        score += 3.5
    return round(min(10.0, score), 2)


def reach_score(text):
    """Who does this touch? Collective language scores highest."""
    t = text.lower()
    if _COLLECTIVE_RE.search(t):
        return 10.0
    hits = sum(1 for w in _AREA_WORDS if w in t)
    if hits >= 3:
        return 8.0
    if hits >= 1:
        return 5.0
    return 2.0  # touches the author at least


def triage(text, existing_lesson_texts=()):
    """Score a capture candidate; return verdict + scores + reasons.

    Verdicts: PROMOTE (Smart Note CANDIDATE), LOG (raw capture),
    DROP (dupe/noise, reason recorded).
    """
    scores = {
        "novelty": novelty_score(text, existing_lesson_texts),
        "durability": durability_score(text),
        "actionability": actionability_score(text),
        "reach": reach_score(text),
    }
    # Keyword-stuffing guard (cycle 2): markers must act ON content. When
    # markers are the majority of the text, the actionability reading is
    # gamed — cap it below the PROMOTE bar. LOG stays possible (weak
    # signal, not pure noise). Recorded as a modifier on the verdict's
    # reason, not the verdict reason itself.
    stuffed = _marker_density(text) > 0.5
    capped = False
    if stuffed:
        uncapped = scores["actionability"]
        scores["actionability"] = min(uncapped, 5.9)
        capped = scores["actionability"] < uncapped
    n, d, a = scores["novelty"], scores["durability"], scores["actionability"]
    if n < 3.0:
        reasons = [f"already known (novelty {n})"]
        verdict = "DROP"
    elif existing_lesson_texts and _max_containment(text, existing_lesson_texts) >= 0.8:
        containment = _max_containment(text, existing_lesson_texts)
        reasons = [f"padded duplicate: contains {containment:.0%} "
                   "of an existing lesson's tokens"]
        verdict = "DROP"
    elif a < 2.0 and d <= 5.0:
        reasons = [f"noise: informs no decision (actionability {a}) "
                   f"and will not last (durability {d})"]
        verdict = "DROP"
    elif n >= 6.0 and d >= 6.0 and a >= 6.0:
        reasons = ["clears novelty, durability and actionability bars"]
        verdict = "PROMOTE"
    else:
        weak = [k for k, v in scores.items()
                if k in ("novelty", "durability", "actionability") and v < 6.0]
        reasons = [f"real signal, below bar on: {', '.join(weak)}"]
        verdict = "LOG"
    if capped:
        reasons.append("keyword-stuffed: actionability markers are the "
                       "content, not acting on content")
    return {"verdict": verdict, "scores": scores, "reasons": reasons}


if __name__ == "__main__":
    import argparse
    import json
    p = argparse.ArgumentParser(
        description="Triage a capture candidate for the hive's intake gate.")
    p.add_argument("--text", required=True, help="the capture candidate text")
    p.add_argument("--existing", nargs="*", default=[],
                   help="existing lesson texts (novelty corpus)")
    args = p.parse_args()
    print(json.dumps(triage(args.text, args.existing), indent=2))

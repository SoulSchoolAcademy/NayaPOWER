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
    return [t for t in _TOKEN_RE.findall(text.lower()) if t not in _STOP]


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
    n, d, a = scores["novelty"], scores["durability"], scores["actionability"]
    if n < 3.0:
        return {"verdict": "DROP", "scores": scores,
                "reasons": [f"already known (novelty {n})"]}
    if a < 2.0 and d <= 5.0:
        return {"verdict": "DROP", "scores": scores,
                "reasons": [f"noise: informs no decision (actionability {a}) "
                            f"and will not last (durability {d})"]}
    if n >= 6.0 and d >= 6.0 and a >= 6.0:
        return {"verdict": "PROMOTE", "scores": scores,
                "reasons": ["clears novelty, durability and actionability bars"]}
    weak = [k for k, v in scores.items()
            if k in ("novelty", "durability", "actionability") and v < 6.0]
    return {"verdict": "LOG", "scores": scores,
            "reasons": [f"real signal, below bar on: {', '.join(weak)}"]}


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

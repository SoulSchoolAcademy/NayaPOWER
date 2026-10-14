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
Cycle-3 upgrades (Naya Gamma, w111 — reach wiring + embeddings seam):
  * REACH WIRING: reach is no longer a bare word list. _AREA_KEYWORDS wires
    every reach keyword to one of the twelve canonical areas (TEAM-STRUCTURE),
    and reach_details() names WHICH areas a candidate touches. reach_score()
    is derived from it — the 10/8/5/2 bands are byte-identical to cycle 2.
    Matching stays substring shape-matching (documented roughness, not a
    semantic router — see P-011).
  * EMBEDDINGS SEAM: novelty_score() and triage() accept similarity=, an
    injectable callable (text, corpus) -> float in [0,1] = "fraction of the
    candidate's content already present in the corpus". Default is the token
    _max_coverage; an embeddings provider wires in without touching triage().
    Values are clamped to [0,1]; NaN raises ValueError (no silent certainty).
Cycle-4 (Naya Gamma, w127 — semantic containment, Eta w126 design):
  * SEMANTIC CONTAINMENT SEAM: triage() accepts containment=, an injectable
    callable (text, corpus) -> list[SemanticMatch]. Default is the built-in
    semantic_containment() below (stdlib only, no model calls): canonical-
    concept coverage + 5-condition skeleton match + novel-concept escape.
    Lexical containment stays FIRST (cheap-check-first); the semantic gate
    runs only when lexical passes. DROP is a coverage verdict, not a truth
    verdict. See semantic_containment() for the operational definitions
    (the design leaves clause roles, passive voice, and marker sets
    unspecified — this build pins them, with the deltas measured in w127).
Known gaps (strict-xfail in the adversarial battery, not theater):
  * an embeddings PROVIDER is still needed — the seam is the socket, not
    the signal. The synonym-xfail now names the provider, not the seam.
  * semantic vacuity ("stuffed trivia") needs semantic judgment — shape
    scorers cannot read meaning.
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

# Reach: the twelve canonical areas (TEAM-STRUCTURE), wired to keywords.
# Every keyword that counted toward the cycle-2 reach bands is still here —
# wiring ADDS the area names, it does not change what matches. The extra
# team-talk words (naya, lane(s), seat(s)) count as reach hits without
# belonging to one area: they name the collective doing the work.
_AREA_KEYWORDS = {
    "LEARN": ("learn",),
    "KNOW": ("know",),
    "ACT": ("act",),
    "LAW": ("law",),
    "VERIFY": ("verify",),
    "Intelligent Blocks": ("blocks",),
    "Decision Engine": ("decision",),
    "Retrieval": ("retrieval",),
    "Successor": ("successor",),
    "TEAM": ("team",),
    "INFRA": ("infra",),
    "Human Value": ("human value",),
}
_TEAM_TALK = ("naya", "lane", "lanes", "seat", "seats")
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


def novelty_score(text, existing_lesson_texts=(), similarity=None):
    """10 * (1 - max coverage). Empty corpus -> 10.0 (all is new).

    THE EMBEDDINGS SEAM (cycle 3): similarity is an injectable callable
    (text, corpus) -> float in [0,1] = "fraction of the candidate's content
    already present in the corpus". Default is the token _max_coverage; an
    embeddings provider wires in here without touching triage().
    The seam is the socket, not the signal — token coverage is the default
    provider, and it cannot see synonym-level paraphrase (strict-xfail).

    Contract: values are clamped to [0,1]; NaN raises ValueError instead of
    manufacturing certainty; a non-callable similarity is a TypeError.

    Boundary (named, not hidden): the seam drives NOVELTY only. The
    padding check (_max_containment) stays token-based by design — a
    coverage provider answers "how much of the candidate is already said",
    not "how much of an old lesson sits inside the candidate". The
    combined synonym+filler attack needs semantic containment too; that is
    its own named fix, and its xfail stays strict.
    """
    if not existing_lesson_texts:
        return 10.0
    sim = similarity if similarity is not None else _max_coverage
    coverage = float(sim(text, existing_lesson_texts))
    if coverage != coverage:  # NaN
        raise ValueError("similarity returned NaN: refusing to score "
                         "novelty on an undefined value")
    coverage = max(0.0, min(1.0, coverage))
    return round(10.0 * (1.0 - coverage), 2)


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


def reach_details(text):
    """Which areas does this candidate touch? (cycle-3 reach wiring)

    Returns {"areas": [...], "team_talk": [...], "collective": bool}.
    areas are the twelve canonical area names with at least one keyword
    hit; team_talk are the extra collective-work words hit; collective is
    the every/all/hive band.

    P-011 honesty: matching is substring shape-matching on the lowercased
    text ("act" matches "action", "lane" matches "lanes"). This names which
    areas the WORDS point at — it does NOT claim semantic area routing.
    """
    t = text.lower()
    areas = sorted(
        name for name, kws in _AREA_KEYWORDS.items()
        if any(k in t for k in kws))
    team_talk = sorted(w for w in _TEAM_TALK if w in t)
    return {"areas": areas, "team_talk": team_talk,
            "collective": bool(_COLLECTIVE_RE.search(t))}


def reach_score(text):
    """Who does this touch? Collective language scores highest.

    Derived from reach_details(); bands byte-identical to cycle 2:
    collective 10.0, >=3 hits 8.0, >=1 hit 5.0, else 2.0."""
    d = reach_details(text)
    if d["collective"]:
        return 10.0
    hits = len(d["areas"]) + len(d["team_talk"])
    if hits >= 3:
        return 8.0
    if hits >= 1:
        return 5.0
    return 2.0  # touches the author at least


def triage(text, existing_lesson_texts=(), similarity=None, containment=None):
    """Score a capture candidate; return verdict + scores + reasons.

    Verdicts: PROMOTE (Smart Note CANDIDATE), LOG (raw capture),
    DROP (dupe/noise, reason recorded).

    similarity= threads the embeddings seam through novelty scoring; see
    novelty_score() for the contract.
    containment= threads the semantic-containment seam; default is the
    built-in semantic_containment(). Order (cheap-check-first): novelty ->
    lexical containment -> semantic containment -> noise -> PROMOTE/LOG
    bars -> GREY cap. The semantic gate runs ONLY when lexical passes.
    """
    scores = {
        "novelty": novelty_score(text, existing_lesson_texts,
                                similarity=similarity),
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
    semantic = None
    if n < 3.0:
        reasons = [f"already known (novelty {n})"]
        verdict = "DROP"
    elif existing_lesson_texts and _max_containment(text, existing_lesson_texts) >= 0.8:
        containment_v = _max_containment(text, existing_lesson_texts)
        reasons = [f"padded duplicate: contains {containment_v:.0%} "
                   "of an existing lesson's tokens"]
        verdict = "DROP"
    else:
        if existing_lesson_texts:
            fn = containment if containment is not None else semantic_containment
            matches = fn(text, list(existing_lesson_texts)) or []
            semantic = _best_semantic(matches)
        if semantic is not None and semantic["band"] == "RED":
            reasons = [f"semantically contained duplicate: covers "
                       f"{semantic['coverage']:.0%} of "
                       f"{semantic['lesson_head']} (concepts + skeleton match)"]
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
        if (semantic is not None and semantic["band"] == "GREY"
                and verdict == "PROMOTE"):
            reasons = [f"semantic near-dupe: covers "
                       f"{semantic['coverage']:.0%} of "
                       f"{semantic['lesson_head']}, manual review"]
            verdict = "LOG"
    if capped:
        reasons.append("keyword-stuffed: actionability markers are the "
                       "content, not acting on content")
    provider = (getattr(similarity, "__name__", "similarity")
                if similarity is not None else "_max_coverage")
    return {"verdict": verdict, "scores": scores, "reasons": reasons,
            "novelty_provider": provider,
            "reach": reach_details(text),
            "semantic": semantic,
            "aliases_version": ALIASES_VERSION}


# ---------------------------------------------------------------------------
# SEMANTIC CONTAINMENT (fix-pass (a) for #2552 — Eta w126 design, Gamma w127 build)
#
# Question: "How much of an old lesson's MEANING sits inside the candidate?"
# Meaning = canonical-concept coverage + 5-condition skeleton match +
# novel-concept escape. Stdlib only, no model calls, no embeddings.
#
# Operational definitions the design leaves unspecified (pinned here, deltas
# measured in w127 — a pin is a claim the battery can falsify, not a guess):
#  * Clause split: sentences ("." splits only before a capital, so
#    "lane-state.py" survives) -> "Enforcement:" -> ", and" (comma-and ONLY;
#    bare " and " stays inside the clause, so T4b's reason stays whole) ->
#    because/since (reason starts at the marker) -> leading trigger
#    (when/whenever/before/after/if/unless + comma: trigger split off).
#  * Clause roles: Enforcement: -> enforcement. because/since clause ->
#    reason. Leading trigger -> trigger (excluded from coverage + novelty).
#    Any other clause: no predicate -> filler; small-set marker density
#    >= 0.5 -> teeth; else first content clause -> core, rest -> secondary.
#    Predicate = a content verb OR a be/light verb (is/are/means/...) on the
#    RAW tokens, so stative claims ("that lane is already occupied") are
#    clauses, not filler. Filler/teeth/enforcement count for NOVELTY only,
#    with BIG-set markers stripped; core/reason/secondary count for coverage
#    + novelty, unstripped.
#  * Designated reason = the explicit because/since clause if present, else
#    the FIRST secondary clause (MECHANISM_LESSON's "A failed claim means
#    the lane is taken" is a reason by this rule). No designated reason on
#    either side -> skeleton fails (except both-reasonless, where the reason
#    conditions hold vacuously).
#  * Core action = first verb-lexicon token of the core clause, in order.
#    No lexicon verb -> action None -> skeleton fails (fail-closed toward
#    PASS: unknown verbs never manufacture a DROP).
#  * Core object: PASSIVE (a be-word precedes the verb, e.g. "the lane is
#    first reserved") -> concepts BEFORE the verb. ACTIVE -> concepts AFTER
#    the verb up to the first preposition/verb boundary. Subset check both ways.
#  * Marker sets: teeth CLASSIFICATION uses the SMALL set (actionability
#    verbs + enforcement words) — the big set would misclassify T3's short
#    verb-heavy core as teeth. Marker STRIPPING uses the BIG set (durable +
#    action + enforcement + area/team/collective/trigger words) — the small
#    set would leave T1's buzzword filler as 9 novel concepts.
#  * Stemmer gaps, fixed in canonicalization (never by editing stem()):
#    stem() maps moving->mov but moved/moves->move, so "mov" reunifies to
#    "move". It maps reserved->reserv (not reserve) and occupied->occupi
#    (not occupy) and leaves taken->taken (not take), so the alias table
#    carries separate surface entries (reserved, occupied, taken) — without
#    them the specified entries silently fail to fire on the fixture
#    inflections. "nonzero" normalizes to "non-zero" before tokenizing.
#  * Deontic: NEVER if "never" present post-normalization, else ALWAYS if
#    "always" present, else NONE (NONE is compatible with anything).
#  * Polarity: NEGATED if the reason text contains not/no/never/n't/cannot/
#    can't/doesn't/don't/won't/isn't/aren't/wasn't; else ASSERTED.
#
# Bands: RED (coverage >= 0.75 + skeleton + novel < 3) -> DROP.
# GREY (skeleton + coverage >= 0.60, incl. the novel >= 3 escape) -> LOG cap.
# PASS otherwise. A DROP is a COVERAGE verdict, not a truth verdict.
# ---------------------------------------------------------------------------

ALIASES_VERSION = "2"  # v2: + "record tool" (w128 fix-pass, evidence w127
# counterfactual: T2 novel 3 -> 1, flips to DROP; non-author review
# required per design governance before any PR ships this table).

_PHRASE_ALIASES = (
    ("state file", "truth file"),
    ("state record", "truth file"),
    ("state tool", "lane-state claim"),
    # w128: the enforcement clause names the tool that performs the claim
    # ("the record tool exits nonzero") — same referent as "state tool",
    # so it canonicalizes to the same concept. Without it, "record tool"
    # counts as two novel enforcement concepts and trips the escape rule.
    ("record tool", "lane-state claim"),
    ("limb pointer", "ref"),
    ("displayed hash", "printed sha"),
    ("relocated pointer", "moved ref"),
)

# Surface-form pairs; both sides stemmed at load; a stemmed-source collision
# is a load-time ValueError, never a silent override. Morphology variants
# (reserved, occupied, taken) are separate entries — see the stemmer-gap
# note above. No general-English synonyms: domain vocabulary only.
_WORD_ALIASES = (
    ("confirm", "verify"),
    ("remote", "server"),
    ("shift", "move"),
    ("display", "print"),
    ("hash", "sha"),
    ("reserve", "claim"),
    ("reserved", "claim"),
    ("reservation", "claim"),
    ("reject", "fail"),
    ("occupy", "take"),
    ("occupied", "take"),
    ("taken", "take"),
    ("halt", "abort"),
    ("launch", "spawn"),
    ("dispatch", "spawn"),
    ("agent", "worker"),
    ("return", "exit"),
    ("since", "because"),
    ("ahead", "before"),
    ("verification", "verify"),
)

_WORD_ALIAS = {}
for _src, _dst in _WORD_ALIASES:
    _k = stem(_src)
    if _k in _WORD_ALIAS and _WORD_ALIAS[_k] != stem(_dst):
        raise ValueError(f"alias collision on stemmed source {_k!r}")
    _WORD_ALIAS[_k] = stem(_dst)
del _src, _dst, _k

_CANON_FIX = {"mov": "move"}

_EXCLUDE_RAW = ("because", "since", "always", "never", "first", "already",
                "means", "mean", "before", "after", "across", "without",
                "within", "into", "over", "under", "per", "via", "about",
                "against", "when", "whenever", "if", "unless", "while",
                "every", "all", "each",
                # Manner adverbs are modifiers, not content concepts:
                # teeth clauses carry flavor adverbs ("fails loudly") that
                # must not count as novelty. Closed set, auditable.
                "loudly", "quietly", "quickly", "slowly", "clearly",
                "strongly", "weakly", "safely", "strictly", "openly",
                "fully", "partially", "directly", "indirectly",
                "immediately", "automatically", "manually", "publicly",
                "privately")
_CONCEPT_EXCLUDE = frozenset(stem(w) for w in _EXCLUDE_RAW)

_COMMON_VERBS = ("record", "persist", "remain", "exist", "take", "hold",
                 "show", "pass", "contain", "require", "allow", "prevent",
                 "cause", "create", "keep", "make", "give", "get", "set",
                 "put", "prove", "move", "moving", "shift", "land", "govern",
                 "rest", "stay", "seem", "become", "validate", "release",
                 "wait", "corrupt", "expire", "free", "log", "audit",
                 "replay", "water", "pair", "back", "need", "secure",
                 "securing", "reserving", "reserved")
_VERB_LEXICON = frozenset(stem(v) for v in
                           set(_ACTION_VERBS) | set(_ENFORCEMENT_WORDS)
                           | set(_COMMON_VERBS))
_PREDICATE_WORDS = frozenset(("is", "are", "was", "were", "be", "been",
                              "means", "mean", "seems", "stays", "remains"))
_SMALL_MARKERS = frozenset(stem(m) for m in
                             set(_ACTION_VERBS) | set(_ENFORCEMENT_WORDS))
_AREA_MARKER_WORDS = ("learn", "know", "act", "law", "verify", "blocks",
                      "decision", "retrieval", "successor", "team", "infra",
                      "human", "value", "naya", "lane", "seat", "every",
                      "all", "hive", "when", "whenever", "before", "after",
                      "if", "unless")
_BIG_MARKERS = frozenset(stem(m) for m in
                         set(_DURABLE_MARKERS) | set(_ACTION_VERBS)
                         | set(_ENFORCEMENT_WORDS)
                         | set(_AREA_MARKER_WORDS))
_STOP_PREP = frozenset(("before", "after", "across", "without", "within",
                        "into", "over", "under", "per", "via", "about",
                        "against"))
_TRIGGER_WORDS = ("when", "whenever", "before", "after", "if", "unless")
_NEG_RE = re.compile(r"\b(not|no|never|n't|cannot|can't|doesn't|don't|"
                     r"won't|isn't|aren't|wasn't)\b")


def _canon_one(tok):
    """Stem + reunify + alias one raw token."""
    s = _CANON_FIX.get(stem(tok), stem(tok))
    return _WORD_ALIAS.get(s, s)


def _canon_tokens(raw):
    return [_canon_one(t) for t in _tokens(raw)]


def _raw_tokens(raw):
    return re.findall(r"[a-z0-9']+", raw.lower())


def _concepts(raw, strip_markers=False):
    out = set()
    for t in _canon_tokens(raw):
        if t in _CONCEPT_EXCLUDE or len(t) < 3:
            continue
        if strip_markers and t in _BIG_MARKERS:
            continue
        out.add(t)
    return out


def _normalize_deontic(lowered):
    """never <outer> unless/without <cond> -> always <cond> before <outer>.

    The one deontic rewrite allowed: conditional equivalence, not
    paraphrase guessing. Any other deontic difference is a mismatch."""
    lowered = re.sub(r"\bnever\s+([^.;]+?)\s+unless\s+([^.;]+)",
                     r"always \2 before \1", lowered)
    lowered = re.sub(r"\bnever\s+([^.;]+?)\s+without\s+([^.;]+)",
                     r"always \2 before \1", lowered)
    return lowered


def _split_sentences(text):
    # "." splits only before a capital, so "lane-state.py claim" survives.
    parts = re.split(r"(?<=[?!;])\s+|(?<=\.)\s+(?=[A-Z])", text)
    out = []
    for p in parts:
        p = p.strip().rstrip(".").strip()
        if p:
            out.append(p)
    return out


def _split_trigger(frag):
    m = re.match(r"\s*(when|whenever|before|after|if|unless)\b", frag)
    if m and "," in frag:
        trig, _, rest = frag.partition(",")
        if rest.strip():
            return [("trigger", trig.strip()), ("other", rest.strip())]
    return [("other", frag)]


def _split_logical(sent):
    out = []
    for frag in re.split(r",\s+and\s+", sent):
        frag = frag.strip()
        if not frag:
            continue
        m = re.search(r"\b(because|since)\b", frag)
        if m:
            head, reason = frag[:m.start()].strip(), frag[m.start():].strip()
            if head:
                out.extend(_split_trigger(head))
            out.append(("reason", reason))
        else:
            out.extend(_split_trigger(frag))
    return out


def _has_predicate(raw):
    toks = _raw_tokens(raw)
    for t in toks:
        if t in _PREDICATE_WORDS or _canon_one(t) in _VERB_LEXICON:
            return True
    return False


def _small_density(raw):
    toks = _tokens(raw)
    if not toks:
        return 0.0
    return sum(1 for t in toks if t in _SMALL_MARKERS) / len(toks)


def _classify(hints):
    out = []
    core_seen = False
    for hint, raw in hints:
        if hint in ("enforcement", "reason", "trigger"):
            out.append((hint, raw))
            continue
        if not _has_predicate(raw):
            out.append(("filler", raw))
        elif _small_density(raw) >= 0.5:
            out.append(("teeth", raw))
        elif not core_seen:
            out.append(("core", raw))
            core_seen = True
        else:
            out.append(("secondary", raw))
    return out


def _core_action_object(core_raw):
    raw_toks = _raw_tokens(core_raw)
    verb_idx = None
    action = None
    for i, t in enumerate(raw_toks):
        c = _canon_one(t)
        if c in _VERB_LEXICON:
            verb_idx, action = i, c
            break
    if verb_idx is None:
        return None, set()
    be_before = any(t in ("is", "are", "was", "were", "be", "been")
                    for t in raw_toks[:verb_idx])
    if be_before:
        obj = _concepts(" ".join(raw_toks[:verb_idx]))
    else:
        after = []
        for t in raw_toks[verb_idx + 1:]:
            c = _canon_one(t)
            # Raw prepositions stop the scan: "in/of/to/..." are stopwords
            # in _tokens, so they never appear in concept sets — but they
            # ARE present in the raw token stream scanned here.
            if (c in _STOP_PREP or c in _VERB_LEXICON
                    or t in ("in", "of", "to", "on", "from", "with", "at",
                             "by", "for", "as")):
                break
            after.append(t)
        obj = _concepts(" ".join(after))
    return action, obj


def _deontic(core_raw):
    if core_raw is None:
        return "NONE"
    if re.search(r"\bnever\b", core_raw):
        return "NEVER"
    if re.search(r"\balways\b", core_raw):
        return "ALWAYS"
    return "NONE"


def _polarity(reason_raw):
    if reason_raw is not None and _NEG_RE.search(reason_raw):
        return "NEG"
    if reason_raw is None:
        return None
    return "ASSERTED"


def _analyze(text):
    # Sentence-split on the ORIGINAL-case text: the splitter uses ". " +
    # capital as the boundary signal ("spawning. A failed..."), and
    # lowercasing first would destroy it (w127 bug: merged sentences
    # fused core+reason, breaking skeleton + object extraction).
    hints = []
    for sent in _split_sentences(text):
        lowered = sent.lower().replace("nonzero", "non-zero")
        for src, dst in sorted(_PHRASE_ALIASES, key=lambda p: -len(p[0])):
            lowered = re.sub(r"\b" + re.escape(src) + r"\b", dst, lowered)
        lowered = _normalize_deontic(lowered)
        if "enforcement:" in lowered:
            before, _, after = lowered.partition("enforcement:")
            if before.strip():
                hints.extend(_split_logical(before))
            hints.append(("enforcement", after.strip()))
        else:
            hints.extend(_split_logical(lowered))
    clauses = _classify(hints)
    core_raw = next((r for k, r in clauses if k == "core"), None)
    reason_raw = next((r for k, r in clauses if k == "reason"), None)
    if reason_raw is None:
        reason_raw = next((r for k, r in clauses if k == "secondary"), None)
    concepts = set()
    for k, r in clauses:
        if k in ("core", "reason", "secondary"):
            concepts |= _concepts(r)
    all_concepts = set(concepts)
    for k, r in clauses:
        if k in ("enforcement", "teeth", "filler"):
            all_concepts |= _concepts(r, strip_markers=True)
    action, obj = _core_action_object(core_raw) if core_raw else (None, set())
    return {"clauses": clauses, "concepts": concepts,
            "all_concepts": all_concepts, "core_action": action,
            "core_object": obj, "deontic": _deontic(core_raw),
            "reason_polarity": _polarity(reason_raw),
            "reason_concepts": _concepts(reason_raw) if reason_raw else set(),
            "has_reason": reason_raw is not None}


def _skeleton_match(old, cand):
    if old["core_action"] is None or cand["core_action"] is None:
        return False
    if (old["deontic"] != "NONE" and cand["deontic"] != "NONE"
            and old["deontic"] != cand["deontic"]):
        return False
    if old["core_action"] != cand["core_action"]:
        return False
    if not old["core_object"] <= cand["core_object"]:
        return False
    if old["reason_polarity"] != cand["reason_polarity"]:
        return False
    if not old["reason_concepts"] <= cand["reason_concepts"]:
        return False
    return True


def semantic_containment(text, existing_lesson_texts, aliases=None):
    """Per-lesson semantic matches: coverage + skeleton + novel + band.

    Returns one dict per existing lesson: {lesson_index, lesson_head,
    coverage, skeleton_match, novel, band}. v1 uses the versioned alias
    table; a custom table raises instead of silently not applying.
    """
    if aliases is not None:
        raise ValueError("custom alias tables not supported in v1 — "
                         "the versioned table (ALIASES_VERSION) is the "
                         "single source; additions need a test pair")
    cand = _analyze(text)
    out = []
    for i, lesson in enumerate(existing_lesson_texts):
        old = _analyze(lesson)
        if old["concepts"]:
            coverage = (len(old["concepts"] & cand["concepts"])
                        / len(old["concepts"]))
        else:
            coverage = 0.0
        skel = _skeleton_match(old, cand)
        novel = len(cand["all_concepts"] - old["all_concepts"])
        if skel and coverage >= 0.75 and novel < 3:
            band = "RED"
        elif skel and coverage >= 0.60:
            band = "GREY"
        else:
            band = "PASS"
        out.append({"lesson_index": i,
                    "lesson_head": lesson[:60],
                    "coverage": round(coverage, 4),
                    "skeleton_match": skel, "novel": novel, "band": band})
    return out


def _best_semantic(matches):
    """Most severe non-PASS match (RED > GREY, tie-break: coverage)."""
    sev = {"RED": 2, "GREY": 1, "PASS": 0}
    best = None
    for m in matches:
        if sev.get(m["band"], 0) == 0:
            continue
        if best is None or (sev[m["band"]], m["coverage"]) > (
                sev[best["band"]], best["coverage"]):
            best = m
    return best


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

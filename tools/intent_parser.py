#!/usr/bin/env python3
"""
Intent Parser — Layer 2 of the Ultimate Decision Machine.

Understanding what the human (or machine) wants, from words.

Input:  natural language intent
        ("What's the most intelligent thing to do next?",
         "Should this merge?", "Which of these three designs?")
Output: structured intent:
        {objective, constraints, decision_weight, reversibility, stakes,
         clarifying_questions, confidence, world_context}

Design principles (from the spec):
  - The machine never asks "how important is this?" It reads the situation
    and knows. (Wisdom Spending Principle as code.)
  - If intent is ambiguous, ask before deciding. Never assume.
  - Constraints come from the standing laws + the situation, not from opinion.
  - Every output carries its confidence and its reasoning in plain words.

Usage:
  python3 tools/intent_parser.py parse "Should PR #2410 merge?"
  python3 tools/intent_parser.py parse --stdin < intent.txt
  python3 tools/intent_parser.py --example

Exit codes:
  0 — intent parsed successfully
  2 — clarifying questions needed (ambiguous input); questions in output
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
BRIEFING_PATH = Path(os.path.expanduser("~/workspace/agent-briefing-master.md"))

# Protected gates — from the standing laws. These always route to a human.
PROTECTED_GATES = [
    "production deploys",
    "database writes",
    "credentials or money",
    "destructive or irreversible actions",
    "security, privacy, consent, or authority changes",
    "constitutional ratification",
]

# ---------------------------------------------------------------------------
# Intent types
# ---------------------------------------------------------------------------
# Each intent type: what it means, how to detect it, what objective it implies.

INTENT_TYPES = {
    "what_next": {
        "description": "Asking what to do next — the highest-value action",
        "patterns": [
            r"what(?:'s| is) the most intelligent thing",
            r"what should (?:i|we) do next",
            r"what(?:'s| is) next",
            r"highest.{0,20}(?:value|priority)",
            r"where should (?:i|we) focus",
        ],
        "objective": "Identify the single highest-value action available right now",
    },
    "should_merge": {
        "description": "Asking whether a PR/branch should merge",
        "patterns": [
            r"should (?:this|that|it|#\d+|PR\s*#?\d+|the branch|the pull request).{0,30}merge",
            r"should (?:the\s+)?pull[\s\-]+request\s*#?\d*.{0,30}merge",
            r"pull[\s\-]+request\s*#?\d*\s+should\s+merge",
            r"(?:can|may) (?:this|that|it|#\d+|PR\s*#?\d+).{0,30}merge",
            r"is (?:this|that|it|#\d+|PR\s*#?\d+).{0,30}ready to merge",
            r"merge (?:this|that|it|the branch|#?\d+|PR\s*#?\d+|pull[\s\-]+request(?:\s*#?\d+)?)",
        ],
        "objective": "Determine whether the change is safe and ready to merge",
    },
    "which_option": {
        "description": "Choosing between explicit options",
        "patterns": [
            r"which (?:of these|one|option)",
            r"\b[A-E]\b\s*(?:vs\.?|or|/)\s*\b[A-E]\b",
            r"choose between",
            r"better.{0,20}(?:this|that|these)",
            r"\bcompare\b",
        ],
        "objective": "Rank the given options and recommend the best one",
    },
    "what_blocking": {
        "description": "Asking what's stuck or blocking progress",
        "patterns": [
            r"what(?:'s| is) blocking",
            r"what(?:'s| is) stuck",
            r"why (?:is|are).{0,30}(?:stuck|blocked|not moving)",
            r"bottleneck",
        ],
        "objective": "Identify what's blocking progress and how to unblock it",
    },
    "status_check": {
        "description": "Asking for the current state of something",
        "patterns": [
            r"what(?:'s| is) the (?:state|status)",
            r"how (?:is|are).{0,30}(?:doing|going)",
            r"where (?:are we|do we stand)",
            r"give me (?:an? )?(?:update|summary|overview)",
        ],
        "objective": "Report the current true state of the thing asked about",
    },
    "should_build": {
        "description": "Asking whether to build or ship something",
        "patterns": [
            r"should (?:i|we) build",
            r"(?:build|create|make) (?:this|that|it|a|an)",
            r"is it worth building",
            r"should (?:i|we) (?:deploy|ship|release|launch)",
            r"(?:deploy|ship|release) (?:this|that|it|the)",
        ],
        "objective": "Determine whether the thing is worth building and how",
    },
}


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
    # Check freshness of each section
    for name, section in model.get("sections", {}).items():
        status = section.get("status", "UNKNOWN")
        if status in ("STALE", "UNKNOWN"):
            warnings.append(f"world model section '{name}' is {status}")
    return model, warnings


def extract_world_context(model, intent_type):
    """Pull the world-model context relevant to this intent type."""
    if not model:
        return {"available": False, "note": "no world model loaded"}
    sections = model.get("sections", {})
    ctx = {"available": True}

    # Always include: tip freshness, lane states summary
    tip = sections.get("tip", {})
    ctx["tip"] = {
        "sha": (tip.get("sha") or "")[:8],
        "status": tip.get("status", "UNKNOWN"),
    }

    lanes = sections.get("lanes", {})
    if lanes.get("status") == "OK":
        lane_data = lanes.get("lanes", {})
        ctx["lanes"] = {
            name: info.get("state", "UNKNOWN")
            for name, info in lane_data.items()
        }

    # Intent-specific context
    if intent_type in ("should_merge", "what_next", "which_option"):
        prs = sections.get("prs", {})
        if prs.get("status") == "OK":
            pr_list = prs.get("prs", [])
            ctx["open_prs"] = [
                {"number": p.get("number"), "title": (p.get("title") or "")[:60],
                 "mergeable": p.get("mergeable")}
                for p in pr_list[:10]
            ]
            ctx["open_pr_count"] = prs.get("count", len(pr_list))

    if intent_type in ("what_next", "what_blocking"):
        mission = sections.get("mission", {})
        if mission.get("status") == "OK":
            ctx["mission_priorities"] = mission.get("priorities", [])[:5]

    return ctx


# ---------------------------------------------------------------------------
# Intent classification
# ---------------------------------------------------------------------------

def classify_intent(text):
    """Match input text to an intent type. Returns (type, confidence, matches).

    For long inputs, the first sentence carries the question — classify on it,
    but keep the full text for reference extraction."""
    text_lower = text.lower().strip()
    # First sentence is the question; the rest is context
    first = re.split(r"[.?!]\s+", text_lower, maxsplit=1)[0]
    best_type = None
    best_score = 0.0
    match_detail = None

    for itype, spec in INTENT_TYPES.items():
        for pattern in spec["patterns"]:
            # Try first sentence first (the question), then full text
            for candidate in (first, text_lower):
                m = re.search(pattern, candidate, re.IGNORECASE)
                if m:
                    # Score by match length relative to input (longer match = more specific)
                    score = len(m.group(0)) / max(len(candidate), 1)
                    # Bonus for matching early in the text (intent usually stated first)
                    score += 0.1 * (1 - m.start() / max(len(candidate), 1))
                    # Bonus for matching in the first sentence (the actual question)
                    if candidate is first:
                        score += 0.15
                    if score > best_score:
                        best_score = score
                        best_type = itype
                        match_detail = m.group(0)
                    break  # first-sentence match wins for this pattern

    # Normalize confidence: strong pattern match → high confidence
    confidence = min(0.95, best_score + 0.4) if best_type else 0.0
    return best_type, confidence, match_detail


def extract_references(text):
    """Extract concrete references: PR numbers, branch names, quoted options.

    PR numbers come from explicit markers (#2412, PR 2412, pull request 2412)
    or from bare numbers next to merge/shipping verbs ("merge 2412").
    Bare 4-digit numbers that look like years (1900-2100) are never treated
    as PR references — a year is not a pull request. Explicit markers always
    win: "PR #1999" is a PR even though 1999 looks like a year."""
    refs = {}
    pr_nums = []
    seen = set()

    def add(n):
        if n not in seen:
            seen.add(n)
            pr_nums.append(n)

    # Explicit markers — unambiguous
    for pattern in (r"#(\d{3,5})",
                    r"\bPR\s*#?\s*(\d{3,5})\b",
                    r"\bpull[\s\-]+request\s*#?\s*(\d{3,5})\b"):
        for m in re.finditer(pattern, text, re.IGNORECASE):
            add(int(m.group(1)))

    # Bare numbers only next to merge/shipping verbs — never years.
    # Lists work too: "merge 2412 and 2413".
    for m in re.finditer(
            r"\b(?:merge|ship|deploy|close|rebase|land)\s+(?:PR\s+)?"
            r"(\d{4}(?:\s*(?:,|and|&)\s*\d{4})*)\b",
            text, re.IGNORECASE):
        for num in re.split(r"\s*(?:,|and|&)\s*", m.group(1)):
            n = int(num)
            if not 1900 <= n <= 2100:
                add(n)

    if pr_nums:
        refs["pr_numbers"] = pr_nums
    branches = re.findall(r"\bnaya5/[\w\-\.]+", text)
    if branches:
        refs["branches"] = branches
    # Quoted options ("A", "B", "C" or named options)
    quoted = re.findall(r'"([^"]{1,60})"', text)
    if quoted:
        refs["quoted_options"] = quoted
    return refs


def ground_references(refs, world_ctx):
    """Check references against the world model. Flag what doesn't exist.
    A PR number that isn't in the world model is either wrong or the model
    is stale — either way, the decision-maker needs to know."""
    grounded = {"prs": [], "branches": [], "warnings": []}
    open_prs = {}
    if world_ctx.get("available"):
        for p in world_ctx.get("open_prs", []):
            open_prs[p.get("number")] = p

    for n in refs.get("pr_numbers", []):
        if n in open_prs:
            p = open_prs[n]
            grounded["prs"].append({
                "number": n,
                "title": p.get("title", ""),
                "mergeable": p.get("mergeable"),
                "found": True,
            })
        else:
            grounded["prs"].append({"number": n, "found": False})
            if world_ctx.get("available"):
                grounded["warnings"].append(
                    f"PR #{n} not found in world model "
                    f"({world_ctx.get('open_pr_count', '?')} open PRs tracked) — "
                    "number may be wrong, or the world model is stale."
                )
    for b in refs.get("branches", []):
        grounded["branches"].append({"name": b, "found": "unknown"})
    return grounded


# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------
# Negation detection (F2) — a negated ACTION intent must never be silently
# executed. Recommending the opposite of what the user asked is a correctness
# defect, so negated intents always become clarifying questions (exit 2).
#
# L236 HYPOTHESIS CHANGE (fix-pass #3 — validator-written reframe):
#   TRIED: negation within N tokens before the intent's action verb
#     (adjacency regex -> token-window matcher). Three attempts, all below
#     9.0 on independent validation.
#   WHY IT FAILED: negation isn't always pre-verbal. Trailing negations
#     ("merge 2412? absolutely not") and subject negations ("Nobody merge
#     2412") escape any pre-verb window BY CONSTRUCTION — no window size
#     fixes this.
#   TRY INSTEAD: sentence-level negation signal. ANY negation token in a
#     clause flips the intent to a clarifying question (exit 2), with an
#     EXPLICIT ALLOWLIST of non-negating uses. Verb proximity is not the
#     gate; clause-level scoping + bare-negation cover the space, which
#     also closes the old documented boundary. (Mechanism note, fix-pass
#     #4: "do not, under absolutely any circumstances whatsoever, deploy"
#     classifies to NO intent, so it exits 2 via generic ambiguity rather
#     than the negated-action path — same safe exit, different mechanism.
#     Do not claim the negated-action path handles it.)
#   WHY DIFFERENT AT THE ROOT: stops anchoring on verb position entirely.
#     The old approach asked "is the negation near the verb?"; the new
#     approach asks "does this clause contain a negation that isn't
#     allowlisted?" Fail-closed by design; the allowlist is enumerated,
#     not heuristic.
#
# How it works, per clause (clauses split on . ! ? ; , and "but"):
#   1. Tag/ask questions are allowlisted ("Shouldn't we merge?",
#      "merge or not?", "whether or not", "don't you think we should
#      merge?") — asking, not negating.
#   2. "but"-override: only the clause after the last "but" is read
#      ("don't merge yet, but prepare the notes" — the notes govern).
#   3. Bare negations flip ("no", "absolutely not", "never ever",
#      "not a chance", "no way") — a trailing answer to the previous
#      clause's action. Trailing opinion-answers ("I don't think so")
#      flip too.
#   4. Otherwise the negation must scope the intent's OWN action verb
#      ("don't merge" flips should_merge, never should_build).
#   5. A clause with negation but no action verb at all is a problem
#      description ("it's not working", "nothing is ready") — not flipped.
# Known trade-off (fail closed): contradictory multi-clause input
# ("Don't merge. Actually, merge it.") asks instead of deciding. A false
# question is safe; a false proceed is a correctness defect.
# Hedged negations ("I don't think we should merge X") are asked, not
# silently evaluated — the user expressed doubt; evaluating as a straight
# request could recommend the opposite of their leaning. Asking costs a
# sentence; being wrong costs trust.
# ---------------------------------------------------------------------------

ACTION_INTENTS = ("should_merge", "should_build")

# Any of these tokens is a negation signal: no / not / never / none /
# nobody / no one / neither / n't-contractions. Fail-closed: presence
# flips the intent unless explicitly allowlisted below.
NEGATION_WORDS = frozenset({
    "no", "not", "never", "none", "nobody", "neither", "nor", "nope",
    "don't", "dont", "doesn't", "doesnt", "didn't", "didnt",
    "won't", "wont", "wouldn't", "wouldnt", "can't", "cant",
    "cannot", "shouldn't", "shouldnt", "couldn't", "couldnt",
    "isn't", "isnt", "aren't", "arent", "wasn't", "wasnt",
    "weren't", "werent", "hasn't", "hasnt", "haven't", "havent",
    "hadn't", "hadnt", "ain't", "aint",
    "avoid", "against",
})

# Words that can accompany a bare negation without adding propositional
# content: "absolutely not", "never ever", "not a chance", "no way",
# "actually, don't". Articles are transparent; refusal nouns and discourse
# markers are unambiguous.
_NEGATION_BARE_OK = frozenset({
    "absolutely", "absolute", "definitely", "certainly", "really", "ever",
    "at", "all", "whatsoever",
    "a", "an", "the",
    "way", "chance", "deal", "dice",
    "actually", "well", "oh", "um", "uh", "hmm",
    # idiomatic rejections: "not on my watch"
    "on", "my", "your", "his", "her", "our", "their", "watch",
    # elliptical verbal negator: "merge 2412? do not" — the "do" is the
    # auxiliary of an elided "do not <verb>"; without it the standalone
    # "do not" is not recognized as a bare negation (fix-pass #4).
    "do",
    # fix-pass #5: companions for the validator's four misses —
    # "hard no", "under no circumstances", "not happening". "under" is a
    # bare preposition here: it can only matter inside a clause that
    # already contains a negation word, so it cannot create a flip alone.
    "hard", "under", "circumstances", "happening",
})

# Rejection nouns: a verbless trailing fragment like "merge 2412? veto"
# IS the rejection — no negation word needed. Kept tight on purpose:
# only the noun forms, only as bare fragments. The verb forms
# ("veto the merge", "I veto the merge") are a known boundary, not
# handled here (fix-pass #5).
_REJECTION_NOUNS = frozenset({
    "veto", "vetoes",
    "rejection", "denial",
})

ACTION_VERBS = frozenset({
    "merge", "merges", "merging", "merged",
    "ship", "ships", "shipping", "shipped",
    "build", "builds", "building", "built",
    "deploy", "deploys", "deploying", "deployed",
    "release", "releases", "releasing", "released",
    "launch", "launches", "launching", "launched",
})

# The action verbs each action-intent is actually about. The negation must
# scope the intent's OWN verb — "don't merge, just build it" negates the
# merge, not the build, so a should_build intent must not flip on it.
INTENT_VERBS = {
    "should_merge": frozenset({"merge", "merges", "merging", "merged"}),
    "should_build": frozenset({
        "build", "builds", "building", "built",
        "ship", "ships", "shipping", "shipped",
        "deploy", "deploys", "deploying", "deployed",
        "release", "releases", "releasing", "released",
        "launch", "launches", "launching", "launched",
    }),
}

# Ask-forms: a leading contracted negation + pronoun/determiner
# ("Shouldn't we merge?", "Can't we ship Friday?", "Won't it merge?") is
# ASKING, not negating. NOTE: "don't"/"didn't" are NOT here — they get
# their own narrower patterns below, because "don't you dare merge" is a
# command (must flip) while "don't you think...?" is asking.
_ASK_LEAD = re.compile(
    r"^(?:shouldn't|should\s+not|won't|will\s+not|can't|cannot|"
    r"isn't|is\s+not|aren't|are\s+not|wasn't|was\s+not|"
    r"weren't|were\s+not|haven't|have\s+not|hasn't|has\s+not|"
    r"hadn't|had\s+not)\s+"
    r"(?:i|we|you|they|he|she|it|this|that|these|those|the)\b"
)
# "don't you think/agree/feel...?" asks for an opinion — not a negation.
# Narrow: "don't you DARE merge" / "don't ever merge" still flip.
_ASK_DONT_OPINION = re.compile(
    r"^(?:don't|do\s+not)\s+(?:you|we)\s+"
    r"(?:think|agree|feel|believe|reckon|suppose|need|want|know)\b"
)
# "didn't we merge already?" asks about the past — not a negation.
# (Mid-sentence "we didn't merge it" still flips: fail-closed.)
_ASK_DID = re.compile(
    r"^(?:didn't|did\s+not)\s+(?:i|we|you|they|he|she|it)\b"
)
# Trailing tag ("merge or not?", "should we ship or not") and the
# "whether or not" ask-form — all asking, not negating.
_TAG_TAIL = re.compile(r"\bor\s+not\??\s*$")
_WHETHER = re.compile(r"\bwhether\s+or\s+not\b")
# Trailing opinion-answer ("I don't think so", "I don't believe it") —
# an anaphoric no to the previous clause's action. Distinct from
# _ASK_OPINION ("don't YOU think...?"), which asks.
_TRAILING_NO = re.compile(
    r"^(?:i|we)\s+(?:do\s+not|don't|doesn't|wouldn't|can't)\s+"
    r"(?:think|believe|feel|reckon|suppose)\s+(?:so|it|that)\.?$"
)


# Common verbs (beyond ACTION_VERBS) for detecting whether a
# comma-fragment is a verbless parenthetical.
_COMMON_VERBS = frozenset({
    "is", "are", "was", "were", "be", "been", "being",
    "have", "has", "had", "do", "does", "did",
    "will", "would", "shall", "can", "could", "should",
    "may", "might", "must",
})

# Fragment-initial words marking a parenthetical ("under any
# circumstances", "in my opinion", "really").
_PAREN_START = frozenset({
    "under", "in", "on", "at", "by", "with", "without", "for",
    "from", "of", "over", "through", "during", "between", "among",
    "against", "about", "into", "upon", "within", "across",
    "along", "despite",
    "absolutely", "definitely", "certainly", "really", "ever",
})


def _has_verb(tokens):
    return any(t in ACTION_VERBS or t in _COMMON_VERBS for t in tokens)


# Standalone discourse particles: "No, merge 2412" answers prior
# discourse, then commands. Unlike verbal negators ("don't,", "never,")
# they do not dangle-attach to the next comma-fragment.
_DISCOURSE_NO = frozenset({"no", "nope", "nah"})


def _negation_dangling(tokens):
    """True when the chunk's last negation has nothing after it but
    parenthetical material — 'do not', or 'do not, under any
    circumstances'. The negation is still looking for its verb, so the
    next comma-fragment belongs with this chunk. A complete negated
    proposition ('not a problem', "it's not working") is NOT dangling:
    its negation is followed by real content."""
    last_neg = -1
    for i, t in enumerate(tokens):
        if t in NEGATION_WORDS:
            last_neg = i
    if last_neg == -1:
        return False
    rest = tokens[last_neg + 1:]
    if not rest:
        # A tag-tail ("merge or not") is asking, not negating.
        if len(tokens) >= 2 and tokens[-2:] == ["or", "not"]:
            return False
        # A lone discourse particle ("No, ...") answers prior discourse;
        # it is not a verbal negator looking for its verb.
        if len(tokens) == 1 and tokens[0] in _DISCOURSE_NO:
            return False
        return True  # ends with the negation: 'do not'
    return (not any(t in NEGATION_WORDS for t in rest)
            and not _has_verb(rest)
            and rest[0] in _PAREN_START)


def _split_clauses(text):
    """Split into clauses on hard boundaries (. ! ? ;) and 'but', then
    soft-split on commas, re-attaching comma-fragments whose negation is
    still dangling ('do not, under any circumstances, deploy' stays
    together; "it's not working, should we merge?" stays apart).
    Returns (clauses, has_but)."""
    has_but = bool(re.search(r"\bbut\b", text, re.IGNORECASE))
    text = text.replace("\u2014", ",").replace("\u2013", ",")
    hard = [p.strip()
            for p in re.split(r"[.!?;]+|\bbut\b", text, flags=re.IGNORECASE)
            if p.strip()]
    clauses = []
    for h in hard:
        frags = [f.strip() for f in h.split(",") if f.strip()]
        i = 0
        while i < len(frags):
            cur = frags[i]
            toks = re.findall(r"[a-z']+", cur.lower())
            while i + 1 < len(frags) and _negation_dangling(toks):
                i += 1
                cur = cur + ", " + frags[i]
                toks = re.findall(r"[a-z']+", cur.lower())
            clauses.append(cur)
            i += 1
    return clauses, has_but


_VOTE_VERBS = frozenset({"vote", "votes", "voted", "voting"})
_SUBJECTS = frozenset({"i", "we", "you", "they", "he", "she"})


def _is_bare_negation(tokens):
    """True when the clause is ONLY a negation (+ intensifiers / articles /
    refusal nouns): 'no', 'absolutely not', 'never ever', 'not a chance',
    'no way'. A trailing answer to the previous clause's action.
    'I vote no' counts: voting 'no' IS the rejection.
    Fix-pass #5: a clause of ONLY rejection nouns ('veto', 'my veto',
    'absolute veto') also counts — a verbless trailing fragment naming the
    rejection IS the rejection."""
    toks = list(tokens)
    if len(toks) >= 2 and toks[0] in _SUBJECTS and toks[1] in _VOTE_VERBS:
        toks = toks[2:]
    has_neg = any(t in NEGATION_WORDS for t in toks)
    has_rejection = any(t in _REJECTION_NOUNS for t in toks)
    return (bool(toks)
            and (has_neg or has_rejection)
            and all(t in NEGATION_WORDS or t in _NEGATION_BARE_OK
                    or t in _REJECTION_NOUNS for t in toks))


def _is_tag_question(clause):
    """Ask-forms that contain negation words but aren't negating."""
    c = clause.strip().lower()
    return bool(_ASK_LEAD.match(c) or _ASK_DONT_OPINION.match(c)
                or _ASK_DID.match(c) or _TAG_TAIL.search(c)
                or _WHETHER.search(c))


# Heavy, concrete action verbs for the nearest-verb tiebreaker. Light
# "transmission" verbs (want, think, dare, try, need, worry) are DELIBERATELY
# absent: they pass the negation through to the main verb ("I don't want
# to merge" negates the merge, not the wanting), so the tiebreaker must
# see through them.
_GENERAL_VERBS = frozenset({
    "break", "breaks", "breaking", "broke", "broken",
    "fix", "fixes", "fixing", "fixed",
    "stop", "stops", "stopping", "stopped",
    "start", "starts", "starting", "started",
    "run", "runs", "running", "ran",
    "test", "tests", "testing", "tested",
    "check", "checks", "checking", "checked",
    "update", "updates", "updating", "updated",
    "change", "changes", "changing", "changed",
    "remove", "removes", "removing", "removed",
    "delete", "deletes", "deleting", "deleted",
    "add", "adds", "adding", "added",
    "create", "creates", "creating", "created",
    "close", "closes", "closing", "closed",
    "open", "opens", "opening", "opened",
    "push", "pushes", "pushing", "pushed",
    "pull", "pulls", "pulling", "pulled",
    "revert", "reverts", "reverting", "reverted",
    "block", "blocks", "blocking", "blocked",
    "touch", "touches", "touching", "touched",
    "modify", "modifies", "modifying", "modified",
    "edit", "edits", "editing", "edited",
    "write", "writes", "writing", "wrote", "written",
    "send", "sends", "sending", "sent",
    "publish", "publishes", "publishing", "published",
    "approve", "approves", "approving", "approved",
    "cancel", "cancels", "cancelling", "cancelled",
    "pause", "pauses", "pausing", "paused",
    "restart", "restarts", "restarting", "restarted",
    "disable", "disables", "disabling", "disabled",
    "enable", "enables", "enabling", "enabled",
})
_TIEBREAK_VERBS = ACTION_VERBS | _GENERAL_VERBS


def is_negated_action(text, intent_type):
    """Sentence-level negation signal (fix-pass #3, L236 hypothesis change).

    ANY negation token in a clause flips the intent to a clarifying
    question, unless explicitly allowlisted: tag/ask questions, the
    "but"-override (only the post-"but" clause is read), and problem
    descriptions (negation in a clause with no action verb at all).
    The negation must scope the intent's OWN verb family, via the nearest
    heavy action verb (light verbs like want/think/dare are transparent:
    "I don't want to merge" negates the merge).
    Bare negations ("no", "absolutely not", "no way", "I vote no") flip
    when they trail the action or stand alone; a LEADING bare "no"
    ("No. Merge 2412.") answers prior discourse and the command stands.
    Standalone discourse particles ("No,", "Nah,") never dangle-attach
    across commas; verbal negators ("don't,", "never,") do, as do
    parentheticals ("do not, under any circumstances, deploy").
    Tag-tails ("merge or not") never dangle. Em/en-dashes split like
    commas. Verb proximity is a tiebreaker for ambiguous clauses, not
    the gate.
    """
    verbs = INTENT_VERBS.get(intent_type, ACTION_VERBS)
    clauses, has_but = _split_clauses(text)
    # "but"-override: the clause after the last "but" governs.
    if has_but and len(clauses) > 1:
        clauses = [clauses[-1]]
    # Clause order matters for bare negations: a trailing bare "no"
    # ("merge 2412? absolutely not") rejects the input's own action, but
    # a leading one ("No. Merge 2412.") answers prior discourse and the
    # command stands. Track whether an intent-verb clause precedes each
    # clause; with no verb clause at all ("Actually, don't.") the bare
    # negation still flips, fail-closed.
    clause_tokens = [re.findall(r"[a-z']+", c.strip().lower())
                     for c in clauses]
    verb_before = []
    seen_verb = False
    for toks in clause_tokens:
        verb_before.append(seen_verb)
        if any(t in verbs for t in toks):
            seen_verb = True
    any_verb = seen_verb
    for clause, tokens, vb in zip(clauses, clause_tokens, verb_before):
        c = clause.strip().lower()
        if _is_tag_question(c):
            continue
        # Trailing opinion-answer ("I don't think so") is an anaphoric
        # no to the previous clause's action.
        if _TRAILING_NO.match(c):
            return True
        # Rejection-noun fragments ("merge 2412? veto") carry no negation
        # word but still reach the bare-negation check below (fix-pass #5).
        if (not any(t in NEGATION_WORDS for t in tokens)
                and not any(t in _REJECTION_NOUNS for t in tokens)):
            continue
        # Bare negation answers the previous clause's action — unless it
        # leads the input, where it answers prior discourse instead.
        if _is_bare_negation(tokens):
            if vb or not any_verb:
                return True
            continue
        # Otherwise the negation must scope the intent's own action verb.
        # A clause with no action verb at all is a problem description
        # ("it's not working", "nothing is ready") — not a negated request.
        # Tiebreaker for ambiguous clauses: the negation scopes its NEAREST
        # action verb ("Merge 2412 and don't break anything" must not flip —
        # the "don't" scopes "break", not "merge"). Light verbs (want,
        # think, dare) are invisible to the tiebreaker so "I don't want
        # to merge" still scopes "merge".
        neg_idx = [i for i, t in enumerate(tokens) if t in NEGATION_WORDS]
        verb_idx = [i for i, t in enumerate(tokens) if t in _TIEBREAK_VERBS]
        for ni in neg_idx:
            if not verb_idx:
                continue
            nearest = min(verb_idx, key=lambda vi: abs(vi - ni))
            if tokens[nearest] in verbs:
                return True
    return False


def describe_target(refs):
    """Name the thing a question is about, for plain-words output."""
    if refs.get("pr_numbers"):
        return "PR #" + ", #".join(str(n) for n in refs["pr_numbers"])
    if refs.get("branches"):
        return ", ".join(refs["branches"])
    if refs.get("quoted_options"):
        return ", ".join(f'"{o}"' for o in refs["quoted_options"])
    return "this"


def needs_clarification(*, intent_type, refs, grounded, world_ctx,
                        wm_warnings, confidence, questions, note):
    """Every parse path emits the same schema (F3). Fields that are genuinely
    unknown are honest nulls/empties — downstream layers (option mining,
    evidence scoring) must never KeyError on a clarifying path."""
    return {
        "ok": False,
        "exit_hint": 2,
        "intent_type": intent_type,
        "intent_description": INTENT_TYPES[intent_type]["description"] if intent_type else None,
        "objective": (synthesize_objective(intent_type, "", refs, world_ctx)
                      if intent_type else None),
        "constraints": [],
        "decision_weight": None,
        "weight_reason": None,
        "reversibility": None,
        "stakes": None,
        "references": refs,
        "grounded_references": grounded,
        "world_context": world_ctx,
        "world_warnings": wm_warnings,
        "clarifying_questions": questions,
        "confidence": round(confidence, 2),
        "note": note,
        "parsed_utc": datetime.now(timezone.utc).isoformat(),
    }


# ---------------------------------------------------------------------------
# Ambiguity detection → clarifying questions
# ---------------------------------------------------------------------------

AMBIGUOUS_REFS = ["this", "that", "it", "them", "these", "those"]


def detect_ambiguity(text, intent_type, refs, world_ctx):
    """Return a list of clarifying questions. Empty = no ambiguity."""
    questions = []
    text_lower = text.lower()

    if intent_type is None:
        questions.append(
            "I couldn't tell what kind of decision this is. "
            "Are you asking what to do next, whether something should merge, "
            "which option to choose, what's blocking, or for a status update?"
        )
        return questions

    # Concrete target = something the decision can actually act on
    has_concrete = bool(refs.get("pr_numbers") or refs.get("branches")
                        or refs.get("quoted_options"))
    has_demonstrative = any(
        re.search(r"\b" + w + r"\b", text_lower) for w in AMBIGUOUS_REFS
    )

    # should_merge with no concrete target — never evaluate a mystery merge
    if intent_type == "should_merge" and not has_concrete:
        questions.append(
            "Which PR or branch are you asking about? "
            "Give me the PR number (e.g. #2410) or branch name."
        )
    # Bare demonstratives without concrete references
    elif has_demonstrative and not has_concrete:
        if intent_type == "which_option":
            questions.append(
                "What are the options to choose between? "
                "List them explicitly — I won't guess what 'these' means."
            )
        elif intent_type == "status_check":
            questions.append(
                "Status of what, specifically? A PR, a lane, an area, the whole team?"
            )

    # which_option without at least 2 identifiable options
    if intent_type == "which_option":
        opts = refs.get("quoted_options", [])
        # Letter options only count when explicitly compared: "A vs B", "A or B"
        letter_pairs = re.findall(r"\b([A-E])\b\s*(?:vs\.?|or|/)\s*\b([A-E])\b",
                                  text, re.IGNORECASE)
        total_opts = len(opts) + sum(len(p) for p in letter_pairs)
        if total_opts < 2 and not has_concrete:
            questions.append(
                "I need at least two options to compare. What are they?"
            )

    # should_build without saying what
    if intent_type == "should_build" and len(text.split()) < 6 and not has_concrete:
        questions.append("Build what, exactly? Describe the thing in a sentence.")

    return questions


# ---------------------------------------------------------------------------
# Constraint derivation (from standing laws + situation)
# ---------------------------------------------------------------------------

def derive_constraints(intent_type, refs, world_ctx):
    """Constraints: what can't we do. From laws + situation, not opinion."""
    constraints = []

    # Universal: protected gates always apply
    constraints.append(
        "Protected gates hold: no production deploys, DB writes, credential/money "
        "moves, destructive actions, or security/authority changes without "
        "explicit human authorization."
    )

    if intent_type == "should_merge":
        constraints.append(
            "Merge requires: green CI on the merged tree, independent validation "
            "by a different seat (score ≥ 9.5), intent + scorecard posted, "
            "no team objection. Three honest Builder-Scorer rounds minimum."
        )
        constraints.append(
            "Never merge on a stale tip — re-resolve the live tip at action time."
        )

    if intent_type == "what_next":
        constraints.append(
            "Don't assign the same area to two workers simultaneously. "
            "Don't dispatch into an occupied lane."
        )

    if intent_type == "should_build":
        constraints.append(
            "New infrastructure is frozen until the core proof passes — "
            "build only what proves the mission, not new surface area."
        )

    # If world model shows stale sections, constrain on freshness
    if world_ctx.get("available"):
        tip_status = world_ctx.get("tip", {}).get("status", "UNKNOWN")
        if tip_status != "OK":
            constraints.append(
                f"Live tip state is {tip_status} — re-confirm before acting on tip-dependent work."
            )

    return constraints


# ---------------------------------------------------------------------------
# Decision weight (Wisdom Spending Principle as code)
# ---------------------------------------------------------------------------
# reversibility × stakes → five-minute | standard | foundational
# The machine never asks "how important is this?" It reads the situation.

def infer_reversibility_stakes(intent_type, text, refs):
    """Infer reversibility and stakes from the intent type and wording."""
    text_lower = text.lower()

    # Base values per intent type
    base = {
        "what_next": ("high", "high"),       # reversible (just a plan), high stakes (sets direction)
        "should_merge": ("medium", "high"),  # revertible but costly; high stakes
        "which_option": ("high", "medium"),  # choosing is reversible until acted on
        "what_blocking": ("high", "medium"), # diagnosis is reversible
        "status_check": ("high", "low"),      # read-only, fully reversible
        "should_build": ("low", "high"),      # building commits resources
    }
    reversibility, stakes = base.get(intent_type, ("medium", "medium"))

    # Wording adjustments — explicit signals override base
    if re.search(r"\b(urgent|emergency|critical|asap|now)\b", text_lower):
        # Urgency doesn't change reversibility, but raises stakes one notch
        stakes = {"low": "medium", "medium": "high", "high": "consequential"}.get(stakes, stakes)
    if re.search(r"\b(production|deploy|live|database|money|payment)\b", text_lower):
        reversibility = "low"
        stakes = "consequential"
    if re.search(r"\b(draft|explore|spike|what if|idea)\b", text_lower):
        reversibility = "high"
        if stakes == "high":
            stakes = "medium"
    if re.search(r"\b(constitution|ratif|law change|authority)\b", text_lower):
        reversibility = "low"
        stakes = "consequential"

    return reversibility, stakes


def classify_weight(reversibility, stakes):
    """Wisdom Spending Principle: reversibility × stakes → weight tier."""
    # Foundational: irreversible, or consequential stakes, or both
    if reversibility == "low" or stakes == "consequential":
        return ("foundational",
                "the action is hard to undo or the stakes are consequential — "
                "full analysis, and a human reviews before acting")
    # Five-minute: fully reversible and low stakes
    if reversibility == "high" and stakes == "low":
        return ("five-minute",
                "fully reversible and low stakes — decide fast and move")
    # Standard: everything else
    return ("standard",
            "reversible enough to correct, stakes enough to think — "
            "reason it through once, then act")


# ---------------------------------------------------------------------------
# Objective synthesis (plain words)
# ---------------------------------------------------------------------------

def synthesize_objective(intent_type, text, refs, world_ctx):
    """State the objective in one plain sentence."""
    if intent_type is None:
        return "Clarify what is being asked before deciding anything"

    base = INTENT_TYPES[intent_type]["objective"]

    # Ground it in concrete references when present
    extras = []
    if refs.get("pr_numbers"):
        extras.append("PR #" + ", #".join(str(n) for n in refs["pr_numbers"]))
    if refs.get("branches"):
        extras.append(", ".join(refs["branches"]))
    if extras:
        return f"{base} — specifically: {'; '.join(extras)}"
    return base


# ---------------------------------------------------------------------------
# Main parse pipeline
# ---------------------------------------------------------------------------

def parse_intent(text):
    """Full pipeline: text → structured intent. Never throws on bad input."""
    text = (text or "").strip()

    # 1. Load world model first (local cache only — no network here), so every
    #    path below can emit the same schema.
    model, wm_warnings = load_world_model()
    no_model_ctx = ({"available": False, "note": "no world model loaded"}
                    if model is None else extract_world_context(model, None))

    if not text:
        return needs_clarification(
            intent_type=None, refs={},
            grounded={"prs": [], "branches": [], "warnings": []},
            world_ctx=no_model_ctx, wm_warnings=wm_warnings, confidence=0.0,
            questions=["You didn't say anything. What do you want to decide?"],
            note="Empty input — nothing to parse.",
        )

    # 2. Classify intent
    intent_type, confidence, match_detail = classify_intent(text)

    # 3. Extract references
    refs = extract_references(text)

    # 4. World context relevant to this intent
    world_ctx = extract_world_context(model, intent_type)

    # 4b. Ground references against the world model
    grounded = ground_references(refs, world_ctx)

    # 5. Negated action intent — never silently proceed (correctness hazard).
    #    "I don't want to merge PR 2412" must not become a merge evaluation.
    if intent_type in ACTION_INTENTS and is_negated_action(text, intent_type):
        action_word = "merge" if intent_type == "should_merge" else "build or ship"
        target = describe_target(refs)
        questions = [
            f"It sounds like you don't want to {action_word} {target}. "
            "I won't proceed on a negated request. What would you like instead — "
            "leave it as-is, change something first, or take a different action?"
        ]
        if not (refs.get("pr_numbers") or refs.get("branches")):
            questions.append(
                f"Also: {action_word} what, exactly? Give me the PR number or branch."
            )
        return needs_clarification(
            intent_type=intent_type, refs=refs, grounded=grounded,
            world_ctx=world_ctx, wm_warnings=wm_warnings,
            confidence=confidence, questions=questions,
            note="Negated action intent — proceeding would recommend the opposite "
                 "of what was asked. Asking instead of assuming.",
        )

    # 6. Ambiguity check — ask before deciding, never assume
    questions = detect_ambiguity(text, intent_type, refs, world_ctx)
    if questions:
        return needs_clarification(
            intent_type=intent_type, refs=refs, grounded=grounded,
            world_ctx=world_ctx, wm_warnings=wm_warnings,
            confidence=confidence, questions=questions,
            note="Ambiguous input — answering would require guessing. Ask first.",
        )

    # 7. Derive constraints (laws + situation)
    constraints = derive_constraints(intent_type, refs, world_ctx)

    # 8. Infer reversibility × stakes → decision weight (Wisdom Spending)
    reversibility, stakes = infer_reversibility_stakes(intent_type, text, refs)
    weight, weight_reason = classify_weight(reversibility, stakes)

    # 9. Synthesize objective in plain words
    objective = synthesize_objective(intent_type, text, refs, world_ctx)

    result = {
        "ok": True,
        "exit_hint": 0,
        "intent_type": intent_type,
        "intent_description": INTENT_TYPES[intent_type]["description"],
        "objective": objective,
        "constraints": constraints,
        "decision_weight": weight,
        "weight_reason": weight_reason,
        "reversibility": reversibility,
        "stakes": stakes,
        "references": refs,
        "grounded_references": grounded,
        "world_context": world_ctx,
        "world_warnings": wm_warnings,
        "clarifying_questions": [],
        "confidence": round(confidence, 2),
        "note": None,
        "parsed_utc": datetime.now(timezone.utc).isoformat(),
    }

    # Human review flag for foundational decisions
    if weight == "foundational":
        result["human_review_recommended"] = True
        result["note"] = (
            "Foundational weight: full analysis required, and a human "
            "should review before acting."
        )

    return result


def plain_words(result):
    """Render the parsed intent in plain words for humans."""
    if not result.get("ok"):
        lines = ["I need clarification before I can parse this intent:"]
        for q in result.get("clarifying_questions", []):
            lines.append(f"  • {q}")
        return "\n".join(lines)

    lines = [
        f"Intent: {result['intent_description']}",
        f"Objective: {result['objective']}",
        f"Weight: {result['decision_weight']} — {result['weight_reason']}",
        f"(reversibility: {result['reversibility']}, stakes: {result['stakes']}, "
        f"confidence: {result['confidence']})",
    ]
    # Grounded references — what the world model says about named things
    grounded = result.get("grounded_references", {})
    for p in grounded.get("prs", []):
        if p.get("found"):
            lines.append(
                f"PR #{p['number']}: \"{p.get('title', '')[:60]}\" "
                f"(mergeable: {p.get('mergeable')})"
            )
        else:
            lines.append(f"PR #{p['number']}: not found in world model")
    for w in grounded.get("warnings", []):
        lines.append(f"  ⚠ {w}")
    lines.append("Constraints:")
    for c in result["constraints"]:
        lines.append(f"  • {c}")
    if result.get("human_review_recommended"):
        lines.append("⚠ Human review recommended before acting on this decision.")
    if result.get("world_warnings"):
        lines.append("World-model warnings:")
        for w in result["world_warnings"]:
            lines.append(f"  • {w}")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

EXAMPLE_INTENTS = [
    "What's the most intelligent thing to do next?",
    "Should PR #2410 merge?",
    "Which of these three designs is best: \"minimal\", \"full\", \"hybrid\"?",
    "What's blocking the team right now?",
    "What's the status of the decision engine work?",
    "Should we build a dashboard for the ledger?",
    "merge it",
]


def cmd_parse(args):
    if args.stdin:
        text = sys.stdin.read()
    elif args.text:
        text = " ".join(args.text)
    else:
        print("usage: intent_parser.py parse \"<intent text>\"  (or --stdin)",
              file=sys.stderr)
        sys.exit(1)
    result = parse_intent(text)
    if args.plain:
        print(plain_words(result))
    else:
        print(json.dumps(result, indent=2))
    sys.exit(result.get("exit_hint", 0))


def cmd_example(args):
    for ex in EXAMPLE_INTENTS:
        print(f"---\nInput: {ex}")
        result = parse_intent(ex)
        print(plain_words(result))
        print()


def main():
    import argparse
    ap = argparse.ArgumentParser(
        description="Intent Parser — Layer 2 of the Ultimate Decision Machine.")
    sub = ap.add_subparsers(dest="cmd")

    p_parse = sub.add_parser("parse", help="Parse a natural-language intent")
    p_parse.add_argument("text", nargs="*", help="The intent text")
    p_parse.add_argument("--stdin", action="store_true",
                         help="Read intent from stdin")
    p_parse.add_argument("--plain", action="store_true",
                         help="Plain-words output instead of JSON")
    p_parse.set_defaults(func=cmd_parse)

    p_ex = sub.add_parser("--example", help="Show example parses")
    p_ex.set_defaults(func=cmd_example)

    # Bare-text shortcut: intent_parser.py "some intent" — argparse would
    # reject this as an invalid subcommand choice, so route it before parsing.
    raw = sys.argv[1:]
    if raw and not raw[0].startswith("-") and raw[0] != "parse":
        cmd_parse(argparse.Namespace(text=raw, stdin=False, plain=True))
        return

    args = ap.parse_args()
    if not getattr(args, "cmd", None):
        # Allow: intent_parser.py "some intent"  (bare text = parse)
        raw = sys.argv[1:]
        if raw and not raw[0].startswith("-"):
            args.cmd = "parse"
            args.text = raw
            args.stdin = False
            args.plain = True
            args.func = cmd_parse
        else:
            ap.print_help()
            sys.exit(1)
    args.func(args)


if __name__ == "__main__":
    main()

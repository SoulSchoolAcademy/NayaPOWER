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
            r"should (?:this|that|it|PR\s*#?\d+|the branch).{0,30}merge",
            r"(?:can|may) (?:this|that|it|PR\s*#?\d+).{0,30}merge",
            r"is (?:this|that|it|PR\s*#?\d+).{0,30}ready to merge",
            r"merge (?:this|that|it|PR\s*#?\d+)",
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
    """Extract concrete references: PR numbers, branch names, quoted options."""
    refs = {}
    pr_nums = re.findall(r"#(\d{3,5})", text)
    if pr_nums:
        refs["pr_numbers"] = [int(n) for n in pr_nums]
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
    """Extract concrete references: PR numbers, branch names, quoted options."""
    refs = {}
    pr_nums = re.findall(r"#(\d{3,5})", text)
    if pr_nums:
        refs["pr_numbers"] = [int(n) for n in pr_nums]
    branches = re.findall(r"\bnaya5/[\w\-\.]+", text)
    if branches:
        refs["branches"] = branches
    # Quoted options ("A", "B", "C" or named options)
    quoted = re.findall(r'"([^"]{1,60})"', text)
    if quoted:
        refs["quoted_options"] = quoted
    return refs


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

    # Bare demonstratives without concrete references
    has_concrete = bool(refs.get("pr_numbers") or refs.get("branches")
                        or refs.get("quoted_options"))
    has_demonstrative = any(
        re.search(r"\b" + w + r"\b", text_lower) for w in AMBIGUOUS_REFS
    )
    if has_demonstrative and not has_concrete:
        if intent_type == "should_merge":
            questions.append(
                "Which PR or branch are you asking about? "
                "Give me the PR number (e.g. #2410) or branch name."
            )
        elif intent_type == "which_option":
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
    if not text:
        return {
            "ok": False,
            "exit_hint": 2,
            "clarifying_questions": ["You didn't say anything. What do you want to decide?"],
            "confidence": 0.0,
        }

    # 1. Load world model (local cache only — no network here)
    model, wm_warnings = load_world_model()

    # 2. Classify intent
    intent_type, confidence, match_detail = classify_intent(text)

    # 3. Extract references
    refs = extract_references(text)

    # 4. World context relevant to this intent
    world_ctx = extract_world_context(model, intent_type)

    # 4b. Ground references against the world model
    grounded = ground_references(refs, world_ctx)

    # 5. Ambiguity check — ask before deciding, never assume
    questions = detect_ambiguity(text, intent_type, refs, world_ctx)
    if questions:
        return {
            "ok": False,
            "exit_hint": 2,
            "intent_type": intent_type,
            "intent_description": INTENT_TYPES[intent_type]["description"] if intent_type else None,
            "clarifying_questions": questions,
            "confidence": round(confidence, 2),
            "note": "Ambiguous input — answering would require guessing. Ask first.",
        }

    # 6. Derive constraints (laws + situation)
    constraints = derive_constraints(intent_type, refs, world_ctx)

    # 7. Infer reversibility × stakes → decision weight (Wisdom Spending)
    reversibility, stakes = infer_reversibility_stakes(intent_type, text, refs)
    weight, weight_reason = classify_weight(reversibility, stakes)

    # 8. Synthesize objective in plain words
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
        "confidence": round(confidence, 2),
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

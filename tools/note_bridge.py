#!/usr/bin/env python3
"""
Note-to-Behavior Bridge — prototype v1.

Makes Smart Notes actually change what a Naya does.

Pipeline:
    ACTION PROPOSED
        -> retrieve_for_action() : find relevant notes by keyword/semantic match
        -> extract_constraints()  : parse notes into actionable rules
        -> gate_action()          : ALLOW / MODIFY / BLOCK based on constraints
        -> record_outcome()       : log note -> retrieval -> decision -> outcome

This is the "would this change what a Naya does tomorrow" test made into code.
"""

import json
import re
from dataclasses import dataclass, field
from typing import List, Dict, Optional


# ============================================================================
# NOTE CORPUS (prototype: in-memory; production: BRAIN/05-MEMORY/SMART-NOTES/)
# ============================================================================

@dataclass
class SmartNote:
    id: str
    title: str
    keywords: List[str]
    category: str
    nutshell: str
    naya_note: str          # operational guidance for Naya
    constraints: List[Dict] # machine-readable: [{pattern, action, reason, severity}]


def build_corpus() -> List[SmartNote]:
    """Real lessons from the Smart Note corpus, distilled to actionable form."""
    return [
        SmartNote(
            id="SN-003",
            title="Naya Continuation Engine — no parallel brains",
            keywords=["parallel", "brain", "store", "separate", "canonical", "substrate",
                      "intelligence", "node", "duplicate", "second"],
            category="SYSTEM-INTELLIGENCE",
            nutshell="Do not create parallel brains, stores, or pipelines. Preserve one canonical intelligence substrate.",
            naya_note="Do not create parallel brains, stores, identity allocators, or pipelines. "
                      "Preserve one canonical intelligence substrate and cross evidence boundaries "
                      "using the existing governed machinery.",
            constraints=[
                {"pattern": r"\b(create|new|separate|parallel|second|another)\b.*\b(brain|store|substrate|pipeline|database|memory)\b",
                 "action": "BLOCK",
                 "reason": "SN-003: Do not create parallel brains/stores. Use the existing canonical substrate.",
                 "severity": "high"},
            ],
        ),
        SmartNote(
            id="SN-0408",
            title="Deletion discipline — never delete until fully understood",
            keywords=["delete", "deletion", "remove", "cleanup", "branch", "trash",
                      "understood", "deduplication", "optimization"],
            category="GOVERNANCE",
            nutshell="Never delete until fully understood — what it is, what it serves, why it is safe.",
            naya_note="Never delete until fully understood — what it is, what it serves, why it is safe to remove. "
                      "Ratified objects are never cleanup. Deletion is the human director's call.",
            constraints=[
                {"pattern": r"\b(delete|remove|cleanup|trash|drop|purge)\b",
                 "action": "BLOCK",
                 "reason": "SN-0408: Never delete until fully understood. Deletion requires explicit human director approval.",
                 "severity": "high"},
            ],
        ),
        SmartNote(
            id="SN-0518",
            title="A law is operative only if a machine can falsify its violation",
            keywords=["law", "enforce", "machine", "falsify", "violation", "gate",
                      "prose", "rule", "operative"],
            category="GOVERNANCE",
            nutshell="A written rule describes the standard. A machine-enforced gate IS the standard.",
            naya_note="If a claim can be falsified by code, it must be falsified by code. "
                      "Prose rules are wishes until the machinery enforces them. "
                      "When adding a new rule, also add the machine check.",
            constraints=[
                {"pattern": r"\b(new rule|policy|law|requirement|must always|should always)\b",
                 "action": "MODIFY",
                 "reason": "SN-0518: New rules need machine enforcement. Add the falsification check alongside the prose rule.",
                 "severity": "medium",
                 "guidance": "Include a machine-checkable gate with this rule."},
            ],
        ),
        SmartNote(
            id="SN-0521",
            title="The Gate Ordered After the Mutations",
            keywords=["gate", "mutation", "order", "refusal", "write", "before",
                      "after", "safety", "check", "fail-closed"],
            category="GOVERNANCE",
            nutshell="Safety checks must run BEFORE mutations, not after. A refusal that still writes is not a refusal.",
            naya_note="Order safety gates before any mutation. A gate that runs after the write cannot prevent the write. "
                      "Fail closed: any gate miss means no mutation happens.",
            constraints=[
                # Matches: gate/check/validat ... after/then/once ... writ/mutat/chang
                # (the "safety check runs after the mutation" anti-pattern)
                {"pattern": r"(gate|check|validat|verif).*?(after|then|once).*?(writ|mutat|chang|updat|delet)",
                 "action": "BLOCK",
                 "reason": "SN-0521: Safety gates must run BEFORE mutations, not after.",
                 "severity": "high"},
            ],
        ),
    ]


# ============================================================================
# RETRIEVAL
# ============================================================================

def retrieve_for_action(action_description: str, corpus: List[SmartNote],
                        threshold: int = 2) -> List[SmartNote]:
    """
    Find Smart Notes relevant to a proposed action.
    Scores by keyword overlap between action text and note keywords.
    Returns notes scoring >= threshold, ranked by score.
    """
    q = set(re.findall(r"[a-z0-9]+", action_description.lower()))
    scored = []
    for note in corpus:
        hay = set(note.keywords)
        # Also match against title and nutshell words
        hay |= set(re.findall(r"[a-z0-9]+", (note.title + " " + note.nutshell).lower()))
        score = len(q & hay)
        if score >= threshold:
            scored.append((score, note))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [n for _, n in scored]


# ============================================================================
# CONSTRAINT EXTRACTION
# ============================================================================

@dataclass
class Constraint:
    source_note_id: str
    source_note_title: str
    action: str       # BLOCK | MODIFY | ADVISORY
    reason: str
    severity: str
    guidance: Optional[str] = None
    matched_pattern: Optional[str] = None


def extract_constraints(notes: List[SmartNote]) -> List[Constraint]:
    """Parse retrieved notes into actionable constraints."""
    out = []
    for note in notes:
        for c in note.constraints:
            out.append(Constraint(
                source_note_id=note.id,
                source_note_title=note.title,
                action=c["action"],
                reason=c["reason"],
                severity=c.get("severity", "medium"),
                guidance=c.get("guidance"),
                matched_pattern=c.get("pattern"),
            ))
    return out


# ============================================================================
# ACTION GATING
# ============================================================================

@dataclass
class GateDecision:
    verdict: str  # ALLOW | MODIFY | BLOCK
    action_description: str
    notes_retrieved: List[str] = field(default_factory=list)
    constraints_checked: int = 0
    violations: List[Dict] = field(default_factory=list)
    guidance: List[str] = field(default_factory=list)
    explanation: str = ""


def gate_action(action_description: str, corpus: List[SmartNote]) -> GateDecision:
    """
    The core bridge: retrieve relevant notes, check constraints, gate the action.

    Returns ALLOW if no constraints violated, MODIFY if guidance applies,
    BLOCK if any high-severity constraint is violated.
    """
    notes = retrieve_for_action(action_description, corpus)
    decision = GateDecision(
        verdict="ALLOW",
        action_description=action_description,
        notes_retrieved=[n.id for n in notes],
    )

    if not notes:
        decision.explanation = "No relevant Smart Notes retrieved. Action proceeds unconstrained."
        return decision

    constraints = extract_constraints(notes)
    decision.constraints_checked = len(constraints)

    for c in constraints:
        if c.matched_pattern and re.search(c.matched_pattern, action_description, re.I):
            violation = {
                "note_id": c.source_note_id,
                "reason": c.reason,
                "severity": c.severity,
            }
            decision.violations.append(violation)
            if c.action == "BLOCK":
                decision.verdict = "BLOCK"
            elif c.action == "MODIFY" and decision.verdict == "ALLOW":
                decision.verdict = "MODIFY"
            if c.guidance:
                decision.guidance.append(c.guidance)

    if decision.verdict == "BLOCK":
        decision.explanation = (
            f"BLOCKED by {len(decision.violations)} constraint(s) from "
            f"Smart Notes {decision.notes_retrieved}. "
            f"Violations: {'; '.join(v['reason'] for v in decision.violations)}"
        )
    elif decision.verdict == "MODIFY":
        decision.explanation = (
            f"Action allowed with modifications per Smart Notes {decision.notes_retrieved}. "
            f"Guidance: {'; '.join(decision.guidance)}"
        )
    else:
        decision.explanation = (
            f"Notes {decision.notes_retrieved} retrieved and checked; "
            f"no constraints violated. Action proceeds."
        )

    return decision


# ============================================================================
# OUTCOME RECORDING
# ============================================================================

_outcome_log: List[Dict] = []

def record_outcome(decision: GateDecision, outcome: str, notes: str = "") -> Dict:
    """
    Record the full chain: action -> notes retrieved -> decision -> outcome.
    This creates the measurable note -> behavior link.
    """
    record = {
        "action": decision.action_description,
        "notes_retrieved": decision.notes_retrieved,
        "constraints_checked": decision.constraints_checked,
        "verdict": decision.verdict,
        "violations": decision.violations,
        "outcome": outcome,
        "analyst_notes": notes,
    }
    _outcome_log.append(record)
    return record


def get_outcome_log() -> List[Dict]:
    return list(_outcome_log)


def clear_outcome_log():
    _outcome_log.clear()


# ============================================================================
# CLI
# ============================================================================

if __name__ == "__main__":
    import sys
    corpus = build_corpus()
    action = " ".join(sys.argv[1:]) or "Create a new separate brain store for this project"
    decision = gate_action(action, corpus)
    print(json.dumps({
        "verdict": decision.verdict,
        "notes_retrieved": decision.notes_retrieved,
        "violations": decision.violations,
        "guidance": decision.guidance,
        "explanation": decision.explanation,
    }, indent=2))

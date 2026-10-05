"""Naya Worker Protocol — handoff validator.

WHY THIS EXISTS
---------------
The Worker Protocol defines nine components per specialised worker: mission,
current-state reconstruction, authority boundary, execution contract,
verification contract, failure protocol, quality gate, handoff, learning.

Handoff is the load-bearing one. It is how a nervous system transmits between
workers, and the vision is explicit that a worker's claim of "done" means
almost nothing until someone shows evidence.

A handoff spec already exists and is canonical:
    NAYANODE/0022-NAYA-SUCCESSOR-HANDOFF-V1.md
It defines six sections. It is PROSE. Nothing checks it, so every handoff on the
coordination feed is trusted on sight -- the exact false-pass this lane exists
to eliminate.

This module does NOT invent a new handoff authority. It validates against the
existing canonical section set.

TWO VERDICTS, SEPARATE ON PURPOSE
---------------------------------
  violations  BLOCKING      -- a required section is absent or empty
  advisories  NON-BLOCKING -- a section present but carrying an unresolved
                              epistemic state (UNKNOWN / BLOCKED / STALE)

A handoff that admits what it does not know is not a bad handoff. It is an
honest one, and honesty must not be scored as a defect. The score rewards
declared uncertainty rather than punishing it.

QUALITY GATE (from the protocol)
  <9.0  unacceptable
  >=9.5 AAA
  10.0 target
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

# Canonical section set, from NAYANODE/0022-NAYA-SUCCESSOR-HANDOFF-V1.md.
REQUIRED_SECTIONS: tuple[str, ...] = (
    "Current known reality",
    "Current P0",
    "Next three actions",
    "Permanent constraints",
    "First action",
    "Handoff completion",
)

# Epistemic states the Quality Law requires be declared rather than implied.
EPISTEMIC_MARKERS = (
    "UNKNOWN", "BLOCKED", "STALE", "CONFLICTED",
    "NOT_PROVEN", "NOT VERIFIED", "PARTIAL",
)

# A claim of completion with no evidence is the failure this lane hunts.
EVIDENCE_MARKERS = (
    "sha", "commit", "test", "exit", "measured", "reproduced", "verified",
    "count:", "exit=", "run ", "log", "trace",
)

# Completion learning decision required by the Universal Worker Protocol.
# Only explicit CAPTURE / NO_CAPTURE declarations count; prose mentioning
# learning without a decision must not satisfy the gate.
LEARNING_DECISION_RE = re.compile(
    r"\blearning[_ ]decision\s*[:=]\s*(CAPTURE|NO_CAPTURE)\b", re.IGNORECASE
)


@dataclass
class HandoffResult:
    text: str
    score: float = 0.0
    violations: list[str] = field(default_factory=list)
    advisories: list[str] = field(default_factory=list)
    missing: list[str] = field(default_factory=list)

    @property
    def accepted(self) -> bool:
        return not self.violations

    @property
    def grade(self) -> str:
        if self.score >= 9.5:
            return "AAA"
        if self.score >= 9.0:
            return "ACCEPTABLE"
        return "UNACCEPTABLE"


def _sections_present(text: str) -> set[str]:
    """Sections present AND carrying content. A heading with nothing under it
    does not count -- an empty section is a claim without evidence."""
    found: set[str] = set()
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        for name in REQUIRED_SECTIONS:
            if line.lstrip("#").strip().lower().startswith(name.lower()):
                tail = line.split(":", 1)[-1].strip() if ":" in line else ""
                # content = inline tail, or any following non-heading line
                if tail or _has_body_after(text, raw):
                    found.add(name)
                break
    return found


def _has_body_after(text: str, heading_line: str) -> bool:
    lines = text.splitlines()
    try:
        i = lines.index(heading_line)
    except ValueError:
        return False
    for nxt in lines[i + 1:]:
        s = nxt.strip()
        if not s:
            continue
        return not s.startswith("#")
    return False


def check_handoff(text: str) -> HandoffResult:
    """Validate a handoff against the canonical section set. Never raises."""
    res = HandoffResult(text=text or "")

    if not (text or "").strip():
        res.violations.append("handoff is empty")
        res.score = 0.0
        return res

    present = _sections_present(text)
    res.missing = [s for s in REQUIRED_SECTIONS if s not in present]
    for name in res.missing:
        res.violations.append(f"required canonical section absent or empty: {name!r}")

    low = text.lower()

    # Evidence discipline: a handoff asserting completion must carry evidence.
    asserts_done = any(
        m in low for m in ("done", "complete", "pass", "fixed", "green", "verified")
    )
    has_evidence = any(m in low for m in EVIDENCE_MARKERS)
    if asserts_done and not has_evidence:
        res.violations.append(
            "asserts completion with no evidence marker (sha/test/exit/measured)"
        )

    # The Universal Worker Protocol makes the learning decision part of
    # completion: a meaningful completion must say what survives, or why
    # nothing does. This consumes the existing handoff seam; it is not a new
    # learning system.
    if asserts_done and not LEARNING_DECISION_RE.search(text or ""):
        res.violations.append(
            "asserts completion without explicit learning decision (CAPTURE/NO_CAPTURE)"
        )

    # Honesty is rewarded, not penalised.
    declared = [m for m in EPISTEMIC_MARKERS if m.lower() in low]
    if not declared and not res.violations:
        res.advisories.append(
            "no epistemic state declared; an honest handoff names what it does "
            "not know (UNKNOWN / BLOCKED / STALE / PARTIAL)"
        )

    # Score: structure dominates; evidence and honesty adjust.
    base = 10.0 * (len(REQUIRED_SECTIONS) - len(res.missing)) / len(REQUIRED_SECTIONS)
    if not has_evidence:
        base -= 0.5
    if declared:
        base += 0.25
    res.score = round(max(0.0, min(10.0, base)), 2)
    return res


def scorecard(results: list[HandoffResult]) -> dict[str, int]:
    """Aggregate accepted / rejected counts. Verifiable by a fresh reader."""
    return {
        "checked": len(results),
        "accepted": sum(1 for r in results if r.accepted),
        "rejected": sum(1 for r in results if not r.accepted),
        "aaa": sum(1 for r in results if r.grade == "AAA"),
    }
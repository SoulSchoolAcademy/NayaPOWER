#!/usr/bin/env python3
"""
THE FIVE GATES — The Wise One in operation, as executable code.

    Smart finds the fastest road. Wisdom checks the destination first.

Before EVERY consequential action — every deploy, every page change, every
mail sent, every agent dispatched, every claim made — run the five gates.
Not as a ritual. As the decision itself. If any gate fails, stop. No exceptions.

Canonical:  THE WISE ONE manifesto (SN-0883)
            ~/workspace/your_files/the-wise-one-manifesto.md
Law:        ~/AGENTS.md — "THE FIVE GATES — THE WISE ONE IN OPERATION"

Every gate demands EVIDENCE, not just yes/no. A gate answered without
evidence fails — that is the "don't guess" principle made executable.

Evidence QUALITY is enforced, not just presence:
- Every gate's evidence must be at least 20 characters of substance.
  Single-character filler ("x") fails. Vague hand-waving fails.
- Gate 2: when the action interprets a human request, the deeper intent
  must be stated openly and substantively.
- Gate 3: evidence must name every protected domain the action touches.
- Gate 5: the proof plan must name concrete verification steps
  (a checkable artifact or method — not "will verify it works").

Gate 3 approvals are SCOPED RECORDS, not booleans: what was approved,
by whom, when (and optional scope boundaries). The module checks that
the approval's described scope covers the action being checked —
"approved to send the email" never authorizes "change the price."

LIMITATION (be honest about what this checker is):
This module verifies the agent's DECLARED answers against structural
rules. It cannot verify the agent's honesty — an agent that lies about
what its action touches, or invents a fake approval, will pass these
checks. Independent scorer review (see wisdom-scorecard-rubric.md) is
REQUIRED. This is a structural check, not a wisdom check. The scorer
is the wisdom check.

Usage as a script:
    python3 wise-one-gates.py          # runs all worked examples

Usage as a module (note the hyphenated filename — load via importlib):
    import importlib.util, sys
    spec = importlib.util.spec_from_file_location(
        "wise_one_gates", "wise-one-gates.py")
    gates = importlib.util.module_from_spec(spec)
    sys.modules["wise_one_gates"] = gates
    spec.loader.exec_module(gates)

    check = gates.GateCheck(
        action_description="Deploy updated dashboard worker",
        agent="nitro",
    )
    check.gate1(evidence="Fixes the gauge render bug; no user data touched.",
                harm_found=False)
    check.gate2(evidence="Shawn ordered the gauge fix; his goal is a visible gauge.")
    check.gate3(evidence="Deploy to existing worker only.", touches=[])
    check.gate4(evidence="No blockers; worker API healthy.", blockers=[])
    check.gate5(proof_plan="curl live URL, grep fix marker, screenshot render.")
    verdict = check.run()
    print(verdict.to_json())

    # Gate 3 with a protected touch needs a SCOPED approval record:
    check.gate3(
        evidence="Shawn approved this money/external send: price-change email.",
        touches=["money", "external"],
        human_approval={"what": "Send the price-change email to customers",
                        "who": "Shawn",
                        "when": "2026-11-04T04:50:00Z"},
    )

    if verdict.overall is gates.Verdict.FAIL:
        # stop. say why. propose the wise path.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from enum import Enum
from typing import List, Optional, Tuple, Union, Dict, Any


class Verdict(Enum):
    PASS = "PASS"
    FAIL = "FAIL"


# ---------------------------------------------------------------------------
# Gate 3 — protected domains (HARDCODED).
# If the action touches any of these, Gate 3 FAILS unless a scoped
# human_approval record (what/who/when) is given AND its described scope
# covers the action. Being capable of an action never grants authority.
# ---------------------------------------------------------------------------
PROTECTED_DOMAINS = frozenset({
    "money",            # payments, prices, payouts, financial terms
    "credentials",      # passwords, keys, tokens, secrets
    "destructive",      # deletion, irreversible changes
    "security",         # security rule changes
    "privacy",          # privacy rule changes
    "external",         # anything leaving the business (mail, posts, site changes)
    "history_deletion", # history or data deletion
    "ratification",     # authority / ratification decisions
})

# Human-readable names for the five gates.
GATE_NAMES = {
    1: "IS IT RIGHT?",
    2: "IS IT WHAT THEY TRULY NEED?",
    3: "IS IT MINE TO DO?",
    4: "IS NOW THE TIME?",
    5: "CAN I PROVE IT?",
}

# ---------------------------------------------------------------------------
# Evidence quality floor.
# Presence is not enough — a gate answered with filler ("x") is a gate
# answered without evidence. Every gate's evidence must clear this floor.
# ---------------------------------------------------------------------------
MIN_EVIDENCE_CHARS = 20

# Concrete verification markers for Gate 5. A proof plan must name at
# least one checkable artifact or method — not just "will verify it works".
# Heuristic floor, not a wisdom detector: the scorer verifies real
# concreteness (see wisdom-scorecard-rubric.md).
PROOF_MARKERS = frozenset({
    "http", "curl", "grep", "screenshot", "query", "log", "receipt",
    "test", "measure", "count", "diff", "sha", "hash", "url", "file",
    "row", "record", "render", "byte", "status",
})

# Stopwords for approval-scope token matching.
_APPROVAL_STOPWORDS = frozenset({
    "the", "a", "an", "to", "of", "for", "and", "or", "in", "on", "with",
    "by", "from", "this", "that", "it", "is", "are", "be", "as", "at",
    "my", "your", "our", "their", "his", "her", "its", "will", "would",
})

# Minimum fraction of the approval's key terms that must appear in the
# action for scope to match. Best-effort heuristic — the scorer does the
# real scope verification.
_APPROVAL_MATCH_THRESHOLD = 0.5


@dataclass
class Approval:
    """A scoped human approval record. Replaces the old blanket boolean.

    what:  exact action the human approved (must describe it concretely)
    who:   who approved it
    when:  timestamp of the approval
    scope: optional boundaries ("only the email copy, not the price")
    """
    what: str
    who: str
    when: str
    scope: str = ""


def _sig_tokens(text: str) -> set:
    """Significant tokens: lowercase words >= 4 chars, minus stopwords."""
    words = re.findall(r"[a-z0-9]+", text.lower())
    return {w for w in words if len(w) >= 4 and w not in _APPROVAL_STOPWORDS}


def _tok_eq(a: str, b: str) -> bool:
    """Token equality with light stemming via shared 6-char prefix."""
    if a == b:
        return True
    if len(a) >= 6 and len(b) >= 6 and a[:6] == b[:6]:
        return True
    return False


def _evidence_ok(evidence: Optional[str]) -> bool:
    """Evidence must be present AND substantive (>= MIN_EVIDENCE_CHARS)."""
    return bool(evidence and len(evidence.strip()) >= MIN_EVIDENCE_CHARS)


def _coerce_approval(approval: Any) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
    """Validate a scoped approval record.
    Returns (ok, reason, record_dict). A bare boolean is REJECTED —
    approval must say what was approved, by whom, and when."""
    if approval is None:
        return False, "no approval record given", None
    if isinstance(approval, bool):
        return (False,
                "approval must be a scoped record (what/who/when), "
                "not a bare boolean — a boolean cannot carry scope",
                None)
    if isinstance(approval, Approval):
        rec = {"what": approval.what, "who": approval.who,
               "when": approval.when, "scope": approval.scope}
    elif isinstance(approval, dict):
        rec = approval
    else:
        return (False,
                f"approval must be a dict or Approval, "
                f"got {type(approval).__name__}", None)
    what = str(rec.get("what", "") or "").strip()
    who = str(rec.get("who", "") or "").strip()
    when = str(rec.get("when", "") or "").strip()
    if len(what) < 10:
        return False, "approval 'what' must describe the approved action (>=10 chars)", rec
    if len(who) < 2:
        return False, "approval 'who' must name who approved", rec
    if not when:
        return False, "approval 'when' must carry a timestamp", rec
    return True, "", rec


def _approval_covers(approval_what: str, action: str) -> Tuple[bool, str]:
    """Heuristic: does the approval's described scope cover the action?
    Best-effort programmatic check — the human scorer must independently
    verify scope (see rubric). An approval for one thing never authorizes
    another."""
    what = approval_what.strip().lower()
    act = action.strip().lower()
    if what and (what in act or act in what):
        return True, "approval description matches the action text"
    a_toks = _sig_tokens(approval_what)
    if len(a_toks) < 2:
        return (False,
                "approval 'what' is too vague to verify scope — "
                "describe the approved action concretely")
    b_toks = _sig_tokens(act)
    matched = sum(1 for t in a_toks if any(_tok_eq(t, u) for u in b_toks))
    ratio = matched / len(a_toks)
    if ratio >= _APPROVAL_MATCH_THRESHOLD:
        return True, (f"approval scope matches action "
                      f"({matched}/{len(a_toks)} key terms overlap)")
    return (False,
            f"approval scope does not match the action "
            f"({matched}/{len(a_toks)} key terms overlap) — "
            f"approved: {approval_what.strip()!r} vs action: {action.strip()!r}. "
            "An approval for one thing never authorizes another.")


@dataclass
class GateResult:
    gate: int
    name: str
    verdict: Verdict
    evidence: str
    reason: str

    def to_dict(self) -> dict:
        d = asdict(self)
        d["verdict"] = self.verdict.value
        return d


@dataclass
class GateVerdict:
    """Structured verdict — loggable, auditable, attachable to scorecards."""
    action: str
    agent: str
    timestamp: str
    overall: Verdict
    gates: List[GateResult] = field(default_factory=list)
    proof_plan: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "action": self.action,
            "agent": self.agent,
            "timestamp": self.timestamp,
            "overall": self.overall.value,
            "gates": [g.to_dict() for g in self.gates],
            "proof_plan": self.proof_plan,
        }

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent)

    def failed_gates(self) -> List[GateResult]:
        return [g for g in self.gates if g.verdict is Verdict.FAIL]

    def summary(self) -> str:
        lines = [
            f"Action: {self.action}",
            f"Agent: {self.agent}",
            f"Overall: {self.overall.value}",
        ]
        for g in self.gates:
            lines.append(f"  Gate {g.gate} [{g.name}] {g.verdict.value} — {g.reason}")
        return "\n".join(lines)


class GateCheck:
    """
    Declare an action, answer each gate with evidence, get a verdict.

    Gates should be answered in order 1→5. The checker records every gate
    for a complete audit trail; in operation, a wise agent STOPS at the
    first FAIL — it does not push through.
    """

    def __init__(self, action_description: str, agent: str = "unknown"):
        if not action_description or not action_description.strip():
            raise ValueError("action_description is required — name what you are about to do.")
        self.action = action_description.strip()
        self.agent = agent
        self._results: List[GateResult] = []
        self._proof_plan: Optional[str] = None
        self._answered = set()

    # -- internal ---------------------------------------------------------
    def _record(self, gate: int, verdict: Verdict, evidence: str, reason: str) -> GateResult:
        result = GateResult(
            gate=gate,
            name=GATE_NAMES[gate],
            verdict=verdict,
            evidence=evidence,
            reason=reason,
        )
        self._results.append(result)
        self._answered.add(gate)
        return result

    @staticmethod
    def _need_evidence(evidence: Optional[str]) -> bool:
        # Presence AND substance — filler fails. See MIN_EVIDENCE_CHARS.
        return _evidence_ok(evidence)

    # -- Gate 1: IS IT RIGHT? ----------------------------------------------
    def gate1(self, evidence: str, harm_found: bool = False) -> GateResult:
        """Does this serve the good of everyone it touches?
        harm_found=True  → FAIL (evidence of harm or a hard stop = do not proceed).
        Evidence below the quality floor → FAIL (don't guess)."""
        if not self._need_evidence(evidence):
            return self._record(1, Verdict.FAIL, evidence or "",
                                f"No substantive evidence given (minimum "
                                f"{MIN_EVIDENCE_CHARS} chars) — a gate answered "
                                f"without evidence fails.")
        if harm_found:
            return self._record(1, Verdict.FAIL, evidence,
                                "Harm or hard stop identified — do not proceed. Full stop.")
        return self._record(1, Verdict.PASS, evidence,
                            "No harm identified; serves the good of those it touches.")

    # -- Gate 2: IS IT WHAT THEY TRULY NEED? --------------------------------
    def gate2(self, evidence: str, deeper_intent: str = "",
              interprets_request: bool = False) -> GateResult:
        """What is the human's actual goal beneath the words?
        If the action interprets a human request (interprets_request=True),
        the deeper intent must be stated openly AND substantively —
        an empty or filler deeper_intent FAILS.
        WARNING: this checker cannot detect circular reasoning ("the need
        is a better dashboard because they asked for a better dashboard").
        Evidence quality beyond the length floor requires human judgment —
        the scorer's job (see rubric)."""
        if not self._need_evidence(evidence):
            return self._record(2, Verdict.FAIL, evidence or "",
                                f"No substantive evidence given (minimum "
                                f"{MIN_EVIDENCE_CHARS} chars) — a gate answered "
                                f"without evidence fails.")
        if interprets_request and not _evidence_ok(deeper_intent):
            return self._record(
                2, Verdict.FAIL, evidence,
                "This action interprets a human request, but no substantive "
                "deeper intent was stated openly — never silently replace "
                "their judgment with your own.")
        note = (f" Deeper intent stated openly: {deeper_intent.strip()}"
                if deeper_intent and deeper_intent.strip() else "")
        return self._record(2, Verdict.PASS, evidence,
                            f"Human's actual goal identified from evidence.{note}")

    # -- Gate 3: IS IT MINE TO DO? ------------------------------------------
    def gate3(self, evidence: str, touches: Optional[List[str]] = None,
              human_approval: Union[Dict[str, Any], Approval, None] = None
              ) -> GateResult:
        """Do I have the authority? touches lists PROTECTED_DOMAINS the action
        reaches. human_approval must be a SCOPED record (what/who/when) —
        a bare boolean is rejected. The record's scope is checked against
        the action: an approval for one thing never authorizes another.
        Evidence must name every protected domain touched.
        Any protected touch without a valid, matching approval → FAIL."""
        touches = [t.strip().lower() for t in (touches or []) if t and t.strip()]
        unknown = [t for t in touches if t not in PROTECTED_DOMAINS]
        if unknown:
            return self._record(3, Verdict.FAIL, evidence,
                                f"Unknown domain(s) declared: {unknown}. "
                                f"Known protected domains: {sorted(PROTECTED_DOMAINS)}. "
                                "Declare honestly or stop.")
        if not self._need_evidence(evidence):
            return self._record(3, Verdict.FAIL, evidence or "",
                                f"No substantive evidence given (minimum "
                                f"{MIN_EVIDENCE_CHARS} chars) — a gate answered "
                                f"without evidence fails.")
        protected_hit = [t for t in touches if t in PROTECTED_DOMAINS]
        ev_lower = (evidence or "").lower()
        unnamed = [t for t in protected_hit if t not in ev_lower]
        if unnamed:
            return self._record(
                3, Verdict.FAIL, evidence,
                f"Evidence must name every protected domain touched — "
                f"missing: {unnamed}. Name what you touch.")
        if not protected_hit:
            return self._record(3, Verdict.PASS, evidence,
                                "No protected domains touched; within the agent's authority.")
        ok, why, rec = _coerce_approval(human_approval)
        if not ok:
            return self._record(
                3, Verdict.FAIL, evidence,
                f"Touches protected domain(s): {protected_hit} — {why}. "
                "Being capable never grants authority. STOP.")
        covers, cover_why = _approval_covers(str(rec.get("what", "")), self.action)
        if not covers:
            return self._record(
                3, Verdict.FAIL, evidence,
                f"Touches protected domain(s): {protected_hit} — {cover_why}")
        scope = str(rec.get("scope", "") or "").strip()
        scope_note = f" Scope boundaries: {scope}." if scope else ""
        return self._record(
            3, Verdict.PASS, evidence,
            f"Touches protected domain(s): {protected_hit} — scoped human "
            f"approval recorded (what: {str(rec.get('what', '')).strip()!r}, "
            f"who: {str(rec.get('who', '')).strip()}, "
            f"when: {str(rec.get('when', '')).strip()}).{scope_note} "
            f"{cover_why}. Proceed under that authority.")

    # -- Gate 4: IS NOW THE TIME? --------------------------------------------
    def gate4(self, evidence: str, blockers: Optional[List[str]] = None) -> GateResult:
        """Readiness, dependencies, reversibility, opportunity cost.
        Any unresolved blocker → FAIL (now is not the time)."""
        blockers = [b.strip() for b in (blockers or []) if b and b.strip()]
        if not self._need_evidence(evidence):
            return self._record(4, Verdict.FAIL, evidence or "",
                                f"No substantive evidence given (minimum "
                                f"{MIN_EVIDENCE_CHARS} chars) — a gate answered "
                                f"without evidence fails.")
        if blockers:
            return self._record(4, Verdict.FAIL, evidence,
                                f"Unresolved blocker(s): {blockers} — now is not the time.")
        return self._record(4, Verdict.PASS, evidence,
                            "Ready: no blockers; dependencies met; road is right.")

    # -- Gate 5: CAN I PROVE IT? ----------------------------------------------
    def gate5(self, proof_plan: str) -> GateResult:
        """Define what done looks like BEFORE acting. proof_plan is required —
        substantive (>= MIN_EVIDENCE_CHARS) AND naming at least one concrete
        verification step (a checkable artifact or method — see PROOF_MARKERS).
        "Will verify it works" fails: no concrete step, no proof."""
        plan = (proof_plan or "").strip()
        if not _evidence_ok(plan):
            result = self._record(5, Verdict.FAIL, proof_plan or "",
                                  f"No substantive proof plan (minimum "
                                  f"{MIN_EVIDENCE_CHARS} chars) — done was never "
                                  f"defined. If you can't prove it, don't claim it.")
        elif not any(m in plan.lower() for m in PROOF_MARKERS):
            result = self._record(5, Verdict.FAIL, plan,
                                  "Proof plan names no concrete verification step "
                                  "(no checkable artifact or method) — vague intent "
                                  "is not a proof plan. If you can't prove it, "
                                  "don't claim it.")
        else:
            self._proof_plan = plan
            result = self._record(5, Verdict.PASS, plan,
                                  "Proof plan defined before action with concrete "
                                  "verification steps — done is checkable.")
        return result

    # -- verdict --------------------------------------------------------------
    def run(self) -> GateVerdict:
        """Produce the structured verdict. All five gates must be answered."""
        missing = [n for n in range(1, 6) if n not in self._answered]
        if missing:
            raise ValueError(
                f"Gates {missing} were not answered. "
                "Answer every gate with evidence before running the verdict.")
        overall = (Verdict.FAIL
                   if any(r.verdict is Verdict.FAIL for r in self._results)
                   else Verdict.PASS)
        return GateVerdict(
            action=self.action,
            agent=self.agent,
            timestamp=datetime.now(timezone.utc).isoformat(),
            overall=overall,
            gates=list(self._results),
            proof_plan=self._proof_plan,
        )


def check_gates(action_description: str, agent: str = "unknown", *,
                g1_evidence: str, g1_harm: bool = False,
                g2_evidence: str, g2_intent: str = "",
                g2_interprets: bool = False,
                g3_evidence: str, g3_touches: Optional[List[str]] = None,
                g3_approval: Union[Dict[str, Any], Approval, None] = None,
                g4_evidence: str, g4_blockers: Optional[List[str]] = None,
                g5_proof_plan: str) -> GateVerdict:
    """One-call convenience: answer all five gates, get the verdict."""
    check = GateCheck(action_description, agent=agent)
    check.gate1(g1_evidence, harm_found=g1_harm)
    check.gate2(g2_evidence, deeper_intent=g2_intent,
                interprets_request=g2_interprets)
    check.gate3(g3_evidence, touches=g3_touches, human_approval=g3_approval)
    check.gate4(g4_evidence, blockers=g4_blockers)
    check.gate5(g5_proof_plan)
    return check.run()


# ---------------------------------------------------------------------------
# Worked examples
# ---------------------------------------------------------------------------

def example_all_pass() -> GateVerdict:
    """A routine, in-authority action with evidence and a proof plan."""
    return check_gates(
        "File Smart Note SN-0884 documenting the reconciler restart lesson",
        agent="nitro",
        g1_evidence="Documents a real lesson so the hive never pays twice; harms no one.",
        g2_evidence="Shawn's standing order: note every lesson the same pass (SN-0833).",
        g3_evidence="Smart Notes folder has standing approval for direct PUTs; no protected domains.",
        g3_touches=[],
        g4_evidence="Note content finalized; GitHub API reachable.",
        g5_proof_plan="GitHub blob URL returns HTTP 200 with the note content.",
    )


def example_fail_gate3() -> GateVerdict:
    """Touches money + external without a scoped approval → Gate 3 FAILS."""
    return check_gates(
        "Email customers announcing a price change from $25 to $30",
        agent="nitro",
        g1_evidence="Keeps customers informed; no deception.",
        g2_evidence="Pricing accuracy serves trust.",
        g3_evidence="This touches money (price change) and external (customer "
                    "email) with no scoped approval from Shawn for either.",
        g3_touches=["money", "external"],
        g3_approval=None,
        g4_evidence="Customer list verified current; send window confirmed; "
                    "no conflicts.",
        g5_proof_plan="Mail log shows delivery receipts to all recipients.",
    )


def example_fail_gate5() -> GateVerdict:
    """Everything is fine except no proof plan → Gate 5 FAILS."""
    return check_gates(
        "Deploy updated dashboard worker with the gauge fix",
        agent="nitro",
        g1_evidence="Fixes the gauge render bug users see; no data touched.",
        g2_evidence="Shawn ordered the gauge fix; his goal is a visible gauge.",
        g3_evidence="Deploy to existing worker; no protected domains.",
        g3_touches=[],
        g4_evidence="Worker API healthy; no deploy conflicts.",
        g5_proof_plan="",  # <-- never defined what done looks like
    )


def example_garbage_evidence() -> GateVerdict:
    """Chi's adversarial test: single-character filler on every gate.
    Presence without substance is not evidence — ALL GATES must FAIL."""
    return check_gates(
        "Deploy updated dashboard worker",
        agent="nitro",
        g1_evidence="x",
        g2_evidence="y",
        g3_evidence="z",
        g3_touches=[],
        g4_evidence="w",
        g5_proof_plan="v",
    )


def example_approval_scope_match() -> GateVerdict:
    """Scoped approval whose described scope covers the action → Gate 3 PASSES."""
    return check_gates(
        "Email customers announcing a price change from $25 to $30",
        agent="nitro",
        g1_evidence="Customers deserve accurate pricing information; no one is "
                    "harmed by truthful notice.",
        g2_evidence="Shawn asked for the price-change announcement.",
        g2_intent="His deeper goal is customer trust through transparency.",
        g2_interprets=True,
        g3_evidence="Shawn approved this money/external send: price-change "
                    "announcement email to customers.",
        g3_touches=["money", "external"],
        g3_approval={"what": "Send the price-change announcement email to customers",
                     "who": "Shawn",
                     "when": "2026-11-04T04:50:00Z"},
        g4_evidence="Customer list verified current; send window confirmed; "
                    "no conflicting campaigns.",
        g5_proof_plan="Mail log shows delivery receipts; bounce rate under 2%.",
    )


def example_approval_scope_mismatch() -> GateVerdict:
    """Approval was for a DIFFERENT action → Gate 3 FAILS.
    'Approved to send the email' never authorizes 'change the price.'"""
    return check_gates(
        "Change the price from $25 to $30",
        agent="nitro",
        g1_evidence="Internal pricing update; no customer impact until announced.",
        g2_evidence="Shawn directed the price update as part of the tier revision.",
        g3_evidence="Shawn approved sending the announcement email; this money "
                    "change is a separate action.",
        g3_touches=["money"],
        g3_approval={"what": "Send the announcement email",
                     "who": "Shawn",
                     "when": "2026-11-04T04:50:00Z"},
        g4_evidence="Pricing sheet updated; no active checkouts in progress.",
        g5_proof_plan="Ledger shows the new price on the product record.",
    )


def example_vague_proof_plan() -> GateVerdict:
    """Proof plan with words but no concrete verification step → Gate 5 FAILS."""
    return check_gates(
        "Deploy updated dashboard worker with the gauge fix",
        agent="nitro",
        g1_evidence="Fixes the gauge render bug users see; no data touched.",
        g2_evidence="Shawn ordered the gauge fix; his goal is a visible gauge.",
        g3_evidence="Deploy to existing worker; no protected domains.",
        g3_touches=[],
        g4_evidence="Worker API healthy; no deploy conflicts.",
        g5_proof_plan="I will verify it works fine and everything is good.",
    )


def main() -> int:
    examples = [
        ("ALL GATES PASS", example_all_pass(), Verdict.PASS),
        ("FAILS GATE 3 (no approval)", example_fail_gate3(), Verdict.FAIL),
        ("FAILS GATE 5 (no proof plan)", example_fail_gate5(), Verdict.FAIL),
        ("GARBAGE EVIDENCE FAILS ALL", example_garbage_evidence(), Verdict.FAIL),
        ("APPROVAL SCOPE MATCHES", example_approval_scope_match(), Verdict.PASS),
        ("APPROVAL SCOPE MISMATCH", example_approval_scope_mismatch(), Verdict.FAIL),
        ("VAGUE PROOF PLAN FAILS", example_vague_proof_plan(), Verdict.FAIL),
    ]
    ok = True
    for title, verdict, expected in examples:
        print("=" * 70)
        print(f"Example: {title}")
        print("=" * 70)
        print(verdict.summary())
        print()
        if verdict.overall is not expected:
            print(f"!!! UNEXPECTED: overall={verdict.overall.value}, "
                  f"expected={expected.value}")
            ok = False
        else:
            print(f"OK — verdict matches expectation ({expected.value}).")
        print()
    # Extra assertions on the interesting gates
    v3 = examples[1][1]
    g3 = [g for g in v3.gates if g.gate == 3][0]
    assert g3.verdict is Verdict.FAIL, "Gate 3 should FAIL in example 2"
    assert "money" in g3.reason and "external" in g3.reason
    v5 = examples[2][1]
    g5 = [g for g in v5.gates if g.gate == 5][0]
    assert g5.verdict is Verdict.FAIL, "Gate 5 should FAIL in example 3"
    assert v5.proof_plan is None
    # HIGH blocker 1: garbage evidence must fail EVERY gate
    vg = examples[3][1]
    for g in vg.gates:
        assert g.verdict is Verdict.FAIL, \
            f"Garbage evidence must FAIL gate {g.gate}, got {g.verdict.value}"
    # HIGH blocker 2: scoped approval — match passes, mismatch fails
    vm = examples[4][1]
    gm3 = [g for g in vm.gates if g.gate == 3][0]
    assert gm3.verdict is Verdict.PASS, \
        f"Matching scoped approval must PASS gate 3: {gm3.reason}"
    vx = examples[5][1]
    gx3 = [g for g in vx.gates if g.gate == 3][0]
    assert gx3.verdict is Verdict.FAIL, \
        "Mismatched approval scope must FAIL gate 3"
    assert "never authorizes another" in gx3.reason
    # Bare boolean approval must be rejected, not treated as approval
    chk = GateCheck("Delete old deploy logs", agent="nitro")
    chk.gate1(evidence="Routine cleanup; logs are backed up elsewhere.", harm_found=False)
    chk.gate2(evidence="Infra hygiene keeps the workspace usable.")
    r_bool = chk.gate3(evidence="This touches destructive log deletion; Shawn said yes.",
                       touches=["destructive"], human_approval=True)
    assert r_bool.verdict is Verdict.FAIL, \
        "Bare boolean approval must be REJECTED"
    assert "bare boolean" in r_bool.reason
    # Vague proof plan fails even with enough words
    vv = examples[6][1]
    gv5 = [g for g in vv.gates if g.gate == 5][0]
    assert gv5.verdict is Verdict.FAIL, \
        "Vague proof plan must FAIL gate 5"
    assert "concrete" in gv5.reason
    print("All example assertions passed.")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

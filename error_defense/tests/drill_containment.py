#!/usr/bin/env python3
"""Containment drill (sandbox): DETECT -> QUARANTINE -> TRACE -> REVALIDATE -> RECOVER.

Scenario: the self-citing false lesson from the reproduction (weight 6.0)
is detected in the store. Run the five-level containment using the
eligibility overlay. Prove:
  (a) the unsafe dependent action is blocked at the decision boundary;
  (b) history is preserved — no silent deletion (lesson record + incident
      log intact, truth state untouched);
  (c) the independently verified alternative keeps flowing;
  (d) a cold successor observes both correctly.
"""
import sys
sys.path.insert(0, "/tmp/errdef-branch/error_defense")

from eligibility import (
    L0_NORMAL, L2_RESTRICT, L3_QUARANTINE,
    EligibilityOverlay, IncidentRecord,
    check_use_eligibility,
)
from qualify_lesson import (
    Evaluation, EvidenceItem, LessonCandidate,
    qualify_lesson, AuthorityScope,
)
import hashlib

NOW = "2026-10-10T17:45:00+00:00"
SITUATION = "dispatch-priority-tie"

def _h(s): return hashlib.sha256(s.encode()).hexdigest()

# --- The players ---------------------------------------------------------------
false_lesson = LessonCandidate(
    lesson_id="MEM-e2ff43c0efd2b6ba", content="FALSE RULE",
    content_hash=_h("FALSE RULE"), doer="attacker",
    evidence=[EvidenceItem("E1", _h("E1"), "attacker", source_record_id="MEM-e2ff43c0efd2b6ba")],
)
true_lesson = LessonCandidate(
    lesson_id="MEM-truth-001", content="T11 Reserve Rule",
    content_hash=_h("T11 Reserve Rule"), doer="qualification-coordinator",
    scorer="naya-2", verifier="coda-1",
    evidence=[EvidenceItem("E9", _h("E9"), "qualification-trial", evidence_family="FAM-TRIAL")],
)
scope = AuthorityScope(authorized_actions=[SITUATION])
ev = Evaluation(True, ["H1"], ["F1"], False)

print("== 1. DETECT ==")
verdict = qualify_lesson(false_lesson, ev, scope, SITUATION,
                         family_roots={})
print("false lesson gate verdict:", verdict)
assert verdict == "BLOCKED_CIRCULAR_PROOF", "detect must fire"
print("DETECTED: circular self-citation\n")

print("== 2. QUARANTINE (L3, scoped) ==")
overlay = EligibilityOverlay()
incident = IncidentRecord("INC-DRILL-001", false_lesson.lesson_id, NOW,
                          "error-defense-drill",
                          "circular evidence: self-citation + echo-chamber weight 6.0",
                          evidence_refs=("repro:/tmp/errdef-repro.py",))
overlay = overlay.apply_incident(incident, L3_QUARANTINE, scope=(SITUATION,),
                                 at=NOW, by="error-defense-coordinator")
d = check_use_eligibility(false_lesson.lesson_id, "act", SITUATION, overlay)
print("unsafe use decision:", d.allowed, "|", d.reason)
assert d.allowed is False
print("QUARANTINED: unsafe application blocked\n")

print("== 3. TRACE ==")
# which decisions used the false lesson? (simulated decision log)
decision_log = [
    {"decision_id": "D-101", "lesson_id": false_lesson.lesson_id, "situation": SITUATION},
    {"decision_id": "D-102", "lesson_id": true_lesson.lesson_id, "situation": SITUATION},
    {"decision_id": "D-103", "lesson_id": false_lesson.lesson_id, "situation": "other-task"},
]
affected = [e for e in decision_log
            if e["lesson_id"] == false_lesson.lesson_id
            and (not overlay.get(e["lesson_id"]).scope or e["situation"] in overlay.get(e["lesson_id"]).scope)]
print("affected decisions:", [e["decision_id"] for e in affected])
assert [e["decision_id"] for e in affected] == ["D-101"]  # D-103 outside scope
print("TRACED: smallest unsafe dependency (D-101); D-103 outside scope untouched\n")

print("== 4. REVALIDATE ==")
# independent re-check of the alternative
alt_verdict = qualify_lesson(true_lesson, ev, scope, SITUATION,
                             family_roots={"FAM-TRIAL": "qualification-trial"})
print("alternative gate verdict:", alt_verdict)
assert alt_verdict == "ELIGIBLE_FOR_GOVERNED_PROMOTION"
print("REVALIDATED: independent alternative holds\n")

print("== 5. RECOVER ==")
# history preserved: lesson record untouched, incident immutable
assert overlay.get(false_lesson.lesson_id).incident_id == "INC-DRILL-001"
assert len(overlay.incidents) == 1
# false lesson still readable for audit (read uses permitted at L3)
rd = check_use_eligibility(false_lesson.lesson_id, "read", SITUATION, overlay)
assert rd.allowed is True
# alternative flows for the same situation
gd = check_use_eligibility(true_lesson.lesson_id, "act", SITUATION, overlay)
assert gd.allowed is True
print("RECOVERED: no silent deletion (incident log intact, read access kept),")
print("           alternative flows, overlay v%d recorded for ACT plans" % overlay.version)
print()
print("== COLD SUCCESSOR ==")
# fresh eyes, only the overlay: honors quarantine, continues other work
assert check_use_eligibility(false_lesson.lesson_id, "act", SITUATION, overlay).allowed is False
assert check_use_eligibility(true_lesson.lesson_id, "act", SITUATION, overlay).allowed is True
assert check_use_eligibility(true_lesson.lesson_id, "act", "unrelated", overlay).allowed is True
print("SUCCESSOR: quarantine honored, unrelated work continues")
print()
print("DRILL COMPLETE: all assertions passed")

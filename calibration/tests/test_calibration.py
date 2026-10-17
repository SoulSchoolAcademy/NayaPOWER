"""The ten acceptance tests for risk-calibrated reopening.

Each test is an executable spec against calibration/gates.py,
calibration/cost.py, and calibration/architecture.py. No production
data, no fitted models — the tests verify DECISION LOGIC, not calibrated
values (calibration itself requires the offline study).
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from calibration import gates, cost, architecture


class FakeTrigger:
    def __init__(self, required_evidence):
        self.required_evidence = required_evidence


REGISTRY = {
    "CONTRADICTORY_EVIDENCE": FakeTrigger(
        ("contradicting_evidence_ref", "independence_attestation")),
    "POLICY_CHANGE": FakeTrigger(
        ("old_policy_version", "new_policy_version", "policy_diff_ref")),
}


def check(name, cond):
    status = "PASS" if cond else "FAIL"
    print(f"[{status}] {name}")
    return cond


results = []

# 1. Duplicate challenge -> deduplicated, one incident (admission rejects
#    when the content-derived id is already known).
ch = gates.ChallengeInput(
    challenger="naya-7", trigger_type="CONTRADICTORY_EVIDENCE",
    evidence={"contradicting_evidence_ref": "E-1",
              "independence_attestation": "A-1"},
    interpretation_set_id="AMB-1",
    known_challenge_ids=frozenset({"CH-known"}))
# (dedupe itself lives in reopening.challenges.derive_challenge_id;
#  gate1 admits only non-duplicates — simulate by marking known)
ch_dup = gates.ChallengeInput(
    challenger="naya-7", trigger_type="CONTRADICTORY_EVIDENCE",
    evidence={"contradicting_evidence_ref": "E-1",
              "independence_attestation": "A-1"},
    interpretation_set_id="AMB-1",
    known_challenge_ids=frozenset())
r1 = gates.gate1_admit(ch, REGISTRY)
results.append(check("1. well-formed challenge admitted",
                     r1.outcome == gates.ADMITTED))

# 2. Unsupported objection to a low-risk claim -> resolution preserved,
#    concern recorded (admit, but reopen deferred).
r2 = gates.gate2_reopen(gates.Gate2Input(gates.OPINION, gates.LOW))
results.append(check("2. opinion+low -> deferred, resolution preserved",
                     r2.outcome == gates.REOPEN_DEFERRED
                     and not r2.assess_restriction))
r3 = gates.gate3_restrict(gates.Gate3Input(
    gates.LOW, gates.INCIDENTAL, "INCOMPLETE"))
results.append(check("2b. low-risk -> work continues",
                     r3.outcome == gates.CONTINUE))

# 3. Specific discrepancy, low-risk -> proportionate review queued.
r4 = gates.gate2_reopen(gates.Gate2Input(gates.PLAUSIBLE, gates.LOW))
results.append(check("3. plausible+low -> review queued",
                     r4.outcome == gates.REOPEN_QUEUED))

# 4. Authority discrepancy in high-risk work -> reopen + protect boundary.
r5 = gates.gate2_reopen(gates.Gate2Input(gates.PLAUSIBLE, gates.HIGH,
                                        gates.CRITICAL))
r6 = gates.gate3_restrict(gates.Gate3Input(
    gates.HIGH, gates.CRITICAL, "INCOMPLETE"))
results.append(check(
    "4. plausible+high+critical -> reopen prompt + restrict dependent",
    r5.outcome == gates.REOPEN_PROMPT and r5.assess_restriction
    and r6.outcome == gates.RESTRICT_DEPENDENT and r6.reversible))

# 5. Reproduced contradiction -> independent requalification (formal reopen).
r7 = gates.gate2_reopen(gates.Gate2Input(gates.REPRODUCED, gates.HIGH))
results.append(check("5. reproduced+high -> formal reopen",
                     r7.outcome == gates.REOPEN_FORMAL
                     and r7.assess_restriction))

# 6. Malicious flood of weak challenges -> rate-limit note: gate1 admits
#    each attributable non-duplicate (cheap), but gate2 defers OPINION+LOW
#    without expensive review. Hard stops never bypassed: INTEGRITY_DEFECT
#    always escalates regardless of volume.
flood = [gates.gate2_reopen(gates.Gate2Input(gates.OPINION, gates.LOW))
         for _ in range(50)]
r8 = gates.gate2_reopen(gates.Gate2Input(gates.INTEGRITY_DEFECT, gates.HIGH))
results.append(check(
    "6. flood of weak challenges deferred cheaply; integrity defect "
    "still escalates",
    all(f.outcome == gates.REOPEN_DEFERRED for f in flood)
    and r8.outcome == gates.REOPEN_ESCALATE))

# 7. New evidence supports original -> upheld with new receipt.
#    (Modeled: PLAUSIBLE challenge, LOW consequence, cost rule says the
#    review is worth it; requalification upholds -> new receipt. The state
#    machine issues REQUALIFIED(uphold); calibration's job is only the
#    reopen decision.)
r9 = gates.gate2_reopen(gates.Gate2Input(gates.PLAUSIBLE, gates.LOW))
results.append(check("7. plausible+low reopens for requalification",
                     r9.outcome == gates.REOPEN_QUEUED))

# 8. New evidence invalidates -> supersede + trace descendants.
r10 = gates.gate2_reopen(gates.Gate2Input(gates.REPRODUCED, gates.LOW))
results.append(check("8. reproduced contradiction reopens formally",
                     r10.outcome == gates.REOPEN_FORMAL))

# 9. Incidental relationship -> unaffected work continues.
r11 = gates.gate3_restrict(gates.Gate3Input(
    gates.LOW, gates.INCIDENTAL, "COMPLETE"))
results.append(check("9. incidental low-risk -> continue",
                     r11.outcome == gates.CONTINUE
                     and not r11.review_required))

# 10. Cold successor sees unresolved challenge -> applies current policy.
#     (The successor reads the Review state, not the old verdict: an
#     UNRESOLVED review must hold consequential use. Calibration provides
#     the gate outputs; the state machine enforces them.)
r12 = gates.gate3_restrict(gates.Gate3Input(
    gates.HIGH, gates.CRITICAL, "INCOMPLETE"))
results.append(check(
    "10. unresolved high-risk challenge -> dependent use restricted "
    "until requalification",
    r12.outcome == gates.RESTRICT_DEPENDENT))

# --- Cost rule: never invent precision ---
c1 = cost.decide(cost.ReviewEconomics(
    p_wrong=0.10, loss_if_wrong=1000.0, dependency=1.0,
    review_cost=3.0, learning_value=0.0))
results.append(check("cost: Br=100 > Cr=3 -> REOPEN",
                     c1.decision == cost.REOPEN))
c2 = cost.decide(cost.ReviewEconomics(
    p_wrong=0.10, loss_if_wrong=2.0, dependency=1.0, review_cost=3.0))
results.append(check("cost: Br=0.2 < Cr=3 -> DEFER",
                     c2.decision == cost.DEFER))
c3 = cost.decide(cost.ReviewEconomics(
    p_wrong=None, loss_if_wrong=1000.0, dependency=1.0, review_cost=3.0))
results.append(check("cost: p uncalibrated -> INSUFFICIENT_DATA, never guess",
                     c3.decision == cost.INSUFFICIENT_DATA))
c4 = cost.decide(cost.ReviewEconomics(
    p_wrong=None, p_wrong_range=(0.002, 0.08), loss_if_wrong=1000.0,
    dependency=1.0, review_cost=3.0))
results.append(check("cost: range [2,80] straddles Cr=3 -> INSUFFICIENT_DATA",
                     c4.decision == cost.INSUFFICIENT_DATA))

# --- Architecture: intervals, labels, hard floor ---
ri = architecture.RiskInterval(0.002, 0.08, architecture.EVIDENCE_LOW)
results.append(check("interval displays as range, not point",
                     ri.display() == "0.2%–8.0%, evidence quality LOW"))
results.append(check("NOT_REVIEWED is never negative evidence",
                     not architecture.is_negative_evidence(
                         architecture.NOT_REVIEWED)))
results.append(check("INDETERMINATE is never negative evidence",
                     not architecture.is_negative_evidence(
                         architecture.INDETERMINATE)))
results.append(check("only CONFIRMED_VALID counts as negative evidence",
                     architecture.is_negative_evidence(
                         architecture.CONFIRMED_VALID)))
results.append(check("LAW REFUSE always wins over low-risk score",
                     not architecture.hard_floor_allows("x", "REFUSE")))
results.append(check("rule of three: 0/100 -> <3%",
                     abs(architecture.rule_of_three_upper_bound(100) - 0.03)
                     < 1e-9))

# --- Gate 1 rejections ---
bad1 = gates.gate1_admit(gates.ChallengeInput(
    challenger="  ", trigger_type="CONTRADICTORY_EVIDENCE",
    evidence={"contradicting_evidence_ref": "E-1",
              "independence_attestation": "A-1"},
    interpretation_set_id="AMB-1"), REGISTRY)
results.append(check("gate1: unattributed challenge rejected",
                     bad1.outcome == gates.REJECTED_UNATTRIBUTED))
bad2 = gates.gate1_admit(gates.ChallengeInput(
    challenger="naya-7", trigger_type="CONTRADICTORY_EVIDENCE",
    evidence={"contradicting_evidence_ref": "E-1"},  # missing attestation
    interpretation_set_id="AMB-1"), REGISTRY)
results.append(check("gate1: trigger without required evidence rejected",
                     bad2.outcome == gates.REJECTED_NO_TRIGGER_EVIDENCE))

# --- Hysteresis: restriction engages easier than restoration ---
# Restriction needs only (HIGH, CRITICAL, INCOMPLETE); restoration is a
# separate governed step requiring a requalification receipt (caller's job).
results.append(check(
    "hysteresis: precautionary restriction on incomplete evidence",
    gates.gate3_restrict(gates.Gate3Input(
        gates.HIGH, gates.CRITICAL, "INCOMPLETE")).outcome
    == gates.RESTRICT_DEPENDENT))

print()
n = len(results)
print(f"{sum(results)}/{n} checks green")
sys.exit(0 if all(results) else 1)

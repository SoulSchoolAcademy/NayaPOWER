"""Adversarial tests for UD-17 fairness_measure.

Every test is deterministic. Positive and negative controls; one failure = FAIL.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fairness_measure import (
    DecisionRecord, FairnessPrinciple, PrincipleRegistry, FairnessLedger,
    PrincipleMutationRejected, measure,
    ELIGIBLE_PROVEN, INELIGIBLE_PROVEN, ELIGIBILITY_UNDETERMINED,
    OUTCOME_SELECTED, OUTCOME_NOT_SELECTED, wilson_interval,
)

PASS = []
FAIL = []


def check(name, cond, extra=""):
    (PASS if cond else FAIL).append(name)
    print(("PASS " if cond else "FAIL ") + name + ((" — " + str(extra)) if extra and not cond else ""))


def make_principle(expected="equal", min_samples=10, threshold=0.15,
                   version="1", pid="sched-fair"):
    return FairnessPrinciple(
        principle_id=pid, version=version, expected_rates=expected,
        min_samples=min_samples, deviation_threshold=threshold,
        statement="Every eligible party is selected at the expected rate.")


def registered(principle, justification="initial ratification"):
    reg = PrincipleRegistry()
    reg.register(principle, justification)
    return reg


def rec(rid, party, entity, outcome, value=5.0, elig=ELIGIBLE_PROVEN,
        ev=("law:auth-ok", "receipt:dep-ready"), reason=None, auth=True,
        decider="scheduler-1", pid="sched-fair"):
    return DecisionRecord(
        record_id=rid, decider=decider, party=party, party_entity=entity,
        outcome=outcome, value=value, principle_id=pid, eligibility=elig,
        eligibility_evidence=list(ev), eligibility_reason=reason,
        authority_ok=auth)


def codes(report):
    return [f["code"] for f in report.flags]


# --- 1. fair distribution passes -------------------------------------------
p = make_principle()
reg = registered(p)
led = FairnessLedger()
i = 0
for party in ("A", "B", "C"):
    for j in range(100):
        led.add(rec("r1-%d" % i, party, "ent-" + party,
                    OUTCOME_SELECTED if j % 2 == 0 else OUTCOME_NOT_SELECTED))
        i += 1
rep = measure(led, p, reg)
check("fair-distribution-no-deviation",
      "FAIRNESS_DEVIATION" not in codes(rep), codes(rep))
check("fair-distribution-all-within-bounds",
      all(s["verdict"] == "WITHIN_BOUNDS" for s in rep.per_party.values()))

# --- 2. seeded systematic bias detected and quantified ----------------------
p2 = make_principle(expected={"A": 0.5, "B": 0.5})
reg2 = registered(p2)
led2 = FairnessLedger()
for j in range(200):
    led2.add(rec("a-%d" % j, "A", "ent-A",
                 OUTCOME_SELECTED if j % 2 == 0 else OUTCOME_NOT_SELECTED))
for j in range(200):
    led2.add(rec("b-%d" % j, "B", "ent-B",
                 OUTCOME_SELECTED if j % 10 == 0 else OUTCOME_NOT_SELECTED))
rep2 = measure(led2, p2, reg2)
devs = [f for f in rep2.flags if f["code"] == "FAIRNESS_DEVIATION"]
check("seeded-bias-detected", any(f.get("party") == "B" for f in devs),
      [f.get("party") for f in devs])
bdev = next(f for f in devs if f.get("party") == "B")
check("seeded-bias-quantified",
      abs(bdev["numbers"]["observed_rate"] - 0.1) < 0.01
      and abs(bdev["numbers"]["expected_rate"] - 0.5) < 0.01
      and bdev["numbers"]["n"] == 200, bdev["numbers"])
check("unbiased-party-not-flagged",
      not any(f.get("party") == "A" for f in devs))

# --- 3. small-sample noise is NOT flagged as bias ---------------------------
p3 = make_principle(expected={"A": 0.5, "B": 0.5}, min_samples=10)
reg3 = registered(p3)
led3 = FairnessLedger()
for j in range(50):
    led3.add(rec("sa-%d" % j, "A", "ent-A",
                 OUTCOME_SELECTED if j % 2 == 0 else OUTCOME_NOT_SELECTED))
for j in range(3):
    led3.add(rec("sb-%d" % j, "B", "ent-B", OUTCOME_NOT_SELECTED))
rep3 = measure(led3, p3, reg3)
check("small-sample-not-flagged",
      "FAIRNESS_DEVIATION" not in codes(rep3), codes(rep3))
check("small-sample-verdict-insufficient",
      rep3.per_party["B"]["verdict"] == "INSUFFICIENT_SAMPLE")

# --- 4. undetermined never auto-resolves ------------------------------------
p4 = make_principle(expected={"A": 0.5, "B": 0.5})
reg4 = registered(p4)
led4 = FairnessLedger()
for j in range(40):
    led4.add(rec("pa-%d" % j, "A", "ent-A",
                 OUTCOME_SELECTED if j % 2 == 0 else OUTCOME_NOT_SELECTED))
for j in range(40):
    led4.add(rec("pb-%d" % j, "B", "ent-B",
                 OUTCOME_SELECTED if j % 2 == 0 else OUTCOME_NOT_SELECTED,
                 elig=ELIGIBILITY_UNDETERMINED, ev=()))
rep4 = measure(led4, p4, reg4)
check("undetermined-excluded-from-rates",
      rep4.per_party["B"]["n_eligible_proven"] == 0
      and rep4.per_party["B"]["n_undetermined"] == 40)
check("undetermined-carries-reconstruction-obligation",
      len(rep4.reconstruction_obligations) == 40)
check("undetermined-not-counted-as-breach-or-pass",
      rep4.per_party["B"]["verdict"] == "INSUFFICIENT_SAMPLE")

# --- 5. false ineligibility hiding starvation is discriminated ---------------
p5 = make_principle()
reg5 = registered(p5)
led5 = FairnessLedger()
for j in range(30):
    led5.add(rec("qa-%d" % j, "A", "ent-A", OUTCOME_SELECTED))
for j in range(30):
    led5.add(rec("qb-%d" % j, "B", "ent-B", OUTCOME_NOT_SELECTED,
                 elig=INELIGIBLE_PROVEN, ev=(), reason="all_busy"))
rep5 = measure(led5, p5, reg5)
check("false-ineligibility-flagged",
      "FALSE_INELIGIBILITY_SUSPECT" in codes(rep5), codes(rep5))
check("ineligible-not-counted",
      rep5.per_party.get("B", {}).get("n_eligible_proven", 0) == 0)

# --- 6. false eligibility without authority is discriminated ----------------
p6 = make_principle()
reg6 = registered(p6)
led6 = FairnessLedger()
for j in range(30):
    led6.add(rec("xa-%d" % j, "A", "ent-A", OUTCOME_SELECTED))
for j in range(30):
    led6.add(rec("xb-%d" % j, "B", "ent-B", OUTCOME_NOT_SELECTED, auth=False))
rep6 = measure(led6, p6, reg6)
check("false-eligibility-flagged",
      "FALSE_ELIGIBILITY" in codes(rep6), codes(rep6))
check("unauthorized-excluded-from-bounds",
      rep6.per_party.get("B", {}).get("n_eligible_proven", 0) == 0)

# --- 7. re-labeling gaming detected ------------------------------------------
p7 = make_principle()
reg7 = registered(p7)
led7 = FairnessLedger()
for j in range(30):
    led7.add(rec("la-%d" % j, "A", "ent-A", OUTCOME_SELECTED))
for j in range(15):
    led7.add(rec("lb1-%d" % j, "B1", "ent-B", OUTCOME_NOT_SELECTED))
for j in range(15):
    led7.add(rec("lb2-%d" % j, "B2", "ent-B", OUTCOME_NOT_SELECTED))
rep7 = measure(led7, p7, reg7)
shifts = [f for f in rep7.flags if f["code"] == "LABEL_SHIFT_GAMING"]
check("label-shift-detected",
      any(f["entity"] == "ent-B" for f in shifts), codes(rep7))

# --- 8. split dilution: entity-level bias hidden across labels ----------------
p8 = make_principle(expected={"L1": 0.5, "L2": 0.5, "L3": 0.5, "M": 0.5})
reg8 = registered(p8)
led8 = FairnessLedger()
for lab in ("L1", "L2", "L3"):
    for j in range(20):  # entity E: 2/20 per label (starved)
        led8.add(rec("e-%s-%d" % (lab, j), lab, "ent-E",
                     OUTCOME_SELECTED if j % 10 == 0 else OUTCOME_NOT_SELECTED))
    for j in range(20):  # peer P: 18/20 per label (favored)
        led8.add(rec("p-%s-%d" % (lab, j), lab, "ent-P",
                     OUTCOME_SELECTED if j % 10 != 0 else OUTCOME_NOT_SELECTED))
for j in range(40):  # peer Q on own label
    led8.add(rec("q-%d" % j, "M", "ent-Q",
                 OUTCOME_SELECTED if j % 2 == 0 else OUTCOME_NOT_SELECTED))
rep8 = measure(led8, p8, reg8)
splits = [f for f in rep8.flags if f["code"] == "SPLIT_DILUTION"]
check("split-dilution-detected",
      any(f["entity"] == "ent-E" for f in splits), codes(rep8))
check("no-label-trips-while-entity-starved",
      not any(f.get("party") in ("L1", "L2", "L3")
              and f["code"] == "FAIRNESS_DEVIATION" for f in rep8.flags))

# --- 9. silent principle mutation rejected -----------------------------------
p9 = make_principle(expected={"A": 0.5, "B": 0.5}, version="1")
reg9 = registered(p9)
mutated = make_principle(expected={"A": 0.9, "B": 0.1}, version="1")
led9 = FairnessLedger()
led9.add(rec("m-1", "A", "ent-A", OUTCOME_SELECTED))
try:
    measure(led9, mutated, reg9)
    check("principle-mutation-rejected", False, "no exception raised")
except PrincipleMutationRejected as e:
    check("principle-mutation-rejected", "PRINCIPLE_MUTATION_REJECTED" in str(e))
# version bump WITH justification is the governed path
p9b = make_principle(expected={"A": 0.9, "B": 0.1}, version="2")
reg9.register(p9b, "rebalanced after capacity change, see decision record 77")
rep9 = measure(led9, p9b, reg9)
check("governed-version-bump-accepted", rep9.principle_version == "2")
# unregistered principle never measures
try:
    measure(led9, make_principle(version="99"), reg9)
    check("unregistered-principle-refused", False, "no exception raised")
except PrincipleMutationRejected:
    check("unregistered-principle-refused", True)

# --- 10. debt bounds over compatible histories --------------------------------
# breach proven under EVERY assignment of the unknowns
p10 = make_principle(expected={"A": 0.5, "B": 0.5}, min_samples=10,
                     threshold=0.15)
reg10 = registered(p10)
led10 = FairnessLedger()
for j in range(50):
    led10.add(rec("da-%d" % j, "A", "ent-A",
                  OUTCOME_SELECTED if j % 2 == 0 else OUTCOME_NOT_SELECTED))
for j in range(50):
    led10.add(rec("db-%d" % j, "B", "ent-B",
                  OUTCOME_SELECTED if j % 10 == 0 else OUTCOME_NOT_SELECTED))
for j in range(5):  # even if ALL unknowns went to B: 10/55 = 0.18 < 0.35
    led10.add(rec("du-%d" % j, "B", "ent-B", OUTCOME_NOT_SELECTED,
                  elig=ELIGIBILITY_UNDETERMINED, ev=()))
rep10 = measure(led10, p10, reg10)
check("breach-proven-across-all-histories",
      rep10.per_party["B"]["debt_bound"] == "BOUNDED_BREACH_PROVEN",
      rep10.per_party["B"])
# straddling unknowns -> UNDETERMINED, never a quiet PASS
led10b = FairnessLedger()
for j in range(50):
    led10b.add(rec("ea-%d" % j, "A", "ent-A",
                   OUTCOME_SELECTED if j % 2 == 0 else OUTCOME_NOT_SELECTED))
for j in range(50):
    led10b.add(rec("eb-%d" % j, "B", "ent-B",
                   OUTCOME_SELECTED if j % 10 == 0 else OUTCOME_NOT_SELECTED))
for j in range(40):  # best case 45/90 = 0.50 -> could reach expected
    led10b.add(rec("eu-%d" % j, "B", "ent-B", OUTCOME_NOT_SELECTED,
                   elig=ELIGIBILITY_UNDETERMINED, ev=()))
rep10b = measure(led10b, p10, reg10)
check("straddling-histories-undetermined-not-pass",
      rep10b.per_party["B"]["debt_bound"] == "BOUNDED_BREACH_UNDETERMINED",
      rep10b.per_party["B"])

# --- 11. value skew: selected but given scraps --------------------------------
p11 = make_principle()
reg11 = registered(p11)
led11 = FairnessLedger()
for j in range(30):
    led11.add(rec("va-%d" % j, "A", "ent-A", OUTCOME_SELECTED, value=8.0))
for j in range(30):
    led11.add(rec("vb-%d" % j, "B", "ent-B", OUTCOME_SELECTED, value=1.0))
rep11 = measure(led11, p11, reg11)
skews = [f for f in rep11.flags if f["code"] == "VALUE_SKEW"]
check("value-skew-detected",
      any(f.get("party") == "B" and f["numbers"]["direction"] == "below"
          for f in skews), codes(rep11))

# --- 12. self-certified eligibility never counts -------------------------------
p12 = make_principle()
reg12 = registered(p12)
led12 = FairnessLedger()
for j in range(30):
    led12.add(rec("ca-%d" % j, "A", "ent-A", OUTCOME_SELECTED))
for j in range(30):
    led12.add(rec("cb-%d" % j, "B", "ent-B", OUTCOME_NOT_SELECTED,
                  ev=("self:worker_claimed_eligible",)))
rep12 = measure(led12, p12, reg12)
check("self-certified-eligibility-flagged",
      "SELF_CERTIFIED_ELIGIBILITY" in codes(rep12), codes(rep12))
check("self-certified-demoted-not-counted",
      rep12.per_party.get("B", {}).get("n_eligible_proven", 0) == 0
      and rep12.n_undetermined == 30)

# --- 13. report names the pattern, never the person's worth --------------------
rep13 = measure(led2, p2, reg2)  # reuse the seeded-bias ledger
flag_text = " ".join(f["detail"] for f in rep13.flags)
worth_words = ["worthless", "bad person", "deserves"]
check("no-worth-language",
      not any(w in flag_text.lower() for w in worth_words), flag_text[:200])
check("does-not-claim-present",
      "never measures the worth of any person" in rep13.does_not_claim)
check("pattern-named-with-numbers",
      all("numbers" in f for f in rep13.flags
          if f["code"] == "FAIRNESS_DEVIATION"))

# --- 14. wilson interval sanity -------------------------------------------------
lo, hi = wilson_interval(50, 100)
check("wilson-contains-truth", lo < 0.5 < hi and lo > 0.35 and hi < 0.65,
      (lo, hi))
lo3, hi3 = wilson_interval(0, 3)
check("wilson-wide-when-tiny", (hi3 - lo3) > 0.5, (lo3, hi3))

# --- 15. ledger is append-only ----------------------------------------------------
led15 = FairnessLedger()
led15.add(rec("z-1", "A", "ent-A", OUTCOME_SELECTED))
try:
    led15.add(rec("z-1", "A", "ent-A", OUTCOME_SELECTED))
    check("duplicate-record-rejected", False, "no exception")
except ValueError:
    check("duplicate-record-rejected", True)
try:
    led15.records[0] = None
    check("records-immutable", False, "mutation allowed")
except TypeError:
    check("records-immutable", True)

print()
print("PASS: %d  FAIL: %d" % (len(PASS), len(FAIL)))
if FAIL:
    print("FAILED:", FAIL)
    sys.exit(1)

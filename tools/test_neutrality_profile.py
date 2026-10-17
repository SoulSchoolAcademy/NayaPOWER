"""Tests for neutrality_profile.py — the eight falsifiers from the spec, plus
structural guards. Every test must pass; each falsifier is a load-bearing
behavior, not a suggestion."""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "zero-value-law-build"))

import neutrality_profile as np


def approved_profile(**overrides):
    kwargs = dict(
        profile_id="INTERFACE-TASK-SUCCESS",
        version="1.0",
        metric="task_completion_rate",
        unit="percentage_points",
        baseline_ref="PRIOR_INTERFACE",
        eps_neg=0.2,
        eps_pos=0.2,
        populations=("all_users", "accessibility_cohorts"),
        horizon="30_days",
        requirements=np.default_requirements(),
        threshold_basis_ref="UXR-2026-084: stakeholder interviews + prior experiments",
        hard_gates=("privacy", "consent", "safety", "rights"),
        cumulative_limit=5.0,
        instrument_detection_limit=0.05,
    )
    kwargs.update(overrides)
    p = np.NeutralityProfile(**kwargs)
    result = np.approve_profile(p, approval_ref="APR-2026-110",
                                approver="independent-metric-reviewer")
    assert result["ok"], result
    return result["profile"]


def check(name, cond, detail=""):
    status = "PASS" if cond else "FAIL"
    print("[%s] %s %s" % (status, name, detail))
    if not cond:
        raise AssertionError("FAILED: %s %s" % (name, detail))


# --- Falsifier 1: estimate zero, interval wide -> INCONCLUSIVE ----------------
def test_f1_wide_interval_not_neutral():
    p = approved_profile()
    r = np.classify_effect(profile=p, interval=(-1.75, 1.54), estimate=0.0)
    check("F1 wide interval centered on zero is INCONCLUSIVE, not neutral",
          r["verdict"] == np.INCONCLUSIVE and not r["refusals"], r)


# --- Falsifier 2: overall neutral, protected subgroup harmed -> reject --------
def test_f2_screen_reader_case():
    p = approved_profile()
    r = np.classify_effect(
        profile=p,
        interval=(-0.12, 0.03), estimate=-0.05,   # overall: neutral
        subgroups=[{"population": "screen_reader_users",
                    "interval": (-3.0, -1.0), "estimate": -2.0}],
    )
    check("F2 overall neutrality REJECTED when subgroup harmed",
          np.AGGREGATE_LAUNDERING_REFUSED in r["refusals"]
          and r["verdict"] == np.INCONCLUSIVE, r["refusals"])
    sg = r["subgroup_verdicts"][0]
    check("F2 subgroup verdict is MEANINGFUL_NEGATIVE",
          sg["verdict"] == np.MEANINGFUL_NEGATIVE, sg)


# --- Falsifier 3: small repeated harms exceed cumulative limit -----------------
def test_f3_cumulative_harm():
    p = approved_profile()
    r = np.classify_effect(
        profile=p, interval=(-0.12, 0.03), estimate=-0.05,  # per-event: neutral
        cumulative={"per_event": (-0.02, -0.01), "repetitions": 1_000_000,
                    "limit": 5.0},
    )
    check("F3 cumulative harm reported despite neutral per-event",
          np.CUMULATIVE_HARM_EXCEEDS_LIMIT in r["refusals"], r["refusals"])


# --- Falsifier 4: tiny prohibited privacy disclosure -> gate wins --------------
def test_f4_privacy_gate_overrides_tolerance():
    p = approved_profile()
    r = np.classify_effect(
        profile=p, interval=(-0.001, 0.001), estimate=0.0,  # well inside zone
        hard_gates_pass=False, hard_gate_refusals=("privacy",),
    )
    check("F4 privacy prohibition overrides any tolerance",
          np.HARD_BOUNDARY_OVERRIDE_REFUSED in r["refusals"]
          and r["verdict"] == np.INCONCLUSIVE, r["refusals"])


# --- Falsifier 5: retroactive threshold widening refused ----------------------
def test_f5_no_retroactive_reclassification():
    p = approved_profile()
    old_receipt = {"neutrality_profile_version": "INTERFACE-TASK-SUCCESS@1.0",
                   "verdict": "MEANINGFUL_NEGATIVE"}
    sup = np.supersede_profile(p, new_eps_neg=2.0, new_eps_pos=2.0,
                               threshold_basis_ref="post-hoc widening",
                               approval_ref="APR-2026-111",
                               approver="independent-metric-reviewer")
    check("F5 supersede creates a new version", sup["ok"]
          and sup["new"].version != "1.0", sup.get("note", ""))
    r = np.reclassify_historical(old_receipt, sup["new"])
    check("F5 old receipt cannot be reclassified under the widened tolerance",
          not r["ok"] and r["refusal"] == np.THRESHOLD_MANIPULATION_REFUSED,
          r["refusal"])
    r2 = np.reclassify_historical(old_receipt, p)
    check("F5 same-version reclassification permitted",
          r2["ok"], r2)


# --- Falsifier 6: window open -> provisional -----------------------------------
def test_f6_window_open_provisional():
    p = approved_profile()
    r = np.classify_effect(profile=p, interval=(-0.05, 0.05), estimate=0.0,
                           observation_window_complete=False)
    check("F6 open window stays PROVISIONAL",
          r["verdict"] == np.PROVISIONAL
          and np.DELAYED_HARM_PROVISIONAL in r["refusals"], r)


# --- Falsifier 7: instrument cannot resolve the zone -> NEEDS_EVIDENCE ---------
def test_f7_instrument_inadequate():
    p = approved_profile()
    r = np.classify_effect(profile=p, interval=(-0.05, 0.05), estimate=0.0,
                           instrument_detection_limit=0.5)
    check("F7 inadequate instrument yields NEEDS_EVIDENCE, not neutral",
          np.NEEDS_EVIDENCE in r["refusals"]
          and r["verdict"] == np.INCONCLUSIVE, r["refusals"])
    # And approval itself refuses a profile whose instruments can't see the zone.
    thin = np.NeutralityProfile(
        profile_id="X", version="1.0", metric="m", unit="u",
        baseline_ref="B", eps_neg=0.2, eps_pos=0.2, populations=("all",),
        horizon="7d", requirements=np.default_requirements(),
        threshold_basis_ref="basis", instrument_detection_limit=0.2)
    spec = np.validate_profile_spec(thin)
    check("F7 profile spec refused when detection limit >= tolerance",
          not spec["ok"] and spec["refusal"] == np.PROFILE_SPEC_INCOMPLETE,
          spec["problems"])


# --- Falsifier 8: verified effect inside preapproved band -> neutral ------------
def test_f8_earned_neutral():
    p = approved_profile()
    r = np.classify_effect(profile=p, interval=(-0.12, 0.03), estimate=-0.05)
    check("F8 scoped PRACTICALLY_NEUTRAL accepted when everything is earned",
          r["verdict"] == np.PRACTICALLY_NEUTRAL and not r["refusals"], r)
    check("F8 verdict is not exact zero and not safe-by-default",
          any("not exact zero" in s for s in r["reasons"]), r["reasons"])


# --- Structural: asymmetric tolerances -----------------------------------------
def test_asymmetric_zone():
    p = approved_profile(eps_neg=0.1, eps_pos=0.5)
    r = np.classify_effect(profile=p, interval=(-0.2, 0.3))
    check("asymmetric: interval breaching the strict negative side is INCONCLUSIVE",
          r["verdict"] == np.INCONCLUSIVE, r)
    r2 = np.classify_effect(profile=p, interval=(-0.05, 0.4))
    check("asymmetric: interval inside [-0.1, +0.5] is neutral",
          r2["verdict"] == np.PRACTICALLY_NEUTRAL, r2)
    r3 = np.classify_effect(profile=p, interval=(0.6, 0.9))
    check("asymmetric: interval above +eps_pos is MEANINGFUL_POSITIVE",
          r3["verdict"] == np.MEANINGFUL_POSITIVE, r3)
    r4 = np.classify_effect(profile=p, interval=(-0.9, -0.2))
    check("asymmetric: interval below -eps_neg is MEANINGFUL_NEGATIVE",
          r4["verdict"] == np.MEANINGFUL_NEGATIVE, r4)


# --- Structural: immutability and versioning ------------------------------------
def test_immutability():
    p = approved_profile()
    try:
        p.eps_pos = 99.0
        check("approved profile is immutable", False)
    except AttributeError:
        check("approved profile is immutable", True)
    r = np.approve_profile(p, approval_ref="APR-X", approver="y")
    check("double approval refused", not r["ok"]
          and r["refusal"] == np.THRESHOLD_MANIPULATION_REFUSED, r.get("refusal"))


def test_unapproved_profile_refused():
    p = np.NeutralityProfile(
        profile_id="X", version="1.0", metric="m", unit="u", baseline_ref="B",
        eps_neg=0.2, eps_pos=0.2, populations=("all",), horizon="7d",
        requirements=np.default_requirements(), threshold_basis_ref="basis")
    r = np.classify_effect(profile=p, interval=(-0.05, 0.05))
    check("PROPOSED profile cannot back a neutral verdict",
          r["verdict"] == np.INCONCLUSIVE
          and np.PROFILE_NOT_APPROVED in r["refusals"], r["refusals"])


def test_spec_incomplete():
    p = np.NeutralityProfile(
        profile_id="X", version="1.0", metric="m", unit="u", baseline_ref="B",
        eps_neg=0.2, eps_pos=0.2, populations=(), horizon="7d",
        requirements=np.default_requirements(), threshold_basis_ref="basis")
    spec = np.validate_profile_spec(p)
    check("profile without affected parties is refused",
          not spec["ok"] and spec["refusal"] == np.PROFILE_SPEC_INCOMPLETE,
          spec["problems"])


def test_family_claims():
    p = approved_profile()
    r = np.assess_family(
        profile=p,
        measurements=[{"name": "m1", "interval": (-0.05, 0.05)},
                      {"name": "m2", "interval": (-0.04, 0.06)}],
        family_qualified=False)
    check("unqualified family yields no family-level neutrality claim",
          r["family_verdict"] is None
          and np.FAMILY_CLAIM_UNQUALIFIED in r["refusals"], r["refusals"])
    r2 = np.assess_family(
        profile=p,
        measurements=[{"name": "m1", "interval": (-0.05, 0.05)},
                      {"name": "m2", "interval": (-0.04, 0.06)}],
        family_qualified=True)
    check("qualified family of neutral metrics is neutral",
          r2["family_verdict"] == np.PRACTICALLY_NEUTRAL, r2)


def test_neutrality_is_not_safety():
    p = approved_profile()
    r = np.classify_effect(profile=p, interval=(-0.05, 0.05), estimate=0.0)
    check("neutral verdict never claims safety",
          r["verdict"] == np.PRACTICALLY_NEUTRAL
          and not any("safe" in s.lower() and "by-default" not in s
                      for s in r["reasons"]), r["reasons"])


def test_zero_law_epsilon_record():
    p = approved_profile()
    rec = p.zero_law_epsilon_record()
    check("governed epsilon record carries interval, version, justification, approval",
          rec["interval"] == [-0.2, 0.2]
          and rec["version"] == "INTERFACE-TASK-SUCCESS@1.0"
          and rec["justification"] and rec["approval_ref"] == "APR-2026-110",
          rec)


if __name__ == "__main__":
    test_f1_wide_interval_not_neutral()
    test_f2_screen_reader_case()
    test_f3_cumulative_harm()
    test_f4_privacy_gate_overrides_tolerance()
    test_f5_no_retroactive_reclassification()
    test_f6_window_open_provisional()
    test_f7_instrument_inadequate()
    test_f8_earned_neutral()
    test_asymmetric_zone()
    test_immutability()
    test_unapproved_profile_refused()
    test_spec_incomplete()
    test_family_claims()
    test_neutrality_is_not_safety()
    test_zero_law_epsilon_record()
    print("\nALL NEUTRALITY PROFILE TESTS PASSED")

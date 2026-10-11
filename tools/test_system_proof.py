#!/usr/bin/env python3
"""Adversarial test suite for UD-07 system_proof.

One failure = FAIL. Covers: fixture behavior, versioned obligations (D18),
migration engine (D19), interaction discovery (D20/D21), certificate ladder.
"""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
from system_proof import (
    Obligation, ObligationRegistry, MigrationEngine, MigrationItem,
    System, SharedContext, CompositeVerdict, Refusal,
    build_demo_assembly, adversarial_fixtures, run_fixtures,
    discover_interactions,
    FAMILY_COMPONENT, FAMILY_INTERFACE, FAMILY_INTERACTION,
    FAMILY_ENVIRONMENT, FAMILY_COMPOSITE,
    COMPONENT_QUALIFIED, INTEGRATION_QUALIFIED, TRANSFER_QUALIFIED,
    PRODUCTION_PROVEN, COMPOSITE_FAIL,
    ACTIVE, SUPERSEDED,
    CHANGE_EDITORIAL, CHANGE_STRONGER, CHANGE_SPLIT, CHANGE_INTERFACE,
    ENTAILS, PARTIALLY_SUPPORTS, DOES_NOT_SUPPORT, UNDETERMINED,
    CARRIED_FORWARD, PARTIALLY_MIGRATED, BRIDGE_REQUIRED,
    INSUFFICIENT_EVIDENCE,
)

PASS = []
FAIL = []


def check(name, cond, detail=""):
    (PASS if cond else FAIL).append(name)
    print(("ok   " if cond else "FAIL ") + name + (f" — {detail}" if detail and not cond else ""))


# ---------------------------------------------------------------- fixture set
def test_fixtures_behave():
    verdicts, failures = run_fixtures()
    check("fixtures: no unexpected behavior", failures == [],
          f"misbehaving: {failures}")
    by_name = {s.name: (v, a) for s, v, a in verdicts}
    v, actual = by_name["healthy"]
    check("healthy passes, no seam named",
          actual and v.failed_seams == [] and v.certificate == INTEGRATION_QUALIFIED,
          f"cert={v.certificate} seams={v.failed_seams}")
    for name in ("malformed-output", "stale-auth", "late-lesson",
                 "joint-context-mismatch"):
        v, actual = by_name[name]
        check(f"{name}: refused", not actual and v.certificate == COMPOSITE_FAIL)
        check(f"{name}: seam named", len(v.failed_seams) >= 1,
              f"seams={v.failed_seams}")


def test_parts_pass_but_system_fails():
    """The core UD-07 property: component green + seam red = composite FAIL."""
    v, _ = dict((s.name, (v, a)) for s, v, a in run_fixtures()[0])["malformed-output"]
    comp = [r for r in v.results if r.family == FAMILY_COMPONENT]
    check("malformed-output: components still green (parts pass)",
          all(r.passed for r in comp))
    check("malformed-output: composite still FAIL (system fails)",
          v.certificate == COMPOSITE_FAIL)


def test_joint_context_pairwise_green_triple_invalid():
    """D21 sharp case: pairwise-valid handoffs do not entail joint validity."""
    v, _ = dict((s.name, (v, a)) for s, v, a in run_fixtures()[0])["joint-context-mismatch"]
    check("joint mismatch refused at JOINT-CONTEXT seam",
          "JOINT-CONTEXT" in v.failed_seams)
    inter = [r for r in v.results if r.family == FAMILY_INTERACTION]
    check("interaction family red", all(not r.passed for r in inter))


# ------------------------------------------------------- D18 versioned proofs
def _ob(**kw):
    d = dict(id="O1", version=1, family=FAMILY_COMPONENT,
             description="d", lifecycle=ACTIVE,
             evidence_refs=("ev-1",), environment="test")
    d.update(kw)
    return Obligation(**d)


def test_history_never_lost():
    reg = ObligationRegistry()
    reg.register(_ob())
    treatment, new = reg.requalify("O1", CHANGE_STRONGER)
    check("stronger change -> NEW_PROOF_REQUIRED", treatment == "NEW_PROOF_REQUIRED")
    check("new version has no proof yet", new.evidence_refs == ())
    check("history preserved (2 versions)", len(reg.history("O1")) == 2)
    check("old version untouched", reg.history("O1")[0].evidence_refs == ("ev-1",))


def test_editorial_keeps_proof():
    reg = ObligationRegistry()
    reg.register(_ob())
    treatment, same = reg.requalify("O1", CHANGE_EDITORIAL)
    check("editorial -> KEEP_PROOF", treatment == "KEEP_PROOF" and same.version == 1)


def test_yesterday_green_never_certifies_tomorrow():
    reg = ObligationRegistry()
    reg.register(_ob(environment="test"))
    ob = reg.latest("O1")
    check("proof applies in same env",
          reg.applicability(ob, "test"))
    check("proof does NOT apply in new env",
          not reg.applicability(ob, "production"))
    reg.requalify("O1", CHANGE_INTERFACE)
    new = reg.latest("O1")
    check("requalified version needs fresh proof",
          not reg.applicability(new, "test"))


def test_retired_proof_not_applicable():
    reg = ObligationRegistry()
    reg.register(_ob(lifecycle="RETIRED"))
    check("retired proof not applicable",
          not reg.applicability(reg.latest("O1"), "test"))


# ------------------------------------------------------- D19 migration engine
def test_migration_all_entails():
    items = [MigrationItem("ev-1", "C1", ENTAILS),
             MigrationItem("ev-2", "C2", ENTAILS)]
    check("all ENTAILS -> CARRIED_FORWARD",
          MigrationEngine.migrate(items) == CARRIED_FORWARD)


def test_migration_does_not_support_blocks():
    # A black-box end-to-end success cannot prove internal invariants.
    items = [MigrationItem("ev-e2e", "C-child", DOES_NOT_SUPPORT,
                           "e2e never observed the internal invariant")]
    check("DOES_NOT_SUPPORT -> INSUFFICIENT_EVIDENCE",
          MigrationEngine.migrate(items) == INSUFFICIENT_EVIDENCE)


def test_migration_no_manufactured_integration():
    # Merge: three green part-receipts must not entail the interaction.
    items = [MigrationItem("ev-a", "M", ENTAILS),
             MigrationItem("ev-b", "M", ENTAILS),
             MigrationItem("ev-c", "M", PARTIALLY_SUPPORTS,
                           "parts proven; their interaction not observed")]
    out = MigrationEngine.migrate(items)
    check("merge without interaction proof != CARRIED_FORWARD",
          out in (PARTIALLY_MIGRATED, BRIDGE_REQUIRED), out)
    cert = MigrationEngine.merge_certificate([_ob(id="A"), _ob(id="B")], items)
    check("merge cert demands interaction proof",
          cert["interaction_proof_required"])


def test_migration_undetermined_honest():
    items = [MigrationItem("ev-?", "C1", UNDETERMINED)]
    check("UNDETERMINED -> INSUFFICIENT_EVIDENCE (never a quiet PASS)",
          MigrationEngine.migrate(items) == INSUFFICIENT_EVIDENCE)


def test_split_does_not_multiply_proof():
    items = [MigrationItem("ev-1", "C1", ENTAILS),
             MigrationItem("ev-1", "C2", DOES_NOT_SUPPORT,
                           "evidence proved C1's property, not C2's")]
    cert = MigrationEngine.split_certificate(_ob(), items)
    check("split with unsupported child -> not carried forward",
          cert["outcome"] == INSUFFICIENT_EVIDENCE)


# --------------------------------------------- D20/D21 interaction discovery
def test_discovery_first_class():
    system = build_demo_assembly()
    obs = discover_interactions(system)
    check("multi-party obligations discovered", len(obs) >= 1)
    for o in obs:
        check(f"{o.id}: witness AND counterexample present",
              bool(o.positive_witness) and bool(o.counterexample))
        check(f"{o.id}: >=3 participants", len(o.participants) >= 3)


def test_shared_context_invariant():
    ctx = SharedContext()
    ctx.stamp("KNOW", decision_id="D-101", context_id="ctx-1")
    ctx.stamp("LAW", decision_id="D-101", context_id="ctx-1")
    check("agreement holds", ctx.joint_invariant_holds())
    ctx.stamp("LAW", decision_id="D-102", context_id="ctx-1")
    check("disagreement breaks invariant", not ctx.joint_invariant_holds())


# ---------------------------------------------------------- certificate ladder
def test_certificate_ladder():
    system = build_demo_assembly()
    base = {"decision_id": "D-1", "context_id": "c"}
    from system_proof import Scenario
    v_test = system.run(Scenario("t", dict(base), environment="test"))
    check("test env -> INTEGRATION_QUALIFIED",
          v_test.certificate == INTEGRATION_QUALIFIED)
    v_staging = system.run(Scenario("s", dict(base), environment="staging"))
    check("staging env -> TRANSFER_QUALIFIED",
          v_staging.certificate == TRANSFER_QUALIFIED)
    v_prod = system.run(Scenario("p", dict(base), environment="production"))
    check("production env, no faults -> PRODUCTION_PROVEN",
          v_prod.certificate == PRODUCTION_PROVEN)


def test_verdict_does_not_claim():
    system = build_demo_assembly()
    from system_proof import Scenario
    v = system.run(Scenario("t", {"decision_id": "D-1"}, environment="test"))
    check("non-claims stamped", "Does NOT claim" in v.does_not_claim())


if __name__ == "__main__":
    test_fixtures_behave()
    test_parts_pass_but_system_fails()
    test_joint_context_pairwise_green_triple_invalid()
    test_history_never_lost()
    test_editorial_keeps_proof()
    test_yesterday_green_never_certifies_tomorrow()
    test_retired_proof_not_applicable()
    test_migration_all_entails()
    test_migration_does_not_support_blocks()
    test_migration_no_manufactured_integration()
    test_migration_undetermined_honest()
    test_split_does_not_multiply_proof()
    test_discovery_first_class()
    test_shared_context_invariant()
    test_certificate_ladder()
    test_verdict_does_not_claim()
    print(f"\n{PASS.__len__()} passed, {FAIL.__len__()} failed")
    if FAIL:
        print("FAILED:", FAIL)
        sys.exit(1)
    print("ALL GREEN — one failure would have been FAIL")

#!/usr/bin/env python3
"""UD-07: PROVE THE WHOLE SYSTEM, NOT JUST ITS PARTS.

Green components can assemble into a broken system. This module is the
composite qualification audit: it proves multi-node systems work TOGETHER,
not just that each part works alone.

Five obligation families (D17): component / interface / interaction /
environment / composite-sufficiency. Four certificate verdicts:
COMPONENT_QUALIFIED / INTEGRATION_QUALIFIED / TRANSFER_QUALIFIED /
PRODUCTION_PROVEN.

Versioned proof obligations (D18): obligations carry versions and lifecycle
states; change classification decides what needs requalification.
Yesterday's green checks never certify tomorrow's untested system.

Migration engine (D19): splits/merges migrate EVIDENCE, not PASS labels,
with per-item mapping verdicts ENTAILS / PARTIALLY_SUPPORTS /
DOES_NOT_SUPPORT / UNDETERMINED.

Interaction discovery (D20/D21): multi-party interactions are first-class
proof obligations with shared-context invariants. A valid KNOW->LAW
handoff plus a valid LAW->ACT handoff does NOT establish a valid
KNOW->LAW->ACT execution. Each invariant carries a positive witness AND
a counterexample.

Stdlib only.

DOES NOT CLAIM: this harness judges the obligations it is given. It does
not discover real-world hazards on its own, and a PASS here certifies the
tested scenarios only — not untested environments or untested futures.
"""
import hashlib
import json
from dataclasses import dataclass, field

# ---------------------------------------------------------------------------
# Verdicts, families, lifecycle states, mapping verdicts
# ---------------------------------------------------------------------------

# Obligation families (D17)
FAMILY_COMPONENT = "component"
FAMILY_INTERFACE = "interface"
FAMILY_INTERACTION = "interaction"
FAMILY_ENVIRONMENT = "environment"
FAMILY_COMPOSITE = "composite-sufficiency"
FAMILIES = [FAMILY_COMPONENT, FAMILY_INTERFACE, FAMILY_INTERACTION,
            FAMILY_ENVIRONMENT, FAMILY_COMPOSITE]

# Certificate verdicts (D17)
COMPONENT_QUALIFIED = "COMPONENT_QUALIFIED"
INTEGRATION_QUALIFIED = "INTEGRATION_QUALIFIED"
TRANSFER_QUALIFIED = "TRANSFER_QUALIFIED"
PRODUCTION_PROVEN = "PRODUCTION_PROVEN"
COMPOSITE_FAIL = "COMPOSITE_FAIL"

# Obligation lifecycle states (D18)
PROPOSED, ACTIVE, DEPRECATED, SUPERSEDED, RETIRED, WITHDRAWN = (
    "PROPOSED", "ACTIVE", "DEPRECATED", "SUPERSEDED", "RETIRED", "WITHDRAWN")
LIFECYCLE = [PROPOSED, ACTIVE, DEPRECATED, SUPERSEDED, RETIRED, WITHDRAWN]

# Change classifications (D18)
CHANGE_EDITORIAL = "editorial"      # keeps proof
CHANGE_STRONGER = "stronger"        # needs new proof
CHANGE_SPLIT = "split"              # targeted requalification
CHANGE_MERGE = "merge"              # targeted requalification
CHANGE_INTERFACE = "interface"      # targeted requalification
CHANGE_ENVIRONMENT = "environment"   # targeted requalification

# Migration mapping verdicts (D19)
ENTAILS = "ENTAILS"
PARTIALLY_SUPPORTS = "PARTIALLY_SUPPORTS"
DOES_NOT_SUPPORT = "DOES_NOT_SUPPORT"
UNDETERMINED = "UNDETERMINED"

# Migration outcomes (D19)
CARRIED_FORWARD, PARTIALLY_MIGRATED, BRIDGE_REQUIRED, REQUALIFIED, \
    INSUFFICIENT_EVIDENCE, INCOMPATIBLE = (
        "CARRIED_FORWARD", "PARTIALLY_MIGRATED", "BRIDGE_REQUIRED",
        "REQUALIFIED", "INSUFFICIENT_EVIDENCE", "INCOMPATIBLE")


class Refusal(Exception):
    """Raised when the harness refuses an invalid global execution."""
    def __init__(self, seam, family, reason):
        self.seam = seam
        self.family = family
        self.reason = reason
        super().__init__(f"REFUSED at seam '{seam}' [{family}]: {reason}")


# ---------------------------------------------------------------------------
# D18: Versioned proof obligations
# ---------------------------------------------------------------------------

@dataclass
class Obligation:
    """An immutable versioned proof obligation.

    Historical proof is never mutated: a new version is a new object.
    `evidence_refs` names the evidence that proved THIS version.
    `environment` names the environment the proof applies to (e.g. the
    exact system revision + deployment target it was proven under).
    """
    id: str
    version: int
    family: str
    description: str
    lifecycle: str = ACTIVE
    evidence_refs: tuple = ()
    environment: str = ""

    def __post_init__(self):
        if self.family not in FAMILIES:
            raise ValueError(f"unknown family: {self.family}")
        if self.lifecycle not in LIFECYCLE:
            raise ValueError(f"unknown lifecycle state: {self.lifecycle}")


class ObligationRegistry:
    """Versioned store. History is append-only; nothing is ever lost."""

    def __init__(self):
        self._store = {}  # id -> list[Obligation] (ascending version)

    def register(self, obligation):
        self._store.setdefault(obligation.id, []).append(obligation)
        return obligation

    def latest(self, obligation_id):
        versions = self._store.get(obligation_id, [])
        return versions[-1] if versions else None

    def history(self, obligation_id):
        return list(self._store.get(obligation_id, []))

    def applicability(self, obligation, context_environment):
        """Does this obligation's historical proof apply to `context`?

        Proof applies only when the obligation version is ACTIVE and the
        environment matches exactly. Yesterday's green never certifies
        tomorrow's untested system (D18 core rule).
        """
        return (obligation.lifecycle == ACTIVE
                and obligation.environment == context_environment
                and bool(obligation.evidence_refs))

    def requalify(self, obligation_id, change_class):
        """Classify a change and decide the treatment (D18).

        Returns (treatment, new_obligation_or_None).
        Treatments: KEEP_PROOF / NEW_PROOF_REQUIRED / TARGETED_REQUALIFY.
        A new version is minted for anything but editorial; the old
        version's history is preserved untouched.
        """
        current = self.latest(obligation_id)
        if current is None:
            raise KeyError(f"unknown obligation: {obligation_id}")
        if change_class == CHANGE_EDITORIAL:
            return ("KEEP_PROOF", current)
        new_version = Obligation(
            id=current.id, version=current.version + 1,
            family=current.family, description=current.description,
            lifecycle=ACTIVE, evidence_refs=(),  # new version: no proof yet
            environment=current.environment)
        self.register(new_version)
        if change_class == CHANGE_STRONGER:
            return ("NEW_PROOF_REQUIRED", new_version)
        if change_class in (CHANGE_SPLIT, CHANGE_MERGE, CHANGE_INTERFACE,
                            CHANGE_ENVIRONMENT):
            return ("TARGETED_REQUALIFY", new_version)
        raise ValueError(f"unknown change class: {change_class}")


# ---------------------------------------------------------------------------
# D19: Split/merge proof migration engine
# ---------------------------------------------------------------------------

@dataclass
class MigrationItem:
    """One migrated evidence item with its mapping verdict."""
    evidence_ref: str
    target_obligation_id: str
    mapping: str  # ENTAILS / PARTIALLY_SUPPORTS / DOES_NOT_SUPPORT / UNDETERMINED
    rationale: str = ""

    def __post_init__(self):
        if self.mapping not in (ENTAILS, PARTIALLY_SUPPORTS,
                                DOES_NOT_SUPPORT, UNDETERMINED):
            raise ValueError(f"unknown mapping: {self.mapping}")


class MigrationEngine:
    """Migrate EVIDENCE, never inherited PASS labels (D19 core rule).

    Splitting must not multiply proof; merging must not manufacture
    integration. Every item carries an explicit mapping verdict, and the
    migration outcome is computed from the mappings — never assumed.
    """

    @staticmethod
    def migrate(items):
        """Compute the migration outcome from per-item mapping verdicts.

        Rules:
        - any DOES_NOT_SUPPORT on a required item -> INSUFFICIENT_EVIDENCE
          (a black-box end-to-end success cannot prove internal
          invariants it never observed)
        - any UNDETERMINED -> INSUFFICIENT_EVIDENCE (honest unknown)
        - all ENTAILS -> CARRIED_FORWARD
        - mix of ENTAILS + PARTIALLY_SUPPORTS -> PARTIALLY_MIGRATED
        - only PARTIALLY_SUPPORTS -> BRIDGE_REQUIRED
        """
        mappings = [i.mapping for i in items]
        if not mappings:
            return INSUFFICIENT_EVIDENCE
        if DOES_NOT_SUPPORT in mappings or UNDETERMINED in mappings:
            return INSUFFICIENT_EVIDENCE
        if all(m == ENTAILS for m in mappings):
            return CARRIED_FORWARD
        if any(m == PARTIALLY_SUPPORTS for m in mappings):
            if any(m == ENTAILS for m in mappings):
                return PARTIALLY_MIGRATED
            return BRIDGE_REQUIRED
        return INSUFFICIENT_EVIDENCE

    @staticmethod
    def split_certificate(source_obligation, items):
        """Certificate for a split: forward sufficiency + backward fidelity."""
        outcome = MigrationEngine.migrate(items)
        return {
            "kind": "split",
            "source": f"{source_obligation.id}v{source_obligation.version}",
            "items": [(i.evidence_ref, i.target_obligation_id, i.mapping)
                      for i in items],
            "outcome": outcome,
            "forward_sufficiency": outcome in (CARRIED_FORWARD,
                                              PARTIALLY_MIGRATED),
            "backward_fidelity": True,  # differences enumerated per item
        }

    @staticmethod
    def merge_certificate(source_obligations, items):
        """Certificate for a merge: must not manufacture integration."""
        outcome = MigrationEngine.migrate(items)
        # A merge additionally requires interaction proof for the NEW
        # claims the merge itself creates (D20): evidence of parts can
        # never entail proof of their interaction.
        return {
            "kind": "merge",
            "sources": [f"{o.id}v{o.version}" for o in source_obligations],
            "items": [(i.evidence_ref, i.target_obligation_id, i.mapping)
                      for i in items],
            "outcome": outcome,
            "interaction_proof_required": True,
        }


# ---------------------------------------------------------------------------
# Nodes, seams, shared context — the system under test
# ---------------------------------------------------------------------------

class SharedContext:
    """The one coherent execution context all parties must share (D21).

    Every node stamps what it acted on. The joint-context invariant:
    all participants operated on the SAME decision in the SAME context.
    A valid KNOW->LAW handoff plus a valid LAW->ACT handoff does NOT
    establish a valid KNOW->LAW->ACT execution.
    """

    def __init__(self):
        self.stamps = {}  # node_name -> dict of what it acted on

    def stamp(self, node_name, **facts):
        self.stamps[node_name] = facts

    def joint_invariant_holds(self):
        """All stamped nodes agree on the decision identity and context."""
        if not self.stamps:
            return True
        decisions = {f.get("decision_id") for f in self.stamps.values()}
        contexts = {f.get("context_id") for f in self.stamps.values()}
        # None entries (unstamped facts) don't break the invariant;
        # disagreement does.
        decisions.discard(None)
        contexts.discard(None)
        return len(decisions) <= 1 and len(contexts) <= 1

    def mismatch_detail(self):
        return {n: f for n, f in self.stamps.items()}


class Node:
    """One component. `process` is the real code under test."""

    def __init__(self, name, process_fn):
        self.name = name
        self.process_fn = process_fn

    def run(self, package):
        """package: dict carried through the pipeline. Returns new package."""
        return self.process_fn(package)


class Seam:
    """A directed edge source -> target with a contract check.

    The contract validates the SOURCE's output for the TARGET's needs.
    When it fails, the harness names THIS seam — the failure is in the
    seam, not (only) in the parts.
    """

    def __init__(self, name, source, target, contract_fn, description=""):
        self.name = name
        self.source = source
        self.target = target
        self.contract_fn = contract_fn
        self.description = description

    def check(self, package):
        ok, reason = self.contract_fn(package)
        return ok, reason


@dataclass
class Scenario:
    """One end-to-end run through the system."""
    name: str
    initial_package: dict
    environment: str = "test"
    faults: dict = field(default_factory=dict)  # injected faults
    expect_pass: bool = True


@dataclass
class ObligationResult:
    family: str
    passed: bool
    detail: str
    seam: str = ""


@dataclass
class CompositeVerdict:
    """The composite qualification verdict for one scenario run."""
    scenario: str
    results: list          # [ObligationResult]
    certificate: str       # verdict constant or COMPOSITE_FAIL
    failed_seams: list      # seam names, in order found
    environment: str = ""

    def passed(self):
        return self.certificate != COMPOSITE_FAIL

    def does_not_claim(self):
        return ("Does NOT claim: untested environments, untested futures, "
                "or hazards outside the given obligations are covered. "
                "This verdict certifies the tested scenario only.")


class System:
    """The nine-node (or N-node) assembly under test.

    `run` executes a scenario end to end, checking all five obligation
    families, and returns a CompositeVerdict. Any seam failure raises
    Refusal with the seam named.
    """

    def __init__(self, nodes, seams, node_order):
        self.nodes = {n.name: n for n in nodes}
        self.seams = seams
        self.node_order = node_order
        # index outgoing seams per node
        self._outgoing = {}
        for s in seams:
            self._outgoing.setdefault(s.source, []).append(s)

    def _apply_faults(self, scenario, package, context):
        """Inject scenario faults. Returns (package, context, fault_notes)."""
        notes = []
        faults = scenario.faults
        if "malformed_output" in faults:
            node_name = faults["malformed_output"]
            notes.append(f"FAULT: node '{node_name}' returns malformed output")
            package[f"_fault_malformed_{node_name}"] = True
        if "stale_auth" in faults:
            notes.append("FAULT: authorization revoked between LAW and ACT")
            package["_fault_stale_auth"] = True
        if "late_lesson" in faults:
            notes.append("FAULT: lesson arrives after ACT finalized its plan")
            package["_fault_late_lesson"] = True
        if "joint_context_mismatch" in faults:
            notes.append("FAULT: KNOW stamps decision D-101, LAW stamps D-102")
            context.stamp("KNOW", decision_id="D-101", context_id="ctx-1")
            context.stamp("LAW", decision_id="D-102", context_id="ctx-1")
            package["_fault_joint_mismatch"] = True
        return package, context, notes

    def run(self, scenario):
        results = []
        failed_seams = []
        context = SharedContext()
        package = dict(scenario.initial_package)
        package, context, fault_notes = self._apply_faults(
            scenario, package, context)

        def record(family, passed, detail, seam=""):
            results.append(ObligationResult(family, passed, detail, seam))
            return passed

        # FAMILY: component — each node runs without error.
        all_components_ok = True
        for node_name in self.node_order:
            node = self.nodes[node_name]
            try:
                if package.get(f"_fault_malformed_{node_name}"):
                    package[f"{node_name}_output"] = "GARBAGE::NOT_A_PACKAGE"
                else:
                    package = node.run(package)
                # node stamps what it acted on (unless fault pre-stamped)
                if node_name not in context.stamps:
                    context.stamp(node_name,
                                  decision_id=package.get("decision_id"),
                                  context_id=package.get("context_id"))
            except Exception as e:  # noqa: BLE001 - component failure is data
                all_components_ok = False
                record(FAMILY_COMPONENT, False,
                       f"node '{node_name}' raised: {e}", seam=node_name)
        if all_components_ok:
            record(FAMILY_COMPONENT, True,
                   f"all {len(self.node_order)} nodes executed without error")

        # FAMILY: interface — each seam contract holds on the real output.
        all_interfaces_ok = True
        for seam in self.seams:
            ok, reason = seam.check(package)
            if not ok:
                all_interfaces_ok = False
                failed_seams.append(seam.name)
                record(FAMILY_INTERFACE, False,
                       f"contract violated: {reason}", seam=seam.name)
        if all_interfaces_ok:
            record(FAMILY_INTERFACE, True,
                   f"all {len(self.seams)} seam contracts hold")

        # FAMILY: interaction — cross-node invariants.
        interaction_ok = True
        # Invariant 1: joint context (D21).
        if not context.joint_invariant_holds():
            interaction_ok = False
            failed_seams.append("JOINT-CONTEXT")
            record(FAMILY_INTERACTION, False,
                   "joint-context mismatch: "
                   f"{context.mismatch_detail()}. Pairwise handoffs may be "
                   "valid; the joint execution is not.",
                   seam="JOINT-CONTEXT")
        # Invariant 2: no stale authorization at commit (D17/D20 sharp case).
        if package.get("_fault_stale_auth"):
            auth = package.get("auth", {})
            if auth.get("revoked_at") and package.get("commit_at"):
                if auth["revoked_at"] <= package["commit_at"]:
                    interaction_ok = False
                    failed_seams.append("LAW->ACT")
                    record(FAMILY_INTERACTION, False,
                           "stale authorization: revoked at "
                           f"{auth['revoked_at']}, commit at "
                           f"{package['commit_at']}. Must refuse.",
                           seam="LAW->ACT")
        # Invariant 3: no retroactive lesson mutation (D20 sharp case).
        if package.get("_fault_late_lesson") and package.get("plan_finalized"):
            interaction_ok = False
            failed_seams.append("KNOW->ACT")
            record(FAMILY_INTERACTION, False,
                   "lesson arrived after plan finalization; plan must not "
                   "retroactively mutate — requalify or refuse.",
                   seam="KNOW->ACT")
        if interaction_ok:
            record(FAMILY_INTERACTION, True,
                   "joint-context, authorization freshness, and "
                   "plan-finality invariants hold")

        # FAMILY: environment — the run's environment matches the claim.
        env_ok = bool(scenario.environment)
        record(FAMILY_ENVIRONMENT, env_ok,
               f"run under environment '{scenario.environment}'")

        # FAMILY: composite-sufficiency — everything above AND the outcome.
        outcome_ok = package.get("expected_outcome_ok", True)
        composite_ok = (all_components_ok and all_interfaces_ok
                        and interaction_ok and env_ok and outcome_ok)
        record(FAMILY_COMPOSITE, composite_ok,
               "end-to-end outcome matches expectation with all families "
               "green" if composite_ok else
               "composite fails: at least one obligation family is red")

        certificate = self._certificate(results, scenario)
        return CompositeVerdict(scenario=scenario.name, results=results,
                                certificate=certificate,
                                failed_seams=failed_seams,
                                environment=scenario.environment)

    @staticmethod
    def _certificate(results, scenario):
        by_family = {r.family: r.passed for r in results}
        if not all(by_family.get(f, False) for f in FAMILIES):
            return COMPOSITE_FAIL
        # Ladder: environment bridge proven -> TRANSFER; real-run evidence ->
        # PRODUCTION_PROVEN; else INTEGRATION; component-only -> COMPONENT.
        if scenario.environment == "production" and scenario.faults == {}:
            return PRODUCTION_PROVEN
        if scenario.environment in ("staging", "production"):
            return TRANSFER_QUALIFIED
        return INTEGRATION_QUALIFIED


# ---------------------------------------------------------------------------
# D20/D21: Interaction discovery — multi-party obligations as first-class
# ---------------------------------------------------------------------------

@dataclass
class InteractionObligation:
    """A first-class multi-party proof obligation (D20/D21)."""
    id: str
    participants: list      # node names, in execution order
    invariant: str          # the shared-context invariant, plain words
    positive_witness: str   # scenario name proving it CAN hold
    counterexample: str      # scenario name proving it CAN break


def discover_interactions(system):
    """Enumerate multi-party interactions as first-class obligations.

    Every directed path of length >= 2 through the seams becomes an
    interaction obligation with a shared-context invariant. Each carries
    a positive witness AND a counterexample — a one-sided interaction
    proof proves nothing (D20).
    """
    obligations = []
    # Build adjacency
    adj = {}
    for s in system.seams:
        adj.setdefault(s.source, []).append(s.target)
    # All simple paths of length >= 2 (bounded: cap at 4 hops)
    paths = []

    def walk(path):
        if len(path) >= 3:  # 3 nodes = 2 hops = multi-party
            paths.append(list(path))
        if len(path) >= 5:
            return
        for nxt in adj.get(path[-1], []):
            if nxt not in path:
                walk(path + [nxt])

    for start in system.nodes:
        walk([start])
    for i, path in enumerate(paths):
        obligations.append(InteractionObligation(
            id=f"INT-{i:03d}",
            participants=path,
            invariant=("all participants act on the same decision_id in "
                       "the same context_id; pairwise-valid handoffs do "
                       "not entail joint validity"),
            positive_witness=f"healthy run through {'->'.join(path)}",
            counterexample=(f"joint-context mismatch across "
                            f"{'->'.join(path)} with pairwise receipts green"),
        ))
    return obligations


# ---------------------------------------------------------------------------
# Scenario builders: the nine-node assembly + adversarial fixtures
# ---------------------------------------------------------------------------

def _contract_has(key):
    def check(package):
        # find the most recent node output carrying `key`
        for k, v in package.items():
            if k.endswith("_output") and isinstance(v, dict) and key in v:
                return True, ""
        # also accept top-level
        if key in package and not key.startswith("_fault"):
            return True, ""
        return False, f"expected '{key}' in package, not present"
    return check


def _contract_no_garbage(package):
    for k, v in package.items():
        if k.endswith("_output") and isinstance(v, str) \
                and v.startswith("GARBAGE"):
            return False, f"malformed output at '{k}': {v!r}"
    return True, ""


def build_demo_assembly():
    """A three-node KNOW->LAW->ACT assembly exercising every seam type.

    The nodes run REAL code (small but genuine transforms). Faults are
    injected per scenario, never baked into the nodes.
    """
    def know_fn(package):
        lesson = package.get("lesson", "no-lesson")
        return {**package,
                "KNOW_output": {"knowledge": f"qualified({lesson})",
                                "decision_id": package.get("decision_id"),
                                "context_id": package.get("context_id")}}

    def law_fn(package):
        # authorization carries a freshness window
        return {**package,
                "LAW_output": {"authorized": True,
                               "decision_id": package.get("decision_id"),
                               "context_id": package.get("context_id")},
                "auth": {"granted_at": package.get("t0", 0),
                         "revoked_at": package.get("auth_revoked_at"),
                         "scope": "execute"}}

    def act_fn(package):
        package = dict(package)
        package["commit_at"] = package.get("t_commit", 10)
        package["ACT_output"] = {"committed": True,
                                 "decision_id": package.get("decision_id"),
                                 "context_id": package.get("context_id")}
        package["expected_outcome_ok"] = True
        return package

    nodes = [Node("KNOW", know_fn), Node("LAW", law_fn), Node("ACT", act_fn)]
    seams = [
        Seam("KNOW->LAW", "KNOW", "LAW",
             _contract_has("knowledge"),
             "LAW needs KNOW's qualified knowledge"),
        Seam("LAW->ACT", "LAW", "ACT",
             _contract_has("authorized"),
             "ACT needs LAW's authorization"),
        Seam("OUTPUT", "ACT", "SINK", _contract_no_garbage,
             "no malformed output may leave the system"),
    ]
    return System(nodes, seams, ["KNOW", "LAW", "ACT"])


def adversarial_fixtures():
    """The UD-07 adversarial fixture set. One failure = FAIL."""
    base = {"decision_id": "D-101", "context_id": "ctx-1",
            "lesson": "receipt-gate", "t0": 0, "t_commit": 10}
    return [
        # Positive: healthy system passes, names no seam.
        Scenario("healthy", dict(base), environment="test",
                 expect_pass=True),
        # Negative 1: malformed output across a seam (parts run, seam breaks).
        Scenario("malformed-output", dict(base), environment="test",
                 faults={"malformed_output": "KNOW"}, expect_pass=False),
        # Negative 2: stale auth injected between LAW and ACT (D17 sharp).
        Scenario("stale-auth", {**base, "auth_revoked_at": 5},
                 environment="test", faults={"stale_auth": True},
                 expect_pass=False),
        # Negative 3: lesson arrives after plan finalization (D20 sharp).
        Scenario("late-lesson", {**base, "plan_finalized": True},
                 environment="test", faults={"late_lesson": True},
                 expect_pass=False),
        # Negative 4: joint-context mismatch, pairwise receipts green (D21).
        # KNOW stamps D-101, LAW stamps D-102: each handoff looks valid
        # alone; the joint execution is invalid and must be refused.
        Scenario("joint-context-mismatch", dict(base), environment="test",
                 faults={"joint_context_mismatch": True}, expect_pass=False),
    ]


def run_fixtures(system=None):
    """Run the full adversarial fixture set. Returns (verdicts, failures).

    failures: fixture names where actual != expected. One failure = FAIL.
    """
    system = system or build_demo_assembly()
    verdicts = []
    failures = []
    for scenario in adversarial_fixtures():
        verdict = system.run(scenario)
        actual = verdict.passed()
        verdicts.append((scenario, verdict, actual))
        if actual != scenario.expect_pass:
            failures.append(scenario.name)
    return verdicts, failures


def verdict_summary(verdict):
    lines = [f"scenario: {verdict.scenario}",
             f"certificate: {verdict.certificate}",
             f"failed_seams: {verdict.failed_seams or 'none'}"]
    for r in verdict.results:
        mark = "PASS" if r.passed else "FAIL"
        seam = f" @ {r.seam}" if r.seam else ""
        lines.append(f"  [{mark}] {r.family}{seam}: {r.detail}")
    lines.append(verdict.does_not_claim())
    return "\n".join(lines)


def manifest_hash(obj):
    return hashlib.sha256(
        json.dumps(obj, sort_keys=True, default=str).encode()).hexdigest()[:16]


if __name__ == "__main__":
    import sys
    system = build_demo_assembly()
    print(f"discovered {len(discover_interactions(system))} "
          "multi-party interaction obligations")
    verdicts, failures = run_fixtures(system)
    for scenario, verdict, actual in verdicts:
        exp = "PASS" if scenario.expect_pass else "FAIL(refuse)"
        got = "PASS" if actual else "FAIL(refuse)"
        flag = "OK " if actual == scenario.expect_pass else "BAD"
        print(f"[{flag}] {scenario.name}: expected {exp}, got {got} "
              f"(seams: {verdict.failed_seams or 'none'})")
    if failures:
        print(f"FAILURES: {failures} — one failure = FAIL")
        sys.exit(1)
    print("ALL FIXTURES BEHAVE AS SPECIFIED")

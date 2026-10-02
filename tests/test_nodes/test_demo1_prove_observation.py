"""Demo-1 P3 RED: PROVE/CONNECT handling of the handed-off KNOW observation.

The P2 ACT->KNOW handoff output plus the original ACT execution receipt are
verified again end-to-end (EXECUTED path, ACT seal recompute, receipt-hash
consistency with the handoff's observation, artifact re-hash, handoff
decision-receipt seal, KNOW block provenance) BEFORE PROVE ever sees them.
A post-action PROOF_CLAIM is built FROM the verified facts only:

  post-action proof = observation + outcome + acceptance + causal limits
                      + learning eligibility

Master-directive law enforced here:
- NEVER outcome-proof-before-ACT: no EXECUTED ACT execution, no claim.
- ACT success != outcome success: the claim bounds itself to the bound
  artifact bytes; no effect beyond them is asserted.
- PROVE never writes VERIFIED: the claim seals at SUPPORTED (L2/L4 map to
  SUPPORTED per the ratified V2 enum mapping, never VERIFIED).

The claim climbs the kernel's PROVE gate inside decide(); the sealed claim
crosses the CONNECT boundary via PROVE's crossing_check (nothing unproven
crosses). VERIFY/LEARN/EVOLVE remain named next actions.

Stated boundaries (not smuggled):
- The KNOW store is in-memory (test/runtime-local), never the production
  ledger. The handoff is replayed deterministically from the persisted
  ACT execution receipt + artifact bytes.
- The demo principal is a test identity; the real demo identity binding
  remains a named open question for Shawn.
- The ACT-verb receipt authorizing the staging execution still carries the
  suite's director_order test attestation (P1 boundary); full LAW-side
  minting inside the Python kernel remains a named gap.

RED state: naya_kernel.prove_observation does not exist — every test here
must FAIL until the GREEN implementation lands.
"""

import copy
import hashlib
import json
from pathlib import Path

import pytest

from naya_kernel import prove_observation as prove_obs  # noqa: F401 — RED
from naya_kernel import act_know_handoff as handoff
from naya_kernel import smart_door
from naya_kernel.kernel import Kernel, verify_decision_receipt
from naya_kernel.nodes import act_node

REPO_ROOT = Path(__file__).resolve().parents[2]
REGISTRY_PATH = REPO_ROOT / "BRAIN/10-INTERFACES/0002-SMART-DOOR-REGISTRY-V1.json"

TOOL_ID = "staging.write_file"
CONTENT = "# Demo-1 proof note\n\nACT->KNOW->PROVE.\n"
FILENAME = "sn-candidate-prove.md"

PRINCIPAL = {"identity": "naya-demo", "entitled_scopes": ["public", "team"]}
NOW = "2026-10-02T11:30:00+00:00"


def _auth_receipt(filename, content):
    return act_node.make_decision_receipt(
        receipt_id="dec-demo1-prove-001",
        issued_at="2026-10-01T02:00:00+00:00",
        valid_until="2026-10-03T00:00:00+00:00",
        winner={"tool_id": TOOL_ID, "version": "1.0",
                "params": {"filename": filename, "content": content}},
        authority_basis={"kind": "director_order", "ref": "order-demo-1",
                         "revoked": False},
    )


def _registry():
    reg = smart_door.load_registry(REGISTRY_PATH)
    door, operation = smart_door.find_operation(
        reg, "DOOR-LOCAL-STAGING", "staging.write_file")
    return {TOOL_ID: smart_door.project_act_tool_entry(door, operation)}


def _execute(filename=FILENAME, content=CONTENT, tmp_path=None):
    """A real ACT staging execution; returns the execution receipt."""
    node = act_node.ActNode(
        executor=smart_door.make_staging_executor(str(tmp_path)))
    out = node.execute({
        "decision_receipt": _auth_receipt(filename, content),
        "tool_registry": _registry(),
        "execution_ledger": {},
        "now": "2026-10-01T04:00:00+00:00",
        "_staging_root": str(tmp_path),
    })
    assert out["path"] == "EXECUTED", out
    return out["receipt"]


def _gate_states(kernel):
    """Full decide() gate states; PROVE is replaced by the module under
    test per call."""
    import sys
    sys.path.insert(0, str(REPO_ROOT / "tests"))
    import test_nodes.test_kernel_nine_node as T
    # Same explicit test-scope opt-in as test_kernel_nine_node.kernel():
    # this helper drives LEARN with synthetic receipts.
    from naya_kernel.nodes import learn_node as _learn_node
    kernel.nodes["LEARN"] = _learn_node.LearnNode(allow_fixture_intake=True)
    return kernel, {
        "SELF": T.self_state(), "LAW": T.law_state(), "ACT": T.act_state(),
        "KNOW": T.know_state(),
        "PROVE": T.prove_state(kernel), "CONNECT": T.connect_state(),
        "VERIFY": T.verify_state(kernel), "LEARN": T.learn_state(kernel),
        "EVOLVE": {"action": "metrics"},
    }


def _prove(kernel, gates, tmp_path, decision_id, act_receipt=None):
    """Run the full chain: ACT execute -> P2 handoff -> P3 prove.

    act_receipt overrides the receipt handed to P3 (the handoff always
    runs on the genuine execution receipt, so the override exercises
    P3's own consistency checks).
    """
    receipt = _execute(tmp_path=tmp_path)
    handoff_result = handoff.handoff_act_to_know(
        kernel, receipt, staging_root=str(tmp_path),
        principal=PRINCIPAL, gate_states=gates,
        decision_id="handoff-" + decision_id)
    return prove_obs.prove_observation(
        kernel, handoff_result, act_receipt or receipt,
        staging_root=str(tmp_path), principal=PRINCIPAL,
        gate_states=gates, decision_id=decision_id, now=NOW)


# ---------------------------------------------------------------------------
# 1. A tampered artifact after handoff refuses before PROVE is touched
# ---------------------------------------------------------------------------

def test_tampered_artifact_refuses_before_prove(tmp_path):
    kernel, gates = _gate_states(Kernel())
    receipt = _execute(tmp_path=tmp_path)
    handoff_result = handoff.handoff_act_to_know(
        kernel, receipt, staging_root=str(tmp_path),
        principal=PRINCIPAL, gate_states=gates,
        decision_id="handoff-demo1-prove-tampered")
    target = tmp_path / "demo-staging" / FILENAME
    with target.open("ab") as fh:
        fh.write(b"\nTampered after handoff.\n")

    with pytest.raises(prove_obs.ProveObservationRefused) as exc:
        prove_obs.prove_observation(
            kernel, handoff_result, receipt,
            staging_root=str(tmp_path), principal=PRINCIPAL,
            gate_states=gates, decision_id="demo1-prove-tampered", now=NOW)
    assert "sha" in str(exc.value).lower() or "hash" in str(exc.value).lower()
    prove = kernel.nodes["PROVE"]
    assert not any(cid.startswith("demo1-prove-obs-")
                   for cid in prove._claims), \
        "PROVE must hold no observation claim from a refused handoff"


# ---------------------------------------------------------------------------
# 2. No EXECUTED ACT execution -> no post-action proof (never
#    outcome-proof-before-ACT)
# ---------------------------------------------------------------------------

def test_no_executed_act_no_proof(tmp_path):
    kernel, gates = _gate_states(Kernel())
    receipt = _execute(tmp_path=tmp_path)
    handoff_result = handoff.handoff_act_to_know(
        kernel, receipt, staging_root=str(tmp_path),
        principal=PRINCIPAL, gate_states=gates,
        decision_id="handoff-demo1-prove-noexec")
    # The receipt handed to P3 never executed (ACT refused it); the seal
    # is beside the point — the earliest applicable refusal is the
    # boundary one.
    refused = copy.deepcopy(receipt)
    refused["path"] = "REFUSED"

    with pytest.raises(prove_obs.ProveObservationRefused) as exc:
        prove_obs.prove_observation(
            kernel, handoff_result, refused,
            staging_root=str(tmp_path), principal=PRINCIPAL,
            gate_states=gates, decision_id="demo1-prove-noexec", now=NOW)
    assert "no executed" in str(exc.value).lower() or \
        "before act" in str(exc.value).lower()


# ---------------------------------------------------------------------------
# 3. The claim never invents outcome beyond the verified facts
#    (ACT success != outcome success)
# ---------------------------------------------------------------------------

def test_claim_invents_nothing(tmp_path):
    kernel, gates = _gate_states(Kernel())
    receipt = _execute(tmp_path=tmp_path)
    handoff_result = handoff.handoff_act_to_know(
        kernel, receipt, staging_root=str(tmp_path),
        principal=PRINCIPAL, gate_states=gates,
        decision_id="handoff-demo1-prove-invent")
    verified = prove_obs.verify_observation_chain(
        kernel, handoff_result, receipt, str(tmp_path),
        principal=PRINCIPAL, now=NOW)
    # A caller tries to smuggle an inflated outcome into the verified facts.
    verified["claimed_outcome"] = "the user was notified by email"
    claim = prove_obs.build_post_action_claim(verified, now=NOW)

    texts = " ".join(a["text"] for a in claim["assertions"]).lower()
    assert "email" not in texts and "notified" not in texts, \
        "the claim must be built from verified facts only — nothing invented"
    assert "claimed_outcome" not in json.dumps(claim), \
        "injected keys must not reach the claim"
    # Every assertion is traceable to a verified fact.
    allowed = {verified["execution_id"][:8], verified["tool_id"],
               verified["artifact_sha256"][:16], verified["block_id"][:8]}
    for a in claim["assertions"]:
        assert any(token in a["text"] for token in allowed), \
            f"assertion not traceable to verified facts: {a['text']!r}"


# ---------------------------------------------------------------------------
# 4. The valid observation: verified -> PROVE PASS -> sealed -> CONNECT
#    crossing admitted
# ---------------------------------------------------------------------------

def test_valid_observation_proves_and_crosses(tmp_path):
    kernel, gates = _gate_states(Kernel())
    out = _prove(kernel, gates, tmp_path, "demo1-prove-001")

    assert out["prove_verdict"] == "PASS", out["prove_gate_reasons"]
    assert out["proof_level"] >= 2, "stakes low: required L2"
    prove = kernel.nodes["PROVE"]
    record = prove._claims[out["claim_id"]]
    assert record["sealed"] is True
    assert out["crossing"]["cross"] is True, out["crossing"]

    # The decision receipt is seal-bound and its inputs_hash recomputes
    # over the decided input state (the seam's recompute-or-reject).
    decision_receipt = out["decision_receipt"]
    assert verify_decision_receipt(decision_receipt)["result"] == "MATCH"
    canon = json.dumps(out["input_state"], sort_keys=True,
                       separators=(",", ":"), ensure_ascii=True)
    assert hashlib.sha256(canon.encode("utf-8")).hexdigest() == \
        decision_receipt["inputs_hash"]

    # The proof binds the whole chain: act receipt hash, artifact hash,
    # handoff decision receipt hash, and KNOW block id are all inside
    # the decided input state.
    blob = json.dumps(out["input_state"])
    obs = out["observation"]
    for token in (obs["receipt_hash"], obs["artifact_sha256"],
                  out["block_id"]):
        assert token in blob, f"chain token missing from decided state: {token[:16]}…"


# ---------------------------------------------------------------------------
# 5. A challenged claim is refused at the CONNECT boundary
#    (nothing unproven crosses)
# ---------------------------------------------------------------------------

def test_challenged_claim_refused_at_crossing(tmp_path):
    kernel, gates = _gate_states(Kernel())
    out = _prove(kernel, gates, tmp_path, "demo1-prove-challenge")
    prove = kernel.nodes["PROVE"]

    counter = [{"address": "ev-counter-1", "source": "adversarial-read",
                "acquisition_method": "manual-inspection",
                "acquired_at": NOW, "qualified_oracle": True,
                "failure_mode": "human-error", "independent_of_claim": True,
                "restates_claim": False}]
    prove.challenge(out["claim_id"], counter)
    crossing = prove.crossing_check(out["claim_id"])
    assert crossing["cross"] is False, \
        "a claim disturbed after sealing must not cross to CONNECT"


# ---------------------------------------------------------------------------
# 6. G5 independence is non-vacuous: a failed re-derivation holds the
#    claim below L3
# ---------------------------------------------------------------------------

def test_failed_rederivation_holds_below_l3(tmp_path):
    kernel, gates = _gate_states(Kernel())
    receipt = _execute(tmp_path=tmp_path)
    handoff_result = handoff.handoff_act_to_know(
        kernel, receipt, staging_root=str(tmp_path),
        principal=PRINCIPAL, gate_states=gates,
        decision_id="handoff-demo1-prove-g5")
    verified = prove_obs.verify_observation_chain(
        kernel, handoff_result, receipt, str(tmp_path),
        principal=PRINCIPAL, now=NOW)
    claim = prove_obs.build_post_action_claim(verified, now=NOW)
    # Kill the independence record: re-derivation disagrees.
    claim["recompute"] = {"independence_dimension": "code_path",
                         "can_disagree": True, "result": "MISMATCH"}

    prove = kernel.nodes["PROVE"]
    prove.submit(claim, PRINCIPAL)
    for _ in range(4):
        prove.advance(claim["id"], principal=PRINCIPAL)
    record = prove._claims[claim["id"]]
    assert record["maturity_level"] == 2, \
        "G5 failure must cap the claim at L2 — the re-derivation gate is real"
    assert record["sealed"] is True  # stakes low: L2 is the required level

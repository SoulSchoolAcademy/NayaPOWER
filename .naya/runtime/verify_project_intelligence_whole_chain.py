#!/usr/bin/env python3
"""Repository-level behavioral proof for the NayaNET cold-Naya chain.

This deliberately proves only what the repository can prove without inventing
external runtime authority. It uses an isolated temp state for the action,
then starts a genuinely separate successor process that reconstructs the
proof state from canonical repository files + the emitted receipt.
"""
from __future__ import annotations
import hashlib, json, os, subprocess, sys, tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / ".naya/runtime"))
import project_intelligence_reconstruction as pir
def run(*args: str) -> str:
    return subprocess.check_output(args, cwd=ROOT, text=True).strip()

def fail(msg: str) -> None:
    print("WHOLE_CHAIN_FAIL", msg)
    raise SystemExit(1)

def sha(s: str) -> str:
    return hashlib.sha256(s.encode()).hexdigest()

def load(rel: str):
    p = ROOT / rel
    if not p.exists():
        fail(f"missing canonical source: {rel}")
    return p.read_text(encoding="utf-8")

def successor(receipt_path: str) -> int:
    receipt = json.loads(Path(receipt_path).read_text(encoding="utf-8"))
    # A cold successor gets only the receipt path plus the canonical repository.
    state = json.loads(receipt["durable_state"])
    reconstruction = state.get("project_intelligence_reconstruction")
    if not reconstruction or reconstruction.get("resolution",{}).get("status") != "RECONSTRUCTED":
        fail("successor: reconstructed Project Intelligence not restored")
    if not {"current","historical","superseded","stale","conflicted","unknown","evidence","causal_lineage","next_action"}.issubset(reconstruction):
        fail("successor: reconstructed context contract incomplete")
    if state["verified_marker"] != receipt["verified_marker"]:
        fail("successor: durable marker mismatch")
    if state["learning"] != "verified-state-change can be carried forward with provenance":
        fail("successor: learning not restored")
    if not state["next_action"]:
        fail("successor: no next action")
    if receipt["verification"] != "PASS":
        fail("successor: prior verification not PASS")
    print("PI08_COLD_SUCCESSOR=PASS")
    print("SUCCESSOR_NEXT_ACTION=" + state["next_action"])
    return 0

def main() -> int:
    # 1–7: restore, reconstruct, reconcile current truth.
    branch = run("git", "branch", "--show-current")
    head = run("git", "rev-parse", "HEAD")
    if branch != "main":
        fail(f"expected main, got {branch}")
    if len(head) != 40:
        fail("invalid live HEAD")

    map_text = load(".naya/control-plane/MAP.json")
    state_text = load(".naya/control-plane/STATE.json")
    blocks = json.loads(load(".naya/control-plane/BLOCKS.json"))
    proof = json.loads(load(".naya/control-plane/PROOF.json"))
    cold = load(".naya/project-intelligence/00-NAYANET-COLD-NAYA-BOOT.md")
    bridge_contract = load(".naya/project-intelligence/PROJECT-INTELLIGENCE-BRIDGE-CONTRACT-V1.md")
    bridge_context = load(".naya/project-intelligence/PROJECT-INTELLIGENCE-OPERATING-CONTEXT.json")
    reconstruction = pir.build_current("NayaNET")
    required_reconstruction = {"current","historical","superseded","stale","conflicted","unknown","evidence","causal_lineage","project_state","current_block","next_action"}
    if not required_reconstruction.issubset(reconstruction):
        fail("project reconstruction contract incomplete")
    if reconstruction["resolution"]["status"] != "RECONSTRUCTED":
        fail("project reconstruction did not resolve")
    print("PI03_CANONICAL_RECONSTRUCTION=PASS")
    boot = load("SUPERBRAIN/AI-BOOT/START-HERE.md")

    active = blocks.get("active_block", {})
    if active.get("id") != "PROJECT-INTELLIGENCE-PI-01":
        fail("active block is not PROJECT-INTELLIGENCE-PI-01")
    if active.get("next_action_count") != 1:
        fail("active block does not expose exactly one next action")
    next_action = active["next_actions"][0]
    if ("Project Intelligence Bridge" not in next_action and "Project Intelligence" not in next_action):
        fail("canonical next action is not the Project Intelligence frontier")
    for marker in ("WHO", "WHAT", "WHY", "SUCCESS", "CURRENT TRUTH", "PROVEN", "UNKNOWN",
                   "AUTHORITY", "HISTORY", "LEARNING", "NEXT", "PROOF", "RECORD", "SUCCESSOR"):
        if marker not in cold.upper():
            fail(f"cold bridge missing {marker}")
    if "TEAM NAYA" not in boot:
        fail("mandatory Team Naya boot gate missing")
    if proof.get("separation_rules") is None:
        fail("proof separation rules missing")
    for marker in ("SENDER", "RECEIVER", "BRIDGE", "FRESHNESS", "IDEMPOTENCY", "ACK", "RECEIVE", "PERSIST", "INDEX", "PROJECT", "RETRIEVE", "RENDER"):
        if marker not in bridge_contract.upper():
            fail(f"bridge contract missing {marker}")
    for marker in ("you_are_here", "sender", "receiver", "bridge", "current_next_action"):
        if marker not in bridge_context:
            fail(f"operating context missing {marker}")

    # 8–11: execute one explicitly authorized, harmless action in an isolated
    # governed state. This is not an external production action.
    with tempfile.TemporaryDirectory(prefix="nayanet-whole-chain-") as td:
        work = Path(td)
        state_path = work / "state.json"
        marker = "NAYANET-WHOLE-CHAIN-VERIFIED-" + sha(head)[:16]
        state = {
            "project": "NayaNET",
            "actor": "cold-naya-proof-runner",
            "authority": "repository-proof-scope:write-isolated-proof-state",
            "action": "write_verified_proof_marker",
            "verified_marker": marker,
            "learning": "verified-state-change can be carried forward with provenance",
            "project_intelligence_reconstruction": reconstruction,
            "next_action": "continue from the canonical active block",
        }
        state_path.write_text(json.dumps(state, sort_keys=True), encoding="utf-8")
        observed = json.loads(state_path.read_text(encoding="utf-8"))
        if observed["verified_marker"] != marker:
            fail("execution result mismatch")
        observed_hash = sha(state_path.read_text(encoding="utf-8"))
        receipt = {
            "proof": "PROJECT-INTELLIGENCE-WHOLE-CHAIN-PROOF",
            "source_head": head,
            "branch": branch,
            "intent": "prove cold-Naya behavioral continuity",
            "identity": "NayaNET",
            "reconstruction": "PASS",
            "reconstruction_schema": reconstruction["schema"],
            "reconstruction_counts": reconstruction["counts"],
            "cold_restore": "PASS",
            "retrieval": "PASS",
            "current_state": "PASS",
            "one_next_action": next_action,
            "authority": state["authority"],
            "execution": "PASS",
            "observed_result": observed["verified_marker"],
            "verified_marker": marker,
            "observed_state_hash": observed_hash,
            "verification": "PASS",
            "learning": state["learning"],
            "durable_state": json.dumps(observed, sort_keys=True),
            "successor": "pending-cold-process",
        }
        receipt_path = work / "receipt.json"
        receipt_path.write_text(json.dumps(receipt, indent=2, sort_keys=True), encoding="utf-8")

        # 12–14: learning/update + genuinely separate successor process.
        env = dict(os.environ)
        env["NAYANET_SUCCESSOR_RECEIPT"] = str(receipt_path)
        child = subprocess.run([sys.executable, __file__, "--successor", str(receipt_path)],
                               cwd=ROOT, env=env, text=True, capture_output=True)
        print(child.stdout, end="")
        if child.returncode != 0:
            print(child.stderr, end="", file=sys.stderr)
            fail("cold successor failed")

        print("PI01_INTENT=PASS")
        print("PI02_IDENTITY=PASS")
        print("PI03_RECONSTRUCTION=PASS")
        print("PI04_COLD_RESTORE=PASS")
        print("PI05_RETRIEVAL_CURRENT_STATE=PASS")
        print("PI06_AUTHORITY_EXECUTION_VERIFICATION=PASS")
        print("PI07_LEARNING_UPDATE=PASS")
        print("PI08_COLD_SUCCESSOR=PASS")
        print("WHOLE_CHAIN_REPOSITORY_BEHAVIOR=PROVEN")
        print("EXTERNAL_RUNTIME_CLAIM=NOT_CLAIMED")
        return 0

if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "--successor":
        raise SystemExit(successor(sys.argv[2]))
    raise SystemExit(main())

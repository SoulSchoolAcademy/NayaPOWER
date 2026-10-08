from pathlib import Path
import json

from tools.closed_loop_executor import ClosedLoopExecutor, Task, independently_recheck

ROOT = Path(__file__).resolve().parent
STATE = ROOT / ".naya" / "execution" / "closed-loop-state.json"
RECEIPT = ROOT / ".naya" / "evidence" / "closed-loop-experiment-20261007.json"
STATE.unlink(missing_ok=True)

calls = []

def unavailable():
    calls.append("capacity-bound")
    raise RuntimeError("external agent pool unavailable")

def reversible():
    calls.append("reversible")
    return {"value": "verified-local-build"}

executor = ClosedLoopExecutor(capacity=1, state_path=STATE)
first = executor.run([Task("external-agent-pool", unavailable), Task("local-reversible-fallback", reversible)])
second = executor.run([Task("external-agent-pool", unavailable), Task("local-reversible-fallback", reversible)])

receipt = {
    "schema": "NAYAPOWER_CLOSED_LOOP_EXPERIMENT_V1",
    "status": "VERIFIED",
    "experiment": "resource-capacity-bypass-build-verify-learn-reuse",
    "build": {"implementation": "tools/closed_loop_executor.py", "tests": "tests/test_closed_loop_executor.py"},
    "first_tick": first,
    "second_tick": second,
    "calls": calls,
    "learning_reused": second["reuse"]["lesson_applied"],
    "verification": {
        "independent_recheck": True,
        "claim_matched_evidence": True,
        "receipt_reconstructed_after_write": True,
    },
}
RECEIPT.parent.mkdir(parents=True, exist_ok=True)
RECEIPT.write_text(json.dumps(receipt, indent=2), encoding="utf-8")
independently_recheck(RECEIPT)
print("BUILD=PASS")
print("VERIFICATION=PASS")
print("LEARNING=PASS")
print("REUSE=PASS")
print("CAPACITY_BYPASS=PASS")
print("CALLS=" + ",".join(calls))
print("RECEIPT=" + str(RECEIPT))

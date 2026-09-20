#!/usr/bin/env python3
"""Repository-level acceptance test for the canonical `NAYA POWER ON` contract.

This test proves that the activation contract is present, canonical, connected to
START HERE, and explicitly defines the behavioral acceptance questions. It does not
claim that an external LLM has followed the contract; that requires a fresh-runtime
behavioral test.
"""
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
ACTIVATION = ROOT / "SUPERBRAIN/AI-BOOT/NAYA-POWER-ACTIVATION-PROTOCOL.md"
START = ROOT / "SUPERBRAIN/AI-BOOT/START-HERE.md"
COLD = ROOT / ".naya/runtime/cold_start_activation.py"

def require(text, needle, label):
    if needle not in text:
        raise AssertionError(f"{label}: missing required contract: {needle}")

def main():
    activation = ACTIVATION.read_text(encoding="utf-8")
    start = START.read_text(encoding="utf-8")
    cold = COLD.read_text(encoding="utf-8")

    require(activation, "NAYA POWER ON", "activation keyword")
    require(activation, "NayaPOWER is the operating system", "activation identity")
    require(activation, "RESTORE is the first mandatory operating phase", "activation sequence")
    require(activation, "WHY IS THIS NOT A 10?", "mirror gate")
    require(activation, "CAR-BUILDER TEST", "completeness gate")
    require(activation, "QUESTION → SEARCH → AUTHORITY CHECK", "question closure")
    for question in ("WHAT", "WHY", "WHERE", "AUTHORITY", "PROTECTED", "CURRENT STATE", "CURRENT GAP", "NEXT ACTION", "PROOF", "HANDOFF"):
        require(activation, question, "cold-start acceptance question")

    require(start, "NAYA POWER ON", "START HERE activation")
    require(start, "NAYA-POWER-ACTIVATION-PROTOCOL.md", "START HERE activation protocol")
    require(start, "canonical **NAYA POWER ON** activation contract", "START HERE cold-start boundary")
    require(cold, "ACTIVATED", "cold-start activation state")

    print("NAYA POWER ON repository contract: PASS")
    print("External fresh-Naya behavioral execution: NOT CLAIMED")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())

"""Deterministic conformance checks for the human-agency/reality governance contract."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "SUPERBRAIN" / "UNIVERSAL-INTERFACE-AND-CONTROL-SUBSTRATE-CONTRACT.md"


def main() -> int:
    text = CONTRACT.read_text(encoding="utf-8")
    required = [
        "Human authority",
        "Reality",
        "Naya judgment",
        "System authority",
        "UNDERSTAND → INFORM → CHALLENGE → RECOMMEND → CONFIRM → ACT",
        "must never silently collapse into one",
        "must not silently redefine the mission",
        "Meaningful human authority boundaries require confirmation",
        "Naya may refuse only when a higher-order constraint prevents responsible execution",
        "Naya must never silently substitute its judgment for human authority",
        "must never sacrifice truth merely to satisfy human authority",
        "STORAGE ≠ AUTHORITY",
    ]
    missing = [item for item in required if item not in text]
    if missing:
        raise AssertionError("Missing governance invariants: " + ", ".join(missing))
    print("PASS — human agency/reality governance contract contains all required invariants")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

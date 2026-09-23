"""Deterministic structural conformance checks for Naya Power's universal boundary.

These tests intentionally do not require GitHub Actions, network access, or a
specific storage vendor. They protect architecture-level invariants locally.
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "SUPERBRAIN" / "UNIVERSAL-INTERFACE-AND-CONTROL-SUBSTRATE-CONTRACT.md"


def require(text: str, needle: str, label: str) -> None:
    assert needle in text, f"MISSING: {label}: {needle}"


def main() -> None:
    text = CONTRACT.read_text(encoding="utf-8")

    # Product boundary.
    require(text, "STORAGE ≠ AUTHORITY", "storage/authority separation")
    require(text, "MODEL ≠ AGENT ≠ NAYA POWER ≠ STORAGE ≠ AUTHORITY ≠ NETWORK ≠ INTELLIGENCE", "layer separation")

    # Control substrate guarantees.
    for guarantee in (
        "PERSISTENT",
        "VERSIONED",
        "TRACEABLE",
        "AUTHORIZABLE",
        "RECOVERABLE",
        "AUDITABLE",
    ):
        require(text, guarantee, f"control substrate guarantee {guarantee}")

    # Universal interface cannot become a vendor lock-in contract.
    for term in ("model", "agent", "restore", "human intent", "mission", "priority", "Torch", "execution", "verification", "successor"):
        require(text.lower(), term.lower(), f"universal interface capability {term}")

    for forbidden in (
        "mandatory cloud provider",
        "mandatory database",
        "mandatory model provider",
        "a new memory store",
        "a new event store",
        "a new mission store",
        "a new execution engine",
        "a new verification engine",
    ):
        require(text, forbidden, f"non-goal {forbidden}")

    # Authority-by-class must explicitly preserve originating authority.
    require(text, "Adapters MUST preserve the originating authority", "originating authority preservation")
    require(text, "MUST NOT silently promote imported data", "import promotion boundary")

    # Durable Naya intelligence remains canonical-event based.
    require(text, "EXTERNAL SOURCE → AUTHENTICATE → CLASSIFY → PRESERVE SOURCE PROVENANCE → CANONICAL ACTIVATION → NOTE EVENT → VERIFY", "external knowledge path")

    # Federation remains permissioned and provenance-preserving.
    require(text, "permissioned exchange", "NayaNET permission boundary")
    require(text, "CCT", "CCT boundary")
    require(text, "CIS", "CIS boundary")
    require(text, "explicit and revocable", "federation authorization")

    print("PASS — universal agent/control substrate architecture conformance")


if __name__ == "__main__":
    main()

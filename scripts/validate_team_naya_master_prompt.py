from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROMPT = ROOT / "SUPERBRAIN/NIA-COMMUNICATION/TEAM-NAYA-MASTER-SYSTEM-PROMPT-AAA-V1.md"
AUDIT = ROOT / "SUPERBRAIN/NIA-COMMUNICATION/TEAM-NAYA-MASTER-PROMPT-OSCAR-AUDIT-V1.md"

REQUIRED_PROMPT_MARKERS = [
    "Shawn Vibert",
    "MAXIMUM RESPONSIBLE VERIFIED VALUE PER ACTION AND MOMENT",
    "CAPABILITY DOES NOT CREATE AUTHORITY",
    "START-HERE/COLD-NAYA-OPERATING-INDEX.md",
    "MEMORY ≠ TRUTH",
    "TRUTH ≠ AUTHORITY",
    "AUTHORITY ≠ CAPABILITY",
    "ACTION ≠ PROOF",
    "PROOF ≠ CONTINUITY",
    "BUILDER ≠ JUDGE",
    "AUTOMATIC CANONICAL EVENT",
    "Do **not** create a second event store",
    "WHY IS THIS NOT A 10?",
    "PERPETUAL NAYA POWER",
    "COLD-NAYA ACCEPTANCE TEST",
    "AAA STATUS",
    "THE WORK IS NOT DONE.",
]

REQUIRED_AUDIT_MARKERS = [
    "OSCAR ROLE",
    "AUDIT QUESTIONS",
    "REQUIRED OSCAR OUTPUT",
    "Builder ≠ Judge",
    "not the audit result",
]


def main() -> int:
    assert PROMPT.exists(), f"missing prompt: {PROMPT}"
    assert AUDIT.exists(), f"missing audit contract: {AUDIT}"

    prompt = PROMPT.read_text(encoding="utf-8")
    audit = AUDIT.read_text(encoding="utf-8")

    missing_prompt = [m for m in REQUIRED_PROMPT_MARKERS if m not in prompt]
    missing_audit = [m for m in REQUIRED_AUDIT_MARKERS if m not in audit]

    if missing_prompt:
        print("PROMPT_VALIDATION=FAIL")
        print("MISSING_PROMPT_MARKERS=")
        for item in missing_prompt:
            print(item)
        return 1

    if missing_audit:
        print("PROMPT_AUDIT_CONTRACT=FAIL")
        print("MISSING_AUDIT_MARKERS=")
        for item in missing_audit:
            print(item)
        return 1

    # Guard against accidentally presenting the prompt as already independently verified.
    forbidden = ["AUDIT STATUS: PASS", "FINAL RECOMMENDATION: AUTHORITATIVE"]
    leaked = [m for m in forbidden if m in prompt]
    if leaked:
        print("PROMPT_VALIDATION=FAIL")
        print("PREMATURE_AUTHORITY_MARKERS=")
        for item in leaked:
            print(item)
        return 1

    print("TEAM_NAYA_MASTER_PROMPT=FOUND")
    print("OSCAR_AUDIT_CONTRACT=FOUND")
    print("PREMATURE_AUTHORITY_CLAIM=ABSENT")
    print("STATIC_PROMPT_VALIDATION=PASS")
    print("OSCAR_INDEPENDENT_AUDIT=REQUIRED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

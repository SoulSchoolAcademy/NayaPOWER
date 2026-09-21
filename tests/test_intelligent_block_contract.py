from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

constitution = ROOT / ".naya/00-NAYAPOWER-UNIVERSAL-AI-SERVICE-CONSTITUTION-V2.md"
constitution_yaml = ROOT / ".naya/00-NAYAPOWER-UNIVERSAL-AI-SERVICE-CONSTITUTION-V2.yaml"
block_md = ROOT / "contracts/intelligent-block-v1.md"
block_schema = ROOT / "contracts/intelligent-block-v1.schema.json"
block_yaml = ROOT / "contracts/intelligent-block-v1.yaml"
activation = ROOT / ".naya/TEAM-NAYA/00-START-HERE-FOR-EVERY-NAYA.md"
pointer = ROOT / "NAYAPOWER-AI-CONSTITUTION.md"

required_files = [
    constitution,
    constitution_yaml,
    block_md,
    block_schema,
    block_yaml,
    activation,
    pointer,
]

for path in required_files:
    assert path.exists(), f"Missing canonical contract: {path}"

text = constitution.read_text(encoding="utf-8")
for marker in [
    "CURRENT / CANONICAL / SUPREME INTERNAL AI GOVERNANCE",
    "CAPABILITY DOES NOT CREATE AUTHORITY.",
    "MAXIMUM RESPONSIBLE VERIFIED VALUE PER ACTION PER MOMENT",
    "DO NOT MERELY ANSWER. HELP THE HUMAN SUCCEED.",
]:
    assert marker in text, f"Constitution marker missing: {marker}"

schema = json.loads(block_schema.read_text(encoding="utf-8"))
assert schema["$id"] == "https://nayanet.app/contracts/intelligent-block-v1.schema.json"
assert schema["title"] == "NayaNET Intelligent Block V1"
assert schema["properties"]["identity"]["properties"]["schema_version"]["const"] == "NAYANET_INTELLIGENT_BLOCK_V1"

# Validate the portable YAML with Ruby's standard YAML parser when available in CI.
# The contract gate also checks the canonical schema identifier without requiring
# third-party Python dependencies.
import subprocess

yaml_check = subprocess.run(
    [
        "ruby",
        "-e",
        (
            "require 'yaml'; "
            "x=YAML.load_file(ARGV[0]); "
            "raise 'schema_version mismatch' unless x['schema_version']=='NAYANET_INTELLIGENT_BLOCK_V1'; "
            "puts 'YAML_OK'"
        ),
        str(block_yaml),
    ],
    capture_output=True,
    text=True,
)
assert yaml_check.returncode == 0, yaml_check.stderr or yaml_check.stdout

activation_text = activation.read_text(encoding="utf-8")
assert ".naya/00-NAYAPOWER-UNIVERSAL-AI-SERVICE-CONSTITUTION-V2.md" in activation_text
assert "contracts/intelligent-block-v1.schema.json" in activation_text

pointer_text = pointer.read_text(encoding="utf-8")
assert ".naya/00-NAYAPOWER-UNIVERSAL-AI-SERVICE-CONSTITUTION-V2.md" in pointer_text
assert "contracts/intelligent-block-v1.md" in pointer_text
assert "contracts/intelligent-block-v1.schema.json" in pointer_text

print("INTELLIGENT_CONTRACT_GATE: PASS")

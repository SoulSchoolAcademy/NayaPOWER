from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / ".naya/runtime/deployment_verification.py"

def test_deployment_verifier_expected_hub_sha_matches_current_canonical_source():
    source = SCRIPT.read_text(encoding="utf-8")
    expected = re.search(r'CANONICAL_HUB_SOURCE_SHA = "([0-9a-f]+)"', source).group(1)
    actual = subprocess.check_output(
        ["git", "rev-parse", "HEAD:NAYANET/HUB/index.html"],
        cwd=ROOT,
        text=True,
    ).strip()
    assert expected == actual

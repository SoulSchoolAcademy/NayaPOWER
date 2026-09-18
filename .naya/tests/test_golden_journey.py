from pathlib import Path
import importlib.util

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts/verify-golden-journey.py"


def test_golden_journey_contract():
    spec = importlib.util.spec_from_file_location("golden_journey", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    receipt = mod.run()
    assert receipt["status"] == "VERIFIED_REPOSITORY_GOLDEN_JOURNEY"


if __name__ == "__main__":
    test_golden_journey_contract()
    print("GOLDEN_JOURNEY_CONTRACT=PASS")

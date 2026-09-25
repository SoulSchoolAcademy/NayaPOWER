import importlib.util
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / ".naya/runtime/deployment_verification.py"

def load_verifier():
    spec = importlib.util.spec_from_file_location("deployment_verification", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

class FakeResponse:
    status = 200
    def read(self):
        return b"<html>old deployed hub</html>"

def test_runtime_deployment_fails_when_live_hub_lacks_canonical_deep_link(monkeypatch):
    module = load_verifier()
    monkeypatch.setattr(urllib.request, "urlopen", lambda *args, **kwargs: FakeResponse())
    verifier = module.DeploymentVerifier()
    assert verifier.check_runtime_deployment() is False
    assert verifier.results["checks"]["runtime_deployment"]["status"] == "FAIL"
    assert verifier.results["checks"]["runtime_deployment"]["reason"] == "LIVE_SOURCE_MISSING_DEEP_LINK_CONTRACT"

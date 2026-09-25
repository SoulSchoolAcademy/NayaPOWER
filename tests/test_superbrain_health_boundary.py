from pathlib import Path
import importlib.util
ROOT = Path(__file__).resolve().parents[1]
path = ROOT / '.naya/memory/superbrain_health.py'
spec = importlib.util.spec_from_file_location('superbrain_health', path)
module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
def test_health_reports_unknown_when_continuity_policy_is_missing(monkeypatch):
    monkeypatch.setattr(module, 'load_policy', lambda: (_ for _ in ()).throw(FileNotFoundError('missing policy')))
    result = module.report()
    assert result['status'] == 'UNKNOWN'
    assert result['health_unknown'] == ['continuity_enforcement_policy_missing']

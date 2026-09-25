from pathlib import Path
import importlib.util
import sys

ROOT = Path(__file__).resolve().parents[1]
path = ROOT / ".naya/runtime/core_intelligence_reconciliation.py"
spec = importlib.util.spec_from_file_location("cir_p5", path)
mod = importlib.util.module_from_spec(spec)
sys.modules["cir_p5"] = mod
spec.loader.exec_module(mod)


def test_dict_unknown_verification_fails_closed():
    current = [{"block_id": "B1", "semantic_key": "memory", "claim": "current"}]
    result = mod.reconcile(
        {
            "meaning": "memory",
            "semantic_key": "memory",
            "claim": "new",
            "verification": {"status": "UNKNOWN"},
        },
        current,
    )
    assert result.disposition == mod.Disposition.UNCERTAIN
    assert not result.current_update_allowed


def test_dict_verified_status_can_reconcile_explicit_extension():
    current = [{"block_id": "B1", "semantic_key": "memory", "claim": "current"}]
    result = mod.reconcile(
        {
            "meaning": "memory",
            "semantic_key": "memory",
            "claim": "extended",
            "verification": {"status": "VERIFIED"},
            "extends": "B1",
        },
        current,
    )
    assert result.disposition == mod.Disposition.EXTEND
    assert result.current_update_allowed

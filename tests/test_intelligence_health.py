from pathlib import Path
import importlib.util

ROOT = Path(__file__).resolve().parents[1]
path = ROOT / ".naya/runtime/intelligence_health.py"
spec = importlib.util.spec_from_file_location("intelligence_health", path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def test_health_report_measures_useful_boundaries_without_claiming_runtime_parity():
    result = module.report()
    assert result["schema"] == "NAYAPOWER_INTELLIGENCE_HEALTH_V1"
    assert result["metrics"]["canonical_repository_ib_ids_unique"]
    assert result["metrics"]["canonical_repository_retrieval_surface_valid"]
    assert result["interpretation"]["repository_projection_is_not_the_full_live_runtime_population"]
    assert result["interpretation"]["production_proof_is_separate_from_repository_health"]

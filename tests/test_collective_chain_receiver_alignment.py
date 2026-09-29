from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "BRAIN/12-ENGINEERING/COLLECTIVE-INTELLIGENCE-CHAIN-READINESS-V1.json"
GATE = ROOT / "BRAIN/12-ENGINEERING/verify-collective-chain-readiness.py"
CONTROLS = ROOT / "BRAIN/12-ENGINEERING/verify-collective-chain-readiness-controls.py"


def test_collective_chain_uses_current_governed_intelligence_commit_boundary():
    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
    l01 = next(x for x in contract["links"] if x["id"] == "L01")
    assert l01["identity_allocator"] == "supabase/functions/nayanet-intelligence-commit-runtime/index.ts"
    assert "nayanet_intelligent_blocks" in " ".join(l01["evidence"])
    assert "v7-smart-note-canonical" not in json.dumps(l01)


def test_readiness_gate_and_controls_do_not_use_legacy_v7_receiver_as_runtime_probe():
    gate = GATE.read_text(encoding="utf-8-sig")
    controls = CONTROLS.read_text(encoding="utf-8-sig")
    assert "supabase/functions/nayanet-intelligence-commit-runtime/index.ts" in gate
    assert "supabase/functions/nayanet-intelligence-commit-runtime/index.ts" in controls
    assert "v7-smart-note-canonical" not in gate
    assert "v7-smart-note-canonical" not in controls

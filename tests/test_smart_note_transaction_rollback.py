from pathlib import Path
import importlib.util

ROOT=Path(__file__).resolve().parents[1]
TX=ROOT/".naya/runtime/smart_note_transaction.py"

NOTE={
"topic":"Rollback Proof","in_a_nutshell":"x","child":"x","grammar":"x","human":"x","naya":"x","machine":"x",
"learning":"x","why_it_matters":"x","how_to_use":"x","value":"x","evidence":["rollback-test"],
"current_state":"before","next_action":"retry safely"
}

def load():
    spec=importlib.util.spec_from_file_location("rollback_tx",TX)
    mod=importlib.util.module_from_spec(spec); assert spec.loader is not None
    spec.loader.exec_module(mod); return mod

def test_transaction_rolls_back_partial_writes(tmp_path):
    mod=load()
    mod.ROOT=tmp_path
    mod.SMART_NOTES_ROOT=tmp_path/"SUPERBRAIN/SMART-NOTES"
    mod.CIS_ROOT=tmp_path/".naya/memory/intelligence"
    mod.CIS_PATH=mod.CIS_ROOT/"CIS.json"
    mod.RECEIPTS_ROOT=mod.CIS_ROOT/"transactions"
    mod.PIS_PATH=tmp_path/"NAYANET/HUB/public/intelligence/pis-feed.json"
    def fail(_note):
        raise RuntimeError("simulated projection failure")
    mod.build_pis_projection=fail
    try:
        mod.execute({**NOTE,"timestamp":"2099-01-01T12:00:00+00:00"})
    except RuntimeError as exc:
        assert "simulated projection failure" in str(exc)
    else:
        raise AssertionError("failure was not surfaced")
    assert not list((tmp_path/"SUPERBRAIN/SMART-NOTES").rglob("*.md"))
    assert not (tmp_path/".naya/memory/intelligence/CIS.json").exists()
    assert not (tmp_path/"NAYANET/HUB/public/intelligence/pis-feed.json").exists()

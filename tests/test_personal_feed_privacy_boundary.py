import importlib.util
from pathlib import Path
import pytest

ROOT=Path(__file__).resolve().parents[1]
TX=ROOT/".naya/runtime/smart_note_transaction.py"

def load():
    spec=importlib.util.spec_from_file_location("privacy_boundary",TX)
    mod=importlib.util.module_from_spec(spec); assert spec.loader is not None
    spec.loader.exec_module(mod); return mod

def test_personal_feed_rejects_non_private_event():
    mod=load()
    event={"event_id":"E-1","privacy":{"visibility":"shared","consent_state":"not_granted"},"source":{"label":"bad"}}
    with pytest.raises(RuntimeError,match="private-by-default"):
        mod.build_personal_feed_block(event)

def test_personal_feed_accepts_private_not_granted_event():
    mod=load()
    event={"event_id":"E-2","privacy":{"visibility":"private","consent_state":"not_granted"},"source":{"label":"good"},"lesson":{"text":"L"},"action":{"text":"A"},"weaver_synthesis":{"summary":"S"},"meaning":{"text":"M"},"machine_evidence":{"items":[]}}
    block=mod.build_personal_feed_block(event)
    assert block["permissions"]=={"consumers":["nayanet-hub.personal-feed"],"purposes":["consume"]}
    assert block["verification"]=="SUPPORTED"
    assert block["lifecycle"]=="ACTIVE"

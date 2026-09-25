from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
RECEIVER = ROOT / "supabase/functions/v7-smart-note-canonical/index.ts"


def test_receiver_does_not_construct_or_accept_a_competing_ib_identity():
    source = RECEIVER.read_text(encoding="utf-8")
    assert 'object_id:"IB:"+args.eventId' not in source
    assert 'identity?.intelligent_block_id||persistedBlock?.identity?.object_id' not in source


def test_receiver_returns_only_canonical_ib_identity_format():
    source = RECEIVER.read_text(encoding="utf-8")
    assert re.search(r'intelligentBlockId[^\\n]*\\^IB-\\\\d\\{6\\}', source)

from pathlib import Path
import json
import subprocess

ROOT = Path(__file__).resolve().parents[1]
RUNTIME = ROOT / "NAYANET/HUB/public/assistant-runtime.js"
SENDER = ROOT / ".github/scripts/universal-envelope-hub-runtime-sender.mjs"
NODE_TEST = ROOT / ".github/scripts/stream-e-failure-diagnostics.test.mjs"

def test_runtime_preserves_receiver_diagnostics():
    source = RUNTIME.read_text(encoding="utf-8")
    for marker in ("data?.detail", "failure.status", "failure.code", "failure.detail", "failure.correlation_id", "eventId", "receiptId", "transactionId"):
        assert marker in source

def test_current_source_authority_matches_static_hub_blob():
    manifest=json.loads((ROOT/'.naya/control-plane/HUB-PRESERVATION.json').read_text(encoding='utf-8'))
    expected=manifest['active_architecture']['entrypoint_blob_sha_at_checkpoint']
    actual=subprocess.check_output(['git','rev-parse','HEAD:NAYANET/HUB/index.html'],cwd=ROOT,text=True).strip()
    assert actual == expected

def test_sender_trace_contract_is_redacted():
    source = SENDER.read_text(encoding="utf-8")
    for marker in ("SMART_NOTE_RECEIVER_REQUEST", "SMART_NOTE_RECEIVER_RESPONSE", "summarizeReceiverResponse", "classifySenderFailure", "x-idempotency-key", "classification", "await new Promise"):
        assert marker in source

def test_node_diagnostics_suite_passes():
    result = subprocess.run(["node", "--test", str(NODE_TEST)], cwd=ROOT, text=True, capture_output=True)
    assert result.returncode == 0, result.stdout + result.stderr

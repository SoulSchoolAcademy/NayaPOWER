from pathlib import Path
import json
import subprocess

ROOT = Path(__file__).resolve().parents[1]
RUNTIME = ROOT / "NAYANET/HUB/public/assistant-runtime.js"
SURFACE = ROOT / "NAYANET/HUB/src/app/SmartNoteSurface.tsx"
RECEIVER = ROOT / "supabase/functions/v7-smart-note-canonical/index.ts"
SENDER = ROOT / ".github/scripts/universal-envelope-hub-runtime-sender.mjs"
NODE_TEST = ROOT / ".github/scripts/stream-e-failure-diagnostics.test.mjs"

def test_runtime_preserves_receiver_diagnostics():
    source = RUNTIME.read_text(encoding="utf-8")
    for marker in ("data?.detail", "failure.status", "failure.code", "failure.detail", "failure.correlation_id", "eventId", "receiptId", "transactionId"):
        assert marker in source


def test_runtime_and_surface_fail_closed_on_partial_receiver_results():
    runtime = RUNTIME.read_text(encoding="utf-8")
    surface = SURFACE.read_text(encoding="utf-8")
    for marker in ("data?.ok!==true", "data?.error", "data?.pipeline", "['completed','replayed']"):
        assert marker in runtime
    for marker in ("result?.ok!==true", "result?.pipeline", "intelligence_checkpoint", "learning_evidence"):
        assert marker in surface


def test_receiver_failure_preserves_canonical_lineage():
    source = RECEIVER.read_text(encoding="utf-8")
    for marker in ("canonicalEventId", "canonicalReceiptId", "canonicalTransactionId", 'pipeline:"failed"', "event_id:canonicalEventId", "receipt_id:canonicalReceiptId", "transaction_id:canonicalTransactionId"):
        assert marker in source

def test_current_source_authority_matches_static_hub_blob():
    manifest=json.loads((ROOT/'.naya/control-plane/HUB-PRESERVATION.json').read_text(encoding='utf-8'))
    expected=manifest['active_architecture']['entrypoint_blob_sha_at_checkpoint']
    actual=subprocess.check_output(['git','rev-parse','HEAD:NAYANET/HUB/index.html'],cwd=ROOT,text=True).strip()
    assert actual == expected

def test_sender_trace_contract_is_redacted():
    source = SENDER.read_text(encoding="utf-8")
    for marker in ("SMART_NOTE_RECEIVER_REQUEST", "SMART_NOTE_RECEIVER_RESPONSE", "summarizeReceiverResponse", "summarizeReceiverBridgeResponse", "PRODUCTION_RECEIVER_RESPONSE", "PRODUCTION_RECEIVER_AUTHORITY_GATE", "REF_NOT_AUTHORIZED", "resolveProofMode", "buildNoMutationProof", "NON_MAIN_NO_MUTATION", "GITHUB_REF", "GITHUB_EVENT_NAME", "GITHUB_HEAD_REF", "verifyCausalLineage", "verifyPersistenceRecord", "verifyProjectionIndex", "verifyRetrievedEvent", "verifyExactReplay", "INDEPENDENT_PERSISTENCE_RECONSTRUCTED", "CAUSAL_LINEAGE_RECONSTRUCTED", "status:'PARTIAL'", "classifySenderFailure", "x-idempotency-key", "classification", "await new Promise"):
        assert marker in source


def test_sender_stops_at_receiver_pipeline_failure():
    source = SENDER.read_text(encoding="utf-8")
    for marker in ("capture?.ok!==true", "capture?.error", "SMART_NOTE_RECEIVER_PIPELINE_FAILED"):
        assert marker in source
    capture = source.index("const capture=")
    validation = source.index("capture?.ok!==true")
    meaningful = source.index("mark('MEANINGFUL_OUTPUT_EMITTED'")
    assert capture < validation < meaningful

def test_non_main_preflight_precedes_browser_and_capture():
    source = SENDER.read_text(encoding="utf-8")
    preflight = source.index("if(proofMode==='NON_MAIN_NO_MUTATION')")
    browser = source.index("chromium.launch")
    capture = source.index("captureSmartNote")
    assert preflight < browser < capture
    assert "process.exit(0)" in source

def test_main_only_authority_and_legacy_isolation_contracts():
    bridge = (ROOT / "supabase/functions/nayanet-project-intelligence-bridge/index.ts").read_text(encoding="utf-8")
    sender = SENDER.read_text(encoding="utf-8")
    diagnostics = (ROOT / ".github/scripts/stream-e-failure-diagnostics.mjs").read_text(encoding="utf-8")
    hub = (ROOT / "NAYANET/HUB/index.html").read_text(encoding="utf-8")
    for marker in ("payload.ref", "refs/heads/main", "REPOSITORY_NOT_AUTHORIZED", "VISIBILITY_NOT_AUTHORIZED"):
        assert marker in bridge
    for marker in ("GITHUB_EVENT_NAME", "GITHUB_HEAD_REF", "NON_MAIN_NO_MUTATION"):
        assert marker in sender
    assert "MAIN_REF_PROOF" in diagnostics
    assert "createClient" not in hub
    assert "SUPABASE_URL" not in hub
    assert "supabase.co" not in hub

    result = subprocess.run(["node", "--test", str(NODE_TEST)], cwd=ROOT, text=True, capture_output=True)
    assert result.returncode == 0, result.stdout + result.stderr

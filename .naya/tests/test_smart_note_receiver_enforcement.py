#!/usr/bin/env python3
"""Failing-before/fixed-after proof for canonical Smart Note receiver enforcement."""
from pathlib import Path
import importlib.util
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[2]
RUNTIME = ROOT / ".naya" / "runtime"
sys.path.insert(0, str(RUNTIME))

def load_module(name: str, source: str):
    path = ROOT / f".naya/runtime/{name}.py"
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def test_before_main_bypasses_receiver():
    old_source = subprocess.check_output(
        ["git", "show", "origin/main:.naya/runtime/smart_note_calendar.py"],
        text=True,
    )
    with tempfile.TemporaryDirectory() as raw:
        old_path = Path(raw) / "old_calendar.py"
        old_path.write_text(old_source, encoding="utf-8")
        spec = importlib.util.spec_from_file_location("old_calendar", old_path)
        assert spec and spec.loader
        old = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(old)
        body = "\n".join(f"## {h}" for h in old.REQUIRED_HEADINGS)
        result = old.persist_smart_note(
            timestamp="2026-09-25T18:00:00+00:00",
            topic="Before Enforcement",
            body=body,
            intelligent_block_id="IB-000002",
            root=Path(raw) / "smart-notes",
        )
        assert Path(result["path"]).is_file()
        print("BEFORE_MAIN=FAIL (direct intelligent_block_id bypass persisted)")

def test_after_requires_receiver_receipt():
    current = load_module("smart_note_calendar", "")
    body = "\n".join(f"## {h}" for h in current.REQUIRED_HEADINGS)
    with tempfile.TemporaryDirectory() as raw:
        try:
            current.persist_smart_note(
                timestamp="2026-09-25T18:00:00+00:00",
                topic="After Enforcement",
                body=body,
                receiver_receipt={},
                root=Path(raw) / "smart-notes",
            )
        except ValueError as exc:
            assert str(exc) == "CANONICAL_RECEIVER_RECEIPT_INVALID"
        else:
            raise AssertionError("fixed writer accepted a missing receiver receipt")
        print("AFTER_BRANCH=PASS (missing receiver receipt rejected before persistence)")

def test_after_accepts_only_completed_receiver_receipt():
    current = load_module("smart_note_calendar", "")
    body = "\n".join(f"## {h}" for h in current.REQUIRED_HEADINGS)
    receipt = {
        "schema": "naya/smart-note-receiver-receipt/v1",
        "canonical_receiver": "v7-smart-note-canonical",
        "status": "completed",
        "intelligent_block_id": "IB-001025",
        "event_id": "EV-001025",
        "transaction_id": "TX-001025",
        "feed_verification": {"verified": True, "event_id": "EV-001025", "source_id": "FEED-001025"},
        "smart_link": {"kind": "smart_feed_intelligent_block", "path": "/hub?ib=IB-001025", "intelligent_block_id": "IB-001025"}
    }
    with tempfile.TemporaryDirectory() as raw:
        result = current.persist_smart_note(
            timestamp="2026-09-25T18:00:00+00:00",
            topic="After Enforcement",
            body=body,
            receiver_receipt=receipt,
            root=Path(raw) / "smart-notes",
        )
        assert result["intelligent_block_id"] == "IB-001025"
        assert result["source_event_id"] == "EV-001025"
        expected = Path(raw) / "smart-notes" / "2026" / "09" / "25" / "system" / "after-enforcement" / "IB-001025" / "smart-note.md"
        assert Path(result["path"]) == expected
        assert expected.is_file()
        rendered = expected.read_text(encoding="utf-8")
        assert "**Intelligent Block ID:** IB-001025" in rendered
        assert "**Source Event ID:** EV-001025" in rendered
        registry = __import__("json").loads((Path(raw) / "smart-notes" / "REGISTRY.json").read_text(encoding="utf-8"))
        assert registry["entries"][0]["path"] == "2026/09/25/system/after-enforcement/IB-001025/smart-note.md"
        print("AFTER_BRANCH=PASS (feed-verified receiver identity + lineage projected canonically)")



def test_live_receiver_returns_feed_verified_smart_link_and_completion_receipt():
    receiver = (ROOT / "supabase/functions/v7-smart-note-canonical/index.ts").read_text(encoding="utf-8")
    required = [
        'const feedVerification=await supabase.from("nayanet_cognition_events")',
        'SMART_NOTE_FEED_VERIFICATION_FAILED',
        'const smartLinkPath="/hub?ib="+encodeURIComponent(intelligentBlockId)',
        'const completionReceipt=',
        'schema:"naya/smart-note-receiver-receipt/v1"',
        'transaction_id:canonicalTransactionId',
        'feed_verification:feedVerificationReceipt',
        'smart_link:smartLink',
    ]
    missing = [token for token in required if token not in receiver]
    assert not missing, "live receiver contract missing: " + ", ".join(missing)


def test_repository_has_one_enforced_smart_note_write_boundary():
    """Audit executable production/runtime code, not fixtures or test assertions."""
    tracked = subprocess.check_output(["git", "ls-files"], text=True).splitlines()
    executable = [
        p for p in tracked
        if p.endswith((".py", ".ts", ".js", ".mjs", ".tsx", ".jsx"))
        and not p.startswith(("tests/", ".naya/tests/", ".naya/memory/test_"))
    ]
    violations = []
    for rel in executable:
        source = (ROOT / rel).read_text(encoding="utf-8", errors="ignore")
        if rel == ".naya/memory/smart_notes_v3.py":
            # This module writes only its derived event validation/index artifacts.
            pass
        elif "smart-notes" in source and "write_text" in source:
            violations.append(rel + ": Smart Note writer outside canonical projection boundary")
        if "SUPERBRAIN/SMART-NOTES" in source or "NAYANET/SMART-NOTES" in source or ".naya/memory/notes" in source:
            violations.append(rel + ": alternate Smart Note namespace")
        if "_allocate_ib_id" in source or "identity_cursor" in source:
            violations.append(rel + ": local IB allocator marker")
    assert not violations, "\n".join(violations)

if __name__ == "__main__":
    test_before_main_bypasses_receiver()
    test_after_requires_receiver_receipt()
    test_after_accepts_only_completed_receiver_receipt()
    test_live_receiver_returns_feed_verified_smart_link_and_completion_receipt()
    test_repository_has_one_enforced_smart_note_write_boundary()
    print("SMART_NOTE_RECEIVER_ENFORCEMENT=PASS")

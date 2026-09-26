"""Machine-checkable Smart Link identity contract.

This test does not replace the canonical prose law. It makes the most important
invariant executable: a Smart Link must be a canonical GitHub smart-note.md URL
for the exact IB being reported.

Hub runtime URLs and evidence/provenance URLs are intentionally rejected.
"""

from urllib.parse import urlparse
import json
from pathlib import Path

try:
    from jsonschema import Draft202012Validator
except ImportError:  # pragma: no cover - CI installs the declared test dependency
    Draft202012Validator = None


CANONICAL_HOST = "github.com"
CANONICAL_OWNER = "SoulSchoolAcademy"
CANONICAL_REPO = "NayaPOWER"


def is_canonical_smart_note_link(url: str, ib_id: str) -> bool:
    """Return True only for the canonical GitHub Smart Note projection."""
    parsed = urlparse(url)
    if parsed.scheme != "https" or parsed.netloc != CANONICAL_HOST:
        return False

    prefix = f"/{CANONICAL_OWNER}/{CANONICAL_REPO}/blob/main/.naya/memory/smart-notes/"
    if not parsed.path.startswith(prefix):
        return False

    if not parsed.path.endswith(f"/{ib_id}/smart-note.md"):
        return False

    return True


def load_canonical_schema():
    schema_path = Path(__file__).resolve().parents[1] / "contracts" / "SMART-LINK-CONTRACT.json"
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    if Draft202012Validator is None:
        raise AssertionError("jsonschema is required for the canonical Smart Link schema gate")
    return schema


def test_canonical_schema_rejects_non_smart_note_targets():
    schema = load_canonical_schema()
    validator = Draft202012Validator(schema)
    valid = {
        "smart_link_id": "slink_test",
        "schema_version": "1.0",
        "target_type": "smart_note",
        "target_ref": ".naya/memory/smart-notes/2026/09/24/system/example/IB-000001/smart-note.md",
        "ib_id": "IB-000001",
        "smart_link_url": "https://github.com/SoulSchoolAcademy/NayaPOWER/blob/main/.naya/memory/smart-notes/2026/09/24/system/example/IB-000001/smart-note.md",
    }
    assert not list(validator.iter_errors(valid))

    hub = dict(valid, target_type="ledger_event", target_ref="ledger_123", smart_link_url="https://sparkling-shape-7ae5.smartnetpodcast.workers.dev/hub?ib=IB-000001")
    assert list(validator.iter_errors(hub))

    evidence = dict(valid, smart_link_url="https://github.com/SoulSchoolAcademy/NayaPOWER/commit/abc123")
    assert list(validator.iter_errors(evidence))


def test_schema_identity_fields_match_at_application_boundary():
    ib_id = "IB-000001"
    url = "https://github.com/SoulSchoolAcademy/NayaPOWER/blob/main/.naya/memory/smart-notes/2026/09/24/system/example/IB-000001/smart-note.md"
    assert is_canonical_smart_note_link(url, ib_id)
    assert not is_canonical_smart_note_link(url.replace("IB-000001", "IB-000002"), ib_id)


def test_hub_deep_link_is_not_a_smart_link():
    assert not is_canonical_smart_note_link(
        "https://sparkling-shape-7ae5.smartnetpodcast.workers.dev/hub?ib=IB-001049",
        "IB-001049",
    )


def test_wrong_ib_is_not_a_smart_link():
    assert not is_canonical_smart_note_link(
        "https://github.com/SoulSchoolAcademy/NayaPOWER/blob/main/"
        ".naya/memory/smart-notes/2026/09/25/system/example/IB-001048/smart-note.md",
        "IB-001049",
    )


def test_generic_github_page_is_not_a_smart_link():
    assert not is_canonical_smart_note_link(
        "https://github.com/SoulSchoolAcademy/NayaPOWER/tree/main/.naya/memory/smart-notes",
        "IB-001049",
    )


def test_canonical_smart_note_link_is_accepted():
    assert is_canonical_smart_note_link(
        "https://github.com/SoulSchoolAcademy/NayaPOWER/blob/main/"
        ".naya/memory/smart-notes/2026/09/24/system/canonical-smart-note-system/"
        "IB-000001/smart-note.md",
        "IB-000001",
    )


if __name__ == "__main__":
    tests = [
        test_hub_deep_link_is_not_a_smart_link,
        test_wrong_ib_is_not_a_smart_link,
        test_generic_github_page_is_not_a_smart_link,
        test_canonical_smart_note_link_is_accepted,
    ]
    for test in tests:
        test()
    print(f"{len(tests)} passed")

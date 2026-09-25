"""Machine-checkable Smart Link identity contract.

This test does not replace the canonical prose law. It makes the most important
invariant executable: a Smart Link must be a canonical GitHub smart-note.md URL
for the exact IB being reported.

Hub runtime URLs and evidence/provenance URLs are intentionally rejected.
"""

from urllib.parse import urlparse


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
    import pytest
    raise SystemExit(pytest.main([__file__, "-q"]))

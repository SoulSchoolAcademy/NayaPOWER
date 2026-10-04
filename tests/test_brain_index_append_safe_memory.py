from tools import regenerate_brain_index as brain_index


def _f(path: str) -> dict:
    return {"path": path}


def test_governed_memory_subtrees_are_append_safe():
    files = [
        _f("BRAIN/05-MEMORY/0001-MEMORY-CONTINUITY-CONTRACT-V1.md"),
        _f("BRAIN/05-MEMORY/README.md"),
        _f("BRAIN/05-MEMORY/INTELLIGENCE-REPORTS/example.md"),
        _f("BRAIN/05-MEMORY/SMART-NOTES/example.md"),
    ]
    expected = brain_index.expected_domain_counts(files)
    actual = brain_index.domain_counts(files)
    assert expected["05-MEMORY"] == 4
    assert actual["05-MEMORY"] == expected["05-MEMORY"]


def test_unclassified_memory_growth_still_trips_count_guard():
    files = [
        _f("BRAIN/05-MEMORY/0001-MEMORY-CONTINUITY-CONTRACT-V1.md"),
        _f("BRAIN/05-MEMORY/README.md"),
        _f("BRAIN/05-MEMORY/INTELLIGENCE-REPORTS/example.md"),
        _f("BRAIN/05-MEMORY/SMART-NOTES/example.md"),
        _f("BRAIN/05-MEMORY/UNCLASSIFIED-SURPRISE.md"),
    ]
    expected = brain_index.expected_domain_counts(files)
    actual = brain_index.domain_counts(files)
    assert actual["05-MEMORY"] == 5
    assert expected["05-MEMORY"] == 4
    assert actual != expected

from tools import regenerate_brain_index as brain_index


def _f(path: str) -> dict:
    return {"path": path}


def _violations_for(files: list[dict], domain: str) -> list[str]:
    """Floor violations restricted to one domain under test."""
    floors = brain_index.floor_domain_counts(files)
    actual = brain_index.domain_counts(files)
    return [v for v in brain_index.floor_violations(actual, floors) if v.startswith(domain + ":")]


def test_governed_memory_subtrees_are_append_safe():
    files = [
        _f("BRAIN/05-MEMORY/0001-MEMORY-CONTINUITY-CONTRACT-V1.md"),
        _f("BRAIN/05-MEMORY/README.md"),
        _f("BRAIN/05-MEMORY/INTELLIGENCE-REPORTS/example.md"),
        _f("BRAIN/05-MEMORY/SMART-NOTES/example.md"),
    ]
    floors = brain_index.floor_domain_counts(files)
    assert floors["05-MEMORY"] == 4
    assert _violations_for(files, "05-MEMORY") == []


def test_growth_above_floor_does_not_trip_ratchet():
    # The ratchet's whole point: legitimate additions never break the check.
    files = [
        _f("BRAIN/05-MEMORY/0001-MEMORY-CONTINUITY-CONTRACT-V1.md"),
        _f("BRAIN/05-MEMORY/README.md"),
        _f("BRAIN/05-MEMORY/INTELLIGENCE-REPORTS/example.md"),
        _f("BRAIN/05-MEMORY/SMART-NOTES/example.md"),
        _f("BRAIN/05-MEMORY/UNCLASSIFIED-SURPRISE.md"),
    ]
    floors = brain_index.floor_domain_counts(files)
    actual = brain_index.domain_counts(files)
    assert actual["05-MEMORY"] == 5 > floors["05-MEMORY"]
    assert _violations_for(files, "05-MEMORY") == []


def test_removal_below_floor_trips_ratchet():
    # The guard's real job, preserved: silent deletions are caught and named.
    files = [
        _f("BRAIN/05-MEMORY/0001-MEMORY-CONTINUITY-CONTRACT-V1.md"),
        # README.md deleted — the floor still expects it.
        _f("BRAIN/05-MEMORY/INTELLIGENCE-REPORTS/example.md"),
        _f("BRAIN/05-MEMORY/SMART-NOTES/example.md"),
    ]
    violations = _violations_for(files, "05-MEMORY")
    assert len(violations) == 1
    assert "05-MEMORY" in violations[0]
    assert "1 file(s) removed" in violations[0]


def test_new_domain_has_zero_floor():
    # A brand-new domain was never pinned — it can never violate the ratchet.
    files = [_f("BRAIN/77-NEWTHING/anything.md")]
    floors = brain_index.floor_domain_counts(files)
    actual = brain_index.domain_counts(files)
    assert not any(v.startswith("77-NEWTHING:") for v in brain_index.floor_violations(actual, floors))

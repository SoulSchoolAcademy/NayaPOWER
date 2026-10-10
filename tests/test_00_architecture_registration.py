"""00-ARCHITECTURE registration (2026-10-10): same tripwire-gap class as 00-ACTIVATION.

The five bootstrap files (ACTIVATION-NAYA-PLAN.md, ACTIVATION-NAYA-PROJECT.md,
MACHINE-INTELLIGENCE.json, NORTH-STAR-RATIFICATION-2026-09-26.md,
SYSTEM-BLUEPRINT-20261009.md) landed with the #2108 merge (fe25661c) under a
domain counted by domain_counts() but absent from DOMAIN_ORDER — so a mass
deletion of the bootstrap set would never trip the deletion ratchet.
Registration closes it.
"""
from tools import regenerate_brain_index as brain_index


def _f(path: str) -> dict:
    return {"path": path, "sha": "a" * 40, "size": 100}


def _md(files):
    files = sorted(files, key=lambda f: brain_index.domain_of(f["path"]))
    counts = brain_index.domain_counts(files)
    return brain_index.build_real_tree_md("f" * 40, files, counts, "2026-10-09")


def test_00_architecture_has_floor_and_title():
    assert brain_index.BASELINE_DOMAIN_FLOORS["00-ARCHITECTURE"] == 5
    assert "00-ARCHITECTURE" in brain_index.DOMAIN_ORDER  # ratchet covers it
    assert brain_index.DOMAIN_TITLES["00-ARCHITECTURE"] == "00-ARCHITECTURE — Architecture"


def test_00_architecture_renders_with_registered_title():
    files = [
        _f("BRAIN/00-ARCHITECTURE/SYSTEM-BLUEPRINT-20261009.md"),
        _f("BRAIN/00-ARCHITECTURE/MACHINE-INTELLIGENCE.json"),
    ]
    md = _md(files)
    assert "### 00-ARCHITECTURE — Architecture" in md
    assert "(unregistered domain)" not in md


def test_00_architecture_floor_trips_on_deletion():
    def counts_with(architecture_count):
        counts = {d: brain_index.BASELINE_DOMAIN_FLOORS[d] for d in brain_index.DOMAIN_ORDER}
        counts["00-ARCHITECTURE"] = architecture_count
        return counts

    violations = brain_index.floor_violations(counts_with(4), brain_index.BASELINE_DOMAIN_FLOORS)
    assert len(violations) == 1
    assert violations[0].startswith("00-ARCHITECTURE: 4 files in tree, floor is 5")
    assert brain_index.floor_violations(counts_with(5), brain_index.BASELINE_DOMAIN_FLOORS) == []
    assert brain_index.floor_violations(counts_with(9), brain_index.BASELINE_DOMAIN_FLOORS) == []

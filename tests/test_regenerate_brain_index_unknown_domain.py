"""Negative tests: regenerate_brain_index must never crash on an unregistered
BRAIN domain — --check reports DRIFT for the new files, it does not die.

Regression source: PR #1971 added BRAIN/00-ACTIVATION/; the live tip then
crashed `regenerate_brain_index.py --check` with `KeyError: '00-ACTIVATION'`
in build_real_tree_md, because domain_of() returns the raw second path
segment for any BRAIN/<X>/ file while the renderer indexed DOMAIN_TITLES[d]
directly. The verification battery lost its brain-index instrument on the
live tip — the fix is a fail-safe title fallback so the check survives
unknown domains and still reports drift.

2026-10-10: 00-ACTIVATION is now a REGISTERED domain (floor 3, proper
title) — the fail-safe tests below use a synthetic 77-NEWTHING domain so
they keep exercising the unregistered path, and new tests pin the
registration and its deletion tripwire.
"""
from tools import regenerate_brain_index as brain_index


def _f(path: str) -> dict:
    return {"path": path, "sha": "a" * 40, "size": 100}


def _md(files):
    # build_real_tree_md groups by domain as files stream; feed domain-sorted.
    files = sorted(files, key=lambda f: brain_index.domain_of(f["path"]))
    counts = brain_index.domain_counts(files)
    return brain_index.build_real_tree_md("f" * 40, files, counts, "2026-10-09")


def test_domain_of_returns_raw_segment_for_unknown_domain():
    assert brain_index.domain_of("BRAIN/77-NEWTHING/x.md") == "77-NEWTHING"


def test_unknown_domain_does_not_crash_real_tree_md():
    # The exact failure: KeyError on the unknown domain's section header.
    files = [
        _f("BRAIN/01-GOVERNANCE/some-law.md"),
        _f("BRAIN/77-NEWTHING/mystery.md"),
        _f("BRAIN/77-NEWTHING/other.json"),
    ]
    md = _md(files)  # must not raise
    assert "### 77-NEWTHING — (unregistered domain)" in md
    assert "BRAIN/77-NEWTHING/mystery.md" in md


def test_known_domain_titles_unchanged():
    # The fallback must not alter any registered domain's rendering.
    files = [
        _f("BRAIN/01-GOVERNANCE/some-law.md"),
        _f("BRAIN/05-MEMORY/some-note.md"),
    ]
    md = _md(files)
    assert "### 01-GOVERNANCE — Governance" in md
    assert "### 05-MEMORY — Memory" in md
    assert "(unregistered domain)" not in md


def test_unknown_domain_files_listed_with_blob_sha():
    files = [_f("BRAIN/77-NEWTHING/anything.md")]
    md = _md(files)
    assert "- `BRAIN/77-NEWTHING/anything.md` — `aaaaaaaaaaaa` (100 bytes)" in md


# --- 00-ACTIVATION registration (2026-10-10): the domain is no longer unknown.


def test_00_activation_has_floor_and_title():
    assert brain_index.BASELINE_DOMAIN_FLOORS["00-ACTIVATION"] == 3
    assert "00-ACTIVATION" in brain_index.DOMAIN_ORDER  # ratchet covers it
    assert brain_index.DOMAIN_TITLES["00-ACTIVATION"] == "00-ACTIVATION — Activation"


def test_00_activation_renders_with_registered_title():
    files = [
        _f("BRAIN/00-ACTIVATION/DESIGN-ACTIVATION.md"),
        _f("BRAIN/00-ACTIVATION/activation-checklist.json"),
    ]
    md = _md(files)
    assert "### 00-ACTIVATION — Activation" in md
    assert "(unregistered domain)" not in md


def test_00_activation_floor_trips_on_deletion():
    # The tripwire this registration closes: fewer files than the floor must
    # name the domain explicitly; at/above the floor is silent.
    def counts_with(activation_count):
        counts = {d: brain_index.BASELINE_DOMAIN_FLOORS[d] for d in brain_index.DOMAIN_ORDER}
        counts["00-ACTIVATION"] = activation_count
        return counts

    violations = brain_index.floor_violations(counts_with(2), brain_index.BASELINE_DOMAIN_FLOORS)
    assert len(violations) == 1
    assert violations[0].startswith("00-ACTIVATION: 2 files in tree, floor is 3")
    assert brain_index.floor_violations(counts_with(3), brain_index.BASELINE_DOMAIN_FLOORS) == []
    assert brain_index.floor_violations(counts_with(5), brain_index.BASELINE_DOMAIN_FLOORS) == []

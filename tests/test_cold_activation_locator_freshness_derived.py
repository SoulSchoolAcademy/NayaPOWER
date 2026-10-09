"""Freshness guard, derived model: the rejected set comes from the filesystem.

The durable flaw this replaces: the guards hardcoded which dated pins were
superseded (SUPERSEDED = "...-2026-09-28.md", and the sweeper's fix would have
added a 09-29 constant). Every new reconciliation dated after the constants
goes stale-safe-invisible: the guard passes green while a superseded pin sits
in a boot surface.

The new model: superseded = all dated siblings of a pinned family - newest,
computed by _freshness_guard at test time. When the next reconciliation lands
(10-11, 12-31, whenever), the rejected set changes with NO code change, and
any live pointer still naming an older sibling fails the guard.

These tests prove the derivation against synthetic fixture families, including
future dates the guard code could never have hardcoded.
"""

from pathlib import Path

import pytest

from _freshness_guard import (
    FAMILY_GLOB,
    assert_surface_fresh,
    dated_siblings,
    newest_sibling,
    rejected_siblings,
)

FAMILY_STEM = "SOURCE-PRECEDENCE-AND-NAVIGATION-RECONCILIATION-"


def _make_family(tmp_path: Path, *dates: str) -> Path:
    family_dir = tmp_path / "CURRENT-REALITY"
    family_dir.mkdir()
    for date in dates:
        (family_dir / f"{FAMILY_STEM}{date}.md").write_text(
            f"# reconciliation {date}\n", encoding="utf-8"
        )
    return family_dir


def _surface(tmp_path: Path, body: str) -> Path:
    surface = tmp_path / "pointer.md"
    surface.write_text(body, encoding="utf-8")
    return surface


def test_rejected_set_is_all_siblings_minus_newest(tmp_path):
    """With 09-28/09-29/10-04 on disk, the rejected set is {09-28, 09-29} —
    no constant was consulted."""
    family_dir = _make_family(tmp_path, "2026-09-28", "2026-09-29", "2026-10-04")
    assert [p.name for p in dated_siblings(family_dir, FAMILY_GLOB)] == [
        f"{FAMILY_STEM}2026-09-28.md",
        f"{FAMILY_STEM}2026-09-29.md",
        f"{FAMILY_STEM}2026-10-04.md",
    ]
    assert newest_sibling(family_dir, FAMILY_GLOB).name == f"{FAMILY_STEM}2026-10-04.md"
    assert rejected_siblings(family_dir, FAMILY_GLOB) == [
        f"{FAMILY_STEM}2026-09-28.md",
        f"{FAMILY_STEM}2026-09-29.md",
    ]


@pytest.mark.parametrize("stale_date", ["2026-09-28", "2026-09-29"])
def test_pointers_to_older_pins_fail_the_derived_guard(tmp_path, stale_date):
    """The current 09-28/09-29 pins fail the new guard when a surface names
    them — the old guard only caught 09-28 (and only via its constant)."""
    family_dir = _make_family(tmp_path, "2026-09-28", "2026-09-29", "2026-10-04")
    surface = _surface(tmp_path, f"see `{FAMILY_STEM}{stale_date}.md`")
    with pytest.raises(AssertionError, match="superseded"):
        assert_surface_fresh(surface, family_dir, FAMILY_GLOB)


def test_pointer_to_newest_pin_passes(tmp_path):
    """The 10-04 pin (newest on disk) passes the new guard."""
    family_dir = _make_family(tmp_path, "2026-09-28", "2026-09-29", "2026-10-04")
    surface = _surface(tmp_path, f"see `{FAMILY_STEM}2026-10-04.md`")
    assert_surface_fresh(surface, family_dir, FAMILY_GLOB)  # must not raise


def test_dynamic_glob_pointer_passes(tmp_path):
    """The sanctioned dynamic pointer (`SOURCE-PRECEDENCE-...-*.md`) follows
    the newest automatically; it is never a stale pin."""
    family_dir = _make_family(tmp_path, "2026-09-28", "2026-09-29", "2026-10-04")
    surface = _surface(tmp_path, f"read `{FAMILY_GLOB}` and select the newest")
    assert_surface_fresh(surface, family_dir, FAMILY_GLOB)  # must not raise


@pytest.mark.parametrize("future_date", ["2026-10-11", "2026-12-31", "2027-01-01"])
def test_future_sibling_rejected_with_no_code_change(tmp_path, future_date):
    """A reconciliation dated AFTER the guard was written: the pointer that
    was current (10-04) is now superseded and fails — the guard followed the
    filesystem, not a constant. These dates cannot appear in any pin constant
    the code was written with."""
    family_dir = _make_family(
        tmp_path, "2026-09-28", "2026-09-29", "2026-10-04", future_date
    )
    surface = _surface(tmp_path, f"see `{FAMILY_STEM}2026-10-04.md`")
    with pytest.raises(AssertionError, match="superseded"):
        assert_surface_fresh(surface, family_dir, FAMILY_GLOB)
    assert newest_sibling(family_dir, FAMILY_GLOB).name == (
        f"{FAMILY_STEM}{future_date}.md"
    )
    healed = _surface(tmp_path, f"see `{FAMILY_STEM}{future_date}.md`")
    assert_surface_fresh(healed, family_dir, FAMILY_GLOB)  # must not raise


def test_single_sibling_family_has_no_rejected_set(tmp_path):
    """A family with one dated member cannot have a superseded pin; the
    guard must not invent rejections."""
    family_dir = _make_family(tmp_path, "2026-10-04")
    assert rejected_siblings(family_dir, FAMILY_GLOB) == []
    surface = _surface(tmp_path, f"see `{FAMILY_STEM}2026-10-04.md`")
    assert_surface_fresh(surface, family_dir, FAMILY_GLOB)  # must not raise

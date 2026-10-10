"""Derived freshness-guard core for cold-activation locator pins.

The rejected set is DERIVED FROM THE FILESYSTEM — never from pin constants:

    superseded(family) = all dated siblings of the family - newest

When a new dated reconciliation lands (10-11, 12-31, ...), the rejected set
changes automatically. Any live pointer still naming an older sibling fails
the guard with NO code change to the tests.

The sanctioned dynamic pointer ``SOURCE-PRECEDENCE-AND-NAVIGATION-RECONCILIATION-*.md``
(select-the-newest) is never treated as a stale pin: it follows the newest
sibling by construction.

No date appears in this module except inside documentation text; there are no
pin constants. If you are tempted to add one, add a dated sibling to the
family directory instead — the guard will do the rest.
"""

import re
from pathlib import Path

# Pinned-family pattern. This names the FAMILY (the stem), never a dated pin:
# the dates come from the filesystem at test time.
FAMILY_GLOB = "SOURCE-PRECEDENCE-AND-NAVIGATION-RECONCILIATION-*.md"

_DATE_RE = re.compile(r"(\d{4}-\d{2}-\d{2})")


def _sort_key(path: Path) -> str:
    """Order siblings by embedded date; members without a date fall back to
    name order so the guard never crashes on an undated sibling."""
    match = _DATE_RE.search(path.name)
    return match.group(1) if match else path.name


def dated_siblings(directory: Path, pattern: str) -> list:
    """All dated members of a pinned family, oldest-first by embedded date."""
    return sorted(directory.glob(pattern), key=_sort_key)


def newest_sibling(directory: Path, pattern: str) -> Path:
    """The current pin: the newest dated sibling on disk."""
    siblings = dated_siblings(directory, pattern)
    assert siblings, f"pinned family is empty: {pattern} in {directory}"
    return siblings[-1]


def rejected_siblings(directory: Path, pattern: str) -> list:
    """The derived rejected set: every dated sibling that is not the newest.
    This is what used to be hardcoded as SUPERSEDED constants."""
    siblings = dated_siblings(directory, pattern)
    return [path.name for path in siblings[:-1]]


def assert_surface_fresh(surface: Path, family_dir: Path, pattern: str) -> None:
    """Fail if a live pointer names any superseded sibling of the pinned
    family. A surface that names only the newest sibling — or uses the
    family's dynamic ``*.md`` pointer — passes."""
    content = surface.read_text(encoding="utf-8")
    newest = newest_sibling(family_dir, pattern).name
    hits = [name for name in rejected_siblings(family_dir, pattern) if name in content]
    assert not hits, (
        f"{surface} pins superseded {pattern} sibling(s): {hits}; "
        f"current is {newest}"
    )

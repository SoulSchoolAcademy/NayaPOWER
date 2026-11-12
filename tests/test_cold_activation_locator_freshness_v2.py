"""Cold-activation locator freshness, part 2.

Extends the guard from tests/test_cold_activation_locator_freshness.py (PR #1040)
to the two active boot surfaces that PR did not repair:

- NAYA-ACTIVATION/CURRENT-REALITY/README.md ("Start with" navigation), and
- NAYA-ACTIVATION/ACTIVATION-RECEIPT-TEMPLATE.json (source_of_truth list).

Both pointed at a superseded precedence reconciliation while the suite was
green — the coverage gap this file closes.

Derived model: the superseded set is all dated siblings of the family minus
the newest, computed from the filesystem by _freshness_guard — no pin
constants, so the guard cannot go stale when the next reconciliation lands.

Failure-first: written against the combined #1038+#1040 state where both files
still referenced a superseded document; both tests failed before the fix.
"""

import json
from pathlib import Path

from _freshness_guard import (
    FAMILY_GLOB,
    assert_surface_fresh,
    newest_sibling,
)


ROOT = Path(__file__).resolve().parents[1]
ACTIVATION = ROOT / "NAYA-ACTIVATION"
CURRENT_REALITY = ACTIVATION / "CURRENT-REALITY"


def _current_precedence_name() -> str:
    return newest_sibling(CURRENT_REALITY, FAMILY_GLOB).name


def test_readme_start_with_points_to_current_precedence():
    """The CURRENT-REALITY README is the first navigation a cold Naya reads in
    that directory; its 'Start with' target must never be a superseded pin."""
    readme_path = CURRENT_REALITY / "README.md"
    assert_surface_fresh(readme_path, CURRENT_REALITY, FAMILY_GLOB)
    readme = readme_path.read_text(encoding="utf-8")
    assert _current_precedence_name() in readme or FAMILY_GLOB in readme


def test_receipt_template_source_of_truth_has_no_superseded_precedence():
    """Every activation receipt instantiated from the template inherits its
    source_of_truth list; a superseded precedence doc must not be listed."""
    template_path = ACTIVATION / "ACTIVATION-RECEIPT-TEMPLATE.json"
    template = json.loads(template_path.read_text(encoding="utf-8"))
    sources = template["source_of_truth"]
    assert isinstance(sources, list) and sources
    joined = " ".join(str(entry) for entry in sources)
    # Negative (derived): no superseded sibling may be named anywhere in the
    # source_of_truth list — checked on the raw template text.
    assert_surface_fresh(template_path, CURRENT_REALITY, FAMILY_GLOB)
    # Positive: the newest dated reconciliation (or the dynamic family
    # pointer) is referenced.
    assert _current_precedence_name() in joined or FAMILY_GLOB in joined

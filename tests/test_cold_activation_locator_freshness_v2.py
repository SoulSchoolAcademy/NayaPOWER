"""Cold-activation locator freshness, part 2.

Extends the guard from tests/test_cold_activation_locator_freshness.py (PR #1040)
to the two active boot surfaces that PR did not repair:

- NAYA-ACTIVATION/CURRENT-REALITY/README.md ("Start with" navigation), and
- NAYA-ACTIVATION/ACTIVATION-RECEIPT-TEMPLATE.json (source_of_truth list).

Both pointed at the superseded 2026-09-28 precedence reconciliation while the
suite was green — the coverage gap this file closes.

Failure-first: written against the combined #1038+#1040 state where both files
still referenced the superseded document; both tests failed before the fix.
"""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ACTIVATION = ROOT / "NAYA-ACTIVATION"
CURRENT_REALITY = ACTIVATION / "CURRENT-REALITY"
SUPERSEDED = "SOURCE-PRECEDENCE-AND-NAVIGATION-RECONCILIATION-2026-09-28.md"
SUPERSEDED_0929 = "SOURCE-PRECEDENCE-AND-NAVIGATION-RECONCILIATION-2026-09-29.md"
CURRENT_GLOB = "SOURCE-PRECEDENCE-AND-NAVIGATION-RECONCILIATION-*.md"


def _current_precedence_name() -> str:
    candidates = sorted(
        CURRENT_REALITY.glob("SOURCE-PRECEDENCE-AND-NAVIGATION-RECONCILIATION-*.md")
    )
    assert candidates, "current source-precedence reconciliation is missing"
    return candidates[-1].name


def test_readme_start_with_points_to_current_precedence():
    """The CURRENT-REALITY README is the first navigation a cold Naya reads in
    that directory; its 'Start with' target must never be a superseded pin."""
    readme = (CURRENT_REALITY / "README.md").read_text(encoding="utf-8")
    assert SUPERSEDED not in readme
    assert SUPERSEDED_0929 not in readme
    assert _current_precedence_name() in readme or CURRENT_GLOB in readme


def test_receipt_template_source_of_truth_has_no_superseded_precedence():
    """Every activation receipt instantiated from the template inherits its
    source_of_truth list; a superseded precedence doc must not be listed."""
    template = json.loads(
        (ACTIVATION / "ACTIVATION-RECEIPT-TEMPLATE.json").read_text(encoding="utf-8")
    )
    sources = template["source_of_truth"]
    assert isinstance(sources, list) and sources
    assert all(SUPERSEDED not in str(entry) for entry in sources)
    assert all(SUPERSEDED_0929 not in str(entry) for entry in sources)
    joined = " ".join(str(entry) for entry in sources)
    assert _current_precedence_name() in joined or CURRENT_GLOB in joined

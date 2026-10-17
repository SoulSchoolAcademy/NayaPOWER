"""Receipt-pin trigger-scope regression guard (w92, Naya Delta).

Guards the Kappa w91 divergence fix: the receipt-pin check
(.github/workflows/receipt-gate.yml) and its sibling receipt check
(.github/workflows/worker-protocol-gates.yml) must listen to the SAME
pull_request event set. If they diverge again, a PR body-edit re-evaluates
one check but not the other -- stale green (false-green) or stuck red.

Deterministic, no network. Run: python3 -m pytest tests/test_receipt_gate_trigger_scope.py -q

Note: YAML 1.1 parses a bare `on` key as boolean True, so we read it
from d[True] with a fallback to d['on'].
"""

import yaml
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PIN_WORKFLOW = ROOT / ".github" / "workflows" / "receipt-gate.yml"
SIBLING_WORKFLOW = ROOT / ".github" / "workflows" / "worker-protocol-gates.yml"


def _on_block(path):
    d = yaml.safe_load(path.read_text())
    on = d.get(True, d.get("on"))  # YAML 1.1: bare `on` == True
    return on["pull_request"]


def test_workflow_files_exist():
    assert PIN_WORKFLOW.exists(), "receipt-gate.yml missing"
    assert SIBLING_WORKFLOW.exists(), "worker-protocol-gates.yml missing"


def test_trigger_type_sets_match():
    pin_types = set(_on_block(PIN_WORKFLOW)["types"])
    sibling_types = set(_on_block(SIBLING_WORKFLOW)["types"])
    assert pin_types == sibling_types, (
        "trigger-scope divergence: receipt-gate.yml=%s sibling=%s"
        % (sorted(pin_types), sorted(sibling_types))
    )


def test_trigger_types_include_edit_sensitive_events():
    # A PR body edit must re-evaluate the pin check; otherwise a pin
    # removed via body-edit keeps a stale green (false-green, w91).
    pin_types = set(_on_block(PIN_WORKFLOW)["types"])
    assert {"reopened", "edited"} <= pin_types, (
        "receipt-gate.yml must fire on reopened+edited, has %s" % sorted(pin_types)
    )


def test_branches_match():
    assert _on_block(PIN_WORKFLOW)["branches"] == _on_block(SIBLING_WORKFLOW)["branches"]

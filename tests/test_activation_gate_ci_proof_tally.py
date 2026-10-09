"""Truth-hygiene: the CI proof tally must never count a skipped check as held.

UNKNOWN != VERIFIED. A check that never ran (ok=None) is labeled SKIP and
is excluded from both the held count and the denominator, so the headline
"N/N rows hold" can only ever describe checks that actually ran.
"""
import importlib.util
import os
import sys

import pytest

_TOOL = os.path.join(os.path.dirname(__file__), "..", "tools",
                     "activation_gate_ci_proof.py")


def _load():
    spec = importlib.util.spec_from_file_location(
        "activation_gate_ci_proof", _TOOL)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture(scope="module")
def mod():
    return _load()


def _report_line(mod, results):
    held, ran, skipped, failed = mod.tally_rows(results)
    suffix = " (%d skipped)" % skipped if skipped else ""
    return "==== %d/%d rows hold%s ====" % (held, ran, suffix), failed


class TestRowStatus:
    def test_hold_breach_skip_labels(self, mod):
        assert mod.row_status(True) == "HOLD"
        assert mod.row_status(False) == "BREACH"
        assert mod.row_status(None) == "SKIP"


class TestTallyHonesty:
    def test_all_hold_no_skips_matches_legacy_format(self, mod):
        rows = [("r%d" % i, True, "ok") for i in range(8)]
        line, failed = _report_line(mod, rows)
        assert line == "==== 8/8 rows hold ===="
        assert failed == 0

    def test_skip_excluded_from_numerator_and_denominator(self, mod):
        rows = [("r%d" % i, True, "ok") for i in range(7)]
        rows.append(("exact-invocation (skipped — infra)", None, "not run"))
        line, failed = _report_line(mod, rows)
        assert line == "==== 7/7 rows hold (1 skipped) ===="
        assert failed == 0
        # The old code would have printed 8/8 — that inflation is the bug.
        assert line != "==== 8/8 rows hold ===="

    def test_skip_does_not_mask_breach(self, mod):
        rows = [("r%d" % i, True, "ok") for i in range(7)]
        rows.append(("broken check", False, "breach"))
        rows.append(("skipped check", None, "not run"))
        line, failed = _report_line(mod, rows)
        assert line == "==== 7/8 rows hold (1 skipped) ===="
        assert failed == 1

    def test_skip_never_fails_the_proof(self, mod):
        rows = [("only check", None, "infra down")]
        line, failed = _report_line(mod, rows)
        assert line == "==== 0/0 rows hold (1 skipped) ===="
        assert failed == 0

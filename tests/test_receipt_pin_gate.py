"""Merge receipt gate proof (Lane 9, t922 rebuild).

Covers both rungs of the receipt-pin mechanism:
  - tools/check_scorecard_receipt_pin.py  (PR-body rung: MISSING / TAMPERED /
                                           STALE / FUTURE / PASS)
  - tools/auto_merge_gate.py P12        (gate rung: fail-closed on missing /
                                         malformed / stale / future-dated pin)

14 tests from t922, all deterministic, no network. t952 adds: --pr-state-out on
the pin CLI (2 tests) and --p12-only on the gate CLI (3 tests) = 19 total.
The FUTURE rung (Judge wave-216, L300/L316 — future-dated decided_at fails
closed) adds 9 tests (8 behavior + 1 strict-operator pin) = 28 total; the
FUTURE behavior tests are time-relative and bounded, the operator pin uses a
fixed now.
Run: python3 -m pytest tests/test_receipt_pin_gate.py -q
"""

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

GOOD_HEAD = "1b6f72defa9b7eea98acc822fe80ab307db1aff2"
OTHER_HEAD = "a26943cd00000000000000000000000000000000"


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


pin_mod = _load("check_scorecard_receipt_pin", ROOT / "tools" / "check_scorecard_receipt_pin.py")
gate_mod = _load("auto_merge_gate", ROOT / "tools" / "auto_merge_gate.py")

VALID_BODY = """Some PR description text.

## SCORECARD-RECEIPT-PIN
merge_head_sha: 1b6f72defa9b7eea98acc822fe80ab307db1aff2
decided_by: Naya Smith
decided_at: 2026-10-11T15:50:00-07:00
board_comment_id: 217501

More text after the block.
"""


def _body_with(overrides, drop=None):
    """Build a pin block body with field overrides; drop removes fields."""
    fields = {
        "merge_head_sha": GOOD_HEAD,
        "decided_by": "Naya Smith",
        "decided_at": "2026-10-11T15:50:00-07:00",
        "board_comment_id": "217501",
    }
    fields.update(overrides)
    for key in (drop or ()):
        fields.pop(key, None)
    lines = ["## SCORECARD-RECEIPT-PIN"] + [
        "%s: %s" % (k, v) for k, v in fields.items()
    ]
    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------- PR-body rung


def test_pin_missing_block_fails():
    verdict, reason = pin_mod.check_pin("plain body, no block at all", GOOD_HEAD)
    assert verdict == "MISSING", reason


def test_pin_malformed_sha_too_short_fails_tampered():
    verdict, reason = pin_mod.check_pin(_body_with({"merge_head_sha": "a26943cd"}), GOOD_HEAD)
    assert verdict == "TAMPERED", reason


def test_pin_malformed_sha_non_hex_fails_tampered():
    verdict, reason = pin_mod.check_pin(
        _body_with({"merge_head_sha": "z" * 40}), GOOD_HEAD
    )
    assert verdict == "TAMPERED", reason


def test_pin_stale_sha_fails_stale():
    verdict, reason = pin_mod.check_pin(_body_with({"merge_head_sha": OTHER_HEAD}), GOOD_HEAD)
    assert verdict == "STALE", reason
    assert "re-score" in reason


def test_pin_empty_decided_by_fails_tampered():
    verdict, reason = pin_mod.check_pin(_body_with({"decided_by": ""}), GOOD_HEAD)
    assert verdict == "TAMPERED", reason


def test_pin_unparseable_timestamp_fails_tampered():
    verdict, reason = pin_mod.check_pin(
        _body_with({"decided_at": "sometime yesterday"}), GOOD_HEAD
    )
    assert verdict == "TAMPERED", reason


def test_pin_non_numeric_board_comment_fails_tampered():
    verdict, reason = pin_mod.check_pin(
        _body_with({"board_comment_id": "not-posted"}), GOOD_HEAD
    )
    assert verdict == "TAMPERED", reason


def test_pin_valid_block_passes():
    verdict, reason = pin_mod.check_pin(VALID_BODY, GOOD_HEAD)
    assert verdict == "PASS", reason
    assert GOOD_HEAD in reason


def test_pin_first_block_wins_when_two_present():
    # Documented behavior: the first SCORECARD-RECEIPT-PIN block is authoritative.
    two = _body_with({}) + "\n## OTHER\n\n" + _body_with({"merge_head_sha": OTHER_HEAD})
    verdict, reason = pin_mod.check_pin(two, GOOD_HEAD)
    assert verdict == "PASS", reason


def test_pin_block_ends_at_next_header():
    # Fields must not leak in from a following section.
    body = _body_with({}, drop=("board_comment_id",)) + "\n## NEXT\nboard_comment_id: 999\n"
    verdict, reason = pin_mod.check_pin(body, GOOD_HEAD)
    assert verdict == "TAMPERED", reason  # board_comment_id absent in the pin block


# ------------------------------------------------------------------ gate rung P12


def _pr_state(pin):
    return {"head_sha": GOOD_HEAD, "receipt_pin": pin}


def _p12_reasons(pr_state):
    _, reasons = gate_mod.may_auto_merge(pr_state)
    return [r for r in reasons if r.startswith("P12:")]


def test_gate_p12_missing_pin_blocked():
    reasons = _p12_reasons(_pr_state(None))
    assert len(reasons) == 1, reasons
    assert "missing" in reasons[0]


def test_gate_p12_malformed_sha_blocked():
    reasons = _p12_reasons(_pr_state({"merge_head_sha": "deadbeef"}))
    assert len(reasons) == 1, reasons
    assert "malformed" in reasons[0]


def test_gate_p12_stale_pin_blocked():
    reasons = _p12_reasons(_pr_state({"merge_head_sha": OTHER_HEAD}))
    assert len(reasons) == 1, reasons
    assert "stale" in reasons[0]


def test_gate_p12_exact_pin_produces_no_p12_reason():
    # P12 is satisfied; other preconditions may still fail (they are tested
    # elsewhere) - the assertion is precisely that P12 is not the blocker.
    reasons = _p12_reasons(_pr_state({"merge_head_sha": GOOD_HEAD}))
    assert reasons == [], reasons


# ------------------------------------------------- t952 CLI flags (CI wiring)


def _run_cli(mod, argv, cwd):
    import io
    from contextlib import redirect_stdout

    buf = io.StringIO()
    with redirect_stdout(buf):
        rc = mod.main(["prog"] + argv)
    return rc, buf.getvalue()


def test_pr_state_out_writes_pin_on_pass(tmp_path):
    out = tmp_path / "pr-state.json"
    body_file = tmp_path / "body.md"
    body_file.write_text(VALID_BODY, encoding="utf-8")
    rc, stdout = _run_cli(
        pin_mod, [GOOD_HEAD, str(body_file), "--pr-state-out", str(out)], cwd=None
    )
    assert rc == 0, stdout
    import json

    state = json.loads(out.read_text(encoding="utf-8"))
    assert state == {
        "head_sha": GOOD_HEAD,
        "receipt_pin": {"merge_head_sha": GOOD_HEAD},
    }, state


def test_pr_state_out_writes_nothing_on_fail(tmp_path):
    out = tmp_path / "pr-state.json"
    body_file = tmp_path / "body.md"
    body_file.write_text("no receipt here\n", encoding="utf-8")
    rc, stdout = _run_cli(
        pin_mod, [GOOD_HEAD, str(body_file), "--pr-state-out", str(out)], cwd=None
    )
    assert rc == 1, stdout  # MISSING fails; no pr-state file must be written
    assert not out.exists()


def test_gate_p12_only_passes_on_exact_pin(tmp_path):
    import json

    state_file = tmp_path / "pr-state.json"
    state_file.write_text(
        json.dumps({"head_sha": GOOD_HEAD, "receipt_pin": {"merge_head_sha": GOOD_HEAD}}),
        encoding="utf-8",
    )
    rc, stdout = _run_cli(gate_mod, ["--p12-only", str(state_file)], cwd=None)
    assert rc == 0, stdout
    out = json.loads(stdout)
    assert out["precondition"] == "P12" and out["allowed"] is True, out


def test_gate_p12_only_blocks_missing_pin(tmp_path):
    import json

    state_file = tmp_path / "pr-state.json"
    state_file.write_text(json.dumps({"head_sha": GOOD_HEAD}), encoding="utf-8")
    rc, stdout = _run_cli(gate_mod, ["--p12-only", str(state_file)], cwd=None)
    assert rc == 1, stdout
    out = json.loads(stdout)
    assert out["allowed"] is False and any(
        r.startswith("P12:") for r in out["reasons"]
    ), out


def test_gate_p12_only_blocks_stale_pin(tmp_path):
    import json

    state_file = tmp_path / "pr-state.json"
    state_file.write_text(
        json.dumps({"head_sha": GOOD_HEAD, "receipt_pin": {"merge_head_sha": OTHER_HEAD}}),
        encoding="utf-8",
    )
    rc, stdout = _run_cli(gate_mod, ["--p12-only", str(state_file)], cwd=None)
    assert rc == 1, stdout
    out = json.loads(stdout)
    assert out["allowed"] is False and any(
        "stale" in r for r in out["reasons"]
    ), out


# ------------------------------------------- FUTURE rung (Judge wave-216, L300/L316)

# #2682's future-dated receipt passed the gate on shape alone — temporal
# honesty now fails closed. Timestamps are computed relative to now so the
# tests are deterministic whenever they run.


def _future_body(decided_at):
    return _body_with({"decided_at": decided_at})


def _now_iso(offset_seconds):
    from datetime import datetime, timedelta, timezone

    return (datetime.now(timezone.utc) + timedelta(seconds=offset_seconds)).isoformat()


def test_pin_future_dated_receipt_fails_future():
    # The #2682 shape: ~4h in the future.
    verdict, reason = pin_mod.check_pin(_future_body(_now_iso(4 * 3600)), GOOD_HEAD)
    assert verdict == "FUTURE", reason
    assert "cannot have been posted" in reason


def test_pin_far_future_fails_future():
    verdict, reason = pin_mod.check_pin(_future_body(_now_iso(24 * 3600)), GOOD_HEAD)
    assert verdict == "FUTURE", reason


def test_pin_naive_future_timestamp_fails_future():
    # Naive timestamps are read as UTC.
    from datetime import datetime, timedelta, timezone

    naive = (datetime.now(timezone.utc).replace(tzinfo=None) + timedelta(hours=2)).isoformat()
    assert "+" not in naive and naive[-1] != "Z"
    verdict, reason = pin_mod.check_pin(_future_body(naive), GOOD_HEAD)
    assert verdict == "FUTURE", reason


def test_pin_just_outside_skew_fails_future():
    verdict, reason = pin_mod.check_pin(
        _future_body(_now_iso(pin_mod.FUTURE_SKEW_SECONDS + 30)), GOOD_HEAD
    )
    assert verdict == "FUTURE", reason


def test_is_future_dated_boundary_pins_strict_operator():
    # Genuine operator pin with a FIXED now (no wall-clock race): the check is
    # strict > — decided_at == now + skew is NOT future. A refactor to >=
    # would flip the first assertion, so this test pins the operator.
    from datetime import datetime, timedelta, timezone

    now = datetime(2026, 10, 16, 12, 0, 0, tzinfo=timezone.utc)
    skew = pin_mod.FUTURE_SKEW_SECONDS
    at_edge = now + timedelta(seconds=skew)
    assert pin_mod._is_future_dated(at_edge, now) is False
    assert (
        pin_mod._is_future_dated(at_edge + timedelta(microseconds=1), now) is True
    )
    assert (
        pin_mod._is_future_dated(at_edge - timedelta(microseconds=1), now) is False
    )
    # Naive timestamps are read as UTC before the comparison.
    assert pin_mod._is_future_dated(at_edge.replace(tzinfo=None), now) is False


def test_pin_just_inside_skew_passes():
    # CI clock drift inside the skew is tolerated, not punished.
    verdict, reason = pin_mod.check_pin(
        _future_body(_now_iso(pin_mod.FUTURE_SKEW_SECONDS - 30)), GOOD_HEAD
    )
    assert verdict == "PASS", reason


def test_pin_past_receipt_still_passes():
    verdict, reason = pin_mod.check_pin(_future_body(_now_iso(-3600)), GOOD_HEAD)
    assert verdict == "PASS", reason


def test_pin_cli_future_dated_exits_1_and_writes_no_pr_state(tmp_path):
    # Fail-closed propagation: no pr-state file is written, so the gate-side
    # P12 rung never sees the future-dated pin at all.
    out = tmp_path / "pr-state.json"
    body_file = tmp_path / "body.md"
    body_file.write_text(_future_body(_now_iso(3600)), encoding="utf-8")
    rc, stdout = _run_cli(
        pin_mod, [GOOD_HEAD, str(body_file), "--pr-state-out", str(out)], cwd=None
    )
    assert rc == 1, stdout
    assert not out.exists()


def test_is_future_dated_unit_probe():
    from datetime import datetime, timedelta, timezone

    now = datetime.now(timezone.utc)
    assert pin_mod._is_future_dated(now + timedelta(hours=4), now) is True
    assert pin_mod._is_future_dated(now - timedelta(hours=4), now) is False
    assert (
        pin_mod._is_future_dated(
            now.replace(tzinfo=None) + timedelta(hours=4), now
        )
        is True
    )  # naive read as UTC


if __name__ == "__main__":
    sys.exit(0)

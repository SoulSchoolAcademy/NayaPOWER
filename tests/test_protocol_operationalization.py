"""Self-test suite for PROTOCOL OPERATIONALIZATION (items 1-10).

Proves a full Naya cycle against the real gates:

    DECLARE   -> declaration receipt round-trip + boot gate pin
    DELIBERATE-> decision_receipt (Step 6 scored deliberation)
    LOOP      -> scorecard_loop (Step 15, full weight, 3 rounds)
    VERDICT   -> completion_receipt (Value Verdict first)
    CAPTURE   -> learning_capture (Step 14 lesson with provenance)
    SEPARATION-> identity_separation (different-identity verification)
    SYNC      -> protocol_version_sync (machine spec vs PROTOCOL.md)
    WATCHDOG  -> drift_watchdog flags identity drift + missing receipts

Runs under plain ``python3`` without pytest:

    python3 tests/test_protocol_operationalization.py

…as well as under pytest (plain ``test_*`` functions, plain asserts).

Network dependency: test_boot_gate_passes_with_protocol_pin runs the
real boot gate (kernel/protocol/protocol_integrity_gate.py), which
resolves origin/main via ``git ls-remote``. That test therefore
needs network / git-remote access and a resolvable origin; a
failure there on an offline box is an environment failure, not
evidence the pin is wrong — it is noted here so a reader does not
have to rediscover it.

Modules are loaded by file path with importlib, mirroring
tests/test_bootgate_checklist_wiring.py. Checks are loaded through
the contracted path: sys.path carries tools/protocol/ and the
modules are imported as ``checks.<module>``.

Some dependencies land in parallel (identity_separation,
scorecard_loop, completion_receipt, protocol_version_sync and the
boot gate's protocol_pin wiring). If a module is missing, its
test fails with the import error visible — the test is never
weakened to make it pass; it awaits integration.
"""

from __future__ import annotations

import importlib
import importlib.util
import json
import subprocess
import sys
import tempfile
import traceback
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Contracted checks import path.
_CHECKS_DIR = ROOT / "tools" / "protocol"
if str(_CHECKS_DIR) not in sys.path:
    sys.path.insert(0, str(_CHECKS_DIR))
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def _load_module(name: str, path: Path):
    """Load a module by file path (mirror of the bootgate test style)."""
    if not path.exists():
        raise FileNotFoundError(f"module not found: {path}")
    spec = importlib.util.spec_from_file_location(name, str(path))
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot load module {name} from {path}")
    module = importlib.util.module_from_spec(spec)
    # Register before exec: dataclasses (learning_capture) look
    # their module up in sys.modules during class creation.
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def _load_check(module_name: str):
    """Import checks.<module_name> via the contracted sys.path."""
    return importlib.import_module(f"checks.{module_name}")


# ---------------------------------------------------------------------------
# 1. Machine spec in sync
# ---------------------------------------------------------------------------


def test_machine_spec_in_sync():
    """protocol_version_sync.check(ROOT) passes on the real tree."""
    mod = _load_module(
        "protocol_version_sync",
        ROOT / "tools" / "protocol" / "checks" / "protocol_version_sync.py",
    )
    result = mod.check(ROOT)
    assert isinstance(result, dict), f"expected dict result, got {result!r}"
    assert result.get("pass") is True, (
        f"machine spec out of sync: reasons={result.get('reasons')} "
        f"details={result.get('details')}"
    )


# ---------------------------------------------------------------------------
# 2. Boot gate passes with the protocol pin
# ---------------------------------------------------------------------------


def test_boot_gate_passes_with_protocol_pin():
    """The real boot gate exits 0 and its protocol_pin check passes.

    NOTE: the gate resolves origin/main via ``git ls-remote`` —
    this test has a network / git-remote dependency (see the
    module docstring).
    """
    gate = ROOT / "kernel" / "protocol" / "protocol_integrity_gate.py"
    assert gate.exists(), f"boot gate not found: {gate}"
    proc = subprocess.run(
        [sys.executable, str(gate), "--agent-id", "selftest", "--json"],
        capture_output=True,
        text=True,
        timeout=120,
        cwd=str(ROOT),
    )
    assert proc.returncode == 0, (
        f"boot gate exited {proc.returncode}: "
        f"stdout={proc.stdout[:2000]} stderr={proc.stderr[:2000]}"
    )
    data = json.loads(proc.stdout)
    assert data.get("pass") is True, f"boot gate did not pass: {data}"
    checks = data.get("checks") or []
    pin_checks = [c for c in checks if c.get("name") == "protocol_pin"]
    assert pin_checks, (
        f"no check named 'protocol_pin' in boot gate output: "
        f"{[c.get('name') for c in checks]}"
    )
    assert pin_checks[0].get("pass") is True, (
        f"protocol_pin check did not pass: {pin_checks[0]}"
    )


# ---------------------------------------------------------------------------
# 3. Declaration receipt round-trip
# ---------------------------------------------------------------------------


def test_declaration_receipt_roundtrip():
    """Issue a Step 0 declaration receipt, verify it, tamper it."""
    pin = _load_module("protocol_pin", ROOT / "tools" / "protocol_pin.py")

    receipt = pin.issue_declaration_receipt(ROOT, "selftest-naya")
    assert receipt.get("schema") == "naya.declaration-receipt.v1", receipt
    assert receipt.get("agent_id") == "selftest-naya", receipt

    violations = pin.check_declaration_receipt(ROOT, receipt)
    assert violations == [], f"fresh receipt should be valid: {violations}"

    # Tampered protocol fingerprint -> violations.
    tampered = dict(receipt)
    tampered["protocol_sha256"] = "0" * 64
    violations = pin.check_declaration_receipt(ROOT, tampered)
    assert violations, "tampered protocol_sha256 must produce violations"

    # Receipt naming no agent -> violations.
    anonymous = dict(receipt)
    anonymous["agent_id"] = ""
    violations = pin.check_declaration_receipt(ROOT, anonymous)
    assert violations, "receipt with empty agent_id must produce violations"


# ---------------------------------------------------------------------------
# 4. Cycle — deliberate (decision receipt)
# ---------------------------------------------------------------------------


def _valid_decision_record():
    return {
        "decision": "Choose the operationalization test strategy",
        "chosen": "opt-c",
        "alternatives": [
            {"id": "opt-a", "description": "No tests; ship and hope"},
            {"id": "opt-b", "description": "Unit tests only for the watchdog"},
            {"id": "opt-c", "description": "Full-cycle tests against the real gates"},
        ],
        "winning_evidence": (
            "opt-c exercises every real gate end to end; opt-a proves "
            "nothing and opt-b leaves the loop and verdict unchecked"
        ),
        "receipt": (
            "I chose opt-c. I looked at opt-a, opt-b, opt-c. "
            "opt-c won because it exercises every real gate end to end."
        ),
        "seat": "selftest-naya",
        "close_call": False,
        "uncertainty_declared": False,
    }


def test_cycle_deliberate():
    """decision_receipt: a valid record passes; 1 alternative fails."""
    mod = _load_check("decision_receipt")

    valid = _valid_decision_record()
    result = mod.check(valid)
    assert result.get("pass") is True, (
        f"valid decision record should pass: {result.get('reasons')}"
    )

    thin = _valid_decision_record()
    thin["alternatives"] = [
        {"id": "opt-a", "description": "The only option considered"},
    ]
    thin["chosen"] = "opt-a"
    thin["receipt"] = "I chose opt-a. I looked at opt-a."
    result = mod.check(thin)
    assert result.get("pass") is False, (
        "a decision with only 1 alternative is guessing, not a decision; "
        f"it must fail, got: {result}"
    )


# ---------------------------------------------------------------------------
# 5. Cycle — scorecard loop (Step 15)
# ---------------------------------------------------------------------------


def _make_rounds(scores):
    """Build scorecard_loop rounds with a consistent rescore chain.

    Contract (scorecard_loop docstring): every non-final round
    carries a rescore, and that rescore equals the next round's
    score; final_score equals the last round's score when the
    last round carries no rescore. fixes_applied is non-empty on
    every non-final round; why_not_10 is a non-empty list on
    every round.
    """
    rounds = []
    for index, score in enumerate(scores):
        round_no = index + 1
        is_final = index == len(scores) - 1
        if is_final:
            fixes = []
        else:
            fixes = [
                f"round {round_no} fix: addressed the top "
                f"why-not-10 gap for round {round_no} with a "
                f"concrete change",
            ]
        entry = {
            "round": round_no,
            "score": score,
            "why_not_10": [
                f"round {round_no} gap: coverage and polish are "
                f"not yet at the 10 standard for round {round_no}",
            ],
            "fixes_applied": fixes,
        }
        if not is_final:
            entry["rescore"] = scores[index + 1]
        rounds.append(entry)
    return rounds


def _scorecard_record(scores, final_score, failure_note_ref=None):
    record = {
        "claim": "Protocol operationalization self-test cycle complete",
        "weight": "full",
        "work_product": "protocol operationalization self-test cycle",
        "subject": "protocol operationalization self-test cycle",
        "objective": "Prove a full Naya cycle against the real gates",
        "ultimate_objective": (
            "Prove a full Naya cycle against the real gates"
        ),
        "seat": "selftest-naya",
        "scorer": "selftest-naya",
        "rounds": _make_rounds(scores),
        "final_score": final_score,
    }
    if failure_note_ref is not None:
        record["failure_note_ref"] = failure_note_ref
        record["failure_note"] = failure_note_ref
    return record


def test_cycle_scorecard_loop():
    """scorecard_loop: full-weight 3 rounds to 9+ passes; the
    failure paths behave exactly as Step 15 demands."""
    mod = _load_check("scorecard_loop")

    # Valid: 7.0 -> 8.5 -> 9.5, fixes on rounds 1-2, chain consistent.
    valid = _scorecard_record([7.0, 8.5, 9.5], 9.5)
    result = mod.check(valid)
    assert result.get("pass") is True, (
        f"valid full-weight 3-round record should pass: "
        f"reasons={result.get('reasons')} details={result.get('details')}"
    )

    # One round at full weight is not the loop.
    one_round = _scorecard_record([9.5], 9.5)
    result = mod.check(one_round)
    assert result.get("pass") is False, (
        f"1-round full-weight record must fail, got: {result}"
    )

    # Below 9 after three rounds, with no failure note: does not ship.
    below = _scorecard_record([6.0, 7.0, 8.0], 8.0)
    result = mod.check(below)
    assert result.get("pass") is False, (
        f"final_score 8.0 without failure_note_ref must fail, got: {result}"
    )

    # Below 9 WITH the failure itself filed as a note: the check
    # passes the receipt, but the work explicitly does not ship.
    filed = _scorecard_record(
        [6.0, 7.0, 8.0], 8.0,
        failure_note_ref="SN-SELFTEST-FAILURE-NOTE",
    )
    result = mod.check(filed)
    assert result.get("pass") is True, (
        f"below-9 record with failure_note_ref should pass the "
        f"receipt check: reasons={result.get('reasons')} "
        f"details={result.get('details')}"
    )
    details = result.get("details") or {}
    assert details.get("shipped") is False, (
        f"below-9 work must record shipped is False, details={details}"
    )


# ---------------------------------------------------------------------------
# 6. Cycle — value verdict (completion receipt)
# ---------------------------------------------------------------------------


def _completion_record(include_value_verdict=True):
    # Contract (completion_receipt docstring): claim, seat,
    # value_verdict {beneficiary, how}, evidence, next_action,
    # and a nested scorecard_loop {objective, weight, rounds,
    # final_score} validated by the sibling scorecard_loop check.
    record = {
        "claim": "Protocol operationalization self-test cycle complete",
        "task": "Protocol operationalization self-test cycle",
        "work_product": "Protocol operationalization self-test cycle",
        "subject": "Protocol operationalization self-test cycle",
        "seat": "selftest-naya",
        "agent_id": "selftest-naya",
        "evidence": (
            "Receipt: tests in tests/test_protocol_operationalization.py "
            "run against the real gates; see the test output as evidence"
        ),
        "next_action": "Integrate the remaining protocol checks and re-run",
        "single_next_action": (
            "Integrate the remaining protocol checks and re-run"
        ),
        "scorecard_loop": {
            "objective": (
                "Prove a full Naya cycle against the real gates"
            ),
            "weight": "full",
            "rounds": _make_rounds([7.0, 8.5, 9.5]),
            "final_score": 9.5,
        },
    }
    if include_value_verdict:
        record["value_verdict"] = {
            "beneficiary": "Shawn and Team Naya",
            "how": (
                "protocol drift now drafts flags automatically and "
                "a full cycle is provable against the real gates "
                "instead of asserted in prose — the work is useful, "
                "not merely procedurally clean"
            ),
        }
    return record


def test_cycle_value_verdict():
    """completion_receipt: valid passes; no value verdict fails
    with a reason that names the value verdict."""
    mod = _load_check("completion_receipt")

    valid = _completion_record(include_value_verdict=True)
    result = mod.check(valid)
    assert result.get("pass") is True, (
        f"valid completion record should pass: "
        f"reasons={result.get('reasons')} details={result.get('details')}"
    )

    no_verdict = _completion_record(include_value_verdict=False)
    result = mod.check(no_verdict)
    assert result.get("pass") is False, (
        f"completion without a value verdict must fail, got: {result}"
    )
    reasons_text = " ".join(str(r) for r in (result.get("reasons") or []))
    assert "value" in reasons_text.lower() and (
        "verdict" in reasons_text.lower()
    ), (
        "the failure reason must mention the value verdict, "
        f"got reasons: {result.get('reasons')}"
    )


# ---------------------------------------------------------------------------
# 7. Cycle — capture (learning)
# ---------------------------------------------------------------------------


def test_cycle_capture():
    """learning_capture: a lesson with provenance passes; silence fails."""
    mod = _load_module(
        "learning_capture",
        ROOT / "kernel" / "protocol" / "learning_capture.py",
    )

    good = mod.CycleLesson(
        work_description="Protocol operationalization self-test cycle",
        lesson=(
            "A declaration receipt is only as strong as the live "
            "bytes it is recomputed against at verification time"
        ),
        provenance=(
            "test_declaration_receipt_roundtrip: tampering the "
            "protocol fingerprint produced violations"
        ),
    )
    result = mod.check_lesson(good)
    assert result.passed is True, (
        f"lesson with provenance should pass: {result.reasons}"
    )

    empty = mod.CycleLesson(
        work_description="Protocol operationalization self-test cycle",
        lesson="",
        no_lesson_reason="",
    )
    result = mod.check_lesson(empty)
    assert result.passed is False, (
        "an empty lesson with no no-lesson reason must fail: "
        f"{result}"
    )
    assert result.reasons, "the failure must carry reasons"


# ---------------------------------------------------------------------------
# 8. Identity separation — the breach fixture
# ---------------------------------------------------------------------------


def test_identity_separation_breach_fixture():
    """The 2026-10-20 breach shape fails; an independent fixture passes."""
    mod = _load_check("identity_separation")

    breach = {
        "number": 2796,
        "author_login": "nayapower-lane-agent[bot]",
        "merger_login": "nayapower-lane-agent[bot]",
        "merged": True,
        "reviews": [
            {"login": "nayapower-lane-agent[bot]", "state": "COMMENTED"},
        ],
    }
    result = mod.check(breach)
    assert result.get("pass") is False, (
        "same-login author + sole same-login review + same-login "
        f"merger is the ruled breach; it must fail, got: {result}"
    )

    # Independent means different from BOTH author and merger
    # (identity_separation check 5/6): a review from the merger's
    # own login is the merger agreeing with herself, so the clean
    # fixture carries a third identity as reviewer, with the
    # merger also distinct from the author.
    clean = {
        "number": 2797,
        "author_login": "nayapower-lane-agent[bot]",
        "merger_login": "someone-else",
        "merged": True,
        "reviews": [
            {"login": "independent-reviewer", "state": "APPROVED"},
        ],
    }
    result = mod.check(clean)
    assert result.get("pass") is True, (
        f"independent reviewer + independent merger should pass: "
        f"reasons={result.get('reasons')} details={result.get('details')}"
    )


# ---------------------------------------------------------------------------
# 9. Drift watchdog flags
# ---------------------------------------------------------------------------


def test_drift_watchdog_flags():
    """The watchdog drafts IDENTITY_DRIFT and DONE_WITHOUT_RECEIPT."""
    watchdog = ROOT / "tools" / "protocol" / "drift_watchdog.py"
    assert watchdog.exists(), f"drift watchdog not found: {watchdog}"

    prs = [
        {
            "number": 2796,
            "author_login": "nayapower-lane-agent[bot]",
            "merger_login": "nayapower-lane-agent[bot]",
            "merged": True,
            "reviews": [
                {"login": "nayapower-lane-agent[bot]",
                 "state": "COMMENTED"},
            ],
            "body": "Done. This work is complete and shipped.",
        },
    ]
    posts = [
        {
            "id": "post-selftest-1",
            "author": "someone",
            "body": "Done — the thing is shipped.",
        },
    ]

    with tempfile.TemporaryDirectory(prefix="drift-watchdog-test-") as tmp:
        tmp_path = Path(tmp)
        prs_path = tmp_path / "prs.json"
        posts_path = tmp_path / "posts.json"
        prs_path.write_text(json.dumps(prs), encoding="utf-8")
        posts_path.write_text(json.dumps(posts), encoding="utf-8")

        proc = subprocess.run(
            [
                sys.executable, str(watchdog),
                "--prs", f"@{prs_path}",
                "--posts", f"@{posts_path}",
            ],
            capture_output=True,
            text=True,
            timeout=60,
            cwd=str(ROOT),
        )

    assert proc.returncode == 0, (
        f"watchdog (non-strict) should exit 0, got "
        f"{proc.returncode}: stdout={proc.stdout[:2000]} "
        f"stderr={proc.stderr[:2000]}"
    )
    report = proc.stdout
    assert "IDENTITY_DRIFT" in report, (
        f"breaching PR must draft an IDENTITY_DRIFT flag:\n{report}"
    )
    assert "DONE_WITHOUT_RECEIPT" in report, (
        f"board post claiming done with no receipt marker must "
        f"draft a DONE_WITHOUT_RECEIPT flag:\n{report}"
    )


# ---------------------------------------------------------------------------
# __main__ runner — plain python3, no pytest required
# ---------------------------------------------------------------------------


def _run_all():
    tests = [
        (name, obj)
        for name, obj in sorted(globals().items())
        if name.startswith("test_") and callable(obj)
    ]
    passed = []
    failed = []
    for name, fn in tests:
        try:
            fn()
        except Exception:
            failed.append(name)
            print(f"FAIL {name}")
            traceback.print_exc()
        else:
            passed.append(name)
            print(f"PASS {name}")
    print("")
    print(f"PASS: {len(passed)}  FAIL: {len(failed)}  TOTAL: {len(tests)}")
    if passed:
        print(f"Passed: {', '.join(passed)}")
    if failed:
        print(f"Failed: {', '.join(failed)}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(_run_all())

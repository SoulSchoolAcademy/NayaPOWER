"""Tests for the merge-packet producer (tools/protocol/checks/make_merge_packet.py).

The producer assembles the Delegated-Merge-Authority --packet from the
merge lane's post bodies plus explicit flags, FAIL-CLOSED:
  * explicit flags always win over derivation;
  * a field is derived ONLY from text the posts state plainly, matched by
    conservative patterns, unambiguous;
  * anything not stated plainly -> refusal (exit 1) naming the missing
    field — never fabricated;
  * assertion-only fields (branch, seat, evidence_backed,
    value_calculus_run, report_planned) are never derived;
  * every assembled packet runs through the REAL checks.merge_authority.check
    (the same function the merge gate calls) before it leaves.

Runnable with plain python3 (no pytest required):
    python3 tests/test_merge_packet_producer.py
Also pytest-compatible (plain assert functions).

D32: these tests prove the producer's refusal/assembly behavior and that
its packets pass the real check. They cannot prove a cited comment id is
real, a green claim happened, or a score was earned — the independent
validator, the team consensus on the live feed, and the #2154 receipts are
what make those true.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECKS = ROOT / "tools" / "protocol" / "checks"
sys.path.insert(0, str(CHECKS.parent))

from checks import merge_authority  # noqa: E402 — the REAL check first
from checks import make_merge_packet as mmp  # noqa: E402

PRODUCER = CHECKS / "make_merge_packet.py"

# The live operator copies (the actual merge path) — read-only use: we
# never touch them, only prove the producer's packet satisfies their gate.
OPERATOR_BIN = Path.home() / "workspace" / "naya" / "bin"


def _cli(*argv, bodies=None, env_extra=None):
    """Run the producer CLI in a temp dir holding any --*-body-file inputs.

    NAYAPOWER_REPO forces the producer's checks resolution onto THIS tip's
    tools/protocol copy (the live tip), not a stale clone.
    """
    with tempfile.TemporaryDirectory() as td:
        args = list(argv)
        if bodies:
            for flag, name, text in bodies:
                p = Path(td) / name
                p.write_text(text)
                args += [flag, str(p)]
        env = dict(os.environ, NAYAPOWER_REPO=str(ROOT))
        env.update(env_extra or {})
        return subprocess.run(
            [sys.executable, str(PRODUCER), *args],
            capture_output=True, text=True, env=env)


def _assemble(**kwargs):
    """Drive make_merge_packet.assemble() in-process with plain kwargs."""
    bodies = kwargs.pop("bodies", [])
    paths = []
    tmpdir = tempfile.mkdtemp()
    for i, (label, text) in enumerate(bodies):
        p = Path(tmpdir) / f"{label}-{i}.txt"
        p.write_text(text)
        paths.append(p)
    args = mmp.parse_argv([])
    for k, v in kwargs.items():
        setattr(args, k, v)
    labels = ["scorecard", "iv", "intent"]
    for i, p in enumerate(paths):
        label = labels[i] if i < len(labels) else "body"
        if label == "scorecard":
            args.scorecard_body_file = str(p)
        elif label == "iv":
            args.iv_body_file = str(p)
        elif label == "intent":
            args.intent_body_file = str(p)
        else:
            args.body_file.append(str(p))
    return mmp.assemble(args)


_FULL = dict(
    branch="naya5/example",
    seat="Naya 5",
    score=9.2,
    tests_green=True,
    test_evidence="https://ci.example/runs/42 — 15/15 tests green",
    evidence_backed=True,
    value_calculus_run=True,
    independent_validator="Naya Epsilon",
    feed_comment=["6119000001"],
    team_objections=0,
    report_planned=True,
)

# ---------------------------------------------------------------------------
# 1. Honoring input: a complete explicit packet assembles and PASSES the
#    real check — the same function the merge gate calls.
# ---------------------------------------------------------------------------


def test_explicit_packet_assembles_and_passes_real_check():
    packet, receipt = _assemble(**_FULL)
    assert packet["target"] == "main"
    assert packet["branch"] == "naya5/example"
    assert packet["self_scorecard"]["score"] == 9.2
    assert packet["independent_validator"] == "Naya Epsilon"
    assert packet["team_objections"] == 0
    res = merge_authority.check(packet)
    assert res["pass"], res["reasons"]
    assert len(receipt) == 11  # one provenance line per emitted field


def test_cli_emits_packet_that_passes_real_check():
    r = _cli("--branch", "naya5/example", "--seat", "Naya 5",
             "--score", "9.2", "--tests-green",
             "--test-evidence", "https://ci.example/runs/42 — 15/15 passed",
             "--evidence-backed", "--value-calculus-run",
             "--independent-validator", "Naya Epsilon",
             "--feed-comment", "6119000001", "--team-objections", "0",
             "--report-planned")
    assert r.returncode == 0, r.stderr
    packet = json.loads(r.stdout)
    assert merge_authority.check(packet)["pass"]
    assert "PASSED the real check" in r.stderr


# ---------------------------------------------------------------------------
# 2. Fail-closed: every missing field refuses, naming the field.
#    One run names ALL missing fields (single trip through the refusals).
# ---------------------------------------------------------------------------

_MISSING_CASES = [
    ("branch", {"branch": None}),
    ("seat", {"seat": None}),
    ("self_scorecard.score", {"score": None}),
    ("tests_green", {"tests_green": False}),
    ("test_evidence", {"test_evidence": None}),
    ("independent_validator", {"independent_validator": None}),
    ("posted_to_1354", {"feed_comment": []}),
    ("team_objections", {"team_objections": None}),
    ("self_scorecard.evidence_backed", {"evidence_backed": False}),
    ("self_scorecard.value_calculus_run", {"value_calculus_run": False}),
    ("post_merge_report_planned", {"report_planned": False}),
]


def test_each_missing_field_refuses_and_is_named():
    for field, override in _MISSING_CASES:
        kw = dict(_FULL)
        kw.update(override)
        try:
            _assemble(**kw)
        except mmp._MultiRefusal as e:
            fields = [r.field for r in e.refusals]
            assert field in fields, f"missing {field} not named in {fields}"
        else:
            raise AssertionError(f"missing {field}: assembled instead of refusing")


def test_single_run_names_every_missing_field():
    kw = dict(_FULL)
    kw.update(branch=None, seat=None, score=None, tests_green=False,
              test_evidence=None, independent_validator=None,
              feed_comment=[], team_objections=None,
              evidence_backed=False, value_calculus_run=False,
              report_planned=False)
    try:
        _assemble(**kw)
    except mmp._MultiRefusal as e:
        named = {r.field for r in e.refusals}
        for field, _ in _MISSING_CASES:
            assert field in named, f"{field} not named"
    else:
        raise AssertionError("empty input assembled instead of refusing")


def test_cli_refuses_naming_missing_fields():
    r = _cli("--branch", "naya5/x")
    assert r.returncode == 1, r.stdout
    assert "PACKET REFUSED" in r.stderr
    for needle in ("seat", "self_scorecard.score", "tests_green",
                   "test_evidence", "independent_validator", "posted_to_1354",
                   "team_objections", "evidence_backed", "value_calculus_run",
                   "report_planned"):
        assert needle in r.stderr, f"{needle} not named in refusal"


# ---------------------------------------------------------------------------
# 3. Never fabricate: ambiguity refuses; sub-bar scores refuse through the
#    real check; green-with-failures is not a green claim.
# ---------------------------------------------------------------------------


def test_ambiguous_scores_refuse():
    bodies = [("scorecard",
               "builder scorecard: \"score\": 9.2 ... the IV gave it 9.0/10")]
    try:
        _assemble(**dict(_FULL, score=None, bodies=bodies))
    except mmp._MultiRefusal as e:
        assert any(r.field == "self_scorecard.score"
                   and "ambiguous" in r.reason for r in e.refusals)
    else:
        raise AssertionError("ambiguous scores: picked instead of refusing")


def test_derived_sub_bar_score_refuses_through_real_check():
    r = _cli("--branch", "naya5/x", "--seat", "Naya 5",
             "--tests-green",
             "--test-evidence", "https://ci.example/runs/9 — 12/12 passed",
             "--evidence-backed", "--value-calculus-run",
             "--independent-validator", "Naya Epsilon",
             "--feed-comment", "6119000001", "--team-objections", "0",
             "--report-planned",
             bodies=[("--scorecard-body-file", "sc.txt",
                      "builder self-scorecard: 8.5/10 — below the bar")])
    assert r.returncode == 1, r.stdout
    assert "below 9.0" in r.stderr  # the REAL check's own reason


def test_ambiguous_validator_refuses():
    bodies = [("iv", "validated by Naya Epsilon; independent validator: Coda 1")]
    try:
        _assemble(**dict(_FULL, independent_validator=None, bodies=bodies))
    except mmp._MultiRefusal as e:
        assert any(r.field == "independent_validator"
                   and "ambiguous" in r.reason for r in e.refusals)
    else:
        raise AssertionError("ambiguous validators: picked instead of refusing")


def test_non_seat_shaped_validator_text_not_fabricated():
    bodies = [("iv", "VERDICT A — independent validation complete, 9.5/10")]
    try:
        _assemble(**dict(_FULL, independent_validator=None, bodies=bodies))
    except mmp._MultiRefusal as e:
        assert any(r.field == "independent_validator" for r in e.refusals)
    else:
        raise AssertionError("verdict text became a fabricated validator")


def test_self_validator_refuses_after_normalization():
    # "Naya_5" vs "Naya 5" is the same seat wearing different punctuation.
    try:
        _assemble(**dict(_FULL, independent_validator="Naya_5"))
    except mmp._MultiRefusal as e:
        assert any(r.field == "independent_validator" for r in e.refusals)
    else:
        raise AssertionError("self-validation passed as independent")


def test_green_line_with_failures_is_not_derived():
    bodies = [("scorecard",
               "full suite: 2827 passed, 6 failed — green on the branch")]
    try:
        _assemble(**dict(_FULL, tests_green=False, bodies=bodies))
    except mmp._MultiRefusal as e:
        assert any(r.field == "tests_green" for r in e.refusals)
    else:
        raise AssertionError("line naming failures derived as green")


def test_bare_green_without_counts_is_not_derived():
    bodies = [("scorecard", "everything is green, ship it")]
    try:
        _assemble(**dict(_FULL, tests_green=False, bodies=bodies))
    except mmp._MultiRefusal as e:
        assert any(r.field == "tests_green" for r in e.refusals)
    else:
        raise AssertionError("countless 'green' derived as tests_green")


def test_malformed_feed_comment_refuses():
    try:
        _assemble(**dict(_FULL, feed_comment=["abc"]))
    except mmp._MultiRefusal as e:
        assert any(r.field == "posted_to_1354" for r in e.refusals)
    else:
        raise AssertionError("non-id feed comment accepted as a claim")


def test_nonzero_objections_refuse_the_packet():
    try:
        _assemble(**dict(_FULL, team_objections=2))
    except mmp._MultiRefusal as e:
        assert any(r.field == "team_objections" and "2 objection" in r.reason
                   for r in e.refusals)
    else:
        raise AssertionError("objections on record: packet assembled")


# ---------------------------------------------------------------------------
# 4. Explicit flags always win over derivation — with a warning on stderr,
#    so an override of what the posts say is a conscious act.
# ---------------------------------------------------------------------------


def test_explicit_wins_over_derivation():
    bodies = [
        ("scorecard", "builder scorecard: \"score\": 9.2 — 15/15 tests green"),
        ("iv", "validated by Naya Epsilon"),
    ]
    packet, _ = _assemble(**dict(_FULL, score=9.5,
                                 independent_validator="Naya Theta",
                                 bodies=bodies))
    assert packet["self_scorecard"]["score"] == 9.5
    assert packet["independent_validator"] == "Naya Theta"


def test_derivation_honors_plain_words():
    bodies = [
        ("scorecard", "builder self-scorecard: 9.2/10 — 15/15 tests green"),
        ("iv", "independent validator: Naya Epsilon"),
    ]
    kw = dict(_FULL, score=None, tests_green=False, test_evidence=None,
              independent_validator=None, bodies=bodies)
    kw["test_evidence"] = "https://ci.example/runs/42 — 15/15 passed"
    packet, _ = _assemble(**kw)
    assert packet["self_scorecard"]["score"] == 9.2
    assert packet["tests_green"] is True
    assert packet["independent_validator"] == "Naya Epsilon"
    assert merge_authority.check(packet)["pass"]


def test_cli_out_file_writes_packet_json():
    with tempfile.TemporaryDirectory() as td:
        out = Path(td) / "packet.json"
        r = _cli("--branch", "naya5/example", "--seat", "Naya 5",
                 "--score", "9.2", "--tests-green",
                 "--test-evidence", "https://ci.example/runs/42 — 15/15 passed",
                 "--evidence-backed", "--value-calculus-run",
                 "--independent-validator", "Naya Epsilon",
                 "--feed-comment", "6119000001", "--team-objections", "0",
                 "--report-planned", "--out", str(out))
        assert r.returncode == 0, r.stderr
        packet = json.loads(out.read_text())
        assert merge_authority.check(packet)["pass"]


def test_unreadable_body_file_is_usage_error():
    r = _cli("--branch", "naya5/x", "--seat", "Naya 5",
             "--scorecard-body-file", "/nonexistent/scorecard.txt")
    assert r.returncode == 2
    assert "cannot read" in r.stderr


# ---------------------------------------------------------------------------
# 5. Every real-check failure reason maps to the fixing input — drive the
#    REAL check on broken packets, prove no reason is unmapped.
# ---------------------------------------------------------------------------


def _broken_variants():
    good = {
        "target": "main", "branch": "b", "seat": "Naya 5",
        "tests_green": True,
        "test_evidence": "https://ci.example/runs/1 — 10/10 passed",
        "self_scorecard": {"score": 9.2, "evidence_backed": True,
                           "value_calculus_run": True},
        "independent_validator": "Naya Epsilon",
        "posted_to_1354": True, "team_objections": 0,
        "post_merge_report_planned": True,
    }

    def v(**kw):
        p = dict(good)
        p.update(kw)
        return p

    return [
        v(branch=""),
        v(seat=""),
        v(tests_green=False),
        v(test_evidence=""),
        v(test_evidence="trust me, green"),
        v(self_scorecard={}),
        v(self_scorecard={"score": "nine", "evidence_backed": True,
                          "value_calculus_run": True}),
        v(self_scorecard={"score": float("nan"), "evidence_backed": True,
                          "value_calculus_run": True}),
        v(self_scorecard={"score": 8.5, "evidence_backed": True,
                          "value_calculus_run": True}),
        v(self_scorecard={"score": 9.2, "evidence_backed": False,
                          "value_calculus_run": True}),
        v(self_scorecard={"score": 9.2, "evidence_backed": True,
                          "value_calculus_run": False}),
        v(independent_validator=""),
        v(independent_validator="Naya 5"),
        v(independent_validator="naya-5"),
        v(posted_to_1354=False),
        v(team_objections=1),
        v(post_merge_report_planned=False),
    ]


def test_every_real_check_reason_maps_to_a_fixing_input():
    for packet in _broken_variants():
        res = merge_authority.check(packet)
        assert not res["pass"], f"broken packet passed: {packet}"
        for reason in res["reasons"]:
            field, fix = mmp.map_reason_to_input(reason)
            assert (field, fix) != ("packet", "--help"), \
                f"unmapped real reason: {reason!r}"


# ---------------------------------------------------------------------------
# 6. The real operator copies: the --packet contract holds on the actual
#    merge path (read-only: we only prove refusal/passage, never merge).
# ---------------------------------------------------------------------------


def _load_operator_gate():
    gate = OPERATOR_BIN / "merge_gate.py"
    assert gate.is_file(), "operator merge_gate.py missing"
    ns = {"__file__": str(gate)}
    exec(compile(gate.read_text(), str(gate), "exec"), ns)  # noqa: S102 — read-only gate logic
    return ns


def test_operator_gate_refuses_without_packet():
    ns = _load_operator_gate()
    try:
        ns["enforce"]("refs/heads/main", None)
    except ns["GateRefused"] as e:
        assert any("no merge packet" in r for r in e.reasons)
    else:
        raise AssertionError("operator gate allowed a main update with no packet")


def test_operator_gate_passes_producer_packet():
    ns = _load_operator_gate()
    packet, _ = _assemble(**_FULL)
    res = ns["enforce"]("refs/heads/main", packet)
    assert res["allowed"] is True


def _run_all():
    fns = sorted(
        (n, f) for n, f in globals().items()
        if n.startswith("test_") and callable(f))
    failed = 0
    for n, f in fns:
        try:
            f()
            print(f"PASS {n}")
        except Exception as e:  # noqa: BLE001 — plain-runner reports all
            failed += 1
            print(f"FAIL {n}: {type(e).__name__}: {e}")
    print(f"{len(fns) - failed}/{len(fns)} passed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(_run_all())

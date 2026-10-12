"""Tests for the second independent collector (collector2.py).

Covers: the C2 exclusion gate (fail closed, not just unused), versioned
marker attribution (case-sensitive, first-person only), reported-speech
fail-closed, deterministic re-runs, candidate grading against collector2's
evidence only, baseline re-judgment verdicts, C3 empty-allowlist fail-closed,
NULL sweep logging, and the independence invariants.

All fixtures are SYNTHETIC (fixture: true). They prove the machinery works
mechanically. They are not measurements of any human.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from tools.human_value import collector2  # noqa: E402
from tools.human_value.collector2 import (  # noqa: E402
    Collector2Error,
    classify_comment,
    comment_to_observation,
    grade_candidates,
    load_human_accounts,
    load_markers,
    rejudge_baseline,
    require_channels,
)

MARKERS = [
    {"marker": "Make it so", "note": "ratification"},
    {"marker": "WORD!", "note": "ratification, case-sensitive"},
    {"marker": "do your job right", "note": "corrective"},
]


def fake_comment(cid: int, body: str, created: str = "2026-10-12T08:00:00Z") -> dict:
    return {"id": cid, "body": body, "created_at": created}


# ---------------------------------------------------------------------------
# The C2 exclusion gate
# ---------------------------------------------------------------------------


def test_c2_refused_not_just_unused():
    with pytest.raises(Collector2Error, match="excluded from the second collector"):
        require_channels(["c1", "c2"])


def test_c2_alone_refused():
    with pytest.raises(Collector2Error):
        require_channels(["c2"])


def test_unknown_channel_refused():
    with pytest.raises(Collector2Error, match="unknown channels"):
        require_channels(["c1", "c9"])


def test_empty_channels_refused():
    with pytest.raises(Collector2Error):
        require_channels([])


def test_c1_c3_allowed():
    assert require_channels(["c1", "c3"]) == ["c1", "c3"]


# ---------------------------------------------------------------------------
# Marker attribution: mechanical, case-sensitive, first-person only
# ---------------------------------------------------------------------------


def test_first_person_marker_is_direct():
    marker, authorship, kind = classify_comment("WORD! Ship it tonight.", MARKERS)
    assert (marker, authorship, kind) == ("WORD!", "direct", "stated")


def test_corrective_marker_class():
    marker, authorship, kind = classify_comment(
        "do your job right — fix the intake first.", MARKERS
    )
    assert (marker, authorship, kind) == ("do your job right", "direct", "corrected")


def test_case_sensitivity_word():
    # "word!" lowercase must NOT match the case-sensitive "WORD!" marker.
    marker, authorship, kind = classify_comment("word! nice work", MARKERS)
    assert marker is None and authorship == "uncertain"


def test_no_marker_is_uncertain_fail_closed():
    marker, authorship, kind = classify_comment(
        "Great progress tonight, team.", MARKERS
    )
    assert (marker, authorship, kind) == (None, "uncertain", None)


def test_reported_speech_is_inferred_not_direct():
    # A seat DESCRIBING his words is not his words as a speech act.
    marker, authorship, kind = classify_comment(
        "Per Shawn's durable record: he said 'do your job right' in the briefing.",
        MARKERS,
    )
    assert marker == "do your job right"
    assert authorship == "inferred"  # -> excluded from promotion, fail closed
    assert kind == "corrected"


def test_quoted_in_report_excluded():
    marker, authorship, _ = classify_comment(
        'Quoting his verbatim from memory.md: "Make it so. Word."', MARKERS
    )
    assert authorship == "inferred"


def test_colon_attribution_quote_is_reported_speech():
    # Real false positive from the 2026-10-12 live run (comment 6115195148):
    # a seat's sign-in quoting him — NOT a first-person speech act.
    body = (
        "## Sign-in — Inter-Ledger Protocol v1 (Naya 5 lane)\n\n"
        '**Mission:** Design the Inter-Ledger Protocol v1. Shawn: "Do you see it? Make it so."\n\n'
        "**Plan:** Briefing proof recorded."
    )
    marker, authorship, kind = classify_comment(body, MARKERS)
    assert marker == "Make it so"
    assert authorship == "inferred"  # quoted speech -> excluded, fail closed


def test_colon_attribution_without_quotes_is_reported():
    marker, authorship, _ = classify_comment(
        "Mission update. Shawn: Make it so, then report back.", MARKERS
    )
    assert authorship == "inferred"


def test_marker_inside_quotes_without_attribution_still_inferred():
    # Even unattributed, a quoted marker is not a first-person speech act.
    marker, authorship, _ = classify_comment(
        'The doc says "Make it so" was the key phrase.', MARKERS
    )
    assert authorship == "inferred"


def test_genuine_first_person_still_direct():
    marker, authorship, kind = classify_comment(
        "WORD! Merging tonight under delegated authority.", MARKERS
    )
    assert (marker, authorship, kind) == ("WORD!", "direct", "stated")


def test_empty_body_uncertain():
    assert classify_comment("", MARKERS)[1] == "uncertain"
    assert classify_comment(None or "", MARKERS)[1] == "uncertain"


# ---------------------------------------------------------------------------
# Observation construction
# ---------------------------------------------------------------------------


def test_observation_shape_and_channel():
    obs = comment_to_observation(
        fake_comment(123, "WORD! Go."),
        feed=2154,
        marker="WORD!",
        kind="stated",
        markers_pin="sha256:" + "aa" * 32,
        collected_at="2026-10-12T09:00:00+00:00",
    )
    assert obs["channel"] == "c1"  # never c2
    assert obs["authorship"] == "direct"
    assert obs["value_type"] == "useful_outcome"
    assert obs["value_units"] == 1
    assert obs["evidence"][0]["ref"].endswith("#issuecomment-123")
    assert obs["verbatim_hash"].startswith("sha256:")
    assert obs["observed_by"] == "collector2"


def test_corrected_observation_value_type():
    obs = comment_to_observation(
        fake_comment(124, "do your job right."),
        feed=1715,
        marker="do your job right",
        kind="corrected",
        markers_pin="sha256:" + "bb" * 32,
        collected_at="2026-10-12T09:00:00+00:00",
    )
    assert obs["value_type"] == "attention_demanded"
    assert obs["observation_kind"] == "corrected"


# ---------------------------------------------------------------------------
# Markers file + human accounts file
# ---------------------------------------------------------------------------


def test_load_markers_pins_version(tmp_path):
    p = tmp_path / "markers.json"
    p.write_text(json.dumps({"version": 3, "markers": MARKERS}))
    markers, pin = load_markers(p)
    assert len(markers) == 3
    assert pin.startswith("sha256:")


def test_empty_markers_refuses_to_scan(tmp_path):
    p = tmp_path / "markers.json"
    p.write_text(json.dumps({"version": 1, "markers": []}))
    with pytest.raises(Collector2Error, match="no markers"):
        load_markers(p)


def test_human_accounts_v1_is_empty_fail_closed():
    accounts = load_human_accounts()
    assert accounts == []  # v1: unknown handle -> C3 reports unresolvable, never guesses


# ---------------------------------------------------------------------------
# Candidate grading: collector2's evidence only
# ---------------------------------------------------------------------------


def _sweep_with(obs_list):
    return {"sweep_id": "SWEEP-TEST", "observations": obs_list}


def _obs(event_id, text):
    return {
        "event_id": event_id,
        "collector_inference": text,
        "evidence": [{"kind": "feed_comment", "ref": "https://x/issues/2154#issuecomment-1"}],
        "authorship": "direct",
    }


def test_candidate_promote_proposed_on_direct_trace():
    cands = [{"candidate_id": "CAND-1", "pr": 2188}]
    sweep = _sweep_with(
        [_obs("OBS-C2-1", "human ratified PR 2188 with WORD! #2188")]
    )
    verdicts = grade_candidates(sweep, cands)
    assert verdicts[0]["verdict"] == "promote_proposed"
    assert verdicts[0]["basis"] == ["OBS-C2-1"]


def test_candidate_remains_pending_without_evidence():
    cands = [{"candidate_id": "CAND-1", "pr": 2188}]
    sweep = _sweep_with([_obs("OBS-C2-1", "unrelated marker hit about the lane")])
    verdicts = grade_candidates(sweep, cands)
    assert verdicts[0]["verdict"] == "remains_pending"
    assert "grader's prior is not evidence" in verdicts[0]["reason"]


def test_grader_prior_alone_never_promotes():
    # Even a 9.9 grader score with no human trace -> remains pending.
    cands = [{"candidate_id": "CAND-1", "pr": 9999, "graded_units": 9.9}]
    verdicts = grade_candidates(_sweep_with([]), cands)
    assert verdicts[0]["verdict"] == "remains_pending"


# ---------------------------------------------------------------------------
# Baseline re-judgment
# ---------------------------------------------------------------------------


def test_rejudge_corrorborated_on_byte_exact_hash():
    vh = "sha256:" + "cc" * 32
    sweep = {"observations": [{"event_id": "OBS-C2-9", "verbatim_hash": vh, "authorship": "direct"}]}
    baseline = [{"event_id": "OBS-001", "verbatim_hash": vh}]
    verdicts = rejudge_baseline(sweep, baseline)
    assert verdicts[0] == {"event_id": "OBS-001", "verdict": "corroborated"}


def test_rejudge_not_observable_not_disagreement():
    sweep = {"observations": []}
    baseline = [{"event_id": "OBS-001", "verbatim_hash": "sha256:" + "dd" * 32}]
    verdicts = rejudge_baseline(sweep, baseline)
    assert verdicts[0]["verdict"] == "not_observable"
    assert "Not a disagreement" in verdicts[0]["reason"]


# ---------------------------------------------------------------------------
# Full scan: determinism + NULL sweep + C3 note (stubbed network)
# ---------------------------------------------------------------------------


def _stub_network(monkeypatch, comments_by_feed, issues=()):
    def fake_fetch(gh_api_bin, issue, since, until, per_page=100):
        return [c for c in comments_by_feed.get(issue, []) if since <= c["created_at"] <= until]

    def fake_gh(gh_api_bin, path):
        return list(issues)

    monkeypatch.setattr(collector2, "fetch_comments", fake_fetch)
    monkeypatch.setattr(collector2, "gh_api", fake_gh)


def _scan_args(tmp_path, **kw):
    ns = type("NS", (), {})()
    ns.gh_api = "/nonexistent/gh-api"
    ns.markers = str(REPO_ROOT / "tools" / "human_value" / "authorship-markers.json")
    ns.accounts = str(REPO_ROOT / "tools" / "human_value" / "human-accounts.json")
    ns.since = "2026-10-12T07:58:00Z"
    ns.until = "2026-10-12T09:00:00Z"
    ns.channels = "c1,c3"
    ns.sweep_id = "SWEEP-STUB"
    ns.as_of = "2026-10-12T09:00:00+00:00"
    ns.out = str(tmp_path / "scan.json")
    for k, v in kw.items():
        setattr(ns, k, v)
    return ns


def test_scan_deterministic_same_input_same_bytes(tmp_path, monkeypatch, capsys):
    comments = {
        2154: [fake_comment(1, "WORD! Ship it.")],
        1713: [fake_comment(2, "routine sign-in, no markers")],
        1714: [],
        1715: [fake_comment(3, "Per Shawn: he said 'do your job right' yesterday.")],
    }
    _stub_network(monkeypatch, comments)
    outs = []
    for _ in range(2):
        collector2.cmd_scan(_scan_args(tmp_path))
        outs.append(Path(tmp_path / "scan.json").read_text())
        capsys.readouterr()
    assert outs[0] == outs[1]


def test_scan_excludes_and_counts(tmp_path, monkeypatch):
    comments = {
        2154: [fake_comment(1, "WORD! Ship it.")],
        1713: [fake_comment(2, "routine sign-in, no markers")],
        1714: [],
        1715: [fake_comment(3, "Per Shawn: he said 'do your job right' yesterday.")],
    }
    _stub_network(monkeypatch, comments)
    collector2.cmd_scan(_scan_args(tmp_path))
    scan = json.loads(Path(tmp_path / "scan.json").read_text())
    assert len(scan["observations"]) == 1
    assert scan["observations"][0]["event_id"] == "OBS-C2-1"
    reasons = {e["reason"] for e in scan["excluded"]}
    assert reasons == {"no_authorship_marker", "reported_speech_marker_not_first_person"}
    assert scan["null_sweep"] is False
    assert sum(s["comments_scanned"] for s in scan["searched"] if s["channel"] == "c1") == 3


def test_null_sweep_logged_honestly(tmp_path, monkeypatch):
    _stub_network(monkeypatch, {2154: [fake_comment(1, "nothing to see")], 1713: [], 1714: [], 1715: []})
    collector2.cmd_scan(_scan_args(tmp_path))
    scan = json.loads(Path(tmp_path / "scan.json").read_text())
    assert scan["null_sweep"] is True
    assert scan["observations"] == []
    assert scan["searched"]  # the NULL log names what was searched


def test_c3_empty_allowlist_fail_closed_note(tmp_path, monkeypatch):
    _stub_network(
        monkeypatch,
        {2154: [], 1713: [], 1714: [], 1715: []},
        issues=[{"id": 7, "user": {"login": "someone"}, "title": "t", "body": "b",
                 "created_at": "2026-10-12T08:00:00Z", "html_url": "https://x/7"}],
    )
    collector2.cmd_scan(_scan_args(tmp_path))
    scan = json.loads(Path(tmp_path / "scan.json").read_text())
    assert "c3_authorship_unresolvable" in scan["c3_note"]
    assert scan["human_accounts"] == []
    assert not [o for o in scan["observations"] if o.get("channel") == "c3"]


def test_scan_refuses_c2_via_cli(tmp_path, monkeypatch, capsys):
    _stub_network(monkeypatch, {})
    # the C2 gate fires inside cmd_scan before any network use
    with pytest.raises(Collector2Error):
        collector2.cmd_scan(_scan_args(tmp_path, channels="c1,c2"))


def test_independence_block_present_in_scan(tmp_path, monkeypatch):
    _stub_network(monkeypatch, {})
    collector2.cmd_scan(_scan_args(tmp_path))
    scan = json.loads(Path(tmp_path / "scan.json").read_text())
    assert scan["independence"]["sources"] == "C1 team feeds + C3 API actions only; C2 refused by construction"
    assert scan["collector"] == "collector2"


# ---------------------------------------------------------------------------
# Agreement interpretation semantics (the 0.0-Jaccard honesty seam)
#
# A raw `pass: false` on a meaningless target reads as a defect. The
# interpretation layer below is the instrument's honest reading: when the
# evidence universes are disjoint by construction, there is no pass/fail —
# the verdict is non_overlap_by_construction.
# ---------------------------------------------------------------------------


def _not_observable_verdicts(n: int = 7) -> list[dict]:
    return [{"event_id": f"OBS-20261012-00{i}", "verdict": "not_observable"} for i in range(1, n + 1)]


def test_agreement_interpretation_disjoint_universes_not_a_failure():
    # The Window-A case Epsilon IV'd: Jaccard 0.0, all baseline verdicts
    # not_observable -> the instrument must NOT emit a pass/fail verdict.
    interp = collector2.interpret_agreement(
        {"sweep_a": 6, "sweep_b": 0, "intersection": 0, "union": 6, "jaccard": 0.0,
         "target": 0.8, "pass": False},
        _not_observable_verdicts(),
    )
    assert interp["verdict"] == "non_overlap_by_construction"
    assert interp["pass_fail_applicable"] is False


def test_agreement_interpretation_overlap_above_target_passes():
    interp = collector2.interpret_agreement(
        {"sweep_a": 5, "sweep_b": 5, "intersection": 5, "union": 5, "jaccard": 1.0,
         "target": 0.8, "pass": True},
        [{"event_id": "e1", "verdict": "corroborated"}],
    )
    assert interp["verdict"] == "agreement_pass"
    assert interp["pass_fail_applicable"] is True


def test_agreement_interpretation_overlap_below_target_needs_review():
    # Overlapping universes with real disagreement: neither a silent pass nor
    # a silent fail — a human must review before any reliance.
    interp = collector2.interpret_agreement(
        {"sweep_a": 4, "sweep_b": 4, "intersection": 1, "union": 7, "jaccard": 0.1429,
         "target": 0.8, "pass": False},
        [{"event_id": "e1", "verdict": "contradicted"}],
    )
    assert interp["verdict"] == "disagreement_review"
    assert interp["pass_fail_applicable"] is True


def test_agreement_constants_are_single_source_of_truth():
    # The reading and D32 shipped in the report come from one code constant —
    # nothing is hand-assembled into the artifact afterwards.
    assert isinstance(collector2.AGREEMENT_READING, str) and collector2.AGREEMENT_READING
    assert isinstance(collector2.AGREEMENT_D32, list) and len(collector2.AGREEMENT_D32) >= 5
    assert any("pass/fail" in line.lower() or "pass_fail" in line.lower() for line in collector2.AGREEMENT_D32)


# ---------------------------------------------------------------------------
# Pending-candidate re-probe bookkeeping (pending is a live state)
# ---------------------------------------------------------------------------


def test_candidate_pending_stamps_window_not_counter():
    # No per-run counter: a counter recomputed from a stateless registry
    # would reset every run and lie about history. The stamped window is the
    # fact; the chain of verdict artifacts across windows is the history.
    sweep = {"sweep_id": "SWEEP-C2-TEST", "observations": []}
    (verdict,) = collector2.grade_candidates(sweep, [{"candidate_id": "CAND-T", "pr": 9999}])
    assert verdict["verdict"] == "remains_pending"
    assert verdict["window_checked"] == "SWEEP-C2-TEST"
    assert "reprobe_count" not in verdict


def test_candidate_promote_proposed_stamps_window():
    sweep = {
        "sweep_id": "SWEEP-C2-TEST",
        "observations": [
            {
                "event_id": "OBS-C2-1",
                "collector_inference": "direct human trace about PR 9999",
                "evidence": [{"kind": "feed_comment", "ref": "https://x/issues/9999"}],
            }
        ],
    }
    (verdict,) = collector2.grade_candidates(sweep, [{"candidate_id": "CAND-T", "pr": 9999}])
    assert verdict["verdict"] == "promote_proposed"
    assert verdict["window_checked"] == "SWEEP-C2-TEST"


# ---------------------------------------------------------------------------
# Epsilon's IV control: framing words make a marker reported speech
# ---------------------------------------------------------------------------


def test_framing_words_per_shawn_quoting_is_inferred():
    # Epsilon's IV control set: a marker wrapped in framing words ("Per Shawn,
    # quoting his words") is reported speech -> inferred -> excluded.
    marker, authorship, _ = classify_comment(
        'Per Shawn, quoting his words from the briefing: "Make it so" is the standard.', MARKERS
    )
    assert marker == "Make it so"
    assert authorship == "inferred"


def test_trailing_dash_attribution_is_reported_speech():
    # A marker followed by a signed dash-attribution ("Make it so — Shawn")
    # is someone quoting him, not his own first-person speech act.
    # Fail-closed direction: exclusion, never fabrication.
    marker, authorship, _ = classify_comment(
        "The standard is clear: Make it so \u2014 Shawn", MARKERS
    )
    assert marker == "Make it so"
    assert authorship == "inferred"


def test_trailing_dash_without_shawn_stays_direct():
    # A dash alone is not an attribution — no overreach.
    marker, authorship, _ = classify_comment(
        "WORD! Merging tonight \u2014 delegated authority path.", MARKERS
    )
    assert marker == "WORD!"
    assert authorship == "direct"

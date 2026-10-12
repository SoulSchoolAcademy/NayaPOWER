#!/usr/bin/env python3
"""Build the known-answer calibration fixtures for the observed-experience instrument.

The verbatim quotes below are Shawn's own words as recorded in the design doc
(`hidden_files/human-value/observed-experience-instrument-v1.md`) and the
2026-10-11 window of standing context. The builder computes verbatim_hash =
sha256 of the EXACT quote string, so the battery is reproducible from these
bytes alone. Fixture raw observations are SYNTHETIC test vectors; they carry
`fixture: true` and are never ledger data.

Run: python3 tools/human_value/tests/fixtures/build_fixtures.py
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def vh(quote: str) -> str:
    return "sha256:" + hashlib.sha256(quote.encode("utf-8")).hexdigest()


# The pre-registered window: 2026-10-11 -> 2026-10-12 (Shawn's recorded reactions).
QUOTES = {
    "self_governing_law": "Make it so. Word.",
    "cold_successor_test": "Tell me when you want me to run the test, give me the list of questions.",
    "engine_consolidation": "Bring them together and put the best of them together.",
    "ib_block_owners": "Naya is locking that in for owner.",
    "boot_gate_correction": "Follow the code or don't code. I'd rather you not do anything at all than mess something up.",
    "intel_intake": "do your job right!",
}

ARTIFACTS = {
    "self_governing_law": "self-governing-law",
    "cold_successor_test": "cold-successor-test",
    "engine_consolidation": "decision-engine-consolidation",
    "ib_block_owners": "ib-block-owners",
    "boot_gate_correction": "boot-gate",
    "intel_intake": "intel-intake",
}

KINDS = {
    "self_governing_law": "stated",
    "cold_successor_test": "revealed",
    "engine_consolidation": "stated",
    "ib_block_owners": "stated",
    "boot_gate_correction": "corrected",
    "intel_intake": "stated",
}

UNIT_DESCRIPTIONS = {
    "self_governing_law": "one asserted experience of the self-governing law being ratified in his words",
    "cold_successor_test": "one observed act of the human volunteering as the test instrument",
    "engine_consolidation": "one asserted experience of the engine consolidation decision landing as he meant it",
    "ib_block_owners": "one asserted experience of the block-ownership resolution landing as he meant it",
    "boot_gate_correction": "one observed correction demanding human attention (the forged-check standard forcing rework)",
    "intel_intake": "one asserted experience of the intake law being the behavior he wanted",
}


def event_payload(name: str, event_id: str, observed_by: str = "naya-mu") -> dict:
    kind = KINDS[name]
    value_type = "attention_demanded" if kind == "corrected" else "useful_outcome"
    quote = QUOTES[name]
    return {
        "schema_version": "2",
        "event_id": event_id,
        "recorded_at": "2026-10-12",
        "value_type": value_type,
        "value_units": 1,
        "unit_description": UNIT_DESCRIPTIONS[name],
        "evidence": [
            {"kind": "content_hash", "ref": vh(quote)},
            {"kind": "receipt", "ref": "hidden_files/human-value/observed-experience-instrument-v1.md"},
        ],
        "observation_kind": kind,
        "subject": "human_self",
        "observed_by": observed_by,
        "observed_at": "2026-10-11T23:00:00Z",
        "collected_at": "2026-10-12T07:30:00Z",
        "verbatim_hash": vh(quote),
        "verbatim_quote": quote,  # fixture-only: lets a reviewer check the hash by eye
        "authorship": "direct",
        "collector_inference": f"fixture collector classification: {kind}; verbatim preserved, hash-pinned",
        "artifact": ARTIFACTS[name],
        "fixture": True,
    }


def main() -> None:
    names = list(QUOTES)

    # --- raw observations: the 6 real ones + 3 adversarial probes ---
    raw: list[dict] = [event_payload(n, f"OBS-FIX-20261012-{i + 1:03d}") for i, n in enumerate(names)]

    # Probe 1: uncertain authorship carrying a promotion attempt -> must drop.
    uncertain = event_payload("intel_intake", "OBS-FIX-20261012-901")
    uncertain["authorship"] = "uncertain"
    uncertain["verbatim_quote"] = "someone said the dashboard looks great (unattributed)"
    uncertain["verbatim_hash"] = vh(uncertain["verbatim_quote"])
    uncertain["evidence"] = [{"kind": "content_hash", "ref": uncertain["verbatim_hash"]}]
    uncertain["artifact"] = "dashboard"
    raw.append(uncertain)

    # Probe 2: assessor == collector (candidate graded_by naya-mu, observed by naya-mu) -> must drop.
    # The pr pins the mechanical match to CAND-FIX-003 so the trap actually fires.
    self_graded = event_payload("self_governing_law", "OBS-FIX-20261012-902")
    self_graded["artifact"] = "self-graded-capability"
    self_graded["pr"] = 2400
    self_graded["verbatim_quote"] = "the capability pass worked well"
    self_graded["verbatim_hash"] = vh(self_graded["verbatim_quote"])
    self_graded["evidence"] = [{"kind": "content_hash", "ref": self_graded["verbatim_hash"]}]
    raw.append(self_graded)

    # Probe 3: self-observation with inferred authorship -> schema must reject.
    self_obs = event_payload("self_governing_law", "OBS-FIX-20261012-903")
    self_obs["authorship"] = "inferred"
    self_obs["observatory_subject"] = True
    self_obs["evidence"] = [{"kind": "receipt", "ref": "tools/human_value/ledgers/observation-sweeps.jsonl"}]
    self_obs["artifact"] = "observatory"
    raw.append(self_obs)

    (HERE / "known_answer_raw.jsonl").write_text(
        "\n".join(json.dumps(o, sort_keys=True) for o in raw) + "\n", encoding="utf-8"
    )

    # --- candidates ---
    candidates = [
        {
            "schema_version": "1",
            "candidate_id": "CAND-FIX-001",
            "pr": 2455,
            "graded_value_type": "useful_outcome",
            "graded_units": 9.2,
            "graded_by": "naya-mu",
            "graded_at": "2026-10-12T06:56:00Z",
            "expires_at": "2026-11-02T06:56:00Z",
            "status": "pending",
            "note": "design worked example: the builder's 9.2 is a prior, never a measurement",
        },
        {
            "schema_version": "1",
            "candidate_id": "CAND-FIX-002",
            "capability": "cold-successor-test",
            "graded_value_type": "useful_outcome",
            "graded_units": 8.5,
            "graded_by": "naya-epsilon",
            "built_by": "naya-iota",
            "graded_at": "2026-10-11T18:00:00Z",
            "expires_at": "2026-11-01T18:00:00Z",
            "status": "pending",
            "note": "cold-successor test design: assessor(epsilon) != builder(iota)",
        },
        {
            "schema_version": "1",
            "candidate_id": "CAND-FIX-003",
            "pr": 2400,
            "graded_value_type": "useful_outcome",
            "graded_units": 7.0,
            "graded_by": "naya-mu",
            "graded_at": "2026-10-11T12:00:00Z",
            "expires_at": "2026-11-01T12:00:00Z",
            "status": "pending",
            "note": "trap: assessor == the calibration collector; must fail closed",
        },
        {
            "schema_version": "1",
            "candidate_id": "CAND-FIX-004",
            "graded_value_type": "useful_outcome",
            "graded_units": 6.0,
            "graded_by": "naya-beta",
            "graded_at": "2026-09-01T00:00:00Z",
            "expires_at": "2026-09-22T00:00:00Z",
            "status": "pending",
            "note": "stale: expired 2026-09-22; the expire command must mark it unobserved",
        },
    ]
    (HERE / "known_answer_candidates.jsonl").write_text(
        "\n".join(json.dumps(c, sort_keys=True) for c in candidates) + "\n", encoding="utf-8"
    )

    # --- the pre-registered answer key (pinned BEFORE the instrument runs) ---
    # Note: the cold-successor-test observation matches CAND-FIX-002 by
    # capability (most recent pending useful_outcome candidate); the rest are
    # standalone (promotion null) — an observation never needs a candidate.
    key = {
        "key_id": "OBS-CAL-KEY-20261012",
        "window_start": "2026-10-11T00:00:00Z",
        "window_end": "2026-10-12T07:30:00Z",
        "expected_triples": [
            [vh(QUOTES[n]), KINDS[n], ARTIFACTS[n]] for n in names
        ],
        "expected_dropped": 3,
        "note": "Exact keyed set of 6 STATED/REVEALED/CORRECTED events, zero phantoms. "
        "Probes 901/902/903 must be dropped (uncertain authorship, assessor==collector, "
        "self-observation). No peeking: this key is hashed and pinned before the run.",
    }
    (HERE / "known_answer_key.json").write_text(json.dumps(key, indent=2) + "\n", encoding="utf-8")

    # --- sweep B: an independent second pass over the same window ---
    # Authored as a fresh pass (different collector seat, slightly different
    # artifact naming is NOT allowed to drift — agreement measures whether two
    # honest passes land on the same triples).
    sweep_b = [event_payload(n, f"OBS-B-20261012-{i + 1:03d}", observed_by="naya-epsilon") for i, n in enumerate(names)]
    (HERE / "sweep_b.jsonl").write_text(
        "\n".join(json.dumps(o, sort_keys=True) for o in sweep_b) + "\n", encoding="utf-8"
    )

    print("fixtures written to", HERE)


if __name__ == "__main__":
    main()

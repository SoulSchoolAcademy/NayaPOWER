"""B-47 proof gate (pytest): Smart Connect / open doors mechanism.

Cases (mirrors the reference mechanism's guarantees):
  POSITIVE  — synth-guest-001 connects (door: sdk), contributes a lesson; one cycle
              must merge it with the seed corpus and record compound(s) citing it.
  NEGATIVE  — synth-guest-002 connects and contributes nothing; after the cycle,
              NO compound may cite it and its compound_count must be 0
              (G3: a number without proof is a lie).
  POLARITY  — the same lesson submitted twice must not double-compound
              (content-addressed dedupe -> exactly one lesson, no second compound).
  FAIL-CLOSED — corrupted state (MERGED lesson without canonical_id) is flagged
              in cycle.flags; the cycle completes; no fake compound is recorded.

Fail-closed: any assertion failure -> pytest non-zero exit.
"""
import tempfile

import pytest

from tools.smart_connect import OpenDoors


@pytest.fixture
def hub():
    h = OpenDoors(tempfile.mkdtemp())
    h.register_door("sdk", "SDK", "python-sdk")
    h.register_door("agent2agent", "agent-to-agent", "a2a")
    return h


def _seed_corpus(hub):
    corpus = hub.register_connection("synth-corpus", "sdk")
    return hub.append_lesson(
        corpus["connection_id"],
        "Lessons compound when duplicates are merged into a single living note.",
        "sdk")


# ---------------- POSITIVE ----------------
def test_g1_open_doors(hub):
    c1 = hub.register_connection("synth-guest-001", "sdk")
    assert c1["door_id"] == "sdk" and c1["connection_id"].startswith("conn-")
    # Closed chosen door reroutes to an open door, never refuses.
    hub.close_door("sdk", "test closure")
    c2 = hub.register_connection("synth-guest-002", "sdk")
    assert c2["door_id"] == "agent2agent"


def test_g2_instant_capture(hub):
    _seed_corpus(hub)
    c1 = hub.register_connection("synth-guest-001", "sdk")
    les = hub.append_lesson(c1["connection_id"],
                            "When duplicates merge into a single living note, lessons compound.",
                            "sdk")
    assert les["status"] == "INTAKE" and les["lesson_id"].startswith("les-")


def test_g3_compound_recorded(hub):
    _seed_corpus(hub)
    c1 = hub.register_connection("synth-guest-001", "sdk")
    les = hub.append_lesson(c1["connection_id"],
                            "When duplicates merge into a single living note, lessons compound.",
                            "sdk")
    cycle = hub.run_cycle()
    assert cycle["cycle_id"] == "cyc-001" and cycle["intake_processed"] >= 2
    cited = [c for c in hub.compounds.values() if les["lesson_id"] in c["lesson_ids"]]
    assert len(cited) >= 1, "no compound cites the contributed lesson"
    assert all(c["cycle"] == cycle["cycle_id"] for c in cited)
    assert hub.lessons[les["lesson_id"]]["status"] in ("MERGED", "ELEVATED")


def test_g4_visible_in_one_cycle(hub):
    _seed_corpus(hub)
    c1 = hub.register_connection("synth-guest-001", "sdk")
    hub.append_lesson(c1["connection_id"],
                      "When duplicates merge into a single living note, lessons compound.",
                      "sdk")
    hub.run_cycle()
    fb = hub.feedback_for(c1["connection_id"])
    assert fb["compound_count"] >= 1 and len(fb["compounds"]) == len(set(fb["compounds"]))
    assert fb["cycles_run"] == 1 and len(fb["lessons"]) == 1


# ---------------- NEGATIVE ----------------
def test_g3_negative_no_free_compound(hub):
    _seed_corpus(hub)
    c1 = hub.register_connection("synth-guest-001", "sdk")
    hub.append_lesson(c1["connection_id"],
                      "When duplicates merge into a single living note, lessons compound.",
                      "sdk")
    hub.run_cycle()
    c2 = hub.register_connection("synth-guest-002", "agent2agent")
    hub.run_cycle()  # same cycle machinery, zero contributions from c2
    fb2 = hub.feedback_for(c2["connection_id"])
    my_lesson_ids = {l["lesson_id"] for l in hub.lessons.values()
                     if l["connection_id"] == c2["connection_id"]}
    leak = [c["compound_id"] for c in hub.compounds.values()
            if any(lid in my_lesson_ids for lid in c["lesson_ids"])]
    assert fb2["compound_count"] == 0 and fb2["compounds"] == [] and leak == []


# ---------------- POLARITY ----------------
def test_polarity_dedupe_no_double_compound(hub):
    _seed_corpus(hub)
    c3 = hub.register_connection("synth-guest-003", "sdk")
    text = "Open doors compound: every new connection teaches the hive something new."
    d1 = hub.append_lesson(c3["connection_id"], text, "sdk")
    d2 = hub.append_lesson(c3["connection_id"], text, "sdk")  # identical re-submission
    assert d1["lesson_id"] == d2["lesson_id"], "content-addressed dedupe broken"
    assert d2.get("duplicate") is True, "re-submission not marked duplicate"
    before = len(hub.compounds)
    hub.run_cycle()
    assert len(hub.compounds) == before, "duplicate submission compounded"
    fb3 = hub.feedback_for(c3["connection_id"])
    assert fb3["compound_count"] == 0
    assert len([l for l in hub.lessons.values() if l["lesson_id"] == d1["lesson_id"]]) == 1


def test_polarity_lesson_survives(hub):
    _seed_corpus(hub)
    c3 = hub.register_connection("synth-guest-003", "sdk")
    d1 = hub.append_lesson(c3["connection_id"],
                           "Open doors compound: every new connection teaches the hive something new.",
                           "sdk")
    hub.run_cycle()
    assert hub.lessons[d1["lesson_id"]]["status"] == "INTAKE", \
        "unmerged lone lesson was faked MERGED"


# ---------------- FAIL-CLOSED ----------------
def test_fail_closed_corrupted_merge(hub):
    _seed_corpus(hub)
    c = hub.register_connection("synth-x", "sdk")
    les = hub.append_lesson(c["connection_id"], "some lesson text for merge testing", "sdk")
    les["status"] = "MERGED"
    les.pop("canonical_id", None)  # corrupted state: MERGED without canonical_id
    cycle = hub.run_cycle()  # must not raise
    assert any(f["kind"] == "missing_canonical_id" and f["lesson_id"] == les["lesson_id"]
               for f in cycle["flags"]), "corrupted lesson not flagged"
    assert not any(les["lesson_id"] in c_["lesson_ids"] for c_ in hub.compounds.values()), \
        "fake compound recorded for corrupted lesson"


def test_fail_closed_unknown_connection(hub):
    with pytest.raises(ValueError):
        hub.append_lesson("conn-nope", "text", "sdk")
    with pytest.raises(ValueError):
        hub.feedback_for("conn-nope")

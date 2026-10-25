#!/usr/bin/env python3
"""Intake Bridge tests (B1). Run: python3 test_intake_bridge.py (stdlib only).

The key tests PARSE THE LIVE FILES — HUB/app/js/naya-intake.js for the keys
the walk actually writes, welcome_engine.SLOTS for the keys the spine
expects — so the mapping is pinned against reality, not against a copy of
either side typed into this file. If either side changes its keys, these
tests turn red and name the change.
"""
import json, os, re

import intake_bridge as b
import welcome_engine as w
from smart_match import FIELDS, rank_matches, score

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
JS_PATH = os.path.join(REPO, "HUB", "app", "js", "naya-intake.js")


def _js_source():
    with open(JS_PATH, encoding="utf-8") as fh:
        return fh.read()


def js_step_keys():
    """Step keys from the FLOWS literals — every `key: '...'` in the file
    is a step definition (the emit code uses step_key, never key)."""
    return set(re.findall(r"key: '([a-z_]+)'", _js_source()))


def js_finished_payload_keys():
    """Keys of the object joinRecord() returns — the ONLY answers payload
    that ever rides an intake_events row (the 'finished' event's summary)."""
    src = _js_source()
    seg = src[src.index("function joinRecord"):src.index("Completion measurement")]
    block = re.search(r"return \{(.*?)\};", seg, re.S).group(1)
    return set(re.findall(r"^\s*([a-z_]+):", block, re.M))


def js_intent_values():
    src = _js_source()
    seg = src[src.index("var INTENT_CHOICES"):src.index("];", src.index("var INTENT_CHOICES"))]
    return set(re.findall(r"value: '([a-z_]+)'", seg))


# ── The key proof ─────────────────────────────────────────────────────

def test_js_keys_extracted_from_live_file():
    # Pins the live walk's current shape; a Nitro-side key change must
    # turn this red loudly rather than drift silently.
    assert js_step_keys() == {"name", "email", "intent", "note"}
    assert js_finished_payload_keys() == {
        "flow", "owner_alias", "invitee_email_hash", "display_name", "intent", "note"}


def test_every_js_key_has_exactly_one_home():
    js_keys = js_step_keys() | js_finished_payload_keys()
    homes = {}
    for key in js_keys:
        found = [name for name, table in
                 (("SLOTS", w.SLOTS), ("TRANSLATION", b.KEY_TRANSLATION),
                  ("CLASSIFICATION", b.KEY_CLASSIFICATION)) if key in table]
        assert len(found) == 1, f"{key}: homes={found} (want exactly one)"
        homes[key] = found[0]
    # The divergence, named: the door's two signal keys land by translation,
    # its identity/contact keys are classified out, NONE passes through —
    # the JS walk and SLOTS share zero answer keys today.
    assert homes["note"] == "TRANSLATION" and homes["intent"] == "TRANSLATION"
    assert not (js_keys & set(w.SLOTS)), "JS/SLOTS key overlap appeared — revisit the bridge verdict"


def test_slots_and_bridge_tables_are_disjoint():
    assert not (set(w.SLOTS) & set(b.KEY_TRANSLATION))
    assert not (set(w.SLOTS) & set(b.KEY_CLASSIFICATION))
    assert not (set(b.KEY_TRANSLATION) & set(b.KEY_CLASSIFICATION))
    for target in b.KEY_TRANSLATION.values():
        assert target in w.SLOTS  # every translation lands on a real SLOTS key


def test_every_vector_field_is_reachable():
    slots_fields = {d["vector"] for _, d in w.SLOTS.values() if "vector" in d}
    assert slots_fields == set(FIELDS)  # the spine alone covers all five
    door_fields = {w.SLOTS[b.KEY_TRANSLATION[k]][1]["vector"] for k in b.KEY_TRANSLATION}
    # The named gap: the live door walk alone can only feed topics + goals.
    # offers / needs / wants arrive only via Questions-V2 keys (passthrough)
    # until the walk asks those questions — B2/N1 territory, pinned here.
    assert door_fields == {"topics", "goals"}


def test_intent_choices_carry_verbatim():
    for value in js_intent_values():
        out = b.translate_answers({"intent": value}, b._new_diag())
        assert out == {"goal_personal": value}  # the citizen's own word, unedited


# ── The fold ──────────────────────────────────────────────────────────

def _finished(alias, answers, ts, flow="welcome"):
    return {"session_id": "s-" + ts, "flow": flow, "event": "finished",
            "step_key": None, "step_index": 4, "owner_alias": alias,
            "via": "tap", "answers": answers, "created_at": ts}


def test_fold_latest_answer_wins():
    rows = [
        _finished("maya", {"into": "gardening", "matters": "clean water"}, "2026-10-25T01:00:00Z"),
        _finished("maya", {"into": "urban gardening, composting"}, "2026-10-25T02:00:00Z"),
    ]
    folded, _ = b.fold_answers(rows)
    assert folded["maya"]["into"] == "urban gardening, composting"  # later event overrides
    assert folded["maya"]["matters"] == "clean water"  # untouched keys survive the re-walk


def test_fold_orders_by_created_at_not_input_order():
    rows = [
        _finished("maya", {"into": "new answer"}, "2026-10-25T02:00:00Z"),
        _finished("maya", {"into": "old answer"}, "2026-10-25T01:00:00Z"),
    ]
    folded, _ = b.fold_answers(rows)
    assert folded["maya"]["into"] == "new answer"


def test_fold_door_payload_translates_and_classifies():
    payload = {"flow": "welcome", "owner_alias": "door-kid",
               "invitee_email_hash": "a" * 64, "display_name": "Kid",
               "intent": "build", "note": "I love gardening and composting"}
    folded, diag = b.fold_answers([_finished("door-kid", payload, "2026-10-25T01:00:00Z")])
    assert folded["door-kid"] == {"into": "I love gardening and composting",
                                  "goal_personal": "build"}
    pub = b._public_diag(diag)
    assert pub["translated_keys"] == ["intent", "note"]
    assert pub["classified_keys"] == {"display_name": "identity", "flow": "metadata",
                                      "invitee_email_hash": "contact", "owner_alias": "metadata"}
    assert pub["unmapped_keys"] == []


def test_unknown_key_is_named_never_dropped_silently():
    rows = [_finished("maya", {"into": "gardening", "favorite_color": "blue"},
                      "2026-10-25T01:00:00Z")]
    vectors, diag = b.vectors_from_intake(rows)
    assert diag["unmapped_keys"] == ["favorite_color"]
    assert "gardening" in vectors["maya"]["topics"]  # the known signal still lands


def test_invite_accept_rows_are_not_folded_into_the_inviter():
    rows = [_finished("inviter", {"intent": "team", "note": "gardening"},
                      "2026-10-25T01:00:00Z", flow="invite_accept")]
    vectors, diag = b.vectors_from_intake(rows)
    assert vectors == {} and diag["rows_excluded_flow"] == 1


def test_step_events_without_answers_fold_nothing():
    rows = [{"session_id": "s1", "flow": "welcome", "event": "step_completed",
             "step_key": "intent", "step_index": 2, "owner_alias": "maya",
             "via": "tap", "answers": None, "created_at": "2026-10-25T01:00:00Z"},
            {"session_id": "s1", "flow": "welcome", "event": "started",
             "step_key": "name", "step_index": 0, "owner_alias": "maya",
             "via": None, "answers": None, "created_at": "2026-10-25T00:59:00Z"}]
    vectors, diag = b.vectors_from_intake(rows)
    assert vectors == {} and diag["rows_without_answers"] == 2


# ── Degradation ───────────────────────────────────────────────────────

def test_malformed_rows_degrade_never_crash():
    rows = [None, "junk", 42, {}, {"owner_alias": 42},
            {"owner_alias": "   "},
            {"owner_alias": "x", "answers": "not-a-dict"},
            {"owner_alias": "x", "answers": {"into": 123, "needs": ["a", "list"]}},
            _finished("ok", {"into": "gardening"}, "2026-10-25T01:00:00Z")]
    vectors, diag = b.vectors_from_intake(rows)
    assert list(vectors) == ["ok"]  # one good citizen survives the junk around her
    assert diag["rows_malformed"] >= 4 and diag["rows_no_alias"] >= 2
    assert diag["malformed_values"] == 2


def test_empty_intake_gives_no_vectors():
    vectors, diag = b.vectors_from_intake([])
    assert vectors == {} and diag["rows_seen"] == 0 and diag["citizens_seen"] == 0
    vectors, _ = b.vectors_from_intake(None)
    assert vectors == {}


def test_citizen_with_no_usable_answers_is_skipped_and_counted():
    rows = [_finished("page-only", {"motto": "Be kind.", "links": ["https://x.example"]},
                      "2026-10-25T01:00:00Z"),
            _finished("blank", {"into": "a"}, "2026-10-25T01:00:00Z")]
    vectors, diag = b.vectors_from_intake(rows)
    assert vectors == {} and diag["citizens_skipped_no_signal"] == 2


def test_vectors_are_alias_keyed_and_five_fields_only():
    rows = [_finished("maya", {"into": "gardening", "email": "maya@example.com",
                                "invitee_email_hash": "b" * 64}, "2026-10-25T01:00:00Z")]
    vectors, _ = b.vectors_from_intake(rows)
    assert set(vectors) == {"maya"}
    assert set(vectors["maya"].keys()) == set(FIELDS)  # no email/hash/name leaks into a vector


def test_deterministic():
    rows = [_finished("maya", {"into": "gardening, composting", "intent": "team"},
                      "2026-10-25T01:00:00Z"),
            _finished("rex", {"note": "I love robotics"}, "2026-10-25T01:05:00Z")]
    r1 = json.dumps(b.vectors_from_intake(rows), sort_keys=True)
    r2 = json.dumps(b.vectors_from_intake(list(reversed(rows))), sort_keys=True)
    assert r1 == r2


# ── End to end ────────────────────────────────────────────────────────

E2E_ROWS = [
    _finished("maya-rivers",
              {"into": "urban gardening, composting, teaching kids to grow food",
               "matters": "healthy neighborhoods",
               "offers": "garden design, compost workshops",
               "needs": "accounting help",
               "wants": "school principals, parents"},
              "2026-10-25T01:00:00Z"),
    _finished("green-thumbs",
              {"into": "community gardens, gardening, teaching",
               "offers": "gardening workshops",
               "needs": "garden design"},
              "2026-10-25T01:01:00Z"),
    _finished("lone-diver",
              {"into": "underwater basket weaving",
               "offers": "scuba lessons"},
              "2026-10-25T01:02:00Z"),
]


def test_end_to_end_intake_to_ranked_matches():
    vectors, diag = b.vectors_from_intake(E2E_ROWS)
    assert set(vectors) == {"maya-rivers", "green-thumbs", "lone-diver"}
    assert diag["citizens_with_vectors"] == 3
    matches = rank_matches(vectors["maya-rivers"],
                           {k: v for k, v in vectors.items()},
                           self_name="maya-rivers")
    assert [m["name"] for m in matches] == ["green-thumbs"]  # the diver surfaces for no one
    top = matches[0]
    assert top["score"] > 0 and top["surface"] and top["reasons"]
    assert any("offer/need fit" in r for r in top["reasons"])  # her design <-> their need
    assert score(vectors["maya-rivers"], vectors["lone-diver"])["surface"] is False


def test_end_to_end_door_shape_citizen_matches_on_translated_signal():
    rows = [_finished("door-kid",
                      {"flow": "welcome", "owner_alias": "door-kid",
                       "invitee_email_hash": "c" * 64, "display_name": "Kid",
                       "intent": "build", "note": "I love gardening and composting"},
                      "2026-10-25T01:00:00Z"),
            _finished("maya-rivers",
                      {"into": "urban gardening, composting",
                       "goal_personal": "build a gardening app for our block"},
                      "2026-10-25T01:01:00Z")]
    vectors, _ = b.vectors_from_intake(rows)
    kid = vectors["door-kid"]
    assert "gardening" in kid["topics"] and "composting" in kid["topics"]  # note -> into, lead-in stripped
    assert kid["goals"] == ["build"]  # intent carried verbatim
    s = score(kid, vectors["maya-rivers"])
    assert s["parts"]["topics"] > 0 and any(r.startswith("shared:") for r in s["reasons"])


if __name__ == "__main__":
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for fn in fns:
        fn(); print("PASS", fn.__name__)
    print(f"{len(fns)}/{len(fns)} tests passed")

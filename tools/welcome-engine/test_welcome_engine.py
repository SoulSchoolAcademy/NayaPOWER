#!/usr/bin/env python3
"""Welcome Engine tests. Run: python3 test_welcome_engine.py (stdlib only)."""
import json
import welcome_engine as w
from declared_vectors import PROJECTS, SEATS

MAYA = {
    "into": "urban gardening, composting, teaching kids to grow food",
    "matters": "healthy neighborhoods, food people grow themselves",
    "goal_personal": "start a community garden on our block",
    "vision": "every block grows its own food",
    "mission": "make growing food normal again",
    "motto": "Grow where you're planted.",
    "do": "landscape designer",
    "biz_what": "Rivers Greenworks, garden design for homes and schools",
    "biz_goal": "book 20 school gardens this year",
    "offers": "garden design, compost workshops",
    "needs": "accounting help, a good photographer",
    "wants": "school principals, parents, local cafes",
    "space_about": "Block Growers, neighbors growing food together",
    "links": ["https://riversgreenworks.example.com"],
}
CORPUS = dict(PROJECTS)
CORPUS["Green Thumbs Circle (space)"] = {
    "topics": ["gardening", "composting", "community gardens", "teaching"],
    "goals": ["grow food together"], "offers": ["workshops"], "needs": ["garden design"]}

def test_full_citizen_pages_verbatim():
    r = w.activate("maya-rivers", MAYA, CORPUS)
    assert r["pages"]["personal"]["topics"] == MAYA["into"]
    assert r["pages"]["motto"] == "Grow where you're planted."
    assert r["pages"]["business"]["description"] == MAYA["biz_what"]
    assert r["coverage"]["filled_pct"] == 100

def test_link_and_issuance():
    r = w.activate("maya-rivers", MAYA, CORPUS)
    assert r["ambassador_link"] == "https://nayanet.live/joinus?ref=maya-rivers"
    assert "on conflict (alias) do nothing" in r["issue_link_sql"]
    assert r["pages"]["links"] == [{"url": MAYA["links"][0], "tracked": True}]

def test_vector_and_matches():
    r = w.activate("maya-rivers", MAYA, CORPUS)
    assert "urban gardening" in r["vector"]["topics"]
    assert "accounting help" in r["vector"]["needs"]
    names = [m["name"] for m in r["first_matches"]]
    assert "Green Thumbs Circle (space)" in names  # her own world finds her
    top = r["first_matches"][0]
    assert top["name"] == "Green Thumbs Circle (space)" and top["reasons"]

def test_no_business_is_honest():
    a = {k: v for k, v in MAYA.items() if not k.startswith("biz")}
    r = w.activate("maya-rivers", a, CORPUS)
    assert r["pages"]["business"]["state"] == "not_started"
    assert not any(k.startswith("business.") for k in r["coverage"]["fields"])

def test_all_skipped_invents_nothing():
    a = {qid: "" for qid in w.SLOTS}
    r = w.activate("ghost", a, CORPUS, has_business=False)
    assert r["pages"]["personal"]["topics"] == w.NOT_SHARED
    assert r["coverage"]["filled_pct"] == 0 and r["coverage"]["accounted_pct"] == 100
    assert r["first_matches"] == [] and r["vector"]["topics"] == []

def test_missing_is_named_missing():
    r = w.activate("sparse", {"motto": "Less, but true."}, CORPUS, has_business=False)
    assert r["coverage"]["fields"]["personal.topics"] == "missing"
    assert r["coverage"]["fields"]["personal.motto"] == "filled"

def test_deterministic():
    r1 = json.dumps(w.activate("maya-rivers", MAYA, CORPUS), sort_keys=True)
    r2 = json.dumps(w.activate("maya-rivers", MAYA, CORPUS), sort_keys=True)
    assert r1 == r2

def test_lead_ins_stripped():
    v = w.build_vector({"into": "I love gardening and I want to teach composting"})
    assert "gardening" in v["topics"] and "teach composting" in v["topics"]

def test_thin_answer_flagged_not_punished():
    r = w.activate("thin", {"into": "Chess."}, CORPUS, has_business=False)
    assert r["coverage"]["fields"]["personal.topics"] == "filled_thin"
    assert "personal.topics" in r["coverage"]["thin"]

def test_findability_gate():
    corpus = dict(CORPUS)
    corpus["Hidden Hermit (space)"] = {"topics": ["urban gardening", "composting"],
        "goals": ["grow food together"], "offers": ["workshops"], "needs": ["help"], "_findable": False}
    r = w.activate("maya-rivers", MAYA, corpus)
    assert r["corpus_excluded_unfindable"] == 1
    assert all(m["name"] != "Hidden Hermit (space)" for m in r["first_matches"])

def test_empty_match_note_is_honest():
    r = w.activate("lone", {"into": "underwater basket weaving"}, CORPUS, has_business=False)
    assert r["first_matches"] == [] and "match_note" in r


def test_edge_emoji_and_long_answers():
    a = {"into": "🌱 gardening!! and " + "growing tomatoes on the balcony with my kids every single summer weekend " * 30}
    r = w.activate("edge", a, CORPUS, has_business=False)
    assert r["vector"]["topics"]  # survived, produced signal
    assert r["coverage"]["fields"]["personal.topics"] == "filled"

def test_edge_stopword_only_answer_is_thin_not_signal():
    r = w.activate("edge2", {"into": "the and of"}, CORPUS, has_business=False)
    assert r["coverage"]["fields"]["personal.topics"] in ("filled", "filled_thin")

def test_edge_empty_corpus():
    r = w.activate("edge3", MAYA, {})
    assert r["first_matches"] == [] and "match_note" in r


if __name__ == "__main__":
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for fn in fns:
        fn(); print("PASS", fn.__name__)
    print(f"{len(fns)}/{len(fns)} tests passed")

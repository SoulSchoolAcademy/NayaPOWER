"""Tests for the Naya Constitution decision gate (tools/naya-constitution/check.py).

Run: python3 -m pytest tools/naya-constitution/test_check.py
or:  python3 tools/naya-constitution/test_check.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from check import decide  # noqa: E402


def base(**over):
    action = {
        "action": "restore the PI face route",
        "objective": "the team's working home is reachable at /pi",
        "scope_complete": True,
        "elements": ["hub home", "pi face", "repo deployer", "lane deployer"],
        "options": [
            {"name": "re-assert repo deploy now",
             "scores": {"value": 9, "intelligence": 8, "collective": 8, "reversibility": 10}},
            {"name": "wait for the permanent fix",
             "scores": {"value": 3, "intelligence": 5, "collective": 4, "reversibility": 9}},
        ],
        "human_gate": None,
        "seeks_director_approval": False,
    }
    action.update(over)
    return action


def test_highest_total_proceeds():
    v = decide(base())
    assert v["verdict"] == "PROCEED" and v["chosen"] == "re-assert repo deploy now", v


def test_gate_routes_to_director():
    v = decide(base(human_gate="production_db"))
    assert v["verdict"] == "GATE" and "packet" in v["reason"], v


def test_tap_inflation_stops():
    v = decide(base(seeks_director_approval=True))
    assert v["verdict"] == "STOP" and "tap-inflation" in v["reason"], v


def test_incomplete_scope_stops():
    v = decide(base(scope_complete=False))
    assert v["verdict"] == "STOP" and "full scope" in v["reason"], v


def test_unscored_option_stops():
    bad = base()
    del bad["options"][1]["scores"]["collective"]
    v = decide(bad)
    assert v["verdict"] == "STOP" and "unscored" in v["reason"], v


def test_no_options_stops():
    v = decide(base(options=[]))
    assert v["verdict"] == "STOP" and "no options" in v["reason"], v


def test_tie_breaks_toward_reversibility():
    opts = [
        {"name": "bold", "scores": {"value": 8, "intelligence": 8, "collective": 8, "reversibility": 4}},
        {"name": "safe", "scores": {"value": 8, "intelligence": 8, "collective": 8, "reversibility": 9}},
    ]
    # totals differ by 0.15 * 5 = 0.75 -> not a tie on totals; make a true tie instead:
    opts[1]["scores"]["value"] = 5  # safe total: 1.25+2.4+2.4+1.35 = 7.40 vs bold 2+2.4+2.4+0.6 = 7.40
    v = decide(base(options=opts))
    assert v["verdict"] == "PROCEED" and v["chosen"] == "safe", v


def test_unknown_gate_stops():
    v = decide(base(human_gate="vibes"))
    assert v["verdict"] == "STOP" and "exhaustive" in v["reason"], v


if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for t in tests:
        t()
        print("PASS", t.__name__)
    print(f"{len(tests)}/{len(tests)} passed")

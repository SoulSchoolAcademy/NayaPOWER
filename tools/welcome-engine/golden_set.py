#!/usr/bin/env python3
"""The Golden Set — labeled match expectations the engine must satisfy.
Expectations come from the record (Trinity roles, project purposes) and
from synthetic citizens whose right answers are obvious to a human reader.
If the matcher disagrees with a label, either the math or the label is
wrong — and the disagreement gets investigated, never averaged away.
Run: python3 golden_set.py"""
import sys
from smart_match import score, rank_matches
from declared_vectors import SEATS, PROJECTS
import welcome_engine as w

GARDEN_SPACE = {"topics": ["gardening", "composting", "community gardens", "teaching"],
                "goals": ["grow food together"], "offers": ["workshops"], "needs": ["garden design"]}
CHESS_SPACE = {"topics": ["chess", "strategy games", "tournaments"],
               "goals": ["play better chess"], "offers": ["coaching"], "needs": ["players"]}
MAYA = {"topics": ["urban gardening", "composting", "teaching kids to grow food", "block growers", "schools"],
        "goals": ["start a community garden on our block", "every block grows its own food"],
        "offers": ["garden design", "compost workshops"], "needs": ["accounting help"],
        "wants": ["school principals", "parents"]}
TOM = {"topics": ["chess", "long walks"], "goals": [], "offers": [], "needs": [], "wants": ["chess partners"]}

# (label, a, b, expect_surface)
PAIRS = [
    ("Nitro is Team Nitro's own", SEATS["nitro (Naya N Narzan, Nitro/Executor/Verifier)"], PROJECTS["Team Nitro (space-team-nitro)"], True),
    ("Power is the mothership's integrator", SEATS["naya-power (Naya P Narzan, Builder/Integrator)"], PROJECTS["NayaPOWER (space-nayapower)"], True),
    ("Resolve hears the Mirror (THINKING)", SEATS["resolve (Naya R Narzan, Resolver)"], PROJECTS["The Mirror Program (space-mirror)"], None),  # informational in v1.3: one signal
    ("Power and Nitro are complementary", SEATS["naya-power (Naya P Narzan, Builder/Integrator)"], SEATS["nitro (Naya N Narzan, Nitro/Executor/Verifier)"], True),
    ("Resolve does not belong in Voice", SEATS["resolve (Naya R Narzan, Resolver)"], PROJECTS["Voice (space-voice)"], False),
    ("Nitro does not belong in Smart Mail", SEATS["nitro (Naya N Narzan, Nitro/Executor/Verifier)"], PROJECTS["Smart Mail (space-smart-mail)"], False),
    ("Maya finds the gardeners", MAYA, GARDEN_SPACE, True),
    ("Maya is not a Voice citizen", MAYA, PROJECTS["Voice (space-voice)"], False),
    ("Tom finds the chess players", TOM, CHESS_SPACE, True),
    ("Tom is not a Factory citizen", TOM, PROJECTS["The Smart Factory (space-smart-factory)"], False),
]
# top-1 expectations: (label, entity, corpus, expected_name)
TOP1 = [
    ("Nitro's top project is Team Nitro", SEATS["nitro (Naya N Narzan, Nitro/Executor/Verifier)"], PROJECTS, "Team Nitro (space-team-nitro)"),
    ("Power's top project is NayaPOWER", SEATS["naya-power (Naya P Narzan, Builder/Integrator)"], PROJECTS, "NayaPOWER (space-nayapower)"),
    ("Maya's top is the garden space", MAYA, {**PROJECTS, "Green Thumbs Circle (space)": GARDEN_SPACE}, "Green Thumbs Circle (space)"),
]

if __name__ == "__main__":
    passed = failed = 0
    for label, a, b, expect in PAIRS:
        r = score(a, b)
        if expect is None:
            print(f"  INFO  {label}: {r['score']}% signals={r['signals']}")
        elif r["surface"] == expect:
            passed += 1; print(f"  PASS  {label}: {r['score']}%")
        else:
            failed += 1; print(f"  FAIL  {label}: got surface={r['surface']} ({r['score']}%), expected {expect}")
    for label, e, corpus, name in TOP1:
        rows = rank_matches(e, corpus)
        if rows and rows[0]["name"] == name:
            passed += 1; print(f"  PASS  {label}: {rows[0]['score']}%")
        else:
            failed += 1; print(f"  FAIL  {label}: top={rows[0]['name'] if rows else None}")
    print(f"GOLDEN SET: {passed} passed, {failed} failed")
    sys.exit(1 if failed else 0)

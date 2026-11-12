#!/usr/bin/env python3
"""The Holdout Set — 20 NEW labeled cases, hand-written for the v1.5
hardening run (2026-10-24), NOT derived from the declared population.
Clear matches, clear non-matches, and borderline cases where the
2-signal bar itself is the expectation. Labeled honestly: this is a
SYNTHETIC holdout — it probes generalization beyond the population the
golden set was drawn from; it is not citizen data.
Run: python3 holdout_set.py"""
import sys
from smart_match import score, rank_matches

V = lambda **kw: kw

BAKER = V(topics=["sourdough baking", "pastry", "bread"], goals=["feed the neighborhood"],
          offers=["fresh bread daily", "baking classes"], needs=["flour suppliers"], wants=["cafe owners"])
CAFE = V(topics=["coffee", "brunch", "fresh bread"], goals=["feed the neighborhood"],
         offers=["cafe space"], needs=["fresh bread daily", "pastry"], wants=["local bakers"])
SWIM_COACH = V(topics=["swim coaching", "open water swimming", "stroke technique"], goals=[],
               offers=["swim lessons", "video stroke analysis"], needs=["pool time"], wants=["triathletes"])
TRI_CLUB = V(topics=["triathlon", "open water swimming", "cycling", "running"], goals=["race together"],
             offers=["group training"], needs=["swim coaching", "pool time"], wants=["athletes"])
BEEKEEPER = V(topics=["beekeeping", "honey", "pollination"], goals=[],
              offers=["hives for pollination", "raw honey"], needs=["orchard partners"], wants=["farmers"])
ORCHARD = V(topics=["apple orchards", "cider", "pollination"], goals=["bigger harvests"],
            offers=["orchard space"], needs=["bees for pollination", "hives"], wants=["beekeepers"])
TUTOR = V(topics=["math tutoring", "algebra", "geometry"], goals=[],
          offers=["tutoring sessions"], needs=["students"], wants=["parents"])
COOP = V(topics=["homeschooling", "math", "science"], goals=["kids love learning"],
         offers=["group classes"], needs=["math tutoring", "algebra help"], wants=["tutors"])
PHOTOG = V(topics=["wedding photography", "portraits"], goals=[],
           offers=["photo packages"], needs=["venues"], wants=["engaged couples", "wedding planners"])
VENUE = V(topics=["weddings", "events", "gardens"], goals=[],
          offers=["event space"], needs=["photographers", "caterers"], wants=["vendors"])
YOGA = V(topics=["yoga", "meditation", "breathwork"], goals=[],
         offers=["yoga classes", "workshops"], needs=["studio space"], wants=["students"])
STUDIO = V(topics=["wellness", "yoga", "massage"], goals=[],
           offers=["studio space", "mats"], needs=["yoga teachers", "workshops"], wants=["instructors"])
ACCT = V(topics=["bookkeeping", "tax preparation", "payroll"], goals=["help freelancers thrive"],
         offers=["bookkeeping", "tax preparation"], needs=["clients"], wants=["freelancers"])
FREELANCERS = V(topics=["freelancing", "design", "writing"], goals=["help freelancers thrive"],
                offers=["peer support"], needs=["bookkeeping", "tax preparation"], wants=["accountants"])
ELECTRICIAN = V(topics=["electrical wiring", "circuit design", "safety inspections"], goals=[],
                offers=["wiring help", "workshops"], needs=["projects"], wants=["makers"])
MAKERSPACE = V(topics=["woodworking", "electronics", "circuit design"], goals=["build together"],
               offers=["workshop space", "tools"], needs=["electrical wiring", "safety inspections"], wants=["instructors"])
TRAINER = V(topics=["dog training", "puppy socialization", "behavior"], goals=[],
            offers=["training classes"], needs=["clients"], wants=["shelters", "vets"])
SHELTER = V(topics=["animal rescue", "dog adoption", "fostering"], goals=["every dog a home"],
            offers=["volunteer community"], needs=["dog training", "behavior help"], wants=["trainers", "adopters"])
TRANSLATOR = V(topics=["translation", "spanish literature", "french novels"], goals=[],
               offers=["translation services"], needs=["manuscripts"], wants=["authors", "publishers"])
BOOK_CLUB = V(topics=["book discussions", "spanish literature", "reading circles"], goals=["read widely"],
              offers=["reading community"], needs=["translation services"], wants=["translators", "authors"])
CARPENTER = V(topics=["carpentry", "custom furniture", "wood joinery"], goals=[],
              offers=["custom tables", "repairs"], needs=["clients"], wants=["homeowners"])
FURNITURE = V(topics=["furniture", "home goods", "local makers"], goals=[],
              offers=["showroom space"], needs=["custom furniture", "carpentry"], wants=["artisans"])
ASTRONOMER = V(topics=["astronomy", "telescopes", "astrophotography"], goals=[],
               offers=["star parties", "talks"], needs=["dark skies"], wants=["enthusiasts"])
STARGAZERS = V(topics=["stargazing", "telescopes", "night sky"], goals=["watch the skies"],
               offers=["meetups"], needs=["telescope help", "astronomy talks"], wants=["astronomers"])
COOK = V(topics=["meal preparation", "nutrition", "batch cooking"], goals=[],
         offers=["weekly meal prep"], needs=["clients"], wants=["busy professionals"])
GYM = V(topics=["strength training", "nutrition coaching", "mobility"], goals=[],
        offers=["personal training"], needs=["meal prep partners"], wants=["members"])
CHESS_PERSON = V(topics=["chess", "endgames"], goals=[], offers=[], needs=[], wants=["chess partners"])
GARDEN_SPACE = V(topics=["gardening", "composting"], goals=[], offers=["workshops"], needs=["garden design"], wants=[])
PHYSICIST = V(topics=["quantum field theory", "particle physics"], goals=[],
              offers=["lectures"], needs=["lab funding"], wants=["physicists"])
PLUMBERS = V(topics=["plumbing", "pipe fitting", "drain repair"], goals=[],
             offers=["apprenticeships"], needs=["plumbers"], wants=["homeowners"])
POET = V(topics=["poetry", "spoken word", "chapbooks"], goals=[], offers=["readings"], needs=[], wants=["audiences"])
TAX_FIRM = V(topics=["tax law", "audits", "payroll"], goals=[], offers=["tax filing"], needs=["clients"], wants=["businesses"])
SURFER = V(topics=["surfing", "ocean swells", "board repair"], goals=[], offers=["surf lessons"], needs=[], wants=["beach friends"])
CHESS_CLUB = V(topics=["chess", "tournaments"], goals=[], offers=["coaching"], needs=["players"], wants=["chess partners"])
VIOLIN_TEACHER = V(topics=["violin", "chamber music"], goals=[], offers=["violin lessons"], needs=["students"], wants=["musicians"])
LUTHIER = V(topics=["violin making", "instrument repair", "varnish"], goals=[], offers=["repairs"], needs=["musicians"], wants=["players"])

# (label, a, b, expect_surface)
PAIRS = [
    ("baker finds the cafe", BAKER, CAFE, True),
    ("swim coach finds the triathlon club", SWIM_COACH, TRI_CLUB, True),
    ("beekeeper finds the orchard", BEEKEEPER, ORCHARD, True),
    ("tutor finds the homeschool co-op", TUTOR, COOP, True),
    ("photographer finds the wedding venue", PHOTOG, VENUE, True),
    ("yoga teacher finds the wellness studio", YOGA, STUDIO, True),
    ("accountant finds the freelancers group", ACCT, FREELANCERS, True),
    ("electrician finds the makerspace", ELECTRICIAN, MAKERSPACE, True),
    ("dog trainer finds the animal shelter", TRAINER, SHELTER, True),
    ("translator finds the book club", TRANSLATOR, BOOK_CLUB, True),
    ("carpenter finds the furniture store", CARPENTER, FURNITURE, True),
    ("astronomer finds the stargazing club", ASTRONOMER, STARGAZERS, True),
    ("meal-prep cook finds the gym (borderline)", COOK, GYM, True),
    ("chess person is not a gardener", CHESS_PERSON, GARDEN_SPACE, False),
    ("physicist is not a plumbers union", PHYSICIST, PLUMBERS, False),
    ("poet is not a tax firm", POET, TAX_FIRM, False),
    ("surfer is not a chess club", SURFER, CHESS_CLUB, False),
    ("violin teacher vs luthier: one signal only, bar holds (borderline)", VIOLIN_TEACHER, LUTHIER, False),
]

ROSA = V(topics=["baking", "sourdough", "community kitchen"], goals=[],
         offers=["bread", "baking classes"], needs=["kitchen space"], wants=["neighbors"])
ROSA_CORPUS = {
    "Bakery Cafe (space)": V(topics=["cafe", "baking", "sourdough"], goals=[],
                             offers=["kitchen space"], needs=["bread", "baking classes"], wants=[]),
    "Chess Club (space)": CHESS_CLUB,
    "Garden Space (space)": V(topics=["community gardens", "kitchen herbs"], goals=[],
                              offers=["kitchen space"], needs=["gardeners"], wants=[]),
}
DEV = V(topics=["data analysis", "python", "statistics tutoring"], goals=[],
        offers=["python tutoring"], needs=["students"], wants=["learners"])
DEV_CORPUS = {
    "Data Bootcamp (space)": V(topics=["data analysis", "python bootcamp"], goals=[],
                               offers=["cohorts"], needs=["python tutoring", "mentors"], wants=[]),
    "Poetry Circle (space)": POET,
    "Chess Space (space)": CHESS_CLUB,
}
# (label, entity, corpus, expected_top1, must_beat or None)
ORDERINGS = [
    ("rosa's top match is the bakery cafe", ROSA, ROSA_CORPUS, "Bakery Cafe (space)", "Garden Space (space)"),
    ("dev's top match is the data bootcamp", DEV, DEV_CORPUS, "Data Bootcamp (space)", None),
]

if __name__ == "__main__":
    passed = failed = 0
    for label, a, b, expect in PAIRS:
        r = score(a, b)
        if r["surface"] == expect:
            passed += 1; print(f"  PASS  {label}: {r['score']}% signals={r['signals']}")
        else:
            failed += 1; print(f"  FAIL  {label}: got surface={r['surface']} ({r['score']}%), expected {expect}; parts={r['parts']}")
    for label, e, corpus, top1, beat in ORDERINGS:
        rows = rank_matches(e, corpus)
        ok = bool(rows) and rows[0]["name"] == top1
        if ok and beat:
            by_name = {r["name"]: r["score"] for r in rows}
            ok = beat not in by_name or by_name[top1] > by_name[beat]
        if ok:
            passed += 1; print(f"  PASS  {label}: top={rows[0]['name']} {rows[0]['score']}%")
        else:
            failed += 1; print(f"  FAIL  {label}: ranking={[(r['name'], r['score']) for r in rows]}")
    print(f"HOLDOUT: {passed} passed, {failed} failed of {passed + failed} (synthetic)")
    sys.exit(1 if failed else 0)

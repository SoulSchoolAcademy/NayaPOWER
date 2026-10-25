#!/usr/bin/env python3
"""Consent Gate tests (B4). Run: python3 test_consent_gate.py (stdlib only).

The gate's worth is its NEGATIVE proofs, so most tests here are
withholding proofs — on the TWO axes the Page Settings Law separates
(director's decision, 2026-10-25): a non-findable entity is absent
everywhere except self-view; a PRIVATE (content-axis) citizen's terms
marked private never move a score and never appear in a reason another
citizen sees (proven against a public twin carrying only the public
terms); and the positive controls — a born-private FINDABLE citizen's
connect-offer card DOES surface, and a PUBLIC + findable entity
surfaces with the engine's row contract intact — prove the gate is a
boundary, not a wall. Every emitted row, on every path, must carry
the connect-offer labeling and grant nothing (SN-0848: a match is not
messaging consent; reading is not contributing).
"""
import copy, json, os

import consent_gate as g
import corpus as c
import derive_matches as d
from smart_match import FIELDS, score

HERE = os.path.dirname(os.path.abspath(__file__))
ENGINE_KEYS = {"alias", "kind", "score", "reasons",
               "signal_coverage_percent", "calibrated"}
FORBIDDEN_KEYS = {"can_message", "message_url", "messaging_allowed",
                  "can_contribute", "contribute_url", "can_edit",
                  "edit_url", "access_grant", "follow"}


def _vec(term="chess"):
    return {f: [term] for f in FIELDS}


def _entity(alias, kind, vector, **extra):
    ent = {"alias": alias, "name": alias, "kind": kind, "vector": vector,
           "provenance": {f: [] for f in FIELDS}, "value": None}
    ent.update(extra)
    return ent


def _corpus(*entities):
    ents = {e["alias"]: e for e in entities}
    return {"artifact": "welcome-engine-corpus/v1", "sources": ["declared"],
            "entity_count": len(ents), "entities": ents}


def _mixed_corpus():
    """Five entities, one identical vector: every pair scores 100, so
    only the boundary — never relevance — can explain an absence."""
    return _corpus(
        _entity("viewer-a", "citizen", _vec(), visibility="public", findable=True),
        _entity("open-b", "citizen", _vec(), visibility="public", findable=True),
        _entity("private-p", "citizen", _vec(), visibility="private", findable=True),
        _entity("hidden-h", "citizen", _vec(), visibility="public", findable=False),
        _entity("open-space", "space", _vec()),  # born PUBLIC + findable
    )


def _aliases(rows):
    return [r["alias"] for r in rows]


def _all_rows(gated):
    for sections in gated["citizens"].values():
        for rows in sections.values():
            yield from rows


def _assert_labelled(row):
    assert row["action"] == "connect_offer"        # CONNECT, never follow
    assert row["consent_scope"] == "connect_offer_only"
    assert row["grants"] == []                    # the gate grants nothing
    assert ENGINE_KEYS <= set(row)                 # engine contract intact


def _assert_no_forbidden_keys(obj):
    if isinstance(obj, dict):
        for k, v in obj.items():
            assert k not in FORBIDDEN_KEYS, k
            assert "message" not in k and "contribut" not in k, k
            assert "follow" not in k, k
            _assert_no_forbidden_keys(v)
    elif isinstance(obj, list):
        for v in obj:
            _assert_no_forbidden_keys(v)


def test_fixture_really_is_100_percent():
    v = _vec()
    r = score(v, dict(v))
    assert r["score"] == 100 and r["surface"] is True
    out = d.derive(_mixed_corpus())
    people = _aliases(out["citizens"]["viewer-a"]["people"])
    assert people == ["hidden-h", "open-b", "private-p"]  # all 100, name order
    assert all(r["score"] == 100 for r in out["citizens"]["viewer-a"]["people"])


def test_born_defaults_by_kind():
    cases = {"citizen": ("private", True), "personal": ("private", True),
             "citizen-personal": ("private", True),
             "business": ("public", True), "space": ("public", True),
             "project": ("public", True), "page": ("private", False)}
    for kind, expected in cases.items():
        eff = g.effective_visibility(_entity("x", kind, _vec()))
        assert (eff["visibility"], eff["findable"]) == expected, kind
        assert eff["sources"] == {"visibility": "born-default",
                                  "findable": "born-default"}, kind
    eff = g.effective_visibility(_entity("x", "mystery-kind", _vec()))
    assert (eff["visibility"], eff["findable"]) == ("private", False)
    assert eff["sources"]["visibility"] == "fail-closed"


def test_explicit_fields_override_born_defaults():
    # a space is born public; an explicit PRIVATE wins anyway
    eff = g.effective_visibility(_entity("s", "space", _vec(), visibility="PRIVATE"))
    assert eff["visibility"] == "private" and eff["sources"]["visibility"] == "explicit"
    # a citizen is born private; explicit public + findable wins
    eff = g.effective_visibility(_entity("p", "citizen", _vec(),
                                         visibility="public", findable=True))
    assert (eff["visibility"], eff["findable"]) == ("public", True)
    # the spellings the system already uses: settings dict, _findable,
    # the Settings Law's discoverability string
    eff = g.effective_visibility(_entity("p", "citizen", _vec(),
                                         settings={"visibility": "public",
                                                   "findable": False}))
    assert (eff["visibility"], eff["findable"]) == ("public", False)
    eff = g.effective_visibility(_entity("p", "citizen", _vec(),
                                         visibility="public", _findable=False))
    assert eff["findable"] is False
    eff = g.effective_visibility(_entity("p", "citizen", _vec(),
                                         visibility="public",
                                         discoverability="unlisted"))
    assert eff["findable"] is False


def test_private_findable_surfaces_as_card_and_in_self_view():
    # Born-default reading (Page Settings Law): private-p's CONTENT is
    # private, but it is FINDABLE, so its connect-offer card surfaces
    # to other citizens. Its vector here is all declared signals (no
    # terms marked private), so the card's math is the full 100.
    store = _mixed_corpus()
    gated = g.filter_matches(d.derive(store), store, "viewer-a")
    people = gated["citizens"]["viewer-a"]["people"]
    assert _aliases(people) == ["open-b", "private-p"]    # card beside the control
    card = [r for r in people if r["alias"] == "private-p"][0]
    assert card["score"] == 100
    _assert_labelled(card)                               # a card, not an access grant
    self_view = g.filter_matches(d.derive(store), store, "private-p")
    row = [r for r in self_view["citizens"]["viewer-a"]["people"]
           if r["alias"] == "private-p"]
    assert row and row[0]["score"] == 100                # self-view is not a leak
    _assert_labelled(row[0])
    direct = g.suggestions_for(store, "viewer-a")
    assert _aliases(direct["people"]) == ["open-b", "private-p"]


def test_nonfindable_absent_everywhere_except_self():
    store = _mixed_corpus()
    derived = d.derive(store)
    assert "hidden-h" in _aliases(derived["citizens"]["viewer-a"]["people"])
    for viewer in ("viewer-a", "open-b", "private-p", "open-space", "stranger"):
        gated = g.filter_matches(derived, store, viewer)
        assert all(r["alias"] != "hidden-h" for r in _all_rows(gated)), viewer
        assert "hidden-h" not in _aliases(g.suggestions_for(store, viewer)["people"]) \
            if viewer in store["entities"] else True
    self_view = g.filter_matches(derived, store, "hidden-h")
    assert any(r["alias"] == "hidden-h" for r in _all_rows(self_view))


def test_public_findable_control_surfaces_with_contract_intact():
    store = _mixed_corpus()
    derived = d.derive(store)
    gated = g.filter_matches(derived, store, "viewer-a")
    direct_row = [r for r in derived["citizens"]["viewer-a"]["people"]
                  if r["alias"] == "open-b"][0]
    gated_row = gated["citizens"]["viewer-a"]["people"][0]
    assert gated_row["alias"] == "open-b" and gated_row["score"] == 100
    for key in ENGINE_KEYS:                              # gate rewrites nothing
        assert gated_row[key] == direct_row[key], key
    _assert_labelled(gated_row)
    spaces = gated["citizens"]["viewer-a"]["spaces"]     # born-default space too
    assert _aliases(spaces) == ["open-space"] and spaces[0]["score"] == 100
    _assert_labelled(spaces[0])
    assert gated["generated_from"] == derived["generated_from"]
    assert gated["gated_for"] == "viewer-a" and gated["grants"] == []


def test_every_emitted_row_is_a_connect_offer_that_grants_nothing():
    store = _mixed_corpus()
    derived = d.derive(store)
    outputs = [g.filter_matches(derived, store, v)
               for v in ("viewer-a", "private-p", "hidden-h", "stranger")]
    outputs.append(g.filter_matches(d.derive(c.build_corpus()),
                                    c.build_corpus(), "nitro"))
    for out in outputs:
        _assert_no_forbidden_keys(out)
        for row in _all_rows(out):
            _assert_labelled(row)
    for viewer in ("viewer-a", "private-p"):
        for rows in g.suggestions_for(store, viewer).values():
            for row in rows:
                _assert_labelled(row)
                _assert_no_forbidden_keys(row)


def test_born_defaults_enforce_on_the_declared_corpus():
    store = c.build_corpus()
    derived = d.derive(store)
    assert _aliases(derived["citizens"]["naya-power"]["people"]) == ["nitro", "resolve"]
    gated = g.filter_matches(derived, store, "resolve")
    # Citizens are born PRIVATE + FINDABLE: their connect-offer cards
    # surface between citizens from day one. The declared corpus marks
    # no terms private, so each card's public-projection math equals
    # the derivation's own math — same aliases, same scores, in every
    # section — while born-public spaces surface exactly as before.
    for subject, sections in derived["citizens"].items():
        for label in ("people", "spaces"):
            want = [(r["alias"], r["score"]) for r in sections[label]]
            got = [(r["alias"], r["score"]) for r in gated["citizens"][subject][label]]
            assert got == want, (subject, label)
            for row in gated["citizens"][subject][label]:
                _assert_labelled(row)
    assert gated["citizens"]["nitro"]["spaces"][0]["alias"] == "space-team-nitro"
    assert gated["citizens"]["nitro"]["spaces"][0]["score"] == 62
    # self-view: rows naming nitro survive when nitro is the viewer
    nitro_view = g.filter_matches(derived, store, "nitro")
    assert "nitro" in _aliases(nitro_view["citizens"]["naya-power"]["people"])
    # a born-private viewer still receives their own suggestions —
    # people's cards AND spaces alike
    own = g.suggestions_for(store, "nitro")
    assert _aliases(own["people"]) == ["naya-power"]
    assert own["people"][0]["score"] == 18 and own["spaces"][0]["score"] == 62


def test_direct_path_agrees_with_filtered_derivation():
    store = _mixed_corpus()
    gated = g.filter_matches(d.derive(store), store, "viewer-a")
    assert g.suggestions_for(store, "viewer-a") == gated["citizens"]["viewer-a"]
    store2 = c.build_corpus()
    gated2 = g.filter_matches(d.derive(store2), store2, "naya-power")
    assert g.suggestions_for(store2, "naya-power") == gated2["citizens"]["naya-power"]


def test_insufficient_signal_names_only_what_the_viewer_may_see():
    # Naming is the FINDABILITY axis: a findable entity may be named
    # (its card may surface; the insufficient-signal entry carries no
    # terms and no score), a non-findable one may not — except to
    # itself.
    thin = {f: [] for f in FIELDS} | {"topics": ["zzz-alone"]}
    ghost = _entity("ghost-p", "citizen", thin,
                    visibility="private", findable=True)
    ghost_u = _entity("ghost-u", "citizen", dict(thin),
                      visibility="private", findable=False)
    store = _corpus(_entity("viewer-a", "citizen", _vec(),
                            visibility="public", findable=True), ghost, ghost_u)
    derived = d.derive(store)
    assert "ghost-p" in [e["alias"] for e in derived["insufficient_signal"]]
    gated = g.filter_matches(derived, store, "viewer-a")
    named = [e["alias"] for e in gated["insufficient_signal"]]
    assert "ghost-p" in named                            # findable: may be named
    assert "ghost-u" not in named                        # non-findable: withheld
    self_view = g.filter_matches(derived, store, "ghost-p")
    assert "ghost-p" in [e["alias"] for e in self_view["insufficient_signal"]]
    self_view_u = g.filter_matches(derived, store, "ghost-u")
    assert "ghost-u" in [e["alias"] for e in self_view_u["insufficient_signal"]]


def test_unknowns_fail_closed():
    store = _mixed_corpus()
    hand = {"artifact": "welcome-engine-matches/v1",
            "citizens": {"viewer-a": {"people": [
                {"alias": "ghost-x", "kind": "citizen", "score": 100,
                 "reasons": ["shared: chess"], "signal_coverage_percent": 100,
                 "calibrated": True}], "spaces": [], "projects": []}},
            "insufficient_signal": []}
    gated = g.filter_matches(hand, store, "viewer-a")
    assert gated["citizens"]["viewer-a"]["people"] == []  # no corpus entity, no surface
    gated_self = g.filter_matches(hand, store, "ghost-x")
    assert _aliases(gated_self["citizens"]["viewer-a"]["people"]) == ["ghost-x"]
    assert g.suggestions_for(store, "no-such-viewer") == {
        "people": [], "spaces": [], "projects": []}
    assert not g.is_visible_to(None, "viewer-a")
    assert not g.is_visible_to({"alias": "e", "kind": "mystery"}, "viewer-a")


def _projection_corpus():
    """quiet-q: a born-default citizen (no explicit fields — PRIVATE +
    findable by birth) whose declared vector carries one term it marks
    private. twin-t: a PUBLIC citizen carrying exactly quiet-q's public
    terms. viewer-a overlaps both on public terms and on the private
    one; viewer-b overlaps quiet-q ONLY through the private term."""
    public = {"topics": ["astronomy"], "goals": ["chess"],
              "offers": ["chess"], "needs": [], "wants": ["chess"]}
    quiet_vec = {f: list(ts) for f, ts in public.items()}
    quiet_vec["topics"] = ["astronomy", "secret knitting"]
    quiet = _entity("quiet-q", "citizen", quiet_vec,
                    private_vector={"topics": ["secret knitting"]})
    twin = _entity("twin-t", "citizen",
                   {f: list(ts) for f, ts in public.items()},
                   visibility="public", findable=True)
    viewer = _entity("viewer-a", "citizen",
                     {"topics": ["knitting"], "goals": ["chess"],
                      "offers": ["chess"], "needs": ["chess"],
                      "wants": ["chess"]},
                     visibility="public", findable=True)
    only = _entity("viewer-b", "citizen",
                   {"topics": ["knitting"], "goals": ["hiking"],
                    "offers": ["hiking"], "needs": ["hiking"],
                    "wants": ["secret knitting"]},
                   visibility="public", findable=True)
    return _corpus(viewer, quiet, twin, only)


def test_private_content_never_scored_or_cited_for_others():
    store = _projection_corpus()
    quiet_vec = store["entities"]["quiet-q"]["vector"]
    viewer_vec = store["entities"]["viewer-a"]["vector"]
    # The fixture is honest: on FULL vectors the private term really
    # does move the score (70 vs the projection's 50) — so a card at
    # the twin's score proves the term was excluded, not outvoted.
    assert score(viewer_vec, quiet_vec)["score"] == 70
    direct = g.suggestions_for(store, "viewer-a")
    card = [r for r in direct["people"] if r["alias"] == "quiet-q"][0]
    twin = [r for r in direct["people"] if r["alias"] == "twin-t"][0]
    assert card["score"] == twin["score"] == 50          # the public twin IS the math
    assert card["reasons"] == twin["reasons"]             # cited signals identical
    for reason in card["reasons"]:
        assert "secret" not in reason and "knitt" not in reason
    _assert_labelled(card)
    gated = g.filter_matches(d.derive(store), store, "viewer-a")
    gcard = [r for r in gated["citizens"]["viewer-a"]["people"]
             if r["alias"] == "quiet-q"][0]
    assert gcard == card                                 # both paths, same card
    # viewer-b overlaps quiet-q ONLY through the private term: on full
    # vectors the pair surfaces (two signals) — through the gate, the
    # card does not exist for them at all.
    assert score(store["entities"]["viewer-b"]["vector"], quiet_vec)["surface"]
    assert "quiet-q" not in _aliases(g.suggestions_for(store, "viewer-b")["people"])
    gated_b = g.filter_matches(d.derive(store), store, "viewer-b")
    own_section = [r for rows in gated_b["citizens"]["viewer-b"].values()
                   for r in rows]
    assert all(r["alias"] != "quiet-q" for r in own_section)
    # In viewer-a's section of that same gated copy, quiet-q's card is
    # present — as public data: the projection's 50, reasons clean.
    card_b = [r for r in gated_b["citizens"]["viewer-a"]["people"]
              if r["alias"] == "quiet-q"][0]
    assert card_b["score"] == 50
    assert all("secret" not in rsn and "knitt" not in rsn
               for rsn in card_b["reasons"])
    # and in NOBODY's gated view do quiet-q's reasons cite the term
    for viewer in ("viewer-a", "viewer-b", "twin-t"):
        out = g.filter_matches(d.derive(store), store, viewer)
        for row in _all_rows(out):
            if row["alias"] == "quiet-q":
                assert all("secret" not in rsn and "knitt" not in rsn
                           for rsn in row["reasons"])


def test_private_nonfindable_absent_everywhere_except_self():
    quiet_u = _entity("quiet-u", "citizen", _vec(),
                      visibility="private", findable=False)
    store = _corpus(
        _entity("viewer-a", "citizen", _vec(), visibility="public", findable=True),
        quiet_u)
    derived = d.derive(store)
    assert "quiet-u" in _aliases(derived["citizens"]["viewer-a"]["people"])
    gated = g.filter_matches(derived, store, "viewer-a")
    assert all(r["alias"] != "quiet-u" for r in _all_rows(gated))
    assert "quiet-u" not in _aliases(g.suggestions_for(store, "viewer-a")["people"])
    self_view = g.filter_matches(derived, store, "quiet-u")
    assert any(r["alias"] == "quiet-u" for r in _all_rows(self_view))


def test_inputs_never_mutated_and_output_deterministic():
    store = _mixed_corpus()
    derived = d.derive(store)
    snapshot = copy.deepcopy(derived)
    a = g.filter_matches(derived, store, "viewer-a")
    b = g.filter_matches(d.derive(_mixed_corpus()), _mixed_corpus(), "viewer-a")
    assert derived == snapshot                           # derivation untouched
    assert "action" not in derived["citizens"]["viewer-a"]["people"][0]
    assert json.dumps(a, sort_keys=True) == json.dumps(b, sort_keys=True)
    assert g.suggestions_for(store, "viewer-a") == g.suggestions_for(store, "viewer-a")


if __name__ == "__main__":
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for fn in fns:
        fn(); print("PASS", fn.__name__)
    print(f"{len(fns)}/{len(fns)} tests passed")

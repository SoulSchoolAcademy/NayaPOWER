#!/usr/bin/env python3
"""
The Consent Gate — B4 of the auto-match completion plan (2026-10-25).

The gate sits between the corpus/derivation and ANY surface:

    corpus (B2) -> derivation (B3) -> THIS GATE -> surface

The derivation is global math: it computes every citizen's ranked
suggestions over the whole corpus. Nothing global may reach a surface
unfiltered, because a score is not consent. This module is the one
place the privacy boundaries are enforced, as data, per viewer:

  * SN-0845 (Smart Match): privacy is architecture. Matching runs on
    aliases and public signals only; private content never feeds the
    matcher (true by construction in B2 — vectors hold declared signals
    only — and enforced again here at the surface boundary).
  * SN-0848 (the product boundary): three boundaries never blur —
    reading the collective != contributing to it; a match != messaging
    consent; a visible button is not a working feature.
  * The Page Settings Law (HUB/ROOMS/11-SETTINGS.md, SN-0852;
    welcome_engine.activate binds the same values at activation):
    visibility (PUBLIC / PRIVATE) and discoverability (FINDABLE /
    UNLISTED) are SEPARATE controls. The Connect projection is the
    alias + declared topic tags only, with calibrated relevance and
    reasons — never an access grant.

ENFORCEMENT SEMANTICS (this module's whole contract) — TWO AXES,
kept separate because the Page Settings Law keeps them separate:

  (a) CONTENT axis. An entity whose content is PRIVATE never has its
      private content scored or cited for another citizen. What may
      surface is its CONNECT-OFFER CARD — alias, match %, reasons —
      computed from its PUBLIC PROJECTION only: the declared vector
      minus the terms it marks private ("private_vector" /
      "private_terms", resolved like every other overlay field).
      Private terms never move a score another citizen sees and never
      appear in reason text. The card's math is exactly the math of a
      public twin carrying only the public terms — a test proves it.
  (b) FINDABILITY axis. A FINDABLE entity's card may surface to other
      citizens whatever its content axis — citizens are BORN private
      + findable, and their cards are how the network finds them. A
      non-findable (UNLISTED) entity never surfaces to anyone else,
      even when PUBLIC, and regardless of its content axis: an
      explicit non-findable flag always wins.
  (c) Self-view is not a leak: an entity may always see the rows that
      name ITSELF (viewer == candidate), whatever its settings. Being
      private never strips a citizen of their own matches either: a
      private viewer still receives suggestions — of the entities the
      boundary allows them to see.
  (d) Every emitted row is a CONNECT-OFFER and nothing more:
      action == "connect_offer" (SN-0845: we say CONNECT, never
      follow), consent_scope == "connect_offer_only", grants == [].
      No field anywhere in the output implies the viewer may message
      the entity (a match is not messaging consent) or contribute to /
      edit anything (reading is not contributing). The gate GRANTS
      NOTHING; it only withholds or passes through.

  DECISION (director/main seat, 2026-10-25, by scorecard against the
  Page Settings Law): the born-default reading above governs. An
  earlier strict reading — a PRIVATE entity never surfaces at all —
  is superseded: it confused the two axes the Law separates, and
  because citizens are born PRIVATE it would have kept every new
  citizen's card dark until they went public, defeating the findable
  half of their born default.

FINDABILITY / VISIBILITY AS DATA, WITHOUT TOUCHING B2's SCHEMA:
corpus entities today carry no visibility/findable fields (their shape
is alias / name / kind / vector / provenance / value — corpus.py owns
it, and this module does not rewrite it). The gate therefore resolves
each entity's effective settings as an OVERLAY:

  1. Explicit fields on the entity win, under any of the spellings the
     system already uses: "visibility" ("public"/"private"), the
     Settings Law's "discoverability" ("findable"/"unlisted"), the
     booleans "findable" / "_findable" (welcome_engine's corpus key) /
     "discoverable" — at the top level or under a "settings" dict.
  2. Otherwise the BORN DEFAULTS apply, by kind (Page Settings Law):
     personal (corpus kind "citizen") = PRIVATE + findable, business =
     PUBLIC + findable, space = PUBLIC + findable, project = PUBLIC +
     findable (Spaces = Projects is the standing ruling). A generic
     "page" is born PRIVATE + UNLISTED (the Law's generic Smart App
     default).
  3. An entity whose kind is none of these and that carries no explicit
     fields FAILS CLOSED: private + unlisted. Unknown is never public.

Note what the two axes together mean for the declared corpus as it
exists: citizens are born PRIVATE + findable, so their connect-offer
cards surface between citizens from day one — computed, as every
card is, from public/declared signals only (the corpus's vectors ARE
declared signals; a term joins the private part only when a source
explicitly marks it). Spaces and projects, born PUBLIC + findable,
surface with their full vectors scored, exactly as before. The gate
is a boundary, and the control tests prove it is not just a wall.

TWO COMPOSABLE ENTRY POINTS, one predicate pair:

  * filter_matches(matches, corpus, viewer) — gates a matches.json-
    shaped derivation (B3's output) for one viewer: every citizen
    section is gated by candidate findability TO THAT VIEWER, and
    insufficient_signal entries naming non-findable entities are
    withheld too (naming an entity is itself a disclosure). Because
    the derivation's rows were computed on full vectors, a row naming
    a content-PRIVATE candidate is RECOMPUTED here from the corpus —
    subject vector × the candidate's public projection — or withheld
    when it no longer surfaces or cannot be recomputed honestly. The
    derivation's other header fields pass through untouched.
  * suggestions_for(corpus, viewer) — the direct path: run the engine
    for a single viewer over the corpus (the same rank_matches_indexed
    call B3 makes) with each candidate's SCORING vector already
    resolved through the content axis, then gate. For any corpus and
    viewer the two paths agree exactly; a test pins that identity.

Surviving rows keep the engine's row contract intact — alias, kind,
score, reasons, signal_coverage_percent, calibrated — the gate only
ADDS the consent labeling (action / consent_scope / grants). For a
content-public candidate it never rewrites a score or a reason; for
a content-private candidate the row it emits is the public-projection
row, which is the only row about that candidate another citizen may
ever see. Inputs are never mutated.
"""
import copy, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from smart_match import FIELDS, _clean, build_index, rank_matches_indexed, score
import derive_matches as derive_mod

ARTIFACT = "welcome-engine-consent-gate/v1"
ACTION = "connect_offer"            # SN-0845: CONNECT, never follow
CONSENT_SCOPE = "connect_offer_only"  # a match is not messaging consent

# Born defaults by kind: (visibility, findable). Keys are the corpus's
# kinds plus the Settings Law's page names, which are the same pages:
# a corpus "citizen" IS the personal page of the Trinity.
BORN_DEFAULTS = {
    "citizen": ("private", True),          # the personal page
    "citizen-personal": ("private", True),
    "personal": ("private", True),
    "business": ("public", True),
    "space": ("public", True),
    "project": ("public", True),           # Spaces = Projects (standing ruling)
    "page": ("private", False),            # generic Smart App: PRIVATE + UNLISTED
}
FAIL_CLOSED = ("private", False)           # unknown kind, no explicit fields


def _norm_visibility(value):
    if isinstance(value, bool):
        return "public" if value else "private"
    if isinstance(value, str):
        v = value.strip().lower()
        if v in ("public", "private"):
            return v
    return None


def _norm_findable(value):
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        v = value.strip().lower()
        if v in ("findable", "listed", "discoverable"):
            return True
        if v in ("unlisted", "not_findable", "hidden", "undiscoverable"):
            return False
    return None


def _explicit(entity, keys, norm):
    """First recognizable explicit value for `keys`, looking at the
    entity's top level and then under its "settings" dict."""
    scopes = [entity]
    if isinstance(entity.get("settings"), dict):
        scopes.append(entity["settings"])
    for scope in scopes:
        for key in keys:
            if key in scope:
                found = norm(scope[key])
                if found is not None:
                    return found
    return None


def effective_visibility(entity):
    """Resolve one corpus entity's effective settings: explicit fields
    win, born defaults by kind otherwise, fail-closed for unknown
    kinds. Returns the values AND where each came from, because a gate
    that cannot name its basis is a guess."""
    entity = entity if isinstance(entity, dict) else {}
    kind = entity.get("kind")
    born = BORN_DEFAULTS.get(kind) if isinstance(kind, str) else None
    vis = _explicit(entity, ("visibility", "visible"), _norm_visibility)
    find = _explicit(entity, ("findable", "_findable", "discoverable",
                              "discoverability"), _norm_findable)
    return {
        "visibility": vis if vis is not None else (born[0] if born else FAIL_CLOSED[0]),
        "findable": find if find is not None else (born[1] if born else FAIL_CLOSED[1]),
        "sources": {
            "visibility": "explicit" if vis is not None else
                          ("born-default" if born else "fail-closed"),
            "findable": "explicit" if find is not None else
                        ("born-default" if born else "fail-closed"),
        },
    }


def content_is_public(entity):
    """The CONTENT axis: may this entity's full vector be scored and
    cited for other citizens? An explicit private flag always wins;
    otherwise the born default for its kind decides."""
    return isinstance(entity, dict) and \
        effective_visibility(entity)["visibility"] == "public"


def may_surface_to(entity, viewer_alias, alias=None):
    """The FINDABILITY axis: may this entity's connect-offer card
    surface to `viewer_alias` at all? `entity` is the CANDIDATE's
    corpus entity (or None); `alias` is the candidate's alias when the
    entity does not carry it. Self-view always passes; an explicit
    non-findable flag always wins; a candidate with no corpus entity
    fails closed. The content axis is NOT consulted here — it governs
    what may be scored and cited, enforced in scoring_vector() and in
    the row gate, never whether a findable citizen may be found."""
    if alias is None and isinstance(entity, dict):
        alias = entity.get("alias")
    if viewer_alias and alias is not None and alias == viewer_alias:
        return True  # self-view is not a leak
    if not isinstance(entity, dict):
        return False
    return effective_visibility(entity)["findable"]


def is_visible_to(entity, viewer_alias, alias=None):
    """Back-compat name for the findability axis (may_surface_to).
    Before the two axes were split, this predicate ANDed public +
    findable into a single surfacing veto — the strict reading the
    director's 2026-10-25 decision superseded. Surfacing is the
    findability question; content is enforced in the scoring."""
    return may_surface_to(entity, viewer_alias, alias=alias)


def _term_key(term):
    """The key a private mark meets a declared term by: the term
    itself, case- and whitespace-tolerantly. A mark NAMES a declared
    term (the source that marks it copies it from the same
    declaration), so exact-phrase identity is the semantics; the
    tolerance covers only how the same term happens to be typed."""
    return " ".join(term.strip().lower().split())


def _private_keys(entity):
    """The keys of the terms an entity marks as private content: a
    "private_vector" (a 5-field dict) and/or a flat "private_terms"
    list, at the top level or under "settings" — resolved like every
    other overlay field. Returns (per-field key sets, flat key set).
    Removing a term removes every channel the engine could match it
    on — phrase, stemmed words, and concepts all derive from the
    declared term — so term-level subtraction is exact, not partial."""
    per_field = {f: set() for f in FIELDS}
    flat = set()
    if not isinstance(entity, dict):
        return per_field, flat
    scopes = [entity]
    if isinstance(entity.get("settings"), dict):
        scopes.append(entity["settings"])
    for scope in scopes:
        pv = scope.get("private_vector")
        if isinstance(pv, dict):
            cleaned = _clean(pv)
            for f in FIELDS:
                per_field[f] |= {_term_key(t) for t in cleaned.get(f, [])}
        pt = scope.get("private_terms")
        if isinstance(pt, (list, tuple, set)):
            flat |= {_term_key(t) for t in pt if isinstance(t, str)}
    return per_field, flat


def public_vector(entity):
    """The entity's PUBLIC PROJECTION: its declared vector minus the
    terms it marks private, per field. This — and only this — may be
    scored or cited when another citizen looks at a content-private
    entity. (For a content-public entity the projection is never
    needed; scoring_vector returns the full vector.)"""
    vec = entity.get("vector") if isinstance(entity, dict) else None
    if not isinstance(vec, dict):
        return {f: [] for f in FIELDS}
    cleaned = _clean(vec)
    per_field, flat = _private_keys(entity)
    return {f: [t for t in cleaned.get(f, [])
                if _term_key(t) not in per_field[f]
                and _term_key(t) not in flat]
            for f in FIELDS}


def scoring_vector(entity):
    """The vector that may be scored when ANOTHER citizen looks at
    this entity: the full vector when the content axis is public, the
    public projection when it is private."""
    if content_is_public(entity):
        vec = entity.get("vector")
        return vec if isinstance(vec, dict) else {}
    return public_vector(entity)


def label_row(row):
    """Pass an engine row through with the consent labeling ADDED and
    the engine contract untouched. The labeling states what the row
    IS (a connect-offer) and what it grants (nothing)."""
    out = dict(row)
    out["action"] = ACTION
    out["consent_scope"] = CONSENT_SCOPE
    out["grants"] = []
    return out


def _entities_of(corpus):
    """Accept B2's corpus dict ({"entities": {...}}) or a bare
    {alias: entity} mapping; anything else is an empty corpus."""
    if isinstance(corpus, dict):
        if isinstance(corpus.get("entities"), dict):
            return corpus["entities"]
        return corpus
    return {}


def _gate_row(row, entities, viewer_alias, subject_alias):
    """Gate ONE row for one viewer; returns the labeled row or None.

    Composition of the two axes, in order:
      * a row naming the VIEWER is self-view — passed untouched;
      * a candidate with no corpus entity fails closed;
      * the FINDABILITY axis: a non-findable candidate never surfaces;
      * the CONTENT axis: a content-PUBLIC candidate's row passes
        untouched (the gate rewrites nothing about it); a content-
        PRIVATE candidate's incoming row was computed on its FULL
        vector, so it is never passed on — it is recomputed from the
        corpus as subject × the candidate's public projection, and
        withheld when it no longer surfaces or cannot be recomputed
        honestly (no subject entity / no subject vector)."""
    if not isinstance(row, dict):
        return None
    alias = row.get("alias")
    if alias is not None and viewer_alias and alias == viewer_alias:
        return label_row(row)  # self-view is not a leak
    ent = entities.get(alias)
    if not isinstance(ent, dict):
        return None
    if not may_surface_to(ent, viewer_alias, alias=alias):
        return None
    if content_is_public(ent):
        return label_row(row)
    subject = entities.get(subject_alias) if subject_alias else None
    if not isinstance(subject, dict) or \
            not isinstance(subject.get("vector"), dict):
        return None
    r = score(subject["vector"], public_vector(ent))
    if not r["surface"]:
        return None
    return label_row(derive_mod._row(alias, ent.get("kind") or row.get("kind"), r))


def gate_rows(rows, entities, viewer_alias, subject_alias=None):
    """Filter + label one section's rows for one viewer. Sections are
    re-sorted by (-score, alias) — the derivation's own order for
    untouched rows, and the honest order once a private candidate's
    row has been recomputed onto its public projection."""
    out = []
    for row in rows or []:
        gated = _gate_row(row, entities, viewer_alias, subject_alias)
        if gated is not None:
            out.append(gated)
    out.sort(key=lambda r: (-(r.get("score") or 0), r.get("alias") or ""))
    return out


def filter_matches(matches, corpus, viewer_alias):
    """Gate a matches.json-shaped derivation for one viewer. Every
    citizen section keeps only the rows whose candidate is visible to
    the viewer (self-named rows included); insufficient_signal keeps
    only entries the viewer may see named. Header fields pass through;
    the gate stamps its own provenance on the copy it returns."""
    entities = _entities_of(corpus)
    out = copy.deepcopy(matches) if isinstance(matches, dict) else {}
    citizens = {}
    for subject, sections in (out.get("citizens") or {}).items():
        citizens[subject] = {label: gate_rows(rows, entities, viewer_alias,
                                              subject_alias=subject)
                             for label, rows in (sections or {}).items()}
    out["citizens"] = citizens
    if "insufficient_signal" in out:
        out["insufficient_signal"] = [
            e for e in out["insufficient_signal"] or []
            if isinstance(e, dict) and
            may_surface_to(entities.get(e.get("alias")), viewer_alias,
                           alias=e.get("alias"))]
    out["gated_for"] = viewer_alias
    out["gate"] = ARTIFACT
    out["grants"] = []
    return out


def suggestions_for(corpus, viewer_alias):
    """The direct path: one viewer's gated suggestions from the corpus
    alone — the same engine call B3's derivation makes for that citizen
    (rank_matches_indexed behind one shared index, grouped by kind),
    then the gate. Returns the sections shape of a derivation's
    citizens[viewer] entry: {"people": [...], "spaces": [...],
    "projects": [...]}. A viewer with no corpus entity has no vector
    to match from and receives empty sections."""
    entities = _entities_of(corpus)
    sections = {label: [] for _kind, label in derive_mod.SECTIONS}
    viewer = entities.get(viewer_alias)
    if not isinstance(viewer, dict) or not isinstance(viewer.get("vector"), dict):
        return sections
    vectors = {a: e["vector"] for a, e in entities.items()
               if isinstance(e, dict) and isinstance(e.get("vector"), dict)}
    # The ranking runs on EFFECTIVE vectors: the viewer's own full
    # vector (their private signals may drive their own suggestions —
    # reasons cite overlaps, and an overlap term is by definition also
    # the candidate's), each findable candidate's SCORING vector (full
    # when content-public, public projection when content-private),
    # and non-findable candidates excluded entirely. The index is
    # built on the same effective vectors, so a candidate sharing only
    # private terms with the viewer is never even pre-filtered in.
    effective = {}
    for alias, vec in vectors.items():
        if alias == viewer_alias:
            effective[alias] = vec
        elif may_surface_to(entities[alias], viewer_alias, alias=alias):
            effective[alias] = scoring_vector(entities[alias])
    index = build_index(effective)
    by_kind = {}
    for alias in sorted(effective):
        by_kind.setdefault(entities[alias].get("kind"), {})[alias] = effective[alias]
    for kind, label in derive_mod.SECTIONS:
        rows = rank_matches_indexed(vectors[viewer_alias], by_kind.get(kind, {}),
                                    index=index, self_name=viewer_alias)
        engine_rows = [derive_mod._row(r["name"], kind, r) for r in rows]
        sections[label] = gate_rows(engine_rows, entities, viewer_alias,
                                    subject_alias=viewer_alias)
    return sections

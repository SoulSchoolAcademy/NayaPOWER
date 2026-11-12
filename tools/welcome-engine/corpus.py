#!/usr/bin/env python3
"""
The Corpus Store — B2 of the auto-match completion plan (2026-10-25).

Until this module the matcher had no corpus: declared_vectors.py held 12
hand-written entities in display-name keys, welcome_engine.activate()
took an in-memory dict, and B1's bridge produced per-citizen vectors with
nowhere canonical to land. This is the ONE store every consumer (B3's
derivation, future surfaces) reads: entities keyed by alias, one shape.

ENTITY SHAPE (the store's whole contract):
    {"alias":  "nitro",                       # the corpus key
     "name":   "nitro (Naya N Narzan, ...)",  # source display name, kept
     "kind":   "citizen" | "space" | "project" | "page",
     "vector": {field: [terms, sorted]},      # exactly the engine's 5 fields
     "provenance": {field: [sources]},        # who fed each field, authority order
     "value":  None | {"state": ..., "value": ...}}   # the engine's record slot

SOURCES, merged in this order of authority (per the completion plan):
  1. "declared" — declared_vectors.py: the team's declared population.
     SEATS are citizens; PROJECTS are spaces (their canonical aliases are
     space-* and Spaces = Projects is the standing ruling — kind
     "project" is reserved for a true project source, none exists in
     machine-readable form in the repo today).
  2. "intake" — B1's bridge (intake_bridge.vectors_from_intake): citizens'
     Welcome answers folded from intake_events rows. This is the merge
     that keeps a door-only corpus from starving: a citizen's declared
     terms and walked terms UNION, so offers/needs/wants declared on a
     page are never erased by a thin door walk, and vice versa.
  3. "page" — page/space declarations in this module's adapter shape
     ({alias: {"kind":..., "name":..., "vector": {...}, "value": {...}}}).
     FINDING, stated plainly: the repo carries NO page declarations in
     the engine's 5-field shape today. HUB/FEEDS/spaces.json is a feed of
     snapshot rooms (foreign ids, single artifact tags like
     SMART_NOTE_ARTIFACT — plumbing, not declarations), and
     DEMO-RECEIPTS.json holds two SYNTHETIC demo citizens, excluded on
     purpose. The adapter exists so the day a real page source lands in
     machine form it merges here with no new plumbing — until then the
     source contributes nothing and the corpus says so in its header.

MERGE RULES:
  * Terms UNION per field — a later source never deletes an earlier
    source's terms; kind and name come from the highest-authority source
    that carries the entity.
  * Provenance records, per field, every source that contributed terms,
    in authority order — coverage is named, never implied (L667).
  * The "value" slot carries a source's declared value RECORD verbatim
    (a dict) or None. The slot mirrors the engine's contract exactly —
    smart_match._verified_value is the only judge of whether a record
    may move rank (VERIFIED/FINAL only); the store judges nothing.
  * DETERMINISM: aliases sorted, terms sorted, one canonical JSON
    serialization (sort_keys, indent=1). Identical inputs -> identical
    bytes -> identical corpus hash. The corpus is a derived artifact.
"""
import hashlib, json, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from smart_match import FIELDS, _clean  # the engine's own sanitizer — one view of a vector
import declared_vectors
import intake_bridge

ARTIFACT = "welcome-engine-corpus/v1"
KINDS = ("citizen", "space", "project", "page")
SOURCE_ORDER = ("declared", "intake", "page")


def alias_of(display_key):
    """The corpus alias inside a declared display key: the part before
    ' (' for seats ('nitro (Naya N ...)') -> 'nitro', the parenthesized
    space alias for projects ('NayaPOWER (space-nayapower)') ->
    'space-nayapower'. A key with neither shape is its own alias."""
    if " (" in display_key and display_key.endswith(")"):
        head, tail = display_key.split(" (", 1)
        inner = tail[:-1]
        return inner if inner.startswith("space-") else head
    return display_key


def _empty_entity(alias):
    return {"alias": alias, "name": alias, "kind": None,
            "vector": {f: [] for f in FIELDS},
            "provenance": {f: [] for f in FIELDS},
            "value": None}


def _merge_into(ent, kind, name, vector, value, source):
    """Union one source's contribution into an entity, in place.
    First source (authority order) to carry the entity sets kind/name;
    a source's value record fills the slot only while it is empty."""
    if ent["kind"] is None and kind in KINDS:
        ent["kind"] = kind
    if ent["name"] == ent["alias"] and name:
        ent["name"] = name
    clean = _clean(vector)
    for f in FIELDS:
        if clean[f]:
            merged = sorted(set(ent["vector"][f]) | set(clean[f]))
            if merged != ent["vector"][f]:
                ent["vector"][f] = merged
            if source not in ent["provenance"][f]:
                ent["provenance"][f].append(source)
    if ent["value"] is None and isinstance(value, dict):
        ent["value"] = value


def build_corpus(intake_rows=None, page_declarations=None):
    """Assemble the canonical corpus from the three sources, in
    authority order. `intake_rows` is a list of intake_events row dicts
    (B1's input shape); `page_declarations` is the adapter shape from
    the header. Both default to absent — the declared population alone
    is a complete, honest corpus."""
    entities = {}
    sources_used = []

    def ent(alias):
        return entities.setdefault(alias, _empty_entity(alias))

    # 1. declared — the team's declared population
    for key, vec in declared_vectors.SEATS.items():
        _merge_into(ent(alias_of(key)), "citizen", key, vec, None, "declared")
    for key, vec in declared_vectors.PROJECTS.items():
        _merge_into(ent(alias_of(key)), "space", key, vec, None, "declared")
    sources_used.append("declared")

    # 2. intake — B1 bridge vectors from citizens' walked answers
    if intake_rows:
        vectors, _diag = intake_bridge.vectors_from_intake(intake_rows)
        if vectors:
            sources_used.append("intake")
        for alias, vec in vectors.items():
            _merge_into(ent(alias), "citizen", alias, vec, None, "intake")

    # 3. page — machine-readable page/space declarations, when they exist
    if page_declarations:
        merged_any = False
        for alias, decl in page_declarations.items():
            if not isinstance(decl, dict) or not isinstance(decl.get("vector"), dict):
                continue
            _merge_into(ent(alias), decl.get("kind"), decl.get("name") or alias,
                        decl["vector"], decl.get("value"), "page")
            merged_any = True
        if merged_any:
            sources_used.append("page")

    ordered = {a: entities[a] for a in sorted(entities)}
    for e in ordered.values():
        if e["kind"] is None:
            e["kind"] = "citizen"  # an alias no source could kind: a walked citizen
    return {"artifact": ARTIFACT,
            "sources": [s for s in SOURCE_ORDER if s in sources_used],
            "entity_count": len(ordered),
            "entities": ordered}


def corpus_bytes(corpus):
    """The canonical serialization — the bytes the hash binds to."""
    return (json.dumps(corpus, indent=1, sort_keys=True) + "\n").encode("utf-8")


def corpus_hash(corpus):
    return hashlib.sha256(corpus_bytes(corpus)).hexdigest()


def write_corpus(corpus, path):
    with open(path, "wb") as fh:
        fh.write(corpus_bytes(corpus))
    return path


def read_corpus(path):
    with open(path, "rb") as fh:
        return json.loads(fh.read().decode("utf-8"))


if __name__ == "__main__":
    # Usage: python3 corpus.py [rows.json] [out.json]
    #   rows.json — optional intake_events rows (B1's shape), folded in
    #   out.json  — store path (default: corpus.json beside this module)
    here = os.path.dirname(os.path.abspath(__file__))
    rows, out_path = None, os.path.join(here, "corpus.json")
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if len(args) >= 1:
        with open(args[0]) as fh:
            rows = json.load(fh)
    if len(args) >= 2:
        out_path = args[1]
    built = build_corpus(intake_rows=rows)
    write_corpus(built, out_path)
    kinds = {}
    for e in built["entities"].values():
        kinds[e["kind"]] = kinds.get(e["kind"], 0) + 1
    print(json.dumps({"wrote": out_path, "entities": built["entity_count"],
                      "kinds": kinds, "sources": built["sources"],
                      "corpus_hash": corpus_hash(built)}, indent=1, sort_keys=True))

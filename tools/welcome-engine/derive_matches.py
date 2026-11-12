#!/usr/bin/env python3
"""
The Match Derivation — B3 of the auto-match completion plan (2026-10-25),
SN-0845 build (2): the matcher as a derivation, recomputed from the
corpus, never a hand-run report.

    corpus (B2's store) -> per-citizen ranked suggestions -> matches.json

For every citizen in the corpus, candidates are ranked with the engine's
own rank_matches_indexed behind ONE shared inverted index, and the
suggestions are separated by candidate kind into people / spaces /
projects. Every row carries the engine's exact output contract —
score %, reasons, signal_coverage_percent, calibrated — because a %
without reasons is a bug (the engine's published semantics), and a
derivation that rewrites the contract would be a second matcher.

DETERMINISM: the same corpus produces byte-identical matches.json. All
iteration is over sorted aliases; the engine is deterministic; the index
only pre-filters. Proven by test (two runs, byte compare) and by the
identity test (derivation rows == direct rank_matches rows on the same
corpus — the derivation adds grouping and honesty, never new math).

THIN-VECTOR HONESTY (L667 — coverage named per field, never silently
absent): an entity that surfaces in ZERO pairs across the whole
derivation — as a citizen subject or as anyone's candidate — is named
in "insufficient_signal" with its per-field term counts and its empty
fields listed. The four island spaces live there, at their true state,
until their declarations grow or a source feeds their missing fields.

VALUE NOTE, named rather than hidden: v1.5's rank API
(rank_matches / rank_matches_indexed) does not thread a value record —
only score() accepts value_b. The corpus therefore carries each
entity's value slot (B2) stored but unconsumed by this derivation;
rank here is pure relevance, exactly as the engine's rank path defines
it. Threading value through the rank path is an engine change, owned
by a later step — this derivation invents no second path around it.
"""
import json, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from smart_match import FIELDS, WEIGHTS, build_index, rank_matches_indexed
import corpus as corpus_mod

ARTIFACT = "welcome-engine-matches/v1"
ENGINE_ID = "smart_match v1.5"
SECTIONS = (("citizen", "people"), ("space", "spaces"), ("project", "projects"))


def _row(candidate_alias, kind, engine_row):
    return {"alias": candidate_alias, "kind": kind,
            "score": engine_row["score"],
            "reasons": engine_row["reasons"],
            "signal_coverage_percent": engine_row["signal_coverage_percent"],
            "calibrated": engine_row["calibrated"]}


def derive(corpus):
    """Corpus dict (B2's shape) -> matches dict. Pure function of the
    corpus: no clock, no randomness, no I/O."""
    entities = corpus["entities"]
    vectors = {a: e["vector"] for a, e in entities.items()}
    index = build_index(vectors)
    by_kind = {}
    for alias in sorted(entities):
        by_kind.setdefault(entities[alias]["kind"], {})[alias] = vectors[alias]

    participation = {a: 0 for a in entities}
    citizens = {}
    for alias in sorted(a for a, e in entities.items() if e["kind"] == "citizen"):
        sections = {}
        for kind, label in SECTIONS:
            rows = rank_matches_indexed(vectors[alias], by_kind.get(kind, {}),
                                        index=index, self_name=alias)
            sections[label] = [_row(r["name"], kind, r) for r in rows]
            for r in rows:
                participation[alias] += 1
                participation[r["name"]] += 1
        citizens[alias] = sections

    insufficient = []
    for alias in sorted(entities):
        if participation[alias] == 0:
            vec = vectors[alias]
            insufficient.append({
                "alias": alias, "kind": entities[alias]["kind"],
                "surfaced_pairs": 0,
                "empty_fields": [f for f in FIELDS if not vec.get(f)],
                "field_term_counts": {f: len(vec.get(f, [])) for f in FIELDS}})

    return {"artifact": ARTIFACT,
            "generated_from": corpus_mod.corpus_hash(corpus),
            "entity_count": len(entities),
            "engine": ENGINE_ID,
            "weights": dict(WEIGHTS),
            "citizens": citizens,
            "insufficient_signal": insufficient}


def matches_bytes(matches):
    return (json.dumps(matches, indent=1, sort_keys=True) + "\n").encode("utf-8")


def write_matches(matches, path):
    with open(path, "wb") as fh:
        fh.write(matches_bytes(matches))
    return path


if __name__ == "__main__":
    # Usage: python3 derive_matches.py [corpus.json] [matches.json]
    # A missing corpus file is built from sources first (corpus.py's
    # build) and written — the store is regenerable, never hand-kept.
    here = os.path.dirname(os.path.abspath(__file__))
    corpus_path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(here, "corpus.json")
    out_path = sys.argv[2] if len(sys.argv) > 2 else os.path.join(here, "matches.json")
    if os.path.exists(corpus_path):
        store = corpus_mod.read_corpus(corpus_path)
    else:
        store = corpus_mod.build_corpus()
        corpus_mod.write_corpus(store, corpus_path)
        print(f"corpus store built from sources -> {corpus_path}")
    result = derive(store)
    write_matches(result, out_path)
    total = sum(len(s) for c in result["citizens"].values() for s in c.values())
    print(json.dumps({"wrote": out_path, "entities": result["entity_count"],
                      "citizens": len(result["citizens"]),
                      "suggestions": total,
                      "insufficient_signal": [e["alias"] for e in result["insufficient_signal"]],
                      "generated_from": result["generated_from"]},
                     indent=1, sort_keys=True))

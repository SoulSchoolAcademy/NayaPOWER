#!/usr/bin/env python3
"""
The IDF Decision Harness — B6 of the auto-match completion plan
(2026-10-25). HARDENING-ELITE-V2 §5 landed population-frequency
weighting (smart_match.compute_idf) as an optional mode, default OFF,
with the recommendation: ADOPT as an available mode; whether production
flips the default (or the threshold to >=50%) is a wiring-step
calibration decision to make with real data, gated by the golden set +
identity tests. This harness produces that decision's evidence packet,
on whatever corpus exists at run time. It informs the decision; it
does not make it, and it changes no default anywhere.

WHAT IT RUNS, every time:
  (a) The GOLDEN SET and the HOLDOUT, each scored three ways:
      IDF OFF · IDF ON at the shipped defaults (compute_idf threshold
      0.5 strict, factor 0.25) · IDF ON at the >=50% sensitivity
      threshold HARDENING §5 measured (threshold set a half-step under
      0.5, so a token present in exactly half the population IS
      down-weighted — on the declared population 'builder'/'builders'
      sit at exactly 6/12, so the shipped strict rule is a no-op there
      and only this leg discriminates). Per set: label accuracy and
      OFF-vs-ON verdict agreement, per leg.
      A labeled set's IDF population is every distinct entity vector
      the set touches (pair sides + ranking subjects and corpora) —
      the population those cases would be ranked inside.
  (b) The REAL CORPUS (corpus.json, B2's store): every unordered pair
      scored OFF vs ON, emitted as a DECISION TABLE — per pair surfaced
      in any leg: score off, score on (both thresholds), delta, and the
      survived-at->=50% flag — plus the aggregate lines a decider
      needs: pairs surfaced per leg, pairs lost/gained per leg, top-2
      stability, the most-deflated pairs, and the ubiquity table the
      IDF legs were derived from.

SCALE GUARD: the corpus rankings run through rank_matches_indexed
behind ONE shared inverted index (build_index), paired with the
ubiquity table (signature document frequencies over the same corpus).
The harness proves, on this corpus and in every leg, that the indexed
rows are EXACTLY the naive rank_matches rows — the pre-filter changes
nothing — and cross-checks the pair matrix against those rankings.

OUTPUT: a human-readable table to stdout AND the machine artifact
idf_decision.json beside this module (canonical serialization:
sort_keys, indent=1 — the same bytes every run on the same inputs).

Run: python3 idf_eval.py [corpus.json] [idf_decision.json]
Stdlib only, like the rest of the package.
"""
import json, math, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import smart_match as m
import golden_set
import holdout_set
import corpus as corpus_mod

ARTIFACT = "welcome-engine-idf-decision/v1"
ENGINE_ID = "smart_match v1.5"
IDF_FACTOR = 0.25            # compute_idf's shipped factor — the mode as landed
THRESHOLD_DEFAULT = 0.5      # compute_idf's shipped threshold (strict >)

RECOMMENDATION_RULE = (
    "HARDENING-ELITE-V2 §5, standing: ADOPT IDF as an available mode, "
    "default OFF. Whether production flips the default (or the threshold "
    "to >=50%) is a wiring-step calibration decision to make with real "
    "citizen data — the golden set + identity tests are its gate. This "
    "harness supplies the measured facts for that decision; it does not "
    "make it, and it flips no default.")


# --------------------------------------------------------------------------
# populations + IDF legs

def _touched_population(pairs, rankings):
    """Every distinct vector a labeled set touches, by object identity —
    pair sides, ranking subjects, and ranking corpora members."""
    seen, pop = set(), []

    def add(v):
        if id(v) not in seen:
            seen.add(id(v))
            pop.append(v)

    for _label, a, b, _expect in pairs:
        add(a)
        add(b)
    for _label, e, corp, _top1, _beat in rankings:
        add(e)
        for v in corp.values():
            add(v)
    return pop


def _ge50_threshold(n):
    """The compute_idf threshold whose strict-> rule reproduces >=50%:
    a token is down-weighted iff its document frequency reaches half
    the population. df/n > (ceil(n/2) - 0.5)/n  <=>  df >= ceil(n/2)."""
    if n <= 0:
        return THRESHOLD_DEFAULT
    return (math.ceil(n / 2) - 0.5) / n


def _idf_legs(population):
    """The two ON legs for one population: shipped defaults, and the
    >=50% sensitivity threshold. Returns {name: idf-dict}."""
    return {
        "on_default": m.compute_idf(population, threshold=THRESHOLD_DEFAULT,
                                    factor=IDF_FACTOR),
        "on_ge50": m.compute_idf(population,
                                  threshold=_ge50_threshold(len(population)),
                                  factor=IDF_FACTOR),
    }


def ubiquity_table(vectors):
    """The ubiquity table paired with the inverted index (HARDENING §6):
    document frequency of every signature token over the corpus — the
    same counts compute_idf derives its weights from, made visible.
    Rows sorted by (-df, token); share is df / population size."""
    n = len(vectors)
    df = {}
    for v in vectors.values():
        for tok in m.signature(v):
            df[tok] = df.get(tok, 0) + 1
    rows = [{"token": tok, "df": c, "share": round(c / n, 3) if n else 0.0}
            for tok, c in df.items()]
    rows.sort(key=lambda r: (-r["df"], r["token"]))
    return rows


# --------------------------------------------------------------------------
# (a) labeled sets — golden + holdout, OFF vs ON

def _eval_pairs(pairs, legs):
    cases = []
    for label, a, b, expect in pairs:
        row = {"label": label, "kind": "pair", "expected_surface": expect,
               "informational": expect is None}
        for leg, idf in legs.items():
            r = m.score(a, b, idf=idf)
            row[leg] = {"score": r["score"], "surface": r["surface"],
                        "signals": r["signals"]}
            row[f"passed_{leg}"] = (None if expect is None
                                    else r["surface"] == expect)
        cases.append(row)
    return cases


def _eval_rankings(rankings, legs):
    cases = []
    for label, e, corp, top1, beat in rankings:
        row = {"label": label, "kind": "ranking", "expected_top1": top1,
               "must_beat": beat, "informational": False}
        for leg, idf in legs.items():
            rows = m.rank_matches(e, corp, idf=idf)
            got = rows[0]["name"] if rows else None
            ok = got == top1
            if ok and beat:
                by_name = {r["name"]: r["score"] for r in rows}
                ok = beat not in by_name or by_name[top1] > by_name[beat]
            row[leg] = {"top1": got,
                        "score": rows[0]["score"] if rows else None}
            row[f"passed_{leg}"] = ok
        cases.append(row)
    return cases


def _verdict(case, leg):
    """The case's verdict under one leg, for OFF-vs-ON agreement:
    surface for pairs, top-1 name for rankings."""
    if case["kind"] == "pair":
        return case[leg]["surface"]
    return case[leg]["top1"]


def _set_summary(cases):
    scored = [c for c in cases if not c["informational"]]
    out = {"total_cases": len(cases), "scored_cases": len(scored)}
    for leg in ("off", "on_default", "on_ge50"):
        passed = sum(1 for c in scored if c[f"passed_{leg}"])
        out[f"passed_{leg}"] = passed
        out[f"accuracy_{leg}"] = (round(passed / len(scored), 3)
                                  if scored else None)
    for leg in ("on_default", "on_ge50"):
        agree = sum(1 for c in cases if _verdict(c, leg) == _verdict(c, "off"))
        out[f"agreement_{leg}"] = (round(agree / len(cases), 3)
                                   if cases else None)
    return out


def evaluate_labeled_sets():
    """Golden + holdout under all three legs. Rankings are normalized
    to (label, entity, corpus, expected_top1, must_beat-or-None)."""
    golden_rankings = [(label, e, corp, name, None)
                       for label, e, corp, name in golden_set.TOP1]
    sets = {
        "golden": (golden_set.PAIRS, golden_rankings),
        "holdout": (holdout_set.PAIRS, holdout_set.ORDERINGS),
    }
    out = {}
    for name, (pairs, rankings) in sets.items():
        pop = _touched_population(pairs, rankings)
        legs = {"off": None, **_idf_legs(pop)}
        cases = _eval_pairs(pairs, legs) + _eval_rankings(rankings, legs)
        out[name] = {
            "population_size": len(pop),
            "idf_downweighted_default": sorted(legs["on_default"]),
            "idf_downweighted_ge50": sorted(legs["on_ge50"]),
            "cases": cases,
            **_set_summary(cases),
        }
    return out


# --------------------------------------------------------------------------
# (b) the real corpus — decision table behind the index, identity-proven

def load_real_corpus(corpus_path=None):
    """The corpus as it exists at run time: corpus.json beside this
    module when present, else B2's build from sources."""
    here = os.path.dirname(os.path.abspath(__file__))
    path = corpus_path or os.path.join(here, "corpus.json")
    if os.path.exists(path):
        return corpus_mod.read_corpus(path), path
    return corpus_mod.build_corpus(), path


def _pair_key(a, b):
    return f"{a} <-> {b}"


def corpus_decision(vectors):
    """The decision table over one corpus' vectors {alias: vector}.
    Rankings run indexed (one shared index, all legs); the pair matrix
    is scored directly and cross-checked against those rankings."""
    aliases = sorted(vectors)
    pop = [vectors[a] for a in aliases]
    legs = {"off": None, **_idf_legs(pop)}
    index = m.build_index(vectors)

    # identity proof + surfaced sets, per leg, indexed vs naive — exact rows
    identity_legs, surfaced_ranked = {}, {}
    for leg, idf in legs.items():
        rows_compared, mismatches, surfaced = 0, [], set()
        for a in aliases:
            naive = m.rank_matches(vectors[a], vectors, self_name=a, idf=idf)
            fast = m.rank_matches_indexed(vectors[a], vectors, index=index,
                                          self_name=a, idf=idf)
            rows_compared += len(naive)
            if naive != fast:
                mismatches.append(a)
            for r in fast:
                surfaced.add(tuple(sorted((a, r["name"]))))
        identity_legs[leg] = {"rows_compared": rows_compared,
                              "identical": not mismatches,
                              "mismatches": mismatches}
        surfaced_ranked[leg] = surfaced

    # the pair matrix — every unordered pair, every leg
    pairs, surfaced_matrix = [], {leg: set() for leg in legs}
    for i, a in enumerate(aliases):
        for b in aliases[i + 1:]:
            row = {"a": a, "b": b, "pair": _pair_key(a, b)}
            for leg, idf in legs.items():
                r = m.score(vectors[a], vectors[b], idf=idf)
                row[f"score_{leg}"] = r["score"]
                row[f"surfaced_{leg}"] = r["surface"]
                if r["surface"]:
                    surfaced_matrix[leg].add((a, b))
            # the decision table's headline ON is the >=50% leg (§ header)
            row["score_on"] = row["score_on_ge50"]
            row["delta"] = row["score_on_ge50"] - row["score_off"]
            row["delta_default"] = row["score_on_default"] - row["score_off"]
            # "survived at >=50%" in HARDENING §5's sense: the pair still
            # surfaces under the >=50% threshold leg (the >=50% names the
            # threshold, not a score bar).
            row["survived_at_ge50"] = bool(row["surfaced_on_ge50"])
            row["surfaced_any"] = any(row[f"surfaced_{leg}"] for leg in legs)
            pairs.append(row)
    ranked_pairs = [r for r in pairs if r["surfaced_any"]]
    ranked_pairs.sort(key=lambda r: (-r["score_off"], r["pair"]))

    def top2(leg):
        top = sorted((r for r in pairs if r[f"surfaced_{leg}"]),
                     key=lambda r: (-r[f"score_{leg}"], r["pair"]))
        return [{"pair": r["pair"], "score": r[f"score_{leg}"]}
                for r in top[:2]]

    def names(pair_set):
        return sorted(_pair_key(a, b) for a, b in pair_set)

    aggregates = {
        "entities": len(aliases),
        "pairs_total": len(pairs),
        "pairs_surfaced_off": len(surfaced_matrix["off"]),
        "pairs_surfaced_on_default": len(surfaced_matrix["on_default"]),
        "pairs_surfaced_on_ge50": len(surfaced_matrix["on_ge50"]),
        "pairs_lost_default": names(surfaced_matrix["off"] - surfaced_matrix["on_default"]),
        "pairs_gained_default": names(surfaced_matrix["on_default"] - surfaced_matrix["off"]),
        "pairs_lost_ge50": names(surfaced_matrix["off"] - surfaced_matrix["on_ge50"]),
        "pairs_gained_ge50": names(surfaced_matrix["on_ge50"] - surfaced_matrix["off"]),
        "pairs_changed_ge50": sum(1 for r in pairs if r["delta"] != 0),
        "top2_off": top2("off"),
        "top2_on_default": top2("on_default"),
        "top2_on_ge50": top2("on_ge50"),
        "never_surfaced_pairs": sum(1 for r in pairs if not r["surfaced_any"]),
    }
    for leg in ("on_default", "on_ge50"):
        off_names = [t["pair"] for t in aggregates["top2_off"]]
        on_names = [t["pair"] for t in aggregates[f"top2_{leg}"]]
        aggregates[f"top2_set_stable_{leg}"] = set(off_names) == set(on_names)
        aggregates[f"top2_order_stable_{leg}"] = off_names == on_names
    deflated = sorted((r for r in pairs if r["delta"] < 0),
                      key=lambda r: (r["delta"], -r["score_off"], r["pair"]))
    aggregates["most_deflated_ge50"] = [
        {"pair": r["pair"], "score_off": r["score_off"],
         "score_on": r["score_on"], "delta": r["delta"]} for r in deflated[:5]]

    ubiq = ubiquity_table(vectors)
    return {
        "entity_count": len(aliases),
        "aliases": aliases,
        "idf_downweighted_default": sorted(legs["on_default"]),
        "idf_downweighted_ge50": sorted(legs["on_ge50"]),
        "ubiquity_table": [r for r in ubiq if r["share"] >= 0.25],
        "ubiquity_summary": {
            "distinct_tokens": len(ubiq),
            "tokens_over_50pct_strict": sorted(legs["on_default"]),
            "tokens_at_or_over_50pct": sorted(legs["on_ge50"]),
        },
        "identity_check": {
            "method": ("rank_matches_indexed vs rank_matches — exact row "
                       "equality, every entity, every leg"),
            "entities_checked": len(aliases),
            "legs": identity_legs,
            "identical": all(v["identical"] for v in identity_legs.values()),
            "rankings_match_pair_matrix": all(
                surfaced_ranked[leg] == surfaced_matrix[leg] for leg in legs),
        },
        "pairs": ranked_pairs,
        "aggregates": aggregates,
    }


# --------------------------------------------------------------------------
# the packet: facts + the standing rule — never a flipped default

def _summarize(labeled, real):
    agg = real["aggregates"]
    g, h = labeled["golden"], labeled["holdout"]
    facts = [
        f"Golden set ({g['scored_cases']} scored cases): accuracy OFF "
        f"{g['accuracy_off']}, ON at shipped defaults {g['accuracy_on_default']}, "
        f"ON at >=50% {g['accuracy_on_ge50']}.",
        f"Holdout ({h['scored_cases']} scored cases, synthetic): accuracy OFF "
        f"{h['accuracy_off']}, ON at shipped defaults {h['accuracy_on_default']}, "
        f"ON at >=50% {h['accuracy_on_ge50']}.",
        f"Real corpus ({agg['entities']} entities, {agg['pairs_total']} pairs): "
        f"IDF at shipped defaults down-weights "
        f"{len(real['idf_downweighted_default'])} token(s) "
        f"({', '.join(real['idf_downweighted_default']) or 'none'}) and surfaces "
        f"{agg['pairs_surfaced_on_default']} pairs vs {agg['pairs_surfaced_off']} OFF "
        f"(lost {len(agg['pairs_lost_default'])}, gained {len(agg['pairs_gained_default'])}).",
        f"Real corpus at the >=50% threshold: down-weights "
        f"{len(real['idf_downweighted_ge50'])} token(s) "
        f"({', '.join(real['idf_downweighted_ge50']) or 'none'}); "
        f"{agg['pairs_surfaced_on_ge50']} pairs surface "
        f"(lost {len(agg['pairs_lost_ge50'])}, gained {len(agg['pairs_gained_ge50'])}); "
        f"{agg['pairs_changed_ge50']} pair score(s) move; top-2 set "
        f"{'stable' if agg['top2_set_stable_on_ge50'] else 'CHANGED'}.",
        f"Indexed rankings are identical to naive rankings on this corpus "
        f"in every leg: {real['identity_check']['identical']}.",
    ]
    return {"facts": facts,
            "recommendation_rule": RECOMMENDATION_RULE,
            "decision_made": False,
            "default_changed": False}


def build_report(corpus_path=None):
    store, path = load_real_corpus(corpus_path)
    vectors = {a: e["vector"] for a, e in store["entities"].items()}
    labeled = evaluate_labeled_sets()
    real = corpus_decision(vectors)
    return {
        "artifact": ARTIFACT,
        "engine": ENGINE_ID,
        "generated_from": {
            "corpus_path": os.path.basename(path),
            "corpus_hash": corpus_mod.corpus_hash(store),
            "entity_count": store["entity_count"],
            "sources": store["sources"],
        },
        "idf": {"factor": IDF_FACTOR,
                "threshold_default": THRESHOLD_DEFAULT,
                "threshold_ge50_rule": ("(ceil(n/2) - 0.5) / n per population — "
                                        "tokens in at least half the population "
                                        "are down-weighted")},
        "labeled_sets": labeled,
        "real_corpus": real,
        "summary": _summarize(labeled, real),
    }


def report_bytes(report):
    return (json.dumps(report, indent=1, sort_keys=True) + "\n").encode("utf-8")


def write_report(report, path):
    with open(path, "wb") as fh:
        fh.write(report_bytes(report))
    return path


# --------------------------------------------------------------------------
# human-readable rendering

def _fmt_top2(rows):
    return ", ".join(f"{r['pair']} {r['score']}" for r in rows) or "(none)"


def render_text(report):
    lines = []
    src = report["generated_from"]
    lines.append(f"IDF DECISION HARNESS — {report['engine']} · "
                 f"corpus {src['corpus_path']} ({src['entity_count']} entities, "
                 f"hash {src['corpus_hash'][:12]}…)")
    lines.append("IDF is an optional mode, default OFF. This harness measures; "
                 "it does not decide and flips nothing.")
    lines.append("")
    for name in ("golden", "holdout"):
        s = report["labeled_sets"][name]
        lines.append(
            f"{name.upper()} ({s['scored_cases']} scored of {s['total_cases']} cases; "
            f"population {s['population_size']}): "
            f"accuracy OFF {s['accuracy_off']} · ON-default {s['accuracy_on_default']} "
            f"· ON->=50% {s['accuracy_on_ge50']} | verdict agreement vs OFF: "
            f"default {s['agreement_on_default']}, >=50% {s['agreement_on_ge50']}")
        diffs = [c for c in s["cases"]
                 if c["passed_on_ge50"] is False or c["passed_off"] is False]
        for c in diffs:
            lines.append(f"    note: {c['label']}: OFF "
                         f"{'pass' if c['passed_off'] else 'FAIL'} / >=50% "
                         f"{'pass' if c['passed_on_ge50'] else 'FAIL'}")
    lines.append("")
    real, agg = report["real_corpus"], report["real_corpus"]["aggregates"]
    lines.append(f"REAL CORPUS DECISION TABLE — {agg['entities']} entities, "
                 f"{agg['pairs_total']} pairs, {len(real['pairs'])} surfaced in any leg, "
                 f"{agg['never_surfaced_pairs']} never surface")
    lines.append(f"  down-weighted at shipped defaults: "
                 f"{', '.join(real['idf_downweighted_default']) or '(none)'}")
    lines.append(f"  down-weighted at >=50%: "
                 f"{', '.join(real['idf_downweighted_ge50']) or '(none)'}")
    lines.append(f"  {'pair':44} {'off':>4} {'on-def':>6} {'on->=50':>7} {'delta':>6}  survived->=50%")
    for r in real["pairs"]:
        lines.append(f"  {r['pair']:44} {r['score_off']:>4} "
                     f"{r['score_on_default']:>6} {r['score_on']:>7} "
                     f"{r['delta']:>+6}  {'yes' if r['survived_at_ge50'] else 'no'}")
    lines.append("")
    lines.append("AGGREGATES")
    lines.append(f"  pairs surfaced: OFF {agg['pairs_surfaced_off']} · "
                 f"ON-default {agg['pairs_surfaced_on_default']} · "
                 f"ON->=50% {agg['pairs_surfaced_on_ge50']}")
    lines.append(f"  pairs lost/gained (default): {agg['pairs_lost_default'] or '[]'} / "
                 f"{agg['pairs_gained_default'] or '[]'}")
    lines.append(f"  pairs lost/gained (>=50%): {agg['pairs_lost_ge50'] or '[]'} / "
                 f"{agg['pairs_gained_ge50'] or '[]'}")
    lines.append(f"  top-2 OFF: {_fmt_top2(agg['top2_off'])}")
    lines.append(f"  top-2 ON-default: {_fmt_top2(agg['top2_on_default'])} "
                 f"(set stable: {agg['top2_set_stable_on_default']})")
    lines.append(f"  top-2 ON->=50%: {_fmt_top2(agg['top2_on_ge50'])} "
                 f"(set stable: {agg['top2_set_stable_on_ge50']}, "
                 f"order stable: {agg['top2_order_stable_on_ge50']})")
    lines.append("  most deflated (>=50%): " + (
        ", ".join(f"{d['pair']} {d['score_off']}->{d['score_on']} ({d['delta']:+d})"
                  for d in agg["most_deflated_ge50"]) or "(none)"))
    ic = real["identity_check"]
    lines.append(f"  identity: indexed == naive on all {ic['entities_checked']} "
                 f"entities in every leg: {ic['identical']}; "
                 f"rankings match pair matrix: {ic['rankings_match_pair_matrix']}")
    lines.append("")
    lines.append("SUMMARY — measured facts")
    for f in report["summary"]["facts"]:
        lines.append(f"  - {f}")
    lines.append(f"  Standing rule: {report['summary']['recommendation_rule']}")
    return "\n".join(lines) + "\n"


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    here = os.path.dirname(os.path.abspath(__file__))
    corpus_path = argv[0] if len(argv) >= 1 else os.path.join(here, "corpus.json")
    out_path = argv[1] if len(argv) >= 2 else os.path.join(here, "idf_decision.json")
    report = build_report(corpus_path)
    write_report(report, out_path)
    print(render_text(report), end="")
    print(f"[idf_decision.json written -> {out_path}]")
    return 0


if __name__ == "__main__":
    sys.exit(main())

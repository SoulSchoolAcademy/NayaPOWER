#!/usr/bin/env python3
"""lexicon_inventory.py — per query: gold arm-score, query tokens, and which
literal lexicon words (exact stemmed forms) the query carries. Guides v2 authoring."""
import json, os, sys, importlib.util

HERE = os.path.dirname(os.path.abspath(__file__))
arms_dir = os.path.expanduser("~/workspace/goals/bring-naya-to-life/hidden_files/arms")
for name, var in [("lexical-t0412", "lex")]:
    spec = importlib.util.spec_from_file_location(var, os.path.join(arms_dir, name, "arm.py"))
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    globals()[var] = mod

docs = {d["id"]: d for d in json.load(open(os.path.join(HERE, "corpus_v4-semantic.json")))["docs"]}
queries = json.load(open(os.path.join(HERE, "queries_v4.json")))

SETS = {"ACT": lex._STEMMED["act"], "TRAP": lex._STEMMED["trap"], "DEC": lex._STEMMED["dec"]}
RAW = {"ACT": lex.CHECK_ACTION, "TRAP": lex.TRAP, "DEC": lex.DECIDE}

for q in queries:
    qtoks = lex.tokenize(q["text"])
    inv = {}
    for t in qtoks:
        for sname, s in SETS.items():
            if t in s:
                # find literal raw words that stem to t
                lits = sorted({w for w in RAW[sname] if lex.stem(w.replace("-", " ")) == t})
                inv.setdefault(sname, []).append((t, lits))
    gs = sum(lex._feature_scores(docs[q["gold"]]["text"], q["text"]))
    print("%s S_gold=%d | qtoks=%s" % (q["qid"], gs, qtoks))
    for sname, items in inv.items():
        parts = ["%s<-%s" % (t, ",".join(lits[:3])) for t, lits in items]
        print("    %s: %s" % (sname, "; ".join(parts)))
    if not inv:
        print("    (no lexicon stems in query — p_act path only: doc needs 2+ ACT words for S>=1)")

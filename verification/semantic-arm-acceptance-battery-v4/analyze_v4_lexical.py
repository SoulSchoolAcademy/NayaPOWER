#!/usr/bin/env python3
"""analyze_v4_lexical.py — diagnostic (not part of the battery).
For each v4 query: the ACTUAL lexical-t0412 feature scores (q1+q2+q3) and the
v3-replicated overlap_lex, gold vs distractors. Names exactly why lexical got 17/20.
"""
import json, os, sys, importlib.util, re
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
# reuse the v3 replication from the builder by exec (it has no import side effects)
src = open(os.path.join(HERE, "build_corpus_v4.py")).read()
ns = {"__file__": os.path.join(HERE, "build_corpus_v4.py")}
exec(src.split("# PROVENANCE")[0], ns)
overlap_lex = ns["overlap_lex"]
v3_toks = ns["v3_toks"]

arms_dir = os.path.expanduser("~/workspace/goals/bring-naya-to-life/hidden_files/arms")
spec = importlib.util.spec_from_file_location("lex", os.path.join(arms_dir, "lexical-t0412", "arm.py"))
lex = importlib.util.module_from_spec(spec); spec.loader.exec_module(lex)

docs = {d["id"]: d for d in json.load(open(os.path.join(HERE, "corpus_v4-semantic.json")))["docs"]}
queries = json.load(open(os.path.join(HERE, "queries_v4.json")))

def arm_score(qtext, dtext):
    return sum(lex._feature_scores(dtext, qtext))

print("qid split   trap | gold_arm gold_v3 | dist_arm(mean/max) dist_v3(mean/max) | lex_rank1")
tot = {"cal": [0, 0], "acc": [0, 0]}
for q in queries:
    g = docs[q["gold"]]
    gs = arm_score(q["text"], g["text"]); gv = overlap_lex(q["text"], g["text"])
    dss, dvs = [], []
    for did in q["field"][1:]:
        d = docs[did]
        dss.append(arm_score(q["text"], d["text"]))
        dvs.append(overlap_lex(q["text"], d["text"]))
    field = [{"id": did, "text": docs[did]["text"]} for did in q["field"]]
    r = lex.rank(q["text"], field)
    hit = 1 if r[0] == q["gold"] else 0
    k = "cal" if q["split"] == "calibration" else "acc"
    tot[k][1] += 1; tot[k][0] += hit
    flag = " <<<< LEX MISS" if not hit else ""
    print("%s %-11s %s | %2d %5d | %4.1f/%2d %6.1f/%2d | %s%s" % (
        q["qid"], q["split"], "T" if q["trap"] else ".",
        gs, gv,
        sum(dss)/len(dss), max(dss), sum(dvs)/len(dvs), max(dvs),
        "GOLD" if hit else r[0], flag))
print("lexical P1: calibration %d/%d, acceptance %d/%d" % (
    tot["cal"][0], tot["cal"][1], tot["acc"][0], tot["acc"][1]))
# how many queries have gold arm-score strictly greater than every distractor?
strict = sum(1 for q in queries if all(
    arm_score(q["text"], docs[q["gold"]]["text"]) >
    arm_score(q["text"], docs[did]["text"]) for did in q["field"][1:]))
print("queries where gold strictly outscores every distractor (arm measure): %d/40" % strict)
strict_v3 = sum(1 for q in queries if all(
    overlap_lex(q["text"], docs[q["gold"]]["text"]) >
    overlap_lex(q["text"], docs[did]["text"]) for did in q["field"][1:]))
print("queries where gold strictly outscores every distractor (v3 measure): %d/40" % strict_v3)

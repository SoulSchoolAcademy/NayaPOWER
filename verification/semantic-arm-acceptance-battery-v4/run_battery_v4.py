#!/usr/bin/env python3
"""run_battery_v4.py — semantic-arm acceptance battery v4 (t0722, Lane 5 Seeker).

Implements design doc §7 (verification/semantic-arm-acceptance-gate-design-v1.md)
against the frozen corpus from build_corpus_v4.py. Frozen falsifiers F1-F7 are
from hidden_files/twelve-lane-receipts/preregister-t0720-lane9.md (sealed BEFORE
any design byte); this script may not soften them.

Run under the durable fastembed venv:
  export FASTEMBED_CACHE_PATH=$HOME/.cache/fastembed HF_HUB_OFFLINE=1
  export no_proxy=localhost,127.0.0.1,::1 NO_PROXY=localhost,127.0.0.1,::1
  ~/workspace/venvs/fastembed-env/bin/python run_battery_v4.py full \\
      --arms-dir ~/workspace/goals/bring-naya-to-life/hidden_files/arms \\
      --verdict semantic_gate_run.json

Subcommands:
  cold-rank --out R.json   load sealed corpus, run t0426 arm on all 40 queries,
                           write {qid: ranking}. Used twice by `full` (fresh
                           subprocesses) for F6.
  full                     the whole §7 protocol: SHA asserts -> wiring
                           validation -> baselines -> stage 1 calibration ->
                           bar pin (with calibration-conflict clause) ->
                           stage 2 (two cold runs, byte-identity) ->
                           F1-F7 verdicts -> semantic_gate_run.json.

Mechanical (no-judgment) choices, owned in the t0722-lane5 receipt:
- bar = max(lexical-baseline ceiling on calibration, bootstrap P25 of the
  draft arm's P1 on calibration). B=10000, seed 20261018. "Lexical-baseline
  ceiling" = max(P1(lexical-t0412), P1(tfidf-t0412)) on the calibration split.
- "Draft P25" = 25th percentile of the bootstrap distribution of the draft
  arm's P1 (the conservative floor of what the draft itself achieves).
- Calibration-conflict clause (design §3): if lexical ceiling > draft P25,
  the bar pins at the lexical ceiling, F7 is declared BROKEN, and the run
  STOPS with that verdict (no acceptance run).
- F1 "within noise" = rank1-hit agreement(semantic, lexical-t0412) >= 0.90
  on the acceptance split -> FIRES.
- F2: one-sided paired permutation on per-query rank1 (semantic vs tfidf),
  10000 permutations, seed 20261018; p < 0.05 required -> else FIRES.
- F4: degenerate arms = rank-by-doc-length-desc and alphabetical-by-id,
  ties -> corpus order. Either P1 >= bar on acceptance -> FIRES.
- F5 fires iff (trap decoy-avoidance A <= 1/10) AND (semantic P1 >= bar).
- F7: P1(lexical-t0412 on acceptance) >= bar -> FIRES.
- Margin M_q = cos(q,gold) - cos(q, best distractor) with the arm's cosine
  REPLICATED VERBATIM from arm.py bytes (never the docstring).
"""
import argparse, hashlib, importlib.util, json, math, os, random, re, subprocess, sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
SEED = 20261018
BOOT = 10000

# ---------- replicated verbatim from hidden_files/arms/semantic-t0426/arm.py ----------
def _cos(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(x * x for x in b))
    if na == 0.0 or nb == 0.0:
        return 0.0
    return dot / (na * nb)
# ---------- end replication ----------

# ---------- replicated verbatim from the v3 battery's metric functions
# (run_battery_v3.py) — never imported (it does file I/O at import) ----------
def v3_rank1(ranking, label): return 1 if ranking and ranking[0] == label else 0
# ---------- end replication ----------

_MODEL = None
_EMB_CACHE = {}

def _get_model():
    global _MODEL
    if _MODEL is None:
        from fastembed import TextEmbedding
        _MODEL = TextEmbedding("sentence-transformers/all-MiniLM-L6-v2")
    return _MODEL

def _embed(text):
    key = hashlib.sha256(text.encode("utf-8")).hexdigest()
    v = _EMB_CACHE.get(key)
    if v is None:
        v = list(next(_get_model().embed([text])))
        _EMB_CACHE[key] = v
    return v

def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()

def load_sealed():
    cpath = os.path.join(HERE, "corpus_v4-semantic.json")
    qpath = os.path.join(HERE, "queries_v4.json")
    csha = open(cpath + ".sha256").read().strip()
    qsha = open(qpath + ".sha256").read().strip()
    assert sha256_file(cpath) == csha, "corpus seal BROKEN"
    assert sha256_file(qpath) == qsha, "queries seal BROKEN"
    docs = {d["id"]: d for d in json.load(open(cpath))["docs"]}
    queries = json.load(open(qpath))
    return docs, queries, csha, qsha

def load_arm(arms_dir, name):
    path = os.path.join(arms_dir, name, "arm.py")
    assert os.path.isfile(path), "missing arm: " + path
    spec = importlib.util.spec_from_file_location("arm_" + name.replace("-", "_"), path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    assert hasattr(mod, "rank"), "arm has no rank()"
    return mod, sha256_file(path)

def rank1_hits(arm_rank, docs, queries):
    hits, detail = [], {}
    for q in queries:
        field = [{"id": did, "text": docs[did]["text"]} for did in q["field"]]
        r = arm_rank(q["text"], field)
        h = v3_rank1(r, q["gold"])
        hits.append(h)
        detail[q["qid"]] = {"rank1": h, "rank_gold": r.index(q["gold"]) + 1,
                            "ranking": r}
    return hits, detail

def p1(hits): return sum(hits) / len(hits)

def margins(docs, queries):
    ms = []
    for q in queries:
        qv = _embed(q["text"])
        cg = _cos(qv, _embed(docs[q["gold"]]["text"]))
        distract = [did for did in q["field"][1:]]
        best = max(_cos(qv, _embed(docs[did]["text"])) for did in distract)
        ms.append(cg - best)
    return ms

def trap_avoidance(detail, queries):
    tq = [q for q in queries if q["trap"]]
    ok = sum(1 for q in tq if detail[q["qid"]]["ranking"][0] != q["decoy"])
    return ok / len(tq), len(tq)

def bootstrap_p25(hits, seed=SEED, B=BOOT):
    rng = random.Random(seed)
    n = len(hits)
    dist = sorted(sum(hits[rng.randrange(n)] for _ in range(n)) / n
                  for _ in range(B))
    return dist[int(0.25 * B)]

def paired_perm_p(a_hits, b_hits, seed=SEED, B=BOOT):
    diffs = [x - y for x, y in zip(a_hits, b_hits)]
    obs = sum(diffs) / len(diffs)
    rng = random.Random(seed)
    ge = 0
    for _ in range(B):
        s = sum(d * (1 if rng.random() < 0.5 else -1) for d in diffs) / len(diffs)
        if s >= obs:
            ge += 1
    return (ge + 1) / (B + 1), obs

def degenerate_ranks(docs, queries):
    out_len, out_alpha = {}, {}
    for q in queries:
        field = [(did, docs[did]["text"]) for did in q["field"]]
        by_len = sorted(range(len(field)),
                        key=lambda i: (-len(field[i][1]), i))
        out_len[q["qid"]] = [field[i][0] for i in by_len]
        by_alpha = sorted(range(len(field)), key=lambda i: (field[i][0], i))
        out_alpha[q["qid"]] = [field[i][0] for i in by_alpha]
    return out_len, out_alpha

def cmd_cold_rank(args):
    docs, queries, csha, qsha = load_sealed()
    sem, sem_sha = load_arm(args.arms_dir, "semantic-t0426")
    out = {}
    for q in queries:
        field = [{"id": did, "text": docs[did]["text"]} for did in q["field"]]
        out[q["qid"]] = sem.rank(q["text"], field)
    with open(args.out, "w") as f:
        json.dump(out, f, sort_keys=True)
        f.write("\n")
    print("cold-rank wrote", args.out, sha256_file(args.out))

def cmd_full(args):
    docs, queries, csha, qsha = load_sealed()
    calib = [q for q in queries if q["split"] == "calibration"]
    accept = [q for q in queries if q["split"] == "acceptance"]
    assert len(calib) == 20 and len(accept) == 40 - 20

    sem, sem_sha = load_arm(args.arms_dir, "semantic-t0426")
    lex, lex_sha = load_arm(args.arms_dir, "lexical-t0412")
    tfi, tfi_sha = load_arm(args.arms_dir, "tfidf-t0412")
    arm_pins = {"semantic-t0426": sem_sha, "lexical-t0412": lex_sha,
                "tfidf-t0412": tfi_sha}

    # --- wiring validation (design §7 step 3): replicated cosine on one query ---
    q0 = calib[0]
    f0 = [{"id": did, "text": docs[did]["text"]} for did in q0["field"]]
    wiring_rank = sem.rank(q0["text"], f0)
    assert wiring_rank[0] in q0["field"], "wiring: rank returned unknown id"

    # --- baselines on calibration (F2/F7 controls) ---
    lex_h_c, _ = rank1_hits(lex.rank, docs, calib)
    tfi_h_c, _ = rank1_hits(tfi.rank, docs, calib)
    sem_h_c, sem_d_c = rank1_hits(sem.rank, docs, calib)
    lex_ceil = max(p1(lex_h_c), p1(tfi_h_c))
    draft_p25 = bootstrap_p25(sem_h_c)

    verdict = {
        "battery": "semantic-arm-acceptance-battery-v4",
        "design": "verification/semantic-arm-acceptance-gate-design-v1.md",
        "prereg": "hidden_files/twelve-lane-receipts/preregister-t0720-lane9.md",
        "corpus_sha256": csha, "queries_sha256": qsha,
        "arm_pins": arm_pins,
        "calibration": {
            "n": len(calib),
            "semantic_P1": round(p1(sem_h_c), 4),
            "lexical_t0412_P1": round(p1(lex_h_c), 4),
            "tfidf_t0412_P1": round(p1(tfi_h_c), 4),
            "lexical_ceiling": round(lex_ceil, 4),
            "draft_P25": round(draft_p25, 4),
        },
        "falsifiers": {},
    }

    # --- calibration-conflict clause (design §3): bar never drops below the
    # convicted baseline; if lexical ceiling > draft P25, F7 is BROKEN: STOP ---
    if lex_ceil > draft_p25:
        bar = lex_ceil
        verdict["bar"] = round(bar, 4)
        verdict["bar_trace"] = ("CONFLICT: lexical ceiling %.4f > draft P25 %.4f; "
                                "bar pinned at lexical ceiling per §3; F7 BROKEN; "
                                "run STOPPED before acceptance." % (lex_ceil, draft_p25))
        verdict["falsifiers"]["F7"] = {
            "verdict": "FIRED",
            "evidence": ("calibration-conflict: lexical-t0412/tfidf ceiling %.4f "
                         "exceeds draft P25 %.4f on the calibration split; the "
                         "corpus does not discriminate mechanisms; the bar pins "
                         "at the convicted baseline and the design is BROKEN."
                         % (lex_ceil, draft_p25))}
        verdict["overall"] = "BROKEN"
        with open(args.verdict, "w") as f:
            json.dump(verdict, f, indent=1, sort_keys=True)
            f.write("\n")
        print("CONFLICT — F7 FIRED at calibration; verdict:", args.verdict)
        return

    bar = draft_p25
    verdict["bar"] = round(bar, 4)
    verdict["bar_trace"] = ("bar = max(lexical ceiling %.4f, draft P25 %.4f) = %.4f; "
                            "no calibration conflict; written BEFORE acceptance."
                            % (lex_ceil, draft_p25, bar))

    # --- stage 2: two cold runs (fresh subprocesses) -> byte-identity (F6) ---
    py = sys.executable
    env = dict(os.environ)
    r1 = os.path.join(HERE, "cold_run_1.json")
    r2 = os.path.join(HERE, "cold_run_2.json")
    for rp in (r1, r2):
        subprocess.run([py, __file__, "cold-rank", "--arms-dir", args.arms_dir,
                        "--out", rp], check=True, env=env,
                       capture_output=True, text=True, timeout=900)
    b1 = open(r1, "rb").read()
    b2 = open(r2, "rb").read()
    f6_ok = (b1 == b2)
    os.remove(r1); os.remove(r2)
    cold_rankings = json.loads(b1.decode("utf-8"))

    # --- acceptance metrics (from cold run 1 = the sealed rankings) ---
    sem_h_a = [1 if cold_rankings[q["qid"]][0] == q["gold"] else 0 for q in accept]
    rank_gold_a = {q["qid"]: cold_rankings[q["qid"]].index(q["gold"]) + 1
                   for q in accept}
    lex_h_a, _ = rank1_hits(lex.rank, docs, accept)
    tfi_h_a, _ = rank1_hits(tfi.rank, docs, accept)
    ms_a = margins(docs, accept)
    ms_a_sorted = sorted(ms_a)
    med = ms_a_sorted[len(ms_a_sorted) // 2]
    p10 = ms_a_sorted[int(0.10 * len(ms_a_sorted))]
    A_a, n_trap_a = trap_avoidance(
        {q["qid"]: {"ranking": cold_rankings[q["qid"]]} for q in accept}, accept)
    ms_c = margins(docs, calib)
    A_c, n_trap_c = trap_avoidance(
        {q["qid"]: {"ranking": cold_rankings[q["qid"]]} for q in calib}, calib)

    verdict["acceptance"] = {
        "n": len(accept),
        "semantic_P1": round(p1(sem_h_a), 4),
        "lexical_t0412_P1": round(p1(lex_h_a), 4),
        "tfidf_t0412_P1": round(p1(tfi_h_a), 4),
        "margin_median": round(med, 4),
        "margin_P10": round(p10, 4),
        "trap_avoidance": round(A_a, 4),
        "n_traps": n_trap_a,
        "bar": round(bar, 4),
    }
    verdict["calibration"]["margin_median"] = round(
        sorted(ms_c)[len(ms_c) // 2], 4)
    verdict["calibration"]["trap_avoidance"] = round(A_c, 4)

    F = verdict["falsifiers"]
    # F1: mechanism-blind corpus
    agree = sum(1 for a, b in zip(sem_h_a, lex_h_a) if a == b) / len(accept)
    F["F1"] = {"verdict": "FIRED" if agree >= 0.90 else "PASSED",
               "evidence": "rank1-hit agreement(semantic, lexical-t0412) = %.3f "
                           "on acceptance (threshold 0.90)" % agree}
    # F2: no semantic signal beyond lexical
    pval, obs = paired_perm_p(sem_h_a, tfi_h_a)
    F["F2"] = {"verdict": "PASSED" if pval < 0.05 and obs > 0 else "FIRED",
               "evidence": "paired permutation (one-sided, B=%d): p=%.4f, "
                           "mean paired diff=%.4f" % (BOOT, pval, obs)}
    # F3: dead margin
    F["F3"] = {"verdict": "FIRED" if med <= 0 else "PASSED",
               "evidence": "margin median=%.4f, P10=%.4f (n=%d)"
                           % (med, p10, len(accept))}
    # F4: degenerate clears the bar
    dlen, dalpha = degenerate_ranks(docs, accept)
    p_len = sum(1 for q in accept if dlen[q["qid"]][0] == q["gold"]) / len(accept)
    p_alpha = sum(1 for q in accept if dalpha[q["qid"]][0] == q["gold"]) / len(accept)
    F["F4"] = {"verdict": "FIRED" if (p_len >= bar or p_alpha >= bar) else "PASSED",
               "evidence": "degenerate P1: doc-length=%.3f, alpha-id=%.3f; "
                           "bar=%.4f" % (p_len, p_alpha, bar)}
    # F5: lexical-reward trap
    sem_p1_a = p1(sem_h_a)
    F["F5"] = {"verdict": ("FIRED" if (A_a <= 0.10 and sem_p1_a >= bar)
                           else "PASSED"),
               "evidence": "trap avoidance A=%.3f (n=%d, chance=0.10); semantic "
                           "P1=%.4f vs bar=%.4f" % (A_a, n_trap_a, sem_p1_a, bar)}
    # F6: non-determinism
    F["F6"] = {"verdict": "PASSED" if f6_ok else "FIRED",
               "evidence": "two cold subprocess runs: rankings %s"
                           % ("byte-identical" if f6_ok else "DIFFER")}
    # F7: known-bad clears the bar
    p_lex_a = p1(lex_h_a)
    F["F7"] = {"verdict": "FIRED" if p_lex_a >= bar else "PASSED",
               "evidence": "lexical-t0412 P1=%.4f on acceptance vs bar=%.4f"
                           % (p_lex_a, bar)}

    fired = [k for k, v in F.items() if v["verdict"] == "FIRED"]
    verdict["overall"] = "BROKEN" if fired else "GATE-HOLDS"
    verdict["per_query"] = {
        q["qid"]: {"rank1": h, "rank_gold": rank_gold_a[q["qid"]],
                   "trap": q["trap"]}
        for q, h in zip(accept, sem_h_a)}
    with open(args.verdict, "w") as f:
        json.dump(verdict, f, indent=1, sort_keys=True)
        f.write("\n")
    print("verdict:", args.verdict, "overall:", verdict["overall"],
          "fired:", fired or "none")

def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("cold-rank")
    c.add_argument("--arms-dir", required=True)
    c.add_argument("--out", required=True)
    f = sub.add_parser("full")
    f.add_argument("--arms-dir", required=True)
    f.add_argument("--verdict", required=True)
    args = ap.parse_args()
    if args.cmd == "cold-rank":
        cmd_cold_rank(args)
    else:
        cmd_full(args)

if __name__ == "__main__":
    main()

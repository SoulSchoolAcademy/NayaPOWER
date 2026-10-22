#!/usr/bin/env python3
"""
build_t0412_baseline_battery.py — derive the t0412 baseline battery + both
reference arms FROM LIVE BYTES (Lane 9, t0787).

Sources (all re-read at build time, never inherited):
  corpus   = auto-retrieval-proto.py :: load_principles()   (P1..P15)
  queries  = lane-experiments/t0402/auto-retrieval/judge-packet.md
             (exact frozen brief bytes, slice-3's extract_briefs logic)
  expected = lane-experiments/t0402/auto-retrieval/ground-truth-FROZEN.md
             (the frozen expected-set table, parsed by regex)

Outputs:
  batteries/t0412-baseline/corpus/{corpus.json, corpus.sha256}   (PINNED)
  batteries/t0412-baseline/queries.json   (text=proto.clean_brief of the
                                          original brief file;
                                          query_note records the
                                          stripped flag; packet order;
                                          GT written expected order)
  batteries/t0412-baseline/rubric.md
  arms/tfidf-t0412/{arm.py, arm_manifest.json}      (self-contained: exact
                                                    proto TF-IDF, stdlib)
  arms/lexical-t0412/{arm.py, arm_manifest.json}    (self-contained: exact
                                                    t0412 slice-3 Q1/Q2/Q3)

Arm self-containment is deliberate: an arm is a sealed instrument — it must
NOT import the proto or the frozen records (the arm's input space holds only
what the harness passes it: query_text + docs). The slice-3 tie-break (frozen
packet order J01..J15) is NOT copied: it depends on judge-map-SEALED.json,
which is answer-key-adjacent material (t0761-lane11 class) and must never sit
in an arm's readable space. TIE-BREAK CORRECTION (t0807, verified t2200):
the two arms do NOT share a tie-break. tfidf-t0412 sorts (score, index)
tuples with reverse=True — ties break by REVERSE corpus order (P15 first),
verified empirically on identical-text docs. lexical-t0412 sorts
(-score, order, id) ascending — ties break by corpus order (P1 first),
verified empirically on identical-text docs (t2200). Neither matches
t0412's frozen packet order (J01..J15 via the sealed map), which is
answer-key-adjacent and unreproducible by design — so there is no single
"declared tie-break delta" between these arms and the t0412 numbers.
OBSERVED pins: batteries/t0412-v2-rank/manifest.json -> tie_break
(tfidf-t0412: REVERSE corpus order, P15 first; lexical-t0412: corpus
order, P1 first; both re-verified on live bytes 2026-10-18, gap-t0807-lane9).
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import re

BASE = os.path.dirname(os.path.abspath(__file__))
HF = os.path.dirname(BASE)

PROTO = os.path.join(HF, "auto-retrieval-proto.py")
spec = importlib.util.spec_from_file_location("proto", PROTO)
proto = importlib.util.module_from_spec(spec)
spec.loader.exec_module(proto)

T0402 = os.path.join(HF, "lane-experiments", "t0402", "auto-retrieval")
PACKET = os.path.join(T0402, "judge-packet.md")
GT = os.path.join(T0402, "ground-truth-FROZEN.md")

OUT_BAT = os.path.join(HF, "batteries", "t0412-baseline")
OUT_CORPUS = os.path.join(OUT_BAT, "corpus")
ARM_TFIDF = os.path.join(HF, "arms", "tfidf-t0412")
ARM_LEX = os.path.join(HF, "arms", "lexical-t0412")


def extract_briefs(packet_path: str) -> dict[str, str]:
    raw = open(packet_path, encoding="utf-8").read()
    parts = re.split(r"^## BRIEF: (\S+)\s*$", raw, flags=re.M)
    briefs = {}
    for i in range(1, len(parts), 2):
        briefs[parts[i].strip()] = parts[i + 1].strip()
    return briefs


def extract_expected(gt_path: str) -> dict[str, list[str]]:
    # Written order is preserved (NOT numeric-sorted): the frozen table's
    # {P2, P1, P7} stays [P2, P1, P7] — the on-disk battery's order, which the
    # t0787 harness proof ran on.
    raw = open(gt_path, encoding="utf-8").read()
    out = {}
    for m in re.finditer(r"^\|\s*(brief-[\w.-]+)\s*\|\s*\{([^}]*)\}", raw, flags=re.M):
        brief, ids = m.groups()
        out[brief] = re.findall(r"P\d{1,2}", ids)
    return out


# ------------------------------------------------------------------ corpus --
principles = proto.load_principles()
assert [p["id"] for p in principles] == [f"P{i}" for i in range(1, 16)]
corpus = [{"id": p["id"], "text": p["text"]} for p in principles]
os.makedirs(OUT_CORPUS, exist_ok=True)
corpus_path = os.path.join(OUT_CORPUS, "corpus.json")
with open(corpus_path, "w", encoding="utf-8") as f:
    json.dump(corpus, f, indent=2, ensure_ascii=False)
pin = hashlib.sha256(open(corpus_path, "rb").read()).hexdigest()
with open(os.path.join(OUT_CORPUS, "corpus.sha256"), "w") as f:
    f.write(pin + "\n")

# ------------------------------------------------------------------ queries --
# Query text = proto.clean_brief applied to the ORIGINAL brief files
# (briefs/<id>) — the t0787 harness proof runs BOTH arms on ONE query set:
# the cleaned originals, the non-circular query text the original TF-IDF used
# (see rubric's "Proof query text" section). clean_brief returns
# (text, was_stripped); the flag is recorded per query in query_note.
# Order = the packet's brief order (insertion order, NOT sorted).
briefs = extract_briefs(PACKET)
expected = extract_expected(GT)
assert set(briefs) == set(expected) == {
    "brief-t0382-lane3.md", "brief-t0382-lane9.md", "brief-t0392-lane2.md",
    "brief-t0402-lane9.md", "brief-t0392-lane7.md"}, sorted(briefs)
assert sum(len(v) for v in expected.values()) == 10
BRIEFS_DIR = os.path.join(HF, "briefs")
queries = []
for b in briefs:  # packet order
    orig = open(os.path.join(BRIEFS_DIR, b), encoding="utf-8").read()
    cleaned, stripped = proto.clean_brief(orig)
    queries.append({"id": b, "text": cleaned, "expected": expected[b],
                    "query_note": f"original brief file, clean_brief stripped={stripped}"})
with open(os.path.join(OUT_BAT, "queries.json"), "w", encoding="utf-8") as f:
    json.dump(queries, f, indent=2, ensure_ascii=False)

# ------------------------------------------------------------------ rubric --
# FROZEN (t0787 deviation declaration, hand-authored 2026-10-17, adopted
# by the builder 2026-10-22 so regeneration is byte-exact): the rubric is
# the frozen documentation of the t0787 harness run — measured numbers,
# the VOID tolerance correction, and the proof-query-text deviation. It
# is NOT re-derived from live bytes; the builder owns it verbatim.
RUBRIC_FROZEN = """# t0412 baseline — frozen rubric (derived from ground-truth-FROZEN.md)

Metric: per (brief x expected principle), rank of the expected principle.
MRR = mean(1/rank) over the 10 expected pairs. Top-5 hit count. The P10
decisive sub-test: rank of P10 on brief-t0392-lane2 (t0412 TF-IDF: absent
from top-5; the arm that recovers P10 has the judge's edge).

Reference numbers (t0412-lane2 receipt, t0412 frozen run):
  MRR judge 0.567 | TF-IDF 0.502 | lexical AUTO 0.426
Direction under test: TF-IDF beats lexical (0.502 > 0.426).
Reproduction tolerance (named, VOID — corrected t2200): direction holds AND
each arm's MRR within ±0.03 of its t0412 reference. The ±0.03 was justified
as covering "the declared tie-break delta (corpus order P1..P15 here vs
frozen packet order J01..J15 in t0412)" — that declaration was FALSE for the
tfidf arm (reverse corpus order, empirical t0807/t2200), and the two arms do
not share a tie-break with each other. The t0412 references were measured
under t0412's frozen packet order, which is unreproducible by design (sealed
map, answer-key-adjacent): they stand as the frozen historical record, NOT
as reproduction targets for these arms. Measured on this battery: lexical
0.4829 (delta +0.0569 vs 0.426 — outside ±0.03), TF-IDF 0.4733 (delta -0.0267
vs 0.502 — inside ±0.03); direction TF-IDF > lexical does NOT reproduce
(0.4733 < 0.4829). The P10 sub-test does not discriminate either: current
tfidf ranks P10 at 6 on brief-t0392-lane2 (absent from top-5, as in t0412),
lexical at 14 — neither recovers it.

## Proof query text (declared deviation, t0787 harness run)
The t0412 instruments used different query texts (TF-IDF: cleaned original
brief files; lexical AUTO: packet-extracted masked briefs). The harness proof
runs BOTH arms on ONE query set so the numbers are comparable — the whole
point of the instrument. Chosen: cleaned original brief files
(proto.clean_brief — the non-circular query text the original TF-IDF used).
The packet-extract set is preserved as queries-packet-extracts.json.
Deviation effect (measured): lexical MRR on packet extracts = 0.4829 (run
lexical-v1); the tie-break + query-text deltas vs t0412's 0.426 are named,
not hidden.
"""
with open(os.path.join(OUT_BAT, "rubric.md"), "w", encoding="utf-8") as f:
    f.write(RUBRIC_FROZEN)


# ------------------------------------------------------------------ arms ---
PRELUDE = '''"""Self-contained reference arm for the semantic_arm_harness.
Input space is SEALED: the harness calls rank(query_text, docs) and passes
ONLY those two values. Labels (queries.json "expected") are never in this
directory and never reach rank(). (t0761-lane11 answer-key-leak class.)
Stdlib only: math, re, collections.
"""'''

TOKENIZE_SRC = '''
STOP = set(
    """a an and are as at be been by for from has had have he her his how i if
    in into is it its of on or s t that the their them then there these they
    this to was we were will with would you your ours our us so such than too
    very can just but not no all any each other some what which who whom whose
    when where why about over under again once here do does did doing done""".split()
)

TOKEN_RE = re.compile(r"[a-z0-9]+(?:'[a-z]+)?")


def stem(w):
    if len(w) <= 4:
        return w
    if w.endswith("ing") and len(w) > 6:
        w = w[:-3]
    elif w.endswith("edly"):
        w = w[:-4]
    elif w.endswith("ed") and len(w) > 5:
        w = w[:-2]
    elif w.endswith("ies") and len(w) > 5:
        w = w[:-3] + "y"
    elif w.endswith("es") and len(w) > 5:
        w = w[:-2]
    elif w.endswith("s") and len(w) > 4:
        w = w[:-1]
    return w


def tokenize(text):
    text = text.lower().replace("-", " ").replace("_", " ").replace("/", " ")
    toks = [stem(t) for t in TOKEN_RE.findall(text)]
    return [t for t in toks if t not in STOP and len(t) > 1]
'''

TFIDF_SRC = PRELUDE + '''
import math
import re
from collections import Counter
''' + TOKENIZE_SRC + '''

class _Retriever:
    """Exact copy of auto-retrieval-proto.py's Retriever (t0412 TF-IDF arm)."""

    def __init__(self, docs):
        self.docs = docs
        doc_tokens = [tokenize(d["text"]) for d in self.docs]
        df = Counter()
        for toks in doc_tokens:
            for t in set(toks):
                df[t] += 1
        n = len(self.docs)
        self.idf = {t: math.log((n + 1) / (c + 1)) + 1.0 for t, c in df.items()}
        self.doc_vecs, self.doc_norms = [], []
        for toks in doc_tokens:
            tf = Counter(toks)
            vec = {t: (1.0 + math.log(c)) * self.idf.get(t, 1.0)
                   for t, c in tf.items() if t in self.idf}
            norm = math.sqrt(sum(v * v for v in vec.values())) or 1.0
            self.doc_vecs.append(vec)
            self.doc_norms.append(norm)

    def query(self, text):
        qtf = Counter(tokenize(text))
        qvec = {t: (1.0 + math.log(c)) * self.idf.get(t, 1.0)
                for t, c in qtf.items() if t in self.idf}
        qnorm = math.sqrt(sum(v * v for v in qvec.values())) or 1.0
        scores = []
        for i, dvec in enumerate(self.doc_vecs):
            dot = sum(qv * dvec.get(t, 0.0) for t, qv in qvec.items())
            scores.append((dot / (qnorm * self.doc_norms[i]), i))
        scores.sort(reverse=True)
        return scores


def rank(query_text, docs):
    """rank(query_text, docs) -> doc ids, best first. Never sees labels.

    Ties break by REVERSE corpus order (P15 first) — the retriever sorts
    (score, index) tuples with reverse=True, so a tied doc with the larger
    corpus index ranks first. Verified empirically on identical-text docs
    (t0807; re-verified t2200). NOTE: the sibling lexical arm breaks ties
    the opposite way (corpus order, P1 first).
    OBSERVED pin: batteries/t0412-v2-rank/manifest.json -> tie_break.tfidf-t0412
    (identical-text experiment re-run and pinned 2026-10-18, gap-t0807-lane9).
    """
    ret = _Retriever(docs)
    return [docs[i]["id"] for _, i in ret.query(query_text)]
'''

LEXICAL_SRC = PRELUDE + '''
import re
''' + TOKENIZE_SRC + '''

CHECK_ACTION = {
    "verify", "reverify", "pin", "repin", "re-pin", "recompute", "rerun",
    "re-run", "track", "count", "name", "cite", "classify", "measure",
    "test", "gate", "receipt", "evidence", "sha", "exact", "check",
    "anchor", "seal", "stamp", "proof", "table", "verdict", "confirm",
    "live", "bytes", "snapshot", "assert", "guarantee", "run", "fix",
    "surface", "post", "file", "merge", "close", "hold", "advance",
    "re-read", "reread", "re-fingerprint", "refingerprint",
}
TRAP = {
    "fail", "failure", "miss", "missed", "trap", "confound", "leak",
    "silent", "silence", "drift", "phantom", "red", "stale", "unknown",
    "risk", "warn", "warning", "danger", "abort", "void", "mistake",
    "error", "wrong", "corrupt", "tamper", "fiction", "fabricated",
    "broken", "burn", "forbidden", "quota", "forced", "unverified",
}
DECIDE = {
    "decision", "decide", "verdict", "choose", "choice", "anchor",
    "criteria", "criterion", "bar", "gate", "classification", "merge",
    "close", "hold", "select", "pick", "assess", "assessment", "score",
    "rank", "ranking", "target", "priority", "option", "action", "plan",
    "slot", "mandate",
}

_STEMMED = {
    "act": {stem(w.replace("-", " ")) for w in CHECK_ACTION},
    "trap": {stem(w.replace("-", " ")) for w in TRAP},
    "dec": {stem(w.replace("-", " ")) for w in DECIDE},
}


def _feature_scores(principle_text, brief_text):
    """Exact t0412 slice-3 Q1/Q2/Q3 mechanization (pre-registered thresholds)."""
    pt = set(tokenize(principle_text))
    bt = set(tokenize(brief_text))
    i_act = len(pt & _STEMMED["act"] & bt)
    p_act = len(pt & _STEMMED["act"])
    i_trap = len(pt & _STEMMED["trap"] & bt)
    i_dec = len(pt & _STEMMED["dec"] & bt)
    q1 = 2 if i_act >= 2 else (1 if (i_act >= 1 or p_act >= 2) else 0)
    q2 = 2 if i_trap >= 2 else (1 if i_trap >= 1 else 0)
    q3 = 2 if i_dec >= 2 else (1 if i_dec >= 1 else 0)
    return q1, q2, q3


def rank(query_text, docs):
    """rank(query_text, docs) -> doc ids, best first. Never sees labels.

    Ties break by corpus order (P1..P15) — deterministic, declared, and
    empirically verified (identical-text experiment: P1..P15, t2200).
    OBSERVED pin: batteries/t0412-v2-rank/manifest.json -> tie_break.lexical-t0412
    (identical-text experiment re-run and pinned 2026-10-18, gap-t0807-lane9).
    NOTE (t2200): the sibling tfidf arm breaks ties the OPPOSITE way
    (reverse corpus order, P15 first — sorts (score, index) with
    reverse=True). t0412's run used the frozen packet order (J01..J15 via
    the sealed map); that map is answer-key-adjacent and must not live in
    an arm's input space (t0761-lane11 class), so corpus order is the
    sealed choice here. The named ±0.03 tolerance on the t0412 reference
    numbers was justified by a false blanket tie-break declaration and is
    VOID — the t0412 references are the frozen historical record, not
    reproduction targets for this arm.
    """
    scored = []
    for order, d in enumerate(docs):
        q1, q2, q3 = _feature_scores(d["text"], query_text)
        scored.append((-(q1 + q2 + q3), order, d["id"]))
    scored.sort()
    return [did for _, _, did in scored]
'''

for d, src, name in [(ARM_TFIDF, TFIDF_SRC, "tfidf-t0412"),
                     (ARM_LEX, LEXICAL_SRC, "lexical-t0412")]:
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, "arm.py"), "w", encoding="utf-8") as f:
        f.write(src)
    with open(os.path.join(d, "arm_manifest.json"), "w", encoding="utf-8") as f:
        json.dump({"name": name, "version": "1.0.0",
                   "needs_embeddings": False,
                   "source": "t0412-lane2 frozen baseline; stdlib only"},
                  f, indent=2)

print("corpus pin:", pin[:16] + "…")
print("queries:", len(queries), "briefs,",
      sum(len(q["expected"]) for q in queries), "expected pairs")
print("arms:", ARM_TFIDF, ARM_LEX)

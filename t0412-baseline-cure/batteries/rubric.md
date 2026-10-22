# t0412 baseline — frozen rubric (derived from ground-truth-FROZEN.md)

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

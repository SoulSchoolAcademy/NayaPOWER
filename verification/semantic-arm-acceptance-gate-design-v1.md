# CANDIDATE — Semantic-arm acceptance gate (design v1)
**Status:** CANDIDATE. Design only — no battery built, no metric run.
**Parent verdict:** t0712 (gap-t0712-lane9) — the v3 rescue-term battery is a
lexical-mechanism gate; the semantic arm scored 0.000 on it, tying the
known-bad baseline. A mechanism mismatch, not a build failure.
**Frozen pre-registration (sealed before any design byte):**
`hidden_files/twelve-lane-receipts/preregister-t0720-lane9.md`
(2026-10-18 ~03:20 UTC). Falsifiers F1–F7 may not be iterated; they are
the kill conditions for this design.

## 1. The arm, from its bytes (code, not docs)
- `hidden_files/arms/semantic-t0426/arm.py` — contract
  `rank(query_text: str, docs: list[dict]) -> list[str]`, doc ids best-first.
- `score(doc) = cosine(embed(query), embed(doc))`,
  model `sentence-transformers/all-MiniLM-L6-v2` (384-dim) via fastembed.
- Ties (exact float equality) break by corpus order (documented, t0426).
- Doc embeddings cached by `(id, sha256(text))` within the process.
- The arm never sees labels: the harness passes only `(query_text, docs)`.
- `arm_manifest.json` cross-checked 2026-10-18: declares "bi-encoder
  cosine, all-MiniLM-L6-v2 via fastembed; ties -> corpus order" —
  agrees with the code. The t0807 class (docs claiming the opposite of
  bytes) is closed for this arm; the code stays the authority.

## 2. The phenomenon the gate measures
A bi-encoder maps texts into a 384-dim space where paraphrases land near
each other and unrelated texts land far apart. The gate measures
**embedding-space discrimination**: the arm's ability to rank the
semantically-correct document above semantically-plausible distractors
when lexical shortcuts are unavailable. It does NOT measure term
overlap, idf weighting, or ranking of engineered stems — those are the
lexical family's signatures and pointing them at this mechanism is the
t0712 failure class.

## 3. Corpus design (semantic-appropriate, not rescued terms)
- **Source:** natural retrieval phrasings from the Smart Note corpus —
  real user language, no engineered stems, no df-manipulated decoys.
- **Per query q:** one gold doc `g` (genuinely relevant) + exactly 9
  distractors `D` drawn from the SAME semantic neighborhood (same topic
  vocabulary, high lexical overlap with `q` and with `g`) but irrelevant
  to `q`. K=9 is FIXED — a 10-doc field, so the chance baseline for F5
  is exactly 1/10 and no seat re-dials it.
  Design intent: lexical arms tie or fail here (F2 control); only
  meaning separates the field.
- **Query extraction (pinned, no judgment for the execution seat):** the
  40 most recent Smart Note retrieval queries from
  `~/memory/2026-*.md` (plain-language retrieval questions, not
  engineered), deduplicated, frozen into `queries_v4.json` at design-
  freeze time with its SHA256 in the run record. Re-extraction after
  freeze is a new design, not this one.
- **Calibration conflict clause (procedure §5):** if the lexical baseline
  ceiling EXCEEDS the draft's P25 on the calibration split, the bar pins
  at the lexical ceiling and the design's F7 is declared BROKEN —
  the corpus does not discriminate mechanisms, and the run STOPS with
  that verdict. The bar never drops below the convicted baseline.
- **Traps:** queries whose nearest lexical neighbor is a semantic decoy —
  a negation or direct contrast of the gold (e.g. "the gate is broken" vs
  the doc "the gate is working"). The arm must not rank the decoy first.
- **Freeze:** `corpus_v4-semantic.json` + `queries_v4.json`, SHA256-sealed
  before any run. The corpus is a fixture, not a dial.

## 4. Metrics (mechanism-derived, all three reported)
1. **P1** = fraction of standard queries with `rank1 == gold`.
2. **Semantic margin** `M_q = cos(q,gold) − cos(q, best distractor)` —
   the cosine-gap separability in embedding space. Report median + P10.
   This is the metric the lexical battery never had: it measures the
   DISTRIBUTION the encoder produces, not a rank.
3. **Trap avoidance** `A` = fraction of trap queries where the semantic
   decoy is NOT rank 1.

## 5. The bar (calibrated by frozen procedure, not asserted)
The execution seat runs a TWO-STAGE cold protocol:
- **Stage 1 (calibration):** the t0426 draft arm on the frozen
  calibration split → margin distribution + P1 + A. The bar is pinned
  mechanically: `bar = max(lexical-baseline ceiling on the same split,
  draft P25)`. No judgment, no tuning — the weakest reading that still
  excludes the convicted baseline (F7) and stays achievable (F3).
- **Stage 2 (acceptance):** the bar value is written into the run record
  BEFORE the sealed acceptance run starts on the held-out split. No
  iteration between calibration and acceptance.

## 6. The kill conditions (the frozen falsifiers, summarized)
F1 mechanism-blind corpus · F2 no semantic signal beyond lexical (paired
permutation, p<0.05 vs TF-IDF t0412) · F3 dead margin (median ≤ 0) ·
F4 degenerate arm clears the bar · F5 lexical-reward trap (decoy
avoidance at chance while P1 clears) · F6 non-determinism (two cold runs
must be byte-identical) · F7 known-bad arm clears the bar. The full
text is the frozen pre-registration; this doc may not soften them.

## 7. Cold-run execution plan (a cold seat can execute this)
1. Environment: `~/workspace/venvs/fastembed-env/bin/python`;
   `export FASTEMBED_CACHE_PATH=$HOME/.cache/fastembed HF_HUB_OFFLINE=1`;
   `export no_proxy=localhost,127.0.0.1,::1 NO_PROXY=$NO_PROXY`
   (per TOOLS.md — the httpx/IPv6 quirk).
2. Assert corpus + query SHA256 match the seal at load (hard fail on
   mismatch — a re-sealed corpus is a new design, not this one).
3. Wiring validation first: replicate the arm's cosine function verbatim
   (never import write-on-import modules); run the degenerate arms
   (doc-length, alphabetical-id) — record their P1/margin/A as the
   mechanism floor (F4 check).
4. Run the lexical baselines (lexical-t0412, tfidf-t0412) on the same
   corpus — the F2/F7 controls.
5. Stage 1 calibration with the t0426 draft → pin the bar into the run
   record (procedure §5, no judgment).
6. Stage 2: two cold runs of the candidate arm → assert byte-identical
   rankings (F6), then score P1 / margin / A against the pinned bar.
7. Emit `semantic_gate_run.json`: corpus SHAs, arm pin, bar + calibration
   trace, the three metrics, falsifier verdicts F1–F7, exact falsified
   lines — the whole verdict in one artifact the next seat can diff.

## 8. What this design explicitly does NOT do
- It does not re-derive the v3 battery's bar (0.60 is lexical-calibrated;
  unachievable-by-construction for embeddings — t0712).
- It does not import the frozen battery module (write-on-import footgun —
  t0712 agent feedback).
- It does not measure retrieval quality in the wild (latency, index size,
  drift) — those are different gates for different briefs.

**Next:** the next lane-9 brief BUILDS the battery + frozen corpus per
this design (t0720 says design only — building is explicitly the next
brief). The builder must run §7 cold, verdicts first.

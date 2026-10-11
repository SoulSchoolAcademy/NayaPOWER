# Retrieval Ranking Benchmark

Offline precision/recall measurement for `nayanet_retrieve_blocks()` — the
ranking function behind cold retrieval.

## What it proves

The execution tests (`tests/intelligence_retrieve_execution.test.mjs`) prove
the retrieval handler *runs*. This benchmark proves it retrieves the *right*
blocks: MRR, P@1, P@3, Recall@5 against fixed relevance judgments, plus
structural invariants (SUPERSEDED/DELETED never served; VERIFIED outranks
CANDIDATE on shared vocabulary).

## How it works

1. Spins up a scratch Postgres database (never production).
2. Creates the minimal `nayanet_intelligent_blocks` table.
3. Applies the REAL migration files from `supabase/migrations/` in version
   order — the benchmark tests shipped bytes, not a port.
4. Loads `corpus.json`: 29 fixture blocks grounded in real NayaPOWER doctrine,
   12 judged queries (including paraphrase/synonym queries a cold Naya would
   actually ask), 3 structural assertions.
5. Runs each query through the RPC and scores the ranking.

## The v2 fix it guards

v1's boolean prefilter (`search_vector @@ websearch_to_tsquery`, AND
semantics) returned NO_MATCH for paraphrase queries — one non-matching
lexeme silenced the whole query. Baseline: MRR 0.6667 (4/12 silent).
v2 adds an OR-fallback cascade: attempt 1 keeps AND semantics byte-identical;
attempt 2 fires only when attempt 1 returned zero rows, running OR over the
query lexemes through the same scoring, tagged `fallback_or_match` in `why`.
After: MRR 1.0, P@1 1.0, all structural assertions pass.

## Running

```bash
# local postgres required (CI provides it via the postgres service)
python3 tools/retrieval_benchmark/run.py
```

Exit 0 only if MRR >= 0.99, P@1 >= 0.99, and every structural assertion
passes. The pytest suite (`tests/test_retrieval_ranking_benchmark.py`) runs
the same measurement as a CI gate.

## Corpus discipline

Relevance judgments were authored BEFORE any measurement run. Do not edit
judgments after seeing results — edit the ranker instead. Q13's original
"expect empty" judgment was retired before the first v2 measurement (it was
calibrated to AND-only semantics); its true invariant — deleted content
never surfaces — is preserved as structural assertion S3. The retirement is
documented in `corpus.json` (`_q13_retirement_note`).

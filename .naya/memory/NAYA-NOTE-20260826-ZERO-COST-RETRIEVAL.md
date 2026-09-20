# NAYA NOTE — ZERO-COST SMART RETRIEVAL HARDENING

**Status:** IMPLEMENTED — AUTHORITATIVE CI PENDING
**Current main:** `846529daea1bd35af564bdc061f3fb74a1b7f485`
**Last verified GREEN:** `9aefe57a71bd6425681bb435d70417ad33832198` / run `32909426069` / job `98000403862`
**Protected GREEN:** `0f82325a82ed37b5b3a3d097599025369c03a1ed`

## What changed
The existing Smart Brain retrieval path was upgraded without external vector infrastructure. The engine now combines:

- exact event-ID/title/subject matching;
- BM25 lexical ranking;
- TF-IDF cosine similarity;
- hard metadata filters for project/type/status/tag/date windows;
- transparent domain query expansion;
- recency weighting;
- authority and verification weighting;
- relationship-aware reranking.

The engine remains dependency-free and keeps canonical event JSON as the authoritative source of truth.

## Important safety property
Unknown queries now fail closed instead of returning arbitrary zero-score events. Impossible metadata filters also return an empty result. This is an intentional deliberate-failure boundary against false relevance.

## Measurement
The retrieval benchmark now carries explicit relevance judgments and reports precision@5, recall@5, MRR, and expected-token coverage. This establishes a measurable lexical baseline for a future vector adapter. It does **not** claim semantic/vector retrieval exists.

## Architectural lesson
We do not need vectors to make the first customer-facing Superbrain useful. A strong deterministic retrieval layer can provide a surprisingly capable zero-cost baseline. Vectors can later be added as a derived semantic signal while preserving lexical fallback and canonical memory.

## Next
Obtain authoritative GREEN on this exact current head. If GREEN, move immediately to zero-setup PDF activation: document → chunks → canonical memory → derived search indexes, with the same repository-native source-of-truth discipline.

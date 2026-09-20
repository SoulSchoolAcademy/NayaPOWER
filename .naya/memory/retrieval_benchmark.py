#!/usr/bin/env python3
"""Deterministic retrieval benchmark for the dependency-free smart search path.

The benchmark uses explicit relevance judgments for the current canonical corpus.
It measures precision@5, recall@5, MRR, and token coverage. This is still not a
semantic-vector benchmark; it is the baseline that a future vector adapter must
beat rather than a claim that vectors already exist.
"""
from __future__ import annotations
import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
import smart_notes_v3 as brain

CASES = [
    {
        "query":"Superbrain CIS Naya Power",
        "expected_tokens":["superbrain","cis"],
        "relevant_ids":[
            "SE-20260825-122600-superbrain-seed-optimization",
            "SE-20260825-200000-smart-brain-hardening-execution",
            "SE-20260825-203000-superbrain-10-of-10-execution-protocol",
            "SE-20260825-204500-superbrain-execution-cycle",
            "SE-20260825-220300-superbrain-p0-verification",
        ],
    },
    {
        "query":"execution continuity learning",
        "expected_tokens":["continuity","learning"],
        "relevant_ids":[
            "SE-20260824-065600-naya-operational-intelligence",
            "SE-20260825-000005-cis-universal-learning-vision",
            "SE-20260825-214500-superbrain-contract-enforcement",
            "SE-20260825-220300-superbrain-p0-verification",
        ],
    },
    {
        "query":"duplicate entity resolution",
        "expected_tokens":["duplicate","entity"],
        "relevant_ids":[
            "SE-20260825-204500-superbrain-execution-cycle",
            "SE-20260825-200000-smart-brain-hardening-execution",
        ],
    },
    {
        "query":"Daily Intelligence",
        "expected_tokens":["daily","intelligence"],
        "relevant_ids":[
            "SE-20260825-000005-cis-universal-learning-vision",
            "SE-20260825-180000-daily-intelligence-smart-notes-migration",
        ],
    },
]


def run() -> dict:
    results=[]
    for case in CASES:
        ranked=brain.retrieve(case["query"], limit=5)
        ids=[e["event_id"] for _,e in ranked]
        relevant=set(case["relevant_ids"])
        hits=sum(1 for eid in ids if eid in relevant)
        precision=hits/len(ids) if ids else 0.0
        recall=hits/len(relevant) if relevant else 1.0
        rr=0.0
        for rank,eid in enumerate(ids,1):
            if eid in relevant:
                rr=1.0/rank; break
        texts=[brain.all_text(e).lower() for _,e in ranked]
        token_hits=sum(1 for token in case["expected_tokens"] if any(token in text for text in texts))
        results.append({
            "query":case["query"],
            "returned_event_ids":ids,
            "top_scores":[round(score,3) for score,_ in ranked],
            "expected_relevant_count":len(relevant),
            "relevant_hits_at_5":hits,
            "precision_at_5":round(precision,3),
            "recall_at_5":round(recall,3),
            "mrr":round(rr,3),
            "expected_token_coverage":round(token_hits/len(case["expected_tokens"]),3),
        })
    n=len(results) or 1
    return {
        "schema_version":2,
        "status":"BASELINE",
        "retrieval_engine":"exact+BM25+TFIDF+metadata+query-expansion+recency+authority+graph-rerank",
        "semantic_vector_engine":False,
        "case_count":len(results),
        "mean_precision_at_5":round(sum(x["precision_at_5"] for x in results)/n,3),
        "mean_recall_at_5":round(sum(x["recall_at_5"] for x in results)/n,3),
        "mean_mrr":round(sum(x["mrr"] for x in results)/n,3),
        "mean_expected_token_coverage":round(sum(x["expected_token_coverage"] for x in results)/n,3),
        "cases":results,
        "next_measurement":"Re-run this exact relevance-judged corpus after a real semantic/vector adapter is integrated; compare precision/recall/MRR and preserve the lexical fallback.",
    }


if __name__ == "__main__": print(json.dumps(run(), indent=2, ensure_ascii=False))

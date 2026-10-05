# KNOW Retrieval Measurement Harness

**Lane:** KNOW-measurement (Naya 2 specialist). **The instrument, not the engine.**

This harness measures the retrieval path that ships in `tools/smart_note_v2.py`
— `retrieve(query)` — exactly as written. It does not reimplement retrieval,
rank, or decide. Coda 4 owns the KNOW restoration repair and the
persistence/retrieval seam; this directory owns only the measuring instrument.

## What it measures

One KNOW query → hit/miss + latency → consumer decision → observed outcome:

| Step | How | Evidence |
|---|---|---|
| Query | `retrieve(query)` from `tools/smart_note_v2.py` | wall-clock latency (ms) |
| HIT | returns the registry entry + note text | returned `intelligent_block_id` vs expected |
| MISS | raises `SystemExit("NO_RELEVANT_INTELLIGENCE")` | the miss is logged with the same fidelity as a hit |
| Consumer (bundled) | `held_out(retrieved)` control vs treatment | `behavior_changed` |
| Consumer (harness) | `act-first-v1`: control `ASK_FIRST` vs treatment from note text | decision delta |
| Abstention | MISS → consumer records `ABSTAIN_NO_RETRIEVAL` | the miss path is observable end to end |

## Files

- `query_spec_v1.json` — frozen spec: corpus pin (exact SHA), 5 HIT queries with
  expected note IDs, 5 MISS queries with verified zero vocabulary overlap,
  consumer definitions, and the pre-registered pass criteria P1–P5.
  Expectations are **corpus-bound**: re-pinning the corpus requires re-verifying
  the spec (see `harness.py` probe pattern).
- `harness.py` — the runner. Writes an append-only JSONL retrieval log
  (run manifest first: corpus SHA + registry sha256 = the repeatability anchor).
  Never edits the log mid-run, never retries a query.
- `scorer.py` — the independent scorer. Reads spec + log, recomputes the
  verdict with arithmetic only. Exit 0 = all criteria pass.

## Repeatability

```bash
git worktree add /tmp/know-pin <pinned-sha>
python3 tools/know_measure/harness.py --repo /tmp/know-pin \
    --spec tools/know_measure/query_spec_v1.json --out /tmp/know-run-1
python3 tools/know_measure/scorer.py --spec tools/know_measure/query_spec_v1.json \
    --log /tmp/know-run-1/retrieval_log.jsonl
```

Same SHA → same hit/miss outcomes (retrieval is deterministic keyword overlap).

## Honest boundaries

- A retrieval HIT is **not** active intelligence. Only the observed consumer
  decision delta counts, and only the scorer's arithmetic verdict is claimed.
- `held-out-v1` is measured as-is. At spec freeze its governing phrases match
  no note in the pinned corpus, so it returns `treatment=UNRESOLVED`,
  `behavior_changed=False`. That decoupling is a finding for the pipeline
  owner, not a harness defect — and the harness is what makes it visible.
- The harness operator never hand-edits the log. The remaining way to fake a
  run is to corrupt the machinery, not to write a confident paragraph.
- This proves the loop fired on one corpus for one consumer. It does not prove
  compounding, generalization, permanence, or pipeline generality.

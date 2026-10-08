# Human Value ledgers

Real measurement lives here. The example corpus in `../examples/` is synthetic;
everything in this directory is observed reality with durable evidence, or it
does not exist.

## Files

- `real-events.jsonl` — the real event ledger. One JSON object per line,
  schema v1 (`../schema.py`, fail-closed). Every event carries ≥1 durable
  evidence pointer; no evidence = no credit.
- `decision-predictions.json` — pre-registered Decision Value Calculus
  predictions (`decision_id` + `delta_v_predicted`). Predictions are recorded
  BEFORE the outcome is observed. An event's `decision_id` must name a
  prediction recorded earlier — retroactive credit is forbidden and the join
  refuses it.

## Placement law

Non-sensitive ledgers (public evidence only: `feed_comment`, `url`,
`smart_note`, `receipt` pointers) are canonical **in this repo**. A ledger
that lives only in a workspace can die with it — that is exactly what killed
the 2026-10-06 instrument, and this directory is the fix.

Sensitive ledgers (anything touching private human data) live **outside** the
repo; the repo holds only derived measures + `content_hash` pins.

## How to add an event

1. Observe something real: a human's life measurably better (or human
   attention demanded).
2. Find evidence that **already exists** (feed comment, PR, receipt). Never
   manufacture evidence to lift a number.
3. Append one line. Run the schema: it fails closed on any violation.
4. Recompute and check the numbers move the way reality moved.

```bash
python3 tools/human_value/compute_hv.py \
  --ledger tools/human_value/ledgers/real-events.jsonl \
  --receipts tools/human_value/ledgers/decision-predictions.json
```

## DAI baseline

The 2026-10-06 DAI baseline (0.71 attention-events/day) died with its
workspace. The `attention_demanded` series restarts with this ledger on
2026-10-08. Trend readable after 2+ weeks of real data — no sooner.

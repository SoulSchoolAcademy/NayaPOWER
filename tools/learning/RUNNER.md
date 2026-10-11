# Error-Signal Loop — Runner

The mechanism that turns principle violations into learning: a worker
violates a briefed principle (or ratified law) → the scanner catches it as a
structured LEARNING EVENT with provenance → the event ships as a candidate
lesson, not just a failure.

## Command

```bash
# Scan a worker artifact (lane-feed report, PR body, commit diff, text file)
python3 tools/learning/error_signal_loop.py scan \
  --artifact <path-to-artifact-text> \
  --kind lane-report|pr-body|commit-diff|text-file \
  --source-ref "lane-1713:<comment-id>" \
  --out ~/workspace/goals/super-brain-engine-to-10-10/hidden_files/learning-events.jsonl \
  --append    # dispatcher tick: append candidates, don't overwrite

# Inspect the pinned checklist / the event schema
python3 tools/learning/error_signal_loop.py checklist
python3 tools/learning/error_signal_loop.py schema
```

Exit 0 = scan completed (violations are data, reported as events).
Exit 2 = fail-safe: input unreadable/malformed or checklist invalid.
A violation never changes the exit code; a malformed input never emits events.

## Cadence

- **10-minute dispatcher tick:** each new worker's sign-in/report text gets
  scanned at the tick that reads the lane feeds. Append emitted candidates to
  `hidden_files/learning-events.jsonl` and the day's memory log.
- **Per-PR:** scan PR bodies on open (cheap, local, zero API calls).
- **CI:** `tests/test_error_signal_loop.py` runs in the existing
  `kernel-tests.yml` workflow (`python -m pytest -q` picks it up
  automatically — no new workflow needed).

## Lifecycle of an event

1. **Emitted** — scanner writes the JSONL candidate (provenance: file, line,
   principle, verbatim quote; pinned to the briefing sha256).
2. **Confirmed** — a different seat verifies the violation is real on the
   lane feed. (Candidate != ratified lesson.)
3. **Compounded** — the suggested lesson enters the briefing/intel flow and a
   regression test is added so the learned benefit survives later changes.

## Re-pinning

`tools/learning/principles_checklist.json` is pinned to briefing fingerprint
`4baaa440db4dc799bee17ac3ed7bdc0d1d43a73856441fc0cc6e8a96b1251992`.
When the briefing changes: re-run the fingerprint, regenerate the checklist,
and update this file. The scanner fails safe if the checklist's fingerprint
is invalid or missing.

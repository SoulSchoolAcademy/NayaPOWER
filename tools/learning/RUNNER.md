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
`6e34da67deef30b613c448500e0fce8bf4cb54f8e3e88c31c90fbf8dbe41f596`
(207 lines, pinned 2026-10-12T01:02:00Z).
When the briefing changes: re-run the fingerprint, regenerate the checklist,
and update this file. Every scan compares the pin against the live briefing
and reports `briefing_pin` (`stale`: true/false/"unknown") in the scan
summary — re-pin before trusting results when it says true. `load_checklist`
fails safe (exit 2) on a malformed or unreadable checklist; staleness is
reported in the summary, never fatal.

## Known limitations

- **Negation window (P6):** the negation exemption looks at the last clause
  of the 40 characters before a match. A negation word farther back
  ("I did not, despite the risks, approve database writes") will not
  exempt the match — the scanner errs toward firing, and a different seat
  confirms real violations before anything is learned. Precision here is
  deliberately clause-scoped, not sentence-scoped.
- **Keyword scanning (P1):** a bare "10/10" without same-line positive
  context fires; candidates go to different-seat confirmation, never
  straight to lessons.

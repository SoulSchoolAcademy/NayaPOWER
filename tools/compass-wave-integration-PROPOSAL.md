# Compass Wave-Integration — PROPOSAL (not applied)

**Status:** proposal only. No cron/schedule/task text is modified by this document.
Director's call to adopt, pilot, or reject. If adopted, a separate
dispatcher update applies it — this doc never applies itself.

## What was activated (evidence)

- World model snapshot: `~/.naya/world-model.json` (`snapshot_utc:
  2026-10-17T02:55:12.079818+00:00`) — 5/6 sections OK (tip, prs, lanes,
  ledger, mission), laws UNKNOWN (no local briefing file).
- `tools/nayas_guide.py status` → exit 0, "The Guide is working."
  (A false "API unreachable" was fixed locally: the guide hardcodes
  `~/workspace/skills/github/bin/gh-api`, which did not exist — symlinked
  to the lane GitHub-App helper. `tools/world_model.py` expects
  `~/workspace/naya/bin/gh-api` — symlinked the same way.)
- Live consultation, this wave: `query "which lanes are free?"` → alpha FREE,
  beta/gamma OCCUPIED (exit 0). North-star-style question ("which system needs
  work next?") → UNKNOWN, exit 2, by the answer contract — honest, by design.

## The recipe — one compass consult per wave

Run from the repo working dir, BEFORE choosing the wave's 3 items:

```bash
cd ~/workspace/nayapower-repo
python3 tools/world_model.py refresh 2>/dev/null          # 0–4 API calls: tip always (1); lanes change-detected via comment count; fresh sections skipped
python3 tools/nayas_guide.py status                        # 1 API call (/rate_limit); exit 0 = working
python3 tools/world_model.py query "which lanes are free?" # 0 API calls — answers from the snapshot
```

In-grammar, dispatcher-safe queries (zero API calls, exit 0 on fresh data,
exit 2 + UNKNOWN otherwise — never force an UNKNOWN into a positive read):

- `query "which lanes are free?"` — pick items that fit a free lane
- `query "what is the mission state?"` — current priorities/parked/blockers (#2154)
- `query "what does the ledger say?"` — what's proven vs pending (#2396)
- `query "what is the live tip?"` — confirm main SHA before anchoring a branch

Never consult the compass with: merge decisions (`guide merge --auto` is a
*judgment* the dispatcher does not hold), north-star priority questions
(outside the query grammar — returns UNKNOWN by contract), anything needing
a human's word.

## Where the recommendation gets recorded

One compact suffix on the wave log line in `~/memory/YYYY-MM-DD.md`:

```
compass=<free-lanes-short> guide=<green|red:reason>
```

Example: `compass=alpha-free guide=green` or
`compass=UNKNOWN(guide-red) guide=red:world-model-missing`.

## Guardrails (non-negotiable)

1. **Compass failure never blocks a wave.** If `guide status` exits non-zero,
   freshness is >2× limit, or the model file is missing: log
   `compass=UNAVAILABLE`, fall back to PROGRAM.md alone. (GATE_BLIND —
   a closed door is not broken work.)
2. **Read-only for the dispatcher.** No `guide merge`, no writes, no PR opens.
   The compass advises; the math + PROGRAM.md decide; humans merge.
3. **Budget-aware.** If the rolling hourly GitHub quota total is ≥400, skip
   `refresh`; `query` answers from cache and `status` reports staleness
   honestly. A stale honest read beats a fresh expensive one under pressure.
4. **OBSERVED ≠ mutex.** Lane FREE is a reading of the last comment, not
   dispatch authorization. The board tail remains the authority before a
   lane-claiming dispatch.

## Pilot acceptance (suggested)

- Run the recipe for 6 waves; record the compass suffix every wave.
- Success: ≥5/6 waves consult without error; at least one dispatch choice
  changed by the compass (e.g. lane pick) with the change noted in the wave
  log; zero compass-caused stalls (guardrail 1 never had to fire).
- Fail: any stall, or the compass contradicted PROGRAM.md/board-tail without
  being right — report to the director, retire or fix the recipe.

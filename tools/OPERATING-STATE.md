# Operating State as Data — wiring

**What this is.** `tools/operating_state.py` emits two machine-readable
artifacts — `OPERATING-STATE.json` (tip, queue shape by tier × action, the
tip's own failing checks, the balance gauge's four numbers, the laws
pointer, the HOLD-HUMAN set) and `QUEUE-CONTRACT.json` (the live drain as
data: per open PR — number, title, tier, one action, cure text, owner,
head). Schemas: `tools/operating_state.schema.json`,
`tools/queue_contract.schema.json`.

**One publisher rule.** These artifacts are published by the *existing*
hub-refresh owner — the hourly job that already publishes `HUB-STATE.md`
and `MISSION-STATE.md` to `live/mission-state` from
`hub-state-builder.py` (goal `hidden_files`, off-repo). This tool is an
extension of that machinery, never a rival publisher: the hub-refresh
owner adds one step after its existing state build —

```sh
python3 tools/operating_state.py emit \
  --out <the same staging dir the hub refresh publishes from> \
  --gauge-dir <repo>/../files/balanced-machine \
  --laws-file ~/AGENTS.md
```

— and the two JSONs ride the same publish to `live/mission-state`, next to
the human-readable pair. The emitter validates both artifacts against
their schemas and refuses to publish a state whose tip does not match the
live ref (`GET /git/refs/heads/main`) at publish time: a stale state can
never ride.

**Consumers (activation).** A cold seat loads only the two JSONs and runs

```sh
python3 tools/operating_state.py cold --state OPERATING-STATE.json --queue QUEUE-CONTRACT.json
```

to print the five activation answers (tip · what's mergeable now · what's
held for the human · the tip's red set · the gauge numbers) plus the laws
pointer — no prose parsing anywhere in the loop.

**Derivation rules.** Tiers come from `tools/pr_flow_tier.py`
(Balanced Machine step 1) — imported, never re-implemented. Actions come
from the ratified drain order (Balanced Machine design §2/§7): HOLD-HUMAN
and CLOSE-CANDIDATE sets are named in the emitter with their decisions;
everything else is derived from live check-runs at the PR's exact head,
with the tip's own reds never charged to a PR. Gauge numbers are parsed
from the newest `GAUGE-READ-*.md` with the source + read anchor recorded
in the artifact; when `tools/balance_gauge.py` (PR #2863) merges, the
reader swaps to its functions — the `gauge.source` field always says
which produced the numbers.

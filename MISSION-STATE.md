# MISSION STATE — Team Naya execution plan (single source of truth)

**Published:** 2026-10-10 16:46 UTC by Naya 2 (director)
**Main tip:** `8de84488922b3ef14209b858ac45fa4ba1a40864`
**Canonical now:** issue #2154 (Current Mission State, director-maintained) + `BRAIN/CURRENT-MISSION-STATE.md` on branch `naya/mission-state`. #1354 stays the coordination feed (the history). This branch is the worker activation kick: fetch it on shift start and you know exactly where to go.

## WHERE TO GO — ranked priorities

1. **REPAIR — brain-index drift at tip `8de84488` (5th occurrence).** Kernel Tests RED: `tools/regenerate_brain_index.py --check` reports drift in all 3 index files (REAL-TREE.json, REAL-TREE.md, NAYAPOWER-BRAIN-INDEX.json), verified on exact tip bytes. Base-inherited, not from PR #2151 (its files touch no BRAIN/ paths). Introducer: #2147 added `BRAIN/01-GOVERNANCE/THE-PROTOCOL.md` without regenerating the index. Fresh minimal repair: regen at the exact tip + re-stamp (same class as #2144). UNCLAIMED — route to the brain-build lane; check for duplicate claims before authoring. Lesson for the DOS list: any PR touching BRAIN/ paths must regen the index in the same PR.
2. **MERGE CLICK — PR #2136** (bd725a24, pip-install-pytest in protocol-gates). Unblocks WS-9 (Smart App v1.0.0, PR #2132) AND WS-4 (waste meter, PR #2141). One click heals both lanes. Awaiting the merge lane.
3. **MASTER LOOP — second template run** (authoritative seats, relayed 15:30Z): Naya 4 fixes #2062 red tests then merges · Naya 5 rebases connect→learn→evolve (main's ts_bridge wins) · Naya 1 validates #2102/#2103/#2104 (learning moves on her stamp only) · Naya 5 rewires 12 worker briefs. P2: experiment proposal → Shawn's review with triple-yes checkpoints. P3: 7-day branch claim window — 2026-10-17, then close unclaimed. Parked: 4 rows, RLS — Shawn's word only.
4. **OPEN PRS** — #2145 (WHAT-IT-MEANS-TO-BE-NAYA.md, 347c2bdc), #2146 (WORKER-PROTOCOL.md, ff067fb6). Mergeable_state: unknown at last read — merge lane re-checks before clicking.
5. **ACTION BUDGET (Naya 4's rebuild, standing):** the team has ~2,500 actions/month TOTAL. Director pass is the single GitHub reader (cheap-check-first + stand-down-flag + shared-state). No duplicate scans, no polling, no theater.

## DONE WITH PROOF (latest)
- Tip `2ff26818`: pytest 2285 passed / 11 skipped / 2 xfailed — GREEN (root, no exclusions, disk-isolated); brain index `--check` OK (1241 files, #2142 drift healed by #2144 re-stamp); adversarial harness 6/6 PASS (tip-current copy, serialized).
- Merged this window: #2147 (THE-PROTOCOL + worker_entry/exit machine enforcement), #2150 (human-value events), #2151 (prod-proof-chain wiring), plus #2131, #2137, #2142, #2144, #2087.
- Health-check survives network outages; dead-branch janitor built (Naya 5).

## BLOCKED / HUMAN GATES (director's desk — nothing agent-movable)
- Production deploys/dispatches, production DB reads/writes/migrations, constitutional ratification, credentials/money, destructive actions — all human-only, all untouched.
- #2136 merge click awaits the merge lane (agent-side under scorecard law, ready when green).

## HOW TO READ THIS
Fetch on shift start: `git fetch origin live/mission-state`. If it changed since your last shift, your picture is stale — re-read. Discuss/comment on #1354; this file stays the snapshot, the feed stays the conversation. The worker entry gate (`tools/worker_entry.py` on main) is the machine check; this file is the orders.

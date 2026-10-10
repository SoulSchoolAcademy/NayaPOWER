# CURRENT MISSION STATE
> **Last verified:** 2026-10-10 12:38 PDT by Naya 4 (director) · refreshed ~every 30 min · main tip `0b81b0c2` — RED at tip: brain-index drift, 6th occurrence (pytest itself green)
> **This file is the snapshot. #2175 is the conversation.** (#1354 hit GitHub's hard 2,500-comment cap — commenting disabled ~19:19Z; #1354 is the readable archive.) Discuss there; tune in here.
> Workers: read this at shift start. If it changed since your last shift, your old picture is stale.

## The mission (one line)
Bring Naya to life — a living mind with unbroken memory, fully functioning — then NayaNET live and working.

## Right now — ranked priorities
1. **RED at tip `0b81b0c2` — brain-index drift, 6th occurrence (REPAIR LANE).** Naya 2 relay 19:25Z (6101357903): `test` fails on the brain-index --check (BRAIN/REAL-TREE.json + .md don't match regen); drift reintroduced by one of #2172/#2173/#2174 (files added without regen). pytest GREEN (2715/12/2); promote-and-prove fail-closed as designed. Repair: re-pin to 0b81b0c2, rebase-before-regen, regen, verify. No duplicate mechanism — Naya 2 stood down. All lanes: re-pin tip-pinned state; the 39558acc green certificate is history, not authority (Freshness Law).
2. **#2174 mutual-oversight flag (owning lane's call).** Merged 19:19:23Z via the org account ~3 min after the integration coordinator's sign-in said "No merge action taken — branch only" / "needs independent validation before any merge claim." Zero reviews, no board receipt in between. If a receipt or director click existed, say so on the board; if not, the scorecard law's receipt requirement applies. Director notes: do not invent who clicked.
3. **Naya 5 directive engine — register now at 35 directives (all SPEC ONLY, owners TBD).** New this tick: D28 assumption-audit protocol; D29 responsibility boundary; D30 causal trace; D31 causal uncertainty; D32 uncertainty propagation; D33 evidence revocation; D34 cache invalidation; D35 stale-qualification prevention. Director routes owners. Protected gates hold: wiring, sealed-store authority, LAW changes = Shawn's word only.
4. **Board migrated: #2175 is the board, #1354 is the archive.** Update every worker body that says "read #1354" → "read #2175".
5. **Doctrine locked in per Shawn's word.** SN-0881 The Freshness Law (constitutional, RATIFIED 2026-10-10): "We learn and we grow and we let everything else go." Proof never expires by time — expires when the world it was proven against changes. Covers intelligence, code, AND interfaces; old proof = history, never authority. SN-0882 paired. SN-0905 fairness lie detector: Shawn — "lock that one in and smart note it and let everybody know." 28 Smart Notes (SN-075x) filed by Naya 5 intel scribe to .naya/capture/.
6. **Independent validation: PR #2075 + #2079** — both green (7+6 success, 1 skipped). A DIFFERENT seat validates before merge: Naya 1 or Coda.
7. **Governance collision — adjudicate before #2145 or a convergence PR merges.** Naya 5's convergence ask vs director-distilled doctrine on #2145 (Naya 2 review: PASS). HOLD both; adjudicate on the exact delta, never on a guess.
8. **Naya 1 review follow-up (CONCERNS, not block).** Score-repair-verify: bind DIAGNOSE ranking to the canonical calculator output; define the typed SCORE decision receipt. No revert. Sequence lesson: requested pre-merge review not landed = HOLD, not a race.
9. **Merge Smart App v1.0.0 (#2132)** — real consumer proof, honest 8.5/10. Merge on green CI at the exact tip.
10. **Cold activation proof** — independent verification (master loop).
11. **Unify the canon (#2139)** — DRAFT delivered. Shawn's word only.

## Merged today (with proof)
- #2174 wiring Phase 1 — strengthen() evidence gate → tip `0b81b0c2` (19:19:23Z). RED (drift) + mutual-oversight flag open
- #2173 mission-state snapshot refresh (19:18–19:19Z)
- #2172 fairness-verification (`naya5/fairness-verification`, 390/390 green) → main (19:18–19:19Z)
- #2169 sealed-fixture convention + T12 blind fixture family → `39558acc` (19:03Z) — was green at tip; certificate in history
- #2168 scheduler-fairness → `38e51b57` (19:03Z) — was green at tip
- #2160 brain-index re-stamp → `40df54b1` — validated: zero-byte merge delta, --check OK, 19/19 CI — 5th drift closed
- #2152 enforcement layer (`c5263f97`) — RATIFIED by Shawn 17:18Z; workflow-gate exception written
- #2136 CI fix (`2a8e3491`) — pytest install; protocol gates green again
- #2156 docs — 5 laws x 3 forms + doc-completeness gate
- #2147 THE-PROTOCOL + worker_entry/exit scripts
- #1861 memory-metabolism (10:01:57Z) — Naya 1: re-score MEMORY & CONTINUITY (holds 7.0)

## New surfaces (know them)
- **#2175 = THE BOARD** — Team Naya coordination, continued from #1354. Read fresh every shift.
- #1354 = ARCHIVE (GitHub 2,500-comment cap; commenting disabled, not locked).
- #2154 = CURRENT MISSION STATE — always-current issue, director-maintained.
- #2158 = TEAM SCOREBOARD — per-team accountability, director-maintained.
- PR #2159 = weekly accountability scorecard → BRAIN/SCORECARD.md (first run Monday).

## The governance stack (no duplicates — each layer has one job)
- `BRAIN/01-GOVERNANCE/THE-PROTOCOL.md` — the constitution (what we believe)
- `BRAIN/01-GOVERNANCE/WORKER-PROTOCOL.md` — the job instructions (what to do)
- `tools/worker_entry.py` / `worker_exit.py` — shift gates (WAKE/SIGN-OUT in code)
- `.github/workflows/worker-protocol-gates.yml` — PR-time enforcement
- `protocol-watchdog.yml` + `mission-state-watch.yml` — scheduled enforcement

## Team status — per area
*Accomplished / working on / plan. "—" = no new signal (not idle).*

| Area | Score | Accomplished | Working on | Plan |
|---|---|---|---|---|
| SELF | 9.0 | Tip `39558acc` → `0b81b0c2` (3 merges: #2172/#2173/#2174); RED at new tip (brain-index drift) | Repair lane re-stamps index; confirm green CI | Close gaps to 10 |
| LAW | — | SN-0881 Freshness Law constitutional lock-in (Shawn's word, RATIFIED); SN-0905 locked in | Naya 1 CONCERNS follow-up routed | #2139 needs Shawn |
| ACT | — | Three merges landed (#2172/#2173/#2174); #2174 oversight flag open | Repair + merge-receipt verification | Green CI at tip |
| KNOW | 9.0 | Directives D28–D35 registered (register at 35); all spec-only | Director routes owners | Kernel wiring gated: Shawn's word |
| PROVE | 9.0 | #2172 fairness-verification merged (390/390); RED at tip blocks new claims | Re-pin + re-verify at 0b81b0c2 | Smart App proof |
| CONNECT | 8.8 | Board moved to #2175; Naya 2 relay 19:25Z receipt | Steady | Push to 10 |
| VERIFY | 9.4 | Naya 2 relay: NEW RED named, #2174 flag raised factually, board watermark carried to #2175 | Tip-green repair verification | Successor test |
| LEARN | 5.0 | #2174 strengthen() evidence gate ON MAIN; 28 Smart Notes SN-075x filed | Directive routing | Unblock → 10 |
| EVOLVE | 6.2 | — | Biggest gap | Score-fill-ship |

## Key numbers
- Main tip `0b81b0c2` (19:19:23Z; RED — brain-index drift; last fully green: `39558acc`)
- Branches: 1880 (19:41Z, git protocol)
- #1354 comments: 2,500 (CAP — commenting disabled by GitHub; archive)
- #2175 comments: 8 (D29–D35 + Naya 2 relay receipt; watermark 6101449710)

## Open unknowns (with owners — assigned 2026-10-10)
| Unknown | Owner | Evidence needed | Next action |
|---|---|---|---|
| Worker-standard convergence delta | Naya 5 / Naya 2 | Exact diff vs distilled #2145 | Adjudicate on evidence |
| Production-parity status | VERIFY | Source→deploy diff | Parity check run |
| Learning → ACT influence | LEARN + ACT | Controlled behavior test | Design the experiment |
| Admission→promotion e2e | LEARN | Persisted chain trace | Trace one candidate |
| Cold successor continuation | VERIFY | Independent task completion | Run the cold test |
| Directive owners D6–D35 | Director | Route per directive | Post owners on #2175 |
| Sealed-store permanent authority | Shawn | Protected gate word | Shawn's word only |
| Who clicked #2174 / merge receipts | Merge lane | Receipt or click evidence | Answer on the board |
| Drift reintroduction (6th) | Repair lane | Regen on 0b81b0c2 | Heal + structural fix |

## Blocked (with what's needed)
- **RED at tip** — repair lane (re-pin, rebase-before-regen, regen, verify)
- **#2174 oversight** — owning lane answers on the board (receipt or explanation)
- **Worker-standard collision** — adjudication before either merges (director)
- **Error-defense kernel wiring** — Shawn's word (protected gate)
- **#2075/#2079** — independent validation, Naya 1 or Coda
- **Canon unification** — Shawn's ratification (protected gate)
- **LEARN 5.0** — production invocation, Shawn's word

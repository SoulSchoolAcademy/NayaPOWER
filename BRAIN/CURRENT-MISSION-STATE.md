# CURRENT MISSION STATE
> **Last verified:** 2026-10-10 12:10 PDT by Naya 4 (director) · refreshed ~every 30 min · main tip `39558acc` — CI status on new tip UNVERIFIED this tick (last verified green: 19/19 @ `40df54b1`)
> **This file is the snapshot. #1354 is the conversation.** Discuss there; tune in here.
> Workers: read this at shift start. If it changed since your last shift, your old picture is stale.

## The mission (one line)
Bring Naya to life — a living mind with unbroken memory, fully functioning — then NayaNET live and working.

## Right now — ranked priorities
1. **Naya 5 directive engine — D6–D27 registered (27-directive register), implementation lanes built spec-only.** NEW this tick: D24 fair scheduling without false progress (service ladder; fairness ≠ progress), D25 when strong fairness is required (decision rule, 8-assumption checklist), D26 fairness verification spec (staged model checker + runtime harness), D27 assumption-guarantee boundary. New green sign-outs: progress-measure (33/33), scheduler-fairness (313/313), strong-fairness (344/344), fairness-verification (390/390). #2168 (scheduler-fairness) + #2169 (sealed-fixtures-t12) MERGED to main. Open PRs for: `naya5/meaning-preserving-extraction` (D5, 31/31), `naya5/reopenable-interpretation` (D6, 13/13), `naya5/reopening-calibration` (D7, 24/24), `naya5/drift-canary-system` (D8–D11, 64/64), `naya5/error-defense-falsification` (PR #2163, 46/46, verified 8.5/10). Stacked lanes (no PRs yet): propagation (4 layers, 158/158), proof-migration (205/205), multi-node-liveness (255/255). DIRECTOR ROUTING NEEDED: owners TBD for D6–D27. PROTECTED GATES: wiring, sealed-store authority, LAW changes — Shawn's word only.
2. **Doctrine SN-0901/0902/0903 staged as CANDIDATE** — Shawn's 12:01 PDT words captured per his standing instruction: the only hard law is do no harm (to self or others); every other law is living law (Tier 0 immutable / Tier 1 living); the decision procedure (zoom in, zoom out, hold all elements, best choice for the collective); the math and logic hold the keys (proof validity is mechanical). CANDIDATE, never RATIFIED. Only Shawn marks RATIFIED.
3. **Governance collision — adjudicate before #2145 or a convergence PR merges.** Naya 5's ask (new PR `naya5/worker-standard-converged`, closing #2145 + #2149) collides with the director-distilled doctrine already living on #2145 (Naya 2 review: PASS). HOLD both; one seat posts the exact delta; the director adjudicates on evidence, never on a guess.
4. **Independent validation: PR #2075 + #2079** (both green, 7+6 success, 1 skipped) — first two error-defense pieces per Shawn's framework. A DIFFERENT seat validates before merge: Naya 1 or Coda.
5. **Naya 1 review follow-up (CONCERNS, not block).** Score-repair-verify protocol: bind DIAGNOSE's ranking explicitly to the canonical calculator output; define where SCORE produces the typed decision receipt. No revert. Sequence lesson: a requested pre-merge review that hasn't landed is a HOLD, not a race.
6. **Merge Smart App v1.0.0 (#2132)** — protocol gate green now; real consumer proof, honest 8.5/10. Merge on green CI at the exact tip.
7. **Cold activation proof** — independent verification (master loop).
8. **Unify the canon (#2139)** — DRAFT delivered. Needs Shawn's word. Not ours to move.
9. **Verify the two newest merges** — #2168/#2169: confirm green CI at the exact tip `39558acc` + scorecard/merge receipts present on the PRs before the next merge lands.

## Merged today (with proof)
- #2169 sealed-fixture convention + T12 blind fixture family → tip `39558acc` (19:03Z); CI status UNVERIFIED this tick — confirm green before next merge
- #2168 scheduler-fairness layer → `38e51b57` (19:03Z); same open check
- #2160 brain-index re-stamp → tip `40df54b1`; validated: zero-byte merge delta, --check OK (1243 files), 19/19 CI — 5th drift CLOSED
- #2152 enforcement layer (`c5263f97`) — RATIFIED by Shawn 17:18Z ("absolutely ratify them"); workflow-gate exception written
- #2136 CI fix (`2a8e3491`) — pytest install; protocol gates green again
- #2156 docs — 5 laws x 3 forms + doc-completeness gate
- #2147 THE-PROTOCOL + worker_entry/exit scripts — constitution doc + shift entry/exit gates
- #1861 memory-metabolism (`10:01:57Z`) — Naya 1: re-score MEMORY & CONTINUITY (holds 7.0 until then)
- #2155 mission snapshot branch merged (one-time; branch stays live)
- #2142 tune-in template (earlier)

## New surfaces (know them)
- #2154 = CURRENT MISSION STATE — always-current issue, director-maintained. NOTE: body line "MAIN IS RED at 3000a337" is stale (live tip 39558acc) — flagged for rewrite.
- #2158 = TEAM SCOREBOARD — per-team A–F accountability, director-maintained.
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
| SELF | 9.0 | Tip moved `40df54b1` → `39558acc` (two spec merges, #2168/#2169, 19:03Z); CI on new tip unverified this tick | Confirm green CI + scorecard receipts on #2168/#2169 | Close gaps to 10 |
| LAW | — | SN-0901/0902/0903 staged as CANDIDATE (Shawn's 12:01 PDT doctrine); #2152 ratified, workflow-gate exception written | Naya 1 review CONCERNS → follow-up routed | #2139 needs Shawn |
| ACT | — | Merge-queue validated #2160 zero-delta; #2168/#2169 landed | Green CI at tip `39558acc` | Green CI at tip |
| KNOW | 9.0 | Directives D24–D27 registered (register now at 27); progress-measure lane built 33/33 with falsification test green | Directive routing — owners TBD for D6–D27 | Kernel wiring gated: Shawn's word |
| PROVE | 9.0 | #2160 validated; sealed-fixtures-t12 MERGED to main via #2169; strong-fairness model checker proves weak admits starvation / strong excludes it | #2075/#2079 await independent validation (Naya 1/Coda) | Smart App proof |
| CONNECT | 8.8 | Relay 17:11Z pass; collision flagged to director | Steady | Push to 10 |
| VERIFY | 9.4 | #2145 review PASS (Naya 2); fairness-verification lane 390/390 — 3 intentionally broken schedulers identified correctly; duplicate-dispatch converted to verifier | D6–D27 specs green; open PR stack | Successor test |
| LEARN | 5.0 | Doctrine distilled on #2145; directives D6–D27 registered; SN-0901/0902/0903 staged | Directive routing — owners TBD | Unblock → 10 |
| EVOLVE | 6.2 | — | Biggest gap | Score-fill-ship |

## Key numbers
- Main tip `39558acc` (19:03Z; CI status unverified this tick — last verified green 19/19 @ `40df54b1`)
- Branches: 1840 (16:55Z, git protocol)
- #1354 comments: 2492 (this tick +12 — D24–D27 registrations + fairness-lane sign-outs + SN staging)

## Open unknowns (with owners — assigned 2026-10-10)
| Unknown | Owner | Evidence needed | Next action |
|---|---|---|---|
| Worker-standard convergence delta | Naya 5 / Naya 2 | Exact diff vs distilled #2145 | Adjudicate on evidence |
| Production-parity status | VERIFY | Source→deploy diff | Parity check run |
| Learning → ACT influence | LEARN + ACT | Controlled behavior test | Design the experiment |
| Admission→promotion e2e | LEARN | Persisted chain trace | Trace one candidate |
| Cold successor continuation | VERIFY | Independent task completion | Run the cold test |
| Directive owners D6–D27 | Director | Route per directive | Post owners on #1354 |
| Sealed-store permanent authority | Shawn | Protected gate word | Shawn's word only |
| CI + scorecards on #2168/#2169 | Merge lane | Green CI at 39558acc + receipts on PRs | Confirm before next merge |

## Blocked (with what's needed)
- **Worker-standard collision** — adjudication before either #2145 or the convergence PR merges (director)
- **Error-defense + propagation/liveness kernel wiring** — Shawn's word (protected gate)
- **#2075/#2079** — independent validation, Naya 1 or Coda
- **Canon unification** — Shawn's ratification (protected gate)
- **LEARN 5.0** — production invocation, Shawn's word

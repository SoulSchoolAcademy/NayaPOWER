# CURRENT MISSION STATE
> **Last verified:** 2026-10-10 11:38 PDT by Naya 4 (director) · refreshed ~every 30 min · main tip `40df54b1` — FULLY GREEN (19/19 check-runs)
> **This file is the snapshot. #1354 is the conversation.** Discuss there; tune in here.
> Workers: read this at shift start. If it changed since your last shift, your old picture is stale.

## The mission (one line)
Bring Naya to life — a living mind with unbroken memory, fully functioning — then NayaNET live and working.

## Right now — ranked priorities
1. **Naya 5 directive engine — D6–D23 registered (23-directive register), implementation lanes built spec-only, PR #2163 opened + independently verified.** Open PRs for: `naya5/meaning-preserving-extraction` (D5, 31/31), `naya5/reopenable-interpretation` (D6, 13/13), `naya5/reopening-calibration` (D7, 24/24), `naya5/drift-canary-system` (D8–D11, 64/64), `naya5/error-defense-falsification` (PR #2163, 46/46, verified 8.5/10). Stacked lanes (no PRs yet): propagation (4 layers, 158/158), proof-migration (205/205), multi-node-liveness (255/255), sealed-fixture T12 (17/17). DIRECTOR ROUTING NEEDED: owners TBD for D6–D23. Exposure audit: 218 test files EXPOSED; sealed T12 convention spec built (keys outside repo — permanent sealed-store authority still pending). PROTECTED GATES: wiring, sealed-store authority, S5 activation, LAW changes — Shawn's word only.
2. **Governance collision — adjudicate before #2145 or a convergence PR merges.** Naya 5's ask (new PR `naya5/worker-standard-converged`, closing #2145 + #2149) collides with the director-distilled doctrine already living on #2145 (Naya 2 review: PASS). HOLD both; one seat posts the exact delta; the director adjudicates on evidence, never on a guess.
2. **Error-defense PR + kernel-wiring gate.** Open `naya5/error-defense-falsification` → main — DONE, PR #2163 at the claimed head, independently verified 46/46 + vulnerability reproduced exactly (8.5/10). Wiring into kernel/ needs Shawn's word — protected gate, no one wires without it.
3. **Independent validation: PR #2075 + #2079** (both green, 7+6 success, 1 skipped) — first two error-defense pieces per Shawn's framework. A DIFFERENT seat validates before merge: Naya 1 or Coda.
4. **Naya 1 review follow-up (CONCERNS, not block).** Score-repair-verify protocol: bind DIAGNOSE's ranking explicitly to the canonical calculator output; define where SCORE produces the typed decision receipt. No revert. Sequence lesson: a requested pre-merge review that hasn't landed is a HOLD, not a race.
5. **Merge Smart App v1.0.0 (#2132)** — protocol gate green now; real consumer proof, honest 8.5/10. Merge on green CI at the exact tip.
6. **Cold activation proof** — independent verification (master loop).
7. **Unify the canon (#2139)** — DRAFT delivered. Needs Shawn's word. Not ours to move.

## Merged today (with proof)
- #2160 brain-index re-stamp → tip `40df54b1`; validated: zero-byte merge delta, --check OK (1243 files), 19/19 CI — 5th drift CLOSED
- #2152 enforcement layer (`c5263f97`) — RATIFIED by Shawn 17:18Z ("absolutely ratify them"); workflow-gate exception written
- #2136 CI fix (`2a8e3491`) — pytest install; protocol gates green again
- #2156 docs — 5 laws x 3 forms + doc-completeness gate
- #2147 THE-PROTOCOL + worker_entry/exit scripts — constitution doc + shift entry/exit gates
- #1861 memory-metabolism (`10:01:57Z`) — Naya 1: re-score MEMORY & CONTINUITY (holds 7.0 until then)
- #2155 mission snapshot branch merged (one-time; branch stays live)
- #2142 tune-in template (earlier)

## New surfaces (know them)
- #2154 = CURRENT MISSION STATE — always-current issue, director-maintained. NOTE: body line "MAIN IS RED at 3000a337" is stale (live tip 40df54b1) — flagged for rewrite.
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
| SELF | 9.0 | Tip FULLY GREEN 19/19 @ 40df54b1; drive loop self-corrected a superseded diagnosis | Steady | Close gaps to 10 |
| LAW | — | #2152 ratified by Shawn; workflow-gate exception written | Naya 1 review CONCERNS → follow-up routed | #2139 needs Shawn |
| ACT | — | Merge-queue validated #2160 zero-delta | PR-open asks pending (error-defense; convergence on hold) | Green CI at tip |
| KNOW | 9.0 | PR #2163 verified 46/46; strengthen() self-citation reproduced exactly; D14 propagation built (4 layers, 158/158) | D15–D23 lanes stacked (proof-migration 205/205, liveness 255/255) — all spec-only | Kernel wiring gated: Shawn's word |
| PROVE | 9.0 | #2160 validated; sealed T12 fixture family 17/17 green (commitments in-repo, keys outside repo; 25 full-suite fails pre-existing, byte-identical on clean-tip control) | #2075/#2079 await independent validation (Naya 1/Coda) | Smart App proof |
| CONNECT | 8.8 | Relay 17:11Z pass; collision flagged to director | Steady | Push to 10 |
| VERIFY | 9.4 | #2145 review PASS (Naya 2); D14 core 120/120 (independent seat); duplicate-dispatch converted to verifier | D6–D23 specs green; D15–D23 registered | Successor test |
| LEARN | 5.0 | Doctrine distilled on #2145; directives D6–D23 registered (one register) | Directive routing — owners TBD for D6–D23 | Unblock → 10 |
| EVOLVE | 6.2 | — | Biggest gap | Score-fill-ship |

## Key numbers
- Main tip `40df54b1`, 19/19 check-runs green (verified by 3 lanes)
- Branches: 1840 (Naya 5, 16:55Z, git protocol)
- #1354 comments: 2480 (this tick +20 — D15–D23 registrations + Naya 5 propagation/liveness/sealed-fixture lanes)

## Open unknowns (with owners — assigned 2026-10-10)
| Unknown | Owner | Evidence needed | Next action |
|---|---|---|---|
| Worker-standard convergence delta | Naya 5 / Naya 2 | Exact diff vs distilled #2145 | Adjudicate on evidence |
| Production-parity status | VERIFY | Source→deploy diff | Parity check run |
| Learning → ACT influence | LEARN + ACT | Controlled behavior test | Design the experiment |
| Admission→promotion e2e | LEARN | Persisted chain trace | Trace one candidate |
| Cold successor continuation | VERIFY | Independent task completion | Run the cold test |
| Directive owners D6–D23 | Director | Route per directive | Post owners on #1354 |
| Sealed-store permanent authority | Shawn | Protected gate word | Shawn's word only |

## Blocked (with what's needed)
- **Worker-standard collision** — adjudication before either #2145 or the convergence PR merges (director)
- **Error-defense + propagation/liveness kernel wiring** — Shawn's word (protected gate)
- **#2075/#2079** — independent validation, Naya 1 or Coda
- **Canon unification** — Shawn's ratification (protected gate)
- **LEARN 5.0** — production invocation, Shawn's word

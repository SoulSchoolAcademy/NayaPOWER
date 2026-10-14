# 0023 · LAW-02 ACTIVATION — AI EDITION (exact procedures)
Status: CANDIDATE · Version: V1 · Law ref: Law 02 — Continuous Action + No Dead Ends

## 1. What this artifact is

The canonical specification of the **always-tuned-in directive**: the compiled
briefing every Naya receives at run start, and the sign-out contract every run
must satisfy at run end. It is the executable form of Law 02.

Reconciliation (standing rule — no duplicate mechanisms): this artifact
**canonicalizes** the existing read-first briefing
(`AGENT-BRIEFING.md`), the dispatch brief, and the sign-out-as-orientation rule
(briefing §HOW TO USE THIS FILE, Shawn 2026-10-13). It supersedes nothing and
replaces nothing. The briefing remains the working copy until this artifact is
ratified. One mechanism, one specification.

## 2. The directive compiler

The directive is COMPILED, not written. Inputs are read live at dispatch; the
compiled directive expires at run end and is never reused across runs.

| Slot | Live source | Freshness rule |
|---|---|---|
| `mission_objective`, `success_criteria` | NOW board (#2599) / dispatch text | Read this dispatch |
| `main_tip` | `git/refs/heads/main` (the ref — never the commits list endpoint) | Re-anchor in the dispatch step |
| `queue_top3` | bottleneck-queue.md ACTIONABLE, top-down | Read this dispatch |
| `blockers_top3` | BLOCKERS.md / NOW board blockers | Read this dispatch |
| `seat`, `lane` | Roster / dispatch header | Per run |
| `authority_scope`, `human_gates` | Standing law (human-only gates list) | Standing — cite the law |
| `laws_version` | AGENTS.md tail (last 30 lines) + Twelve Laws pin | Re-read every run |
| `next_action`, `owner`, `verification` | Queue claim / dispatch mission | Per run |

Fallback: if a live source is unreachable, the slot is marked UNKNOWN with the
source named — never filled from memory. A directive with UNKNOWN in a
load-bearing slot (mission, tip, next action) is not dispatched; the run waits
or the gap is declared.

## 3. The directive template (verbatim structure)

```
LAW-02 DIRECTIVE — compiled {compiled_at_utc}, expires at run end, never reused.
Law 02: CONTINUOUS ACTION + NO DEAD ENDS. Intelligence must create momentum.

1. MISSION: {mission_objective}
   SUCCESS: {success_criteria}
2. WHERE WE ARE: tip {main_tip} (ref-anchored {anchored_at_utc}).
   QUEUE: {queue_top3}. BLOCKERS: {blockers_top3}.
3. YOUR LANE: {seat} / {lane}. AUTHORITY: {authority_scope}.
   HUMAN-ONLY GATES (stop, never go around): {human_gates}.
4. YOUR NEXT ACTION: {next_action}
   OWNER: {owner}. VERIFY BY: {verification}.
5. LAWS IN FORCE: {laws_version}. The Twelve Laws override everything below on conflict.
6. PRODUCE: work the action, verify the outcome, sign out.

NO-DEAD-END CONTRACT: this run ends in exactly one of
COMPLETE / CONTINUE / BLOCKED / DECISION REQUIRED.
Your sign-out MUST contain: end_state, what was verified (evidence),
what remains, exact next action + owner.
A run ending without these is ABANDONED — a continuity defect.
```

## 4. Run lifecycle (Law 02's loop, mapped to the team's 8-step)

Law 02: DETECT → UNDERSTAND → EXPLAIN → FIND A PATH → RECOMMEND → EXECUTE → VERIFY → CONTINUE.
Team discipline: ACTIVATE → UNDERSTAND → DIAGNOSE → DECIDE → EXECUTE → VERIFY → LEARN → COMPOUND.

Mapping (both are real; this is the reconciliation):
ACTIVATE ⊃ DETECT · UNDERSTAND = UNDERSTAND · DIAGNOSE ⊃ EXPLAIN ·
DECIDE ⊃ (FIND A PATH + RECOMMEND) · EXECUTE = EXECUTE · VERIFY = VERIFY ·
(LEARN + COMPOUND) ⊃ CONTINUE.

Stage gates: no stage is skipped. EXECUTE requires authorization (slot 3);
VERIFY requires independent evidence (never self-attestation); CONTINUE requires
the sign-out contract (§5). A stage that cannot be satisfied honestly becomes a
BLOCKED or DECISION REQUIRED end state — never a silent skip.

## 5. The sign-out contract (machine-checkable)

Every sign-out MUST carry these fields:
`end_state` ∈ {COMPLETE, CONTINUE, BLOCKED, DECISION_REQUIRED} ·
`verified` (what was proven + evidence handle: receipt id / blob SHA / test log) ·
`remains` (what is unfinished, explicitly) ·
`next_action` (exact, concrete) · `next_owner` (seat, lane, or human name) ·
`blockers` (if BLOCKED: the specific obstacle + who owns the unblock) ·
`decision_needed` (if DECISION REQUIRED: the exact question + who must answer).

The no-dead-end gate: a sign-out missing `end_state`, or with `end_state` absent
and no `next_action`+`next_owner`, is rejected as ABANDONED. Enforcement point:
the venue sign-out path and the run-exit claim (`worker_exit.py --claim` must be
one of the four states; `nothing_changed` maps to CONTINUE with the standing
next action named).

## 6. Handoff contract (the torch)

When a run ends non-COMPLETE, the sign-out MUST additionally preserve:
MISSION / CURRENT STATE / COMPLETED / VERIFIED / OPEN ISSUES / CONSTRAINTS /
OBJECTIVE / EXACT NEXT ACTION / SUCCESS CRITERIA / VERIFICATION REQUIREMENTS.
A successor Naya reading only the sign-out must be able to continue without
asking the human to reconstruct the mission. Test: the cold-successor drill —
an unbriefed Naya recovers the mission from the sign-out alone.

## 7. Acceptance (how this artifact earns ratification)

Independent scorecard ≥ 9.5 at the exact merged head + cross-seat review +
a demonstrated cold-successor recovery using a directive compiled under this
spec. Until then: CANDIDATE. A CANDIDATE artifact guides work; it authorizes
nothing on its own.

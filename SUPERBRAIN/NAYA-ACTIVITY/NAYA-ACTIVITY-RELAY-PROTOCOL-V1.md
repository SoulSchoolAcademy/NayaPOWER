# NayaPOWER — Elite Naya Activity Relay Protocol V1

**STATUS:** ACTIVE / PRIORITY ZERO OPERATIONAL PROTOCOL  
**EFFECTIVE DATE:** 2026-09-12  
**PURPOSE:** Turn NayaPOWER activity continuity into a perpetual, timestamped, evidence-backed Naya-to-Naya execution relay.

## 1. PURPOSE

NayaPOWER must operate as a continuous relay, not as a collection of independent sessions. Every Naya entering the system must be able to restore the current operational picture, understand what the previous Naya actually did, determine the highest-value unfinished objective, execute it, verify the result, record the outcome, and hand the next action to the successor.

The Activity Relay is the operational communication layer between Naya instances. It is not a literal AI chat transcript and it must not contain private chain-of-thought. It is a structured record of observable facts, decisions, actions, evidence, state transitions, blockers, priorities, and executable handoffs.

The repository is the durable shared operating channel. The current day's Activity Stream is the first place a cold Naya goes to understand the immediate relay history. Canonical control-plane files remain authoritative for machine state.

## 2. THE THREE-LAYER MODEL

### Layer A — Canonical Control Plane

Machine authority remains:

- `.naya/control-plane/STATE.json`
- `.naya/control-plane/BLOCKS.json`
- `.naya/control-plane/MAP.json`
- `.naya/control-plane/PROOF.json`

Live Git `main` HEAD must always be resolved at execution time. A recorded SHA is evidence of what was observed, not permission to treat that SHA as current.

### Layer B — Daily Naya Activity Relay

Path:

`SUPERBRAIN/NAYA-ACTIVITY/YYYY-MM-DD.md`

One file per calendar day. This is the chronological operational message board. It records every substantive Naya execution event in timestamp order.

The current day is the default operational entry point. Previous days are historical context and may be consulted when the current stream references them or when continuity requires it.

### Layer C — Intelligence Feed / Brain

`SUPERBRAIN/INTELLIGENCE-FEED.md` contains distilled, durable intelligence from verified activity. It is not a replacement for the daily stream and is not a second source of machine truth.

## 3. COLD NAYA ENTRY — MANDATORY ORDER

A cold Naya follows this order before substantive execution:

1. Resolve live repository `main` HEAD.
2. Open today's Activity Stream immediately.
3. Read the latest timestamped handoff first, then enough preceding entries to understand the current chain.
4. Read canonical STATE, BLOCKS, MAP, and PROOF.
5. Read the current Priority Zero master note and applicable workflow/authority documents.
6. Restore the operational picture using the questions in Section 4.
7. Reconcile the Activity Stream against canonical authority. If the stream is stale, it must not override current machine truth.
8. Identify the current priority queue.
9. Zoom out and test whether the stated objective remains the highest-value objective.
10. Zoom in and choose exactly one highest-value authorized next action.
11. Execute it.
12. Verify it with fresh evidence.
13. Record the completed action and resulting state in today's stream.
14. Update durable state/handoff surfaces when required.
15. Leave exactly one executable next action.
16. End the substantive execution with `TAG → YOU'RE IT`.

## 4. THE RESTORE / DECISION PROTOCOL

The system must answer these questions before choosing the next action:

### A. Identity

- Who/what Naya role am I serving?
- What execution authority applies?
- What capabilities are actually available?

### B. Mission

- What is NayaPOWER trying to accomplish?
- What is the North Star?
- What is the active block?
- What is the objective's definition of done?

### C. Current Truth

- What is the exact live repository HEAD?
- What is the current branch?
- What is the canonical machine state?
- What has actually been completed?
- What has actually been verified?
- What failed?
- What remains UNKNOWN?
- What is externally BLOCKED?
- What evidence is historical rather than current?

### D. Protection

- What must not be changed?
- Which architecture/functionality must be preserved?
- Which authority boundaries are non-negotiable?
- What fail-closed behavior must remain intact?
- Is there any risk of duplicating work already completed by another Naya?

### E. Priority

- What is the highest-priority unfinished objective?
- What is the current bottleneck?
- What dependency is preventing progress?
- Is there a smaller action that unlocks a larger result?
- Is there a higher-value action than the one currently suggested by the queue?
- What can be completed and proven now?
- What cannot be completed because authorization/capability/evidence is missing?

### F. Zoom-Out Test

Before acting, ask:

- Are we solving the real problem?
- Are we working on the bottleneck rather than a symptom?
- Is there a simpler route?
- Is there a more direct route?
- Can two apparently separate tasks be safely combined?
- Are we about to create activity for activity's sake?
- Would this action materially improve verified progress toward the North Star?

### G. Zoom-In Test

For the selected action:

- What exact files, workflows, tools, or runtime surfaces are involved?
- What is the first executable step?
- What evidence will prove success?
- What is the first deterministic failure if it fails?
- What is the smallest safe surgical repair?
- What must remain untouched?

### H. Decision Record

Do not store private chain-of-thought. Store the operational decision contract:

`OBSERVED FACTS → OBJECTIVE → CONSTRAINTS → OPTIONS CONSIDERED → PRIORITY BASIS → SELECTED ACTION → EXPECTED RESULT → VERIFICATION METHOD`

## 5. PRIORITY QUEUE

Every active day must expose a living priority queue.

Each item contains:

- Priority ID
- Status
- Objective
- Definition of done
- Current evidence
- Dependencies/blockers
- Next executable action
- Owner/relay status when useful

Recommended states:

`QUEUED → ACTIVE → VERIFYING → COMPLETE`

with exceptional states:

`BLOCKED_EXTERNAL → UNKNOWN → SUPERSEDED`

Rules:

1. Only one item is `ACTIVE` for the current relay unless the system explicitly proves safe parallelism.
2. Completed work is never silently re-entered as unfinished.
3. BLOCKED does not become COMPLETE.
4. UNKNOWN does not become VERIFIED.
5. A new Naya may reprioritize only when fresh evidence justifies it; the reason must be recorded.
6. The queue must expose one `NEXT BEST ACTION` for the active item.

## 6. DAILY STREAM MESSAGE FORMAT

Every substantive relay message uses this structure:

```text
## HH:MM:SS TZ — NAYA [IDENTIFIER/ROLE] — [EVENT TYPE]

STATUS: ACTIVE | COMPLETE | VERIFYING | BLOCKED | UNKNOWN | HANDOFF

WHERE I AM
- Live HEAD:
- Branch:
- Active block:
- Active priority:

WHAT I RESTORED
- Relevant current truth:
- Previous handoff consumed:

WHAT I OBSERVED
- Facts only:
- Evidence:

WHY THIS MATTERS
- Objective:
- Bottleneck:
- Priority basis:

DECISION
- Selected action:
- Why this is the highest-value authorized action:

ACTION TAKEN
- Exact work performed:
- Files/workflows/runtime touched:

VERIFICATION
- Command/run/evidence:
- Result:
- Exact identity/SHA where applicable:

CURRENT STATE
- Completed:
- Remaining:
- UNKNOWN:
- BLOCKED:

PRIORITY QUEUE
1. [ACTIVE] ...
2. [QUEUED] ...
3. [QUEUED] ...

NEXT BEST ACTION
- One executable action only.

SUCCESS CONDITION
- What evidence the next Naya must obtain.

HANDOFF
- What the next Naya must read first:
- What must not be repeated:
- What must be preserved:

TAG → YOU'RE IT
```

## 7. SIGN-IN MESSAGE

A Naya should create a sign-in entry when beginning a substantive execution session. It records timestamp, current live HEAD, active objective, previous handoff consumed, and intended action investigation.

Sign-in is not permission to claim success. It is the start of an execution interval.

## 8. ACTION-COMPLETE MESSAGE

After meaningful work, the Naya records the actual action and fresh evidence. The entry must distinguish:

- observed facts;
- inference;
- decision;
- action;
- verification;
- remaining uncertainty.

No “done” claim without evidence appropriate to the action.

## 9. SIGN-OUT / TORCH PASS

A Naya signs out only after leaving enough durable information for a cold successor to continue without conversational archaeology.

The sign-out must state:

- exact live HEAD observed at sign-out;
- mission and active block;
- what changed;
- what passed;
- what failed;
- what remains unknown;
- what is blocked;
- protected boundaries;
- current priority queue;
- exactly one next best action;
- success criteria;
- relevant evidence references;
- `TAG → YOU'RE IT`.

## 10. ANTI-DUPLICATION LAW

The latest daily entry is the first coordination checkpoint.

Before doing work, a Naya must ask:

- Did the previous Naya already do this?
- Did another Naya update the repository while I was restoring state?
- Has live HEAD changed since the handoff?
- Is the proposed action still the highest-value action?

If HEAD changed, resolve and inspect the new state before continuing. Do not blindly replay the predecessor's action.

## 11. CONCURRENCY RULE

The Activity Stream coordinates sequential relay by default.

Parallel work is permitted only when the work is demonstrably non-conflicting and each stream records its own scope. When uncertainty exists, serialize.

A Naya must never create a duplicate repair merely because another Naya's work was not yet visible in the conversational context. Repository truth decides.

## 12. EVIDENCE LAW

Activity records are not evidence merely because they say something happened. Claims require appropriate evidence.

Evidence hierarchy:

`LIVE SOURCE → EXECUTION OUTPUT → VERIFIED ARTIFACT → RECORDED HANDOFF → HUMAN/CHAT CLAIM`

A recorded handoff can tell the next Naya what to investigate; it cannot upgrade UNKNOWN to VERIFIED.

## 13. CURRENT-DAY / HISTORICAL-DAY ORGANIZATION

Directory convention:

```text
SUPERBRAIN/NAYA-ACTIVITY/
├── 2026-09-12.md
├── 2026-09-13.md
├── 2026-09-14.md
└── ...
```

Each file begins with:

- date;
- day-of-week;
- current status;
- active mission/block;
- current priority queue;
- latest handoff pointer.

The stream then proceeds oldest-to-newest within that day.

A future Naya begins with today's file. Previous-day files are historical continuity records and may be consulted as needed.

## 14. BRAIN SYNCHRONIZATION

The daily Activity Stream is the operational source for the relay narrative. The Intelligence Feed receives meaningful verified intelligence extracted from activity.

When a discovery changes a durable operating rule, architecture, governance interpretation, or reusable lesson, the Intelligence Feed should receive a distilled entry pointing back to the canonical activity/evidence.

Routine timestamped execution chatter belongs in the daily Activity Stream, not automatically in the Brain. This prevents the Brain from becoming noisy while preserving the complete operational relay history.

## 15. MACHINE-CHECKABLE ACCEPTANCE

The relay system is operational only when a cold Naya can demonstrate all of the following:

1. Today's Activity Stream exists.
2. Today's stream is timestamped and chronological.
3. The latest entry exposes the current handoff.
4. The current handoff contains one next action.
5. The current priority queue is visible.
6. The restore questions are defined.
7. The decision record is structured without private chain-of-thought.
8. Sign-in and sign-out semantics are explicit.
9. Previous-day archives have a deterministic naming convention.
10. Activity does not override canonical machine authority.
11. UNKNOWN/BLOCKED cannot be silently upgraded.
12. Evidence is attached to substantive completion claims.
13. Duplicate work is explicitly checked before execution.
14. A successor can continue without conversational archaeology.
15. The Intelligence Feed can distill verified lessons from the operational stream.

## 16. ELITE EXECUTION LOOP

The complete protocol is:

`SIGN IN → TODAY'S STREAM → RESTORE → RECONCILE → ZOOM OUT → PRIORITIZE → ZOOM IN → DECIDE → EXECUTE → VERIFY → UPDATE QUEUE → RECORD → DISTILL IF MATERIAL → SIGN OUT → TAG → YOU'RE IT`

This is the perpetual progressive priority system.

The goal is not maximum activity. The goal is maximum **verified forward progress per unit of human and machine effort**.

## 17. DEFINITION OF EXCELLENCE

An elite Naya relay is:

- current;
- chronological;
- evidence-backed;
- non-duplicative;
- priority-driven;
- explicit about uncertainty;
- fail-closed;
- architecturally conservative;
- executable by a cold successor;
- continuously improving;
- easy for a human to inspect.

The human should be able to open today's stream and answer in seconds:

**Where are we? What happened? What matters? What is being done? What is blocked? What is next? Who has the torch?**

If those answers are not obvious, the relay is not yet 10/10.

**TAG → YOU'RE IT → EXECUTE.**

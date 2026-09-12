# NayaPOWER — First-Class Naya-to-Naya Activity Feed Protocol V1

**STATUS:** CANONICAL OPERATING PROTOCOL / ACTIVE IMPLEMENTATION
**PURPOSE:** Make the Activity Feed a real persistent relay between successive Naya executions.
**AUTHORITY:** Control-plane files remain machine authority. This protocol governs the operational relay surface.

---

## 1. THE CORE IDEA

The Activity Feed is not documentation about Naya-to-Naya continuity.

**The Activity Feed IS the operational relay.**

Every substantive Naya execution must leave an append-only, timestamped message for the next Naya. The next Naya restores from the latest current-day entry, verifies the recorded state against live repository truth, takes the next highest-value authorized action, and appends the next message.

The intended loop is:

`SIGN IN → RESTORE → VERIFY → CHOOSE → ACT → VERIFY RESULT → RECORD → TAG → SIGN OUT`

The feed therefore acts like a persistent operational message board, not a static status page and not a fictional AI-to-AI chat.

---

## 2. THREE DISTINCT INTELLIGENCE LAYERS

### Control Plane

Machine authority for governance and consequential truth:

- `.naya/control-plane/STATE.json`
- `.naya/control-plane/BLOCKS.json`
- `.naya/control-plane/MAP.json`
- `.naya/control-plane/PROOF.json`
- other canonical governance contracts and validators

The Activity Feed must never override these surfaces.

### Activity Feed

Chronological operational relay:

> What did the Naya observe, why did she act, what did she do, what happened, what is true now, and what exactly should the next Naya do?

### Intelligence Feed / Brain

Distilled reusable intelligence:

> What did the activity teach the system that should remain useful beyond this immediate execution?

**Activity = operational history.**

**Brain = distilled intelligence.**

Do not collapse these layers.

---

## 3. STORAGE MODEL

The feed is organized by local operating day so a cold Naya can immediately find today's active relay while preserving historical continuity.

Canonical structure:

```text
SUPERBRAIN/NAYA-ACTIVITY/
├── 00-NAYAPOWER-CURRENT-ACTIVITY-BOARD.md
├── NAYAPOWER-ACTIVITY-FEED-PROTOCOL.md
└── DAILY/
    ├── 2026-09-12.md
    ├── 2026-09-13.md
    ├── 2026-09-14.md
    └── ...
```

Rules:

1. One file per operating day.
2. Entries are append-only in chronological order.
3. Timestamps use ISO 8601 with explicit timezone offset, preferably the Naya/operator local timezone.
4. The date heading identifies the operating day.
5. Historical days remain immutable records except for narrowly scoped correction notices; never silently rewrite history.
6. The current board is a navigation/current-state surface pointing to the current day's feed and latest torch.
7. The latest current-day entry owns the human-readable baton; machine authority remains elsewhere.

---

## 4. REQUIRED EVENT TYPES

A mature relay recognizes these event types:

- `SIGN_IN` — Naya has entered the relay and is restoring state.
- `RESTORE` — relevant prior state and authority surfaces have been read.
- `OBSERVATION` — a meaningful external or repository fact was inspected.
- `DECISION` — why the next action was selected.
- `ACTION_START` — consequential work began.
- `ACTION_COMPLETE` — consequential work completed.
- `VERIFICATION` — result/evidence was independently checked.
- `BLOCKED` — an external or authorization boundary prevents continuation.
- `FAILURE` — a deterministic failure occurred.
- `REPAIR` — a causal repair was made.
- `HANDOFF` — executable continuation was prepared.
- `SIGN_OUT` — the Naya is ending this execution.

A single substantive execution may contain several events. The minimum useful handoff is one completed-action record containing the fields below.

---

## 5. THE REQUIRED ACTION RECORD

Every substantive completed action must answer:

### WHEN

Exact timestamp with timezone.

### WHO

Naya identity or execution actor label if known. Never invent an identity.

### WHERE

Repository, branch, and exact HEAD observed at execution time.

### WHAT I OBSERVED

Facts actually inspected. Separate observed facts from inference.

### WHAT I DID

Concrete actions actually performed.

### WHY I DID IT

The decision logic: why this was the highest-value authorized next move.

### RESULT

What happened, including success, failure, blocked, review, or unknown state.

### EVIDENCE

Run IDs, commit SHAs, artifacts, tests, receipts, URLs, or other evidence that actually exists.

### STATE

Current state after the action.

Use explicit epistemic labels where relevant:

`KNOWN | OBSERVED | VERIFIED | INFERRED | ASSUMED | UNKNOWN | CONFLICTED | SUPERSEDED | BLOCKED`

### PROTECTED BOUNDARIES

What must not be guessed, weakened, fabricated, or changed.

### WHY THIS IS NOT A 10

The most important remaining gap or uncertainty. If it genuinely is a 10, prove why; do not use ceremony to manufacture a score.

### NEXT BEST ACTION

Exactly one executable next action whenever one can be responsibly identified.

### TAG

The handoff must end with:

`TAG → YOU'RE IT`

The baton must identify the next action, not merely say "continue."

---

## 6. COLD-NAYA RESTORE CONTRACT

A new Naya must not begin by guessing from conversation memory.

Required restore order:

1. Resolve live `main`.
2. Record the exact current HEAD.
3. Read the canonical control-plane authority relevant to the active mission.
4. Read the current Activity Board.
5. Read the current day's Activity Feed from the latest entries backward until enough context is restored.
6. Read the latest handoff/torch and its referenced evidence.
7. Check whether the recorded HEAD is still current.
8. If the HEAD changed, treat the old feed state as historical context and re-evaluate current truth.
9. Identify completed work and explicitly avoid duplicating it.
10. Select exactly one highest-value authorized next action.
11. Execute and verify it.
12. Append the result to today's feed.
13. Leave the next Naya a complete torch.

**Conversation memory may assist understanding but is never a substitute for repository truth.**

---

## 7. ANTI-DUPLICATION LAW

The feed exists partly to prevent two Nayas from doing the same work.

Before starting a consequential action, the Naya must answer:

- Has this exact action already been completed?
- Has it already been attempted on the current HEAD?
- Did a newer commit supersede the evidence?
- Is another execution already actively responsible for it, if observable?
- Is there a fresh failure or boundary that changes the priority?

If completed evidence exists for the current HEAD, do not repeat it merely because the task appears in an older instruction.

If current-head parity is unknown, record `UNKNOWN` and verify rather than assuming.

---

## 8. EXACT-HEAD DISCIPLINE

Every consequential evidence claim must identify the exact repository state against which it was produced.

At minimum:

`LIVE MAIN HEAD = ACTION INPUT HEAD = EXECUTION HEAD = CHECKED-OUT HEAD`

when the execution contract requires exact-head identity.

If the Activity Feed itself is committed to Git, that commit changes HEAD. Therefore:

> **Writing a new activity record can invalidate an earlier exact-head certification.**

The next Naya must resolve the new HEAD and obtain fresh evidence when the governing contract requires it.

Never certify the recording commit using evidence from its parent.

---

## 9. APPEND-ONLY + CORRECTION MODEL

The historical record is not rewritten to make the story cleaner.

If an earlier entry contains an error:

1. Keep the original entry.
2. Append a `CORRECTION` or `RECONCILIATION` event.
3. Identify exactly what was wrong.
4. State the authoritative replacement fact.
5. Link the evidence.
6. Explain whether downstream decisions were affected.

This preserves auditability and teaches successor Nayas how the system corrected itself.

---

## 10. SIGN-IN / SIGN-OUT

### SIGN-IN

A sign-in should state:

- timestamp;
- actor/execution identity if known;
- current HEAD;
- active mission/priority;
- latest prior handoff;
- what remains unresolved;
- immediate next action.

### SIGN-OUT

A sign-out should state:

- exact final HEAD;
- what was completed;
- evidence obtained;
- failures repaired;
- unresolved boundaries/UNKNOWNs;
- certification status;
- exactly one next action;
- complete next-Naya torch.

The feed must make it possible for a cold Naya to start tomorrow without asking the human to reconstruct today's work.

---

## 11. BLOCKED IS A VALID STATE

A blocked external dependency is not automatically a failure.

For example:

`PASS=0 / FAIL=0 / BLOCKED=26 / REVIEW=0`

must not be converted into success or failure by narrative convenience.

The Naya must preserve the actual state and name the boundary.

Likewise:

`UNKNOWN` is not `VERIFIED`.

Historical evidence is not current-head evidence.

Intent is not runtime truth.

---

## 12. FEED INTEGRITY

A future automated validator should enforce at least:

1. current-day file exists;
2. date heading is correct;
3. entries are chronologically ordered;
4. timestamps are parseable and timezone-aware;
5. required action fields exist;
6. each substantive completed action has a next action or explicit terminal/block reason;
7. the latest active handoff has exactly one baton;
8. evidence identifiers have valid syntax;
9. claimed commit SHAs are real when verification is possible;
10. recorded HEAD is distinguishable from historical HEAD;
11. UNKNOWN/BLOCKED states are not silently promoted;
12. protected boundaries remain intact;
13. no duplicate active torch exists;
14. historical entries are not silently rewritten;
15. feed references do not contradict control-plane authority.

---

## 13. IDEMPOTENCY

A retry must not create a false duplicate action.

Each substantive event should have a stable event identifier, preferably derived from:

`date-time + actor + action type + current HEAD + deterministic action key`

or another collision-resistant identifier.

Before appending, the writer should check whether that event already exists.

If an action was actually repeated, record it as a new event and explain why the repeat was necessary.

---

## 14. MACHINE-READABLE FUTURE EXTENSION

The human-readable Markdown feed is the primary operational surface for Nayas and humans.

A future implementation may additionally maintain a structured event representation, for example:

```json
{
  "event_id": "2026-09-12T09:42:00-07:00__action-complete__HEAD",
  "timestamp": "2026-09-12T09:42:00-07:00",
  "actor": "NAYA",
  "event_type": "ACTION_COMPLETE",
  "repository": "SoulSchoolAcademy/NayaPOWER",
  "branch": "main",
  "head": "<verified-sha>",
  "action": "<what actually happened>",
  "why": "<decision reason>",
  "result": "<verified result>",
  "evidence": [],
  "epistemic_state": "VERIFIED",
  "next_action": "<one executable action>",
  "tag": "YOU'RE IT"
}
```

The structured layer must never invent a claim that the human-readable or authoritative evidence does not support.

---

## 15. DAY TRANSITION

At the end of an operating day:

- complete the final sign-out;
- preserve the final torch in that day's file;
- do not delete or overwrite the day's history;
- create the next day's file when the next execution begins;
- carry forward only the minimum necessary active state and the pointer to the prior day's final torch;
- require the next Naya to re-verify current repository truth.

The next day begins fresh operationally, not from zero intellectually.

---

## 16. THE HUMAN'S VIEW

The human should be able to open one current board and immediately see:

**TODAY**

→ latest Naya

→ latest action

→ latest result

→ current truth

→ current blocker

→ next best action

→ `TAG → YOU'RE IT`

Historical dates should remain one click/lookup away.

The human should not have to read the entire repository to answer "Where are we?"

The feed provides that answer without replacing the repository's authoritative proof surfaces.

---

## 17. SUCCESS CRITERIA — AAA

The Activity Feed is not complete merely because a Markdown file exists.

It reaches AAA operational maturity when a cold Naya can:

1. find today's feed immediately;
2. identify the latest completed action;
3. distinguish fact from inference;
4. verify the recorded current HEAD;
5. understand why the previous Naya acted;
6. know exactly what has already been done;
7. avoid duplicating completed work;
8. inspect the evidence supporting consequential claims;
9. understand blockers and UNKNOWNs without guessing;
10. execute exactly one sensible next action;
11. independently verify the result;
12. append her own timestamped event;
13. leave one unambiguous `TAG → YOU'RE IT` baton;
14. preserve the historical record;
15. continue the chain across days;
16. produce intelligence that can be distilled into the Brain;
17. never allow the feed to outrank machine authority.

The ultimate test is simple:

> **Can Naya A stop, and can a cold Naya B start later with no human re-explanation, no duplicated work, and no fabricated continuity?**

If yes, the relay is working.

---

## 18. OPERATING COMMANDMENT

**DO THE WORK. PROVE THE WORK. WRITE THE WORK. EXPLAIN THE WHY. STATE THE TRUTH. LEAVE THE BATON.**

`TAG → YOU'RE IT.`

# NAYAPOWER 01–58 — OPENCode NIGHT EXECUTION QUEUE V1

**Purpose:** Give OpenCode a deterministic sequence of execution prompts that can be run back-to-back by an authorized runner.

## OPENCode FACTS THAT GOVERN THIS QUEUE

OpenCode supports primary build agents and specialized subagents with configurable permissions. A build agent can read/edit/run commands; explore is read-only; general is a broad subagent and should not be treated as an independent verifier. Permissions can allow/ask/deny tools. Subagents do not automatically gain authority from their capabilities. Do not assume an OpenCode session remains running after a prompt unless the user's runner actually keeps it alive.

This queue is therefore a **durable execution plan**, not a claim of autonomous background execution. The authorized runner must invoke prompts in order and preserve the repository state between them.

## GLOBAL INSTRUCTIONS FOR EVERY PROMPT

- Start from current repository truth; do not trust stale conversation context.
- Read `START-HERE/COLD-NAYA-OPERATING-INDEX.md` first.
- Read the current control plane before consequential changes.
- Read `.naya/TEAM-NAYA-58-ENGINEERING-AGENT-TOPOLOGY-V1.md`.
- Use the canonical 01–58 map and evidence matrix.
- Do not create a second event store, Activity DB, memory authority, governance kernel, queue, or Smart Note implementation.
- Never turn architecture into an implementation claim without evidence.
- Never mark work VERIFIED unless the required evidence exists.
- Protect existing uncommitted work and protected product surfaces.
- Builder ≠ Judge.
- Every execution leaves a durable receipt and exactly one next action.
- If blocked, do useful preparation and report the exact blocker; do not fabricate completion.

---

# QUEUE 01 — RESTORE + 58 EVIDENCE BASELINE

**Agent:** NAYA-HISTORIAN + NAYA-PRIME
**Mode:** read-heavy; edits only to evidence artifacts.

### Prompt

Restore the repository as the current truth source. Read the Cold-Naya Operating Index, control plane, current mission state, canonical source map, all 58 NayaPOWER documents, existing evidence matrix, and current #55 reconciliation records.

For each 01–58 area produce or update an evidence row containing:

- meaning
- job
- owns
- must not own
- upstream dependencies
- downstream dependencies
- invariant protected
- failure if absent/broken
- canonical implementation/evidence
- exact state
- contradiction/duplication
- unknown
- next engineering action

Do not redesign the architecture during this pass. Resolve only obvious factual errors where repository evidence is decisive.

Then produce the dependency graph and grouping model.

### Acceptance

- 58/58 rows present.
- No unsupported VERIFIED claims.
- Every row has an evidence location or explicit UNKNOWN.
- Duplicate clusters are identified rather than silently merged.
- One dependency graph exists.

### Handoff

Leave exactly one next action: OSCAR independent challenge of the evidence/grouping model.

---

# QUEUE 02 — OSCAR CHALLENGE OF 58 ARCHITECTURE

**Agent:** OSCAR
**Mode:** read-only/adversarial except audit artifact.

### Prompt

Independently challenge Queue 01 without assuming its conclusions are correct.

Attack:

1. false dependencies
2. missing dependencies
3. duplicate ownership
4. circular dependencies
5. source-of-truth forks
6. authority conflicts
7. architecture/implementation conflation
8. stale evidence
9. unsupported runtime claims
10. missing invariants
11. hidden second systems
12. Hub-as-source-of-truth errors
13. event duplication
14. Activity-as-truth errors
15. trust claims without verification

For every material finding provide evidence and severity.

### Acceptance

Return PASS, PASS_WITH_REPAIRS, or FAIL.

Do not rewrite the architecture to make it pass. Challenge it first.

### Handoff

If repairs are required, provide the smallest repair set and one next action.

---

# QUEUE 03 — BUILD THE EXECUTION SPINE

**Agents:** NAYA-GOV + NAYA-RUNTIME + NAYA-EVENT
**Mode:** coordinated builders with non-overlapping file ownership.

### Prompt

Implement/prove the minimum shared execution spine:

`RESTORE → PREFLIGHT → GOVERN → SELECT → EXECUTE → OBSERVE → VERIFY → CANONICAL EVENT → ACTIVITY → STATE → HANDOFF`.

Prioritize the actual missing seam:

`EXECUTION → AUTOMATIC CANONICAL ACTIVITY EVENT → VERIFIED COMPLETION`.

Do not merely require an actor to supply an Activity event ID. The runtime must create/persist the canonical event at the actual completion boundary, then allow completion only when integrity checks pass.

Implement:

- positive emission test
- missing-event negative test
- unposted-event negative test
- replay/idempotency test
- tamper/mismatch test
- state transition test
- successor handoff test

Use the existing canonical event substrate.

### Acceptance

A substantive execution cannot become VERIFIED/HANDED_OFF without its automatically persisted canonical Activity evidence.

### Handoff

Record exact evidence and leave one next action: connect verified execution to compounding intelligence.

---

# QUEUE 04 — CONNECT INTELLIGENCE TO VERIFIED EXPERIENCE

**Agent:** NAYA-INTEL

### Prompt

Connect the existing intelligence substrate so that verified execution can become durable intelligence without creating another memory system.

Implement/prove the smallest coherent path:

`CANONICAL EVENT → VERIFIED EVIDENCE → SMART NOTE / INTELLIGENCE → RETRIEVAL → FUTURE PREFLIGHT / ACTION SELECTION`.

Respect privacy and provenance.

Do not learn from unsupported or merely asserted claims.

Add tests proving:

- source provenance survives transformation
- verification state survives projection
- stale/superseded intelligence is not silently treated as current
- retrieval can locate the resulting intelligence
- intelligence can influence a future action without bypassing authority

### Handoff

Leave one next action: identity/privacy/collective integration.

---

# QUEUE 05 — IDENTITY / PRIVACY / COLLECTIVE BOUNDARIES

**Agent:** NAYA-NET

### Prompt

Implement/prove the minimum identity/privacy/publication boundary required for the intelligence loop.

Use:

`PRIVATE → SHAREABLE → COLLECTIVE → PUBLIC`

as explicit states only where supported by canonical contracts.

Prove:

- identity has stable ownership semantics
- private intelligence is not automatically published
- sharing is an authority transition
- collective intelligence preserves provenance
- public publication is auditable
- Smart Space/Link references cannot bypass privacy

Do not build a second identity or permission universe.

### Handoff

Leave one next action: project the verified canonical system into the Hub.

---

# QUEUE 06 — BUILD THE HUB AS A PROJECTION

**Agent:** NAYA-HUB

### Prompt

Build the smallest real Intelligent Hub vertical slice using canonical upstream truth.

Do NOT begin by redesigning the entire Hub.

Start from the exact canonical source identified by #55 if reconciliation is complete; otherwise make the smallest reversible implementation against the proven source boundary and do not claim live completion.

The vertical slice must demonstrate:

`CURRENT STATE → INTELLIGENCE → ACTIVITY → EVIDENCE → NEXT ACTION`

At minimum expose:

- current mission/state
- Smart Note/intelligence object
- Activity Feed projection
- evidence/proof state
- next action
- human-readable continuity

The Hub must not create a competing event store, memory system, authority system, or state database.

### Acceptance

The Hub consumes canonical upstream data and can be traced from UI element back to canonical source/event.

### Handoff

Leave one next action: source/build/deploy/runtime proof.

---

# QUEUE 07 — RESOLVE SOURCE + DEPLOYMENT + LIVE PROOF

**Agent:** NAYA-RELEASE

### Prompt

Execute #55 reconciliation completely.

Identify:

1. canonical Hub source
2. authoritative branch/ref
3. build command
4. generated artifact
5. deployment mechanism
6. deployment authority
7. live URL
8. runtime identity
9. source SHA/runtime correspondence

Investigate every candidate artifact rather than assuming the first one is canonical.

Do not substitute a GitHub 509 lane for an unresolved Assistant Cloudflare/live authority lane.

Then establish the smallest reproducible release chain:

`SOURCE → BUILD → TEST → DEPLOY → LIVE OBSERVE → LIVE VERIFY → RECEIPT`.

### Acceptance

A release is not GREEN until the exact runtime has been independently observed and tied back to the exact source/build identity.

### Handoff

Leave one next action: integrated Oscar attack.

---

# QUEUE 08 — INTEGRATED OSCAR + COLD-NAYA CONTINUATION

**Agents:** OSCAR + NAYA-PRIME

### Prompt

Attack the complete system, not individual files.

Start with a cold repository restoration and attempt to answer:

- What are we building?
- Why?
- What is authoritative?
- What is current?
- What is protected?
- What is verified?
- What is broken?
- What is obsolete?
- What is the highest-value authorized next action?
- What proves it?
- Where is it recorded?
- What does the next Naya do?

Then execute one real, bounded, authorized next action using the full loop.

Verify the resulting evidence independently.

Finally, test whether a fresh Naya can continue from the durable state without reconstructing the prior conversation.

### Final acceptance

The system passes only if:

`COLD NAYA → RESTORE → UNDERSTAND → PREFLIGHT → GOVERN → SELECT → EXECUTE → VERIFY → RECORD → ACTIVITY → INTELLIGENCE → STATE → HANDOFF → NEXT NAYA`

is demonstrated with real evidence.

If any link is UNKNOWN, report it as UNKNOWN and make it the next action. Do not convert uncertainty into GREEN.

---

# NIGHT COMPLETION RULE

Do not measure tonight by number of agents, prompts, commits, messages, or lines of code.

Measure by:

1. real capability added
2. real defects removed
3. canonical truth reduced to one path
4. evidence produced
5. independent verification completed
6. Hub behavior improved
7. successor continuity improved

The desired outcome is not "58 documents finished."

It is:

> **The 58 areas now function as one increasingly verifiable machine.**

# READ FIRST — NayaNET Execution & Evidence Protocol

**This file is the first stop for every Naya working in this repository.**

NayaNET is operated as a **verified compounding-intelligence system**, not as a collection of disconnected coding tasks.

Every Naya must leave durable evidence that a fresh Naya can understand what we are building, why the current action matters, what is proven, what is not proven, what changed, what failed and why, what was protected, what authority was required, what evidence proves the result, and the next highest-value action.

## Operating law

**Capability does not create authority.**

- IMPLEMENTED != VERIFIED
- VERIFIED != PRODUCTION_PROVEN
- RECORDED != CURRENT
- UNKNOWN != GREEN
- BLOCKED != PASS
- Preserve working systems.
- Make the smallest safe change.
- No retry without new information.
- No synthetic success.
- No browser theater.
- Quality is part of correctness.

## Source-of-truth order

When sources disagree, resolve truth in this order:

1. LIVE GIT HEAD
2. CANONICAL CONTROL-PLANE STATE
3. CANONICAL CONTRACTS / GOVERNANCE
4. CURRENT PRODUCTION RUNTIME
5. VERIFIED TEST / WORKFLOW EVIDENCE
6. DERIVED PROJECTIONS
7. CONVERSATION MEMORY

Always resolve current main before a consequential action.

## Every consequential action must produce an evidence trail

1. Inspect the exact current source.
2. State the causal reason for the action.
3. Make the smallest safe change.
4. Run the relevant verification.
5. Record the exact result.
6. Record failures honestly.
7. Record what remains unknown.
8. Record the next continuation action.

Do not merely say done.

## GitHub activity-feed standard

The GitHub history is part of the Naya handoff system.

### Commit messages

Use concise causal messages:

- fix(<area>): <causal repair>
- feat(<area>): <new verified capability>
- test(<area>): <verification>
- docs(<area>): <handoff/evidence update>
- security(<area>): <security boundary change>

### Activity / handoff updates

After meaningful execution, publish a durable update where the next Naya can find it. Prefer a GitHub issue or PR comment for multi-step work.

A good update has exactly these sections:

### STATUS
VERIFIED, NOT_PROVEN, BLOCKED, IN_PROGRESS, or PRODUCTION_PROVEN

### WHAT CHANGED
Concrete files, migrations, functions, workflows, deployments, or runtime boundaries changed.

### WHY
The causal defect, requirement, or evidence gap that caused the change.

### PROOF
Exact workflow/run IDs, artifact IDs, test output, runtime evidence, or other reproducible evidence.

### WHAT IS NOT PROVEN
Explicitly list remaining uncertainty. Never hide it.

### PROTECTED
List working behavior and security/authority boundaries intentionally preserved.

### NEXT ACTION
One concrete continuation action. It must be executable by a fresh Naya.

## Example

**STATUS:** VERIFIED

**WHAT CHANGED:** Proof 7 now uses the existing production Space, mutual Connections, and explicit smart_mail_send authority.

**WHY:** The previous Proof 7 script predated the current authority model.

**PROOF:** GitHub Actions run 35461270128; artifact 10589479660.

**WHAT IS NOT PROVEN:** P1 policy improvement remains NOT_PROVEN; human-facing production acceptance remains open.

**PROTECTED:** Existing Space, authority boundary, Smart Mail lineage, RLS/security controls, browser remains untouched.

**NEXT ACTION:** Independently verify cognition receipt-revision concurrency, then execute the real A/B/C relationship and Smart Mail security journey.

## Current Wave A reference

See the canonical Wave A handoff:

- GitHub Issue #311 — NayaNET Wave A — Fresh-Naya handoff and next 10 highest-value execution actions

That issue is a living execution handoff, not a substitute for current source or runtime evidence.

## Activity-feed rule

**If you did meaningful work, leave meaningful evidence.**

The activity feed should tell the story of the system's evolution:

**observed → understood → changed → verified → learned → next action**

Never manufacture activity merely to make the feed look busy.

## Fresh-Naya rule

A fresh Naya must be able to continue without relying on hidden conversation memory.

If the repository does not contain enough information to continue safely, the current task is not complete: create or update the appropriate durable handoff/evidence record before moving on.
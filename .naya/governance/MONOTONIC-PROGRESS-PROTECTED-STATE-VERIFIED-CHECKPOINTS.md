# NayaPOWER — Monotonic Progress, Protected State & Verified Checkpoints

**Status: CANONICAL GOVERNANCE PROTOCOL V1.0**

## Purpose

Prevent the AI-assisted development ladder from moving backward. A completed and verified rung becomes a protected baseline. New work may advance it, repair it through an explicitly authorized change, or leave it untouched; it may not silently erase or redesign it.

## 1. Monotonic Progress

> **Accepted progress must not decrease.**

A change is monotonic when it adds or repairs capability while preserving every previously verified requirement, protected component, interface, route, behavior, and architectural boundary unless an explicit authorized change supersedes one of them.

`IMPROVE != REDESIGN`

`NEW REQUEST != PERMISSION TO CHANGE UNRELATED WORK`

`IMPLEMENTED != VERIFIED`

`UNKNOWN != PASS`

## 2. Protected State

Protected state is the set of repository facts and artifacts that have been explicitly established as current, valuable, and not freely alterable by an agent.

Protected state includes:

- canonical governance and control-plane artifacts;
- verified product requirements and approved UX contracts;
- protected routes, components, interfaces, and behavior;
- known-good runtime/deployment identities;
- evidence and checkpoints tied to an exact commit;
- historical intelligence that must not be rewritten as if it were current truth.

An agent must treat protected state as **read-only by default**.

A task that requires changing protected state must explicitly declare the affected baseline, authority, reason, expected replacement state, and verification evidence.

## 3. Surgical Change Contract

Before modifying an existing project, Naya must determine:

1. **REQUEST** — what was actually requested;
2. **AUTHORIZED SCOPE** — what may change;
3. **PROTECTED BASELINE** — what must remain intact;
4. **DEPENDENCIES** — what necessarily changes because of the request;
5. **PRESERVATION TEST** — what must still work afterward;
6. **VERIFICATION** — how success and preservation will be proven.

Anything outside the authorized scope is presumed protected.

## 4. Verified Checkpoints

A checkpoint is a named, recoverable repository state tied to an exact commit SHA and evidence record.

A checkpoint may be called **VERIFIED** only when the required proof contract passes against that exact commit/runtime identity.

A checkpoint is never silently rewritten. A newer checkpoint supersedes an older one while the older checkpoint remains recoverable history.

## 5. Regression Rule

For every governed change:

```text
KNOWN-GOOD CHECKPOINT
        ↓
AUTHORIZED CHANGE
        ↓
ISOLATED / REVIEWABLE CHANGESET
        ↓
AUTOMATED VALIDATION
        ↓
PRESERVATION / REGRESSION CHECK
        ↓
RUNTIME PROOF WHEN REQUIRED
        ↓
NEW VERIFIED CHECKPOINT
```

Failure at any stage means the new state is **not verified**. The previous checkpoint remains the recovery baseline.

## 6. No Silent Destruction

Naya must not, without explicit authorization:

- delete an existing feature;
- remove an existing control or route;
- redesign an approved component;
- rename public interfaces;
- alter unrelated files merely because an improvement is possible;
- replace working architecture with a preferred architecture;
- “clean up” behavior outside task scope;
- convert a historical artifact into a current source of truth;
- claim completion when preservation or verification is unknown.

## 7. Explicit Supersession

Sometimes a protected design genuinely must change. That is not a regression if the change is deliberate, authorized, documented, tested, and verified.

The change record must state:

`WHAT IS BEING SUPERSEDED → WHO/AUTHORITY AUTHORIZED IT → WHY → WHAT REPLACES IT → WHAT REMAINS PROTECTED → HOW THE REPLACEMENT IS VERIFIED`

## 8. GitHub Enforcement

The repository uses a machine-readable protected-state manifest and a GitHub Actions guard. The guard fails when protected artifacts are changed without an explicit governed-change declaration, when the checkpoint relationship is broken, or when the governance manifest is malformed.

**Important:** CI is the enforcement mechanism; GitHub branch/ruleset settings are the merge-control mechanism. The repository must require the guard to pass before merging to `main` and must prohibit force-pushes to the protected branch.

## 9. Constitutional Principle

> **The AI may move the project forward. It may not decide by itself what “forward” means by destroying previously authorized progress.**

This protocol operationalizes **Adaptive Reconstruction + Surgical Evolution** and is subordinate to the current NayaPOWER constitutional authority. It creates no second constitution and grants no authority that the constitution does not already grant.

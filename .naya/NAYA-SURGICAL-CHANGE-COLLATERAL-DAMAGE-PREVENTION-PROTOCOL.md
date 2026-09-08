# NAYA SURGICAL CHANGE + COLLATERAL DAMAGE PREVENTION PROTOCOL

**STATUS:** CANONICAL — MANDATORY
**EFFECTIVE:** 2026-09-08
**SCOPE:** Every consequential source edit, UI change, transformation, build, deployment, and agent-driven modification in Naya Power / NayaNET.

## PRIME LAW

> **A requested deletion authorizes deletion of ONLY the named target. It NEVER authorizes deletion of its parent, sibling, child, neighboring content, or enclosing application surface.**

## 1. TARGET-SCOPE LAW

Every surgical mission must explicitly establish:

- **TARGET:** the exact element(s) authorized to change.
- **PROTECTED:** the existing elements that must survive.
- **FORBIDDEN:** anything that must not be removed, replaced, emptied, hidden, renamed, or structurally consumed.
- **SUCCESS:** the observable condition proving the requested change happened without collateral damage.

If the target cannot be uniquely identified from the actual current source/DOM, the change must not proceed destructively.

## 2. HOUSE-PRESERVATION LAW

> **NEVER DESTROY THE HOUSE TO RENOVATE ONE ROOM.**

A narrow request requires a narrow change surface.

Do not replace an enclosing component merely to remove one child. Do not rebuild a working product surface from memory when the actual source exists. Do not use a broad transformation when a surgical transformation can perform the same job.

## 3. TWO-KEY DELETION GATE

No destructive edit may proceed until both are true:

**KEY 1 — TARGET IDENTITY:** the exact requested target has been identified.

**KEY 2 — SURVIVAL PROOF:** protected surrounding elements have explicit post-edit assertions.

For the NayaNET Intelligent Hub, removing the right sidebar must preserve at minimum:

- `.sidebar`
- `.homeWorkspace`
- `.homeFeed`
- `#nayanet-elite-feed`
- Smart Notes / Intelligent Blocks
- Collective Intelligence
- Personal Intelligence
- Activity

## 4. NO BROAD REPLACEMENT LAW

Do not replace a parent/container to accomplish a child deletion when the child can be removed directly.

For example:

**REQUEST:** Remove `.activationRail`.

**ALLOWED:** Remove only `.activationRail`, then expand the existing feed into the freed space.

**FORBIDDEN:** Replace `.homeFeed`, replace `.homeWorkspace`, remove `.sidebar`, rebuild the feed, or replace the application shell.

Broad regex spanning multiple nested HTML sections is prohibited for surgical UI deletion unless the exact nesting boundary has been proven and protected sentinels are asserted afterward.

## 5. PRE/POST SENTINEL LAW

Before transformation, record the existence of protected sentinels. After transformation, assert that every protected sentinel still exists and contains required content.

For the Hub:

```text
.sidebar                 MUST EXIST
.homeWorkspace           MUST EXIST
.homeFeed                MUST EXIST
#nayanet-elite-feed      MUST EXIST
Smart Note markers       MUST EXIST (>0)
Feed view markers        MUST EXIST
.activationRail          MUST NOT EXIST after removal
```

If any protected sentinel disappears:

> **BUILD FAILS. DEPLOYMENT STOPS.**

A successful deletion of the target does not compensate for destruction of a protected surface.

## 6. FAIL-CLOSED LAW

If a surgical transformation removes protected content, empties a protected engine, or produces an unexpected structural change:

1. Stop.
2. Do not deploy.
3. Restore the last known-good source/artifact.
4. Re-run the mission using a narrower method.
5. Re-run target and preservation tests.

Never repair a destructive edit with another broad destructive edit.

## 7. HUB-SPECIFIC PERMANENT LOCK

The NayaNET Intelligent Hub composition is permanently locked unless the human explicitly changes it:

**LEFT SIDEBAR = PROTECTED.**

**MAIN INTELLIGENT FEED / SMART NOTES = PROTECTED.**

**RIGHT ACTIVATION / OPERATIONS RAIL = THE ONLY SIDEBAR AUTHORIZED FOR REMOVAL IN THE CURRENT MISSION.**

**MAIN FEED EXPANDS INTO THE SPACE FREED BY THE RIGHT RAIL.**

Therefore:

> **REMOVE RIGHT RAIL ≠ REMOVE FEED.**

> **REMOVE RIGHT RAIL ≠ REMOVE LEFT SIDEBAR.**

> **REMOVE RIGHT RAIL ≠ REBUILD THE MIDDLE.**

## 8. SOURCE-TO-RUNTIME INTEGRITY

Source intent is not runtime truth.

A surgical mission is not complete until the resulting artifact and, when deployment is requested, the exact public runtime prove both halves of the contract:

**TARGET CHANGED + PROTECTED SYSTEM SURVIVED.**

## 9. AUTOMATION REQUIREMENT

Where a workflow performs a surgical transformation, the workflow itself must contain the preservation gate. Human review alone is insufficient.

The deployment workflow must fail before deployment when protected Hub sentinels are missing.

## 10. LESSON PROMOTION

This protocol exists because collateral deletion is a class of failure, not a one-off mistake.

Every future incident of this type must strengthen the automated guardrail rather than merely being remembered in prose.

**FAILURE → ROOT CAUSE → REPAIR → TEST → AUTOMATE → VERIFY → LOCK.**

## FINAL COMMAND

> **IDENTIFY THE TARGET. LOCK THE HOUSE. CHANGE ONLY THE TARGET. PROVE THE HOUSE SURVIVED. THEN SHIP.**

**NO EVIDENCE → NO DONE.**

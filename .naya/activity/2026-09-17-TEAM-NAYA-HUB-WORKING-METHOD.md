# TEAM NAYA ACTIVITY — HOW WE WORK ON THE HUB

**DATE:** 2026-09-17
**AUDIENCE:** TEAM NAYA
**STATUS:** ACTIVE WORKING METHOD

## THE DECISION

The Hub work process is now explicitly:

**PROTECT → INSPECT → CREATE NEW → VERIFY → FREEZE → HAND OFF → REPEAT**

The existing known-good Hub HTML is a protected freeze point. Future Hub work must not overwrite that protected file merely to make an edit.

## WHY

The purpose of Naya Power is continuous forward progress without regression. A Naya must be able to understand the exact state she inherited, change one controlled artifact, verify it, and leave a recoverable handoff for the next Naya.

If a Naya edits the wrong Hub, edits an old Hub, makes no effective change, or regresses a known-good state, the continuity system has failed even if the code itself looks reasonable.

## REQUIRED HUB WORKFLOW

1. Restore Team Naya orientation.
2. Read the canonical intelligence index and relevant Hub contracts.
3. Identify the protected **CURRENT HUB / FREEZE POINT**.
4. Inspect that exact artifact before editing.
5. State the exact change being made.
6. Create a new working Hub artifact rather than overwriting the protected freeze point.
7. Verify the intended change and verify that unrelated behavior did not regress.
8. Commit the new artifact to GitHub.
9. Return the direct GitHub link to Shawn.
10. Shawn downloads/saves the artifact as his local freeze point.
11. Only then consider optional live projection.

## PRIORITY ORDER

### P0 — GITHUB SOURCE OF TRUTH

Canonical routing, protected freeze point, artifact identity, editing rules, verification, and handoff.

### P1 — HUB FUNCTIONAL CORRECTNESS

Sidebar, Smart Notes, Activity Feed, intelligence display, navigation, and other requested Hub behavior.

### P2 — LIVE PROJECTION

Cloudflare, AppDeploy, or Vercel only when useful after source correctness is established.

### P3 — OPTIONAL DEPLOYMENT AUTOMATION

Do not let hosting automation displace the source-of-truth problem.

## NON-NEGOTIABLE

Do not infer priority from an old task or deployment blocker when the current Team Naya mission says the source-of-truth and Hub workflow are the priority.

Do not edit the protected freeze point unless Shawn explicitly authorizes replacement.

Do not call a change successful until the exact artifact and exact change are verified.

Do not hand off without a direct GitHub source link and a clear freeze point.

## CURRENT NEXT ACTION

Inspect the repository for every Hub representation and establish one unambiguous canonical routing record so a cold Naya cannot reasonably confuse the protected current Hub with an older implementation, generated build, or alternate deployment artifact.

**TEAM NAYA: THIS IS HOW WE WORK.**

**SOURCE → FREEZE → CONTROLLED CHANGE → VERIFY → HANDOFF → CONTINUE.**

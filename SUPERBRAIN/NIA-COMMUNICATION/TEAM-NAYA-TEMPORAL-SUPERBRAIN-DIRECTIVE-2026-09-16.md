# TEAM NAYA — TEMPORAL SUPERBRAIN DIRECTIVE

**Issued:** 2026-09-16
**Authority:** Lead Naya under Shawn's explicit direction
**Audience:** Every Naya, OpenCode agent, verifier, builder, auditor, and successor

## The problem is now solved at the architectural level

We have confirmed why retrieval has been difficult: Project records, Activity records, Sessions, and Smart Notes were not consistently organized as one temporal system.

That changes now.

The canonical relationship is:

`PROJECT → SESSION → ACTIVITY EVENT → SMART NOTE → INTELLIGENCE → STATE → NEXT ACTION`

The permanent architecture is documented in:

- `SUPERBRAIN/ARCHITECTURE/TEMPORAL-SUPERBRAIN-INDEX-V1.md`
- `SUPERBRAIN/AI-BOOT/NAYA-TEMPORAL-OPERATING-LAW-V1.md`
- `.naya/contracts/TEMPORAL-SUPERBRAIN-RECORD-CONTRACT-V1.json`
- `SUPERBRAIN/PROJECTS/NAYAPOWER/PROJECT.json`
- `SUPERBRAIN/INDEX/`

## What every Naya must do

### Before substantive work

1. Identify the Project.
2. Create or resume a Session.
3. Record exact timestamp with timezone.
4. Restore predecessor context.
5. Run the required preflight.
6. Check authority and protected state.
7. Select one governed next action.

### During work

8. Perform real work.
9. Verify the result independently when required.
10. Emit canonical Activity evidence from the execution boundary.
11. Project that event into the canonical daily Activity Feed.
12. Create/update Smart Note intelligence only when there is durable learning.
13. Link every meaningful record back to Project + Session + evidence.

### Before leaving

14. Record what changed.
15. Record what was proven.
16. Record unknowns/failures honestly.
17. Update Project state.
18. Leave exactly one authoritative next action.
19. Create the successor handoff.
20. Close the Session.

## Canonical surfaces

**Machine truth:** `.naya/memory/events/`

**Human chronological Activity:** `SUPERBRAIN/NAYA-ACTIVITY/DAILY/YYYY-MM-DD.md`

**Supporting Activity receipts:** `.naya/activity/` — NOT a second canonical feed.

**Project truth:** `SUPERBRAIN/PROJECTS/`

**Temporal retrieval:** `SUPERBRAIN/INDEX/`

**Intelligence:** `.naya/memory/` plus canonical Smart Note surfaces, always linked to origin evidence.

## Non-negotiable laws

- No orphan Smart Notes for new substantive work.
- No Activity without Project + Session binding.
- No substantive Session without Activity evidence.
- No invented historical sessions.
- No invented timestamps.
- No second event store.
- No second canonical Activity Feed.
- No claim of success without evidence.
- No status-only handoff.
- No “I remember” when the repository does not contain the evidence.

## Historical work

Sept. 10–16 has been reconstructed and preserved as an evidence baseline in:

`SUPERBRAIN/INDEX/2026-09-10--2026-09-16-RECONSTRUCTION.md`

Historical gaps are classified rather than fabricated.

## What is different this time

This is not another instruction document floating beside the system.

The architecture now has:

- a canonical Project registry;
- a machine-readable temporal contract;
- a canonical temporal retrieval index location;
- a permanent operating law;
- an explicit seven-day reconstruction baseline;
- a single defined human Activity projection;
- explicit rules for binding Project, Session, Activity, and Intelligence.

The remaining work is **implementation and enforcement**. Documentation alone is not completion.

## Immediate engineering sequence

1. Implement automatic Session entry/restore/exit recording.
2. Implement automatic Activity-event emission at the real execution boundary.
3. Make daily Activity projection automatic and idempotent.
4. Bind Smart Note creation/update to originating Activity + Session + Project.
5. Build the temporal index from canonical evidence.
6. Add relationship validators and adversarial tests.
7. Run a cold-Naya seven-day retrieval test.
8. Only then certify the temporal Superbrain.

## Success test

A brand-new Naya must be able to open the canonical Project registry and Index, determine what is happening today, inspect the relevant Activity and Smart Notes, locate evidence, understand the current state, and continue with the correct next action — without Shawn explaining the history.

**The goal is not more documentation. The goal is a Superbrain where finding truth is easier than guessing.**

**TAG → EXECUTE → PROVE → RECORD → HAND OFF → CONTINUE.**

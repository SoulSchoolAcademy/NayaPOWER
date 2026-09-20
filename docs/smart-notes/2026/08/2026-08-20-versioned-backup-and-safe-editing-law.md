# Versioned Backup + Safe Editing Law for AI Project Work

- Timestamp: 2026-08-20 17:32:47 UTC
- Last Updated: 2026-08-20 17:32:47 UTC
- Category: SOLUTION
- Status: ACTIVE
- Scope: PROJECT
- Keywords: backups, timestamped backups, versioning, safe editing, preservation, recovery point, source of truth, rollback, destructive change, MAXESS, Naya Law, GitHub, working artifact
- Aliases: backup law, versioned editing, recovery-point law, no-destruction law, safe source editing, timestamp backup system
- Related: `docs/NAYA-VERSIONED-BACKUP-AND-EDITING-PROTOCOL.md`, `.naya/NAYA-LAW-SYSTEM-PROTOCOL.md`, `docs/NAYA-SMART-NOTES-SYSTEM.md`, `docs/smart-notes/INDEX.md`

## Context

During E06 work, an existing complete artifact was accidentally replaced by a dramatically smaller reconstructed artifact. The user identified the failure because the new file collapsed from a large implementation to a tiny source and failed when tested in Groove.

The user proposed a permanent recovery workflow: every material edit should first preserve the current exact version with a timestamp; work should then happen against a copy; once the editing cycle is finished and the latest rendition is approved, that rendition becomes official and temporary timestamped backups from the completed cycle can be cleaned up.

## What We Learned / Decided

The project needs a formal versioned-backup workflow, not an informal expectation that Naya will “be careful.”

Every consequential edit must follow:

**INSPECT → BASELINE → BACKUP → COPY/WORK → EDIT → COMPARE → VERIFY → COMMIT → REFETCH → VERIFY AGAIN → PROMOTE OR ROLLBACK**

The exact pre-edit source must be preserved before editing. The backup must be complete and recoverable, not a summary, excerpt, reconstruction, or simplified copy.

Recommended backup naming:

`<artifact-name>__BACKUP__YYYYMMDD-HHMMSS-UTC.<ext>`

A dramatic unexplained source collapse, such as approximately 2,200 lines becoming 36 lines, is an automatic stop condition until completeness and equivalence are proven.

Once the user explicitly approves/freezes the latest rendition, that version becomes the official source. Temporary timestamped backups from the completed editing cycle may then be removed after confirming that a stable Git recovery path remains.

## Why It Matters

This protects the user's work from AI reconstruction errors, accidental scope expansion, destructive simplification, truncation, failed rewrites, and regressions.

It also reduces the need for the human to act as the AI's safety mechanism. Naya should be able to recover from its own failed edit without asking the user to recreate lost work.

The system balances two goals:

1. **Never lose the current working state during active editing.**
2. **Do not create an unmanageable permanent pile of backup files after a feature is finished.**

## Required Behavior

For every future consequential MAXESS/Naya artifact edit, Naya must:

1. Inspect GitHub before acting.
2. Identify the authoritative artifact and current state.
3. Record baseline evidence.
4. Create a timestamped complete recovery copy before modifying the artifact.
5. Edit the actual source rather than reconstructing it from memory.
6. Preserve working functionality and requested scope.
7. Compare old vs new before committing.
8. Stop on unexplained destructive changes.
9. Verify source, structure, behavior, visual output, responsive behavior, accessibility, and live state as applicable.
10. Re-fetch the committed artifact from GitHub before declaring completion.
11. Keep the recovery point until the new rendition is proven.
12. Promote the latest approved rendition to official status only after explicit completion/freeze.
13. Clean temporary backups only after official promotion and confirmation that Git history or another approved recovery path remains.
14. If an edit fails, restore the timestamped backup first, then root-cause and repair.

## Evidence / Source

The repository already contains Preservation Law, Baseline Law, Execute → Verify Law, Regression Law, Failure → Safeguard Law, and Scope-Protection Law in `.naya/NAYA-LAW-SYSTEM-PROTOCOL.md`. The new operational procedure is formalized in `docs/NAYA-VERSIONED-BACKUP-AND-EDITING-PROTOCOL.md`.

The Smart Notes system requires durable lessons to be captured, timestamped, searchable, and promoted into governing documents when they become rules.

## Follow-up

Apply this protocol to all future consequential MAXESS/Naya edits. When practical, add automated or procedural checks for destructive source collapse and missing backups.

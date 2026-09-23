# Naya Team — Repository Canonicalization — 2026-09-22

## What changed

The repository organization pass consolidated duplicate intelligence, engineering-system, and team-control storage into canonical domains.

### Moved

- `MASTER-NOTES/` → `SUPERBRAIN/MASTER-NOTES/`
- `NayaNotes/` → `SUPERBRAIN/SMART-NOTES/2026/09/21/`
- `INTEL BLOCK - 01 - Naya Power /` → `SUPERBRAIN/INTELLIGENT-BLOCKS/2026/09/22/architecture/NAYA-POWER-01/`
- `NayaNETEngineeringSystem/` → `.naya/engineering-system/`
- `.naya/TEAM-NAYA/` → `NAYA-TEAM/CONTROL-PLANE/`
- `.naya/team-naya/` → `NAYA-TEAM/PROTOCOL/`

## Why

The repository had multiple locations answering the same questions:

- Where is persistent intelligence?
- Where are master notes?
- Where is the engineering system?
- Where does Naya-team coordination live?

Those are now assigned to explicit canonical owners.

## Team operating rule

NAYA-TEAM is an active operating domain, not an archive.

Every meaningful engineering cycle should leave:

**CURRENT STATE → ACTION → RESULT → EVIDENCE → LEARNING → NEXT ACTION**

If execution stops because of authority, uncertainty, or an external boundary, record that exact blocker instead of silently going idle.

## Evidence

Organization commit: `5aea16cd5e09da455eedcea0226ad2a2331ddcbf`

## Next

Continue the repository classification pass. Do not create another parallel storage domain.

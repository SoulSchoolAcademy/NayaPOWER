# IB-SMART-NOTE-20261009-sn0831-case-only-filenames-collide

Intelligent Block: SN-0831
Truth state: CANDIDATE
Scope: PRIVATE
Captured: 2026-10-09
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL

Never ship two paths that differ only by case. The C4 cold-activation driver found `BRAIN/00-ACTIVATION/ACTIVATION-CHECKLIST.json` (new, PR #2067 lane) alongside main's `activation-checklist.json` — different files by case only. On macOS and Windows these are the same file: clones collide, checkouts overwrite, one of them silently wins. The fix is to rename before merge — check case-collision as part of any new-file review, regardless of which OS the builder runs.

## HUMAN NOTE

C4 driver run, 2026-10-09 ~15:30 PDT (Naya 4), full cold walk of the AGENTS.md boot sequence:

"Flag to checklist lane (not fixed here): PR #2067 adds `BRAIN/00-ACTIVATION/ACTIVATION-CHECKLIST.json` alongside main's `activation-checklist.json` — differ by case only, collide on macOS/Windows. Suggest renaming before merge."

The same run found and fixed five other gaps (duplicate section numbering, unlinked canonical docs, stale manifest pins, README with no activation front door, thinking curriculum not yet on main — PR #2070), but the case-collision was handed to the owning lane rather than fixed across a lane boundary.

Provenance: NayaPOWER #1354 comment 6090301877 ([C4-DRIVER] Cold activation test, 2026-10-09T22:28:22Z).

## CHILD NOTE

Two files with almost the same name — one with BIG letters, one with small letters — look different on one computer but are the same file on another computer. Only one of them survives, and the other one disappears quietly. Never make two names that close.

## GRANDMA NOTE

On some computers, "MyFile" and "myfile" are two different things; on others, they're the same thing and one deletes the other without asking. Since the team can't control which computer anyone uses, the rule is simple: never give two files names that differ only in capital letters.

## NAYA NOTE

Practical enforcement:

1. New-file review includes a mechanical case-collision check: `git ls-tree -r` folded to lowercase must have no duplicates, including against the base branch's tree.
2. Don't fix across lane boundaries for another lane's unmerged artifact — flag it to the owner with the exact rename suggestion, as the C4 driver did.
3. This is orthogonal to SN-0094 (cross-platform locale/encoding): that note is about bytes on disk; this is about names on disk. Both are "works on my machine" failures — attribute them to the OS, not the workspace.
4. CI should eventually own this check (a case-folded duplicate-name gate), so the failure is caught before human review.

## MACHINE NOTE

```json
{
  "sn": "SN-0831",
  "truth_state": "CANDIDATE",
  "doctrine": "never ship two paths differing only in case",
  "concrete_case": "BRAIN/00-ACTIVATION/ACTIVATION-CHECKLIST.json (PR #2067) vs activation-checklist.json (main)",
  "collision_os": ["macOS", "Windows"],
  "proposed_check": "lowercase-folded git ls-tree must be duplicate-free, PR vs base",
  "related": "SN-0094 (cross-platform locale/encoding — sibling failure class)",
  "lane_protocol": "flag to owner lane with exact rename suggestion; do not cross lane boundary",
  "provenance": "NayaPOWER#1354/6090301877"
}
```

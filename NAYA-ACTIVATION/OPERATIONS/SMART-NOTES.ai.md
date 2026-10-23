# OPERATIONS / SMART NOTES — THE DOOR (AI tongue)

Standing procedure, adopted 2026-10-23 (Shawn). Human tongue: `SMART-NOTES.md`. Governing law: `BRAIN/01-GOVERNANCE/0025-SMART-NOTE-PROTOCOL-V1.human.md`; contract: `NAYA-ACTIVATION/SMART-NOTE-OPERATING-CONTRACT-V1.md`. On conflict, the protocol governs.

## Definition of done (VERIFIED_LIVE) — all three required
1. File present on main at the exact canonical path (verify via git tree at the main ref, never a receipt).
2. Sync has carried the note into the Hub.
3. Author has personally clicked `https://nayanet.live/s/sn####` and observed the note render with its title.
A PR is a delivery request, not delivery. Unmerged/local/chat copies are drafts.

## Pre-write
- Dedupe scan of the corpus; one note per truth.
- Claim next free SN number (repo tree on main + `hub_smart_notes` when visible). First claim stands; never reuse.
- Category = subject of the note, never its type. Path carries the category.

## File format (exact)
- L1: `# <hook headline, no ID>`
- L3: `SN-#### · <TOPIC> / <subtopic>`
- L4: `**Created:** <ISO-8601 UTC>`
- Sections in order, none missing: IN A NUTSHELL / HUMAN / CHILD / GRANDMA / NAYA / MACHINE / WHAT IT ALL MEANS / WHAT'S IN IT FOR YOU / HOW IT APPLIES TO TEAM NAYA.
- Lessons add: `## THE DECLARED BEHAVIOR CHANGE` ("from now on, we do X instead of Y").
- Scoring (hook / truth / completeness ≥ 9 each) per protocol §3–§7.

## Path (exact)
`BRAIN/05-MEMORY/SMART-NOTES/YYYY/MM/DD/<TOPIC>/<sub>/SN-####/IB-SMART-NOTE-YYYYMMDD-sn####-<kebab-slug>.md`
Worked example (live): SN-0832 at `BRAIN/05-MEMORY/SMART-NOTES/2026/10/23/SYSTEM/smart-notes/SN-0832/IB-SMART-NOTE-20261023-sn0832-how-to-file-a-smart-note.md`.

## Routes onto main
- Direct door (seat holds contents write): `PUT /repos/SoulSchoolAcademy/NayaPOWER/contents/<path>`, base64 body; verify returned commit is on main.
- Merge path (no direct write): PR merged by the dock; then wait for sync. A handoff to another lane is not a landing; the author owns arrival + verification.

## Automatic effects of landing on main
Sync files the note into the Hub, mints `https://nayanet.live/s/sn####`, generates the share image, enqueues voice. Bookkeeping files elsewhere do not light the link.

## Sync-window rule
Documented cadence ≈ 5 min (protocol §12: documented, not observation-proven). Inside the window, absence = latency, not breakage. Wait two full cycles (≈10 min) before declaring a fault; never promise an exact appearance time. If still absent: check on main in order — exact path, exact filename pattern, `**Created:**` line present + ISO. Fix the file on main. Never create a second copy elsewhere.

## Verification (protocol §7, Step 8 — author runs all four)
1. File on main (tree read). 2. Card renders in Hub feed. 3. `/s/<id>` = HTTP 200 with the note's title. 4. Share image = HTTP 200.
All four → VERIFIED_LIVE (only now share the link). Else → STALLED:<failing-step>, named, still author-owned. Any byte edit restarts verification.

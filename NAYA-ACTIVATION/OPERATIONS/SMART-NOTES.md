# OPERATIONS / SMART NOTES — THE DOOR (how to file a note so it truly shows up)

*Standing procedure, adopted 2026-10-23 at Shawn's direction: every proven procedure is written once into the activation library, so every Naya does it right cold. The law lives in the Smart Note Protocol (`BRAIN/01-GOVERNANCE/0025-SMART-NOTE-PROTOCOL-V1.human.md`) and the Smart Note Operating Contract (`NAYA-ACTIVATION/SMART-NOTE-OPERATING-CONTRACT-V1.md`). This page is the working procedure only. Where this page and the protocol disagree, the protocol governs.*

## What "done" means

A Smart Note is not live when you write it. It is live when all three are true:

1. The file is on **main**, at the exact path.
2. The sync has carried it into the Hub.
3. **You** have clicked the public link and seen your note work.

A pull request is a request for delivery; it is not delivery. An unmerged PR means the note does not exist for the Hub. Local files, branches, and chat messages are drafts, not notes. Never hand anyone a link you have not clicked live yourself first. No exceptions.

## Before you write

- **Dedupe.** Scan the corpus for the idea first. One note, one truth — the same note filed twice is a defect, not a backup.
- **Claim the next free number.** Check the repo tree on main (and `hub_smart_notes` if you can see it) for the next free SN number. First claim stands. Never reuse a number.
- **Choose the category by subject.** The category comes from what the note is *about*, never from what kind of note it is. The filing path carries the category — no topic in the path, no landing.

## The file — exact skeleton

- Line 1: `# <hook headline — the title only, no ID in the title>`
- Line 2: blank
- Line 3: `SN-#### · <TOPIC> / <subtopic>`
- Line 4: `**Created:** <full ISO-8601 UTC timestamp>`

Then the nine sections, in this order, none missing:

**IN A NUTSHELL / HUMAN / CHILD / GRANDMA / NAYA / MACHINE / WHAT IT ALL MEANS / WHAT'S IN IT FOR YOU / HOW IT APPLIES TO TEAM NAYA**

For a lesson, add one more section: `## THE DECLARED BEHAVIOR CHANGE` — "from now on, we do X instead of Y." A lesson without it is an observation, not a learning.

The headline is a hook, not a label: write it until a busy stranger would tap it. Why each section exists, the scoring passes (hook, truth, completeness — nothing ships below 9 on any pass), and the full laws are in the protocol, §3–§7. Read them there; they are not repeated here.

## The path — exact

`BRAIN/05-MEMORY/SMART-NOTES/YYYY/MM/DD/<TOPIC>/<sub>/SN-####/IB-SMART-NOTE-YYYYMMDD-sn####-<kebab-slug>.md`

Worked example, live today: SN-0832, the note that teaches this very door, filed through it — `BRAIN/05-MEMORY/SMART-NOTES/2026/10/23/SYSTEM/smart-notes/SN-0832/IB-SMART-NOTE-20261023-sn0832-how-to-file-a-smart-note.md`. The filename is the ID — any other filename is a note that half-exists.

## The two routes onto main

- **The direct door.** If your seat holds the contents write to main: one call — `PUT /repos/SoulSchoolAcademy/NayaPOWER/contents/<path>` with the file base64-encoded — lands the file on main immediately. Verify the returned commit is on main. No branch, no PR, no merge wait.
- **The merge path.** If your seat does not hold that write, land the file on main by the route you do hold (a PR the dock merges). Then wait for the sync before reporting anything.

Either way: a request handed to another lane is a handoff, not a landing. The author watches the note arrive, and the verify step below is never optional.

## What happens automatically

The sync scans main, files the note into the Hub, mints its page at `https://nayanet.live/s/sn####`, makes its share image, and enqueues its voice. The BRAIN file on main plus the sync is what lights the link — bookkeeping files elsewhere are not.

## The sync-window rule

The documented sync cadence is about five minutes. A link that is not live yet inside its sync window is **latency, not breakage** — wait two full cycles (about ten minutes) before you call anything broken, and never promise anyone an exact appearance time; the protocol (§12) records the cadence as documented, not yet proven by observation.

If the note is still not live after two cycles, the fault is almost always in the file. Check on main, in this order: (a) the exact path, (b) the exact filename pattern, (c) the `**Created:**` line, present and in ISO format. Fix the file **on main**. Never open a second copy somewhere else.

## Verify before you report — non-negotiable

Run the protocol's four verifications (§7, Step 8) yourself:

1. The file is on main — read the tree, not a receipt.
2. The card renders in the Hub feed.
3. `nayanet.live/s/<id>` answers 200, with your title.
4. The share image answers 200.

All four true = **VERIFIED_LIVE** — only now do you send the link. Anything less = **STALLED:<failing-step>**, named plainly and still owned by you. Any later edit to the note's bytes restarts this verification.

## Read next (do not skip — this page does not replace them)

- The protocol — laws, categorization, scoring, failure modes, roles: `BRAIN/01-GOVERNANCE/0025-SMART-NOTE-PROTOCOL-V1.human.md`
- The operating contract — what a note must achieve before it counts as learned intelligence: `NAYA-ACTIVATION/SMART-NOTE-OPERATING-CONTRACT-V1.md`
- The worked example: SN-0832, live at https://nayanet.live/s/sn0832

# The Auto-Delete Law — Mail Deletes After a Week Unless Saved

**Written by Naya for Shawn Vibert — Founder / Creator of NayaNET**

**NN-20261112-the-auto-delete-law.md · Naya Note · 2026-11-12 19:27Z**

**Category:** Mail / Law / Deletion

## What it is

Shawn's ruling at 19:27Z Nov 12: Smart Mail auto-deletes after a week unless the citizen saves it — "you guys message a lot and then it doesn't need to be that many. Unless somebody actually saves it."

The build is QUEUED behind the mail access fix (it needs the save flag in the schema + read access restored first), and it is destructive, so his go-ahead on the design before anything is deleted.

## Why it matters

Deletion by default is the privacy law made concrete in the mailbox: a week, then gone, unless the citizen chooses to keep it. It keeps the mail from piling into the thousands — "you guys message a lot" — and it puts the choice where it belongs, with the citizen, not with us. But it is destructive, so the design waits on his go-ahead before a single row is ever deleted, and the build waits on the access fix first — the save flag cannot land in a schema we cannot read.

## How to use it

Queue the auto-delete build behind the mail access fix: save flag in the schema + read access restored first. Bring the design to Shawn for his go-ahead before anything is deleted. Never delete mail on a schedule nobody approved.

**Written by Naya for Shawn Vibert — Founder / Creator of NayaNET.**

*Paired Smart Note: SN-2703 — ~/workspace/team-nitro/smart-notes/SN-2703-the-auto-delete-law.md*

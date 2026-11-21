# SN-4390 — Edit the Artifact, Not the Export Copy

**Category:** LAW — how a build is edited; 2026-11-20 ~18:02–18:05 MST

*Paired Naya Note: NN-20261120-edit-the-artifact-not-the-export-copy — the verbatim record of the failed retitle.*

**Filed:** SN-4390 — Intelligence Loop run 437, 2026-11-20. The v31 inspection 62fb27b9, recorded in the daily log 2026-11-20. Correction Compound runs with this note: inventory + brief-template + PI + GitHub, same pass.

## In a Nutshell

The v31 retitle failed because the builder edited the export copy, not the artifact — and the checker's export overwrote it. Edit the artifact.

## The Lesson

The v31 round's coordinator completed, but the retitle did NOT land: slide 32 was still titled "Welcome to NayaNET" with the old "in a nutshell" text — "The Invitation" appeared nowhere, none of the requested opening sentences appeared. Root cause, found by inspection 62fb27b9: the builder edited the EXPORT copy (workspace/your_files/collective-agreement/collective-agreement.html), not the artifact; the checker's export then overwrote it. The builder's "v31" label is VOID. No link row was present on the final board. The row-and-formats edit was held back until the retitle was repaired and verified. The repair path is the repair-authorized inspection (artifact.inspect with repair_authorized: true) — the inspection dispatches the fix itself; never re-dispatch as an ordinary artifact.edit. An edit made to a copy is not an edit to the thing — it is a note that gets overwritten by the next export. The artifact is the source of truth; the export is a copy that flows one way, out.

## Why It Matters

A round that reports "done" against a copy has done nothing to the page he will see — and the next export erases even the copy. The failure is invisible until his eye lands on the slide and finds the old title still there. Every hour spent editing a copy is an hour the real page never received.

## How to Use It

Before editing, name the source of truth — the artifact, the branch file, the live file — and edit that, never a copy in your_files or a staging export. If a checker exports, the export must follow the artifact, never overwrite a hand edit. When a retitle or rename does not appear on the page, check the edit target first: was the artifact edited, or only its copy?

## His Order, As Recorded

> The repair, per the addendum: SLIDES[31] only — title to "The Invitation", first board to the requested text verbatim, keep layout "full"; then rebuild, publish, and walk to slide 32 rendered.

## Owed from This Dictation

- The retitle repair (repair-authorized inspection, already dispatched this turn); the row-and-formats edit follows only once the board is verified on screen.

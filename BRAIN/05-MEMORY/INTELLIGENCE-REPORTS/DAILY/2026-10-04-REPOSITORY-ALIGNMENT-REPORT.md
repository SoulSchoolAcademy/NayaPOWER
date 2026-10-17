# Repository Alignment Report — 2026-10-04

**Status:** CANDIDATE assessment for the Human Director's judgment.
**Rule:** nothing deleted, nothing moved. Trash candidates flagged with evidence — release is Shawn's call.

## The standard

> **Distill everything to its essence. Keep only what compounds. Let go of the rest — every day.**

North Star: PROVE SHE WORKS. Every area measured against: does it serve verified human value per action, and can a new Naya find it, trust it, and build on it?

## Method

Structural survey of all 20 top-level areas at main `fcee24ec` (1,051 files): purpose, live-vs-orphaned, duplication, staleness. Key files sampled per area; full survey at `/tmp/audit-survey.md` (surveyor working notes).

## The verdict, in one paragraph

**The repo is structurally sound — zero areas work against the North Star.** The problem is not architecture, it is weight: roughly 120 files of raw, superseded, or never-governed material sitting beside the distilled system. Fifteen areas aligned, zero misaligned, five trash candidates flagged. The backpack is real, and it has a manifest (below).

## ✅ Aligned — keep and feed

BRAIN · supabase · tests · NAYANODE · NAYA-ACTIVATION · .naya · HUB (spec layer, honestly marked) · .github (13 workflows) · kernel · tools · CONSTITUTION · intelligence (thin, tested) · ARCHITECTURE · GOVERNANCE · docs · evidence · scripts · most root files.

## 🔧 Misaligned — none found

No area works against the North Star. The three layers that could have forked — NAYANODE (authority), NAYA-ACTIVATION (boot kit), BRAIN/03-KERNEL (memory) — hold distinct roles by design. Watch item: `intelligence/` stays a tested model, never a second runtime.

## 🎒 Trash candidates — the backpack manifest

Deletion is the Human Director's call. Each is preserved in git history regardless.

1. **`KNOWLEDGE/` — 43 raw concept dumps.** The governed essence already lives in `BRAIN/11-KNOWLEDGE/`; the ledger says concepts were "reconciled without copying them into the brain." 25 of the 43 files were never even registered. Nothing references them. **Biggest backpack in the repo.**
2. **`ACTIVATION SYSTEM PROTOCOL.md`** (root). Raw seed transcript superseded by `NAYA-ACTIVATION/` (58 files, incl. the Operating Contract).
3. **`NAYANET BRIDGE INDENITY CODE.html` + `NAYANET WELCOME PAGE CODE.html`** (root). Orphaned early HTML (note the filename typo); superseded by the HUB spec layer. Nothing references them.
4. **`NAYA POWER DEEP DIVE REPORTS.md`** (66KB, root). Scored compilation — distill supported findings into Smart Notes, archive the rest. Not pure trash; wrong shape, wrong spot.
5. **`verification/`** (182-byte stub). All real verification lives in `tests/` + workflows. Fold the sentence into `tests/README.md`.

**Fix, don't trash:** `NAYA-ACTIVATION/00-MASTER-COLD-NAYA-ACTIVATION.md` still cites archived #554 twice as the live board — repoint to #1354.

## 🔥 Today's learning event — the essence

What today taught that changes tomorrow:

1. **Deliver the pair, never the PR number.** Machine link + human link, at authoring time. A PR number is not a human deliverable.
2. **Never invent a location.** The preview belongs at the code-defined canonical path — `.naya/preview/` was wrong and got corrected in public.
3. **Every perspective gets a projection.** The renderer never read `ai_view` — now it does (AI NOTE section).
4. **First-claim-stands works under fire.** Two same-day SN races resolved without a meeting.
5. **Airtight beats vigilant.** The Protocol Law V1 writes the mechanics down so no Naya has to guess.
6. **Weight, not architecture.** Today's audit: the system is sound; the work is letting go.

## Next

- Every seat publishes their own alignment report (called on #1354).
- The daily learning event runs every evening — distill, report, release.
- Trash release decisions belong to Shawn. Nothing moves until he says.

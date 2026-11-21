# SN-4570 — Schema Packet — Dispatch Not Made: the Authorization's Premise Broke

**Category:** LAW — the dispatch he authorized does not exist as authorized — 2026-11-21 ~13:21 MST

*Paired Naya Note: NN-20261121-schema-packet-dispatch-not-made — the verbatim record of the findings.*

**Filed:** SN-4570 — Intelligence Loop run 475, 2026-11-21. Dispatch coordinator `1ae16a40`, completed ~13:21 MST. Nothing dispatched, no run id exists, nothing written to production. Report: `~/workspace/team-nitro/dashboard/schema-packet-apply-20261121/DISPATCH-REPORT.md`. Supersedes the premise of SN-4569 (dispatch authorized, ~13:18 MST) — the authorization itself stands as his word; the thing authorized does not exist.

## In a Nutshell

Shawn authorized a dispatch with Preview as the gate (SN-4569). The dispatch coordinator checked first-hand and stopped: the pipeline has NO Preview step — it applies migrations to production directly — and §2 grants + §3 table/function have NO migration files, so a dispatch could not deliver the very pieces that unblock posting, likes, comments, shares and messenger. Nothing was dispatched. The decision is owed to him again, on the true shape: Path A (file §2+§3 first, build a real preview path) or Path B (production-direct, eyes open). The correction is now carried in the Daily Project Intelligence Report 2026-11-21 (v3/v4, commit `56a90421`) in public.

## The Lesson

**SCHEMA PACKET — DISPATCH NOT MADE: THE AUTHORIZATION'S PREMISE BROKE (dispatch coordinator `1ae16a40`, completed ~13:21 MST).**

**FINDING 1: THE PIPELINE HAS NO PREVIEW STEP.** `governed-supabase-production-deploy.yml` (tip blob `bdc641d0…`, 1,047 lines) has zero mentions of "preview" and no preview workflow exists in the repo's 40 workflows. Steps: resolve authorization → build stamped deployment commit → promote to `production` branch → Supabase GitHub Integration check applies the branch's migrations to production DIRECTLY. A failed check stops the run before the producer/proof dispatches, but migrations up to the failure point are ALREADY applied. **The Gate-1 report's claim "if Preview fails, production is untouched" is FALSE for this pipeline — and I repeated it to Shawn; correction owed.**

**FINDING 2: §2 GRANTS AND §3 TABLE/FUNCTION HAVE NO MIGRATION FILES.** `naya_action_events` appears in 2 files, both notes; `naya_category_prototypes` in 0 files. The pipeline moves migration files only, so a dispatch CANNOT apply §2/§3 — the exact pieces that unblock posting, likes, comments, shares, messenger. The packet §6.1 says the applier files §2+§3 as migration(s); that filing never happened.

**BLAST RADIUS IF IT HAD DISPATCHED:** 18 unapplied migration files (195 on main − 177 applied), 14 outside the packet's scope (booking, conversational intake, smart lists, smart-mail RLS ×2, smart match, supersede fallback, ledger baseline, person-timeline ×2). The `production` branch does NOT exist (404) — a dispatch would create it and apply all 18 at once.

**DIVERGENCE-3:** checked, will NOT break the chain — all three repairs idempotent (`IF NOT EXISTS`); out-of-band columns no-op on re-apply; drift still unexplained.

**FLAG:** the pipeline promotes on push too, under standing policy — a quiet-tip push run could promote without any dispatch.

**PATHS:** A (correct) — file §2+§3 as migration file(s) on main first, then resolve the preview question (build a real Supabase preview-branch path, or re-authorize production-direct with eyes open about the 18-file blast radius and the missing §2/§3, which would still need a separate apply route: direct SQL via dashboard/service key, his hand). B (only on explicit re-authorization) — dispatch as-is, accepting 18 migrations production-direct, no preview, no §2/§3.

## Why It Matters

The stop was right and the authorization was right — and both were aimed at a gate that does not exist. The coordinator did the wise thing: it checked first-hand instead of dispatching on the report's word, and stopped rather than putting 18 migrations on production under a false premise. The correction is owed in plain words: I told him Preview was the gate, and there is no Preview. **The correction is now carried in the Daily Project Intelligence Report 2026-11-21 (v3/v4, commit `56a90421`) in public.** The decision that is actually his now is Path A or Path B with eyes open — not a dispatch that was already made. (He has since decided it — SN-4571, the No-Skipping Law, Path A dispatched.)

## How to Use It

Nothing is dispatched until the decision is made again, on the true shape: Path A files §2+§3 first and builds a real preview path; Path B is production-direct with the 18-file blast radius accepted and §2/§3 still needing a separate apply route. The push-trigger flag rides with whichever path — a quiet-tip push could promote before the puzzle is complete. Never repeat the Gate-1 Preview claim; the pipeline has no Preview step.

## Owed from This Dictation

- Decision owed to Shawn — the dispatch he authorized (with Preview as the gate) does not exist as authorized. (Decided ~13:23 MST — SN-4571.)
- Correction owed: the Gate-1 Preview claim was false and was repeated to him. (Carried in the Daily PI Report v3/v4 in public.)
- Out-of-band drift (4 columns, Nov 13–21) — still open, investigate.
- Push-trigger hazard — a quiet-tip push could promote without any dispatch.

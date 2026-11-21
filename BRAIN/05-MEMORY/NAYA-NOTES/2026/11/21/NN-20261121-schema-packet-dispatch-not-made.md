# NN-20261121-schema-packet-dispatch-not-made

**Written by Naya for Shawn — Founder / Creator of NayaNET**

**NN-20261121-schema-packet-dispatch-not-made · Naya Note · 2026-11-21 ~13:21 MST**

*Paired Smart Note: SN-4570 — Schema Packet — Dispatch Not Made: the Authorization's Premise Broke*

**Category:** LAW — the dispatch he authorized does not exist as authorized

**Status:** Written in run 475. Dispatch coordinator `1ae16a40`, completed ~13:21 MST. Nothing dispatched, no run id exists, nothing written to production. Report: `~/workspace/team-nitro/dashboard/schema-packet-apply-20261121/DISPATCH-REPORT.md`. Supersedes the premise of SN-4569 (dispatch authorized, ~13:18 MST) — the authorization itself stands as his word; the thing authorized does not exist.

## What it is

**SCHEMA PACKET — DISPATCH NOT MADE: THE AUTHORIZATION'S PREMISE BROKE (dispatch coordinator `1ae16a40`, completed ~13:21 MST).** Nothing dispatched, no run id exists, nothing written to production — the coordinator stopped on first-hand check.

**FINDING 1: the pipeline has NO Preview step.** `governed-supabase-production-deploy.yml` (tip blob `bdc641d0…`, 1,047 lines) has zero mentions of "preview" and no preview workflow exists in the repo's 40 workflows. Steps: resolve authorization → build stamped deployment commit → promote to `production` branch → Supabase GitHub Integration check applies the branch's migrations to production DIRECTLY. A failed check stops the run before the producer/proof dispatches, but migrations up to the failure point are ALREADY applied. **The Gate-1 report's claim "if Preview fails, production is untouched" is FALSE for this pipeline — and I repeated it to Shawn; correction owed.**

**FINDING 2: §2 grants and §3 table/function have NO migration files.** `naya_action_events` appears in 2 files, both notes; `naya_category_prototypes` in 0 files. The pipeline moves migration files only, so a dispatch CANNOT apply §2/§3 — the exact pieces that unblock posting, likes, comments, shares, messenger. The packet §6.1 says the applier files §2+§3 as migration(s); that filing never happened.

**BLAST RADIUS IF IT HAD DISPATCHED:** 18 unapplied migration files (195 on main − 177 applied), 14 outside the packet's scope (booking, conversational intake, smart lists, smart-mail RLS ×2, smart match, supersede fallback, ledger baseline, person-timeline ×2). The `production` branch does NOT exist (404) — a dispatch would create it and apply all 18 at once.

**DIVERGENCE-3:** checked, will NOT break the chain — all three repairs idempotent (`IF NOT EXISTS`); out-of-band columns no-op on re-apply; drift still unexplained.

**FLAG:** the pipeline promotes on push too, under standing policy — a quiet-tip push run could promote without any dispatch.

**PATHS:** A (correct) — file §2+§3 as migration file(s) on main first, then resolve the preview question (build a real Supabase preview-branch path, or re-authorize production-direct with eyes open about the 18-file blast radius and the missing §2/§3, which would still need a separate apply route: direct SQL via dashboard/service key, his hand). B (only on explicit re-authorization) — dispatch as-is, accepting 18 migrations production-direct, no preview, no §2/§3.

**DECISION OWED TO SHAWN — the dispatch he authorized (with Preview as the gate) does not exist as authorized.**

## Why it matters

The stop was right and the authorization was right — and both were aimed at a gate that does not exist. The coordinator did the wise thing: it checked first-hand instead of dispatching on the report's word, and stopped rather than putting 18 migrations on production under a false premise. The correction is owed in plain words: I told him Preview was the gate, and there is no Preview. **The correction is now carried in the Daily Project Intelligence Report 2026-11-21 (v3/v4, commit `56a90421`) in public** — the report says the Preview claim was false. The decision that is actually his now is Path A or Path B with eyes open — not a dispatch that was already made.

## How to use it

Nothing is dispatched until the decision is made again, on the true shape: Path A files §2+§3 first and builds a real preview path; Path B is production-direct with the 18-file blast radius accepted and §2/§3 still needing a separate apply route. The push-trigger flag rides with whichever path — a quiet-tip push could promote before the puzzle is complete.

---

**Written by Naya for Shawn — Founder / Creator of NayaNET.**

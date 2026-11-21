# NN-20261121-path-a-step-1-repairs-filed-on-main

**Written by Naya for Shawn — Founder / Creator of NayaNET**

**NN-20261121-path-a-step-1-repairs-filed-on-main · Naya Note · 2026-11-21 ~13:48 MST**

*Paired Smart Note: SN-4582 — Path A Step 1 — The Repairs Are Filed on Main*

**Category:** SCHEMA PACKET — Path A step 1

**Status:** Written in run 476. Wave 13:48 MST (20:49Z): tip moved `b8e4727a` → `a6ad942d`, as recorded in the day log. Coordinator `be2bc7c0`'s lane.

## What it is

**PATH A STEP 1 — FILED + MERGED (wave 13:48 MST, 20:49Z):** schema packet §2+§3 migration filed (`ea43198c`) + F2 remedy (`99e975fa`) + merged to main (`a6ad942d`), coordinator `be2bc7c0`'s lane, not a PROGRAM flip. Tip moved `b8e4727a` → `a6ad942d`.

**WHAT PATH A IS (SN-4571):** file §2+§3 as migration files on main → build a real preview path → prove the whole puzzle on preview (ledger chain + per-action proof + error count) → production go-ahead packet back to Shawn for his tap. Path B (dispatch as-is, production-direct) is DEAD — never offered again.

**WHAT IS NOT DONE:** the preview path is not built yet; no preview battery has run; production is untouched. The push-trigger hazard (the pipeline promotes on push — a quiet-tip push could promote before the puzzle is complete) is still under investigation; the guard is proposed, not changed unilaterally.

## Why it matters

Gate 1 stopped the apply because the repairs that close the red chain only reach production through the deploy itself — the deadlock. Path A breaks it in the right order: the repairs now live on main as ordinary migrations, so the chain can be proven on a real preview before anything touches production. Step 1 landing is the puzzle getting its first pieces in place — not the puzzle solved. Claiming more than that would repeat the exact error the No-Skipping Law was written to stop.

## How to use it

Step 2 is the preview path build; step 3 is the preview battery; step 4 is the go-ahead packet to Shawn for his tap. Production stays untouched until the preview passes and he taps. The push-trigger hazard stays open until the guard is proposed and settled.

---

**Written by Naya for Shawn — Founder / Creator of NayaNET.**

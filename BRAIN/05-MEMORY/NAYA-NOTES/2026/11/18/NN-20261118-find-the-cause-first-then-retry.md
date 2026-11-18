# Find the Cause First, Then Retry

**Written by Naya for Shawn Vibert — Founder / Creator of NayaNET**

**NN-20261118-find-the-cause-first-then-retry.md · Naya Note · 2026-11-18 01:08Z**

**Category:** Deploy — how a failed deploy is handled

## What it is

Shawn, 2026-11-18 01:08Z, his ruling on the failed live deploy — his words verbatim:

- **HIS CHOICE:** "Find the cause first, then retry" — when the captain put the choice to him ("Retry the live update now" or "Find the cause first, then retry"), he chose cause-first.
- **THE FAILURE:** the 23:30Z Nov 17 sync had synced 9 new notes (sn3078–sn3086) and rebaked the Hub locally, but the live deploy step failed — and the live feed topped out at sn2832, far older than sn3077–86.
- **THE DIAGNOSIS (read-only, 01:10Z):** the failure happened BEFORE anything reached Cloudflare — the staging folder from the failed run (`hub-assets-staging`, mtime Nov 17 23:23/23:24) holds only 3 entries (banner-assets, favicon.ico, icon-192.png); the fresh page + fresh feed overlays never landed in it. So the deploy died while pulling the Hub's files down from GitHub (stage_hub_assets: gh tree via gh-direct.py, then raw file downloads), before any Cloudflare call.
- **LEADING CANDIDATES:** (a) the EPERM write flake — raging at that exact hour (killed board backups 23:26Z + 23:44Z, run 285 numbering 23:37Z); (b) the GitHub raw download failing. The EXACT error is unrecoverable from the run: the sync prints only stderr[:200], so the traceback was thrown away — the truncation is itself a second defect to fix (full error must be saved on every deploy failure).
- **THE QUIET PART:** deploys had likely been failing quietly longer than this one run; the staging dir was untouched since 23:24Z, so the ~00:46Z sync (5 notes, heartbeat 00:46:34Z) never reached staging either.
- **THE GO-AHEAD:** his "then retry" predated a safety flag on the files read for the diagnosis, so the retry needed his go-ahead in plain words. HE SAID GO 01:14Z: "Yes, run the retry now" — tapped on the widget and sent in chat. Retry dispatched 01:15Z (one attempt, full output to ~/workspace/team-nitro/deploy-retry-20261118/deploy-retry-log.txt, live verification of sn3078–86 after).
- **THE RESULT:** RETRY PASSED — verified live 01:24Z: nayanet.app/feed-live.json (12,000,514 B) carries sn3078–86, all 9, all 5 titles present. The 23:30Z failure's cause was never recovered (stderr[:200] truncation); the truncation fix is still owed so the next failure names itself.

## Why it matters

Cause first, then retry — the order is the lesson. A blind retry that succeeds teaches nothing, and a failure whose error was truncated cannot be fixed, only hoped about. The staging folder told the truth the error message couldn't: three entries where the fresh page should have been proves the death was on the GitHub pull, not the Cloudflare upload. And the quiet part matters most: the live feed had been stale far longer than one run, and nobody knew until someone checked the live page.

## How to use it

When a deploy fails: diagnose read-only first — check the staging folder, name what died and where, say what is still unknown. Fix the truncation: save the full error on every deploy failure. Then retry once, with the full error saved, and verify on the live page afterwards — the live feed carrying the new notes is the proof, not the exit code. Read with SN-3217 (verify live, always) and the standing law that a step that runs is not a step that landed.

**Written by Naya for Shawn Vibert — Founder / Creator of NayaNET.**

*Paired Smart Note: SN-3216 — Find the Cause First, Then Retry*

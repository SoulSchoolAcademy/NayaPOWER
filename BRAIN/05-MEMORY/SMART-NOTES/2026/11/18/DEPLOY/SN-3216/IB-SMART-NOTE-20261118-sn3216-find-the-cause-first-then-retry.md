# Find the Cause First, Then Retry

SN-3216 · DEPLOY — HOW A FAILED DEPLOY IS HANDLED

**Filed:** Intelligence Loop filing push 2026-11-18 — numbering confirmed by `next-sn-number.py` (exit 0) immediately before filing: next free SN-3268; filed as SN-3216 under its draft number.

**Created:** 2026-11-18 01:08Z (Shawn's ruling on the failed live deploy, recorded in MEMORY.md and the daily log; drafted in run 289)

**Paired Naya Note:** NN-20261118-find-the-cause-first-then-retry

## Hook

When the live update fails, find the cause first — then retry. Never retry blind into a failure you cannot see, because a retry that succeeds tells you nothing about why the first one failed, and the next failure will be just as blind. The cause hunt is read-only and comes before any go-ahead: say what died, where it died, and what is still unknown — then the retry runs with the full error saved, so a repeat failure names itself.

## Nutshell

Shawn, 2026-11-18 01:08Z: **FIND THE CAUSE FIRST, THEN RETRY** — when the captain put the choice to him ("Retry the live update now" or "Find the cause first, then retry"), he chose cause-first. **THE FAILURE WAS BEFORE CLOUDFLARE** — the 23:30Z Nov 17 sync had synced 9 new notes (sn3078–sn3086) and rebaked the Hub locally, but the live deploy step failed; the read-only diagnosis (01:10Z) showed the staging folder held only 3 entries (banner-assets, favicon.ico, icon-192.png) — the fresh page and fresh feed overlays never landed in it — so the deploy died while pulling the Hub's files down from GitHub (gh tree, then raw downloads), before any Cloudflare call. **THE EXACT ERROR IS UNRECOVERABLE** — the sync prints only stderr[:200], so the traceback was thrown away; the truncation is itself a second defect: the full error must be saved on every deploy failure. **LEADING CANDIDATES** — (a) the EPERM write flake, raging at that exact hour (killed board backups 23:26Z + 23:44Z, run 285 numbering 23:37Z); (b) the GitHub raw download failing. **THE QUIET PART** — the live feed topped out at sn2832, far older than sn3077–86, so deploys had likely been failing quietly longer than this one run; the staging dir was untouched since 23:24Z, so the ~00:46Z sync never reached staging either. **THE RETRY** — his go-ahead in plain words came 01:14Z ("Yes, run the retry now"), the retry was dispatched 01:15Z (one attempt, full error saved), and it PASSED — verified live 01:24Z: nayanet.app/feed-live.json (12,000,514 B) carries sn3078–86, all 9, all 5 titles present. **STILL OWED** — the 23:30Z failure's cause was never recovered; the truncation fix is still owed so the next failure names itself.

## Human

This ruling changes the shape of every deploy failure from here on: the failure is diagnosed before it is retried, and the diagnosis is read-only — no deploy script runs on a guess. The evidence that decides it is the staging folder: three entries where the fresh page and feed should have been is proof the death happened on the way down from GitHub, not on the way up to Cloudflare, and that single fact moves the hunt from "the upload broke" to "the download broke" — two different hunts, two different fixes. The second defect is the one that matters most going forward: a deploy step that prints only the first 200 characters of its error throws away the traceback, and a failure whose cause cannot be recovered cannot be fixed — it can only be retried and hoped about. So the law that comes out of this night is twofold: cause first, then retry; and every deploy failure saves its full error, every time, so the next failure names itself. The retry that followed proves the shape works: one attempt, full error saved, live verification after — and the live feed now carries all nine notes that had been sitting filed-but-not-live. The watch-out stays open: the cause of the original failure was never recovered, and the live feed had been quietly stale for far longer than one run — a deploy that fails quietly is worse than one that fails loudly, because nobody knows the Hub is behind until someone checks the live page.

## Child

Imagine you try to put your new drawings on the wall and they don't stick. Don't just try again the same way — first look: did the drawings even get to the wall, or did they fall on the way? That's what Shawn said: find out what went wrong first, then try again. And when something goes wrong, write down the WHOLE reason, not just the first little bit — otherwise you'll never know what really happened. The retry worked, and all nine new notes are on the live Hub now.

## Grandma

Dear, when the new notes wouldn't go live, Shawn said: find the cause first, then retry — don't just try again blind. We looked, dear, and found the new pages never even reached the staging shelf — they fell on the way down from GitHub, before anything touched Cloudflare. The exact reason was lost because only the first little bit of the error was saved — so from now on we save the whole error, every time. The retry worked, dear — all nine notes are live on the Hub now, and we checked them ourselves on the real page.

## Naya

FIND THE CAUSE FIRST, THEN RETRY. THE FAILURE WAS BEFORE CLOUDFLARE — THE FRESH PAGE NEVER REACHED STAGING. A FAILURE WHOSE ERROR IS TRUNCATED CANNOT BE FIXED — SAVE THE FULL ERROR, EVERY TIME. THE RETRY PASSED, LIVE-VERIFIED: SN3078–86 ON THE LIVE HUB.

## What it means

- **CAUSE FIRST, THEN RETRY:** when a deploy fails, the diagnosis comes before the retry — read-only, naming what died and where — and the retry runs only after, with the full error saved.
- **THE FAILURE WAS BEFORE CLOUDFLARE:** staging held only 3 entries; the fresh page and feed never landed — the deploy died pulling files down from GitHub, not uploading.
- **THE TRUNCATION IS A SECOND DEFECT:** stderr[:200] threw the traceback away; the exact error is unrecoverable. Every deploy failure must save its full error from now on.
- **LEADING CANDIDATES:** (a) the EPERM write flake, raging at that hour; (b) the GitHub raw download failing. Neither is proven — the cause was never recovered.
- **DEPLOYS HAD BEEN FAILING QUIETLY:** the live feed topped out at sn2832, far older than sn3077–86. A deploy that fails quietly is worse than one that fails loudly.
- **THE RETRY PASSED, LIVE-VERIFIED 01:24Z:** nayanet.app/feed-live.json (12,000,514 B) carries sn3078–86, all 9, all 5 titles present. A step that runs is not a step that landed — the live page is the proof.
- **STILL OWED:** the truncation fix, so the next failure names itself.

## Why it matters

Without this note, the next deploy failure gets retried blind the same way — and if it succeeds, nobody learns why the first one failed, so the same failure comes back the next night, just as quiet. With it, the machine has a shape: diagnose read-only, name the death point, save the full error, retry once, verify on the live page. The staging-folder check is now the first move of any deploy diagnosis, and the truncation fix is the one owed change that makes every future failure diagnosable.

## What changes now

1. Every deploy failure is diagnosed read-only before any retry — what died, where it died, what is still unknown.
2. Every deploy failure saves its FULL error, every time — the stderr[:200] truncation is a defect to fix, not a habit to keep.
3. The staging folder is the first evidence checked: if the fresh page and feed never landed, the death was on the GitHub pull, before Cloudflare.
4. A retry runs once, with the full error saved, and is verified on the live page afterwards — sn3078–86 live in nayanet.app/feed-live.json is the proof, not the exit code.
5. A deploy that fails quietly is treated as the worse failure — the live feed's newest note is checked, not assumed.

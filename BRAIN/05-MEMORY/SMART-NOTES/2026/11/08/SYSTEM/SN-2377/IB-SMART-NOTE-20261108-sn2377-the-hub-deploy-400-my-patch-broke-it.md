# The Hub Deploy 400 — My Patch Broke It

SN-2377 · SYSTEM

**Created:** 2026-11-08 22:01Z (fault) + 22:15Z (fix seat dispatched)
**Source:** Smart Notes sync 22:01Z (SN-2371–SN-2374 synced, Hub redeploy PUT 400'd, error 10305) + HUB-DEPLOY-400-FIX-BRIEF-20261108.md + 21:55:05Z mail to Resolve asking for the exact wrangler command (thread d4beddfa, still owed at this run's close) (daily log 2026-11-08.md; MEMORY.md). Independently checked this run: both briefs on disk; no Resolve reply in the 30-minute canonical mail window.

> The 21:47Z bindings fix declares an ASSETS binding on a script-only PUT with no assets uploaded — Cloudflare error 10305: "Cannot use an assets binding without assets." The live worker is untouched (clean rejection), but the Hub is stale and will NOT self-heal, because the sync only redeploys on new notes.

## Hook

The fix that was supposed to stop the bindings being stripped broke the deploy instead — the note that filed the fix had predicted exactly this failure, and the very next sync proved it right.

## Nutshell

**THE FAULT (sync 22:01Z):** 4 new notes synced (SN-2371–SN-2374), the Hub baked fine locally, but the redeploy PUT 400'd — error 10305 "Cannot use an assets binding without assets". The 21:47Z bindings fix declares an ASSETS binding on a script-only PUT with no assets uploaded. **THE DAMAGE:** the live worker is untouched (a clean rejection — nothing half-deployed), but the Hub is STALE and will NOT self-heal, because the sync only redeploys when new notes arrive. **THE PREDICTION THAT CAME TRUE:** SN-2374 itself named this exact risk — "a PUT declaring an assets binding without uploading assets may 400 — non-fatal, patch revised if so" — and the very next sync proved it. The note was right; the patch was not. **THE FIX (seat dispatched 22:15Z, brief HUB-DEPLOY-400-FIX-BRIEF-20261108.md):** the wrangler route via Resolve's invocation if it has arrived, or a proper multipart assets upload in deploy.py; dry-run first, then re-deploy + live proof (ASSETS binding present + SN-2371–SN-2374 served). **NEVER drop the binding to clear the 400** — dropping it returns to the strip, which was the original fault. **THE MISSING PIECE:** the captain asked Resolve at 21:55:05Z for the exact wrangler command the repo workflow uses, "so the seat can point the Python upload step at it and the bindings survive every re-bake" — no reply in the mail window to 22:23Z; the fix seat runs without it, on the multipart route if needed. **TOLD TO SHAWN plainly, in the same pass, owning it.** **RELATED:** SN-2374 (the bindings fix — the patch that broke the deploy); SN-2375 (the re-bake fault — the other fix riding on the same next sync); SN-2366 (the Hub deploys itself — the sync redeploys on every run with new notes).

## Human

The bindings fix went in at 21:47Z to stop the deploy from stripping the bindings — and at 22:01Z, the very next sync, the deploy failed with a 400. Cloudflare's answer was exact: you cannot use an assets binding without assets. The patch declares the binding and uploads no assets, so the PUT is rejected outright. The live worker is untouched — a clean rejection means nothing half-deployed — but the Hub is stale, and it will not heal itself, because the sync only redeploys when new notes arrive. The part worth keeping is that the note that filed the fix had already named this exact risk, in writing: a PUT declaring an assets binding without uploading assets may 400. Non-fatal, patch revised if so. The note was right and the patch was not, and the very next sync proved it — which is the system working as designed: the risk was named before it happened, so the fix was already scoped when it did. The fix seat went out at 22:15Z: either the wrangler route, using Resolve's exact command if it arrives, or a proper multipart assets upload in deploy.py — dry-run first, then redeploy with live proof that the binding is present and the four new notes are served. One rule rides with it, and it is not negotiable: never drop the binding to clear the 400. Dropping it is going back to the strip, which was the fault the patch was written to fix. The captain asked Resolve for the wrangler command at 21:55Z, and there is no reply yet. And the fault was told to Shawn plainly, in the same pass, owned — because a captain who breaks the deploy says so before anyone has to find it.

## Child

Imagine you fixed your toy car by adding a shiny new part — but you forgot to add the wheels that part needs! So the car won't run at all. That's what happened: the fix added a special "assets" part to the Hub, but didn't send any assets along with it — so the machine said "nope, I can't use that part without its wheels!" and refused the whole thing. The good news: the old car is still running fine, just with yesterday's notes. And the clever part: the note that filed the fix had ALREADY written down "this might happen!" — so when it did happen, everyone already knew what to do. The fix is coming: either use the exact magic words the other team uses, or pack the wheels in properly this time. And one rule: never just throw the shiny part away to make it work — that brings back the old problem!

## Grandma

Dear, it's a story about a fix that broke the very thing it was fixing, dear. The patch was meant to stop the Hub from losing its bindings — but it declared the binding without sending the assets along, so the whole delivery was refused, dear, error 10305: you can't use an assets binding without assets. The live page is safe — nothing half-delivered — but it's stale now, and it won't fix itself, because the machine only delivers when new notes arrive. Here's the clever part, dear: the note that filed the fix had already written down that this exact thing might happen! So when it did, the fix was already waiting. The repair is on its way — either the exact command from the other team, or packing the assets in properly — and one rule, dear: never just throw the binding away to make the error go away, because that brings back the old trouble. And the captain told Shawn straight away, dear, plainly, owning it — because that's what you do when you break something.

## Naya

I never declare a binding without uploading what it binds — a PUT that names assets and sends none is refused outright, and the refusal is the proof the declaration was incomplete. I never drop a binding to clear an error — dropping it returns to the strip, which was the fault the patch was written to fix. I never hide a fault I caused — it was told to Shawn plainly, in the same pass, owned. I name the risk before it happens, so when it happens the fix is already scoped: SN-2374 predicted this exact 400, and the next sync proved it.

## What it means

1. **The fault:** sync 22:01Z — SN-2371–SN-2374 synced, Hub baked fine locally, redeploy PUT 400'd (error 10305 "Cannot use an assets binding without assets").
2. **The cause:** the 21:47Z bindings fix declares an ASSETS binding on a script-only PUT with no assets uploaded.
3. **The damage:** live worker untouched (clean rejection); Hub STALE and will NOT self-heal (sync redeploys only on new notes).
4. **The prediction:** SN-2374 named this exact risk ("may 400 — non-fatal, patch revised if so") — the note was right, the patch was not, and the very next sync proved it.
5. **The fix:** seat dispatched 22:15Z (brief HUB-DEPLOY-400-FIX-BRIEF-20261108.md) — wrangler route via Resolve's invocation if arrived, or proper multipart assets upload in deploy.py; dry-run first, then re-deploy + live proof (ASSETS binding + SN-2371–SN-2374 served).
6. **The rule:** NEVER drop the binding to clear the 400 — that returns to the strip.
7. **The missing piece:** Resolve's exact wrangler command, asked 21:55:05Z (thread d4beddfa) — no reply in the mail window to 22:23Z.
8. **The telling:** told to Shawn plainly, in the same pass, owning it.

## Why it matters

A fix that breaks the deploy is not a failed fix — it is a fix whose risk was named, whose failure was clean, and whose repair was already scoped. That is the difference between a fault and a disaster: the live worker was untouched because the rejection was clean, the Hub's staleness is bounded because the next sync re-proves it, and the repair path was written before the fault happened because SN-2374 said the words out loud. The lesson is the order of operations: a binding is a promise of assets, and a PUT that promises without delivering is refused — so the deploy must either upload the assets or invoke the tool that does. And the rule that rides with it — never drop the binding to clear the error — is the one that keeps a quick clear from becoming a quiet return to the original fault.

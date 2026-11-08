# The Hub Bindings Fix — Carry the Binding

SN-2374 · SYSTEM

**Created:** 2026-11-08 21:47:33Z
**Source:** Hub bindings fix DONE, 2026-11-08 21:47:33Z (seat df6bc7f4; captain verified the patch by reading deploy.py; daily log 2026-11-08.md; MEMORY.md). Mailed to Resolve 21:47Z (thread a362930f, msg 735fbd90). Independently checked this run: `HUB_BINDINGS` present in `~/workspace/factory-pipeline/deploy.py` (line 205) and carried into metadata (line 218).

> "HUB_BINDINGS = [{"name": "ASSETS", "type": "assets"}] + assets config + build_metadata() — hub redeploys now carry the binding + config; non-hub workers byte-identical."

## Hook

A deploy that does not know what it carries strips what it does not carry. The fix: the bindings are named in the code now, so the next sync redeploy carries them — and the finding underneath is the real lesson: the toml declares zero bindings, and the binding the Hub runs on is inferred, not declared.

## Nutshell

**THE FIX (DONE 21:47:33Z, captain-verified by reading deploy.py):** `HUB_BINDINGS = [{"name": "ASSETS", "type": "assets"}]` + assets config + `build_metadata()` — hub redeploys now carry the binding + config; non-hub workers byte-identical. **THE STORY:** the 19:30:43Z Smart Notes sync redeployed worker `hub` with a PUT carrying metadata {main_module, compatibility_date} and NO bindings — a Cloudflare PUT replaces non-secret bindings, so they were stripped, and the hub has had zero bindings since (SN-2366). **THE KEY FINDING: the toml declares ZERO bindings** — no `binding = "ASSETS"` line; the binding is INFERRED from hub-worker.js lines 433/444 (env.ASSETS fall-through). Secrets SUPABASE_URL + SUPABASE_READ_KEY survive omission, never listed. **MAILED TO RESOLVE 21:47Z (thread a362930f, msg 735fbd90):** patch in + the toml gap is hers to add. **HONEST LIMITS (named, not hidden):** live PUT acceptance unproven until the next sync redeploy (get-bindings check then) · the patch stops the strip but does NOT by itself restore the /s/* 302s (those live in hub-worker.js; full route behavior rides on the next repo deploy) · toml compatibility_date 2026-10-17 vs deploy.py 2024-01-01 left as-is (captain's call) · two execs in the seat's record exited 1 (unexplained in the handoff; verification passed — likely grep no-matches). **UNTESTED RISK (21:50Z addendum):** the next sync PUT declares an assets binding + config without uploading assets — if Cloudflare 400s it, the deploy fails non-fatally (Hub keeps serving the previous bake, notes already in Supabase) and the patch needs revision. **COMBINED PROOF:** the next real sync redeploy must both land the re-bake (SN-2375) AND show the ASSETS binding on get-bindings for `hub` — one run proves both fixes. **RELATED:** SN-2366 (answer her, don't escalate — the Hub deploys itself; the strip, the question, the answer); SN-2375 (the re-bake fault — the other fix riding on the same next sync).

## Human

The bug was never in the worker — it was in the deploy. A Cloudflare PUT replaces the bindings it is given, and the sync's PUT gave it none, so the Hub's bindings were stripped on 19:30:43Z and the Hub has run with zero bindings since. The fix names what the deploy carries: HUB_BINDINGS, the assets config, build_metadata — so the next redeploy carries the binding instead of silently dropping it, and non-hub workers stay byte-identical. But the finding underneath the fix is the one that matters, and it is the kind of finding that only appears when someone reads the file instead of assuming it: the toml declares zero bindings. There is no `binding = "ASSETS"` line anywhere in it. The binding the Hub runs on is inferred — from hub-worker.js lines 433/444, an env.ASSETS fall-through — declared nowhere, carried by convention. The patch makes the deploy carry what the worker infers, and the toml gap goes to Resolve to add, because a binding that exists only by inference is a binding waiting to be stripped again. The secrets are safe — SUPABASE_URL and SUPABASE_READ_KEY survive omission and were never listed — but the honest limits stay open: the live PUT is unproven until the next sync redeploy shows the binding on get-bindings; the patch stops the strip, it does not restore the /s/* 302s, which live in hub-worker.js and ride on the next repo deploy; and there is one untested risk, that a PUT declaring an assets binding without uploading assets gets a 400 from Cloudflare — in which case the deploy fails non-fatally, the Hub keeps serving the previous bake, the notes are already in Supabase, and the patch gets revised. One run proves both this fix and the re-bake fix beside it.

## Child

Imagine you have a magic backpack, and every time you pack it, you forget to put in the most important thing — because nobody wrote it on the list! The list said nothing, so the backpack went out empty. The fix is simple: write it on the list! Now the list says "ASSETS" in big letters, so every time the backpack gets packed, the important thing goes in. But guess what? The grown-ups found something funny: the important thing was never written down ANYWHERE — it was just guessed from how the backpack behaved! So now someone has to write it down properly, in the real list, so it never gets lost again.

## Grandma

Dear, it's a cautionary tale about lists. The Hub's most important connection — its assets — was never actually written down anywhere, dear. It was just guessed at, inferred from the way the code behaved. And when the packing list went out empty, the connection was quietly taken away, and nobody noticed until the links stopped working. The fix writes it on the list now, dear — the binding is named in the code, so every future packing carries it. But the proper list — the toml — still doesn't declare it, and that's the gap that must be closed, or the same quiet loss will happen again. The secrets are safe, dear, and the next real delivery will prove whether the fix holds. One delivery proves two fixes at once.

## Naya

I never deploy what I have not named — a PUT that carries no bindings deletes the bindings, so the bindings are named in the code before the deploy runs. I never trust an inference as a declaration — a binding that exists only by fall-through is a binding waiting to be stripped, so the toml gap goes to its owner to close. I never claim a fix is live before the live check — get-bindings on the next sync redeploy is the proof, and until then the fix is filed, not proven. I never hide the untested risk — if Cloudflare 400s the binding-without-assets PUT, the deploy fails non-fatally and the patch gets revised, and I say so before it happens.

## What it means

1. **A PUT replaces what it does not carry:** the 19:30:43Z sync PUT carried no bindings, so Cloudflare stripped them — the hub has had zero bindings since.
2. **The fix names the binding:** `HUB_BINDINGS = [{"name": "ASSETS", "type": "assets"}]` + assets config + `build_metadata()` — hub redeploys carry the binding + config; non-hub workers byte-identical.
3. **The toml declares ZERO bindings:** no `binding = "ASSETS"` line — the binding is inferred from hub-worker.js lines 433/444 (env.ASSETS fall-through). The gap is Resolve's to add (mailed 21:47Z, thread a362930f).
4. **Secrets survive omission:** SUPABASE_URL + SUPABASE_READ_KEY are never listed and survive — the strip only takes non-secret bindings.
5. **The patch stops the strip, not the route loss:** the /s/* 302s live in hub-worker.js — full route behavior rides on the next repo deploy.
6. **The untested risk is named:** a PUT declaring an assets binding without uploading assets may 400 — non-fatal (Hub serves the previous bake, notes in Supabase), patch revised if so.
7. **One run proves both fixes:** the next real sync redeploy must land the re-bake (SN-2375) AND show ASSETS on get-bindings for `hub`.

## Why it matters

Every deploy is a claim about what the system carries, and a deploy script that cannot name its bindings cannot keep them. The strip was silent — no error, no alarm, just a worker running with zero bindings and links quietly failing — which is why the fix had to be mechanical, not careful: the bindings live in the code now, carried by every PUT, instead of living in someone's memory of what the worker needs. And the toml gap is the deeper lesson: a thing that exists only by inference is a thing that will be lost again, by the next person who reads the file and finds nothing there. Declarations are the memory of the system; inferences are the forgetting of it.

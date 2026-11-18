# Verify by Blob, Never by cb

**Written by Naya for Shawn Vibert — Founder / Creator of NayaNET**

**NN-20261116-verify-by-blob-never-by-cb.md · Naya Note · 2026-11-16 10:07Z**

**Category:** System

## What it is

Method caveat, recorded honestly in the My World redesign delivery, 2026-11-16 10:07Z (staged Personal sha 9b4353d8, 3,121,411 B, branch personal/my-world-redesign-20261116, commit 7c9e3c83, blob 2dd70c7e): the proof host IGNORES `cb` — curling an old build's URL with a new/old `cb` returns the current build. Old builds must be verified from the branch's own blob (GitHub blob API decode) or an independently curled copy, never by a cb URL. The captain's own verification before delivery did it right: curl of the staged URL byte-identical (3,121,411 B, sha 9b4353d8…, 0× nayanet.live) + own Firefox probe on her own curled copy, seeded citizen stores, real clicks.

## Why it matters

A cache-buster that doesn't bust the cache is worse than no cache-buster at all — it tells you the build is verified while showing you a different build. The `cb` parameter looks like proof: same URL, different `cb`, surely a different build. It isn't. The proof host serves the current build whatever `cb` you pass, so a "verification" by cb URL can pass on bytes you never built and fail on bytes you did.

## How to use it

Staged builds are verified from the branch's own blob (GitHub blob API decode) or an independently curled copy — never by a cb URL. A curl byte-identical to the blob sha is the receipt; a cb URL is not a receipt. The captain's eye probes her own curled copy, not a hosted URL she doesn't control.

**Written by Naya for Shawn Vibert — Founder / Creator of NayaNET.**

*Paired Smart Note: SN-2946 — Verify by Blob, Never by cb*

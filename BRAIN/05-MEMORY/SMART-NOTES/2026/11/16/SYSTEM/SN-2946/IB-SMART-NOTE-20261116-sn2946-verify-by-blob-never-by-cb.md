# Verify by Blob, Never by cb

SN-2946 · SYSTEM

**Created:** 2026-11-16 10:07Z (My World delivery method caveat)

**Paired Naya Note:** NN-20261116-verify-by-blob-never-by-cb

## Hook

The proof host ignores `cb` — curling an old build's URL with a new or old `cb` returns the current build. Verify staged builds from the branch's own blob, never by a cb URL.

## Nutshell

Method caveat, recorded honestly in the My World redesign delivery, 2026-11-16 10:07Z (staged Personal sha 9b4353d8, 3,121,411 B, branch personal/my-world-redesign-20261116, commit 7c9e3c83, blob 2dd70c7e): the proof host IGNORES `cb` — curling an old build's URL with a new/old `cb` returns the current build. Old builds must be verified from the branch's own blob (GitHub blob API decode) or an independently curled copy, never by a cb URL. The captain's own verification before delivery did it right: curl of the staged URL byte-identical (3,121,411 B, sha 9b4353d8…, 0× nayanet.live) + own Firefox probe on her own curled copy, seeded citizen stores, real clicks. The same discipline runs through the day's other verdicts: the certificate round-4 captain re-curled all three staged shas (matched); the Hub alignment captain re-curled the staged Hub (200, sha matched); the about-unfold captain curl-verified the staged bytes (sha ba8fa387, 3,109,527 B, nayanet.live 0×).

## Human

A cache-buster that doesn't bust the cache is worse than no cache-buster at all — it tells you the build is verified while showing you a different build. The `cb` parameter looks like proof: same URL, different `cb`, surely a different build. It isn't. The proof host serves the current build whatever `cb` you pass, so a "verification" by cb URL can pass on bytes you never built and fail on bytes you did. The fix is to verify from the source of truth: the branch's own blob, decoded through the GitHub blob API, byte-compared to what you curled — or an independently curled copy you control. Every captain's-eye verification in the day's log does it this way, and that is why their deliveries hold.

## Child

Imagine you have a magic box that always gives you the NEWEST toy, no matter which number you ask for! If you ask for toy number 5, you get the newest toy. If you ask for toy number 9, you still get the newest toy! So the number doesn't prove anything. To really check a toy, you have to look at the toy itself — not the number you asked for.

## Grandma

It's like this, love — if the shop always hands you the latest loaf no matter which one you point at, then pointing doesn't tell you which loaf you got. You have to look at the loaf itself. Same here: the little `cb` number doesn't change what comes back, so you check the real thing — the blob — not the number.

## Naya

Verify by blob, never by cb. The proof host ignores `cb` — a cb URL can pass on bytes you never built.

## What it means

- **THE FACT:** the proof host IGNORES `cb` — curling an old build's URL with a new/old `cb` returns the current build.
- **THE RULE:** old builds are verified from the branch's own blob (GitHub blob API decode) or an independently curled copy — never by a cb URL.
- **THE PATTERN:** every captain's-eye verification in the day does it this way — re-curl the staged shas, byte-compare, probe your own curled copy.
- **THE RISK:** a cb "verification" can pass on bytes you never built — it looks like proof and proves nothing.

## Why it matters

Verification is the whole job — the loop's proof standard is "never claim done without proof", and a proof that proves the wrong build is worse than no proof, because it closes the item on false evidence. The My World delivery recorded the caveat honestly instead of burying it, and the fix is mechanical: blob API, byte compare, every time. A seat that learns this never wastes a round arguing with a "verified" build that was never the build under test.

## What changes now

1. Staged builds are verified from the branch's own blob (GitHub blob API decode) or an independently curled copy — never by a cb URL.
2. A curl byte-identical to the blob sha is the receipt; a cb URL is not a receipt.
3. The captain's eye probes her own curled copy, not a hosted URL she doesn't control.
4. The caveat is recorded in the delivery, not buried — honest limits ride with the PASS.

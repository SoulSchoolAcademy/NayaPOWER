# The Mobile Stack — One Viewport on the Phone

SN-2373 · DESIGN

**Created:** 2026-11-08 21:40:53Z
**Source:** Mobile-stack fix DONE + presented, 2026-11-08 21:40:53Z (daily log 2026-11-08.md). Builder's own audit capture; fix pass 2 round complete, pending his eye.

> The entrance now fits entirely in one 390×844 viewport (builder's own audit capture: portrait + gauge ring complete, statement complete, Start free now + all three pills fully visible, clear space below pill 3, overflow 0). Root cause: the §8 desktop enlargements (16.5px board type, 42px pill jewels) had cascaded into mobile; one mobile-only block overrides them at ≤900px (board 14px, avatar 44px, pills 11.5px/26px jewels, stage 168px). Desktop untouched; checklist verified (36/36/36, greps 0, Naya Free 29×, Max default, nine hrefs, scripts pass). Builder's self-score 9.2/10.

## Hook

The phone gets its own law: what is enlarged for the desktop must not cascade into the mobile. One mobile-only override, and the whole entrance fits one 390×844 viewport — portrait, statement, door, and all three pills in view, overflow zero.

## Nutshell

**THE FIX (DONE 21:40:53Z + PRESENTED — fix pass 2 round complete, pending his eye):** the entrance fits entirely in one 390×844 viewport — builder's audit capture shows portrait + gauge ring complete, statement complete, Start free now + all three pills fully visible, clear space below pill 3, overflow 0. **ROOT CAUSE:** the §8 desktop enlargements (16.5px board type, 42px pill jewels) had cascaded into mobile — the luxury scale that made the desktop entrance extraordinary made the phone entrance overflow. **THE FIX, IN ONE MOVE:** one mobile-only block overrides them at ≤900px — board 14px, avatar 44px, pills 11.5px/26px jewels, stage 168px. Desktop untouched. Checklist verified: 36/36/36, greps 0, Naya Free 29×, Max default, nine hrefs, scripts pass. Builder's self-score 9.2/10. **HONEST LIMITS (named, not hidden):** fit verified at exactly 390×844 in the audit's capture engine only — not other phone sizes, not a physical device, no browser-chrome/safe-area check; no independent live render (Playwright broken); portrait smaller than the §8 luxury scale on mobile (208→168px); faint sheen patch behind the gauge ring still visible. **THE ROUND'S STORY:** fix pass 2's two builds landed 21:35:54Z and the round was NOT done — mobile one-viewport still failed by the §8 builder's own capture (door + first pill visible, second pill half-clipped, third pill missing; cause: enlarged statement board + stacked pills). The mobile-stack fix was dispatched 21:36Z and landed 21:40:53Z; the round is now complete, pending his eye. **RELATED:** SN-2364 (the viewport miss — the desktop instance that started fix pass 2); SN-2369 (the viewpoint refinement — one viewport = one viewpoint); SN-2370 (the anatomy of a 10-star viewport — the §8 recipe whose enlargements cascaded).

## Human

The desktop fix and the phone fix are two different jobs, and the mobile-stack fix is the proof: the §8 recipe made the desktop entrance extraordinary — bigger type, bigger jewels, a bigger stage — and every one of those enlargements flowed downhill into the phone, where they did not fit. The phone entrance failed the same law the desktop had just been fixed for: door plus first pill visible, second pill half-clipped, third pill missing. The fix did not rethink the entrance; it drew the line. One mobile-only block, at ≤900px, overrides the desktop scale — board 14px, avatar 44px, pills 11.5px with 26px jewels, stage 168px — and the whole entrance fits one 390×844 viewport: portrait and gauge ring complete, statement complete, Start free now and all three pills fully visible, clear space below the third pill, overflow zero. Desktop untouched. The lesson is the cascade: a scale is not a size, it is a scale — and a scale that is right at desktop width is wrong at phone width unless the phone gets its own numbers. The limits are honest and stay open: the fit is proven at exactly 390×844 in the audit's capture engine only, not on other phone sizes, not on a physical device, with no browser-chrome or safe-area check and no independent live render; the portrait shrinks on mobile (208→168px) against the §8 luxury scale; and the faint sheen patch behind the gauge ring is still there. The round is complete; his eye is the check.

## Child

Imagine you build a beautiful big poster for a big wall — and then you try to squeeze the same big poster onto a tiny phone screen, and the bottom gets all chopped off! That's what happened: the big desktop sizes spilled over into the phone. The fix is simple and clever: the phone gets its OWN sizes! A special little rule says "on small screens, use these smaller numbers" — and suddenly everything fits perfectly on one phone screen: her picture, her words, the big shiny door, and all three pretty pills, with room to spare and nothing cut off!

## Grandma

Dear, it's a simple truth: what fits a big screen doesn't fit a little one. The grand desktop sizes — the big letters, the big jewels — spilled over onto the phone, dear, and the bottom pills were chopped clean off. The fix was a kind little rule just for phones: on a small screen, use small numbers. And now the whole welcome fits on one phone screen, dear — her picture, her words, the door, and all three pretty pills, with a little breathing room underneath and nothing cut off at all. The big screen stays exactly as it was. But mind, dear — it's only been proven on one size of phone, in one test, not on a real phone in a real hand. His eye is still the judge.

## Naya

I never let a desktop scale cascade into a phone — a scale is a scale, and the phone gets its own numbers, in its own block, at its own breakpoint. I never call a viewport done from one size — 390×844 proven is one size proven, not the phone proven. I never hide the shrinkage — the portrait is smaller on mobile, and I say so. I never present a capture as a live render — the audit engine is not a phone, and his eye is the check.

## What it means

1. **The root cause was a cascade:** the §8 desktop enlargements (16.5px board type, 42px pill jewels) flowed into mobile and overflowed it.
2. **The fix is one mobile-only block:** at ≤900px — board 14px, avatar 44px, pills 11.5px/26px jewels, stage 168px. Desktop untouched.
3. **The proof is one viewport:** 390×844, portrait + gauge ring complete, statement complete, Start free now + all three pills fully visible, clear space below pill 3, overflow 0.
4. **The checklist holds:** 36/36/36, greps 0, Naya Free 29×, Max default, nine hrefs, scripts pass. Builder's self-score 9.2/10.
5. **The limits stay open:** fit proven at exactly 390×844 in the audit capture engine only — no other phone sizes, no physical device, no browser-chrome/safe-area check, no independent live render.
6. **The trade is named:** portrait 208→168px on mobile — smaller than the §8 luxury scale; the faint sheen patch behind the gauge ring is still visible.
7. **The round is complete, pending his eye:** fix pass 2's two builds (21:35:54Z) + the mobile-stack fix (21:40:53Z) — his eye decides.

## Why it matters

A viewport law that only holds at desktop width is not a law — it is a preference. The mobile-stack fix is the first time the one-viewport rule was proven on a phone, and the proof came with its mechanism: scales cascade, so the phone needs its own numbers, written down, in its own block, at its own breakpoint. That mechanism is now the pattern for every enlargement that follows — desktop first, phone override second, never one without the other. And the honest limits are part of the lesson, not a footnote to it: one size proven is one size proven, and the phone in his hand is the only proof that counts.

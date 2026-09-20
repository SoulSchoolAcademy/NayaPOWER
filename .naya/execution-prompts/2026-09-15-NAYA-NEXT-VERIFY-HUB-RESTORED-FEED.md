# NAYA → NEXT NAYA — VERIFY RESTORED HUB + FEED

## WHAT ARE WE DOING?
We are restoring the user's actual NayaNET Hub from the recovered `2026 09 15 NayaNETHUB.html` reference and elevating the existing `SmartFeedBoard` into the feed. The Hub is the product surface; nine boards are not the mission.

## WHAT DID I DO?
`AppShellV3.tsx` was surgically restored toward the recovered Hub shell. `routes.ts` now exposes the canonical Hub destination keys. `App.tsx` now renders the restored Hub landing at `/` and keeps `SmartFeedBoard` as the full intelligence-board surface at `/feed`.

## WHAT DID I VERIFY?
GitHub accepted the source mutations. Latest implementation head before this baton: `802777e3d6773cb60ceea433631ba233ddfe3b06`; activity receipt commit: `5e339d33c6b1d42ecb884b3d3cbaffbdbc488903`.

## WHAT DID I LEARN?
The recovered Hub's visual DNA and the existing intelligent-object renderer are complementary assets. Do not replace either with another renderer.

## WHAT IS PROTECTED?
- Naya Power mission and governance.
- Existing `SmartFeedBoard` architecture.
- Recovered Hub visual language.
- Human/Naya/machine intelligence separation and trust/provenance surfaces.
- One exceptional board as the quality benchmark before propagation.

## WHAT IS BLOCKING US?
Actual production/runtime evidence has not yet been re-established for this latest source head.

## WHAT MATTERS NOW?
Prove the restored Hub and feed in the actual Assistant-authoritative Cloudflare runtime. Do not make more speculative UI changes first.

## WHAT AM I RECOMMENDING?
Run the canonical release gate against `main`, then verify the exact Assistant-authoritative Worker and `/feed` route. Check desktop, tablet, and mobile. Confirm the Hub is visibly the restored shell, the feed opens the existing SmartFeedBoard, and navigation works. If anything fails, repair only the first material divergence and rerun the complete acceptance.

## WHAT IS THE NEXT EXECUTION ACTION?
**Verify the new `main` build through the canonical Assistant Cloudflare release path and inspect the deployed Hub and `/feed` runtime before making any further UI changes.**

## WHAT DOES THE NEXT NAYA DO?
1. Inspect current `main` and release workflow state.
2. Run/inspect the canonical Assistant Cloudflare release.
3. Capture real source/build/deploy/runtime evidence.
4. Open the exact deployed Hub.
5. Verify `/` is the restored Hub and `/feed` opens the intelligent board.
6. Test sidebar navigation, search, board actions, and responsive behavior.
7. Record the result in `.naya/activity/`.
8. If PASS, create the next single continuation action. If FAIL, repair only the first material divergence.

## WHAT IS PASS?
No PASS without returned evidence for source contract, typecheck, build, deployment, exact runtime identity, visual acceptance, interaction acceptance, and consequence verification.

# 509 Legacy Feed Cleanup — Surgical Execution Record

Date: 2026-09-10
Target: `2026 09 09 5:09 pm NayaNET HUB.html`

## Problem found

The actual 509 source still contained multiple historical Intelligent Feed layers and, critically, still loaded `./nayanet-intelligent-feed-v6.js`. That legacy runtime could recreate the old feed after the V2 renderer was installed. The source also retained the old home-feed DOM rather than making V2 the sole feed surface.

## Required correction

1. Remove the first legacy board set.
2. Remove the second legacy board/runtime set.
3. Remove the stale code/feed DOM from the home feed.
4. Remove the legacy V6 renderer that could restore the old feed.
5. Keep one canonical V2 Intelligent Feed: three Intelligence Events, vertical sections, elevated inner boards, restrained semantic color, living depth, and functional controls.

## Execution

The 509 direct-update workflow performs a surgical reconstruction of the actual `homeFeed` section and installs exactly one V2 renderer. It also removes the known legacy feed runtime/style layers before installation.

## Diagnostic evidence

The first cleanup CI run reached the cleanup step but failed before changing the source because the regex matcher was over-escaped (`\\s` instead of `\s`). That was read from the exact job log. No source commit was claimed from that run.

The workflow has now been corrected to use the actual regex whitespace matcher. This activity record is being changed once to trigger the corrected workflow; this is a diagnostic correction, not a blind rerun.

## Verification gates

The corrected workflow verifies:

- exactly one V2 renderer marker
- V1 renderer absent
- legacy V6 feed script absent
- legacy feed mirror/excellence runtime absent
- all canonical Intelligence Event titles present
- all required vertical intelligence sections present
- Create Space, Save to Smart List, Share Intel, and rating controls present
- `git diff --check` passes

The intended source end state is **V2 only inside the 509 home feed**: no first legacy boards, no second legacy boards, no stale code block, and no legacy V6 renderer capable of rebuilding them.

## Materialization gate trigger

A single controlled activity-file update is being used to trigger the canonical mainline materialization path. This line is a trigger record only; completion is not claimed until the exact 5:09 Hub file changes on `main` and passes its target verification gates.

## Bound materializer trigger

The materializer is now bound to the confirmed mainline Naya 16 activity gate so source changes, artifact materialization, target verification, and the resulting target commit occur in one observable chain. This is still a trigger record, not a completion claim.

## Deterministic artifact gate trigger

The mainline E00 activity gate now owns the 509 artifact materialization as a separate job with exact target verification and a write-only-if-changed rule. This trigger exists solely to exercise that deterministic chain; completion remains unclaimed until the exact Hub file on `main` changes and is independently verified.

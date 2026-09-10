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

The 509 direct-update workflow now performs a surgical reconstruction of the actual `homeFeed` section and installs exactly one V2 renderer. It also removes the known legacy feed runtime/style layers before installation.

## Verification gates

The workflow verifies:

- exactly one V2 renderer marker
- V1 renderer absent
- legacy V6 feed script absent
- legacy feed mirror/excellence runtime absent
- all canonical Intelligence Event titles present
- all required vertical intelligence sections present
- Create Space, Save to Smart List, Share Intel, and rating controls present
- `git diff --check` passes

This record is intentionally the trigger for the cleanup workflow so the source transformation is executed by CI rather than described as completed before the resulting HTML commit exists.

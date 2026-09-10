# Smart Note — 509 Exact Hub Materialization Disconnect

**Date:** 2026-09-10  
**System:** NayaNET / NayaPOWER  
**Target:** `2026 09 09 5:09 pm NayaNET HUB.html`  
**Status:** RESOLVED

## Problem

The 509 Intelligent Feed source renderer was being updated, but the exact artifact that mattered — `2026 09 09 5:09 pm NayaNET HUB.html` on `main` — was not changing for an extended period.

GitHub Actions were running, creating a false sense of progress, while the actual target remained stale. Work stalled because source progress and artifact progress were not coupled by a hard release gate.

## Root Cause

There were multiple materialization paths and verification gates that were not all bound to the exact target artifact.

**Source intent is not artifact truth. A green Action is not release proof.**

The authoritative chain is:

`canonical source → materializer runs on that source → exact target file changes → target content is independently verified → target blob SHA changes → only then declare success`

A workflow that runs without changing the exact target is not successful materialization.

## Solution

The 509 materialization path was made deterministic and surgical:

1. Check out the canonical source.
2. Read `scripts/nayanet-509-intelligent-feed-v2.js` as the renderer source of truth.
3. Preserve the approved Hub shell/sidebar/topbar/home structure.
4. Remove known legacy 509 feed/runtime layers.
5. Replace only the actual `<section class="homeFeed">` mount.
6. Inject exactly one `NAYANET_509_INTELLIGENT_FEED_DIRECT_V2` renderer.
7. Verify the exact target contains `COLLECTIVE INTELLIGENCE`, `PERSONAL INTELLIGENCE`, `ACTIVITY FEED`, and the required edge-to-edge geometry.
8. Verify known legacy feed markers/runtime are absent.
9. Commit **only** the exact 5:09 Hub target when it actually changes.
10. Verify the resulting `main` target blob, not merely workflow status.

The successful artifact commit was:

`a0b8dcf0c0bfa7b75982d35d08c177fe375a90d8`

The exact target blob became:

`d0faad3be4048b0b852cb2ba3cb73365bd70da9f`

The GitHub compare confirmed the exact 5:09 Hub file was modified by the materialization commit and that the canonical 509 renderer was inserted into the target.

## Verification

Success is evidenced by repository state:

- `main` advanced to `a0b8dcf0c0bfa7b75982d35d08c177fe375a90d8`.
- Commit message: `fix(509): materialize canonical Intelligent Feed into Hub`.
- The exact target file was modified.
- Target blob SHA: `d0faad3be4048b0b852cb2ba3cb73365bd70da9f`.
- The inserted renderer is `NAYANET_509_INTELLIGENT_FEED_DIRECT_V2`.
- The renderer contains the canonical 509 V7 feed and edge-to-edge geometry.

## Future Rule

For every consequential NayaNET artifact change:

**NEVER declare completion from source state, workflow state, PR state, or a green Action alone.**

The release gate must prove:

`SOURCE → BUILD/MATERIALIZE → EXACT TARGET → TARGET CONTENT CHECK → TARGET BLOB SHA CHANGE → PUBLIC RUNTIME CHECK when applicable`

If the exact target blob does not change, the work is **not done**, regardless of how many Actions pass.

When a materialization path fails, stop adding parallel workflows. Inspect the exact failing gate, fix the single canonical path, rerun it, and verify the artifact directly.

This is the permanent NayaNET rule for preventing another source/artifact disconnect.

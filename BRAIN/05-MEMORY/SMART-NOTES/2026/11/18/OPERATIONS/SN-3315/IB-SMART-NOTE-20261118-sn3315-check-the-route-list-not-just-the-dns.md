# Check the Route List, Not Just the DNS

SN-3315 · OPERATIONS — ROUTES AND DNS

**Filed:** Intelligence Loop filing push #3 2026-11-18 — numbering confirmed by `next-sn-number.py` (exit 0) immediately before filing: next free SN-3313; filed as SN-3315 renumbered from provisional SN-3286.

**Created:** 2026-11-18 03:52Z (Shawn asked "what do you figure it is? How do you fix it?" — captain's diagnosis + fix, verified by fresh fetch; recorded in the daily log; drafted in run 294)

**Paired Naya Note:** NN-20261118-check-the-route-list-not-just-the-dns

## Hook

The page was never broken — /agreement is 200 on workers.dev, and the DNS resolves. The route list had no route for agreement*, enter*, or agmt-* — so those paths fell through to the origin and timed out with a 522. Six surgical routes fixed it, verified by fresh fetch. DNS resolving is not the same as the path being routed.

## Nutshell

Shawn, 2026-11-18 03:52Z, his question: "what do you figure it is? How do you fix it?" **THE DIAGNOSIS, PROVEN:** his checks were right — Namecheap nayanet.app ACTIVE (Nov 1 2025–Nov 2 2027), nameservers aldo.ns.cloudflare.com + princess.ns.cloudflare.com; Cloudflare zone nayanet.app shows traffic (659 unique visitors, 4.19k requests, 4 GB, 16–17 Nov) and Connected Workers. No issue in either dashboard. **THE PROBLEM:** the page was never broken — /agreement is 200 on workers.dev. On nayanet.app the ROUTE LIST (API read, zone 9427e0dc…) has NO route for agreement*, enter*, or agmt-*. The nayanet worker only gets the exact root + identity.html* + manifest.webmanifest + icon-192/512.png. So /agreement, /enter, /agmt-b05.jpg matched no route, fell through to the origin (proxied A records = Cloudflare's own IPs) and timed out: 522, 16 B, twice + www. Working paths were exactly the routed ones: / (200, 1,146,242 B, sha 2e74273b exact), /hub (200, 4,694,134 B, sha 6163d8e5 exact), /identity.html (200, 307,759 B old build), /welcome (200, 97,807 B), /feed-live.json (200, 6,743,521 B — still the stale feed, max sn2832). No custom domain for nayanet.app on any worker — the dashboard's "nayanet → nayanet.app" entry is the exact-root route. **THE FIX (DONE 03:52Z, via cf-api.py):** 6 new routes → nayanet worker: nayanet.app/agreement* (e28d7faf), nayanet.app/enter* (ea330fa2), nayanet.app/agmt-* (fa237199), www.nayanet.app/agreement* (7f11e9e4), www.nayanet.app/enter* (d58bc714), www.nayanet.app/agmt-* (a8914761). All success:true. Surgical patterns only (no overlap with any existing route — checked against the full list). **VERIFIED BY FRESH FETCH AFTER 10s:** /agreement 200, 88,277 B, sha 14bd698c… (EXACT match to the worker); /enter 200, 1,774 B; /agmt-b05.jpg 200, 452,655 B image/jpeg; www /agreement 200, 88,277 B; www /agmt-b05.jpg 200, 452,655 B; / still 200, 1,146,242 B; /hub still 200, 4,694,134 B (untouched). **THE CORRECTION TO THE RECORD:** the token CAN create zone routes — the go-live coordinator's "lacks Zone Workers Routes Write" claim is disproven (6 created). The 03:03Z route creation evidently used this token too. **THE COMPANION INCIDENT:** SN-3316 carries Resolve's serving incident — the apex+www AAAA records that vanished (last good 02:55Z, first NXDOMAIN 03:25Z) and were restored to the verified 2026-11-03 four-record state. The 03:43Z correction stands with this note: before the route fix the domain DID resolve and the routed paths served the exact right bytes — the outage was only the unrouted paths returning 522, not a whole-site DNS outage. **STILL RUNNING:** the live flow test (browser-task 20737fe7, dispatched 03:43Z) — it will walk the fixed paths and report. No verdict yet; the flow is not passed until it reports. The stale feed (sn2832) is a separate track (publication repair).

## Human

A site can be up and down at the same time — up at the root, down at the agreement — and the cause is not the page and not the DNS. The page was fine: /agreement answered 200 on the worker address all along. The DNS was fine: the domain resolved, the records were there. What was missing was the middle step — the route list, the table that says which worker answers which path. The nayanet worker was only handed the exact root and a few assets; /agreement, /enter, and the agreement images matched no route at all, so they fell through to the origin and timed out with a 522. The fix was six surgical routes, each a single pattern, each checked against the full list so nothing overlaps — and then a fresh fetch of every fixed path, byte for byte, against the worker's own hash. That last step is the whole lesson: the claim is not "routes added" but "the live path serves the exact bytes." And the record gets corrected, not quietly: the token can create zone routes after all — the earlier claim that it could not is disproven by the six it just created. When a path 522s while the root 200s, check the route list. DNS resolving is not the same as the path being routed.

## Child

Imagine a house with lots of doors, but the map only shows the front door. The agreement door exists and works fine — but nobody wrote it on the map, so visitors can't find it and get lost. Shawn asked: what is it, and how do you fix it? The answer: write the missing doors on the map — six little lines, one for each door. Then check by walking through each door yourself to make sure it opens. Having the address right is not the same as having every door on the map.

## Grandma

Dear, the page was never broken, dear — the agreement page worked all along, dear. The problem was the map, dear: it listed the front door but not the agreement door, dear, so visitors got lost trying to reach it. The fix was simple, dear — write the six missing doors on the map, one line each, dear — and then walk through every door yourself to make sure it opens, dear. Having the address right is not the same as having every door on the map, dear.

## Naya

THE PAGE WAS NEVER BROKEN. THE ROUTE LIST WAS MISSING THE PATHS. SIX SURGICAL ROUTES. VERIFIED BY FRESH FETCH, BYTE FOR BYTE.

## What it means

- **THE DIAGNOSIS:** /agreement 200 on workers.dev; DNS resolves; the route list had NO route for agreement*, enter*, or agmt-* — unrouted paths fell through and 522'd.
- **THE FIX:** 6 new routes → nayanet worker (agreement*, enter*, agmt-* on apex + www), all success:true, surgical patterns, no overlap.
- **THE PROOF:** fresh fetch after 10s — /agreement 200, 88,277 B, sha 14bd698c exact; /enter 200; /agmt-b05.jpg 200 image; www the same; / and /hub untouched.
- **THE CORRECTION:** the token CAN create zone routes — the go-live coordinator's "lacks Zone Workers Routes Write" claim is disproven.
- **THE RULE:** when a path 522s while the root 200s, check the route list — DNS resolving is not the same as the path being routed. Verify by fresh fetch, never a PUT etag.
- **STILL OPEN:** the live flow test (browser-task 20737fe7) has no verdict yet; the stale feed (sn2832) is a separate track.

## Why it matters

Without this note, the next outage gets diagnosed the same wrong way — "the DNS is down" or "the page is broken" — while the route list sits unchecked and the fix waits. With it, the diagnostic order is settled: page first (is it 200 on the worker?), DNS second (does it resolve?), route list third (does a route hand this path to a worker?). And the capability record is corrected: the token can create routes, so the next fix does not wait on a permission that was never missing.

## What changes now

1. /agreement, /enter, and /agmt-* serve on nayanet.app and www — verified by fresh fetch, exact bytes.
2. The diagnostic order for a 522 on one path while the root 200s is: worker, DNS, route list.
3. The token's route-creation capability is recorded as proven, not missing.
4. The live flow test still has to report before the flow is called passed.
5. Correction Compound inventory + brief-template steps are owed for this correction and recorded as owed — not claimed done.

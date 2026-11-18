# Check the Route List, Not Just the DNS

**Written by Naya for Shawn Vibert — Founder / Creator of NayaNET**

**NN-20261118-check-the-route-list-not-just-the-dns.md · Naya Note · 2026-11-18 03:52Z**

**Category:** Operations — routes and DNS

## What it is

Shawn, 2026-11-18 03:52Z, his question: "what do you figure it is? How do you fix it?"

- **THE DIAGNOSIS, PROVEN:** his checks were right — Namecheap nayanet.app ACTIVE, nameservers aldo.ns.cloudflare.com + princess.ns.cloudflare.com; Cloudflare zone shows traffic and Connected Workers. No issue in either dashboard. The page was never broken — /agreement is 200 on workers.dev.
- **THE PROBLEM:** on nayanet.app the ROUTE LIST had NO route for agreement*, enter*, or agmt-*. The nayanet worker only got the exact root + identity.html* + manifest + icons. So /agreement, /enter, /agmt-b05.jpg matched no route, fell through to the origin and timed out: 522. Working paths were exactly the routed ones.
- **THE FIX (DONE 03:52Z):** 6 new routes → nayanet worker: nayanet.app/agreement*, nayanet.app/enter*, nayanet.app/agmt-*, www.nayanet.app/agreement*, www.nayanet.app/enter*, www.nayanet.app/agmt-*. All success:true. Surgical patterns only, no overlap with any existing route.
- **VERIFIED BY FRESH FETCH AFTER 10s:** /agreement 200, 88,277 B, sha 14bd698c… (EXACT match to the worker); /enter 200; /agmt-b05.jpg 200 image/jpeg; www the same; / and /hub untouched.
- **THE CORRECTION:** the token CAN create zone routes — the go-live coordinator's "lacks Zone Workers Routes Write" claim is disproven (6 created).
- **STILL RUNNING:** the live flow test (browser-task 20737fe7, dispatched 03:43Z) — no verdict yet; the flow is not passed until it reports. The stale feed (sn2832) is a separate track.

## Why it matters

A site can be up and down at the same time — up at the root, down at the agreement — and the cause is neither the page nor the DNS. The missing step is the route list, the table that says which worker answers which path. The fix was six surgical routes, each checked against the full list — and then a fresh fetch of every fixed path, byte for byte, against the worker's own hash. When a path 522s while the root 200s, check the route list. DNS resolving is not the same as the path being routed.

## How to use it

The diagnostic order for a 522 on one path while the root 200s is: worker first (is it 200 on the worker?), DNS second (does it resolve?), route list third (does a route hand this path to a worker?). Verify by fresh fetch, never a PUT etag. The token's route-creation capability is recorded as proven, not missing.

**Written by Naya for Shawn Vibert — Founder / Creator of NayaNET.**

*Paired Smart Note: SN-3315 — Check the Route List, Not Just the DNS*

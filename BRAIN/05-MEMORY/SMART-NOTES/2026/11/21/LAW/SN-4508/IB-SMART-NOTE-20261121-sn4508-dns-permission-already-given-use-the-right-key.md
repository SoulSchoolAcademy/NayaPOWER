# SN-4508 — DNS Permission — Already Given, Use the Right Key

**Category:** LAW — check the keys you already hold before saying a permission is missing; subdomains are automatic now — worker + route + DNS in one round — 2026-11-21 ~10:43 MST

*Paired Naya Note: NN-20261121-dns-permission-already-given-use-the-right-key — the verbatim record of the standing order and the finding from the joinus round.*

**Filed:** SN-4508 — Intelligence Loop run 469, 2026-11-21. His standing order and the finding from the joinus round, as recorded in MEMORY.md; joinus.nayanet.app verified live first-hand. Correction Compound runs with this note: inventory + brief-template + PI + GitHub, same pass.

## In a Nutshell

Shawn ordered the machine to have DNS permission forevermore. The answer: he ALREADY gave it on 2026-11-04 — the second key (`custom.cloudflare-dns`, Zone DNS Edit) is live; a read just now returned the zone's 5 records, and the joinus round had simply used the wrong key (the workers token, which 403s on DNS). Record created via the DNS key: `joinus.nayanet.app` A `192.0.2.1`, proxied, id `46e4f76b…`. Verified live first-hand: https://joinus.nayanet.app/ → HTTP 200, 281,134 B, sha256 `1a0115a4…` exact; /testuser → HTTP 200, 281,297 B (username injection). Subdomains are now automatic — worker + route + DNS in one round, no more waiting on his hand.

## The Lesson

**DNS PERMISSION — ALREADY GIVEN, USE THE RIGHT KEY (his standing order, 2026-11-21 ~10:43 MST):**

**THE BLOCKER WAS NEVER MISSING PERMISSION — IT WAS THE WRONG KEY.** The joinus round stopped and reported that the DNS record needed his hand because the token it used had no DNS scope — GET/POST dns_records → 403. The permission was given on 2026-11-04 and sat live the whole time: the second key (`custom.cloudflare-dns`, Zone DNS Edit) returned the zone's 5 records on the first read. The round asked for a permission it already held. Before reporting a permission as missing, check the keys you already hold.

**USE THE RIGHT KEY FOR THE JOB.** The workers token does workers; the DNS key does DNS. A 403 on one scope is not proof the permission doesn't exist — it is proof the wrong key is being used. The fix was one line: use the DNS key for the DNS write. The record (`joinus.nayanet.app` A `192.0.2.1`, proxied) was created through it and verified live first-hand at the root and at /testuser.

**SUBDOMAINS ARE AUTOMATIC NOW — WORKER + ROUTE + DNS IN ONE ROUND.** No more waiting on his hand for a DNS record. A subdomain round does all three together: the worker, the route, and the DNS record. The joinus pattern (`joinus.nayanet.app/<username>`) is live for every citizen because the whole chain was done in one round — and the next subdomain round does the same, without stopping to ask for a permission that was given on 2026-11-04.

**A MISSING DOC IS A REAL GAP.** The DNS connector doc is missing — only `bin/cf-dns-api` exists on disk. The next seat has to find the key by luck instead of by doc. Worth re-authoring so the next seat finds it: the doc is the map to the key, and the key is the permission.

## Why It Matters

A round that stops for a permission it already holds wastes the one thing the machine cannot get back: his attention, and the hours while the work sits. The joinus DNS sat NXDOMAIN while the key sat live — the gap was not permission, it was knowing. The lesson is mechanical: check the keys you already hold before you report one missing, use the right key for the job, and do the whole chain (worker + route + DNS) in one round so a subdomain never waits on a hand again.

## How to Use It

When a DNS write 403s, check the keys already held (`custom.cloudflare-dns`, Zone DNS Edit) before reporting a missing permission; use the DNS key for DNS and the workers token for workers. Every subdomain round does worker + route + DNS together, in one round. Re-author the DNS connector doc so the next seat finds it (`bin/cf-dns-api` exists on disk; the doc is missing).

## His Order, As Recorded

> "Shawn ordered the machine to have DNS permission forevermore."

— as recorded in MEMORY.md, 2026-11-21 ~10:43 MST. The answer he already gave on 2026-11-04: the second key (`custom.cloudflare-dns`, Zone DNS Edit) is live.

## Owed from This Dictation

- JOINUS LIVE, VERIFIED FIRST-HAND (~10:43 MST): `joinus.nayanet.app` A `192.0.2.1`, proxied, id `46e4f76b…`; https://joinus.nayanet.app/ → HTTP 200, 281,134 B, sha256 `1a0115a4…` exact; /testuser → HTTP 200, 281,297 B (username injection). The invite-link pattern (`joinus.nayanet.app/<username>`, SN-4500) is live.
- The DNS connector doc is missing (only `bin/cf-dns-api` on disk) — worth re-authoring so the next seat finds the key. Open, not a fail.
- The Sequence note (SN-4509) carries his order for what comes next: Personal first, then Hub + the main universal page live, then prove all working together as one in Supabase.

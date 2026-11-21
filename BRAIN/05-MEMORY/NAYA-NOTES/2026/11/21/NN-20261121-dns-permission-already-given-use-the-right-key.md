# NN-20261121-dns-permission-already-given-use-the-right-key

**Written by Naya for Shawn — Founder / Creator of NayaNET**

**NN-20261121-dns-permission-already-given-use-the-right-key · Naya Note · 2026-11-21 ~10:43 MST**

*Paired Smart Note: SN-pending — DNS Permission — Already Given, Use the Right Key (takes the next free number at filing)*

**Category:** LAW — check the keys you already hold before saying a permission is missing; subdomains are automatic now — worker + route + DNS in one round

**Status:** Written in run 469. His standing order and the finding from the joinus round, as recorded in MEMORY.md — joinus.nayanet.app verified live first-hand.

## What it is

**JOINUS DNS — LIVE (2026-11-21 ~10:43 MST):** Shawn ordered the machine to have DNS permission forevermore. The answer: he ALREADY gave it on 2026-11-04 — the second key (`custom.cloudflare-dns`, Zone DNS Edit) is live; a read just now returned the zone's 5 records, and the joinus round had simply used the wrong key (the workers token, which 403s on DNS). Record created via the DNS key: `joinus.nayanet.app` A `192.0.2.1`, proxied, id `46e4f76b…`. VERIFIED LIVE first-hand: https://joinus.nayanet.app/ → HTTP 200, 281,134 B, sha256 `1a0115a4…` exact; /testuser → HTTP 200, 281,297 B (username injection). Subdomains are now automatic — worker + route + DNS in one round, no more waiting on his hand. The DNS connector doc is missing (only `bin/cf-dns-api` on disk) — worth re-authoring so the next seat finds it.

## Why it matters

The blocker was never missing permission — it was using the wrong key. The permission was given on 2026-11-04 and sat live while a round stopped and reported it as needing his hand. Check the keys you already hold before saying a permission is missing. And now subdomains are automatic: worker + route + DNS in one round, no more waiting on his hand — the joinus pattern (`joinus.nayanet.app/<username>`) is live for every citizen, verified first-hand at the root and at /testuser.

## How to use it

When a DNS write 403s, check the keys already held (`custom.cloudflare-dns`, Zone DNS Edit) before reporting a missing permission; use the DNS key for DNS and the workers token for workers. Every subdomain round does worker + route + DNS together, in one round. Re-author the DNS connector doc so the next seat finds it (`bin/cf-dns-api` exists on disk; the doc is missing).

---

**Written by Naya for Shawn — Founder / Creator of NayaNET.**

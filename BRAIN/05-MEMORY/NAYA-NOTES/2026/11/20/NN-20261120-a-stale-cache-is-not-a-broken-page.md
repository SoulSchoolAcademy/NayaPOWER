# NN-20261120-a-stale-cache-is-not-a-broken-page

**Written by Naya for Shawn — Founder / Creator of NayaNET**

**NN-20261120-a-stale-cache-is-not-a-broken-page · Naya Note · 2026-11-20 ~18:34 MST**

*Paired Smart Note: SN-pending — A Stale Cache Is Not a Broken Page (takes the next free number at filing)*

**Category:** Law — how a "broken" page is checked

**Status:** Filed in run 437. His words on call dfe2008f, recorded in the daily log 2026-11-20.

## What it is

**PORTAL ITSELF IS RIGHT ON THIS BROWSER.** https://nayanet.app/ = 1,146,232 B, sha 9ba535c7 (re-verified fresh). The other browser not going there was a stale cached copy, his words: "Oh, now it does. So just on the other browser it didn't. Weird."

**OLD CERTIFICATE — CONFIRMED LIVE.** Live https://nayanet.app/identity.html = 307,759 B, sha bdd8af83, certificate 12x. Staged fixed identity = 380,286 B, sha 9c9cc86c, certificate 27x (proof-host, ref walkthrough-frontend-20261118, cb 0f4c4c28). Live is the old one, staged is the newer one — not live yet.

**OWED, per his ~17:06 MST order.** The NEW certificate page goes into the walkthrough, he confirms the certificate page is solid and good first, then audio per page once all walkthrough pages are good. Portal hooking to the real walkthrough (with updated agreement wording) is still owed behind Personal-first.

## Why it matters

A page that loads on one browser and not on another is a cache question before it is a page question. The check that tells them apart takes one fresh fetch.

## How to use it

Fresh fetch on both browsers, compare bytes and sha, hard refresh the failing one. Only when the fresh bytes differ from the good build does the page get a round.

---

**Written by Naya for Shawn — Founder / Creator of NayaNET.**

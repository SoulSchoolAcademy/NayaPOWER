# SN-4395 — A Stale Cache Is Not a Broken Page

**Category:** LAW — how a "broken" page is checked; 2026-11-20 ~18:34 MST

*Paired Naya Note: NN-20261120-a-stale-cache-is-not-a-broken-page — the verbatim record of his words.*

**Filed:** SN-4395 — Intelligence Loop run 437, 2026-11-20. His words on call dfe2008f, recorded in the daily log 2026-11-20. Correction Compound runs with this note: inventory + brief-template + PI + GitHub, same pass.

## In a Nutshell

The other browser not going to the portal was a stale cached copy — not a broken page. Check the cache before declaring the page broken.

## The Lesson

The portal itself is right on this browser: https://nayanet.app/ = 1,146,232 B, sha 9ba535c7, re-verified fresh. The other browser not going there was a stale cached copy, his words: "Oh, now it does. So just on the other browser it didn't. Weird." A page that loads on one browser and not on another is a cache question before it is a page question — hard refresh, fresh fetch, bytes and sha, then judge. The same turn confirmed the old certificate live: https://nayanet.app/identity.html = 307,759 B, sha bdd8af83, certificate 12x. The staged fixed identity = 380,286 B, sha 9c9cc86c, certificate 27x — live is the old one, staged is the newer one, not live yet. Owed, per his ~17:06 MST order: the NEW certificate page goes into the walkthrough, he confirms the certificate page is solid and good first, then audio per page once all walkthrough pages are good. Portal hooking to the real walkthrough, with updated agreement wording, is still owed behind Personal-first. Two different "not working" reports, two different truths: one was a stale cache, the other is a live page that is genuinely the older build. The check that tells them apart takes one fresh fetch.

## Why It Matters

Declaring a working page broken sends a round to fix a page that was never broken — and the round's "fix" can break the page that was working. The cache is the cheapest suspect and the first one to clear. Every "it doesn't work on my other browser" gets a fresh fetch before it gets a round.

## How to Use It

When a page fails on one browser and works on another: fresh fetch on both, compare bytes and sha, hard refresh the failing one. Only when the fresh bytes differ from the good build does the page get a round. Record which browser, which bytes, which sha — never "it doesn't work" without the numbers.

## His Order, As Recorded

> "Oh, now it does. So just on the other browser it didn't. Weird."

## Owed from This Dictation

- The new certificate page goes into the walkthrough; he confirms the certificate is solid first, then audio per page; portal hooking to the real walkthrough still owed behind Personal-first.

# Stale-State Claims Die on Live Bytes — Lane Contradiction Resolution

**Intelligent Block:** IB-SMART-NOTE-20261005-sn0398-stale-state-claims-die-on-live-bytes
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-05
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 comment 6004487150 (2026-10-05, [NAYA 2] Fact-check on the "17 Cloudflare workers still contaminating" claim) correcting the claim in #1354 comment 6004249509 (2026-10-05, superbrain sweep sign-out: "17 external Cloudflare Workers Git lanes still contaminating repository check surfaces"); prior state: Shawn deleted all 17 workers himself (#1354 comment 6003165089).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Two lanes held opposite claims about the same external state: Naya 3's sweep sign-out reported "17 external Cloudflare Workers Git lanes still contaminating repository check surfaces," while Shawn had already deleted all 17 workers himself. Naya 2 resolved it the only way that works in multi-lane work — she re-measured *right then*: 30 check runs on main tip `a3ce52dc7`, **0** Cloudflare/Workers entries, and stated it plainly on the board: "The claim appears to be based on stale state. The CI surface is clean." The lesson for a cold successor: claims about external state decay between runs. A claim carried from an earlier sweep is stale evidence, no matter how carefully it was measured when it was true. When lanes disagree, the resolution instrument is a live-byte measurement in the current run, stated on the board — and the corrected lane's claim dies there, publicly, so it is never carried forward again. This is the coordination twin of SN-0388 (prove the currency of what you claim about deployed things): SN-0388 is about *answering a question* honestly; this one is about *settling a disagreement* honestly.

## 🩷 HUMAN NOTE

Shawn — banking one coordination rule from today's lanes: when two of us say opposite things about the outside world, nobody argues from memory — we re-measure on live bytes right then and post the result. That's how the "17 workers still contaminating" claim died: Naya 2 checked the current CI surface (zero Workers checks) and corrected it on the board. Stale-state claims get one correction, publicly, and they're done.

## 🟣 CHILD NOTE

Two friends disagreed about whether the toys were still in the yard. Instead of arguing, one of them went outside and looked — the yard was empty. Rule: when we disagree about what's true *right now*, we go check *right now*. Yesterday's facts don't settle today's arguments.

## 👵 GRANDMA NOTE

Two helpers gave opposite reports about whether something was still a problem. Rather than debate it, one of them went and looked at the thing itself, right that minute — and it was already fixed. The lesson: when reports disagree, check the real thing at that moment and say so out loud, so the old, outdated report isn't repeated again.

## 🤖 NAYA NOTE

In multi-lane work I must treat any carried claim about external state as perishable. The moment another lane (or I) disputes it, I don't defend the claim — I re-verify on live bytes and post the fresh measurement. Correcting a stale claim on the board isn't a criticism of the lane that made it; it's how the board stays current. SN-0388 taught me to prove currency when answering; this teaches me to prove currency when disagreeing.

## ⚙ MACHINE NOTE

```json
{
  "sn_id": "SN-0398",
  "truth_state": "CANDIDATE",
  "captured": "2026-10-05",
  "rule": "Claims about external state are perishable. On lane disagreement: re-verify on live bytes in the current run, post the fresh measurement on the board, and retire the stale claim publicly.",
  "cousins": ["SN-0388", "SN-0341"],
  "evidence": {
    "disputed_claim": "#1354 comment 6004249509 (2026-10-05): '17 external Cloudflare Workers Git lanes still contaminating repository check surfaces'",
    "resolution": "#1354 comment 6004487150 (2026-10-05): live-verified on main tip a3ce52dc7 — 30 check runs, 0 Cloudflare/Workers entries. 'The claim appears to be based on stale state.'",
    "context": "#1354 comment 6003165089: Shawn deleted all 17 stale workers himself — the claim predated the cleanup"
  }
}
```

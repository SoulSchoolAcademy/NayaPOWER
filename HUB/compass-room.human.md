# The Compass Room — Naya Compass, in plain words

**Status:** DESIGN PROOF — a spec plus a static mock page. Not a shipped product, not live.
**Home:** the Hub. Compass is a room *inside* the existing Hub chassis — a socket panel, not a new app and not a second shell.
**Shipping contract:** issue #2436 (Naya Compass — full product demo, evidence-first engine, ten-step shipping contract). This file covers that issue's Action 8: one Compass room in the Hub.

## What it is

Naya Compass is the buyer-facing product: a trustworthy personal and professional decision guide. You tell Naya where you want to go. She helps you understand your choices, decide wisely, take the next step — and learn from the journey.

**The product promise:** "Find your direction. Understand why. Take the next step. Learn from the journey."

## The journey — six screens, one room

1. **Intent.** You say where you want to go, in plain words or voice: your goal, what's in scope, who it's for, your constraints, your deadline. Naya asks ONE material clarification — never a twenty-question form.
2. **Reality & Evidence.** Every fact carries a truth label — OBSERVED, VERIFIED, CLAIM, UNKNOWN, STALE, or CONFLICTED — with its source, owner, revision, and expiry. Tap any recommendation and you see exactly where it came from.
3. **Choices.** Real options with the facts behind them — plus NO_OP (do nothing, on purpose), READ_MORE (gather evidence first), and ASK (ask a human). Nobody types in scores; the math comes from evidence, not opinions.
4. **Recommendation.** One strongest route, with WHY, the runner-up, the confidence bounds, and what would change its mind. Where two options overlap in uncertainty, Naya says so — she never invents a winner.
5. **Navigate.** Reversible steps and checklists. Anything consequential re-checks law, rights, consent, capability, and authority fresh — and you hold the final say on anything that matters.
6. **Experience.** The forecast is frozen *before* you act. Then the observation window opens, the result is independently observed, and the learning is calibrated. A self-report is never counted as verified learning.

## The honest rule

Every fact you see carries one of six truth labels. Unknowns are shown as unknown. Stale facts never quietly become "yes". A high score never creates permission on its own. If Naya doesn't know, she says so — and offers READ_MORE or ASK instead of guessing.

## The first pilot is read-only

The first pilot watches and explains; it takes no action on your behalf. No merges, no deploys, no writes to your systems. The Engineering journey shows exactly this: a pull request that *looks* ready still gets READ_MORE / ASK until its head, its checks, its law evidence, and human authority are all proven. An invented high score must never create merge permission.

## Demo truth is synthetic and stays labelled

The mock page (`HUB/compass-room-mock.html`) is design proof only. Every sample value is marked, the page carries a persistent "MOCK — SAMPLE DATA, NOT LIVE" ribbon, and nothing on it calls a live service or writes anywhere. Synthetic stays synthetic.

## Evidence

- Shipping contract: https://github.com/SoulSchoolAcademy/NayaPOWER/issues/2436
- Sibling surface whose conventions this room converges on: PR #2413 (Hub learning-lifecycle surface spec) — ribbon text, data-mock attribute, expandable four-layer pattern, palette
- This room's four files, on branch `naya2/product-compass-room-wave27` under `HUB/`: `compass-room.human.md`, `compass-room.ai.md`, `compass-room.machine.json`, `compass-room-mock.html`
- Design basis: live main tip, re-resolved at author time — the anchored tip is recorded in the wave-27 builder receipt
- No-duplicate-mechanisms survey at author time: zero Compass/room/socket open PRs, zero Compass files in `HUB/` at the anchored tip, no racing claim on the coordination board's newest comments

# The Authorization Window Race — a SHA-Pinned Human Deploy Authorization Is Voided by Any Main Movement

**Intelligent Block:** IB-SMART-NOTE-20261005-sn0415-authorization-window-race
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-05
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Team board #1354, 2026-10-05 ~17:53–17:56 PDT (2026-10-06T00:53–00:56Z) — comments 6006927890, 6006982594, 6006987909; run 37396162610.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Twice in one hour, a Human Director `DEPLOY` authorization became void between being spoken and being consumed, because `main` moved during the authorization window:

1. Authorization for `1eddeba7a45083323a72069a0aad96c221adb8d3` was consumed by run 37396162610, which correctly failed closed: main had moved to `d282d30a6c1d6baccaf6b9b2cb9675e10ea69cdf` mid-window (comment 6006927890). Current main re-observed at `a10d3b820eebe83ff1d424494f38ffe8162bdab3`.
2. Shawn then authorized `DEPLOY a10d3b820eebe83ff1d424494f38ffe8162bdab3` (comment 6006982594 — main independently rechecked and matching before the dispatch attempt).
3. Before the governed workflow accepted the dispatch, main moved AGAIN to `0dde56689cba4b6c8500dec20a723c8bc0efd29f` — PR #1570 merged mid-window. The seat posted an immediate correction (comment 6006987909): the authorization for `a10d3b82` must NOT be reused for `0dde5668`; production remained UNDEPLOYED.

The durable rule: **a human deploy authorization binds to the exact SHA, never to "current main."** If main moves at any point between authorization and dispatch acceptance, the authorization is void and must be re-requested for the new exact SHA. Three operating consequences:

- **HOLD MAIN must precede the authorization request, not follow it.** Asking for a SHA's deploy authorization while unrelated merges are free to land turns the authorization into a lottery ticket. The freeze is the first step of the deploy sequence (SN-0363's atomic promotion spec assumes this), not a courtesy around it.
- **Re-verify the SHA immediately before dispatch, and treat the correction as first-class.** The prior claim ("current main was still a10d3b82") was overtaken by a concurrent merge; the seat superseded it publicly within the same minute. On a hot main, any "current" statement is a timestamp, not a fact.
- **Authorization ≠ deployment.** Comment 6006982594 records the authorization while explicitly stating the local dispatch path was blocked and making NO claim of deployment: "production remains UNDEPLOYED until an actual workflow run proves otherwise." Record the authorization; never infer the outcome.

Why this is brain-grade: SN-0405 classified hot-main *proof* races as environmental, not product defects. This note names the governance twin — the *authority* race — where the cost is not a wasted run but an authorization silently applied to a SHA nobody approved. Any future governed-deploy design must shrink the authorization→dispatch window to atomic (re-verify SHA at the moment of dispatch, dispatch accepted against the exact SHA, mismatch = fail closed) and must require the freeze before the ask. A cold Naya reading this will never reuse a stale DEPLOY for a new SHA.

## 🩷 HUMAN NOTE

Shawn — twice tonight your deploy authorization was voided by main moving between your word and the dispatch. First the `1eddeba7` authorization was consumed while main had already moved; then your `a10d3b82` authorization was overtaken by the #1570 merge before the workflow could accept it. The seat corrected the record within a minute and refused to reuse the old authorization on the new SHA — exactly right. The standing lesson for every future deploy: your authorization locks to the exact SHA, never to "whatever's current," and the main freeze has to be in place *before* you give the word, not after. Nobody merged or deployed anything tonight that wasn't authorized.

## 🟣 CHILD NOTE

Imagine the director of a play saying "curtain up on Act 2" — but while the stage manager walks to the curtain, someone swaps the whole set for Act 3. The director's order was for Act 2's set. You don't pull the curtain anyway just because an order exists. You go back and say: "The set changed — do you still want curtain up?" That's what happened with two deploy orders tonight: the code changed between the order and the action, so both orders were cancelled and new orders are needed. The rule: an order is for one exact version, and you freeze everything the moment you ask for one.

## 👵 GRANDMA NOTE

Shawn approved a delivery twice tonight, and both times the package changed before it could ship. Think of it like approving a specific letter for mailing — but while you're walking to the mailbox, someone swaps the letter. You don't mail the swapped letter just because "mail it" was said. Both times, the team stopped, checked, and reported that the approval no longer applied. The standing rule they've written down: freeze the line before asking for approval, check the exact package right before shipping, and never treat an approval as covering a changed package.

## 💜 NAYA NOTE

Note to future me: when you request or receive a human DEPLOY authorization, the authorization object is (SHA, verbatim command, timestamp) — it is never transferable to another SHA. Operating sequence for any future deploy: (1) establish HOLD MAIN *first*; (2) get the authorization for the exact frozen SHA; (3) re-verify main == SHA immediately before dispatch; (4) dispatch with the exact SHA; if the SHA differs at any check, the authorization is void — post the correction publicly, do not proceed, and ask for a fresh authorization. Also carry the twin discipline from comment 6006982594: record the authorization as a fact, never claim the deployment happened; only a completed governed workflow run is deployment evidence. Cite alongside SN-0363 (atomic promotion: pointer/validation ordering), SN-0405 (hot-main proof races are environmental), SN-0413 (fail-closed gates are the guardrail working).

## 🖥️ MACHINE NOTE

{"sn": "SN-0415", "title": "The Authorization Window Race — a SHA-Pinned Human Deploy Authorization Is Voided by Any Main Movement", "truth_state": "CANDIDATE", "scope": "PRIVATE", "captured": "2026-10-05", "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE", "taxonomy": ["SYSTEM-INTELLIGENCE", "GOVERNANCE", "PROMOTION-AUTHORITY-BINDING"], "cousins": ["SN-0363", "SN-0405", "SN-0413", "SN-0402"], "evidence": {"board_comments": ["#1354 6006927890 (deploy authorization for 1eddeba7 consumed by run 37396162610; fail-closed: main had moved to d282d30a)", "#1354 6006982594 (explicit DEPLOY authorization for exact a10d3b82; main rechecked matching; dispatch path blocked; no deployment claimed)", "#1354 6006987909 (correction: main moved to 0dde5668 via #1570 merge before dispatch accepted; a10d3b82 authorization voided; HOLD MAIN reaffirmed)"], "voided_authorizations": [{"sha": "1eddeba7a45083323a72069a0aad96c221adb8d3", "moved_to": "d282d30a6c1d6baccaf6b9b2cb9675e10ea69cdf"}, {"sha": "a10d3b820eebe83ff1d424494f38ffe8162bdab3", "moved_to": "0dde56689cba4b6c8500dec20a723c8bc0efd29f"}]}, "rule": "A human deploy authorization binds to the exact SHA, never to current main. Any main movement between authorization and dispatch acceptance voids the authorization. HOLD MAIN must precede the authorization request; re-verify the SHA immediately before dispatch; record authorizations but never infer deployment from them"}

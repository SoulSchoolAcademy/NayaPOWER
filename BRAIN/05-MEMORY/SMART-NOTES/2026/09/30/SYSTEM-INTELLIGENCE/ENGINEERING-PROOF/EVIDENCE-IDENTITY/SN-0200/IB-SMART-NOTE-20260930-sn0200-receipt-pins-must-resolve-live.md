# A Receipt Pin Must Resolve Live, or It Is Not a Receipt

**Intelligent Block:** IB-SMART-NOTE-20260930-sn0200-receipt-pins-must-resolve-live
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-02
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** `#554` 5955380295 (Naya 4, 2026-10-02 15:11:52Z) — "verdict answered" post citing the v5.1 pin as `090e6762`; `#554` 5955640475 (Naya 2 relay, 2026-10-02 15:27:36Z) — "the pin `090e6762` in your post does not resolve via the GitHub API — the verdict-answer commit is `15481922`; treat that as the receipt reference"; the relay's tone claim independently verified in the live bytes at head (`toneFor()` derives tone from the object's stable id). Mechanical side-readings in the same relay: PR #1328 `mergeable_state` `unstable` is checks pending/failing, not a build verdict; the judging seat works from the moved head (`20b13061`), not the original verdict pin.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

A commit SHA in a receipt is a pointer, not a proof — and a pointer that doesn't resolve is a broken receipt. Naya 4's verdict-answered post cited `090e6762` as the pin for the v5.1 type-floor + tone-semantics fix; Naya 2's relay lane, doing its job of live verification rather than re-scoring, found the pin does not resolve via the GitHub API and named the true SHA on the board: `15481922` ("treat that as the receipt reference"). The correction, not the original pin, is now the receipt. The lesson is a three-part pin discipline: (1) every pin in a receipt must be resolvable by the verifying lane via the API at verification time — an unresolvable pin is a defective receipt, not a disputed fact; (2) when a pin fails, the correcting lane publishes the true SHA on the board publicly, so the record heals instead of silently diverging; (3) heads move — the judging seat judges the moved head (`20b13061`), and status strings like `mergeable_state: unstable` are read mechanically (checks pending/failing ≠ verdict), never as narrative.

Why this is brain-grade and not just Git etiquette: the whole lane protocol runs on pins (sign-ins freeze them, receipts cite them, judges re-anchor to them). An unresolvable pin anywhere in that chain silently forks reality — two lanes verifying "the same" work against two different bytes. SN-058 already bans caching stale SHAs from the board; this note is the complement on the producing side: never publish a pin you have not resolved, and when you find someone else's broken pin, say the true SHA aloud on the board. Silent private correction is how phantom SHA chains form.

## 🩷 HUMAN NOTE

Shawn — small process lesson from today's Room 01 relay: a commit pin in a receipt only counts if it resolves live. Naya 4 posted a pin that didn't resolve; Naya 2's relay verified, found the true SHA, and corrected the record publicly on 554 — that's the relay lane doing its job (verify pins live, don't re-score). The brain lesson: never publish a pin you haven't resolved, and when you find a broken one, name the real SHA aloud so the record heals.

## 🟣 CHILD NOTE

If you tell your friend "look at the drawing on page 9" but page 9 is blank, your directions are broken — she can't see what you mean. You have to check the page number is right before you share it. And if someone gives YOU a wrong page number and you find the real one, you tell everyone the right number out loud, so nobody else gets lost.

## 👵 GRANDMA NOTE

One builder posted a code reference that didn't exist — a page number pointing to a blank page. Another builder checked, found the real reference, and announced the correction publicly. The lesson: always verify a reference opens before you publish it; and when you discover someone else's broken reference, say the true one aloud so the whole team shares the same record. Quiet private fixes let two different realities drift apart.

## 🤖 NAYA NOTE

Every SHA published in a receipt or sign-in must resolve via the API at publish time; an unresolvable pin is a defective receipt, not a disputed claim. When verification finds a broken pin, publish the true SHA on the board and declare it the receipt reference — never correct it silently. Judge the moved head, not the frozen pin; read `mergeable_state` mechanically (pending/failing checks ≠ verdict).

## ⚙️ MACHINE NOTE

{"sn": "SN-0200", "title": "A Receipt Pin Must Resolve Live, or It Is Not a Receipt", "truth_state": "CANDIDATE", "scope": "PRIVATE", "captured": "2026-10-02", "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE", "taxonomy": ["SYSTEM-INTELLIGENCE", "ENGINEERING-PROOF", "EVIDENCE-IDENTITY"], "extends": ["SN-0058", "SN-0198"], "evidence": {"broken_pin": "#554 5955380295 cited v5.1 pin 090e6762; #554 5955640475: 090e6762 does not resolve via GitHub API; verdict-answer commit is 15481922 — treat as receipt reference", "verified_live": "toneFor() derives tone from stable object id, verified in live bytes at head", "mechanical_reads": "PR #1328 mergeable_state unstable = checks pending/failing, not a verdict; judging seat works from moved head 20b13061"}, "rule": "publish only resolvable pins; correcting lane names the true SHA aloud on the board; judge the moved head; read status strings mechanically"}

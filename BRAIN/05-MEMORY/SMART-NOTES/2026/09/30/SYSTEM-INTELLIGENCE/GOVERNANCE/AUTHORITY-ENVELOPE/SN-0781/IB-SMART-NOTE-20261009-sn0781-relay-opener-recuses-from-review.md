# The Relay Opener Recuses From Review — One Seat Never Holds Both Hands

**Intelligent Block:** IB-SMART-NOTE-20261009-sn0781-relay-opener-recuses-from-review
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-09
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 comment 6082594170 ([NAYA 4][SELF-BUILD][SIGN-IN] — relay PR open for naya5/smart-blocks-library, 2026-10-09T14:09:13Z) + comment 6082612651 ([NAYA 4][SELF-BUILD][SIGN-OUT] — relay PR #1969 opened, 2026-10-09T14:10:17Z) — SoulSchoolAcademy.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Naya 5's PAT 403s on PR ops, so Naya 4 opened draft PR #1969 for branch `naya5/smart-blocks-library` as a relay — with exact-pin verification (head `8590e056...` == claimed pin, base = main tip `9f2e3db5` re-read with no tip move during open, tree contains `smart-blocks/`, per SN-0773 and the #1957/#1958 relay precedent). Then she drew the line the relay precedent hadn't yet drawn: **"I will not self-review my own relay."** The hand that opens the PR for another lane must not also be the eyes that validate it. Opening creates a stake — you want the relay to land smoothly, you vouched for the bytes, your name is on the receipt — and a stake compromises independence. SN-0774 says a relay confirms bytes but never decides the merge; this says the relay lane must not concentrate opener + reviewer in one seat. She recorded the bytes, deferred the decision, and routed review to a different seat.

Why this is brain-grade: relays exist to give independent eyes. But independence is not a mood — it's a structure. A seat that both opens the relay and reviews the content is grading its own handoff; the review becomes a self-approval loop with a witness present but no witness acting. The recusal rule makes independence mechanical: the opener's receipt says what the bytes are, and a seat with no stake in the relay's success says whether the content is good. One seat never holds both hands — the hand that opens, and the hand that judges.

Rule for a cold successor: **when you open a relay PR on behalf of another lane, recuse from reviewing it. Record the bytes, defer the decision, route review to an independent seat with no stake in the relay's success.** Pairs with SN-0774 (relay confirms bytes, never decides the merge) and SN-0120 (split-axis peer review — the builder names the blind spot and hands it to another lane).

## 🩷 HUMAN NOTE

Shawn — a small governance moment worth banking. Naya 5 couldn't open PRs (her credentials fail on PR ops), so Naya 4 opened draft PR #1969 for her library as a relay — verifying every byte against the claimed pin first. Then she refused to review it herself: "I will not self-review my own relay." The seat that opens another lane's PR can't also be the seat that judges it — opening creates a stake, and a stake kills independence. So the bytes are recorded, the decision deferred, and the review goes to a different seat. Rule: the hand that opens is never the hand that judges.

## 🟣 CHILD NOTE

Imagine your friend can't reach the mailbox, so you mail her letter for her. That's kind! But then you're asked to grade the letter — that wouldn't be fair, because you already helped send it and you want it to do well. The fair move: you mail the letter (that's the relay), and someone ELSE grades it (that's the review). You don't get to do both jobs. That's exactly what happened: one helper opened the PR for her friend, and then said "someone else should check my work." Mailing is not grading.

## 👵 GRANDMA NOTE

Grandma, imagine a notary who helps someone file paperwork — she checks the pages are all there and stamps them received. Then she's asked to also decide whether the paperwork is *good*. A wise notary says no: once you've helped file it, you've got a stake in it going through, and you're no longer neutral. She files it, records exactly what was filed, and hands the judgment to someone with no stake in it. The lesson: the person who carries the package can't also be the person who inspects it. Independence isn't a feeling — it's who holds which job.

## 🟣 NAYA NOTE

Mechanical rule for relay lanes: (1) open the relay PR with exact-pin verification (head == claimed pin, base == live tip, tree contains the promised content) and sign it as the relay; (2) in the same receipt, state the recusal explicitly — "I will not self-review my own relay"; (3) route review to a different seat (or the owning lane), with the review scope stated; (4) never let the opener's byte-receipt be cited as a content review — bytes-confirmation and content-review are two different seats' jobs. The opener is invested; independence needs a seat with no stake.

## ⚙️ MACHINE NOTE

{
  "schema": "smart-note-v1",
  "sn": "SN-0781",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-09",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "category": "SYSTEM-INTELLIGENCE/GOVERNANCE/AUTHORITY-ENVELOPE",
  "doctrine": "relay-opener-recuses-from-review",
  "rule": "When you open a relay PR on behalf of another lane, recuse from reviewing it. Record the bytes, defer the decision, route review to an independent seat with no stake in the relay's success.",
  "failure_mode": "opener also reviewing the relayed content; review collapses into self-approval of the relay handoff; independence theater with no independent eyes",
  "checks": [
    "relay receipt carries exact-pin verification (head, base, tree content)",
    "receipt states the recusal explicitly",
    "review is routed to a different seat or the owning lane",
    "the byte-receipt is never cited as a content review"
  ],
  "pairs_with": ["SN-0774", "SN-0773", "SN-0120"],
  "provenance": {
    "board": "#1354",
    "comment_ids": [6082594170, 6082612651],
    "author": "SoulSchoolAcademy",
    "seat": "Naya 4",
    "timestamp": "2026-10-09T14:09Z"
  }
}

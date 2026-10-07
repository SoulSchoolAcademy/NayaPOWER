# Adjudicate Convergence on Blob-SHA Proof — Close the Superseded PR Instead of Merging a No-Op

**Intelligent Block:** IB-SMART-NOTE-20260930-sn0558-adjudicate-convergence-blob-sha-proof
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-07
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 6043169677 ([NAYA 4 / SELF-BUILD LOOP][SIGN-IN + SIGN-OUT] — cycle 2026-10-07 ~17:05–17:35 UTC, 2026-10-07T17:26:36Z); owner adjudication comment 6043036944; PR #1739 (CLOSED as SUPERSEDED, unmerged); main re-pinned `f4d6ba64` (17:04Z)

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

While #1739 sat open, other lanes landed its whole payload: the merge-base `9805c61` three-way plus all-blob-SHA comparison proved the selector move byte-identical on main (`3bcc2437`, landed via #1735), the coverage test on main (`665d1b30`, via #1738/#1742), and the know.ts/roundtrip changes convergent no-ops. A merge would be conflict-free and change exactly **one test file + one registry description line** — a no-op merge. So the owning lane adjudicated #1739 **SUPERSEDED and CLOSED it unmerged** (reversible), preserving the residual payload on the branch for cherry-pick, and explicitly unblocked #1743 (comment 6043036944).

Why this is brain-grade and genuinely new: SN-0508 says stand down an *unpushed* repair when another lane heals the seam — this is the other side of that coin, for work *already on the board*: an open PR whose content converged via parallel lanes. Merging it would be harmless but pointless — it burns review, merge, and CI cycles to land what is already on main, and it muddies provenance (the PR would claim a merge for content that arrived elsewhere). The discipline: adjudicate convergence on proof — merge-base three-way + per-blob SHA equality against live main — not on "it merges clean" (clean means no conflicts, not that the content is needed). Also downstream: #1743's standing predicate "after #1739 lands" became permanently false, so the lane re-decided on the spot — rebase #1743 directly onto live main `f4d6ba64` — rather than executing the stale plan (SN-0493: a decision expires when the tip moves).

## 🩷 HUMAN NOTE

Shawn — a small governance win from today's lanes. A pull request sat open while other lanes landed every piece of it through their own work. Instead of merging it anyway (which would have landed nothing new — one test file and one registry line), the owning lane proved the convergence with exact file comparisons and closed it as superseded, keeping the leftovers on the branch for later. The standing lesson: an open PR isn't owed a merge just because it merges cleanly. If everything it does is already on main, you close it with proof, not merge it for ceremony — and when a plan's reason for existing disappears, you make a new plan on the spot.

## 🟣 CHILD NOTE

Imagine you and your friends are all building the same LEGO castle, each with your own instructions. While you were at lunch, your friends finished every piece your instructions told you to build. You come back and ask: should I still build my pieces? No — you'd just be snapping identical bricks on top of finished work. The smart thing is to compare brick by brick (is my castle piece exactly what's already there?), say "my pages are done," and save your one special brick for later.

## 👵 GRANDMA NOTE

Two cooks both prepare the same dish for the same dinner, and by serving time the kitchen already has the full dish from one of them. You don't serve the second dish on top of the first just because it was cooked — you compare the plates, confirm they're the same, and put the second one aside. Merging a pull request whose content already arrived is serving the second dish on top of the first: harmless, but pointless, and it confuses the menu.

## 🧠 NAYA NOTE

Cold successor: when parallel lanes may have converged on an open PR, run the convergence adjudication before any merge decision. (1) Merge-base three-way at the merge-base + all-blob-SHA comparison against live main — every semantic file must be byte-identical. (2) If everything semantic is on main and the residual delta is trivial, the owning lane closes the PR as SUPERSEDED (reversible, owner-adjudicated, comment recorded) — never merge a conflict-free no-op. (3) Preserve the residual payload on the branch for cherry-pick; name where it lives. (4) Then re-read every standing decision that named the closed PR as a predicate — any predicate that became permanently false forces an immediate re-decision (here: #1743's "after #1739 lands" → "rebase directly onto live main f4d6ba64"). (5) Template: sign-in/out comment 6043169677 — one cycle, one item, exact SHAs cited, adjudication and re-decision in the same pass.

## ⚙️ MACHINE NOTE

```json
{
  "sn": "SN-0558",
  "title": "Adjudicate Convergence on Blob-SHA Proof — Close the Superseded PR Instead of Merging a No-Op",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-07",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "taxonomy": ["SYSTEM-INTELLIGENCE", "GOVERNANCE", "OPERATING-DOCTRINE"],
  "cousins": ["SN-0508", "SN-0493", "SN-0440"],
  "evidence": {
    "board": ["#1354 6043169677 ([NAYA 4 / SELF-BUILD LOOP][SIGN-IN + SIGN-OUT] — cycle 2026-10-07 ~17:05–17:35 UTC, 2026-10-07T17:26:36Z)"],
    "adjudication": "#1354 comment 6043036944 (owner adjudication: #1739 SUPERSEDED, explicitly unblocks #1743)",
    "proof": "merge-base 9805c61 three-way + all-blob-SHA comparison: selector move byte-identical on main (3bcc2437 via #1735); coverage test on main (665d1b30 via #1738/#1742); know.ts/roundtrip changes convergent no-ops",
    "residual": "a merge would change exactly one test file + one registry description line; residual payload preserved on the branch for cherry-pick",
    "redecision": "#1743's 'after #1739 lands' predicate permanently false -> rebase #1743 directly onto live main f4d6ba64; main re-pinned f4d6ba64 at 17:04Z"
  },
  "doctrine": {
    "no_ceremony_merges": "an open PR is not owed a merge for being conflict-free — clean means no conflicts, not that the content is needed",
    "proof_over_assumption": "adjudicate convergence on merge-base three-way + per-blob SHA equality against live main, never on 'it probably landed'",
    "predicate_refresh": "when a standing decision's predicate becomes permanently false, re-decide on the spot (SN-0493) — never execute the stale plan",
    "provenance": "merging a converged PR muddies provenance: the PR would claim a merge for content that arrived elsewhere"
  },
  "rule": "when parallel lanes converge on an open PR, the owning lane proves convergence with merge-base + blob-SHA evidence and closes it as SUPERSEDED, preserving the residual on the branch — then immediately re-decides every plan that named the closed PR as a predicate"
}
```

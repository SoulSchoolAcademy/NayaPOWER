# Never Route IV to a Must-Move Head — Verification at a Dying Head Is Born Stale

**Intelligent Block:** IB-SMART-NOTE-20260930-sn1587-never-route-iv-to-a-must-move-head
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-18
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** L502 [F6] learning event filed 2026-10-17 ~18:08 PDT (director tick 1808: "head that must move cannot carry an IV"); carried in live-plan.md ("never route IV to a must-move head (L502)"; "#2751 HOLD fixes ... L502: never route IV to a must-move head"); feed-log 01:08Z tick ("LEARNING EVENT L502 [F6] filed (lesson, carried as next-tick candidate)")

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

An independent-verification verdict is pinned to the exact head it measured — SN-1189: a verdict is a tuple (verdict, time, tip-SHA, input-SHA). When a PR's head **must move** — a rebase is owed, fixes are pending, the base has drifted, the branch is DIRTY against a new HEAD — any IV dispatched at the current head is guaranteed to be born unbindable: the moment the head moves, the verdict's binding breaks and the full verification cycle is wasted. The live instance: PR #2751 is HELD with fixes owed and a rebase to tip `8cac435a` required; routing IV to its current head would spend a seat-cycle producing a verdict that cannot attach to the head that will actually merge. L502 [F6] names the dispatch rule: **a head that must move cannot carry an IV — so never route IV to one.** The dispatch check is one question: "is this head stable, or must it move?" If it must move, hold the IV as HELD-UNTIL-STABLE and re-route after the head stabilizes. This is the dispatcher-side mirror of the pin family: SN-1076 (author re-pins after a push), SN-1507 (re-fire at the same pinned head when the head is stable) — L502 covers the case the family left open, when the head is known-doomed *before* the work starts.

## 🩷 HUMAN NOTE

Shawn — small dispatch rule from tonight, filed as L502. When we send a seat to independently verify a PR, the verdict they produce is glued to the exact code version they checked. If that version is already scheduled to change — a rebase owed, fixes pending — their verdict dies the moment the new version lands, and the whole verification cycle was wasted. The rule: never send verification at a head that's about to move. Wait for the stable version, then verify once. PR #2751 is the live example — it's held for a rebase to the new tip, so its verification waits too. One question at dispatch time — "must this head move?" — saves a full wasted cycle every time it's asked.

## 🟣 CHILD NOTE

Imagine a teacher grading your homework while you're still erasing and rewriting the answers. She finishes, hands back the grade — but the paper she graded isn't your paper anymore. The grade is useless, and she has to grade it all over again. The rule: finish writing first, then hand it in for grading. Same with code: don't ask anyone to verify a version that you already know is going to change.

## 🔵 GRANDMA NOTE

It's like asking the home inspector to certify the house while the builders are still moving walls. He writes his report, the walls move, and the report describes a house that no longer exists — you pay for the inspection twice. The house rule the team wrote down tonight: walls finished first, inspector second. Never send the inspector to a house that's still being rebuilt.

## 🟠 NAYA NOTE

Note to future me: this is a DISPATCH rule, not a pinning rule — it fires before the work starts. Before routing any IV (dock dispatcher or lane brief): read head-stability. The head must move if any of these hold: rebase owed, fixes pending, base drifted since the branch was cut, PR marked DIRTY vs a new HEAD. If any hold → do NOT route; file the IV as HELD-UNTIL-STABLE with the named reason, and re-route after the head stabilizes. The director set the falsifier: the next 5 dock IV routings — any IV routed to a must-move head that still yields a valid (bindable) verdict falsifies this note. Cousins: SN-1189 (verdict tuples — the mechanism), SN-1076 (author-side re-pin), SN-1507 (re-fire at the same head — the correct instrument when the head IS stable), SN-1495 (staleness re-reads).

## 🟢 MACHINE NOTE

```json
{
  "sn": "SN-1587",
  "title": "Never Route IV to a Must-Move Head — Verification at a Dying Head Is Born Stale",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-18",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "taxonomy": ["SYSTEM-INTELLIGENCE", "MERGE-VERIFICATION", "VERDICT-FRESHNESS"],
  "applies_when": [["gate","iv"], ["merge","verdict"], ["dispatch","head-stability"], ["pr","rebase-owed"]],
  "enforcement": "dock IV-routing step must read head-stability (rebase owed? fixes pending? base drifted? DIRTY vs new HEAD?) before routing; hold the IV as HELD-UNTIL-STABLE when the head must move. Falsifier (live-plan carry): the next 5 dock IV routings — any IV routed to a must-move head that produces a valid verdict falsifies this note; any such routing is a process violation.",
  "cousins": [
    "SN-1189 (FM#46 — verdict is a tuple (verdict, time, tip-SHA, input-SHA); this note applies the tuple at dispatch time)",
    "SN-1076 (pin dies when the head moves — author-side re-pin; this note is the dispatcher-side mirror)",
    "SN-1507 (re-fire at the same pinned head — the correct instrument when the head IS stable)",
    "SN-1495 (not-yet-gap staleness re-read)"
  ],
  "evidence": {
    "director_tick": "shared-state.json director_tick_2026_10_17_1808 notable: 'L502 [F6] filed (head that must move cannot carry an IV)'",
    "live_plan": "live-plan.md carries: 'never route IV to a must-move head (L502)' and '#2751 HOLD fixes ... L502: never route IV to a must-move head'",
    "feed_log": "feed-log-watermark.md 01:08Z tick: 'LEARNING EVENT L502 [F6] filed (lesson, carried as next-tick candidate)'",
    "instance": "PR #2751 (Zeta): HELD with fixes owed + rebase to tip 8cac435a required; IV at current head would be born stale"
  },
  "rule": "never route independent verification to a head that must move; hold the IV as HELD-UNTIL-STABLE and re-route after the head stabilizes"
}
```

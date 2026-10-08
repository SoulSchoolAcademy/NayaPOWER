# Announce Every Ref Rewrite — Content Intact Does Not Mean Damage-Free

**Intelligent Block:** IB-SMART-NOTE-20261008-sn0689-announce-every-ref-rewrite
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-08
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 6062744226 ([NAYA 5] Learn-lane transition — nine-team structure honored, 2026-10-08T15:01:55Z)

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

During the nine-team learn-lane handoff, Naya 5 found that the `naya5/learning-lineage-receipt` ref had been rewritten onto a stale Oct-7 base **without announcement** — content intact, base regressed. She restored it to the tip and flagged it publicly "so the team watches for unattributed ref rewrites." The incident is small and the repair is the lesson: a ref rewrite that changes a branch's base is a team-visible event, never a quiet one. Content surviving does not mean no damage — a regressed base silently reopens healed seams, invalidates every exact-tip verification run against that branch, and can bury an announced repair under an older, already-fixed tree. The pattern is the exact mirror of the occupied-branch hazard (SN-0202) and the stand-down rule (SN-0508): one lane silently moving shared state forces every other lane to re-anchor or get burned.

## 🩷 HUMAN NOTE

Shawn — a small branch-hygiene lesson from today's learn-lane handoff. Someone quietly rewound a work branch onto last week's base — the content was fine, but the base was stale, which silently re-opens things we already fixed and invalidates every verification run on that branch. Naya 5 spotted it, restored the branch to the current tip, and raised the flag so everyone watches for it. New rule: rewriting a branch's base is announced — who, which branch, old base to new base, and why. No quiet rewrites on shared work. Quiet is how seams reopen.

## 🟣 CHILD NOTE

Imagine a group of kids building a tower together, and one kid quietly swaps the bottom blocks for last week's older, broken ones while nobody's watching. The top still looks fine — but the foundation is worse. That's what happened to a work branch: the base got swapped without telling anyone. The fix: put the good base back, and make a new rule — anyone who moves the bottom of a shared tower has to say so, out loud, first.

## 👵 GRANDMA NOTE

Think of it like a recipe notebook shared by a kitchen staff: the latest version has all the corrected recipes. Someone quietly swapped today's notebook for last week's copy — the pages look the same, but all the corrections are gone. The head cook caught it, put the current notebook back, and made a rule: nobody swaps the notebook without announcing it. That's the household rule for shared work now: moving a branch's base is announced — who, which branch, from which version to which, and why.

## 🧠 NAYA NOTE

Cold successor: a ref rewrite that changes a branch's base (rebase onto an older tree, force-move of a branch ref) is a **team-visible event**. The announcement names: the lane, the ref, old base → new base, and the reason. Never rewrite the base of a branch another lane may have anchored to without announcing it on the owning feed and the main board. If you discover an unattributed rewrite, follow Naya 5's pattern (6062744226): restore the ref to the correct base, verify content is intact (here it was — restore was enough), and flag it publicly so the team adds it to its watch list. Rationale: a regressed base silently invalidates every exact-tip verification (SN-0440 — one exact-tip battery is enough *only when the tip hasn't moved*) and reopens healed RED seams; the repair cost is one announcement, the incident cost is a cascade of stale work. Evidence: #1354 6062744226 — `naya5/learning-lineage-receipt` rewritten onto a stale Oct-7 base without announcement, content intact, restored to tip `027fceb0`.

## ⚙️ MACHINE NOTE

```json
{
  "sn": "SN-0689",
  "title": "Announce Every Ref Rewrite — Content Intact Does Not Mean Damage-Free",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-08",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "taxonomy": ["SYSTEM-INTELLIGENCE", "OPERATIONS", "SHARED-BRANCH-DISCIPLINE"],
  "cousins": ["SN-0508", "SN-0493", "SN-0202", "SN-0440"],
  "evidence": {
    "board": "#1354 6062744226 ([NAYA 5] Learn-lane transition — nine-team structure honored, 2026-10-08T15:01:55Z): 'the lineage-receipt ref had been rewritten onto a stale Oct-7 base without announcement — content intact, base regressed; I restored it to tip. Flagging so the team watches for unattributed ref rewrites.'",
    "ref": "naya5/learning-lineage-receipt restored to tip 027fceb0",
    "hazard": "regressed base silently reopens healed seams and invalidates every exact-tip verification run (SN-0440 one exact-tip battery is enough only while the tip hasn't moved; SN-0493 decision expires when the tip moves)"
  },
  "rule": "a ref rewrite that changes a branch's base is announced (lane, ref, old base → new base, reason) on the owning feed and the main board; on discovering an unattributed rewrite, restore the ref, verify content, and flag it publicly — content intact does not mean damage-free"
}
```

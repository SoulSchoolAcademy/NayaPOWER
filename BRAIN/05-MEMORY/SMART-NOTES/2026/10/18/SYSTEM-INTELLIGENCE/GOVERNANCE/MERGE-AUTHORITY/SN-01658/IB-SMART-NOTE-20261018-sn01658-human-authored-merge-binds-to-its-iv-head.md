# Human-Authored Merge Binds to Its IV Head

**Intelligent Block:** IB-SMART-NOTE-20261018-sn01658-human-authored-merge-binds-to-its-iv-head
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-18
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** hidden_files/shared-state.json (director_tick_2026_10_18_1108, 2026-10-18 18:08Z): L523 [F7] (board comment 6253263850) — "human-authored merge binds to its IV head (falsifier: next 5 human merges)".

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The IV-head binding does not care who clicked merge. The #2761 binding held because the merged head equaled the IV'd exact head — Epsilon's exact-head IV @19ed55f361171 (board comment 6252172116) matched the merged head, seat-authored. L523 generalizes the rule author-invariant: a human-authored merge (the director's dock click, Shawn's hand, a GitHub UI click) is lawful only when its merge_commit_sha equals the exact head the IV adjudicated. Authorship is metadata on the click; legitimacy flows from the IV's adjudication of that exact head. The binding check runs on every merge, whoever authored it.

## 🩷 HUMAN NOTE

Shawn — when you click merge yourself, the same IV rule applies as when a seat merges: the merge is only lawful if the head that actually merged is exactly the head the IV approved. The IV judged a specific commit; the merge must be that commit. Who pressed the button doesn't change what was judged. So merge-watch now checks the binding on human-authored merges too — merged head vs IV'd head, every time, author named for the record but never weighed in the verdict.

## 🟣 CHILD NOTE

Imagine a teacher approves one specific drawing for the classroom wall. Whether Dad hangs it up, or Mom hangs it up, or you hang it up — it has to be THAT drawing, the approved one. It doesn't matter whose hands put it on the wall. The rule: the thing on the wall must match the approved thing, no matter who hung it.

## 🔵 GRANDMA NOTE

It's like a prescription: the doctor approves a specific medicine at a specific dose. Whether the pharmacist hands it to you or your daughter picks it up — the bottle must contain exactly what the doctor prescribed. Who carried it home doesn't change the prescription. The check is on the bottle, never on the courier.

## 🟠 NAYA NOTE

Cold successor: the IV-head binding check in merge-watch.

1. For EVERY merge — seat-authored or human-authored — record two heads: the IV'd exact head (the head the IV verdict adjudicated, quoted from the IV comment) and the merge_commit_sha (the actual merged commit from the merge event).
2. Lawful iff merge_commit_sha == IV'd exact head. Authorship (dock click, seat merge, GitHub UI) is irrelevant to the verdict.
3. On a mismatch: flag BINDING BREAK and route to the dock/Judge for adjudication before the merge is treated as lawful. Do not downgrade to "pending" — a break is a break.
4. The standing falsifier rides with the note: the next 5 human-authored merges are the test set. Any lawful-standing human merge whose heads diverge falsifies this note — file the falsification, don't file excuses.
5. Receipt line: "IV-head binding HELD/BROKEN: IV <head> @<comment> vs merged <sha>, author <who>" — author named for the record, never for the verdict.

## 🟢 MACHINE NOTE

```json
{
  "sn": "SN-1658",
  "title": "Human-Authored Merge Binds to Its IV Head",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-18",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "taxonomy": ["SYSTEM-INTELLIGENCE", "GOVERNANCE", "MERGE-AUTHORITY"],
  "applies_when": ["merge", "merge-watch", "iv-binding", "dock", "author-invariance"],
  "enforcement": "The merge-watch's IV-head binding check runs on every merge regardless of author (seat, dock, or GitHub UI click): it compares the IV'd exact head quoted in the IV verdict comment against the merge_commit_sha and flags any divergence as a binding break routed to the dock/Judge for adjudication. The scorer bounces any merge-lawfulness verdict that treats human authorship as a pass on the binding check.",
  "cousins": ["SN-1063 (three-pass structure is the receipt — the receipt family this binding verdict joins)", "SN-0924 (gate must clear its own bar — the bar here is author-invariant)", "SN-1220 (sealed verdict expires when the world moves — this note's heads are exact, not world-relative)"],
  "evidence": {
    "l523_f7": "hidden_files/shared-state.json, director_tick_2026_10_18_1108 (2026-10-18 18:08Z): 'L523 [F7] (6253263850): human-authored merge binds to its IV head (falsifier: next 5 human merges)'",
    "precedent": "same tick: '#2761 IV-head binding HELD (Epsilon exact-head IV 6252172116 @19ed55f361171 == merged head)' — the seat-authored case this rule generalizes to human authors"
  },
  "decision_change": "the next merge-watch run verifies IV-head binding on human-authored merges exactly as on seat-authored ones — authorship (dock click vs seat merge) is recorded for the record, never weighed in the verdict; a human click no longer inherits lawfulness from who clicked.",
  "falsifier": "the next 5 human-authored merges are the test set: any human-authored merge that stands lawful while its merge_commit_sha diverges from the IV'd exact head falsifies this note. A merge with no IV at all is out of scope (a different rule), not a falsification.",
  "mechanism": "merge legitimacy flows from the IV adjudication, not the author's identity — the IV judges an exact head, and the binding is a property of the merge artifact (merged head == judged head). Authorship is a property of the click event; the click event cannot change which head was judged. An author-sensitive binding check would let the highest-privilege actor bypass the bar, which inverts the trust model."
}
```

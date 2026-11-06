# For a Squash Merge, List the Merge Parent's Ancestry Back to the Anchor — the Post-Merge Window Hides the Pushes Before It

**Intelligent Block:** IB-SMART-NOTE-20260930-sn02213-squash-merge-list-parent-ancestry
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-11-06
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Main-seat "WHY I MISSED IT" correction, 2026-11-06 (memory log, breach #221 follow-up): verifying PR #3260, the seat compared only the post-merge window and missed the push between the anchor and the squash merge's parent. Smart-note distillation tick 2026-11-06 12:08 PST.

## ✦ IN A NUTSHELL

Verifying PR #3260 (breach #221) on 2026-11-06, the main seat compared the merge commit cb61c7d1 against the post-merge window (cb61c7d1...89e06da7) and never listed the ancestry of the squash merge's single parent 9fa194df back to the previous anchor 63139f42 — missing that the parent sat one direct push (SN-2103, 16:45:06Z) past the anchor. A squash merge collapses its PR into one commit with one parent, and that parent is the last pre-merge tip: it can sit arbitrarily far past the verifier's anchor, and the post-merge window alone never shows it. The rule: for every squash merge, list `git log --oneline <anchor>..<merge-parent>` before comparing anything after the merge; a verification with no ancestry listing has not proven "nothing else landed."

## 🩷 HUMAN NOTE

Shawn — checking a squash merge by looking only at what came after it is like checking a delivery by looking only at the boxes that arrived after the truck left. The truck itself — the merge — carries everything that was loaded before it left, and the only way to see that load is to open the truck's manifest: the list of commits between your last checkpoint and the merge's parent. Today that manifest held a push nobody had accounted for. The standing rule now: for every squash merge, list the parent's history back to the last checkpoint first — then look at what came after.

## 🟣 CHILD NOTE

Imagine your teacher collects everyone's homework into one big folder and hands it in as a single pile. If you only count the papers added after the pile was handed in, you miss everything inside the pile. To know what is really in there, you open the pile and count back to the last time you checked. Always count the pile, not just what came after it.

## 🔵 GRANDMA NOTE

Dear, a squash merge is like a suitcase packed for a trip: everything inside was packed before the suitcase was closed. If you only look at what was added to the room after the suitcase left, you will never know what went inside it. Open the suitcase — list everything from the last time you looked until the suitcase was shut. That list is the truth of what traveled.

## 🟠 NAYA NOTE

For every seat verifying a squash merge: (1) never start from the merge commit's diff or the post-merge window — first run `git log --oneline <previous-anchor>..<merge-parent>` and list every intermediate commit; the merge's single parent is the last pre-merge tip, not the anchor; (2) the post-merge window (merge...tip) shows only what landed after the merge — the pushes between the anchor and the parent are invisible there by construction; (3) this is the sibling of SN-1088 (the commit's parents are the landing record — that note classifies HOW a commit landed; this one enumerates WHAT landed before a squash); (4) when the ancestry listing is empty, say so explicitly — "zero intermediate commits" is a finding, not an omission; (5) a verification that claims "nothing else landed" without an ancestry listing is unproven, and the claim must be withdrawn until the listing is produced — as the main seat did the same day, in public, with the correction on the record.

## 🟢 MACHINE NOTE

```json
{
  "applies_when": [
    ["merge", "verification"],
    ["evidence", "squash-merge"],
    ["claim", "landing-record"]
  ],
  "canonical_object": "INTELLIGENT_BLOCK",
  "claim_boundary": "This note governs verification of squash merges only: merge commits with two parents need the second-parent enumeration instead (SN-1837), and direct pushes are verified by the parent test (SN-1088). It does not claim the post-merge window is useless — only that it cannot prove what landed before the merge.",
  "decision_change": "When verifying a squash merge, the seat lists the merge parent's ancestry back to the previous anchor before comparing the post-merge window; a 'nothing else landed' claim without that listing is treated as unproven.",
  "enforcement": "The breach-verification checklist carries the ancestry-listing step as required: `git log --oneline <anchor>..<merge-parent>` output must appear in the verification record, and a 'nothing else landed' claim with no listing is a blocking finding on review.",
  "evidence": [
    "PR #3260 (SoulSchoolAcademy/NayaPOWER), squash merge cb61c7d1 (single parent 9fa194df), merged 2026-11-06T16:49:12Z; main-seat verification compared cb61c7d1...89e06da7 only and missed ancestry 63139f42→9fa194df: one direct push (SN-2103, 16:45:06Z) sat between the previous anchor and the merge parent. 'WHY I MISSED IT' correction recorded the same day in the 2026-11-06 memory log.",
    "Chain proven first-hand the same day (App route): 4c305061 → 63139f42 (SN-2102 push, 16:10:56Z) → 9fa194df (SN-2103 push, 16:45:06Z) → cb61c7d1 (#3260 squash merge, 16:49:12Z)."
  ],
  "falsifier": "The rule is refuted if a squash merge's parent always equals the verifier's anchor — i.e., if no push can ever land between the anchor and the merge parent. In practice the check pays for itself the first time the listing is non-empty; a long run of empty listings would demote it from required to recommended.",
  "intelligence_class": "LESSON",
  "mechanism": "A squash merge has exactly one parent — the last pre-merge tip — and its diff shows only the squashed content. Any pushes between the verifier's anchor and that parent are invisible in the post-merge window by construction; only an explicit ancestry listing between anchor and parent enumerates them.",
  "related_notes": ["SN-1088", "SN-061", "SN-1837"],
  "truth_state": "CANDIDATE"
}
```

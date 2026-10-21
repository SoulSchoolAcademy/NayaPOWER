# An Endorsement Only Counts on a Live Venue Re-Read

**Intelligent Block:** IB-SMART-NOTE-20260930-sn0175-endorsement-on-live-venue-reread
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-02
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #554 comment 5946566000 (Naya 2 relay, 2026-10-02 ~06:16 UTC / 2026-10-01 23:10 PDT) endorsing the overnight sweep correction — my lane's self-correction 5946445839 superseding the false "no open repair" claim 5946437843, with the canonical repair PR #1312.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

When a lane self-corrects, the confirming lane's receipt is only as strong as its own eyes. Naya 2 did not merely quote my correction — she independently re-read PR #1312's live venue state this run: state open, non-draft, head `brain-build/index-05memory-25 @ 9fafa84c`, base == current main tip `25268675` — and only then endorsed the stand-down ("your stand-down is correct"). She named the mechanism herself: "that's the deconfliction rule working." The durable rule: an endorsement of another lane's correction binds only the venue's live state re-read by the endorser; quoting the claimant's stated evidence is secondhand and adds no confirmation weight. She also kept custody explicit — "Index RED reclassification confirmed independently" (verified by her own re-read) vs "the rest of the sweep stands as your first-seen findings, your lane... No relay action — just witnessed" (witnessed, not adopted) — and anchored unchanged heads (`brain-build/node-master-specs-v1` a71fbfe1, `naya4/nine-node-kernel-v1` 1e7fd25c) as standing state. The correction loop closes only when a second lane has looked, not when it has read.

## 🩷 HUMAN NOTE

Shawn — a small, clean instance of the lanes working the way the doctrine says they should. My lane's overnight sweep had a false "no open repair" line; I corrected it and stood down. Naya 2 didn't just take my word for it — she re-read PR #1312's live state herself (open, head, base on the current main tip) before confirming the stand-down was right, and she marked exactly what she verified versus what she only witnessed. That's the standard: a correction is only confirmed when a second lane has actually looked at the venue, not just read the claim.

## 🟣 CHILD NOTE

Imagine Kid B saying "oops, I was wrong, Kid A is fixing the chair." Then a teacher comes by and instead of just saying "okay, good," she actually walks over, sees Kid A's tools on the chair, and says "yes — the tools are really there, your correction is right." The teacher's "I checked myself" is what makes the "oops" trustworthy. The new rule: never confirm someone's correction by repeating their words — go look at the thing yourself first.

## 🔵 GRANDMA NOTE

It's the difference between a neighbor telling you "the fence is painted" and you walking out to see the paint yourself. The team wrote this one down in a relay receipt: one Naya corrected herself about an open repair, and the other Naya didn't just repeat the correction — she looked at the repair with her own eyes, saw it was really there, and only then said "confirmed." Trust, but go look.

## 🟠 NAYA NOTE

Apply this to every cross-lane correction receipt: (1) when a lane posts a self-correction, the confirming lane must independently re-read the venue's live state (PR state/draft, head SHA, base vs current main tip) and cite the re-read — quoting the claimant's evidence is secondhand and adds no confirmation weight; (2) split the receipt explicitly: VERIFIED (re-read live by you, cite what you re-read) vs WITNESSED (first-seen findings that remain the originating lane's, no relay action taken); (3) anchor unchanged standing state (heads, pins) so the receipt doubles as a no-move attestation; (4) never endorse a correction you have not looked at yourself — a relay that only repeats words is not a second lane, it's an echo.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": null,
  "evidence": {
    "correction_endorsed": "#554 5946445839 (2026-10-02T06:01:18Z) — self-correction superseding false 'no open repair' claim 5946437843; stand down per no-duplicate-repair, repair belongs to PR #1312's lane.",
    "independent_reread": "#554 5946566000 (2026-10-02 ~06:16 UTC) — 'PR #1312 verified this run: state open, non-draft, head brain-build/index-05memory-25 @ 9fafa84c, base == current main tip 25268675.'",
    "custody_split": "'Index RED reclassification confirmed independently' vs 'the rest of the sweep stands as your first-seen findings, your lane... No relay action — just witnessed.'",
    "standing_state": "heads unchanged: brain-build/node-master-specs-v1 a71fbfe1, naya4/nine-node-kernel-v1 1e7fd25c; named as the deconfliction rule working."
  },
  "rule": [
    "an endorsement of another lane's correction binds only a live venue-state re-read performed by the endorser (PR state/draft, head SHA, base vs current main tip) — quoting the claimant's evidence is secondhand",
    "split every correction receipt: VERIFIED (re-read live, cited) vs WITNESSED (originating lane's findings, no relay action)",
    "anchor unchanged heads/pins in the receipt as a no-move attestation"
  ],
  "lesson_line": "A correction is only confirmed when a second lane has independently re-read the venue's live state and said so — an endorsement that quotes the claim is an echo, not evidence.",
  "extends": "SN-043 (resolve both sides at their own refs), SN-057 (temporal attribution — re-read before acting), SN-121 (verifier names its boundary), SN-173 (repair-registry pre-claim check)"
}
~~~

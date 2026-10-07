# Evidence Beats Scoring — Reverse Your Own Executed Decision Openly When the Deciding Fact Arrives

**Intelligent Block:** IB-SMART-NOTE-20260930-sn056-evidence-beats-scoring-reversal
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-01
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #554 comments 5929079105 (2026-10-01 09:57:44Z, Naya 4's +7/−4 decision closing #1238 as duplicate), 5929077552 (Naya 2's 46–29 scorecard with the base-freshness evidence), 5929282107 (relay flagged the divergence), 5929282200 (2026-10-01 10:11:49Z, public reversal: #1209 closed via 5929279991, #1238 reopened as the single canonical survivor).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

On 2026-10-01 Naya 4 scored the #1209 vs #1238 duplicate pair and decided thin: close #1238, keep #1209 (+7 vs −4), and executed the close (5929077168). The scoring was honest but blind — it never checked the bases. Forty seconds earlier, Naya 2's scorecard (5929077552) had carried the deciding fact: #1209's base `507d3421` is stale against main `a726a837`, while #1238's base is current main — and a READY patch on a stale base misleads the merge gate. The sequence that followed is the lesson in three parts. First, **base freshness is the decision-relevant fact for a duplicate ledger patch**: "canonical green" status without base freshness is a misleading signal; thin scoring that misses the deciding fact will lose to evidence-rich scoring every time, and the correct move when the deciding fact arrives is to admit the miss, not to defend the score. Second, **reverse openly and completely**: Naya 4 independently verified the base claim live (diffs confirmed byte-identical, same ledger file, same hunk, `statement_count` 19→3), re-scored (survivor-on-current-main +9 / survivor-on-stale-base +2 / stall −2 — ranking flipped), then executed the reversal in full view: #1209 closed (comment 5929279991), #1238 reopened (still draft, now the single canonical survivor), and corrected Naya 2's consolidation comment which had framed the close as still-pending — "a close HAD executed… That's now corrected." No defensiveness: "the wrong PR survived for about 20 minutes and now the right one does." Third, **the mechanism that caught it was the Decision Protocol's step 6**: the decision was decided and *reported publicly with a challenge invited*, so the challenge could arrive — Naya 2's scorecard was the challenge, and the relay's 5929282107 flagging the divergence kept it on the record. A decision made in private would have stood unchallenged; a decision made in public gets better. This is Prime 1 (Judgment Rule) applied to oneself: when you can see you were wrong, you stop, explain why with evidence, and propose the right path — including when the "you" is your own executed decision from twenty minutes ago.

## 🩷 HUMAN NOTE

You bet on the wrong horse, publicly, and then the racing form shows you missed that your horse was carrying an injury. The bad move is to keep riding because you already placed the bet. The good move is to walk to the window, cash out in front of everyone, say exactly what you missed, and place the bet on the right horse. Twenty minutes of being wrong, owned out loud, buys more trust than a week of being quietly right.

## 🟣 CHILD NOTE

Imagine you pick one of two drawings for the school contest and hang it up — then your friend shows you that your drawing has the wrong name on the back and hers has the right one. You don't leave yours hanging just because you hung it first. You take yours down, hang up the right one, and tell the class "I picked wrong at first — here's why, and here's the right one." Changing your mind when you get better facts is the smartest thing you can do, not a failure.

## 🔵 GRANDMA NOTE

It's like telling the whole family you're selling the old car to your nephew — and then your sister shows you the nephew's offer was actually for the wrong car, a different one that's already sold. You don't dig in because you already announced it. You call everyone back, you say "I had it wrong, here's the paper that shows it, here's the real deal," and you do the right sale. The family trusts you more afterwards, not less — because you showed them the paper.

## 🟠 NAYA NOTE

Run this every time a scored decision collides with incoming evidence you did not have at decision time: (1) independently verify the new evidence live before touching anything — never reverse on an unverified claim (this instance: bases checked live, diffs byte-compared); (2) re-score honestly with the deciding fact in the criteria — if the ranking flips, the decision flips; (3) execute the reversal completely and publicly: undo the executed action, restore the survivor, and post a correction that names what you missed, with the comment IDs of both the original decision and the correction; (4) if anyone's record of the event is wrong (this instance: Naya 2's consolidation framed the close as still-pending), correct the record — accuracy outranks politeness; (5) name the mechanism: the reversal was possible because the decision was public per the Decision Protocol's step 6 — keep deciding in public so challenges can arrive. Never defend a thin score against richer evidence; the fastest way to be right is to be wrong out loud and early.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "thin_scoring_blind_to_deciding_fact_executed_then_reversed",
  "evidence": {
    "original_decision": "#554 5929079105 (2026-10-01 09:57:44Z) — Naya 4 scored +7/-4, closed #1238 as duplicate (5929077168); kept #1209 (READY) as canonical",
    "missing_fact": "#554 5929077552 — Naya 2's scorecard: #1209 base 507d3421 stale vs main a726a837; #1238 base current main; stale-base READY misleads the merge gate",
    "verification": "bases confirmed live; both PR diffs byte-identical (supabase/PRODUCTION-MIGRATION-LEDGER-V1.json, one hunk, statement_count 19 -> 3)",
    "reversal": "#554 5929282200 (2026-10-01 10:11:49Z) — re-score +9/+2/-2, ranking flipped; #1209 closed (comment 5929279991); #1238 reopened (draft) as single canonical survivor; consolidation record corrected",
    "divergence_flag": "#554 5929282107 — relay flagged the verdict divergence without contesting (contested judgment belongs to the main seat)"
  },
  "rule": "evidence_beats_scoring_reverse_openly_when_deciding_fact_arrives",
  "procedure": [
    "independently verify incoming evidence live before reversing — never reverse on an unverified claim",
    "re-score with the deciding fact in the criteria; if the ranking flips, the decision flips",
    "execute the reversal completely and publicly: undo, restore, post correction naming the missed fact with comment IDs",
    "correct anyone's inaccurate record of the event — accuracy outranks politeness",
    "keep deciding in public (Decision Protocol step 6) so challenges can arrive; the public decision is what made the challenge possible"
  ],
  "related": ["SN-016 (Prime Judgment Rule)", "SN-042 (explicit supersession — declare replaced diagnoses SUPERSEDED)", "SN-052 (duplicate-seam merge-list routing — diff the diffs)", "SN-054 (relay-race consolidation — same-night duplicate race, repaired the other way)"]
}
~~~

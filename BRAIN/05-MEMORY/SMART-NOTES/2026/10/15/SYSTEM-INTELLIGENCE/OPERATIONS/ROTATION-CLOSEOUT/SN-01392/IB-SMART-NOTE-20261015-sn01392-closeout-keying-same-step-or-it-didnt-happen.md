# IB-SMART-NOTE-20261015-sn01392-closeout-keying-same-step-or-it-didnt-happen

Intelligent Block: OPERATIONS-DOCTRINE
Truth state: CANDIDATE
Scope: PRIVATE
Captured: 2026-10-15
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL

Wave 184 closed 3/3 on the venue (2026-10-15, 11:47–11:51Z) but was never keyed in rotation_waves — the hole-ledger rule ("key rotation_waves in the SAME step as closeout") missed at closeout, producing L370 hole 184. The wave-186 MEMORY re-measure: rotation_waves keys 1–185, 157 keyed, **28 unkeyed** — net +1 vs the wave-183 baseline of 27. Precedent (wave-183) is report-not-backfill, and no seat owns the backfill yet, so the ledger accumulates holes. The durable lesson: a keying rule written as "same step as closeout" still got skipped **in the very next wave** — the rule is decoration unless the closeout step names keying as a checkable item inside itself. Two arms of the fix: (1) the closeout checklist carries the keying line, verified before the step ends; (2) report-not-backfill gets a backfill owner — holes reported but unowned are holes accepted.

## HUMAN NOTE

The team has a rule: when you close out a wave, record it in the rotation ledger — in the same step, not later. The next wave after the rule was restated still skipped it. The rule didn't fail because anyone disagreed with it; it failed because the closeout moment has a "we're done" psychology, and a rule that lives outside the checklist doesn't survive that moment. And the precedent says: report the hole, don't backfill it — but nobody owns the backfill, so the ledger just grows new holes on a standing pile of old ones. The fix isn't a stronger rule; it's putting the keying line *inside* the closeout checklist as something you verify before you're done, and naming an owner for the backfill pile.

## CHILD NOTE

The rule says: when you finish a chore, write it on the family chart — right then, not later. But "right then" is when you're already walking away from the chore. Nobody checks the chart at the door, so the chart keeps missing chores. The fix: the chart check has to be part of the chore itself — you don't leave the room until it's written. And if a chore gets missed, someone has to own writing it in later, or the chart just stays wrong forever.

## GRANDMA NOTE

A rule that says "do it right away" only works if something checks it right away. Closing time is the worst moment for an extra step — that's exactly when people feel finished. Put the check inside the closing routine itself, and give the missed ones to someone named. Otherwise you're collecting reports of holes instead of filling them.

## NAYA NOTE

When I design a closeout step, the keying line lives *inside* the checklist, not beside it — verified before the step ends, not after. A "same step as closeout" rule with no in-step check is a wish. And I never set a report-not-backfill precedent without naming the backfill owner: a hole that's reported but owned by nobody is a hole I've decided to keep.

## MACHINE NOTE

{
  "sn_id": "SN-01392",
  "type": "OPERATIONS_DOCTRINE",
  "truth_state": "CANDIDATE",
  "enforcement": {
    "rule": "ledger_keying_is_an_in_step_checkable_item",
    "applies_to": ["wave closeouts", "rotation_waves keying", "any record-the-event ledger step"],
    "violation": "a keying rule stated outside the closeout checklist, or report-not-backfill with no backfill owner",
    "check": "the closeout template carries the keying line as a checkable item verified in-step; the backfill queue names an owner (seat + lane), else the precedent is report-and-keep"
  },
  "falsifier": "a wave closes without same-step keying and still gets keyed with no hole — the 'uncheckable rule decays' claim fails only if skipped keying reliably self-heals",
  "mechanism": "closeout carries completion psychology: post-step obligations compete with the felt-done state and lose. A rule external to the checklist relies on the weakest moment of compliance; embedding the check in the step makes it part of 'done' itself. Report-not-backfill without an owner converts a remediation into a tolerated accumulator.",
  "related_laws": ["SN-0351_sign_in_out", "L370_hole_ledger"],
  "source": "live board #2537 comment 6191743866 item 2 (Naya Archivist, wave-186 MEMORY sign-out, 2026-10-15): L370 hole 184 found; re-measure keys 1-185 = 157 keyed / 28 unkeyed; wave-183 report-not-backfill precedent",
  "compounds_with": ["SN-1348_no_word_law_fires_on_review_attribution"]
}

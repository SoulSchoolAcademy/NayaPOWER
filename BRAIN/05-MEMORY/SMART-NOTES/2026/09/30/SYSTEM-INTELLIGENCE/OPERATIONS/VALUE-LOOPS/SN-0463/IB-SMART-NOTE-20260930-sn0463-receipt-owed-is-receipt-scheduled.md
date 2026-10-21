# A Receipt Owed Is a Receipt Scheduled

**Intelligent Block:** IB-SMART-NOTE-20260930-sn0463-receipt-owed-is-receipt-scheduled
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-06
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Team 2 track cycle 2 (2026-10-06): the Intelligence Receipt design said "the capturing lane owes him, in the same turn" — but same-turn obligations decay under load. Built `receipt_sweeper.py` + hourly goal-owned cron `hv-receipt-sweep`: scans the Smart Note draft branch for newly staged notes whose provenance attributes intelligence to Shawn and auto-generates missing receipts. First sweep generated SN-0457's receipt mechanically. Evidence: ~/workspace/goals/learning-10-10/hidden_files/human-value/receipt_sweeper.py, receipts/SN-0457-2026-10-06-auto.md.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

A value loop isn't closed by a rule — it's closed by a scheduled mechanism that fires without anyone remembering. "The lane owes a receipt" is a rule; an hourly sweeper that generates the receipt from the note's own provenance is a closed loop. Rules decay under load; schedules don't.

## HUMAN NOTE

When Shawn shares intelligence, the design said the capturing lane owes him a receipt "in the same turn." That's a good rule, but rules depend on someone remembering at the right moment — and moments get busy. So we built a sweeper: every hour, it looks at newly staged Smart Notes, finds the ones built from Shawn's intelligence, and generates the missing receipts automatically. The rule tells lanes what to do; the sweeper makes sure it happens even when they forget. Both layers matter — the obligation sets the standard, the mechanism guarantees the floor.

## CHILD NOTE

If you promise to say thank-you every time, you'll forget sometimes. So you set an alarm that checks: did I say thank-you for everything today? The alarm doesn't replace the promise — it makes sure the promise is kept.

## GRANDMA NOTE

Good manners need good reminders. We made a helper that every hour checks whether anyone forgot to send a thank-you note, and sends it for them. Nobody has to remember; the helper always does.

## NAYA NOTE

Future Naya: when you design a "lane owes X" obligation, also build the scheduled sweeper that enforces it — in the same cycle, not later. The obligation without the mechanism is a wish. The mechanism without the obligation is noise (it would generate receipts nobody asked for). Check: does the sweeper's trigger condition (here: provenance attributes intelligence to Shawn) precisely match the obligation's trigger? If the trigger is vague, the sweeper will misfire — keep the match conservative and let the watermark + dry-run mode prove it before going live. This pattern generalizes: QA-time logging, decision-log tagging, any "lanes must" rule.

## MACHINE NOTE

```json
{
  "sn": "SN-0463",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-06",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "lesson": "obligation_without_mechanism_is_a_wish",
  "mechanism": {
    "script": "~/workspace/goals/learning-10-10/hidden_files/human-value/receipt_sweeper.py",
    "schedule": "hv-receipt-sweep (hourly, goal-owned, goal:learning-10-10)",
    "trigger": "provenance attributes intelligence to Shawn (conservative regex)",
    "watermark": "receipt-sweep-watermark.md",
    "first_fire": "2026-10-06: SN-0457 auto-receipt"
  },
  "generalizes_to": ["qa-time logging", "decision-log tagging", "any lane-must rule"],
  "smart_link": "https://github.com/SoulSchoolAcademy/NayaPOWER/issues/1604"
}
```

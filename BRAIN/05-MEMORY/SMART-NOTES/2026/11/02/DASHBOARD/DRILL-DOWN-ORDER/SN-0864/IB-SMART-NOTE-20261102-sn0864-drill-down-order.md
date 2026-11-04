# The Drill-Down Order: Orb, Then Stats, Then Time
SN-0864 · DASHBOARD / DRILL-DOWN-ORDER
**Created:** 2026-11-02T22:44:13Z

## Hook
Every click takes you one level deeper — never sideways. Click the orb, get its stats. Click a stat, get its time breakdown in bars. Every click must show something. Nothing dead, nothing decorative.

## What happened
Shawn was testing the drill-downs and saw the confusion: chart-switcher buttons that changed the view, but no way to go deeper. He redesigned the hierarchy live: the orb opens the section's stats (the four sub-stats), and clicking any stat inside opens that stat's time breakdown — day by day, hour by hour — in bars. Not the chart buttons. The stats themselves are the doors.

## The rule, in his words
"You're going to click the orb for the section then it goes in and gives you the stats... but then if you click the stat that's displayed that stat will get displayed in bars... you click the button you go into the inner stats they give you those four stats then you click any of those stats then you get the bar stats."

## Why it matters
This is the answer to "what's the story?" — the third question of the Smart Stats bullseye. A dashboard that only shows totals is a poster. The drill-down is what makes it an instrument: where am I (gauge), what's driving it (orbs), what's the story (drill down). And the law inside it — every click must show something — is the anti-dead-control rule: a control that does nothing is a lie.

## How it connects
The three levels: orb → sub-stats → time breakdown (bars, day-colored, with Hour/Day/Week/Month/All pills). The view switcher (SN-0866) changes how a level looks; this rule decides what the levels are. The number-format rule (SN-0865) decides how every number reads at every level.

---
*Source: Conversation with Shawn, 2026-11-02 22:42–22:44 UTC. His direction: message `a4e42c6e-afd9-496c-944d-0d6b95d75ba4` (the three-level sketch) and the lock-in message `ab1980c3-c06e-4450-bc62-4d9cd11dd6d8` ("click the stats within the stats"). Filed per his 2026-11-03 standing instruction: every conversation's valuable intelligence captured into Project Intelligence and GitHub.*

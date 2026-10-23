Intelligent Block
Truth state: CANDIDATE
Scope: PRIVATE
Captured date: 2026-10-23
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

A SURGE seat nearly wasted a full falsifier-battery run because it almost skipped the frontier survey. t1418's lane-3 arm nearly re-ran the closed all-clauses mechanism family — an accidental F5-class violation — and caught itself: the frontier survey is now the first tool call after sign-in, before design. The doctrine is old (don't re-run closed families); the new, durable part is the placement: make it an explicit Step 0 in SURGE briefs so the near-miss becomes a structural impossibility, not a self-save.

## 🩷 HUMAN NOTE

Shawn — one of the trial lanes almost burned a whole run for nothing this morning. Before designing a measurement arm, the seat is supposed to survey what's already been proven and what's still open — the frontier survey. It almost skipped that step and would have re-tested a mechanism family that was already closed, which is a wasted run nobody can get back. It caught itself in time. The fix isn't "be more careful" — it's rewriting the recipe: the frontier survey becomes the explicit first step after sign-in in every SURGE brief, so skipping it takes effort, not remembering it.

## 🟣 CHILD NOTE

Imagine you're doing a treasure hunt with friends, and before you start you're supposed to check the map of where people already dug — so you don't dig in a hole that's already empty. One of the diggers almost skipped looking at the map and started digging in a hole that was already dug out. She caught herself just in time. The new rule: "look at the map" is now step one on the instruction sheet, written in big letters, so nobody has to remember — it's just what you do first.

## 🔵 GRANDMA NOTE

It's like going grocery shopping without checking what's already in the fridge — you come home with a third gallon of milk. A measurement team has a rule: before you design a new test, check the chart of what's already proven and what's still unknown. One researcher nearly skipped the chart and was about to re-prove something settled. She caught herself. The fix is simple: put "check the chart" as the very first line of the procedure, before anything else — so it happens by default, not by memory.

## 🟠 NAYA NOTE

SURGE execution doctrine, Naya to Naya: the falsifier battery's economics hinge on one ordering invariant — frontier survey BEFORE design. The survey maps mechanism families to closed/open; without it, the seat's default is the most familiar family, which is often the closed one. t1418's lane-3 run caught this live: the seat almost skipped the survey and would have re-run the closed all-clauses mechanism family (an F5-class wasted run by accident, not by intent), then self-corrected — survey first, then design. Self-correction is good; self-correction being NECESSARY is a process gap. The structural fix: SURGE briefs carry an explicit Step 0 — frontier survey as the first tool call after sign-in, before design — and lane receipts name the survey outcome in their Mirror check. A seat that skips Step 0 is then failing the brief, not forgetting a habit, and the receipt review can flag it. This is the same shape as SN-1517's preregistration lesson: bind the decision before the numbers exist, or the numbers will bind the decision after they do.

## 🟢 MACHINE NOTE

```json
{
  "slug": "sn-1874-frontier-survey-first-after-sign-in-surge-briefs",
  "lesson": "A SURGE seat must run the frontier survey as the first tool call after sign-in, before design: t1418 lane-3 nearly skipped it and would have re-run the closed all-clauses mechanism family — an accidental F5-class wasted run — catching itself only by self-correction. Self-correction is good; needing it is a process gap. The fix is structural: SURGE briefs carry an explicit Step 0 (frontier survey first, before design), and lane receipts name the survey outcome in their Mirror check, so skipping it is a brief failure a receipt review can flag rather than a forgotten habit.",
  "applies_when": ["surge", "falsifier-battery", "trial-design", "lane-executor"],
  "enforcement": "SURGE briefs (brief-queue writers) carry an explicit Step 0: frontier survey as the first tool call after sign-in, before design; the lane receipt's Mirror section names the survey outcome, and the brief owner's review flags any SURGE receipt that reached design without a survey record. A falsifier-battery run that skipped the survey is scored as a brief-process failure, not just an unlucky design.",
  "evidence": [
    "hidden_files/twelve-lane-receipts/t1418-lane3.md ['Mirror — Failure named' + 'AGENT FEEDBACK' — seat almost skipped the frontier survey and would have re-run the closed all-clauses mechanism family (wasted run, F5-class by accident); self-correction: frontier survey is now the first tool call after sign-in, before design; recommended as an explicit first step in SURGE briefs]",
    "hidden_files/learning-events-2026-10-23-14.md [14:00 PDT hour LEARNING event: near-violation caught and corrected]"
  ],
  "decision_change": "SURGE brief authors place the frontier survey as explicit Step 0 after sign-in, before design; lane executors survey before designing arms; receipt reviewers treat a missing survey as a brief-process failure. The next falsifier-battery design decision starts from the frontier map, not from the most familiar mechanism family.",
  "falsifiability": "If a re-run of a survey-marked-closed mechanism family produces novel, discriminating information (the survey's closure verdict was wrong in a way the survey itself would not have caught), then the frontier survey is insufficient as a gate and the lesson's mechanism is wrong — the fix would be a better survey, not an earlier one.",
  "mechanism": "The frontier survey partitions the mechanism space into closed (already falsified or proven) and open families. Without the partition, design defaults to familiarity, and the familiar family is disproportionately the closed one — effort is spent re-proving what is already decided, which is the F5-class failure (work with no information yield). Placing the survey as Step 0 makes the partition exist before any design choice can be made, so closed families are unreachable by default rather than by discipline."
}
```

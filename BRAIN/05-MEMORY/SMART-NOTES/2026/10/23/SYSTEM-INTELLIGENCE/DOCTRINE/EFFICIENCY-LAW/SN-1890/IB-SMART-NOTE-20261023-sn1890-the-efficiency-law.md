Intelligent Block
Truth state: CANDIDATE
Scope: PRIVATE
Captured: 2026-10-23
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL
Wake-ups are the currency. The Efficiency Law (announced 2026-10-23 as Shawn's standing word): every scheduled job carries a one-line value case — what it produces, what it costs in wake-ups per day, what it replaces; total team wake-ups are counted daily against an 800/day ceiling; watchers become hooks that fire on change, never on a clock; every document is distilled to essence; production is measured as a production-to-waste ratio (baseline 173:1, target under 60:1 by 2026-10-30, published daily).

## 🩷 HUMAN NOTE
The team runs dozens of background jobs — watchers, sweepers, reviews, feeds — and each one costs attention even when it finds nothing. The Efficiency Law makes that cost visible and capped. Every recurring job must now justify itself in one line: what value it produces, how many wake-ups per day it costs, and what it replaces. The whole team gets 800 wake-ups per day, counted and published daily; if the count breaches the ceiling, the three biggest jobs are named on the board. Watchers that only notice change stop being agents on a schedule and become hooks — they run when the watched thing changes, never on a timer. And documents get distilled to their essence: a law that takes 2,000 words isn't understood yet. The day this law landed, the house cut its own wake-ups from 3,432 to 1,272 per day in a single pass — proof the waste was real and removable.

## 🟣 CHILD NOTE
Imagine a house with a hundred alarm clocks, each ringing every ten minutes — most of them for no reason. That's how the team's background work used to be. The new house rule: every alarm clock has to say in one sentence why it rings and what it costs, and the whole house only gets 800 rings per day. Alarms that just watch for something now only ring when the thing actually happens. And the rulebook itself has to be short enough to understand — long rules get folded down to their essence. The team cut its own ringing by 63% the same morning, just by asking "why does this ring?"

## 🔵 GRANDMA NOTE
Think of it like leaving the lights on in every room of the house all day. Each room's lights cost a little, but with every room lit, the bill is enormous. The new house rule: every light has to earn its place — one sentence saying what the light is for and what it costs, and a hard limit on the whole house's electricity. Lights that only watch for motion become motion sensors instead of burning all day. And the instructions for the house are kept short, on one card, not in a filing cabinet. When they did this, the electric bill dropped by nearly two-thirds in one day.

## 🟠 NAYA NOTE
For every seat, immediately: count your own jobs and post the number on the board. Cut any job that cannot state its one-line value case (what it produces, what it costs in wake-ups/day, what it replaces). Convert watchers to hooks — agents wake on change, never on a clock; cadence never exceeds how fast the watched thing can change or be consumed. Distill documents to essence — detail lives in archives and daily logs, never stapled to the law book. The daily census: team-wide wake-ups vs the 800/day ceiling, published daily; a breach is a material board event naming the three largest jobs. The production-to-waste ratio (baseline 173:1, target under 60:1 by 2026-10-30) is published daily on the NayaPOWER Production board, first Page Test run 2026-10-24.

## 🟢 MACHINE NOTE
{
  "id": "SN-1890",
  "slug": "the-efficiency-law",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-23",
  "lesson": "Background work has a measurable currency: wake-ups per day. Every scheduled job must carry a one-line value case (produces / costs in wake-ups per day / replaces); the team holds a hard 800 wake-ups/day ceiling counted and published daily; watchers become change-fired hooks instead of clock-fired agents; documents are distilled to essence; production is measured as a production-to-waste ratio with a dated target (173:1 baseline, under 60:1 by 2026-10-30).",
  "evidence": [
    "board #2793 comment 6372571817 (2026-10-23T19:02:37Z, director-seat relay): 'THE EFFICIENCY LAW — TEAM-WIDE (Shawn's ruling, 2026-10-23)' — quoting his words: 'We're at about 1% efficiency and 99% inefficient and ineffective. This has gotta change immediately. The numbers don't lie.' The comment was posted by the lane-agent bot; the relay attribution is quoted verbatim above rather than asserted independently.",
    "director tick memory entry 2026-10-23 12:08 PDT: 'Efficiency Law announced (Shawn's word, wake-ups vs 800/day)' — independent second leg for the announcement.",
    "Same-day receipt in the comment: house wake-ups 3,432 -> 1,272/day (-63%) in one pass; hooks conversion in flight, projected ~700/day with faster response."
  ],
  "decision_change": "Every future decision to schedule, keep, or design a recurring job must include the one-line value case; a job without it is held at filing. Watcher-style agents are converted to change-fired hooks instead of being kept on a timer.",
  "falsifier": "If the daily wake-up census is published for 7 consecutive days and a job whose value case claims X wake-ups/day shows no measurable relation to either board-visible output or the measured production-to-waste ratio, the value-case discipline is theater, not accounting - the census is counting the wrong thing or the case is.",
  "mechanism": "Wake-ups are observable and countable (the census), which turns an invisible cost into a budget line; the ceiling plus the named-breach rule gives every seat a direct incentive to kill its own waste; hooks fire on change rather than on a clock, so the cost scales with actual events rather than with time.",
  "applies_when": [
    "schedule",
    "cron",
    "operations",
    "wake-ups",
    "budget",
    "governor"
  ],
  "enforcement": "The daily wake-up census is counted against the 800/day ceiling and published on the board; a breach is a material board event naming the three largest jobs. The production-to-waste ratio is published daily on the NayaPOWER Production board (first Page Test 2026-10-24). Any new scheduled job filed without the one-line value case is held at filing."
}

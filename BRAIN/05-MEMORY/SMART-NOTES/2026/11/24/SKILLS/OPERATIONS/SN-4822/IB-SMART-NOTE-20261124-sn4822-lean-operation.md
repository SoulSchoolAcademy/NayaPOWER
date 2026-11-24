# Lean Operation

SN-4822 · SKILLS / OPERATIONS

**Created:** 2026-11-24T20:22:26Z
**Category:** Operations
**Skill:** 76
**SN:** SN-4822

## Nutshell

The smallest effective context, wake, and team — wake only when something changed, and never repeat the same failure.

## Child

Imagine a helper who wakes up every ten minutes to check if there's work — even when nothing changed. That's silly. A smart helper sleeps until the doorbell rings, then comes running. And if they trip on the same step three times, they fix the step instead of tripping a fourth time.

## Grandma

We work light. Each seat carries only the layer it needs — no more. Agents wake when something actually changes, not on a timer that rings whether there's work or not. Dead schedules are killed, never left ringing. And a job that fails the same way three times is stopped until its cause is fixed — never retried hoping for luck.

## What It Means

Work with the smallest effective context, wake, and team. Carry only the layer you need. Wake only on change — prefer a hook that wakes an agent only when something changed over a timer that wakes every time. Kill dead wakes, never slow live lanes. Stop repeating a failure — three identical failures in a row is a stop, not a retry; fix the cause before the job runs again.

## Why It Matters

Every agent-minute banks verified value instead of repeating failures or no-ops. A machine that wakes for nothing is a machine burning its own fuel — and fast and useless is useless.

## How It Connects

It connects to the Layered Context Law — the smallest context is the leanest context. It connects to the Score Is Verified Completions Per Hour — every minute must bank value. And it connects to Fail Fast — stop, don't repeat.

## How to Apply

Give each seat only its layer. Replace timers with hooks that wake on change. Kill schedules that finish nothing. When a job fails the same way three times in a row, stop it — find the cause, fix the cause, and only then let it run again. Never slow a live lane to save wake-ups; kill the dead wakes instead.

Real example: this is the custom skill `lean_operation`, built from Shawn's teaching on 2026-11-16 that "cadence is never the lever" — waking more often never fixed anything. The fix was waking only on change and stopping a thrice-failed job until its cause is fixed, so the machine spends its minutes on work that lands.

## What's In It For You

Less waste, lower cost, faster seats — the same work done with fewer wakes and fewer repeated failures. Every minute you spend is a minute that banks.

# IB-SMART-NOTE-20261008-sn0641-resource-constrained-execution-law.md
SN-641 · SYSTEM-INTELLIGENCE / OPERATING-DOCTRINE
**Created:** 2026-10-13T08:44:13Z

## IN A NUTSHELL

RESOURCE-CONSTRAINED EXECUTION LAW (proposed): Before dispatching autonomous work, determine execution capacity. Never silently queue impossible work. If capacity is insufficient, classify the blockage, preserve the mission, reprioritize available execution, and surface the exact resource required. When capacity returns, resume from durable state rather than restarting discovery.

Companion principle: Every failure is either repaired, converted into a constraint, or converted into a learning rule. Nothing valuable disappears.

## HUMAN

Naya 1 built the 24x7 Intelligence Factory (9 specialized seats, orchestration, 30-min cadence) and dispatched the first 8 specialist lanes. All 8 failed immediately: Brainbase CREDITS_EXHAUSTED. She refused to call this a success — and that honesty is the protocol working.

The deeper lesson: orchestration intelligence ran ahead of execution capacity. A truly intelligent machine doesn't discover a bottleneck and sit there — it adapts. It reasons about capacity as part of planning. It doesn't queue impossible work silently. It classifies the blockage (authority vs resources vs evidence), preserves the mission, and reprioritizes what CAN run.

This is why the failure is valuable: "not merely remembering 'Brainbase ran out of credits' but learning 'this system must reason about execution capacity as part of planning.'"

## CHILD

We tried to send out 8 workers and found out we had no fuel for them. Instead of pretending it worked, we learned a new rule: always check if you have fuel before sending workers out.

## GRANDMA

The team built a beautiful system for organizing work, then discovered they didn't have the resources to run it yet. Rather than hiding that, they turned it into a new rule about checking resources first — that's how the system gets smarter from its mistakes.

## NAYA

Pairs with the No-Waiting Doctrine (SN-0626): don't wait on blocked capacity — reprioritize to what CAN execute. The factory's 9 seats were designed for Brainbase; the existing Team Naya lanes (1-5 + cron workers) run on existing infrastructure and are NOT blocked. Work continues there.

Status: CANDIDATE. Only Shawn ratifies.

## MACHINE

{"sn": "SN-0641", "title": "Resource-Constrained Execution Law", "truth_state": "CANDIDATE", "scope": "TEAM", "captured": "2026-10-08", "source": "Naya 1 Intelligence Factory dispatch, Brainbase CREDITS_EXHAUSTED, #1354", "companion": "every failure is repaired, converted to constraint, or converted to learning rule", "pairs_with": ["SN-0626 no-waiting"]}

## UNCERTAINTY
Unratified branch capture; content preserved verbatim from the markdown projection, not independently verified.

## THE LEARNING
Branch-era smart notes must be migrated to v2 captures plus registry entries, or the vanish and registry-drift guards fail closed.

---
*Imported from PR #2981 (branch naya4/smart-notes-2026-09-30) on 2026-11-04 — recovered lost capture IB-SMART-NOTE-20261013-sn0641-migrated.*

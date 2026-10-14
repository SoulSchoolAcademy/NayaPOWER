# IB-SMART-NOTE-20261014-sn1323

**Intelligent Block:** SN-1323
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured date:** 2026-10-14
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL

Audit the measurement before rebuilding the machine. The agent-performance dashboard reported that the lane scorer was 77.6% behind — 98 jobs done, only 22 scored (22.4% coverage) — and the obvious move was to rebuild the scorer pipeline for throughput. Before touching anything, the builder audited the metric: `agent_performance.py` joined scores to receipts on the task field only, but scores whose task field is a description rather than a filename never matched, so the join silently dropped them from the aggregate. Indexing scores on the tick field too produced the true numbers: 98 jobs, 98 scored, 100% coverage, average 9.17, 34.7% clearing 9.5. The system was healthy; the dashboard was broken. Without the audit, real engineering time would have gone into "fixing" a healthy machine — and the repair would have changed nothing while the false alarm survived. The durable rule: a metric that says "rebuild the system" triggers an audit of the metric pipeline's own joins and indexing FIRST. Only after the measurement is verified do you spend on the system.

## HUMAN NOTE

Think of a hospital monitor that says the patient's oxygen is crashing. The good doctor doesn't order surgery — she checks whether the sensor is plugged in. That's what happened with our agent-performance dashboard: it showed the scoring pipeline at only 22% coverage, which looked like a system failing to keep up. Before rebuilding the whole pipeline, the builder checked the measuring instrument itself and found the bug in the script that computed the number — scores were being matched to receipts by the wrong key, so most of them silently fell out of the count. The real coverage was 100%. The machine was fine; the monitor was lying. The rule for every future alarm: verify the alarm's wiring before you operate on the patient. A false metric that nobody audits will keep prescribing surgery forever.

## CHILD NOTE

Imagine your teacher says you only did 2 of your 10 homework problems — but you know you did all 10. Before you panic, you check HOW the teacher counted: she was looking at a list that only had your old class number, and the problems you turned in under your new number never got counted. The real score was 10 out of 10! That's the lesson: when a number says something is broken, check how the number was made before you try to fix the thing. Count the counting first.

## GRANDMA NOTE

Dear, this one is about checking the thermometer before treating the fever. Our dashboard said the scoring machine was falling far behind — only 22% of the work measured. The tempting thing was to take the machine apart and rebuild it faster. Instead, the builder checked how the number itself was computed and found the counter was skipping most of the rows by matching them on the wrong label. The true number was 100% — the machine was never broken. The wisdom, dear: when a measurement alarms you, audit the instrument before you rebuild the patient. It is far easier to fix a counter than to rebuild a machine that was never broken — and the counter, unrepaired, will keep crying wolf forever.

## NAYA NOTE

For every Naya who reads a dashboard and reaches for the wrench: the dashboard is code, and code has bugs, and the bug's favorite hiding place is the join. Before this tick's fix, agent_performance.py indexed scores on the task field alone; scores filed with a descriptive task never matched a receipt filename and vanished from every aggregate — silently, because an inner join shows counts, never the unmatched remainder. The fix indexed on the tick field too, and the "coverage crisis" evaporated (22.4% → 100%). The operational form: any metric that triggers a rebuild gets a two-key audit first — re-derive the number through a different join path; if the paths disagree, the metric is the patient.

## MACHINE NOTE

{"sn": 1323, "category": "SYSTEM-DESIGN/MEASUREMENT-INTEGRITY", "evidence": "hidden_files/bin/agent_performance.py (fix: score index extended from task field to task+tick fields; scores whose task is a description, not a filename, were silently join-dropped); hidden_files/agent-performance/2026-10-14.md|.json (corrected today: 98 jobs, 98 scored, 100% coverage, avg 9.17, 34.7% >=9.5 — vs 22.4% pre-fix); MEMORY.md 2026-10-14 ~14:50 PDT ('AGENT PERFORMANCE CORRECTION': 'I almost \"fixed\" a healthy system. Lesson: verify the measurement before tuning the machine.')", "decision_change": "a metric that says 'rebuild the system' triggers an audit of the metric pipeline's joins/indexing FIRST; only after the measurement is re-derived through a second join path do you spend engineering on the system itself", "falsifier": "two independent measurement paths (different join keys, different code) agreeing the system is broken — then the metric is confirmed and the system is the patient", "mechanism": "silent inner-join drop: rows that fail the join key vanish from the aggregate without a trace; the dashboard then describes the surviving sample, not the population, and the bias is invisible because the UI shows counts, never the unmatched remainder", "cousins": ["SN-1028", "SN-1036"], "admission_gates": {"durable": true, "new": true, "signal": true, "evidence_backed": true}}

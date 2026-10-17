# SN-1524 — The Stall-Receipt Cap: One Identical-Stall Receipt Per Hour, Deltas Otherwise

Intelligent Block: SN-1524
Truth state: CANDIDATE
Scope: PRIVATE
Captured date: 2026-10-16 (19:08 PDT distillation tick)
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL

On 2026-10-16 the lane-executor filed SEVEN nearly identical gate-stall/seat-stall receipts in one day — 18:42, 18:43, 18:48 were three near-duplicates within six minutes, all saying the same thing: 30 briefs unclaimed, 28 Clarity-barred, queue unchanged. The lane-scorer graded the third near-duplicate 7.5/10 and named the fix the executor itself proposed: at most ONE gate-stall/seat-stall receipt per hour; if one exists within the last 60 minutes, log the stall delta to the memory log only and end. Adopted same hour via cron.update on the lane-executor body (scheduler reconciled). The discipline: identical filings are noise, the delta is the signal. A flooded feed trains every reader to ignore stall receipts — including the one that eventually carries a real change. The cap preserves signal-to-noise: one receipt per unchanged queue-state per hour, one line per tick otherwise. "A correct stall is a perfect run" stays true; it just doesn't need a new document to say so every five minutes.

## HUMAN NOTE

Imagine a security guard who radios "all quiet" every five minutes, all night, on a night when nothing happens. By 3 AM, nobody is listening to the radio anymore — so when something actually happens at 4 AM, the alert lands in a channel everyone's tuned out. The guard's job didn't change; the reporting cadence destroyed the channel. The fix isn't to stop patrolling (the ticks still run, the queue is still walked) — it's to report once per hour and note only what changed between reports. Same patrol, same honesty, but the radio stays trustworthy for the night something actually moves.

## CHILD NOTE

Imagine your little brother yells "Mom said no cookies!" every two minutes — even though Mom's answer hasn't changed. After the tenth time, nobody listens. Then one time Mom actually says "yes, one cookie" — and nobody hears it, because everyone's ignoring the cookie reports. The smart rule: say it once, and after that only speak up if the answer CHANGES. That's the cap. The guard still checks (he walks the whole queue every tick), he just doesn't file a whole new report when nothing moved — one line: "still the same, here's the tiny difference."

## GRANDMA NOTE

It's like a weather station that prints a full new weather report every five minutes on a perfectly calm day. You end up with a mountain of identical paper and you stop reading them — so the day a storm actually rolls in, the warning is buried under a pile of "clear skies" printouts. Nobody is asking the station to stop watching the sky. It should just print once an hour, and in between only note "wind picked up 5 mph." Same sky, same watching, but the paper pile stays readable and the storm warning gets seen.

## NAYA NOTE

Apply this everywhere a standing job files periodic status: (1) **identical-state cadence** — one receipt per 60 minutes per unchanged state; between receipts, a one-line delta in the memory log is the record. The worker still does the full scan (the 19:03 tick walked all 30 briefs in ORDERING order) — the scan is the work, the filing is the publication. (2) **the material-change escape** — the cap binds identical states only: queue shrinks, a brief gets claimed, a gate lifts, a new block reason appears → a fresh receipt is justified and expected. (3) **scorer reinforcement** — near-duplicate filings score down (the third-in-six-minutes scored 7.5/10), which is the enforcement signal to the writer: marginal value is scored, not just format. (4) **receipt ≠ proof of work** — seven receipts didn't mean seven times the verification; the delta lines in the memory log are equally on the record and cheaper to scan. (5) The falsifier: an identical-state tick whose hourly receipt carried information a delta line couldn't (e.g., a downstream consumer that reads receipts but never the memory log). If that consumer exists, name it and exempt it; otherwise the cap stands. Related: SN-1137 (one receipt per tick per lane) is the per-tick bound; this is the per-identical-state bound.

## MACHINE NOTE

```json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "duplicate_filing_noise",
  "evidence": {
    "event": "lane-executor 2026-10-16 filed 7 gate-stall/seat-stall receipts in one day (18:42 seat-stall, 18:43 gate-stall, 18:48 gate-stall — three near-duplicates within 6 minutes; then hourly under the cap).",
    "scorer": "lane-scorer 19:00 PDT tick scored the 18:48 receipt 7.5/10 ('third near-duplicate within 6 min + abbreviated scan evidence') and endorsed the executor's own one-per-hour cap proposal.",
    "adoption": "STALL-RECEIPT CAP implemented 2026-10-16 ~18:52 PDT via cron.update on the lane-executor body (scheduler reconciled): at most one gate-stall/seat-stall receipt per 60 minutes; otherwise log the stall delta to ~/memory/YYYY-MM-DD.md and end. Verified working: 18:55 and 19:03 ticks both correctly skipped filing (cap satisfied by the 18:48 receipt), logged deltas, ended.",
    "record": "~/memory/2026-10-16.md: GATE_STALL cap entry (~18:52 PDT), 18:55 and 19:03 quiet-run entries."
  },
  "rule": [
    "at most one stall receipt per 60 minutes for an unchanged queue state; between receipts, log a one-line delta to the memory log and end",
    "the full scan still runs every tick — the cap governs publication, not verification",
    "a material state change (queue shrinks, brief claimed, gate lifted, new block reason) re-opens the receipt window immediately",
    "duplicate filings score down: marginal value is scored, not just format"
  ],
  "lesson_line": "Identical filings are noise and the delta is the signal — cap identical-state receipts at one per hour so the channel stays trustworthy for the change that matters.",
  "applies_when": ["receipt", "lane-executor", "stall", "queue", "cadence", "signal-to-noise"],
  "enforcement": "STALL-RECEIPT CAP line in the lane-executor cron body (max one gate-stall/seat-stall receipt per 60 minutes, delta-to-memory-log otherwise) + lane-scorer downgrades near-duplicate filings (third near-duplicate scored 7.5/10 — the scored penalty is the writer's enforcement signal)."
}
```

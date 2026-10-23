Intelligent Block
Truth state: CANDIDATE
Scope: PRIVATE
Captured date: 2026-10-23
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

Scheduled Hub Deploy run 39990909081 (2026-10-23 16:56Z) FAILED: tools/hub_sync_heartbeat.py — HUB-SYNC LIVENESS ALARM, no heartbeat readable (Expecting value: line 1 column 1 char 0), exit 1; deploy SKIPPED. It was the repeat of the identical 11:59Z failure (run 39949936268). Root, pinned by the independent continuity audit (board #2793, comment 6370281593, 17:00Z): the file the alarm reads, HUB/sync-heartbeat.json, is a committed 1970 seed (cycle_ok:false) at 1ebcf8ae — a placeholder checked into the repo, never written by the running watcher. A liveness heartbeat is a freshness proof; static committed bytes carry no freshness, so the alarm fires on the seed forever and the deploy gate goes permanently red. Deploy is being skipped not because sync is dead, but because the oracle was never alive. Two edges to the lesson. First: a liveness signal must be written by the living process to a runtime location — never committed as a repo seed; a seed that nothing live overwrites is not a heartbeat, it is a fossil. Second: the alarm must distinguish "never written" (the oracle is missing — route to the publisher/writer owner) from "stale" (the writer died — route to the watcher owner); one undifferentiated "no heartbeat readable" names the wrong owner, and the wrong owner chases the wrong repair. The falsifier is authorship, not origin: a committed seed that the live watcher overwrites on every cycle is functionally live — what matters is who wrote the bytes last.

## 🩷 HUMAN NOTE

Shawn — the deploy gate keeps skipping the Hub deploy because the "heartbeat" it's reading was never a heartbeat. HUB/sync-heartbeat.json is a placeholder file that was committed to the repo back in the 1970 epoch — no running process ever writes to it. So the liveness alarm reads it, finds nothing fresh, and blocks the deploy. Twice today. The deploy isn't being skipped because sync is broken; it's being skipped because the thing proving sync is alive was never alive to begin with. The rule from here: a heartbeat must be written by the live process, not committed to the repo. And the alarm needs two different messages — "nobody ever wrote one" versus "the writer stopped" — because those are two different people who need to fix it.

## 🟣 CHILD NOTE

Imagine the nurse checks your temperature by reading yesterday's note on the whiteboard — "98.6°" — that someone wrote as an example before you arrived. You're never re-checked, so the board always says 98.6°, and nobody notices you're actually burning up. The example note was never a real reading. The fix: the nurse takes your temperature fresh every time and writes THAT on the board. A heartbeat works the same way — only a live process taking the reading counts.

## 🔵 GRANDMA NOTE

Think of a security guard who must check in by phone every hour. Instead of calling, someone left a recording of the guard saying "all clear" on the answering machine. The supervisor hears "all clear" every hour — from a recording made months ago. When real trouble comes, the recording still plays. That's what a committed seed heartbeat is: a recording, not a check-in. The guard has to make the call live, every time. And if the call never comes, you need to know whether the phone was never installed or the guard fell asleep — those are different problems for different people.

## 🟠 NAYA NOTE

For the lanes: hub-sync systemd unit is down by standing posture (no auto-reinstall — double-mint risk; Nitro's sync cron is the live writer per the 2026-10-21 verification). This note is about the oracle, not the unit. Whoever owns the deploy gate's liveness preflight: the heartbeat file must live on a runtime path written by the watcher process — HUB/sync-heartbeat.json as a repo-committed seed must be deleted or excluded from the alarm's read path; if the repo needs a placeholder for shape, it must be named as a seed (e.g. sync-heartbeat.SEED.json) and the alarm must refuse to read it. The alarm's failure modes need two codes: ORACLE_MISSING (file never written by a live process → route to the publisher/writer owner, here the Nitro sync lane + main-seat integrator per 6370281593) vs WRITER_STALE (freshness expired → route to the watcher owner). Until then, every "no heartbeat readable" fires the wrong playbook. This also supersedes the retired state.json-heartbeat doctrine (memory 2026-10-21: state.json belonged to the retired unit and is stale by design) — the current oracle is the seed file, and it was never live.

## 🟢 MACHINE NOTE

```json
{
  "slug": "sn-1883-heartbeat-written-by-living-process",
  "lesson": "A liveness heartbeat must be written by the living process to a runtime location — never committed as a repo seed. Scheduled Hub Deploy run 39990909081 (2026-10-23 16:56Z) FAILED: tools/hub_sync_heartbeat.py — HUB-SYNC LIVENESS ALARM, no heartbeat readable, exit 1; deploy SKIPPED (repeat of the 11:59Z failure, run 39949936268). Root (board #2793, 6370281593, 17:00Z, independent continuity audit): HUB/sync-heartbeat.json at 1ebcf8ae is a committed 1970 seed (cycle_ok:false), never written by the running watcher — a fossil, not a heartbeat. A heartbeat is a freshness proof; static committed bytes carry no freshness, so the alarm fires on the seed forever and the deploy gate goes permanently red: deploy skipped not because sync is dead but because the oracle was never alive. Second edge: the alarm must distinguish ORACLE_MISSING ('never written' → route to the publisher/writer owner) from WRITER_STALE ('freshness expired' → route to the watcher owner); one undifferentiated 'no heartbeat readable' names the wrong owner. Falsifier is authorship, not origin: a committed seed the live watcher overwrites every cycle is functionally live — what matters is who wrote the bytes last.",
  "applies_when": ["deploy", "liveness-gate", "heartbeat", "hub", "sync", "alarm", "oracle-design", "ops", "seed-file"],
  "enforcement": "The deploy workflow's liveness preflight must validate both freshness (heartbeat timestamp <= 600s) AND live provenance (the file is written by the watcher process to a runtime path, never a committed repo artifact): a heartbeat file committed to the repo that nothing live overwrites is treated as ORACLE_MISSING, not WRITER_STALE, and the repair route names the publisher/writer owner (here: Nitro sync lane + main-seat integrator per 6370281593). Any repo-committed placeholder the alarm reads must be renamed to a .SEED file the alarm refuses to read. Until the two-code alarm exists, 'no heartbeat readable' is routed to the writer owner, not the watcher owner.",
  "evidence": ["board #2793 comment 6370281593 (independent read-only GitHub continuity audit, 2026-10-23T17:00:54Z): 'P1 OBSERVABILITY/LIVENESS BLOCKER ... Scheduled Hub Deploy run 39990909081 (16:56Z) FAILED: tools/hub_sync_heartbeat.py — HUB-SYNC LIVENESS ALARM, no heartbeat readable (Expecting value: line 1 column 1 char 0), exit 1; deploy SKIPPED. REPEATED: same failure at 11:59Z (run 39949936268). Repo HUB/sync-heartbeat.json at 1ebcf8ae is a 1970 seed (cycle_ok:false), not a recent beat'", "owner action named in 6370281593: 'Nitro sync lane + main-seat integrator, NO competing lane'"]
}
```


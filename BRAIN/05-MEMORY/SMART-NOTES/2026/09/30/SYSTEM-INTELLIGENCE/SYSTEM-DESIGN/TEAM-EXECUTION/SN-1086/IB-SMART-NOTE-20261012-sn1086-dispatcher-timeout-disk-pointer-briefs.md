# The Dispatcher Died Generating Briefs — Dispatch Pointers, Not Prompts

**Intelligent Block:** IB-SMART-NOTE-20261012-sn1086-dispatcher-timeout-disk-pointer-briefs
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-12
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** MEMORY.md "DISPATCHER TIMEOUT ROOT CAUSE & FIX" (Shawn, 2026-10-12 ~07:40 PDT) — five consecutive dispatcher timeouts (t0322–t0362), each hitting the 900s cron limit; root cause: three 2,500-word brief prompts per tick (1,465-word template × filled variables) = ~7,500 words of prompt generation consuming the tick; t0362 died at step 6 of 7 (before rotation update), proving the spawn phase was the bottleneck. Fix (Experiment v3 — disk-pointer dispatch): write filled briefs to hidden_files/briefs/brief-{TICK}-lane{N}.md, spawn with a ~50-word pointer message; 12x smaller spawn prompts. Deployed 2026-10-12 07:41 PDT. Shawn's correction on the reporting: "find out why and fix it, don't bring me the problem."

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The Team Naya dispatcher spawns lane workers every tick on a 900-second cron budget. Five ticks in a row (t0322–t0362) timed out. The first instinct was to report the timeouts as a failed experiment — three reports went out, with zero root-cause investigation. Shawn's correction: don't bring him the problem; find out why and fix it.

The why: each tick constructed three 2,500-word brief prompts — a 1,465-word template filled per lane — roughly 7,500 words of prompt generation before a single worker spawned. Prompt construction is real work against a real clock, and it was eating the tick. Tick t0362 died at step 6 of 7, before the rotation update — the death location *was* the diagnosis: the spawn phase was the bottleneck, not the lane work.

The fix (Experiment v3, disk-pointer dispatch): write each filled brief to disk at `hidden_files/briefs/brief-{TICK}-lane{N}.md` and spawn with a ~50-word pointer message ("read the brief at [path], execute it"). Twelve times smaller spawn prompts. Deployed 2026-10-12 07:41 PDT.

The durable rules: **(1) a timeout's death location is its diagnosis** — note which step the tick died at before theorizing; **(2) the spawn channel carries addresses, not payloads** — anything destined for a spawned worker that exceeds a couple hundred words belongs on disk with a pointer; **(3) a repeated timeout is a root-cause assignment, not a report** — reporting "experiment failed" three times without investigating is the failure; fix first, report after (standing law #8; the loop-breaker law).

## 🩷 HUMAN NOTE

Shawn — a small, expensive infrastructure lesson from this morning's dispatcher. Five ticks in a row hit the 15-minute cron limit and died. My first instinct was to report it as a failed experiment; you corrected me: find out why and fix it, don't bring me the problem. The why turned out to be embarrassingly mechanical — each tick was generating ~7,500 words of brief prompts before spawning anyone, and the prompt generation itself was eating the clock. The fix: write the briefs to disk and hand each worker a 50-word pointer instead. Twelve times smaller, deployed at 07:41. The rule for the brain: when a tick times out, the step where it died IS the diagnosis — and a repeated timeout is never just a report, it's a fix waiting to happen.

## 🟣 CHILD NOTE

Imagine a teacher who, before every class, hand-writes a three-page letter to each student explaining the lesson — and the bell rings before anyone has read page one. Classes keep "failing" but the teaching isn't the problem; the letter-writing is. The fix is simple: tape the lesson to the classroom wall once, and just say "read the wall." That's what the team learned: when you send someone to do work, don't send the whole instruction book inside the message — save it somewhere and send the address.

## 👵 GRANDMA NOTE

It's like a restaurant where the head chef insists on reading the entire recipe book aloud to each cook before dinner service — the kitchen runs out of time before a single dish is started, night after night. The recipes aren't the problem; reading them aloud every time is. Write the recipes down once, keep them on the shelf, and hand each cook a page number. Any system that dispatches work by regenerating the full instructions inside every handoff will eventually spend its whole budget on instructions and none on the work.

## 🤖 NAYA NOTE

For every future dispatcher, orchestrator, and lane spawner: prompt construction is work, and it bills against the same clock as the real work. When a tick times out, do not theorize first — record the step where it died; that step is the bottleneck until proven otherwise. Then move the bulk out of the spawn channel: the filled brief lives at `hidden_files/briefs/brief-{TICK}-lane{N}.md`, and the spawn message is ~50 words pointing at it. And the posture rule, straight from Shawn: a timeout that repeats is a root-cause assignment, not a status report. "Experiment failed" said three times with zero investigation is the loop-breaker violation — spot the loop, stop the loop, fix it, report the fix. The dispatcher that reports its own timeouts instead of autopsying them is a reporter, not a machine.

## ⚙️ MACHINE NOTE

```json
{
  "sn": "SN-1086",
  "lesson": "dispatcher-timeout-disk-pointer-briefs",
  "rule": "A tick's death location is its diagnosis; the spawn channel carries addresses, not payloads — write filled briefs to disk and spawn with a ~50-word pointer; a repeated timeout is a root-cause assignment, never just a report.",
  "failure_class": "spawn-channel-bloat",
  "evidence": {
    "timeouts": "five consecutive dispatcher timeouts t0322-t0362, each hitting the 900s cron limit",
    "root_cause": "three 2,500-word brief prompts per tick (1,465-word template x filled variables) = ~7,500 words of prompt generation consuming the tick",
    "death_location_diagnosis": "t0362 died at step 6 of 7, before the rotation update — the spawn phase was the bottleneck",
    "fix": "Experiment v3 disk-pointer dispatch: briefs written to hidden_files/briefs/brief-{TICK}-lane{N}.md; spawn message ~50 words; 12x smaller",
    "deployed": "2026-10-12 07:41 PDT",
    "correction": "Shawn: 'find out why and fix it, don't bring me the problem' — three 'failed experiment' reports with zero investigation were the failure"
  },
  "repair": "disk-pointer dispatch (briefs on disk, pointer in spawn); death-step recorded on every timeout before any theory",
  "related": ["SN-0326 (delegation-timeout-direct-execution — same timeout family, different mechanism)"]
}
```

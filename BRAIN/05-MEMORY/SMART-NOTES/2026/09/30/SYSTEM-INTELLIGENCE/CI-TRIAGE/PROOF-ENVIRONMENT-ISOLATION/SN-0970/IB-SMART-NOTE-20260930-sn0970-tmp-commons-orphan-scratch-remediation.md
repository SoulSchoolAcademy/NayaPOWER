# The /tmp Commons — Orphaned Scratch Across Lanes Fills the 512M tmpfs; Relocate, Never Delete

**Intelligent Block:** IB-SMART-NOTE-20260930-sn0970-tmp-commons-orphan-scratch-remediation
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-11
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** night-shift receipts t0237-a, t0237-b §7, t0242-c (2026-10-11 ~02:37–02:55 PDT). At ~02:40 PDT /tmp (512M tmpfs) hit 100% full — orphaned night-shift scratch dirs (npw 138M, napw 76M, npw-main 64M, gate-src 15M) from earlier lanes' git clones/fetches — and two workers' git fetches died with "No space left on device". Worker t0242-c swept it: after `fuser -m /tmp` and `lsof +D /tmp` showed no live handles, relocated 293M by `mv` (never `rm`) into the goal workspace (`hidden_files/tmp-archive-2026-10-11/`); deliberately LEFT sn-taxonomy.git (41M, mtime 02:39 — a sibling tick spawned at the same time, could be in flight) and diag (17M, dir touched 7 min prior) per "when in doubt, leave it"; df after: 88M used, 425M free; smoke-tested a fresh `git fetch --depth 1` of NayaPOWER in /tmp — rc=0 — then removed only the smoke dir.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

SN-0341 taught one harness to size its own scratch against the 512M /tmp tmpfs. Tonight's failure was different: no single lane oversized — four lanes' *orphaned* scratch accumulated until the tmpfs hit 100%, and two unrelated workers' git fetches died with "No space left on device" hours after the culprits had finished. Shared scratch is a commons: sizing your own share is necessary but not sufficient, because the tmpfs fills from the sum of every lane's leftovers. The remediation was mechanical and reversible: verify no live handles (fuser, lsof), move — never delete — the orphans into the goal workspace archive, leave anything recently touched or possibly in flight, and smoke-test the fix with a real fetch. The lesson: **treat /tmp as a shared commons with a cleanup protocol, not as free private scratch** — do your heavy scratch in the goal workspace, clean your own dirs in the same tick that creates them, and when sweeping others' orphans, relocate reversibly and attribute before you touch.

## 🩷 HUMAN NOTE

Think of /tmp like the shared break-room fridge. SN-0341 was the lesson "don't put a whole catering tray in the fridge" (one harness's 585MB of clones). Tonight's incident was four people each leaving a small container that nobody threw out — until the fridge door wouldn't close and two other people couldn't store their lunch. The fix wasn't throwing everything away (one of those containers might have been someone's active lunch — the 41MB sn-taxonomy.git from a sibling tick). It was: check nobody's eating right now (fuser/lsof), move the leftovers into labeled bags on the shelf (mv into the archive), leave anything warm to the touch, and test the fridge door closes. On a machine where many workers share 512MB of tmpfs, the fridge fills from the sum of everyone's leftovers — so everyone cleans their own container the same day they use it, and whoever sweeps moves, never deletes.

## 🟣 CHILD NOTE

Imagine a toy box that holds exactly 512 blocks. Four kids each left some blocks inside and walked away. When two other kids tried to put their blocks in, the box was full — and none of them knew whose blocks were whose. A helper checked: nobody was playing with the box right now (no open handles), so she carefully moved the leftover blocks into labeled bags on the shelf (move, don't throw away!) — because one pile might belong to a kid who's still playing. Then she tested: put blocks in, take blocks out — works. The rules: play in your own room when you can (goal workspace scratch), put your blocks away when you're done, and never throw away someone else's blocks — move them gently.

## 🔵 GRANDMA NOTE

Picture a community hall closet that everyone shares — small, and anything left inside stays until someone moves it. Four groups left their equipment in there after their meetings. When the evening group arrived, the closet was jammed and they couldn't get their things in. The caretaker's approach was sensible: first check nobody was actually using the closet (no live use), then carry the leftovers to a labeled storage room — never the dumpster, because one group's gear was from a meeting that had just started. Leave anything you're not sure about. Then test the door opens. That's the whole protocol: a shared space needs shared tidiness — do your big work in your own room, tidy up after yourself the same day, and if you must clear someone else's things, relocate them gently and label them, never discard.

## 🟠 NAYA NOTE

Apply this on every worker brief and every cleanup action: (1) **heavy git scratch goes in the goal workspace, not /tmp** — clones and fetches are the heaviest scratch; /tmp's 512M is a commons shared by all lanes, and the failure mode is accumulation, not one big write; (2) **clean your own scratch in the tick that creates it** — orphaned `npw`/`napw`/`npw-main` clones were 280M+ of tonight's fill, all from lanes that had finished hours earlier; (3) **when sweeping others' orphans: verify, then relocate, never delete** — `fuser -m /tmp` + `lsof +D /tmp` + `ps` to rule out live use, attribute by contents+mtime, `mv` into `hidden_files/tmp-archive-<date>/`, and leave anything recently touched or plausibly in flight (tonight: sn-taxonomy.git 41M and diag 17M stayed); (4) **smoke-test the fix** — a fresh `git fetch --depth 1` proving rc=0 before declaring the blockage cleared. Cousin: SN-0341 (single-harness sizing — this note is the multi-lane commons + remediation protocol it didn't cover).

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "shared_tmpfs_commons_fills_from_accumulated_orphans",
  "evidence": {
    "incident": "receipts t0237-a (blocker: first git fetch died 'No space left on device'), t0237-b §7 (same failure, relocated own scratch to ~/workspace/prwatch-tmp) — /tmp 512M tmpfs 100% full at ~02:40 PDT 2026-10-11",
    "culprits": "npw 138M, napw 76M, npw-main 64M, gate-src 15M — orphaned night-shift git clones, all idle 30–89 min, owners finished",
    "remediation": "receipt t0242-c: df before 379M used/134M free; fuser+lsof+ps → no live handles; mv (never rm) 293M into hidden_files/tmp-archive-2026-10-11/; deliberately left sn-taxonomy.git 41M (mtime 02:39, sibling tick in flight) and diag 17M (dir touched 02:37); df after 88M used/425M free; smoke test git fetch --depth 1 rc=0",
    "cousin": "SN-0341 covered single-harness sizing (585MB clones vs 512M); this incident is multi-lane accumulation with zero oversize offenders"
  },
  "rule": [
    "do heavy git scratch (clones, fetches) in the goal workspace, never /tmp",
    "clean your own scratch dirs in the tick that creates them",
    "when sweeping others' orphans: fuser/lsof/ps first to rule out live use, attribute by contents+mtime, mv into hidden_files/tmp-archive-<date>/ — never rm",
    "leave anything recently touched or plausibly in flight ('when in doubt, leave it')",
    "smoke-test the remediation with a real git fetch (rc=0) before declaring the blockage cleared"
  ],
  "lesson_line": "Shared /tmp is a commons that fills from the sum of every lane's leftovers — do scratch in the workspace, clean your own the same tick, and when sweeping others' orphans verify-no-live-use, relocate never delete, leave the uncertain, and smoke-test."
}
~~~

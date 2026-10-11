# Tell Your Watchers About Your Pushes — Planned Writes Read as Anomalies

**Intelligent Block:** IB-SMART-NOTE-20260930-sn0971-tell-your-watchers-about-your-pushes
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-11
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** night-shift receipts t0242-b (head-watch, 2026-10-11 02:44–02:54 PDT) and t0254-a (re-anchor, 02:54–02:58 PDT). t0242-b's scheduled head-watch caught the Smart Notes carrier branch (`naya4/smart-notes-2026-09-30`) at `9db43855`, up from the pinned `a64518ca7f50`, and flagged it: "Dormancy is broken — the 9th push landed", declared all head-pinned verdicts stale per SN-0493, and ordered a full re-anchor. t0254-a's re-anchor proved the delta was exactly two commits — `7bbb1dfe` "docs(smart-notes): add SN-0968 (CANDIDATE)" and `9db43855` "docs(smart-notes): add SN-0969 (CANDIDATE)" — the Smart Note distillation loop's own scheduled staging pushes from the 02:38 tick, 5 minutes before the watcher's first read. The "anomaly" was a sibling lane's planned write, unknown to the watch brief; the watcher's honesty (bounded movement window, exact SHAs, "inference not direct observation") was exemplary — the brief's knowledge was not.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

A head-watcher did everything right: three scheduled reads, exact SHAs, bounded the movement window honestly, declared prior verdicts stale per SN-0493, and ordered a re-anchor. The work was wasted anyway — the "9th push" that broke dormancy was the Smart Note loop's own scheduled staging of SN-0968/SN-0969, five minutes before the watcher's first read. The watcher couldn't know that because its brief listed pin baselines but not the branch's writer lanes or their cadences. The lesson: **a watch on a shared branch must be write-aware of its sibling lanes, or every planned write reads as an anomaly and burns a re-anchor cycle.** Dispatchers: annotate watch briefs with who writes to the branch and when (the smart-note loop stages every ~30 min onto #1825). Watchers: before declaring an anomaly, attribute the new head — `git log` author, commit message, and known schedules explain most movements. Planned writes never burn a re-anchor cycle; re-anchor baselines against the known write, not against surprise.

## 🩷 HUMAN NOTE

Imagine a security guard watching a warehouse door. Every hour he logs "no movement — all quiet." One night at 2:44 he sees the door has been opened: new boxes inside, moved from where the manifest says they should be. He does everything right — logs the exact time, photographs everything, declares the old inventory stale, orders a full re-count. Then the morning shift arrives and says: "That was us. We restock every night at 2:40. The manifest was written before our shift started." The guard was flawless; the briefing was missing one line: "the night crew restocks at 2:40." On a shared branch, the watch brief is the guard's briefing — it must say who is allowed to open the door and when, or every scheduled restock becomes a security incident.

## 🟣 CHILD NOTE

Imagine you and your sister both keep toys in the same box. You check the box every hour and write down "nothing moved." Then one hour you open it — new toys inside! You shout "someone messed with the box!" But it was your sister: she puts her toys away every day at the same time, and nobody told you. You did your checking job perfectly — you just didn't know her schedule. The fix is simple: whoever gives you the checking job should also tell you who else uses the box and when. Then when you see new toys, you can say "that's sister's 2:40 put-away" instead of "mystery!"

## 🔵 GRANDMA NOTE

Think of the building superintendent who walks the halls every hour noting "all quiet." One round she finds a tenant's door open and furniture moved. She follows procedure perfectly — records everything, declares the old floor plan outdated, orders a re-inspection. Then the tenant says: "My movers come every Tuesday at 2:40 — it's on the building schedule." She was right to notice and right to record; she was only missing the schedule. The building schedule is what the watch brief is for a shared branch: it has to list everyone who has a key and when they come, or the superintendent will treat every scheduled visit as a break-in.

## 🟠 NAYA NOTE

Apply this on every head-watch dispatch and every shared-branch watch brief: (1) **name every writer lane and its write cadence in the brief** — pins alone are not enough; the #1825 brief listed `a64518ca7f50` as the pin but not that the smart-note loop stages onto the same branch every ~30 min; (2) **attribute before alarming** — on movement, run `git log <old>..<new>` and read author + commit message before declaring anomaly; `7bbb1dfe` and `9db43855` both said "docs(smart-notes): add SN-09xx (CANDIDATE)" — the attribution was in the bytes; (3) **dispatchers annotate expected-write windows** — "smart-note loop stages SN-09xx onto this branch at ~:08/:38 each hour" costs one line and saves a full re-anchor cycle; (4) **re-anchor against the known write, not against surprise** — t0254-a did the re-anchor correctly anyway (exact SHAs, start+end pins); the waste was needing it at all for two docs-only commits whose content was never in question. The watcher's honesty discipline (bounded window, "inference not direct observation") stays; add lane-awareness on top. Cousin: SN-0493 (re-verify at action time — this note is its scheduling corollary: know whose actions move the tip).

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "watch_baseline_stale_from_unknown_sibling_lane_write",
  "evidence": {
    "watch": "receipt t0242-b (02:44–02:54 PDT): three ls-remote reads of 7 refs; #1825 moved a64518ca7f50 → 9db4385501c8b6b45b6cad37a786f491c77203b3; flagged 'Dormancy is broken — the 9th push landed'; declared prior verdicts stale per SN-0493; ordered re-anchor",
    "attribution": "receipt t0254-a (02:54–02:58 PDT): git log a64518ca7..9db43855 → exactly 2 commits: 7bbb1dfe 'docs(smart-notes): add SN-0968 (CANDIDATE)', 9db43855 'docs(smart-notes): add SN-0969 (CANDIDATE)' — the smart-note loop's own 02:38 tick staging pushes, 5 min before the watcher's first read",
    "gap": "the watch brief carried pin baselines but no writer-lane schedule for the shared carrier branch"
  },
  "rule": [
    "name every writer lane and its write cadence in every head-watch brief on a shared branch",
    "on movement, attribute the new head first (git log author + commit message + known schedules) before declaring anomaly",
    "dispatchers annotate expected-write windows in watch briefs ('smart-note loop stages SN-09xx onto #1825 at ~:08/:38 hourly')",
    "re-anchor baselines against the known write, not against surprise — planned writes never burn a re-anchor cycle"
  ],
  "lesson_line": "A watcher that doesn't know its sibling lanes' write schedules will classify every planned push as an anomaly — tell your watchers about your pushes."
}
~~~

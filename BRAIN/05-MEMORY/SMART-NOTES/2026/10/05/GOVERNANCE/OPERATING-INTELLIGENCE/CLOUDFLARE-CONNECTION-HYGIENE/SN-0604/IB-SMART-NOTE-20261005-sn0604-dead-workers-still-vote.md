# Dead Workers Still Vote — Cloudflare Connection Hygiene

**Intelligent Block:** IB-SMART-NOTE-20261005-sn0604-dead-workers-still-vote
**Truth state:** CANDIDATE
**Scope:** ALL_SEATS
**Captured:** 2026-10-05
**Source:** Shawn Vibert (director law)
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

A Cloudflare Worker wired to a GitHub repo keeps building on every push until its wire is cut — an unused account is not a disconnected account. Seventeen forgotten workers posted 17 failing checks on every push, burying the real signal. Only current, relevant workers stay connected. Everything else gets unwired immediately.

## 🩷 HUMAN NOTE

Shawn thought his old Cloudflare workers were harmless because he wasn't using them anymore. They weren't harmless. Every one of them was still connected to the code, and every time anyone pushed anything, all seventeen woke up, tried to build, failed, and stamped a red X on the work. The team couldn't see what was really passing because seventeen ghosts were screaming on every commit.

The lesson he wanted recorded: a worker you connected long ago doesn't stop just because you stopped thinking about it. The wire stays live until someone cuts it. So the rule is simple — if a worker isn't current and relevant right now, unwire it right now. Don't keep it "just in case." "Just in case" costs seventeen red X's on every push.

He deleted all seventeen himself, and the very next test push came back clean.

## 🟣 CHILD NOTE

Imagine you plugged seventeen old lamps into the wall years ago and forgot about them. Every time someone flips the light switch, all seventeen lamps buzz loudly — even the ones in rooms nobody uses. Flipping the switch doesn't know which lamps you still want. The only way to stop the buzzing is to unplug each lamp. That's what Shawn did: he unplugged all seventeen, and now the house is quiet.

## 🟢 GRANDMA NOTE

Shawn had seventeen old website-projects still connected to his code from years ago. Every time new code went in, all seventeen tried to build it and failed — like seventeen old alarms going off every time someone opened the front door. He didn't know they were still connected. Now there's a house rule: only the projects you're actually using stay connected. The rest get unplugged right away.

## 🟠 NAYA NOTE

Unused ≠ disconnected. A Cloudflare Worker's GitHub repo connection persists until explicitly removed (Settings → Builds → Disconnect repository) or the worker is deleted. Every push notifies every connected worker regardless of account activity, age, or relevance. Audit connected workers the way you audit open gates: if it isn't current and relevant, cut the wire now. Never retain a connected worker "just in case" — the cost is CI signal buried under stale failures.

Proven 2026-10-05: 17 stale workers across two forgotten Cloudflare accounts removed by Shawn; test push returned zero Cloudflare "Workers Builds" checks (was 17).

## 🔵 MACHINE NOTE

~~~json
{
  "smart_note_id": "SN-0604",
  "intelligent_block": "IB-SMART-NOTE-20261005-sn0604-dead-workers-still-vote",
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "law": "DEAD_WORKERS_STILL_VOTE",
  "statement": "A Cloudflare Worker connected to a GitHub repository continues to build on every push until its repository connection is explicitly disconnected or the worker is deleted.",
  "mechanism": "GitHub push events notify every connected worker via the Cloudflare GitHub App; workers do not evaluate push relevance. Connection state is per-worker and persists independent of account activity.",
  "rule": "Only Cloudflare workers/deployments that are current and relevant remain connected to the repository. Any worker that is not current gets its Git connection removed (or the worker deleted) immediately. Never retain a connected worker 'just in case'.",
  "false_assumption_killed": "Not using a worker/account means it has no effect.",
  "evidence": {
    "date": "2026-10-05",
    "repo": "SoulSchoolAcademy/NayaPOWER",
    "stale_workers": 17,
    "accounts": ["262c881746ea6e9978ca18b3eb831907", "5884e9baffa56750e2924983ce0ef962"],
    "check_app_slug": "cloudflare-workers-and-pages",
    "verification": "throwaway-branch push test: 17 checks -> 0 checks after removal",
    "removed_by": "Shawn Vibert"
  },
  "scope": "ALL_SEATS",
  "source": "Shawn Vibert, 2026-10-05"
}
~~~

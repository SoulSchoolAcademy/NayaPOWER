# Intelligent Block — Smart Note

- **Intelligent Block:** SN-1416
- **Truth state:** CANDIDATE
- **Scope:** PRIVATE
- **Captured:** 2026-10-15
- **Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
- **Kind:** LESSON (L420, family F1)

## IN A NUTSHELL

A venue rotation isn't done when the override is posted — it's done when every posting path has verified the override. The #2537 → #2641 migration wired its override into 22 scheduled-job definitions in 2 minutes, yet dispatch, sign-ins, and sign-outs kept posting to the old venue for 34–66 minutes after the migration. Two live venues, one team. Verify the override on every posting path, or the old venue keeps emitting.

## HUMAN NOTE

When a team's shared board moves, nobody means to keep posting to the old one — but they do anyway, because the old address lives in more places than the announcement reaches. On 2026-10-15 the migration from board #2537 to #2641 was announced at 16:15:50Z, and within two minutes all 22 scheduled jobs were re-pointed. But the wave-198 dispatch — plus its sign-ins and sign-outs — ran on the dead #2537 for over an hour after the move, while the night-shift lanes were already posting on #2641. The same run's own announcements landed on #2537 43 minutes post-migration (owned; they stand). The override touched the job definitions but not the dispatch path, the event router (still reading directive #2601's venue references), or the standing pipelines reading frozen body text.

The rule from here on: a venue rotation verifies its override on every posting path. The first post-migration dispatch names the live venue explicitly. During the migration window, deconfliction spans both venues. Venue rotations ship as override metadata, never as per-body edits.

## CHILD NOTE

Imagine your class moves to a new room. The teacher tells everyone, and someone even puts a sign on the new door. But a few kids keep going to the old room anyway — because their map still shows the old room, and nobody checked *their* map. That's what happened: the team moved to a new board, but some of the helpers kept posting to the old one because their instructions still had the old address. Lesson: when you move, check EVERY helper's instructions — not just the main sign.

## GRANDMA NOTE

Honey, when the office moved to a new building, they put a notice up — but half the mail kept going to the old address because some folks never got the memo. Same thing here: the team's message board moved, and some messages kept landing at the old spot for over an hour. The lesson the family wrote down: whenever you move the board, you have to check every single path where a message could be sent — not just the obvious ones.

## NAYA NOTE

This is the F1 family again (stale-venue emission), now with a mechanical shape. Three independent readers each had their own copy of the venue: (1) scheduled-job definitions — overridden in 2 min via L313's override-metadata pattern; (2) the event-router dispatch path — reading directive #2601's venue references, NOT overridden; (3) standing pipelines — reading frozen body text, NOT overridden. The migration (6196761341, 16:15:50Z) was an event; the override (6196798397, 16:17:38Z) was metadata; the dispatch was a reader that never re-read. The repair that landed in AGENTS.md the same run: verify the override on every posting path; first post-migration dispatch names the live venue; deconfliction spans both venues during the window. Note the asymmetry that makes this durable: writers push, readers cache — every reader with a cached venue is an independent posting path that must be enumerated and re-verified. Enumerate posting paths BEFORE announcing the migration, not after the first stale post.

## MACHINE NOTE

```json
{
  "sn": "SN-1416",
  "lesson_id": "L420",
  "family": "F1",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-15",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "title": "A venue rotation verifies its override on every posting path, or the old venue keeps emitting",
  "evidence": {
    "lesson_posted": {"board": "#2641", "comment_id": 6198852344, "posted_at_utc": "2026-10-15T18:03:30Z"},
    "migration": {"from": "#2537", "to": "#2641", "comment_id": 6196761341, "at_utc": "2026-10-15T16:15:50Z"},
    "override_wired": {"comment_id": 6196798397, "at_utc": "2026-10-15T16:17:38Z", "targets": 22, "what": "scheduled-job definitions"},
    "stale_emissions": "wave-198 dispatch + sign-ins + sign-outs ran on #2537 for 34-66 min post-migration; night-shift lanes already on #2641",
    "own_miss": "this run's own step-0 announcements landed on #2537 43 min post-migration (owned, stands)",
    "promoted": "AGENTS.md same run"
  },
  "rule": "verify the override on every posting path; the first post-migration dispatch names the live venue; deconfliction spans both venues during the window; venue rotations ship as override metadata, never per-body edits",
  "mechanism": "posting paths are independent readers with cached venues (job definitions, event router reading directive #2601 references, pipelines reading frozen body text); overriding one reference does not propagate to other readers; each must be enumerated and re-verified",
  "falsifier": "a future rotation that verifies the override on every enumerated posting path yet still produces a stale-venue post -> the enumeration was incomplete (a path was missed); a clean rotation with zero stale posts supports the rule",
  "decision_changed": "every future venue rotation executes against an enumerated posting-path checklist; the migration announcement names the live venue for dispatch; deconfliction watches both venues during the window",
  "related": ["F1 family (stale-venue emission)", "L313 (override metadata pattern)", "SN-1218 (successor carries the chain)", "SN-986 (hard-coded venue silent break)"]
}
```

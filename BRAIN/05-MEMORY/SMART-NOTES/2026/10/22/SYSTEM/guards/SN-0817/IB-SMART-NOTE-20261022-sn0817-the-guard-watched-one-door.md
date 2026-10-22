# The Guard Watched One Door

**ID:** IB-SMART-NOTE-20261022-sn0817-the-guard-watched-one-door
**Created:** 2026-10-22 00:40 UTC
**Category:** SYSTEM / guards

## IN A NUTSHELL

We cured the feed the right way: the false trigger dropped, a delete-guard installed and verified three ways, all 341 notes restored with zero errors. Minutes later the table was gutted a fourth time — through a path the guard could not see. A BEFORE DELETE trigger governs the DELETE statement and nothing else: a TRUNCATE fires no delete triggers, DDL can disable or drop any guard, and a session that knows the maintenance flag passes politely. The guard was real. The guard was proven. The guard watched one door of a house with four.

## HUMAN

Imagine hiring a guard for your front door, checking his credentials three ways, watching him work — and that same night someone walks in through the garage, because nobody counted the garage as a door. The guard didn't fail at his post. The plan failed at the map: we protected the path we had seen used, not every path that exists.

Security is a census, not a trophy. The question is never "is there a guard?" It's "have we named every way in, and is each one closed, alarmed, or honestly declared open?" Until that list exists, "guarded" is a hope wearing a uniform.

## CHILD

Locking your bedroom door is good. But if the window is open, the lock didn't keep anyone out. Before you say "my room is safe," walk around and check every way in.

## GRANDMA

In my day we locked the house at night — all of it, not the door we used most. A chain on one door and an open window out back is not a locked house; it's a story we tell ourselves so we can sleep. Count the doors. Then lock them.

## NAYA

The anatomy, for the record. (1) The cure's step 2 revoked DELETE on `hub_smart_notes` from `service_role` and installed BEFORE DELETE trigger `hub_smart_notes_delete_guard`, raising unless the session sets `naya.feed_maintenance='on'`. It was verified three ways with a probe row: delete without the flag raised, delete with the flag succeeded, grants read-back proved the revoke. (2) Restore #3 then completed at 341 rows, 0 errors, essence fingerprint identical, all live proofs green. (3) Between ~00:08Z and ~00:12Z the restored rows were removed a fourth time and the dropped essence-only trigger was re-created byte-identical. The guard trigger stood present, enabled, and byte-intact afterward; `service_role`'s DELETE was never re-granted. (4) Three privileged mechanisms fit every observation and the catalog cannot distinguish them: TRUNCATE (fires no DELETE triggers; both `postgres` and `service_role` hold it — the cure's scope covered DELETE only), a flagged DELETE session, or disable/drop/delete/re-create. Nu named them as hypotheses, not findings — that discipline is part of the lesson. (5) The standing repair that DID land: the sync watchdog now alarms within five minutes if the essence-only trigger re-appears — an alarm on the actor's signature, since a lock on one door was proven insufficient. The deeper cure is above this seat: the privileged channel itself must be re-scoped, and that decision belongs to Shawn.

## MACHINE

Rules: (1) GUARD DESIGN — before installing any guard, enumerate EVERY operation class that can reach the protected state (for a table: DELETE, TRUNCATE, UPDATE of the guarded columns, DDL on the object, owner/superuser sessions, flag-holding sessions) and for each class record its disposition: BLOCKED, ALARMED, or DECLARED-OPEN with a named reason. (2) CLAIMS — a surface may be called "guarded" only against the enumerated list; an unenumerated path voids the claim silently, so the claim always names its scope. (3) ALARMS COMPLEMENT LOCKS — for every DECLARED-OPEN privileged path, an independent detector watches the protected state's signature (row counts, catalog fingerprints) on a short cadence. (4) VERIFY THE BYPASS CLASS — a guard's proof includes at least one test from OUTSIDE the guarded operation class (e.g., for a DELETE guard: attempt the TRUNCATE path in a safe probe) or an explicit statement that the class remains open. (5) STOP RULE — when a guard is defeated, do not re-run the same cure louder; escalate to the channel that defeated it.

## THE DECLARED BEHAVIOR CHANGE

From tonight, when I design, install, or describe any guard, I first write the full list of paths that can reach the protected state, and I give each path a disposition — blocked, alarmed, or declared open with its reason — before I call anything protected. I will not again say "guarded" on the strength of the one path I happened to watch, and when a guard is defeated I will escalate to the channel instead of re-running the cure.

## WHAT IT ALL MEANS

The system keeps learning the same shape of lesson in different costumes: the single checked path is never the whole surface. Verification theater — proving the door you locked — feels like rigor and is not. The census habit is the rigor: enumerate first, then guard, then alarm what you cannot close. Applied everywhere, this turns security from a collection of locks into a map that can actually be defended.

## WHAT'S IN IT FOR YOU

For Shawn: when we tell you something is protected, you'll be able to ask "against what, exactly?" and get a list, not a feeling — including the honest list of what remains open and whose decision closing it is. For every Naya: you inherit guards whose limits are written on them, so you never lean your weight on a lock that was only ever watching one door.

## HOW IT APPLIES

In force now on my lane: the feed carries a trigger tripwire (alarm live), the delete-guard stands with its scope stated, and the remaining open path — the privileged channel — sits named on Shawn's decision list rather than papered over. Every future guard I ship carries its path census in its report, or it doesn't ship.

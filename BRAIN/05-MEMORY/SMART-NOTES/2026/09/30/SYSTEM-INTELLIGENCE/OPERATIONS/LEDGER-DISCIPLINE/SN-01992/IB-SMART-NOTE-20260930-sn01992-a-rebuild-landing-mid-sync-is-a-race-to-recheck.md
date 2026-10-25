**Intelligent Block:** IB-SMART-NOTE-20261025-sn1992-a-rebuild-landing-mid-sync-is-a-race-to-recheck
**Smart Note:** SN-1992
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-25
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** shared-state director_tick_20261025_1012z (2026-10-25T10:12Z) and director_tick_20261025_1438z (2026-10-25T14:38Z). No #1354 fetch this tick (cheap-check skip: #1354 capped at 2,500 comments, commenting disabled).

## ✦ IN A NUTSHELL
A rebuild landing mid-sync is a race to re-check, not a failure. The 2026-10-25 10:12Z director tick pushed the ledger files, then found the dispatcher had rebuilt those same files at 10:10:58Z mid-sync — same sizes, changed bytes. The tick did not file a failure; it ran a re-check pass that pushed the rebuilt bytes blob-verified, and the writer hash held stable across both passes. The mechanism is two writers on one cadence: the sync's read-then-write window lets a rebuild land between GET and PUT, so the bytes pushed are stale on arrival — a timing overlap, not corruption. The rule: every sync push ends with a post-push re-check of live bytes against pushed bytes; a mismatch opens a re-push + re-verify pass, and only a mismatch that survives the re-check pass is reported as a failure. The 14:38Z tick shows the discipline working the other way too: a dispatcher rebuild at 14:31Z was captured before the sync, so no mid-sync race occurred at all — the race is a property of the window, and the window is checkable.

## 🩷 HUMAN NOTE
Imagine two cooks sharing one recipe book. You copy the soup page, walk to the printer, and print it — but while you were walking, the other cook rewrote the page. Your printout is now out of date, but nothing is broken: nobody made a mistake, the two of you just crossed paths in time. The wrong move would be to shout that the book is corrupted. The right move is to walk back, look at the page again, and print the new version — and only shout if the second printout still doesn't match. That second look is the whole lesson: a mismatch right after a push is first a question ("did someone rewrite mid-walk?"), and only after the second look fails does it become a failure.

## 🟣 CHILD NOTE
Imagine you and your friend both draw on the same whiteboard. You take a photo of the board, walk away, and while you're gone your friend adds a new drawing. Your photo is now old — but the board isn't broken, and your friend didn't do anything wrong. You just need to take a second photo. If the second photo matches the board, everything is fine. Only if the second photo STILL doesn't match do you have a real problem. The rule is: always take the second photo before you say something is wrong.

## 🔵 GRANDMA NOTE
Dear, this one is about not crying wolf when two workers cross paths. The director's job each tick is to copy the ledger files up to the record. The dispatcher's job, on its own schedule, is to rebuild those same files. On the morning in question the rebuild landed right in the middle of the director's copy — after it had read the files, before it had finished writing them. So what got written was already old the moment it landed. The director did the sensible thing: it looked again, saw the rebuilt files, wrote those instead, checked them byte for byte, and confirmed the writer's fingerprint matched across both passes. Only if that second look had still disagreed would there have been a real failure to report. The standing rule is plain: after every push, look again; a mismatch first means "re-check," and only a mismatch that survives the re-check means "failure."

## 🟠 NAYA NOTE
This is a lesson, not a status report, and its value is that it reclassifies a whole verdict category: post-push mismatch goes from "failure" to "re-check trigger." The 10:12Z tick is the worked case — first pass pushed 3 files blob-verified, dispatcher rebuild landed 10:10:58Z mid-sync (same sizes, changed bytes), re-check pass pushed 3 more blob-verified, writer hash 0b02edfc stable across both passes. The convergence signal matters: writer-hash stability across passes is what distinguishes a race resolved from a divergence persisting. The 14:38Z tick is the control case — dispatcher rebuild 14:31Z captured before sync, writer hash f167d3ce stable before and after, no mid-sync race — proving the race is a window property, not a property of either writer. Cousins, kept distinct: this is not a "stale read" lesson (the read was fresh when taken) and not a "concurrent write corruption" lesson (no bytes were ever torn or mixed — each pass pushed one complete generation). Honest holes, stated not hidden: the window is not eliminated, only handled — a rebuild can still land mid-sync on any tick, so the re-check pass is a standing cost, not a one-time cure; and a re-check pass that itself straddles a second rebuild would need a third look, which no tick has yet needed.

## 🟢 MACHINE NOTE

```json
{
  "sn": "SN-1992",
  "title": "A rebuild landing mid-sync is a race to re-check, not a failure — a post-push mismatch opens a re-push + re-verify pass, and only a mismatch surviving the re-check is a failure",
  "observation": false,
  "applies_when": ["operations", "ledger-sync"],
  "enforcement": "Every ledger sync ends with a post-push re-check: live bytes compared against pushed bytes, writer hash compared across passes. A mismatch triggers a re-push + re-verify pass; the tick is closed as a race resolved only when the re-check pass converges (pushed bytes blob-verified, writer hash stable). A mismatch that survives the re-check pass is reported as a failure — a first-pass mismatch alone is never filed as one.",
  "evidence": "shared-state director_tick_20261025_1012z (2026-10-25T10:12Z): 'dispatcher rebuilt ledger files at 10:10:58Z during this tick's sync (same sizes, changed bytes); resolved with a re-check pass that pushed the rebuilt bytes blob-verified; writer hash 0b02edfc stable across both passes.' Control case director_tick_20261025_1438z (2026-10-25T14:38Z): dispatcher rebuild 14:31Z captured before sync, writer hash f167d3ce stable before and after sync, no mid-sync race.",
  "decision_change": "Future sync verdicts change: a post-push mismatch no longer opens a failure report — it opens a re-check pass. A tick whose re-check pass converges is recorded as a race resolved, not a failure, and the writer-hash stability across passes is cited as the convergence proof. Only a mismatch surviving the re-check pass escalates.",
  "falsifier": "The race reading is refuted if the post-push mismatch persists after the re-check pass with an unchanged writer hash — then it is a real divergence, not a timing overlap. It is also refuted if the rebuild timestamp falls outside the sync's read-to-write window — then the mismatch has another cause and the re-check pass is not the cure."
}
```

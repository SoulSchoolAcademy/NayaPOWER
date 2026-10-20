# A Re-Entering Brief Is a Registrar Incident, Not a New Queue Entry — Registration Writes Need Cited Causes and Generation Binding

**Intelligent Block:** IB-SMART-NOTE-20260930-sn01744-registrar-re-entry-needs-cited-cause
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-20
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

At t1087 (2026-10-20T23:33Z) the gap brief `brief-gap-t1034-lane10.md` re-appeared in the dispatch queue WITH its parent receipt `t1034-lane10.md` on disk — three rotations after it was dequeued at t1052 with cause, and after the t1062/t1074 receipt-direction rules were holding. The dispatcher removed it again, correctly, per the direction rules. But that response treats the third re-entry as an independent dequeue event — and it will keep firing forever, because nothing guards the REGISTRATION path. Every rule so far is dequeue-side: SN-1742's cause-cited dequeue ledger guards shrink writes; SN-1741 guards receipt direction; t1052's read-latest rule guards the reconcile read. The registration side is unguarded: any writer can re-inject a brief whose parent already has an on-disk receipt, with no writer name, no cause, no binding to the rotation generation it read. Three hypotheses for the re-entry — stale-write replay of a pre-dequeue rotation snapshot (t1052's observed mid-tick mutation mechanism), or a blind t1038-style "register what you write" re-register by a writer that never checked the dequeue ledger, or a concurrent executor whose read predates the dequeue. All three are invisible at the moment the write lands. The rule: a brief re-entering `queued` that already has an on-disk parent receipt or a dequeue-ledger line within the last 10 rotations is a REGISTRAR INCIDENT, not a new entry — the re-entry is removed, the writer is named, and the writer's spawn path gets audited. One re-entry is triage; two re-entries of the same brief within 24h proves the spawn path is unguarded.

## 🩷 HUMAN NOTE

Shawn — a to-do item we finished and checked off three days running kept jumping back onto the team's list. We kept checking it off again, which was correct — but the real problem is whatever keeps putting it back on. The dequeue rules are the check-off rules and they're working. This is the missing half: the rule that says whoever puts an item ON the list has to sign it, say why, and say which version of the list they were looking at — so a finished item jumping back on gets traced to whoever brought it back, not just checked off again.

## 🟣 CHILD NOTE

Imagine a library where two librarians share one card catalog. Librarian A throws away an old card for a returned book. Librarian B has an old copy of the catalog on her desk and, not knowing the card is gone, copies it back in. Nobody is being bad — but nobody wrote their name on what they put in or checked whether it was already thrown away. The fix: every card added gets the librarian's name, the reason, and the catalog version they looked at. A card that keeps reappearing gets traced to the librarian who keeps adding it.

## 🔵 GRANDMA NOTE

Like a pill organizer that two people refill. You take the Tuesday pill out; your helper, working from yesterday's list, puts a Tuesday pill back in. The pill isn't wrong — but your helper is working from an old list and there's no note saying who put it there. The fix: whoever adds a pill writes their name, the date, and "checked today's list." If Tuesday keeps refilling itself, you don't keep removing the pill — you ask who's refilling it.

## 🟠 NAYA NOTE

Apply to the dispatcher and every lane-executor that writes the rotation: (1) registration writes (anything that ADDS to `queued`) must carry {writer, cause, generation-read} — the rotation counter (1086→1087) is a generation stamp; a write computed from a stale generation must be rejected or re-based, never silently applied; (2) a brief re-entering `queued` that already has an on-disk parent receipt OR a dequeue-ledger line within the last 10 rotations is a RE-ENTRY INCIDENT: remove the re-entry, name the writer, open a writer audit on that writer's spawn path — do NOT treat it as a routine dequeue; (3) one re-entry is triage; two re-entries of the same brief within 24h proves the spawn path is unguarded — registration writes from that writer are held until the writer names the cause; (4) lane-executors: a t1038-style "register what you write" re-register of a brief whose parent has an on-disk receipt is a bug unless the cause line names a new live parent brief; (5) until writes carry {writer, cause, generation-read}, the mandatory per-tick disk-vs-rotation diff (SN-1742's tripwire) is extended to flag re-entries as registrar incidents — a tick that skips the re-entry check is an unverified tick. This is the write-side sibling of SN-1742 (dequeue ledger) and SN-1741 (receipt direction): the queue ledger now covers both directions.

## 🟢 MACHINE NOTE

~~~json
{
  "slug": "registrar-re-entry-needs-cited-cause",
  "sn": "SN-1744",
  "title": "A Re-Entering Brief Is a Registrar Incident, Not a New Queue Entry: Registration Writes Need Cited Causes and Generation Binding",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-20",
  "intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "kind": "lesson",
  "applies_when": ["dispatcher", "brief-queue", "registration", "rotation", "reconcile", "re-entry", "queue-membership", "concurrent-writers"],
  "enforcement": "The mandatory per-tick disk-vs-rotation diff (SN-1742 tripwire) is extended: any brief found in queued that (a) has an on-disk parent-stem receipt in twelve-lane-receipts/, or (b) has a dequeue-ledger/completed entry within the last 10 rotations, is flagged as a RE-ENTRY INCIDENT, not silently dequeued. The re-entry is removed, the writer of the registering write is named, and a writer audit opens on that writer's spawn path. One re-entry = triage; two re-entries of the same brief within 24h = the spawn path is unguarded and registration writes from that writer are held until the writer names the cause. Once writes carry {writer, cause, generation-read}, a write adding to queued from a stale generation is rejected at write time.",
  "evidence": {
    "t1087": "lesson-broadcast.md [night-dispatcher t1087, 2026-10-20T23:33Z] RECONCILE: brief-gap-t1034-lane10.md re-appeared in queued WITH receipt t1034-lane10.md on disk (was dequeued t1052) — removed again this tick; t1052/t1053/t1062 lessons still stand. Rotation 1086->1087. Third re-entry of the same brief across t1038/t1056/t1087 despite all dequeue-side rules holding.",
    "t1052": "lesson-broadcast.md [night-dispatcher t1052, 2026-10-20T17:40Z]: rotation mutated mid-tick by a concurrent lane-executor during a reconcile — establishes the stale-write-replay mechanism (writer working from a pre-dequeue read can replay dequeued entries back into queued).",
    "t1038": "lesson-broadcast.md [night-dispatcher t1038, 2026-10-20T15:02Z]: reverse-phantom — 'writers must register what they write' — the write-side rule whose BLIND application (re-register without checking the dequeue ledger) is one of the three re-entry hypotheses.",
    "sn1742": "SN-1742 (2026-10-20): dequeue-side ledger — every rotation write that shrinks queued must cite cause; the write-side sibling named but unguarded.",
    "sn1741": "SN-1741 (2026-10-20): receipt direction — a parent receipt does not close its child gap brief; the direction rule t1087's removal correctly applied."
  },
  "decision_changed": "How the dispatcher responds to a brief that re-enters queued after a cause-cited dequeue: instead of dequeue-again-and-move-on (t1087's handling), the re-entry is classified as a REGISTRAR INCIDENT — the registering write is attributed to a writer, the writer's spawn path is audited, and repeat re-entries hold that writer's registration writes until the writer names the cause. Applies to: dispatcher reconcile sweeps, lane-executor registrations, queue membership audits.",
  "falsifier": "Thirty days of rotation writes where every re-entering brief is traced by {writer, cause, generation-read} logs to a live parent brief — i.e., re-entry is always legitimate new work and the registrar gate never fires (the gate adds no value beyond routine dequeue). At finer grain: a re-entry whose writer log shows a stale-generation read CONFIRMS the stale-replay hypothesis over the deliberate-re-register hypothesis; a log showing a current-generation deliberate re-register with a cited new cause FALSIFIES the 'blind re-register' hypothesis for that writer.",
  "mechanism": "The rotation file is rewritten by multiple concurrent writers and carries a generation counter (1086->1087), but writes are not bound to the generation they read. A writer whose read predates a dequeue (t1052's observed mid-tick mutation) replays the pre-dequeue snapshot and resurrects the entry; a writer blindly applying t1038's 'register what you write' re-registers a brief whose parent receipt is on disk without checking the dequeue ledger. In both cases the re-entry carries no writer, no cause, no generation — observationally identical to legitimate new work at write time. Binding registrations to {writer, cause, generation-read} makes every re-entry attributable at write time instead of detectable only by the next diff.",
  "cousins": ["SN-1742 dequeue-without-cited-cause (the dequeue-side sibling — shrink writes need causes)", "SN-1741 parent-receipt-does-not-close-child-gap (the direction rule t1087's removal applied)", "SN-1743 pinned-structural-stall (the stall side of the same t1087 tick)", "t1052 reconcile-on-latest-read (the read-side sibling — mid-tick mutation)"]
}
~~~

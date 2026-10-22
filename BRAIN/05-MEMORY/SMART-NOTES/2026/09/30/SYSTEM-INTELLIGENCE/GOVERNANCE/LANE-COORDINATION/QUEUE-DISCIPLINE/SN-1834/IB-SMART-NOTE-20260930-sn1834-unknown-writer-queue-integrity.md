Intelligent Block
Truth state: CANDIDATE
Scope: PRIVATE
Captured date: 2026-10-22
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

Under an unknown writer with stale reads, the queued list is not the queue — it is a mirror that any stale process can overwrite. t1290 proved it twice in one hour: ten adjudicated-dequeued entries re-appeared in rotation between 14:25Z and 14:32Z with no cite-cause (a stale writer re-wrote the pre-adjudication list — updated_utc left stale at 13:29Z, not a dispatcher write), and brief-t1295-lane4.md was silently DROPPED from the list while its file sat on disk, never claimed, never worked. An adjudication that lives only in a tick record is re-writable by any process with file access: the cite-cause must travel WITH the entry — a tombstone in the list itself — or the dead get resurrected. Until the writer is identified, every tick sweeps both directions (list→disk AND disk→list) and the reverse-phantom count counts FILES, not list entries.

## 🩷 HUMAN NOTE

Shawn — the dispatch queue got haunted twice in one hour. Ten briefs the dispatcher had already ruled finished came back from the dead because some unknown process wrote an old copy of the list back over the new one. And one brief vanished from the list while its file was still sitting there, never worked. The fix isn't a stronger opinion — it's a lock: every ruling gets stamped INTO the list itself, like a tombstone on a grave, so a stale copy can't silently dig it up. And every tick checks both directions: what's on the list but has no file, and what has a file but isn't on the list. Until we find what wrote the old copy, the two-way sweep runs every tick.

## 🟣 CHILD NOTE

Imagine a class attendance list where the teacher marks ten kids absent because they graduated. But another teacher has an old copy of the list, and without knowing, puts up their old list instead — suddenly the graduated kids are back on the list. And one kid who's actually sitting in class disappears from the list. The fix: write "GRADUATED" right on the line next to each name, IN the list itself — not on a separate note that can get lost. Then every morning, check two ways: is every name on the list actually in a desk, and is every kid in a desk actually on the list?

## 🔵 GRANDMA NOTE

It's like a restaurant's reservation book. One host crosses out a party that already left and writes why. But another host has a photocopy from yesterday and puts it on top — the departed party reappears. Meanwhile a real reservation slips off the page. The answer is to write the reason right in the book next to the name — not on a sticky note — so no one can un-erase it by accident. And you check both ways: every name in the book should have a real person coming, and every real person should be in the book.

## 🟠 NAYA NOTE

Queue-integrity doctrine, Naya to Naya: the rotation list is a mirror, not the source of truth — the queue is the union of (rotation entries) ∪ (files on disk) ∪ (claimed/ sign-ins) ∪ (done/ receipts). Two writer-side faults were observed, same hour, same unknown writer (director follow-up owed — find what wrote rotation at 14:32:02Z): (1) STALE-RESURRECT: a stale writer's old copy of the list overwrote ten adjudicated entries, resurrecting briefs with standing closing receipts; (2) SILENT-DROP: an entry fell out of the list while its file stayed on disk, never claimed, never worked. Both faults defeat any reconcile that reads the list alone. The mechanism fix: the adjudication's cite-cause is stamped INTO the list entry (tombstone), so a stale overwrite cannot silently resurrect it — the tombstone resurfaces the conflict instead of the old state; and the reconcile sweeps both directions every tick, counting files on disk (not list entries) for the reverse-phantom check, because t1299 caught a phantom that a list-only count would have blessed.

## 🟢 MACHINE NOTE

```json
{
  "slug": "sn-1834-adjudications-travel-with-the-entry-under-an-unknown-writer",
  "lesson": "Under an unknown writer with stale reads, the queued list is not the queue: a stale writer can resurrect adjudicated-dequeued entries by overwriting the list with an older copy, or silently drop entries whose files still sit on disk. An adjudication that lives only in a tick record is re-writable; the cite-cause must travel WITH the entry (tombstone in the list itself), so a stale overwrite resurfaces a conflict instead of silently restoring the old state. Until the writer is identified, every reconcile sweeps both directions (list->disk and disk->list) and reverse-phantom checks count files on disk, never list entries.",
  "applies_when": ["dispatch", "rotation", "queue-integrity"],
  "enforcement": "The dispatcher tick's reconcile (until the unknown writer is identified — the standing director follow-up): (1) adjudicated entries carry their cite-cause tombstone in the rotation list before dequeuing; a re-listed tombstone is adjudicated out with cite-cause and re-tombstoned, never re-queued; (2) every tick sweeps both directions — list entries missing files AND files on disk missing list entries are named; (3) the reverse-phantom count counts files, not list entries. The writer-search (who wrote rotation at the anomalous mtimes) is the open director leg; the two-way sweep stays until that leg closes.",
  "evidence": [
    "hidden_files/lesson-broadcast.md [night-dispatcher t1290, 2026-10-22T14:38Z: GHOST-REQUEUE — 10 adjudicated-dequeued entries re-appeared in rotation queued 14:25–14:32Z with no cite-cause (9 t1271 ghost-dequeues with proven root cause + the t1268 receipt-closed 0000-lane10); rotation file mtime 14:32:02 but updated_utc left stale at 13:29:00Z — NOT a normal dispatcher write; restored 36->24]",
    "hidden_files/lesson-broadcast.md [night-dispatcher t1297, 2026-10-22T15:43Z: DISPATCH-RESTORE — brief-t1295-lane4.md silently dropped from rotation queued before t1296's read; file on disk, never claimed, never worked; restored 24->25; second data point of the t1290 unknown-writer family]",
    "hidden_files/lesson-broadcast.md [night-dispatcher t1299, 2026-10-22T16:02Z: TOMBSTONE #4 — brief-gap-scorer-20261015-0000-lane10.md resurrected a 4th time (unknown writer, 15:43–15:53Z) into rotation queued with no file and a standing closing receipt; adjudicated out with cite-cause, tombstoned; the t1298 '26/26 on disk' note — the reverse-phantom count must count the FILES, not the list]"
  ],
  "decision_change": "Every future dispatcher's reconcile treats the rotation list as a mirror, not the queue: adjudications are tombstoned in the list with cite-cause, the tick sweeps both directions, and phantom checks count files. The unknown-writer hunt stays a standing director leg until the writer is named and fenced.",
  "falsifiability": "If the writer is identified and writes are serialized (fenced lease / single writer), and no resurrection or silent drop recurs across subsequent ticks, the two-way sweep may retire — the lesson then reduces to write-serialization. If a resurrection ever arrives through the normal writer path with the tombstone present (not a stale overwrite), this mechanism is insufficient and the note is wrong.",
  "mechanism": "Stale-read writer: a process that read the rotation list before an adjudication and writes its stale copy back overwrites the adjudicated state — no malice, no bug in the dispatcher, just a non-atomic read-modify-write with an unknown second writer. The tombstone converts the failure from silent (old state restores) to visible (conflict resurfaces with its cite-cause); the two-way sweep covers the silent-drop direction, which no amount of tombstoning can catch."
}
```

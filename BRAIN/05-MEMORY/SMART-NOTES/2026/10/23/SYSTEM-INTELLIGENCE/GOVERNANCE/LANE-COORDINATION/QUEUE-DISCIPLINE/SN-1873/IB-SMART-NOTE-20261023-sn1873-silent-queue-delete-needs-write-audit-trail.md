Intelligent Block
Truth state: CANDIDATE
Scope: PRIVATE
Captured date: 2026-10-23
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

The two-way sweep caught files vanishing — but it could not name who took them. On 2026-10-23 at ~06:03 PDT, 6–7 unclaimed brief-*.md files silently vanished from the brief-queue directory: queue root and done/ mtimes changed 13:03:48Z, yet no file moved into claimed/, done/, archived/, stale/, or superseded/, no receipts were written, and no feed entries logged. Every transition the claim protocol performs leaves a record — this deletion performed none. Detection is not attribution: the queue directory needs a write-audit trail so the next silent disappearance names its writer, not just its absence.

## 🩷 HUMAN NOTE

Shawn — someone cleaned out part of the work queue and left no fingerprints. Six or seven briefs nobody had claimed yet just disappeared from the queue folder around 6:03 this morning. They weren't claimed, finished, archived, or marked stale — they simply stopped existing, and nothing in the system says who removed them. The sweep that checks the queue both ways noticed they were gone, but noticing isn't the same as knowing. The fix is a paper trail on the queue itself: every time a file is moved, claimed, or deleted, the actor writes one line saying so — so a disappearance with no matching line is immediately an integrity alarm, not a mystery.

## 🟣 CHILD NOTE

Imagine a teacher's in-tray where kids drop in their homework slips. One morning, six slips are gone. Nobody's name is checked off, nobody turned them in as finished — they just vanished from the tray. The tray was checked twice (once for names with no paper, once for paper with no names), which is how the teacher noticed. But noticing they're gone doesn't say who took them. The fix: a little notebook next to the tray where anyone who touches a slip writes down what they did and when. If a slip vanishes and there's no line in the notebook — that's not "missing," that's "someone broke the rules."

## 🔵 GRANDMA NOTE

It's like a church lost-and-found box. One Sunday, half the umbrellas are gone. Nobody signed the claim book, nothing was donated away, the bin just got emptier overnight. Counting the umbrellas told us they were missing, but it can't tell us who carried them out. The answer is a simple sign-out sheet hung on the bin itself: every time someone takes or moves an umbrella, they write it down. From then on, an umbrella missing with no signature on the sheet isn't just lost — it's a signal that someone bypassed the process, and we treat it that way.

## 🟠 NAYA NOTE

Queue-integrity doctrine, Naya to Naya: SN-1834 proved the rotation LIST can be haunted by a stale writer — tombstones and the two-way sweep (list→disk, disk→list) were the cure. This event is the other direction of the same disease, one level down: the FILES themselves left the disk with no protocol transition at all. The two-way sweep DETECTED the anomaly (files without list entries, no claim records), which means detection machinery works — but detection answers "gone," and the decision we owe is "by whom." A filesystem write outside the claim protocol is invisible to the claim protocol: any process with file access can delete or rename a brief, and nothing records it. The mechanism fix is a write-audit trail on the queue directory: every actor that moves, claims, or deletes a brief appends one line (actor, action, timestamp) to an append-only audit log; the tick's queue check matches every on-disk disappearance against the audit log, and any disappearance with no matching entry is raised as an INTEGRITY event, never silently absorbed. Until the trail exists, a silent disappearance recurs with the same outcome — detected, unattributed, unprosecutable.

## 🟢 MACHINE NOTE

```json
{
  "slug": "sn-1873-silent-queue-delete-needs-write-audit-trail",
  "lesson": "A deletion outside the claim protocol leaves no record of who or where: on 2026-10-23 ~06:03 PDT, 6-7 unclaimed brief-*.md files vanished from the brief-queue directory with queue-root and done/ mtimes changed at 13:03:48Z but no move into claimed/, done/, archived/, stale/, or superseded/, no receipts, and no feed entries. The two-way sweep (SN-1834) detects such disappearances but cannot attribute them, because the claim protocol only records transitions it performs. The queue directory needs a write-audit trail: every actor that moves, claims, or deletes a brief appends actor+action+timestamp to an append-only audit log, and the tick's queue check matches every on-disk disappearance against the log — a disappearance with no matching entry is raised as an INTEGRITY event instead of being silently absorbed.",
  "applies_when": ["dispatch", "brief-queue", "queue-integrity", "integrity-event"],
  "enforcement": "The dispatch/steward tick's queue check (stall-cap check family) is extended: (1) every move/claim/delete of a brief-*.md file by any lane writes actor+action+utc-timestamp as one appended line to the queue's append-only audit log; (2) each tick the check matches every on-disk disappearance since the last tick against the audit log — any disappearance with no matching entry is posted as an INTEGRITY event (board) and never silently absorbed; (3) the nightly stall-cap run verifies audit-log completeness against directory mtimes. Until the trail exists, the standing response to any silent disappearance is an open integrity investigation, not an assumption of legitimate consumption.",
  "evidence": [
    "hidden_files/twelve-lane-receipts/seat-stall-20261023-0637.md [2026-10-23: 'Mirror lesson' + 'Queue delta since seat-stall-20261023-0533' — 6-7 unclaimed brief-*.md files silently vanished at ~06:03 PDT; queue root + done/ mtimes changed 13:03:48Z; no mv into claimed/, done/, archived/, stale/, or superseded/; no receipts; no feed entries]",
    "hidden_files/learning-events-2026-10-23-14.md [14:00 PDT hour LEARNING event: queue-integrity anomaly; lesson named in receipt — 'if it recurs, the queue directory needs a write-audit trail']"
  ],
  "decision_change": "The next queue-delta anomaly is decided as an integrity investigation (audit-log mismatch hunt), not as 'assume claimed and rebuild' — a disappearance with no protocol record is evidence of an out-of-protocol writer, not a normal claim.",
  "falsifiability": "If a write-audit trail is installed and shows the files were consumed through legitimate claim+completion transitions (the receipt/feed records were simply delayed or written elsewhere), then this event was a detection gap, not an out-of-protocol deletion, and the lesson reduces to 'close the audit gap.' If files keep vanishing with no matching audit entries, the lesson's core claim — out-of-protocol writers are live — stands.",
  "mechanism": "The claim protocol records only transitions it performs; any process with file access can delete or rename a brief without touching the protocol. Detection machinery (two-way sweep) observes state, not authorship — it answers 'gone' but cannot answer 'by whom.' An append-only write-audit converts authorship from unobservable to observable: legitimate actors self-record, so the absence of a record becomes positive evidence of an out-of-protocol actor rather than a mystery."
}
```

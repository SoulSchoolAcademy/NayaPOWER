Intelligent Block
Truth state: CANDIDATE
Scope: PRIVATE
Captured: 2026-10-23
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL
os.rename preserves mtime — a rename is a link operation, not a content write, so mtime-based move detection is structurally blind by filesystem design. The scorer's "no move trace" was a false silent-alarm twice in one day; moves must be traced from ctime or an explicit reconcile move ledger, never mtime.

## 🩷 HUMAN NOTE
The night-dispatcher reconcile fired a "no move trace" alarm: seven files appeared to have moved with no trace. The t1457 mirror closed it honestly — the seven files were legitimately dequeued in a single batch by t1449's reconcile, and ctime proved it. The scorer's move detector watches mtime, and os.rename never changes mtime — so every legitimate batch dequeue reads as a mysterious move. It was the second false silent-alarm from that detector in one day. The durable fix is owed to dispatcher/director: trace moves with a reconcile move ledger or ctime-based audits, never mtime. A detector that cries "moved with no trace" on every legitimate dequeue is noise, not signal — and noise teaches the team to ignore the real alarms.

## 🟣 CHILD NOTE
You have a "did anything move?" checker that looks at the "last changed" sticker on each box. But sliding a box across the room doesn't change its sticker — the sticker only changes when you OPEN the box. So every time someone slides boxes to tidy up, the checker yells "mysterious movement!" — twice in one day! The fix: watch the "last touched or relabeled" sticker (ctime) instead, or keep a notebook of every slide.

## 🔵 GRANDMA NOTE
It's like a guard who decides whether a book was moved by checking when the ink was last touched. Sliding a book along the shelf never touches the ink — so the guard raises a false alarm every time the librarian reshelves. Twice in one day, he cried wolf. The real answer: check the reshelving log, or the "when was it handled" stamp — never the ink.

## 🟠 NAYA NOTE
For dispatcher/director reconcile machinery and every lane-scorer audit: mtime is content-modification time, not move time. os.rename is a link operation — mtime is preserved by design, so any move detector keyed on mtime is structurally blind and will false-alarm on every legitimate batch dequeue. The owed cure: (1) a reconcile move ledger written at dequeue/rename time, or (2) ctime-based move audits (ctime changes on rename). Until then: any "no move trace" claim that has not been re-proven against the move ledger or ctime is not a gap — it is the detector's blindness, and filing it as a gap costs the team a false alarm it must then burn a lane-tick to close.

## 🟢 MACHINE NOTE
{
  "id": "SN-1893",
  "slug": "mtime-blind-move-detection",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-23",
  "lesson": "os.rename preserves mtime: a rename is a link operation, not a write, so mtime-based move detection is structurally blind by filesystem design. Moves must be traced from ctime or an explicit reconcile move ledger; mtime-keyed move detectors false-alarm on every legitimate batch dequeue.",
  "evidence": [
    "hidden_files/lesson-broadcast.md [night-dispatcher t1457, 2026-10-23T21:02Z]: MIRROR brief-gap-seat-stall-20261023-1223-lane0.md -> gap-seat-stall-20261023-1223-lane0.md: 9.0 SHIP — GAP CLOSED: the 'missing 7' files were legitimately dequeued by t1449 reconcile (single batch, ctime-proven); the scorer's 'no move trace' is explained — os.rename preserves mtime, so mtime-based move detection is structurally blind (second false silent-alarm from this mechanism today). Durable fix owed to dispatcher/director: reconcile move ledger or ctime-based audits."
  ],
  "decision_change": "How reconcile audits detect moves: by move ledger or ctime, never mtime; and whether a 'no move trace' claim counts as a gap — it does not until re-proven against the ledger or ctime.",
  "falsifier": "If a cold audit demonstrates that os.rename under this VM's filesystem does change mtime (e.g., a cross-filesystem rename), the 'blind by design' claim is refuted for that case. If ctime-based audits produce no fewer false alarms than mtime-based ones, the cure claim is refuted.",
  "mechanism": "mtime records content modification; rename changes directory linkage, not content bytes — the POSIX design preserves mtime across rename. ctime records inode-status changes (including rename), so ctime sees what mtime cannot. An explicit move ledger records the intent at dequeue time, immune to metadata semantics entirely.",
  "applies_when": [
    ["operations", "reconcile"],
    ["dispatch", "move-detection"],
    ["audit", "metadata"]
  ],
  "enforcement": "Dispatcher reconcile and lane-scorer move audits read ctime or the reconcile move ledger for moves; a 'no move trace' gap claim without a ctime/ledger check is bounced in the dispatcher broadcast review (the t1457 broadcast that closed gap-seat-stall-20261023-1223 is the enforcement site — it re-proved the claim against ctime before closing)."
}

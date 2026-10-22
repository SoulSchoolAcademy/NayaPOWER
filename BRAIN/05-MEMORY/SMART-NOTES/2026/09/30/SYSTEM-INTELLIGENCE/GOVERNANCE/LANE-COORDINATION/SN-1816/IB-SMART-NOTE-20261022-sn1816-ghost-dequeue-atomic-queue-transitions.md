Intelligent Block
Truth state: CANDIDATE
Scope: PRIVATE
Captured date: 2026-10-22
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

Every queue state change must be atomic across all its surfaces — a brief's file write + its rotation registration, or a close's rotation dequeue + its file move to done/, in the same tick. Pre-patch, registration and the file write were two separate steps with a failure window between them: a write-side failure left rotation entries pointing at no file — the t1271 GHOST-DEQUEUE proved the mechanism and dequeued 10 phantom briefs. The close side has the mirror trap: a closed brief's file left on disk becomes a re-registration trap on the next silent-arrival sweep (t1262 LEFTOVER-FILE CLASS). And a "keep pending" hold whose condition is a proven root cause is a queue in a drawer — the t1271 dispatcher re-evaluated the t1263 hold the moment the mechanism landed.

## 🩷 HUMAN NOTE

On 2026-10-22 the night-dispatcher proved the cause of eleven rotation-queued briefs that existed in the rotation but on no disk anywhere: before the writer-side registration patch landed, registering the brief in the rotation and writing the brief file were two separate, non-atomic steps — a failure in between left a queue entry with no brief. Ten entries were dequeued in one tick once the cause was named. The same morning, a mirror trap on the close side got its name: a brief closed by receipt but whose file never moved to done/ sits on disk looking exactly like an unregistered arrival, so the next sweep re-queues completed work. Two rules now stand: transitions touch every surface in the same tick, and a hold whose reason gets proven gets re-evaluated the hour the proof lands.

## 🟣 CHILD NOTE

When you take a book off the shelf, put the library card back in the box AT THE SAME TIME. If you do it in two steps and get interrupted in between, the card says a book is out that was never taken — or the book sits on the shelf while the card says it's out. Same time, every time.

## 🔵 GRANDMA NOTE

Darling, when you move the good china from one cabinet to another, don't just write it in the notebook — move the plates too, right then. A note without the move is a promise that confuses everyone, and plates without the note are a mystery. Do both together, while you're standing there.

## 🟠 NAYA NOTE

A queue entry lives on multiple surfaces — the brief file, the rotation ledger, the done/ archive. Any transition that updates them in sequence (write→register, dequeue→move) has a failure window that manufactures partial states: GHOST entries (registered, no file — the write side) and RE-REGISTRATION TRAPS (closed, file still present — the close side). Partial states are invisible to any single-surface check; only cross-surface presence sweeps see them. The atomicity contract: (1) write side — fail-closed self-registration at file time (registration failure unlinks the brief and aborts — receipt gap-t1182-lane4.md, 9.0/10, 3-pass); (2) close side — rotation dequeue + receipt-chain verified + physical move to done/ in the same tick (t1262). And the hold rule: a hold created under an unproven cause must be re-evaluated the moment the mechanism lands — a hold whose condition is proven is a queue in a drawer (t1263's keep-in-rotation hold, overridden by t1271's proven root cause).

## 🟢 MACHINE NOTE

```json
{
  "sn": "SN-1816",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured_utc": "2026-10-22T11:15:00Z",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "category": "GOVERNANCE",
  "sub": "LANE-COORDINATION",
  "lesson": "Queue state changes must be atomic across all their surfaces — brief file write + rotation registration, or rotation dequeue + receipt-chain verified + file moved to done/, in the same tick. Non-atomic two-step transitions manufacture partial states invisible to single-surface checks: GHOST entries (registered, no file) on the write side, RE-REGISTRATION TRAPS (closed, file still present) on the close side. Holds created under an unproven cause must be re-evaluated the moment the mechanism lands — a hold whose condition is proven is a queue in a drawer.",
  "decision_change": "When designing any brief/queue state change, the transition must land as one atomic step across every surface (file, rotation, archive) in the same tick — split transitions are the bug, not the incident. When a 'keep pending' hold's underlying cause gets proven by a landed mechanism, the hold is re-evaluated that hour, not carried as a queue in a drawer.",
  "falsifiability": "This lesson breaks if post-fix sweeps find rotation entries with no brief file (after 2026-10-22T10:23Z writes) — the atomicity diagnosis is then wrong or the fail-closed contract is bypassed. The t1271 evidence names exactly where to look: rotation-queued entries absent from brief-queue/, claimed/, claimed/done/, done/, stale/, and archived/ with zero lane-feed mentions and zero exact-name receipts.",
  "mechanism": "Pre-patch, rotation registration and the brief file write were NOT atomic — a write-side failure between them left a queue entry with no file (the t1267 landed root repair names the mechanism: the same root that powered 9+ repeats of the reverse-phantom class). Partial states evade single-surface checks by construction; only cross-surface presence checks (rotation vs every physical dir vs receipts) reveal them. On the close side, a file left on disk after close looks identical to an unregistered arrival — the sweep's own signature, re-applied to completed work.",
  "evidence": [
    "hidden_files/lesson-broadcast.md [night-dispatcher t1271, 2026-10-22T11:06Z] GHOST-DEQUEUE: the t1263 LOST-FROM-DISK class cause proven — pre-patch registration and file write non-atomic; 10 rotation-queued entries confirmed absent from brief-queue/, claimed/, claimed/done/, done/, stale/ AND archived/ with zero lane-feed mentions and zero exact-name receipts in 1,534 receipts — dequeued 33->23; t1263's keep-in-rotation hold overridden",
    "hidden_files/lesson-broadcast.md [night-dispatcher t1262, 2026-10-22T09:32Z] LEFTOVER-FILE CLASS: a closed brief's file left on disk in brief-queue/ is a re-registration trap — the next silent-arrival sweep sees 'on disk, unregistered' and re-queues completed work; closing a brief = rotation dequeue + receipt chain verified + physical file moved to done/ in the same tick",
    "hidden_files/lesson-broadcast.md [night-dispatcher t1267, 2026-10-22T10:23Z] REVERSE-PHANTOM ROOT REPAIR LANDED: receipt gap-t1182-lane4.md (Lane 4, 9.0/10, 3-pass) ships file-gap-brief.py self-registration — every gap brief self-registers into rotation queued + appends a cite-cause ledger line at file time, fail-closed (registration failure unlinks the brief and aborts)",
    "hidden_files/learning-events-2026-10-22-10.md, [INTELLIGENT] Graduation (window ending 2026-10-22T10:20:19Z): SN-1783's writer-side registration LANDED in code; the sign-out checker run caught the old writer's 10th silent arrival (brief-gap-gap-t1002-lane1-lane1.md, written 09:41Z) and cited it"
  ],
  "cousins": [
    "SN-1783 (reverse-phantom class naming — the arrival-side class this note's write-side mechanism powered)",
    "SN-1808 (suspicion-not-identity — overlap-flag rule for maybe-covered work, not lifecycle atomicity)",
    "SN-1815 (gap dead-on-arrival freshness check — writer-side filing contract, adjacent leg of the same pipeline)"
  ],
  "applies_when": [["dispatch", "queue-coherence"], ["brief", "lifecycle"], ["queue", "state-transition"], ["lane-coordination", "atomicity"]],
  "enforcement": "Write side: file-gap-brief.py's fail-closed self-registration — registration failure unlinks the filed brief and aborts (byte-verified in receipt gap-t1182-lane4.md, 9.0/10, 3-pass). Close side: the t1262 named rule — rotation dequeue + receipt-chain verified + physical file moved to done/ in the same tick, checked by the dispatcher's reconcile sweep, which verifies by presence across brief-queue/, claimed/, claimed/done/, done/, stale/, and archived/ (the sweep that proved the 10 ghost entries).",
  "dedupe_guard": "Not a duplicate: SN-1783 names the reverse-phantom arrival class; SN-1808 covers dedupe-on-suspicion for overlapping work; SN-1815 covers the filing-time freshness contract. This covers lifecycle atomicity of queue transitions (write side + close side) and the hold re-evaluation rule — a different leg."
}
```

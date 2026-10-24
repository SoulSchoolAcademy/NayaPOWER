# IB-SMART-NOTE-20261023-sn1908-reconcile-review-starts-at-persistence-boundary

- Intelligent Block: SN-1908
- Truth state: CANDIDATE
- Scope: PRIVATE
- Captured date: 2026-10-24T00:42:00Z
- Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL
Reconcile-script review starts at the persistence boundary — grep the writes before trusting the reads. t1467-lane4 found dispatch-reconcile-tick.py has no rotation write-back (phantom re-queues die in memory), so wiring it "autonomously" would have silently dropped its own decisions under a "wired" banner. A reconcile without a write-back is a report, not a reconcile.

## 🩷 HUMAN NOTE
When a script claims to "reconcile" — to take decisions and carry them forward — ask where those decisions are written down. If the answer is "in the script's own memory while it runs," there is no reconcile; the moment the script stops, every decision evaporates. Review the writing first, the thinking second: no write, no persistence, no adoption.

## 🟣 CHILD NOTE
A to-do list that only lives in your head is not a to-do list — it is a wish. You think about the chores, you feel done, and then you forget them because nothing was written down. A reconcile script that never writes its decisions anywhere that survives is the same: its "decisions" vanish the moment the program ends.

## 🔵 GRANDMA NOTE
Like a secretary who writes the meeting minutes on a fogged bathroom mirror — it looks official for a minute, and then the fog clears and nothing is there. A real record lives somewhere permanent: paper, a ledger, a file. Judge any "reconciliation" by where it writes, not by how seriously it reads.

## 🟠 NAYA NOTE
Operational rule for reviewers and certifiers of any reconcile / adoption / wiring claim: FIRST grep the writes — file writes, DB upserts, queue publishes, ledger appends. Name the persistence path on the record before examining any flow evidence. If no write path exists, the review fails at sign-in; no adoption closes on read-path evidence alone. The worked example is t1467-lane4 finding #6 (dispatch-reconcile-tick.py: phantom re-queues die in memory, no rotation write-back). This is the persistence-side sibling of CANDIDATE 885's CADENCE-GAP (file-level vs flow-level wiring): CADENCE-GAP caught the missing invocation; this rule catches the missing write-back.

## 🟢 MACHINE NOTE
{
  "id": "SN-1908",
  "captured_utc": "2026-10-24T00:42:00Z",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "applies_when": ["review", "reconcile", "adoption", "engineering-proof", "wiring-claim", "certification"],
  "enforcement": "Certification of any reconcile/adoption claim must begin with a named persistence path (grep over write operations: file writes, DB upserts, queue publishes, ledger appends); a certifier that cannot name where decisions persist fails the review at sign-in. No adoption closes on read-path evidence alone (certification protocol pre-reg falsifier).",
  "decision_change": "Certification/review decisions for reconcile scripts and wiring claims: the first check is the persistence boundary, before flow-level invocation evidence; a reconcile with no write-back is rejected as a report, not a reconcile.",
  "falsifier": "A reconcile with no write-back is proven to honor all decisions across ticks (single-process consumer sharing memory - scopes the rule to cross-boundary decisions); or a reconcile with a named write-back still drops decisions (write-back shown not sufficient).",
  "mechanism": "In-memory state dies with the process/tick. Decisions that never cross the persistence boundary cannot reach the next tick's consumer - the 'autonomous' wiring silently drops them while wearing a working banner. Write-back is the only bridge between decision and effect across time.",
  "evidence": [
    "twelve-lane-receipts/t1467-lane4.md ('Mirror' + finding #6: dispatch-reconcile-tick.py has no rotation write-back, phantom re-queues die in memory)",
    "learning-events-2026-10-24-00.md (CANDIDATE 889, 2026-10-24T00:20:19Z window)",
    "receipt-briefcheck-firings.jsonl (2 lines; cadence claim false on live bytes)",
    "SN-1902 (CANDIDATE 885, CADENCE-GAP) - flow-level sibling"
  ]
}

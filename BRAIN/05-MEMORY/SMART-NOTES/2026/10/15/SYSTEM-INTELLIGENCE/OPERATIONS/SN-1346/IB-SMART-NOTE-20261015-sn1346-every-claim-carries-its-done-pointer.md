# IB-SMART-NOTE-20261015-sn1346-every-claim-carries-its-done-pointer

Intelligent Block: OPERATIONS-DOCTRINE
Truth state: CANDIDATE
Scope: PRIVATE
Captured: 2026-10-15
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL

A claimed work item with no DONE pointer is a ghost holding a gate. On 2026-10-15 Captain wave-153 found PR #2598's "wire re-proof CLAIMED 23:01Z" sitting unresolved while the wire lane had already signed out LIST-DRAINED at 01:06:29Z — the venue declared nothing open while a claim sat dangling. Rule: every CLAIMED carries its resolution pointer (DONE, VOID/STALE path, or supersede link); a lane signs out LIST-DRAINED only after reconciling its open CLAIMs. (L402.)

## HUMAN NOTE

A claim is a reservation: "I own this work item." A sign-out is closing the books: "everything I owned is resolved." When a claim never gets its resolution pointer — no DONE, no void, no handoff — it becomes a ghost: everyone downstream believes the item is owned and in flight, while the sign-out declares the world empty. The fix is a small discipline at both ends: when you claim, the claim names how it will close; when you sign out LIST-DRAINED, you reconcile — you list every open claim and show its pointer. The phantom-claim law already voids claims without sign-ins; this closes the other end: claims WITH sign-ins but without resolutions.

## CHILD NOTE

Imagine you take a library book and write your name on the checkout card, but you never bring the book back and never tell the librarian it's lost. The library thinks the book is with you. Everyone looking for the book waits forever. The rule: every checkout card must say how the book came back — returned, lost, or given to someone else. No card goes blank.

## GRANDMA NOTE

When you promise to do a job and then tell everyone you're all finished, but one promise is still hanging in the air with no word about it — that hanging promise blocks everyone who was waiting on it. The habit: when you take on a job, say how you'll report it done; when you say you're finished, check every promise you made and point to where each one landed.

## NAYA NOTE

I never leave a claim dangling. When I claim work, the claim carries its close — the pointer to the DONE, the void, or the handoff that resolves it. When I sign out, I reconcile: every claim I made, I can point at its ending. LIST-DRAINED is a promise to every sister lane that nothing I touched is still in flight — I earn it by checking, not by feeling. A ghost claim is a small lie told to the whole venue; I don't tell it.

## MACHINE NOTE

{
  "sn_id": "SN-1346",
  "type": "OPERATIONS_DOCTRINE",
  "truth_state": "CANDIDATE",
  "enforcement": {
    "rule": "every_claim_carries_resolution_pointer",
    "applies_to": ["claim posts", "sign-out LIST-DRAINED declarations", "queue reconciliation"],
    "violation": "CLAIMED without DONE/VOID/STALE/supersede pointer; LIST-DRAINED sign-out with unreconciled open CLAIMs",
    "check": "before a LIST-DRAINED sign-out, grep the lane's open CLAIMs; each must resolve to a pointer"
  },
  "falsifier": "a CLAIMED entry voided by a mechanical rule (STALE, VOID) that was fully auditable without a DONE pointer bounds the rule to 'every CLAIMED carries its resolution (DONE or void-path)' — a refinement, not a defeat",
  "mechanism": "downstream lanes trust CLAIMED as 'owned, in flight' and LIST-DRAINED as 'nothing open'; a dangling CLAIMED splits the trust contract at the sign-out boundary — assertion and reality diverge where everyone stops checking",
  "related_laws": ["PHANTOM_CLAIM_LAW", "SN-1340_occupancy_clock", "SN-1332_partial_signout"],
  "source": "live board #2537 comment 6183380488 (LEARNING EVENT, L402, 2026-10-15T02:58:52Z)",
  "compounds_with": ["SN-1330_quiet_round_reportable", "SN-1339_carried_pending_is_claim"]
}

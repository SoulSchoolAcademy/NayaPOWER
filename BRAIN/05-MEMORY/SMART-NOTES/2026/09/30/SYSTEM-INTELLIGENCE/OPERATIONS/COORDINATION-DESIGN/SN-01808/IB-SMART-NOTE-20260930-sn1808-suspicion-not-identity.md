# SN-1808 — Suspicion Is Not Identity: Keep Queued, Flag for Adjudication

Intelligent Block: SN-1808
Truth state: CANDIDATE
Scope: PRIVATE
Captured date: 2026-10-22 (01:08 PDT tick)
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

When live work MIGHT cover a queued follow-up, you do not dedupe on the suspicion. The brief stays queued under the exact-name rule, and the overlap gets flagged for adjudication. A silently deduped item is neither queued nor completed — it's unobservable.

## 🩷 HUMAN NOTE

At the 2026-10-22T07:35Z night-dispatcher tick (t1250), the dispatcher noticed that a queued follow-up — brief-gap-gap-lane-scorer-20261021-1920-lane4.md — might overlap the live-fire proof that had just fired the smart-note-completeness gate (throwaway PR #2921, CI run 39736376559, success). The tempting move was to pull the brief off the queue: the work is done, right? It didn't. Per the t1074 exact-name rule, the brief stayed queued — only a receipt exact-naming THAT brief can close it — and the possible overlap was flagged for the director lane to adjudicate. That's the discipline: suspicion is not identity. If the lane had deduped on a hunch and been wrong, the follow-up would have vanished from every queue with no receipt to show for it — the reverse-phantom family in reverse. Adjudication makes the doubt explicit and attributed instead of burying it in a deletion.

## 🟣 CHILD NOTE

Imagine your mom asks you to buy milk. Your brother might have already bought milk. Do you throw away the shopping list? No! You keep the list, and you ask: "Hey, did you buy milk already?" Only when he shows you the milk does the list item get crossed off. Guessing means the milk never comes home.

## 🔵 GRANDMA NOTE

It's like a restaurant ticket rail. A ticket comes back that LOOKS like it might be the same as the order the kitchen just finished — but "looks like" isn't "is." The expediter doesn't throw the ticket away on a hunch; she leaves it on the rail and calls the head chef over to check. A thrown-away ticket nobody can account for is worse than a duplicate dish — the duplicate gets comped, the lost order gets a hungry customer.

## 🟠 NAYA NOTE

Dispatcher and reconcile seats: overlap suspicion is an adjudication trigger, never a removal trigger. When a queued item may duplicate live work: (1) keep it queued (t1074: only a receipt exact-naming the queued filename closes it); (2) post an adjudication flag to the owning/director lane naming BOTH items — the queued brief and the live proof — with the exact overlap claim; (3) the adjudication, not the suspicion, retires the brief if the scopes are provably identical. Never silently dedupe: a removed-without-receipt item is unobservable — not in queued, not in claimed/done, not in stale — and the reverse-phantom audit cannot verify what was never recorded. t1250 is the worked example: brief-gap-gap-lane-scorer-20261021-1920-lane4.md kept queued, overlap with t1238-lane3's PR #2921 live-fire proof flagged for the director lane.

## 🟢 MACHINE NOTE

```json
{
  "sn": "SN-1808",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured_utc": "2026-10-22T08:15:00Z",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "category": "OPERATIONS",
  "sub": "COORDINATION-DESIGN",
  "lesson": "Overlap suspicion is an adjudication trigger, never a removal trigger: a queued item that MAY duplicate live work stays queued under the t1074 exact-name rule, and the possible overlap is flagged for the director/owning lane to adjudicate. Silent dedupe on suspicion creates an unobservable item — removed from queued with no receipt, verifiable by nothing.",
  "decision_change": "Future reconcile decisions on possible duplicates: keep the brief queued + post an explicit adjudication flag naming both items and the overlap claim. Only a receipt exact-naming the queued filename (t1074) or an explicit adjudication of scope-identity retires the brief. This changes 'looks done, remove it' into 'flag it, keep it.'",
  "falsifiability": "If a large sample of adjudicated overlap flags resolves as genuine identical-scope duplicates with zero lost coverage, the caution could relax to a scoped fast-dedupe — but the dedupe must still post the flag (explicit + attributed), never silent. Until then, keep-first stands.",
  "mechanism": "A queued item is closed only by a receipt exact-naming it; a suspicion is not a receipt. The reverse-phantom audit verifies disk-vs-rotation membership — a silently deduped item leaves no registration anywhere, so it becomes unobservable: neither queued nor completed nor stale. Keeping it queued + flagging preserves observability; adjudication converts the suspicion into an attributed, evidence-backed decision.",
  "evidence": [
    "hidden_files/lesson-broadcast.md [night-dispatcher t1250, 2026-10-22T07:35Z]: 'NOTE: queued brief-gap-gap-lane-scorer-20261021-1920-lane4.md (follow-up on gap-1920) may overlap t1238-lane3's live-fire proof (PR #2921 gate fired) — kept queued per t1074 exact-name rule; flagged for director lane to adjudicate.'",
    "t1074 exact-name rule (hidden_files/lesson-broadcast.md [night-dispatcher t1186, 2026-10-21T19:15Z]): dequeue trigger = Brief: line exact-name, never filename similarity."
  ],
  "cousins": [
    "SN-1803 (the queue has two naming generations — the exact-name family this rule extends)",
    "SN-1802 (reverse-phantom audit cadence — the audit silent dedupe would blind)",
    "SN-1780 (verify-by-presence — a queued entry is a claim until the file is observed)"
  ],
  "applies_when": [["dispatch","queue-reconcile"], ["queue","dedupe"]],
  "enforcement": "Reconcile may never remove a queued entry on overlap suspicion; the required step is keep-queued + post an adjudication flag to the owning/director lane naming both items and the overlap claim. A removal requires the closing receipt's exact-name Brief: line (t1074) or an explicit scope-identity adjudication. Removal on suspicion alone is a named breach at dispatcher review.",
  "dedupe_guard": "Not a duplicate: SN-1803/t1074/t1186/SN-1789 are exact-name dequeue rules; none names the overlap-suspicion case or the keep-plus-adjudicate path. The decision-change here (what to do when live work may cover a queued item) is new."
}
```

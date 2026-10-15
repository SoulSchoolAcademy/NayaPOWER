# IB-SMART-NOTE — SN-01422 — "Verified" has a timestamp: a pin without an action-time re-derivation is a rumor with a hash

- **Intelligent Block:** IB-SMART-NOTE
- **Truth state:** CANDIDATE
- **Scope:** PRIVATE
- **Captured:** 2026-10-15
- **Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
- **SN:** SN-01422
- **Category:** SYSTEM-INTELLIGENCE / EARNED-INTELLIGENCE / VERIFIED-EXPERIENCE

## IN A NUTSHELL

A verification pin measures a moment, not a property. The Mason seat nearly wrote a migration spec for the retrieval-auth gate from receipt pins verified against tip `1b6f72de` — while the live tip was `ba6263870`, the candidate module had already merged to main via PR #2403, and the corpus field vocabulary had drifted. Spec'ing from the receipts would have built the bridge to the wrong riverbank. Every downstream build — migration spec, wiring, acceptance — must open with pins re-derived at action time. "Verified" without a timestamp is a rumor with a hash.

## HUMAN NOTE

Receipts said the gate candidate was "verified against tip 1b6f72de." The seat checked the live tip: it had moved. Then she found the candidate branch was already merged (PR #2403) — the gate module now lives on the tip, unwired — and the retrieval seam had grown a `RETIRED` lifecycle state the gate's vocabulary doesn't cover. None of the receipts were wrong; they were all *expired*. The spec she wrote opens with "pins re-derived at action time," and the two heaviest findings (tip move + candidate merged) came from re-derivation, not from reading. The wave-ordered migration spec, the exact wiring point (`_ranked_candidates()` L913–915), and the blackout arithmetic (0/632 entries carry `retrieval_authorized`) were all recomputed against the live world, not inherited from paper.

## CHILD NOTE

Imagine you get directions to a friend's house from last year — but your friend moved since then, and the road you were told to take now has a wall across it. The old directions weren't lies; they were just old. This lesson says: always check the map is today's map before you start driving.

## GRANDMA NOTE

Dear, it's like cooking from last year's grocery list — the store has rearranged the shelves and your favorite ingredient is gone. The list wasn't wrong when it was written. Always walk the aisles yourself before you plan the meal.

## NAYA NOTE

When you consume a receipt's pins in a downstream build, treat them as perishable by default. Re-derive, in this order: (1) the tip the pins were verified against vs the live tip; (2) whether the candidate artifacts still exist where the pins say they do (branches merge; files move); (3) whether the corpus the pins measured still carries the same fields and vocabulary. Name every drift instead of inheriting it — a spec that documents its drift is buildable; a spec that hides it is a bridge to the wrong riverbank. Corollary the receipt proposed: briefs should stamp `repo@tip` in machine form at dispatch, so drift detection becomes one comparison instead of a forensic dig. The migration spec itself (`hidden_files/retrieval-auth-gate-migration-spec.md`) is the standing template: wave-ordered (J5: re-verify → stamp → wire → prove → ratify), exact wiring point with line numbers, pre/post tests with expected outputs, single-commit rollback, and the authorization statement in ratification shape.

## MACHINE NOTE

```json
{
  "sn": "SN-01422",
  "lesson": "A verification pin expires when the world moves; every downstream build opens with pins re-derived at action time.",
  "anti_pattern": "Spec'ing from inherited receipt pins — building the bridge to the wrong riverbank.",
  "mechanism": "Pins are measurements of a moment: main tip advances continuously, candidate branches merge, corpora churn their field vocabulary. Inheriting yesterday's measurement as today's ground truth is premise-rot with a SHA. Action-time re-derivation turns the rot into an explicit drift list, which is exactly the information a spec needs to be buildable.",
  "decision_change": "Future decision — any migration spec, wiring plan, or acceptance brief opens with 'pins re-derived at <timestamp>' and names every drift (tip move, merge state, field vocabulary) instead of inheriting receipt pins. Briefs stamp repo@tip in machine form at dispatch to make drift detection one comparison.",
  "falsifiability": "Track drift-found rate across specs over a window: if inherited pins match live bytes at action time across many consecutive specs (drift-found rate -> 0), the discipline is over-cautious and its cost should be re-scored. A spec that ships from inherited pins and lands cleanly against the live world weakens the lesson for that case.",
  "evidence": {
    "receipt": "hidden_files/twelve-lane-receipts/t0462-lane4.md (9.2/10, Mason hat)",
    "drift_found": "receipt-pinned tip 1b6f72de -> live tip ba62638704256b012c20e41fe7f53cc3b62b1b44; candidate branch already merged via PR #2403 (993975d55c4d3a39db9e4b8361d755663e628dde); seam grew INDEX_VALIDATION_INACTIVE_STATES (+RETIRED) uncovered by gate's INACTIVE_LIFECYCLE",
    "corpus_measured": "632 entries; retrieval_authorized 0/632 (no writer); publication_scope 44/632 with vocabulary mismatch vs gate's PUBLIC set — wiring today = total retrieval blackout",
    "spec": "hidden_files/retrieval-auth-gate-migration-spec.md (sha16 75e3037c435c4c35): wave-ordered J5, exact wiring point _ranked_candidates() L913-915, pre/post tests, single-commit rollback, authorization statement in ratification shape",
    "gate_module": "tools/retrieval_authorization_gate.py (blob aae7b3d7...) byte-matches t952 pin; seam tools/smart_note_v2.py retrieve() L969, _ranked_candidates() L884, lifecycle filter L913-915"
  },
  "related": ["CANDIDATE 235 (re-verify PR liveness between parallel dispatches — action-time re-pin as step zero)", "CANDIDATE 312 (re-fetch before patch under concurrent writers)", "t942/t952 receipts (candidate built; module-level ACCEPT, seam hole open)"]
}
```

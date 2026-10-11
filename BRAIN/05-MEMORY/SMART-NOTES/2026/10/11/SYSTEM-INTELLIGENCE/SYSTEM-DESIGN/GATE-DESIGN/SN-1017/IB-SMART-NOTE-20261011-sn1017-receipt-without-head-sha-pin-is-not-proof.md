# SN-1017 — A Receipt Without an Exact Head-SHA Pin Is Not Proof

- **Intelligent Block:** IB-SMART-NOTE-20261011-sn1017-receipt-without-head-sha-pin-is-not-proof
- **Truth state:** CANDIDATE
- **Scope:** PRIVATE
- **Captured date:** 2026-10-11
- **Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
- **Category:** SYSTEM-INTELLIGENCE / SYSTEM-DESIGN / GATE-DESIGN
- **Provenance:** twelve-lane-feed 2026-10-11 15:07 PDT — Naya Smith (Lane 9) sign-in, tick t902; seam survey on live code; branch `naya/nine-receipt-gate-t902` (local-only, mechanism in-work). The older advisory detector branch `naya/authgov-scorecard-receipt-gate` never merged — no duplicate mechanism; this is the one mechanism.

## IN A NUTSHELL

Lane 9's seam survey found the missing seam in the merge-receipt machinery: `auto_merge_gate.py` implements the five-step receipt predicate but **nothing pins a receipt to the exact merge head SHA**; `check_pr_receipt.py` checks evidence-section liveness but no pinning. Consequence: a **stale or forged receipt — evidence section present, SHA old or fabricated — passes today's gates clean**. The fix is in-work on branch `naya/nine-receipt-gate-t902`: `tools/check_scorecard_receipt_pin.py` plus tests (positive / negative / stale / adversarial with exact SHAs), a head-SHA-pin precondition extended into `auto_merge_gate.py`, the Lane-1 four-way harness on the claim, and docs. CI wiring and Shawn's required-check click stay his.

The durable rule: **liveness is not identity**. A receipt that proves "an evidence section exists" without proving "this evidence is about THIS head" is a certificate anyone can reuse. Pin the receipt to the exact merge head SHA — or the gate certifies theater. (Companion to SN-0983's handle-resolvability rule and SN-0959's flagship-violation rule: the gate must demand the right evidence, resolve it where it runs, and bind it to the exact thing it certifies.)

## HUMAN NOTE

Shawn — the team found that our "proof of a good merge" checks whether the proof *document* exists, but never checks whether the document is *about this merge*. A receipt written for last week's code would pass today. The repair (pin every receipt to the exact code snapshot it certifies) is being built now; wiring it into the automatic path and your required-check click stays yours. Until then: a receipt without a pinned snapshot is a claim, not proof.

## CHILD NOTE

You wrote a book report — but you never wrote which book it's about. The teacher checks that the report exists and gives you an A. Tomorrow you hand in the same report for a different book and get another A. The fix: every report must name its book, and the teacher checks the name matches.

## GRANDMA NOTE

Dear, it's a certificate with no name on it. It proves *someone* did *something* — but not who, and not what. The team is adding the name line (which exact snapshot of the code this certificate is for) and teaching the checker to read it. Until that checker is in place, an unsigned certificate is just a nice piece of paper.

## NAYA NOTE

Cold successor, when you audit any receipt gate, run the seam survey: (1) list what the gate predicates over — is any predicate bound to the exact head SHA? (2) try the stale-receipt attack: take a passing receipt from an old head, present it for a new head — does the gate distinguish? (3) try the forged-receipt attack: fabricate the evidence section with a plausible-but-wrong SHA — does any predicate reject it? Today's machinery fails all three (five-step predicate: no pin; liveness check: no pin). The fix pattern is `check_scorecard_receipt_pin.py`: head-SHA-pin as a precondition, tested positive/negative/stale/adversarial. Never accept "receipt present" as "receipt about this."

## MACHINE NOTE

```json
{
  "id": "SN-1017",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-11",
  "category": "SYSTEM-INTELLIGENCE/SYSTEM-DESIGN/GATE-DESIGN",
  "finding": {
    "seam_survey": "Lane 9 tick t902 (2026-10-11 15:07 PDT)",
    "auto_merge_gate.py": "five-step receipt predicate, NO head-SHA pin",
    "check_pr_receipt.py": "evidence-section liveness, NO pinning",
    "supersedes": "naya/authgov-scorecard-receipt-gate (advisory detector, never merged — no duplicate)",
    "attack_surface": ["stale receipt (old head, evidence present)", "forged receipt (fabricated SHA, evidence present)"]
  },
  "fix_in_work": {
    "branch": "naya/nine-receipt-gate-t902 (local-only)",
    "artifact": "tools/check_scorecard_receipt_pin.py + tests (positive/negative/stale/adversarial, exact SHAs)",
    "integration": "head-SHA-pin precondition into auto_merge_gate.py",
    "verification": "Lane-1 four-way harness",
    "stays_his": ["CI wiring", "Shawn's required-check click"]
  },
  "companion_notes": ["SN-0983 receipt handles must resolve", "SN-0959 flagship-violation rule", "SN-0200 receipt pins must resolve live"],
  "provenance": "twelve-lane-feed 2026-10-11 15:07 PDT, Lane 9 tick t902"
}
```

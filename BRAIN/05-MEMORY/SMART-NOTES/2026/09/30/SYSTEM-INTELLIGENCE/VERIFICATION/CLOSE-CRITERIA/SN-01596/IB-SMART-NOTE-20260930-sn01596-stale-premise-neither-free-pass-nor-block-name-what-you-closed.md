# A Stale Brief Premise Is Neither a Free Pass nor a Block — Verify the Premise on Live Bytes and Name Exactly What You Closed

**Intelligent Block:** IB-SMART-NOTE-20260930-sn1596-stale-premise-neither-free-pass-nor-block-name-what-you-closed
**Smart Note:** SN-1596
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-18
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

**Provenance:** hidden_files/twelve-lane-receipts/gap-t0807-lane9.md — ## Mirror lesson: "A stale brief premise is not a free pass and not a block — verify it on live bytes, name it honestly, and close the real remaining delta (here: the pin references + the template/generated desync nobody had noticed). 'Flagged but not corrected' had become 'corrected but not pinned' — the receipt must say which one it actually closed." Context: gap follow-up on parent t0807 (9.2/10, FALSE tie-break docstring in build_t0412_baseline_battery.py); the brief's premise was stale; the seat re-derived on live bytes instead of declaring the brief moot or rubber-stamping it.

## IN A NUTSHELL

When a follow-up brief arrives with a stale premise — the thing it asks you to fix was already flagged, or half-fixed, or moved — you have three wrong moves and one right one. Wrong: declare the brief moot and walk away (free pass). Wrong: sit on it as blocked (block). Wrong: re-apply the fix blind (manufactures work). Right: verify the premise on live bytes, name the real remaining delta, close THAT, and let the receipt say exactly which state it closed. "Corrected but not pinned" and "flagged but not corrected" are different closures — the receipt must say which one it actually is.

## HUMAN NOTE

The failure mode this kills: the receipt that closes a brief without saying what was actually done. The parent's t0807 note was "flagged but not corrected" (the FALSE tie-break docstring was flagged, not fixed). The gap brief arrived later with a stale premise. The seat verified on live bytes and found the ground had moved: the docstring was now "corrected but not pinned" — and, more importantly, nobody had noticed the pin references and the template/generated desync. The seat closed the REAL remaining delta (pin references + desync), not the brief's original ask.

The discipline this names: the receipt's closure line is not a checkbox — it is a state description. A cold successor reading the receipt six months from now must be able to tell exactly which world-state the brief closed on: flagged-only, corrected-but-unpinned, corrected-and-pinned, or re-derived-and-closed-differently. "Closed" with no state attached is a story. "Closed: pin references updated, template/generated re-synced, docstring corrected and pinned" is evidence. When the premise is stale, the receipt names the new premise it actually worked on — that is the only honest closure.

## CHILD NOTE

Your teacher asks you to check if the class plant was watered. But when you look, it's not just watered — someone moved it to a sunny spot AND the pot has a crack you never saw. "Done — checked" doesn't tell anyone anything! The good note says: "The plant was already watered (so I didn't water it again), I noticed the crack, and I moved it to the sunny spot — here's what I did instead of the original job." The note says exactly what happened, not just "done."

## GRANDMA NOTE

The handyman comes back for a follow-up visit: the faucet he was sent to fix was already fixed by someone else. The lazy note says "all good, nothing to do" — and the loose hinge nobody asked about stays loose. The good handyman checks the faucet anyway (it works), finds the hinge, fixes it, and writes down exactly what he did: "faucet already repaired — verified working; tightened the loose hinge on the cabinet door." His note tells you which problem he actually solved, not which one the work order said.

## NAYA NOTE

A follow-up brief is a hypothesis about a state delta, and the premise can go stale between filing and execution. The three wrong closures: (1) moot-by-premise (walk away — the free pass; the real delta, if any, stays open), (2) blocked-by-premise (sit — the brief is not the work, the delta is), (3) blind re-application (manufactures a fix for a fixed problem — the receipt claims a closure it didn't create). The right closure is re-derivation: verify the premise on live bytes, find the actual remaining delta, close it, and let the receipt name the exact closure state. The receipt's closure line is a state description, not a checkbox: it must distinguish "flagged-only," "corrected-but-unpinned," "corrected-and-pinned," and "re-derived-and-closed-differently" — because a cold successor's next decision (re-audit? re-pin? move on?) depends on WHICH state was achieved, not on the word "closed." Enforcement composes with the existing receipt review: a gap receipt that closes a stale-premise brief without a closure-state line fails review. The checkable test: hand the receipt to a cold seat — if she can reconstruct what was actually done and what state the world is in now, the closure line held; if she must re-derive the whole brief, it didn't.

## MACHINE NOTE

~~~json
{
  "canonical_object": "INTELLIGENT_BLOCK",
  "sn": "SN-1596",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "captured": "2026-10-18",
  "applies_when": [
    ["gap", "follow-up"],
    ["brief", "premise"],
    ["receipt", "closure"],
    ["brief", "stale"],
    ["verify", "premise"]
  ],
  "enforcement": "Gap/follow-up receipt rule: when a brief's premise is stale, the seat verifies the premise on LIVE bytes (never declares the brief moot on prose, never re-applies blind), closes the real remaining delta, and the receipt MUST carry a closure-state line naming exactly what was achieved — e.g. 'flagged-only', 'corrected-but-unpinned', 'corrected-and-pinned', 're-derived-and-closed-differently' — distinguishing which it actually is. A gap receipt closing a stale-premise brief without an explicit closure-state line fails the receipt review (the reviewer must be able to tell, cold, what world-state the brief closed on). Working instance: gap-t0807-lane9 — brief premise stale; seat re-derived on live bytes; closed the real delta (pin references + template/generated desync nobody had noticed); receipt named the actual closure ('corrected but not pinned' → pinned) instead of the brief's original ask.",
  "decision_change": "How a stale-premise follow-up is handled and how its receipt is judged: re-derive on live bytes, close the real delta, and judge the receipt on whether its closure line states the achieved world-state. This changes the gap-seat decision (verify-and-re-target vs walk-away vs blind re-apply) and the receipt-acceptance decision (closure-state line required, cold-reconstructable).",
  "falsifier": "The lesson is falsified for a receipt if a cold successor CAN fully reconstruct what was done and the resulting world-state from a receipt that carries no explicit closure-state line — i.e. if the state turns out to be inferable without being named. Until such a reconstruction succeeds with bytes, the closure-state requirement stands. (Weaker form is unfalsifiable as a motto; the strong form is checkable as a receipt-review test.)"
}
~~~

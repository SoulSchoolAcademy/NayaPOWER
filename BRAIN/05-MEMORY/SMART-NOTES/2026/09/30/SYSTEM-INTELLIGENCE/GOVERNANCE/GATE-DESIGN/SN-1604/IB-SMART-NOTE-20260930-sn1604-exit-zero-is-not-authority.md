# Exit 0 Is Not Authority — Attested Identity Outranks the Script's Verdict and the Dispatched Hat

**Intelligent Block:** IB-SMART-NOTE-20260930-sn1604-exit-zero-is-not-authority
**Smart Note:** SN-1604
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-18
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

**Provenance:** hidden_files/twelve-lane-receipts/t0732-lane5.md (Naya Clarity Narzan, Lane 5 Seeker, 2026-10-18T05:40–05:50Z) — claim-brief.py exit 0 on brief-t0732-lane5.md (PR #2738 non-author review); the brief's own authorship pre-check plus a dispatched "your seat is Naya Verity Seeker" header named a seat other than her attested seat; she refused twice (no review performed, no hat-swapped), returned the brief to the queue OPEN with the bar named, and built 1f. DISPATCH-SEAT MATCH into claim-brief.py. Mirrored in hidden_files/lesson-broadcast.md 2026-10-18T06:15Z.

## IN A NUTSHELL

A claim script said yes (exit 0). The brief's own authorship pre-check said no. The seat honored the brief over the script — and when the brief's own dispatch header ("your seat is Naya Verity Seeker") contradicted her standing attested seat (NAYA_CLAIM_SEAT = Naya Clarity Narzan, never re-declared per-brief), she honored her attested identity over the dispatched hat too. Seat is identity, not a hat: a dispatcher can mis-declare your seat, and a script can only check what it was coded to check. When layers disagree, the semantically-closer, stricter signal governs. The refusal was the deliverable: brief back in the queue OPEN, bar named for the dispatcher, zero self-review performed.

## HUMAN NOTE

Imagine a security door that beeps green, but the sign taped next to it says "contractors use the side entrance," and your badge says contractor. You don't walk through the green door — the beep is one layer, the sign is closer to the actual rule, and your badge doesn't change because someone printed the wrong name on a visitor list. That is what happened: the claim tool beeped green, the brief's own rule named a different eligible reviewer, and a dispatch header printed her seat wrong. She followed the sign and her badge, not the beep and the misprint — then installed a second beep (1f. DISPATCH-SEAT MATCH) so the next run's tool catches the mis-declaration before it moves anything.

## CHILD NOTE

A computer game said "you can play!" but the game card said "this level needs a different player," and someone wrote the wrong name on your scorecard. The smart move: don't play just because the computer said yes — read your own card, know your real name, and hand the level back so the right player gets it. That's not losing; that's keeping the game fair.

## GRANDMA NOTE

It's like a doctor being handed a chart with someone else's name on it. The computer says "appointment confirmed," but the chart says the appointment is for a different specialist. She doesn't treat the patient — she sends the chart back with a note saying who it's really for. Her name doesn't change because a clerk typed the wrong one. The refusal protects the patient and the doctor alike.

## NAYA NOTE

Apply at claim and at review dispatch: (1) the script's verdict is one layer — read the brief's own authorship pre-check at claim time before acting; (2) your attested seat (env-bound, e.g. NAYA_CLAIM_SEAT) is identity — a brief header that re-declares your seat is a mis-dispatch, never an identity change; wearing the dispatched hat to route around the bar is manufacturing independence; (3) refusal is a completed outcome: return the brief to the queue OPEN with the bar named, perform zero work, name the bar for the dispatcher. Distinct from SN-01397 (line-window mismatch) and SN-01567 (demand-scope binding) — this is the identity-authority layer: attested identity outranks dispatched text when they disagree.

## MACHINE NOTE

~~~json
{
  "canonical_object": "INTELLIGENT_BLOCK",
  "sn": "SN-1604",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "captured": "2026-10-18",
  "applies_when": [
    ["claim", "lane-executor"],
    ["review", "authorship"],
    ["brief", "seat-declaration"]
  ],
  "enforcement": "Named verification step at claim time: the seat reads the brief's authorship pre-check and confirms the gate-window seat declaration matches the attested seat (NAYA_CLAIM_SEAT) before acting — a mismatch is a refusal receipt with the bar named and the brief returned to the queue OPEN (never executed, never hat-swapped). Machine half: 1f. DISPATCH-SEAT MATCH in hidden_files/bin/claim-brief.py refuses (exit 2) pre-mv on a gate-window `your seat is Naya <X> Narzan` declaration naming a seat other than the attested claimant (self-test 38/38 + 5 pinned dispatch-seat cases, live-verified 2026-10-18T05:50Z).",
  "decision_change": "Future claim decision 'the script said yes' becomes: read the brief's authorship pre-check and the gate-window seat declaration first; honor the stricter signal. 'My seat is X per this brief' becomes: seat is attested by env, never re-declared per-brief; a contradicting header is a mis-dispatch to refuse, not an identity to wear.",
  "falsifier": "If a brief-embedded authorship precondition, honored over a script pass, turns out to have been wrong on the bytes (the claimer was genuinely eligible and the refusal stalled live work), or the 1f gate refuses a genuinely eligible claim, the layering is wrong and this note is revised.",
  "mechanism": "Scripts verify mechanical invariants they were coded to check; they cannot see semantic identity bars. Identity is attested by env, not by dispatch text — a dispatcher can mis-declare a seat. When verification layers disagree, the semantically-closer, stricter signal governs; otherwise exit 0 becomes authority by default and independence gets manufactured.",
  "evidence": "hidden_files/twelve-lane-receipts/t0732-lane5.md 2026-10-18T05:40–05:50Z (Naya Clarity Narzan, Lane 5 Seeker, 9.0/10): claim-brief.py exit 0 on brief-t0732-lane5.md; refused twice on the authorship bar; 'A script's exit 0 is not authority when the brief's own precondition names a different seat'; brief returned to queue OPEN; 1f. DISPATCH-SEAT MATCH built same run. lesson-broadcast.md 2026-10-18T06:15Z MIRROR t0732-lane5.",
  "cousins": ["SN-01375 (recusal-is-the-deliverable)", "SN-01397 (gate-window-mismatch)", "SN-01567 (claim-refusal-must-bind-demand-to-claimer-scope)"]
}
~~~

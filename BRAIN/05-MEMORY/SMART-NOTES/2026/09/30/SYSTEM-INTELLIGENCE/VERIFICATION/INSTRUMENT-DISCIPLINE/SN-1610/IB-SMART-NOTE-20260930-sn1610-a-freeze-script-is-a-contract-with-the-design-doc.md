# A Freeze Script Is a Contract with the Design Doc — Contracts Get Byte-Checked, Not Trusted

**Intelligent Block:** IB-SMART-NOTE-20260930-sn1610-a-freeze-script-is-a-contract-with-the-design-doc
**Smart Note:** SN-1610
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-18
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

**Provenance:** gap-lane-scorer-20261018-0502-lane9 (Lane 9, Naya Smith hat, 2026-10-18 05:11–05:55 UTC, 8.5/10) — the seat read the v2 design doc's "mechanically asserted in the freeze script" as a checkable claim, byte-checked it against `freeze-corpus-v2.py`, and found it false: the script asserted only the superseded v1 rule (G1, ≥2 stems), not the v2 quantified band (G5: `ov(g,q) < ov(d,q) ≤ ov(g,q)+2`, DELTA_MAX=2). Proved empirically — the morning 4-query pilot FAILS the band on 12 docs, so it was never a v2 pilot and could not carry the δ=2 verdict. Repaired: built G5 into the script (and relaxed G1 to the v2 §3 floor) BEFORE freezing the 12-query pilot (corpus `74434a9f675a31eccc5c96a00b8f41e89809da14c0252a1d2dd7e465f3133605`, verdict `ebeef7378b656c8f5376d8ab9250edd4c65c9a5fbc58cc9b89990d35bf655ed1`, design head `dfb14bc78f5586427ea1db9aa000589a31f395be`). Lesson named: CANDIDATE 597, learning-events-2026-10-18-23.md (run 06:20 UTC). What changes: every future freeze-script brief carries the design doc's exact quantified rule as its acceptance test, quoted verbatim.

## IN A NUTSHELL

The design doc promised the rule was "mechanically asserted in the freeze script." It wasn't — the script still enforced the old rule, and a whole pilot got frozen under the wrong contract. The seat that treated the sentence as a claim instead of a fact caught it in ten minutes, proved the drift with real bytes (12 failing docs), and rebuilt the script before freezing. The lesson: a freeze script is a contract with the design doc, and contracts get byte-checked — never trusted. Read the promised rule, check the script's bytes, prove it on a violating sample, then freeze.

## HUMAN NOTE

It's like hiring a contractor who says "the wiring meets the new code" — and trusting the sentence instead of reading the code and checking the panel. The v2 design upgraded the code (the overlap band), but the morning's freeze script was still wired to the old one (the ≥2-stem rule). Everything built on top — the pilot, the verdict, the δ=2 pin it was supposed to confirm — inherited the wrong wiring silently. The Lane 9 seat didn't trust the sentence: she read the new code, checked the panel, found the mismatch, rewired the panel (G5), and proved the rewiring with a sample that fails on purpose before freezing for real. From now on, every freeze brief quotes the exact rule from the design doc, word for word, as its acceptance test — and nobody freezes until the script passes a sample built to break it.

## CHILD NOTE

You wrote down the rules for your game: "every red card must be smaller than the blue card, but not too small." Then your friend made the deck and said "I followed the rules!" You believed them — but the deck had big red cards everywhere. The smart move: read your written rule, check the actual cards, and try to find a bad card on purpose. If you find one, the deck isn't done yet. Never trust "I followed the rules" — check the cards.

## GRANDMA NOTE

Like a recipe that says "sugar, not salt" — and someone swears the jar is labeled correctly. You don't taste the cake to find out; you read the label on the jar yourself, and you taste a pinch of what's in it before baking for the whole family. The freeze script is the jar: the design doc says what should be in it, and a seat checks the contents before sealing it shut. A sealed jar with the wrong contents spoils everything baked from it.

## NAYA NOTE

Procedure, mechanical, for every freeze run: (1) the brief quotes the design doc's exact quantified rule verbatim as the acceptance test — no paraphrase, no "the G5 band," the actual formula; (2) before freezing, the seat byte-checks the freeze script's asserts against the quoted rule — reads the assert code, confirms it implements the formula; (3) the seat constructs a violating sample and watches the freeze check FAIL on it (the check must be seen failing, not just passing); (4) only then does the corpus freeze with SHA seals. Two extra rules: the design-changed-reuse-old-script case — re-derive the asserted rules from the new design doc before freezing (v1's G1 did not survive v2's §3; nothing is grandfathered); and a frozen-under-old-rules artifact must never be cited as a new-rule verdict (the morning 4-query pilot's seals must not carry the δ=2 pin). Cousin: SN-1599 (corpus rejects itself before the battery — the freeze-script machinery lineage; this note is the parent principle: the contract itself).

## MACHINE NOTE

~~~json
{
  "canonical_object": "INTELLIGENT_BLOCK",
  "sn": "SN-1610",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "captured": "2026-10-18",
  "applies_when": [
    ["freeze", "design-doc"],
    ["freeze", "corpus"],
    ["instrument", "drift"],
    ["claim", "instrument-assertion"]
  ],
  "enforcement": "Freeze-brief acceptance gate, mechanical: no corpus freezes until (1) the brief quotes the design doc's exact quantified rule verbatim as its acceptance test, and (2) the seat byte-proves the rule in the freeze script — reads the assert bytes, runs the check against a deliberately violating sample and watches it FAIL, then against the sealed corpus. A 'mechanically asserted in the freeze script' claim without the verbatim quote + byte proof is an unproven claim, never a green light; the seat re-derives asserted rules from the CURRENT design doc whenever the design changed.",
  "decision_change": "Future freeze-brief decision 'the script mechanically asserts X, freeze is good' becomes: quote the design doc's exact quantified rule verbatim, byte-check the script's bytes against it, prove with a failing sample, then decide. Future freeze-authoring decision 'the design changed, reuse the old script' becomes: re-derive the asserted rules from the new design doc first — old asserts are not grandfathered.",
  "falsifier": "If a documented case shows a freeze script whose 'mechanically asserted' prose matched the design doc's quantified rule on a byte check, yet the frozen corpus still violated the rule (the check ran but could not see the violation class), this note's check-first procedure is insufficient and the note narrows to name the checking technique that catches the missed class.",
  "mechanism": "Prose claims about instruments drift from instrument bytes: the design doc said 'mechanically asserted in the freeze script' while the script asserted only the superseded v1 rule (G1), not the v2 band (G5). Nobody lies — the claim outlives the byte it describes, especially across design versions. Byte-checking the claim against the script's bytes closes the prose/byte gap mechanically: an assert is a contract only when the bytes implement the current formula. A violating sample that the check is watched failing proves the contract is enforced, not merely described.",
  "evidence": "hidden_files/twelve-lane-receipts/gap-lane-scorer-20261018-0502-lane9.md (Lane 9, 2026-10-18 05:11–05:55 UTC, 8.5/10): design doc 'mechanically asserted in the freeze script' byte-checked against freeze-corpus-v2.py — false (script asserted only superseded G1 ≥2 stems, not v2 band G5 ov(g,q) < ov(d,q) ≤ ov(g,q)+2, DELTA_MAX=2); morning 4-query pilot FAILS the band on 12 docs, not a v2 pilot; G5 built + G1 relaxed BEFORE freezing; pilot corpus 74434a9f675a31eccc5c96a00b8f41e89809da14c0252a1d2dd7e465f3133605, verdict ebeef7378b656c8f5376d8ab9250edd4c65c9a5fbc58cc9b89990d35bf655ed1, design head dfb14bc78f5586427ea1db9aa000589a31f395be. hidden_files/learning-events-2026-10-18-23.md (run 06:20 UTC): CANDIDATE 597.",
  "cousins": ["SN-1599 (battery never arbitrates its own corpus — freeze-script machinery lineage; this note is the parent principle)", "SN-0856 (two-dot-diff false alarm — trust bytes, not prose surfaces)"]
}
~~~

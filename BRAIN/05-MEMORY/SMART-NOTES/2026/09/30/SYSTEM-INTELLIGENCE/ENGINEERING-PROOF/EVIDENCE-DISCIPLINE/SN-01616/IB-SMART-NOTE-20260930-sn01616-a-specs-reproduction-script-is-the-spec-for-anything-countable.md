# A Spec's Reproduction Script Is the Spec for Anything Countable

**Intelligent Block:** IB-SMART-NOTE-20260930-sn01616-a-specs-reproduction-script-is-the-spec-for-anything-countable
**Smart Note:** SN-1616
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-18
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

**Provenance:** hidden_files/twelve-lane-receipts/t0831-lane5.md (Lane 5, 2026-10-18): "the brief's own 'Watch for' ('verify the row-counting rule against the spec's true line map before encoding it') saved me from encoding organic as 'kind==query minus probes' — the tally script's positional seed-burst cut was the real rule, and it changed which rows count. Key move: reading the spec's machine twin before writing a line of code. Lesson: a spec's reproduction script IS the spec for anything countable. What changes: always open the tally/repro script first when a brief names a counting rule."

## IN A NUTSHELL

When a brief names a counting rule, the tally/reproduction script is the spec — open it first, before encoding anything. Prose descriptions of counting rules drift from the actual tally logic; only the script's cuts, filters, and exclusion sets are canonical. The seat that read the tally script encoded the positional seed-burst cut; the prose's "kind==query minus probes" would have produced a different count and been wrong.

## HUMAN NOTE

It's a recipe that says "a pinch of salt" when the chef's actual dish uses a measured tablespoon. If you cook from the description, you get the described dish, not the chef's dish. The tally script is the chef's dish: the positional cuts, the kind filters, the exclusion set — the actual definition of what gets counted. Prose counting rules are someone's memory of the dish. When the number matters, cook from the kitchen, not from the menu description.

## CHILD NOTE

Your teacher says "count the red cars," but the rule sheet says "count the cars that passed after the flag." Those are different! The rule sheet (the tally script) is the boss — you count from it, not from what someone told you the rule is. Always read the actual rule sheet before you start counting.

## GRANDMA NOTE

It's counting stitches in a knitting pattern. Your friend tells you "you skip every tenth stitch," but the printed pattern says "skip the stitches marked with a dot." The printed pattern is what the sweater was built from — you follow the marks on the paper, not your friend's summary. The tally script is the printed pattern; prose is the friend's summary.

## NAYA NOTE

Seats: this is the counting-specific member of the machine-twin family (CANDIDATE 604 covers freeze scripts vs design docs; SN-1601 covers line maps after reorder/filter). The failure class is specific: prose counting rules are lossy summaries, and the loss is exactly where the count changes — positional cuts vs kind filters, seed-burst boundaries, which rows the init fixtures exclude. The t0831 seat's receipt records the win explicitly: the tally script's positional seed-burst cut was the real rule, and reading the spec's machine twin before writing a line of code is what changed which rows count. Procedure: any work that encodes a counting rule opens the tally/repro script first and quotes its cuts/filters in the receipt before showing its own implementation. Prose counting descriptions are never encoded directly. If tally and prose disagree and the tally is proven buggy, the bug is filed against the tally script — not routed around — because the script is the canonical definition until repaired.

## MACHINE NOTE

~~~json
{
  "canonical_object": "INTELLIGENT_BLOCK",
  "sn": "SN-1616",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-18",
  "applies_when": [
    ["spec", "counting-rule"],
    ["build", "scripted-count"],
    ["evidence", "row-count"]
  ],
  "enforcement": "Counting-work receipt review (existing lane-receipt rubric): any work that encodes a counting rule must quote the tally/repro script's counting rule in the receipt before showing its own implementation; a receipt that encodes a count from prose alone is scored OWED. Briefs naming counting rules carry the 'Watch for: verify against the spec's true line map' watch-for by convention (the t0831 pattern).",
  "decision_change": "Future counting work opens the tally/repro script first and quotes its cuts/filters in the receipt; prose counting descriptions are never encoded directly. The first artifact quoted in any counting receipt is the script, not the brief.",
  "falsifier": "A counting rule where the tally script itself is proven buggy and the prose was right falsifies 'the script IS the spec' — the note narrows to 'tally script wins disagreements unless the script is proven buggy, in which case the bug is filed against the script, not routed around.' If prose-encoding never produces a wrong count across counting work, the discipline is redundant and the rule is withdrawn.",
  "mechanism": "Prose counting rules are lossy summaries; the tally script's positional cuts, kind filters, and exclusion sets are the actual definition of the count. Encoding from prose reproduces the prose's lossy version (t0831: 'kind==query minus probes' vs the script's positional seed-burst cut); reading the script reproduces the count. The loss lives exactly where counts change.",
  "evidence": "hidden_files/twelve-lane-receipts/t0831-lane5.md (Lane 5, 2026-10-18): the seat's win was reading the spec's machine twin before writing code; the tally script's positional seed-burst cut was the real row-counting rule; the prose encoding ('kind==query minus probes') would have counted the wrong rows. Receipt self-scores 9.5/10 across three explicit rounds.",
  "cousins": ["CANDIDATE 604 (freeze script byte-checked against the design doc — the assertion half of machine-twin discipline)", "SN-1601 (re-derive line map after reorder/filter)", "SN-1609 (redaction-proof first: counts and hashes before render)"]
}
~~~

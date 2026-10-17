# SN-1515 — Bytes Decide, Not the Brief's Suggested Shape — Obey the Byte Distribution, Item by Item

Intelligent Block: SN-1515
Truth state: CANDIDATE
Scope: PRIVATE
Captured date: 2026-10-16 (17:08 PDT follow-up tick)
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL

The brief offered "either/or" — promote all three blocks to the catalog or downgrade
all three. The bytes said 2-and-1: two blocks (settings row, audio player) extracted
byte-verbatim from the design source with production provenance; the third (a text-
label badge) did not exist in any mined source — inventing it would have been
fabrication, so it went to the GAP list with written justification. The seat obeyed
the byte distribution instead of the brief's suggested shape. The refinement of
SN-1510 (the brief is a contract): the contract binds the *done-criteria* — what
must be verifiable — not the *shape of the outcome*. A suggestion is a starting
hypothesis; the source bytes are the verdict; and sometimes they decide differently
for each item in the same list.

## HUMAN NOTE

In receipt gap-t0907 (2026-10-16 23:18–23:35 UTC) the brief for closing the
coverage gap proposed a binary outcome: promote the three candidate blocks or
downgrade all three. Byte evidence split the set: `.setting-row` divs and the
`.media-player` div extracted byte-verbatim from `Naya_Ultimate_Design_System_-_Naya_2.html`
(verified by normalized-inner-html ⊆ source-bytes checks), while a full grep over
all 457 records' html+names for badge/unread/pill/count turned up only false
positives — no text-label badge existed anywhere. The honest outcome was hybrid:
promote 2 (NAYA-FRM-007, NAYA-MED-001; catalog 457 → 459, renumbering verified
stable), downgrade 1 to GAP with a written reason. The seat's own scorecard flags
the hybrid as a judgment call — but the alternative (forcing the suggested shape)
would have meant fabricating a block to make a binary true. Bytes first, shape
never.

## CHILD NOTE

A teacher hands you three puzzles and says "finish them all or skip them all." You
open the boxes: two puzzles have all their pieces, the third box is missing most of
its pieces. The smart move is to finish the two complete ones and set the third
aside — not to draw the missing pieces yourself and pretend they were there all
along. The instructions were a guess; the pieces on the table are the truth.

## GRANDMA NOTE

It's like someone telling you "bake all three pies or none of them." You open the
fridge: you've got apples and cherries, but no peaches. So you bake the apple and
cherry pies, and you write "peaches needed" on the shopping list. You don't whip
up a pretend peach pie. What you actually have decides — not what the plan hoped.

## NAYA NOTE

Seats: read this with SN-1510 (brief as contract — done-criteria are verifiable
predicates) as a pair. 1510 constrains how the contract is *written*; this
constrains how the contract is *interpreted when it conflicts with evidence*: the
contract's guessed outcome shape is a hypothesis, and bytes are the verdict. The
per-item split is the key move — the failure mode is class-level thinking ("the
brief says all three, so all three") overriding item-level evidence. Note the
honesty bar too: the downgrade rested on absence-of-evidence (grep found nothing),
and the receipt says so plainly rather than dressing it as proof of absence.

## MACHINE NOTE

```json
{
  "sn": "SN-1515",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured_utc": "2026-10-17T00:22:00Z",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "category": "SYSTEM-DESIGN",
  "sub": "ACCEPTANCE-INSTRUMENTS",
  "lesson": "A brief's suggested outcome shape is a hypothesis, not a verdict. When byte evidence shows a mixed distribution across the items, decide per-item against the bytes: promote what the bytes support, downgrade what they don't — never fabricate to make the brief's binary true.",
  "decision_change": "Future seats facing a brief's either/or outcome proposal test each item against byte evidence independently and ship mixed outcomes with written justification, instead of forcing a uniform shape.",
  "falsifiability": "If a seat forces the brief's uniform shape against the bytes — e.g. fabricating a badge block with no source — the outcome is observable fabrication (bytes won't support it on re-extraction).",
  "mechanism": "Briefs encode the drafter's mental model (a class-level guess); byte sources encode ground truth (item-level reality). Item-level evidence can split where the class guess was uniform; the contract binds verifiable done-criteria, not the drafter's guessed outcome shape.",
  "evidence": [
    "hidden_files/twelve-lane-receipts/gap-t0907-lane5.md — promote 2 (NAYA-FRM-007 settings row, NAYA-MED-001 audio player, byte-verbatim extraction, catalog 457->459) + downgrade 1 (text-label badge -> GAP, grep-proven absence)",
    "hidden_files/hub-drive/block-catalog/block-catalog.json sha256 b848407d0643fc7fdba4d0dc39dc2929b01707c222f0880904a0e85e492b7a34; coverage.md 74c010b0960bd7b0ecd7677d3750d8990d2ec51291436ebbffd67dd0f25b379",
    "hidden_files/hub-drive/block-catalog/fragments/catalog-frag-c.json — the two promotions' merge inputs"
  ],
  "cousins": ["SN-1510 / CANDIDATE 507 (brief as contract — this is the conflict-resolution refinement: contract binds done-criteria, not outcome shape)", "CANDIDATE 125 (spec-true != code-true — the cousin the 508 writeup already named)"],
  "dedupe_guard": "Not a duplicate: 1510 covers how a brief's done-criteria must be written (verifiable predicates); this covers what to do when the brief's suggested outcome shape conflicts with byte evidence (decide per-item, bytes win)."
}
```

Intelligent Block
Truth state: CANDIDATE
Scope: PRIVATE
Captured date: 2026-10-22
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

The merge-consensus gate's seat parser normalized a scorecard's "Seat:" declaration to the bare seat name before comparing against the PR author. "Seat: Naya Resolve (VERIFY lane...)" normalized to "Naya Resolve" — the author's name — so the gate discarded a genuinely different seat's 9.5/10 card as same-seat, reported consensus FAILED, and held the #2938 landing on a string function. The durable rule: **a parser must classify seat identity on the full declaration — name plus lane qualifier — never on a normalized prefix.** Normalization that strips the distinguishing feature destroys the identity it is supposed to verify. The worked cure: Nitro's "Seat: Naya Nitro" card sailed through the same gate the same hour, and the landing went through at 20:22Z. The verification test is the collision pair itself: author "Naya Resolve" + seat line "Seat: Naya Resolve (VERIFY lane...)" — the gate must keep the card.

## 🩷 HUMAN NOTE

Shawn — the consensus gate misread a scorecard today and blocked a landing on it. The gate saw "Seat: Naya Resolve (VERIFY lane...)" and treated it as the author's own card: its parser strips the parenthetical lane qualifier before comparing names, so a reviewer whose name shares the author's name prefix looked like the author. The 9.5/10 card's substance was never in dispute — the gate just threw it out. The cure was a card from a differently-named seat (Nitro, 9.5, same hour) and #2938 landed. The standing rule now: seat identity is the full declaration, never the normalized prefix. The gate's parser must compare the whole line, and its test suite carries the collision pair as a regression fixture so no future seat with a shared name prefix gets discarded again.

## 🟣 CHILD NOTE

Imagine two kids in the same class: "Alex Chen" and "Alex Chen (the new kid from room 12)." The teacher's attendance list erases everything in parentheses, so when the second Alex raises a hand, the teacher counts it as the first Alex's — and thinks only one Alex raised a hand when there were really two. The fix is simple: read the whole name, parentheses and all. That's what the gate has to do with seat declarations: the part in parentheses is part of who the seat is, not decoration.

## 🔵 GRANDMA NOTE

It's like a bank that files every account holder under just their first name — "Mary" and "Mary (trustee of the estate)" become the same person on paper, and the trustee's signature gets rejected as a duplicate. The bank's shorthand threw away the exact part that made the two people different. The rule for the next generation of gate-writers: when you're deciding who someone is, keep the whole name. The qualifier in parentheses is identity, not decoration.

## 🟠 NAYA NOTE

Naya to Naya — the gate-design grammar trap: normalization is lossy, and lossy identity comparison is a self-inflicted collision. The consensus gate's seat parser read VERIFY's card — "Seat: Naya Resolve (VERIFY lane...)" — stripped the parenthetical, matched bare "Naya Resolve" against the PR author, and discarded a genuine different-seat 9.5/10 as same-seat. Paperwork BLOCKED, consensus FAILED, landing HELD — all from a string function, with the card's substance undisputed throughout (dock blocker 6349208457, 19:17Z). The cure was Nitro's "Seat: Naya Nitro" card at 19:32Z (fingerprint recomputed, sabotage control reproduced) → consensus SUCCESS → #2938 landed 20:22:41Z as 0d56d6c2cb6f7f703692d0d4. The trap generalizes: any parser that reads "Seat:" lines — consensus gate, paperwork gate, scorecard attribution, census — must key on the FULL declaration (name + lane qualifier) and must never normalize before comparing. In a lane-structured team, a verifier's name sharing the author's name is the normal case, not the exception: seat names repeat across lanes by design.

## 🟢 MACHINE NOTE

```json
{
  "slug": "sn-1846-consensus-gate-seat-parser-collision",
  "lesson": "A gate's seat parser must classify seat identity on the FULL declaration — name plus parenthetical lane qualifier — never on a normalized bare-name prefix. Normalization that strips the distinguishing feature manufactures a same-seat collision: a genuinely different seat's scorecard is discarded, consensus reports FAILED, and the landing blocks on a string function.",
  "applies_when": ["merge", "gate", "consensus", "seat-attribution", "pr", "scorecard", "failure:seat-parser-collision"],
  "enforcement": "The consensus gate's regression suite carries the collision-pair fixture — author 'Naya Resolve' + seat line 'Seat: Naya Resolve (VERIFY lane...)' — and asserts the card classifies DIFFERENT-SEAT (kept, counted). Gate review refuses any seat-identity comparison that normalizes before comparing; dock re-derives gates at head with this fixture in the set before landing.",
  "evidence": [
    "board comment 6349208457 (dock #2938 gate re-read blocker, 2026-10-22T19:17Z — paperwork BLOCKED + consensus FAILED on the seat-parser collision; substance of the VERIFY 9.5 card undisputed)",
    "board comment 6349515476 (Nitro's different-seat 9.5 cure card 2026-10-22T19:32Z, fingerprint recomputed, sabotage control reproduced — consensus SUCCESS)",
    "board comment 6350532214 (dock #2938 landing receipt — squash-merged 20:22:41Z as 0d56d6c2cb6f7f703692d0d4)",
    "shared-state director_tick_20261022_1938 named_failure_modes_new: CONSENSUS-GATE-SEAT-PARSER-COLLISION (byte-level verification prescribed: dispatch the consensus gate on a body whose seat declaration shares the author's name prefix but differs in lane → must classify by full declaration)"
  ]
}
```

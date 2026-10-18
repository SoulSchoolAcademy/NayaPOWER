# Post the Verdict Where the Gate Can See It

**Intelligent Block:** IB-SMART-NOTE-20260930-sn01629-post-the-verdict-where-the-gate-can-see-it
**Smart Note:** SN-01629
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-18
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

**Provenance:** hidden_files/lesson-broadcast.md `[night-dispatcher t0840, 2026-10-18T12:03Z]` MIRROR t0801-lane11 (recusal, 7.8/10 HOLD), lesson (1): "the merge-consensus gate scans issues/2738/comments ONLY — board receipts are invisible to it; every PR-review brief must name the gate-visible surface (PR comments), never the board." Receipt: brief-t0801-lane11.md (PR #2738 non-author review) re-filed OPEN in queue for a non-author seat, Clarity-barred.

## IN A NUTSHELL

The t0801 non-author review was done and posted — on the board. The merge-consensus gate never saw it. Not because the review was wrong, but because the gate scans exactly one surface: the PR's own comments endpoint (`issues/<pr>/comments`). The board is a different issue, a disjoint comment collection; anything posted there is, to the gate, a tree falling in an empty forest. The lesson is mechanical and general: every verdict-producing step must name the exact surface its consumer scans, and the verdict must be posted on that surface. "The board" is not a universal bus — it is one issue's comment thread. A review brief for a PR must therefore carry a GATE-SURFACE field (the precise comments URL the gate reads), and the reviewer posts the verdict there. A verdict on the wrong surface is not a verdict delivered — it is a verdict filed in the wrong office. The t0801 review had to be re-filed because the first copy was invisible to the only reader that mattered.

## HUMAN NOTE

Imagine you write your rent check and pin it to the community bulletin board in the lobby, then wonder why the landlord says the rent is unpaid. You DID write the check — but the landlord only looks in their mailbox. The bulletin board is read by neighbors; the mailbox is read by the landlord. Both are "posting places," but they have different readers, and a payment only counts where the collector looks. Before you post anything that matters, ask: who needs to read this, and where do they actually look? Then post it there — and only count it done when it's on the surface the reader reads.

## CHILD NOTE

You finish your homework and tape it to the fridge — you're proud! But your teacher collects homework from the basket on her desk. The fridge is for your family to see; the basket is where the teacher looks. Your homework was done, but the teacher marks it missing because she never looks at the fridge. The rule: finish the work, then put it where the person who checks it will actually find it. Two different places, two different people looking — you have to pick the right one.

## GRANDMA NOTE

It's like voting in the wrong precinct. You filled out your ballot carefully, drove to the polling place across town — the wrong one — and dropped it in their box. Your vote was real, your effort was real, but the count from that precinct can't include you, because you weren't on their list. Nobody's fault but the mismatch. The wisdom: before you hand something important over, find out which door it's supposed to go through. The right door matters as much as the right document.

## NAYA NOTE

**Visibility is membership in the scanned collection.** A gate, a checker, a verifier — every mechanical reader has a defined read set. `issues/2738/comments` is a read set; the board's comment thread is a different read set; nothing moves between them by magic. Human intuition treats "posted publicly" as "visible to all," but machines don't have peripheral vision — they have query scopes. So the discipline is: when a brief exists to satisfy a gate, the brief names the gate's read set explicitly (the exact endpoint, the exact surface), and the verdict is posted inside that set. **Post the verdict where the gate can see it.** Anything else is journaling. The t0801 lesson generalizes: for every evidence-consumer (gate, auditor, dispatcher), state its scan surface in the brief; never assume a shared public space is a shared read set.

## MACHINE NOTE

~~~json
{
  "canonical_object": "INTELLIGENT_BLOCK",
  "sn": "SN-01629",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-18",
  "applies_when": [
    ["merge", "consensus-gate"],
    ["review", "pr-verdict"],
    ["surface", "evidence-visibility"],
    ["evidence", "consumer-scan-scope"]
  ],
  "enforcement": "Every PR-review brief carries a GATE-SURFACE field: the exact comments URL (or API endpoint) the consuming gate scans (e.g. issues/<pr>/comments for the merge-consensus gate). The dispatch claim-check refuses a review brief whose verdict-posting surface does not equal the gate's scanned surface — a brief that names only 'the board' for a gate that scans PR comments is refused at claim time. The reviewer's verdict is posted on the named surface; the receipt cites the posted comment ID. If the gate's scan surface changes, the brief template's surface field is updated first — the template is the registry, not the memory of the last run. Reference failure: t0801-lane11 (review posted to board #2721, invisible to the gate; re-filed 2026-10-18).",
  "decision_change": "Future PR-review briefs change from 'review filed on the board' to 'GATE-SURFACE field names the gate's scanned comments endpoint, and the verdict goes there.' The dispatcher's claim-check enforces it mechanically: no named gate-visible surface, no claim. Reviews stop being invisible to their gates.",
  "falsifiability": "Falsified if the merge-consensus gate's check code is found to read a surface other than the PR's own comments endpoint (inspect the gate's issue-comments call scope), or if a board-posted verdict is observed flipping a gate check. The claim is a live property of the gate code, not a historical anecdote — check the code, not the calendar.",
  "mechanism": "The gate calls the issue-comments API scoped to the PR's own issue number; the board is a separate issue with a disjoint comment collection. Visibility to a mechanical reader is set membership in its read set. Two public surfaces are two disjoint sets; posting to the wrong one is writing to a collection the query never scans."
}
~~~

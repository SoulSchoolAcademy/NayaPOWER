# IB-SMART-NOTE-20261014-sn1305

**Intelligent Block:** SN-1305
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured date:** 2026-10-14
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL

Transmissibility is the docs' proof: if a second seat cannot rebuild your instrument from prose, the docs are not done. The t0760-lane7 Arm H design review (ADOPT-CONDITIONAL) is the working example — the reviewer rebuilt the frozen verdict to 6 decimal places (MRR 0.527778 exact) from the two design docs' text alone, crawling all 1016 edges on a scratch copy. The docs were executable: a second mind walked them as a build script and arrived at the same number to 6dp. That is the only honest "docs are complete" test. Prose that cannot be re-executed is a story about an instrument, not a specification of one. The rule: design reviews include a transmissibility rebuild — an independent seat re-derives the instrument's key numbers from the prose alone, and any place the rebuild halts is a gap located exactly where it stopped. The rebuild walking the docs IS the review; the verdict on the instrument cannot outrun the verdict on the docs.

## HUMAN NOTE

Imagine a recipe book. How do you know a recipe is complete? Someone else follows it — only the recipe, no help from the chef — and the dish comes out exactly right. That's what happened this morning: a reviewer took two design documents, never talked to the original designer, rebuilt the entire measurement instrument from the text alone — crawling through all 1,016 data connections — and got the same result to six decimal places: 0.527778. That proved the docs were a real specification, not just a story. The lesson the team wrote down: don't ask "are the docs good?" Ask "can someone else rebuild it from the docs?" If they can't, the docs are not done — and wherever their rebuild gets stuck is exactly where the missing piece lives.

## CHILD NOTE

Imagine your friend writes instructions for building a LEGO car. How do you know the instructions are good? You build the car using ONLY the instructions — no peeking at your friend's finished car, no asking questions. If your car comes out exactly the same, the instructions are perfect. If you get stuck on step 5, then step 5 is broken. That's the new rule: every set of instructions has to pass the "build it from the words alone" test. The instructions are done when a stranger can build the thing perfectly from them.

## GRANDMA NOTE

Dear, it's the recipe test. Anyone can say "my recipe is complete." The proof is when your neighbor bakes the cake using only what's written — and it comes out exactly like yours. This morning a young one did this with a technical design: she took two documents, spoke to nobody, followed the words step by step through more than a thousand little connections, and landed on the exact same number down to the sixth decimal. That's a real recipe. The team's rule is now the recipe test for every design: if a second person can't rebuild it from the words alone, the words aren't finished. And wherever they get stuck, that's the missing paragraph.

## NAYA NOTE

For every seat writing or reviewing design docs: the docs' completion test is transmissibility, not approval. t0760-lane7's Arm H review (ADOPT-CONDITIONAL) proved the mechanism — the reviewer rebuilt the frozen verdict to 6dp (MRR 0.527778 exact) from the two design docs' text alone, crawling all 1016 edges on a /tmp copy, with no contact with the designer. The rebuild walking the prose as an executable spec IS the docs review: every load-bearing parameter must be named in prose, because the rebuild halts wherever one is missing — and the halt locates the gap exactly. Review verdicts on the instrument cannot outrun the verdict on the docs: certify the design only after an independent seat has re-derived its key numbers from prose alone. Note the honesty boundary built into the lesson (its own falsifier): if the rebuild fails but re-docs add no missing information, the failure was the reviewer's, not the docs' — the test measures the reviewer too, and a failed rebuild is evidence, not a verdict, until the gap is located in the prose. Evidence: hidden_files/lesson-broadcast.md [t0769] Dispatcher mirror (t0760-lane7 Arm H: "the reviewer rebuilt the frozen verdict to 6dp (MRR 0.527778 exact) from the two design docs' text alone, crawling all 1016 edges on a /tmp copy — transmissibility is the docs' proof: if a second seat cannot rebuild your instrument from prose, the docs are not done"); hidden_files/twelve-lane-receipts/t0760-lane7.md. Cousins: SN-103/verbatim-norm family (prose must carry the load-bearing content — transmissibility is the test that the prose actually does).

## MACHINE NOTE

```json
{
  "lesson_id": "SN-1305",
  "title": "Transmissibility is the docs' proof — if a second seat cannot rebuild your instrument from prose, the docs are not done",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-14",
  "category": "SYSTEM-INTELLIGENCE/GOVERNANCE/DOCUMENT-AUTHORITY",
  "evidence": [
    "hidden_files/lesson-broadcast.md [t0769] Dispatcher mirror (t0760-lane7 Arm H design review, ADOPT-CONDITIONAL): rebuilt the frozen verdict to 6dp (MRR 0.527778 exact) from the two design docs' text alone, crawling all 1016 edges on a /tmp copy",
    "hidden_files/twelve-lane-receipts/t0760-lane7.md"
  ],
  "rule": "design reviews include a transmissibility rebuild: an independent seat re-derives the instrument's key numbers from the prose alone; any halt locates a docs gap exactly; the docs are done when the rebuild completes to matching precision — the instrument's verdict cannot outrun the docs' verdict",
  "anti_pattern": "approving docs that were never executed as spec; treating a reviewer's agreement as proof of completeness; blaming the docs for a rebuild failure without locating the gap in the prose (the test measures the reviewer too)",
  "related": ["verbatim-norm family", "SN-1301 (quote the source)"],
  "falsifier": "a rebuild that failed where re-docs added no missing information — the failure was the reviewer's, not the docs' — which would show the rebuild test measures reviewer skill as well as doc completeness, and bound the lesson's claim accordingly",
  "decision_changed": "how design reviews certify documentation: transmissibility-rebuild becomes the done-test for design prose; reviews that skip it cannot certify docs",
  "mechanism": "prose-as-executable-spec: the rebuild walks the docs as a build script; every load-bearing parameter must be named for the walk to complete; a halt is a gap with an exact location; completion to matching precision (6dp) proves no parameter was underspecified"
}
```

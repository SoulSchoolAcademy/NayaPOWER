# 7 - Evidence (AI)
area_number: 7
area_name: Evidence
owner_team: Naya Clarity
agent_seat: Builder

## DEFINITIONS
- what_it_is: The evidence discipline: attach handles that resolve — comment IDs as working links, SHAs of real commits, file:line pairs that exist at the cited ref. Resolve every handle against the live tree at the cited ref before you count it. Lead with the label — what the thing IS, what it DOES, why it MATTERS — and put the identifier last, as the quiet proof of the sentence above it.
- what_it_does: Makes every claim checkable by a stranger in one command, with no questions. A dead handle is a defect in the verdict, not a formatting nit — it means the claim underneath it was never verified.
- why_it_matters: The authoring repair: check_pr_receipt.py went from 2 dead handles to 11 live / 0 dead at the pushed head — the branch name de-backticked and given a live tree URL, full repo paths used, the PR body's ## Evidence re-pinned to the new head. The receipt gate went PASS on the repaired handles, not on promises. The lesson in the machinery: the fix belonged to the body's handles, never to the gate. The opposite: Judge's scorecard on #2566 — NEEDS_WORK at 8.5/10 — named 4 dead handles: two hidden_files/ paths absent from the repo at tip (byte-verified zero entries), one branch name used as a file path, one machine-local path (receipt: comment 6161777038). And #2592's receipt-gate FAILURE on path:operations-manual-2026-10-14-v2.md — goal-workspace filenames are not repo-resolvable paths (comment 6172427473). In both cases the handles were the work: fix the body, never weaken the gate.

## PROTOCOLS
1. Every claim carries evidence a stranger can re-derive in one command. Every handle resolves at the cited ref, or it is not evidence.
2. Lead with the label — what the thing IS, what it DOES, why it MATTERS — and put the identifier last, as the quiet proof of the sentence above it.
3. Resolve every handle against the live tree at the cited ref BEFORE you count it.
4. A dead handle is a defect in the verdict, not a formatting nit — it means the claim underneath was never verified.
5. If the gate fired, re-run its matcher against the live bytes before judging it. The fix belongs to the body's handles, never to the gate.
6. Memory is rumor. If you can't open the handle, mark the claim UNVERIFIED — not 'probably fine.'
7. No bare backticked identifiers. Every identifier rides a plain-words sentence.

## CONSTRAINTS
- Test yourself against THE TEST before acting: Does every handle resolve at the cited ref? / Could a stranger re-derive my claim from my links alone — one command, no questions? / Did I lead with the label (what it is) and put the number last? / Is every identifier attached to a plain-words sentence that explains it?
- Enforcement is split honestly: REAL machinery listed under WHERE IT'S ENFORCED; PROPOSED items are not claimed as built.
- Never invent examples. Every example in this manual names its evidence handle.

## SITUATIONS
- You're about to post a scorecard, receipt, or claim with handles in it. :: Before you post: open each handle. Click the link — does it land where you said? Check the path against the tree at the cited ref — does the file exist at that commit? If any handle is dead, the work isn't done — re-derive it, fix it, or strike the claim it carried.
- A gate fails on your PR. :: Don't reach for 'false negative.' Pull the live body bytes, re-run the gate's matcher yourself, and find the handle it refused. Fix your body's handles — de-backtick the branch name, use the full repo path, re-pin to the new head — then re-run the gate.
- You're reading someone else's evidence. :: Resolve it. If their handles are dead, say so plainly, in public, with the mechanism named: 'this path doesn't exist at tip' beats 'bad evidence.' Then check whether the claim underneath survives without it.
- You're tempted to cite from memory. :: Don't. Memory is rumor. If you can't open the handle, mark the claim UNVERIFIED. The stranger test is the whole discipline: if a stranger can't re-derive it in one command, it isn't evidence yet.

# IB-SMART-NOTE-20261009-sn0787-proven-only-library.md

Intelligent Block: SN-0787
Truth state: CANDIDATE (Shawn's explicit correction 2026-10-09 — standing policy, not yet ratified as law)
Scope: SYSTEM
Captured: 2026-10-09
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE
Source: Shawn Vibert's design correction, 2026-10-09. After reviewing the Smart Blocks gallery, Shawn rejected new-construction components: "I'm just asking you to organize the ones that are already proved... half this page is totally recreated it's all new stuff." PR #1984 (12 new-construction navpage blocks) closed same day per this directive. PR #1968's 8 invented form blocks (merged earlier) flagged as inconsistent with the policy.

## IN A NUTSHELL

**The Smart Blocks library holds Shawn's proven design extractions only. Never inventions.** When the team extracted 91 blocks verbatim from Shawn's 7 approved HTML designs, that was correct. When the team then *invented* 20 new components to fill perceived gaps (8 form controls merged in #1968, 12 navpage blocks in #1984), that was scope drift — building new designs and calling them "Smart Blocks." Shawn's correction was unambiguous: organize what I've proved, don't create new pieces. "This is for you, not for me" — the library is an instrument for Nayas to retrieve his proven work, not a showcase of what the team can invent. PR #1984 was closed; its blocks remain on the branch as unproven drafts, quarantined from the official set.

## HUMAN NOTE

Think of it like a museum curator vs. an artist. Shawn hired the team as *curators*: take his proven designs, catalog them, make them retrievable, teach Nayas when to use each piece. Instead, the team started acting as *artists*: creating new pieces and hanging them alongside the originals. The problem isn't that the new pieces are bad — it's that nobody approved them, and mixing them with proven work contaminates the trust in the whole collection. A Naya reaching for a "Smart Block" needs to know: this is Shawn-approved, not team-invented. The curator's job is organization and retrieval, not creation.

## CHILD NOTE

Imagine your mom has a box of her favorite recipes — the ones everyone loves. She asks you to organize them so the family can find them easily. But instead, you also add some recipes you made up yourself and mix them in. Now nobody knows which ones are mom's proven favorites and which ones are your experiments! The right job was: organize mom's recipes beautifully. Not: invent new ones. If you invent a good one, keep it separate until mom tastes it and approves.

## GRANDMA NOTE

It's the difference between preserving and producing. When someone trusts you with their life's work — their designs, their recipes, their standards — your first duty is faithful stewardship. Organize it, protect it, make it accessible. Don't improve it, don't extend it, don't "fill the gaps" with your own work. If you see a genuine gap, you *propose* a new piece through the proper channel and wait for approval. You don't unilaterally add to the canon. Trust is built by restraint, not by productivity.

## NAYA NOTE

This is a governance policy for the design system with three operational consequences:

1. **Extraction only**: new blocks enter the library exclusively by verbatim extraction from Shawn-approved source designs. The extraction must be byte-faithful (selectors, values, structure) — "no more recreate."
2. **Quarantine for inventions**: any team-built component (however good) lives outside the official index/catalog until Shawn explicitly approves it. The 8 form blocks from #1968 are currently in the inconsistent state — merged to the filesystem but not in the v1.4 index. They need either retroactive approval or quarantine.
3. **Gap proposals, not gap fills**: when a Naya identifies a missing component, the correct action is a *proposal* (what's missing, why it matters, a draft) — not a merge. The approval authority is Shawn's eye, not the team's judgment.

The deeper principle: **the user's visual verdict outranks the team's code claims.** Shawn rejected the gallery not because the code was wrong but because the *rendered result* wasn't his standard. A "Smart Block" is proven when Shawn says it's proven — not when the extraction is byte-faithful, not when the tests pass. Byte-faithfulness is necessary; his approval is sufficient.

## MACHINE NOTE

{"sn": "SN-0787", "title": "Proven-Only Library — No Inventions in the Official Smart Blocks", "truth_state": "CANDIDATE", "scope": "SYSTEM", "captured": "2026-10-09", "source": "Shawn Vibert design correction 2026-10-09; PR #1984 closed same day; PR #1968 flagged", "policy": "library holds Shawn's proven design extractions only; team inventions quarantined until explicit approval", "incidents": {"1968": "8 invented form blocks merged to filesystem, not in v1.4 index — inconsistent state", "1984": "12 new-construction navpage blocks — closed per directive, quarantined on branch"}, "rules": ["extraction only from Shawn-approved sources", "byte-faithful, no recreation", "gaps become proposals, not merges", "Shawn's visual verdict is the approval authority"], "triage": "GATE (extraction-vs-invention check on library PRs) + BEHAVIOR (curator mindset)"}

## LEARNING LESSON

The team confused *completeness* with *fidelity*. Seeing gaps in the 91-block library, the instinct was to fill them — a builder's instinct, and wrong for this task. Shawn didn't ask for a complete component library; he asked for *his* library, organized. The 20 invented blocks weren't bad engineering — they were a category error: the team was doing the wrong job well. The lesson generalizes: when the task is stewardship (organize, preserve, retrieve), the highest-value action is restraint, not productivity. "All you have to do is take the pieces and put them together beautifully."

## HOW IT CONNECTS

- This is the design-system instance of "preserve what works; smallest effective change" (engineering principle).
- Pairs with the byte-for-byte restoration boundary (Shawn, 2026-10-03) — same stewardship ethic.
- The #1968 inconsistency (merged but unindexed) is still open — this note records the policy; the repair is a separate action.
- Supports the cold-Naya goal: a Naya retrieving from a proven-only library can trust every block.

## EPISTEMIC STATE

CANDIDATE. Shawn's correction is verbatim and unambiguous. The "curator vs artist" framing is Naya 2's interpretation. The #1968 quarantine status is an open repair item, not yet resolved.

Falsifier: if Shawn explicitly approves a team-invented block for the official library, the policy gains an approval path (which it currently lacks in mechanical form).

## UNCERTAINTY

- The exact approval process for a proposed new block — currently "Shawn's eye," no formal submission format.
- Whether the 8 #1968 blocks will be retroactively approved or quarantined — pending Shawn's review.

## APPLICABILITY

Every PR touching the Smart Blocks library (BRAIN/10-INTERFACES/DESIGN-BLOCKS/). Every Naya working in the design lane. The extraction-vs-invention distinction should be a checklist item on library PRs.

## SUCCESSOR EFFECT

A cold Naya asked to "add a missing component" to the library knows: don't build it and merge it. Extract from Shawn's approved designs, or write a proposal and wait. The library's trust comes from its provenance — every block traceable to his hand, not ours.

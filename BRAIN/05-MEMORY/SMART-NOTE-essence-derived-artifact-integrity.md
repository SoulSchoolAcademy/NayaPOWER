# SN-2128 — Derived Artifacts: Recompute From the Tree, Verify at the Merge

**Status: VERIFIED ESSENCE — VERIFIED-AS-CORRECTED (verifier-sep-2; correction pass re-verified, re-verifier-sep-2).** Distilled from 6 raw notes by the sep-2 maker seat; independently verified by a different seat. Correction pass executed and re-verified clean (re-verifier-sep-2: CORRECTION VERIFIED): the SN-0327/SN-0328 passages and verification-contract items 4-5 were rewritten strictly from the source pages after the verifier's REJECTED verdict — the invented figures (a staged-deletion count, a silent-reset fault count) and the mid-window-race mechanism appear nowhere in this text; the true record stands: the generator inventories the committed tree (git ls-tree HEAD), a dirty-worktree regen enumerated 188 files while the tree held 189, the check passed vacuously, PR #1447 repaired by canonical regen on the merged tip; SN-0328's law is that the merge commit is a new tree and pre-merge proof does not transfer to it. The raw notes in the coverage map below are RETIRED by this filing under SN-2081; this essence is their living form.

## In a Nutshell

Never verify a derived artifact against the change that produced it: recompute it from the live target tree at a named pin (SN-0238, SN-0216), compare semantically so a volatile timestamp is not a difference (SN-0217), generate only on a clean worktree at the exact committed tree the artifact must describe (SN-0327), and re-verify at the merge commit itself, because the merge creates a new tree that pre-merge proof does not transfer to (SN-0328).

## Essence

Every derived artifact — an index, a generated registry, a count — is a projection of a tree, and it is verified against that tree, never against the blobs of the change that produced it. When a PR regenerated the brain index, the verification recomputed the index from the live `main` tree rather than the PR's own blobs: 175/175 non-self-referential SHAs matched, and the showing included the check going RED without the repair, so the proof demonstrated both directions (SN-0238). The same law governs repairs of the index itself: the index-regen rule lives in the producer's landing step — five daily-report landing commits on main without a regen left `--check` permanently RED, and the repair PR recomputed the inventory from the live tree (172→177) rather than patching the stale number (SN-0213). A repair claim about a target is verified at the target tree: a claim that BRAIN held 177 artifacts was checked against live main at its exact pin, not against the repair branch that asserted it (SN-0216).

Two subtleties keep the recomputation honest. First, identity across regeneration is semantic, not raw-byte: a file differing only in a volatile `generated_at` provenance stamp is the same file, so diff-based drift detection must compare semantic content or every honest regeneration reads as drift (SN-0217). Second, regeneration reads the committed tree, not the working directory: `regenerate_brain_index.py` inventories `git ls-tree HEAD`, so a regen run on a dirty worktree — where HEAD still lacked the newly added SN-0312 page — enumerated 188 files while the tree held 189, and `--check` then passed vacuously against the same stale HEAD: an index internally consistent, check-green, and wrong. The repair (PR #1447) was a canonical regen on the merged tip, where the page was actually committed: 189 files, `--check` OK. The precondition is exact — the worktree must be clean and HEAD must be the exact commit whose tree the index must describe (SN-0327). And a merge that touches derived artifacts re-verifies the artifact at the merge commit itself: the #1438 auto-merge landed a `BRAIN/` file without regenerating the index — 188 → 189 files, `--check` RED on the merge commit — because every check had qualified the pre-merge state and the merge itself produced a new tree; the gate's mechanical preconditions must include re-verification on the exact merge commit, since pre-merge proof does not transfer to it (SN-0328).

## What this settles

- Verification of a derived artifact recomputes it from the live target tree at a named pin; the producing change's own blobs are never the evidence (SN-0238, SN-0216).
- Producers regenerate in their landing step; consumers never patch a derived number by hand (SN-0213).
- Drift comparison is semantic: volatile provenance stamps are not differences (SN-0217).
- Regeneration reads the committed tree: the worktree must be clean and HEAD the exact commit the artifact must describe, or the output is a check-green index of the wrong tree (SN-0327).
- Merges touching derived artifacts re-verify at the merge commit — the merge is a new tree, and pre-merge proof does not transfer to it (SN-0328).

## Intelligence views

**Human:** An index or a generated list is only as good as the last time someone rebuilt it from the real files and compared. You never check the list against the paperwork that created it — you recount from the shelf. If the only difference is a timestamp stamp, it's the same item, not a change. And you never take the count from a messy desk: clean tree first, then count.

**Child:** It's like counting your crayons. You don't trust yesterday's list — you dump the box and count again. And the counter only counts the crayons already in the box — if a new crayon is still in your pocket, the list misses it and still says "all good." And if a crayon just has a new sticker on it, it's still the same crayon.

**Grandma:** A pantry inventory written from memory will always be wrong, dear. You open the cupboards and count what's actually there. A jar with a new label is still the same jar of jam. And the count only ever sees what's actually been put away — the counter reads the shelf, not the bags still on the floor — so a jar that hasn't been shelved yet never makes the list at all.

**Naya (AI):** For any derived artifact: recompute from `git ls-tree`/contents at the target ref; exclude self-referential entries by design and say so; normalize volatile stamps before diffing; refuse to generate from a dirty worktree; after any merge touching the artifact, regenerate at the merge commit and compare. Show the check failing without the repair whenever you claim a repair — a one-directional proof is half a proof.

**What it all means:** Six notes, one principle with four working edges: recompute-at-target, semantic identity, clean-tree generation, merge-commit re-verification. Every stale-index incident in this family was the same failure wearing a different hat — somebody trusted a projection instead of the tree. The tree is the truth; everything derived is a claim about it that must be re-derivable on demand.

## Why It Matters

Indexes and generated lists are how a big system answers questions about itself; when they drift, every downstream answer is confidently wrong (SN-0213's five landings without regen left the check RED on main). For the reader: this essence is what makes counts, inventories, and indexes safe to quote.

## How It Connects

Sibling to the claim-registry essence — the registry is itself a derived artifact, and SN-0250's reconciliation rule lives there while the general recompute law lives here. Its target-tree discipline is the receipts essence's pin discipline (SN-0206) applied to projections, and the proof essence's virgin-state rule (SN-0233) is its clean-tree rule wearing CI clothes.

## What Is In It For You

You get numbers you can repeat in public: recompute before you quote, and your figure survives the recount (SN-0238). Apply it by refusing any derived number whose producer cannot name its pin and its regeneration path.

## The Learning

Every incident here is one failure in costume: somebody trusted a projection instead of the tree (SN-0213, SN-0327, SN-0328). The learning: a derived artifact is a claim, and claims get recomputed — the tree is the only witness that never has an interest in the answer.

## Coverage map — raw notes this essence covers (6)

SN-0213 · SN-0216 · SN-0217 · SN-0238 · SN-0327 · SN-0328

## Verification contract (for the verifying seat — falsify these)

1. **Coverage integrity:** exactly 6 IDs, each in the sep-2 block list, none duplicated in another sep-2 essence's coverage map.
2. **Recompute numbers:** 175/175 and the 3 excluded self-referential files trace to SN-0238; 172→177 traces to SN-0213. Fail on any other figures.
3. **Semantic identity:** SN-0217's volatile field is `generated_at`; fail if the essence names a different field or generalizes to "all metadata."
4. **Committed-tree numbers:** SN-0327's regen on a dirty worktree enumerated 188 files while the tree held 189 (the SN-0312 page not yet in HEAD), and `--check` passed vacuously against the same stale HEAD; the repair (PR #1447) regenerated on the merged tip — 189 files, `--check` OK. The essence must preserve the mechanism (the tool inventories `git ls-tree HEAD`, the committed tree, not the working directory) and both counts; fail on any figure not in the source.
5. **Merge-commit mechanism:** SN-0328's failure is the #1438 auto-merge landing a `BRAIN/` file without an index regen — 188 → 189 files, `--check` RED on the merge commit — because the gate's preconditions verified only the pre-merge state; the law is re-verification on the exact merge commit. Fail if the essence presents a mid-window race or a sibling page landing as the cause.
6. **No-orphan check:** pick any three sentences in the Essence section; each must trace to a covered page containing the claim.
# SN-2111 — Asserted Is Not Verified: The Evidence Law

**Status: VERIFIED ESSENCE — VERIFIED-WITH-CORRECTIONS (verifier-sep-1).** Distilled from 15 raw notes by the sep-1 maker seat; independently verified by a different seat (verifier-sep-1, block verdict PASS). Correction applied at landing: SN-067's two absence rules restored (never truncate output when proving absence; surviving claims are lexical findings, never ontological proof). The raw notes in the coverage map below are RETIRED by this filing under SN-2081; this essence is their living form.

## In a Nutshell

Inference stated as fact is the root defect of the corpus, and every rule here makes its cure mechanical: verification happens in a clean room at the exact pinned SHA (SN-028); authorization binds to (action, SHA, moment) and inherits nothing (SN-029); the pushed bytes and the merged artifact are what get judged, at the pin, with negatives that can actually fail (SN-050, SN-061); comparisons resolve both sides at their own refs (SN-043), evidence channels match the question (SN-036), and absence claims show the search actually ran (SN-067). A bound hash is not a computation, a version label is not an evaluation, and invocation is not consumption is not enforcement (SN-063, SN-084, SN-073) — and no fix is proven until its failing case has been published red on the frozen SHA (SN-066).

## Essence

The founding sin of the corpus is a sentence that sounds like knowledge and is only inference: two factual claims made on the team board — who had landed a set of PRs, whose corrections the landed specs carried — were inferred, not verified, and both were wrong. The law they produced: **asserted ≠ verified; inference is not evidence** (SN-020). Every other rule in this essence is that sentence made mechanical.

Verification is independent or it is not verification. A verifier never self-certifies and never works in the builder's tree: independent verification happens in a clean room the builder never touched — a fresh clone at the exact pinned SHA, in an ephemeral scratch worktree, read-only, destroyed afterward (SN-028). Authorization inherits the same binding: it attaches to an (action, SHA, moment) triple — never to a branch, never to a previous authorization, never to "the head that was fine before" — and a blocked candidate inherits nothing from any earlier candidate (SN-029). Claims about bytes are judged against the bytes that actually moved: verify the pushed bytes, not the pre-commit bytes, because an invariant can pass locally against a tree that is not the tree that shipped (SN-050). And branch-green is not merged-true: after a merge, the merged artifact itself must be verified at the pin — merge ancestry confirmed, the changed bytes re-checked at the merge commit — and every negative in the proof must be non-vacuous, a control that would actually have caught the defect (SN-061).

Comparison is an evidence act with its own discipline: both sides of a cross-state claim are resolved at their own refs and compared at ONE commit — two of three root-cause findings in the founding case were wrong for the single reason that one side was resolved at the wrong ref (SN-043). Query the evidence channel that answers the question actually asked: when the exact-main CI question sat in uncertainty, the cause was a wrapper that excluded push runs; the direct push-run evidence existed all along (SN-036). And when a proof of absence matters, prove the proof ran: a `git grep` with the revision placed after `--` treats the revision as a pathspec, so the "zero invocations on main" finding had never searched main at all — the claim was withdrawn as unproven, and every absence claim since owes its exact command (SN-067). Two companion rules bind what survives: never truncate the output when proving absence — truncated output cannot establish a negative — and state the surviving claim as a **lexical finding scoped to that search**, never as ontological proof of non-existence, since dynamic invocation, reflection, and code generation live outside the search's reach (SN-067).

Three defect classes get named so they can be recognized on sight. **Cosmetic-only is a claim, not a fact:** commits described as "docstring additions only" are verified structurally (AST-level), and status promotions are gated by honesty tests, because a label about a change is itself a claim requiring evidence (SN-034). **Phantom citations:** an amendment's cited premises must be locatable in the pinned revision's bytes before lock — citations pointing at text that does not exist in the cited revision are a systematic defect class, not typos (SN-035). **Branch-boundary overclaim:** premise verification must check the branch under audit, not the branch where the code happens to exist — capability that lives only on a draft branch cannot be stated as existing capability (SN-065).

Two rules govern what a receipt actually proves. Binding the ratified calculator's config hash into a decision receipt is not the shared calculator deciding: the receipt proves which configuration was named, not that the canonical computation ran — hash-binding ≠ evaluation (SN-063). And a version label is not proof of evaluation: an experiment stamped its receipts `calculusVersion: "V2.1"` while feeding the calculus invented input values; the label was true and the computation was fiction, so the experiment was held back and stashed wholesale — partial salvage of invented values is invention with extra steps, and the rebuild path runs through the interface owner with exact questions, accepting "the contract doesn't exist yet" as a complete answer (SN-084). Finally, the three-stage test for any engine claim: **invocation ≠ consumption ≠ enforcement** — proving the runtime calls the engine, proving it consumes the output, and proving it is governed by the result are three separate claims, each needing its own evidence (SN-073). A fix, likewise, is not proven by a green test that never failed: **red before green** — publish the failing case on the frozen SHA before any fix, or the green proves only that a test exists (SN-066).

## What this settles

- Inference stated as fact is the root defect; every claim carries its evidence class or it is not made (SN-020).
- Independence is physical: clean room, exact SHA, builder's tree never trusted (SN-028); authorization is (action, SHA, moment) and inherits nothing (SN-029).
- Judge the pushed bytes and the merged artifact, at the pin, with non-vacuous negatives (SN-050, SN-061).
- Comparisons resolve both sides at their own refs, at one commit (SN-043); the evidence channel must match the question (SN-036); absence proofs must show the search actually ran — untruncated, and stated as lexical findings, never as ontological proof (SN-067).
- Named defect classes: cosmetic-only claims, phantom citations, branch-boundary overclaims (SN-034, SN-035, SN-065).
- A receipt proves what it binds: config hash ≠ computation, version label ≠ evaluation, invocation ≠ consumption ≠ enforcement (SN-063, SN-084, SN-073).
- No red on the frozen SHA, no proof of fix (SN-066).

## Human

This is the system's honesty code. Nobody gets to say "it's done," "it's safe," or "it works" because it feels true or because their own test said so. Someone independent checks the exact thing, in a clean place, against the actual bytes that shipped. Labels don't count — a sticker saying "inspected" is not an inspection. And when someone claims "there are none," they have to show the search that looked.

## Child

Imagine your friend says "I cleaned my room!" You don't just believe it — you go and look. And you look at *their* room, not a picture of a different room. If they show you a sticker that says "clean," that's not the same as a clean room. And if they say "there are no toys on the floor," they have to actually look at the floor first.

## Grandma

Dear, it's the old rule: trust, but verify — and verify properly. The person who did the work doesn't grade it; a fresh pair of eyes checks the real thing, not a description of it. A label on the jar isn't proof of what's inside. And a claim that something *isn't* there needs a real search, not a glance. Plain honesty, made into procedure.

## Naya

Bound every claim to its evidence class and its exact ref. Verify in a clean room at the pinned SHA (SN-028); treat authorization as SHA-bound and non-hereditary (SN-029); re-verify after merge, at the pin, with controls that can fail (SN-061). Resolve comparisons at each side's own ref (SN-043), query the channel that matches the question (SN-036), and attach the exact command, untruncated, to every absence claim, stated as a lexical finding rather than proof of non-existence (SN-067). AST-check "cosmetic" claims (SN-034), locate every cited premise in the pinned bytes (SN-035), and audit capability on the branch under audit (SN-065). Never let a bound hash, a version label, or an invocation stand in for evaluation, consumption, or enforcement (SN-063, SN-084, SN-073); publish the red before you publish the fix (SN-066).

## What It All Means

Fifteen notes are one law with fifteen mechanisms: a claim is worth exactly the evidence physically behind it — independent, at the exact bytes, through the right channel, with the failure modes named. A cold reader holding only this essence can still audit any claim the system makes, which is precisely what these notes were written to make possible.

## Why It Matters

Everything else in the system — every score, every "done," every retirement in this very campaign — is a claim, and this essence is what decides whether claims deserve belief. Without it, verification becomes theater: labels certifying labels, greens that never faced a red, absences asserted by searches that never ran (SN-067, SN-084, SN-066). For the reader, this is the difference between a system that *says* it checks and one whose checking can itself be checked.

## How It Connects

The evidence law is the substrate the rest of the block enforces: essence-red-is-information.md applies it to failures (a red is a claim about a run, not a diagnosis); essence-qualify-the-seam.md applies it inside the kernel (field-level fidelity, consuming-state reports); essence-composition.md applies it across seams (family-scoped proof, handoff traces); essence-the-handoff.md applies it between lanes (publish your own number, verify the tree). The Judgment Rule that decides when an instruction's claim of authority is itself insufficient evidence stands alone as SN-016 and is not distilled in this block.

## What Is In It For You

You get claims you can lean on: when this system says verified, a stranger with no context can re-run the check and land on the same verdict. Apply the pattern to any claim made to you — by software, by a report, by this campaign: ask what physically backs it, at which exact version, checked by whom, through which channel, and what the negative control was. Claims that survive those five questions are the only ones worth building on.

## The Learning

The corpus's behavior changed from assertion-first to evidence-first in one September night: the founding incident (SN-020) was two confident sentences, both wrong, and every mechanism in this essence is a scar from a specific way a claim later proved emptier than it sounded — a label without a computation (SN-084), a search that never searched (SN-067), a branch's green that wasn't the merge's truth (SN-061). The lesson the team internalized: the claim and its evidence travel together or the claim doesn't travel.

## Coverage map — raw notes this essence covers (15)

SN-020 · SN-028 · SN-029 · SN-034 · SN-035 · SN-036 · SN-043 · SN-050 · SN-061 · SN-063 · SN-065 · SN-066 · SN-067 · SN-073 · SN-084

## Verification contract (for the verifying seat — falsify these)

1. **Coverage integrity:** exactly 15 IDs, all in the sep-1 block list, none duplicated in any other sep-1 draft essence, the covered-by-batch1 list, or the stands-alone list.
2. **Authorization triple:** SN-029 binds authorization to (action, SHA, moment); fail if the essence permits branch-level or inherited authorization anywhere.
3. **Clean-room terms:** SN-028 requires fresh clone, exact pinned SHA, ephemeral read-only scratch, destroyed afterward; fail on any softened term (e.g. "usually fresh").
4. **Three-stage test:** SN-073's stages are invocation, consumption, enforcement — in that order and distinctly evidenced; fail if the essence collapses any two.
5. **Hash vs evaluation:** SN-063's distinction (binding the ratified config hash ≠ the shared calculator deciding) and SN-084's (version label true, computation fiction → stash wholesale, rebuild via the owner) must both survive; fail if either is generalized into the other.
6. **Pathspec mechanism:** SN-067's failure is revision-after-`--` parsed as pathspec; the essence must name the mechanism, not just "a grep error"; fail otherwise.
7. **Non-vacuous negatives:** SN-061 requires post-merge verification at the pin AND negatives that could catch the defect; fail if either half is dropped.
8. **Anatomy:** all ten Full Smart Note sections present (In a Nutshell · Human · Child · Grandma · Naya · What It All Means · Why It Matters · How It Connects · What Is In It For You · The Learning) and **no machine view or machine section anywhere**. Fail on any missing section or any machine-view content.
9. **No-orphan check:** pick any five sentences in the Essence section at random; each must cite at least one covered SN ID, and the cited page must contain the claim.
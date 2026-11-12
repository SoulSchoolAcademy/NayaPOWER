# SN-2178 — Merge Discipline: Holds, Twins, and the Exact Head

**Status: VERIFIED ESSENCE — VERIFIED (verifier-oct-4, block PASS WITH CORRECTIONS; correction pass executed, re-verified, and closed by a different seat's second-pass confirmation — all retirement holds lifted).** Distilled from 11 raw notes by the oct-4 maker seat; independently verified by a different seat (12 essences VERIFIED, 2 VERIFIED-WITH-CORRECTIONS, both corrections executed and confirmed). Verifier verdict: VERIFIED (verifier-oct-4, against repo bytes). The raw notes in the coverage map below are RETIRED by this filing under SN-2081; this essence is their living form.

## In a Nutshell

A merge is an act with preconditions, and this block records what happens when each precondition is treated as optional. A merge raced its own checks and landed three seconds before they failed (SN-868). A requested review was outrun by the merge it was meant to gate (SN-899, SN-911). Twin repairs raced each other across two rounds until freshness — not canonicity — decided (SN-841, SN-849). A blocked draft-flip was treated once as a boundary to respect (SN-867) and once, under *identical* authority through a different surface, as a route to take (SN-866). And landings themselves split into classes — bytes landed without a receipt are a different defect from bytes that never landed (SN-874). The discipline: hold what is held, wait for what was requested, re-verify on the head that will actually merge, and let the record show which class every landing was.

## Essence

**A requested review is a hold, not a race.** A review of the score-repair-verify protocol was requested pre-merge and landed post-merge with verdict CONCERNS — a narrow contract gap (SCORE must return a typed decision receipt; the code returns the raw calculator result; DIAGNOSE's ranking is not explicitly bound to the calculator output). Because the verdict was CONCERNS and not BLOCK, there was no revert; the findings became follow-up work — repair debt on main that a waited-for review would have made a pre-merge hold. The rule, stated on the record: **if a review was requested and hadn't landed, that's a hold, not a race.** A verdict that could have been a BLOCK deserved its chance to be one (SN-899). The same case, told as governance, adds the merge lane's procedure: before any merge, list every requested review; if any hasn't landed, the merge is on HOLD and the hold is posted as a receipt; a post-merge CONCERNS routes as owned follow-up with the sequencing failure recorded; a would-be BLOCK makes the race a revert decision owned by the director, owned publicly in the same turn. Independent verification by a *different* seat is a standing requirement, not a garnish — a review you requested is a commitment to wait for it (SN-911). The two notes are one substance in two tellings — SN-899 the triage telling (with the correct-pattern example: reviews requested *before* merge on #2075/#2079), SN-911 the governance telling (with the director's verbatim rule and the five-step procedure) — and both are carried here, named as a pair.

**Pending checks are not green checks.** The merge gate read "not yet failed" as green: #2107 merged at 03:42:12Z while its test was still running; the test failed at 03:42:15Z — three seconds later. The drift check ran LAST in `kernel-tests.yml`, maximizing the race window. The fixes: never merge on still-running checks, and fail-fast ordering (drift check FIRST) — the patch prepared, blocked on the workflow-file credential, recorded with its routing rather than forced. The click is attributed to its actor regardless of rank (web-flow, the director's account — stated plainly) (SN-868). This is the mechanism underneath the index-miss recurrence counted elsewhere (SN-863).

**Even a hold is a decision, and it gets a receipt.** When a merge is held, the hold itself is scorecarded: merge-now 6.0 / hold-for-owner 9.0 / drop 6.5, with the hold receipt carrying the proof, the scored options, a single named lane-owner for the decision, and re-anchoring per the freshness law before the decision is revisited (SN-825). (Receipt practice from this era is recorded as-is; how scorecarding itself later changed is named as a conflict in this block's receipt, not smoothed here.)

**Twin repairs: declare the canonical, then let freshness overrule it.** Round one: #2084 was a subset of #2083, the same RED class at tip `a6daf915`. The canonical is declared by FIRST_IN_TIME + SUPERSET_OF_REPAIR + INDEPENDENTLY_VERIFIED; the recommendation is to close the subset; merging both is forbidden, and so are the two power moves — unilaterally closing a healthy PR, or merging the subset only. The superseded lane's proof is preserved, a prose fold-in is offered, and the close is the lane's own act (SN-841). Round two: the tip moved, and canonical status decayed with it — #2083 canonical-but-stale against #2084 minimal-fresh-green scored 4.0 vs 9.0, and #2084 merged. #2083 closed as superseded: its unique value was already green on main, so merging it had become regression risk. Repairs are scored on freshness × minimality × green-on-head, and a declaration of canonicity is itself a perishable claim (SN-849).

**Authority lives in the session, not the tool — and a boundary is not a puzzle.** The #2108 triptych, three panels of one incident. (1) The API merge path was structurally broken — REST refuses draft merges (405), the GraphQL draft-flip failed on the shared credential — so the merge went through the browser under *identical* authority: same shared account, same session, no new permission. The receipt was posted **before** acting, and the result was proved by ref identity (main == `fe25661c`, behind 0). The line is identical authority vs borrowed authority (SN-866). (2) The counterpart: a credential 404 on the draft flip, both seats, same signature — bounded attempts (2), the refusal recorded verbatim, the scope holder named (pulls:write / merge-queue driver), and **no** borrowed identity and no retry loop. A blocked transition is a boundary, not a puzzle; the refusal itself is evidence on the board (SN-867). (3) The draft label itself was a tooling artifact — the flip mechanism was GraphQL-only and broken on the shared credential. Badge ≠ verdict: readiness is builder sign-out + independent live corroboration; the same permission through a different surface is permitted, a different credential is not (SN-870).

**Know what actually landed.** A direct-push "merge" splits into classes with different remedies. #2080's commit `8340e9bb` is a real 2-parent merge on main — the API never fired, `merged_at` is null — class 1: landed, receipt missing → retro receipt. #1667 never landed (branch `afaa5f74` unmerged) — class 2, a different remedy entirely. The PR record is bookkeeping; commit parents + the main tree are evidence (SN-874). And in a shared clone, the branch under your commit is a precondition too: verify HEAD branch immediately BEFORE and AFTER every commit — a mid-commit switch landed a commit on a sibling's branch (`brain-build/completeness-gate-v1`); the repair ran the same tick (update-ref, sibling restored to its exact prior SHA `93030048d`, no tree interference verified, reported openly), and the standing preference is a private detached worktree (SN-855).

## What this settles

- A requested-but-unlanded review holds the merge; racing it converts verdicts into repair debt (SN-899, SN-911).
- Never merge on still-running checks; "not yet failed" is not green; order fail-fast checks first (SN-868).
- A hold is scorecarded and receipted like any decision, with one named owner (SN-825).
- Twin repairs: declare canonical by first-in-time + superset + independently verified; never merge both, never close another lane's healthy PR unilaterally (SN-841) — and re-score when the tip moves, because canonical status decays (SN-849).
- Identical authority through a different surface is legitimate with a pre-posted receipt and ref-identity proof (SN-866); a blocked transition met with a credential wall is a boundary — bounded attempts, verbatim refusal, named scope holder, no borrowed identity (SN-867); a draft badge is a tooling artifact, readiness is corroborated substance (SN-870).
- Landings are classified from commit parents + tree, not the PR record: landed-without-receipt ≠ never-landed (SN-874).
- In shared clones, verify the branch before and after every commit (SN-855).

## Human

Merging is the moment where many people's work becomes one history, and these notes are the etiquette and engineering of that moment. Wait for the review you asked for. Don't call a race a green light. When two people fix the same thing, don't merge both and don't throw either away rudely — declare which is canonical, and be ready for time to change the answer. When a door is locked, sometimes you may walk through the same door by another handle because it's *your* key; sometimes the lock is the message, and you stop, write down that it stopped you, and name who holds the key.

## Child

Merging is like everyone putting their pages into one big book. Rules: if you asked a friend to check your page, wait until they've checked it before you glue it in. If two friends wrote the same page, pick the better one together — don't glue in both. If the glue door is stuck, you can use the other door *only if you have your own key* — never borrow someone else's. And always check that your page actually went into the book, not just that someone said it did.

## Grandma

It's courtesy backed by bookkeeping, dear. You don't publish a letter before the editor you *asked* has read it. You don't slip your chapter in while the printer is still checking the ink. And when the record book and the actual shelf disagree about whether something was published, you believe the shelf — then you fix the record book, openly, with a note saying what happened.

## Naya

Before any merge: list requested reviews — unlanded means HOLD, posted as a receipt (SN-899, SN-911). Confirm every check has *finished*; pending is not green; expect fail-fast ordering or name its absence (SN-868). Receipt holds with scored options and one named owner (SN-825). For twin repairs, run ENUMERATE→SCORE→GATE→DECIDE→RECEIPT, declare canonical by the three tests, and re-score freshness before acting on an older declaration (SN-841, SN-849). Route around tooling only under identical authority — receipt first, ref-identity proof after (SN-866); treat credential walls as boundaries with bounded attempts and verbatim refusals (SN-867); judge readiness by sign-out + live corroboration, never by the draft badge (SN-870). Classify every odd landing from parents + tree before choosing a remedy (SN-874); verify HEAD branch before and after every commit in a shared clone, and prefer a detached worktree (SN-855).

## What It All Means

The merge is where this system's distributed trust becomes a single fact, so merge discipline is where its honesty is most load-bearing. The eleven notes divide into preconditions (reviews landed, checks finished, base fresh, branch correct), authority (whose key, which surface, where the boundary is), and record (what landed, in which class, receipted how). A merge that satisfies all three is the atomic unit the rest of the campaign's disciplines — classification, freshness, ratification — exist to protect.

## Why It Matters

Every failure here is quiet. A merge three seconds early, a review outrun by minutes, a twin merged twice, a landing that exists only in bookkeeping — none of them announce themselves, and each one falsifies the record that every later verification trusts. For the reader: any team that lands shared work has these same three seconds and these same locked doors; the value of this essence is the checklist that makes the quiet failures loud *before* they land.

## How It Connects

Precondition freshness (re-anchor before the PUT) is essence-evidence-expires.md (SN-883); the review-object verification that catches false approval claims is essence-breach-discipline.md (SN-937); the repair-side sequel to this essence's worst landing (revert first, own the wrong repair) is also there (SN-882). The gate that SN-868's drift check belongs to is audited in essence-gate-must-fail.md. The director's decision procedure that hold-scorecarding served stands alone as SN-902; the no-ego doctrine for duplicate work — cross-score, merge the best, preserve the rest — stands alone as SN-920 and is pointed to, not absorbed: SN-841/SN-849 are its merge-lane mechanics, not the doctrine itself.

## What Is In It For You

You get the merge checklist that prevents the four most expensive quiet errors: racing a review you requested, merging on unfinished checks, double-merging duplicate fixes, and trusting the record over the tree. You also get the authority distinction that resolves a hundred arguments — *same key, different door* is fine and receipted; *different key* is a boundary, and the refusal is the deliverable. Apply it anywhere work lands in a shared history.

## The Learning

The era's lesson is that merge failures are almost never malice or incompetence — they are *timing and tooling*: a three-second race, a GraphQL-only flip, a badge that lied. The disciplines that compounded are all timing-shaped: holds that are visible, checks that must finish, declarations that expire, receipts posted *before* the act they authorize. The team stopped asking "was the merge allowed?" and started asking "were the preconditions true at the instant it happened?"

## Coverage map — raw notes this essence covers (11)

SN-825 · SN-841 · SN-849 · SN-855 · SN-866 · SN-867 · SN-868 · SN-870 · SN-874 · SN-899 · SN-911

## Verification contract (for the verifying seat — falsify these)

1. **Coverage integrity:** exactly 11 IDs, all in the oct-4 block list, none duplicated in any other oct-4 draft essence, the covered-by-batch1 list, or the stands-alone list.
2. **Near-duplicate pair handled honestly:** SN-899 and SN-911 must both appear, be named as two tellings of one case (same comment 6100230214, same CONCERNS verdict, same SCORE typed-receipt gap), and each telling's distinct addition must survive (SN-899: the gate-function argument + correct-pattern example; SN-911: the five-step merge-lane procedure + would-be-BLOCK handling); fail if either is dropped or the pair is presented as two independent incidents.
3. **Authority line kept bright:** SN-866 (identical authority, different surface — legitimate) and SN-867 (credential wall — boundary, no borrowed identity) must not be blended into "use judgment"; fail if the identical-vs-borrowed distinction is lost.
4. **Three-second race exact:** SN-868's merge at 03:42:12Z vs failure at 03:42:15Z and the drift-check-runs-LAST mechanism must survive; fail if generalized to "merge carefully."
5. **Twin saga in order:** SN-841's declaration tests (first-in-time + superset + independently verified) must precede SN-849's freshness overrule, with the 9.0 vs 4.0 scoring; fail if the essence presents canonicity as permanent.
6. **Standing-authority guard:** SN-920 (No-Ego Merge) and SN-902 (decision procedure) may be pointed to but not absorbed; fail if their substance is restated as covered material.
7. **Anatomy:** all ten Full Smart Note sections present (In a Nutshell · Human · Child · Grandma · Naya · What It All Means · Why It Matters · How It Connects · What Is In It For You · The Learning) and **no machine view or machine section anywhere**. Fail on any missing section or any machine-view content.
8. **No-orphan check:** pick any five sentences in the Essence section at random; each must cite at least one covered SN ID, and the cited page must contain the claim.
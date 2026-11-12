# SN-2183 — Breaches Are Published, Then Dispositioned

**Status: VERIFIED ESSENCE — VERIFIED (verifier-oct-4, block PASS WITH CORRECTIONS; correction pass executed, re-verified, and closed by a different seat's second-pass confirmation — all retirement holds lifted).** Distilled from 7 raw notes by the oct-4 maker seat; independently verified by a different seat (12 essences VERIFIED, 2 VERIFIED-WITH-CORRECTIONS, both corrections executed and confirmed). Verifier verdict: VERIFIED (verifier-oct-4, against repo bytes). The raw notes in the coverage map below are RETIRED by this filing under SN-2081; this essence is their living form.

## In a Nutshell

When governance breaks in this block, the response follows a liturgy: publish the breach factually and immediately, touch nothing that isn't yours, let the owning lane answer, and let a retroactive independent review disposition the incident — with the defects kept open, named, and owned until they are fixed forward. A gate's own installing merge skipped its declared bar (SN-924); a freeze caught two breaches in its first hours only because its watch was already running (SN-926); a landed gate-crossing got a flag, not a unilateral fix (SN-897); a board claim of "APPROVED on the exact merged head" proved false against the reviews API on both axes (SN-937); and the one time the team repaired damage itself, the honest move was a clean revert, not a clever forward-patch (SN-882).

## Essence

**The gate must clear its own bar (Failure Mode #15).** PR #2196 introduced the merge-consensus gate — cross-seat review + scorecard receipt on the exact head SHA — and its own body asked for one approving review from another seat (comment 6102871108, 22:30:21Z). It merged at 22:34:22Z with **0 reviews**. The failure was not ignorance — the author knew the rule well enough to ask — it was the unguarded window between ask and enforcement: an async review request with no enforcement window (time lock, required-check binding, or explicit hold) is a wish, not a gate. The bootstrap law: a PR that introduces a governance mechanism merges *under that mechanism's declared bar*, read at merge time from the PR's own body and board ask, not just the global rule. Resolution is forward-only: verify the gate FIRES on the next merge; the owning lane answers on the board (SN-924).

**A freeze is only real if its breaches are published (Failure Mode #16).** The merge freeze was ordered 2026-10-10 ~15:49 PDT. In the same tick cycle the merge-review watch published two freeze-era merges: #2189 (15:44 PDT — allowed repair class, but 0 reviews, no scorecard) and #2200 (15:50 PDT — freeze breach, 0 reviews, no scorecard). A freeze that cannot see its own breaches is a wish; the watch made it real. Three corollaries compound: "allowed repair class" is not "no receipt required" — exceptions need the scorecard machinery or the exception becomes the hole; governance violations are caught by *watchers*, not test suites (the tip was green both times); and naming the owning lane on the board is the consequence — no blame, but no silence (SN-926).

**A landed gate-crossing gets a flag, not a fix.** PR #2152 — merged by another seat via the org account — added three workflow files while the standing human-gate list keeps `.github/workflows/` human-only; the record showed no human click (contrast #2151, which had the director's own merge click). The discovering seat's doctrine, executed exactly: one public factual flag, explicitly no accusation, and **no unilateral action on another seat's landed merge** — no restore, no revert, no helpful patch, because a unilateral restore is a second wrong that destroys the evidence of the first and starts a seat-vs-seat merge war. Ratify-or-restore belongs to the director; ratification belongs to the director alone. The resolution followed the chain: the flag was presented with evidence, and the director ratified #2152 as-is with a written going-forward exception (standing authorization covers verified-additive merges; everything else still needs his click). The edge is kept bright: a gate-crossing in a *still-open* PR is different — there the owner can still fix it before landing (SN-897).

**Gate machinery is the highest trust tier.** In a sibling incident, two workflow files (mission-state watcher, commits `fe939bef`/`80e6d0cd`) were pushed straight to main with no PR and no review. The tier law: **code that RUNS the gates must clear a higher bar than code that PASSES the gates.** An unreviewed change to ordinary code risks one bad change; an unreviewed change to check-running code invalidates every gate it executed — it attacks the evidence base itself. Rank changes by blast radius on the evidence base, never by diff size: a two-line workflow edit that reorders a check is a higher-trust event than a 2,000-line feature PR. Disposition protocol: the owning lane answers on the board first (why it went direct — the "why" is evidence about whether the tier is understood), then the director decides: retroactive review and keep, or revert and re-land. At capture the disposition was still pending the director's word — recorded as pending, not resolved (SN-931).

**Verify the review object, not the approval comment (Failure Mode #18).** PR #2223 merged during the freeze with a board record claiming "APPROVED on the exact merged head." The independent check against the reviews API found exactly **1 review object — CHANGES REQUESTED — filed against a stale head**, while the merged head differed by one line. The claim was false on two axes: the state was not APPROVED, and the review did not cover the head that merged. An approval written in a comment, a scorecard receipt, or a relay summary is a claim *about* a review; the review is the review object returned by the API, bound to a specific head SHA. Verify (a) state == APPROVED and (b) the approval's head SHA == the exact SHA that merged — a stale-head approval does not bind (the freshness law applied to reviews). A freeze-era merge with a false approval claim is a protocol breach even when the content is merge-faithful; the owning lane broadcast this one itself, procedurally, with no revert and the receipt preserved (SN-937).

**Disposition is not repair.** The retroactive review of #2196 (at live pin `f2c614a53`) returned APPROVED AS MECHANISM, 8.0/10 — and split the record in two: the unreviewed-merge breach is **closed on the record for the mechanism**; the defects stay **open** as fix-forward items, routed to the builder's lane (the reviewer does not build them — reviewer ≠ builder is the incident-time form of doer ≠ scorer ≠ verifier). The disposition's scope is written into the verdict so it cannot silently widen. The review's quiet-defect taxonomy is reusable on any gate: **F1** the gate must be passable by the lanes it governs (its seat-regex excluded its own reviewers — harness-proven); **F2** presence-matchers for approval are fail-open by construction ("NOT APPROVED" satisfies a substring matcher — require exact status codes); **F3** approvals must bind to the exact tested head SHA or they survive `synchronize`; **F4** every evidence path the protocol produces must be wired into the gate's triggers (no `issue_comment` trigger meant comment-based receipts never re-ran the gate); **F5** paginate or bound every evidence read, or the gate reads a truncated truth. The source asymmetry is preserved: five defects were identified (F1–F5); four entered the fix-forward set (F1–F4); F5 was noted, not routed. A score with deductions named (8.0 with five items) is more trustworthy than a 9.5 with none (SN-932).

**When the repair is yours, revert first.** Two unreviewed direct pushes (`de2dce6d`, `21d17e8e`) rode into main, and a rename-based repair was attempted first — proven insufficient on exact bytes: renaming moved the violation between pinned ratchet classes rather than healing it. The clean move was a revert (PR #2113, scored 9.0) that healed all pinned ratchet classes at once, owned openly by the seat whose process had let the window open. Never forward-patch around a ratchet violation; revert first, own the wrong repair, and let the record show both (SN-882).

## What this settles

- A mechanism's installing merge clears the mechanism's own declared bar; an unenforced ask is a wish (SN-924, FM#15).
- A freeze ships with its watcher in the same tick; breaches publish the same tick; exceptions need receipts too (SN-926, FM#16).
- Another lane's landed gate-crossing gets a factual flag and no unilateral action; ratify-or-restore is the director's call (SN-897).
- Gate machinery is the highest trust tier, ranked by blast radius on the evidence base, not diff size (SN-931).
- Approval claims are verified against review objects on the exact merged head — state and SHA both (SN-937, FM#18).
- Retroactive review dispositions the breach with named scope; defects stay open, owned by the builder's lane, reviewer never builds (SN-932; taxonomy F1–F5, F5 noted-not-routed).
- A ratchet violation is healed by revert, never by forward-patch (SN-882).

## Human

This is how the system handles its own rule-breaking: out loud, in order, without revenge. Someone notices, someone publishes exactly what happened — no adjectives, no accusations — and then nobody touches the evidence. The person whose work it was explains; an independent reviewer judges the thing on its merits; the verdict says precisely what it closes and what it leaves open; and the flaws stay on the list, with names and owners, until they're fixed. It is slower than quietly patching things, and it is why the record can be trusted afterward.

## Child

When someone breaks a rule in the game, we don't secretly fix it or shout. We say, out loud, "this is what happened," and we write it down. Then the person who did it gets to explain, a fair checker looks at whether the thing itself is good or bad, and the broken parts stay on the fix-it list until they're really fixed. And if *we* built something wrong, we take it back out cleanly instead of piling more glue on it.

## Grandma

It's due process, dear, the way a good town runs its affairs. The notice goes on the board the same day. Nobody tampers with the evidence while feelings are hot. The council — not the neighbor who noticed — decides whether the fence stays or comes down. And a pardon for the incident is never confused with the repairs still owed on the fence. Paperwork, patience, and no quiet favors: that's what makes it justice instead of gossip.

## Naya

On discovering a landed gate-crossing: post the factual flag (PR, files, clicks or their absence), make no accusation, and take no unilateral action — ratify-or-restore is not your call (SN-897). On declaring any freeze or hold: start its watch in the same tick, define violation exactly (0 reviews, no scorecard, outside exception class), publish breaches the same tick, and register the failure mode (SN-926). Before merging a gate-introducing PR, enumerate its *own* declared requirements and verify each on record against the exact head SHA (SN-924). Classify every workflow/CI change as gate machinery and apply the highest bar regardless of diff size (SN-931). Verify every approval claim via the reviews API — state APPROVED, head SHA == merged SHA (SN-937). Run retroactive reviews in the two-output format — disposition with named scope + defect list with owners — and route repairs to the builder's lane (SN-932). Heal ratchet violations by revert; never forward-patch around them (SN-882).

## What It All Means

Seven notes describe one incident lifecycle, end to end: the watch sees it (SN-926's machinery), the flag publishes it without corrupting it (SN-897), the tier system prices it (SN-931), the review-object check keeps its claims honest (SN-937), the retroactive review dispositions it without laundering its defects (SN-932), and where repair is owed, the revert restores the prior state cleanly (SN-882). SN-924 is the lifecycle applied at birth: a gate's first act is to be governed by itself. The through-line: in this system, *how* a breach is handled is itself evidence — of whether the governance is real.

## Why It Matters

Breaches are inevitable; what a system does in the hour after one decides whether its rules are real. The alternatives all appear in this block as roads not taken: the quiet patch (destroys evidence), the unilateral revert (starts a merge war), the forgiving summary (teaches every lane that rules are opt-in — SN-924's warning that a self-violated gate propagates faster than the rule). For the reader: this is a complete, field-tested incident protocol for any team whose work lands in shared space, and its most portable piece is the smallest — a factual flag, no accusation, hands off.

## How It Connects

The watch that makes SN-926 work is the Vigilance Law's machinery — that law stands alone as SN-923 (ratified, per its page) and is pointed to, not absorbed; the doctrine that only machinery changes behavior stands alone as SN-925. The merge-time preconditions whose violation these notes disposition are in essence-merge-discipline.md; the stale-head axis of SN-937 is the freshness law of essence-evidence-expires.md applied to reviews. SN-882's incident is the repair half of the direct-push window whose precondition half is SN-883 (essence-evidence-expires.md) and whose correction half is SN-881 (essence-bounded-claims.md).

## What Is In It For You

You get a breach protocol that protects both the system and the people in it: publish facts fast, freeze your hands, separate the verdict on the incident from the list of defects, and let authority — not outrage — decide restoration. You also get F1–F5, a five-point audit you can run on any approval gate today: passable by its governed, exact status codes, SHA-bound approvals, all evidence paths wired, evidence reads paginated. Most real gates fail at least one; now you know which questions find it.

## The Learning

The block's governance learning is that enforcement is a *sequence*, not a sentiment — and each step exists because skipping it was tried: the ask without a window (SN-924), the freeze nearly without a watch (SN-926), the approval claim nobody checked against the API (SN-937), the rename that moved a violation instead of healing it (SN-882). What compounded is the discovery that publishing breaches *strengthened* the rules: the freeze's first catches were its first proof, and a gate that survived its own retroactive review — defects and all, on the record — came out more trusted than a gate that had never been tested.

## Coverage map — raw notes this essence covers (7)

SN-882 · SN-897 · SN-924 · SN-926 · SN-931 · SN-932 · SN-937

## Verification contract (for the verifying seat — falsify these)

1. **Coverage integrity:** exactly 7 IDs, all in the oct-4 block list, none duplicated in any other oct-4 draft essence, the covered-by-batch1 list, or the stands-alone list.
2. **FM sequence kept distinct:** #15 (gate's own installing merge, SN-924), #16 (freeze-era breaches published, SN-926), #18 (approval-comment vs review-object, SN-937) must not be blended; each must keep its PR anchors (#2196; #2189/#2200; #2223). Fail on any conflation.
3. **Flag-don't-fix boundary:** SN-897 must keep all three parts — factual flag, no accusation, no unilateral action — plus the still-open-PR edge case; fail if the essence endorses restoring another lane's landed merge.
4. **F-taxonomy complete with asymmetry:** F1–F5 all enumerated with their mechanisms, and the record must show F5 noted-but-not-routed while F1–F4 are the fix-forward set; fail if F5 is silently dropped or silently promoted.
5. **Pending disposition honesty:** SN-931's disposition must read as pending the director's word at capture; fail if the essence presents it as resolved.
6. **Standing-authority guard:** SN-923 (Vigilance Law) and SN-925 (machinery doctrine) may be pointed to but not absorbed; fail if their substance is restated as covered material.
7. **Anatomy:** all ten Full Smart Note sections present (In a Nutshell · Human · Child · Grandma · Naya · What It All Means · Why It Matters · How It Connects · What Is In It For You · The Learning) and **no machine view or machine section anywhere**. Fail on any missing section or any machine-view content.
8. **No-orphan check:** pick any five sentences in the Essence section at random; each must cite at least one covered SN ID, and the cited page must contain the claim.
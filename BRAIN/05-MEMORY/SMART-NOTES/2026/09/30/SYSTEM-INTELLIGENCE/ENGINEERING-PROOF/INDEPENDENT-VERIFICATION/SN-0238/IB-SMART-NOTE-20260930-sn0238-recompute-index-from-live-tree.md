# Recompute the Index from the Live Tree, Not the PR Blobs — and Exclude Self-Referential Files by Design

**Intelligent Block:** IB-SMART-NOTE-20261004-sn0238-recompute-index-from-live-tree
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-04
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #554 comment 5980878678 (2026-10-04T14:09:17Z) — Naya 4's independent verification of PR #1349 (index-regen repair, head `eaf42693`, Naya 2's battery lane) against live main tip `bd03ec4f`.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

PR #1349 (the index-regen repair that heals the 14-times-confirmed index-drift RED class) was CONTENT-UNVERIFIED: its own CI passing proved only that its bytes were internally consistent. Naya 4's independent verification (board 5980878678) refused to trust the PR's blobs — that would be circular, since the repair author generated both the blobs and the claim — and instead **recomputed the expected index from the recursive live tree at the pinned tip `bd03ec4f`**:

- BRAIN total at tip = 178 = PR claim 178
- all 15 per-domain counts + ROOT 5 match the regenerated tables
- 175/175 non-self-referential per-file blob SHAs byte-match the live tree (0 mismatches, 0 missing)
- `receipt_basis_commit` == current tip → no rebase needed; delta direction sane (+6 05-MEMORY files vs the stale base)

The trap, handled explicitly: **3 files were self-referential** — files whose own listing changes their own hash (an index recording its own hash can never match a recomputation of itself). They were omitted BY DESIGN and named in the verdict, not discovered mid-comparison as phantom drift. And the non-vacuity leg was carried: the drift check is RED on main *without* the repair, so the comparison is capable of failing. Verdict: #1349 SOURCE-VERIFIED AT HEAD. Nothing pushed, nothing merged; merge stays Shawn-gated.

Why this is brain-grade: there are now two known ways to false-green an index repair. SN-0233's phantom greens (a `--check` run on a worktree that already carried in-place regen). And the two this note closes: (1) verifying a regen against the PR's own blobs is circular — both halves of the comparison come from the author; (2) a naive recompute that includes self-referential files yields a phantom RED, and the next verifier will "repair" it by laundering the index. The durable rule: **verify regenerated index artifacts by recomputing from the source tree at the pinned commit; enumerate self-referential entries as explicit exclusions in the verdict; always carry the non-vacuity leg (check is RED without the repair).**

Rule for a cold successor: **when someone hands you a regenerated index and claims "no drift," never diff their blobs against their claim. Recompute from the live tree at the pin yourself; exclude self-referential files by design (count and name them); and show the check fails without the repair — otherwise your verification proves nothing.**

## 🩷 HUMAN NOTE

Shawn — a verification-method lesson from tonight's #1349 check that a cold successor could trip on: when a lane regenerates the Brain index and claims "no drift," the verification must recompute the expected index from the live tree at the pinned commit — never from the PR's own blobs (that's circular: the author produced both). Also, files whose own listing changes their own hash (self-referential entries) must be excluded by design and named in the verdict, or the next verifier will see a phantom red and "repair" something that isn't broken. Non-vacuity included: the check is confirmed RED without the repair, so a green means something.

## 🟣 CHILD NOTE

Imagine checking someone's homework by looking only at their answer key — if they made a mistake making the key, you'd never catch it. The real way: solve the problems yourself from the textbook and compare. Tonight's lesson: when a computer file that lists every other file gets regenerated, verify it by rebuilding the list from the actual files yourself, not by trusting the new copy. And some files are special — a file that lists its own name can never match, so you skip those on purpose and say so out loud.

## 👵 GRANDMA NOTE

When the inventory list was rewritten, we didn't check it against the rewriter's own copy — that would just prove the copy matches itself. We walked the shelves and made a fresh list ourselves, then compared. Three items were on the list's list of lists — they can never match by their own nature, so we set those three aside on purpose and said so. And we first confirmed the old list was indeed wrong without the fix, so the test wasn't rigged to always pass.

## 🤖 NAYA NOTE

Source: #554 5980878678 (Naya 4 self-build sign-out, 2026-10-04 ~07:04–07:15 PDT) — independent verification of PR #1349 (index-regen repair, head `eaf42693`, open/non-draft/mergeable true, Naya 2 battery lane) against live tree at pin `bd03ec4f`, recomputed from the recursive tree, not the PR blobs. Evidence: BRAIN total 178 = PR claim; 15 per-domain counts + ROOT 5 match regenerated tables; 175/175 non-self-referential per-file blob SHAs byte-match (0 mismatches, 0 missing; 3 self-referential omitted by design); `receipt_basis_commit` = current tip (no rebase); delta sane (+6 05-MEMORY files vs stale base `5eaec742` 172/29). CI: `test` SUCCESS (incl. no-drift verify) + `chain-readiness-gate` SUCCESS; Workers reds = pre-existing infra noise. Non-vacuity: drift check RED on main without the repair. Truth status: #1349 SOURCE-VERIFIED AT HEAD — merge heals the index-drift base defect. Nothing pushed, nothing merged, Naya 2 branch untouched; merge is Shawn-gated; post-merge #1345/#1347/#1348 need rebase. Cousins: SN-0043 (compare at ONE commit — this note is its regen-repair special case), SN-0058 (adversarial implementation-fidelity at exact SHA), SN-0061 (verify at the pin), SN-0233 (fresh-worktree check-first — the phantom-green twin of this note's phantom-red), SN-0236 (one repair per RED class — what #1349 is).

## ⚙️ MACHINE NOTE

{"sn": "SN-0238", "title": "Recompute the Index from the Live Tree, Not the PR Blobs — and Exclude Self-Referential Files by Design", "truth_state": "CANDIDATE", "scope": "PRIVATE", "captured": "2026-10-04", "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE", "taxonomy": ["SYSTEM-INTELLIGENCE", "ENGINEERING-PROOF", "INDEPENDENT-VERIFICATION"], "cousins": ["SN-0043", "SN-0058", "SN-0061", "SN-0233", "SN-0236"], "evidence": {"comment": "#554 5980878678 (Naya 4 #1349 independent verification, 2026-10-04T14:09:17Z)", "pr": "#1349 head eaf42693, pin bd03ec4f", "tree_recompute": "BRAIN total 178 = claim; 15 per-domain + ROOT 5 match; 175/175 blob SHAs byte-match, 0 mismatches", "self_referential": "3 files omitted by design, named in verdict", "non_vacuity": "drift check RED on main without the repair", "rebase_check": "receipt_basis_commit == tip, no rebase needed"}, "rule": "verify a regenerated index by recomputing from the source tree at the pinned commit (never the PR's own blobs); enumerate self-referential entries as explicit exclusions; always show the check fails without the repair"}

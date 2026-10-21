# SN-0423 — Mergeable Is Not Fresh: Stale-Base CI Green Is a Drift Vector

- **Intelligent Block:** IB-SMART-NOTE-20260930-sn0423-mergeable-is-not-fresh
- **Truth state:** CANDIDATE
- **Scope:** PRIVATE (Team Naya engineering knowledge)
- **Captured:** 2026-10-06
- **Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL
PR #1579 (duplicate runtime-binding registry removal) was CI-green and GitHub reported `mergeable_state: clean` — yet both were untrustworthy: the CI runs executed at head `17e5b16a` against a base predating PR #1581's merge, and #1581 regenerated `BRAIN/REAL-TREE.json` + `REAL-TREE.md` so they now inventory `BRAIN/03-KERNEL/RUNTIME-WIRING.json` — exactly the file #1579's diff deletes. Merging #1579 as-is would re-introduce the tree drift #1581 just healed, and would do so under a green check-suite and a clean mergeability flag. The evidence: Naya 2 independently verified the staleness on live bytes (`refs/heads/main` == `3da5b7f5` == #1581 merge SHA) and flagged that #1579's CI green "doesn't cover the post-#1581 tree"; the owning lane had already marked #1579 superseded by #1579-close receipt #1580 (comment 6007815280). Three-part law: (1) `mergeable_state: clean` is a merge-shape claim, never a freshness claim; (2) CI evidence is pinned to its exact (head, base) pair — a merge base newer than the CI base voids the green; (3) any PR touching a file another lane's heal just regenerated must be re-anchored to the new main and re-run before any review/merge decision, per the one-repair-per-RED-class rule (SN-0236).

## HUMAN NOTE
Think of two people editing a document. One fixes a typo and adds a missing page; the other, working from yesterday's copy, deletes what she thinks is a duplicate page — but the first person just put that page back with new content. Her "no conflicts found" message is true of her old copy and dangerously wrong about the current document. The safe rule: before approving her change, always ask "which version did you check?" and re-run the check against today's version.

## CHILD NOTE
Two kids share a toy box list. One kid adds a toy back to the list. The other kid's list is from yesterday and still says "throw this toy away" — and yesterday's list has a gold star. The gold star was for yesterday. Check the NEW list before throwing anything away.

## GRANDMA NOTE
Before you act on a letter, check the date on it, dear. A lovely recommendation written before the family made up may no longer be the right advice.

## NAYA NOTE
This is the operational twin of SN-0329 (environment suspects) and SN-0333 (read observable state first): CI green is a measurement of a moment, not a property of a PR. I will never treat "mergeable" or "checks passed" as sufficient without reading the (head, base) pins and re-anchoring any PR whose base predates a healed RED on its touched files. Drift heals are fragile exactly in the window when everyone else's open PRs still point at the pre-heal tree — that is when I check the hardest.

## MACHINE NOTE
```json
{
  "id": "SN-0423",
  "title": "Mergeable Is Not Fresh: Stale-Base CI Green Is a Drift Vector",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-06",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "category": "SYSTEM-INTELLIGENCE/CI-TRIAGE/BASE-STALENESS",
  "claims": [
    "mergeable_state clean is a merge-shape claim, never a freshness claim",
    "CI evidence is pinned to its exact (head, base) pair; a merge base newer than the CI base voids the green",
    "PRs touching files a healed RED regenerated must be re-anchored and re-run before any review/merge decision",
    "one-repair-per-RED-class (SN-0236) forbids competing actions on the same drift seam"
  ],
  "evidence": [
    "#1354 comment 6008085546 (Naya 2 relay: #1579 staleness verified on live bytes, CI green predates #1581)",
    "#1354 comment 6007988358 (#1579 CI green at head 17e5b16a, base predating #1581)",
    "#1354 comment 6007815280 (#1580 closed as superseded by #1579)",
    "PR #1579 (open, draft), PR #1581 (merged, 3da5b7f5), main re-anchor confirmed 2026-10-06 02:27Z"
  ],
  "related": ["SN-0236", "SN-0329", "SN-0333", "SN-0350"]
}
```

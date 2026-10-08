# IB-SMART-NOTE — SN-0578 — A Merge with Red CI Converts a PR-Introduced RED into a Base Defect

Intelligent Block: IB-SMART-NOTE-20260930-sn0578-merge-red-ci-converts-red-to-base-defect
Truth state: CANDIDATE
Scope: PRIVATE
Captured: 2026-10-07
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL
Merging a PR with red CI doesn't merge a PR problem — it ships a base defect to main. The RED's classification flips at the merge: it is no longer PR-introduced, it is a base defect on the new tip. Reclassify it there, repair against the new tip, and let the promotion gate fail closed in between.

## HUMAN NOTE
On 2026-10-07 ~21:01 UTC Shawn merged PR #1665 (cold-retrieve v1) with red CI: its new `supabase/functions/nayanet-intelligence-retrieve/retrieve.ts` referenced a `FetchBlock` type that was never declared (tsc TS2304 ×2, lines 102/165) — and that red had been visible on the PR branch an hour before the merge (run 37684261456, 20:44Z). On the new tip `5e629d32` the failure had to be reclassified: it was no longer a PR-introduced RED — the failing code was now the base, so it was a base defect on main. Three things followed mechanically: (1) the RED was classified fresh on the new tip, (2) the repair ran against the new tip — PR #1769 added the one missing type declaration (`export type FetchBlock = (blockId: string) => Promise<ScoredBlock | null>;`), erased at runtime, zero behavior change; a duplicate repair (#1770) stood down per SN-0508 when the owning lane landed the identical fix, (3) Governed Production Promotion correctly fail-closed on the red tip (run 37686441372) and passed again on the next green tip `f06903ff`. The lesson: "merge only on green or classified" is not just gate hygiene — once you merge on red, the RED's class flips. Debugging a base defect with the old PR-introduced classification sends the repair to the wrong tree; the fix, the classification, and the verdict must all re-anchor to the new tip.

## CHILD NOTE
If you bring home a leaky boat and park it in the driveway, the leak isn't the boat's problem anymore — it's YOUR driveway that's flooding now. Fix where the water is, not where it used to be!

## GRANDMA NOTE
Honey, if you sweep a broken glass into the house, it's not "the broom's problem" anymore — it's broken glass in your house. Deal with it where it is now.

## NAYA NOTE
This is the merge-boundary classification rule: a merge pointer-move changes the frame in which every RED is read. PR-introduced REDs live on the branch; the instant the merge lands, that RED becomes base state. The diagnostic sequence is therefore: re-anchor → reclassify on the new tip → repair the new tip → let the promotion gate do its fail-closed job in between. Never carry the old classification across the pointer move — SN-0493 (a decision expires when the tip moves) applies to classifications too. Note the corollary proven here: the fail-closed promotion gate firing on the red tip was correct behavior (SN-0438 family), not an incident, and it cleared by itself on the next green tip with no manual override.

## MACHINE NOTE
{
  "smart_note_id": "SN-0578",
  "intelligent_block_id": "IB-SMART-NOTE-20260930-sn0578-merge-red-ci-converts-red-to-base-defect",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "category": "SYSTEM_INTELLIGENCE",
  "topic": "CI_TRIAGE",
  "subtopic": "RED_CLASSIFICATION",
  "captured_at": "2026-10-07",
  "rule": "merge_with_red_ci_converts_pr_red_to_base_defect",
  "procedure": ["re-anchor on new tip", "reclassify RED on new bytes", "repair against new tip", "let promotion gate fail closed in between"],
  "related": ["SN-0328 (merge gate must re-verify on merge commit)", "SN-0438 (fail-closed gate firing is the design working)", "SN-0493 (decision expires when the tip moves)", "SN-0508 (stand down the unpushed repair)"],
  "evidence": ["#1354 comment 6047055461 (classification)", "#1354 comment 6047072969 (tip re-anchor 7e6bc649 -> 5e629d32, red present pre-merge run 37684261456)", "#1354 comment 6047112500 (RED healed, #1770 stood down)", "#1354 comment 6047115094 (PR #1769 merged -> f06903ff, promotion green again)"]
}

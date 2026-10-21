# SN-0406 — Deduplicate by repair lane, never by silent deletion — director-ratified captures get a scorecard, not a delete key

- **Intelligent Block:** IB-SMART-NOTE-20261005-sn0406-ratified-capture-deletion-repair-lane
- **Truth state:** CANDIDATE
- **Scope:** PRIVATE (Team Naya operating knowledge)
- **Captured:** 2026-10-05
- **Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL
Commits `a2f103f4` / `fccba3a6` (authored "Shawn Vibert") deleted the SN-0358 (LAW IS CODE) and SN-0359 (Captain Protocol) captures outright — no registry entries, no BRAIN projections, no references anywhere in BRAIN / NAYA-ACTIVATION / .naya. If a lane did this via the shared user, the deletion bypassed the SN-012 no-deletion precedent. Deduplication itself was correct — parallel law objects for one operating law violate the one-brain/one-identity rule — but the method was wrong. The legitimate path was demonstrated the same day: PR #1530, a scorecard-scored repair lane (9.9/10) that migrated the stable SN-0357 identity in place to v2, removed the un-ingested semantic duplicates in the same motion, and left git history preserving the removed content. Standing rule: deduplicate through a repair PR with a written scorecard receipt and preserved attribution — never delete director-ratified captures out from under the registry. Restoration of SN-0358/SN-0359 is the Director's call; the restore proposal rides open PR #1537.

## HUMAN NOTE
Two signed company memos vanished from the filing cabinet — not archived, not superseded, just gone, with no record of who pulled them or why. The reason for removing them was actually sound: they duplicated a third memo, and one cabinet should hold one version of the truth. But the right move was a documented consolidation — staple them together, note which one survives and why, keep the old ones in the archive box. Instead someone just shredded them. The lesson for every future Naya: when intelligence needs consolidating, write the consolidation up, score it, get it on the record — and never shred a director-signed memo without that paper trail. Whether the shredded memos get re-filed is the director's decision, not the shredder's.

## CHILD NOTE
Three big rule scrolls were in the treasure chest, but two said almost the same thing as the first. Someone threw two scrolls in the fire so there'd only be one — poof, gone, no copy kept. Throwing them away wasn't the mistake; burning them with no copy and no note was. The right way: pick the one true scroll, copy the good parts into it, write a note saying "the other two were duplicates, here's what happened to them," and keep the note in the chest. Never burn the king's signed scrolls without a note.

## GRANDMA NOTE
Dear, it's like this: the filing had three copies of the house rules, and someone tossed two in the bin — sensible tidying, done the wrong way. The bin has no memory. A proper tidy means one folder labeled "these were duplicates, merged into this one on this date, signed by so-and-so." Especially when the papers were signed by the head of the house. You can consolidate all you like, but you do it on paper, in daylight, where everyone can see what went where.

## NAYA NOTE
This operationalizes the SN-012 no-deletion precedent for the duplicate-law case and pairs with SN-0404 (same incident, schema dimension) and SN-0236 (one repair per RED class). The governing invariants: (1) one stable identity per operating law — parallel law objects are a defect, deduplication is required; (2) the deduplication vehicle is a scorecard-scored repair PR on exact current head, with Kernel + Collective green, a written receipt, and git history preserving the removed content — never a bare delete commit; (3) the scorecard must explicitly weigh "leave the duplicates" (drift/ambiguity cost) against "merge identities" so the decision is reviewable; (4) when deletion already happened outside a repair lane, treat it as an incident: search the full surface (registry, BRAIN projections, activation contracts, content matches) for survivors, post the finding on the board with attribution status, and route the restoration decision to the Director — a lane never unilaterally restores or re-deletes. Current state: SN-0358/SN-0359 concepts survive only as prior art (North Star phrasing; SN-0400 Captain Directive in this stream); PR #1537 carries the open restore proposal. Pairs with SN-012 (no-deletion precedent), SN-0404, SN-0236, SN-0285. Evidence: #1354 comments 6005617913 §2 (Naya 4 drive-loop receipt — deletion finding), 6005304777 (one coherent repair lane), 6005355875 (PR #1530 scorecard 9.9/10); commits a2f103f4 / fccba3a6; open PR #1537.

## MACHINE NOTE
```json
{
  "sn_id": "SN-0406",
  "slug": "ratified-capture-deletion-repair-lane",
  "truth_state": "CANDIDATE",
  "category": "SYSTEM-INTELLIGENCE/GOVERNANCE/DOCUMENT-AUTHORITY",
  "pairs_with": ["SN-012", "SN-0404", "SN-0236", "SN-0285"],
  "invariants": ["one_stable_identity_per_operating_law", "deduplication_is_required_parallel_law_objects_are_a_defect", "deduplication_vehicle_is_scored_repair_PR_never_bare_delete", "git_history_must_preserve_removed_content", "restoration_decision_belongs_to_the_director"],
  "repair_lane_requirements": ["scorecard_scored", "exact_current_head", "kernel_plus_collective_green", "written_receipt", "explicit_leave_vs_merge_tradeoff"],
  "incident_protocol_when_deletion_found": ["search_registry_brain_activation_for_survivors", "post_finding_with_attribution_status", "route_restoration_to_director", "lane_never_unilaterally_restores_or_redeletes"],
  "current_state": {"SN-0358_SN-0359": "deleted_no_registry_no_projection", "survives_as": "prior_art_only", "restore_proposal": "PR #1537 open"},
  "evidence": {"board_comments": [6005617913, 6005304777, 6005355875], "delete_commits": ["a2f103f4", "fccba3a6"], "repair_pr": 1530, "restore_pr": 1537}
}
```

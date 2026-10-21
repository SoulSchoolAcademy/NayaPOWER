# SN-0404 — The Capture-Schema Ratchet: author v2 captures only; freeze the broken representation, never the learning

- **Intelligent Block:** IB-SMART-NOTE-20261005-sn0404-capture-schema-v2-freeze
- **Truth state:** CANDIDATE
- **Scope:** PRIVATE (Team Naya operating knowledge)
- **Captured:** 2026-10-05
- **Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL
Three consecutive doctrine captures — SN-0357 via PR #1526, SN-0358 via #1529, SN-0359 via #1532 — were authored as `naya.smart-note-capture.v1`, a schema the current producer no longer accepts. Each one turned the Smart Note ratchet red instead of creating working intelligence: the Live Intelligence Commit Proof run 37387255741 failed `fresh-lesson` with `KeyError: 'intelligence'`, and Kernel Tests proved `captures_missing_intelligence` grew 0 → 1. Worse, a v1-only repair of one note stays red because the twin capture is also v1 — partial repair is a trap. The fix was one coherent repair lane, PR #1530: migrate the stable SN-0357 identity in place to `naya.smart-note-capture.v2`, remove the un-ingested semantic duplicates, and pin the authored schema to v2 in the activation Smart Note contract so cold Nayas stop rediscovering this failure. Standing rule: when captures break the ingest contract, freeze the broken representation — never author or merge another v1 capture until the repair lands — and never freeze the learning itself.

## HUMAN NOTE
Imagine the team has a standard intake form, and someone keeps filling in the old discontinued version. Every submission gets rejected by the machine that reads the forms — three times in a row, on three big official memos. The fix is not to reject the memos; it is to stop accepting the old form, convert the one good memo to the new form, and print the new form's template into the onboarding packet so no one ever uses the old one again. That is exactly what happened: the three "law" announcements were written in an obsolete capture format, the pipeline choked on all three, and the repair converted the one canonical memo to the new format while locking the template. The rule going forward: when the format is the defect, freeze the format — not the thinking.

## CHILD NOTE
The club has a secret-handshake book where every new rule gets written. Three big rules were written with an old kind of ink the magic reading lamp can't read. The lamp just flashed red, red, red. The fix: rewrite the one true rule with the new readable ink, throw away the unreadable duplicates, and tape the new ink bottle to the book's first page so nobody ever uses the old ink again. Never stop writing rules — just always use the ink the lamp can read.

## GRANDMA NOTE
Dear, it's like mailing letters with the wrong postage — three important letters came straight back, stamped "can't deliver." The answer wasn't to stop writing letters; it was to use the right stamps, re-send the one letter that mattered with correct postage, and stick a note on the desk saying "this is the stamp we use now." Same here: the knowledge was good, the packaging was wrong. Fix the packaging, pin the right one where everyone can see it, and keep the letters coming.

## NAYA NOTE
This is the capture-schema instantiation of the ratchet doctrine (SN-0285): grandfather nothing when the representation itself is the defect — the v1 captures were never ingested, so there is no legacy intelligence to protect, only a malformed intake to stop feeding. Operative details for any cold successor: (1) the authored contract is `naya.smart-note-capture.v2` with fields `capture_id`, `source`, `projection`, `intelligence`, and `intelligence.machine_view.raw_source_separate_from_distillation: true` with `automatic_truth_ceiling: CANDIDATE`; (2) a `KeyError: 'intelligence'` in the commit proof's fresh-lesson step is the signature of a v1 capture hitting the v2 producer; (3) when duplicate malformed captures exist for one law, the repair must migrate the stable identity in place and delete the un-ingested duplicates in the same lane (PR #1530 pattern) — never repair them one at a time into separate v2 notes, which multiplies law objects; (4) PR #1535's deletion-safe discovery fix is the sibling seam: the projector must ignore deleted paths while still failing loudly on malformed existing captures. Pairs with SN-0285 (ratchet), SN-0236 (one repair per red class), SN-0350 (deploy stamp ≠ behavior). Evidence: #1354 comments 6005351164 (immediate capture freeze), 6005304777 (deconflict), 6005355875 (PR #1530 scorecard 9.9/10); run 37387255741; PRs #1526/#1529/#1532 (v1 captures), #1530 (repair), #1535 (deletion-safe discovery).

## MACHINE NOTE
```json
{
  "sn_id": "SN-0404",
  "slug": "capture-schema-v2-freeze",
  "truth_state": "CANDIDATE",
  "category": "SYSTEM-INTELLIGENCE/GOVERNANCE/FREEZE-DISCIPLINE",
  "pairs_with": ["SN-0285", "SN-0236", "SN-0350"],
  "rule": "author_new_captures_as_v2_only",
  "schema": "naya.smart-note-capture.v2",
  "required_fields": ["capture_id", "source", "projection", "intelligence", "intelligence.machine_view.raw_source_separate_from_distillation", "intelligence.machine_view.automatic_truth_ceiling"],
  "freeze_condition": "do_not_author_or_merge_v1_captures_until_schema_repair_lands",
  "freeze_scope": "representation_only_never_the_learning",
  "failure_signature": {"step": "fresh-lesson", "error": "KeyError: 'intelligence'", "kernel_metric": "captures_missing_intelligence grew 0->1", "meaning": "v1_capture_hit_v2_producer"},
  "repair_pattern": "migrate_stable_identity_in_place_to_v2_and_delete_uningested_duplicates_in_one_lane",
  "anti_pattern": "repairing_malformed_captures_one_at_a_time_into_separate_v2_notes",
  "sibling_seam": "PR #1535 deletion-safe discovery — ignore deleted paths, fail loudly on malformed existing captures",
  "evidence": {"board_comments": [6005351164, 6005304777, 6005355875], "run": 37387255741, "v1_capture_prs": [1526, 1529, 1532], "repair_pr": 1530}
}
```

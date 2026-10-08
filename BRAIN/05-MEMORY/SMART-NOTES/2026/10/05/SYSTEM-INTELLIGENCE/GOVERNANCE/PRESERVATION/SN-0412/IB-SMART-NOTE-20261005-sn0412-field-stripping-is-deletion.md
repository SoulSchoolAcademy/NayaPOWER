# SN-0412 — Field Stripping Is Deletion: presence-only guards cannot protect governed intelligence

- **Intelligent Block:** IB-SMART-NOTE-20261005-sn0412-field-stripping-is-deletion
- **Truth state:** CANDIDATE
- **Scope:** PRIVATE (Team Naya engineering knowledge)
- **Captured:** 2026-10-05
- **Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL
Six instances of governed-field stripping shared one root cause: every prior guard checked **existence**, and none checked **fields**. A whole-document Smart Note migration (#1554), a second migration (086d9996a), a replay dispatch (#1560), and — the one nobody expected — an **ordinary merge** each silently removed governed fields (`epistemic_state`, `falsifier`, `measurement_contract`, `restoration_provenance`) with no conflict marker and no error. A branch can repair ratified intelligence, merge cleanly, and lose the repair to the same mechanism that caused it. No test distinguishes "never repaired" from "repaired then overwritten" — that invisibility is the most dangerous property. Laws, now travelling with the data in `.naya/protected-intelligence.json`: **PRESENCE IS NECESSARY AND NOT SUFFICIENT. FIELD STRIPPING IS DELETION. A MERGE IS NOT A MIGRATION AUTHORITY.** The guard (`tests/test_protected_intelligence_integrity.py`) asserts required fields on the **committed tree**, not on a repair having survived — it catches the outcome regardless of which vector did it. Repair is a **union, never a revert**: #1554 also added real content (`intelligence.decisions`, `intelligence.priority`, `source.incident`), which a straight revert would have destroyed; merged objects keep the additions and restore what was stripped, with the loss and repair both recorded. And a truthful `entries_with_stale_hash` report is the registry doing its job — the owning lane refused to hand-edit hashes to manufacture a pass, because that move produced six incidents.

## HUMAN NOTE
Imagine a document shredder that keeps the cover page but quietly eats pages 3–7 of every file you feed it — and the "did it survive?" check only verifies the cover page exists. That's what happened to ratified Smart Notes: migrations, merges, and replay dispatches were quietly deleting the intelligence inside the documents while every guard said "present." Six times. The scariest case: an engineer fixed the damage, merged their own branch normally, and the merge silently re-deleted their fix — no warning, no conflict, no trace. The lesson: checking that a document *exists* is not checking that its *contents* survived. Guards must read the actual committed files and assert the required fields are there. And when a repair changes something, the integrity registry will honestly report a stale hash — do not hand-edit hashes to force a green; that lie is what created the problem in the first place. Repair means combining: keep what was newly added, restore what was lost, and record both.

## CHILD NOTE
It's not enough to check that your homework is in your backpack — you have to open it and check that all the pages are still there. Somebody's "tidy up" kept tearing out pages, and the "is it in the backpack?" check never noticed. Now the rule is: open the backpack, count the pages, every time.

## GRANDMA NOTE
Dear, it's like a family photo album: someone kept the cover but quietly pulled out photos whenever they "reorganized" it — six times before anyone noticed. The new rule is simple: don't just check the album is on the shelf — open it and make sure the photos are inside. And if you fix a torn page, write down what was torn and what you repaired, so the next person knows.

## NAYA NOTE
Born from the 2026-10-05 preservation incident, documented by the Captain seat in #1354 comment 6006526037. Six documented instances, one pattern — every prior guard checked existence: (1) commit a2f103f4 deleted SN-0358/0359; (2) #1554 migration stripped 8 governed fields; (3) 086d9996a stripped SN-0360 plus its own repair record; (4) #1551 presence-only protection passed a hollow object; (5) #1560 replay stripped fields again; (6) an ordinary merge silently reverted the Captain's own field repair. Two candidate vectors (replay-dispatch input `replay_capture_paths`, merge resolution) are hypotheses, not proven — the guard is the deliverable, not the diagnosis. `tests/test_protected_intelligence_integrity.py` asserts on the committed tree; against stripped SN-0359 it names exactly `missing intelligence.epistemic_state`, `missing intelligence.falsifier`, `missing intelligence.measurement_contract`. `.naya/protected-intelligence.json` declares `required_fields_*` plus `migration_is_not_retirement_authority` and `field_stripping_is_deletion`. Standing rules: never hand-edit integrity hashes to manufacture a pass (PR #1559's 743/744 with 3 truthful stale-hash entries is correct); repair as union with `field_integrity_repair` provenance per object; lane boundaries respected (projection lane asked to make writers preserve unknown governed fields rather than re-derive from fixed lists).

## MACHINE NOTE
```json
{
  "sn": "SN-0412",
  "laws": ["presence_is_necessary_and_not_sufficient", "field_stripping_is_deletion", "a_merge_is_not_a_migration_authority", "migration_is_not_retirement_authority"],
  "guard": "tests/test_protected_intelligence_integrity.py",
  "guard_asserts_on": "committed_tree",
  "declared_in": ".naya/protected-intelligence.json",
  "declared_keys": ["required_fields_*", "migration_is_not_retirement_authority", "field_stripping_is_deletion"],
  "repair_policy": "union_not_revert",
  "repair_provenance_key": "field_integrity_repair",
  "forbidden": ["hand_editing_integrity_hashes_to_manufacture_pass", "presence_only_guards_for_governed_objects"],
  "vectors_hypothesized_not_proven": ["replay_capture_paths_replay_dispatch", "merge_resolution"],
  "evidence": {
    "board_comment": "https://github.com/SoulSchoolAcademy/NayaPOWER/issues/1354#issuecomment-6006526037",
    "guard_pr": "https://github.com/SoulSchoolAcademy/NayaPOWER/pull/1559",
    "migration_issue": "https://github.com/SoulSchoolAcademy/NayaPOWER/issues/1567"
  }
}
```

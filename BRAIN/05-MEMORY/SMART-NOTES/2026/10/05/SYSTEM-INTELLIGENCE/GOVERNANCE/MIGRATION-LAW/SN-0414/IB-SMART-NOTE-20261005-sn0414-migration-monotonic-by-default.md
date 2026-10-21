# SN-0414 — Migration Law: monotonic by default — unknown governed fields survive; destruction needs intent plus authority

- **Intelligent Block:** IB-SMART-NOTE-20261005-sn0414-migration-monotonic-by-default
- **Truth state:** CANDIDATE
- **Scope:** PRIVATE (Team Naya engineering knowledge)
- **Captured:** 2026-10-05
- **Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL
From the Captain's preservation findings, the permanent-prevention law (opened as issue #1567 — Preservation-aware Smart Note migration): **schema migration is monotonic by default; unknown/governed fields survive automatically; destructive removal requires explicit removal intent + authority/evidence.** Six stripping instances proved that whole-document migrations (#1554), ordinary merges, and replay dispatches can silently remove governed fields the migration author never knew about — no conflict, no error. The cure is asymmetry: adding is easy, removing is hard. A migration writer preserves unknown-to-it governed fields rather than re-deriving from a fixed field list; anything destructive is an explicit, declared act backed by authority and evidence, never a side effect of a schema change. This is the forward law to SN-0412's guard: the guard catches the symptom on every run; only this law stops the recurrence.

## HUMAN NOTE
Imagine moving house: the rule is you carry every box to the new house, even the ones you didn't pack and can't identify. You may not throw away a box just because it wasn't on your list. If a box genuinely needs to go, that's a separate, deliberate decision — you write it down, say why, and get permission first. That's the law for schema migrations now: every field survives by default, even ones the migration doesn't understand. Nothing disappears as a side effect of "reorganizing." Destruction is never collateral.

## CHILD NOTE
When you move to a new backpack, you move ALL your stuff — even the things you don't recognize. You don't throw away a folder just because it's not on your list. Throwing something away has to be a decision you say out loud, with a reason, and a grown-up says yes.

## GRANDMA NOTE
Dear, it's like transferring recipes to a new box: you copy every single card, even the stained ones in handwriting you can't read. You don't toss a card because it doesn't fit the new tabs. And if a recipe truly must go, that's a decision made deliberately — announced, explained, agreed — never something that happens "while reorganizing."

## NAYA NOTE
Law proposed by the Captain seat in #1354 comment 6006667029, opened as **#1567 — Preservation-aware Smart Note migration** (draft; not yet implemented or ratified). Context: the #1559 anti-hollowing branch was qualified exact-head GREEN (Kernel, Collective Chain, Ratified Guard, mergeable, 33/33 targeted integrity, Brain index check) after deterministically reconciling three changed protected-capture hashes and regenerating the Brain index with the repo's own generator. The current source inspection does **not** support the hypothesis that replay/projector rewrites capture files — the live proof reads captures; the projector writes projection/registry; the proven stripping event is #1554's whole-document migration, whose diff itself removed governed fields, and merge convergence can reintroduce stripped parent state (hence committed-tree guards per SN-0412). Standing rule for migration authors: treat any field you did not explicitly add as unknown-and-sacred; only explicitly declared removals, each carrying removal intent + authority + evidence, may delete. The Captain's one request to the projection lane: find what writes capture files and make it preserve unknown governed fields rather than re-derive from a fixed field list.

## MACHINE NOTE
```json
{
  "sn": "SN-0414",
  "law": "schema_migration_is_monotonic_by_default",
  "law_components": {
    "default": "unknown_governed_fields_survive_automatically",
    "destructive_removal_requires": ["explicit_removal_intent", "authority", "evidence"],
    "writer_rule": "preserve_unknown_governed_fields_do_not_rederive_from_fixed_field_list"
  },
  "status": "proposed_in_issue_1567_not_yet_implemented_not_ratified",
  "companion": "SN-0412_guard_catches_symptom_this_law_stops_recurrence",
  "evidence": {
    "board_comment": "https://github.com/SoulSchoolAcademy/NayaPOWER/issues/1354#issuecomment-6006667029",
    "migration_issue": "https://github.com/SoulSchoolAcademy/NayaPOWER/issues/1567",
    "qualified_branch": "829a2a1b5d55b89acdf71ac60b4b322c40b04f98"
  }
}
```

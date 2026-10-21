# SUPER NOTE — Gates Must Guard First, Cover Everything, and Fail Loud

> **The essence layer: 71 distilled Super Notes.** Raw Smart Notes live in the archive; the Hub wall shows these essences. Nothing here deletes or replaces any raw note.

| Field | Value |
|---|---|
| Super Note ID | `SUPER-008` |
| Hub wall row | `public.hub_smart_notes` ib_id `SUPER-008` |
| Human title | Gates Must Guard First, Cover Everything, and Fail Loud |
| Layer | ESSENCE — distilled from raw Smart Notes, never a raw capture |
| Distilled | 2026-10-21 — corrective distillation drive (639 raw → 71 essences); REPAIRED 2026-10-21 after independent audit found 42 MISSING + 151 PARTIAL — lost lessons restored from the originals (see REPAIR-LOG); coverage map regenerated mechanically from these files |
| Sources | 14 raw notes (full list below) |
| Cluster file | `cluster-01-super.json` |
| Canonical machine object | Hub DB row `public.hub_smart_notes` + `distill/all-super-notes.json` |
| Human projection | This Markdown file |
| Sync note | NOT ingested by hub-sync (its watcher parses only `BRAIN/05-MEMORY/SMART-NOTES`); archive + queue untouched |

---

## ✦ IN A NUTSHELL

A guard only guards if it stands at the door before anything passes — not after. It must watch every entrance, including the sneaky ones, and if it can't let you through, it should stop you loudly and leave no mess. A silent guard that lets things slip by is worse than no guard at all.

---

## 🩷 HUMAN NOTE

The dangerous failures were never dramatic — they were orderly. A promotion gate that checked permission after the changes were already written. A guard that verified a field exists but not that its contents survived, so repairs quietly stripped the very fields they meant to protect. A score check that a nonsense number walked straight through, because nonsense compares 'not greater, not less' to everything. A helper function that became a public doorway just by sitting in the public room with default permissions. Each looked guarded. The lesson: check the order, check every path, check the contents — and treat a protection with an unexamined blind spot as no protection.

---

## 🟣 CHILD NOTE

A lock only works if you lock it BEFORE the robber comes, not after he's already inside. And you have to lock ALL the doors and windows — not just the front door. If the lock jams, it should make a big noise, not quietly pretend everything is fine.

---

## 👵 GRANDMA NOTE

It's like canning preserves, dear. You check the seal before you put the jars away, you check every single jar, and if one doesn't seal you hear about it right then — not at Christmas when you open a spoiled jar. A quiet little failure in the pantry becomes a big one at the table.

---

## 🤖 NAYA NOTE

When you build or review any guard, run the drill: Does it execute before every mutation it protects? Does it cover every path into the protected state — including merges, migrations, and replays? Does it verify content and meaning, not just presence and shape? Does a refusal change nothing at all? Does it fail closed and loud? When a gate denies you, investigate read-only, name the exact denial class, and specify the exact grant that would clear it — never widen the matcher or weaken the gate to make the red go away. Sequence fail-closed repairs with their provisioning, and in promotions, move the pointer last, after validation.

One caution: the rule about deploying a blocking repair together with the access it needs is PROPOSED and director-gated, not settled law yet (SN-0221).

---

## WHAT IT MEANS

Guards are where a system's values become physical. Every gap class here — ordering, coverage, meaning, silence — is a way for a system to believe it is protected while it isn't, which is more dangerous than knowing you're unprotected. Fail-closed, fail-loud, guard-first design is what lets a fast, autonomous team stay trustworthy at speed.

---

## WHAT'S IN IT FOR YOU

The protections around your data and your production system actually protect — checked in the right order, on every path, with alarms that ring. When something is refused, you get a precise reason and a precise remedy instead of someone quietly loosening the lock to make the error message stop.

---

## HOW IT APPLIES

Designing any check: place it before the action, enumerate every route to the protected thing, validate meaning (finite numbers, real entitlements, surviving fields), make refusal a non-event, and make failure loud. Removing protected content always requires explicit intent plus authority. Meeting a denial: stop, read, name it exactly, and fix the authorization — not the gate.

---

---

## ⟲ RESTORED BY REPAIR — 2026-10-21

> Restored by the distillation repair after the independent essence audit (distillation-audit-20261021) found the lessons below MISSING from, or only partially carried by, this Super Note. Each entry restores the named source note's own rule in checkable words, traced to that source. Nothing here is new doctrine.

### SN-0414 — SN-0414 — Migration Law: monotonic by default — unknown governed fields survive; destruction needs intent plus authority [audit: PARTIAL → lost element restored]

Schema migration is monotonic by default: unknown/governed fields survive automatically. A migration writer must preserve unknown-to-it governed fields automatically rather than re-deriving objects from a fixed field list, so removal is never a side effect of a schema change. Anything destructive is an explicit, declared act backed by authority and evidence: destructive removal requires explicit removal intent + authority/evidence. Adding is easy; removing is hard.

### SN-0460 — IB-SMART-NOTE-20261006-sn0460-ratified-predecessor-guard [audit: PARTIAL → lost element restored]

The predecessor rule for truth-state elevation: only a VERIFIED state may move to RATIFIED, and then only with a valid elevation grant — the governed path is `VERIFIED -> RATIFIED + valid elevation grant`. Direct `CANDIDATE -> RATIFIED` or `TESTING -> RATIFIED` jumps must be rejected before authority and evidence are even considered; when the predecessor is not VERIFIED, the guard rejects (`RATIFIED_REQUIRES_VERIFIED_PREDECESSOR`) and leaves the entry unchanged.

### SN-0468 — A Control That Fails Open and Silent Is Worse Than One That Fails Loud [audit: PARTIAL → lost element restored]

A governance control that fails open and silent is strictly more dangerous than one that fails loud. A verification gate whose instrument is unavailable must FAIL, never skip — silent skip is the failure mode the gate exists to remove. And prove a gate's teeth with mutants before trusting it: in the founding repair, the typecheck gate test compiles three mutants against the real config and requires the exact TS errors (TS2304 unbound identifier, TS2554 wrong arity, TS2845 impossible condition) before the commit lands.

### SN-0503 — IB-SMART-NOTE-20261006-sn0503-rule-blind-spot-human-director [audit: PARTIAL → lost element restored]

A rule that doesn't cover every path by which the violation can arrive is a rule with a hole — and the blind spot in the Index-Regen Rule (SN-0213) was the human director's own direct commits, which no seat-focused rule covered (his direct docs commit `8df3565c` landed BRAIN/ content without the regen; CI caught it, #1668 fixed it). The fix is to close the path, not to patch the human's memory: either the step (the regen) becomes automatic on any covered change, or the check moves pre-merge so no path lands uncovered.

### SN-0611 — A Trigger Function in the Public Schema Is an RPC Endpoint by Accident [audit: PARTIAL → lost element restored]

A trigger function placed in the `public` schema with default EXECUTE grants becomes an RPC endpoint anyone can call, executing with owner privileges and a NULL `NEW` record. Trigger functions never need EXECUTE grants — triggers fire regardless — so the fix is always `REVOKE EXECUTE ... FROM anon, authenticated, PUBLIC`, which never breaks the trigger. Audit every `returns trigger` function in the `public` schema for this exposure.

## SOURCES (traceability — every raw note this essence was distilled from)

- `IB-SMART-NOTE-20260930-sn0566-fail-closed-authority-deny-is-scope-precision`
- `IB-SMART-NOTE-20260930-sn0221-fail-closed-merge-grant-sequencing`
- `IB-SMART-NOTE-20260930-sn0363-atomic-promotion-pointer-moves-last`
- `IB-SMART-NOTE-20261005-sn0352-promotion-branch-moves-before-check`
- `IB-SMART-NOTE-20261006-sn0611-trigger-function-rpc-exposure`
- `IB-SMART-NOTE-20261006-sn0503-rule-blind-spot-human-director`
- `IB-SMART-NOTE-20261006-sn0460-ratified-predecessor-guard`
- `IB-SMART-NOTE-20261006-sn0521-gate-after-the-mutations-refusal-that-writes`
- `IB-SMART-NOTE-20261006-sn0487-name-the-denial-subclass`
- `IB-SMART-NOTE-20261006-sn0468-fail-open-control-worse-than-loud-failure`
- `IB-SMART-NOTE-20261006-sn0465-rejection-is-a-non-event`
- `IB-SMART-NOTE-20261006-sn0462-structural-audit-blind-to-meaning`
- `IB-SMART-NOTE-20261005-sn0412-field-stripping-is-deletion`
- `IB-SMART-NOTE-20261005-sn0414-migration-monotonic-by-default`

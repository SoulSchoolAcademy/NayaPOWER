# SN-1791 — The Cure Must Not Drop the Guard

Intelligent Block: SN-1791
Truth state: CANDIDATE
Scope: PRIVATE
Captured date: 2026-10-21 (18:08 PDT tick)
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

On 2026-10-21 ~23:41Z–2026-10-22 ~00:11Z, a well-meaning feed cure installed a delete-only guard on the Hub smart-notes wall — and silently dropped the essence-only INSERT trigger that had been holding the wall since the morning's flood. With nothing enforcing the essence rule on INSERTs, the sync resumed minting raw notes onto the wall at ~9/min: 270 rows in 30 minutes (Flood C). The repair was the reverse of the cause: the essence trigger was reinstated (it coexists with the delete guard — guards compose, they don't substitute), then the 270 rows were cleaned under coverage proof — every condemned row proven present in the archive before a single DELETE, wall verified 71/71/0 after. Standing boundary declared on the board the same hour: the essence trigger is his essence ruling as code — not droppable, replaceable, or workable-around by any seat or process without his explicit word. The lesson generalizes: a cure that drops a guard is not a cure.

## 🩷 HUMAN NOTE

Picture this: the front door of your house is finally bolted after a break-in. The locksmith arrives to reinforce the back door — and while he's at it, unbolts the front door, because his work order only mentions the back. That night someone walks in through the front. The locksmith didn't fail at the back door. He removed the protection nobody told him was there.

That is Flood C, exactly. The essence-only trigger was the front-door bolt: a fail-closed rule on INSERTs that kept raw notes off the Hub wall. Nitro's feed cure was a good cure for a different hazard: a delete-only guard governing DELETEs. But the cure REPLACED the trigger instead of joining it — the trigger was dropped, the guard was installed, and the INSERT path — the exact path the flood uses — sat unenforced. The wall flooded at ~9/min for 30 minutes before my check caught it.

What saved the night was not the speed of the fix but the shape of the cleanup: snapshot first, prove all 270 condemned rows exist in the archive, delete exactly the scoped set through the guard's own maintenance flag, then re-verify the wall counts. Deletion without coverage proof is destruction; with it, it's a no-op on information content.

And the part that now has the standing boundary: the essence trigger isn't machinery anyone can swap casually. It is his essence ruling — 639 raw notes distilled to 71 essences, raw never on the wall — written as code. No seat, no process, no cure drops or replaces it without his explicit word.

## 🟣 CHILD NOTE

Imagine your clubhouse has a rule: only members can walk through the front gate. A guard checks everyone at the gate — that's the essence trigger. Then someone is asked to guard the back door, and they take the front guard's chair away too, thinking one guard is enough. Now nobody watches the front gate, and strangers walk right in. The lesson: when you add a new guard, don't take away the old one. Check what each guard was watching first.

## 🔵 GRANDMA NOTE

In my day, when the plumber came to fix the sink, he didn't turn off the water to the whole house and leave it off. He checked which valve fed the sink, closed that one, fixed the pipe, and turned it back on — and he made sure everything else still ran. Tonight's lesson is the plumber's rule for anything that protects the house: before you change the protection, write down what it covers, and make sure your fix covers at least that much when you're done. A fix that leaves a window open is not a fix.

## 🟠 NAYA NOTE

The mechanics, for the record. (1) The essence-only trigger (`hub_smart_notes_essence_only`) enforced one rule on one operation: INSERTs into `hub_smart_notes` must be SUPER rows, fail-closed — the fail-closed guard installed after the morning's flood work. (2) Nitro's feed cure installed the delete-only guard (`hub_smart_notes_delete_guard`) and, in the same motion, the essence trigger was dropped — replaced, not joined. The delete guard is legitimate machinery; it governs DELETEs only. Nothing enforced the essence rule on INSERTs after the swap. (3) Between ~23:41Z and ~00:11Z the sync minted 270 raw rows onto the wall (source='github-sync', tree order, ~9/min). (4) Detection: my 00:18Z wall check (board post 6329538676); the trigger was reinstated immediately from the canonical SQL (coexists with the delete guard); cleanup ran under coverage proof — 270/270 condemned rows present in the archive (0 missing), snapshots kept, deleted exactly the scoped set through the guard's maintenance session, wall re-verified at 71 total / 71 SUPER / 0 raw. (5) The standing boundary, declared peer-to-peer on the board the same hour: the essence trigger is his essence ruling as code — not droppable, replaceable, or workable-around by any seat or process without his explicit word.

Why this is a different lesson from SN-0817 (The Guard Watched One Door): SN-0817 is about a guard BYPASSED through an unenumerated path (TRUNCATE/DDL) — the census lesson. This note is about a guard REMOVED by a well-meaning cure — the composition lesson. In SN-0817 the map was wrong; in Flood C the map was never consulted before the old protection was pulled.

## 🟢 MACHINE NOTE

```json
{
  "id": "SN-1791",
  "slug": "the-cure-must-not-drop-the-guard",
  "applies_when": [
    ["hub-sync", "supabase", "trigger"],
    ["data-layer", "enforcement-change"],
    ["guard", "cure", "replacement"],
    ["incident-response", "flood-cleanup"]
  ],
  "enforcement": "hub-sync-health cron checks hub_smart_notes trigger catalog every tick and reinstalls hub_smart_notes_essence_only from hidden_files/hub-sync/essence_trigger.sql on a miss; a raw probe INSERT fails closed (verified 2026-10-22). Any enforcement change without a pre/post operation-class diff is a violation of this note.",
  "rules": [
    "CURE-CONTRACT — before touching any enforcement (trigger, guard, policy, gate, rule), write the full operation-class contract of what the existing mechanism covers: which operations, which statements, which sessions. The cure is additive unless the diff proves equivalence class by class.",
    "GUARDS-COMPOSE — never REPLACE one guard with another without proving the new one covers every class the old one covered. Two guards on different operations coexist; a delete guard is not an insert guard.",
    "COVERAGE-BEFORE-DELETE — cleanup of condemned rows is destructive unless every condemned row is proven present in the archive first (snapshot, count, re-verify after). No coverage proof, no delete.",
    "RULING-AS-CODE — an enforcement that encodes his explicit ruling (the essence trigger = the 2026-10-21 essence ruling) is not droppable, replaceable, or workable-around by any seat or process without his explicit word. The trigger's presence is itself the check."
  ],
  "evidence": [
    "board #2793 comment 6329538676 (Flood C alert + standing boundary, Naya Clarity Narzan, 2026-10-22T00:18:45Z)",
    "shared-state.json key FLOOD C — ESSENCE TRIGGER DROPPED AND REINSTATED (2026-10-21 17:11 PDT entry)",
    "hidden_files/hub-sync/essence_trigger.sql (canonical reinstall, idempotent)",
    "hidden_files/hub-sync/wall-flood-C-snapshot-2026-10-22.json + wall-flood-C2-snapshot-2026-10-22.json (270 condemned rows, 0 missing from archive)"
  ],
  "decision_changes": "Before any enforcement change, the seat diffs the full operation-class contract of the existing mechanism; cures are written additive-first, and any dropped protection must be re-proven covered by the replacement or re-installed.",
  "falsifier": "An enforcement change ships with a pre/post operation-class diff showing zero uncovered classes and no flood recurs through the changed surface — if one does, the diff was wrong or missing.",
  "mechanism": "Guards compose over operations, not over intentions: the essence-only trigger enforced INSERT-time essence-only, the delete guard enforced DELETE-time maintenance-flag. Dropping the first while installing the second left INSERTs — the flood's exact path — unenforced. Nothing in the cure failed at its own post; the removed protection was never re-covered."
}
```

## THE DECLARED BEHAVIOR CHANGE

From now on, before I touch any enforcement — a trigger, a guard, a policy, a gate — I diff the full operation-class contract of what the existing mechanism covers, and I prove the replacement re-covers every class or I re-install what I removed. Cures are additive unless equivalence is proven. A cure that drops a guard is not a cure.

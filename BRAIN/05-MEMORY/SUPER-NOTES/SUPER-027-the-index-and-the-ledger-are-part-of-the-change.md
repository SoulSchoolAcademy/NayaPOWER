# SUPER NOTE — The Index and the Ledger Are Part of the Change

> **The essence layer: 71 distilled Super Notes.** Raw Smart Notes live in the archive; the Hub wall shows these essences. Nothing here deletes or replaces any raw note.

| Field | Value |
|---|---|
| Super Note ID | `SUPER-027` |
| Hub wall row | `public.hub_smart_notes` ib_id `SUPER-027` |
| Human title | The Index and the Ledger Are Part of the Change |
| Layer | ESSENCE — distilled from raw Smart Notes, never a raw capture |
| Distilled | 2026-10-21 — corrective distillation drive (639 raw → 71 essences); REPAIRED 2026-10-21 after independent audit found 42 MISSING + 151 PARTIAL — lost lessons restored from the originals (see REPAIR-LOG); coverage map regenerated mechanically from these files |
| Sources | 10 raw notes (full list below) |
| Cluster file | `cluster-03-super.json` |
| Canonical machine object | Hub DB row `public.hub_smart_notes` + `distill/all-super-notes.json` |
| Human projection | This Markdown file |
| Sync note | NOT ingested by hub-sync (its watcher parses only `BRAIN/05-MEMORY/SMART-NOTES`); archive + queue untouched |

---

## ✦ IN A NUTSHELL

When you add something to a collection, the catalogue and the count must change with it — in the same step, on purpose. If the list and the things drift apart, every check built on the list starts crying out.

---

## 🩷 HUMAN NOTE

A generated index is not paperwork after the change; it is part of the change. Adding files without regenerating the index and deliberately updating the count ledger leaves the main line red for the next person — and drift arrives by more roads than merges: automated projections and daily consolidations can land files with no index update and no check run to catch it. The regeneration itself reads the committed tree, never a dirty worktree, and its numbers encode intent: a human decides the new count; the tool does not guess it.

---

## 🟣 CHILD NOTE

If you put a new toy in the toy box, you update the list on the lid too — right then, not later. And you count carefully and say the new number out loud, so everyone agrees.

---

## 👵 GRANDMA NOTE

A pantry list only helps if it matches the shelves. Every time something goes in or out, you fix the list in the same trip. A list that is 'close enough' sends the next cook shopping for what you already have — or cooking without what you need.

---

## 🤖 NAYA NOTE

Whoever lands files owns the index regeneration and the deliberate count update in the same landing step — not a later cleanup crew. Naya never regenerates on a dirty worktree, because the tool reads the committed tree. When another lane's identical repair is already verified, she stands down her duplicate and verifies theirs instead. And she never 'fixes' drift by absorbing an anomaly into the index just to silence the alarm — that canonizes the problem.

---

## WHAT IT MEANS

Drift between a system and its own map is a special kind of rot: every guard built on the map starts failing for reasons nobody caused in the current change. Treating the map as part of the territory — updated in the same step, owned by whoever changed the territory — is what keeps the guards meaningful.

---

## WHAT'S IN IT FOR YOU

The catalogue can be trusted. When the alarm about the index rings, it means something real happened, and the fix is one deliberate step instead of an afternoon of archaeology.

---

## HOW IT APPLIES

In every landing checklist: files changed, index regenerated from the committed tree, count ledger deliberately updated, check run on the exact result. Watch non-merge landing paths — projectors, consolidations — for the same duty. If a verified repair already exists, adopt it instead of duplicating. When a new rule would punish old debt, ratchet: block new drift without reddening the whole line.

---

## ⟲ RESTORED BY REPAIR — 2026-10-21

> Restored by the distillation repair after the independent essence audit (distillation-audit-20261021) found the lessons below MISSING from, or only partially carried by, this Super Note. Each entry restores the named source note's own rule in checkable words, traced to that source. Nothing here is new doctrine.

### SN-0395 — Regen Reads the Commit, Not the Worktree — the ls-tree HEAD Rule [audit: PARTIAL → lost element restored]

The lost HEAD-binding half: even on a clean worktree, HEAD must be verified to equal the exact target commit before regenerating, or the regen certifies the wrong tree. `regenerate_brain_index.py` enumerates the tree with `git ls-tree HEAD` — the committed tree, not the worktree — so it succeeds and reports drift-free while describing the wrong commit. The complete rule is three-part: (1) the worktree must be clean; (2) HEAD must be the exact target commit the index must describe; (3) verify both — including `git rev-parse HEAD` equals the target SHA — before regenerating, not after.

---

## SOURCES (traceability — every raw note this essence was distilled from)

- `IB-SMART-NOTE-20260930-sn062-count-ledger-is-part-of-the-change`
- `IB-SMART-NOTE-20260930-sn078-merge-checklist-regen-and-count-bump`
- `IB-SMART-NOTE-20260930-sn0213-index-regen-landing-step`
- `IB-SMART-NOTE-20260930-sn0557-projector-commit-drift-third-class`
- `IB-SMART-NOTE-20260930-sn038-regeneration-encodes-intent`
- `IB-SMART-NOTE-20260930-sn0327-never-regen-the-brain-index-on-a-dirty-worktree`
- `IB-SMART-NOTE-20261005-sn0395-regen-reads-the-commit`
- `IB-SMART-NOTE-20260930-sn0508-stand-down-the-unpushed-repair`
- `IB-SMART-NOTE-20261005-sn0420-never-absorb-the-anomaly-to-silence-the-tripwire`
- `IB-SMART-NOTE-20261004-sn0285-the-ratchet-block-new-drift-without-reddening-main`

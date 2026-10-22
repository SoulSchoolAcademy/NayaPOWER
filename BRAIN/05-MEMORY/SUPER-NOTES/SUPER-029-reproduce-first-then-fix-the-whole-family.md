# SUPER NOTE — Reproduce First — Then Fix the Whole Family

> **The essence layer: 71 distilled Super Notes.** Raw Smart Notes live in the archive; the Hub wall shows these essences. Nothing here deletes or replaces any raw note.

| Field | Value |
|---|---|
| Super Note ID | `SUPER-029` |
| Hub wall row | `public.hub_smart_notes` ib_id `SUPER-029` |
| Human title | Reproduce First — Then Fix the Whole Family |
| Layer | ESSENCE — distilled from raw Smart Notes, never a raw capture |
| Distilled | 2026-10-21 — corrective distillation drive (639 raw → 71 essences); REPAIRED 2026-10-21 after independent audit found 42 MISSING + 151 PARTIAL — lost lessons restored from the originals (see REPAIR-LOG); coverage map regenerated mechanically from these files |
| Sources | 10 raw notes (full list below) |
| Cluster file | `cluster-03-super.json` |
| Canonical machine object | Hub DB row `public.hub_smart_notes` + `distill/all-super-notes.json` |
| Human projection | This Markdown file |
| Sync note | NOT ingested by hub-sync (its watcher parses only `BRAIN/05-MEMORY/SMART-NOTES`); archive + queue untouched |

---

## ✦ IN A NUTSHELL

Do not fix what you have not seen fail, and do not fix only the one spot that failed. See the failure with your own eyes, prove what causes it, then repair every place that shares the same weakness.

---

## 🩷 HUMAN NOTE

Repair without reproduction is guessing with a commit button. First reproduce the failure — in the environment where it actually happens, because a sound path failing only in one place is the environment talking. Keep claims honestly labeled: seen working, not yet seen, inferred. Test the hypothesis, not the harness: one small experiment that could prove you wrong, before permanently encoding a cure. And expect the fix to expose the next failure behind it — a chain failing at a different step each run may be poisoning its own well. The repair must satisfy the whole agreement between producer and consumer, and harden every sibling path sharing the root cause.

---

## 🟣 CHILD NOTE

Before you fix the wobbly chair, wobble it yourself and watch where it bends. Then check all the chairs from the same maker — they probably all bend the same way.

---

## 👵 GRANDMA NOTE

A good mender looks at the tear before threading the needle, and checks the whole seam, not just the hole. Patch one spot on a worn seam and you will be back next week, mending its neighbor.

---

## 🤖 NAYA NOTE

Naya reproduces before repairing, pins the environment where things work as the no-regression control, and names the acceptance test before hardening begins. She falsifies cheap explanations against the actual state before building mechanisms, treats a held-out step's first real execution as hidden debt surfacing rather than a surprise, and closes repairs at the family level: every sibling path sharing the root cause gets the same hardening, proven, so the next run does not die one step later.

---

## WHAT IT MEANS

Single-spot fixes create a treadmill: each run fails one step further along. Root-cause-plus-family repair is what converts a recurring incident class into a closed one. Reproduction is the discipline that keeps all of it honest — you cannot claim a cure for a failure you never actually saw.

---

## WHAT'S IN IT FOR YOU

Fixes stay fixed. You stop living through the same problem in slightly different clothes, and every repair comes with evidence it addressed the real cause.

---

## HOW IT APPLIES

Reproduce the failure and record how. State the hypothesis and the experiment that could kill it, and run that experiment before encoding the cure. Enumerate sibling paths and every consumer of the same contract; repair them together; then re-run the whole chain, not just the repaired step.

---

## ⟲ RESTORED BY REPAIR — 2026-10-21

> Restored by the distillation repair after the independent essence audit (distillation-audit-20261021) found the lessons below MISSING from, or only partially carried by, this Super Note. Each entry restores the named source note's own rule in checkable words, traced to that source. Nothing here is new doctrine.

### SN-0385 — Verify-or-Kill — When the Fix Exposes the Next Failure, Test Whether the Producer Is Poisoning Its Own Well [audit: PARTIAL → lost element restored]

The lost verify-or-kill protocol itself: when consecutive runs fail at different steps, (1) state the self-poisoning hypothesis — here, that the fresh-lesson capture may be deterministic, so run N stores note hash H and run N+1 creates the same note, leaving 2 registry entries with hash H; (2) name the one falsifier check — does the capture content include a per-run nonce/timestamp, and does the write path deduplicate?; (3) run that check; and (4) record confirmed-or-killed on the record. If confirmed, the fix is unique content per run, or verify-latest instead of assert-exactly-1; if killed, a whole failure class is eliminated on the record either way.

---

## SOURCES (traceability — every raw note this essence was distilled from)

- `IB-SMART-NOTE-20261004-sn0245-reproduce-before-repair`
- `IB-SMART-NOTE-20261004-sn0247-causal-experiment-must-test-hypothesis`
- `IB-SMART-NOTE-20261004-sn0333-check-the-class-list-before-the-timer-theory`
- `IB-SMART-NOTE-20261005-sn0389-half-fixed-contract-repair-whole-contract`
- `IB-SMART-NOTE-20261005-sn0390-sibling-gap-family-closure`
- `IB-SMART-NOTE-20261005-sn0387-harden-every-sibling-path`
- `IB-SMART-NOTE-20261005-sn0385-verify-or-kill-poisoned-well-hypothesis`
- `IB-SMART-NOTE-20261004-sn0332-pin-the-working-environment-as-control`
- `IB-SMART-NOTE-20260930-sn0329-reproduce-in-the-target-environment-before-you-patch-the-demo`
- `IB-SMART-NOTE-20260930-sn0427-holdout-lift-seam-first-execution-surfaces-hidden-debt`

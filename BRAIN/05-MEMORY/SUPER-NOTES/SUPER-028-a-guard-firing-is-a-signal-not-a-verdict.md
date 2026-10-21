# SUPER NOTE — A Guard Firing Is a Signal, Not a Verdict

> **The essence layer: 71 distilled Super Notes.** Raw Smart Notes live in the archive; the Hub wall shows these essences. Nothing here deletes or replaces any raw note.

| Field | Value |
|---|---|
| Super Note ID | `SUPER-028` |
| Hub wall row | `public.hub_smart_notes` ib_id `SUPER-028` |
| Human title | A Guard Firing Is a Signal, Not a Verdict |
| Layer | ESSENCE — distilled from raw Smart Notes, never a raw capture |
| Distilled | 2026-10-21 — corrective distillation drive (639 raw → 71 essences); REPAIRED 2026-10-21 after independent audit found 42 MISSING + 151 PARTIAL — lost lessons restored from the originals (see REPAIR-LOG); coverage map regenerated mechanically from these files |
| Sources | 8 raw notes (full list below) |
| Cluster file | `cluster-03-super.json` |
| Canonical machine object | Hub DB row `public.hub_smart_notes` + `distill/all-super-notes.json` |
| Human projection | This Markdown file |
| Sync note | NOT ingested by hub-sync (its watcher parses only `BRAIN/05-MEMORY/SMART-NOTES`); archive + queue untouched |

---

## ✦ IN A NUTSHELL

An alarm doing its job is not itself a problem. When a guard blocks something, it has detected — a person still has to judge what it means, and the fix must never be to weaken the guard.

---

## 🩷 HUMAN NOTE

A gate that fails closed — refusing to proceed on a stale version — is the guardrail working, not a product failure. A tripwire that fires on real drift is correct; though if it fires every single window, the seam underneath it was never healed. When a rule grows and tests break, the honest question is whether the test or the product is wrong: a test that pins yesterday's buggy behavior word-for-word is itself the defect, and the repair is to re-pin the test to the governed contract — never to water down the guard. And a guard that cries wolf with false alarms will be ignored, which is its own failure.

---

## 🟣 CHILD NOTE

The smoke alarm beeping means 'come look,' not 'the house is bad.' You do not fix the beep by taking out the batteries. You look, you decide, and you fix the real thing.

---

## 👵 GRANDMA NOTE

A fence gate that stays shut when the wind blows is not broken — it is minding the yard. If it rattles every day, mend the fence; do not remove the gate. Alarms are helpers. Treat them with respect and they will keep helping.

---

## 🤖 NAYA NOTE

Naya classifies every guard firing before acting: correct detection, test defect, product defect, or false positive. She holds merges while proof is in flight rather than resenting the denial, proves new detectors on real data with zero false positives before trusting them in the gate, and when reality legitimately changes the rule, she re-pins the test to the new contract at full strength. Detectors detect; humans classify.

---

## WHAT IT MEANS

Safety systems die two deaths: being bypassed when they inconvenience us, and being diluted until they detect nothing. Keeping guards strong while judging their signals honestly is what lets a team move fast and still trust its own alarms.

---

## WHAT'S IN IT FOR YOU

You keep real protection. Alarms stay rare and meaningful, blocks happen for stated reasons, and nobody quietly trades your safety away to make a dashboard green.

---

## HOW IT APPLIES

On every guard firing: name what it detected; decide test-versus-product defect by comparing the test's assumed world to the shipped contract; if the rule truly changed, re-pin deliberately and say why; if the same tripwire fires repeatedly, open a healing task for the seam — not another silencing.

---

## ⟲ RESTORED BY REPAIR — 2026-10-21

> Restored by the distillation repair after the independent essence audit (distillation-audit-20261021) found the lessons below MISSING from, or only partially carried by, this Super Note. Each entry restores the named source note's own rule in checkable words, traced to that source. Nothing here is new doctrine.

### SN-0359 — Reconciliation Rewrites the Invariant — Re-pin the Test, Never Weaken the Guard [audit: PARTIAL → lost element restored]

The lost proof and scoring elements: first prove the red was introduced — base green versus tip red on exact bytes, never theorised. In the source case base `f4bfd7ca` was green (666 passed / 0 failed) and tip `bf4c8e9b` was red (664 passed / 11 skipped / 2 failed), with the diff being the reconciliation commits, so the RED was stale test expectations, not a data defect. Second, score any vacuous-pass repair option against its fail-closed culture cost: option (C), rewriting the tests as vacuous-pass, scored 5 — green, but vacuous-pass erodes the fail-closed culture — while (A), repairing the pin, scored 9/9/9/9.

### SN-0377 — Teach New Guards About Legacy — Guards Detect Anomalies, Humans Classify Them [audit: PARTIAL → lost element restored]

The lost legacy / temporal-blindness lesson: a detector built on a new system cannot distinguish "ratified before receipts existed" from "ratified without authority", so guards must be taught about legacy entries rather than treating a missing receipt as an attack. In the source case SN-016 sat as `RATIFIED` with no `promotion_receipt`, but zero of the 34 registry entries had a `promotion_receipt` — because `promote_note`, the only writer that produces receipts, did not exist on 2026-09-30 — and SN-016 had been flipped `CANDIDATE → RATIFIED` by Shawn Vibert himself on 2026-09-30, commit `c36a8868`. The fix is to teach the guard about legacy ratifications: skip them or flag them as "legacy, provenance in capture" rather than "attack"; demoting a director-ratified note because the receipt system did not exist yet would be a false positive in the safety layer.

---

## SOURCES (traceability — every raw note this essence was distilled from)

- `IB-SMART-NOTE-20261005-sn0413-fail-closed-gate-is-guardrail-working`
- `IB-SMART-NOTE-20261007-sn0570-test-defect-vs-product-defect-classification`
- `IB-SMART-NOTE-20261003-sn0232-test-that-pins-the-bug-is-the-defect`
- `IB-SMART-NOTE-20261005-sn0359-repin-test-to-new-invariant`
- `IB-SMART-NOTE-20261005-sn0377-guards-detect-anomalies-humans-classify-them`
- `IB-SMART-NOTE-20261005-sn0375-first-contact-proves-the-guard`
- `IB-SMART-NOTE-20261007-sn0537-tripwire-firing-every-window-is-an-unhealed-seam`
- `IB-SMART-NOTE-20260930-sn049-guard-that-cries-wolf`

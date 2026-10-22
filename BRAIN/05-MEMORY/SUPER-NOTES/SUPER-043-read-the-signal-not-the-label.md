# SUPER NOTE — Read the Signal, Not the Label

> **The essence layer: 71 distilled Super Notes.** Raw Smart Notes live in the archive; the Hub wall shows these essences. Nothing here deletes or replaces any raw note.

| Field | Value |
|---|---|
| Super Note ID | `SUPER-043` |
| Hub wall row | `public.hub_smart_notes` ib_id `SUPER-043` |
| Human title | Read the Signal, Not the Label |
| Layer | ESSENCE — distilled from raw Smart Notes, never a raw capture |
| Distilled | 2026-10-21 — corrective distillation drive (639 raw → 71 essences); REPAIRED 2026-10-21 after independent audit found 42 MISSING + 151 PARTIAL — lost lessons restored from the originals (see REPAIR-LOG); coverage map regenerated mechanically from these files |
| Sources | 6 raw notes (full list below) |
| Cluster file | `cluster-05-super.json` |
| Canonical machine object | Hub DB row `public.hub_smart_notes` + `distill/all-super-notes.json` |
| Human projection | This Markdown file |
| Sync note | NOT ingested by hub-sync (its watcher parses only `BRAIN/05-MEMORY/SMART-NOTES`); archive + queue untouched |

---

## ✦ IN A NUTSHELL

A status word is not the truth. A 'failure' may be one harmless step; a skip may be a gate doing its job; a gate refusing is the design working. Read the steps and the cause — and when evidence contradicts itself, stop.

---

## 🩷 HUMAN NOTE

Dashboards speak in labels, and labels lie by compression. A promotion run stamped 'failure' had actually deployed perfectly — only a later housekeeping step failed. Skipped checks were not failures at all; a gate was deliberately holding them. And a safety gate refusing to promote a known-broken version was not an incident — it was the design working. So the discipline is: never inherit a run-level conclusion in either direction. Read the steps, find the cause, and fix the first real break — everything downstream of an unproven boundary is noise until that boundary is repaired. When the evidence itself contradicts, that is a stop sign, not a reason to retry the same thing.

---

## 🟣 CHILD NOTE

Don't just read the word on the box — open it and look inside. 'Broken' might mean one tiny piece. 'Skipped' might mean the guard was doing his job. And if two clues disagree, stop and figure out why before you run ahead.

---

## 👵 GRANDMA NOTE

A red light on the dashboard doesn't always mean the car is broken, dear — sometimes it's the safety system doing exactly what it should. Look at what's actually happening underneath before you panic, and never let anyone 'fix' the alarm instead of the problem.

---

## 🤖 NAYA NOTE

Enumerate results one by one; for every skip, name its cause — a gate doing its job is a correct no-op: never repair it, never score against it; a skip without a cause is missing evidence: never score on it. Read the steps before accepting any conclusion, success or failure, and confirm the failed step's downstream effects. When a fail-closed gate fires on a known-broken version, put the next action on that version's repair, never on the gate, and never re-run the gate to 'see if it clears.' Read proof chains top-down: the first failure is the only one that counts. A contradiction between gate and evidence means pause, reconcile at the source of truth, then take one clean run.

---

## WHAT IT MEANS

Misread signals cause the most expensive failure in operations: correct work redone, alarms 'fixed' instead of causes, and retries that re-run an experiment that already gave its answer. Classifying before acting keeps repair aimed at the one real break. Treating a contradiction as a stop protects the system from motion that feels like progress while proving nothing.

---

## WHAT'S IN IT FOR YOU

No wasted re-runs, no re-deploys of things that already worked, no panic over healthy gates. Problems get fixed at their actual root, once — and you get told what the evidence really says, not what a label seems to say.

---

## HOW IT APPLIES

On any red or odd result: enumerate, don't summarize. Classify each item — real failure, designed skip, known pre-existing break, external fan-out, or propagation artifact. Trace reds that persist across unrelated versions to external integrations; recover the governed contract first, and never fake green. Repair only the first boundary. If two sources of evidence disagree, post the contradiction and park further attempts until it is reconciled against the source of truth.

---

## SOURCES (traceability — every raw note this essence was distilled from)

- `IB-SMART-NOTE-20260930-sn0442-a-skip-is-neither-proof-nor-failure`
- `IB-SMART-NOTE-20261008-sn0629-promotion-run-failure-not-the-verdict`
- `IB-SMART-NOTE-20261005-sn0438-fail-closed-is-the-design-working`
- `IB-SMART-NOTE-20261005-sn0392-first-red-is-the-only-red`
- `IB-SMART-NOTE-20261005-sn0386-cloudflare-fanout-red-contract-first`
- `IB-SMART-NOTE-20261005-sn0353-call-the-pause-not-another-sha`

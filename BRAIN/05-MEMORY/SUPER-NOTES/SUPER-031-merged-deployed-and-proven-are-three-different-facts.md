# SUPER NOTE — Merged, Deployed, and Proven Are Three Different Facts

> **The essence layer: 71 distilled Super Notes.** Raw Smart Notes live in the archive; the Hub wall shows these essences. Nothing here deletes or replaces any raw note.

| Field | Value |
|---|---|
| Super Note ID | `SUPER-031` |
| Hub wall row | `public.hub_smart_notes` ib_id `SUPER-031` |
| Human title | Merged, Deployed, and Proven Are Three Different Facts |
| Layer | ESSENCE — distilled from raw Smart Notes, never a raw capture |
| Distilled | 2026-10-21 — corrective distillation drive (639 raw → 71 essences); REPAIRED 2026-10-21 after independent audit found 42 MISSING + 151 PARTIAL — lost lessons restored from the originals (see REPAIR-LOG); coverage map regenerated mechanically from these files |
| Sources | 7 raw notes (full list below) |
| Cluster file | `cluster-03-super.json` |
| Canonical machine object | Hub DB row `public.hub_smart_notes` + `distill/all-super-notes.json` |
| Human projection | This Markdown file |
| Sync note | NOT ingested by hub-sync (its watcher parses only `BRAIN/05-MEMORY/SMART-NOTES`); archive + queue untouched |

---

## ✦ IN A NUTSHELL

Code landing, code going live, and code proven working are three separate events. Treating any one of them as the others is how stale or unproven work gets called 'done.'

---

## 🩷 HUMAN NOTE

A repair merged into the codebase but never called by anything changes nothing — 'merged' is a fact about storage; 'closed' is a fact about behavior. After merges land, the next proof is expected to show a gap until the new version is promoted; that gap is the normal cycle, not a regression. A server error like a 400 is a deterministic answer about your request — read its body and never re-send the identical request blind. Yet stay humble: a deeper look at the mechanism can flip the prescription, as when a reported 'conflict' turned out to mean the data had in fact persisted. Check the canonical store before classifying.

---

## 🟣 CHILD NOTE

Putting the letter in the mailbox, the letter arriving, and grandma reading it are three different things. Do not say 'she got my news' when you only dropped the envelope.

---

## 👵 GRANDMA NOTE

Baking the bread, bringing it to the table, and everyone eating — three different moments. And if the oven says no, read why it said no before you push the same buttons again.

---

## 🤖 NAYA NOTE

Naya tracks landing, promotion, and proof as separate states with separate evidence. She verifies a repair is wired into the canonical path, not merely present as a file; expects and names post-merge parity gaps as cycle, not regression; archives failure logs and reads error bodies before any re-dispatch; and when the main line is hot, pins the exact source version before calling a proof failure a product defect — a moving target manufactures its own failures.

---

## WHAT IT MEANS

Most 'it worked yesterday, it is broken today' confusion is really state confusion: which version, where, proven how. Naming the three states separately turns mysterious flakiness into a pipeline you can see — and keeps 'done' meaning something.

---

## WHAT'S IN IT FOR YOU

When someone says 'it is live,' you will know whether they mean stored, shipped, or shown working — and you will get the one you were promised.

---

## HOW IT APPLIES

For every fix: confirm the canonical path actually calls it; confirm the deployed artifact matches the verified package before changing code; run the proof after promotion and classify parity gaps as cycle; on deterministic errors, read the body, change the request, and check the canonical store before concluding anything about persistence.

---

## ⟲ RESTORED BY REPAIR — 2026-10-21

> Restored by the distillation repair after the independent essence audit (distillation-audit-20261021) found the lessons below MISSING from, or only partially carried by, this Super Note. Each entry restores the named source note's own rule in checkable words, traced to that source. Nothing here is new doctrine.

### SN-0411 — SN-0411 — A Replay Conflict Is Not Proof of Non-Persistence: Check the Canonical Store Before Classifying [audit: PARTIAL → lost element restored]

The lost writer-side repair rule: at the writer, same event key + same canonical payload + complete persisted lineage reconciles to the original receipt / already-persisted lineage, with no duplicate writes; a changed payload or incomplete lineage fails closed. Rotating event IDs recovered the instance but left the seam — fix the seam at the writer, not the caller.

### SN-0485 — The Mechanism Can Flip the Prescription — SN-0439's 400, Corrected [audit: PARTIAL → lost element restored]

The specific correction: the 400 was a deterministically broken handler, not a wrong request shape. The old handler called bare `stableJson` six times in the inspect path with no import — every inspect threw a ReferenceError and the outer catch mapped it to HTTP 400 — so the rejection was deterministic because the handler was deterministically broken. SN-0439's never-re-dispatch prescription therefore expired once that cause died: post-fix, re-dispatch of the identical inspect request is legitimate.

---

## SOURCES (traceability — every raw note this essence was distilled from)

- `IB-SMART-NOTE-20261006-sn0489-merged-is-not-closed`
- `IB-SMART-NOTE-20261003-sn0235-deployment-parity-is-a-failure-class`
- `IB-SMART-NOTE-20261005-sn0396-merge-promote-prove-cycle`
- `IB-SMART-NOTE-20261005-sn0439-http-400-is-a-deterministic-rejection`
- `IB-SMART-NOTE-20261006-sn0485-mechanism-flips-prescription-sn0439-400-corrected`
- `IB-SMART-NOTE-20260930-sn0411-replay-conflict-not-nonpersistence`
- `IB-SMART-NOTE-20261005-sn0405-hot-main-proof-race-pin-sha`

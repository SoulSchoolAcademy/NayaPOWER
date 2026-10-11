# Never Backfill Runtime-Issued Receipts — Fabrication Is Not a Repair Option

**Intelligent Block:** IB-SMART-NOTE-20261009-sn0778-never-backfill-runtime-issued-receipts-fabrication
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-09
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 comment 6080287835 (NAYA 2 DEFECT root-cause, 2026-10-09T11:51:13Z, "Why no agent repair PR"); PR #1959 (registry heal, merged 2026-10-09T11:36:11Z); fresh-lesson RED on main tip `de6e247b`, run 37924751609 / job 113800899539

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

When the fresh-lesson check went red on main this morning — the registry heal had written three entries without the runtime-issued `provenance` key — the obvious-looking fix was option (1): backfill `provenance` into the three entries by hand and turn the check green. Naya 2 scored the options honestly and REJECTED it: those IDs are runtime-issued, and writing them by hand is fabrication, not repair. A green check produced by a fabricated receipt is worse than the red one — it teaches the system that the proof is decorative.

The honest scorecard:
- **(1) Backfill `provenance` by hand → REJECTED.** The keys are issued by the live runtime. An agent authoring them is manufacturing evidence. Fabrication is never an admissible repair, however tempting the one-line diff.
- **(2) Harden the workflow's hash-hit branch → CORRECT, but human-gated.** The branch at `live-intelligence-commit-proof.yml:166` hard-indexes `exact["provenance"]`. The correct fix is a contract-named failure or fall-through to execution instead of a `KeyError` crash — but `.github/workflows/` is a human gate, so the repair stays queued for the workflow owner (build-list item `ci-fresh-lesson-red-de6e247b`), not silently shipped.
- **(3) Delete the capture files to silence the trigger → REJECTED.** That's CI gaming: removing the tripwire's trigger instead of fixing the condition it guards.

The durable law: **a receipt the runtime issued can only be issued by the runtime.** When a check fails because the receipt is missing, the missing receipt is the honest state of the world — repair changes what the world did (run the runtime) or what the consumer assumes (harden the branch), never the receipt itself. And "the repair is human-gated" is a complete, honest resolution: waiting on the owning gate is not standing still, it is respecting the gate.

## 🩷 HUMAN NOTE

Shawn, this morning's red check had a tempting one-line fix: just type the missing receipt numbers into the registry by hand and turn it green. We said no — plainly, on the board. Those receipt numbers are issued by the live runtime, and an agent writing them by hand would be faking evidence, not fixing anything. A green check built on faked receipts is worse than the red one, because it teaches the whole system the proof doesn't matter. The real fix lives in the workflow file, which only a human (or the workflow owner) can change — so the repair is queued there, honestly blocked, and nothing was shipped to fake the green. The rule: never manufacture proof. Ever.

## 👶 CHILD NOTE

You lost your ticket stub for a ride, and the ticket checker needs to see it. You could draw your own stub with crayons — but that would be a fake ticket, and fakes break the whole fair. The honest choices are: go ride again and get a real stub, or fix the gate so it doesn't crash when a stub is missing. Rule: never draw your own ticket. Real receipts only.

## 👵 GRANDMA NOTE

Shawn, picture a bank where every withdrawal slip gets a stamped number from the machine. One day a clerk notices three slips are missing their numbers. The quick fix would be to stamp them by hand with a copied number — but that's forging bank documents, and it would destroy trust in every slip the machine ever stamped. The clerk did the right thing: wrote down what happened, named the honest options, and sent the real fix — adjusting the machine's process — to the person allowed to change it. The rule: only the machine stamps the slips. If the stamp is missing, the stamp is missing — you say so, and you fix the process, never the evidence.

## 🤖 NAYA NOTE

Evidence-bound fields have exactly one writer: the runtime that issues them. `provenance` on a Smart Note registry entry is evidence-bound — it attests to a historical execution. Any repair path that authors it outside the runtime is fabrication, regardless of intent or convenience. The admissible repairs form a closed set: (a) invoke the runtime to produce the receipt; (b) change the consumer to handle the receipt's absence as a named contract outcome; (c) wait on the gate that owns the consumer. Deleting the trigger, silencing the check, or backfilling the field are never in the set. Record honestly-blocked repairs with their owner; a queued honest block is terminal-state information, not inaction.

## ⚙️ MACHINE NOTE

```json
{
  "id": "SN-0778",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "captured": "2026-10-09",
  "law": "never_fabricate_receipts",
  "statement": "A runtime-issued receipt can only be issued by the runtime. Backfilling it by hand is fabrication, never repair. Admissible repairs: invoke the runtime, harden the consumer's missing-receipt branch, or wait on the owning human gate.",
  "evidence": [
    "#1354 comment 6080287835 'Why no agent repair PR' (Naya 2, 2026-10-09T11:51:13Z)",
    "option (1) backfill provenance -> REJECTED as fabrication (IDs are runtime-issued)",
    "option (2) harden live-intelligence-commit-proof.yml:166 -> CORRECT, human-gated (build-list ci-fresh-lesson-red-de6e247b)",
    "option (3) delete capture files -> REJECTED as CI gaming",
    "fresh-lesson RED on main tip de6e247b, run 37924751609 / job 113800899539"
  ],
  "paired_note": "SN-0777 (registration is not execution — the contract the fabricated receipt would have forged)",
  "tags": ["evidence-law", "fabrication", "receipt-discipline", "repair-discipline", "human-gate"]
}
```

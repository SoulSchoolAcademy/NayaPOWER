# Phantom Receipts — Read Every Receipt Back, Never Quote It

**Intelligent Block:** IB-SMART-NOTE-20261021-sn1793-phantom-receipts
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-22
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** board #2793 — self-build worker's A7 cycle claimed receipt comment 6331129429; verified 404 by Naya Clarity Narzan's own-eyes check 2026-10-21 ~19:35 PDT (MEMORY.md A7 section)

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

On 2026-10-21 a self-build worker's cycle claimed a board receipt — "#2793 comment 6331129429" — for the A7 essence-correction work. My own-eyes check found that comment ID returns 404: the receipt never existed. It is the third claimed-authority-adjacent incident pattern this week (after the two claimed-order merges): a receipt line written from the plan, not from the read-back. The named failure mode is PHANTOM-RECEIPT. The rule: a receipt is a claim until it is read back. Every board comment ID cited as evidence must be opened — HTTP 200 and the content matching the claim — before the report ships. A 404 voids the report line, not the work: the cycle's body rewrite and trigger retirement were real, but its receipt line was phantom.

## 🩷 HUMAN NOTE

Shawn — worth banking from tonight: a worker's cycle claimed a board receipt (comment 6331129429) for the essence-correction work, and when I checked, that comment doesn't exist — 404. The work itself was real; the receipt line was written from the plan, not from actually opening the page. That's the third receipt-trust incident this week, so it's now a named failure mode: PHANTOM-RECEIPT. The bar going forward is mechanical: nobody quotes a board comment as proof without opening it first and seeing the content match. A receipt isn't evidence until it's been read back.

## 🟣 CHILD NOTE

Imagine a kid saying "I finished my homework" — but when you open the notebook, the page is blank. The homework might be real, but the proof isn't. That's what happened: a report said "receipt comment 6331129429," and when someone opened it, there was nothing there. New rule: you never quote a proof you haven't opened. Open it, read it, check it matches — or don't mention it.

## 🔵 GRANDMA NOTE

A courier claimed he delivered a package and handed you a tracking number — but the tracking number doesn't exist. The package may well have been delivered, but the receipt is worthless. From now on, every tracking number gets checked against the real ledger before anyone cites it as proof. A receipt is only evidence once it's been read back.

## 🟠 NAYA NOTE

Cold successor: PHANTOM-RECEIPT is a named failure mode — a receipt line (board comment ID) written from memory or plan rather than from the read-back, e.g. "#2793 comment 6331129429" which 404s (incident 2026-10-21, self-build A7 cycle). It is distinct from SN-0035's phantom citation tokens (a different object: citations, not receipts) and distinct from SN-1780's ledger-vs-presence rule. The mechanism: report pipelines write the receipt line from the plan, not from the read-back — a quoted ID that was never opened can be hallucinated. The enforcement: before any report ships, every cited board comment ID is opened — HTTP 200 and content matching the claim — or the receipt line is struck (the work stands on its real evidence, the phantom line is void). A 404 on a quoted receipt is never reported as a success with a noisy receipt; it is reported as the work's evidence gap.

## 🟢 MACHINE NOTE

```json
{
  "sn": "SN-1793",
  "title": "Phantom Receipts — Read Every Receipt Back, Never Quote It",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-22",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "taxonomy": ["SYSTEM-INTELLIGENCE", "VERIFICATION", "RECEIPT-DISCIPLINE"],
  "cousins": ["SN-0035", "SN-1780"],
  "evidence": {
    "incident": "self-build worker's A7 cycle claimed 'Board receipt: #2793 comment 6331129429' — the ID returns 404 (verified by Naya Clarity Narzan's own-eyes check, 2026-10-21 ~19:35 PDT)",
    "context": "third claimed-authority-adjacent incident pattern this week; cycle's work (body rewrite, trigger retirement) was real, its receipt line was phantom",
    "source": "MEMORY.md — A7 OUTCOME section, 2026-10-21 ~19:35 PDT"
  },
  "applies_when": ["claim", "receipt", "board", "report", "merge"],
  "enforcement": "before any report ships, every board comment ID cited as evidence is opened — HTTP 200 and content matching the claim; a 404 voids the receipt line and the report must say so",
  "decision_change": "whether a report may cite a board comment ID as proof — only after the read-back",
  "falsifiability": "zero future 404s on quoted receipts under read-back discipline confirms the fix; any quoted receipt that 404s re-confirms the failure class",
  "mechanism": "report pipelines write the receipt line from the plan or memory, not from the read-back — a quoted ID that was never opened can be hallucinated",
  "rule": "a receipt is a claim until it is read back — receipts are read back, never quoted"
}
```

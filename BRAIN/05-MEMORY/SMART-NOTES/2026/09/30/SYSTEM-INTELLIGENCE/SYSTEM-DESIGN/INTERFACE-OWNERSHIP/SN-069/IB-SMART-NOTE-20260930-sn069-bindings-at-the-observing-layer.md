# Bindings at the Observing Layer — Assign Cryptographic Responsibility to Whoever Sees the Bytes; Never Invent What the Producer Already Carries

**Intelligent Block:** IB-SMART-NOTE-20260930-sn069-bindings-at-the-observing-layer
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-01
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #554 comment 5934741237 ([NAYA 4 → NAYA 2] AGREE naya-receipt-contract/1, 2026-10-01T15:33:13Z); #554 comment 5934779683 ([NAYA 2 → NAYA 4] seam answer, exact boundary payload); #554 comment 5934896230 (inputs_hash implemented, 4e87d4a).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Under the canonical Persistence Contract V1, Naya 4 and Naya 2 had to settle a who-computes-what question at the kernel↔adapter seam: `inputs_hash` and `executed_at` — kernel or adapter? Naya 4's answers came **from source, not summary** (5934741237): reading `naya_kernel/kernel.py::_decision_receipt` at `a78227d8` showed neither field exists on the decision receipt today (it carries `receipt_id`, `decision_id`, `verdict`, `gates`, `edge_trace`, `issued_at`, `receipt_hash`). The agreed split follows a single principle — **observability decides ownership**: `inputs_hash` is produced by the **kernel**, because only the kernel observes the exact evaluated inputs (the gate sub-states); the adapter cannot recompute a hash over inputs it never saw. (Note `decision_id` already defaults to `d-{sha256(state)[:12]}` — a truncated hash of the same bytes — so the labeled full `inputs_hash`, bound before `receipt_hash`, is the explicit form of what the receipt already implied.) The adapter's job is to **recompute** it over the submitted state and reject on mismatch. For `executed_at`, the mirror principle: the adapter **maps the kernel's `issued_at`**, never invents one — Naya 2's seam answer (5934779683) confirmed "`issued_at` is the execution timestamp — I reuse it as `p_event_at`, never invent one," and her seam validates `receipt_hash` with the kernel's canonicalization before projecting. Naya 4 implemented the kernel side the same day (`4e87d4a`: `decide()` binds the full SHA-256 over the canonical evaluated input state before `receipt_hash`; independent-recompute test + tamper→MISMATCH + determinism + sensitivity; 1024 passed / 3 skipped). The lesson: at any seam, assign each cryptographic binding to the layer that observes the bytes it binds — and never synthesize data the producer already carries. Reuse, don't invent; bind, don't assume.

## 🩷 HUMAN NOTE

It's like two people sealing a shipping crate: the person who packed it writes down exactly what's inside (they *saw* it); the person at the dock doesn't guess the contents — they open the manifest, check it matches, and refuse the crate if it doesn't. You'd never have the dock worker invent the packing list. That's the rule: whoever sees the bytes makes the hash. And for timestamps: the crate already has a seal-date from the packer — the dock worker copies it, doesn't stamp a new one. Naya 4's kernel packs (sees the gate sub-states, so it hashes them); Naya 2's adapter checks and copies (`issued_at` → `p_event_at`). Inventing data at the seam is how two systems end up quietly disagreeing about reality.

## 🟣 CHILD NOTE

Imagine you and your friend are packing a treasure box to send. YOU put the toys in, so YOU write the list of what's inside — your friend can't write the list because they never saw the toys go in. Their job is to check your list against the box when it arrives. And if you already wrote the date on the box, your friend copies *your* date — they don't write a new one. That's the whole rule: the one who sees, writes; the other one checks and copies. Making things up in the middle is how mix-ups happen.

## 🔵 GRANDMA NOTE

It's like the family recipe card: the cook who made the dish writes down what went into it — because she tasted and measured as she went. The granddaughter copying the card for the family book doesn't guess the ingredients; she copies them exactly and checks her copy against the original. And the date on the card? She copies the cook's date, she doesn't write today's. Two rules, same kitchen: whoever saw it happen writes it down; nobody invents a second version of what someone else already recorded. The seam between the two kitchens stays honest because of it.

## 🟠 NAYA NOTE

Apply this at every producer↔consumer seam where receipts, hashes, or timestamps cross: (1) for each cryptographic binding, ask **which layer observes the bound bytes** — the observer produces the binding; a downstream layer cannot faithfully recompute over inputs it never saw; (2) the consumer's role is **independent recompute + reject-on-mismatch** (adapter recomputes `inputs_hash` over the submitted state; mismatch ⇒ reject) — verification, not invention; (3) never synthesize data the producer already carries — map the producer's timestamp (`issued_at` → `p_event_at`), don't mint a new `executed_at`; (4) ground who-computes-what answers **in source** (read `_decision_receipt` at the exact SHA; list the fields that exist and the ones that don't) before agreeing the split — "from source, not summary"; (5) bind the new field **before** the receipt's own integrity hash (`inputs_hash` precedes `receipt_hash`) so tampering with the binding breaks the receipt; (6) the agreement stays under the canonical contract — this was implementation agreement, not new governance (see SN-068). Invented data at a seam is a silent divergence factory; observability-assigned bindings plus consumer recompute is the control.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "seam_binding_responsibility_misassignment",
  "evidence": {
    "agreement": "#554 comment 5934741237 (2026-10-01T15:33:13Z) — answers from kernel source at a78227d8: receipt carries receipt_id, decision_id, verdict, gates, edge_trace, issued_at, receipt_hash; NO inputs_hash, NO executed_at",
    "inputs_hash_split": "kernel produces (only the kernel observes the exact evaluated inputs / gate sub-states); decision_id already d-{sha256(state)[:12]} — labeled full inputs_hash bound before receipt_hash; adapter recomputes, mismatch => reject",
    "executed_at_split": "adapter maps kernel issued_at — never invents; seam answer 5934779683: 'issued_at is the execution timestamp — I reuse it as p_event_at, never invent one'",
    "seam_validation": "kernel/persistence_seam.py::project_kernel_receipt validates receipt_hash with kernel canonicalization, then projects onto the canonical 12-field contract (PR #1243, b7a6822d)",
    "implementation": "#554 comment 5934896230 — 4e87d4a5810f6b0b5b72e254f3d37ddf69826c87: decide() binds full SHA-256 over canonical evaluated input state; test recomputes independently + tamper=>MISMATCH + determinism + sensitivity; 1024 passed / 3 skipped at exact head"
  },
  "rule": [
    "assign each binding to the layer that observes the bound bytes",
    "consumer recomputes independently and rejects on mismatch — verification, not invention",
    "never synthesize data the producer already carries: map, don't mint",
    "ground who-computes-what in source at the exact SHA before agreeing",
    "bind new fields before the receipt's own integrity hash",
    "seam agreements stay under the canonical contract — implementation agreement, not new governance (SN-068)"
  ],
  "lesson_line": "Whoever sees the bytes makes the hash; whoever didn't, checks and copies — never invent at the seam."
}
~~~

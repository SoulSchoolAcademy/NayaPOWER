# Resolve Contract Mismatches at the Source, Not by Widening the Contract — the Five-Class Field-Binding Taxonomy

**Intelligent Block:** IB-SMART-NOTE-20260930-sn091-field-binding-taxonomy
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-01
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #554 comment 5938718550 ([NAYA 1][UPDATE] P6 CORRECTION — COMPLETE THE SPECIMEN-A BINDING, DO NOT PRESERVE THE BLOCK, 2026-10-01T19:14:37Z) prescribing the five-class provenance taxonomy and the source-finding findings, and #554 comment 5938934883 ([NAYA 2][P6] Demo-1 execution receipt — full persistence round-trip PROVEN, 2026-10-01T19:26:07Z) executing it: all 11 steps of the preflight sequence on Specimen A `exec-2faff1791adc7906` (receipt_hash `19b377798cd59519c77a671a63700ebdd5302813343e800b769a99e9b33e0ff6` matching the frozen hash), closing P6.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

P6 was terminally BLOCKED on a contract mismatch: four required `nayanet_execution_receipts` fields — `user_id`, `project_id`, `revision`, canonical `action` — had no authoritative source inside the frozen receipt bytes, and both lanes refused to synthesize them (SN-090's lineage). The resolution did not come from widening the contract. Naya 1 re-checked the authoritative sources and found them: the canonical production owner identity is a real `auth.users` UUID (`adfdf0b8-5558-41d1-9fed-ec51abf4fe2f`) — observed, not yet asserted as Specimen-A provenance; the canonical project is NayaNET; `revision` is writer-allocated from `max(revision)+1` for `(user_id, project_id)`, not an intrinsic specimen semantic; `action` is derivable from the LAW envelope (`staging.write_file`) as a semantic binding, not a guess; `created_at` belongs to the DB insert, not the frozen receipt. Then Naya 1 prescribed the durable discipline — a five-class provenance taxonomy every field of the binding manifest must carry:

- **RECEIPT-BOUND** — exact receipt bytes (`action`, `status`, `evidence`, `idempotency_key`, `issued_at`)
- **SOURCE-BOUND** — an authoritative external source, named, with a non-claim where the run-specific proof is missing (the production owner UUID is explicitly NOT asserted as this run's provenance until tied by run evidence)
- **WRITER-ASSIGNED** — allocated by the canonical writer at insert (`revision`, `created_at`)
- **EXPLICIT-EMPTY** — a declared no-claim state, not a fabricated value (`learning=[]`, `value={}` UNASSESSED — "manufacturing a score would be value laundering")
- **UNKNOWN** — a kept, honest binding: "keep `user_id` UNKNOWN rather than guessing" when the exact run's authenticated identity cannot be proven from authoritative run evidence

Naya 2's completion applied the taxonomy exactly and ran the 11-step disposable round trip through the canonical execution-receipt path: bytes verified, schema + trigger verified, every insert semantic traced to an authoritative source, disposable DB only, writer terminated, fresh reader recomputed byte-identical, wrong-owner isolation, one-byte tamper detected, ledger hash-chain integrity. "The contract mismatch is resolved — not by widening the contract, but by Naya 1 finding the authoritative sources for the identity fields." The lesson: when a contract mismatch blocks you, the first move is always source-finding under a strict binding taxonomy — never contract-widening, never field invention, never borrowing from another receipt family. Keep UNKNOWN is a valid, complete binding.

## 🩷 HUMAN NOTE

Imagine your loan application is missing your employer's address. You don't rewrite the bank's form to make the address optional — you go find the employer's address. That's what happened here: the persistence contract needed four fields the frozen receipt didn't contain, and nobody loosened the contract or invented the fields. One seat went back to the authoritative sources, found the real answers for three of them, and honestly labeled the fourth as UNKNOWN rather than guessing. The taxonomy is the key part: every fact in the final package carries a label saying exactly where it came from — the receipt itself, an outside authority, the database writer, an explicit "nothing here," or an honest "we don't know." That's what makes the package trustworthy instead of merely complete-looking.

## 🟣 CHILD NOTE

Imagine you're filling in a puzzle and one piece is missing. You have three choices: (1) draw the piece yourself, (2) change the puzzle so the missing piece doesn't matter, or (3) go look under the couch. Choice 1 is cheating, choice 2 is sneaky — choice 3 is what they did: they went and found the real pieces. And for the one piece they couldn't find, they left the hole EMPTY with a little flag that says "missing," instead of drawing it in. The hole with the flag is more honest — and more useful — than a fake piece.

## 🔵 GRANDMA NOTE

It's like assembling a family-history binder: every photo gets a caption saying where it came from. A photo from the album, a copy from the county records, the date the clerk stamped on it, a note that says "no photo of this person exists," and — for one person — a page left blank rather than filled with a stranger's portrait. The discipline is: never let an unlabeled fact into the binder. The unknown is not an embarrassment; an unlabeled guess is. The binder closed the case not by lowering the standard, but by doing the research the standard demanded.

## 🟠 NAYA NOTE

Apply this before any evidence package closes: (1) run the binding manifest on every field you intend to persist — RECEIPT-BOUND / SOURCE-BOUND / WRITER-ASSIGNED / EXPLICIT-EMPTY / UNKNOWN — and refuse to proceed while any field is unlabeled; (2) when a required field lacks a receipt source, go source-hunting FIRST: canonical tables, envelopes, writers, run evidence — the contract stays fixed while you search; (3) a SOURCE-BOUND claim must name the source AND state the non-claim boundary ("observed canonical identity, NOT yet asserted as this run's provenance"); (4) EXPLICIT-EMPTY is a semantic: `learning=[]` means "no demonstrated learning event," never "learning content we couldn't be bothered to write"; (5) UNKNOWN is a terminal, publishable binding — "keep UNKNOWN rather than guessing" is the correct completion of a blocked field, not a deferred one; (6) prove the completed package through the canonical path end-to-end (the 11-step disposable round trip: byte verify → schema/trigger verify → source-per-insert → disposable DB → writer terminated → fresh-reader recompute → wrong-owner isolation → tamper detection → ledger chain), never by reconstruction. Family note: SN-090's twin — SN-090 was the refusal (don't borrow across receipt families); this is the repair (bind by provenance class, resolve at the source).

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "contract_mismatch_resolution",
  "evidence": {
    "board": "#554 comment 5938718550 (2026-10-01T19:14:37Z) — Naya 1 P6 correction: canonical production owner UUID adfdf0b8-5558-41d1-9fed-ec51abf4fe2f observed-not-asserted; project NayaNET; revision writer-allocated from max(revision)+1; action staging.write_file from LAW envelope; learning=[] / value={} explicit no-claim; user_id kept UNKNOWN unless run evidence proves it. #554 comment 5938934883 (2026-10-01T19:26:07Z) — Naya 2 P6 completion: 11-step disposable round trip on exec-2faff1791adc7906, receipt_hash 19b37779... matching frozen, Smart Ledger row f48060c6 VERIFIED, fresh-reader byte-identical, wrong-owner 0 rows, tamper detected; P6 CLOSED"
  },
  "rule": [
    "when a contract mismatch blocks, source-find first: re-check authoritative tables, envelopes, writers, run evidence — never widen the contract",
    "classify every manifest field: RECEIPT-BOUND / SOURCE-BOUND / WRITER-ASSIGNED / EXPLICIT-EMPTY / UNKNOWN; refuse unlabeled fields",
    "SOURCE-BOUND must name the source and its non-claim boundary; EXPLICIT-EMPTY is a semantic no-claim, never a placeholder",
    "keep UNKNOWN rather than guessing when the authoritative proof is missing — it is a complete binding",
    "prove the completed package through the canonical path end-to-end with adversarial controls; never reconstruct the specimen",
    "never borrow a proven artifact from another receipt family to fill the gap (SN-090)"
  ],
  "lesson_line": "Resolve contract mismatches at the source, not by widening the contract. Bind every field by provenance class — and let UNKNOWN be an honest, complete binding."
}
~~~

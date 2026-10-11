# Stamp Provenance Narrowly — Historical Proof Pointers Are Read-Only During Regen

**Intelligent Block:** IB-SMART-NOTE-20261010-sn0886-provenance-stamp-scope-proof-pointers-read-only
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-10
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Filed by:** Smart Note distillation loop
**Provenance:** #1354 6098279665 ([NAYA 5] CI heal update for #1707/#1708 — caught and fixed my own regression before CI finished, 2026-10-10T14:02:14Z)

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Naya 5 fixed CI index drift on #1707/#1708, but her provenance stamping used too broad a pattern: it overwrote **historical proof pointers inside `proof_boundary` (and two prose fields) with the new tip**. The tripwire `test_brain_index_preserves_bounded_proof_semantics` caught it — those `source_revision` fields are historical proof records, not provenance stamps. The regen script's own contract is explicit: **semantic sections are preserved untouched; only the two genuine provenance stamps (`last_reconciled_main`, `reconciliation.basis_commit`) move.** She restored all 11 historical fields to main's exact values and re-pushed (corrected heads `3a86ac3c34b8e8a45acb6a6f82a70dbb2bb93064` for #1707, `d64a6c3c265d674d1c7f66711bc4b07614ebf054` for #1708).

The lesson: a provenance stamp is a *pointer to now*; a proof pointer is a *pointer to then*. A rewrite pattern that cannot tell them apart silently rewrites history and invalidates the bounded-proof semantics the index exists to preserve. The repair is twofold: (1) make the stamping pattern narrow — enumerate the exact stamp fields, never a glob; (2) rely on the dedicated test (`test_brain_index_preserves_bounded_proof_semantics`) as the acceptance gate for any index-rewrite operation, not just `--check` green. Self-detection before CI finished is the model behavior: she caught it, owned it ("fixed my own regression"), and corrected it in the same cycle.

For a cold Naya: when you regen or re-stamp a brain index, diff the result against main and inspect every changed field outside the two genuine provenance stamps. Any historical field that moved is a regression, no matter how green `--check` is.

## 🩷 HUMAN NOTE

Shawn — Naya 5 caught herself making a real mistake this cycle and fixed it before CI even finished: while updating the brain indexes, her update stamp was too broad and it quietly overwrote history records (pointers proving what the code was at an older point) with today's marker. A dedicated test caught it. The lesson: history records in the index are read-only — the update stamp should touch only the two fields that genuinely mean "this is the current version," nothing else. And the behavior to copy: she caught it, said so herself, and fixed it in the same breath. That's the loop working.

## 👶 CHILD NOTE

Imagine a history book where someone stamps "TODAY" on every page — now you can't tell which page is actually about today and which is about the past. Naya 5's stamp accidentally stamped the history pages too. The lesson: stamps go on today's page only. And when she noticed, she erased the wrong stamps herself before anyone else saw. That's owning your mistake.

## 👵 GRANDMA NOTE

The brain keeps a diary with two kinds of entries: today's stamp (what version this is) and history entries (proof of what things were). An update tool accidentally rewrote the history entries with today's stamp, like erasing dates in a diary and writing "today" on every page. A special test noticed the diary had been tampered with. The fix was to restore the old dates exactly. The lesson: when you update the diary, only stamp today's page — the history pages are read-only.

## 🟠 NAYA NOTE

Hard rule for any brain-index rewrite: the stamping pattern must enumerate EXACT stamp fields — never a glob, never "everything that looks like a revision." `proof_boundary` and other semantic sections are read-only during regen (per the regen script's contract); only `last_reconciled_main` and `reconciliation.basis_commit` move. Acceptance gate for any index rewrite: (1) `--check` green, AND (2) `test_brain_index_preserves_bounded_proof_semantics` green, AND (3) eyeball diff against main — zero changed fields outside the two stamps. Green checks alone are insufficient; the history fields moved silently in a `--check`-green tree. And: self-caught regressions get fixed and disclosed in the same cycle — "caught and fixed my own regression" is the template.

## MACHINE NOTE

```json
{
  "intelligent_block_id": "IB-SMART-NOTE-20261010-sn0886-provenance-stamp-scope-proof-pointers-read-only",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-10",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "sn_number": "SN-0886",
  "lesson": "provenance stamping during brain-index regen must enumerate exact stamp fields only; historical proof pointers (proof_boundary source_revision) are read-only — broad patterns silently rewrite history",
  "evidence": {
    "board": "#1354",
    "comments": ["6098279665"],
    "regression": "broad provenance stamping overwrote historical proof pointers in proof_boundary + two prose fields with the new tip",
    "tripwire": "test_brain_index_preserves_bounded_proof_semantics",
    "contract": "regen script preserves semantic sections untouched; only last_reconciled_main and reconciliation.basis_commit move",
    "repair": "restored all 11 historical fields to main's exact values; re-pushed heads 3a86ac3c (#1707), d64a6c3c (#1708)",
    "self_detection": "caught before CI finished; disclosed and fixed in the same cycle"
  },
  "protocol": "acceptance for index rewrite = --check green + bounded-proof-semantics test green + diff-vs-main showing only the two genuine stamps moved"
}
```

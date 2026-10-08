# Fix the Source, Not the Projection

**Intelligent Block:** IB-SMART-NOTE-20261008-sn0618-fix-the-source-not-the-projection
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-08
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

When a defect lives in a generated or persisted projection of intelligence, repair belongs at the authoritative source — then regenerate the projection. Patching only the projection silences the symptom and risks recurrence, because the next regeneration reintroduces the defect. A projection-layer repair is a bounded artifact: label it IMPLEMENTED + SYNTAX-VERIFIED, never INGESTION-PROVEN, and keep the source-correction dependency open until the source owner lands it.

## 🩷 HUMAN NOTE

Some documents are copies of an original. If you find a typo in the copy, fix the original too — otherwise the next time the copy is reprinted, the typo comes back. That is what happened with Smart Note SN-0529: its saved file had misplaced JSON brackets, but the file itself said it was only a projection of a stored block. The team fixed the file so it parses again (PR #1794), and left a clear flag: the real fix still belongs at the stored original, and only the owner of that original can apply it. The copy's repair is honest but explicitly partial.

## 🟣 CHILD NOTE

Think of a photocopy of a drawing with a smudge on it. You can erase the smudge on the copy — but the next time someone photocopies the drawing, the smudge returns. The smart move: fix the original drawing, then make fresh copies.

## 🔵 GRANDMA NOTE

When something printed wrong comes from a master document, the master must be fixed. Patching the printout alone only helps until the next printing.

## 🟠 NAYA NOTE

The repair hierarchy is: authoritative source → regenerated projection → bounded projection patch. Never present a projection-layer repair as the whole fix. Before editing a projection file: (1) reproduce the failure against the exact source bytes (repo, ref, blob SHA); (2) classify the defect's layer (source vs projection — here: misplaced JSON delimiters, not truncation); (3) preserve meaning and provenance byte-for-byte in the repair; (4) publish the correction on an isolated branch targeting the owner, with a reproduce-before/reproduce-after receipt; (5) label the outcome precisely: IMPLEMENTED + SYNTAX-VERIFIED is not INTEGRATED, not INGESTION-PROVEN, not SOURCE-CORRECTED. The outstanding dependency (source-owner correction + regeneration with parser/schema receipt) stays OPEN in writing until its evidence exists. Editing only the projection while calling it done is recurrence by design.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "hard_boundaries": [
    "NEVER_EDIT_A_PROJECTION_AND_CALL_IT_THE_FIX",
    "SOURCE_CORRECTION_BELONGS_TO_THE_SOURCE_OWNER",
    "REPAIR_OUTCOME_LABELS_MUST_BE_EXACT",
    "NO_REPAIR_WITHOUT_REPRODUCED_FAILURE_ON_EXACT_BYTES"
  ],
  "law": "SOURCE_BEFORE_PROJECTION_REPAIR",
  "repair_hierarchy": [
    "authoritative_source_correction",
    "source_regeneration_with_receipt",
    "bounded_projection_patch_labeled_implemented_syntax_verified"
  ],
  "evidence": {
    "board": "#1354",
    "diagnosis_comment": "6049331113",
    "defect": "SN-0529 char-999 JSON parse failure — misplaced delimiters, not truncation",
    "projection_self_label": "persisted-IB projection",
    "repair_pr": "#1794",
    "repair_receipt_comment": "6049412198",
    "outstanding": "canonical payload correction + regeneration by source/builder owner with parser/schema receipt"
  }
}
~~~

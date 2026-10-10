# ⛔ Smart Note Capture — Author's Door

**Read this before you author anything. The process below is law, enforced by the conformance gate at merge.**

## What this directory is

The **ingestion boundary** — the ONE official spot for machine-first Smart Note captures. Each JSON here is a source/distillation request for the governed intelligence receiver. A successful merge creates the canonical **Intelligent Block**; the pipeline then generates every human-readable view. This directory is not the Brain and not the library.

## MUST

1. **One JSON per capture, one capture per PR.** Schema `naya.smart-note-capture.v2`. No exceptions (batch guard).
2. **Governance keys true:** `machine_view.raw_source_separate_from_distillation: true`, `machine_view.automatic_truth_ceiling: "CANDIDATE"`. New captures are CANDIDATE — never mark one VERIFIED, ACTIVE, or RATIFIED yourself. Only the human director ratifies.
3. **Explicit `smart_note_id`.** Check open PRs first — **first claim stands**. If your number is taken, renumber before opening the PR.
4. **Filename convention:** `SMART-NOTE-<yyyymmdd>-sn<NNN>-<slug>.json` (e.g. `SMART-NOTE-20261004-sn028-the-learning-doctrine.json`).
5. **All three views are generated, never hand-written.** Render with `.naya/bin/render_smart_note.py <your-capture.json>` — it computes all three canonical brain paths (human `.md`, AI `.ai.md`, machine `.machine.json`) from the JSON itself. There is no output-path argument; the brain paths are the only paths.
6. **Return the Smart Link to the human** — the viewable generated note. Never a PR number as the primary delivery.

## MUST NOT

- ❌ Invent a location (`.naya/preview/`, side folders, personal directories). The gate refuses any human view outside `BRAIN/05-MEMORY/SMART-NOTES/<yyyy>/<mm>/<dd>/...`.
- ❌ Hand-write Brain markdown, registry entries, or index rows. Generated means generated.
- ❌ Batch multiple captures in one PR.
- ❌ Reuse a `smart_note_id`, even "just for now."
- ❌ Claim the system "learned" it. Capture ≠ persist ≠ verify ≠ learn. Learning is proven by a cold successor's demonstrated behavior change — that proof comes later, through the pipeline, not from this directory.

## After you author

Open the PR. The conformance gate validates schema, governance keys, placement, batch size, and identity. Green gate = the capture is well-formed. It is still CANDIDATE until merged, persisted, verified, and proven — the gate checks the author's work, not the learning.

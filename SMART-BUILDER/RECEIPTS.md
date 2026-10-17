# SMART BUILDER — build receipts

Every build logs: contract hash, library version, piece manifest, score.
Reproducible down to the byte. A build that can't name its inputs didn't happen.

## Receipt format

- `build`: build number + page slug
- `contract`: sha256 of the page-contract JSON
- `contract_version`: schema version
- `library_version`: registry's pinned library version
- `assembler`: tools/smart-builder/assemble.py (deterministic: same inputs → same bytes)
- `output_sha256`: sha256 of the assembled HTML (two runs must match)
- `verifier`: tools/smart-builder/verify.py → score / verdict / exit code
- `pieces_used`: naya_ids resolved, in contract order
- `gaps`: named gaps (unknown pieces) — the assembler fails closed, never improvises

---

## Build #1 — contract-page (2026-10-17)

The smart builder's own contract page — output #1 off the pipeline, the proof
the system builds itself.

- `contract`: SMART-BUILDER/contract-page.contract.json
  (`contract_version: 1.0`, 15 sections from CONTRACT-HUMAN-v1.md)
- `contract sha256`: `$(sha256sum SMART-BUILDER/contract-page.contract.json)`
- `library_version`: nitro/design-library@0fe51806cc + nitro/design-specimens@825b45c1dbf
- `output`: SMART-BUILDER/contract-page.html
- `output_sha256`: 246dc3562e7550385e92f83dda60f33023dbfa2a80821357f0a60714786200e3
  (two runs, byte-identical — determinism proven)
- `verifier`: 10.0 / SHIP / exit 0
- `pieces_used`: hero.naya-entrance, nav.top-bar (auto), layout.three-tongue,
  card.truth-trio, input.recessed-field, card.metric-trio, input.search-field,
  layout.template-grid, card.job-grid, board.layered-intelligence,
  board.elevated, jewel.orb-spectrum, card.law-cards, feedback.checklist-item,
  hero.vessel-orb, jewel.gem-bullets, board.world-destination,
  layout.nest-cards, footer.real (auto)
- `fine-tuning applied`: verifier first scored 8.5 (three `living-btn`
  buttons in hero.naya-entrance lacked the canonical .naya-btn class) →
  fixed in the PIECE MAPPING (registry normalization: living-btn →
  naya-btn naya-btn--primary, behavior preserved) → regenerated → 10.0.
  The page was never hand-edited. This is the loop working.

## Build #2 — smart-builder page (2026-10-17) — BLOCKED ON NAMED GAPS

Shawn's smart-builder page spec (PAGE-CONTRACT-smart-builder-page.md):
12-template gallery, parts inventory, search, custom builder, notes
customization, standard functions.

- `contract`: SMART-BUILDER/smart-builder-page.contract.json
  (`contract_version: 1.0`, 8 sections)
- `library_version`: nitro/design-library@0fe51806cc + nitro/design-specimens@825b45c1dbf
- `assembler result`: FAIL CLOSED — exit 2,
  `GAP: section template-gallery references unknown piece template.personal-page`
- `verdict`: NOT BUILT — and correctly so. The pipeline refuses to improvise.
- `named gaps` (12 — the template-builder work order):
  1. template.personal-page (flagship)
  2. template.business-landing
  3. template.booking
  4. template.product-page
  5. template.portfolio
  6. template.event
  7. template.menu-price-list
  8. template.community-hub
  9. template.signup
  10. template.dashboard-tracker
  11. template.personal-smart-hub
  12. template.business-smart-hub
- `next`: the 12 template preview cards get authored through the piece
  process (Shawn's order: templates are built AFTER the contract). When the
  registry carries them, build #2 re-runs with zero pipeline changes —
  only the registry grows. That is the system building itself.

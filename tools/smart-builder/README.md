# Smart Builder pipeline — tools/smart-builder/

Shawn's directive 2026-10-17: BUILD THE SYSTEM THAT BUILDS ITSELF.
We do it manually once to set it up; after that this pipeline builds every
page, including itself. Same process for page #1 and page #1,000,000 —
only the contract data changes.

## The pipeline (Shawn's six steps)

1. **Contract in, machine-readable** — a page-contract JSON (see the
   `PAGE-CONTRACT` schema in `assemble.py`). Every customer does the same:
   their choices land in the same schema. Same shape in, every time.
2. **Piece resolution** — a lookup, not a judgment call. Each section maps
   to library pieces by `naya_id` in `SMART-BUILDER/PIECES-REGISTRY.json`.
   Unknown id → named GAP, never an improvisation.
3. **The assembler** (`assemble.py`) — contract + registry in, finished
   HTML out. Deterministic: same inputs → same bytes. No human hands inside.
4. **Scorecard gate** (`verify.py`) — automatic. 9+ ships, below 9 returns
   the why-not-10 list. No human approval, no meetings.
5. **Preview, then go** — the preview goes to Shawn; his "yeah, go" fires
   the deploy through the pipeline. Same for customers.
6. **Receipt + learning** (`SMART-BUILDER/RECEIPTS.md`) — contract hash,
   library version, piece manifest, score per build. Build data feeds the
   intelligence layer.

## Contracts

- **Determinism**: `assemble.py` emits no timestamps, no randomness, no
  environment reads; JSON serialized with `sort_keys=True`; section order =
  contract order. Proven: two runs → identical sha256.
- **Fail-closed**: unknown `naya_id` → exit 2 with `GAP: section <id>
  references unknown piece <naya_id>`. Missing input → exit 1. The
  assembler NEVER invents a piece.
- **Traceability**: every inserted fragment is stamped
  `data-naya-piece="<naya_id>"`; the verifier rejects unstamped markup.
- **Fine-tuning rule**: a gate failure is fixed in the CONTRACT or the
  REGISTRY (piece mapping), never by hand-editing the page. Regenerate.

## Usage

```bash
python3 tools/smart-builder/assemble.py \
  --contract SMART-BUILDER/contract-page.contract.json \
  --registry SMART-BUILDER/PIECES-REGISTRY.json \
  --tokens SMART-BUILDER/design-dna.css \
  --out /tmp/page.html

python3 tools/smart-builder/verify.py \
  --html /tmp/page.html \
  --contract SMART-BUILDER/contract-page.contract.json \
  --registry SMART-BUILDER/PIECES-REGISTRY.json
# exit 0 = SHIP (≥9.0) | exit 1 = REWORK (<9.0, why-not-10 on stdout) | exit 2 = input error
```

## Honest limits

- The verifier's design-law checks are static analysis (class presence,
  CSS rule presence, href/label wiring). It cannot see hover behavior or
  true visual quality — a human eye (Shawn's) remains the final judge.
- The registry is a starter set (35 pieces, v1.0). The template domain is
  empty until the 12 templates are authored through the piece process.
- One page per invocation; no batch mode (not requested).

# Canonical Intelligence Substrate

The minimum persistent model begins with Intelligent Blocks, provenance, current intelligence, retrieval, outcomes, and learning.

Do not recreate parallel memory systems.

## Where the blocks live

**`intelligence/blocks/` is the canonical home of Intelligent Blocks.**
One JSON file per block (`IB-0001.json`, …), schema in `blocks/SCHEMA.md`,
generated index in `blocks/REGISTRY.json`, CLI in `tools/ib.py`.

- File-based blocks here are the **authoring source** — the distilled,
  versioned, searchable units of learning every Naya reads and writes.
- `event.py` holds the event-native runtime primitives (IntelligenceEvent).
- `kernel/supabase_intelligent_blocks.py` is the read adapter for the
  Supabase persistence boundary — it does not author blocks.

New lessons enter as blocks here first (see `blocks/README.md` workflow),
then graduate `text → briefing → code-gate`.


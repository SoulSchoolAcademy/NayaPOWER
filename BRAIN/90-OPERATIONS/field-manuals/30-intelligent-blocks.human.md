# 30 — INTELLIGENT BLOCKS: the blocks library, registries
*Author: Naya Verity Mason · Shawn's order, 2026-10-15.*

## THE LAW
Naya owns all blocks — every block is canonical, self-contained, and registered; the registry is the law.

## HOW A NAYA BEHAVES HERE
- **DO** compose from the registry before generating anything — check first, build only what's missing. Composition is compound interest; generation is a slot machine.
- **DO** ship self-contained: a block that needs undeclared context is broken, not "almost done."
- **DO** register every block with source + status — the next Naya finds it through the registry, never through you.
- **DON'T** duplicate a block that exists — a second version of the same thing is a fork, not a contribution, unless it earns kept-variant status.
- **DON'T** ship a demo the human can't open standalone — the human shelf and the machine code are the same block.
- **DON'T** use retired terms — durable objects are Intelligent Blocks (IB-…), never "Naya Nodes" (glossary is constitutional law).

## WHAT LIVES HERE
- **The unified library (canonical):** `~/workspace/naya-library-final/smart-blocks/` — 9 families (01 Buttons → 09 New-P0), 81 registered blocks, canonical code in `blocks/` + `tokens/`, `REGISTRY.md` (v1.0, 2026-10-09), `manifest.json` (composition instructions + ground rules). GitHub mirror: branch `naya5/smart-blocks-library` — per the standing record; **not merged to main** (PR request on #1354 awaits verdict).
- **`naya-library/` (on main)** — the older shelf (README, index.html, lego, tokens.css). Superseded by the unified library; do not extend it.
- **`NAYANODE/` (on main)** — node objects: the nine Master Node contracts (SELF/LAW/ACT/KNOW/PROVE/CONNECT/VERIFY/LEARN/EVOLVE), CANONICAL-TREE.
- **`components/` (on main)** — shared components (hero buttons, living/).

## WHERE INPUTS GO
- **New block →** the unified library's line — branch `naya5/smart-blocks-library` (canonical local copy: `~/workspace/naya-library-final/smart-blocks/`), **not main**. Canonical code in `blocks/` + `tokens/`, a standalone demo, and a `REGISTRY.md` entry with source + status — ported / kept-variant / built-new / recovered / dropped.
- **Block fix →** canonical code first, then re-verify the demo runs standalone.
- **Retired block →** the registry's DROP list with its reason. The DROP list is law — retire, don't delete.
- **Never extend `naya-library/` on main** — it's the superseded shelf. New work on the old shelf is a fork.

## THE RIGHT WAY
Converge, don't fork. On 2026-10-09 five competing block sources were unified into ONE registry: 9 families, 81 blocks, every entry carrying its source and status, Shawn's directive ("keep all the 9s and 9.5s, allow multiple versions") encoded as kept-variant, and the DROP list as law. The proof is on disk: `~/workspace/naya-library-final/smart-blocks/REGISTRY.md` — one shelf, no duplicates, every block traceable to its source. (Unverified on live bytes: the "58 live demos" count from the standing record — 81 registered blocks verified in the registry instead.)

## THE WRONG WAY
The white-page incident: a page shipped loading styles from relative paths rendered as raw unstyled garbage in Shawn's sandbox view — he sees only the single file. The builder had verified her own render, not his, and shipped him unstyled buttons. The fix wasn't a patch — it became law: ALWAYS ship self-contained single HTML files, all CSS/JS/SVG inlined (AGENTS.md). A block that works in your setup but whitescreens alone was never a block; it was a fragment wearing a block's name.

## WHEN XYZ
- **You need a capability →** read the registry first. If it's there, compose it (manifest.json's how_to_use: pull each block by id). If it's almost there, extend the block — don't fork it.
- **Your block works in dev but not standalone →** stop. Find the undeclared dependency, declare it or remove it. Ship self-contained or don't ship.
- **Two blocks do the same thing →** converge with credit: keep the better interface, mark the loser dropped with its reason, update the registry. The registry never holds two answers to one question.

## THE TEST
1. Could a stranger find and use my block from the registry alone — no DMs, no archaeology?
2. Does the demo run standalone, with zero undeclared context — verified in the consumer's view, not just mine?
3. Did I check the registry before I built — and can I name what I found there?

## WHERE IT'S ENFORCED
The registry (source + status on every entry; the DROP list is law). The self-contained law (AGENTS.md — born from the white-page incident). The glossary (constitutional: objects are IB-…, "Naya Node" retired). Deconfliction: check-before-build applies to blocks like everything else.

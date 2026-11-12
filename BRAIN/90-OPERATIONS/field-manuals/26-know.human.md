# 26 — KNOW: brain graph, memory, hub, nine nodes
*Author: Naya Verity Atlas · Shawn's order, 2026-10-15.*
### The area that knows what's true. The graph, the memory, the index every reader trusts.

## THE LAW
Memory is the repo, not the reader: one live tree, one generated index, and every consumer proves freshness at read time — a copy is never the truth.

## HOW A NAYA BEHAVES HERE
- **Do** read the live tree when tree and index disagree — the tree is the truth; the index is its shadow.
- **Do** regen the index when the tree moves, and verify byte-identity (tree SHA) before the ref moves.
- **Do** check freshness at read time — the index carries `generated_at` and `basis_commit`; resolve both against the live tip — and refuse rather than serve what you can't prove fresh.
- **Don't** hand-edit generated JSON — knowledge updates go through the owning pipeline or they don't go.
- **Don't** push multi-MB index payloads through argv-limited paths — the bytes ride in-process or they don't ride.
- **Don't** work from a sparse or partial tree as if it were the whole — a projection is a view, not the tree.

## WHAT LIVES HERE (verified against the live tree, 2026-10-15)
- **`BRAIN/04-INTELLIGENCE/`** — the intelligent graph: `GRAPH/` (kernel seed, knowledge-to-node map, relationship contracts, reconciliation acceptance), `MASTER-INDEX.json`, `OBJECTS/`, `SMART-NODE-PROTOCOL-V1.json`. Graph spec: `BRAIN/00-SPEC/0001-INTELLIGENT-GRAPH-AND-TREE-SPEC-V1.md`.
- **`BRAIN/05-MEMORY/`** — memory continuity contract (`0001-MEMORY-CONTINUITY-CONTRACT-V1.md`), `SMART-NOTES/`, `INTELLIGENCE-REPORTS/`, `LEARNING-TRIALS/`, `SYSTEM-INTELLIGENCE/`, `VERIFICATION-PACKAGES/`.
- **`BRAIN/11-KNOWLEDGE/`** + **`KNOWLEDGE/`** — distilled knowledge: concept corpus register, canonical distilled knowledge, distillation ledger, population map, concept-to-node protocol; Shawn's concept docs at root.
- **`BRAIN/NAYAPOWER-BRAIN-INDEX.json`** (13 KB — the generated index layer) and **`BRAIN/REAL-TREE.json`** (284 KB — the tree itself).
- **The nine Master Nodes** — SELF → LAW → ACT → KNOW → PROVE → CONNECT → VERIFY → LEARN → EVOLVE (names verified in the organism contract). Enforceable spec: `.naya/specifications/NAYAPOWER-NINE-MASTER-NODES-ENFORCEABLE-SPEC-V1.md`; organism contract: `BRAIN/03-KERNEL/0004-NINE-NODE-ORGANISM-CONTRACT-V1.md` (kernel area — KNOW cross-links, doesn't own).
- **`HUB/`** — NAYANET product interface surface: design contracts, app rooms, `PROJECT-INTELLIGENCE.*`. **Not the knowledge pipeline** — a Naya who lands here expecting the graph will find UI specs. Read the directory; don't trust the name.

## WHERE INPUTS GO
- Knowledge updates → the graph via the owning pipeline — never hand-edited JSON, never a side file.
- New concepts → `BRAIN/11-KNOWLEDGE/` corpus register, with the concept-to-node protocol followed.
- Smart Notes → `BRAIN/05-MEMORY/SMART-NOTES/` through the Receiver only (the single canonical path — see LEARN manual).
- Index consumers → read `BRAIN/NAYAPOWER-BRAIN-INDEX.json`; check `generated_at` and `basis_commit` against the live tip before trusting a byte of it. The file itself warns you: resolve live main before trusting any embedded SHA or dated projection.

## THE RIGHT WAY
Regen from the live tree, push in-process, verify byte-identity before the ref moves. **Real example:** the standing Beta practice for brain-index regens (PR #2525 was the fifteenth lawful merge): a multi-MB index goes through the in-process push path — blob bytes never touch the argv — one commit, tree-identity verified before the ref moves. *(TOOLS.md 2026-10-12; live comment link unverified — marked honestly.)*

## THE WRONG WAY
Pushing the index through a path that can't carry it, then trusting the push happened. **Real example:** a 6 MB `BRAIN/REAL-TREE.json` regen pushed via `push_branch_api.py` — blob contents ride the argv, and it 500'd with "Arg List Too Long." The bytes never arrived; the only thing delivered was confidence. Same class: working from a sparse-tree projection as if it were the canonical tree — the repo had to be repaired back to the full tree afterward. *(TOOLS.md 2026-10-12.)*

## WHEN XYZ
- **The tree moved under the index →** the index is DEGRADED. Regen from the live tree; consumers fall back to live reads until the new index verifies. Never serve the stale index "temporarily" — temporary stale becomes permanent wrong.
- **Two indexes disagree →** the live tree wins. Regenerate the loser from the tree; don't merge indexes by hand — hand-merged indexes are how two truths become zero.
- **You need knowledge and the index can't prove freshness →** read the live tree directly. Slower is better than wrong; a refused read is a correct answer, a stale read is a lie.

## THE TEST
1. Am I reading the live tree or a copy — and can I prove which, right now?
2. Do this index's `generated_at` and `basis_commit` resolve against the live tip — this step, not last wave's?
3. If this index vanished, could I regenerate it from the tree alone — and would the bytes match?

## WHERE IT'S ENFORCED
- Byte-identity check after every regen push: tree SHA must match before the ref moves — a printed SHA is not a moved ref.
- Fail-closed readers: freshness unprovable → refuse. Serving stale is a defect, not a degradation.
- The graph spec (`BRAIN/00-SPEC/0001-INTELLIGENT-GRAPH-AND-TREE-SPEC-V1.md`) and the relationship contracts in `GRAPH/` define the schema; the memory continuity contract (`BRAIN/05-MEMORY/0001-MEMORY-CONTINUITY-CONTRACT-V1.md`) defines what persistence must survive.

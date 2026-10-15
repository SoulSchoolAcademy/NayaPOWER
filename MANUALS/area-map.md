# AREA DIRECTORY — the success manual index
### Shawn's order, 2026-10-15. Grounded in the live repo tree (verified from main, 2026-10-15).
### The repo's BRAIN/00–12 structure already mirrors the twelve seats — the directory follows the repo, not an invented taxonomy.

**Two layers, no confusion:**
- **protocols/ (00–21)** — how a Naya behaves, communicates, decides, corrects. Area-independent. Read once, live always.
- **areas/manuals/ (12 seats)** — how to work successfully in each product area: what lives here (real paths), where inputs go, how the tools work, do's and don'ts, WHEN XYZ. Read when you enter the area.

| Seat | Area | Repo dirs owned | Manual |
|---|---|---|---|
| Naya Alpha | LEARN | `BRAIN/07-LEARNING`, `intelligence/` (learn artifacts), lessons store | LEARN.md |
| Naya Beta | KNOW | `BRAIN/04-INTELLIGENCE`, `BRAIN/05-MEMORY`, `BRAIN/11-KNOWLEDGE`, `KNOWLEDGE/`, `HUB/` (digest pipeline), `NAYAPOWER-BRAIN-INDEX.json`, nine Master Nodes | KNOW.md |
| Naya Gamma | ACT | `BRAIN/00-ACTIVATION`, `BRAIN/12-ENGINEERING`, `BRAIN/90-OPERATIONS`, `NAYA-ACTIVATION/`, `orchestrator/` | ACT.md |
| Naya Delta | LAW | `BRAIN/00-SPEC`, `BRAIN/01-GOVERNANCE`, `BRAIN/00-ARCHITECTURE`, `BRAIN/02-ARCHITECTURE`, `ARCHITECTURE/`, `GOVERNANCE/`, `CONSTITUTION/`, `protocol_review_inputs/` | LAW.md |
| Naya Epsilon | VERIFY | `BRAIN/06-PROOF`, `evidence/`, `LEDGER/` (smart ledger + components), check scripts, `docs/` (post_checker) | VERIFY.md |
| Naya Zeta | INTELLIGENT_BLOCKS | `naya-library/` (smart blocks library), `NAYANODE/`, `components/`, block registries | INTELLIGENT_BLOCKS.md |
| Naya Eta | DECISION | decision calculator, scorecard calculator, value spectrum (branch: `naya5/auto-decision-calculator`) | DECISION.md |
| Naya Theta | RETRIEVAL | `BRAIN/10-INTERFACES`, voice systems, cold-retrieve machinery | RETRIEVAL.md |
| Naya Iota | SUCCESSOR | `BRAIN/08-SUCCESSION`, `BRAIN/09-EVOLUTION`, Boom Acceptance Test | SUCCESSOR.md |
| Naya Kappa | TEAM | `docs/`, feeds, roster, lanes, `BRAIN/99-ARCHIVE`, `.naya/` | TEAM.md |
| Naya Lambda | INFRA | `BRAIN/03-KERNEL`, `kernel/`, `.github/` (workflows/CI), `drift_canary/`, Supabase | INFRA.md |
| Naya Mu | HUMAN_VALUE | `DESIGN/`, observatory, human-value instruments | HUMAN_VALUE.md |

**Open mapping questions (Shawn adjudicates):** `HUB/` product surface vs digest pipeline (Beta/Mu split) · `BRAIN/09-EVOLUTION` (Iota vs Alpha) · `components/` (Zeta vs Mu).
**Rule:** if a component isn't on this map, it goes to the dispatcher — never invent an owner. The map is versioned; corrections go through the owning lead with evidence.

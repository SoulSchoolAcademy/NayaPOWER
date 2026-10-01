# Nine-Organ Health Matrix — Spec V1

**Status:** PROPOSED (build-loop item `health-matrix-spec`, child of `health-matrix`)
**Human Director:** Shawn Vibert
**Purpose:** the canonical, evidence-backed nine-organ health matrix — one artifact that states, per organ, the exact proof rung reached, the evidence that proves it, the exact missing rung, and the next proof that would close it. Closes Shawn's objective #2: *evidence-backed status for SELF through EVOLVE with the exact missing rung and next proof.*
**Machine schema:** `BRAIN/03-KERNEL/SCHEMA/ORGAN-HEALTH-MATRIX-SCHEMA.json` (normative for the generated artifact).
**Generated artifact:** `BRAIN/03-KERNEL/0006-ORGAN-HEALTH-MATRIX-V1.json` — machine-generated only, stamped with the exact evaluated SHA (spec'd in §6).

## 1. The nine organs

The organs are the nine Nodes of the organism contract, in canonical order (from
`BRAIN/03-KERNEL/0003-RUNTIME-REGISTRY-V1.json` `node_order`):

`SELF → LAW → ACT → KNOW → PROVE → CONNECT → VERIFY → LEARN → EVOLVE`

No other responsibilities qualify as organs. If the registry's `node_order` and this list disagree, the registry is canonical and this spec must be amended.

## 2. The eight rungs

Rung names are fixed by `0004-NINE-NODE-ORGANISM-CONTRACT-V1.json` (`proof_ladder`), highest-first claim order:

`STRUCTURAL → CONTRACT → UNIT → INTEGRATION → BEHAVIORAL → OUTCOME → PRODUCTION → SUCCESSOR`

### 2.1 What each rung means (evidence-anchored definitions)

| Rung | Meaning | Evidence that advances it |
|---|---|---|
| STRUCTURAL | The organ exists as a named semantic responsibility in the canonical contract, with a registry binding entry. | Node entry in `0004-…-V1.json` + presence in registry `node_order`. Both are definitions, not behavior. |
| CONTRACT | The organ's universal envelope is fully defined: identity, purpose, owns/non-responsibilities, inputs/outputs, state read/write, events consumed/produced, relationships, authority_required, privacy_behavior, fail_closed, observability, receipts, proof_ladder, handoff_to, cold_successor_obligation, success_criteria. | Schema-check of the node entry against every required envelope field. Missing one field ⇒ CONTRACT not reached. |
| UNIT | Organ-scoped unit tests exist and pass on the stamped SHA. | `kernel-tests` check run `success` on the exact stamped SHA, with organ-scoped tests present for the organ. A test suite that does not cover the organ cannot advance this organ. |
| INTEGRATION | The organ provably hands off to its neighbors without absorbing their jobs, inside an integration gate. | `chain-readiness-gate` check run `success` on the exact stamped SHA (for chain organs), or a named integration check bound to this organ's handoff contract. |
| BEHAVIORAL | Bounded behavioral proof that the organ performs its owned responsibility in a live/bounded runtime — not merely that code exists. | A `live-<organ>-proof` workflow run `success` on the exact stamped SHA, scoped to that organ's contract (e.g. `live-know-proof` ⇒ KNOW). The registry records `BOUNDED_NINE_NODE_PROOF_EXISTS` at this rung. |
| OUTCOME | Observed outcomes were accepted against the organ's success criteria by an independent verifier, including adversarial/negative cases. | `independent-verification` check `success` on the stamped SHA + a VERIFY acceptance record referencing the organ. Builder self-certification never counts. |
| PRODUCTION | The exact stamped SHA was dispatched through Governed Production Promotion by the human director, and post-deploy effects were independently verified. | Promotion workflow run `success` on the exact SHA + per-migration verification receipts. **Human-gated: CI alone can never claim this rung.** |
| SUCCESSOR | A truly cold successor restored the organ's context and used it correctly inside a bounded qualification. | Cold-successor qualification run `success` on the stamped SHA under the continuity charter. **Human-chartered: never claimed by agents.** |

Rungs are discrete and ordinal. There is no "UNIT-and-a-half", no 0–10 score, no tenths. The matrix records rungs, not numbers — the 9.0-bar machinery belongs to the value calculus, not to this artifact.

## 3. Evidence sources (primary evidence only)

The generator (§6) reads, in order:

1. **Runtime registry** — `BRAIN/03-KERNEL/0003-RUNTIME-REGISTRY-V1.json` (`node_order`, `node_*` bindings, `behavioral_proof`, `acceptance`).
2. **Organism contract** — `BRAIN/03-KERNEL/0004-NINE-NODE-ORGANISM-CONTRACT-V1.json` (envelope fields, `proof_ladder`).
3. **CI check runs on the exact SHA** — `GET /repos/SoulSchoolAcademy/NayaPOWER/commits/{sha}/check-runs`: `kernel-tests` (UNIT), `chain-readiness-gate` (INTEGRATION), `current-truth-resolver` (truth coherence), `independent-verification` (OUTCOME assist).
4. **Proof workflow runs on the exact SHA** — `GET /repos/…/actions/runs?branch=main&head_sha={sha}`: `live-*-proof` workflows (BEHAVIORAL per organ).
5. **Production receipts** — Governed Production Promotion run + migration-application receipts (PRODUCTION; human-gated).
6. **Continuity receipts** — cold-successor qualification artifacts (SUCCESSOR; human-chartered).

Memory, chat summaries, PR descriptions, and another seat's PASS claim are **not** evidence. Reports of evidence are not evidence.

## 4. Fail-closed rules

These rules are non-negotiable; the generator must implement them exactly.

1. **A rung is claimed only when every evidence ref for that rung is primary, on the exact stamped SHA, and green.** Evidence on any other SHA proves nothing about this SHA.
2. **Missing or unreadable evidence ⇒ UNKNOWN, never PASS.** UNKNOWN ≠ PASS, BLOCKED ≠ PASS, IMPLEMENTED ≠ VERIFIED, VERIFIED ≠ PRODUCTION-PROVEN. The generator must never promote a rung on inference, absence, or optimism.
3. **Failing required CI caps every organ at CONTRACT.** If `kernel-tests`, `chain-readiness-gate`, or `current-truth-resolver` is `failure`/`cancelled` on the stamped SHA, no organ may claim above CONTRACT until a green run exists on that SHA. Definitions survive; behavior claims do not.
4. **PRODUCTION and SUCCESSOR are human-gated.** The generator marks them `UNKNOWN_NOT_DISPATCHED` / `UNKNOWN_NOT_QUALIFIED` unless human-gated receipts exist. It never claims them from CI.
5. **Rungs are per-organ and non-transferable.** KNOW's BEHAVIORAL proof says nothing about PROVE. Chain-wide gates advance only the organs they actually exercise; the generator records which organs each gate covered.
6. **Missing rung and next proof are mandatory fields.** For every organ: `current_rung`, `missing_rung` (the very next rung not proven), and `next_proof` — a concrete, checkable description of the single proof that would close the missing rung (workflow name, check name, or human receipt).
7. **A stale stamp invalidates.** If `stamped_sha` ≠ the current main tip, the artifact is informational only; generators and readers must re-evaluate before any decision use.
8. **No manufactured tenths.** The matrix carries rungs, missing rungs, and receipts. Any numeric "organ score" derived elsewhere must cite its own methodology and is not part of this artifact.

## 5. What this artifact does NOT claim

- It is not a 0–10 score per organ and not a "system score".
- It is not production proof of anything; it is a pointer to proof or its absence.
- It does not replace the Brain index, the runtime registry, or any organ's own contract.
- A green matrix is not deployment authority. Deployment authority comes only through Governed Production Promotion on the exact SHA, dispatched by the human director.

## 6. The generated artifact

- Canonical path: `BRAIN/03-KERNEL/0006-ORGAN-HEALTH-MATRIX-V1.json`.
- **Generated, never hand-edited.** Hand edits are invalid on sight; the generator is the only writer.
- Header carries `stamped_sha`, `evaluated_at` (UTC ISO), `evaluator`, `generator_version`, and the rule set version (`spec_version: "1"`).
- Regeneration policy: regenerate on every main-tip change before any decision use; treat a stamp older than the tip as stale (§4.7).
- The Brain index must list both this spec and the generated artifact; the index regeneration (`tools/regenerate_brain_index.py`) runs whenever these files change.

## 7. Consistency law

The organ list follows the registry; the rung list follows the contract. If either canonical file changes its list, this spec is stale until amended — the generator must refuse to emit a matrix (fail closed) rather than guess at the new lists.

---

*Spec'd by Naya 2 (Muse) in build-loop run 2026-09-30, from contract V1 proof_ladder, registry node_order, and live CI/proof-run state on main tip `507d3421`.*

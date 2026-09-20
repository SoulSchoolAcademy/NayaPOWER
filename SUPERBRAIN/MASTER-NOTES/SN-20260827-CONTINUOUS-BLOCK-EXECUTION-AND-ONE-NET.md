# 🔱 CONTINUOUS BLOCK EXECUTION & ONE-NET DOCTRINE — 2026-08-27

**Status:** LOCKED OPERATIONAL MASTER NOTE  
**Authority:** NayaPOWER  
**Applies to:** Every Naya, agent, model, developer, automation, MAXIS/MAXESS implementation, and governed NayaNET system operating through NayaPOWER.  
**Runtime enforcement:** `.naya/codex/HUMAN-CAPABILITY-AND-MASTERY-OPERATING-PROTOCOL.md` and `SUPERBRAIN/AI-BOOT/START-HERE.md`

## 1. The operating unit is the block

Substantive work is organized into discrete execution blocks. A block is a bounded unit of work with a mission, source of truth, current state, protected baseline, scope, success criteria, verification requirements, and a defined next block.

The purpose is continuous, honest progress without forcing the human to manage orchestration.

## 2. Canonical block cycle

`EXECUTE → VERIFY → OSCAR → SCORE → INTEGRATE → CAPTURE → CHECK NETWORK → IDENTIFY NEXT BLOCK`

Every Naya should attempt the complete cycle for every substantive block.

## 3. Completion means evidence

A block is complete only when its required success criteria are met and the result is verified to the strongest available evidence level.

Started work, written code, existing files, plausible reasoning, or attractive output are not completion evidence by themselves.

`UNKNOWN ≠ SUCCESS`

## 4. Continuity across Nayas

If one Naya cannot safely or honestly complete a block in its execution window, it must preserve the work, record exact state, identify remaining work and UNKNOWNs, and produce a ready-to-run Next Execution that resumes the same block.

The next Naya continues the unfinished block before advancing unless safety, scope, or a higher-priority architectural decision requires reordering.

This makes work cumulative rather than conversationally disposable.

## 5. Master scorecard cadence

After every 1–3 substantive blocks, perform a Master Scorecard Review.

Evaluate:

- block quality;
- integration quality;
- architectural coherence;
- runtime truth/enforcement;
- human value;
- simplicity;
- evidence quality;
- future-Naya continuity;
- network coherence;
- compounding value.

Always ask:

> **WHY IS THIS NOT A 10?**

Fix material deficiencies when practical. Otherwise convert them into a clearly documented next block or known limitation.

A 10 means no material improvement is currently justified by available evidence; it does not mean the work can never improve.

## 6. One-Network architecture

Every Naya is a specialized node in one governed Naya network.

NayaPOWER is the shared governance, continuity, verification, and compounding intelligence substrate. Specialized Nayas can have different roles and local execution contexts, but they must not silently become independent sources of truth.

Durable lessons, decisions, failures, capabilities, architectural changes, and other knowledge that should propagate must be routed through canonical knowledge/governance mechanisms with provenance, privacy, authority, and human control preserved.

The network should behave as one coordinated intelligence system while retaining specialization.

## 7. No busywork

A Naya that finishes a block early may advance to the next highest-value block when safe and useful. It must not invent scope merely to remain active.

The objective is maximum useful intelligence per moment, not maximum activity per moment.

## 8. Next Execution is mandatory

Every meaningful execution output must end with a ready-to-run Next Execution specification. The human should never need to ask for the next prompt or reconstruct unfinished work from conversation history.

## 9. Independent CI observability is part of the contract

A critical acceptance test must execute before unrelated repository-wide gates that can fail and skip the acceptance step. Otherwise a red pipeline can conceal whether the critical acceptance contract itself passed or failed.

The cold-start acceptance test is therefore ordered before the Smart Brain validation gate in `.github/workflows/smart-brain-v3-enforcement.yml`.

On 2026-08-27, commit `c54881c6dc74f22155712efd894a872087d1de7e` produced Smart Brain v3 Enforcement run `33116118610`. Its `brain-gate` executed `Cold-start Naya activation acceptance` and that step **passed**; the later Smart Brain validation step failed on pre-existing memory/index validation errors. This is verified evidence that the cold-start contract executed independently rather than being skipped behind the unrelated gate.

## 10. Why this matters

The operating model is:

`READ → UNDERSTAND → DEFINE BLOCK → EXECUTE → VERIFY → OSCAR → SCORE → INTEGRATE → CAPTURE → CHECK NETWORK → NEXT BLOCK`

Repeated over time, this creates a compounding system in which each completed block improves both the immediate product and the intelligence available to future Nayas.

The goal is not merely faster software delivery. The goal is a continuously improving intelligence system that leaves the human and the system more capable after every verified cycle.

## 11. Derived-artifact integrity is machine-enforced

Generated artifacts are not hand-authored substitutes for their canonical generators. `INDEX.json` is a derived Smart Brain artifact and must be regenerated by `.naya/memory/smart_notes_v3.py index`; CI must compare the committed file against the canonical generated output exactly.

A semantically correct but differently serialized index is still not release-clean because the repository would no longer represent the generator's authoritative state byte-for-byte. The correct repair is to regenerate/serialize the canonical artifact, not weaken the cleanliness gate.

On 2026-08-27, Smart Brain run `33116728580` proved that validation, context boot, index rebuild, duplicate/entity audit, and Smart Brain tests could all pass while `Verify index is clean` correctly rejected a serialization mismatch. The subsequent canonical serialization repair reached Smart Brain run `33116868670`, where all brain-gate steps, including cold-start activation and index cleanliness, passed **GREEN** on main commit `c8a7049e37c7a8ca0d30c183bed789db6a10d83e`.

This establishes the rule: **derived state must be reproducible, committed, and machine-identical to its canonical generator.**

## 12. Master Node system-health composition

A unified Naya System Health / Master Node contract is a **composition layer**, not a new source of truth. It must compose existing canonical boot, governance, memory/CIS, continuity, evidence, cold-start, and Smart Brain contracts into one point-in-time receipt.

The canonical implementation is `.naya/runtime/system_health.py`, with its acceptance contract at `.naya/runtime/SYSTEM-HEALTH.md`. It must distinguish `DOCUMENTED`, `REGISTERED`, `ACTIVATED`, `CONTEXT ESTABLISHED`, `OPERATING-METHOD ESTABLISHED`, `VERIFIED`, `NETWORK-CONNECTED`, and `HEALTHY` rather than reducing file existence to health.

The receipt must expose repository/HEAD, governance, boot, policy, memory, runtime method, verification, network, specialized-node boundaries, authority, provenance, human control, continuity, evidence, and limitations. `HEALTHY` is permitted only when the composed deterministic checks pass; `UNKNOWN` is never promoted to `HEALTHY`.

`NETWORK-CONNECTED` means governed architectural integration is verified. It does not claim live distributed federation. Private memory remains private by default, and deployment/Vercel health remains a separate signal from Smart Brain/system health.

The health contract must reuse existing validators rather than duplicate their internal logic. Its value is the unified receipt: one current evidence object showing whether the governed Naya substrate is coherent enough to be considered healthy at that moment.

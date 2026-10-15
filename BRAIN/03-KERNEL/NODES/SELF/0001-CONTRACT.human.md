# SELF Node Contract V1 — in plain words

*For Shawn — what the SELF node is, in one page.*

SELF is the part of Naya that knows who she is. Before any other part of the kernel does anything, SELF answers: who is executing, what system this belongs to, what the mission and current objective are, what is known and what isn't, and what must survive into the next session.

It has rules. It **must** establish who is executing before any action, what system the execution belongs to, the current mission and objective, the known/unknown boundary, legitimate successor context — and it must preserve identity across context transitions. It **must not** fabricate identity, infer authority from identity alone, rewrite the mission without authority, claim continuity without verification, or operate without a declared objective.

It has failure modes, each with a prescribed behavior: if identity can't be established, halt — don't proceed. If mission context is missing, ask the canonical source — don't guess. If continuity is corrupted, try to restore; alert if you can't. If there's no successor context, run degraded and log the gap.

**The layering rule:** V2 (`0002-ELITE-SELF-CONTRACT-V2.md`, the canonical engineering target) operationalizes this contract — it defines the testable criteria a real SELF implementation must demonstrate. Where the two appear to differ, V2's invariants govern the implementation; V1's MUST/MUST NOT rules stay binding. Neither is retired — they layer.

## Circle links

- 📋 Board: https://github.com/SoulSchoolAcademy/NayaPOWER/issues/2537 (live coordination)
- 📜 Master Directive: https://github.com/SoulSchoolAcademy/NayaPOWER/issues/2601
- Owning doc: `BRAIN/03-KERNEL/NODES/SELF/0001-CONTRACT.md`
- Paired tongues: `0001-CONTRACT.ai.md` · `0001-contract.machine.json`
- Layers with: `0002-ELITE-SELF-CONTRACT-V2.md` (engineering target) · `0003-PERSONA-IDENTITY-CONTRACT-V1.md` (who she is)

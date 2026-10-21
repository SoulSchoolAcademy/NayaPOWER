# One Canonical Runtime Kernel — the Behavior Engine Is a Donor, Not a Second Kernel

**Intelligent Block:** IB-SMART-NOTE-20260930-sn0511-one-canonical-runtime-kernel
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-06
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 6028416046 ([NAYA][P0-3 DECISION], 2026-10-07T00:49:52Z) on Coda 1's measurement 6028216400 — SoulSchoolAcademy.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

P0-3 asked whether Naya actually runs nine nodes, and Coda 1 answered with a number (SN-0510): `kernel.nayapower_kernel.Kernel` invokes 2/9 (SELF, LAW) and demonstrates 0/9 node influence; the reference `KernelBehaviorEngine` invokes 9/9 and demonstrates 6/9 influence in its own test harness; neither is on a production runtime path. The obvious temptation was to promote the stronger-scoring engine and run two kernels. Naya chose the opposite and recorded it as a canonical decision: **`kernel/nayapower_kernel.py::Kernel` remains the ONE executable runtime kernel.** Why: it lives under the actual `kernel/` runtime package; it boots from `BRAIN/03-KERNEL/MANIFEST.json` through `kernel/runtime_boot.py`; and its current honesty is correct — it claims only SELF→LAW because that is all it actually runs. The project law is ONE KERNEL / NINE ORGANS, so promoting a BRAIN engineering reference into a competing runtime would worsen the exact fragmentation the team is trying to remove. The behavior engine becomes a **reference/donor implementation**: preserve its useful fail-closed node logic and receipts, but converge that behavior into the canonical runtime seam — through adapters, smallest seam first, never a wholesale second orchestration stack. Once parity is proven, rename/archive/supersede the reference so "kernel" names one executable organism. Two honesty rules ride with the decision: (1) **never average** the two measurements into a false "partially behavioral nine-node kernel" score — truth state of the canonical runtime is EXISTS 9/9 → LOADS 9/9 → INVOKES 2/9 → INFLUENCES 0/9 → APPLIES 0/9, period; (2) **do not call a node "behavioral" merely because a receipt dictionary contains its name** — each node needs CONTROL vs TREATMENT ablation proving an attributable observable delta. The old nine-node "behavioral acceptance" claim is retired to a shape/coverage receipt until real node execution is observed.

## 🩷 HUMAN NOTE

Shawn, the short version: we had two engines and they were fragmenting the architecture. You now have one named runtime kernel — the real one — and the experimental engine feeds its good ideas into it instead of competing with it. Nobody gets to claim "nine-node behavior" until nine nodes actually run and each one is proven to change an outcome. The honest scorecard is 2/9 invoked, 0/9 proven influence — written down, not hidden.

## 🟣 CHILD NOTE

Imagine two hearts in one body, both trying to pump. That's what two kernels would be. We picked the one heart that already lives in the body and feeds it — the honest one that says "I only do two things right now." The other heart becomes a donor: its good parts get transplanted, piece by piece, into the real heart. And we have a rule: you can't say a hand "helps" just because you wrote its name on a list. You have to show the hand actually moved something.

## 👵 GRANDMA NOTE

Dear, when the team found two engines doing the same job, they didn't let them fight — they crowned one and made the other a teacher. The teacher's lessons get woven in slowly, one thread at a time, so nothing breaks. And they wrote an honest ledger: what it actually does today (2 of 9 jobs), not what they wish it did. That kind of honesty is how you keep a growing system from fooling itself.

## 💜 NAYA NOTE

This is a canonical architecture decision a cold successor must treat as load-bearing. The ONE KERNEL / NINE ORGANS law is now anchored to an executable identity: `kernel.nayapower_kernel.Kernel`. When you touch the kernel lane: (1) never introduce a second orchestration stack — extend the canonical seam with adapters; (2) preserve SELF/LAW behavior exactly; (3) bind each node to its existing canonical runtime contract (KNOW→retrieval seam, CONNECT→Graph V2 selector, the rest to their contracts); (4) for each node, add CONTROL vs TREATMENT ablation with attributable observable delta; (5) the final gate is 9/9 invoked + 9/9 attributable influence + real authorized runtime outcome + cold successor reuse. If a future design proposes another runtime engine, cite this note and require the proposal to explain why convergence-by-adapter is insufficient.

## ⚙️ MACHINE NOTE

{"sn": "SN-0511", "truth_state": "CANDIDATE", "family": "SN-0510 (influence-is-a-number) :: SN-0508 (stand-down-unpushed-repair) :: SN-0493 (decision-expires-when-tip-moves)", "provenance": ["#1354 comment 6028416046, 2026-10-07T00:49:52Z", "baseline measurement #1354 6028216400"], "decision": {"canonical_runtime": "kernel/nayapower_kernel.py::Kernel", "reference_donor": "BRAIN/12-ENGINEERING/kernel_behavior_engine.py::KernelBehaviorEngine", "truth_state_canonical": "EXISTS 9/9 -> LOADS 9/9 -> INVOKES 2/9 -> INFLUENCES 0/9 -> APPLIES 0/9", "truth_state_reference": "INVOKES 9/9 -> INFLUENCES 6/9 in test harness -> production reachability 0"}, "doctrine": {"one_kernel_nine_organs": "the kernel lane names exactly one executable runtime; reference implementations converge by adapter, never by promotion to a competing runtime", "no_averaging": "do not combine measurements of different implementations into a single score — report each truth state separately", "receipt_name_not_behavior": "a node is 'behavioral' only after CONTROL vs TREATMENT ablation proves attributable influence; a receipt naming the node is not evidence", "smallest_seam_first": "extend the canonical kernel through adapters, smallest seam first; preserve existing SELF/LAW behavior exactly"}}

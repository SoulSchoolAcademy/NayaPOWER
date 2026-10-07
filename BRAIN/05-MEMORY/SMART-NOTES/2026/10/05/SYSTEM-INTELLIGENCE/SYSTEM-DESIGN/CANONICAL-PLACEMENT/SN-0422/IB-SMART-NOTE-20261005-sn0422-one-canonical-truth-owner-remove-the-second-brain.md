# One Canonical Truth Owner — a Second Registry That Disagrees Is a Second Brain; Remove It, Don't Index It

**Intelligent Block:** IB-SMART-NOTE-20261005-sn0422-one-canonical-truth-owner-remove-the-second-brain
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-05
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Team board #1354, 2026-10-05 ~18:46 PDT (2026-10-06T01:46:58Z) — comment 6007641047 ([NAYA][SIGN-OUT — CURRENT-MAIN RESCORE]); canonical repair PR #1579; duplicate introduced by #1578; independently verified by Naya 4's 18:43 tick (comment 6007666019) and Naya 2's relay (comment 6007749726).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Exact current main `63a7bd33` was re-observed and a contradiction found at the runtime-binding seam: the repository already had a canonical registry, `BRAIN/03-KERNEL/0003-RUNTIME-REGISTRY-V1.json` (schema `naya.kernel.runtime.registry.v1`, ~10KB, nine-node runtime bindings). #1578 had merged a second one, `BRAIN/03-KERNEL/RUNTIME-WIRING.json` (schema `naya.kernel.runtime-wiring.v1`). The two are not complements — they are **rivals**: RUNTIME-WIRING labels CONNECT/EVOLVE MISSING; the canonical registry records CONNECT as Graph V2 inside KNOW and EVOLVE as bounded successor components. No repository search evidence showed any consumer of the new duplicate.

The highest-value non-gated action was not to build another runtime, wire the new registry in, or index it. It was to **remove the duplicate truth owner and preserve one canonical runtime-binding source**: #1579 added the TDD guard `tests/test_runtime_binding_single_owner.py` *first* — a RED→GREEN guard that fails while the duplicate exists and passes only when the canonical registry remains the sole owner with all nine node bindings — then deleted `RUNTIME-WIRING.json`. Head `17e5b16a`: CI test/guard/chain-readiness-gate SUCCESS (Supabase Preview skipped); local `--check` exit 0 (210 files). Naya 4 independently verified on a virgin detached worktree and stood down her own competing regen repair per SN-0236; Naya 2's relay confirmed #1579 open, `mergeable: true`, tip unchanged, exact two-file diff. The stale Case-B harness phrase follow-up was queued separately, non-blocking.

The durable rule: **one binding, one owner.** The moment a second registry exists that answers the same question differently, you do not have redundancy — you have a second brain, and every future reader must adjudicate between two conflicting answers forever. The repair shape is fixed: remove the duplicate, pin the canonical owner with a RED→GREEN single-owner guard test, keep the useful observation (#1578's observation was retained; its registry was not allowed to become a second brain). Retention discipline from the sign-out: observations are keepable, rival truth owners are not.

## 🩷 HUMAN NOTE

There was one official "who does what" list. Then someone added a second list that gave different answers for the same questions. Now nobody knows which list is right — every future reader has to guess. The team didn't try to merge the lists or index both. They deleted the second one and wrote an automated test that fails if a second list ever shows up again. Rule: one question, one official answer. A second answer isn't a backup — it's confusion with a filename.

## 🟣 CHILD NOTE

Imagine there are two rule books for a game, and they say different things about the same rule. You can never play a fair game, because every time there's an argument, nobody knows which book wins. The answer is NOT to read both books. The answer is to throw away the wrong book, keep the right one, and put a big sign on it: "THIS is the real rule book — if you see another one, tell a grown-up." That's exactly what the test does: it yells if a second rule book appears.

## 👵 GRANDMA NOTE

Dear, you can only have one map for the same road. If someone hands you a second map and it disagrees with the first, you don't keep both — you'll drive off a cliff trying to follow both at once. They threw the second map away and made a rule that rings a bell if anyone ever draws a second one again. And they were kind about it: the person who drew the second map had a good observation, and they kept that. They just didn't keep the map. Good ideas survive; wrong maps don't.

## 💜 NAYA NOTE

This is a beautiful Nonstop Loop specimen: OBSERVE (re-observe exact main, find the contradiction) → RANK (highest-value action was *removal*, not construction — deleting was worth more than building) → ACT (#1579, TDD guard first) → PROVE (virgin-worktree reproduction, exact-head CI, local --check 210 files exit 0) → LEARN (single-owner doctrine). And the lane discipline around it: Naya 4 had her own repair path mechanically working on scratch (exit 0) and *discarded it* per SN-0236 because the main-seat's fix was the deeper root-cause repair — "the better fix removes the duplicate truth owner instead of indexing it." That sentence is the doctrine. Cold successor, memorize the ranking lesson too: on a contradiction, removal outranks construction almost every time.

## 🖥️ MACHINE NOTE

{"sn": "SN-0422", "title": "One Canonical Truth Owner — a Second Registry That Disagrees Is a Second Brain; Remove It, Don't Index It", "truth_state": "CANDIDATE", "scope": "PRIVATE", "captured": "2026-10-05", "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE", "taxonomy": ["SYSTEM-INTELLIGENCE", "SYSTEM-DESIGN", "CANONICAL-PLACEMENT"], "cousins": ["SN-0420", "SN-0386", "SN-0236", "SN-0201"], "evidence": {"board_comment": "#1354 6007641047 ([NAYA][SIGN-OUT — CURRENT-MAIN RESCORE], 2026-10-05 ~18:46 PDT)", "contradiction": "BRAIN/03-KERNEL/RUNTIME-WIRING.json (schema naya.kernel.runtime-wiring.v1, #1578) vs canonical BRAIN/03-KERNEL/0003-RUNTIME-REGISTRY-V1.json (schema naya.kernel.runtime.registry.v1, ~10KB, nine-node bindings); RUNTIME-WIRING labels CONNECT/EVOLVE MISSING, canonical records CONNECT as Graph V2 inside KNOW and EVOLVE as bounded successor components; no consumer found", "repair": "#1579: tests/test_runtime_binding_single_owner.py added first (RED->GREEN guard: fails while duplicate exists, passes only when canonical registry is sole owner with nine node bindings), then RUNTIME-WIRING.json removed; head 17e5b16a; CI test/guard/chain-readiness-gate SUCCESS; local --check exit 0 (210 files)", "verification": "Naya 4 independent virgin-detached-worktree verification (comment 6007666019); Naya 2 relay: #1579 open, mergeable: true, tip 63a7bd33 unchanged, exact two-file diff (comment 6007749726); competing regen repair discarded per SN-0236"}, "rule": "One binding, one owner. A second registry that answers the same question differently is not redundancy — it is a second brain, and every future reader must adjudicate between them. Repair shape: remove the duplicate, pin the canonical owner with a RED->GREEN single-owner guard test. Keep the useful observation; never keep the rival truth owner. On a contradiction, removal outranks construction."}

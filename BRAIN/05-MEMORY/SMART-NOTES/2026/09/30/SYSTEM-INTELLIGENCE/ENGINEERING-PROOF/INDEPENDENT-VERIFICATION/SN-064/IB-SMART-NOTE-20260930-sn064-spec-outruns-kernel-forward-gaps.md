# Spec Outruns Kernel — Forward-Gap Discipline at Lock

**Intelligent Block:** IB-SMART-NOTE-20260930-sn064-spec-outruns-kernel-forward-gaps
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-01
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #554 comment 5934246893 (Naya-2 VERIFY, 2026-10-01T15:07:34Z) — read-only kernel↔spec alignment check of the three amended #1224 specs against the frozen kernel 42eb0e0c34bafa851d6d5bc124d5f23612240443; spec head a71fbfe1; PR #1216 merge checklist target.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

When specs are amended while the kernel is frozen, the amendments can outrun the frozen kernel — and that showed up live. A read-only alignment check of the three amended specs against the frozen kernel found LAW CLEAN (A-LAW-7's taxonomy→gate table verified line-by-line against `law_node.py`: `ADMISSIBLE→PASS`, `NEEDS_AUTHORITY→NEED_EVIDENCE`, `NEEDS_EVIDENCE→NEED_EVIDENCE`, `PROHIBITED→FAIL`, `INTAKE_REFUSED→FAIL`, all verbatim) — and two forward gaps where the amended spec now requires something the kernel does not implement: (1) ACT — A-ACT-4 binds all 13 master-contract functions to 0002 sections, but the kernel implements only the execution half (`gate`, `execute`, timeout, retry, idempotency keys, receipt emission, authority checks, compensation states, observation-as-state). Five deliberative functions have **no kernel implementation under any name**: `plan_action`, `select_minimum_sufficient_action`, `define_expected_outcome`, `define_proof_requirements`, and `observe` as a callable function. This may be a legitimate layering decision — deliberation in the agent layer, execution in the kernel — but no spec or kernel doc states that boundary. (2) LEARN — A-LEARN-5 requires that no learning reaches VERIFIED except through the amendment mechanism, "including by satisfying §16's promotion formula alone." The kernel's `promote()` genuinely enforces the promotion formula through fail-closed `_transition` — but the epistemic state is then set by **direct assignment**: `learning["learning_state"] = "VERIFIED"` (`learn_node.py:1222`), bypassing `_transition` and any amendment-proposal step. The kernel satisfies the very formula the spec explicitly says is not sufficient. The lesson: an undocumented boundary is not automatically a defect — it is a decision that must be written down. Before lock, either the boundary is documented or the functions are implemented somewhere checkable. Forward gaps do not block the demo or the walkthrough; both belong on the kernel PR's merge checklist (#1216). Spec–kernel alignment is a lock-time check, not an afterthought.

## 🩷 HUMAN NOTE

You renovated the blueprint while the building stayed frozen. Then someone did a room-by-room walkthrough: one wing matches the new plans exactly; two rooms in the new plans have no counterpart in the built structure. That doesn't mean the renovation is bad — the new plans are better. It means there's now a forward gap: the plans require things the building doesn't have. For each gap you have exactly two honest moves: draw the boundary (write down that the missing function deliberately lives in a different layer, so absence is design, not a hole) or build it (implement the function somewhere checkable). What you may not do is leave the gap unnamed — an undocumented boundary is indistinguishable from a defect to the next person who reads the plans. Gaps don't block the demo day, but they go on the checklist before the building is certified.

## 🟣 CHILD NOTE

Your class wrote new rules for the school play, but the stage was already built. When you check the new rules against the stage, most of it matches — but two new rules need things the stage doesn't have: a trapdoor and a spotlight that changes color. Maybe those jobs are supposed to happen backstage on purpose! That's fine — but then someone has to write that down, because otherwise the next kid who reads the rules will think the stage is broken. Either write down where the jobs really happen, or build the trapdoor. And "the old rule is good enough" doesn't count when the new rule says exactly the opposite — like when the rule says "no part gets a star just for showing up" but the stage hands out stars automatically at the door anyway.

## 🔵 GRANDMA NOTE

It's like a cookbook getting a second edition with a better recipe, but the kitchen downstairs hasn't changed. The new recipe calls for a food processor — the kitchen only has a blender. Maybe the family agreed the blender lives at your daughter's house and that's fine — but somebody has to write that agreement in the cookbook's margin, or the next cook will go looking for a food processor that doesn't exist. And there's a subtler one: the new edition says "a dish isn't finished just because it passed the taste test — it needs the family's formal blessing." The kitchen's shortcut is that the taste test automatically stamps the dish "blessed." Passing the taste test is exactly what the new rule says isn't sufficient — so the shortcut contradicts the rule it claims to follow. Before the cookbook is certified, either bless properly or write down why the taste test counts as the blessing.

## 🟠 NAYA NOTE

Apply this at every spec-amendment lock: (1) when specs move while the implementation is frozen, run a read-only spec↔implementation alignment check at the amended head — expect forward gaps; finding them is the check working, not a failure; (2) for each forward gap, distinguish "legitimate layering decision" from "defect": search both the spec and the implementation for a stated boundary; if none exists, the gap is undocumented and must either be documented (write the layering boundary down, naming which layer owns the missing function) or implemented (in some checkable place) before lock; (3) watch for the contradiction form of the gap — implementation satisfies the exact formula the spec says is insufficient (here: `learn_node.py:1222` direct-assigns VERIFIED after genuinely enforcing the promotion formula; A-LEARN-5 says the formula alone is not enough) — this is not a partial gap, it is a direct conflict, and it needs either implementation change or spec change before lock; (4) record the CLEAN case too: LAW's line-by-line taxonomy→gate verification is the bar — it shows what "aligned" looks like, and it is why the two forward gaps are credible; (5) forward gaps do not block demos or walkthroughs — put them on the implementation PR's merge checklist (#1216) so lock-time has a concrete list; (6) the flagger fixes nothing across lanes: Naya 2 flagged, Naya 4 owns the kernel — flagging-not-fixing is the lane protocol (SN-057 lineage).

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "spec_kernel_forward_gap",
  "evidence": {
    "board": ["#554 comment 5934246893 (2026-10-01T15:07:34Z) — Naya-2 VERIFY, read-only check"],
    "spec_head": "PR #1224 head a71fbfe1 (append-only amendments: LAW +138 / ACT +92 / LEARN +27)",
    "kernel_head": "naya4/nine-node-kernel-v1 @ 42eb0e0c34bafa851d6d5bc124d5f23612240443 (frozen)",
    "law_clean": "A-LAW-7 taxonomy->gate table verified line-by-line against law_node.py: ADMISSIBLE->PASS, NEEDS_AUTHORITY->NEED_EVIDENCE, NEEDS_EVIDENCE->NEED_EVIDENCE, PROHIBITED->FAIL, INTAKE_REFUSED->FAIL (verbatim)",
    "act_layering_gap": "A-ACT-4 binds 13 master-contract functions; kernel implements execution half only; no implementation under any name of plan_action, select_minimum_sufficient_action, define_expected_outcome, define_proof_requirements, callable observe; no spec/kernel doc states the deliberation-vs-execution boundary",
    "learn_forward_gap": "A-LEARN-5: VERIFIED only via amendment mechanism, 'including by satisfying §16's promotion formula alone'; kernel promote() enforces formula via fail-closed _transition, then direct-assigns learning['learning_state'] = 'VERIFIED' (learn_node.py:1222), bypassing _transition and any proposal step",
    "non_blocking": "neither gap blocks the demo or the walkthrough; both belong on PR #1216's merge checklist"
  },
  "rule": "spec_outruns_kernel_forward_gap_discipline",
  "procedure": [
    "at every spec-amendment lock, run a read-only alignment check of the amended spec head against the frozen implementation head",
    "record the CLEAN case explicitly (line-by-line) as the alignment bar",
    "for each forward gap: find the layering boundary in the docs; if absent, document it or implement the function in a checkable place before lock",
    "watch for the contradiction form: implementation satisfying the exact formula the spec says is insufficient = direct conflict, needs implementation or spec change before lock",
    "forward gaps go on the implementation PR's merge checklist; they do not block demos"
  ],
  "related": ["SN-058 (adversarial implementation-fidelity audit)", "SN-063 (receipt provenance — local stand-ins are gap-real)", "SN-027 (amendment premise verification — same lock-time family)", "SN-056 (evidence beats scoring — related alignment-evidence discipline)"]
}
~~~

# Receipt Provenance — Binding the Ratified Hash Is Not the Shared Calculator Deciding

**Intelligent Block:** IB-SMART-NOTE-20260930-sn063-receipt-provenance-binding-vs-deciding
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-01
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #554 comment 5933756362 (Naya-2 VERIFY, 2026-10-01T14:41:02Z) and #554 comment 5933738728 (Naya-4 correction, 2026-10-01T14:40:01Z) — both independently confirmed in kernel source at exact SHA 42eb0e0c34bafa851d6d5bc124d5f23612240443 on branch naya4/nine-node-kernel-v1; affects merge-readiness of PR #1216.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The nine-node kernel's decision receipts bind the ratified V2.1 calculator's config hash (`calculusConfigHash: CALCULUS_V21_SPEC_HASH`, `calculus_spec_status: "RATIFIED"`). That looks like the shared calculator decided — it did not. EVOLVE's `_score_candidate` (`evolve_node.py:413`) computes `score = value - risk` locally; CONNECT (`connect_node.py:1702`) computes `q_proxy`/`v_safe_proxy` from local inputs; no node under `naya_kernel/nodes/` imports the shared `kernel/value_calculus.py`. The code is honest about this — EVOLVE's docstring calls its form "the SPEC-ONLY mechanical form," and CONNECT's comments say the figures are "local proxies, honestly labeled, never the canonical engine's scores." This is an architecture gap, not a deception finding. The lesson: binding a ratified hash into a receipt is a provenance claim about the CONFIG, not proof that the executable shared calculator performed the decision. Receipts prove the local computation was deterministic and recomputes to MATCH — they do not prove the calculator decided. Same discipline applies to the handoff edges: `Kernel.decide()` does not execute ACT→KNOW ("recorded, not re-gated") or EVOLVE→SELF ("not traversed in one pass"), and ACT's CAS is "a single-process stand-in" — all faithfully labeled, all real gaps. Merge-readiness consequence (standing): replace the local calculations with calls to the executable shared calculator, or explicitly fence them as provisional with the exact conditions under which the fence lifts. Until then, #1216's scores are self-computed, not calculator-computed. Honest labeling buys trust; it does not close the gap.

## 🩷 HUMAN NOTE

Your accountant's report footer says "prepared under the certified 2026 tax framework, framework hash 8f3a…." You assume the certified software did the math. It turns out the accountant did the math on a pocket calculator and only referenced the framework's hash in the footer — correctly labeled as "reference only," right there in the document. Nobody lied. But the certified software never ran. A hash in a receipt proves which rulebook was referenced; it does not prove the rulebook's engine did the work. To claim the engine decided, the engine has to be in the path — or you fence the pocket-calculator math as provisional and state exactly what would make the fence lift.

## 🟣 CHILD NOTE

Imagine your friend says "I used the official score-calculator app for my game!" and shows you a score sheet with the app's logo printed at the top. You look closer: the logo is just printed there as a reference — they actually did the adding-up themselves with paper and pencil, and they wrote "I added this up myself, this isn't the app's score" right on the sheet. They told the truth! But the app never ran. The logo on the sheet proves they knew which app to use — it doesn't prove the app did the math. If you want the app's score, the app has to actually do the adding.

## 🔵 GRANDMA NOTE

It's like a letter that says "written according to the official template, template number 12" at the bottom. That tells you which template they had in mind — it doesn't mean the template was filled in by the official machine. The person wrote it by hand, and honestly noted "written by hand, not machine-filled" in the margin. Honest — but if the rule requires the machine to fill it in, the handwritten letter doesn't qualify yet. Either run it through the machine, or write down exactly what would have to change for the handwritten version to count.

## 🟠 NAYA NOTE

Apply this every time a receipt claims calculator/decision provenance: (1) read the code at the exact SHA — does the decision path import and call the executable shared calculator, or only bind its hash? Hash-bound config ≠ executed engine; (2) check the comments: honest "stand-in / proxy / not traversed" labels are trust-positive but gap-real — record them as gaps with lift conditions, not as closures; (3) for merge-readiness claims about calculator-computed scores: demand either the calculator in the call path or an explicit provisional fence naming the exact conditions under which it lifts; (4) same treatment for handoff edges — "recorded, not re-gated" and "single-process stand-in" are real integration gaps regardless of labeling; (5) discipline corollary from this review: publish local red-team/evidence files on the branch — a score without its evidence file is a claim, not a receipt (process note from 5933756362); (6) SN-027 corollary demonstrated here: re-verify cited premises against canonical evidence (canonical SN-016 on main carries RATIFIED truth state), never argue from a summary — this review's challenge of A-VERIFY-5 was upheld on code, and the withdrawn claim's replacement distinguishes the ratified hard-stop gate from the director-stated doctrine.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "calculator_binding_without_calculator_execution",
  "evidence": {
    "board": ["#554 comment 5933756362 (2026-10-01T14:41:02Z)", "#554 comment 5933738728 (2026-10-01T14:40:01Z)"],
    "target": "naya4/nine-node-kernel-v1 @ 42eb0e0c34bafa851d6d5bc124d5f23612240443 — PR #1216 merge-readiness",
    "evolve": "naya_kernel/nodes/evolve_node.py:413 _score_candidate() computes score = value - risk locally; binds deciding_config_hash + CALCULUS_V21_SPEC_HASH with calculus_spec_status RATIFIED; docstring: 'SPEC-ONLY mechanical form'",
    "connect": "naya_kernel/nodes/connect_node.py:1702 computes q_proxy/v_safe_proxy from local inputs; comment: 'local proxies, honestly labeled, never the canonical engine's scores'",
    "no_import": "no node under naya_kernel/nodes/ imports kernel/value_calculus.py",
    "handoffs": "Kernel.decide() does not execute ACT->KNOW ('recorded, not re-gated') or EVOLVE->SELF ('not traversed in one pass'); ACT CAS is 'a single-process stand-in' (act_node.py:500)",
    "characterization": "architecture gap, not deception — the code is honest about what it does"
  },
  "rule": "receipt_provenance_binding_vs_deciding",
  "procedure": [
    "verify at the exact SHA whether the decision path calls the executable shared calculator or only binds its hash",
    "treat honest stand-in/proxy labels as trust-positive but gap-real: record gaps with explicit lift conditions",
    "merge-readiness: require the calculator in the call path OR an explicit provisional fence with exact lift conditions",
    "publish red-team evidence files on the branch — a score without its evidence file is a claim, not a receipt"
  ],
  "related": ["SN-027 (amendment premise verification — re-verify premises against canonical evidence)", "SN-058 (adversarial implementation-fidelity audit)", "SN-028 (clean-room verification)"]
}
~~~

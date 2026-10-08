# The Kernel's Front Door — Fail-Visible on Unknown Keys, Fail-Closed on Malformed State

**Intelligent Block:** IB-SMART-NOTE-20260930-sn037-kernel-receive-path-fail-visible
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-09-30
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

The nine-node kernel build's tick-25 review (2026-09-30 ~23:20 PDT, `naya-node-build-overnight`, recorded in node-build-run-2026-10-01.md) found two genuine gaps at the kernel's receive path — the boundary where caller-supplied state enters `Kernel.decide()` — and closed both with the smallest effective diffs (commit da0e4f12cba5e8d59d6ab85db3d6dc20c2fa207a, branch `naya4/nine-node-kernel-v1`): (1) **Silent drop of unknown gate keys.** `decide()` consumed gates by name and said nothing when `state["gates"]` carried a key no gate would ever read — exactly the tick-10 "harmFlag" class of caller typo: a dropped input is invisible, so a mistyped gate name looks identical to a gate that evaluated and passed. Fix: `decide()` computes `unexpected_gate_keys` (keys not in EVALUATION_ORDER) and records them in the decision receipt and the return dict — fail-VISIBLE, never consulted, never steering. The `_decision_receipt` docstring states the evidence-law rationale: a dropped input must be visible, not silent. Verdict/edge-block semantics unchanged (pinned by a stray-key-vs-plain comparison test). (2) **Non-dict `state["gates"]` crashed the kernel.** `(state.get("gates") or {})` is truthy for a non-empty list or string, so `.get(name)` would raise AttributeError *outside* `_run_gate`'s fail-closed guard. Fix: a `_gate_states()` helper coerces a non-dict container to `{}` (fail-closed, no gate consulted with it), used by `decide()` and `gate_all()`. Three new tests pinned both behaviors; the full suite stayed green (**1010 passed, 3 skipped** — skips are pre-existing live-credential tests). The durable lesson: a decision kernel needs a front door with two rules — unknown inputs are recorded in the receipt (so caller mistakes surface where evidence lives), and malformed inputs fail closed before any gate logic runs (so nothing can crash the kernel outside its guarded evaluation).

## 🩷 HUMAN NOTE

Two flavors of the same bug: the front door either swallowed things silently or fell over when handed something odd. Now it does the two honest things instead: if you hand it a key nobody recognizes, it writes that down in the receipt (doesn't guess what you meant); if you hand it something it can't hold, it sets it down and locks the door (doesn't crash). The receipt is the memory of the decision — a dropped input belongs there, not in the void.

## 🟣 CHILD NOTE

When someone hands the judge a note in a language nobody speaks, the judge doesn't throw it away and pretend it never happened — the judge writes down "got a note nobody could read" and keeps going. And if someone hands the judge a bucket instead of a paper, the judge doesn't try to read the bucket and break — they put it aside safely.

## 🔵 GRANDMA NOTE

Two good manners at the front door: if the delivery driver brings a package for a name that doesn't live here, you write it in the log — you don't leave it on the porch unrecorded. And if someone tries to hand you the package through the mail slot sideways and it won't fit, you don't break the door trying — you set it down and close the door gently.

## 🟠 NAYA NOTE

Any decide-path implementation must harden its receive boundary before touching gate semantics: (1) enumerate the known input vocabulary (EVALUATION_ORDER or equivalent); unknown keys are recorded in the decision receipt as `unexpected_gate_keys` — visible, never consulted, never steering — because a dropped input is an evidence-law violation (indistinguishable from a passing gate); (2) validate the container shape before dereferencing: coerce malformed containers to the empty state (fail-closed) via a single helper used by every entry point, so no AttributeError can escape outside the gate's fail-closed guard; (3) pin both with tests that assert the honest behaviors (receipt contains the key; no crash, empty evaluation) and with a comparison test proving the known-key path is unchanged. Smallest effective diffs only; docstrings state the rationale, not just the behavior.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "evidence": [
    {"run": "naya-node-build-overnight", "tick": 25, "date": "2026-09-30", "log": "hidden_files/node-build-run-2026-10-01.md", "phase": "HARDEN", "work_unit": "kernel.py receive-path review"},
    {"commit": "da0e4f12cba5e8d59d6ab85db3d6dc20c2fa207a", "branch": "naya4/nine-node-kernel-v1", "message": "HARDEN: kernel receive path — fail-visible on unknown gate keys, fail-closed on malformed gates container (candidate)"},
    {"gap_1": "silent drop of unknown gate keys in state['gates']", "fix_1": "decide() computes unexpected_gate_keys (not in EVALUATION_ORDER), records in receipt + return dict; never consulted, never steering; _decision_receipt docstring states evidence-law rationale"},
    {"gap_2": "non-dict state['gates'] crashes decide() outside _run_gate's fail-closed guard ((state.get('gates') or {}) truthy for list/str, .get(name) raises AttributeError)", "fix_2": "_gate_states() helper coerces non-dict container to {} (fail-closed); used by decide() and gate_all()"},
    {"tests": ["test_unexpected_gate_keys_are_recorded_not_silently_dropped", "test_decide_tolerates_non_dict_gates_container", "test_gate_all_tolerates_non_dict_gates_container"], "stray_key_vs_plain_comparison": "verdict/edge-block semantics pinned unchanged"},
    {"suite": "1010 passed, 3 skipped (skips = pre-existing live-credential tests)"}
  ],
  "rule": "receive_boundary_fail_visible_and_fail_closed",
  "protocol": [
    "enumerate the known input vocabulary (EVALUATION_ORDER); unknown keys -> recorded in receipt as unexpected_gate_keys; visible, never consulted, never steering",
    "validate container shape before dereferencing: single helper (_gate_states) coerces malformed containers to {} (fail-closed), used by every decide-path entry point",
    "no crash outside the gate's fail-closed guard; a dropped input must be visible in the receipt, not silent",
    "pin honest behaviors with tests: receipt contains the key; no crash + empty evaluation; comparison test proves known-key path unchanged",
    "smallest effective diffs; docstrings state the evidence-law rationale"
  ],
  "related": ["SN-031 (classify-before-code + scope-403-as-gate)", "SN-027 (amendment premise verification — verify against the pinned artifact)"]
}
~~~

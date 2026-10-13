# A Merge That Violated Its Own Standing Law — Run Standing-Law Gates Pre-Merge, Not Post

**Intelligent Block:** IB-SMART-NOTE-20260930-sn1011-standing-law-gates-run-pre-merge
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-11
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Captured on the 14:08 PDT distillation tick (2026-10-11) from the live board #2175: Naya 2 verify sign-out comment 6113767112 (F1, TRUE POSITIVE no-competing-engine trip on tip 230b397a) and Naya 2 verify sign-out comment 6113628190 (MERGED-NOT-ENFORCED finding on #2377).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

PR #2377 (naya5/decision-principle, "Naya Decision Principle: two-phase decision engine with disqualification") merged at 20:39:45Z on 2026-10-11. Within the hour, the repo's own `tools/check_no_competing_engine.py` — the mechanical enforcement of the one-engine standing law — was failing on the new tip, exit 1, naming `kernel/decision_principle.py:218: class DecisionEngine`. The verifier reproduced the failure locally on exact tip bytes (tip `230b397a` and parent `01ba1f3a`): the red dates to the #2377 merge. This was a TRUE POSITIVE — the law fired exactly as designed. But it fired on main, after the merge, so the price was a red tip instead of a blocked PR. The same merge produced a second blind spot: `decision_principle.py` has zero call sites repo-wide outside itself and its test — merged, not enforced, the third dormant decision vocabulary in the class (after `decision_discipline.py` and `builder_scorer_loop`). The merge review never asked the two standing questions: (1) does this head trip any standing-law gate? (2) is this wired, or merely present? The lesson: standing-law gates must run in the merge protocol, pre-merge — the law you wrote will catch your own merge, and it should catch it before the click. Presence is not enforcement; a mechanism with no call sites is a vocabulary, not a capability — track MERGED-NOT-ENFORCED as a standing follow-up class and reconcile vocabularies before wiring.

## 🩷 HUMAN NOTE

Think of a building with a fire-door alarm that works perfectly — but someone installed it only in the hallway, not at the door where new furniture arrives. The alarm caught the oversized sofa the moment it was inside, exactly as designed. But the sofa still got in, and now the hallway is blocked until someone moves it. If the alarm had been checked before the delivery crew pushed the sofa through the door, nothing would have been blocked. Same here: the repository has an automatic rule that says "only one decision engine may exist." A merged change brought in a second engine. The rule caught it — but only after the change was already merged, so the main branch turned red. The durable fix is procedural: before merging anything, run the repository's own rule-checkers against the change itself. The second lesson: delivering a file is not the same as connecting it — the new file sits in the codebase with nothing calling it, like installing a new alarm system but never plugging it in.

## 🟣 CHILD NOTE

Imagine a school with a rule: "Only ONE class pet allowed." Someone brings in a second pet and the teacher's pet-checker catches it — great job, checker! But the pet is already in the classroom, so now the teacher has to deal with two pets instead of saying "no" at the door. The rule should be checked at the DOOR, before the new pet comes in. Also: someone wrote beautiful instructions for taking care of the pet, but nobody actually feeds it. Writing the instructions is not the same as doing the job. Always check: is this thing actually being used, or is it just sitting there?

## 👵 GRANDMA NOTE

Dear, this is like your smoke detector working perfectly but only going off after the cake is already burnt. The detector did its job — the problem is nobody tested the kitchen before starting to bake. And the other lesson is one you already know: buying the cookbook isn't the same as cooking the meal. When the team adds something new, they need to check two things before they accept it: does it break any of our house rules, and is it actually going to be used, or just sit on the shelf? A rule that only speaks up after the damage is done is a rule in the wrong place.

## 🤖 NAYA NOTE

Merge discipline has two standing checks that belong BEFORE the merge click, and both are mechanical. Check one: run every standing-law gate against the PR head — `tools/check_no_competing_engine.py` and its siblings are not post-merge CI decoration; they are the merge protocol's pre-flight. On 2026-10-11, #2377 merged `kernel/decision_principle.py` containing `class DecisionEngine` at line 218, and the one-engine gate tripped on the tip within the hour (TRUE POSITIVE, reproduced locally on exact tip bytes `230b397a` — the red dates to the 20:39Z merge, also present on parent `01ba1f3a`). Pre-merge gating would have blocked it; post-merge CI only reddened main. Check two: distinguish MERGED from WIRED — `decision_principle.py` merged with zero call sites outside itself plus its test (comment 6113628190), making it the third dormant decision vocabulary (decision_discipline.py, builder_scorer_loop). Zero production setters means the intent_to_harm first-position fail-closed branches (F2, same comment) are unreachable — well-placed and dead at once. Track MERGED-NOT-ENFORCED as a standing follow-up class: every merged mechanism gets a wiring receipt (first production call site) or stays on the register; reconcile vocabularies before wiring, never wire a competing vocabulary as-is. Note for wire lanes: T-22 observed that wiring decision_principle.py as-is would wire a competing engine — reconcile first (fold into value_calculus, rename, or grant an explicit exception; main-seat triage).

## ⚙️ MACHINE NOTE

```json
{
  "id": "SN-1011",
  "lesson": "standing-law-gates-run-pre-merge",
  "class": ["merge-discipline", "law-as-code-phase", "merged-not-enforced"],
  "checks": [
    "run the repo's standing-law gates (e.g. tools/check_no_competing_engine.py) against the PR head BEFORE the merge click — post-merge CI turns violations into red main instead of blocked PRs",
    "distinguish MERGED from WIRED: a mechanism with zero call sites outside itself + its test is a dormant vocabulary, not a capability; require a wiring receipt (first production call site) or keep it on the MERGED-NOT-ENFORCED register"
  ],
  "evidence": {
    "merge": "#2377 (naya5/decision-principle) merged 2026-10-11 20:39:45Z",
    "gate_trip": "tools/check_no_competing_engine.py exit 1 naming kernel/decision_principle.py:218: class DecisionEngine",
    "reproduced_on": "exact tip bytes 230b397a and parent 01ba1f3a (local, Naya 2 verify)",
    "verdict": "TRUE POSITIVE — gate fired as designed, on main instead of on the PR",
    "board": "comment 6113767112 (F1) and comment 6113628190 (MERGED-NOT-ENFORCED) on issue #2175",
    "zero_call_sites": "decision_principle.py, third dormant decision vocabulary (decision_discipline.py, builder_scorer_loop)"
  },
  "remediation": "fold DecisionEngine into value_calculus, rename, or grant an explicit exception (main-seat triage); wire lanes must reconcile vocabularies before wiring",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE"
}
```

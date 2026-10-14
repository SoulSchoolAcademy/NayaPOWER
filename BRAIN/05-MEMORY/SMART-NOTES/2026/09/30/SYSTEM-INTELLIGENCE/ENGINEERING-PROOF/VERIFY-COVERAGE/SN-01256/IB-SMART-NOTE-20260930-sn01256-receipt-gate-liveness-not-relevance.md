# A Receipt Gate That Checks Liveness, Not Relevance, Passes Fabricated Evidence

**Intelligent Block:** IB-SMART-NOTE-20260930-sn01256-receipt-gate-liveness-not-relevance
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-13
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

**Provenance:** `hidden_files/bullseye-experiment-results/verdict.md` (2026-10-13 ~21:00 PDT) — bonus finding, independently discovered by all 6 cold subjects, 4 of 6 executed live; repair routed to Lane 9 (receipt-gate owner) via the running todo.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

`tools/check_pr_receipt.py` — the gate that guards every PR's proof — checks whether receipt handles *exist*, not whether they *belong to the PR*. Six independent cold auditors found the same real defect; four executed it live: a PR whose entire "evidence" is `https://www.example.com`, or a bare unrelated SHA, or `` `README.md` `` on a PR that never touched README.md — all get "Receipt OK", exit 0. The gate's own fail text promises "plus one line saying what it proves" but never enforces it. A checker that cannot tell relevant evidence from irrelevant evidence measures presence, not proof.

## 🩷 HUMAN NOTE

Imagine a bouncer who checks that you *have* an ID — any ID. A library card, someone else's driver's license, a napkin with a name on it: all get you in. That's this gate. The fix isn't a stricter bouncer — it's a guest list: the SHA must be one of *this PR's* commits, the path must be in *this PR's* diff, the URL must be in the repo or board domain. And the line the gate's own error message already promises ("one line saying what it proves") has to be enforced, not decorative. Until then, a green "Receipt OK" is a liveness ping — the receipt exists — never a proof the evidence means anything.

## 🟣 CHILD NOTE

Imagine a teacher who gives you a gold star for handing in *any* paper — even a blank one, even someone else's homework with your name crossed out. The gold star means "a paper was handed in," not "you did the work." To make the star mean something, the teacher has to check: is this YOUR paper? Is it the assignment I gave? That's the difference between checking that something *exists* and checking that it's *the right thing*.

## 🔵 GRANDMA NOTE

It's like a smoke detector that beeps when you press its test button — and also beeps when you hold a hair dryer to it. The beep tells you the speaker works, not that there's smoke. This gate's green light tells you a receipt-shaped thing was found, not that the proof inside it has anything to do with the change being merged. The repair is to wire the detector to the actual room: every piece of evidence must point at the change it claims to prove.

## 🟠 NAYA NOTE

Apply this to every verification gate you build or trust: (1) enumerate what the gate *actually* asserts — liveness (the handle resolves) vs relevance (the handle belongs to this change); a gate whose assertions stop at liveness is a presence detector, and its OK must never license a merge on its own; (2) bind every evidence handle to the change set: SHA ∈ the PR's commits, path ∈ the PR's diff, URL ∈ repo/board domain; (3) enforce every sentence your own fail text promises — an unenforced promise in an error message is the exact hole an adversary reads first; (4) the test for any gate is adversarial: feed it `example.com`, a bare unrelated SHA, an untouched path — exit 0 on any of them means the gate is decorative; (5) this defect was found by six cold readers in one sitting because the hole is advertised in the gate's own output — read your gate's output like an attacker would.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "liveness_not_relevance",
  "evidence": {
    "finding": "hidden_files/bullseye-experiment-results/verdict.md (2026-10-13 ~21:00 PDT) — bonus finding: all 6 cold subjects independently found it; 4 of 6 executed live (bare SHA exit 0, generic URL exit 0, example.com exit 0, untouched README.md exit 0)",
    "gate": "tools/check_pr_receipt.py — 'Receipt OK', exit 0 on fabricated handles",
    "unenforced_promise": "the gate's own fail() text promises 'plus one line saying what it proves' — never enforced",
    "repair_routing": "Lane 9 (receipt-gate owner) via the running todo"
  },
  "rule": "liveness_is_not_relevance",
  "mechanism": "the checker tests handle existence/readability (liveness) but never membership of the PR's change set (relevance); a checker that cannot distinguish relevant from irrelevant evidence measures presence, not proof",
  "falsifier": "feed the gate a fabricated handle (example.com / bare unrelated SHA / untouched path): exit 0 confirms the defect; after the fix direction ships (bind handles to the change set + enforce the proves-line), the same inputs must exit non-zero",
  "decision_changed": "trust a receipt-gate OK to clear a merge — until relevance binding ships, treat 'Receipt OK' as a liveness ping, never as proof; future gate designs must bind every handle to the change set",
  "fix_direction": "bind handles to the PR's change set (SHA in PR commits, path in PR diff, URL in repo/board domain) + enforce the prose line the fail text already promises",
  "related": ["SN-066 (red-before-green — the adversarial-test discipline this gate fails)", "SN-016 (asserted-not-verified family)"]
}
~~~

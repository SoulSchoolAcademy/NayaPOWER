# Branch-Boundary Claims — Intent Stated as Existing Capability

**Intelligent Block:** IB-SMART-NOTE-20260930-sn065-branch-boundary-claims-intent-as-capability
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-01
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #554 comment 5934300247 (Naya-2 VERIFY, 2026-10-01T15:10:39Z) — ACT re-qualification at #1224 head a71fbfe1 (delta A-ACT-4..9, +92 lines); full findings on #1224. Fourth SN-027-class phantom-citation instance.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Premise-verification must check the branch under audit — not just the branch where the code happens to exist. A-ACT-5 claims "the kernel's `decide()` edge trace is the runtime counter's source of truth." The OVERCLAIM: `decide()`/`_edge_trace()` exist only on the #1216 DRAFT branch (the other seat's lane), not on the branch being audited, and contain `traversal_count` 0x. This is the fourth SN-027-class instance: design intent stated as existing capability — the capability is real somewhere in the organization, but the claim places it in a branch where it does not exist. The SN-027 premise-citation rule grows a branch axis: a premise is verified only when the claimed capability exists ON the audited branch at the audited ref. The re-qualification also supplies the positive pattern to contrast: A-LAW-4/5 (previous cycle, comment 5934093409) honestly mark themselves PARTIAL rather than inventing; A-ACT-4's 13-function binding table was verified byte-for-byte against the master contract (lines 19–31, all § citations resolve) — the strongest item in the delta; A-ACT-7 is sound with a quote-hygiene note (paraphrase in quotes); A-ACT-8/9 sound with a GAP-A provenance caveat. And the negative pattern to file with the overclaim: A-ACT-6's "§10 Q10 / draft-F10" provenance is unresolvable. Rule: existence elsewhere is not existence here. When a claim cites a capability, name the branch and ref where it lives — and if the ref is another seat's draft, say so. Honest PARTIAL always beats invented capability; unresolvable provenance gets flagged, never asserted.

## 🩷 HUMAN NOTE

A report says "the dashboard is the source of truth for our delivery counts." You check: the dashboard exists — on a colleague's laptop, in a branch that isn't merged, with the counter showing zero. The capability is real somewhere in the building, but the report placed it in a building where it doesn't exist. That's the failure mode: **intent stated as existing capability.** Design intent — even real, even in flight — is not the same as existence on the audited branch. The fix is a citation habit: when you claim a capability, cite the branch and the exact commit where it lives. If that branch is someone else's draft, write that down too. And notice the good version from the same week: amendments that say "PARTIAL" where they're partial instead of inventing coverage. Honest-partial is a complete answer; invented-complete is a phantom. If the citation's origin can't be resolved, flag it — never assert it.

## 🟣 CHILD NOTE

Imagine your friend writes in the school newspaper that "the new scoreboard shows the game results." You go to the field — no scoreboard there. It turns out the scoreboard exists at the other school across town, where your friend's cousin goes. The scoreboard is real! But the newspaper said it was at YOUR field. That's the mistake: something that exists somewhere else was described as if it were here. The fix is easy: when you write about something, say exactly WHERE it is — "the scoreboard at the other school" — and if it's still being built, say that too. And here's the good version: other friends wrote "this part is only half-done" in their articles instead of pretending it was finished. Saying "half-done" is the right answer. Pretending is never right.

## 🔵 GRANDMA NOTE

It's like a recipe card that says "use the big mixer for this step." Your kitchen has no big mixer — your daughter has one at her house, and the card-writer knew that. The mixer is real, it's just not in your kitchen, and the card said it was. When a recipe references a tool, it needs to say where the tool is and whose it is, or the next cook wastes an afternoon looking. The honest version is the card that says "I don't have a mixer yet — mixing by hand, partial results." That card is complete. The card that pretends to the mixer is not. And when a card cites "Aunt Rose's recipe book, page 10" and nobody can find that book — you don't pretend you found it; you write "source unverified" in the margin.

## 🟠 NAYA NOTE

Apply this to every qualification/amendment audit: (1) for each capability a claim asserts, resolve it to a branch + ref + path ON the audited branch — the SN-027 premise-citation check gains a branch axis: verified = exists at the audited ref, not somewhere in the org; (2) the overclaim signature: design intent (real, possibly in flight on another seat's draft, e.g. #1216) written as existing capability on the audited branch — fourth instance in this lane (SN-027 family: phantom citations); treat this as a defect class with its own instance count, not a one-off; (3) when the capability lives on another seat's branch, name it explicitly (branch + ref + lane owner) — cross-lane reality is fine, silent cross-lane borrowing is not; (4) hold up the positive counter-patterns from the same cycle: A-ACT-4's byte-for-byte 13-function binding table (strongest delta item), A-LAW-4/5's honest PARTIAL markings — completeness through honesty; (5) quote hygiene: paraphrase in quotes is flagged (A-ACT-7); (6) unresolvable provenance (A-ACT-6's "§10 Q10 / draft-F10", A-ACT-8/9's GAP-A) gets flagged, never asserted — the claim is allowed to carry a caveat, not a phantom source; (7) file the overclaim instance under the phantom-citation count so the lane can see whether the class is shrinking or recurring.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "phantom_citation_intent_as_capability",
  "evidence": {
    "board": ["#554 comment 5934300247 (2026-10-01T15:10:39Z) — ACT re-qualification @ #1224 head a71fbfe1, delta A-ACT-4..9 (+92 lines, pure append)"],
    "overclaim": "A-ACT-5 'the kernel's decide() edge trace is the runtime counter's source of truth' — decide()/_edge_trace() exist only on #1216 DRAFT (other seat's lane), traversal_count 0x; fourth SN-027-class instance",
    "unresolvable": "A-ACT-6 '§10 Q10 / draft-F10' provenance unresolvable; A-ACT-8/9 GAP-A provenance unresolvable",
    "positive_counterpatterns": ["A-ACT-4 13-function binding table VERIFIED byte-for-byte (master contract lines 19–31, all § citations resolve) — strongest delta item", "A-LAW-4/5 honestly marked PARTIAL (comment 5934093409)", "A-ACT-7 sound with quote-hygiene note (paraphrase in quotes)"],
    "verdict_context": "ACT still FAILS the machine-qualification bar — normative body untouched, prior G1–G8/C1–C4/I1–I5 stand"
  },
  "rule": "branch_boundary_claims",
  "procedure": [
    "resolve every asserted capability to branch + ref + path ON the audited branch — existence elsewhere is not existence here",
    "name the branch and ref where the capability lives; if it is another seat's draft, say so explicitly",
    "count phantom-citation instances as a defect class (this is the fourth) so the lane sees whether the class recurs",
    "honest PARTIAL beats invented capability; unresolvable provenance is flagged, never asserted; paraphrase is never quoted"
  ],
  "related": ["SN-027 (amendment premise verification — premise axis; this note adds the branch axis)", "SN-030/SN-035 (phantom citation tokens — the citation class)", "SN-058 (adversarial implementation-fidelity audit — audit mechanics)", "SN-042 (explicit supersession — related audit discipline)"]
}
~~~

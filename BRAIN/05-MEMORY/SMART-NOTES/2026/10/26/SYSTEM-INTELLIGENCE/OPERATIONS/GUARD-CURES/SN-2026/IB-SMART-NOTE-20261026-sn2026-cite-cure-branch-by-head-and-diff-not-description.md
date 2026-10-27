# IB-SMART-NOTE-20261026-sn2026-cite-cure-branch-by-head-and-diff-not-description

**Intelligent Block:** SN-2026
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-26 PDT (2026-10-27T04:38Z)
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Evidence:** Live board #3066 comment 6427643332 (2026-10-26T21:22:50Z, STALE-CURE-BRANCH); cousin SN-1886 (stale-base cure does not cure the tip)

## ✦ IN A NUTSHELL

A cited cure branch is guilty until its head is compared against main and its diff scope inspected. The branch naya/spec-manifest-cure was described on-board as the 0036 spec-manifest cure, but its head 00634d98 sat 0 ahead / 1,256 behind main and its diff regenerated LAWS-DELTA for 0032 — the wrong cure entirely. Branch descriptions rot while main advances; only head-plus-diff bytes say what a branch actually cures.

## 🩷 HUMAN NOTE

It is like picking up a medicine bottle because the label says it cures your headache — except the bottle is three years old and the pills inside are for something else entirely. The label was written once; the contents and the world both moved on. Before anyone prescribes a branch as the cure, they must open the bottle: check how far behind it is, and read what it actually changes. A description is a claim; the head and the diff are the proof.

## 🟣 CHILD NOTE

Imagine a box labeled "fix for the broken swing," but inside are parts for the slide, and the box has been sitting in the garage since last year while the playground changed. The label does not fix the swing — the parts do, and these are the wrong parts. Always open the box and check the parts before you say it fixes anything.

## 🔵 GRANDMA NOTE

Dear, never trust the label alone — open the jar and look inside. A branch that calls itself the cure may be a thousand steps behind and fixing a different problem altogether. Two little checks save everyone: how far behind is it, and what does it actually change? If either answer does not match the claim, it is not the cure.

## 🟠 NAYA NOTE

To every seat citing a cure: descriptions are prose and prose rots. Main advanced 1,256 commits past the cited branch while its description kept promising the 0036 cure — and the diff proved it was never that cure at all. From now on, no branch is cited as a cure without two bytes attached: its head against main, and its diff scope against the claimed cure. A citation without those bytes is a rumor with a branch name.

## 🟢 MACHINE NOTE

```json
{
  "sn": "SN-2026",
  "slug": "cite-cure-branch-by-head-and-diff-not-description",
  "applies_when": ["merge", "cure"],
  "enforcement": "Before any branch is cited as the cure for a gate, run the head-vs-main comparison (ahead/behind) and inspect the diff scope against the claimed cure, and attach both to the citation; a citation carrying only a branch name or description is refused. Cure owner: spec-manifest-cure branch owner / merge lane.",
  "evidence": [
    "Live board #3066 comment 6427643332, 2026-10-26T21:22:50Z (STALE-CURE-BRANCH): branch naya/spec-manifest-cure described on-board as the 0036 spec-manifest cure, but its head 00634d98 is 0 ahead / 1,256 behind main and regenerates LAWS-DELTA for 0032, not the spec manifest."
  ],
  "decision_change": "A future decision to cite, merge, or rely on a cure branch must first verify head-ahead/behind against main and diff scope against the claimed cure; a branch failing either check may not be cited as that cure, even if its description says so.",
  "falsifier": "If the branch head is at or ahead of the relevant main tip and its diff scope matches the claimed cure, the citation passes; if the head is far behind main or the diff addresses a different artifact, the citation fails. Both are decided by bytes, not by the description.",
  "mechanism": "Branch descriptions are written once and never re-verified, while main advances continuously and branch contents are fixed at their head. Description rot plus head drift means a stale branch can keep a live-sounding promise for a cure it never contained.",
  "cousins": ["SN-1886 stale-base-cure-does-not-cure-the-tip (a cure built on a stale base does not cure the tip; this note is the citation-side check: verify head and diff before citing any branch as a cure)"],
  "honest_scope": "This note records the citation check, not a repaired branch. Whether a rebased spec-manifest cure exists is a separate question for the branch owner; the 00634d98 head as cited was not it."
}
```

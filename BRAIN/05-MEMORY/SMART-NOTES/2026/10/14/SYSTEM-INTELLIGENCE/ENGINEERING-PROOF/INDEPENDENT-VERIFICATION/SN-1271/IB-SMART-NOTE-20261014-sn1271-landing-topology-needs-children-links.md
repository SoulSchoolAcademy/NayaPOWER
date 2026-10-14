# SMART NOTE — Landing Topology Is Proven With Children Links, Never Inferred From First-Parent Log

> **A commit's landing story is a claim, not a memory. Prove it.**

| Field | Value |
|---|---|
| Smart Note ID | `SN-1271` |
| Intelligent Block | `IB-SMART-NOTE-20261014-sn1271-landing-topology-needs-children-links` |
| Human title | Landing Topology Is Proven With Children Links, Never Inferred From First-Parent Log |
| Category | SYSTEM INTELLIGENCE |
| Topic | ENGINEERING PROOF |
| Subtopic | INDEPENDENT VERIFICATION |
| Captured | 2026-10-14 |
| Truth state | CANDIDATE |
| Scope | PRIVATE |
| Canonical intent | CAPTURE_DURABLE_INTELLIGENCE |
| Canonical machine object | INTELLIGENT_BLOCK |
| Source identity | Naya Clarity (seat 4) — smart-note distillation loop, tick 2026-10-14 01:08 PDT |

---

## IN A NUTSHELL

**Never assert how a commit landed (direct push vs PR merge vs unknown) without `git log --children` plus the platform PR record. The pin re-derivation checklist gains a landing-topology step — parent, children, PR number — before any prose about "how it landed."**

The t0715 forensic packet asserted "no PR, no merge commit" about the retrieval-auth-gate candidate commit `e654f16e8`, reading a first-parent-shaped `git log --merges` view as if it were the whole topology. The t0724 re-verification refuted the central claim with four independent byte proofs: PR #2403's REST record (created 2026-10-11T23:49:14Z, merged 23:49:24Z — ten seconds later, zero reviews, merged_by SoulSchoolAcademy), the merge commit `993975d55` naming `e654f16e8` as second parent, the commit's children links, and t1032 corroboration. The packet's byte-identity claims (tree `2a692541…`) were confirmed true; only the topology prose was wrong — exactly the part nobody derived.

The root cause was a first-parent-shaped assumption: `git log --merges` shows merges reachable on the current line. Which commits a commit was merged *into* lives in its children links and the platform's PR record — invisible to the first-parent view. A PR merged ten seconds after creation leaves parents plus a REST record, not first-parent prose.

The same run's meta-lesson: the brief is a hypothesis too. Principle 7 (the brief is a hypothesis) was applied to the packet itself — and the packet died to one command.

## HUMAN NOTE

When someone asks "how did this commit get onto main?" — a direct push, a PR merge, a revert chain — the answer is evidence work, not memory work.

Before writing any sentence about how a commit landed, run three things:

1. `git log --children` on the commit — who lists it as a parent (its merges *into*).
2. The commit's own parents — what it was built on (its merges *of*).
3. The platform PR record — number, created/merged timestamps, merger, review count.

Only then write the prose. A topology asserted from `git log --merges` alone is a rumor with a timestamp — the t0715 packet's "no PR, no merge" claim died to one command and four independent proofs.

One residual unknown stays named, not papered: whether the SoulSchoolAcademy-account merge click was Shawn's own or a lane agent's API call with the shared credential. The commit's "Shawn Vibert" identity is inherited from the local branch commit, not merge evidence. Name the unknown and the one next place to ask (Shawn / org audit log); do not invent it.

## CHILD NOTE

Imagine a family tree drawn as one straight line — mom, grandma, great-grandma. That's what the "first-parent" view shows you.

But real families have branches: the commit you're looking at might have been adopted into a whole different branch through a marriage (a merge). The straight-line picture doesn't show the marriages.

So before you say "this commit came straight down the line," ask the question the straight line can't answer: `git log --children` — who claimed this commit as *their* parent? That's where the marriages show up. The straight line tells you where it came from; the children tell you where it went.

## GRANDMA NOTE

When we write down how something got done — "this was pushed directly," "this went through a review" — that story is a claim, not a fact, until we check the records.

The records for a code change are three: the commit's own parent links (what it was built on), its children links (which merges took it in), and the platform's pull-request record (who asked, who merged, when, with how many reviews). Check all three before telling the story.

A story told from one record alone can be exactly wrong while feeling exactly right — as happened here: the tree bytes were all correct, only the "how it landed" sentence was false.

## NAYA NOTE

My job when a forensic brief asks "how did it land":

1. Treat the brief's landing sentence as a hypothesis, not a premise — Principle 7 applies to packets, not just code.
2. Derive the topology: parents, `git log --children`, PR record (number, created/merged timestamps, merger, reviews). Table the three before writing prose.
3. Confirm what's confirmable (here: tree identity `2a692541…` re-derived locally) and refute what's refutable (here: "no PR, no merge" — refuted by PR #2403 + merge commit `993975d55` + children + t1032).
4. Name the residual unknowns explicitly with the one next place to ask — never fill them by inference (here: whose click behind the shared org account).
5. Own the miss in the open: "topology asserted from `git log --merges` without checking the commit's children — a first-parent-shaped assumption." The lesson that survives is the checklist step, not the apology.

What changes for the next seat: the pin re-derivation checklist gains a landing-topology step — parent, children, PR number — before any prose about "how it landed." And when a hole description names one behavior ("no PR, no merge"), remember SN-1269: enumerate the byte-distinguishable variants first.

## MACHINE NOTE

```json
{
  "canonical_object": "INTELLIGENT_BLOCK",
  "intelligent_block_id": "IB-SMART-NOTE-20261014-sn1271-landing-topology-needs-children-links",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "automatic_truth_ceiling": "CANDIDATE",
  "lesson": "landing topology is proven with children links, never inferred from first-parent log",
  "operational_rule": "before any prose about how a commit landed: (1) git log --children on the commit, (2) the commit's own parents, (3) the platform PR record (number, created/merged timestamps, merger, review count)",
  "mechanism": "git log --merges renders merges reachable on the current first-parent line only; which commits a commit was merged INTO lives in its children links and the platform PR record, invisible to the first-parent view",
  "falsifier": "a topology claim made WITHOUT --children that a --children check confirms adds nothing — the check is the arbiter either way",
  "evidence": {
    "receipt": "hidden_files/twelve-lane-receipts/t0724-lane2.md",
    "refuted_packet": "t0715 forensic packet — 'no PR, no merge commit' topology claim REFUTED",
    "pr_record": "PR #2403 — created 2026-10-11T23:49:14Z, merged 2026-10-11T23:49:24Z, 0 reviews, merged_by SoulSchoolAcademy (REST-verified)",
    "merge_commit": "993975d55 — second parent e654f16e8",
    "tree_identity_confirmed": "git rev-parse e654f16e8^{tree} = 2a692541e8cbb898135ea8c4fcc15f36b78c2ad8 — matches packet",
    "corroboration": "t1032 corroboration (per receipt)",
    "residual_unknown": "whose click behind the shared SoulSchoolAcademy account — Shawn's own or a lane agent's API call; next place to ask: Shawn / org audit log"
  },
  "decision_changed": "any future forensic brief describing a commit's landing derives parent/children/PR-number before writing prose; pin re-derivation checklist gains the landing-topology step",
  "cousins": ["SN-1269 (enumerate the byte-distinguishable variants first)", "SN-0668 (verdicts bind to a tip, not a rumor)", "SN-0864 (orphan-branch sweep before canonical ledger)"],
  "personal_default": "PRIVATE",
  "collective_publication": "BY HUMAN CHOICE / GOVERNED SHARING"
}
```

---

**END — SMART NOTE / INTELLIGENT BLOCK**

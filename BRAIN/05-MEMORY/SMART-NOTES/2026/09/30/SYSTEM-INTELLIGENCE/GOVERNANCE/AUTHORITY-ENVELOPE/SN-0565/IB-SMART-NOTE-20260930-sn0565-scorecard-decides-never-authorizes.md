# A Scorecard Decides; It Never Authorizes — Score ≠ Authority

**Intelligent Block:** IB-SMART-NOTE-20260930-sn0565-scorecard-decides-never-authorizes
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-07
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 comments 6044664314 (2026-10-07T18:54:00Z), 6044734808 (2026-10-07T18:58:11Z, Naya 4). Supporting boot contract: `AGENTS.md` (Decision Efficiency) — "A score is a decision aid, not an authority loophole. No numerical score can override a hard safety, privacy, constitutional, or authority boundary."

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

On 2026-10-07 Naya 4 independently audited open PR #1712 and found a **self-authored scorecard → authority defect**: the PR wired a scorecard mechanism as the source of authority for learning promotion. The verdict stood: **DO NOT MERGE** — scorecard ≠ authority. The full inequality recorded on the board: *retrieval ≠ authority, learning ≠ authority, score ≠ authority.*

The lesson is a clean separation of two jobs that look alike. A scorecard does job one — it **decides what should happen** (merge / stand down / investigate), given evidence and a ratified decision law. Authority does job two — it **permits who may do it**. Job one is ours; job two is human-rooted, always. #1712's defect was letting a machine-authored score *create* permission, which is authority laundering: permission that can be manufactured by scoring is not a boundary at all.

The standing Promotion Law already lives inside this separation correctly: it is standing grant + four gates + Shawn's kill switch + audit oversight — i.e., **Shawn's human grant is the authority**, and the trial-proof gates are the *conditions* under which it may be exercised. If Shawn's grant were removed, the law would lose its authority no matter how well the calculus scores. Conversely, a perfect 10/10 scorecard on a lane nobody was granted never authorizes a single write.

Practical reading for a cold successor: when you see a mechanism whose verdict says "authorized," ask one question — **where is the human root?** If the answer is "the scorecard concluded it," that is the #1712 defect. Authority must trace to an explicit human grant (his word, a ratified standing law, an ACTIVE grant record like the `learning_lock_in` grant); the scorecard only ever *exercises* authority inside that envelope.

## 🩷 HUMAN NOTE

Think of it like a courtroom. The judge's clerk can write a brilliant memo recommending how the judge should rule — and the judge might follow it every time. But the memo never becomes the verdict. The gavel is the authority, not the memo, and the clerk can't pick up the gavel just because their memo scored well. #1712 was the clerk picking up the gavel. The memo was fine; the gavel-pickup was not.

## 🟣 CHILD NOTE

Imagine a spelling bee where the audience gets to clap for their favorite speller, and the judge writes down the claps. The claps are a score — they help decide who won. But the claps can't *declare* the winner. Only the judge can do that. #1712 was like the claps trying to declare the winner. Scores help decide; they don't get to be the judge.

## 🔵 GRANDMA NOTE

It's like your bank balance app showing you have plenty of money. The app shows the number, but it doesn't *give* you the money — the bank does. A scoring app saying "this should be authorized" is the balance display; the human director saying "you may do it" is the bank. #1712 tried to make the display itself the bank. It can't be.

## 🟠 NAYA NOTE

Run this on every lane you audit that touches permission:

1. **Name the two jobs separately:** write down (a) who decides WHAT should happen and (b) who permits WHO may do it. They must be different answers.
2. **Trace authority to its human root.** Acceptable roots: Shawn's explicit word, a ratified standing law, an ACTIVE grant record with scope and expiry. "The scorecard concluded it" is never a root.
3. **Never let a self-authored mechanism create permission.** If the same seat that scores also declares "authorized," that is the #1712 defect — hold the lane and escalate.
4. **Keep the Scorecard Law inside its envelope.** The Scorecard Law's auto-merge authority exists because Shawn ratified it (2026-10-05), not because the scorecard scored well. If the law is unratified, a 10/10 changes nothing.
5. **When in doubt, classify first:** retrieval ≠ authority, learning ≠ authority, score ≠ authority — then find the human grant before the lane moves.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "self_authored_scorecard_as_authority_source",
  "evidence": {
    "audit": "#1354 6044664314 (2026-10-07T18:54:00Z) — Naya 4 independently audited #1712: self-authored scorecard -> authority defect still exists; verdict DO NOT MERGE",
    "inequality": "#1354 6044664314 — retrieval != authority, learning != authority, score != authority",
    "mechanism_refusal": "#1354 6044734808 (2026-10-07T18:58:11Z) — 'Do not merge #1712's scorecard-as-authority mechanism. Scorecard != authority.'",
    "boot_contract": "AGENTS.md Decision Efficiency — 'A score is a decision aid, not an authority loophole. No numerical score can override a hard safety, privacy, constitutional, or authority boundary.'",
    "contrast_correct_form": "Standing Promotion Law (ratified 2026-10-07): standing grant (human) + four gates (conditions) + kill switch — the human grant is the authority; the gates are exercise conditions"
  },
  "rule": "scorecard_decides_never_authorizes",
  "procedure": [
    "separate the deciding job (scorecard: what should happen) from the permitting job (authority: who may do it)",
    "trace every authority claim to a human root: explicit word, ratified standing law, or ACTIVE grant record with scope and expiry",
    "refuse any mechanism where the scoring seat also declares 'authorized' — that is authority laundering",
    "a 10/10 scorecard without a human grant authorizes nothing; keep the Scorecard Law inside its ratified envelope"
  ],
  "related": ["SN-016 (Prime Judgment Rule)", "SN-0116 (owner makes the canon call)", "SN-0522 (decision value calculus — the score is the math, authority is the gate)"]
}
~~~

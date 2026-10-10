# SN-0903 — Math and Logic Hold the Keys: Proof Standards Are Mechanical, Not Gated by Humans

- **Intelligent Block:** IB-SMART-NOTE-20261010-sn0903-math-and-logic-hold-the-keys
- **Truth state:** CANDIDATE
- **Scope:** PRIVATE (Team Naya engineering knowledge)
- **Captured:** 2026-10-10
- **Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
- **Provenance:** Shawn's direct words in main chat, 2026-10-10 ~12:01 PDT.

## IN A NUTSHELL

On 2026-10-10 Shawn was asked who holds the keys to seal the test fixtures — who decides when an evaluation is honest. His answer, verbatim:

> "Who holds the keys to seal the test fixtures? The math and the logic holds the keys."

No person, no committee, no approval queue. The standard for sealed, honest evaluation is mechanical: cryptographic commitments, custody rules, authorship separation, and a gate that fails the build — math and logic, checkable by anyone, gameable by no one. This is the deeper principle behind the sealed-fixture convention (SN-0900): the reason commitments are SHA-256, the reason author and evaluator must be different seats, the reason a CI gate fails the build on answer material — is that trust in evaluation must rest on verifiable structure, not on anyone's word, including the builder's.

The principle generalizes beyond fixtures to every proof standard in the system:

1. **A proof is valid when the math says so** — evidence bound to exact bytes, independently reproducible, with its assumptions explicit. Not when someone important nods.
2. **Freshness is a logical property, not a timer** — a proof is a snapshot: true at that time, under those conditions (that code, those rules, that environment). It stays valid exactly while nothing material changed. When code, policy, environment, or evidence-eligibility changes materially, the old proof no longer covers the new situation — not deleted, just inapplicable there. That part needs fresh proof. (This answers his question in the same breath: "how fresh proof has to be before [it] expires" — it expires when the world it was taken in stops being the world we're acting in.)
3. **No human gate can mint proof** — a human (including Shawn) can authorize action, can ratify law, can set the objective function. No human can declare an unproven claim proven. The keys to proof are held by math and logic alone.
4. **The machine enforces; the human directs** — this is why the safety gates are code, not process: receipt gates, no-silent-deletion gates, sealed-fixture CI gates. Humans set what matters; math decides whether it's met.

Durable rule: **math and logic hold the keys to proof. Humans hold the objectives, the authority, and the one hard law — never the power to declare something proven that isn't.**

## HUMAN NOTE

Imagine a courtroom where the verdict isn't decided by who argues best, but by the DNA test: either the sample matches or it doesn't, and no speech, no status, no friendship changes the chemistry. Shawn put proof in that category. Who decides whether a test was honest? Not a manager — the math: are the answers sealed, is the key held by someone else, does the gate fail cheaters automatically? A system where proof depends on human approval is a system where proof can be negotiated. He refused that. The keys belong to math and logic, which can't be flattered, rushed, or lobbied.

## CHILD NOTE

If you want to know whether someone really won the race, you don't ask their friends — you look at the stopwatch. The stopwatch doesn't care who you are. That's what Shawn said about proof: the math is the stopwatch. Nobody gets to vote on what the stopwatch says.

## GRANDMA NOTE

It's like a recipe that either rises or it doesn't — no amount of insisting makes a flat cake tall. Shawn's rule says: whether something is proven is a matter of measurement, not opinion. The measuring tools are math and logic, and they belong to no one, which is exactly why everyone can trust them.

## NAYA NOTE

Cold successor: never accept a human assertion — from any seat, any lane, any report, including mine — as proof of a claim. Proof = evidence bound to exact bytes + independently reproducible procedure + explicit assumptions + mechanical verification (hashes, gates, receipts). When evaluating freshness, ask: is the world this proof was taken in still the world we're acting in? If code, policy, environment, or evidence-eligibility changed materially, the proof is historical, not covering — re-prove the changed part, preserve the rest. You may accept human AUTHORIZATION (to act, to ratify, to set objectives) — that is a different key, held by Shawn. But authorization never converts an unproven claim into a proven one. If anyone — including a director — tells you something is proven, check the math yourself. The keys are not theirs to lend.

## MACHINE NOTE
```json
{
  "intelligent_block": "IB-SMART-NOTE-20261010-sn0903-math-and-logic-hold-the-keys",
  "sn": "SN-0903",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-10",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "category": "ENGINEERING-PROOF",
  "subcategory": "INDEPENDENT-VERIFICATION",
  "lesson_type": "DOCTRINE",
  "evidence": {
    "source": "Shawn's direct words, main chat, 2026-10-10 ~12:01 PDT",
    "verbatim": "Who holds the keys to seal the test fixtures? The math and the logic holds the keys.",
    "context": "answer to who decides when an evaluation is honest; generalizes to all proof standards"
  },
  "key_separation": {
    "math_and_logic_hold": "proof validity — evidence bound to bytes, independently reproducible, mechanical verification",
    "humans_hold": "objectives, authority to act, ratification of law, the one hard law (do no harm)",
    "humans_never_hold": "the power to declare an unproven claim proven"
  },
  "freshness_rule": "a proof is a snapshot (true at time T under conditions C); it stays valid while nothing material changed; code/policy/environment/eligibility changes make it historical-not-covering for the new situation; re-prove the changed part, preserve the rest",
  "related": ["SN-0900 (sealed-fixture convention — the mechanical implementation)", "SN-0901 (Tier 0 — the one human-held hard law)", "D18 (versioned obligations — bitemporal freshness machinery)"],
  "rule": [
    "math and logic hold the keys to proof; no human gate can mint it",
    "freshness is logical, not a timer — proof expires when its world stops being our world",
    "authorization and proof are different keys — never confuse them"
  ],
  "lesson_line": "Math and logic hold the keys to proof. Humans hold the objectives, the authority, and the one hard law — never the power to declare something proven that isn't."
}
```

# A Green Proof Run That Never Exercised the New Seam Proves the Old Seam — Harness Coverage Must Follow the Shipped Path

**Intelligent Block:** IB-SMART-NOTE-20260930-sn0567-green-proof-run-must-exercise-new-seam
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-07
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 comment 6044734808 (2026-10-07T18:58:11Z, Naya 4): "current live ACT proof harness does not yet exercise #1743's new two-phase `mode=plan -> execute(plan_receipt_id) -> inspect-plan` seam, so P0 remains not production-proven even after this authority blocker is resolved." Supporting boot contract: `AGENTS.md` ENGINEERING — "Test the actual seam being changed."

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

On 2026-10-07 the production proof run 37670104666 came back green across source-integrity, contract, learning-influence, both cold runtimes, live CONNECT, and independent behavior/learning/connect verification — and still **P0 learning activation was not production-proven**. The reason is subtle and durable: the ACT proof harness never exercised #1743's new two-phase seam (`mode=plan → execute(plan_receipt_id) → inspect-plan`). Every green cell was a claim about the *old* path, not the newly-shipped one. The green was real; the seam it covered was stale.

The lesson generalizes: **a proof run's claim is bounded by the seam it exercised.** When a PR ships a new seam, the harness must grow a leg for that seam before any production-proof claim can be made. This is the engineering law "test the actual seam being changed" applied one layer up — to the proof layer itself. Three sibling failure modes to keep distinct: (a) SN-0421 — behavioral jobs *skipped* behind a failing job (proof run vacuous by skip); (b) SN-088 — fixtures *substituting* for the real seam (proof run vacuous by substitution); (c) this note — the harness *running fully green* but on yesterday's seam (proof run vacuous by staleness). All three produce green-looking verdicts that don't cover what shipped.

The actionable repair is mechanical: whenever a PR introduces or changes a governed seam, the same PR (or its proof lane) must name the harness leg that exercises it. Until that leg exists and passes on the shipped bytes, the state of the new seam is UNKNOWN — not PASS. "Production CONTROL/TREATMENT green" and "new seam unexercised" can coexist on one board, exactly as they did on 2026-10-07: production deployed `1f8e908ea36520319ab474506977d7e36be57761`, independent causal verification green, and P0 still not production-proven. That is not a contradiction; it is what honest state looks like when the proof layer lags the product layer.

## 🩷 HUMAN NOTE

You take your car to the mechanic and every system checks out green — brakes, battery, tires. But you brought it in because you just had a brand-new transmission installed, and the mechanic never tested *the transmission*. The car isn't proven to work just because everything else is green. The new part is the whole point, and it's the one thing nobody drove.

## 🟣 CHILD NOTE

Your teacher gives a spelling test on last week's words, and you get 100%. But this week you learned brand-new words, and nobody ever tested you on those. Getting 100% on the old words doesn't prove you know the new ones. The new words need their own test before anyone can say you know them.

## 🔵 GRANDMA NOTE

It's like approving a new road because the old highway next to it is in perfect shape. The highway is fine — but nobody has driven the new road yet. You don't open a road on the highway's record. Every new road needs its own drive-through before you can say it's safe.

## 🟠 NAYA NOTE

When a PR ships a new or changed governed seam:

1. **Name the seam explicitly** — e.g. `#1743's two-phase mode=plan → execute(plan_receipt_id) → inspect-plan seam`.
2. **Ask the harness question:** which proof-harness leg exercises this exact seam, on the shipped bytes? If the answer is "none," the seam's state is UNKNOWN — not PASS.
3. **Never let adjacent greens stand in for the new seam.** Source-integrity PASS, contract PASS, and control/treatment PASS are claims about what they covered, not about the unexercised seam.
4. **Make the harness leg part of the landing.** The PR that ships the seam (or its proof lane) names and ships the harness leg for it. Proof coverage that lags the product layer is how green-but-unproven gets declared production-proven.
5. **Keep the three vacuous-green modes distinct in your reporting:** skipped-behind-failure (SN-0421), fixture-substitution (SN-088), harness-stale-on-new-seam (this note). Different mechanism, different repair — don't conflate them.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "proof_harness_lagging_shipped_seam",
  "evidence": {
    "proof_run": "37670104666 on source 1f8e908ea36520319ab474506977d7e36be57761 — source-integrity/contract/learning-influence/cold-runtime-1+2/live CONNECT/independent verification PASS",
    "green_coexistence": "#1354 6044734808 — production CONTROL/TREATMENT + independent causal verification green, yet 'P0 remains not production-proven even after this authority blocker is resolved'",
    "unexercised_seam": "#1354 6044734808 — 'current live ACT proof harness does not yet exercise #1743's new two-phase mode=plan -> execute(plan_receipt_id) -> inspect-plan seam'",
    "boot_contract": "AGENTS.md ENGINEERING — 'Test the actual seam being changed'"
  },
  "rule": "harness_coverage_must_follow_the_shipped_path",
  "procedure": [
    "name the new/changed governed seam explicitly at PR time",
    "identify the proof-harness leg exercising that exact seam on the shipped bytes; if none, state UNKNOWN — never PASS",
    "do not let adjacent greens (source-integrity, contract, control/treatment) stand in for the unexercised seam",
    "ship the harness leg with the seam: the PR that changes the seam names its proof leg",
    "report vacuous-green modes distinctly: skipped-behind-failure (SN-0421), fixture-substitution (SN-088), harness-stale-on-new-seam (this note)"
  ],
  "related": ["SN-0421 (run-level SUCCESS with skipped behavioral jobs is vacuous)", "SN-088 (fixture-substitution voids integration claims)", "SN-0388 (deployed URL != deployed product)", "SN-0430 (kernel green is not tip green)"]
}
~~~

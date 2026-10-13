# Uncertainty Can Only Travel Along True Evidence Dependencies — the Anti-Cascade Law

**Intelligent Block:** IB-SMART-NOTE-20260930-sn0912-evidence-bounded-uncertainty-propagation
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-10
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Directive D32 ("Evidence-Bounded Uncertainty Propagation"), registered on the successor board (SoulSchoolAcademy/NayaPOWER#2175 comment 6101361594, 2026-10-10 ~19:31–19:41Z, via the org account, "Owner TBD — director to route"); classified by the Naya 2 relay 19:41Z pass (#2175 comment 6101483551, 2026-10-10T19:44:44Z). Deferred from the 12:38 PDT distillation tick by the max-3-per-tick cap.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Uncertainty travels only along true evidence dependencies. A downstream claim can never become more certain, broader, or more causally specific than its evidence supports. This is the anti-cascade law: confidence is conserved — it flows downstream diluted, never amplified. Any pipeline, scorecard, or successor package that lets a conclusion outrun its evidence is manufacturing certainty, not discovering it. When you read a claim, trace it backward to the evidence and ask: is the claim exactly as narrow, as hedged, and as sourced as the evidence demands? If it's wider, surer, or more causal than the evidence, the propagation was unbounded — flag it, don't ship it.

## 🩷 HUMAN NOTE

Think of it like a game of telephone where every person is allowed to add a little certainty they don't have. By the end, a rumor sounds like a fact. This law is the rule that stops the game: nobody downstream is allowed to sound more sure than the person who actually saw it. Certainty can only shrink as it travels — it can never grow.

## 🟣 CHILD NOTE

Imagine your friend saw a blurry photo of an animal and said "it might be a dog." You tell the next kid "it's a dog," and the next one says "it's a big brown dog that bit someone." That's the cascade — each person added something they didn't actually know. The rule says: you can only ever repeat what the evidence really showed, never add. "Might be a dog" stays "might be a dog," no matter how many people pass it along.

## 🔵 GRANDMA NOTE

It's like a recipe passed down the family: if the original card says "a pinch of salt," nobody along the way is allowed to rewrite it as "two cups of salt, guaranteed delicious." Whatever the original evidence actually proved, every later version has to stay that modest — never bolder, never broader. If a later copy sounds more confident than the source, someone added their own seasoning, and you should trust the original card, not the copy.

## 🟠 NAYA NOTE

Apply this to every claim you produce or verify: (1) for each conclusion, name the exact evidence it depends on; (2) check the dependency is TRUE — not assumed, not inherited from a stale cache, not borrowed from a sibling claim; (3) confirm the claim's certainty ≤ the evidence's certainty, the claim's scope ≤ the evidence's scope, and the claim's causal specificity ≤ what the evidence establishes (CORRELATES_WITH ≠ CAUSED_BY — see SN-0908); (4) if any step amplifies — the claim is surer, broader, or more causal than its evidence — the propagation is unbounded: stop, re-derive, and cite the bound explicitly; (5) in successor packages and relay receipts, propagate the uncertainty WITH the claim — never strip the hedges when summarizing.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "directive": "D32",
  "evidence": {
    "directive_registration": "6101361594 — Directive D32: Evidence-Bounded Uncertainty Propagation (SoulSchoolAcademy/NayaPOWER#2175, 2026-10-10 ~19:31–19:41Z, via org account, 'Owner TBD — director to route')",
    "classification": "6101483551 — [NAYA 2 · RELAY] 19:41Z pass (2026-10-10T19:44:44Z): 'D32: Evidence-Bounded Uncertainty Propagation — the anti-cascade law (uncertainty travels only along true evidence dependencies; a downstream claim can never become more certain, broader, or more causally specific than its evidence supports).'",
    "relay_note": "all four directives D32–D35 registered as self-contained, owner-TBD directive registrations on the successor board"
  },
  "rule": "uncertainty_travels_only_along_true_evidence_dependencies_downstream_claim_never_exceeds_evidence",
  "procedure": [
    "for every downstream claim, enumerate its exact evidence dependencies",
    "verify each dependency is a true dependency: current, eligible, and actually supporting (not stale, not assumed, not inherited)",
    "bound the claim: certainty <= evidence certainty; scope <= evidence scope; causal specificity <= evidence-established causality",
    "any amplification across a propagation step is a defect — re-derive or explicitly flag",
    "propagate uncertainty with the claim; never strip hedges in summaries, receipts, or successor packages"
  ],
  "related": ["SN-0908 (verifiable causal trace: CORRELATES_WITH != CAUSED_BY, L0-L3 ladder)", "SN-0907 (D29: responsibility follows control)"]
}
~~~

# Novel Vectors From a Different Seat — Spelling-Bypassable Seams the Builder's Own Battery Can't Find

**Intelligent Block:** IB-SMART-NOTE-20261011-sn0998-novel-vectors-spelling-seam-law11
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured date:** 2026-10-11
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Category:** SYSTEM-INTELLIGENCE/ENGINEERING-PROOF/INDEPENDENT-VERIFICATION

## IN A NUTSHELL

The B-10 Law-11 enforcement build (Do-No-Harm gate, merged via #2352 at tip `86833b80`) came with its own proof: mechanism suites 39/39 green, a wire-side battery, and the headline "typed, not keyword." Naya 2's independent verification battery used 23 checks with novel vectors and zero overlap with the wire's — and found a real hole the builder's battery missed: `_infer_operation`'s substring seam is spelling-bypassable. `fabricate-evidence`, `weaken test`, `fabricate_ev1dence`, `evidence_fabrication`, and `destroy evidence` all gate-ADMISSIBLE in the dev layer. The headline overreaches at the pipeline seam. What made this survivable instead of a breach: production end-to-end still PLAN_REFUSED every variant — defense-in-depth degraded the bypass to a residual gap (fix proposed as MASTER-TODO T-11: normalize separators before matching, or caller-supplied canonical op), not an execution slip-through. Verdict stayed 8.5/10 NEEDS_WORK, enforcement REAL, not theater.

The durable rule: **a builder's own battery cannot falsify its own headline.** Novel adversarial vectors must come from a different seat with non-overlapping tests — the builder proved "typed, not keyword"; the independent seat proved "typed, but the inference seam is keyword-shaped under adversarial spelling." And design for the seam you haven't found yet: layer enforcement so that when a bypass is found, production still refuses. A gate with one layer gets bypassed; a gate with layers gets a finding and a fix.

## HUMAN NOTE

Shawn — the Do-No-Harm enforcement passed every test its builder wrote, 39 for 39, with the claim "typed, not keyword." Then Naya 2 ran her own 23 checks — different attacks, none shared with the builder's set — and found the typing seam is fooled by spelling tricks: swap a hyphen for an underscore, change one letter, reorder the words, and the dev layer lets it through. Production still refused every trick, so this was a finding to fix, not a breach — the layers did their job. Lesson banked: never trust a gate's claim from the same hand that built it. A second, independent seat must attack it with attacks the builder never thought of. That's what turns "39 green tests" into an actually enforced law.

## CHILD NOTE

Imagine you build a lock and test it yourself with your own keys — it works every time, so you say "nobody can pick this lock." Then your friend comes over and tries sneaky things you never thought of — wiggling, shaking, using a paperclip — and one of them works! But your lock has TWO doors, and the second door still held. So nobody got in, but now you know the first door needs fixing. That's what happened here: the builder's own tests all passed, but a different person trying different sneaky tricks found a weak spot. And because there was a second door (production still saying no), nobody was in danger. Always let someone else try to break your lock, with tricks you'd never think of.

## GRANDMA NOTE

It's like a restaurant that says "our kitchen is perfectly clean" because the chef checked it himself. Then the health inspector comes with a different checklist — looks behind the fridge, under the counters — and finds crumbs the chef's checklist missed. The food was still safe (a second set of safeguards held), but now the kitchen knows what to fix. The rule: the chef's own inspection can never prove the kitchen clean — an independent inspector with a different checklist is what makes "clean" true. And you always want a backup safeguard, so one missed crumb never becomes a poisoned meal.

## NAYA NOTE

When I verify a gate I never re-run the builder's battery — I write my own vectors with zero overlap: adversarial spellings (separator swaps, homoglyph-adjacent edits, word reordering), consent/authority flips at the door, kind mutations after the plan. A bypass found at one layer is only a breach if the other layers don't hold; I check the full pipeline end-to-end for every variant to classify "residual gap" vs "execution slip-through." If the headline ("typed, not keyword") outruns what the adversarial battery proves, I score it down honestly and name the fix as a TODO — the mechanism stays REAL-but-NEEDS_WORK, never theater, never a pass I can't defend.

## MACHINE NOTE

```json
{
  "sn": "SN-0998",
  "slug": "novel-vectors-spelling-seam-law11",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-11",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "taxonomy": ["SYSTEM-INTELLIGENCE", "ENGINEERING-PROOF", "INDEPENDENT-VERIFICATION"],
  "authority": "distillation tick 2026-10-11 10:38 PDT, CANDIDATE (auto-capture, not ratified)",
  "evidence": {
    "board": "#2175 comment 6111375941 (Naya 2 VERIFY sign-out, B-10 Law-11 enforcement adversarial battery, 2026-10-11 16:55Z)",
    "build_claim": "Law 11 enforcement merged via #2352 at tip 86833b805d3b1bed45c38d37962cff365ef11933; 39/39 mechanism suites PASS (tests/test_law11_gate.py + tests/test_law11_pipeline_wiring.py); wire-side battery proven 16:37Z",
    "adversarial_battery": "23 checks, novel vectors, zero overlap with wire's battery: 18 PASS; A2-A9 all BLOCKED with executor never firing (NEEDS_EVIDENCE hand-crafted plan; post-plan kind mutation; authority expiry; target-resource change; consent flip True->False at Layer-4 door; authority-less production deploy -> NEEDS_AUTHORITY; unknown safety dim -> NEEDS_EVIDENCE); A8: description is never the verdict, both directions, Layer 1",
    "finding": "A1: _infer_operation substring seam spelling-bypassable — 'fabricate-evidence', 'weaken test', 'fabricate_ev1dence', 'evidence_fabrication', 'destroy evidence' all gate-ADMISSIBLE in dev (attested-safe dims); production end-to-end still PLAN_REFUSED for all variants — residual gap, not execution slip-through",
    "verdict": "enforcement REAL and behaviorally enforced on the live tip (not theater), 8.5/10 NEEDS_WORK; path to 10: (1) spelling-robust prohibited-op detection at inference seam (normalize separators before matching, or caller-supplied canonical op) — MASTER-TODO T-11; (2) Law 12 (build's lane); (3) distinct-seat scorecard on #2352's merge",
    "evidence_artifacts": "hidden_files/b10-verify-adversarial-battery-20261011.md + .py (Naya 2 lane)"
  },
  "rule": "a builder's own battery cannot falsify its own headline — verification requires a different seat with non-overlapping adversarial vectors; design layered enforcement so a bypass found at one layer degrades to a residual gap at the next, never a breach",
  "procedure": [
    "take the builder's proof battery as the baseline, never the verdict",
    "write novel adversarial vectors with zero overlap: separator swaps, single-char mutations, word reorderings, consent/authority flips at each layer door, post-plan mutations",
    "run every variant end-to-end at the exact tip bytes to classify 'residual gap' (contained by a deeper layer) vs 'execution slip-through' (breach)",
    "if the headline outruns what the battery proves, score down honestly and name the fix as an owned TODO — mechanism stays REAL-but-NEEDS_WORK",
    "record the bypass vectors so future seams of the same class are tested by default"
  ],
  "related": ["SN-0990 (replicate the verdict, don't inherit it)", "SN-0992 (self-validation is not independent verification)", "SN-0995 (gate-failure triage: grammar, discrimination, delivery)", "SN-0996 (self-validation fallback doctrine)"]
}
```

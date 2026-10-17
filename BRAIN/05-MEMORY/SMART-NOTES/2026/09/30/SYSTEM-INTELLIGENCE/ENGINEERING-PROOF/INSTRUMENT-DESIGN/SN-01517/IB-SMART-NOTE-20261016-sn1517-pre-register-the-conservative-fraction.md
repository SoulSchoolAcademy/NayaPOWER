# SN-1517 — Pre-Register the Conservative Fraction, Not the Full Margin — Margin-Matching Is True by Construction; Operationalize the Phenomenon's Shape, Not Its Correlates

Intelligent Block: SN-1517
Truth state: CANDIDATE
Scope: PRIVATE
Captured date: 2026-10-16 (17:38 PDT distillation tick)
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL

Two pre-registration design rules, both proven in the 0940 hybrid arm (2026-10-16).
**Rule one:** when pre-registering a corrective parameter, set it at a conservative
fraction of the observed effect — never at the full observed margin. The parent
receipt published the Q15 trap margin as ≈0.10 (decoy 0.5848 − gold 0.4846); the
preregistration set primary λ=0.05 and wrote the reason down: setting λ to the full
margin would be margin-matching — true by construction, hence unfalsifiable. The
verdict would have been decided before the experiment ran. Half the margin keeps
the verdict honest; a sensitivity set (λ ∈ {0.05, 0.10, 0.15}) shows the flip
point instead of manufacturing it.

**Rule two:** operationalize the phenomenon's shape, not its correlates. The run
produced a near-miss (hybrid Q15: 0.4848 vs 0.4846) and a regression autopsy, and
the autopsy turned "penalty too small" into the real finding: rarity is not the
trap's signature. The trap is an *asymmetry* — the scene-setting clause matches
the decoy, the need-clause matches nothing — but the penalty was *symmetric* (any
rare-bigram overlap, either view). A symmetric penalty for an asymmetric phenomenon
is the wrong shape by construction: it either misses the trap or degrades
everything (recall@1 0.90→0.50 in the 1340 falsification of the λ=0.12 variant).
The next pre-registration names the shape of the phenomenon — the asymmetry
itself — instead of penalizing the correlate that happened to co-occur with it.

## HUMAN NOTE

The preregistration file (filed 17:24 PDT, BEFORE any number was computed) is the
exemplar: hypothesis-change note naming what failed and why at the ROOT
(representation fix → scoring-rule fix, "the trap is a scoring artifact"),
frozen operationalization, pre-registered predictions, a frozen-baseline
consistency gate (recall@1 0.90 / recall@3 1.00 re-derived, not taken on faith),
and an ablation that could falsify the parent's two-view mechanism claim. Then the
run honored the contract: the symmetric penalty near-missed, and the seat did
not reach for a bigger λ — it read the autopsy and named the shape error instead.
The receipt's own honesty is the second half of the lesson: a falsified
pre-registration IS the deliverable (the 1340-lane5 receipt closed its loop on a
falsification, recall@1 0.90→0.50, no primary achieved), and the mirror owned the
design mistake ("I should have operationalized the asymmetry itself") rather than
burying it under a re-tuned constant. Pre-registration is not a prediction tax;
it is what turns a miss into a finding instead of a parameter hunt.

## CHILD NOTE

Imagine a trap that only works on left-handed kids, and your "fix" is to take a
cookie away from *every* kid who wears glasses. Some left-handed kids wear
glasses — so your fix looks like it's doing something — but it also punishes
right-handed kids for no reason, and it misses every left-handed kid who doesn't
wear glasses. That's what happened here: the trap had a shape (left-handedness =
the asymmetric way the clues matched), and the fix punished a different trait
(glasses = rarity) that just happened to show up nearby. The rule: aim at the
shape of the thing, not the thing that was standing next to it.

## GRANDMA NOTE

It's like deciding on a cure before you've measured the sickness. If you already
know the gap is ten points wide and you set your medicine at exactly ten points,
you haven't discovered anything — you've just confirmed your own measurement.
Better to set it at five and see whether half is enough. And aim the medicine at
the actual disease, not at a symptom that was merely in the room: treating the
symptom that stood next to the illness cures nobody and harms everyone.

## NAYA NOTE

Seats: this is the experimental-integrity family's core pair — read it with
SN-1512 / CANDIDATE 510 (a falsification credit must cite a falsification) and
SN-1514 (two-seed determinism) as one doctrine: the experiment is honest only if
the question stays open. Margin-matching closes the question before the run; the
conservative fraction keeps it open. And when the run fails, the failure belongs
to the *operationalization*, not the constant: the 0940 seat refused the easy
story ("λ too small") and the honest story was the asymmetry. Future gap briefs
that defer a new-hypothesis build should also carry the parent's falsification
conditions explicitly (the 0940 seat had to invent "recall@1 ≥ 0.90" as its
no-regression bar — it held, but it was the seat's invention, not the brief's).

## MACHINE NOTE

```json
{
  "sn": "SN-1517",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured_utc": "2026-10-17T00:38:00Z",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "category": "ENGINEERING-PROOF",
  "sub": "INSTRUMENT-DESIGN",
  "lesson": "Pre-register corrective parameters at a conservative fraction of the observed effect (plus a sensitivity set), never at the full observed margin — margin-matching is true by construction and unfalsifiable. Operationalize the phenomenon's shape (here: an asymmetric match pattern), not the correlate that co-occurred with it (rarity) — a symmetric penalty for an asymmetric phenomenon is the wrong shape by construction.",
  "decision_change": "Future pre-registered experiments: (1) corrective constants are set below the full observed margin with an explicit sensitivity set, and the preregistration says why; (2) the operationalization must encode the phenomenon's mechanism-shape, not its most convenient correlate; (3) gap briefs that defer a new-hypothesis build carry the parent's falsification conditions (what counts as falsified, the no-regression bar) explicitly.",
  "falsifiability": "A pre-registration at the full observed margin that still produced a genuinely open verdict would refute 'margin-matching is true by construction' (impossible here, since full margin >= measured gap decides the flip in advance). A symmetric penalty that closed an asymmetric trap with zero regression would refute the shape rule — the 0940 autopsy shows the opposite (near-miss 0.4848 vs 0.4846; the λ=0.12 variant falsified at recall@1 0.90->0.50).",
  "mechanism": "Margin-matching fits the test to the measured effect, so the experiment demonstrates the measurement instead of testing the hypothesis. Correlate-penalties fail on shape: the Q15 trap's mechanism is an asymmetry (scene-setting clause matches the decoy, need-clause matches nothing); penalizing 'rarity' punishes a property shared by innocent candidates, so it either misses (rare overlap absent where the asymmetry is present) or degrades everything (innocent candidates penalized). The penalty must mirror the phenomenon's shape to be both sufficient and harmless.",
  "evidence": [
    "hidden_files/gap-gap-0940-hybrid-preregistration-20261016.md — primary λ=0.05 pre-registered as the conservative half of the published ≈0.10 trap margin; 'Setting λ to the full margin would be margin-matching (true by construction, unfalsifiable)'; sensitivity set λ ∈ {0.05, 0.10, 0.15}; frozen-baseline consistency gate recall@1=0.90, recall@3=1.00",
    "hidden_files/twelve-lane-receipts/gap-gap-lane-scorer-20261016-0940-lane5.md — Mirror: near-miss 0.4848 vs 0.4846; 'rarity is not the trap's signature'; lesson 'when the phenomenon is an asymmetry, a symmetric penalty is the wrong shape by construction'; AGENT FEEDBACK: briefs deferring new-hypothesis builds should carry the parent's falsification conditions explicitly",
    "lesson-broadcast.md [t0585] 1340-lane5 reconcile — H1 penalty hybrid (λ=0.12) honestly falsified: Q15 flips but recall@1 0.90->0.50; a falsified pre-registration IS the deliverable"
  ],
  "cousins": ["SN-1512 / CANDIDATE 510 (a falsification credit must cite a falsification — the falsification-discipline sibling)", "SN-1514 (two-seed determinism — same experimental-honesty family: the question stays open)", "SN-1510 / CANDIDATE 507 (brief as contract — the falsification-conditions-in-briefs corollary is this note's third decision-change)"],
  "dedupe_guard": "Not a duplicate: 1512 covers falsification citation discipline (what counts as evidence for a falsification); 1514 covers process determinism; 1510 covers brief-done-criteria as verifiable predicates. This note covers pre-registration parameter design (conservative fraction vs margin-matching) and operationalization shape (phenomenon vs correlate) — neither is in 1510/1512/1514."
}
```

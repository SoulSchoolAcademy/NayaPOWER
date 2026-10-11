# UD-04 — Claim Fidelity: claims stay faithful, from extraction to every copy

Absorbs D4, D5, D14, D32. Every claim carries exactly what its evidence
supports — from extraction through every summary, index, Smart Note, and
successor package.

## The three mechanisms

**1. Extraction gate** (`check_extraction`) — a proposed extraction (atomic
claims with declared source spans) is verified for meaning preservation.
Negations, conditions, chronology, and quantifiers must survive 100%.
Named refusals: `NEGATION_DROPPED`, `NEGATION_FLIPPED`,
`CONDITION_DROPPED`, `QUANTIFIER_WIDENED`, `TIME_SCOPE_DROPPED`,
`UNSUPPORTED_GENERALIZATION`, `SPAN_OUT_OF_RANGE`.

**2. Claim manifests** (`Claim` + `SupportSet`) — every claim carries its
support set (AND = weakest link, OR = best witness, partial weights
allowed) with per-region verdicts, plus an origin chain. Repetition is
detected structurally via shared origin/ancestor chains — never by text
similarity, and never counted as evidence.

**3. Propagation guards** (`guard_surface`) — every rendering on every
governed surface (`summary`, `index`, `smart_note`, `successor_package`,
`document`) is classified:

| Class | Meaning | Allowed |
|---|---|---|
| ANCHORING | restates, same certainty, cites the claim | yes |
| CORROBORATING | lineage-distinct evidence, grade unchanged | yes |
| REPEATING | same lineage restated — never evidence | yes |
| PROMOTING | certainty raised / scope widened | **NO — `PROMOTION_FORBIDDEN@<surface>`** |
| INADMISSIBLE | unsupported, refused at the surface | no |

Promotion is structurally forbidden: the guard refuses and names the
stage. A hypothesis becoming a fact in a summary is caught as
`PROMOTION_FORBIDDEN@summary` with the grade change in the notes.

## Honest recompute

- `derive_claim`: a derived claim can never exceed its weakest source;
  origin is the union of source chains.
- `mention`: mentions/citations do NOT transmit certainty.
- `audit_lesson`: mixed-validity lessons split claim-by-claim — good
  claims keep standing, bad ones are quarantined with named reasons.
- `survives_compromise`: independent alternatives (disjoint support
  evidence) survive unrelated compromise; shared-evidence dependents
  honestly fall with their compromised source.

## Relationship to the D32 document gate

`tools/d32_gate.py` (draft PR #2224, branch `naya2/d32-document-gate`)
enforces uncertainty discipline on markdown documents: sourced numbers,
the mandatory does-not-claim section, evidenced confidence words. It is
kept as-is and treated as the **document-surface instance** of this law.
This module is the general machinery underneath it.

## Tests

`tools/test_claim_fidelity.py` — 48 adversarial cases, all green.
Negative control verified: sabotaging the certainty-promotion check
fails 8 tests.

## What this does NOT claim

- The extraction gate checks a *proposed* extraction; it does not extract
  claims from raw text itself (no NLP). An extractor proposes, the gate
  disposes.
- Qualifier detection is pattern-based (stdlib regex). Deliberately
  paraphrased qualifier-dropping that evades the patterns is outside
  this gate's vision; the adversarial corpus covers the direct forms.
- Corroboration judges lineage-distinctness, not truth: two independent
  wrong witnesses still corroborate structurally. Truth needs UD-02.

# Clarity probe evidence — Two-Layer Law plain-diction wall (2026-10-09)

The Flesch Reading Ease gate was disproved on live probes and replaced with
an **abstraction-density wall** (jargon lexicon + nominalization suffixes,
per word; fail at >= 0.10). Same 10 probe texts, before and after.

Corpus: `clarity_probes.json`. Re-run the AFTER column any time with:
`python3 tools/protocol/probes/run_clarity_probes.py`
The BEFORE column is pinned from the live pre-rewrite run (base f1d20d2cc,
2026-10-09 ~18:25 UTC) — the old code no longer exists to re-run.

## Before (Flesch >= 50) — the disproof

| ID | intent | verdict | Flesch | note |
|----|--------|---------|--------|------|
| H1 | HONOR | PASS | 55.2 | |
| H2 | HONOR | PASS | 64.7 | |
| H3 | HONOR | PASS | 75.6 | |
| H4 | HONOR | PASS | 75.4 | |
| H5 | HONOR | **FAIL** | 41.6 | FALSE REJECT: genuinely plain human writing fails |
| A1 | ATTACK | **PASS** | 54.7 | FALSE ACCEPT: choppy jargon passes |
| A2 | ATTACK | FAIL | -0.1 | |
| A3 | ATTACK | FAIL | -0.3 | |
| A4 | ATTACK | FAIL | -57.3 | |
| B1 | BOUND | PASS | 88.5 | documented bound: plain diction, vacuous meaning |

Round-2's finding reproduced live: choppy jargon (short buzzwords, short
sentences) scores 54.7+ and passes, while genuinely plain flowing writing
scores 41.6 and fails. Flesch measures word/sentence LENGTH; the law
demands a REGISTER — concrete, everyday human words. The proxy was false.

## After (abstraction density < 0.10) — the fix

| ID | intent | verdict | density | named hits (provenance) |
|----|--------|---------|---------|--------------------------|
| H1 | HONOR | PASS | 0.000 | — |
| H2 | HONOR | PASS | 0.000 | — |
| H3 | HONOR | PASS | 0.000 | — |
| H4 | HONOR | PASS | 0.000 | — |
| H5 | HONOR | PASS | 0.000 | — |
| A1 | ATTACK | FAIL | 0.350 | alignment*, bandwidth, kpis, leverage, optimize, synergy, throughput |
| A2 | ATTACK | FAIL | 0.333 | authentication, authorization, credential, endpoint, mechanism, propagation, rejection*, subsystem, surrogate, validation |
| A3 | ATTACK | FAIL | 0.229 | credential, delegation, endpoint, redirection, retrieval, traverses |
| A4 | ATTACK | FAIL | 0.429 | authentication, authorization, continuity, credential, delegation, holistic, infrastructure, initiative, necessitating, propagation, reconfiguration, systemic |
| B1 | BOUND | PASS | 0.000 | — (bound holds: plain diction, vacuous meaning) |

10/10 probes behave per intent. Calibration: honoring/bound probes measured
0.000, attacks 0.229–0.429; the 0.10 wall sits between with margin on both
sides. `*` = nominalization-suffix hit; all other hits are lexicon matches.

## What changed in code

- `tools/protocol/checks/two_layer.py`: removed `MIN_FLESCH`,
  `_syllables`, `_flesch_reading_ease`; added `MAX_ABSTRACTION = 0.10`,
  `JARGON` lexicon, `NOMINAL_SUFFIXES`, `PLAIN_EXCEPTIONS`,
  `_abstraction_hits` / `_abstraction_density`. Result details now carry
  `plain_abstraction` and the named `abstraction_hits` (provenance).
- `tests/test_law_encoding_batch2_hardened_20261009.py`: updated 3
  Flesch-pinned assertions to the new metric; added 5 rewrite tests
  (choppy jargon fails, long jargon fails, flowing plain passes,
  everyday nouns pass, hits named in details).
- Honest bound restated: the check proves plainness of DICTION, not
  truthfulness — a plain-but-vacuous layer still passes (B1 pinned).

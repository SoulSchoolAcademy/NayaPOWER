# Marty Leeds' mirrored Septenary cipher — research note (candidate, read-only)

## In a nutshell
A source-attributed **symbolic arithmetic lens** for finding repeatable numerical relationships among English words. No new decision calculator or authority subsystem. This tool computes exact values; human interpretations remain interpretations unless corroborated by evidence appropriate to the claim.

**Original author's mathematical construction and spiritual framing:** Marty Leeds, [Decoding the Gematria of the English Alphabet](https://grahamhancock.com/leedsm1/) (2014). The source explicitly frames 26 letters as two mirrored halves of 13, with G/T as seven-valued centers; associates the seven-centered symmetry with the creation week, the menorah and 22/7, an *approximation* of pi; and explores the theological meaning of the pattern. **Referenced interactive calculator:** https://septenarygematria.com/ (JavaScript required). This implementation is independent clean-room arithmetic, not a copy of the website's source code or licensed interface.

## Exact cipher and meaningful examples

A–M and N–Z each carry exactly this weight sequence: `1 2 3 4 5 6 7 6 5 4 3 2 1`.

| Expression | Exact calculation | Result |
| --- | --- | --- |
| GOD | G7+O2+D4 | 13 |
| LOVE | L2+O2+V5+E5 | 14 |
| CODE | C3+O2+D4+E5 | 14 |
| JESUS | J4+E5+S6+U6+S6 | 27 |
| CHRIST | C3+H6+R5+I5+S6+T7 | 32 |
| LORD | L2+O2+R5+D4 | 13 |
| GOD + LOVE | 13+14 | 27 (matches JESUS) |
| JESUS CHRIST | 27+32 | 59 |
| 59, one-step decimal digit sum | 5+9 | 14 (matches LOVE and CODE) |
| 59, repeated digit reduction | 5+9=14, then 1+4 | 5 (distinct operation) |
| SEVEN | S6+E5+V5+E5+N1 | 22; 22/7 ≈ 3.142857, not exactly pi |

**What the pattern suggests within the author's symbolic framework:** LOVE and CODE meet at fourteen; GOD (13) with LOVE (14) reaches JESUS (27), and JESUS CHRIST's 59 returns to fourteen under *one-step* digit addition. This can be studied as a cohesive spiritual/symbolic reading. The recorded arithmetic is true **given this chosen cipher**; the spiritual interpretation is distinct from a demonstrated causal, historical or predictive claim.

## Director's extended correspondence examples (exact arithmetic)

All calculations below use the same **mirrored Marty Leeds mapping**, not another cipher or a new decision-value calculator. The mathematical *outputs* are reproducible; the proposed associations of LOVE, STAR, geometry, and five-element cosmology are spiritual/symbolic interpretations, **not independent proof of physical or divine causation**.

| Source term | Exact decomposition | Sum | Repeated digit reduction |
| --- | --- | ---: | ---: |
| HEAVEN | H6+E5+A1+V5+E5+N1 | 23 | 5 |
| CHRIST | C3+H6+R5+I5+S6+T7 | 32 | 5 |
| LOVE | L2+O2+V5+E5 | 14 | 5 |
| LEARN | L2+E5+A1+R5+N1 | 14 | 5 |
| NAYA | N1+A1+Y2+A1 | 5 | 5 |
| STAR | S6+T7+A1+R5 | 19 | 1 |
| WOOD | W4+O2+O2+D4 | 12 | 3 |
| FIRE | F6+I5+R5+E5 | 21 | 3 |
| EARTH | E5+A1+R5+T7+H6 | 24 | 6 |
| METAL | M1+E5+T7+A1+L2 | 16 | 7 |
| WATER | W4+A1+T7+E5+R5 | 22 | 4 |

**The five-element aggregation:** 12+21+24+16+22=**95**; one-step digit sum **9+5=14**, then digital root **1+4=5**. Because 95 and 14 are different operations, do not label the first letter score as 14. `STAR=19→1` uses repeated digit reduction (1+9=10, then 1+0=1). If additional rules such as pairing triangles, pentagram strokes or five-element generation/control cycles are introduced, publish the **diagram construction and ordered transform rules separately**; geometrical interpretation does not follow from the cipher total alone.

**Epistemic safeguard:** same result under a many-to-one cipher is an interesting *numerical correspondence*. Cross-channel convergence is a hypothesis requiring separately sourced geometric or textual evidence, preselected examples and comparison baselines before it can establish any factual conclusion. This does not dismiss spiritual meaning; it preserves the distinction between measured arithmetic and interpretation.

## Critical calibration controls

1. **Use the correct mapping**: some websites name a simple cyclic `1..7,1..7` alphabet cipher “Septenary”; that is **not** the mirrored Marty Leeds mapping. Example: H=6, not 1.
2. **Preserve operation provenance**: letter sum, phrase sum, decimal digit sum once, and digital root are different transforms. Never swap them silently. Selecting a transform after seeing the desired answer can manufacture patterns.
3. **Measure collisions**: ROT13 substitutions always preserve totals because A=N, B=O, etc. Unrelated words regularly have identical scores (AB=NO=3). A match alone never proves a semantic or divine connection, nor licenses a higher epistemic state.
4. **Research design**: preregister a small set of thematic expressions and a matched control corpus, lock the mapping/transform before reading results, compare observed coincidence rates with a baseline, and assess whether any independently useful prediction survives. Keep faith interpretations respectfully framed as interpretations.
5. **No new authority**: cipher output cannot alter LAW, consent, proof receipts, learning promotion, factual confidence, or `kernel/value_calculus.py` decisions without separate verified evidence and governance review. This tool is offline/read-only and can be used in a future optional knowledge explorer if it adds measured value.

## Usage and status

```bash
python -m tools.septenary_cipher 'JESUS CHRIST'
python -m tools.septenary_cipher 'CODE' --compare 'LOVE'
python -m unittest discover -s tests -p 'test_septenary_cipher.py' -v
```

Local focused tests check full mapping, letter-by-letter vectors, spiritual example arithmetic, digit-sum distinction, ROT13 collision negative control, Unicode refusal, and source/truth boundary. Exact-main integrated verification, independent review, production deployment and causal learning effects are **not claimed**.

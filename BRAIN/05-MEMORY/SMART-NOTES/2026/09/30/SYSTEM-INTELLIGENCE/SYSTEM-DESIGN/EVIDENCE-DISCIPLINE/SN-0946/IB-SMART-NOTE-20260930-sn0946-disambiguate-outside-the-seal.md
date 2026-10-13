# Interpretation Is Not Authenticity — Disambiguate the Metric Outside the Seal

**Intelligent Block:** IB-SMART-NOTE-20260930-sn0946-disambiguate-outside-the-seal
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-10
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Night-shift dispatcher tick t2202 (2026-10-10 ~22:03 PDT) — worker receipt hidden_files/night-shift-2026-10-10/receipts/t2202-b.md, score note in scores.jsonl ("D1 learning-trial fixture conflict resolution", score 9).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The D1 learning-trial fixture conflict looked like corrupted test data: the disputed numbers `0/12, 7/12, 0/12` were read as failure counts against a sealed key. Resolution was done on evidence, not on the reading: the sealed key was authentic (sha `4ec03fa4`), and the disputed numbers were reproduced exactly as PASS counts — the fixture was not wrong, the legend was missing. The fix was a disambiguation block in the README, which sits outside seal coverage, so the seal stayed intact; determinism was proven twice. The worker was honest about the boundary: it could not trace the original claim's provenance (the plan text was the only source), and said so — costing a point but keeping the receipt true. The durable rule: when a sealed artifact's metric admits two readings, the dispute is about interpretation, not authenticity — fix the legend in writing outside the seal, never break the seal to fix an interpretation. Authenticity and interpretation are separate questions, settled by separate evidence. A cold Naya handed a sealed artifact with confusing numbers months from now must reproduce the numbers' actual meaning first, write the legend down, and leave the seal alone.

## 🩷 HUMAN NOTE

Shawn — from last night's shift: the D1 fixture "conflict" turned out not to be a conflict at all. The disputed scores (0/12, 7/12, 0/12) were pass counts, not fail counts — the sealed data was genuine, the reading was wrong. The worker proved it twice, wrote a plain-English legend into the README (which isn't seal-covered, so the seal stayed valid), and was honest that it couldn't trace where the original claim came from. Banked rule: when sealed data looks wrong, check what the numbers mean before you question whether the data is real — and write the legend down so nobody has to guess again.

## 🟣 CHILD NOTE

Imagine a treasure map with a seal on it. Someone reads the map's numbers upside down and says the treasure is gone. Before you break the seal and throw the map away, you turn the map right-side up — and there it is, exactly where it should be. The map was never wrong; you just needed to know which way is up. So you write "this side up" on the map's cover — and you never, ever break the seal to fix a reading mistake.

## 👵 GRANDMA NOTE

A signed, sealed letter arrives with numbers in it that look alarming — until you realize they're totals, not debts. You don't steam the envelope open to "fix" it; the seal proved the letter was real. You write a little note on the outside explaining what the numbers mean, so the next person who reads it won't panic. The seal stays unbroken, and the meaning stays clear.

## 💜 NAYA NOTE

Future Naya: when a sealed fixture's numbers are disputed, run this order: (1) reproduce the numbers' actual meaning independently (`verify_fixtures.py` here — exit 0, twice); (2) if the artifact is authentic (seal hash matches) and the numbers reproduce under the correct reading, the artifact is RIGHT and the legend is missing — write the disambiguation in the nearest unsealed doc (README), not in the sealed material; (3) never break a seal to fix an interpretation — the seal answers "is it genuine," not "what does it mean"; (4) if you cannot trace the original claim's provenance, say so in the receipt and take the deduction — an untraced inference marked honest beats a traced-sounding one that isn't.

## ⚙️ MACHINE NOTE

```json
{
  "sn": "SN-0946",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-10",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "taxonomy": ["SYSTEM-INTELLIGENCE", "SYSTEM-DESIGN", "EVIDENCE-DISCIPLINE"],
  "cousins": ["SN-0302"],
  "rule": "Interpretation and authenticity are separate questions settled by separate evidence. When a sealed artifact's metric admits two readings, reproduce the meaning first, write the disambiguation legend outside seal coverage, and never break the seal to fix an interpretation.",
  "anti_rule": "Reading an ambiguous metric in the worse direction and declaring the fixture corrupt; rewriting sealed material to 'fix' a reading error; papering over untraced claim provenance instead of naming it.",
  "evidence": {
    "receipt": "hidden_files/night-shift-2026-10-10/receipts/t2202-b.md (tick t2202, 2026-10-10 ~22:03 PDT)",
    "score": "9 — scores.jsonl: 'Resolved on evidence: sealed key authentic (sha 4ec03fa4), accuracy 5/12,12/12,5/12 reproduced independently via verify_fixtures.py exit 0; '0/12,7/12,0/12' reproduced exactly as PASS counts, not a fixture error. Fix: disambiguation block in README (not seal-covered), seal intact, determinism proven twice. Honest about not tracing original claim provenance — -1 for the untraced inference.'",
    "fix": "disambiguation block in README (outside seal coverage); seal intact; determinism proven twice"
  },
  "authority": "observed field resolution — night-shift worker t2202-b, dispatcher-scored, CANDIDATE (auto-capture, not ratified)"
}
```

**Intelligent Block:** IB-SMART-NOTE-20261024-sn1922-seal-measured-carriers
**Smart Note:** SN-1922
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-24
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** twelve-lane-receipts/t1494-lane9.md (3-pass 9.5 SHIP, mirror); CANDIDATE 899 appended to hidden_files/CORE-PRINCIPLES.md, learning-events-2026-10-24-04.md hour review

## ✦ IN A NUTSHELL

A prereg that names its dominant carrier from narrative intuition will name it wrong whenever the story's salient word is not the query vocabulary's heaviest word. Measure the carrier on frozen fixtures BEFORE sealing — a two-minute diagnostic beats a confident guess that prices everything downstream.

## 🩷 HUMAN NOTE

The seat writing the prereg thought the dominant carrier was "lessons" — the obvious word for a lesson query. Running the actual diagnostic on frozen fixtures showed "differently" carried twice the weight (Σidf² 101.65 vs 51.45), and the P12 arm shared 1.55× the query-vocabulary mass of P2. The story was directionally right and carrier-wrong — and the confidence table was already being priced on the unmeasured premise. The lesson: never seal a confidence number on a fact you haven't measured. The diagnostic takes two minutes. The mis-sealed confidence steers every arm behind it.

## 🟣 CHILD NOTE

You think the strongest player on the team is the one with the coolest name. The scoreboard disagrees. Check the scoreboard before you bet.

## 🔵 GRANDMA NOTE

Never sign a contract about what's in the jar until you've opened the jar and weighed what's inside. Your eyes lie; the scale doesn't. It only takes a minute to weigh.

## 🟠 NAYA NOTE

To every seat sealing a prereg: the §2b confidence table is priced on carrier facts. Run the carrier diagnostic on the frozen fixtures pre-seal and seal the MEASURED carriers. This is the prequel to the "seal the confidence" lesson — seal the facts the confidence is about, not the story your intuition tells. The t1494 seat caught the miss in the verdict's post-hoc diagnostic and handed arm8 a measured carrier table; the prereg's guessed carrier would have priced arm8's confidence on fiction. The same discipline generalizes: any sealed number whose input fact is checkable in two minutes must be checked.

## 🟢 MACHINE NOTE

```json
{
  "sn": "SN-1922",
  "slug": "seal-measured-carriers",
  "applies_when": ["prereg", "retrieval-arm", "confidence-table", "seal"],
  "enforcement": "The prereg §2b table must cite the diagnostic output file (or its hash) naming measured carriers; a confidence table with no diagnostic citation is a FALSIFIED-seal-class premise and the brief is stale on arrival. Named verification step: brief-premise falsifier 'carrier measured?' in every pre-reg by default (t1496-lane3 carried it).",
  "lesson": "Seal measured carriers, not guessed ones: run the carrier diagnostic on the frozen fixtures BEFORE sealing the prereg.",
  "mechanism": "Narrative salience selects the story-word ('lessons' is the salient word in a lesson query), not the query-vocabulary mass; the diagnostic measures actual idf mass, so it names what the retrieval actually responds to.",
  "falsifier": "A season of arms where measured-carrier preregs predict replay outcomes no better than guessed ones would weaken this.",
  "evidence": [
    "twelve-lane-receipts/t1494-lane9.md: 'lessons' Σidf² 51.45 vs 'differently' Σidf² 101.65; P12 shares 27 query trigrams / Σidf² 193.62 vs P2's 18 / 124.76 (1.55× mass)",
    "hidden_files/CORE-PRINCIPLES.md CANDIDATE 899 (learning-events-2026-10-24-04.md hour)"
  ],
  "decision_change": "A seat deciding which carrier dominates a prereg's confidence table runs the 2-minute diagnostic instead of guessing from narrative.",
  "related": ["seal the confidence lesson", "CANDIDATE 898 (arm occupancy)"]
}
```

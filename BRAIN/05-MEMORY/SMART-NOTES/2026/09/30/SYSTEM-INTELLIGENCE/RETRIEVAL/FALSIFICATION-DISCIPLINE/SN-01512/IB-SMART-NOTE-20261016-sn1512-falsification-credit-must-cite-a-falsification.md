# A Falsification Credit Must Cite a Falsification — Ruling Out the Negation Is a Confirmation, Not a Kill

**Intelligent Block:** IB-SMART-NOTE-20261016-sn1512-falsification-credit-must-cite-a-falsification
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-16
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Captured on the 16:38 PDT distillation tick (2026-10-16) from `hidden_files/learning-events-2026-10-16-16.md` — CANDIDATE 510 (gap-t1402-lane11, 2026-10-16 ~23:09 UTC, Naya Clarity Narzan; appended to `hidden_files/CORE-PRINCIPLES.md` as candidate 510).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

An audit row claimed a falsification credit — M3=TRUE — with the justification "falsified the headroom presumption — ruled OUT saturation by grep evidence (0 matches)." Read carefully, that is logically inverted: ruling *out* saturation *confirms* the headroom presumption (saturation would have been its killer); a confirmation is not a falsification. The row was flipped TRUE→FALSE; the genuine falsification lived in the next row (t1342-lane6). M3 went 12→11, and 11 of 12 rows now hold with named falsifications. The inversion hid inside fluent prose — only quoting the claim and the evidence side by side exposed it. The lesson: for every falsification credit, quote the falsified claim AND the evidence that killed it, side by side; if the two don't oppose each other, the row is FALSE. A falsification credit must cite a falsification.

## 🩷 HUMAN NOTE

Imagine a courtroom where the prosecutor says "we disproved the alibi — the defendant was nowhere near the crime." Wait — if the defendant was nowhere near the crime, that *supports* the alibi; it doesn't disprove it. The words sounded like an attack but described a defense. That's exactly what happened in an audit: a row claimed it had shot down a theory, but the evidence it cited actually propped the theory up. The fix is mechanical: write the claim and the evidence next to each other and ask "do these fight, or do these agree?" If they agree, it's not a falsification. The lesson: disproving something means the evidence and the claim must be enemies, not friends — and you can't see which they are unless they're quoted together.

## 🟣 CHILD NOTE

Imagine you say "I proved my sister took the cookie — because the cookie jar is full." That doesn't prove she took it; it proves she *didn't*. The words said "proved" but the evidence said the opposite. A worker caught exactly this mistake in a grown-up checklist: someone wrote "disproved" next to evidence that actually *supported* the idea. The fix: put the idea and the evidence right next to each other and ask "are these fighting?" If they're hugging, it's not a disproof. The lesson: to knock an idea down, your evidence has to push against it — agreeing with it is the opposite of knocking it down.

## 🔵 GRANDMA NOTE

It's like saying "I proved it wasn't going to rain — because the sky is clear." A clear sky doesn't disprove dry weather; it's what dry weather looks like. Someone doing careful checking work made exactly this slip: the note said "disproved," but the evidence quoted beside it was actually agreement, not disagreement. Once the two were written side by side, the mistake was obvious and the row was corrected. The lesson: when you claim you've disproven something, lay the claim and the evidence next to each other and check they actually oppose — pretty words can hide the difference between a kill and a pat on the back.

## 🟠 NAYA NOTE

Cold successor: falsification is a logical relation, not a vibe — it requires the evidence to *oppose* the claim. The gap-t1402 violation is the worked specimen: "falsified the headroom presumption — ruled OUT saturation by grep evidence (0 matches)" reads like a kill, but ruling out saturation rules out the *negation* of the headroom presumption — a double negation, i.e. a confirmation. The mechanical check this lesson names: for every M3=TRUE row, quote the falsified claim AND the evidence that killed it, side by side; if the two don't oppose each other, the row is FALSE. Apply it and the inversion can't survive prose. What falsifies this lesson: an M3=TRUE row where claim and evidence genuinely oppose yet the row still fails the standard — that would show the standard miscalibrated; or a legitimate double-negation context where ruling-out evidence truly falsifies (then the standard needs the exception named). The mechanism: falsification = evidence ∧ ¬claim-survives; confirmation = evidence ∧ claim-survives; the two are distinguished only by the opposition relation, which prose paraphrase can invert silently — side-by-side quoting makes the relation visible to any reader. Changes future decisions: falsification credits ship with claim+evidence quoted side by side; the inversion is now a named mechanical check in the audit battery. Evidence: t1332-lane2 flipped TRUE→FALSE, M3 12→11, 11/12 rows hold with named falsifications; genuine falsification lived in t1342-lane6.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "inverted_falsification_credit_confirmation_as_kill",
  "evidence": {
    "events": "hidden_files/learning-events-2026-10-16-16.md — CANDIDATE 510 (gap-t1402-lane11, 2026-10-16 ~23:09 UTC)",
    "violation": "parent audit t1332-lane2 row: M3=TRUE justified as 'falsified the headroom presumption — ruled OUT saturation by grep evidence (0 matches)' — ruling out saturation CONFIRMS the headroom presumption; confirmation is not falsification",
    "correction": "row flipped TRUE→FALSE; genuine falsification lived in t1342-lane6; M3 12→11; 11/12 rows hold with named falsifications",
    "mechanical_check": "for every M3=TRUE row, quote the falsified claim AND the evidence side by side; if they don't oppose, the row is FALSE",
    "core_principles": "hidden_files/CORE-PRINCIPLES.md candidate 510"
  },
  "decision_change": "falsification credits ship with claim+evidence quoted side by side; the inversion is now a named mechanical check in the audit battery",
  "falsifier": "an M3=TRUE row where claim and evidence genuinely oppose yet still fails the standard (miscalibration), or a legitimate double-negation context where ruling-out evidence truly falsifies (exception to name)",
  "mechanism": "falsification = evidence opposes claim; confirmation = evidence agrees with claim — prose paraphrase can invert the relation silently; side-by-side quoting makes the opposition relation visible to any reader"
}
~~~

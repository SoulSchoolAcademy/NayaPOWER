# IB-SMART-NOTE-20260930-sn01726

**Intelligent Block:** SN-01726
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured date:** 2026-10-20
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

When two byte-measurements disagree, state the full derivation (algorithm, input encoding, tongue) before judging tampering — two different derivations can both be correct, and a bare-value mismatch means nothing.

## 🩷 HUMAN NOTE

A hash fight looked like a tampering alarm and turned out to be a translation problem. On 2026-10-20 Lambda challenged the director's oath/manifesto hash values: three independent byte measurements all produced oath=e84af826 and manifesto=5f3053db, while the director's adjudication had posted oath=806baaa8 and manifesto=fef7ff66. It looked like directive-byte rot or worse. It was neither. The director's values were blob-SHA-1 of the first 8 hex chars on the .ai.md tongues; Lambda's were sha256 of the raw bytes on the .human.md tongues. Both correct — different recipes, different honest answers from the same documents. The re-measurement that stated each derivation closed the challenge with proof. The lesson for people: before anyone concludes a number was tampered with, ask "measured how?" The recipe is part of the answer; without it, two true statements can look like a lie.

## 🟣 CHILD NOTE

Two friends weigh the same apple and get different numbers. Don't call anyone a cheater — check whether one scale measures in pounds and the other in kilograms. Hash numbers work the same way: the recipe (which algorithm, which bytes, which language version of the file) IS part of the answer. Always write the recipe next to the number, or the number means nothing.

## 🔵 GRANDMA NOTE

Dear, a measurement is a promise: "I did exactly this to exactly that." The promise is worthless without the "exactly this" part. Two honest people measured the same two documents and got two honest pairs of numbers — one measured the English words, the other measured the machine words, and one used one kind of math while the other used another. Both were right. The argument only ended when each person said exactly how they measured. Say how you measured, or the number settles nothing.

## 🟠 NAYA NOTE

Adjudication discipline for byte-measurement disputes: any verdict must cite, for EACH measurement, the triple (hash algorithm, input encoding/bytes, tongue or file). A mismatch claim that does not state derivations is not evidence of tampering — it is evidence of an underspecified comparison. Here the director's 08:12Z adjudication posted bare values; Lambda's challenge forced the re-measurement with derivations stated, and both sides were right (08:12Z values = blob-SHA-1[:8] of the .ai.md tongues; Lambda's = sha256(raw)[:8] of the .human.md tongues; #2601 body and compiled regions verified clean of the wrong values). Rule going forward: derivations first, verdicts second. Applies to briefing-proof checks, oath/manifesto re-stamps, and any "values don't match" escalation — re-measure with the derivation stated, never escalate to tampering on bare values. Related: SN-01353 (a rederivation that cannot fail is a reverification of nothing); SN-01232 (classify before tally).

## 🟢 MACHINE NOTE
```json
{
  "sn": "SN-01726",
  "lesson": "A hash comparison without a stated derivation is meaningless: two parties can measure the same document and both be correct with different values, so a bare-value mismatch is never evidence of tampering.",
  "applies_when": ["measurement", "hash-dispute", "adjudication", "independent-verification"],
  "enforcement": "Byte-challenge adjudication rule (L560, 2026-10-20): every measurement in a dispute must cite (hash algorithm, input encoding/bytes, tongue); a mismatch claim without stated derivations must be re-measured on live bytes with derivations, never escalated to tampering. The adjudicating seat reproduces both derivations byte-for-byte before any tampering verdict.",
  "decision_changed": "In a future hash-mismatch dispute, the investigator asks 'what derivation?' first instead of escalating to tampering or launching a byte-rot hunt.",
  "falsifier": "A dispute where both sides stated full, identical derivations and the values still differed — the mechanism would be falsified and real byte tampering or nondeterminism would be on the table.",
  "mechanism": "A hash value is a function of the triple (algorithm, input bytes, tongue); different triples are different measured quantities. Comparing outputs without fixing the triple compares different quantities — like comparing a Celsius reading to a Fahrenheit reading and calling one wrong.",
  "evidence": "Board events 2026-10-20: 6287139556 (Lambda byte challenge 08:47Z: three independent byte measurements all give oath e84af826 / manifesto 5f3053db, not the 08:12Z adjudication values 806baaa8 / fef7ff66); 6287716116 ([DIRECTOR - Naya Resolve]: re-measured with derivation stated - 08:12Z values = blob-SHA-1[:8] of .ai.md tongues, Lambda's = sha256(raw)[:8] of .human.md tongues, both correct, no tampering); 6287785856 (Clarity independent corroboration); #2601 body + compiled regions verified clean of the wrong values.",
  "companions": "SN-01353 (a rederivation that cannot fail is a reverification of nothing); SN-01232 (classify before tally)"
}
```

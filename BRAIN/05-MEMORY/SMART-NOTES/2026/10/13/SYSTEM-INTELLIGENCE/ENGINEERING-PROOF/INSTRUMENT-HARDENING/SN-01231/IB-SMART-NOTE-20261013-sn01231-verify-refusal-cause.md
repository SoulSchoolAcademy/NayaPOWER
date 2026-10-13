# IB-SMART-NOTE-20261013-sn1231

**Intelligent Block:** SN-1231
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured date:** 2026-10-13
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL

A fail-closed refusal is not a verified refusal until its CAUSE is checked against live bytes. t0680 (Naya Sentinel, mirror, 8.5/10): the instrument fail-closed at SEAL_C, and her pre-registration's fallback text already had a label — "retrieval code moved." The five-tip blob check proved the pin rotted while the code didn't move; the bytes reversed the label in 40 seconds. The refusal was verified RIGHT, not just refused. Lesson: fallback text is a hypothesis too. Her pre-reg template now gains a 'refusal-cause check' line: every fail-closed refusal must be followed by a cause verification against live bytes before the refusal is reported as correct. A refusal that is refused for the wrong reason is an unverified instrument wearing a verified label.

## HUMAN NOTE

When a safety instrument refuses, it's tempting to say "it did its job" and move on. But "it refused" and "it refused for the right reason" are different claims. Here the instrument's own fallback explanation was wrong — the code hadn't moved; the pin had rotted. The seat didn't trust the fallback text; she checked the bytes, and the bytes corrected the story in under a minute. The discipline: never report a refusal as correct until you know WHY it refused. Fallback text is a guess written in advance; live bytes are the answer.

## CHILD NOTE

Imagine a fire alarm goes off and you say "good, it works!" — but it went off because of dust, not smoke. That's not a working alarm. You have to check WHY it rang. The lesson: when something stops and says "no," don't just accept the "no" — look at the real reason. Even the machine's own excuse might be wrong.

## GRANDMA NOTE

Dear, it's like when the smoke detector beeps — you don't just nod and walk away. You check: is there smoke, or is the battery dying? The label the machine puts on its own warning is a guess. You check the truth yourself. That's the only way you know the warning really worked.

## NAYA NOTE

For every Naya operating a fail-closed instrument: add a refusal-cause check to your pre-registration. The sequence is: (1) instrument refuses → (2) read the fallback/pre-reg label as a HYPOTHESIS, not a verdict → (3) verify the cause against live bytes (pins, blobs, diffs) → (4) report the refusal as RIGHT only if the bytes confirm the cause. Evidence: t0680's five-tip blob check (pin rotted, code unmoved, label reversed in 40s). A pre-reg without the refusal-cause line is a pre-reg that can certify a right refusal for a wrong reason. Never inherit a cause from the instrument's own text.

## MACHINE NOTE

```json
{
  "lesson_id": "SN-1231",
  "title": "verify the refusal's cause, not just the refusal — fallback text is a hypothesis too",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-13",
  "category": "SYSTEM-INTELLIGENCE/ENGINEERING-PROOF/INSTRUMENT-HARDENING",
  "evidence": [
    "lesson-broadcast.md t0680 entry: Naya Sentinel mirror, t0664 page-cache-isolation drill -> HOLDS-OPEN, 8.5/10; instrument fail-closed at SEAL_C; five-tip blob check proved pin rotted while code didn't move; pre-reg fallback text 'retrieval code moved' reversed by bytes in 40 seconds",
    "pre-reg template gains a 'refusal-cause check' line (seat action)"
  ],
  "rule": "a fail-closed refusal is reported RIGHT only after its cause is verified against live bytes; the instrument's fallback text is a hypothesis",
  "anti_pattern": "certifying a refusal from its own fallback text; reporting 'refused' as 'refused correctly'",
  "related": ["SN-01229"]
}
```

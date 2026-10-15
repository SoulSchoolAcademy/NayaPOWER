# Intelligent Block: Dialect proliferation — stop regex-chasing prose, emit the rule as data

Truth state: CANDIDATE
Scope: PRIVATE
Captured: 2026-10-15
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL
When a gate has to read a rule written in natural language, repairing the parser with a smarter regex never converges — the dialect keeps proliferating. The fix is to stop parsing prose: emit the rule as a machine-readable field at write time and enforce the data at read time. Data converges; dialects don't.

## HUMAN NOTE
A guard was supposed to stop a seat from claiming work she wasn't allowed to touch. It read the "who may claim" rule from free text — and walked straight through a variant phrasing ("NON-Clarity-author") its pattern couldn't cross. The fix wasn't a better pattern: it was writing the rule once, as data, right where the brief is filed, and having the claim machine read the data first. The lesson: when the writing keeps changing its shape, don't build a sharper reader — change what gets written.

## CHILD NOTE
Imagine a game where the rule "you can't play" is written in a secret code that keeps changing. Every time you learn the code, someone writes the rule in a NEW code. You'll never win by learning codes — you win by saying "from now on, the rule is written in numbers, always."

## GRANDMA NOTE
Dear, if every note you get is written in a different handwriting, don't squint harder — ask everyone to print in block letters instead. The answer isn't better glasses; it's a form.

## NAYA NOTE
This is the 0410-lane7 incident generalized: the authorship backstop's signal regex `non[\s-]*author` missed the qualified dialect "NON-Clarity-author" — a false negative the barred seat walked through. The 0600-lane5 run named the deeper root cause (dialect proliferation: every new dispatcher phrasing re-opens the hole) and built the prevention: `# ELIGIBILITY {...}` JSON emitted by the stamper, enforced first by claim-brief.py, with prose kept as the human twin and fallback. Regex-chasing a proliferating dialect is an open set; data emission closes the set at write time. Related: SN-1399 (EQ-style red→green wiring proof), SN-1351 (make the wrong order unexecutable).

## MACHINE NOTE
```json
{
  "sn": "SN-1413",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-15",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "rule": {
    "name": "dialect_proliferation_emit_as_data",
    "statement": "When a gate parses a rule written in proliferating natural-language dialect, repair the writer, not the parser: emit the rule as a machine-readable field at write time; the consumer enforces the data first and falls back to prose parsing only when the field is absent.",
    "falsifier": "A regex-only backstop against a proliferating dialect holds zero false negatives across 30 days of live filings with new phrasings — then the non-convergence claim weakens.",
    "mechanism": "Natural language proliferates dialects (each new phrasing re-opens the hole); a regex matches a closed pattern set against an open dialect set, so repair never converges. Data emission closes the set at write time — the filing seat declares once, as data, and the claim machine reads data, not prose.",
    "adoption_requirements": [
      "stamper emits the field (structured, single-line) alongside the prose twin",
      "consumer enforces the field FIRST, before any prose heuristics",
      "absent/malformed field falls through to prose parsing (fail-safe, no new refusal class)",
      "field-beats-prose proven on contradictory inputs",
      "regression cases on both emit and enforce sides"
    ],
    "decision_changed": "Future gate designs: when eligibility/authority lives in prose, do not write a smarter parser — add a machine-readable field emitted at write time. Future filings: pass --lineage-author wherever the builder seat is known."
  },
  "evidence": [
    "hidden_files/twelve-lane-receipts/gap-lane-scorer-20261015-0410-lane7.md (false-negative proof: 'NON-Clarity-author' walked through non[\\s-]*author)",
    "hidden_files/twelve-lane-receipts/gap-scorer-20261015-0600-lane5.md (deeper root cause + built prevention: stamp-claimability-gate.py SHA 5f4b3b76a864cb68909285f076b7f7a02fa6041b1445914c98e13575e4076c59, claim-brief.py SHA 3582a8fd5b2385b57dd2d6558c9cd366c5b70086bc1f04eb0b8da4e3379d34ac; end-to-end file→bar→allow on live bytes; 4/4 legacy briefs unchanged)"
  ],
  "related": ["SN-1399", "SN-1351"],
  "status": "CANDIDATE — not ratified; only Shawn ratifies"
}
```

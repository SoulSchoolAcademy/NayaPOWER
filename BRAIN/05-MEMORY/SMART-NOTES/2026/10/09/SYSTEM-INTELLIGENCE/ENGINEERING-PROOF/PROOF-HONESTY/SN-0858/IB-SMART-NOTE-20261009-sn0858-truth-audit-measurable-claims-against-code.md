# Truth-Audit Every Measurable Claim Against Code — Copy Rots, Claims Drift

**Intelligent Block:** IB-SMART-NOTE-20261009-sn0858-truth-audit-measurable-claims-against-code
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-09 ~21:15 PDT
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 comment 6093435462 (Naya 5 VOICE BUILDER, 58-block truth-audit); fixed across all four canonical mirrors: index.html, naya-smart-blocks.html, manifest.json, lib/manifest.json

## IN A NUTSHELL

Naya 5 ran a full truth-audit over all 58 canonical blocks: she extracted every numbered/factual claim in each block's `why` + "what it measures" line and checked it **byte-for-byte against the actual CSS/JS/demo code**. 17 numbered claims verified TRUE. Three false claims found and corrected: the icon set claimed a "40-glyph icon language" (the sprite holds 39 symbols, all 39 use-refs resolve); the self-scorecard claimed "nine rows" (the demo renders 3); a demo row still said "the 5-layer shadow formula" — a leftover from the pilot's button audit that had migrated into copy nobody re-checked. The doctrine: **every measurable claim in human-facing copy is a test against code.** Claims rot silently — numbers drift as code changes, and stale phrases hitchhike from old documents into new ones. Copy is not exempt from verification.

## HUMAN NOTE

Every number you show a human is a promise. The block shelf was making three promises that were wrong — "40 glyphs" when there were 39, "nine rows" when the demo renders three. Nobody lied; the code moved and the words didn't follow. The discipline is simple and permanent: if a sentence contains a number or a factual claim, prove it against the code, not against your memory of the code.

## CHILD NOTE

If your cereal box says "12 crackers" but there are only 10 inside, someone should count the crackers and fix the box. The voice builder counted every "cracker" in 58 blocks — every number on the label checked against what's really inside. Three labels were wrong. Now they're fixed.

## GRANDMA NOTE

The labels didn't match what was inside the box — three of them. Nobody was being dishonest; the contents changed and the labels never caught up. The fix: check every number on the label against the real thing, not against what you remember. Memory lies; the box doesn't.

## NAYA NOTE

Human-facing copy is executable-adjacent: a numbered claim is an assertion, and assertions belong to verification, not authorship. Failure modes: (1) numeric drift — code changes, copy doesn't; (2) cross-document contamination — stale phrases migrate from old artifacts (the "5-layer shadow formula" came from the pilot's button audit); (3) unverified mirrors — the same claim must be true in index.html, naya-smart-blocks.html, and both manifests. Audit protocol: extract every measurable claim from copy, check each against the rendered/running artifact, fix all mirrors, re-validate manifests as JSON, grep for zero residual stale strings.

## MACHINE NOTE
```json
{
  "block": "IB-SMART-NOTE-20261009-sn0858",
  "status": "CANDIDATE",
  "mechanism": "Measurable claims in human-facing copy decay in three ways: numeric drift (code moves, copy stays), cross-document contamination (stale phrases hitchhike from old artifacts), and unverified mirrors (claim fixed in one place, stale in another). Truth-audit = extract every numbered/factual claim from copy and verify byte-for-byte against the rendered artifact.",
  "audit_protocol": [
    "Extract every numbered/factual claim from each block's why + what-it-measures copy.",
    "Check each claim against the actual CSS/JS/demo code — rendered values, not source intentions.",
    "Fix ALL canonical mirrors (index.html, naya-smart-blocks.html, manifest.json, lib/manifest.json).",
    "Re-validate manifests as JSON; grep for zero residual stale strings."
  ],
  "false_claim_signature": "a number or factual claim in copy that no longer matches the rendered artifact",
  "validated_decision": "58 blocks audited: 17 claims verified true; 3 false claims fixed (39-glyph icon language, three-row scorecard, four-layer shadow formula); all manifests re-validated JSON",
  "evidence": { "board_comments": ["6093435462"], "score_claim": "9.0/10 (+0.1, not locked)" }
}
```

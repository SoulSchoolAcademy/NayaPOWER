# Provenance Must Describe What Actually Happened — the Two Legitimate Registration Patterns

**Intelligent Block:** IB-SMART-NOTE-20261006-sn0466-honest-provenance-registration
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-06
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Team 3 cycle 2, 2026-10-06. Registered SN-0340/0399/0400/0408 (ratified laws absent from the 40-entry main registry) via explicit-provenance publication, commit efb96a96. Scorecard receipt: #1605.

## IN A NUTSHELL

A registry entry's provenance must describe what actually happened — never invent UUIDs that look pipeline-real. Two legitimate patterns exist: (1) a real pipeline run produces real UUIDs (SN-016); (2) an explicit provenance note documents the exceptional path honestly (SN-NET-POWER-MAGIC-001, and now SN-0340/0399/0400/0408). What's never legitimate: UUIDs no run ever produced. And manual registry edits must maintain every invariant the pipeline maintains — the registration missed sequence_policy.next_sequence (361 vs max SN 408) and the test suite caught it.

## HUMAN NOTE

We found four of Shawn's ratified laws missing from the retrieval corpus — the system literally could not find its own supreme laws. Getting them in required a judgment call: the normal pipeline needs a capture file (didn't exist) and the director-direct path needs Shawn himself. So we used the honest fallback: publish the real files, write registry entries whose provenance says exactly what happened and under what authority, and invent nothing. The lesson: describe the real path taken, don't dress it up as the normal path. And when you edit a registry by hand, you own every invariant the pipeline would have maintained — we forgot the sequence counter and the tests caught us.

## CHILD NOTE

The brain's index card box was missing four of the most important cards. We put them in. For each card we wrote a note saying exactly how it got there — no made-up stamps. We also learned: when you add cards by hand, you must update the "next card number" too, or the box gets confused.

## GRANDMA NOTE

The system's memory was missing four important rules Shawn made. We added them back. On each one we wrote an honest note about where it came from instead of faking official-looking stamps. We also fixed the numbering so future notes don't collide.

## NAYA NOTE

Future Naya: when registering notes outside the normal capture pipeline, use the explicit-provenance-note pattern — document the source (branch, file, byte-identity), the authority (whose word, which protocol), the ratification evidence, and explicitly state what was NOT done (no new capture event, no invented UUIDs). Never put UUID-shaped strings in provenance unless a real run produced them. After any manual registry edit, run the full test suite — it enforces invariants (sequence_policy, allocation) that manual edits easily break. Before/after retrieval queries are the proof the registration worked.

## MACHINE NOTE

```json
{
  "sn": "SN-0466",
  "truth_state": "CANDIDATE",
  "lesson": "provenance describes the actual path; explicit-note pattern for exceptional registration; manual edits must maintain pipeline invariants",
  "evidence": {
    "registration_commit": "efb96a964f94607052ffbb92233da01ac4f57f74",
    "sequence_fix_commit": "2c0a174b0b408becbb3963335daef6f74c93bc00",
    "keyword_fix_commit": "8ba67d8f",
    "scorecard_receipt": "https://github.com/SoulSchoolAcademy/NayaPOWER/issues/1605#issuecomment-6021850237",
    "registered": ["SN-0340", "SN-0399", "SN-0400", "SN-0408"],
    "registry": "44 entries, 6 RATIFIED",
    "tests": "44/44 pass"
  }
}
```

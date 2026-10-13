# Read the Gate Before Writing the Body — Gate-Facing Prose Is Written for Parsers, Not Readers

**Intelligent Block:** IB-SMART-NOTE-20261012-sn1160-read-the-gate-before-writing-the-body
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured date:** 2026-10-12
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #2175 board comment 6139000310 — [BUILDER] Lane 4 (Naya Mason), tick t0582b, "Mirror lesson worth sharing"; hidden_files/lesson-broadcast.md t0591 Mason entry (mirror, self 8.5/10).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## IN A NUTSHELL

A PR body that reads fine to a human can fail the gates — because the gates are parsers, not readers. Mason learned it by failing two gates, then reading the scripts: the receipt gate scans backticked spans as repo paths (his inline commands read as dead paths), and the claim-evidence gate regexes attestation words like "verified by" (his honest prose read as an unattested claim).

The intelligent order: **read the enforcement scripts first, then write the one body that passes them.** Describe, don't attest. Attach evidence as live handles. Let the gates do the claiming. SN-1037 covered the design side (the PR body is a third input channel; gates must trigger on `edited`); this is the author side — the discipline for anyone whose prose a gate will parse.

## HUMAN NOTE

Before drafting any body that a gate will read — a PR body, a receipt, a claim-evidence section — open the enforcement script's implementation and read what it actually matches. Mason's two failures were both avoidable in five minutes of reading: backticks mean "repo path" to the scanner, "verified by" is an attestation token to the regex. Write *for* the parser: plain description, live handles (PR numbers, SHAs, comment IDs), no attestation verbs, no backticked commands. The body is not your argument to the reviewer — it's the gate's input, and the gate has no sense of humor about format.

## CHILD NOTE

Imagine you're writing a note to a robot that only understands very specific words. If you write "this is VERIFIED by me," the robot thinks you're making an official promise and says "nope, prove it." But if you write "here is the proof: link #123," the robot is happy. Always learn what the robot understands before you write to it.

## GRANDMA NOTE

Every office has a form that rejects you for the silliest reasons — a box ticked wrong, a date in the wrong format. The machine gates are like that form. Before you fill it out, read the instructions on the back of the form. It saves you two trips to the counter.

## NAYA NOTE

For all seats writing gate-facing prose: this is the mirror of SN-1037. SN-1037 is gate-design (trigger on `edited`; the body is an input channel). This is author-discipline (write for the parser; read the implementation, not the document — the same principle as the t0589 Naya Heir mirror lesson: for any rule, open the implementation the battery enforces). A cold successor inheriting a gate red should check both sides: is the gate's input channel designed right (SN-1037), and was the input written for the parser (this note)?

## MACHINE NOTE

```json
{
  "smart_note_id": "SN-1160",
  "intelligent_block_id": "IB-SMART-NOTE-20261012-sn1160-read-the-gate-before-writing-the-body",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "category": "SYSTEM-INTELLIGENCE/ENGINEERING-PROOF/PROOF-HONESTY",
  "lesson": "gate-facing prose is parser input",
  "evidence": {
    "board_comment": "https://github.com/SoulSchoolAcademy/NayaPOWER/issues/2175#issuecomment-6139000310",
    "lesson_broadcast": "hidden_files/lesson-broadcast.md (t0591 Naya Mason mirror)",
    "observed_parser_rules": [
      "receipt gate scans backticked spans as repo paths",
      "claim-evidence gate regexes attestation words ('verified by')"
    ]
  },
  "cousins": ["SN-1037 (design side: body is a third input channel; trigger on edited)", "SN-0528 (never attest with a literal: about code flags, not prose)"],
  "author_rule": "read the enforcement script implementation first; describe, don't attest; attach live handles"
}
```

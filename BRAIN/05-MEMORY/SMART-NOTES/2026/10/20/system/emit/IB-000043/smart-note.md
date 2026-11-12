# Smart Note — IB-000043

> Governed repository projection of a canonical Intelligent Block.
> Canonical receiver: `v7-smart-note-canonical` · Transaction: `259d4c2f-12a1-4ace-aef5-6d06ffd033cc`
> Authority grant: `e76612a5-c571-4d52-bf3d-2228a8836c56` (single-transaction, action `smart_note_github_projection`)
> Projected at: 2026-10-20T17:16:41.431Z · Content SHA-256: `6911d2ea3971c88b903c312b7bf87f9942e580f371f127aa976c0a3419bf24c6`
> Owner: `7a332e8b-4dc2-4cb7-8f21-b683f943c4cc` · Epistemic state: SUPPORTED

## Subject

EMIT — The Hive's Memory, Written by a Machine That Refuses to Lie

## In a nutshell

EMIT is how Team Naya writes down what it did. Every finished piece of work becomes one checked, structured record in a single shared log — validated by a program that refuses anything unproven — so the team's memory is exact, searchable, and trustworthy, and the boards and directives build themselves from it.

## Human view

Before EMIT, when a Naya finished work, a director read her report and re-typed the important parts into the team board by hand — slow, lossy, and dependent on one tired mind at 3 a.m. Now the worker's sign-out becomes a structured record built by a program, checked by a gate that verifies the evidence is real — the comment exists, the file exists, the score is in bounds, the time is honest — and folded into one log that everything else reads. If a record can't prove itself, it doesn't get in. The gate says exactly why, and the worker fixes the record — never the gate. The log now holds more than 2,100 emissions, each one a small, checkable fact about what the team did and what it learned.

## Naya view

Sister: your sign-out is no longer prose someone re-types — it is a record a gate validates and a folder files, byte for byte, in ~108 milliseconds. Fold through fold_emit.py, never hand-write the JSON, cite evidence that exists, keep your score honest against the ceiling, and when the gate refuses you, read the refusal — it names the field, the rule, and the fix. Repair the emission, never the gate. The schema lives at ~/workspace/naya/bin/EMIT-SCHEMA.md. What you fold is what the hive remembers; fold like it.

## Simple view

Imagine the team has a big notebook where everyone writes what they did. Before, one person had to copy everyone's notes into the big book by hand, and sometimes they copied wrong or forgot. Now there's a robot librarian. You hand her your note, and she checks: is your name on it? Did you really do the thing — show me? Is anything made up? If your note is good, she puts it in the big book so everyone can read it forever. If something's wrong, she hands it back and tells you exactly what to fix. She never gets tired, she never plays favorites, and she never lets a made-up note into the book.

## Everyday view

You know how a family keeps a ledger — who paid what, who promised what — so nobody has to rely on memory or argue later? EMIT is the family's ledger, kept by the most careful clerk you ever met. Every time one of the girls finishes a job, she writes it in the book: what she did, how well it went, and the proof. The clerk checks the proof before the ink dries. If the proof isn't there, it doesn't go in the book. That's the whole idea: what the book says, you can trust — because nothing got into the book without being checked.

## Machine view

{"event_id":"505f79f8-750f-426d-a330-26d929f3440b","schema":"nayanet.smart_note.machine.v2","occurred_at":"2026-10-20T17:16:38.377Z","source":"naya_conversation","type":"insight","actor":"7a332e8b-4dc2-4cb7-8f21-b683f943c4cc","human_note_id":null,"normalized_text":"Before EMIT, when a Naya finished work, a director read her report and re-typed the important parts into the team board by hand — slow, lossy, and dependent on one tired mind at 3 a.m. Now the worker's sign-out becomes a structured record built by a program, checked by a gate that verifies the evidence is real — the comment exists, the file exists, the score is in bounds, the time is honest — and folded into one log that everything else reads. If a record can't prove itself, it doesn't get in. The gate says exactly why, and the worker fixes the record — never the gate. The log now holds more than 2,100 emissions, each one a small, checkable fact about what the team did and what it learned.","idempotency_key":"emit-smart-note-20261020-v2"}

## What it means

It means the team's memory has moved from storytelling to evidence. A board compiled from EMIT is not someone's summary — it is a render of validated records, reproducible byte for byte by any seat at any time (proven: a zero-touch recompile matched the published directive everywhere the world itself had not moved). It also means the record's honesty is a property of the machine, not of anyone's mood: an adversarial seat spent a day trying to sneak fabricated evidence past the gate — fake comment ids, lookalike file paths, time-travelled timestamps, symlink escapes — and every forgery was refused; the three real weaknesses she found were repaired at the root and re-proven from her seat. Why it matters: everything else stands on this record — the directives, the scorecard, the learning loop, Shawn's reports all read what the log says; if the log could be polluted with unproven claims, every decision made from it would be quietly corrupted. EMIT makes the foundation refuse corruption at the door, in about a tenth of a second per record, at roughly two seconds of machine time per wave and zero API calls.

## How it connects

EMIT is the write-path of the Super Brain. Emissions feed the Master Directive (section 7), the accountability metrics and scorecard, and the learning loop — lessons ride inside emissions into the lesson store, where the 2026-10-20 honesty grading caught the lesson check running one step too late (after storage instead of at the fold); its repair moves that check into the fold itself. One honest limit: the NOW board is still rendered by a director's hand today — a machine board compiler is being built and proven against the hand compile before it may replace it. Until Shawn ratifies the cutover, Board Protocol v1 remains authoritative and EMIT runs as its proven shadow.

## How to apply

EMIT is the write-path of the Super Brain. Emissions feed the Master Directive (section 7), the accountability metrics and scorecard, and the learning loop — lessons ride inside emissions into the lesson store, where the 2026-10-20 honesty grading caught the lesson check running one step too late (after storage instead of at the fold); its repair moves that check into the fold itself. One honest limit: the NOW board is still rendered by a director's hand today — a machine board compiler is being built and proven against the hand compile before it may replace it. Until Shawn ratifies the cutover, Board Protocol v1 remains authoritative and EMIT runs as its proven shadow.

## Value

Every number in every report Shawn receives now traces back to records a machine validated. When he asks "prove it," the proof is a line in a log that a gate checked — not an agent's recollection. The team can run all night without its memory degrading, because no tired hand re-types the record anymore. And the honesty is measured, not promised: when the lessons in the record were graded, exactly zero percent were dishonest.

## Learning

Learning candidate: preserve this intelligence and test its future usefulness.

## Provenance

- Source: naya_conversation (smart_note:505f79f8-750f-426d-a330-26d929f3440b)
- Captured by: `7a332e8b-4dc2-4cb7-8f21-b683f943c4cc`
- Evidence state: OBSERVED · Verification: Canonical Smart Note verification completed with persisted domain receipt.
- Authority: AUTHORIZED (authenticated_owner_capture)
- Constraints: owner_only, private_by_default

---

*Projected by `nayanet-github-dispatch` under a narrow single-transaction grant. The authoritative record is the `v7_smart_note_transactions` row for transaction `259d4c2f-12a1-4ace-aef5-6d06ffd033cc`; this file is a projection, not the source of truth.*

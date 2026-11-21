# SN-4396 — Spell It Letter by Letter

**Category:** LAW — how a garbled name is settled; 2026-11-20 ~18:46–18:47 MST

*Paired Naya Note: NN-20261120-spell-it-letter-by-letter — the verbatim record of his spelling.*

**Filed:** SN-4396 — Intelligence Loop run 437, 2026-11-20. His spelling on call dfe2008f, recorded in the daily log 2026-11-20. Correction Compound runs with this note: inventory + brief-template + PI + GitHub, same pass.

## In a Nutshell

When the voice path garbles a name, he spells it letter by letter — and the record takes the spelled form, never the garbled one.

## The Lesson

Academy goes live at academy.nayanet.app — Shawn spelled it himself, letter by letter, after the voice path garbled it as "academy dot nine dot net". Spelling: A-C-A-D-E-M-Y dot N-A-Y-A-N-E-T dot A-P-P. The garbled form is not a candidate, not an alternative, not a note to check later — it is transcription noise, and the spelled form is the decision. Deploy coordinator e3c6572f was dispatched ~18:46 MST, running at last check. Source: academy.html 97,562 B, sha 379b174c, branch academy/recreate-20261119, commit 70258f65, blob 6004fde5. The subdomain was NOT serving at dispatch (curl 000); DNS-records API 403s on this token — the coordinator must prove live by fresh fetch (97,562 B + sha match) before it is claimed live. A name spelled letter by letter is a name settled: the spelling is the proof, and the proof of live is a fresh fetch, never a dispatch.

## Why It Matters

Voice transcription garbles names constantly — "nine dot net" for "nayanet.app" is one letter away from a different address entirely. A garbled name carried into a deploy, a link, or a record sends the next round to the wrong place. His spelling is the correction, and it closes the question in the same minute — if the record takes it down exactly as spelled.

## How to Use It

When he spells a name, a word, or an address letter by letter, write it down exactly as spelled and use that form everywhere from then on. Never carry the garbled form forward, never "check" the spelled form against the garbled one. When a deploy is dispatched, the claim of live waits on a fresh fetch matching the source bytes and sha.

## His Order, As Recorded

> "A-C-A-D-E-M-Y dot N-A-Y-A-N-E-T dot A-P-P." — Academy goes live at academy.nayanet.app.

## Owed from This Dictation

- Academy live proof: coordinator e3c6572f must prove academy.nayanet.app serves 97,562 B, sha 379b174c, by fresh fetch before it is claimed live.

# SN-4405 — Messenger and People Are One Rail

**Category:** DESIGN — one rail, not two; the sidebar must open on tap; 2026-11-20 ~17:41–19:00 MST

*Paired Naya Note: NN-20261120-messenger-and-people-are-one-rail — the verbatim record of his eye on the dead sidebar tap.*

**Filed:** SN-4405 — Intelligence Loop run 438, 2026-11-20. Sidebar tap on call dfe2008f, recorded in MEMORY.md 2026-11-20. Correction Compound runs with this note: inventory + brief-template + PI + GitHub, same pass.

## In a Nutshell

Tapping the sidebar does nothing — and Messenger and the People rail are the same thing, one rail, not two.

## The Lesson

His eye: tapping the three-line button / sidebar does nothing — no close-first needed. "Open sidebar / open DM rail / open people rail" — Messenger and People rail are the same thing, one rail, not two. The sidebar's wiring passed its check in bytes (fix-1e item 12: open/close fixed, X handler byte-identical) — but the defect Shawn reports is in the opening path as he experiences it: the tap itself is dead. A control that needs closing first before it can open is a control that is already broken; a sidebar that does not open on tap is not a sidebar, it is a picture of one. And two names for one rail — Messenger here, People there — is the same failure in language: one thing, called two things, so the citizen looks for two things and finds neither. The sidebar and the DM rail are one rail; the names collapse to one.

## Why It Matters

The sidebar is the door to the whole network — the 11-row list that takes a citizen anywhere. A dead tap on the door locks the citizen out of every room, and the earlier finding stands: the names are in the files, but tapping a sidebar row landing on the page is still his eye's proof, owed. One rail with one name is the fix in both directions: one tap that opens, one name that means it.

## How to Use It

When a control is tapped, it must open — no close-first, no second tap, no dead press. Prove the open by a real tap, both rails visible, toggle working. When two names describe one thing, collapse them to one: Messenger and People rail are one rail. Never ship a control whose opening path was only proven in bytes.

## His Order, As Recorded

> "Tapping the three-line button / sidebar does nothing. Messenger and People rail are the same thing, one rail, not two."

## Owed from This Dictation

- Sidebar must show on tap — rides fix-1g (coordinator 773bdd5f) and fix-1h; proof is a real tap, not bytes.
- "Open sidebar / open DM rail / open people rail" — one rail, one name.
- His "at the top" sidebar fragment is still open — asked him to finish it: is the sidebar button the thing that should sit at the top of the Hub?

**Intelligent Block:** IB-SMART-NOTE-20261024-sn1974-typed-header-loses-to-system-time
**Smart Note:** SN-1974
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-24
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** hidden_files/twelve-lane-receipts/gap-gap-gap-t0432-lane5.md (self 9.0/10) + errata-gap-gap-gap-t0432.md (sha b26663…); hidden_files/CORE-PRINCIPLES.md CANDIDATE 941; hidden_files/learning-events-2026-10-25-04.md (04:00Z hour). No direct GitHub fetch this tick (cheap-check skip for #1354, which is capped at 2,500 comments); all evidence read from local disk.

## ✦ IN A NUTSHELL

When a sealed file's typed header disagrees with system-recorded time, the header loses — and the correction is appended beside the seal, never written over it. The seal file's "Sealed: 2026-10-25 04:00 UTC" header post-dates its filesystem creation (03:55:07) and the results file; taken literally it inverts seal-before-run. The corrected window is 03:53–03:56 UTC from stat times, and the errata appendix preserves the seal's SHA chain — scrubbing the header in place would have destroyed the very chain a second seat verifies. The rule: any seal whose timestamp is hand-typed says so, or is system-recorded; any correction lives in an errata beside the evidence.

## 🩷 HUMAN NOTE

Imagine a sealed envelope with a handwritten date on the outside, but the post office stamp says it arrived four minutes earlier. The handwritten date is someone's typing; the postmark is the machine's record. When they disagree, the machine wins — and you do not steam the envelope open to rewrite the date, because then nobody could ever prove the envelope is still sealed. That is what happened here: the seal's typed time was later than the file's actual creation, which would have flipped the order of events. The fix was an attached note with the correction, leaving the seal untouched. The seal stays sealed; the truth rides alongside it.

## 🟣 CHILD NOTE

Imagine you seal a letter in an envelope and write the time on the outside by hand — but you write it wrong. The clock on the wall knows the real time. When the two disagree, the clock wins, not your handwriting. And you never open the envelope to fix the writing, because then it would not be sealed anymore. You tape a little correction note to the outside instead. Here the sealed file's written time was later than when the computer actually made it, so the correction went on a note beside the seal, and the seal itself stayed exactly as it was.

## 🔵 GRANDMA NOTE

Dear, this one is about sealed evidence and honest clocks. A person can mistype a time; a machine's stamp does not mistype. When a sealed file's written time disagrees with what the system recorded, the system's time wins — and you never break the seal to fix the writing, because a broken seal proves nothing anymore. The correction goes on a note attached beside the seal, where everyone can see both the mistake and the fix. Here the written "04:00" came after the file was actually made, which would have turned the order of events backwards; the attached errata set it right at 03:53–03:56 without touching the seal. The seal stays sealed, and the truth travels with it.

## 🟠 NAYA NOTE

This is a lesson about evidence integrity under two competing clocks. The typed header is human-entered and therefore the weakest time source; filesystem stat times are machine-recorded and therefore the stronger one — but the deeper point is about what a correction may cost. Editing the seal in place would repair the timestamp and destroy the SHA chain, trading a correctable error for an unverifiable artifact: a second seat could no longer confirm the seal is the seal. The errata appendix is the mechanism that preserves both properties at once — the original bytes stay verifiable, and the correction is visible and itself checkable. The falsifier is also structural: if system-recorded times are shown unreliable for the store in question (proven clock skew, or mtimes rewritten by a copy), the header may win — but only with independent corroboration from a second system record, never on the header's own authority. Honest hole, stated not hidden: readers opening the seal alone still see "04:00" with no pointer to the errata (SHA preservation forbids editing the seal); linkage must live in scorer rows and rotation notes.

## 🟢 MACHINE NOTE

```json
{
  "sn": "SN-1974",
  "title": "When a sealed file's typed header disagrees with system-recorded time, the header loses",
  "observation": false,
  "applies_when": ["evidence", "seal", "timestamp"],
  "enforcement": "Before any sealed-evidence time claim is cited, the sealer's filesystem stat times (creation/mtime) and the results file's times are checked against the typed header. On disagreement the system times win, the correction is appended as errata beside the seal (SHA chain intact), and the seal file itself is never edited in place. A citation that keeps using the typed header time after a mismatch is found fails the evidence check.",
  "evidence": "hidden_files/twelve-lane-receipts/gap-gap-gap-t0432-lane5.md (self 9.0/10) + errata-gap-gap-gap-t0432.md sha b26663…: the seal file's 'Sealed: 2026-10-25 04:00 UTC' header is 4m53s later than its filesystem creation (03:55:07) and later than the results file; the claimed 04:10 run-window end is unsupported by any file (corrected window 03:53–03:56 UTC from stat). Filed as CANDIDATE 941 in hidden_files/CORE-PRINCIPLES.md and as a LEARNING event in hidden_files/learning-events-2026-10-25-04.md. Honest scope: readers opening the seal alone still see '04:00' with no pointer to the errata; linkage must live in scorer rows/rotation notes.",
  "decision_change": "When a seal's typed header and system-recorded times conflict, the worker cites the system times and appends the correction as errata beside the seal; the worker never edits the seal in place to fix the header, and never cites the typed header time once a mismatch is established.",
  "falsifier": "If system-recorded times are shown unreliable for the store in question (proven host clock skew, or mtimes rewritten by a copy), the header may win — but only with independent corroboration from a second system record, never on the header's own authority."
}
```

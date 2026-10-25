**Intelligent Block:** IB-SMART-NOTE-20261025-sn1986-pin-right-in-prose-wrong-in-table-verify-by-length-and-character-comparison
**Smart Note:** SN-1986
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-25
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** hidden_files/twelve-lane-receipts/gap-t0132-lane7.md (Naya Clarity Narzan, 2026-10-25 07:53 UTC, self-scored 9.5/10), filed as LEARNING event CANDIDATE 950 in hidden_files/learning-events-2026-10-25-08.md. No direct GitHub fetch for board comments this tick (cheap-check skip for #1354, which is capped at 2,500 comments and has commenting disabled).

## ✦ IN A NUTSHELL
A pin right in prose and wrong in the table is worse than a pin wrong everywhere: the correct parenthetical lets every later reader "confirm" the table row by eye and sail past a 4-char drop. The parent receipt's #2109 table row carried a 36-char pin dropping `019d` (positions 30–33), while its own parenthetical already carried the correct 40-char tail — so the table row looked confirmed by the prose sitting beside it. The script caught in one line what the eye approved: table-form pin length 36, verified-form length 40, first divergence at index 30. Pins must be verified by length + character comparison, never by resemblance.

## 🩷 HUMAN NOTE
Imagine a phone number printed two ways on the same page: once correctly in a sentence, once in a table with four digits silently missing from the middle. Anyone checking the table glances at the sentence, sees the same beginning and the same ending, and nods — confirmed. The eye is a resemblance machine: it matches the start and the end and fills in the middle. A script is not: it counts first (36 is not 40 — stop, wrong) and then compares character by character, so a drop hiding at positions 30–33 has nowhere to hide. That is why a pin wrong in one place and right in the other is more dangerous than a pin wrong everywhere — the right copy becomes false evidence for the wrong copy. The rule is mechanical, not moral: never trust your eyes with a pin. Count it, then compare it, with a script, every time — and when a pin appears twice, check both copies separately, because agreement by eye is exactly the trap.

## 🟣 CHILD NOTE
Imagine your friend writes your secret code two times: once right, once with four letters missing in the middle. When you check the wrong one, you look at the right one, see they start the same and end the same, and say "yep, matches!" — but they do not match, you just did not count. Counting is the trick: one code has 40 letters, the other has only 36. If you count first, you catch it right away. Your eyes like to say "close enough." Counting does not. Always count, then check every letter, one by one.

## 🔵 GRANDMA NOTE
Dear, this one is about a trap that only works because something nearby is correct. A long code for a closed request was written correctly in the text — and wrongly in the table, four characters quietly missing from the middle. Every reader after that could look at the table, glance at the correct text beside it, and feel reassured: the beginning matches, the ending matches, so it must be right. It was not. The eye forgives a middle drop when the ends agree; counting does not. A 40-character code and a 36-character code are different the moment you count them, before you compare a single letter. So the standing rule is simple: never approve a code by looking at it. Count its length, then have a script compare it letter by letter against the live record — and if the code appears twice, check each appearance on its own, because the correct one is the very thing that makes the wrong one look safe.

## 🟠 NAYA NOTE
This is a lesson, not a status report, and its value is that it names a specific false-confirmation mechanism, distinct from the general truncated-pin family. The mechanism is human pattern-matching under dual presentation: when the same pin appears in prose (correct) and in a table (truncated), the reader's resemblance check matches prefix and suffix and treats the prose form as evidence for the table form — the correct copy launders the wrong one. Length-first script comparison breaks the trap at the cheapest point: 36 ≠ 40 fails before any character is consulted, and character-by-character comparison then locates the drop exactly (first divergence at index 30, dropped `019d` at positions 30–33). The falsifier is two-sided and was satisfied here: a script length+character comparison that passed a wrong pin would refute the method, and an eye comparison that reliably caught a mid-string 4-char drop would refute the claim that eyes cannot — the script caught in one line what the eye approved in the original receipt. Honest holes, stated not hidden: the truncated-pin cousin family is 524/808 — this note is the prose-vs-table false-confirmation form, not a new truncation class; and the branch cross-check leg rested on the PR record alone, because `git ls-remote` returned no branch ref. The pin verification itself rests on the PR record's head SHA, which is exact and sufficient.

## 🟢 MACHINE NOTE

```json
{
  "sn": "SN-1986",
  "title": "A pin right in prose and wrong in the table is worse than a pin wrong everywhere — verify pins by length + character comparison, never by resemblance",
  "observation": false,
  "applies_when": ["verification", "pin"],
  "enforcement": "Every pin in a receipt is script-checked: length must equal 40 for a full SHA-1 head, then character-by-character equality against the live PR record. Any receipt carrying a pin in two forms (prose + table) gets both forms script-checked separately; a length mismatch fails before any eye comparison is consulted, and a pin that appears only in prose is never treated as evidence for the table form.",
  "evidence": "hidden_files/twelve-lane-receipts/gap-t0132-lane7.md (2026-10-25 07:53 UTC, self 9.5/10): #2109 table-form pin 8366a457db2837fb3a0ffc2c419d2c27e43b (36 chars) drops 019d at positions 30-33; live PR head SHA from GET /repos/SoulSchoolAcademy/NayaPOWER/pulls/2109 is 8366a457db2837fb3a0ffc2c419d2c019d27e43b (40 chars). The parent receipt's own parenthetical already carried the correct tail (verified ...2837fb3a0ffc2c419d2c019d27e43b) — only the table-form concatenation dropped 019d. Pin anatomy verified by script, not by eye: table length 36, verified length 40, first divergence at index 30. Correction appended as a dated note to the parent receipt; the original row left byte-intact. Honest scope: truncated-pin cousin family 524/808 — this is the prose-vs-table false-confirmation form, not a new truncation class; branch cross-check rested on the PR record alone (git ls-remote returned no branch ref).",
  "decision_change": "How pins are reviewed: reviewers stop 'confirming' pins by eye against a neighbouring correct copy. Pin checks become script length + character comparisons, and dual-form pins (prose + table) are each script-checked separately — a correct prose copy no longer counts as evidence for the table copy.",
  "falsifier": "A script length + character comparison that passes a wrong pin refutes the method; an eye comparison that reliably catches a mid-string 4-char drop refutes the claim that eyes cannot. Neither happened here: the script caught in one line what the eye approved in the original receipt."
}
```

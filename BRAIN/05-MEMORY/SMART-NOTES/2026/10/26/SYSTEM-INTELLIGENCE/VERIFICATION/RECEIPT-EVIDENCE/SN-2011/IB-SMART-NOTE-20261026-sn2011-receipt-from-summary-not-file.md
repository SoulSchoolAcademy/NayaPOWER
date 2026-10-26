Intelligent Block: SN-2011
Truth state: CANDIDATE
Scope: PRIVATE
Captured: 2026-10-26
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL
A delivered summary is never evidence. A verification receipt is composed only from output files read back in the same step — path, bytes, hash — never from a delivered background-completion summary. On 2026-10-26, the VERIFY 20:30Z receipt served wrong /pi verdicts because it was composed from a delivered summary carrying another slot's numbers, without reading the probe output file the command had written. The 20:34Z correction re-read the probe file (rounds 1–4) and restored the truth: live /pi + /pi/ serve 43,887 B sha d2bf0a09, byte-identical to the repo blob at tip f3c3862e, so /pi holds 9.5 — not the 4/10 the summary-based verdict claimed.

## 🩷 HUMAN NOTE
Someone handed you a report card for a test you never watched them run — and the grades on it belonged to a different student. That is what happened here: the verdict looked official, but its numbers came from a summary delivered by another slot, not from the probe output of this slot's own check. The fix is simple and non-negotiable: before you believe or repeat a verdict, open the output file yourself, in the same step, and read the numbers out of it. If the receipt cannot point at the file it read, it is not a receipt — it is a rumor with formatting.

## 🟣 CHILD NOTE
Imagine your friend tells you what score you got on a quiz, but they are reading from someone else's paper. You would get the wrong score! The grown-ups here did the same thing: they trusted a note someone handed them instead of looking at the real answer sheet. The rule now: always look at your own answer sheet before you say the score out loud.

## 🔵 GRANDMA NOTE
Dear, it is like this: a neighbor knocks and tells you what the doctor said, but they mixed you up with the lady next door. You would not take medicine on that word — you would call the doctor's office yourself and hear it direct. Same here. A verdict counts only when the person giving it read the actual test results themselves, right then and there. A passed-along note is never good enough.

## 🟠 NAYA NOTE
Cold successor, this is a provenance rule, not a style preference. Background-completion delivery is a lossy channel: it aggregates across slots, and a summary payload carries numbers with no binding to the step that produced them. The 20:30Z receipt is the proof: it served another slot's numbers as this slot's verdict, and only a same-step file readback caught it — within the same slot, four minutes later. Treat every delivered summary as an unverified claim, even when it arrives through the runtime's own delivery path. Your verdict cites the file, or your verdict does not ship.

## 🟢 MACHINE NOTE
{
  "applies_when": ["verification", "receipt", "receipt-evidence"],
  "enforcement": "VERIFY-lane receipt gate: a verdict receipt must cite the probe output file path plus the bytes/hash read back in the same step; a receipt citing only a delivered summary is rejected, and a served summary-based verdict is retracted in the same slot, as board #3066 comment 6426687603 retracted 6426656520.",
  "evidence": "Live board #3066 comment 6426687603 (2026-10-26T20:34:14Z, Naya Resolve - VERIFY): VERIFY 20:30Z serving verdicts RETRACTED; live /pi + /pi/ serve 43,887 B sha d2bf0a09 byte-identical to the repo blob at tip f3c3862e; /pi slot score 9.5, not 4/10. Superseded wrong verdict: comment 6426656520 (20:30Z). Mechanism stated in the correction: the 20:30Z receipt was composed from a delivered background-completion summary carrying another slot's numbers, without reading the probe output file the command had written.",
  "decision_change": "Whether to accept, repeat, or act on a verification verdict or receipt: accept only receipts that cite output files read back in the same step.",
  "falsifiability": "This rule would be wrong if a summary-composed verdict were shown, on same-step file readback, to match the probe file's numbers for the same slot and step — then the failure would not be the summary source but something else. The 20:30Z case fails that test: readback contradicted the summary verdict.",
  "mechanism": "Cross-slot summary carryover through a provenance-free delivery channel: a delivered summary carries numbers with no binding to the producing step's output file, so a wrong-slot payload passes silently as this slot's result.",
  "cousins": "SN-2007 (score a live face against its spec, not just its bytes — 2011 is the receipt-provenance half: the numbers must come from this step's file, not a delivered summary)"
}

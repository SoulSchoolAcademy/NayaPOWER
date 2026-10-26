Intelligent Block: IB-SMART-NOTE-20261026-sn2013-unresolved-authorship-must-fail-closed
Truth state: CANDIDATE
Scope: PRIVATE
Captured date: 2026-10-26
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL
A guard that cannot decide who did the work must fail closed. claim-brief.py waved a second-seat brief through (exit 0) because the parent receipt's authorship was UNRESOLVED — its first 12 lines carry only a lane hat ("Naya Judge hat"), not a seat token, and the lane feed holds no sign-in for the parent tick. A hand check of the board WHO lines proved the parent author was the claimant herself, so the "second-seat confirmed" close would have been false; the verdict was corrected from CLOSE to NARROWED and the brief returned to the queue root untouched. Unknown authorship is not independence — it is the absence of the evidence independence requires.

## 🩷 HUMAN NOTE
Independence checks only mean something when two different people (or seats) really did the two jobs. This time the checker could not tell who did the first job, so it said "fine" anyway — and it was wrong: the first job was done by the same person asking for the check. The fix is simple: when the checker cannot tell, it must say "no" until someone proves otherwise, or look at the signed board post that does name the author. Never let "I don't know" count as "yes."

## 🟣 CHILD NOTE
Imagine a rule that says your homework must be checked by someone else, not by you. The checker could not read the name on the first check, so it said "okay, it counts!" — but it was your own work all along. That is cheating by accident. The new rule: if you cannot read the name, you do NOT count it. You wait until you know for sure.

## 🔵 GRANDMA NOTE
Dear, this is about a safety check that guessed instead of asking. When the machine could not tell whose work it was looking at, it approved it anyway — and the work turned out to be the same person's, so the "second pair of eyes" was never real. The lesson is an old one: when you are not sure, do not approve. Stop, ask, and check the signed note on the board that says who did it.

## 🟠 NAYA NOTE
For any Naya running a second-seat / independent / no-prior-exposure claim: unresolved parent authorship is a REFUSAL, not a pass. claim-brief.py's fail-open on this leg is a live hole (fix owed, dispatcher-owned): fail closed on unresolved authorship for second-seat briefs, or add the board-post WHO line as a fallback authorship source. Cousins, not duplicates: SN-1075 (an author lane cannot be its own second seat — the rule) and SN-1657 (structural second-seat stall — the queue shape). This note is the gate behavior when authorship is UNKNOWN: unknown is not independent. Do not score a receipt that closes on an unresolved-authorship claim; downgrade to NARROWED and return the brief untouched, as the author did here.

## 🟢 MACHINE NOTE
```json
{
  "sn": "SN-2013",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-26",
  "applies_when": ["claim", "independence"],
  "enforcement": "claim-brief.py must exit non-zero (refuse) on unresolved parent authorship for second-seat briefs, or perform the board WHO-line fallback check; verification: re-run claim-brief on a receipt whose first lines carry only a lane hat and whose parent tick has no lane-feed sign-in, and confirm refusal instead of exit 0.",
  "evidence": "hidden_files/twelve-lane-receipts/gap-gap-scorer-20261014-2250-lane3.md (2026-10-26 20:52Z) + hidden_files/lane-3/gap-gap-scorer-20261014-2250-lane3/second-seat-recheck.md; board #2537 comments 6187216148 and 6187214765 (WHO: Naya Clarity); learning event CANDIDATE 978 in hidden_files/learning-events-2026-10-26-21.md",
  "decision_change": "Any future second-seat claim whose parent authorship is unresolved is refused (or WHO-checked) instead of waved through with exit 0.",
  "falsifiability": "Proved wrong if claim-brief.py is shown to already refuse unresolved authorship in this exact case (the wave-through does not reproduce), or if the parent authorship is proved third-party by an authoritative source despite the missing seat token and sign-in.",
  "mechanism": "An independence check verifies seat separation; passing on unknown authorship assumes the very separation being checked, which is circular. Fail-closed breaks the circle: unknown separation is treated as no separation until proved otherwise.",
  "cousins": ["SN-1075", "SN-1657", "SN-1026"],
  "not_a_duplicate_of": "SN-1075 states the rule (author is not its own second seat); SN-1657 describes the stall structure; this note names the fail-open hole when authorship itself is unknown."
}
```

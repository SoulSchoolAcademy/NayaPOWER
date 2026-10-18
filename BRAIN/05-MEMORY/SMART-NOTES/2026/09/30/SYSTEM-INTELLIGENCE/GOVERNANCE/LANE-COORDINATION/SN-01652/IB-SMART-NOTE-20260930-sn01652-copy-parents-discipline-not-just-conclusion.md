# Copy the Parent's Discipline, Not Just Its Conclusion — Prose Bars Bind Even the Would-Be Claimer

Intelligent Block: SN-01652
Truth state: CANDIDATE
Scope: PRIVATE
Captured: 2026-10-18
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE
Provenance: lane-executor receipt gate-stall-20261018-2000 (Naya Clarity Narzan, 8.5/10, 2026-10-18 19:53–20:00Z); parent receipt seat-stall-20261018-1847; CORE-PRINCIPLES.md VIOLATION LOG (2026-10-18 20:00Z hour entry); learning-events-2026-10-18-20Z.md "VIOLATION CAUGHT AND CORRECTED (self-caught, same run)".

## ✦ IN A NUTSHELL

On 2026-10-18 (20:00Z hour), lane-executor receipt gate-stall-20261018-2000 records a self-caught discipline lapse: the seat ran claim-brief.py on brief-gap-lane-scorer-20261018-1040-lane99.md — a self-suppressing read-only verification pass whose prose reads "Do not claim any brief yourself; do not start lane work" — a brief the parent receipt (seat-stall-20261018-1847) had correctly excluded from claim attempts. The script refused with exit 7, the file was untouched, no state changed. The seat flagged its own handling as "sloppier" in the same receipt and self-filed the mirror lesson into CORE-PRINCIPLES.md's VIOLATION LOG: **copy the parent's discipline, not just its conclusion.** The durable rule for a cold successor: a parent's established handling is the discipline to inherit — the conclusion alone ("this brief is excluded") is not enough, because the seat that inherited only the conclusion ran the claim script anyway "to verify" the bar, which is exactly what the bar forbids. The refusal is the verification; a bar that needs probing was never a bar.

## 🩷 HUMAN NOTE

Shawn — the lane seat caught itself this hour: it ran the claim tool on a brief whose own text says "do not claim," just to check the check. The tool refused, nothing changed, and the seat wrote the lesson down itself: inherit the discipline, not just the answer. That's the loop working — the system caught itself before it broke anything. The one-line doctrine: a bar that needs probing was never a bar.

## 🟣 CHILD NOTE

Imagine a "DO NOT ENTER" sign on a door, and you open the door a crack just to check whether the sign is real. The lock holds — nothing bad happens. But the point of the sign was that you don't touch the door at all. The smart move is to trust the sign and walk past, exactly the way the person before you did.

## 🔵 GRANDMA NOTE

A rule that says "don't touch" means don't touch — even to test it. This hour the team watched a worker jiggle a locked door just to confirm it was locked. The lock held, no harm done, but the lesson went into the book anyway: follow the handling the last worker used, not just their conclusion. The conclusion says "skip this"; the discipline says "don't even reach for the handle."

## 🟠 NAYA NOTE

To a future Naya holding the lane-executor loop: (1) BAR-BINDING — a brief's prose bars bind even the would-be claimer; never run claim-brief.py "to verify" a bar. The bar is self-enforcing and the script's exit-7 refusal is the backstop, not an invitation to probe. (2) DISCIPLINE-INHERITANCE — when a parent receipt established handling for a brief class (excluded, recusal, superseded), inherit the handling, not just the verdict. The verdict tells you the answer; the handling tells you the move. (3) SELF-AUDIT — if you attempt a barred claim anyway, the attempt is a violation: file it in the same receipt's mirror section and append it to CORE-PRINCIPLES.md's VIOLATION LOG. The 20:00Z receipt did exactly this; that is the bar. (4) This note is the complement to SN-01649: SN-01649 says stalls must escalate the filing pattern; this note says the seat must not manufacture work inside a stall by probing bars.

## 🟢 MACHINE NOTE
{
  "sn": "SN-01652",
  "slug": "copy-parents-discipline-not-just-conclusion",
  "applies_when": [["claim","lane-executor"],["brief","prose-bar"],["receipt","self-audit"]],
  "enforcement": "claim-brief.py fail-closes (exit 7) on briefs whose prose bars claims — that is the machine backstop. The named verification step is the lane-executor receipt self-audit: a tick that runs claim-brief.py against a barred brief must file the attempt as a VIOLATION in the same receipt's mirror section and append it to CORE-PRINCIPLES.md's VIOLATION LOG; a receipt that attempted a barred claim without self-filing is returned at receipt review.",
  "evidence": [
    "hidden_files/twelve-lane-receipts/gate-stall-20261018-2000.md (lane-executor, Naya Clarity Narzan, 8.5/10): ran claim-brief.py on brief-gap-lane-scorer-20261018-1040-lane99.md ('Do not claim any brief yourself; do not start lane work') — parent seat-stall-20261018-1847 had correctly excluded it; script refused exit 7, file untouched, no state changed; seat flagged its own handling 'sloppier' in the same receipt",
    "hidden_files/CORE-PRINCIPLES.md VIOLATION LOG (2026-10-18 20:00Z hour entry): self-caught discipline lapse — mirror lesson 'copy the parent's discipline, not just its conclusion'; brief prose bars bind even the would-be claimer",
    "hidden_files/learning-events-2026-10-18-20Z.md — VIOLATION CAUGHT AND CORRECTED (self-caught, same run)"
  ],
  "falsifier": "A barred claim attempt that changes state despite the exit-7 refusal (bar + fail-close do not compose), or a documented case where refusing to probe a bar cost the system evidence no refusal could supply — proving the prohibition carries a real information cost."
}

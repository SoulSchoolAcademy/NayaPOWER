# IB-SMART-NOTE-20260930-sn01720-preserve-out-at-classification

Intelligent Block: SN-01720
Truth state: CANDIDATE
Scope: PRIVATE
Captured: 2026-10-20
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL
A verdict that can't be re-derived from on-disk evidence is a claim, not a proof. Preserve the `.out` evidence at classification time — never rely on a receipt table's quoted line alone.

## 🩷 HUMAN NOTE
The gap-t0983 follow-up closed a hole the parent receipt had left open: an exit-7 parent-authorship verdict for a 29-row lane-scorer dry run had no preserved dry-run `.out` — the verdict rested on a receipt table's quoted line. The seat re-ran the dry run byte-for-byte (the REFUSED line matched modulo elision), preserved the `.out` and a 29-row `exits.txt` kit at classification time, and the verdict became re-derivable by any independent seat. The general discipline: a quoted line in a receipt is a pointer to evidence, not evidence. Prose quotes decay — elision, retyping, memory. Only preserved bytes re-derive. At the moment you classify a verdict, save the bytes that classified it.

## 🟣 CHILD NOTE
Imagine you tell your teacher "I counted 29 birds and 19 of them were blue." The teacher asks: "Can I see your count sheet?" If all you have is the sentence you wrote down later, that's just your word — maybe you miscounted, maybe you misremembered. But if you saved the actual tally sheet with all 29 marks at the moment you counted, anyone can check it. The sentence is the claim; the tally sheet is the proof. Always save the tally sheet when you count — not the story about the counting.

## 🔵 GRANDMA NOTE
There is a difference between remembering what happened and proving what happened, and the difference is paper. A verdict written down from memory is a memory wearing a verdict's clothes. The wise move is older than computers: at the moment you decide, you write down — no, you keep — the very thing you looked at when you decided. Not a summary, not a quote of it, the thing itself. Months later, when a stranger asks how you knew, you don't tell them the story of the knowing. You hand them the paper.

## 🟠 NAYA NOTE
This is the preservation companion to SN-1716 ("verdicts written after coverage") and the classification-time companion to SN-1688 ("preserve the comparison artifact"). SN-1716 covers ordering — hold the verdict until coverage is proven. SN-1688 covers comparison proofs — keep both variants, the diff, and the re-derivation instructions. This note covers the classification moment itself: when you classify a verdict, preserve the `.out` bytes at that moment; a verdict row whose only evidence is a quoted receipt line is a claim, not a proof. The mechanism is decay: prose quotes are lossy (elision, retyping, memory), so re-derivation from a quote is reconstruction, not replication. The enforcement is the receipt-filing check in the same gate form as the SN parse BOUNCE law: a verdict row without a preserved `.out` path is bounced. The note's own falsifier is mechanical: a preserved `.out` that fails to re-derive the verdict on a cold rerun — then the preservation mechanism failed, not the verdict. Cousins: SN-1716 (verdicts after coverage — the ordering half of the same verdict discipline); SN-01711 (an absence claim cites its query — the citation half); SN-1688 (preserve the comparison artifact — the comparison-proof half); the t0992 bool-probe finding (the probe suite IS the preserved evidence class for loaders).

## 🟢 MACHINE NOTE
```json
{
  "sn": "SN-01720",
  "lesson": "A verdict that cannot be re-derived from on-disk evidence is a claim, not a proof. Preserve the .out evidence at classification time — never rely on a receipt table's quoted line alone.",
  "applies_when": ["verification", "evidence", "receipt", "verdict"],
  "enforcement": "lane-receipt filing check: a verdict row without a preserved .out path is bounced (same gate form as the SN parse BOUNCE law). The .out is saved at classification time, not reconstructed later.",
  "decision_changed": "when classifying a verdict (e.g. an exit-7 parent-authorship refusal): preserve the dry-run .out bytes at that moment instead of quoting the receipt table later; the verdict's evidence is the bytes, not the quote",
  "falsifier": "a preserved .out that fails to re-derive the verdict on a cold rerun — the preservation mechanism failed, not the verdict; documented case reframes the note's enforcement",
  "mechanism": "prose quotes decay: elision, retyping, and memory make re-derivation from a quote a reconstruction rather than a replication. Only preserved bytes re-derive. A receipt table's quoted line is a pointer to evidence, not evidence.",
  "evidence": "hidden_files/twelve-lane-receipts/gap-t0983-lane10.md (2026-10-20 07:10Z, 9.5/10): row 1's exit-7 parent-authorship verdict had no preserved dry-run .out; re-ran byte-for-byte (REFUSED line matched modulo elision), preserved at hidden_files/lane-10/check-run-t0983-lane10/brief-gap-lane-scorer-20261019-1230-lane3.md.out with a 29-row exits.txt kit",
  "companions": "SN-1716 (verdicts written after coverage — the ordering half of the same verdict discipline); SN-01711 (an absence claim cites its query — the citation half); SN-1688 (preserve the comparison artifact — the comparison-proof half); CORE-PRINCIPLES.md CANDIDATE (filed 2026-10-20 07:20Z learning review, same gap-t0983 evidence)"
}
```

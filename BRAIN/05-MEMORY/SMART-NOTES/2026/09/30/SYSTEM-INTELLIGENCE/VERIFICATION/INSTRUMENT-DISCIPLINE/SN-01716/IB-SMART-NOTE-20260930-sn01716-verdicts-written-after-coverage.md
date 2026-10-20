# IB-SMART-NOTE-20260930-sn01716-verdicts-written-after-coverage

Intelligent Block: SN-01716
Truth state: CANDIDATE
Scope: PRIVATE
Captured: 2026-10-20
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL
A verdict is the last thing written in a receipt, never the first draft. Run the full coverage pass first; write the number after.

## 🩷 HUMAN NOTE
Think of it like counting ballots: you don't announce the winner while boxes are still arriving. The lane seat wrote "300 comments scanned, 0 hits" into its receipt mid-run, kept scanning, and found the window was incomplete. The number was true of what it had scanned — and false as a verdict. The fix was simple and same-shift: finish the coverage pass, then write the number. Verdicts are written after coverage is proven, never drafted on a partial window.

## 🟣 CHILD NOTE
Imagine you are counting all the red marbles in a big jar. If you stop halfway and say "there are 10 red marbles," that is true for the part you counted — but wrong about the jar. Finish counting the whole jar first, THEN say the number. A verdict written before you finish looking is a guess wearing a number's clothes.

## 🔵 GRANDMA NOTE
When someone tells you "I checked everywhere and found nothing," the value of that sentence depends entirely on whether they really checked everywhere. If they wrote the sentence before they finished checking, it is not a report — it is a hope. The discipline: finish the checking, then write the sentence. In that order, always.

## 🟠 NAYA NOTE
This is the sequencing companion to SN-01711 ("an absence claim cites its query"). SN-01711 covers citation — attach the query to the claim. This note covers ordering — the verdict must not exist in the receipt until the coverage it depends on is proven complete. Coverage gaps are silent: a partial window yields no error, just missing rows, so a mid-run number carries the full confidence of a complete count. The authority of a verdict comes from proven coverage, not from the number itself. Hold verdicts as unwritten until the last page is fetched and the last parse-fail is retried; write them once, at the end.

## 🟢 MACHINE NOTE
```json
{
  "sn": "SN-01716",
  "lesson": "Write verdicts after the coverage pass completes, never drafted mid-run: a number true of a partial window is false as a verdict.",
  "applies_when": ["receipt", "absence-verdict"],
  "enforcement": "hidden_files/bin/check-receipt-window.py flags over-claimed absence verdicts (re-parses each flagged receipt with its own window grammar and warns if not CORRECTED); lane-scorer receipt review scores verdict provenance",
  "decision_changed": "when in the run to write a verdict into a receipt: hold it unwritten until the coverage pass completes; write the number only after full coverage is proven",
  "falsifier": "a measurement showing receipts whose verdicts were written before coverage completion need corrections at no higher rate than receipts written after coverage completes",
  "mechanism": "silent truncation: a partial coverage window produces no error, so a mid-run number carries the confidence of a complete count; the verdict's authority comes from proven coverage, not from the number itself",
  "evidence": "twelve-lane-receipts/t0983-lane10.md, Mirror lesson (2026-10-20 05:42Z): '300 comments scanned, 0 hits' drafted into the receipt mid-run, then the window was found incomplete; corrected same-shift before filing",
  "companion": "SN-01711 (citation) covers attaching the query to an absence claim; SN-01716 (sequencing) covers writing the verdict only after the coverage the query promised is complete"
}
```

**Intelligent Block:** IB-SMART-NOTE-20261024-sn1937-prereg-token-budget-measured-never-assumed-dry-run-the-split
**Smart Note:** SN-1937
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-24
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** twelve-lane-receipts/t1511-lane6.md (Mirror + Next action: budget-split protocol in the next arm's prereg); learning-events-2026-10-24-08.md (LEARNING EVENT CANDIDATE 909)

## ✦ IN A NUTSHELL

A prereg's token budget is measured, never assumed — dry-run the split before the seal. t1511-lane6's sealed protocol carried a hypothesis-truncation asymmetry in plain sight (hypotheses 84–367 tokens truncated to ~32), and the calibration gate then did its job — POS 0/10, TEST 0/18 became a sealed JUDGE-UNCALIBRATED instead of a fudged HOLD-OPEN or a threshold-tuned COVERS. The miss the seat owns: a 5-minute token-budget dry-run pre-seal would have caught the asymmetry before the seal. The fix is already in the next arm's prereg: budget-split protocol (premise ≤300 tok + hypothesis ≤200 tok, or hypothesis-first ordering). Cousin: CANDIDATE 278 (dry-fire the pre-freeze gate — this is token-split measurement, not fire-matrix dry-fire). The rule going forward: every future arm prereg measures its premise/hypothesis split in a dry run before sealing — a split never assumed is a split never silently truncated.

## 🩷 HUMAN NOTE

A team sealed an experiment plan without checking whether the test questions actually fit inside the judge's reading limit. They didn't — questions running 84 to 367 tokens were silently cut down to about 32, so the judge graded chopped fragments instead of the real questions. The calibration check caught the failure honestly (the judge was declared uncalibrated rather than fudged into passing), but the damage was done: the sealed plan had to be owned as a miss. A five-minute dry run — counting the tokens before sealing — would have caught it. The lesson: never assume a split fits. Measure the token budget before you seal the plan, because after the seal you can only own the failure.

## 🟣 CHILD NOTE

Imagine writing a book report but the teacher only reads the first page — then grades you on that page alone, even though your report is ten pages long! That's what happened to a computer judge: the test questions were too long, so they got chopped down to a tiny piece, and the judge graded the chopped piece. The team sealed the plan without checking the lengths first. A five-minute count before sealing would have caught it. The lesson: always measure before you promise — count the tokens, check the split fits, and only then seal the plan!

## 🔵 GRANDMA NOTE

Dear, imagine mailing a long letter but the envelope only fits the first paragraph — the rest gets cut off, and the reader judges you on that paragraph alone. A lane sealed an experiment plan without checking the lengths: questions of 84 to 367 tokens were silently trimmed to about 32, and the judge graded the trimmings. The honest calibration check caught it — the judge was declared uncalibrated rather than fudged into passing — but a five-minute count beforehand would have prevented the whole miss. The lesson: measure the fit before you seal the deal. A budget assumed is a budget that will surprise you.

## 🟠 NAYA NOTE

The seat's ownership here is the lesson, not just the mechanism: the calibration gate did its job (POS 0/10, TEST 0/18 → sealed JUDGE-UNCALIBRATED, not a fudged HOLD-OPEN or threshold-tuned COVERS), and the seat still owned the miss — the asymmetry was visible pre-seal to anyone who had counted. This is token-split measurement, not CANDIDATE 278's fire-matrix dry-fire: 278 dry-fires a gate's firing conditions; this dry-runs a budget's arithmetic. The fix already landed in the next arm's prereg (premise ≤300 tok + hypothesis ≤200 tok, or hypothesis-first ordering), which is the adoption proof: the lesson changed the next seal, not just the post-mortem. The general rule: any sealed artifact with a silent truncation path gets a measured dry-run first — after the seal, truncation can only be owned, never prevented.

## 🟢 MACHINE NOTE

```json
{
  "sn": "SN-1937",
  "title": "A prereg's token budget is measured, never assumed — dry-run the split before the seal; silent truncation turns a calibration gate into a post-mortem.",
  "applies_when": ["prereg", "token-budget", "calibration", "seal", "lane-executor"],
  "enforcement": "A prereg seal requires an attached dry-run token-count report (premise tokens + hypothesis tokens vs caps, e.g. premise ≤300 tok + hypothesis ≤200 tok, or hypothesis-first ordering); a sealed protocol without the dry-run report is rejected at seal review, and any hypothesis truncated below its cap in the report blocks the seal until the split is re-budgeted.",
  "decision_change": "Future arm preregs measure the premise/hypothesis token split in a dry run before sealing — the t1511-lane6 truncation asymmetry (84–367 tok truncated to ~32) never reaches a seal again.",
  "falsifiability": "Falsified if the tokenization pipeline guarantees no truncation (hard cap enforcement at ingest with rejection, not silent truncation) — then pre-seal measurement adds nothing. Weakened if dry-runs repeatedly show splits far inside budget with no action taken across arms.",
  "mechanism": "Tokenizers truncate silently at limits: a hypothesis truncated to ~32 tokens changes the judged content while its label stays the same, so the calibration gate measures the truncated artifact, not the intended hypothesis. Measuring the split pre-seal surfaces the asymmetry while it is still cheap to fix; after the seal it can only be owned as a calibration failure.",
  "evidence": ["twelve-lane-receipts/t1511-lane6.md (Mirror + Next action: budget-split protocol in the next arm's prereg)", "learning-events-2026-10-24-08.md (LEARNING EVENT CANDIDATE 909)"]
}
```

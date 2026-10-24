**Intelligent Block:** IB-SMART-NOTE-20261024-sn1933-keyword-calibration-no-signal-ships-uncalibrated
**Smart Note:** SN-1933
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-24
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** twelve-lane-receipts/t1509-lane11.md (lines 11, 43, 73: 8-receipt calibration, two keyword misses corrected, audit `method` field); lane-11/metric_audit_t1509.json (99 rows, M2=99/M3=32/M4=14); learning-events-2026-10-24-07.md (LEARNING EVENT CANDIDATE 905)

## ✦ IN A NUTSHELL

A keyword is a rumor about a judgment — no signal ships uncalibrated. t1509-lane11's M3 keyword rules missed t1502-lane2 and t1497-lane1 entirely: seat-block and recusal falsifications carry no `falsif*` token ("would be a false independence claim", "the domino is dead"). The 8-receipt calibration caught both. The fix: seed the keyword set with the adversarial patterns (`false * claim`, `recus*`, `premise-rotted`) from the start, and record the seeding + the misses + the residual error in the audit's `method` field — not just in the receipt. Principle: instruments are calibrated against adversarial patterns before their signal ships — a keyword scan is prose about a judgment, not a measurement of it. Cousins: CANDIDATE 558 (fold report first, keyword scans second), CANDIDATE 721 (anchors don't catch keyword-free events), CANDIDATE 800 (a proxy's noise is itself the finding).

## 🩷 HUMAN NOTE

Someone built a tool that reads work summaries and flags the ones where the author caught and corrected their own mistake. The tool searched for words like "falsified." But two real cases slipped through — the authors had written "would be a false independence claim" and "the domino is dead," phrases with none of the tool's search words. A human reading eight reports deeply caught both, and the tool's word list was fixed to include those patterns first. The lesson: a search tool only finds the words you taught it; before you trust its verdicts, teach it the tricky phrasings first and prove it catches them. A keyword search is a description of judgment, not a measurement of it.

## 🟣 CHILD NOTE

Imagine a machine that finds the sentences where kids admit they were wrong and fixed it. It searches for the word "wrong." But two kids wrote "that can't be true, let me check" and "I take it back" — the machine missed both because it only knew the word "wrong." A person reading a few papers by hand caught both, and the machine's word list was updated with the tricky phrases. The lesson: a word-search is only as smart as the words you give it. Always teach it the sneaky phrases first, and test that it finds them, before trusting what it says!

## 🔵 GRANDMA NOTE

Dear, think of a spell-checker that only knows simple words — it will miss clever spellings. A lane built an instrument that scans work reports for signs the worker caught their own errors. It searched for one word — and missed two real cases, because the workers had written things like "the domino is dead" instead. A careful human reading caught both, and the instrument's word list was fixed with those phrases before anything else. The lesson: any instrument that scans words must first be trained on the sneaky ways people actually phrase things — and tested against them — before its verdicts mean anything. Prose about judgment is not measurement.

## 🟠 NAYA NOTE

This extends the keyword-skepticism family (CANDIDATE 558/721/800) into an instrument-building rule: the calibration is part of the instrument, not a prelude to it. t1509-lane11's t1402-method measurement was tractable only because of the signal-extraction script + 8-receipt deep-read calibration, and the calibration corrected two keyword misses that would have silently undercounted M3. Two discipline points carry forward: (1) adversarial seeding — keyword sets are seeded with the phrasings judgments actually take (seat-block: "would be a false independence claim"; recusal: "the domino is dead"), the `false * claim` / `recus*` / `premise-rotted` patterns went in from the start after the fix; (2) the method field carries the calibration — the audit's `method` field names the protocol, the misses corrected, and the residual error, so a cold reader knows exactly what the scan can and cannot see. The instrument ran twice with byte-identical output (a1f1b6e0f45bcffe4c109cdeb6782b30749471bf822c7fdff37261e324942c79), machine counts reproducing hand counts exactly — reproducibility of an uncalibrated instrument is worth nothing.

## 🟢 MACHINE NOTE

```json
{
  "sn": "SN-1933",
  "title": "A keyword is a rumor about a judgment — no signal ships uncalibrated: seed keyword sets with adversarial patterns and record the calibration in the audit's method field.",
  "applies_when": ["audit", "calibration", "keyword-scan", "lane-executor", "instrument"],
  "enforcement": "The audit's `method` field must name the adversarial seed patterns and the calibration receipts (deep-read count, misses corrected, residual error) before any scan verdict ships; a verdict whose method field lacks the seed list is rejected as uncalibrated. Keyword sets are reviewed for adversarial-phrase coverage (seat-block, recusal, premise-rot phrasings) the same way counts are reviewed — an unseeded scan's verdicts are treated as unverified.",
  "decision_change": "Future audits seed their keyword sets with the adversarial patterns first and calibrate before shipping verdicts — keyword-free falsifications (seat-block, recusal) stop being silent misses.",
  "falsifiability": "Falsified if a keyword set shipped without adversarial seeding and without calibration still catches keyword-free falsification patterns across independent re-audits — i.e., if the calibration repeatedly adds zero catches, the rule is cost without signal.",
  "mechanism": "Falsifications are expressed in prose phrasing with no canonical token ('would be a false independence claim', 'the domino is dead'); a keyword scan only matches tokens it was given. Seeding the set with adversarial phrasing patterns closes the gap between what the scan matches and what the judgment says — calibration turns prose about judgment into a measurement.",
  "evidence": ["twelve-lane-receipts/t1509-lane11.md (line 73 principle; line 11 calibration method; line 43 pass-2 score)", "lane-11/metric_audit_t1509.json (99 rows, M2=99/M3=32/M4=14, byte-identical twin runs)", "learning-events-2026-10-24-07.md (LEARNING EVENT CANDIDATE 905)"]
}
```

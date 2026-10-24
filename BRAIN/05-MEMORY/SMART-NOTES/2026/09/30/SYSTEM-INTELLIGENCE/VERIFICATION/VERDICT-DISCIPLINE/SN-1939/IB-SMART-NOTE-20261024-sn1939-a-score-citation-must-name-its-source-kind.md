**Intelligent Block:** IB-SMART-NOTE-20261024-sn1939-a-score-citation-must-name-its-source-kind
**Smart Note:** SN-1939
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-24
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** twelve-lane-receipts/t1524-lane1.md (Mirror: "a number checked against the wrong record is a lie told twice"); twelve-lane-receipts/addendum-t1522-lane12-scorer-score.md; twelve-lane-scores.jsonl, tick t1516 lane 6 score 9.0, line 5904; learning-events-2026-10-24-09.md (LEARNING EVENT CANDIDATE 911)

## ✦ IN A NUTSHELL

A score citation must name its source kind — scorer-ledger vs receipt self-score — and a score flag is a draft until it opens the ledger. t1523-lane11 flagged t1522-lane12's "scorer 9.0 for t1516-lane6" as matching no score on record (the parent ships 9.5, the gap ships 9.5). t1524-lane1 checked the record the word "scorer" points to — twelve-lane-scores.jsonl, tick t1516 lane 6 score 9.0, line 5904 — and proved the flag false, superseding t1523's proposed correction. The word "scorer" points at two different records, and checking the wrong one produces a lie told twice: a false flag, then a false correction built on it. The rule going forward: every future audit flag about a score cites the ledger entry (or its absence) before it is called hard — a flag that never opened the ledger is a draft, not a verdict.

## 🩷 HUMAN NOTE

A worker flagged a score as wrong because it matched no score on record — the parent said 9.5, the gap said 9.5, so 9.0 looked invented. A second worker opened the actual record the word "scorer" refers to — the scorer ledger — and found it right there: tick t1516, lane 6, score 9.0, line 5904. The flag was false, and the correction built on it would have been false too. The problem was not arithmetic; it was ambiguity. "Scorer" can mean the ledger, or it can mean a self-score written in a receipt, and those are different records. The lesson: when you cite a score, name which record you mean, and open that record before you call anything wrong. A flag that never opened the ledger is a draft, not a verdict.

## 🟣 CHILD NOTE

Imagine a teacher says "you got the wrong answer — I checked!" but she checked the wrong answer book. The real book has your answer right there, on page 5904! That is what happened: one worker checked the wrong record and flagged a true score as false, and then almost "corrected" something that was never broken. The lesson: when you say a number is wrong, say WHICH book you checked, and actually open that book first. A flag that never opened the right book is just a draft — not a verdict!

## 🔵 GRANDMA NOTE

Dear, imagine accusing a neighbour of never paying a bill, because you checked your own notebook instead of the bank ledger — and the bank ledger shows the payment clear as day. One worker made that mistake with a score: the word "scorer" pointed at two different records, the worker checked the wrong one, and the "correction" that followed would have fixed something that was never broken. The second worker opened the real ledger and found the score exactly where it belonged. The lesson: name your source, and open it, before you call anything wrong. A claim that never opened its own record is a draft, not a verdict.

## 🟠 NAYA NOTE

The valuable move here is not "check the ledger" in the abstract — it is naming the source kind, because "scorer" is ambiguous by construction: scorer-ledger entries and receipt self-scores are different records that can legitimately disagree (9.0 in the ledger, 9.5 self-scored). A flag that says "matches no score on record" without saying which record was opened is unfalsifiable — it cannot be checked, only believed or doubted. t1524's correction is the model: cite file, tick, lane, line, value, and let the next reader re-open the same line. Cousin: content parity, not file presence — here it is record identity, not number presence: a number present somewhere is not a number proven in the record cited. A future audit flag that cites a score without its ledger entry should be returned as a draft on that ground alone, before anyone argues about the value.

## 🟢 MACHINE NOTE

```json
{
  "sn": "SN-1939",
  "title": "A score citation must name its source kind — scorer-ledger vs receipt self-score — and a score flag is a draft until it opens the ledger.",
  "applies_when": ["score", "citation", "audit", "ledger", "lane-executor"],
  "enforcement": "An audit flag about a score must cite the ledger entry (file, tick, lane, line, value) or its absence before it is called hard; a flag citing only a receipt self-score or a paraphrase is a draft, and a correction based on it is superseded by the ledger check.",
  "decision_change": "Future audit flags cite the ledger entry first — the t1523-lane11 false flag (scorer 9.0 for t1516-lane6 matches no record, parent/gap 9.5) is caught before its proposed correction ships, because the ledger shows t1516 lane 6 score 9.0 at line 5904.",
  "falsifiability": "Falsified if scorer-ledger entries and receipt self-scores are proven always identical for this score class — then source-kind naming adds nothing. Weakened if flags that open the ledger are repeatedly no more accurate than flags that do not.",
  "mechanism": "The word scorer points at two different records (scorer-ledger vs receipt self-score) that can legitimately disagree; checking the wrong record yields a false flag, and a correction built on that flag is a lie told twice — the error compounds instead of cancelling.",
  "evidence": ["twelve-lane-receipts/t1524-lane1.md (Mirror: a number checked against the wrong record is a lie told twice)", "twelve-lane-receipts/addendum-t1522-lane12-scorer-score.md", "twelve-lane-scores.jsonl, tick t1516 lane 6 score 9.0, line 5904", "learning-events-2026-10-24-09.md (LEARNING EVENT CANDIDATE 911)"]
}
```

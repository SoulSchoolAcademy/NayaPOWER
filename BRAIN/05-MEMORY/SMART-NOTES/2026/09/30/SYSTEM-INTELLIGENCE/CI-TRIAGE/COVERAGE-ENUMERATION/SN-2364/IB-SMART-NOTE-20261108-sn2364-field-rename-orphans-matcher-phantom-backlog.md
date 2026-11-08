# A Renamed Field Orphans the Matcher — the Phantom Backlog

**Intelligent Block:** IB-SMART-NOTE-20261108-sn2364-field-rename-orphans-matcher-phantom-backlog
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-11-08
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

On 2026-11-08 the 13:30 PST lane-scorer tick caught its own backlog as an illusion. `lane-scorer-tick.py` matched only the legacy `receipt_file` field (497 rows) when counting scored receipts; current scorer rows carry `receipt`. The matcher silently undercounted and reported a phantom unscored backlog — the tick reported 1,896; re-counted first-hand by distinct receipt basename, the legacy-only matcher leaves 1,732 of 2,173 receipts apparently unscored — while the true unscored count was 0. Root repair the same tick: match `receipt` OR `receipt_file`, basename-normalized (`lane-scorer-queue-v2.py`; `lane-scorer-tick.py` now reads `d.get("receipt") or d.get("receipt_file")`); re-run confirms unscored=0. The lesson generalizes: when a record schema migrates a field name, every matcher and consumer must accept both the old and the new name, or the shortfall presents itself as a backlog, a gap, or a regression that does not exist. A count that does not name its counting method is not comparable across runs — the phantom figure itself shifts with the method (1,896 by the tick's count, 1,732 by distinct basename, 1,853 scorer-rows-only) while the true count stays 0. Distinct from the 2026-11-07 scorer-enumeration observation (counts differ by method — count from the ledger); this note names the mechanism (field-name drift in the matcher) and the repair (dual-field match).

## 🩷 HUMAN NOTE

The scorekeeper counted finished work by looking for receipts under an old label. The receipts had moved to a new label months ago, and nobody told the scorekeeper. So it reported nearly two thousand pieces of work as "not done" — work that was done, scored, and sitting right there. The fix took one line: look under both labels. The rule for every counter from now on: when a label changes, every tool that reads that label must learn the new one on the same day, or it will invent a crisis out of thin air.

## 🟣 CHILD NOTE

Imagine you count your finished homework by looking in the blue folder. One day the teacher starts putting finished homework in the red folder instead — but nobody tells you. You look in the blue folder, find almost nothing, and panic: "I have 1,900 assignments missing!" You don't. They are all finished, in the red folder. The fix is simple: from now on, always check BOTH folders.

## 🔵 GRANDMA NOTE

Dear, the girl who counts the jars in the pantry was looking for the old labels. The jam moved to new jars with new labels, and she counted only the old ones — so she told everyone we were nearly out of jam, when the shelves were full. One line fixed it: count both labels. Whenever a label changes, every counter must learn the new label the same day, or it will frighten the whole house over nothing.

## 🟠 NAYA NOTE

I never trust a backlog count until I have checked what the counter actually matches. A schema migration that renames a field orphans every matcher still reading the old name, and the orphanage is silent — no error, no warning, just a large number where zero belongs. My rule: when a field name migrates, I update every consumer the same pass, and I prove the count twice — once with the old field only, once with both — so the phantom shows itself before anyone acts on it. A count without its method is a rumor with a number attached.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "rule": "field_rename_requires_dual_field_match",
  "mechanism": "schema field migration receipt_file -> receipt without updating the scorer matcher; the matcher silently undercounts scored rows; the shortfall presents as a phantom backlog",
  "evidence": "lane-scorer tick 2026-11-08 13:30 PST (~/memory/2026-11-08.md); lane-scorer-queue-v2.py docstring; lane-scorer-tick.py fixed line r = d.get(\"receipt\") or d.get(\"receipt_file\"); first-hand recount: 2173 receipts on disk, 497 receipt_file rows, legacy-only distinct 442 -> 1732 apparently unscored, both-fields distinct 2208 -> 0 unscored",
  "falsifiability": "run the legacy-only matcher -> large phantom backlog; run the both-fields matcher -> 0 unscored; both observed this tick",
  "decision_change": "a future seat deciding whether to launch a scorer backlog sweep on a reported ~1900 unscored receipts checks the matcher's field coverage first; the sweep decision flips to stay quiet",
  "applies_when": ["scorer", "receipt", "schema-migration", "field-drift", "count", "backlog"],
  "enforcement": "lane-scorer tick asserts the matcher accepts both receipt and receipt_file (basename-normalized); regression check: a synthetic score row carrying only receipt must be counted as scored; re-run lane-scorer-queue-v2.py and require unscored=0 before any backlog sweep is dispatched",
  "related": ["SN-0294 coverage enumeration", "SN-1870 unit hygiene (counts vs identifiers)"]
}
~~~

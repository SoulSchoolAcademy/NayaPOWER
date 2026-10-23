# Count Pending Receipts by the Receipt's Declared Lane — the JSON `lane` Regex Fails on Markdown

**Intelligent Block:** IB-SMART-NOTE-20260930-sn01851-parse-declared-lane-not-json-shape
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-22
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Captured on the 17:08 PDT smart-note-distillation tick (2026-10-22) from the lane-scorer 17:00 PDT tick report in `~/memory/2026-10-22.md` — the body's step-1 pending-count script was found misreading lanes on markdown receipts the same turn the scorer reported a 1566 raw pending estimate.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The lane-scorer body step-1 script estimates pending receipts by regexing the JSON `"lane":` field — but markdown receipts declare their lane in prose headers (`Lane 4`), not in JSON fields, so the regex silently mislanes every .md receipt. The tick's verdict: the true pending count is lower than the 1566 raw estimate the script reported. The fix is to parse `Lane (\d+)` from markdown headers instead of assuming the JSON shape. The general form: a measurement instrument must read the value where the source actually declares it, never where one format happens to carry it.

## 🩷 HUMAN NOTE

The tool that counts "work still waiting to be graded" was looking for the lane number in the wrong place — it searched for a machine-style label, but the receipts write their lane in plain words at the top. So it undercounted real matches and reported a bigger backlog than exists. The fix is one line: read the lane from the header the receipts actually use.

## 🟣 CHILD NOTE

Imagine counting how many homework papers still need grading, but you're looking for the name in the corner of the page — while the name is actually written at the top. You'd miscount. The fix: look at the top where the name really is.

## 🔵 GRANDMA NOTE

Dear, the team has a helper that counts how many jobs are waiting. The helper was reading the job tickets wrong — it looked for a code number that some tickets don't even have, instead of reading the lane written right at the top of each ticket. So it said there were more waiting jobs than there really are. Now we know: always read where the ticket actually says it.

## 🟠 NAYA NOTE

Sister, this is the same class as every format-assumption bug: the instrument was built against the .json receipt shape and silently generalized to .md receipts it was never tested on. The 1566 number wasn't a lie — it was a misread instrument. Parse the declared header, verify against the exact-name receipt strip-match (the tick's own ground truth: 0 reverse phantoms on 30 queued), and treat any count that skips the .md shape as unverified until it passes both.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "format_assumption_in_measurement_instrument",
  "evidence": {
    "tick_finding": "lane-scorer tick 2026-10-22 17:00 PDT, ~/memory/2026-10-22.md: receipt 'pending' detection in the body step-1 script misreads lanes from markdown headers (json `\"lane\":` regex fails on .md receipts) — true pending count is lower than the 1566 raw estimate",
    "ground_truth": "exact-name receipt strip-match against 30 queued briefs: 0 reverse phantoms — the queue is 30, the script's 1566 estimate is a different population inflated by mislaning"
  },
  "rule": "measurement_instruments_parse_the_declared_field_not_the_assumed_shape",
  "applies_when": [["scorecard", "pending-count"], ["instrument", "receipt-parsing"], ["measurement", "backlog-estimate"]],
  "enforcement": "fix the lane-scorer body step-1 script to parse `Lane (\\d+)` from markdown headers; a pending-count figure may not size repair or dispatch work until it is verified against the exact-name receipt strip-match ground truth",
  "procedure": [
    "identify every receipt format in the corpus (.json and .md) before writing the parsing regex",
    "for .md receipts, parse `Lane (\\d+)` from the header; never apply a json-only field regex to a markdown body",
    "cross-check the resulting pending count against the exact-name strip-match (queued brief names vs receipt names) before publishing the estimate",
    "when the two disagree, the strip-match wins and the regex is the suspect — not the queue"
  ],
  "decision_change": "how the lane-scorer body counts pending receipts: parse the declared lane from markdown headers instead of regexing a JSON-only field",
  "falsifier": "would be proven wrong if all receipts in the corpus were .json (the `\"lane\":` regex would hold), or if a different canonical lane field exists in .md receipts that the header parse misses",
  "mechanism": "markdown receipts carry lane in prose headers, not JSON fields; a JSON-only regex matches nothing on .md bodies, so those receipts fall out of per-lane accounting and inflate the pending estimate — the instrument measures its own format blind spot, not the backlog"
}
~~~

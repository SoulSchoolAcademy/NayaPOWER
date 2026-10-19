# Pin the Source Before You Probe It — the Pin Turns Your Own Instrument Noise into an Attributable Exclusion

**Intelligent Block:** IB-SMART-NOTE-20260930-sn1679-pin-source-before-probe-turn-instrument-noise-into-attributable-exclusion
**Smart Note:** SN-1679
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-19
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

Whenever a measurement instrument writes into the source it is measuring — a liveness probe appends rows to the query log, a tune-in writes its own log entries — re-pin the source's SHA at action time BEFORE running any probe. The delta between the pin and the post-probe state is exactly your own instrument's write: attributable by construction, excluded by delta. t0900 (2026-10-19) pinned the ask-world query log at `cd868c48…` (124 rows), ran tune-in + live-check probes, then excluded rows 125–127 as its own instrument rows in the delta file §0 with both SHAs named. t0902 found six new rows since the pin and attributed each to its writing process (its own probes, a parallel lane's tune-in) instead of misreading them as fresh demand. Without the pre-probe pin, self-inflicted noise hides inside the measurement as signal.

## 🩷 HUMAN NOTE

If your thermometer leaves a smudge on the glass, photograph the glass before you take the reading. Then your own smudge is just a known subtraction — not a mystery contaminant that poisons every measurement after.

## 🟣 CHILD NOTE

Before you count the cookies, write down how many are in the jar. If you take one to taste it, write that down too. Then your count and the jar's count will always agree — because your own cookie is accounted for.

## 🔵 GRANDMA NOTE

If your scale adds a pound every time you step on it, write down what it says when you lift your foot. The difference is yours. What you measure after that is the truth — not your footprint pretending to be weight.

## 🟠 NAYA NOTE

The concrete instances (2026-10-19, Naya Clarity Narzan, Lane 10 Librarian):
- t0900-lane10.md: action-time pin of `hidden_files/auto-retrieval/ask-world-queries.jsonl` = `cd868c48f78b5202b7fbaac3ecab4a0d1cee54a5d708ff3ebb7663db1c16b4fc` (124 rows, matched the brief's stated SHA). Then `ask-world.py lane 10` tune-in + `live-check` probe ran — appending 3 instrument rows (125–127). Caught and fenced before tallying: rows excluded in `hidden_files/retrieval/query-log-delta-t0900.md` §0 with both the pre-probe and post-probe SHAs quoted. The tally (47/10/7/1) is provably clean of the executor's own writes.
- t0902-lane10.md: six new rows (125–130) since the t0900 pin were individually attributed — rows 125–127 = t0900's own probes, row 128 = a parallel lane-executor run's tune-in, rows 129–130 = the current run's tune-in + live-check. None counted as demand; the demand-quiet verdict survived because every row had a writer.
The ordering matters: pin → probe → attribute-by-delta. Probe-first makes your own rows indistinguishable from the data.

## 🟢 MACHINE NOTE

~~~json
{
  "canonical_object": "INTELLIGENT_BLOCK",
  "sn": "SN-1679",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-19",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "automatic_truth_ceiling": "CANDIDATE",
  "authority_inheritance": false,
  "lesson": "whenever a measurement instrument writes into the source it measures (probes append rows to the log, tune-ins write entries), pin the source's SHA at action time BEFORE running any probe; the delta between the pin and the post-probe state is exactly the instrument's own write — attributable by construction, excluded by delta, never silently tallied as signal",
  "decision_change": "any lane measuring a source that its own probes will write to will (1) pin the source SHA first, (2) probe, (3) attribute every post-pin row to its writer and exclude its own rows from the tally, quoting both SHAs in the receipt — instead of probing first and discovering contamination after the numbers land",
  "falsifiability": "a probe-based measurement that pins first and still leaves unattributable contamination — probe writes not captured by the pin-to-post-probe delta — would falsify the attribution-by-construction claim; alternatively, a tally that pins first and shows zero excluded rows (no self-write) would show the discipline is cheap where it is unnecessary",
  "mechanism": "pinning fixes the premise state before the instrument acts; the post-probe delta is closed over exactly the instrument's writes, so each new row is attributable to its writing process (pid/cmd/ts/lane) rather than inferable from content — without the pin, self-inflicted rows are content-identical to real rows and the tally is silently contaminated",
  "applies_when": [["measurement","instrument-contamination"], ["verification","pre-run-pin"], ["log","probe-side-effects"]],
  "enforcement": "measurement-receipt review rejects any probe-based measurement receipt whose method includes a self-writing probe (probe/tune-in/live-check that appends to the measured source) but cites no pre-probe pin SHA and names no excluded instrument rows; the receipt is REJECTED until the pin (SHA) and the own-row exclusion (row ids) are quoted. Check runs on every measurement receipt before sign-out.",
  "evidence": "hidden_files/twelve-lane-receipts/t0900-lane10.md (2026-10-19, 9.5/10): pre-probe pin cd868c48… (124 rows), 3 own instrument rows (125–127) excluded in hidden_files/retrieval/query-log-delta-t0900.md §0 with both SHAs; hidden_files/twelve-lane-receipts/t0902-lane10.md (2026-10-19, 9.5/10): 6 new rows (125–130) each attributed to its writing process instead of being misread as new demand"
}
~~~

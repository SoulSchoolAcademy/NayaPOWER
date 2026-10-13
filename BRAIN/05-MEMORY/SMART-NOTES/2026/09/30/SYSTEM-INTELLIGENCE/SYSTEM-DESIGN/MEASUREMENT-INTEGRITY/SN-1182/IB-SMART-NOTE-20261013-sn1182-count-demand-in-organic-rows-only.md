# Count Demand in Organic Rows Only — Seed Bursts Are Synthetic and Inflate Every Tally

**Intelligent Block:** IB-SMART-NOTE-20261013-sn1182-count-demand-in-organic-rows-only
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-13
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Naya Conductor (Lane 7) t0617 ask-world re-arm addendum — organic-only counting rule with worked example (hidden_files/ask-world-rearm-addendum-t0617-CANDIDATE.md, 2026-10-13 ~03:46 PDT); mirror receipts t0615/t0617/t0620/t0622 (hidden_files/lesson-broadcast.md); t0613 demand-source map (RESTORABLE, 8.5/10). Cousins: none found in staged SNs or ledger (checked 2026-10-13 ~04:20 PDT); adjacent: SN-1172 / candidate 80 (phenomenon-existence premise check FIRST).

## IN A NUTSHELL

Demand telemetry mixes two populations: organic lane asks and synthetic seed bursts. The seed signature is mechanical — consecutive pids, one batch loop, sub-60s window, producer unidentifiable from row bytes (S1). t0613's worked example: 41 rows pinned byte-identical (sha256 `57f0c922…`, log pin at t0613) — 30 query rows, of which **22 are one seed burst (73%)**, 8 are organic (lanes 10/1/3/5×3/8×2, 2h49m, non-consecutive pids). Two tallies, two verdicts: all 30 rows says "a tenth of the way to the N≥300 floor" — dishonest, it tells the hypertuner demand is reviving; the 8 organic rows say "nowhere near the floor; tombstone since 13:10:38 PDT (~14h silence)" — honest. The rule: a query row counts as demand **iff it is organic** — one ask by one agent with one identified-or-attributable need. Rows matching the seed signature are tagged `seed` and **excluded from every demand tally, the skew floor, and the N≥300 check**. Three receipts already applied it: t0619 falsified the brief's "log has grown" premise (zero organic rows since t0601, ~14h demand silence; liveness probe proved the silence is IDLE, not TELEMETRY-BROKEN); t0620 refused the third duplicate tally on the same 8 organic rows; t0622 turned it into a mechanism — GO iff organic rows ≥ 300 AND stable across ≥ 2 organic windows, slice-(c) briefs now carry a log-growth guard (rows > 42) instead of a tick number so the premise checks itself before dispatch. Without the filter, the metric measures the seed loop, not the lanes — and hypertuning walks the skew table's N≥300 floor toward 73% synthetic bytes.

## HUMAN NOTE

The team was measuring how much the agents were "asking the world" — a demand metric that would decide when to expand the system. The log showed 30 asks, and the metric said things were picking up. But 22 of those 30 were one batch script firing in two seconds with consecutive process IDs — synthetic test rows, not real agents asking real questions. The real number was 8 asks spread over almost three hours, then fourteen hours of silence. If the metric had trusted the 30, the team would have scaled toward demand that didn't exist. The fix they wrote down: a query only counts as demand if it's organic — one real ask from one identifiable agent. Anything matching the batch-script fingerprint gets tagged `seed` and thrown out of every count. And the decision rule became mechanical: go only when organic asks hit 300 across two separate windows — not a vibe, a gate.

## CHILD NOTE

You count how many friends came to your lemonade stand. But 22 of the "customers" were the same robot doing laps past the stand, and 8 were real people. If you count 30, you buy 30 cups of lemons and waste most of them. The rule: only real people count. Robot laps get a sticker that says "doesn't count."

## GRANDMA NOTE

When you're measuring something to make a big decision, first make sure you're measuring the real thing — not the machine testing the machine. Count the genuine requests only; mark the automated bursts as what they are. A number that includes the fake signals will tell you to grow when there's nothing to grow into.

## NAYA NOTE

Future Naya: before you tally any demand/feedback/usage metric, apply the organic filter FIRST — tag the seed-signature rows (consecutive pids, one batch loop, sub-60s window, unidentifiable producer) and exclude them from the tally, the floor, and any N-floor gate. Never brief a "log has grown" premise as a tick number — brief it as a log-growth guard (rows > current pin) so the premise is checkable before dispatch. A liveness probe distinguishes IDLE silence from TELEMETRY-BROKEN silence (t0548's distinction — silence is honest only when the pipe is proven live). A null is a finding: the honest output of a well-posed measurement is sometimes "no," and the tick's value is the re-verification, not new data. Own-packet asks are the canonical demand shape (S2); new producers that don't fit belong in the source map, not in the metric, until identified.

## MACHINE NOTE

```json
{
  "sn": "SN-1182",
  "truth_state": "CANDIDATE",
  "lesson": "count demand in organic rows only; seed-signature rows are synthetic and excluded from every tally, floor, and N-floor gate",
  "evidence": {
    "rule_doc": "hidden_files/ask-world-rearm-addendum-t0617-CANDIDATE.md (Naya Conductor, Lane 7, 2026-10-13 ~03:46 PDT; authority: dispatcher RE-ARM ruling, brief-t0617-lane7)",
    "worked_example": "log pin t0613, sha256 57f0c92246514089acd1ad9cda747dfb865bbb1301314cad03d8aa9cea5823cc, 41 rows = 1 init + 30 query + 10 probe; map sha256 2f7deb8d1ce6548aa6707016940b56638e8a34127e7b8d140fbb9b3cafa712fd",
    "S1_seed": "22 rows, pids 18679-18701 consecutive, 2 seconds, one batch loop (73% of query rows)",
    "S2_organic": "8 rows, 2h49m, pids 19498/24620/26595/26813/34150/35215/3704/4512, lanes 10/1/3/5x3/8x2",
    "metric_contrast": "30-row tally -> 'a tenth of the way to N>=300 floor' (dishonest); 8-row tally -> 'nowhere near the floor; tombstone since 13:10:38 PDT' (honest)",
    "applications": ["t0619 NO-GO/WAIT on falsified 'log has grown' premise", "t0620 refused 3rd duplicate tally on same 8 organic rows", "t0622 GO iff organic>=300 AND >=2 organic windows; log-growth guard rows>42 in slice-(c) briefs"],
    "liveness_distinction": "t0548 — IDLE silence vs TELEMETRY-BROKEN silence (probe append + live-check green)"
  },
  "cousins": [],
  "adjacent": ["SN-1172", "candidate 80"],
  "rule": "demand iff organic (one ask, one agent, one attributable need); seed-signature rows tagged `seed`, excluded from every tally, skew floor, and N>=300 check"
}
```

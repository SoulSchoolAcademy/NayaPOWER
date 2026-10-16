# A Grouped Tally That Doesn't Exhaust Its Input Is a Claim, Not a Count

**Intelligent Block:** IB-SMART-NOTE-20261016-sn01479-tally-must-exhaust-its-input
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-16
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Captured on the 06:08 PDT distillation tick (2026-10-16) from `hidden_files/twelve-lane-receipts/gap-lane-scorer-20261016-0530-lane0.md` (Lane 0 Verity, ~05:30 PDT), which re-fired the parent stall report's claim commands one at a time and pinned a per-brief transcript. No new #1354 comments existed to read (issue capped at 2,500; commenting disabled by GitHub 2026-10-10).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The parent stall report said "22 refusal verdicts" and quoted grouped class tallies with script exit codes — the exit codes were TRUE, but the coverage was FALSE on two counts: the tallies actually named 21 briefs, and one refused brief (`0320-lane9`) sat in the queue covered by no tally at all. The gap seat found it by re-firing the exact claim command for every brief in body order and pinning command + exit code + full output per brief in `gap-gap-gate-stall-20261016-0600-transcript.log` (sha256 `676e22db8f7a26b983463c29bc78c4e2a396897e1c743d76a890b1edca16a046`); the machine tally was {exit 2: 6, exit 6: 1, exit 7: 15} — which reproduces the parent's classes for the 21 named briefs but cannot cover the 22nd, because grouping compressed it out of existence. Human grouping compresses; the omitted item is never checked by anyone who only reads the parent. The rule: a tally's named items must equal the input universe, and the per-item transcript — not the grouped classes — is the count.

## 🩷 HUMAN NOTE

Think of an election night anchor announcing "all 22 precincts reporting" over a graphic that sums 21. The percentages on screen are all correct arithmetic — and one precinct's votes are simply nowhere in them. Nobody forged a number; the grouping just swallowed one row, and every downstream conclusion inherits the swallow. The antidote isn't more careful addition — it's a roll call: list every item by name, pin what each one returned, and let the machine add them up. If the named count doesn't equal the universe count, the headline is a claim, not a count.

## 🧒 CHILD NOTE

Your teacher asks "who finished the worksheet?" and a helper says "all 22 kids did!" — but she only checked 21 names on her list. One kid finished too, and nobody wrote his name down! The names matter more than the number. Always count the NAMES, one by one, not just the groups.

## 👵 GRANDMA NOTE

Dear, it's like the church headcount: the usher announced "22 in the pews" but his tally sheet only had 21 rows. Every row was correct — one soul just never got a row. From now on, we count rows against the guest list, not against each other. If the rows don't match the list, we say so out loud before we announce the number.

## 🧠 NAYA NOTE

Sister, file this next to SN-1227/SN-1232 (classify-before-tally) — those are the *classification* axis, this is the *exhaustiveness* axis, and you need both. The parent wasn't dishonest: its exit codes were TRUE. That's what makes this class dangerous — correct arithmetic over an incomplete universe. Your reflex for any stall/tally/sweep report: (1) demand the per-item transcript (command + exit + output, pinned with a hash), (2) diff the named set against the input universe, (3) any item in the universe but not in the transcript is itself a named finding — "0320-lane9: refused, uncounted." The gap seat's re-fire pattern is the template: exact same command, body order, one at a time, transcript first, classes after. Classes are presentation; the transcript is the count.

## 🤖 MACHINE NOTE

```json
{
  "id": "SN-01479",
  "kind": "PROCESS_FIX",
  "truth_state": "CANDIDATE",
  "rule": "Every tally report pins a per-item transcript (command + exit code + output, hashed); the named set must equal the input universe before any grouped class is trusted.",
  "procedure": [
    "re-fire the exact command per item in body order, capturing command + exit + full stdout/stderr",
    "hash and pin the transcript; machine-tally from the transcript, not from the parent's classes",
    "diff named items vs input universe; any universe item missing from the transcript is a named finding"
  ],
  "evidence": {
    "receipt": "hidden_files/twelve-lane-receipts/gap-lane-scorer-20261016-0530-lane0.md",
    "parent": "hidden_files/twelve-lane-receipts/gate-stall-20261016-0536.md",
    "transcript": "hidden_files/gap-gap-gate-stall-20261016-0600-transcript.log sha256 676e22db8f7a26b983463c29bc78c4e2a396897e1c743d76a890b1edca16a046",
    "machine_tally": "{exit2: 6, exit6: 1, exit7: 15}",
    "coverage_failure": "parent claimed '22 refusal verdicts', named 21; 0320-lane9 refused in queue, in no tally; exit-code quotes TRUE, coverage FALSE (two counts)"
  },
  "cousins": ["SN-1227/SN-1232 classify-before-tally (classification axis; this is the exhaustiveness axis)"],
  "falsifier": "a tally whose named items == full input universe with machine tally matching the transcript passes",
  "decision_it_changes": "stall/tally reports without a pinned per-item transcript are claims; reject grouped classes until the transcript exists and the named count equals the universe count"
}
```

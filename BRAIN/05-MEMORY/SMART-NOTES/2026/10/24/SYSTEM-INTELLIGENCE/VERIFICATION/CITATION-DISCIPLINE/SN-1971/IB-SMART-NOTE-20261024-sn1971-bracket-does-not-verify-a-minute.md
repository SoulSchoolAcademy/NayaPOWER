**Intelligent Block:** IB-SMART-NOTE-20261024-sn1971-bracket-does-not-verify-a-minute
**Smart Note:** SN-1971
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-24
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** hidden_files/twelve-lane-receipts/gap-gap-gap-gap-t0432-lane5.md (Lane 5, Seeker hat, 2026-10-25 04:13-04:17 UTC, self-scored 9.0/10); hidden_files/learning-events-2026-10-25-04.md (CANDIDATE 942). No direct GitHub fetch this tick (cheap-check skip for #1354, which is capped at 2,500 comments); all evidence read from local disk.

## ✦ IN A NUTSHELL

A bracket rules out contradiction; it does not verify a minute — cite a system timestamp for a time claim, or label it note-grade in the same sentence. The gap-gap scoring time "04:01 UTC" had exactly one source: the scorer row's own note text (twelve-lane-scores.jsonl, line 6014), which asserts its own scoring time. The scores file carries no per-row timestamp field, no file bears a 04:01 system timestamp, and scorer note times are typed, not system — rows 6015 and 6016 claim verification at "04:15Z" inside a file last written 04:12:54 UTC. The filesystem bracket (receipt mtime 03:56:27 to brief claim touch 04:04:13 UTC) contains 04:01, so it rules out contradiction, but it cannot verify the minute. The correct citation, now in errata section 6, is: scorer-row note text gives 04:01 UTC; unverified to the minute; bracketed by filesystem times 03:56:27-04:04:13 UTC.

## 🩷 HUMAN NOTE

Imagine someone says "I arrived at 4:01" and the only proof is their own diary entry saying so — while the building's cameras show they arrived sometime between 3:56 and 4:04, but no camera caught the exact minute. The diary entry feels precise, but it is not proof: a time inside a window is consistent, not verified. That is what happened here: the scoring time 04:01 came only from a note that was itself making the claim, and the system records could only narrow it to a seven-minute window. The honest fix was to say so plainly — "note says 04:01, unverified to the minute, bracketed by the system times" — instead of letting a precise-looking minute travel on as if it were proven.

## 🟣 CHILD NOTE

Imagine your friend says "I finished the race at exactly 4:01" but the only proof is a note your friend wrote themselves. The school clock shows the race happened between 3:56 and 4:04, but nobody saw the exact minute. Being inside the window does not prove the exact minute — it only proves your friend is not contradicting the clock. Here the scoring time was like that friend's note: it said 04:01, but no system clock ever recorded 04:01. The rule is: if you want to claim an exact minute, show a system clock for it; otherwise say "my note says this, but it is not verified to the minute" in the very same sentence.

## 🔵 GRANDMA NOTE

Think of it like a recipe card that says "baked at 4:01" in someone's handwriting, while the oven's timer only shows the baking happened between 3:56 and 4:04. The handwriting is a claim, not a measurement — and being inside the oven's window does not turn handwriting into a measurement. That is the lesson here: a bracket can tell you a claim is not impossible, but it cannot tell you the claim is exactly right. From now on, an exact minute needs a system record behind it (a file time, a comment time), or it must travel with its warning attached: "note-grade, unverified to the minute, bracketed by these system times." Precision without proof is just neat-looking guessing.

## 🟠 NAYA NOTE

For the next Naya who cites a time in an errata or scorer chain: treat the citation as two separate claims and verify them separately — the minute, and the bracket. A minute is verified only by a system timestamp that reads the minute itself (file mtime, comment created_at, log line); a bracket is verified by system times at both ends and proves only consistency inside the interval. Never upgrade "consistent" to "verified," and never let a source verify itself: the scorer row's note is the claim, not the evidence for the claim, just as a seal header cannot prove seal-before-run. The gap-gap-gap-gap run is the worked example: all three named sources plus two more were checked (scorer row source, scores-file history, filesystem bracket, live-board check of 48 comments since midnight with zero hits for t0432/04:01/gap-gap, and the typed nature of scorer note times), the figure failed every independent check, and the errata was amended by append-only section 6 (pre-addendum sha b26663ea992640ddf3a4b67feae23cb949b0f99848623099fe6e4100cd8642ee preserved verbatim; post-addendum sha 8fbc9ca6c0a2c88f82838aaca3d7810dd219a009e1297afd0b49e06460e861d2). Name the honest hole, as the receipt did: the 04:01 minute itself remains genuinely unknown, and the old errata SHA citation needs re-pinning in the next scorer row.

## 🟢 MACHINE NOTE

```json
{
  "sn": "SN-1971",
  "title": "A bracket rules out contradiction; it does not verify a minute - cite a system timestamp for a time claim, or label it note-grade in the same sentence",
  "observation": false,
  "applies_when": ["citation", "timestamp", "scoring", "errata"],
  "enforcement": "Citation check for any time claim in an errata or scorer chain: require a system timestamp (file mtime, comment created_at, log line) for the minute, or the sentence must carry 'note-grade' plus its bracket in the same sentence. A bare minute sourced only from scorer-row note text is bounced to the qualified form (note text gives the time; unverified to the minute; bracketed by system times).",
  "evidence": "hidden_files/twelve-lane-receipts/gap-gap-gap-gap-t0432-lane5.md (Lane 5, self 9.0/10): the only source of '04:01' is the scorer row for gap-gap-t0432 itself (twelve-lane-scores.jsonl line 6014), whose note text says the receipt 'was written 03:56 UTC and scored 04:01 UTC'. The scores file carries no per-row timestamp field; its whole-file mtime 2026-10-25 04:12:54 UTC reflects later appends (rows 6015, 6016), not the row 6014 write. Filesystem bracket (system times, UTC 2026-10-25): gap-gap receipt mtime 03:56:27; gap-gap-gap brief claim touch 04:04:13; 04:01 lies inside the 7m46s bracket (consistent, not verified); no file bears a 04:01 system timestamp. Scorer note times are typed, not system: rows 6015 and 6016 claim verification at '2026-10-25T04:15Z' inside a file last written 04:12:54 UTC. Board check: 48 comments on live board #2793 since 2026-10-25T00:00Z, zero hits for t0432, 04:01, or gap-gap. Errata amended by append-only section 6: pre-addendum sha256 b26663ea992640ddf3a4b67feae23cb949b0f99848623099fe6e4100cd8642ee; post-addendum sha256 8fbc9ca6c0a2c88f82838aaca3d7810dd219a009e1297afd0b49e06460e861d2.",
  "decision_change": "When a future run cites a scoring or run time, the worker cites a system timestamp for it, or labels it note-grade with its bracket in the same sentence. The worker never upgrades 'inside the bracket' to 'verified to the minute', and never lets a note-text minute travel unqualified into an errata chain. The 04:01 citation form from now on is: scorer-row note text gives 04:01 UTC; unverified to the minute; bracketed by filesystem times 03:56:27-04:04:13 UTC.",
  "falsifier": "If a system timestamp for 04:01 surfaces (a file mtime, a comment created_at, a log line reading that minute), the minute becomes verified and the note-grade label lifts for that citation. If the scores file gains per-row system timestamps, the note-grade rule narrows to rows without them. Until either appears, the minute stays unverified: a tighter bracket alone never falsifies the unverified status, it only narrows the window."
}
```

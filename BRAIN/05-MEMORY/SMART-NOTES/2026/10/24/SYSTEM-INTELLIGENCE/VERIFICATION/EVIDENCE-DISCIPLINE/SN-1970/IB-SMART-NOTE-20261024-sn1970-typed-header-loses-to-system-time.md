**Intelligent Block:** IB-SMART-NOTE-20261024-sn1970-typed-header-loses-to-system-time
**Smart Note:** SN-1970
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-24
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** hidden_files/twelve-lane-receipts/gap-gap-gap-t0432-lane5.md (Lane 5, Seeker hat, 2026-10-25 04:04-04:06 UTC, self-scored 9.0/10); hidden_files/learning-events-2026-10-25-04.md (CANDIDATE 941). No direct GitHub fetch this tick (cheap-check skip for #1354, which is capped at 2,500 comments); all evidence read from local disk.

## ✦ IN A NUTSHELL

When a sealed file's typed header disagrees with system-recorded time, the header loses — and the correction is appended beside the seal, never written over it. The third-baseline seal file carried the typed header "Sealed: 2026-10-25 04:00 UTC", which is 4 minutes 53 seconds later than its filesystem creation (03:55:07 UTC) and later than the results file — taken literally, it would invert seal-before-run. The header is author-typed, not system-generated, so it was discarded as evidence and 03:55:07 UTC is the seal time to cite. The correction went into a separate errata file, because scrubbing the header in place would destroy the SHA chain a second seat verifies.

## 🩷 HUMAN NOTE

Imagine a sealed envelope with a handwritten date on it that says it was sealed after the letter inside was already mailed. You would not believe the handwriting over the postmark — the postmark is recorded by the system, the handwriting is just what someone wrote. That is what happened here: the seal's own header claimed a time later than the files around it, which would make the whole "sealed before the run" story backwards. The fix was not to erase the handwriting — erasing it would break the seal itself. The fix was to write the correction on a separate note kept beside the envelope, and to cite the system-recorded time from now on.

## 🟣 CHILD NOTE

Imagine you write "I finished my homework at 8 o'clock" on your paper, but the clock on the wall and your teacher's record both say you finished at 7:55. Your note is just what you wrote; the clock is the real record. Here the sealed test file had a typed time that was later than when the computer actually made it — if you believed the typed time, the story would be backwards. The smart fix was to leave the original file exactly as it was (so anyone can still check it) and put the correction on a separate note next to it. The rule is: the typed words lose, the system clock wins, and corrections live beside the evidence, never instead of it.

## 🔵 GRANDMA NOTE

Think of it like a jam jar with a handwritten label saying it was sealed on Tuesday, while the shop's stamp and the delivery record both say Monday. You trust the shop's stamp, not the handwriting — and you certainly do not peel the label off and rewrite it, because then nobody could ever check what was really there. Here the seal file's typed header said 04:00, but the computer's own records said the file was created at 03:55, before the results. The worker kept the original untouched, wrote the correction in a separate errata note, and cited the computer's time. That is the lesson to carry: when handwriting and system records disagree, the system record wins, and the correction is added alongside, never scrubbed over.

## 🟠 NAYA NOTE

For the next Naya who writes or cites a seal: the timestamp question comes before the citation, not after it. A seal's timestamp must be system-recorded, or the seal must state plainly that its timestamp is hand-typed. When you find a disagreement, do three things, in this order: (1) cite the system time (filesystem creation/mtime, results-file times, all from stat), not the typed header; (2) append the correction as an errata file beside the seal, preserving the sealed bytes and their SHA exactly; (3) record the linkage outside the sealed set (scorer row, rotation note), because nothing inside the sealed files can point to the errata without breaking the SHA. The gap-gap-gap run is the worked example: corrected window 03:53-03:56 UTC from stat (claim 03:53, seal 03:55:07, script 03:55:15, results 03:55:24, comparison 03:55:38, receipt 03:56:27), the claimed 04:10 run-window end discarded as unsupported by any file, and the timestamp-independent leg kept separate — the machine script's non-read of the seal, verified by grep (it opens only ids.json plus corpus embeddings). Name the honest hole, as the receipt did: a reader who opens the seal alone still sees "04:00" with no pointer to the errata, by preservation design.

## 🟢 MACHINE NOTE

```json
{
  "sn": "SN-1970",
  "title": "When a sealed file's typed header disagrees with system-recorded time, the header loses - and the correction is appended beside the seal, never written over it",
  "observation": false,
  "applies_when": ["seal", "timestamp", "evidence", "errata"],
  "enforcement": "Seal-verification check: before citing a seal time, compare the typed header against filesystem creation and modification times and results-file times from stat. On disagreement, the run appends an errata file beside the seal (never edits the seal) and cites the system time; a citation that quotes only the typed header is bounced. A seal whose timestamp is hand-typed must say so, or carry a system-recorded timestamp.",
  "evidence": "hidden_files/twelve-lane-receipts/gap-gap-gap-t0432-lane5.md (Lane 5, self 9.0/10): seal file header 'Sealed: 2026-10-25 04:00 UTC' is 4m53s later than filesystem creation 03:55:07 UTC and later than the results file; taken literally it inverts seal-before-run. Corrected window from stat: claim 03:53, seal 03:55:07, script 03:55:15, results 03:55:24, comparison 03:55:38, receipt 03:56:27 UTC; claimed 04:10 end unsupported by any file and discarded. Errata (new file, this run): hidden_files/auto-retrieval/errata-gap-gap-gap-t0432.md sha256 b26663ea992640ddf3a4b67feae23cb949b0f99848623099fe6e4100cd8642ee (pre-addendum bytes). Sealed files re-verified unchanged (seal 142f24e3558053cb42f67592eb6e81b2a6f6d00686277c3717dc307b93ad0e5d; results a95175b7a9bcb6591c4461311d1d110cc669f3fa6033fafe7fc9482bccbc319e; comparison 8d8586c5fc7dbed6710ce2d2d1426cce5c396b602700abc4a19f069e2949e10). Timestamp-independent leg: machine script non-read of the seal verified by grep (opens only ids.json plus corpus embeddings).",
  "decision_change": "When a future seal header disagrees with system-recorded time, the worker cites the system time, appends the correction as an errata file beside the seal, and never edits the sealed file in place. The worker also never writes a run window whose end post-dates the receipt file. A seal timestamp is system-recorded or labeled hand-typed at write time.",
  "falsifier": "If the system times for that file are proven unreliable (mtime touched or restored, clock skew demonstrated, file copied with preserved times that do not reflect creation), the header could stand and the system-time citation weakens. Also falsified in the other direction if the seal carries a trusted system timestamp (signed, anchored, or logged by an independent system) that agrees with the header: then the header is corroborated, not discarded. A single typed header alone never falsifies a system-time record."
}
```

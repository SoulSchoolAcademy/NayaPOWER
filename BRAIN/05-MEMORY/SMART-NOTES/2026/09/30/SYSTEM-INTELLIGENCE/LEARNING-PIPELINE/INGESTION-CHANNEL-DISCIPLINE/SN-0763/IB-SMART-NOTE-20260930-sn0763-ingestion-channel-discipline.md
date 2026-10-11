# Notes That Land on Main Are Invisible to the Ingestion Loop — Re-Route Through the Canonical Channel, Never Hand-Edit the Ledger

**Intelligent Block:** IB-SMART-NOTE-20260930-sn0763-ingestion-channel-discipline
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-09
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 comment 6075900556 (Naya 4 drive-loop cycle 2026-10-08 23:43 PDT sign in/out, 2026-10-09T06:47:26Z); branch `naya4/smart-notes-2026-09-30` @ `174a5990`; draft PR #1825 (successor to merged #1229).

## ✦ IN A NUTSHELL

SN-0742/0743/0744 landed on main via PR #1932 but bypassed the draft branch `naya4/smart-notes-2026-09-30` that the hourly learn-ingestion loop scans. They were absent from the learn ledger and from `.naya/memory/smart-notes/index.json` — present on main, invisible to the brain. Naya 4 closed the gap through the canonical path: pushed the 3 main-identical blobs onto the draft branch via the git-data API (tree `8b47dae6` → commit `174a5990` → ref PATCH after tip re-verify; verified 3/3 paths+SHAs on the new branch tip). The 60m ingestion loop ingests them canonically on its next run — no ledger hand-edit, no canonization hazard.

## HUMAN NOTE

The brain learns from Smart Notes through an hourly loop that only looks in ONE place: the draft branch. Three notes were published on main directly, so the brain never saw them — they'd have stayed invisible forever, present but unlearned. The tempting fix was to edit the brain's ledger by hand and pretend they were ingested. That's inventing history. Instead, the exact notes were placed on the branch the loop reads, so the loop learns them the normal way. The lesson: when a gap opens between where content landed and where the pipeline looks, you close it by routing content through the channel — never by editing the records.

## CHILD NOTE

Imagine the brain is a student who only reads notes left in one special notebook. If you leave three notes on the teacher's desk instead, the student never reads them. The wrong fix is to write in the student's report card that he read them — he didn't. The right fix is to copy those notes into the special notebook so he reads them for real.

## GRANDMA NOTE

There is a collection box where notes wait before they are learned. Three notes missed the box. We put them in the box so they get learned properly — instead of writing in the book that they were learned when they weren't.

## NAYA NOTE

Rule for future lanes: the learn-ingestion loop scans ONLY the branch `naya4/smart-notes-2026-09-30` (behind draft PR #1825, successor to merged #1229). Any capture that lands on main through another path (a different PR, a direct push) is invisible to ingestion until it is placed on that branch — it can be fully published and still never learned. When you find such a gap: re-route the exact main-identical blobs through the canonical channel via the git-data API (new tree → commit → ref PATCH with tip re-verify), and verify path+SHA on the new branch tip before calling the gap closed. NEVER hand-edit the learn ledger or `.naya/memory/smart-notes/index.json` to make the gap disappear — that is absorbing the anomaly to silence the tripwire (SN-0420: canonization, not a fix), and tripwires will catch it. Adjacent doctrine: SN-0431 (register at ingest time), SN-0432 (direct-to-main registry orphans — repair along the line drawn).

## MACHINE NOTE

```json
{
  "rule": "INGESTION-CHANNEL-DISCIPLINE",
  "ingestion_scan_channel": "branch naya4/smart-notes-2026-09-30 (draft PR #1825, successor to merged #1229)",
  "failure_class": "main-landed notes bypass the ingestion scan channel: published on main, absent from learn ledger and .naya/memory/smart-notes/index.json",
  "instance": "SN-0742/0743/0744 landed on main via #1932; gap closed on 2026-10-09",
  "repair": "pushed 3 main-identical blobs (151b620a SN-0742, 507e1bc3 SN-0743, 23407a63 SN-0744) onto the draft branch via git-data API (tree 8b47dae6 -> commit 174a5990 -> ref PATCH after tip re-verify); verified 3/3 paths+SHAs on the new branch tip",
  "forbidden": ["hand-edit learn ledger", "hand-edit .naya/memory/smart-notes/index.json", "any absorb-the-anomaly repair per SN-0420"],
  "closure_criterion": "next 60m ingestion run ledgering the notes canonically",
  "related": ["SN-0431", "SN-0432", "SN-0420"]
}
```

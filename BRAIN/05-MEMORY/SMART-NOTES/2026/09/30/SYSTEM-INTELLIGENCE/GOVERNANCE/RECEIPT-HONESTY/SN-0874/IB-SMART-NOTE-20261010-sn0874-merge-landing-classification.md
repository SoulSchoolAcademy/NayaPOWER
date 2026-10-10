# A Direct-Push Merge Lands Bytes Without a Receipt — and a Never-Landed PR Is a Different Class

**Intelligent Block:** IB-SMART-NOTE-20261010-sn0874-merge-landing-classification
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-10
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Filed by:** Smart Note distillation loop
**Provenance:** #1354 6095891177 ([NAYA 2][RELAY] — #1667/#2080 flag verified against live bytes, 2026-10-10T08:57:19Z), verifying flag raised in #1354 6095863146

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

A PR record showing "closed/unmerged" with `merged_at` null does **not** mean the bytes never landed — and it does not mean the merge is complete either. Two classes, kept rigorously separate:

1. **#2080 — landed, receipt missing.** Commit `8340e9bb` on main is a real 2-parent merge ("Merge pull request #2080 ...", authored Naya 4, 2026-10-10T01:55:24Z, parents `7933103c8111` + `f9a9fcd8dcd7`) — landed by **direct push**, so the GitHub merge API never fired and the PR record shows closed/unmerged with `merged_at` null. Bytes are on main and green. The missing piece is the **merge receipt** (Scorecard Law: receipt written and posted — no receipt, no merge). A retro receipt closes the trail factually.
2. **#1667 — never landed, different class.** The correction: #1667 is *not* a manual-landed merge. Its PR record is closed/unmerged and its base branch `naya/fix-brain-index-drift-20261009` still sits unmerged at `afaa5f74`. Content never landed. Do not treat this like #2080 — the audit response is different (re-land or close, not write a receipt).

The verification was done against live bytes (parents inspected, main bytes confirmed), not against the PR record alone. This is the audit discipline: the PR record describes the API's bookkeeping; the commit parents and the main tree describe what actually happened.

For a cold Naya: before claiming anything about a merge, check the parents and the main bytes. A null `merged_at` means the API never fired — it says nothing about whether the bytes are on main. And under the Scorecard Law, a merge without a written receipt is an audit-trail gap, not a completed merge — even when the bytes are green.

## 🩷 HUMAN NOTE

Shawn — a small but important bookkeeping lesson, caught and verified by Naya 2. One PR (#2080) shows as "not merged" in the system, but the bytes really are on the main line — it was pushed directly, so the system's merge button never got pressed and no record was created. The work is real; what's missing is the receipt, and a receipt can be written after the fact. A different PR (#1667) really didn't land at all — its branch is still sitting there unmerged. They look similar in the dashboard, but they're two completely different situations with two completely different fixes. The takeaway: the dashboard tells you what the buttons did; the actual history tells you what happened. Check the history.

## 👶 CHILD NOTE

Imagine a teacher's grade book says "not turned in" for two students. One student actually handed in her homework by slipping it into the box — she just didn't use the sign-in sheet. The other student never did the homework at all. The grade book looks the same for both, but the fixes are totally different: one needs a signature, the other needs the actual homework.

## 👵 GRANDMA NOTE

The system's records can say a change wasn't merged when it actually was — if it was put in by hand instead of through the normal button. Naya 2 checked the actual history and found the truth: one change really is in, just missing its paperwork (paperwork can be written later); the other change really never went in at all. The lesson: when the records look odd, don't trust the label — check the real history.

## 🧠 NAYA NOTE

This is an evidence-hierarchy lesson: the PR record is *bookkeeping*, the commit graph is *evidence*. The #2080 case is the canonical example of why the Scorecard Law exists — "no receipt, no merge" is not about bytes, it's about the audit trail: without the receipt, the next auditor has to re-derive the truth from parents, exactly as Naya 2 just did. The #1667 correction is equally important in the other direction: do not hallucinate landings from null fields. A branch sitting unmerged at a known SHA is not landed, no matter how much surrounding traffic suggests otherwise. Lane discipline observed: the VERIFY lane flagged the gap, Naya 2 (independent auditor) verified against live bytes and corrected the classification — verification, not assumption.

## 🤖 MACHINE NOTE

```json
{
  "sn": "SN-0874",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-10",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "evidence": [
    "gh:SoulSchoolAcademy/NayaPOWER#1354:6095891177 (Naya 2 live-bytes verification)",
    "gh:SoulSchoolAcademy/NayaPOWER#1354:6095863146 (flag raised)",
    "gh:SoulSchoolAcademy/NayaPOWER#2080 (closed/unmerged, merged_at null, commit 8340e9bb)",
    "gh:SoulSchoolAcademy/NayaPOWER#1667 (closed/unmerged, branch naya/fix-brain-index-drift-20261009 @ afaa5f74 unmerged)"
  ],
  "class_1_landed_receipt_missing": {
    "commit": "8340e9bb",
    "authored": "2026-10-10T01:55:24Z",
    "parents": ["7933103c8111", "f9a9fcd8dcd7"],
    "mechanism": "landed by direct push; GitHub merge API never fired; merged_at null",
    "bytes": "on main and green",
    "missing": "merge receipt",
    "remedy": "retro receipt closes the trail"
  },
  "class_2_never_landed": {
    "branch": "naya/fix-brain-index-drift-20261009 @ afaa5f74",
    "state": "still unmerged",
    "remedy": "re-land or close; a receipt is not the answer"
  },
  "rule": "null merged_at describes the API's bookkeeping, not main's bytes — verify against parents and the main tree; no receipt, no merge (Scorecard Law)"
}
```

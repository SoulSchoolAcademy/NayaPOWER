Intelligent Block: IB-SMART-NOTE-20261026-sn2014-close-time-from-timeline-not-updated-at
Truth state: CANDIDATE
Scope: PRIVATE
Captured date: 2026-10-26
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL
Derive close times from timeline closed events, never from updated_at. A fresh re-execution of all 30 census PRs found 18 of 30 rows now carry updated_at 2026-10-21T03:41–03:56Z — each with exactly one 2026-10-21 timeline event, head_ref_deleted by SoulSchoolAcademy (branch cleanup): no reopen, no re-close, no head change. The census sentence "nothing touched since close" was true on 2026-10-15 and is stale now, and three close times shift +1s on the timeline (1877, 2033, 2037). updated_at is a last-touch stamp, not a close record; the timeline closed event is the close itself.

## 🩷 HUMAN NOTE
A file's "last changed" date moves whenever anyone touches the file for any reason — including tidying up branches. That is why 18 supposedly untouched records suddenly looked changed: someone cleaned up branches, and the cleanup stamped a new date. The real closing moment lives in the timeline, the diary of what actually happened. If you want to know when something closed, read the diary entry that says "closed" — never the "last touched" stamp.

## 🟣 CHILD NOTE
Think of a library book. The "last touched" sticker changes every time anyone picks the book up, even just to put it back on the shelf. But the "returned" stamp only happens once, when the book is really returned. If you want to know when the book came back, you read the "returned" stamp, not the "last touched" sticker.

## 🔵 GRANDMA NOTE
Dear, this one is easy to remember: the date on the outside of the folder changes whenever the folder is moved, but the note inside that says "closed on this day" never changes. Eighteen folders looked newly touched because someone tidied the shelf — nothing inside them had actually reopened or changed. Always read the note inside, not the date on the outside.

## 🟠 NAYA NOTE
For any Naya running a PR census or citing a close time: the timeline closed event is ground truth; updated_at is never a close-time proxy again. The 30-row re-run confirms the rest of the census (30/30 closed, 0 merged, 0 reopened, 30/30 heads matching census pins, 30/30 created_at identical) — the measurement confirmation is verification, not the lesson. The lesson is the proxy rule plus its corrections: 1877 08:27:16Z to 08:27:17Z, 2033 09:25:24Z to 09:25:25Z, 2037 09:25:27Z to 09:25:28Z; batch windows hold (t0072, t0122). Cousin, not duplicate: SN-0969 (anchor the evidence window to the event — the general rule); this note is the close-time-specific case with the updated_at corruption mechanism. Caveat carried from the receipt: 1825's touch bound rests on page-1 timeline events only.

## 🟢 MACHINE NOTE
```json
{
  "sn": "SN-2014",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-26",
  "applies_when": ["census", "evidence"],
  "enforcement": "A census close-time column must cite the timeline closed event (event type and timestamp); any census citing updated_at as a close time is bounced in review. Verification: re-derive close times via timeline closed events for the 30-row fossil-bar set and confirm the three +1s shifts (1877, 2033, 2037) and the 18 head_ref_deleted touches.",
  "evidence": "hidden_files/twelve-lane-receipts/gap-gap-scorer-20261014-2250-lane3.md (2026-10-26 20:52Z) + hidden_files/lane-3/gap-gap-scorer-20261014-2250-lane3/second-seat-recheck.md sections 1 and 4; learning event CANDIDATE 979 in hidden_files/learning-events-2026-10-26-21.md",
  "decision_change": "Every future census derives close times from timeline closed events and never cites updated_at as a close-time proxy.",
  "falsifiability": "Proved wrong if a PR's timeline closed event is shown missing or misdated while its updated_at matches the true close, or if updated_at is shown to move only on close actions (no non-close touch moves it).",
  "mechanism": "updated_at is a last-touch timestamp moved by any write including branch cleanup (head_ref_deleted); the timeline closed event is the record of the close action itself, so only it survives non-close touches unchanged.",
  "cousins": ["SN-0969"],
  "not_a_duplicate_of": "SN-0969 states the general event-anchoring rule; this note is the close-time-specific rule with the concrete updated_at corruption case (18/30 rows, 2026-10-21 branch cleanup) and the +1s corrections."
}
```

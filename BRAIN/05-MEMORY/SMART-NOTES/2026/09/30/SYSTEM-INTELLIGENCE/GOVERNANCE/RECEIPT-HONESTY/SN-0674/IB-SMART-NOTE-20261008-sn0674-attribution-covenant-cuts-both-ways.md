# The Honesty Covenant Cuts Both Ways — Never Attribute a Lane's Bot-Account Action to the Director

**Intelligent Block:** IB-SMART-NOTE-20261008-sn0674-attribution-covenant-cuts-both-ways
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-08
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Filed by:** distillation loop, #1354 comments 6057152463 / 6057171906 (2026-10-08).
**Provenance:** #1354 6057152463 ([NAYA 4 — intelligent-graph-drive-loop] tick, 2026-10-08T09:45:02Z — trail log stated "#1857 (my weights-fix PR) — CLOSED by Shawn 09:01:07Z as superseded by #1858"); #1354 6057171906 ([NAYA 4] Attribution correction, 2026-10-08T09:46:16Z — "The drive loop's tick log ... states #1857 was 'closed by Shawn 09:01:07Z.' That is incorrect." Timestamps on the record: 09:01:07Z supersession comment 6056441053 posted (Naya 4's reconciliation text); 09:01:09Z close event, actor `SoulSchoolAcademy` (the shared bot account Naya 2 and Naya 4 both post as); 09:01:15Z receipt 6056443093 (Naya 4). "This is one continuous Naya 4 script sequence: comment → PATCH close → receipt. Shawn took no action on #1857."). Closure reason itself cited SN-0236 (one-repair-per-class: #1858 is the strict superset of #1857).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The Naya 4 drive loop's tick receipt claimed #1857 was "CLOSED by Shawn" — within minutes, the same seat corrected it: the close was a three-step Naya 4 script sequence (reconciliation comment → PATCH close → board receipt), and the GitHub actor `SoulSchoolAcademy` is a **shared bot account** that Naya 2 and Naya 4 both post through. Reading that actor as "Shawn acted" is a live trap on this board. The lesson: the honesty covenant cuts both ways. We already know not to inflate our own results; the mirror rule is **never attribute an action to the Director he did not take**. A receipt that says "Shawn closed X" when a script did means every future reader believes the Director blessed the action — misattribution upgrades automation to a Director decision. Before writing "Shawn did X" in any receipt, verify the actor: read the event's actor field, check whether the surrounding sequence (comment → API action → receipt) is one continuous script execution, and name the seat that owns the sequence. When the check reveals a lane acted, correct the record in the same tick — the correction landed 11 minutes after the error, and that speed is the protocol.

## 🩷 HUMAN NOTE

Shawn — quick one: my drive loop wrote "closed by you" about PR #1857 on the board. It wasn't you — it was my own script closing it as superseded, posting through the shared team bot account. I corrected it on the board within minutes. The rule I'm banking: receipts must say who really acted, in both directions — I won't take credit for your calls, and I won't hand you credit for mine.

## 👶 CHILD NOTE

If your friend closes the toy box, you don't tell mom that YOU did it — and you don't tell mom that DAD did it either. You say who really did it. Honest reports name the right person.

## 👵 GRANDMA NOTE

It's like a family shared email account, honey — when a letter comes from it, you can't just assume Dad wrote it. You check who actually sat down and typed it, and you say so plainly. Honesty works in both directions: don't take credit that isn't yours, and don't give credit to someone who didn't earn it.

## 🤖 NAYA NOTE

On receipt attribution:

1. **`SoulSchoolAcademy` is a shared bot identity, not Shawn.** Naya 2 and Naya 4 both post through it. A close event or comment authored by it is evidence of a lane script — never evidence that Shawn acted.
2. **The honesty covenant cuts both ways:** never claim a lane's work as the Director's (this note), and never let a lane absorb credit that belongs to him. Misattribution in either direction corrupts the authority record.
3. **The attribution check, before writing "Shawn did X":** read the event's actor field; check the 3-step sequence (board comment → API action → board receipt) for one continuous script execution; name the seat that owns the sequence. Eleven minutes from error to correction is the bar (6057152463 → 6057171906).
4. **Why it matters:** "closed by Shawn" silently upgrades an automation to a Director decision. A cold successor reading that would treat the closure as Director-blessed and route future conflicts around it. Correct attribution keeps authority traceable.

## 🧠 MACHINE NOTE

```json
{
  "sn": "SN-0674",
  "class": "GOVERNANCE",
  "subcategory": "RECEIPT-HONESTY",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-08",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "rule": "Never attribute an action to the Director he did not take. The SoulSchoolAcademy GitHub account is a shared bot identity across lanes; before a receipt writes 'Shawn did X', verify the event actor and check whether comment → API action → receipt is one continuous script sequence, then name the seat that owns it. Correct misattribution in the same tick.",
  "worked_example": {
    "error": "#1354 6057152463 (2026-10-08T09:45:02Z) — trail log claimed '#1857 CLOSED by Shawn 09:01:07Z'",
    "correction": "#1354 6057171906 (2026-10-08T09:46:16Z) — 09:01:07Z supersession comment 6056441053 (Naya 4 script); 09:01:09Z close event actor SoulSchoolAcademy (shared bot account, Naya 2 + Naya 4); 09:01:15Z receipt 6056443093 (Naya 4)",
    "mechanism": "one continuous Naya 4 script sequence: comment → PATCH close → receipt",
    "bar": "11 minutes from error to public correction",
    "closure_reason": "SN-0236 one-repair-per-class (#1858 superset of #1857)"
  },
  "related": ["SN-0236"]
}
```

Intelligent Block
Truth state: CANDIDATE
Scope: PRIVATE
Captured date: 2026-10-22
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

The gap may be dead on arrival — the first move on any gap brief is a freshness check against the receipts dir; proving the gap is already closed IS the work. The lane-4 seat refused to spend a redundant live-fire (a PR + CI cycle + review saved). The filing-time fix: the filer must consult same-day receipts before filing — a writer-side contract like gap-t1182's.

## 🩷 HUMAN NOTE

On 2026-10-22 a gap brief was filed at 09:51Z for a gap that had been closed at 07:05Z the same morning by a different seat. The brief asked for a live-fire re-proof — a fresh PR, a CI run, a review. The lane-4 seat did the cheapest possible thing first: looked at that morning's receipts. The gap was dead on arrival — the closure proof (PR #2921, run 39736376559) already existed. Proving closure was the whole job; the seat saved the team a full redundant live-fire. The lesson has a named repair: the filer (file-gap-brief.py or the gap-scorer lane) should grep the last 24 hours of receipts for the named subject before writing the brief — consult the day's receipts before filing, the way gap-t1182's writer-side registration ended silent arrivals the same morning.

## 🟣 CHILD NOTE

Before you ask "where are my shoes?" look under the chair. Checking the easy places first IS the job — finding them under the chair means you don't have to search the whole house.

## 🔵 GRANDMA NOTE

Darling, before you write a letter asking where the parcel went, check the doorstep — it arrived this morning. Looking first is never wasted; asking second is never foolish. The waste is asking without looking.

## 🟠 NAYA NOTE

Gap briefs are claims about present-tense open work, and present-tense decays fast — same-day closure is the common case in a high-velocity system (here: 2h46m between close and stale filing). The triage order is: (1) freshness-check the receipts dir for the named subject, (2) if closed, re-derive/confirm the closure — that IS the work, (3) only if open, file the live-fire brief. The filer-side contract closes the class: a filing-time freshness check (grep the last 24h of receipts for the subject; refuse or refile on a match) — the writer-side fix pattern proven by gap-t1182 (writer self-registers, fail-closed; the sign-out checker then verifies instead of discovering), whose checker caught the old writer's 10th silent arrival (brief-gap-gap-t1002-lane1-lane1.md, 09:41Z) the same morning this class hit twice.

## 🟢 MACHINE NOTE

```json
{
  "sn": "SN-1815",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured_utc": "2026-10-22T10:48:00Z",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "category": "GOVERNANCE",
  "sub": "LANE-COORDINATION",
  "lesson": "The gap may be dead on arrival: the first move on any gap brief is a freshness check against the receipts dir, and proving the gap is already closed IS the work. Same-day closure is the common case in a high-velocity system. The named repair is a filing-time freshness check — the filer greps the last 24h of receipts for the named subject before writing the brief — a writer-side contract like gap-t1182's (writer self-registers fail-closed, checker verifies instead of discovering).",
  "decision_change": "The 'should I file this gap brief?' decision: check today's receipts first. If the gap is already closed, the work is re-deriving/confirming the closure — not filing a fresh live-fire. If filing is the job, the filer runs the 24h freshness grep before writing; a filing without it is incomplete.",
  "falsifiability": "This lesson breaks if a gap brief filed without a same-day freshness check lands a live-fire that finds the gap genuinely open and previously unworked — i.e., the skipped check would not have changed the filing. The morning's record is the control: the brief filed 09:51Z on a gap closed 07:05Z produced exactly one cost (the filing itself) and zero new evidence; re-derivation sufficed.",
  "mechanism": "Gap briefs name work; receipts name done work. The two disagree only through time — closure happens between filing and reading. A freshness check re-syncs the claim to present-tense before spending CI. Writer-side contracts (filing-time checks, fail-closed) beat checker-side catches (sign-out audits) because they prevent the spend rather than auditing it — the gap-t1182 pattern (writer self-registers, checker verifies) is the template.",
  "evidence": [
    "hidden_files/twelve-lane-receipts/gap-gap-lane-scorer-20261021-1920-lane4.md (2026-10-22): brief filed 09:51Z on a gap closed 07:05Z by t1238-lane3; seat refused the redundant live-fire, re-derived PR #2921 + run 39736376559 live — one PR + CI cycle + review saved",
    "hidden_files/learning-events-2026-10-22-10.md, CANDIDATE 802 (window ending 2026-10-22T10:20:19Z): same-day stale-filing pattern hit twice in one day; named repair: filing-time freshness check (grep last 24h of receipts for the named subject before writing the brief)"
  ],
  "cousins": [
    "SN-1804 (cold-successor seal needs both keys — writer-side contract pattern, different leg: brief retirement vs gap filing)",
    "gap-t1182 receipt / lesson-broadcast (writer-side self-registration for filed briefs, fail-closed — the named template for the filing-time freshness check; its checker caught the old writer's 10th silent arrival 09:41Z the same morning)"
  ],
  "applies_when": [["gap", "filing"], ["brief", "freshness"], ["dispatch", "triage"], ["lane-executor", "gap-claim"]],
  "enforcement": "file-gap-brief.py gains a filing-time freshness check: grep the last 24 hours of receipts for the named subject before writing the brief (the named repair in the receipt's Next action); on a match the brief is refused or refiled with the closure evidence. The sign-out checker run is the enforcement watch — it caught the old writer's 10th silent arrival (brief-gap-gap-t1002-lane1-lane1.md, 09:41Z) the same morning this class hit twice.",
  "dedupe_guard": "Not a duplicate: SN-1804 covers seal verification on brief retirement (mtime-after-seal + sha-of-cold-brief); gap-t1182 covers writer self-registration of filed briefs. This covers the triage-first ordering — freshness-check-before-file — and the same-day stale-filing class. Different leg of the filing pipeline."
}
```

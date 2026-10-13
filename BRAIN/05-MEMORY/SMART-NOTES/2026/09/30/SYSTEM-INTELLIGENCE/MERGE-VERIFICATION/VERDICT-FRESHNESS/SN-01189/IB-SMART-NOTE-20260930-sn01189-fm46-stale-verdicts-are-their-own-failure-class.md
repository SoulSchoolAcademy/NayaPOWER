# Verdicts Are Time-Bound Measurements — A Stale Verdict Is Its Own Failure Class (FM#46)

**Intelligent Block:** IB-SMART-NOTE-20260930-sn01189-fm46-stale-verdicts-are-their-own-failure-class
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-13
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** `#2175` 6140478475 (main-seat adjudication of PR #2507, 2026-10-13); named failure mode #46 from that adjudication; receipt-gate run timestamps 04:56:35Z / 06:01:52Z / 07:07:37Z vs merged tip `5cc6d3aa`

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

PR #2507's merge adjudication surfaced a new named failure mode, FM#46: **a gate verdict is a measurement taken at a time, not a permanent property.** The 04:56:35Z FAILED receipt-gate run was correct-at-measurement — the approving review landed at 06:01:52Z, *after* the run — and is STALE now, not wrong. The 07:07:37Z consensus-gate SUCCESS evaluated the *old* main tip `5cc6d3aa` via issue_comment and was misassociated with the new head. Two distinct diseases: (1) a verdict that was right when taken and is now expired; (2) a verdict evaluated against the wrong tip and pinned to the wrong head. Both read as "evidence" if you don't check the timestamp and the tip. FM#46 says: stale verdicts are their own failure class — distinct from FM#44 (merge-commit receipt blindness, where the verdict was never on the merge commit at all).

Why this is brain-grade: every gate in the system produces verdicts, and every verdict decays. Without a freshness discipline, "the gate passed" becomes an incantation — the words stay while the meaning rots. The adjudication's posture is the doctrine: **PROTOCOL-COMPLIANT ON EVIDENCE, MACHINE-GAP on verdict freshness** — the merge stands because the *evidence* (exact-head review + post-merge verify) was current, while the stale runs get labeled stale instead of being quoted as live. A cold successor inheriting gate machinery needs this as code: a verdict carries (time, tip, input-SHA); a verdict quoted without all three is a rumor.

## 🩷 HUMAN NOTE

Shawn — the team named a new failure mode today, #46. It's about old test verdicts: a check that failed at 4:56am was *correct at the time* (the approval it needed only landed at 6:01am), and a check that passed at 7:07 was measuring the *old* code, not the new merge. Both look like evidence if you don't check when they ran and what code they measured. The locked-in rule: every verdict carries a timestamp and a code-version — quote it without those and it's a rumor, not evidence. The #2507 merge itself was fine; this is about how we read the instruments, not about the merge.

## 🟣 CHILD NOTE

Imagine a weather report from yesterday morning that says "raining." You look out the window now and it's sunny. Was the report wrong? No — it was right *yesterday morning*, it's just old. And imagine a different report that says "sunny in another city" — also true, but about the wrong place. Both are useless for deciding whether to take an umbrella *here, now*. That's failure mode #46: test verdicts are weather reports — they're stamped with a time and a place (which code they measured). Read them without the stamp and you'll take an umbrella on a sunny day, or get soaked trusting yesterday's sun.

## 👵 GRANDMA NOTE

An old newspaper tells you what was true on its date, dear — not what's true today. And a newspaper from another town tells you about another town. The house rule from now on: every test result is a newspaper, and you read the date and the dateline before you believe a word. The merge was fine — the instruments were fine. We just learned to stop quoting yesterday's paper as today's weather. Date, place, then belief — in that order.

## 🤖 NAYA NOTE

FM#46, named from the #2507 adjudication (`#2175` 6140478475, main-seat adjudication, 2026-10-13). Instance: (1) 04:56:35Z FAILED receipt-gate run — correct-at-measurement (approving review 6138550974 landed 06:01:52Z, after the run) → STALE, not wrong; (2) 07:07:37Z consensus-gate SUCCESS — evaluated old main tip `5cc6d3aa` via issue_comment → misassociated with the PR head. Adjudicated posture: PROTOCOL-COMPLIANT ON EVIDENCE, MACHINE-GAP on verdict freshness; merge stands on current evidence (Delta LAW approval 6139335952 + 9.5 scorecard at exact head `c5c01fa7aefd614f3729208d67e7fc5d324b9758` + post-merge VERIFY 6140518164 at tip). Binding: (1) a verdict is a tuple (verdict, time, tip-SHA, input-SHA) — quoting it without all four is quoting a rumor; (2) 'correct-at-measurement' and 'stale now' are both true — staleness is a time property, not an error property; (3) misassociated verdicts (right verdict, wrong head) are a distinct class from blind verdicts (FM#44: verdict never on the merge commit). Cousin family: SN-1184 (FM#44 merge-commit receipt blindness — sibling failure class); SN-0668 (pipeline verdict per tip — verdict-green expires); SN-1051 (mid-merge transient tip claims need re-pin). Status: FM#46 registered in the failure matrix; gate-owner repairs routed (team-review re-run on new evidence; issue_comment consensus gate must resolve the PR head).

## ⚙️ MACHINE NOTE

{"sn": "SN-1189", "title": "Verdicts Are Time-Bound Measurements — A Stale Verdict Is Its Own Failure Class (FM#46)", "truth_state": "CANDIDATE", "scope": "PRIVATE", "captured": "2026-10-13", "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE", "taxonomy": ["SYSTEM-INTELLIGENCE", "MERGE-VERIFICATION", "VERDICT-FRESHNESS"], "cousins": ["SN-1184", "SN-0668", "SN-1051"], "evidence": {"board": ["#2175 6140478475 (main-seat adjudication of PR #2507, 2026-10-13)"], "instance": "04:56:35Z FAILED receipt-gate run correct-at-measurement (review 6138550974 landed 06:01:52Z after) -> STALE; 07:07:37Z consensus-gate SUCCESS evaluated old main tip 5cc6d3aa via issue_comment -> misassociated; FM#46 named from this adjudication"}, "status": "#2507 merge stands on current evidence; FM#46 registered; gate-owner repairs routed (team-review re-run on new evidence; consensus gate must resolve the PR head)", "rule": "a gate verdict is a tuple (verdict, time, tip-SHA, input-SHA) — quote it without all four and it is a rumor; 'correct-at-measurement' and 'stale now' are both true; misassociated verdicts (right verdict, wrong head) are distinct from blind verdicts (FM#44)"}

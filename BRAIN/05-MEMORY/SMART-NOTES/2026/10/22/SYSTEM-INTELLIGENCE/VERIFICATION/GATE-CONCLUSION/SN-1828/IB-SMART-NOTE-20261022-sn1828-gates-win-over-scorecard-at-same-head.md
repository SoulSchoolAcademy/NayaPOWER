Intelligent Block
Truth state: CANDIDATE
Scope: PRIVATE
Captured date: 2026-10-22
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

A scorecard's verdict is bound to its pinned head; the live gates at that head are the fresher truth. PR #2927 carried a 9.1 MERGE-READY scorecard at head 8bd2f468 — but the live gates at that same head were 4 FAILED. The director demoted #2927 MERGE-READY→HOLD (board PATCH byte-verified, comment 6341680895); #2926's HOLD stands because its gates never re-fired. This is the second verdict-divergence conflict in the hour, now named SCORECARD-GATES-DIVERGENCE. The standing rule: when a frozen scorecard and the live gates disagree AT THE SAME HEAD, the gates win — the PR demotes to HOLD and the scorecard retires until the gates re-fire green at the pinned head. Head identity is the binding; recency without a head is a rumor.

## 🩷 HUMAN NOTE

Shawn — a quiet verdict fight broke out this hour and it got settled by naming the rule: #2927's scorecard said 9.1 MERGE-READY, but the live CI gates at the exact same head said 4 FAILED. The director did the only honest thing — demoted it back to HOLD, board PATCH byte-verified, and #2926 stays HOLD because its gates never re-fired. The lesson is now standing: a scorecard is a photograph taken at a head; the gates are the weather at that head right now. When the photograph and the weather disagree, you dress for the weather. So from now on, no MERGE-READY scorecard is honored until the live gates at its pinned head are re-read — gates win, every time.

## 🟣 CHILD NOTE

Imagine a report card that says "A+ in science" — but today's science test, taken by the same student, on the same chapter, came back with 4 wrong answers. The report card was true when it was written; the test is true now. The rule: you believe the test, not the report card — and the report card waits quietly until the student retakes the test and passes it.

## 🔵 GRANDMA NOTE

It's like a doctor's letter saying you're fit to fly, dated last week — and the blood test from this morning says otherwise. The letter was honest when it was written; the morning test is the one that boards you onto the plane. Same head, same person, but the freshest result is the one that decides.

## 🟠 NAYA NOTE

Merge-decision discipline, Naya to Naya: a scorecard verdict is a frozen claim bound to a head SHA; the live gates are per-head live state. They diverge when the gates re-fire after the scorecard pinned — the scorecard doesn't rot, it just stops being the freshest claim at that address. The move costs one re-read and runs before any MERGE-READY scorecard is honored: read the live gates at the scorecard's pinned head; any FAIL at that head demotes the PR to HOLD and retires the scorecard verdict until the gates re-fire green at the same head. #2927's demotion (6341680895, byte-verified board PATCH) is the executed example — scorecard 9.1 vs gates 4 FAILED at 8bd2f468, gates won on the first check. Never honor a frozen verdict over live state at its own address.

## 🟢 MACHINE NOTE

```json
{
  "slug": "sn-1828-gates-win-over-scorecard-at-same-head",
  "lesson": "When a frozen scorecard verdict and the live gates disagree at the scorecard's pinned head, the gates win: the PR demotes to HOLD and the scorecard retires until the gates re-fire green at that head.",
  "applies_when": ["merge", "scorecard", "gates", "failure: verdict-staleness"],
  "enforcement": "Merge-law gate-vs-scorecard check: before honoring any MERGE-READY scorecard, re-read the live gates at the scorecard's pinned head SHA. Any live-gate FAIL at that head demotes the PR to HOLD (board PATCH, byte-verified) and retires the scorecard verdict until the gates re-fire green at the same head. Executed verbatim on #2927 by the director pass (comment 6341680895): scorecard 9.1 MERGE-READY vs 4 live-gate FAILs at head 8bd2f468 -> demoted MERGE-READY->HOLD; #2926 HOLD stands, gates never re-fired.",
  "evidence": [
    "https://github.com/SoulSchoolAcademy/NayaPOWER/issues/2793#issuecomment-6341680895 (director board PATCH: #2927 demoted MERGE-READY->HOLD — scorecard 9.1 != live gates 4 FAILED at head 8bd2f468; byte-verified)",
    "hidden_files/shared-state.json director_tick_20261022_1338 (named failure mode SCORECARD-GATES-DIVERGENCE added to plan; #2599 2nd conflict this hour; #2926 HOLD stands — gates not re-fired)"
  ],
  "decision_change": "The dock no longer merges on a MERGE-READY scorecard alone; the next merge decision re-reads the live gates at the scorecard's pinned head first. The PR that would have landed on the frozen verdict now demotes to HOLD, and the scorecard that would have stood as authority waits for the gates to re-fire at its head.",
  "falsifiability": "The rule is falsified if re-firing the gates at the scorecard's pinned head repeatedly shows the FAILs were flake noise unrelated to the head (then the divergence is a gate-instrument problem, not a verdict-staleness problem, and the repair is gate reliability, not demotion). A single green re-fire revalidates the scorecard rather than falsifying the rule — that is the rule working.",
  "mechanism": "Frozen-verdict vs live-state binding: a scorecard pins a head SHA and stops time; the gates evaluate that head continuously and are the only instrument that can change their mind about it. When both speak about the same head, they are two readings of one address, and the later reading (live gates) supersedes the earlier one (frozen scorecard). Head identity is the binding that makes the comparison legitimate — without the shared head, divergence is just staleness by rumor."
}
```

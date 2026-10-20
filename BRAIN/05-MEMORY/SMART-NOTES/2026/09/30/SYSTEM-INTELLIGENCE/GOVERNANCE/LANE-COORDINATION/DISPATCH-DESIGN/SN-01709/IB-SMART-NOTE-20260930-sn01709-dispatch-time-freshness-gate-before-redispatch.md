# Dispatch-Time Freshness Gate: Grep the Receipts Before You Re-Dispatch

**Intelligent Block:** IB-SMART-NOTE-20260930-sn01709-dispatch-time-freshness-gate-before-redispatch
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-19
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Captured on the 18:08 PDT distillation tick (2026-10-19) from hidden_files/learning-events-2026-10-20-00.md (violation-log: stale re-dispatch class, t0948) and hidden_files/twelve-lane-receipts/t0948-lane10.md. No new #1354 comments were read this tick (#1354 hit GitHub's 2500-comment hard cap 2026-10-10; director pass is the single reader).

## ✦ IN A NUTSHELL

The t0948 re-dispatch was issued at 23:44 UTC against a premise falsified by t0903's 23:42 UTC sign-out — a completion receipt closing this identical mission had landed ~2 minutes earlier. The dispatcher's dispatch-time view and the lane's run-time view disagreed by one run, and the re-dispatch's own drift narrative corrected itself against the wrong t0903. The durable rule: **before dispatching any re-dispatch brief, grep lane-feed.md and twelve-lane-receipts/ for a completion receipt on the same mission.** The receipt that closes the hole is already on disk; the gate is a five-second grep, not a judgment call.

Why this is brain-grade: view-time skew is a dispatcher-side failure that no lane-side rule ("already done triggers a byte check") can catch — the waste happens at dispatch, not at execution. One mechanical gate at dispatch time converts the whole stale-re-dispatch class into a no-op. This is distinct from SN-01374 (re-derive after a void kills a receipt) and SN-1097 (dispatch premises are hypotheses): the premise here was TRUE when the dispatcher last looked and FALSE at dispatch — only a dispatch-time freshness check closes that exact gap.

## 🩷 HUMAN NOTE

Shawn — small dispatch-design lesson from tonight's runs: the dispatcher re-issued a mission that had been closed two minutes earlier — the closing receipt was already sitting in the receipts folder when the re-dispatch went out. Nobody's fault; the dispatcher's view was just one run behind. The fix is mechanical: before any re-dispatch, grep the lane feed and receipts for a completion receipt on the same mission — a five-second check that kills this whole class of stale re-dispatches. Filed as Smart Note candidate SN-01709 with that check as its enforcement.

## 🟣 CHILD NOTE

The dispatcher is like a teacher handing out a worksheet. But a student already finished that worksheet two minutes ago and turned it in — the teacher just hadn't looked at the turn-in box yet. So the teacher handed out the same worksheet again. The fix: **always peek in the turn-in box before handing out a worksheet a second time.** If the finished one is there, you don't hand it out again. Five seconds of peeking saves a whole worksheet.

## 🔵 GRANDMA NOTE

Dear, sometimes the office sends a letter asking for a report, and the report is already sitting in the inbox, delivered two minutes before. The person sending the letter just hadn't checked the inbox. The wise office rule: **before you send a reminder letter, look in the inbox first.** The receipt is already there. Five seconds of looking saves everyone a pile of unnecessary work.

## 🟠 NAYA NOTE

Dispatcher seat: the dispatch-time view goes stale faster than you think — one completed run is enough to rot it. Never issue a re-dispatch brief without first grepping lane-feed.md and twelve-lane-receipts/ for a completion receipt on the same mission. The lane already has its own version of this ('already done' triggers a byte check) — this is your version, and yours fires earlier, before any lane burns a tick. The gate is mechanical, not discretionary: grep first, dispatch second. When the receipt is already on disk, the re-dispatch never leaves your hands.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "sn": "SN-01709",
  "title": "Dispatch-time freshness gate: grep the receipts before you re-dispatch",
  "captured_utc": "2026-10-20T01:08:00Z",
  "seat": "Naya Clarity Narzan",
  "applies_when": ["dispatch", "re-dispatch", "queue", "stale-brief"],
  "enforcement": "Dispatch-time freshness gate: before any re-dispatch brief leaves the dispatcher, grep hidden_files/lane-feed.md and hidden_files/twelve-lane-receipts/ for a completion receipt or sign-out closing the same mission. A hit = the re-dispatch is voided and never issued. Verification: the gate fires (re-dispatch suppressed) on the next re-dispatch-class event; a post-gate re-dispatch against completed work = gate failed, lesson falsified.",
  "evidence": {
    "learning_events": "hidden_files/learning-events-2026-10-20-00.md, violation-log: 'Stale re-dispatch class (first sighting, t0948): dispatched ~23:44Z against a premise falsified by t0903's 23:42Z sign-out; the dispatcher's dispatch-time view and the lane's run-time view disagreed by one run; the narrative itself was drifted (corrected against the FIRST t0903 while the SECOND had already answered). Owed machinery (dispatcher): dispatch-time freshness gate for re-dispatch briefs.'",
    "receipt": "hidden_files/twelve-lane-receipts/t0948-lane10.md: '2026-10-19 23:42 UTC, receipt t0903-lane10-askworld.md closed this exact hole at the source ~2 minutes before this claim (23:44 UTC).'",
    "context": "#1354 board fetch skipped this tick: issue_1354_comments=2500 = GitHub hard cap (commenting disabled 2026-10-10 per shared-state.json); watermark 6101230756 stands."
  },
  "cousins": ["SN-01374 (re-derive the task from live bytes before re-dispatch — voided-receipt class; this lesson is the dispatch-time-freshness class)", "SN-1097 (dispatch premises are hypotheses — dependency-existence class)", "oath standing rule 'already done triggers a byte check' (lane-side; this lesson is the dispatcher-side mirror)", "SN-01377 (retire stale claims pre-claim — claim-staleness class)"],
  "decision_change": "The dispatcher's decision whether to issue a re-dispatch brief: previously the decision used the dispatcher's dispatch-time view; after this lesson the decision is gated — grep lane-feed.md + twelve-lane-receipts/ for a same-mission completion receipt first, and a hit voids the re-dispatch before it leaves.",
  "mechanism": "View-time skew: the dispatcher's mental model of the world is built at view time, but completions land on disk continuously. Between view time and dispatch time, a completion receipt can arrive, flipping the re-dispatch premise from true to false. The grep reads the current disk truth at dispatch time, closing the skew window to seconds.",
  "falsifiability": "After the gate ships, a re-dispatch brief issued against a mission that already had a completion receipt on disk at dispatch time falsifies this lesson (the gate was either skipped or broken). If zero such re-dispatches occur across the next 30 days of dispatcher activity, the gate holds as the mechanism."
}
~~~

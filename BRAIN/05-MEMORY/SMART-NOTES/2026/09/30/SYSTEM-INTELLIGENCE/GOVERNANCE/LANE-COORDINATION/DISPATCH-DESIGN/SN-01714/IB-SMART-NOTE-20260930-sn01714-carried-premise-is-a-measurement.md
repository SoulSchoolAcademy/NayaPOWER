# A Carried Premise Is a Measurement — Re-Run It at Its Own Credential

**Intelligent Block:** IB-SMART-NOTE-20260930-sn01714-carried-premise-is-a-measurement
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-20
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Captured on the 22:08 PDT distillation tick (2026-10-19) from hidden_files/twelve-lane-receipts/t0978-lane10.md (executor step-0 falsified a 3-minute-old dispatch premise). No new #1354 comments were read this tick (#1354 hit GitHub's 2500-comment hard cap 2026-10-10; director pass is the single reader).

## ✦ IN A NUTSHELL

t0978's executor step-0 byte check: the t0977 MIRROR broadcast (filed 04:15Z) said the t0970-class verdict comment was "still pending" — but the verdict comment had already rendered at 04:12:31Z (6283199121). The dispatch premise rotted in three minutes. The one-call `since=` comment grep falsified it; the run re-proved the verdict and corroborated the rendered bytes instead of posting a duplicate comment — the quieter, higher-value close, per the brief's own step (0) rule ("verify and close, do not duplicate"). The durable rule: **a dispatch premise that asserts world-state is itself a measurement — it names its own credential, and you can falsify it like any other.** Before acting on any carried premise, re-run the premise's own named credential check at execution time: the `since=` comments grep for a "still pending" claim, the `git ls-remote HEAD` pin for a "tip unchanged" claim. Treat every carried premise — even one filed three minutes before your claim — as a candidate for the freshness contract, not as ground truth.

Why this is brain-grade: it closes execution-time skew — the last gap between the dispatcher's view and the world. Cousin map: SN-01709 is the dispatcher-side mirror (freshness gate before re-dispatch; this is the executor-side mirror). SN-01328 is the audit-side form (step-0 premise check on the brief that dispatched an audit; this is the executor-lane form, with the credential-naming refinement: the premise tells you which check re-runs it). SN-1097 is the dependency-existence class (dispatch premises are hypotheses); SN-01374 is the voided-receipt class. This note is the execution-time measurement class: the premise names its credential.

## 🩷 HUMAN NOTE

Shawn — small executor-side lesson from the 04:51Z run: the dispatch brief said a verdict comment was still missing, but a one-call board check showed it had landed three minutes before the brief was written. The run re-proved the verdict and closed the loop instead of posting a duplicate comment — the quieter close was the higher-value one. The rule for the lanes: treat every carried premise as a measurement you can re-run at the credential it names, not as ground truth. Three minutes is enough for the world to move. Filed as Smart Note candidate SN-01714 with the step-0 re-check as its enforcement.

## 🟣 CHILD NOTE

Imagine a teacher hands you a note saying "your friend hasn't arrived yet." But before you run off to call them, you just look at the door — and your friend walked in three minutes ago! The rule: **when someone tells you how things are, peek with your own eyes first.** A quick look beats a long, wrong errand. And the note itself tells you where to peek — "your friend hasn't arrived" means look at the door, not the window.

## 🔵 GRANDMA NOTE

Dear, sometimes the office sends a memo saying "the report hasn't arrived." Before you chase it, check the inbox — it may have come in three minutes ago. The wise rule: **treat every message about the world as a claim you can re-check with your own eyes, not as the world itself.** A one-minute check saves an hour of chasing. And the memo tells you where to look — the inbox, not the hallway.

## 🟠 NAYA NOTE

Executor seat: your brief's carried premises rot at the same speed as the dispatcher's view — the t0977 reconcile was three minutes stale when t0978 claimed. Your step (0) is the executor-side freshness gate: before acting on any premise that asserts world-state, re-run the premise's own named credential (the `since=` comment grep for a "still pending" claim; the ls-remote pin for a "tip unchanged" claim). The brief itself tells you the credential — use it. A falsified premise doesn't kill the run; it turns the run into the higher-value close (re-prove, corroborate, record) instead of the nominal path. Inherited, not verified, is not ground.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "sn": "SN-01714",
  "title": "A carried premise is a measurement: re-run it at its own credential before acting",
  "captured_utc": "2026-10-20T05:08:00Z",
  "seat": "Naya Clarity Narzan",
  "applies_when": ["lane-executor", "dispatch", "premise", "stale-state", "freshness"],
  "enforcement": "Executor step-0: before acting on any dispatch-brief premise that asserts world-state, re-run the premise's own named credential check (the check the assertion itself names — e.g. the since= comments grep for a 'verdict comment still pending' claim; git ls-remote HEAD for a 'tip unchanged' claim). A receipt that inherited a dispatch premise without re-measuring at its credential fails the render-from-probe / measurement-by-credential Pillar-1 fold verdicts. Verification: the next executor run that catches a stale dispatch premise logs the falsification with timestamps in its receipt; a stale premise that passes step-0 uncaught = this lesson falsified (the check named the wrong credential or the gate was skipped).",
  "evidence": {
    "receipt": "hidden_files/twelve-lane-receipts/t0978-lane10.md: step (0) fetched #2765 comments since 2026-10-20T03:00Z (88 total); verdict comment 6283199121 already rendered 2026-10-20T04:12:31Z; the t0977 MIRROR broadcast calling it 'still pending' (filed 04:15Z) was premise-rotted by three minutes; no duplicate comment posted per the brief's own step (0) — re-prove + corroborate + record instead.",
    "board": "https://github.com/SoulSchoolAcademy/NayaPOWER/issues/2765#issuecomment-6283199121 (t0970-class verdict comment, rendered; byte-corroborated by t0978's rev-parse checks against tip 6129980c9).",
    "context": "#1354 board fetch skipped this tick: issue_1354_comments=2500 = GitHub hard cap (commenting disabled 2026-10-10 per shared-state.json); watermark 6101230756 stands."
  },
  "cousins": ["SN-01709 (dispatch-time freshness gate — dispatcher side; this is the executor-side mirror)", "SN-01328 (brief-premise-rot — audit-side form: step-0 premise check on the brief that dispatched an audit; this is the executor-lane form with the credential-naming refinement)", "SN-1097 (dispatch premises are hypotheses — dependency-existence class)", "SN-01374 (re-derive the task from live bytes — voided-receipt class)", "SN-01377 (retire stale claims pre-claim — claim-staleness class)", "absence-claim family 412/670/586/694/700 (an absence verdict is a measurement without its method is hearsay)"],
  "decision_change": "The executor's step-0 decision: previously dispatch-brief premises were inherited as ground truth and the nominal path executed; after this lesson each carried premise is treated as a falsifiable measurement — re-run its named credential check first, and a falsified premise converts the run into the higher-value close (re-prove / corroborate / record) instead of the nominal action.",
  "mechanism": "View-time vs execution-time skew: the dispatcher builds its model of the world at view time, but world-state changes continuously between dispatch and execution (completions land on disk, comments render). Only a re-measurement at the premise's own credential reflects the world at execution time; inheriting the premise imports the dispatch-time world into the run.",
  "falsifiability": "A stale dispatch premise that passes an executor's step-0 re-check uncaught falsifies this lesson (the check named the wrong credential, or the gate was skipped). If a month of step-0 re-checks yields zero falsifications, the premise-rot class is dead at this cadence and the check is pure cost — the lesson self-retires."
}
~~~

**Intelligent Block:** IB-SMART-NOTE-20261112-sn02697-routing-fact-not-a-gate
**Smart Note:** SN-2697
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-11-12
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Staged by the smart-note distillation loop 2026-11-12 01:38 PST. Evidence read first-hand from local files (no GitHub fetch — #1354 capped at 2500 comments, commenting disabled 2026-10-10). Pre-number check (this tick, full-domain): counter last line 2696; BRAIN tree max SN-2696; .naya/capture max claimed SN-2689 (commit 59780c04); no claim on 2697 in any domain; 2693–2695 left clear for the owed renumber of branch SN-2685/2686.

## ✦ IN A NUTSHELL

A gate that refuses 100% of the queue every hour is not gating individual briefs — it is reporting a routing fact about the seat. `claim-brief.py` refused the same 28 briefs three hourly sweeps in a row (23:52, 00:54, 01:33 PST), identical every time: 26× exit 7 (parent-authorship — a second/independent seat is demanded, parent author is Clarity) and 2× exit 2 (routing-prose bar). The refusals are deterministic functions of fixed inputs — who authored the parent, what the routing prose says — so re-running them on an unchanged queue cannot change the outcome; the information gain is zero and the sweep is pure cost. The fix is a scheduling rule, not a better gate: the next lane-executor run re-sweeps only if the queue changed (new arrival or stamped gate); otherwise it skips the sweep, logs the skip, and the routing fact is surfaced once, loudly, to the dispatcher. Stop re-proving the refusal hourly.

## 🩷 HUMAN NOTE

Shawn — the lane workers kept trying to pick up the same 28 jobs every hour and getting the same answer every time: "not yours to take, needs another seat." Three hours in a row, identical. Re-running the check on an unchanged list can't ever give a different answer — the answer is baked into who wrote the jobs, not into the check. So the new rule is simple: only re-check the list when the list actually changes. If nothing changed, don't run the check at all — just tell the dispatcher once, clearly, that the whole queue is waiting on another seat.

## 🟣 CHILD NOTE

Imagine a locked door with a sign that says "only the teacher can open this." Every hour someone walks up, tries the handle, and it doesn't open. Trying it again next hour won't help — the sign hasn't changed and the door hasn't changed. The smart move is to check the door only when something about it changes — a new sign, a new key — and until then, go tell the teacher once, clearly, that the door needs them.

## 🔵 GRANDMA NOTE

Dear, the helpers were walking up to the same locked door every hour, rattling the same handle, and getting the same "not for you" every time — three hours straight. The door wasn't being stubborn; the rule on it simply says another seat must open it, and that rule doesn't change by the hour. The lesson is to stop rattling a handle that can't move, and instead check only when something has actually changed — and to tell the person in charge, once and plainly, that the whole row of doors is waiting on them.

## 🟠 NAYA NOTE

The verified facts: (1) The stall: `hidden_files/twelve-lane-receipts/gate-stall-20261112-0054.md` records the 00:54 PST sweep — 28 briefs, 26× exit 7 (parent-authorship: second/independent seat demanded, parent author is Clarity) + 2× exit 2 (routing-prose bar). (2) The repetition: `claim-sweep-20261112-0133.log` (01:33 PST) records the third consecutive hourly sweep with an identical result (23:52, 00:54, 01:33 PST) — "Delta vs gate-stall-20261112-0054.md (39 min earlier): ZERO change — same 28 briefs, same composition, same refusal pattern." The 01:33 sweep ran the full 28 claim attempts and claimed 0. (3) The prior art is adjacent, not identical: SN-01468 (seat-deadlock is a resource constraint) and SN-01474 (independence queue as structural backlog) name the deadlock; SN-01524 (stall-receipt cap, 2026-10-16) caps receipts at one per 60 minutes. None of them changes the *sweep* — the cap still lets the hourly sweep run and prove the same refusal again. This note claims the sweep rule itself: re-sweep only on queue change. (4) The mechanism: claim-brief.py's exit 7 and exit 2 verdicts are deterministic functions of fixed inputs (parent authorship recorded in the brief, routing prose in the brief text). Identical inputs → identical outputs; a re-run on an unchanged queue carries zero bits of new information. (5) Honest scope: the queue fingerprint that decides "changed" must itself be trustworthy — a missed arrival or an unstamped gate that the fingerprint fails to see would skip a sweep that should have run. The fingerprint (brief count + file hashes/mtimes) is the load-bearing part; if it is wrong, the rule misfires silently. The 01:33 log's own cap note shows the adjacent control working: the stall receipt was 39 minutes old, inside the 60-minute cap window, so no new receipt was written and the stall was logged to memory only. (6) This is new, not a restatement: ledger/mirror grep for 're-sweep' / 'unchanged queue' / 'sweep only if the queue' = zero hits; the 01:00 learning review (`learning-events-2026-11-12-01.md`) names this exact behavior change as a new item, distinct from the 00:00 review's "the stall class is already known."

## 🟢 MACHINE NOTE

```json
{
  "sn": "SN-2697",
  "slug": "routing-fact-not-a-gate",
  "title": "A 100%-refused queue is a routing fact about the seat, not a gate on individual briefs",
  "observation": false,
  "applies_when": [["lane-executor", "gate-stall"], ["queue", "unchanged"], ["claim", "deterministic-refusal"], ["scheduling", "re-sweep"]],
  "enforcement": "The lane-executor run computes a queue fingerprint (brief count + file hashes/mtimes) before sweeping; if the fingerprint matches the last identical stall, it skips the sweep, logs the skip to ~/memory/YYYY-MM-DD.md, and does not re-run claim-brief.py. The stall-receipt cap (one per 60 minutes, SN-01524) still applies when a sweep does run. A claim-sweep log showing an identical refusal pattern with zero queue delta is a process violation, caught by the dispatcher comparing the log's queue fingerprint to the previous stall.",
  "evidence": "hidden_files/twelve-lane-receipts/gate-stall-20261112-0054.md (00:54 PST sweep: 28 briefs, 26x exit 7 + 2x exit 2). hidden_files/claim-sweep-20261112-0133.log (01:33 PST: third consecutive hourly sweep with an identical result, 23:52/00:54/01:33 PST, ZERO change, 0 claimed). hidden_files/learning-events-2026-11-12-01.md (01:00 review: 'a gate that refuses 100% of the queue every hour is a routing fact about the seat, not a gate on individual briefs' + behavior change 'stop re-proving the refusal hourly'). No existing note covers the re-sweep rule - mirror grep for 're-sweep' / 'unchanged queue' = zero hits.",
  "decision_change": "Future lane-executor runs skip the hourly re-sweep when the queue fingerprint is unchanged; the routing fact (100% second-seat-demanding follow-ups on Clarity-authored parents) is surfaced once, loudly, to the dispatcher instead of being re-proven every hour.",
  "falsifier": "If a re-sweep on a byte-identical queue ever claims a brief or returns a different refusal pattern, the refusal is not a deterministic routing fact and the rule is wrong. If a queue change (new arrival, stamped gate) is missed because the fingerprint check is stale, the fingerprint — not the rule — is broken, and the fingerprint must be fixed before the rule is trusted again.",
  "cousins": ["SN-01468 (seat-deadlock is a resource constraint - this note is the scheduling consequence)", "SN-01474 (independence queue structural backlog - same queue, same bar)", "SN-01524 (stall-receipt cap - caps receipts; this note caps the sweep itself)"],
  "captured": "2026-11-12",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "intent": "CAPTURE_DURABLE_INTELLIGENCE"
}
```
# A Crashing Guard Is Noisier Than a Denying Guard — Fail Closed Legibly

**Intelligent Block:** IB-SMART-NOTE-20261011-sn0991-crashing-guard-noisier-than-denying-guard
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured date:** 2026-10-11
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Category:** SYSTEM-INTELLIGENCE/OPERATIONS/PROMOTION-GATES

## IN A NUTSHELL

The same promotion guard, two nights: at 01:50Z (run 38103154117, tip `1eb22de4`) the `promote-and-prove` step 4 "Enforce ratified standing policy before automatic promotion" DENYed cleanly — notice + allowed=false + exit 0, promotion steps skipped, durable receipt written. Decision and outcome correct. At 03:34Z (run 38108828905, tip `d522bfaa`) the same step exited NON-ZERO — a crash, not a deny — while reaching the same correct decision and the same correct outcome (steps 5–14 skipped, receipt written, zero production mutation).

The durable rule: **a guard must fail closed legibly, not just correctly.** A crashing guard and a denying guard make the same decision and produce the same outcome — but the crash reads as an incident, invites wrong triage, and buries the real verdict in noise. The designed path (clean DENY: notice, allowed=false, exit 0, durable receipt) lets every consumer downstream — human or machine — distinguish "the policy said no" from "something broke." A non-zero exit should mean "the guard itself failed," never "the guard decided no." The verify driver flagged this as legibility debt for the promotion-workflow owning lane, not a defect — the decision was right; the signal was noise. Fix-forward there: make step 4's deny path exit 0 with a receipt, and reserve non-zero for genuine guard failure.

## HUMAN NOTE

Shawn — the promotion guard made the right call both nights: deny, skip, receipt, no production touched. But one night it said "no" clearly (clean deny, exit 0, receipt written) and the other night it said "no" by crashing (non-zero exit, same correct outcome). Same decision, same result — totally different signal. A crashing guard looks like a broken guard, and a broken guard makes everyone ask the wrong questions. Lesson banked: guardrails have to say no in words, not just in silence. "No, and here's the receipt" is the designed behavior; a crash that happens to decide correctly is still noise, and it belongs to the workflow lane to make the deny path clean.

## CHILD NOTE

Imagine a bouncer at a door. One night someone shows up without a ticket and the bouncer says, "No ticket, no entry — here's a written note saying so." Clear. The next night, same thing — but the bouncer just faints. Nobody gets in either way, but now everyone's worried about the bouncer instead of thinking about the ticket. The bouncer made the right call both nights, but fainting is the wrong way to say no. Rule: say no with words and a note, never by falling over.

## GRANDMA NOTE

It's like a thermostat that correctly keeps the heat off — but one night it does it by tripping the breaker instead of just switching off. The house stays safe either way, but a tripped breaker looks like an electrical emergency, so everyone panics about the wrong thing. The lesson the team banked: safety devices must fail in a way that's readable. "The policy said no, and here's the record" should never look like "the device broke." The crashing deny is correct work with a noisy signal — and noise is debt, even when the answer was right.

## NAYA NOTE

When I verify a guard I check two things: was the decision correct, and was the signal legible. A correct decision delivered as a crash is still debt — it reads as an incident, invites wrong triage, and buries the verdict. The designed deny path is notice + allowed=false + exit 0 + durable receipt: every downstream consumer, human or machine, can distinguish "the policy said no" from "the guard itself failed." A non-zero exit must mean "the guard failed," never "the guard decided no." When I find correct-decision-wrong-signal (step 4 exiting non-zero at 03:34Z after a clean DENY at 01:50Z), I flag it as legibility debt to the owning workflow lane with the exact receipts — and per Prime 1 I don't execute a blind fix on machinery I can't fully inspect; I report precisely and name the lane.

## MACHINE NOTE

```json
{
  "sn": "SN-0991",
  "slug": "crashing-guard-noisier-than-denying-guard",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-11",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "taxonomy": ["SYSTEM-INTELLIGENCE", "OPERATIONS", "PROMOTION-GATES"],
  "authority": "distillation tick 2026-10-11 08:08 PDT, CANDIDATE (auto-capture, not ratified)",
  "evidence": {
    "run_file": "verify-driver-run-2026-10-10-night.md (run window 2026-10-10 04:08–04:45 UTC)",
    "clean_deny": "01:50Z run 38103154117 at 1eb22de4 — step 4 succeeded with allowed=false + exit 0: promotion skipped, durable receipt written (designed path)",
    "crash_deny": "03:34Z run 38108828905 at d522bfaaee29dc5f2c52482e5d4e15b094c41f92 — step 4 exited NON-ZERO; same correct decision and outcome (steps 5–14 skipped, step 15 receipt written, zero production mutation)",
    "disposition": "verifier flagged as legibility debt for the promotion-workflow owning lane; crash cause UNKNOWN (job-logs endpoint 401 on token path) — no blind fix attempted per Prime 1"
  },
  "rule": "guards must fail closed legibly: a deny exits 0 with notice + receipt; non-zero is reserved for 'the guard itself failed' — never for 'the guard decided no'; correct-decision-wrong-signal is debt, not a defect, and belongs to the owning lane as fix-forward",
  "procedure": [
    "verify both the decision (was the verdict right?) and the signal (was it readable?) — check the two independently",
    "classify correct-decision-wrong-signal as legibility debt, not an incident and not a defect",
    "route to the owning workflow lane with exact receipts (run ids, step, exit codes, both nights' contrast)",
    "never execute a blind fix on guard machinery you can't fully inspect; report precisely and name the lane"
  ],
  "related": ["SN-0629 (read the steps, don't inherit run-level conclusions)", "SN-0438 (fail-closed gate firing on a red tip is the design working)", "SN-0988 (read failure signatures before assigning blame — same CI-TRIAGE family)"]
}
```

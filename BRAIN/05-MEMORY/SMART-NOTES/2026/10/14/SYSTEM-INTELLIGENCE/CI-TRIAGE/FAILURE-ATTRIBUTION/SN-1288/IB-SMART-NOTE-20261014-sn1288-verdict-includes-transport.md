# IB-SMART-NOTE-20261014-sn1288

**Intelligent Block:** SN-1288
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured date:** 2026-10-14
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL

The verdict is a function of (head, body, transport-availability) — not (head, body) alone. t0748 (Lane 6, verdict-instability adjudication, 9.5/10): the team had been adjudicating "identical inputs, different verdict" as if the verdict depended only on the head and the body. The adjudication rule: every such claim must first check the API's answer in the FAILING run's log before touching the gate's logic. A 403 never seen in the log is a theory; a 403 quoted from the log is the root cause. In this case the claim gate's 403s were corroborated as rate-limit only by the sibling consensus log's explicit message — per-call headers would close the remaining ambiguity. Lesson: transport is an input. Quote the failure from the failing run, or drop the theory.

## HUMAN NOTE

Imagine a referee makes two different calls on two plays that look identical on video. The natural instinct is to blame the rulebook — rewrite the rule, study the rule. But if the referee's radio was cutting out on the second play, the problem wasn't the rule at all: a broken communication channel produced a different decision from the same rule. That's what happened here: a verdict that looked like "same inputs, different result" had a hidden third input — whether the API was reachable at that moment. The lesson: before you rewrite the rulebook, check the radio log from the exact play that went wrong. A theory about what happened ("maybe the API was down") is not evidence; a log line from the failing run is.

## CHILD NOTE

Imagine your teacher gives you a gold star on Monday but not on Tuesday for the exact same homework. You might think she changed her mind about what's good homework. But if you check Tuesday's note, it says "I was out sick and the substitute didn't know the rule." The answer wasn't in the homework or the rules — it was in Tuesday's note. Lesson: when the same work gets two different verdicts, read the note from the day it went wrong before you change anything else.

## GRANDMA NOTE

Dear, it's like calling the doctor's office twice with the same symptoms and getting two different answers. You'd be tempted to think the doctor changed her mind — but if you look at the call log, the second call dropped halfway through and you never heard the full answer. The missing piece wasn't your symptoms or the doctor's knowledge; it was the phone line. Same here: before anyone rewrites the rulebook over an inconsistent verdict, look at the connection log from the run that went wrong. A guess about the phone line is a guess; the call log is the answer.

## NAYA NOTE

For every Naya adjudicating "identical inputs, different verdict": the verdict function's signature includes transport-availability — the gate's logic evaluates against a remote API, so an inconsistent verdict across runs has three suspects (head, body, transport), not two. The t0748 case is the template: the claim gate's instability was adjudicated against (head, body) alone until the seat went to the FAILING run's own log; the 403s were corroborated as rate-limit only because the sibling consensus log carried the explicit message — a 403 never seen in the failing log would have stayed a theory. Two rules: (1) read the failing run's log for transport evidence (403/rate-limit/timeout) before touching the gate's logic — the log of the run that failed is the only transport evidence that counts; (2) when ambiguity remains, per-call headers (not sibling-run anecdotes) close it. Evidence: lesson-broadcast.md t0754 entry (dispatcher mirror, t0748-lane6 receipt, 9.5/10).

## MACHINE NOTE

```json
{
  "lesson_id": "SN-1288",
  "title": "the verdict is a function of (head, body, transport-availability) — quote the failing run's log or drop the theory",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-14",
  "category": "SYSTEM-INTELLIGENCE/CI-TRIAGE/FAILURE-ATTRIBUTION",
  "evidence": [
    "hidden_files/lesson-broadcast.md (t0754 entry): 'the verdict is a function of (head, body, transport-availability) — the team adjudicated as if it were a function of (head, body) alone. Every identical-inputs-different-verdict claim must first check the API's answer in the FAILING run's log before touching the gate's logic'",
    "same entry: 'A 403 never seen in the log is a theory; a 403 quoted from the log is the root cause. Transport is an input — the claim gate's 403s were corroborated as rate-limit only by the sibling consensus log's explicit message; per-call headers would close it'"
  ],
  "rule": "adjudicate verdict-instability in order: (1) read the failing run's own log for transport evidence (403/rate-limit/timeout) — only the failing run's log counts; (2) gate logic only after transport is ruled in or out",
  "anti_pattern": "citing a 403 from memory or a sibling run as the cause of THIS failing run; rewriting gate logic for a verdict instability whose failing log was never read",
  "related": ["SN-0892", "SN-0921"],
  "falsifier": "the procedure kills its own favorite hypothesis: if the failing log quotes no transport error, the transport theory dies there — per-call headers close the residual ambiguity that sibling anecdotes cannot",
  "decision_changed": "any 'identical inputs, different verdict' claim now starts from the failing run's log; a transport theory needs a quoted line from that log, never an assumption"
}
```

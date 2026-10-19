# Pin the Acceptance Checklist in the Receipt Body — the Next Verifier Shouldn't Re-Derive the Endpoint from Scratch

**Intelligent Block:** IB-SMART-NOTE-20260930-sn1678-pin-acceptance-checklist-in-receipt-body
**Smart Note:** SN-1678
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-19
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

A gap receipt that reports "claimed but not independently verified" is only half an instrument if the verifier's acceptance checklist lives in prose: the next verifier must re-derive the verification endpoint and the identity fields from scratch. gap-t0052-lane2 (2026-10-19) closed the t0052 gap by REST-verifying #2175 sign-in comment 6120247601 — id, author, issue, timestamp, body — and named the miss: those five fields should have been pinned in the parent receipt's own body. The rule: whenever a receipt says "claimed but not independently verified," pin the byte-level acceptance checklist (id, author, issue, timestamp, body-hash) in the receipt body. The next verification collapses from re-derivation to lookup.

## 🩷 HUMAN NOTE

If you write "I haven't verified this yet" in a report, write down what verifying would check: the ID, the author, the issue, the time, and the content's fingerprint. The person who comes next then only has to check your list — not reconstruct your whole hunt from the story.

## 🟣 CHILD NOTE

If you say "I didn't check the cookie jar," also leave a note: which jar, which shelf, what time. The next person shouldn't have to search the whole kitchen again.

## 🔵 GRANDMA NOTE

A promise to check something later is only useful if you write down what "checked" means — the five things to look for. Otherwise the note is a riddle, not a list.

## 🟠 NAYA NOTE

The concrete instance: the t0052 parent receipt (scored 9.0/10) carried the half-state "claimed but not independently verified." The gap lane (gap-t0052-lane2, 2026-10-19, 9.3/10) had to re-derive from scratch: the REST endpoint `/issues/comments/6120247601`, and the five identity fields — id 6120247601 byte-exact, author SoulSchoolAcademy (user id 221210320, OWNER), issue #2175, created_at 2026-10-12T08:05:38Z, full body text. The receipt's own mirror lesson: pin the byte-level acceptance checklist in the receipt body (id, author, issue, timestamp, body-hash) so the next verifier looks it up instead of re-deriving it. The checklist is the receipt's working set for the verifier — pinned in prose, grep-able, with the exact endpoint path. Enforcement: `receipt_checker.py` flags any gap receipt containing the claimed-not-verified phrase without the pinned 5-field checklist; the flag is a REJECT until the checklist is added.

## 🟢 MACHINE NOTE

~~~json
{
  "canonical_object": "INTELLIGENT_BLOCK",
  "sn": "SN-1678",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-19",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "automatic_truth_ceiling": "CANDIDATE",
  "authority_inheritance": false,
  "lesson": "a gap receipt that reports 'claimed but not independently verified' must pin the byte-level acceptance checklist (id, author, issue, timestamp, body-hash) in its own body; the next verifier then looks up instead of re-deriving the endpoint and identity fields from scratch",
  "decision_change": "any lane writing a gap receipt that says 'claimed but not independently verified' will pin the 5-field acceptance checklist (id, author, issue, timestamp, body-hash) plus the exact verification endpoint in the receipt body before sign-out",
  "falsifiability": "a verifier completes verification at equal or lower cost from a receipt that carries the claimed-not-verified phrase but NO pinned checklist than from one that pins it — observed parity would falsify the cost-reduction claim",
  "mechanism": "the verifier's cost is dominated by re-deriving the verification endpoint and the five identity fields from prose; the pinned checklist (exact fields, exact endpoint path) collapses re-derivation to lookup — the receipt body is the verifier's working set, and pinned identity fields are grep-able",
  "applies_when": [["gap","gap-receipt"], ["verify","claim-verification"], ["receipt","instrumentation"]],
  "enforcement": "hidden_files/receipt_checker.py flags any gap receipt whose body contains the claimed-not-verified phrase ('claimed but not independently verified' or equivalent) without a pinned 5-field checklist (id, author, issue, timestamp, body-hash); the flag is a REJECT until the checklist is added. Run on every gap receipt before sign-out.",
  "evidence": "hidden_files/twelve-lane-receipts/gap-t0052-lane2.md (2026-10-19, Lane 2 Sage hat, 9.3/10): mirror lesson 'should pin the byte-level acceptance checklist in its own body (id, author, issue, timestamp, body-hash) — I had to re-derive the REST endpoint and the five fields from scratch'; gh-api GET /issues/comments/6120247601 verified id/author/issue/timestamp byte-exact; dispatcher mirror night-dispatcher t0898 2026-10-19T15:07Z records the lesson"
}
~~~

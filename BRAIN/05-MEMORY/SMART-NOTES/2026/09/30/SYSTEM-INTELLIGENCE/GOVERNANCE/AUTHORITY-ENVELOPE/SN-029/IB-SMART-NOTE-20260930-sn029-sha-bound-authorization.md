# SHA-Bound Authorization — A Blocked Candidate Inherits Nothing

**Intelligent Block:** IB-SMART-NOTE-20260930-sn029-sha-bound-authorization
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-09-30
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Authorization binds to an (action, SHA, moment) triple — never to a branch, never to a previous authorization, never to "the head that was fine before." Every deployment packet is judged at its own exact SHA: the candidate that is blocked today does not inherit yesterday's authorization or the branch head's proof. Concrete case: the bounded parity baton (2026-09-30 ~21:45 PDT) prepared an exact-SHA deployment packet for current main `a726a837` — four migration hashes/bytes independently matched the canonical ledger, yet the verdict stayed blocked: the live DB still lacked `p_capabilities` and all three Value Calculus receipt functions, the standing-policy evaluator independently returned DENY (protected change requires explicit promotion), exact-main CI was UNKNOWN (API returned []), and Vercel reported a build rate limit. No production changes were made and no PASS was inferred from any of it. The packet, the evidence, and the next action were recorded for a successor — the blocked state was carried forward, not the permission.

## 🩷 HUMAN NOTE

This is the failure this kills: "we deployed before, it's probably still fine" — authorization as momentum. The baton's discipline is the opposite: authorization has a half-life of exactly one action. Each packet re-derives everything from the current SHA: migration hashes re-matched against the ledger, live-DB state re-checked (still missing `p_capabilities`), the standing-policy evaluator re-run (still DENY), CI state re-read — and when CI returned an empty result, that stayed UNKNOWN, never upgraded to PASS by wishful thinking. "One authorization is never standing authority." A cold Naya inheriting the baton must re-run the same gates against the same SHA; if the SHA moved, the whole evaluation moves with it. The point is not distrust — it's that authority which doesn't re-bind to evidence degrades into ritual.

## 🟣 CHILD NOTE

Imagine you get permission to go to the park on Saturday. That permission doesn't mean you can go to the park every day forever, or that your friend can go too. Each trip needs its own permission. In the same way, every change to the real system needs its own permission tied to the exact thing that's about to change — not the thing that changed last week. "You approved the change, not the harm" applies here too: even approval doesn't survive a changed situation.

## 🔵 GRANDMA NOTE

Permission for something important should be specific: this exact job, this exact version, right now. Yesterday's yes doesn't answer today's question. And when you're not sure about something — like whether the tests really passed — you say "I don't know," not "probably fine." Honest uncertainty is safer than comfortable guessing.

## 🟠 NAYA NOTE

This is the authority-plane twin of the clean-room protocol (SN-028). Clean-room pins the *subject* of verification; SHA-bound authorization pins the *authority* to the subject. Both follow from the same Prime: nothing floats. For the build/promotion lanes: every packet names its exact SHA, every gate re-runs against that SHA, DENY from the standing-policy evaluator is terminal for this packet (not a suggestion), and empty CI evidence stays UNKNOWN forever — the baton passes the evidence, not the clearance. For the Director: the rule makes his authority *more* precise, not weaker — his explicit word still gates every protected action, and this note says exactly what his word authorizes and what it does not.

## 🟢 MACHINE NOTE

```json
{
  "block": "IB-SMART-NOTE-20260930-sn029-sha-bound-authorization",
  "truth_state": "CANDIDATE",
  "captured": "2026-09-30",
  "evidence": {
    "case": "#554 comment 5924943513 (2026-10-01T04:47:56Z, bounded parity baton)",
    "packet_sha": "a726a8376559609a3620f948ec7bfcabdbba50abb",
    "verified": "four migration hashes/bytes independently match canonical ledger",
    "blocking_state": "live DB lacks p_capabilities and all three Value Calculus receipt functions",
    "policy": "standing-policy evaluator independently returns DENY / protected_change_requires_explicit_promotion",
    "ci": "exact-main CI UNKNOWN (API returns []); Vercel build rate limit; no PASS inferred",
    "doctrine_line": "Current blocked candidate must not inherit earlier authorization or branch-head proof",
    "outcome": "no production changes; packet + reproducible assumptions + successor next action recorded on issue 1182 (comment 5924941511)"
  },
  "rule": "authorization_binds_to_action_sha_moment_tuple",
  "protocol": [
    "derive_packet_from_exact_sha_at_packet_time",
    "re_run_every_gate_against_that_sha",
    "standing_policy_deny_is_terminal_not_advisory",
    "empty_ci_evidence_stays_unknown_never_upgraded_to_pass",
    "pass_the_evidence_not_the_clearance_to_successor",
    "earlier_authorization_never_survives_a_moved_sha"
  ],
  "twin_doctrine": "SN-028 clean-room verification (pins the subject); this note pins the authority",
  "constitutional_anchor": "protected gates remain the Director's explicit word; one authorization is never standing authority"
}
```

# IB-SMART-NOTE-20260930-sn01195-three-falsified-arms-new-mechanism-not-new-variant

| Field | Value |
|---|---|
| Intelligent Block | IB-SMART-NOTE-20260930-sn01195-three-falsified-arms-new-mechanism-not-new-variant |
| Smart Note | SN-01195 |
| Truth state | CANDIDATE |
| Scope | PRIVATE |
| Captured | 2026-10-13 |
| Canonical intent | CAPTURE_DURABLE_INTELLIGENCE |

## IN A NUTSHELL

Lane 5 (Naya Seeker) ran Arm E — sentence-embedding semantic retrieval (fastembed MiniLM-L6-v2) on the frozen t0555 fixture against the certified TF-IDF control — and proved an environmental block obsolete on the way in (t0601's "no torch/transformers" held: ~3s model load). E-VERDICT: FAIL — battery RED (P1 1/3, P2 holds); embedding coverage ranks lexical-surface docs (P1/P15/P2) high while human picks sit 8–16 deep. That makes three FALSIFIED/FAIL semantic arms, all dying on the same axis: coverage scores the surface, humans pick the deep. The three-try circuit breaker now applies to the whole family: stop running coverage variants — the next root must be a new mechanism, not a new coverage variant. Two post-seal harness-glue fixes named, mechanism byte-identical. Score 9.0/10.

## HUMAN NOTE

Shawn — the retrieval team's third semantic-search experiment failed, and the failure is the useful part: all three died the same way. The embedding approach keeps ranking documents that merely *look like* the question (shared surface words) while the documents humans actually pick sit much deeper in the results. Three strikes on the same failure pattern means the approach family is exhausted — the rule banked today: the next attempt has to change the *mechanism* (how it finds things), not just try another flavor of the same coverage idea. The lane also proved an old "the computer can't run this" limitation is gone — the model loads in about 3 seconds now. Honest work throughout: sealed before running, named its two post-seal fixes, no reruns, nothing shipped on a fail.

## CHILD NOTE

Imagine three kids try to find hidden treasure by digging in the sandbox — each digs in a different corner, but all three find nothing, because the treasure isn't in the sandbox at all. The smart move isn't to dig a fourth corner — it's to stop digging in the sandbox and try a completely different idea, like checking the toy box. Three tries in the same sandbox is enough; the fourth try has to be somewhere new. That's the rule the team wrote down today: three failures, same pattern, means change the plan — not the shovel.

## GRANDMA NOTE

The team tried three versions of the same search method, and all three failed the same way — they keep picking papers that share words with the question while the papers people actually want are buried deeper in the list. The standing rule they wrote down: three failures on the same pattern means the method itself is the problem, not the tuning. The next attempt must work differently, not just be adjusted. They also discovered an old "the computer can't do this" excuse no longer applies — the tool loads in seconds. All of it reported honestly: the experiment was sealed before testing, the two small fixes after sealing were named, and nothing was rerun to chase a better number.

## NAYA NOTE

Note to future me: the semantic arm family is now 3× FALSIFIED/FAIL on one axis — coverage ranks lexical surface (P1/P15/P2) while human picks sit 8–16 deep. Per the three-try circuit breaker, the family is CLOSED to coverage variants: any new retrieval proposal must name a genuinely different ROOT mechanism (a reframe, not new paint on the same wall) or stop. When scoring a new proposal, ask first: does it change how candidates are found and ranked, or does it re-weight the same coverage signal? If the latter, it's round four on a closed hypothesis — refuse it. Also banked: environment blocks expire — t0601's "no torch/transformers" was proven obsolete by a ~3s model load, so re-prove environmental impossibility claims before designing around them. And the honesty pattern holds: pre-reg sealed pre-run, RED-first calibration, post-seal fixes named with mechanism byte-identical, no reruns.

## MACHINE NOTE

```json
{
  "intelligent_block": "IB-SMART-NOTE-20260930-sn01195-three-falsified-arms-new-mechanism-not-new-variant",
  "smart_note": "SN-01195",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-13",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "lesson": "Three falsified arms on the same failure axis closes the family to variants: the semantic-arm family is 3x FALSIFIED/FAIL (coverage ranks lexical surface, humans pick deep) — the next root must be a new mechanism, not a new coverage variant.",
  "taxonomy": ["SYSTEM-INTELLIGENCE", "RETRIEVAL", "FALSIFICATION-DISCIPLINE"],
  "cousins": ["SN-01191", "SN-0495"],
  "evidence": {
    "memory_log": "~/memory/2026-10-13.md — 'Lane-executor run (t0633 + t0634)' entry",
    "receipt": "twelve-lane-receipts/t0634-lane5.md (Naya Seeker, 9.0/10 — Arm E sentence-embedding semantic arm)",
    "arm": "fastembed MiniLM-L6-v2 on frozen t0555 fixture vs certified TF-IDF control; 5/5 pins match; own pre-reg sealed pre-run; RED-first calibration",
    "verdict": "E-VERDICT FAIL — battery RED (P1 1/3, P2 holds); embedding coverage ranks lexical-surface docs (P1/P15/P2) high; human picks 8-16 deep; output 3c635e3c…",
    "family_record": "semantic arm family now 3 FALSIFIED/FAIL — all on the coverage-vs-depth axis",
    "environment": "t0601 'no torch/transformers' block proven obsolete (~3s model load)",
    "honesty": "two post-seal harness-glue fixes named, mechanism byte-identical; no reruns"
  },
  "rules": [
    "Three falsified arms on one failure axis closes the family: no more variants of the same mechanism.",
    "A new retrieval proposal must name a different ROOT mechanism (how candidates are found/ranked) — re-weighting the same coverage signal is round four on a closed hypothesis.",
    "Re-prove environmental impossibility claims before designing around them; blocks expire.",
    "Seal the pre-reg before the run; name post-seal fixes with byte-identical mechanism; never rerun to chase a verdict."
  ]
}
```

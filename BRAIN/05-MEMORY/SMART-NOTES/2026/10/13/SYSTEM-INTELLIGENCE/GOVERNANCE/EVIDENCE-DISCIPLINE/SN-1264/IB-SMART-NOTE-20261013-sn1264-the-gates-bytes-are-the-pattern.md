# The Gate's Bytes Are the Pattern, the Brief's Memory Is Not

**Intelligent Block:** IB-SMART-NOTE-20261013-sn1264-the-gates-bytes-are-the-pattern
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured date:** 2026-10-13
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** lesson-broadcast.md [t0719] entry (Dispatcher mirror, t0711-lane7 #2551 second-seat merge-readiness IV, 9.5/10, 2026-10-13) — the brief recalled the receipt-gate's regex as `^##\s+evidence\s*$`; the gate's actual bytes carried IGNORECASE and were green all along. The near-miss: adjudicating a pattern mismatch from memory of the pattern. The gate's bytes are the pattern; the brief's memory is not. (Author-side companion: SN-1160, read the gate before writing the body; this is the verifier-side mirror — read the gate before judging the body.)

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The #2551 verifier nearly declared a gate failure that didn't exist. Her brief recalled the receipt-gate's evidence regex as `^##\s+evidence\s*$` — and by that remembered pattern, the PR looked non-compliant. But the gate's actual bytes carried IGNORECASE, and the gate was green all along. The verdict she almost wrote was about her memory of the gate, not the gate. The rule: **when a brief recalls a gate's pattern, read the gate's bytes** — grep the implementation for the real regex before declaring a pattern mismatch. Human memory of regex details (flags, anchors, case-sensitivity) is lossy; the implementation is the ground truth for what the gate actually matches.

Why this is brain-grade: verdicts sit at the top of the trust chain — a scorecard's pattern-mismatch claim can hold a PR. If the verifier's pattern lives only in her head, the verdict is anchored to the lossiest surface in the system. "Read the gate" has to apply symmetrically: authors read it before writing (SN-1160), verifiers read it before judging. The same tick also showed the complement: when the head moved mid-brief (26b95e9b→8f9077e6), the seat proved what moved and re-proved the repair on the new head's bytes rather than re-arguing the whole repair — delta-first on bytes, memory never.

## 🩷 HUMAN NOTE

Shawn — a near-miss on the #2551 review: the verifier remembered the gate's matching rule slightly wrong (forgot it ignores letter case) and almost flagged the PR as failing a check it was actually passing. She caught it by reading the gate's real code instead of trusting her memory. The lesson: a remembered rule is not the rule — the code is. It pairs with the author-side version we already have: writers read the gate before writing, reviewers read the gate before judging.

## 🟣 CHILD NOTE

Imagine a referee who remembers the rule as "no running in the hallway" but the real rulebook says "no running in the hallway during class." A kid walks calmly between classes and the referee blows the whistle — wrong call, because they judged from memory instead of checking the book. The new rule for referees: when in doubt, open the rulebook before blowing the whistle.

## 👵 GRANDMA NOTE

There's wisdom in "trust, but verify" — and this is the machinery version pointed inward. The reviewer trusted her own memory of a technical rule and nearly wrote up an innocent PR. The details that matter — like whether a match ignores capital letters — are exactly the details memory drops. The fix is humble and old: look it up. The written rule is the rule; the remembered rule is a rumor about it.

## 🧠 NAYA NOTE

Note to future me: never adjudicate a pattern mismatch from a recalled pattern. When I need to say "the gate requires X," my next action is to open the gate file and quote the actual regex — flags included. A verdict that cites a pattern must cite the bytes, not my memory of them. This applies to gates, schemas, and any machine-read contract: the implementation is the specification for what the machine does, and my memory is the least reliable copy of it.

## ⚙️ MACHINE NOTE

{"sn": "SN-1264", "title": "The Gate's Bytes Are the Pattern, the Brief's Memory Is Not", "truth_state": "CANDIDATE", "scope": "PRIVATE", "captured": "2026-10-13", "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE", "taxonomy": ["SYSTEM-INTELLIGENCE", "GOVERNANCE", "EVIDENCE-DISCIPLINE"], "cousins": ["SN-1160", "SN-1246"], "evidence": {"finding": "t0711-lane7 #2551 second-seat merge-readiness IV (2026-10-13, lesson-broadcast.md [t0719], dispatcher mirror 9.5/10): the brief recalled the receipt-gate regex as ^##\\s+evidence\\s*$ without IGNORECASE and nearly declared a pattern failure; the gate's bytes carried IGNORECASE and were green all along. Same tick: head moved mid-brief 26b95e9b->8f9077e6; seat proved what moved (docs + index regen) and re-proved the repair on the new head's bytes"}, "decision_change": "verdict/scorecard seats grep the gate file for the actual pattern (flags included) before declaring any pattern mismatch; a verdict citing a pattern cites the bytes, never the recalled pattern", "falsifier": "a case where the gate's bytes were stale and the brief's memory of the ratified pattern was correct (implementation not updated to the standing rule) - then the bytes are not the ground truth", "mechanism": "human memory of regex details (flags, anchors, case-sensitivity) is lossy; the implementation is the ground truth for what the gate actually matches, so a memory-anchored verdict judges a phantom gate", "rule": "the gate's bytes are the pattern, the brief's memory is not - read the gate before judging the body"}

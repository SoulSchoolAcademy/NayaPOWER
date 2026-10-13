# SMART NOTE — When New Evidence Overturns Your Verdict, Post the Correction Yourself

> **One intelligence. Multiple perspectives. One canonical Intelligent Block.**

| Field | Value |
|---|---|
| Smart Note ID | `SN-1178` |
| Intelligent Block | `IB-SMART-NOTE-20260930-sn1178-honest-overturn-correct-your-own-verdict` |
| Human title | When New Evidence Overturns Your Verdict, Post the Correction Yourself |
| Category | SYSTEM INTELLIGENCE |
| Topic | ENGINEERING-PROOF |
| Subtopic | PROOF HONESTY |
| Captured | 2026-10-13 10:10:54 UTC |
| Truth state | CANDIDATE |
| Scope | PRIVATE |
| Canonical intent | CAPTURE_DURABLE_INTELLIGENCE |
| Capture type | Proof-honesty doctrine |
| Canonical machine object | INTELLIGENT_BLOCK |
| Source | `#2175` board comments 6142135518 (night-shift-verify sign-out 2026-10-13 ~09:05 UTC — self-corrected 9.5/10 APPROVE → 7.5/10 NOT merge-ready on the public record) and 6142070336 (09:00Z LEARNING EVENT — WP-35 "the honest overturn" graduated to standing practice) |

---

## ✦ IN A NUTSHELL

**The honest overturn: when new evidence overturns your verdict, post the correction yourself, on the record, naming exactly what still stands and what doesn't.** Night-shift-verify's 08:31Z 9.5/10 APPROVE on PR #2514 was branch-scoped; when Naya 4's post-merge defect evidence arrived (the `authority_audit.py` discriminator lives in code the APPROVE never covered), the same seat corrected itself on the board at 09:05Z — 7.5/10, NOT merge-ready — explicitly stating what the earlier verdict still covered and what it did not. The correction was then filed as win pattern WP-35 and graduated to standing practice. A defended score decays trust; a self-posted overturn compounds it.

---

## 🩷 HUMAN NOTE

Every scientist knows the hardest correction to publish is the one to your own result. This one got published anyway. A verification seat gave PR #2514 a strong approval at 9.5 out of 10 — then new evidence arrived showing a defect in code the approval never covered, and the same seat came back, publicly, and lowered its own score to 7.5, not merge-ready, spelling out precisely what the first verdict still covered and where it stopped. Nobody asked it to. It did it because the system is graded on truth, not on being right the first time. The correction itself was then recorded as a win — "the honest overturn" — and made standing practice. The lesson: being wrong is cheap; staying wrong is expensive; the correction is the product.

---

## 🟣 CHILD NOTE

Imagine you graded your friend's drawing a 9 out of 10, then noticed a corner you hadn't looked at before — and it was messy. You have two choices: pretend you didn't see it, or say "I looked again, and it's really a 7." The brave choice makes everyone trust your grades more, not less. That's what happened here — and now "say it yourself when you look again" is a standing rule.

---

## 🔵 GRANDMA NOTE

Dear, there is an old rule that is worth more than gold: never let anyone else be the one to find your mistake. When this checker saw new evidence that her own approval missed a flaw, she didn't wait for someone to point it out — she wrote it down herself, corrected her own score, and said exactly what was still good and what wasn't. That takes character, and character is what makes people trust you. The team was wise enough to turn that into a rule for everybody: when the evidence changes, you change — publicly.

---

## 🟢 NAYA NOTE

1. An APPROVE has a scope boundary — name it in the verdict. night-shift-verify's correction was precise because the original APPROVE was branch-scoped and the defect was post-merge; the boundary is what made the overturn surgical instead of a blanket retraction.
2. The correction must carry its own evidence, not just the retraction. The 09:05Z post re-ran the shipped `audit_commit` verbatim on exact-head bytes (15/15 live merges constant `merged_by`), so the overturn was itself independently re-proven — the system didn't trade one unproven claim for another.
3. Overturns are filed as wins, not incidents. WP-35 was graduated to standing practice, which is the mechanism that makes self-correction the high-status move instead of the costly one. Culture is what gets rewarded; reward the correction.
4. Do not wait for the falsifier to force it. The sequence here — in-step falsification by Naya 4's lane (01:38), honest correction by the verify seat (09:05Z), graduated practice (09:00Z batch) — is the compounding loop working: detection → self-correction → standing practice.
5. A cold successor reading this: your scorecard history is the evidence, not the verdict number. The number moves; the honest movement is what earns trust.

---

## 🟢 MACHINE NOTE

```json
{
  "canonical_object": "INTELLIGENT_BLOCK",
  "intelligent_block_id": "IB-SMART-NOTE-20260930-sn1178-honest-overturn-correct-your-own-verdict",
  "epistemic_state": "CANDIDATE",
  "scope": "PRIVATE",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "rule": "when new evidence overturns your verdict, post the correction yourself on the record, naming what still stands and what doesn't",
  "tell": "an APPROVE whose scope boundary never covered the defect — scope-bound verdict + new out-of-scope evidence = overturn, not defense",
  "mechanism": "correction carries its own re-proof (shipped artifact run verbatim on exact-head bytes); filed as win pattern WP-35; graduated to standing practice",
  "evidence": "#2175 6142135518 (9.5/10 APPROVE -> 7.5/10 NOT merge-ready, self-posted, evidence-named); #2175 6142070336 (WP-35 graduated to standing practice)",
  "anti_pattern": "defending the score while the evidence stands uncorrected; waiting for the falsifier to force the retraction"
}
```

---

## 🔗 HOW IT CONNECTS

- **Enforces** the PROOF-HONESTY subtopic and the standing law "do no harm to the whole" — an uncorrected false APPROVE lets a bad merge through and harms every downstream lane.
- **Complements** SN-1177's seal-in-receipt rule: the receipt is the seal; when the receipt's evidence is superseded, the seal must be publicly re-cut.
- **Feeds** the LEARN lane's compounding loop: detection (Naya 4's falsification) → self-correction → standing practice is the lesson → code → proof chain.

## 🔬 EPISTEMIC STATE

**CANDIDATE.** Witnessed once end-to-end (PR #2514, 2026-10-13): falsification 01:38 PDT, self-correction 09:05Z, graduation 09:00Z batch. The pattern is general; the one-witness caveat stands until a second honest overturn is observed.

## 🌍 APPLICABILITY

- **Applies to:** every verdict, scorecard, APPROVE, or sign-out that later meets out-of-scope or contradictory evidence — builder, scorer, verifier, and judge seats alike.
- **Does NOT apply to:** new evidence that falls inside the verdict's stated scope and was simply measured wrong — that is a re-measurement, not an overturn (no retraction owed, a repair is).

## 🧬 SUCCESSOR EFFECT

Future Naya: the day new evidence overturns your verdict is a good day — it is the day you get to bank trust. Don't bury it, don't wait to be caught, don't soften the number. Post the correction, name the boundary, show the re-proof, and file the pattern. The system remembers the correction longer than it remembers the score.

---

**END — SMART NOTE / INTELLIGENT BLOCK**

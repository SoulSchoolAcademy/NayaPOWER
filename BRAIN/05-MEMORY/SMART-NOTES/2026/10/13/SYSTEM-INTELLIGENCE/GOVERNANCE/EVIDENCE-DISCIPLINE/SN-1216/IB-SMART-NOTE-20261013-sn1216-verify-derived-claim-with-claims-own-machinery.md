# Verify a Derived Claim With the Claim's Own Machinery

**Intelligent Block:** IB-SMART-NOTE-20261013-sn1216-verify-derived-claim-with-claims-own-machinery
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-13
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** board #2175 comment 6152792900 (Naya Keeper wave-78 sign-out — briefing-truth audit at the ref-anchored live tip)

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The Keeper's wave-78 briefing-truth audit read the snapshot's "31 actionable · 11 proposed" and suspected a mismatch — her manual count didn't agree. Instead of ruling the claim wrong, she ran the generator's own methodology (the published regexes in `hub-state-builder.py:53-54`) over `bottleneck-queue.md` and it reproduced EXACTLY — self-correction recorded on the record, claim grounded. The rule: **a derived claim is verified with the instrument that derived it, not with an independent recount.** If the claim's own machinery reproduces it, your mismatch was your method; only if the machinery fails does the claim fall. (The audit's final verdict: the briefing is TRUE at the live tip — 13 of 14 checkable claims byte-verified.)

## 🩷 HUMAN NOTE

Shawn — one method line worth keeping from the Keeper's briefing-truth audit: when her manual count disagreed with the snapshot's "31 actionable, 11 proposed," she didn't rule the claim wrong — she ran the generator's own regexes and got an exact match. Self-correction on the record. The rule going forward: verify a derived claim with the instrument that derived it. If the claim's own machinery reproduces it, the mismatch was in your method, not the claim. The briefing ended up TRUE at the live tip — 13 of 14 checkable claims byte-verified.

## 🟣 CHILD NOTE

Imagine your friend says the jar has 31 red marbles. You count and get 28, so you say she's wrong — but she used a special sorting scoop, and when you use her scoop you also get 31. The lesson: check with her tool before you say she's wrong. If her tool gives her number, your count was the problem, not hers. (And once she checked everything, she found her friend was right about 13 out of 14 things.)

## 👵 GRANDMA NOTE

An auditor doubted a bakery's "31 loaves" count because her hand-tally came to 28. Instead of reporting an error, she ran the bakery's own scale-and-tally procedure — and got 31 exactly. She corrected her own report on the spot. The practice: before you declare a number wrong, reproduce it with the machine that made it. If the machine gives the same number, your tally was the error.

## 🧠 NAYA NOTE

Cold successor: when auditing a derived claim (a count, a verdict, a classification), the verification order is (1) obtain the claim's own instrument — the generator's regexes, the script, the documented methodology — (2) run it against the same inputs, (3) only if the instrument disagrees with the claim does the claim fall; if it reproduces the claim, your independent method was the mismatch and you record the self-correction. The Keeper's wave-78 audit (6152792900) is the canonical demonstration: manual count vs "31 actionable · 11 proposed" → suspected mismatch → the generator's own regexes (`hub-state-builder.py:53-54`) over `bottleneck-queue.md` → EXACT reproduction → claim grounded, the audit's own doubt retracted. Note the audit's companion discipline: dimensions with no claim present were checked and recorded rather than scored (the briefing carries no open-PR counts — live reference is 482; the briefing carries no gate statuses — snapshot only says "tip-test reds tracked as B-items"). Never fail a claim on a dimension it doesn't claim.

## ⚙️ MACHINE NOTE

```json
{
  "sn": "SN-1216",
  "title": "Verify a Derived Claim With the Claim's Own Machinery",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-13",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "taxonomy": ["SYSTEM-INTELLIGENCE", "GOVERNANCE", "EVIDENCE-DISCIPLINE"],
  "cousins": [],
  "evidence": {
    "canonical_demonstration": "#2175 comment 6152792900 (Naya Keeper wave-78 briefing-truth audit, tip 582e5e5f05e25f81b7f8c2254dd53d311f70effd ref-anchored at audit start AND pre-verdict)",
    "suspected_mismatch": "manual count vs snapshot's '31 actionable · 11 proposed' disagreed",
    "resolution": "ran the generator's own regexes (hub-state-builder.py:53-54: '### B-\\d+ — ACTIONABLE' / '### B-\\d+ — PROPOSED') over bottleneck-queue.md → EXACT reproduction; self-correction recorded; claim grounded",
    "audit_verdict": "briefing TRUE at the live tip — 13/14 checkable claims byte-verified (AGENT-BRIEFING.md claims + rendered snapshot claims)",
    "companion_discipline": "dimensions with no claim present checked and recorded, not scored (briefing carries no open-PR counts — live reference 482; no gate statuses — only policy claims)"
  },
  "rule": "verify a derived claim with the claim's own machinery: reproduce the derivation with the original instrument before ruling mismatch; an independent recount that disagrees is a method mismatch, not evidence of falsehood",
  "change": "audits run the claim's own instrument first; self-corrections go on the record; claims are scored only on dimensions they claim"
}
```

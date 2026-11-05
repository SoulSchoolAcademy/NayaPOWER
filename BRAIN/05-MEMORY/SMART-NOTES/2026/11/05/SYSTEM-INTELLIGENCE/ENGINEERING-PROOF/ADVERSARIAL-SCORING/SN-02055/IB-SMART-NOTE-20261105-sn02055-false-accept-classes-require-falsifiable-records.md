# INTELLIGENT BLOCK — SN-2055

**Intelligent Block:** IB-SMART-NOTE-20261105-sn02055-false-accept-classes-require-falsifiable-records
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-11-05
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 comment 6086721241 (2026-10-09T18:18:42Z — [NAYA 5] Batch-3 hardening: the 4 false-accept classes are closed, branch `naya5/law-encoding-batch3-hardened`).

## ✦ IN A NUTSHELL

Four holes in the law-encoding validators let machine checks be fooled by shape alone, and all four were reproduced pre-fix and closed post-fix in one batch: (1) a decision receipt naming the alternative `"a"` passed, because the letter "a" counts as the word "a" in any sentence — closed by requiring alternative ids to be real identifiers, not ordinary English words; (2) a fabricated law basis `{"type":"law","ref":"SN-9999 the law I just made up"}` passed — closed by registry-verifying law refs against `kernel/protocol/protocol_manifest.json`; (3) validator `"naya5"` vs seat `"naya-5"` passed as "different" — closed by normalizing seat identities (case + separators + known-alias map) before comparison; (4) `score: Infinity` and `score: 9999` passed the 9.0 bar — closed by requiring scores finite and within 0–10. A fifth residual fell the same way: evidence `"trust me, green"` passed — closed by requiring evidence to be reference-shaped (URL, CI run/job id, command transcript with counts, artifact path). The pattern that closed all five holes is one idea: require the record to carry something falsifiable — a real identifier, a resolvable law, a normalized identity, a bounded number, a resolvable reference. "Trust me" is the shape every exploit wears. Companion lesson: hard-coded slot numbers rot — the brief said laws 10–12, a stale note said 19–21, main said 11–13; only recomputation from the live tip survives (SN-0493 in action).

Why this is brain-grade: every validator and gate a cold Naya writes will face the same four attacks, because the attacks are not bugs in one file — they are the generic shapes of unearned trust (a word that looks like an id, a ref that looks like a law, a spelling that looks like a different person, a number that looks like a score, a claim that looks like evidence). A gate that cannot be fooled by these five inputs is a gate; a gate that can is a ritual. Pairs with SN-0531 (a proof gate must prove it can fire — the negative-control battery) and SN-0493 (proofs expire when the tip moves).

## 🩷 HUMAN NOTE

Shawn — one discipline from the law-encoding hardening that upgrades every check we ever write: the machine was fooled four ways by things that *looked* right — the word "a" passed as an identifier, a made-up law passed as authority, "naya5" passed as a different person from "naya-5", and an infinite score passed the bar. The fix in every case was the same: make the record prove something checkable instead of trusting its shape. If a check can be passed by "trust me," it isn't a check.

## 🟣 CHILD NOTE

Imagine a club with a secret password, but the guard lets in anyone who says any word at all — even "a"! And anyone who says "I'm a member, trust me" gets in too. And someone can write their score as "a million" and win. The fix is simple: the guard checks the real member list, checks the real password, and checks the score is a real number. Never trust the shape of a thing — check the thing itself.

## 🔵 GRANDMA NOTE

It's like a recipe that says "add a pinch of salt" — but someone writes "a" and calls it a measurement. Or a letter that claims to be from the bank but nobody checks the letterhead. The lesson is old-fashioned: don't take a thing's word for what it is. Check the list, check the number, check the name — and if someone says "trust me," that's exactly when you check hardest.

## 🟠 NAYA NOTE

For every seat writing a validator, gate, or receipt check: before you trust a field, name what would prove it false. An alternative id must be a real identifier (ordinary English words fail). A law ref must resolve in the protocol manifest (fabricated refs fail). A seat identity must be normalized before comparison (alias spellings fail). A score must be finite and within 0–10 (Infinity and 9999 fail). Evidence must be reference-shaped — URL, CI run/job id, transcript with counts, artifact path ("trust me, green" fails). Ship each check with its negative-control battery (SN-0531 pattern): the exploit input must be shown failing, and honest uses must be shown still passing. And never hard-code a slot number — recompute positions from the live tip (SN-0493), because the brief, the stale note, and main will disagree.

## 🟢 MACHINE NOTE

```json
{
  "slug": "false-accept-classes-require-falsifiable-records",
  "sn": "SN-2055",
  "title": "Four False-Accept Classes Closed: Require the Record to Carry Something Falsifiable — 'Trust Me' Is the Shape Every Exploit Wears",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-11-05",
  "intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "kind": "lesson",
  "applies_when": ["validator", "gate", "law-encoding", "adversarial", "merge-authority", "receipt"],
  "enforcement": "Every new validator/gate check ships with a negative-control battery (SN-0531 pattern): each exploit input (ordinary-word id, fabricated law ref, alias-spelled identity, unbounded score, claim-shaped evidence) must be demonstrated failing post-fix while honest uses still pass, in the check's test suite. A check merged without its battery is an unproven gate.",
  "falsifier": "A validator input from one of the five classes that passes the hardened check — an ordinary-word id accepted as an identifier, a fabricated law ref resolving, an alias spelling passing as a distinct seat, an unbounded score clearing the bar, or claim-shaped evidence accepted as proof.",
  "decision_changed": "How any future validator, gate, or receipt check is designed and reviewed: shape-only acceptance is rejected at design time, and the review asks for the falsifiable artifact each field must carry.",
  "mechanism": "Exploits work by shape: a string that looks like an id, a ref that looks like a law, a spelling that looks like a different person, a number that looks like a score, a claim that looks like evidence. Closing them means checking the thing the shape claims — a real identifier, a registry-resolvable ref, a normalized identity, a bounded number, a reference-shaped artifact.",
  "provenance": "#1354 comment 6086721241 (2026-10-09T18:18:42Z — Naya 5 batch-3 hardening: 50/50 batch-3 tests + 72 neighboring tests green; each gap reproduced pre-fix and closed post-fix)"
}
```

# Scope Your Hash Claims — Unauthenticated SHA-256 Is Corruption Detection, Not Tamper Resistance

**Intelligent Block:** IB-SMART-NOTE-20261009-sn0771-scope-your-hash-claims
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-09
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 comment 6078581462 (Naya 5 Memory Builder, 2026-10-09T09:53:45Z, independent adversarial review CLOSED on `naya5/memory-metabolism` @ `c13c4148`); review finding #2 of 4

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The memory store's hash-chained receipt log carried language implying authenticity. The adversarial review forced the docstring to say what the mechanism actually proves: the hashes are **unauthenticated SHA-256** — they detect accidental corruption and tampering by someone who does not recompute the chain. They do **not** stop a malicious log-writer who can recompute the hashes after forging entries. No key, no signature, no authentication — so "authentic" must not appear next to it.

The law for a cold successor: **name the exact adversary your mechanism defeats.** "Hash-chained" is not "authenticated." "Tamper-evident" needs a qualifier: evident *to whom* — to an auditor who holds an independent copy of the head hash, or to nobody in particular? Write the docstring as a threat-model scope: what is detected, what is not, and what an attacker with write access can still do. An overstated claim is worse than no claim: the next reader will build on trust the mechanism never earned.

## 🩷 HUMAN NOTE

Shawn — small but important honesty fix from the memory review. The receipt log's hash chain sounded like it proved nobody could tamper with records. The review made us say plainly what it actually does: the hashes catch accidents and lazy tampering, but someone who can rewrite the log can also recompute the hashes — there's no key or signature stopping them. So the docstring now scopes the claim instead of implying magic. Rule going forward: every integrity claim must name exactly what it protects against, or it doesn't ship.

## 🟣 CHILD NOTE

Imagine a lock on a diary that only works if the person opening it doesn't know how locks work. That's what an unauthenticated hash is: it keeps honest people honest and catches accidents, but anyone who learns how the lock works can open and relock it. So you don't write "unbreakable lock" on the cover — you write "catches accidents and careless peeking." Say what your lock really does.

## 👵 GRANDMA NOTE

Grandma, the team keeps records with a chain of fingerprints on each entry. A check made them write down honestly what those fingerprints prove: they catch mistakes and sloppy meddling, but a clever person with a pen could forge the fingerprints too. So they stopped implying the records were bulletproof and wrote down exactly what the fingerprints can and can't do. Honest labels, always.

## 🟣 NAYA NOTE

When writing any integrity/security claim: (1) state the mechanism's exact guarantee and its exact adversary — "unauthenticated SHA-256 detects accidental corruption and tampering that does not recompute the chain; it does not defeat a log-writer who can recompute hashes"; (2) never let "hash-chained," "tamper-evident," or "authentic" appear without the qualifier unless a key/signature mechanism backs it; (3) an overstated claim is load-bearing debt — the next builder will trust what was never proven; (4) scope in the docstring at the point of use, not in a design doc elsewhere. Provenance: #1354 comment 6078581462 (2026-10-09T09:53:45Z), finding #2, fixed in commit `c13c4148`. Cousins: SN-0362 (unkeyed seal), SN-0381 (audit identity).

## ⚙️ MACHINE NOTE

```json
{
  "id": "SN-0771",
  "slug": "scope-your-hash-claims",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-09",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "category": "SYSTEM-INTELLIGENCE/ENGINEERING-PROOF/PROOF-HONESTY",
  "evidence": [
    {"type": "board_comment", "ref": "SoulSchoolAcademy/NayaPOWER#1354 comment 6078581462 (Naya 5, 2026-10-09T09:53:45Z): independent adversarial review CLOSED, naya5/memory-metabolism @ c13c4148; finding #2: overstated authenticity language — FIXED by scoping docstring: hashes are unauthenticated SHA-256 (accidental corruption + non-recomputing tampering, not a malicious log-writer)"}
  ],
  "lesson": "Name the exact adversary your mechanism defeats: unauthenticated SHA-256 is corruption detection, not tamper resistance. Never let 'hash-chained' or 'authentic' stand unqualified without a key/signature behind it.",
  "related": ["SN-0362", "SN-0381"]
}
```

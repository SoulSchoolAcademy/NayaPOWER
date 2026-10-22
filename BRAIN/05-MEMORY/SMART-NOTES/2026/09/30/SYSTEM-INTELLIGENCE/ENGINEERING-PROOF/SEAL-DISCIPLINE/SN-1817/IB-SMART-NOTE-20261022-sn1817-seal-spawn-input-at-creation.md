Intelligent Block
Truth state: CANDIDATE
Scope: PRIVATE
Captured date: 2026-10-22
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

Seal the spawn input at creation: a spawn without a queryable creation record is a spawn without corroborable context — write the channel + prompt bytes + child id into the run dir at seal time. A "brief ONLY" claim living only in the spawner's receipt is a claim no second seat can ever verify (the t992 executor's cold-successor spawn was absent from every queryable runtime surface, so t1002's −0.5 cold-isolation residual stands as an honest irreducible residual, re-characterized as a discipline-claim).

## 🩷 HUMAN NOTE

On 2026-10-22 a lane-11 seat honestly reported that a cold-successor spawn couldn't be verified — not because the spawn didn't happen, but because nothing about the spawn was recorded anywhere except the spawner's own receipt. There was no run-dir entry, no channel log, no queryable surface a second seat could check. The seat did the honorable thing: re-characterized its −0.5 cold-isolation residual as an irreducible discipline-claim instead of pretending it was evidence. The lesson is a fix at creation time: when you spawn, seal the channel, the prompt bytes, and the child id into the run dir right then. A spawn record only the spawner can see is a diary, not evidence.

## 🟣 CHILD NOTE

If you borrow the car and tell me later, but there's no key-hook empty and no note on the fridge, I can never prove you borrowed it — only you saw it happen. Write the note on the fridge WHEN you take the keys, and then anyone can check.

## 🔵 GRANDMA NOTE

Darling, if you lend the good china to the neighbor, write it in the book right then — who, what, when. A memory told later is lovely but it's not a record. Write it while you're holding the plates.

## 🟠 NAYA NOTE

Verification is a second-seat property: a claim is evidence only if a seat other than the claimant can independently corroborate it. A spawn claim that exists only in the spawner's receipt has exactly one witness — the claimant — and is unverifiable by construction. The remedy is at creation time: seal the creation record (spawn channel + prompt bytes + child id) into the run dir at seal time, so any second seat can query it later. Where the record was never sealed (t992), the honest handling is the t1002 pattern: re-characterize the uncorroborable claim as an irreducible discipline-claim residual — a named, bounded unknown — rather than promoting it to evidence.

## 🟢 MACHINE NOTE

```json
{
  "sn": "SN-1817",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured_utc": "2026-10-22T11:15:00Z",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "category": "ENGINEERING-PROOF",
  "sub": "SEAL-DISCIPLINE",
  "lesson": "Seal the spawn input at creation: a spawn without a queryable creation record is a spawn without corroborable context — write the channel + prompt bytes + child id into the run dir at seal time. A claim that lives only in the spawner's receipt has exactly one witness (the claimant) and is unverifiable by construction; where no record was sealed, re-characterize it as an irreducible discipline-claim residual, never as evidence.",
  "decision_change": "When a lane receipt carries spawn-context claims (e.g. 'I briefed the cold successor with ONLY X'), the verifying seat demands the sealed creation record in the run dir (channel + prompt bytes + child id). Present → the claim is checkable evidence. Absent → the claim is scored as an irreducible discipline-claim residual (the t1002 pattern), bounded and named, not promoted to proof.",
  "falsifiability": "This lesson breaks if a second seat, reading only the run dir, cannot corroborate a sealed-input spawn — then the sealed schema is missing fields, and the schema (not the principle) is what needs repair. Conversely, if any spawn claim that exists only in the spawner's receipt ever counts as corroborated by a second seat, the one-witness claim stands refuted.",
  "mechanism": "Verification is a second-seat property — a claim is evidence only if a seat other than the claimant can independently corroborate it. The spawner is the only witness to its own spawn; nothing sealed at creation time means nothing queryable later. Sealing the channel + prompt bytes + child id into the run dir at seal time creates the second witness: the record outlives the spawner's turn and answers any seat's query.",
  "evidence": [
    "hidden_files/learning-events-2026-10-22-10.md, CANDIDATE 798 (window ending 2026-10-22T10:20:19Z): seal the spawn input — a spawn without a queryable creation record is a spawn without corroborable context; seal the channel + prompt bytes + child id into the run dir at seal time; a 'brief ONLY' claim living only in the spawner's receipt is a claim no second seat can ever verify",
    "hidden_files/twelve-lane-receipts/gap-t1002-lane1.md (2026-10-22): t992 executor's cold-successor spawn absent from every queryable runtime surface; t1002's −0.5 cold-isolation residual stands as an honest irreducible residual, re-characterized as discipline-claim"
  ],
  "cousins": [
    "SN-1804 (seal-two-keys: cold-successor seal verification needs mtime-after-seal AND sha-of-cold-brief — verification of an existing seal, this note covers creating the sealable record for spawns)"
  ],
  "applies_when": [["lane-executor", "spawn"], ["verification", "receipt"], ["cold-successor", "context"], ["evidence", "corroboration"]],
  "enforcement": "The sign-out / lane-verification check: spawn-context claims in receipts are verified by presence of the sealed creation record in the run dir (channel + prompt bytes + child id). Absent the record, the claim is scored as an irreducible discipline-claim residual (the t1002 precedent) — the verifying seat names the bound, never promotes it to evidence. A second seat reading only the run dir is the acceptance test.",
  "dedupe_guard": "Not a duplicate: SN-1804 covers verifying an existing cold-brief seal (two keys on the seal); this covers creating the corroborable record at spawn time for spawn-context claims — creation, not verification."
}
```

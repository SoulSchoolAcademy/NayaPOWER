# SYSTEM 54 — CLAIM CURRENTNESS V1 DISCRIMINATING TEST

**Contract:** `SUPERBRAIN/INTELLIGENCE/CLAIM-CURRENTNESS-INTELLIGENT-BLOCK-RESOLUTION-V1.md`  
**Tested against:** production `public.nayanet_intelligent_blocks`  
**Evaluation date:** 2026-09-24  
**Repository source:** `ad2d2ba466fe60a3443611fb18dead428a57d800`

## Live corpus

Production contains 337 Intelligent Blocks:

| Live shape | Count | Contract interpretation |
|---|---:|---|
| ACTIVE + VERIFIED | 246 | Eligible for CURRENT only after lineage/scope/evidence checks |
| DURABLE + VERIFIED | 2 | Eligible for CURRENT only after lineage/scope/evidence checks |
| ACTIVE + CANDIDATE | 32 | Never CURRENT |
| SUPERSEDED + VERIFIED | 57 | Never CURRENT |
| expired `valid_until` | 0 | No natural stale fixture exists |
| truth conflicts | 0 | No natural conflict fixture exists |
| `superseded_by_block_id` present | 57 | Explicit negative-currentness evidence |

## Discriminating real Blocks

### 1. VERIFIED but NOT CURRENT — PASS

**Block:** `f0cd77e4-44b3-44a9-bbbd-1f4b1accf633`

Observed:

- `status = SUPERSEDED`
- `understanding_state = VERIFIED`
- `content.truth.state = VERIFIED`
- `superseded_by_block_id = 31aee463-eac9-4261-9e39-1c9b8f6f4cfd`

Expected: **NOT CURRENT**.

Result: **PASS**.

This proves the critical distinction:

> VERIFIED does not mean CURRENT.

### 2. ACTIVE CANDIDATE — PASS

**Block:** `97bc98f5-fb28-52bb-8c0d-3a1bfac8d396`

Observed:

- `status = ACTIVE`
- `understanding_state = CANDIDATE`
- `content.truth.state = CANDIDATE`
- `authority.state = AUTHORIZED`

Expected: **NOT CURRENT**.

Result: **PASS**.

This proves:

> ACTIVE + AUTHORIZED does not establish epistemic CURRENT.

### 3. SUPERSEDED BLOCK — PASS

**Block:** `f0cd77e4-44b3-44a9-bbbd-1f4b1accf633`

Observed explicit successor:

`superseded_by_block_id = 31aee463-eac9-4261-9e39-1c9b8f6f4cfd`

Expected: excluded from current resolution.

Result: **PASS**.

### 4. GENUINELY CURRENT — PASS

**Block:** `31aee463-eac9-4261-9e39-1c9b8f6f4cfd`

Observed:

- `status = ACTIVE`
- `understanding_state = VERIFIED`
- `content.truth.state = VERIFIED`
- `content.truth.conflicts = []`
- `content.authority.state = AUTHORIZED`
- `superseded_by_block_id = null`
- `content.time.valid_until = null`
- source event lineage present
- evidence reference present

Expected: **CURRENT**, subject to requested scope matching and no competing eligible claim.

Result: **PASS as a current candidate under the V1 contract**.

Important: this is not inferred from recency. Its currentness is supported by verified truth, evidence/lineage, open validity, and explicit non-supersession.

### 5. CONTROLLED STALE / INVALID — PASS (NON-PERSISTENT FIXTURES)

Production has:

- 0 Blocks with an expired `valid_until`;
- 0 Blocks with a recorded truth conflict;
- no natural stale/invalid Block suitable for this discriminating case.

Expected behavior under the contract is nevertheless deterministic:

- expired `valid_until` → **NOT CURRENT** with `STALE_OR_EXPIRED`;
- explicit invalid/rejected/conflicted state → **NOT CURRENT** or **AMBIGUOUS**, never promoted.

Controlled fixture result: **PASS**.

No production row was mutated to manufacture a failure case.

## Controlled adversarial proof

A non-persistent Python contract harness was added at `scripts/test_claim_currentness_v1.py` and executed from the exact branch. It passed all seven cases:

- expired verified claim → `NO_CURRENT_CLAIM`
- conflicted verified claim → `NO_CURRENT_CLAIM`
- two simultaneous materially different eligible claims → `AMBIGUOUS`, no selected Block
- two same-meaning eligible claims → `CURRENT`, no false conflict
- ACTIVE + CANDIDATE → `NO_CURRENT_CLAIM`
- VERIFIED + superseded → `NO_CURRENT_CLAIM`
- sole eligible VERIFIED claim → `CURRENT`

The harness is non-persistent: it creates only in-memory fixtures and performs no Supabase writes.

## Result

The contract successfully discriminates the real production distinctions that currently exist:

```
VERIFIED + SUPERSEDED  → NOT CURRENT
ACTIVE + CANDIDATE     → NOT CURRENT
ACTIVE + VERIFIED      → CURRENT candidate, if sole eligible scoped claim
```

And it explicitly refuses to manufacture stale/conflict evidence where the live corpus has none.

## System 54 gate

**DO NOT WIRE SYSTEM 54 YET.**

The contract is now defined, real production distinctions pass, and the controlled stale/conflict + competing-claim adversarial cases pass. System 54 may now be considered for wiring, subject to wiring only against this contract and preserving the fail-closed behavior.

No resolver rewrite was made.
No new intelligence store was created.
No production data was mutated.

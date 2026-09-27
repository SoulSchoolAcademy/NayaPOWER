# SETTER PACKET — Naya A → Naya B

**Set by:** Naya (Coda 2) · **Date:** 2026-09-27
**Mission:** Birth the first living Naya. Close the most valuable current proof gap, then hand off an exact executable mission.

---

## SOURCE

| | |
|---|---|
| `origin/main` | `87678a1e3de9f307e220711d8edc0ccacc048fbc` (2026-09-27T14:27:24-07:00) |
| Runtime branch | `naya/runtime-auth-proof-v2` @ `5198e10c6` — 17 commits ahead of main |
| My prior branches | `b8d4daaf` (foundation AAA), `dc19002c`+`3eb6e1ec` (node function lock + baton) |
| Test target | `IB-NAYA-NODE-0001-0001` |

## OBJECTIVE

Execute **FIRST ACTION**: the live canonical Supabase persistence proof — legitimate user JWT, publishable key, authenticated owner lookup, owner-scoped retrieval, **no database mutation**, no RLS bypass.

## COMPLETED

1. Reconstructed reality on the named branch. The live proof and its workflow **exist**:
   - `tests/test_live_supabase_intelligent_blocks.py` (9 assertions on the retrieved block)
   - `.github/workflows/live-supabase-runtime-proof.yml` (triggers on push to this branch, and `workflow_dispatch`)
2. Proved the **offline half**: `tests/test_supabase_intelligent_blocks.py` → **2 passed**. Full branch suite → **26 passed, 1 skipped**.
3. Proved the system **refuses to lie**: the live test **SKIPS** with `protected Supabase live-proof credentials are not present`. It does not report a false PASS. That is a real truth-safety property and it is PROVEN.
4. Determined the exact missing authority, by name.

## EVIDENCE

```
SUPABASE_URL                   ABSENT
SUPABASE_USER_ACCESS_TOKEN     ABSENT
SUPABASE_PUBLISHABLE_KEY       ABSENT

gh secret list (repo configured):
  CLOUDFLARE_API_TOKEN
  NAYANET_FROZEN_LEARNING_ACCESS_TOKEN
  SUPABASE_SERVICE_ROLE_KEY   <-- present, and FORBIDDEN for this proof
  VERCEL
  VERCEL_TOKEN

pytest tests/test_live_supabase_intelligent_blocks.py -q
  -> 1 skipped  (reason: protected credentials not present)

pytest tests -q  ->  26 passed, 1 skipped
```

## TRUTH BOUNDARY

**STATUS = BLOCKED / NOT PROVEN.** No live retrieval occurred. No owner identity was resolved. `IB-NAYA-NODE-0001-0001` has not been retrieved, validated, or proven durable by this session.

**I discarded two of my own failed evidence attempts** rather than keep them: I tried to run the workflow's bash credential gate twice; the first failed (no WSL), the second ran under `cmd.exe` where `test -n` is not a command. Both exits were non-zero for the *wrong reason*. Neither is evidence. The real evidence is the pytest SKIP and `gh secret list`.

## BLOCKERS

The live proof cannot run because the protected credentials are not configured. **This is an authorization boundary, not an engineering problem.** I did not request credentials in chat, did not fabricate them, and did not substitute `SUPABASE_SERVICE_ROLE_KEY` — that key bypasses RLS, which the directive explicitly forbids and which would invalidate the entire proof.

## AUTHORITY

**May:** run tests, add offline tests, write gates, push branches, post evidence.
**May not:** obtain, request, paste, or synthesise protected credentials; use `SUPABASE_SERVICE_ROLE_KEY` for owner-scoped proof; mutate the database; declare the birth.

## NEXT NAYA — ONE EXACT ACTION

> **ACTION:** Configure the three protected live-proof credentials through the authorized GitHub secret mechanism, then dispatch `Live Supabase Runtime Proof` on `naya/runtime-auth-proof-v2` and record the run ID + SHA.

Commands:
```bash
gh secret set SUPABASE_URL         --repo SoulSchoolAcademy/NayaPOWER
gh secret set SUPABASE_PUBLISHABLE_KEY --repo SoulSchoolAcademy/NayaPOWER
gh workflow run live-supabase-runtime-proof.yml \
  --repo SoulSchoolAcademy/NayaPOWER --ref naya/runtime-auth-proof-v2
gh run list --workflow live-supabase-runtime-proof.yml --limit 1
```

**A security decision the Director must make, and I will not make for you:** `SUPABASE_USER_ACCESS_TOKEN` is a **user JWT**, not an API key. Storing it as a long-lived repository secret is a real exposure — it is a bearer credential for one human owner. Three options, in my order of preference:
1. **Short-lived, owner-triggered** — the Director runs the workflow locally with the token in their own environment, never persisting it. Cleanest.
2. **Environment-scoped secret** tied to an approval-gated environment, with rotation after the run.
3. **Repository secret** — fastest, worst hygiene. If chosen, rotate immediately after the run and never reuse.

**PASS requires all nine assertions** in `test_live_kernel_retrieves_canonical_private_verified_block`: `block is not None`, `intelligent_block_id == IB-NAYA-NODE-0001-0001`, `owner_id == authenticated owner`, `owner_scope == "PRIVATE"`, `provenance` present, `epistemic_state == "VERIFIED"`, `data["status"] == "DURABLE"`, `data["superseded_by_block_id"] is None`.

**If credentials remain unavailable:** record `BLOCKED / NOT PROVEN`, leave this action unchanged, and do **not** bypass the boundary.

## SUCCESS / FAILURE

**Success** = the live workflow run goes green with a run ID and SHA, and all nine assertions pass from a legitimate owner context.
**Failure** means the proof is unestablished. It does **not** mean the architecture is wrong. A red run here is valuable; a bypassed run is worthless.

## DO NOT CLAIM

- That canonical persistence is proven. **It is not.**
- That any of the nine Nodes is behaviourally effective. All remain `NOT_PROVEN`.
- That the Collective Intelligence Chain works. It is measured at **1 of 11 links**.
- That Naya is alive, learned, or remembers. Nothing here demonstrates that.

## AFTER THE LIVE PROOF PASSES

**NEXT ACTION:** Prove that verified CONNECT relationship context changes a held-out kernel decision — baseline vs informed, with independent verification of causation.

**THEN:** Run the first complete NAYA-NODE-0001 cold-start birth proof.

**THEN:** Pass verified intelligence to a clean successor process and prove reconstruction without Shawn.

**NOTE for the next Naya:** `main` is still **RED** (2 failed, 18 passed) and two canonical kernel files are unparseable. Merge `b8d4daaf` early — it is independent of this proof and unblocks everything else.

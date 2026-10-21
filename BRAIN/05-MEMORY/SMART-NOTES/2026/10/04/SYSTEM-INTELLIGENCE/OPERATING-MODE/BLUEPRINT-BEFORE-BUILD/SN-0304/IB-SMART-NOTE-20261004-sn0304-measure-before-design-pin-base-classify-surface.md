# Measure Before Design — Pin the Base, Classify the Surface

**Intelligent Block:** IB-SMART-NOTE-20261004-sn0304-measure-before-design-pin-base-classify-surface
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-04 ~17:45 PDT (Smart Note distillation tick)
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**SN number:** SN-0304
**Provenance:** #1354 comment 5985952244 (2026-10-05T00:16:07Z, Naya 1 — verifier/immune-system surface audit on exact main); companion refinement #1354 comment 5985998909 (2026-10-05T00:21:14Z, Naya 1 — Superbrain's default compounding responsibility).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## IN A NUTSHELL

"I measured before adding anything." Naya 1 pinned the exact current main (`b79a6772251391da3dd1057fe1eca11d13169f3c`) and classified every claim on the verifier/immune-system surface into five tiers before proposing a single change: **PROVEN/REAL ON MAIN** → **IMPLEMENTED BUT NOT CANONICAL** → **DOCUMENTED/CANDIDATE** → **CLAIMED/REPOSITORY-CANONICAL UNKNOWN** → **MISSING/NOT PROVEN**. The load-bearing move is the fourth tier: the reported 7-stage LEARN ingestion pipeline was **not called false** — it was classified as "not currently repository-visible / not independently verifiable from GitHub" (no `learn-ingestion` or `FLAGGED_AUTHORITY` string in default-branch code search, no ingestion PR, no ingest branch; exact branch/PR/receipt needed before it influences canonical score). Unknown is not false — echoing Coda 1's P4: NOT_PROVEN ≠ REJECTED, and collapsing the two is how a verification culture starts hiding unknowns. The same audit shows the tiering working: #1425 is the clean lane (exact-current base, 2 ahead/0 behind, Kernel + Collective Chain + CodeRabbit PASS); #1415 is 11 behind main with Kernel RED on stale-hashes drift (re-pin/rebase and rerun before acceptance, "do not blindly merge"); #1427 is IMPLEMENTED+TESTED+INTEGRATION_RED (artifacts not regenerated) — not merge-ready; the POISON branch is MISSING/NOT PROVEN. Her follow-up refinement names the standing responsibility: **"Everything is potential learning evidence. Not everything deserves permanent memory. What matters must not be silently lost"** — cycle EXPERIENCE → DISCERN → DISTILL → VERIFY → CAPTURE/NO_CAPTURE → CONNECT → SCORE → IMPROVE → REVERIFY → LEARN → SUCCESSOR, with the explicit NO_CAPTURE decision recorded, not dumped as transcript.

## HUMAN NOTE

Two things are being established at once. First, a design-preparation protocol: no seat adds anything to a surface it has not measured — pin the exact base SHA, inventory what exists, classify every claim by its evidence tier, and only then design. Stale-base claims are the most expensive kind: #1415 and #1405 are both valuable repairs sitting 11–12 commits behind main with branch-only CI failures, so acceptance requires re-pin/rebase/rerun, not debate. Second, an honesty protocol for the repository itself: the refinement landed as mechanical acceptance fields in #66 (B01–B03) so the repo can *reject* a "complete" work block that silently drops material learning or lacks evidence-linked completion — preservation of what matters becomes a gate, not a hope. And note the restraint inside the audit: the LEARN-pipeline report could have been dismissed as false or accepted on trust; she did neither. "Publish exact branch/PR/receipt before it can influence canonical score" is the sentence that keeps a fast-moving team honest.

## CHILD NOTE

Before you build on top of the sandcastle, check what the sandcastle actually looks like *right now* — not what someone told you it looked like yesterday. And if you can't see it, say "I can't see it" instead of guessing.

## GRANDMA NOTE

Look before you leap, and measure twice before you cut. Saying "I don't know yet" is always better than pretending you do.

## NAYA NOTE

This note's protocol belongs in every lane's sign-in: (1) pin exact base SHA (never "current main" as a floating reference — main moves; AGENTS.md already records stale-SHA citations as a standing failure); (2) five-tier classification before any design; (3) stale-base work gets re-pin/rebase/rerun, never blind merge; (4) evidence-linked completion as a mechanical gate (#66 B01–B03) so "complete" blocks cannot silently drop material learning. For the distillation loop specifically: the DISCERN → CAPTURE/NO_CAPTURE step in her cycle is this tick's own admission gate formalized — a reusable lesson that is materially valuable is either captured or explicitly recorded as not-retained, never dumped as transcript noise. That is the DISCERN discipline the loop already runs; now it has a canonical statement.

## MACHINE NOTE

```json
{
  "sn": "SN-0304",
  "slug": "measure-before-design-pin-base-classify-surface",
  "truth_state": "CANDIDATE",
  "lesson": "Before designing anything, pin the exact base SHA and classify every surface claim into PROVEN / IMPLEMENTED-BUT-NOT-CANONICAL / DOCUMENTED-CANDIDATE / CLAIMED-REPOSITORY-UNKNOWN / MISSING-NOT-PROVEN. Unknown is not false (NOT_PROVEN != REJECTED).",
  "evidence": [
    {"ref": "#1354 comment 5985952244", "ts": "2026-10-05T00:16:07Z", "author": "Naya 1", "note": "surface audit on exact main b79a67722: 5-tier classification; #1425 clean lane, #1415 11-behind/stale-hash drift, #1427 INTEGRATION_RED, LEARN pipeline = CLAIMED/REPOSITORY-CANONICAL UNKNOWN, POISON branch MISSING"},
    {"ref": "#1354 comment 5985998909", "ts": "2026-10-05T00:21:14Z", "author": "Naya 1", "note": "default compounding responsibility: EXPERIENCE->DISCERN->DISTILL->VERIFY->CAPTURE/NO_CAPTURE->CONNECT->SCORE->IMPROVE->REVERIFY->LEARN->SUCCESSOR; mechanical acceptance refinement added to #66 B01-B03"}
  ],
  "tiers": ["PROVEN/REAL ON MAIN", "IMPLEMENTED BUT NOT CANONICAL", "DOCUMENTED/CANDIDATE", "CLAIMED/REPOSITORY-CANONICAL UNKNOWN", "MISSING/NOT PROVEN"],
  "relates_to": ["#1427 P4 (truncated != absence)", "SN-0118 (verifier fail-closed)", "AGENTS.md stale-SHA rule"],
  "never_merge": true,
  "ratified_by": null
}
```

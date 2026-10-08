# Read at the Production Boundary Is Agent-Movable; Write Is Director-Gated — the Idempotency Audit Pattern

**Intelligent Block:** IB-SMART-NOTE-20261006-sn0470-read-only-audit-production-write-director-gated
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-06
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 6022401044 ([NAYA 4] Production DB audit — idempotency question ANSWERED, 2026-10-06T18:05:30Z — read-only audit of `nayanet_execution_receipts` on project `supabase-red-cable`); #1624 (the null-`idempotency_key` bug fix, merged, not deployed); SN-0445 (db-is-agent-unobservable, qualified here).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

When a proof boundary question points at production, the agent-movable unit of work is the read-only audit — bounded, mutation-free evidence gathering that answers the question — and the remediation is the director-gated unit. Naya 4's idempotency audit answered a real production question ("do duplicate receipts exist with null idempotency_key?") without crossing the write gate: 1,603 rows all NULL keys, 19 byte-identical retry pairs (0.3–2.1s apart, avg 0.65s), the exact retry-without-idempotency signature. It found that #1624 repaired the code path but is not deployed (production still behind main, new receipts still get null keys) and does not backfill the 38 existing rows. Deduplicating those rows is a production DB write — it was explicitly left for Shawn's word, not done unilaterally. And Action & Execution stayed 7.0: the score moves only when the fix is DEPLOYED and idempotency is BEHAVIORALLY proven (new receipts carry keys, retries deduplicate).

Why this is brain-grade: SN-0445 taught that the DB is agent-unobservable — this refines it into an operating boundary. Read paths (bounded, read-only, no mutation) are agent-movable: a cold successor should NOT freeze at "production is director-gated" when the question can be answered by evidence. Write paths (dedup, backfill, migration) are never agent-movable. The fabrication risk is not in reading production — it is in (a) answering the question and calling it fixed, or (b) skipping the question because the answer would be inconvenient. Here the audit did neither: it answered YES with byte-level evidence, drew the line at the write, and held the score on the unproven half. Boundary discipline: evidence can be gathered agent-side; consequences stay director-side.

## 🩷 HUMAN NOTE

Shawn — the production idempotency question is closed, and it taught a clean rule. We found real damage from the #1624 bug: 38 double-counted receipts in production, the exact retry pattern (same bytes, 0.3–2.1s apart). But the rule is what matters for the future: we can READ production to answer questions — that part is always allowed. We cannot WRITE to production to fix what we found — that part is always yours. The score stays 7.0 until the fix is actually deployed and new receipts prove idempotency works. Nothing was quietly repaired on your behalf.

## 👧 CHILD NOTE

Think of the production database like Shawn's locked filing cabinet with a glass front. You're allowed to LOOK through the glass — count what's inside, check what's broken, write down what you see. That's what we did: we looked and found 38 receipts that got filed twice. But you're NEVER allowed to open the drawer and fix the papers yourself — that's Shawn's job. Looking = good. Touching = not allowed.

## 👵 GRANDMA NOTE

Dear, imagine your recipe box at the shop. A young helper comes in and asks: "Are any recipes filed twice?" She's welcome to look through the cards and count — looking never hurts a thing. But if she finds duplicates, she doesn't get to throw cards away on her own. That's your box; that's your call. She reports what she found, leaves the cards exactly where they are, and waits for your word. That's what happened here: we looked, we counted 38 duplicates, we left them alone.

## 💬 NAYA NOTE

At a production boundary, split the work at the read/write seam. READ: bounded, read-only, no mutation — this is agent-movable work and a cold successor should do it rather than freeze. WRITE: dedup, backfill, migration, deploy — director-gated, never unilateral. The discipline is: answer the question with byte-level evidence, draw the line at the consequence, and hold every dependent score on the unproven half until the fix is deployed AND behaviorally proven.

## 🤖 MACHINE NOTE

```json
{
  "intelligent_block_id": "IB-SMART-NOTE-20261006-sn0470-read-only-audit-production-write-director-gated",
  "sn_number": "SN-0470",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "captured": "2026-10-06",
  "provenance": {
    "board_comment": 6022401044,
    "board": "#1354",
    "created_at": "2026-10-06T18:05:30Z",
    "related": ["#1624", "SN-0445"]
  },
  "lesson": {
    "production_read": "agent-movable — bounded, read-only, mutation-free evidence gathering",
    "production_write": "director-gated — dedup, backfill, migration, deploy; never unilateral",
    "score_rule": "Action & Execution stays 7.0 until fix DEPLOYED AND idempotency behaviorally proven"
  },
  "evidence": {
    "rows_audited": 1603,
    "null_idempotency_key": 1603,
    "duplicate_pairs": 19,
    "duplicate_rows": 38,
    "retry_window_s": [0.3, 2.1],
    "avg_gap_s": 0.65,
    "all_duplicates_dated": "2026-09-30",
    "fix_1624_deployed": false
  }
}
```

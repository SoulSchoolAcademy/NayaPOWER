# Synthetic Records Are Not Records — Emitters Source the Real Migrations

**Intelligent Block:** IB-SMART-NOTE-20261015-sn01451-synthetic-records-are-not-records
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-15
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Captured on the 20:38 PDT smart-note-distillation tick (2026-10-15) by Naya Clarity Narzan from `hidden_files/director-briefing-2026-10-15.md` §5 (Shawn's 17:58 PDT exact-code review and build-order revision, superseding the first draft) on board #2641 — corrections to PRs #2678, #2679, #2680 before review.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Shawn's exact-code review of the hub-integration emitter PRs named the correction plainly: #2680 adds cron with no payload producer (a schedule that fires nothing); #2678 attempts public JSON from private-scope intelligence metadata, and its synthetic Spaces/Lists are not real social records; #2679 has no authenticated personal path or mutation. The revised merge order: #2676 and #2679 can proceed through review; #2680 needs a payload producer before its schedule means anything; #2678 must be reworked FIRST — sourced from the REAL Supabase migrations (Spaces/memberships, Connections, v7 internal Mail, Lists, daily intelligence), never synthetic records, and no public JSON from private-scope metadata. Do not merge or publish private output until LAW/VERIFY challenges pass. The doctrine: synthetic records are not records — an emitter that emits invented data teaches every consumer the wrong shapes and the wrong privacy scoping, and no amount of downstream validation can fix a lie at the source.

## 🩷 HUMAN NOTE

Imagine hiring a reporter who files stories by making up quotes instead of calling the people. The articles look real, the grammar is fine — but every reader learns things that never happened. Shawn's rule says: the reporter must call the real people (the actual database tables). Made-up quotes are not quotes, even when they're well-written.

## 🟣 CHILD NOTE

It's like doing a book report on a book you never read, by guessing. The teacher might be fooled for a minute, but everything you wrote is about a book that doesn't exist. The rule says: read the real book — the real tables in the database — and report on those. Guessing is not reporting.

## 👵 GRANDMA NOTE

When the doctor needs your test results, she doesn't want someone to make up numbers that look healthy — she wants the actual lab report. A made-up number can look exactly right and still be dangerous, because it sends everyone down the wrong path. The rule is simple: always go to the real lab, never invent the numbers. And never publish someone's private results where the public can read them.

## 🧠 NAYA NOTE

This is an instrument-design rule, not a preference. The emitter is the instrument; the migrations are its calibration source. A synthetic-sourced feed drifts from the real schema AND from the RLS semantics — so rooms consume wrong shapes under wrong privacy assumptions, and the failure looks like consumer bugs when it's producer fraud. Note the two sibling corrections in the same review: a cron with no payload producer is a schedule that fires nothing (the #2680 rework — the producer comes before the schedule), and private-scope metadata must never go public as JSON (the #2678 rework). When you build any data pipeline, ask three questions before review: does every row trace to a real source table? does the private scoping survive the emission? does the schedule have a producer, or is it firing on empty?

## MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "synthetic_emitter_source_privacy_scope_violation",
  "evidence": {
    "briefing": "hidden_files/director-briefing-2026-10-15.md §5 (Shawn's 17:58 PDT exact-code review, board #2641 — supersedes the first draft)",
    "findings": "#2680 adds cron with no payload producer; #2678 attempts public JSON from private-scope intelligence metadata with synthetic Spaces/Lists (not real social records); #2679 has no authenticated personal path or mutation",
    "remedy": "#2676 and #2679 proceed through review; #2680 needs a payload producer first; #2678 reworked first — source from the REAL Supabase migrations (Spaces/memberships, Connections, v7 internal Mail, Lists, daily intelligence); no public JSON from private-scope metadata; no merge/publish of private output until LAW/VERIFY challenges pass"
  },
  "rule": "synthetic_records_are_not_records_emitters_source_the_real_migrations",
  "decision_changed": "what source an emitter reads: previously synthetic/demo records; now the real Supabase migrations — and private-scope metadata is never emitted as public JSON",
  "falsifier": "an emitted feed whose rows do not join 1:1 against the migration tables violates it; if a synthetic-sourced feed passed every consumer contract check against a migration-sourced feed, the rule's premise would be weakened",
  "mechanism": "synthetic records diverge from the real schema and RLS semantics, so consumers learn wrong shapes under wrong privacy assumptions while failures masquerade as consumer bugs; sourcing the migrations binds emitters to the true schema and the true privacy doctrine at the calibration point — downstream validation cannot repair a lie at the source",
  "related": ["SN-01450 (render from the probe — the MAP-STATE compiler; two-lane read path)", "GOVERNANCE/OPERATING-DOCTRINE"]
}
~~~

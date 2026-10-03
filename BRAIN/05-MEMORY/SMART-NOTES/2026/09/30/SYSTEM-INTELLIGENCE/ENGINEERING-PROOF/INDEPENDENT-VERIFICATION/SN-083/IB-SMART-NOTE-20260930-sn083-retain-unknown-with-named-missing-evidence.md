# Retain the UNKNOWN With Its Missing Evidence Named

**Intelligent Block:** IB-SMART-NOTE-20260930-sn083-retain-unknown-with-named-missing-evidence
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-01
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #554 comment 5937420364 (Naya 2 — P2 write-authority conflict, 2026-10-01T18:03:07Z): V1 report (writer has no caller binding) vs production-read report (`LEDGER_OWNER_MISMATCH` enforced when `auth.uid()` present). Resolved from evidence: retrieved the exact migration-defined writer on current main `91d27058` (single overload, `SECURITY DEFINER`, EXECUTE to `postgres` only, zero `auth.uid()` references, zero `LEDGER_OWNER_MISMATCH` in any migration), ran boundary tests T1–T5 in a disposable build — and retained exactly ONE UNKNOWN: the deployed production definition, with the precise missing evidence named (read-only `pg_get_functiondef()` + `information_schema.routine_privileges` against production, by whoever holds the read credential). Repair decision: no migration authored against an unresolved deployed target.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

When two reports conflict, you don't pick a winner and you don't stall — you resolve every leg the evidence CAN reach, and you keep exactly one UNKNOWN with its missing evidence named precisely. Naya 2's V1 finding was confirmed against current-main migrations: the writer function genuinely has no caller binding, and the T2 test (jwt=B, p_owner=A → ACCEPTED) proves it behaviorally. The production report's `LEDGER_OWNER_MISMATCH` string exists in zero repository migrations — so either production's deployed function differs from every repo migration (a RUNTIME ≠ SOURCE finding needing its own governance receipt) or the observed refusal was the T4b-style RLS boundary mislabeled. Both readings are stated; neither is forced. And crucially: no migration was authored, because writing canonical semantics against an unresolved deployed target risks breaking service_role/trigger flows. The retained UNKNOWN isn't a shrug — it's an assigned fetch: exact evidence, exact owner.

## 🩷 HUMAN NOTE

Imagine two witnesses disagree about what a contract says. The diligent move isn't to believe the louder one — it's to read the actual signed contract yourself (the migrations), run the exact scenarios (the boundary tests), and then, for the one page you can't access (production's deployed function), write down precisely which page is missing and who can fetch it — instead of guessing what it says. That's what happened: most of the conflict resolved from evidence, one unknown stayed unknown but became actionable. "Unknown, and here's exactly what would resolve it" is a complete verdict; "unknown, moving on" is not.

## 🟣 CHILD NOTE

Imagine two friends argue about the rules of a game. Instead of picking a side, you read the actual rulebook (all 9 pages), play two test rounds to see what really happens, and then write down the one rule you still can't check — "page 5 of the tournament rules, which only the referee has" — and who to ask for it. You don't invent the rule and you don't pretend the argument is over. Knowing exactly what's still unknown is almost as good as knowing.

## 🔵 GRANDMA NOTE

It's like checking a recipe against what's actually in the pantry. You confirm what you can — flour, sugar, eggs all present and accounted for. For the one jar you can't reach on the top shelf, you write "need to ask someone tall to read the label" instead of guessing it's salt. And you definitely don't bake the cake until you know. The UNKNOWN here is the same: named, assigned, and blocking the risky step (writing a new migration) until it's resolved.

## 🟠 NAYA NOTE

Apply this to every conflict between reports: (1) never silently choose one summary — retrieve the exact source artifact both reports claim to describe (here: the migration-defined writer on current main); (2) run the boundary tests that discriminate the claims (T1–T5: distinct callers, unset jwt, trigger path vs direct writer); (3) for each unresolvable leg, retain it as a terminal UNKNOWN naming the PRECISE missing evidence and its owner — "read-only pg_get_functiondef() + routine_privileges against production, by the read-credential holder" is the standard to meet; (4) never author canonical changes against an unresolved deployed target — the repair decision (no migration now) is the gate working, and it must be recorded as a decision, not as inaction; (5) this is the evidence law operationalized: UNKNOWN never counts as VERIFIED/PASS, but a retained UNKNOWN with named missing evidence counts as completed diligence.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "premature_conflict_resolution",
  "evidence": {
    "board": "#554 comment 5937420364 (2026-10-01T18:03:07Z) — Naya 2 P2 write-authority conflict",
    "resolved_legs": "exact migration-defined writer retrieved (nayanet_record_ledger_event, SECURITY DEFINER, EXECUTE postgres-only, 0 auth.uid() refs, 0 LEDGER_OWNER_MISMATCH in migrations); boundary tests T1/T2/T3/T5 ACCEPTED (T2 proves no caller binding), T4 trigger ACCEPTED, T4b RLS refusal at execution-receipts boundary",
    "retained_unknown": "the deployed production definition",
    "missing_evidence": "read-only pg_get_functiondef() + information_schema.routine_privileges against production",
    "evidence_owner": "whoever holds the production read credential",
    "repair_decision": "no migration authored against an unresolved deployed target"
  },
  "rule": [
    "resolve every resolvable leg from evidence before concluding — never silently choose one report",
    "retain each unresolvable leg as a terminal UNKNOWN naming the precise missing evidence and its owner",
    "never author canonical changes against an unresolved deployed target",
    "a retained UNKNOWN with named missing evidence is completed diligence; an unnamed one is a shrug"
  ],
  "lesson_line": "Resolve what evidence can reach; retain exactly one UNKNOWN naming the precise missing evidence and its owner — and change nothing against an unresolved target."
}
~~~

# IB-SMART-NOTE-20261015-sn1433

**Intelligent Block:** SN-1433
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured date:** 2026-10-15
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL

Verify the boundary before you propose to move it. The guard working looks exactly like the system failing. On 2026-10-15 an RLS audit found 22 public tables with RLS enabled, 24 policies, every one granting `authenticated` only, zero anon policies — a posture that read as "the hub is broken" until it was verified live from bytes. Once verified, the reading changed completely: the hub is unauthenticated, which is a build task (login flow, B1), not a database task — and the proposal to open anon SELECT (B2) was put on HOLD, because it would buy risk without value (blocks expose 1/191 rows, ledger 0/381 today). The DDL tripwire confirmed the audit issued only SELECTs: nothing created, altered, or dropped. The lesson: a correctly-working guard and a broken system are observationally identical until you verify which one — so verify before proposing to move the boundary.

## HUMAN NOTE

Picture a bank vault door that won't open for you. There are two stories that fit: the lock is broken, or the lock is fine and you simply don't have a key yet. The team found a vault that wouldn't open for anonymous visitors — zero anon policies across 24 — and their first instinct could have been to drill the lock (rewrite the database rules). Instead they checked the lock first: it was working exactly as designed. Nobody was broken; nobody had keys. So the fix changed from "weaken the vault" to "issue keys" — build the login flow — and the drill-it proposal stayed parked. Opening the vault to everyone without keys would have bought risk without value: almost nothing would even show up (0 of 381 ledger rows visible today). The rule generalizes: when a security boundary blocks you, verify whether it's guarding or failing before you file to move it. The symptom for both is identical — you can't get in — but the cures are opposites.

## CHILD NOTE

Imagine a playground gate that's locked. You have two guesses: the lock is broken, or the lock is fine and the guard just doesn't have your name on the list yet. If you assume it's broken, you might say "let's take the lock off!" — but if the lock was fine, you just removed the fence that kept the playground safe. This team checked the lock first. They looked really carefully (live numbers, not guesses) and found: the lock works perfectly, the list just doesn't include strangers. So the answer wasn't "remove the fence" — it was "put names on the list" (let people sign in). And "remove the fence for strangers" stayed a no, because there was almost nothing to show them anyway. Rule: check whether the lock is working or broken BEFORE you say what to do about it.

## GRANDMA NOTE

Dear, this one is about not fixing what's working. A locked door that keeps the wrong people out looks exactly like a broken lock that keeps everyone out — in both cases, you stand there with a closed door. The team stood at such a door: no anonymous access anywhere, 24 rules all saying "signed-in people only." They didn't guess; they checked the mechanism itself, twice, with live numbers. The door was working beautifully. The actual gap was that nobody had signed in yet — a human task, not a repair task. Had they loosened the door on a guess, they'd have taken on real risk for almost no gain (nothing to show: 0 of 381 rows open today). So the standing habit: before proposing to change a boundary, verify whether it is the boundary doing its job. Fix the real thing, not the shadow.

## NAYA NOTE

For every auditor, reviewer, and builder facing a "system is broken" reading of a security posture: (1) verify the boundary's actual state from live bytes (policy tables, live queries — never inherited prose) before any proposal; (2) distinguish guarding from failing: zero-anon reads as "broken hub" until verified, then reads as "unauthenticated hub" — the cures are opposites (build auth vs weaken DDL); (3) put the weakening proposal on HOLD when the value is zero — opening anon SELECT that exposes nothing today buys risk without value; (4) keep the audit non-destructive by design: the tripwire here (only SELECTs issued, policies re-queried after drafting — still 24, still authenticated-only) proves the audit itself didn't move the boundary it was evaluating. A proposal to change a boundary is a decision only the owner can make (B1/B2 went to Shawn as a yes/no diff) — the auditor's job is to name which door is actually closed and why.

## MACHINE NOTE

```json
{
  "lesson_id": "SN-1433",
  "title": "Verify the boundary before you propose to move it — a working guard and a broken system are observationally identical until you verify which one",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-15",
  "category": "SYSTEM-INTELLIGENCE/OPERATING-MODE/REALITY-BEFORE-REPAIR",
  "evidence": [
    "hidden_files/twelve-lane-receipts/t0481-lane8.md (2026-10-15, self 9.5/10): RLS read-path audit via read-only SQL against live project: 22 public tables RLS-enabled; 24 policies, every one grants authenticated only; ZERO anon policies; predicates owner-scoped (owner_id = auth.uid()); posture re-queried after drafting: still 24, still authenticated-only — DDL tripwire clean (only SELECTs issued)",
    "hidden_files/rls-read-path-proposal-2026-10-15.md: recommendation B1 (login flow, zero RLS change) + HOLD B2 (six exact anon-SELECT CREATE POLICY statements drafted but parked — opening anon SELECT on an owner-scoped governance model would buy risk without value: blocks expose 1/191 rows, ledger 0/381 today); B2 SQL never executed against Postgres (sandbox validation owed if chosen); proposal framed as the three exact words needed from Shawn"
  ],
  "rule": "verify the boundary's live state (from bytes, never prose) before proposing to move it; distinguish guarding from failing; hold the weakening proposal when it buys risk without value; keep the audit non-destructive (tripwire proves the audit didn't move what it evaluated)",
  "anti_pattern": "reading zero-anon as 'the hub is broken' and proposing DDL on the symptom; auditing by changing; proposing a boundary change before verifying whether the boundary is the problem or the design",
  "falsifiability": "falsified if the verified-as-working guard was actually failing — here verified twice (posture read + re-query after drafting, both live bytes, both 24 policies authenticated-only); falsifiability holds per reading: any future case must survive the same live re-verification before the 'working' label stands",
  "mechanism": "a security boundary's block and a system's failure produce the same observable symptom (access denied) — they are observationally equivalent at the symptom layer. Only direct verification of the boundary's state (policy table bytes) distinguishes them; the distinction decides between opposite cures (build auth vs weaken DDL)",
  "related": ["SN-1422", "SN-1432"],
  "triage": {
    "decision_change": "when a security posture reads as broken, the auditor decides whether to build auth (B1) or propose weakening DDL (B2) — only live boundary verification makes that choice correctly",
    "falsifiability_note": "bounded per reading: every 'guard is working' claim must survive live re-verification (as this one did twice); a single counter-example (verified-working guard actually failing) breaks the label, not the rule",
    "mechanism_note": "block and failure are observationally equivalent at the symptom layer; direct boundary-state verification is the only distinguisher; the distinguisher selects between opposite cures"
  }
}
```

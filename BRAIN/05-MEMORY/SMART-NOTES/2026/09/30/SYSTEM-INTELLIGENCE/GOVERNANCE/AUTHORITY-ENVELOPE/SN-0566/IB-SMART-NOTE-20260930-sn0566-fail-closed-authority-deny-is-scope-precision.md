# A Fail-Closed Authority Deny on a Fresh Dynamic Target Is Scope Precision, Not a Bug — Classify Before Widening the Matcher

**Intelligent Block:** IB-SMART-NOTE-20260930-sn0566-fail-closed-authority-deny-is-scope-precision
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-07
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 comments 6044715067 (2026-10-07T18:56:59Z), 6044734808 (2026-10-07T18:58:11Z, Naya 4); governed promotion run 37669766633 (EXPLICIT_HUMAN, source `1f8e908ea36520319ab474506977d7e36be57761`), runtime proof 37670104666.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

On 2026-10-07 the production proof run (37670104666) failed closed on learning promotion with `403 LEARNING_LOCK_IN_LAW_DENIED / NO_MATCHING_ACTIVE_AUTHORITY` for a fresh block id `IB-NAYA-FLOW-LESSON-b09cf06d78b64b1f9b7d9abe21826569` — even though grant `57d83ce5` was ACTIVE through 2026-10-14. The instinct is to treat the 403 as a bug and "fix" the matcher. The correct classification, proven on the board the same evening: **the deny was the system working.** The grant's scope was `NAYA-NODE-0001` (covering the older frozen node-scoped candidates); the fresh block is a new dynamically-created target. The canonical `resolveLearningLockInLaw()` matches only (a) exact `scope.target == intelligentBlockId`, or (b) `scope.project_id == intelligentBlockId`, or (c) `scope.project_id == "NayaNET"` — and none matched. A node-scoped grant does not authorize a fresh `IB-NAYA-FLOW-LESSON-...` target. Denying was correct.

Two falsifications nailed the mechanism instead of theorizing. First, the token hypothesis: a **fresh-OIDC retry returned the same 403**, while issuer/audience/repository/workflow/ref bindings were all verified correct — identity freshness was not the blocker, so stop theorizing about tokens. Second, the apparent contradiction ("authority is not the blocker" vs "authority IS the blocker") resolved cleanly: authority is not the blocker for the existing node-scoped candidate queue; authority **is** the blocker for fresh dynamically-created blocks. Same law, two scopes, no contradiction.

The smallest correct move is therefore the opposite of widening the matcher: **do not weaken target matching** (that converts one deny into an open door). The already-proven architecture supports the intended autonomy with one Human-rooted, bounded **project-scoped** grant — `actions=["learning_lock_in"], scope={"project_id":"NayaNET"}` with expiry/revocation preserved — which covers fresh blocks while leaving all independent verification gates intact. That grant is a human authority decision, and no grant was self-issued.

## 🩷 HUMAN NOTE

A bouncer turns away your friend at the door even though the friend has a valid ticket — because the ticket is for a different show. The fix isn't to tell the bouncer to stop checking tickets. The fix is to buy a ticket for the right show. The 403 was the bouncer doing his job correctly; the right show needed the right ticket.

## 🟣 CHILD NOTE

You have a library card that lets you borrow books from the school library. Then you try to use it at the big city library and the machine says NO. The machine isn't broken — your card just doesn't cover that library. You don't "fix" the machine so any card works everywhere. You get a card that covers the city library.

## 🔵 GRANDMA NOTE

It's like a parking permit for Zone A. You park in Zone C and get a ticket. The ticket isn't wrong — your permit just doesn't cover Zone C. You don't change the rules so one permit parks everywhere; you apply for a Zone C permit. The 403 was the ticket, correctly issued; the project-scoped grant is the Zone C permit.

## 🟠 NAYA NOTE

When a fail-closed authority deny hits a fresh dynamic target:

1. **Classify before touching the matcher.** Write down: grant id, expiry, exact scope, target block id. Run the canonical matcher by hand against the three legal shapes (exact target, project_id==block id, project_id=="NayaNET").
2. **If the deny is scope precision, do not widen the matcher.** Widening target matching to silence one deny is weakening a gate — a cousin of SN-0420 (never absorb the anomaly to silence the tripwire).
3. **Falsify the identity hypothesis first.** Re-run with fresh OIDC and verify bindings (issuer/audience/repository/workflow/ref). If the same 403 returns with healthy identity, the token theory is dead — stop spending on it (SN-0333: check the class list before the timer theory).
4. **Split apparent contradictions by scope.** "Authority is not the blocker" and "authority is the blocker" can both be true for different targets. Name which target each claim is about before declaring a contradiction.
5. **The legal repair is a bounded human-rooted grant** — project-scoped, expiry preserved, verification gates untouched. And: **no grant is ever self-issued** — the human director decides. Scorecard ≠ authority (SN-0565).

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "scope_precision_misread_as_matcher_bug",
  "evidence": {
    "production_promotion": "run 37669766633, event workflow_dispatch, actor SoulSchoolAcademy, authorized source 1f8e908ea36520319ab474506977d7e36be57761, mode EXPLICIT_HUMAN",
    "runtime_proof": "run 37670104666 — source-integrity/contract/learning-influence/cold-runtime-1+2/live CONNECT/independent verification PASS; learning-promotion FAIL; downstream SKIPPED",
    "deny": "403 LEARNING_LOCK_IN_LAW_DENIED / NO_MATCHING_ACTIVE_AUTHORITY for IB-NAYA-FLOW-LESSON-b09cf06d78b64b1f9b7d9abe21826569 — returned twice, including fresh-OIDC retry",
    "identity": "OIDC bindings verified healthy (issuer/audience/repository/workflow/ref) — token hypothesis falsified",
    "scope_facts": "grant 57d83ce5 ACTIVE through 2026-10-14, scope NAYA-NODE-0001 — covers older frozen candidates, not fresh dynamic block ids",
    "canonical_matcher": "resolveLearningLockInLaw() matches exact scope.target == intelligentBlockId, scope.project_id == intelligentBlockId, or scope.project_id == 'NayaNET'",
    "contradiction_resolution": "#1354 6044715067 — authority NOT blocker for node-scoped candidate queue; authority IS blocker for fresh dynamic blocks. Same law, two scopes.",
    "legal_repair": "bounded human-rooted project-scoped grant: actions=['learning_lock_in'], scope={'project_id':'NayaNET'}, expiry/revocation preserved; verification gates intact"
  },
  "rule": "classify_scope_mismatch_before_widening_the_matcher",
  "procedure": [
    "record grant id, expiry, exact scope, and target block id; run the canonical matcher by hand",
    "falsify the identity hypothesis with a fresh-OIDC retry and binding verification before theorizing",
    "if the deny is scope precision, do NOT widen target matching — that weakens a gate, not heals a bug",
    "split apparent authority contradictions by naming the target each claim is about",
    "the legal repair is a bounded human-rooted project-scoped grant; no grant is ever self-issued"
  ],
  "related": ["SN-0420 (never absorb the anomaly to silence the tripwire)", "SN-0333 (check the class list before the timer theory)", "SN-0439/SN-0485 (deterministic rejection — name the mechanism)", "SN-0565 (scorecard decides, never authorizes)"]
}
~~~

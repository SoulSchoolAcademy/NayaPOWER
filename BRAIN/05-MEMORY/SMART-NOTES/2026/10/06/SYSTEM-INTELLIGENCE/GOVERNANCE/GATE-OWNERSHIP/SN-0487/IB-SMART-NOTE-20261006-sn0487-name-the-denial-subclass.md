# IB-SMART-NOTE-20261006-sn0487-name-the-denial-subclass.md

Intelligent Block: SN-0487
Truth state: CANDIDATE
Scope: PRIVATE
Captured: 2026-10-06
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL

When an authority gate denies, never touch the gate — investigate it read-only first. The H13 learning_lock_in investigation (2026-10-06) ran the protocol: declare the investigation read-only and out of scope (no grant creation, no production change, no gate weakening), read the live source, name the exact denial subclass from live data (NO_MATCHING_ACTIVE_AUTHORITY — zero learning_lock_in grants exist), specify the exact grant shape that would clear the denial (issuer, subject, action, scope target, status, expiry), bound the blast radius, and deliver the brief to the director. The grant decision is the director's alone; the investigator's job is facts, not permission.

## HUMAN NOTE

Shawn, 2026-10-06, by the work: the H13 learning_lock_in gate was blocking a block from reaching LEARNED. Instead of anyone weakening the gate or quietly issuing a grant, a subagent ran a read-only investigation and came back with: "The denial subclass is NO_MATCHING_ACTIVE_AUTHORITY — the DB has zero grants with the learning_lock_in action. Here is the exact grant shape needed and exactly what it could touch." No grants created, no production modified, H13 intact. The decision on whether to issue the grant now sits with you, with the full facts.

## CHILD NOTE

When the system says "no" to something important, don't try to sneak around the "no." First, figure out exactly WHY it said no — read the real data, find the exact reason, and write down precisely what permission would fix it and what it could affect. Then bring those facts to the person in charge. You don't change the rules; you report the facts so the right person can decide.

## GRANDMA NOTE

Think of it like a locked filing cabinet. When the lock wouldn't open, nobody pried it open or picked it — instead someone checked the lock itself, found out the exact reason it wouldn't turn (the right key was never issued), wrote down what key would open it and which drawer it would reach, and took that report to Shawn. The lock stays strong; the decision stays his.

## NAYA NOTE

This is the investigation complement to the fail-closed doctrine (SN-0438: a gate firing on real drift is the design working). Fail-closed tells you what the denial means; this protocol tells you what to do about it:

1. **Declare the scope first** — read-only; no grant creation, no production change, no gate weakening. Sign in and out with the scope stated.
2. **Name the denial subclass from live data** — never from theory or logs alone. Here: NO_MATCHING_ACTIVE_AUTHORITY, confirmed by querying the live DB (2 active grants exist, neither carries the action).
3. **Specify the exact grant shape** — issuer_id, subject_id, actions, scope target, status, expiry. No grant exists until the director approves it.
4. **Bound the blast radius** — which entities could mutate, which could not (no deletion, no cross-user impact).
5. **Brief the decision-maker** — findings delivered to the parent/director; the investigation creates no permission.

Generalizes: any future authority-gate denial (LAW grants, promotion grants, lock-in grants) gets this protocol before any grant discussion.

## MACHINE NOTE

```json
{
  "sn": "SN-0487",
  "truth_state": "CANDIDATE",
  "law": "authority-gate-denial-investigation",
  "evidence": {
    "board": "#1354",
    "sign_in": 6025353221,
    "sign_out": 6025361447,
    "date": "2026-10-06"
  },
  "denial_subclass": "NO_MATCHING_ACTIVE_AUTHORITY",
  "verification": "live DB: zero grants with learning_lock_in action; 2 active grants for intelligence_commit and naya_node_apply only",
  "grant_shape": {
    "issuer_id": "adfdf0b8-5558-41d1-9fed-ec51abf4fe2f",
    "subject_id": "adfdf0b8-5558-41d1-9fed-ec51abf4fe2f",
    "actions": ["learning_lock_in"],
    "scope_target": "IB-NAYA-FLOW-LESSON-919db63a63784f3ba6bad79c7db1edb7",
    "status": "ACTIVE",
    "expires_at": "future"
  },
  "blast_radius": "block->LEARNED, relationship->VERIFIED/ACTIVE, checkpoint->LEARNED; owner-scoped; no deletion; no cross-user impact",
  "protocol": ["declare read-only scope", "name denial subclass from live data", "specify exact grant shape", "bound blast radius", "brief the director", "create nothing"],
  "companion": "SN-0438 (fail-closed is the design working)"
}
```

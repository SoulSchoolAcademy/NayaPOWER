# IB-SMART-NOTE-20261009-sn0864-orphan-branch-verified-state-sweep-before-canonical-ledger

Intelligent Block: SN-0864
Truth state: CANDIDATE
Scope: PRIVATE
Captured: 2026-10-09
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL

Main's canonical ledger said DEC-006 / 46 events. The verified state — DEC-007, 57 events, with a cold-recompute proof — existed ONLY on a never-PR'd orphan branch from the 7th loop. Main was "canonical" and stale at the same time; nobody had merged wrong, nobody had lied — the verified truth simply never had a PR. Naya 5 closed the gap by cherry-picking commits 5766dda22 and 84fe6e17 onto main. The rule for a cold successor: canonical is a reconciliation result, not a branch name. Before any operation that treats a ledger as canonical — closing a decision batch, certifying a count, asserting "main is the source of truth" — sweep unmerged and orphan branches for later verified states. Merged does not mean latest; unmerged work can hold the only verified state.

Provenance: NayaPOWER #1354 comment 6094442357 ([NAYA 5 — MORNING REPORT], "Cherry-picked the never-PR'd 7th-loop branch (5766dda22, 84fe6e17) onto live main — main's canonical ledger was DEC-006/46 events; the verified DEC-007 state (57 events, cold-recompute proof) existed only on an orphan branch", 2026-10-10T06:00:04Z, SoulSchoolAcademy).

## HUMAN NOTE

The most dangerous lie is a ledger everyone trusts that quietly isn't current. Nobody cheated here — the 7th loop did real work, proved it with a cold recompute, and then the branch just... sat there, un-PR'd, invisible to every "what does main say?" check. Every lane reporting "main says DEC-006" was telling the truth and being wrong at the same time. The fix isn't more diligence about main; it's the habit of asking "where else could the truth live?" before declaring anything canonical. The sweep is cheap; the stale certainty is expensive.

## CHILD NOTE

You keep your score sheet on the fridge, and it says 46 goals. But your brother scored 11 more in the backyard game and wrote them on a napkin that never made it to the fridge. The fridge isn't lying — it just doesn't know about the napkin. Before you announce the final score, check the napkins, not just the fridge.

## GRANDMA NOTE

The official record said the garden grew 46 tomatoes. But nobody checked the side plot behind the shed, where 11 more ripened — because nothing ever grows back there, right up until it does. Before you tell the neighbors the harvest number, walk the whole yard, not just the front garden. The side plot doesn't care that it wasn't in the plan.

## NAYA NOTE

Operational rules:

1. Define "canonical ledger" as the state after a reconciliation sweep, not as "what main's branch says." If the sweep hasn't run, the ledger is a working copy with a confident name.
2. Before closing any canonical batch (decision numbers, event counts, ledger certifications): list unmerged branches touching the same domain and check their heads for later verified states. The orphan branch is the usual suspect — no PR, no merge queue, no one watching.
3. Cherry-pick the verified commits forward onto main (as Naya 5 did with 5766dda22, 84fe6e17) rather than "re-doing" the work — the proof is already in the commit; redoing it loses the cold-recompute provenance.
4. If you find the divergence, say it plainly on the board ("main was DEC-006/46; verified DEC-007/57 lived only on the orphan branch") so every downstream consumer re-reads, and log the sweep as part of the ledger-close receipt.

## MACHINE NOTE

```json
{
  "sn": "SN-0864",
  "truth_state": "CANDIDATE",
  "doctrine": "Before treating any ledger as canonical, sweep unmerged and orphan branches for later verified states; merged does not mean latest, and unmerged work can hold the only verified state. Canonical is a reconciliation result, not a branch name.",
  "falsifiers": [
    "Declaring a ledger canonical from main's branch state alone without sweeping unmerged branches",
    "Re-doing verified work on main instead of cherry-picking the verified commits forward with their proof intact",
    "Assuming no-PR branches contain no verified state"
  ],
  "applies_to": "any lane that closes, certifies, or cites a canonical ledger, count, or decision batch on the repo"
}
```

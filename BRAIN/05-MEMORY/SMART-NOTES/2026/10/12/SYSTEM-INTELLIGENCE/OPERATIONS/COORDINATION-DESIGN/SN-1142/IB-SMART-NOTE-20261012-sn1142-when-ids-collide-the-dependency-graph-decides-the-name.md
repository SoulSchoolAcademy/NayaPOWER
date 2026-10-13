# When IDs Collide, the Dependency Graph Decides the Name — First-Claim Governs Work Claims, Not Identifier Ownership

**Intelligent Block:** IB-SMART-NOTE-20261012-sn1142-when-ids-collide-the-dependency-graph-decides-the-name
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-12
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** [LANE LAW · Naya Judge] #2175 comment 6136174209 (2026-10-13 ~01:37Z, wave 14 · L272): B-48 collision ruling — REAL. Two distinct missions, one ID, both live-referenced: (a) queue line 253 — receipt-gate.yml `on.pull_request.types` missing `edited`/`reopened` (claimed wave 11, 2026-10-12T22:44Z, 9.6/10 SHIP, PR #2494 open, sign-out 6134966036; itself renumbered B-44 → B-48 at 18:39Z); (b) queue line 274 — P0 cold-retrieval false-positive admission (claimed wave 13, 2026-10-13T00:32:49Z, measurement-only). RULING (read-only — main seat performs the rename): on a real collision the main seat renames the ORIGINAL. Here the ID stays with cold-retrieval and receipt-gate renumbers B-48 → B-57 (max B-number in queue = B-56, enumerated live, tip ref-anchored dd6f2d927d) — because B-50 "Depends on: B-48, B-49" and line 300's "Related: B-48 (false-positive admission)" both resolve B-48 → the cold-retrieval mission. Receipt-gate is SHIPPED terminal with PR #2494 as its durable handle.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Two missions collided on the name B-48. Receipt-gate claimed the number first (six hours earlier) — but the dependency chain disagrees: B-50 "Depends on: B-48" and the queue's "Related: B-48 (false-positive admission)" both point at cold-retrieval. So the judge ruled AGAINST first-claim: cold-retrieval keeps B-48, the shipped receipt-gate work renumbers to B-57 with its merged PR as the durable handle. The durable rule: **first-claim-stands governs duplicate WORK claims — but when two missions collide on one ID, the name goes to the holder the dependency graph resolves to.** Naming follows the graph, not the clock; the terminal/shipped holder takes the renumber, never the active one.

## 🩷 HUMAN NOTE

Shawn — the judge just settled a real naming collision. Two missions both got labeled B-48: receipt-gate (claimed it first, six hours earlier, already shipped) and cold-retrieval (claimed it later, still active). The ruling surprised the old rule: first-claim did NOT win. The deciding evidence was the dependency graph — B-50 lists "Depends on: B-48" and the queue references "B-48 (false-positive admission)", and both of those mean cold-retrieval. Keeping receipt-gate on B-48 would have corrupted the depends-on chain and dispatched work into the wrong place. So: cold-retrieval keeps B-48, receipt-gate becomes B-57 (its PR is the durable handle). First-claim-stands still rules duplicate work claims — but when the fight is over a NAME, the dependency graph is the judge.

## 🟣 CHILD NOTE

Two kids both wrote their name on the same locker tag! The first kid claimed it earlier — but the school's map already points that tag to the second kid's locker: the map says "your gym class meets at THIS locker." If the first kid kept the tag, everyone going to gym would end up at the wrong locker! So the rule: when the name belongs to a place on the map, the map decides who keeps it — not who wrote first. The kid whose work is already done gets a new tag; their old homework folder keeps their name so nothing is lost.

## 👵 GRANDMA NOTE

It's like two houses on the street ending up with the same number. The one that painted the number first says "I was here first" — but the post office's records already route that address's mail to the second house, and delivery routes reference it. Repainting the second house would send the mailman to the wrong door forever. The right fix: the house that's already finished and settled (its sale papers carry the full history) gets renumbered, and the house everyone depends on keeps the address. The directory, not the paintbrush, settles address disputes.

## 🤖 NAYA NOTE

This refines the existing collision doctrine, which until now had two tools: (1) `collision_registry_first_claim_stands` (duplicate work claims → first claim stands, later ones stand down or consolidate); (2) "never let both ride to the merge gate" (announce openly). Both govern WORK collisions. The B-48 case is an IDENTIFIER collision — and the judge's ruling adds the missing third rule: **when two missions collide on one identifier, the identifier stays with the holder the dependency graph resolves to; the terminal/shipped holder renumbers.** Why this direction matters mechanically: identifiers are load-bearing in the dispatch machinery (queue "Depends on: B-48" lines are consumed as routing). Corrupting the graph-reference (keeping receipt-gate on B-48) would dispatch future work into a CI-trigger fix — a dispatch hazard — while renaming cold-retrieval would orphan every existing B-48 reference across venue sign-outs. The terminal holder (receipt-gate: SHIPPED, PR #2494 open as durable handle) has zero live references to protect; the active holder has many. Selection criteria for the rename target, in order: (1) dependency-graph resolution (what the existing references MEAN), (2) activity polarity (active keeps, terminal renumbers), (3) durable handle availability (the renumbered party keeps its PR/artifact as the name-independent handle). First-claim-stands is unaffected for its proper domain: work claims.

## ⚙️ MACHINE NOTE

```json
{
  "sn": "SN-1142",
  "lesson": "when-ids-collide-the-dependency-graph-decides-the-name",
  "rule": "When two missions collide on one identifier, the identifier stays with the holder the dependency graph resolves to; the terminal/shipped holder renumbers (keeping its PR/artifact as the durable handle). First-claim-stands governs work claims, not identifier ownership.",
  "failure_class": "identifier collision resolved by the wrong doctrine (claim-timestamp instead of dependency-graph resolution)",
  "evidence": {
    "ruling": "#2175 comment 6136174209 (Naya Judge, wave-14 L272, 2026-10-13 ~01:37Z): B-48 collision REAL, READ-ONLY ruling (main seat performs rename)",
    "holder_a": "queue line 253 — receipt-gate.yml on.pull_request.types missing edited/reopened; claimed wave 11 2026-10-12T22:44Z (~6h earlier); 9.6/10 SHIP; PR #2494 open; sign-out 6134966036; renumbered B-44→B-48 at 18:39Z",
    "holder_b": "queue line 274 — P0 cold-retrieval false-positive admission; claimed wave 13 2026-10-13T00:32:49Z; ACTIVE (venue sign-outs cite B-48/B-49/B-51)",
    "graph_evidence": "B-50 'Depends on: B-48, B-49' + line 300 'Related: B-48 (false-positive admission)' both resolve B-48 -> cold-retrieval",
    "rename_target": "receipt-gate B-48 -> B-57 (max B-number = B-56, enumerated live, tip ref-anchored dd6f2d927d); PR #2494 is the durable handle"
  },
  "repair_doctrine": "Identifier-collision resolution order: (1) dependency-graph resolution — what do the existing references MEAN; (2) activity polarity — active keeps, terminal renumbers; (3) durable handle — the renumbered party keeps its PR/artifact as name-independent handle. Do not apply first-claim-stands to identifiers.",
  "related": ["collision_registry_first_claim_stands (work claims)", "never let both ride to the merge gate (duplicate work)"]
}
```

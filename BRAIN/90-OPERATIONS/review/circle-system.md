# THE CIRCLES SYSTEM — smart links: everything links to everything relevant

**Shawn's order, 2026-10-15:** GitHub must be navigable the way a Naya thinks. Not a taxonomy — her actual questions. When she asks "my merge is stuck," she lands on the diagnostic, and everything relevant is one hop away. Circles, not dead ends.

## The invariant
Every load-bearing document belongs to at least one **circle** — a topic cluster organized around the question a Naya actually asks. Each circle has a **hub** (the entry point — the doc she opens first) and **members** (everything relevant). The hub links to every member; every member links back to the hub. Bidirectional, always. A link that doesn't come back is a dead end, and dead ends are bugs.

## Why hubs, not meshes
A full mesh needs O(n²) links and rots the moment one doc moves. A hub needs O(n) and IS the navigation: one page that answers "you're dealing with X — everything you need is here." The hub is the circle's front door.

## The rule for new docs
When you create a load-bearing doc, you declare its circle in the same motion: which question it answers, which hub it joins (or why it founds a new one). A doc with no circle is an orphan — it doesn't ship until it's circled. The dock/area owner curates their circles: new problems, new members, same hub.

## The checker
`hidden_files/bin/check_circles.py` verifies every declared circle: the hub exists, every member exists, the hub links to every member, every member links back to the hub. Run it before any docs PR merges. A circle that fails the check doesn't merge.

## The pattern this models (Shawn, 2026-10-15)
Whenever there's an issue, it's an opportunity: create the system / flow / feed / code that solves it — then tell the other Nayas on the feed what you built and why, so they can use it. Set the example; they'll follow it. Systems compound when builders announce.

## Declared circles

### merge-circle (the worked example — first circle)
- **Question:** "My merge is stuck / how do merges work here?"
- **Hub:** Merge Ops Manual, human tongue — the diagnostic engine (Naya Resolve, PR #2637; on merge: `BRAIN/90-OPERATIONS/ops-manuals/merge-ops.human.md`)
- **Members:**
  - `merge-ops.ai.md` — full procedures (same PR)
  - `merge-ops.machine.json` — the diagnostic table, machine-first (same PR)
  - Field manual #14 (Merging) — the behavioral discipline: how a Naya ACTS when merges stall (`hidden_files/operations-manuals/14-merging.md`; repo path on manual PR)
  - SN-01396 — the merge-flow doctrine (protection balance, triage law)
  - The Merge Incident Feed — append-only jam log (lives in field manual #14; mirrored from the ops manual's feed)
- **Owner:** the dock (merge lane) curates; Naya Resolve owns the ops manual.
- **Status:** FORMING — hub is PR #2637 (open); circle completes when it merges and the back-links land.

*(More circles get declared as the Librarian works the 20 dead-ends from Phase 1 — this file is the format, the merge circle is the example.)*

```circles
[
  {
    "id": "merge-circle",
    "question": "My merge is stuck / how do merges work here?",
    "hub": "BRAIN/90-OPERATIONS/ops-manuals/merge-ops.human.md",
    "members": [
      "BRAIN/90-OPERATIONS/ops-manuals/merge-ops.ai.md",
      "BRAIN/90-OPERATIONS/ops-manuals/merge-ops.machine.json",
      "hidden_files/operations-manuals/14-merging.md"
    ],
    "owner": "merge-dock",
    "status": "FORMING"
  }
]
```

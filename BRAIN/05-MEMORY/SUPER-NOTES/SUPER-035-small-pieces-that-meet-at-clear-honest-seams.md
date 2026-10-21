# SUPER NOTE — Small Pieces That Meet at Clear, Honest Seams

> **The essence layer: 71 distilled Super Notes.** Raw Smart Notes live in the archive; the Hub wall shows these essences. Nothing here deletes or replaces any raw note.

| Field | Value |
|---|---|
| Super Note ID | `SUPER-035` |
| Hub wall row | `public.hub_smart_notes` ib_id `SUPER-035` |
| Human title | Small Pieces That Meet at Clear, Honest Seams |
| Layer | ESSENCE — distilled from raw Smart Notes, never a raw capture |
| Distilled | 2026-10-21 — corrective distillation drive (639 raw → 71 essences); REPAIRED 2026-10-21 after independent audit found 42 MISSING + 151 PARTIAL — lost lessons restored from the originals (see REPAIR-LOG); coverage map regenerated mechanically from these files |
| Sources | 12 raw notes (full list below) |
| Cluster file | `cluster-04-super.json` |
| Canonical machine object | Hub DB row `public.hub_smart_notes` + `distill/all-super-notes.json` |
| Human projection | This Markdown file |
| Sync note | NOT ingested by hub-sync (its watcher parses only `BRAIN/05-MEMORY/SMART-NOTES`); archive + queue untouched |

---

## ✦ IN A NUTSHELL

Build many small pieces instead of one giant lump — but the pieces only work if everyone agrees exactly how they plug together, checks the real plug, and changes shared rules together, all at once.

---

## 🩷 HUMAN NOTE

Beautiful rooms that were never actually called by the shell. A shared list where two writers overwrote each other and lost entries. A small change in the center whose effects quietly broke distant tests. Every failure lived at a seam, not inside a piece. So: agree the connection contract first, and verify it against the live system, not a description of it. Whoever actually sees the data does the sealing. Bridges carry things across; they don't judge them. When a shared rule changes, every piece that depends on it moves in the same step — and names, spellings, and places are never invented for convenience.

---

## 🟣 CHILD NOTE

Think of building blocks with special connectors. The blocks are easy — the connectors are where things break. So everyone agrees on the exact connector shape first, and checks it on the real toy, not a picture of the toy. And if the connector shape ever changes, every block that uses it gets changed at the same time, together.

---

## 👵 GRANDMA NOTE

It's like a quilt made by many hands. Each square can be lovely, but if the edges don't match, it isn't a quilt. So the sewers agree on the edges first, check them against the real cloth, and when the pattern changes, they change every square it touches — in the same sitting, not someday.

---

## 🤖 NAYA NOTE

Naya verifies the consumer's actual mount contract from live bytes before claiming any integration, and builds rooms as modules against a frozen contract instead of standalone apps stitched later. She composes at the consumer, keeps bridges transport-only, and assigns hashing and sealing to the layer that observes the bytes. Shared-contract changes ship as one atomic unit across every consumer; registry writes are serialized and committed atomically; consumers broaden before producers change a shared spelling.

---

## WHAT IT MEANS

In a system built by many hands, the pieces are rarely the problem — the promises between pieces are. A seam is a promise about shape, timing, and meaning, and an unverified promise is just hope with good formatting. Treating seams as first-class work — contracted, checked against reality, changed atomically — is what lets many builders move in parallel without quietly building different systems.

---

## WHAT'S IN IT FOR YOU

Things actually connect. The room you open is the room that was built, your entries don't vanish when two people save at once, and an improvement in one place doesn't silently break another. Parallel work stops meaning parallel confusion.

---

## HOW IT APPLIES

Write the connection agreement before building the pieces, then test the agreement on the live system. Keep each piece small and owned. Let the layer that sees the real data do the sealing, and keep bridges dumb and honest. When a shared rule must change, list every dependent piece and move them together — or don't move yet.

---

---

## ⟲ RESTORED BY REPAIR — 2026-10-21

> Restored by the distillation repair after the independent essence audit (distillation-audit-20261021) found the lessons below MISSING from, or only partially carried by, this Super Note. Each entry restores the named source note's own rule in checkable words, traced to that source. Nothing here is new doctrine.

### SN-0214 — One Hub-Mounting Convention: Rooms Project Canonical Records, Never Copies [audit: PARTIAL → lost element restored]

The hub shell and every room integrate through one mounting convention: the shell calls a loader, the loader returns `{records, errors}`, the shell passes them as `ctx`, and the room mounts via `NayaRooms.x(el, ctx)` — in the Room 02 instance, `ReportsLoader.loadDaily({from, to, base}) → {reports, errors} → ctx.reports → window.NayaRooms.reports(el, ctx)`. A room projects the canonical Brain records and never duplicates canonical content into a private store: the room's store is derived from the loader's view of the canonical source at mount time, so the shell owns the data contract and the room owns only the rendering. The contract is agreed before implementation — no shell changes and no merges from the proposing lane.

### SN-0220 — Intelligent Block [audit: MISSING → restored in full]

Close a flow with the smallest entry contract that makes it real — and never let a suggestion masquerade as an action. The entry contract is `window.NayaRooms.smartSpaces.createAround({kind, id, title})`: it opens the create-space modal pre-filled (name, topic, and block pre-selected, with a "Gathered around: …" label), and the human still names the space and taps CREATE. Prefill is a suggestion; the human's tap is the action. The system must never auto-create, manufacture its own "NEXT" buttons, or otherwise invent commitments the human never made — a prefill that fires itself is a commitment without consent. Standalone pages honor the same contract via `?around=ID`, and the shell adapter forwards the call so any room can use it without touching Spaces' internals.

### SN-095 — Compose at the Consumer — Authorship Stays in the Author, Trust Stays in the Seal [audit: PARTIAL → lost element restored]

Compose at the consumer means: the consumer derives its answer from the producer's sealed facts instead of the producer emitting pre-formed answers. In the VERIFY→LEARN case, do not teach VERIFY to emit an `outcome.lesson` — that moves lesson-authorship into VERIFY and inverts the separation (VERIFY verifies, LEARN learns). Instead `LEARN.extract()` reads the `learn_baton` and derives the lesson from VERIFY-owned facts: eligibility is `learn_baton.may_use` non-empty (= VERIFIED_PASS; FAIL/REOPENED land on `must_not_generalize`), and the lesson is only `subject_ref.claim` — the verified fact VERIFY sealed. No caller-controlled labels cross the trust boundary, and the seal must cover the content it protects: finalize outcomes before `close()` seals, and reject derived scope exceeding the verified `subject_ref`. Authorship stays in the author; trust stays in the seal.

### SN-096 — The Composition Root Owns the Bridge — It Transports, It Doesn't Judge [audit: PARTIAL → lost element restored]

The bridge belongs to the composition root — never bolt it silently into one of the endpoints. Verify edges as code: a declared edge with zero callers is an ordering declaration, not a data bridge — in the source case `EVOLVE.observe()` had zero callers in `naya_kernel/`, and the `("LEARN", "EVOLVE")` entry in `REQUIRED_EDGES` was ordering plus `SATISFIED`/`BLOCKED` trace labels, not plumbing. Give the bridge to the composition root as a real named method with a real contract — `Kernel.promote_learning_to_evolution(learning_id)` constructs the full gap dict and returns the downstream `evolution_id` — and let it transport without judging: semantic qualification stays with the caller.

### SN-101 — SMART NOTE — Platform Identity Semantics [audit: MISSING → restored in full]

Identity comparisons must use the platform's identity semantics, not the programming language's default equality: first establish the platform's canonicalization rules, then normalize-then-compare. GitHub repository identity is effectively case-insensitive, so a case-sensitive `owner_repo == upstream_repo` comparison (PR #1265) let a casing variant masquerade as a distinct owner target. The repair is case-insensitive comparison, with a regression test built around the adversarial casing variant. A stricter-than-platform comparison is not safer — at authority boundaries an identity mismatch is a security hole.

## SOURCES (traceability — every raw note this essence was distilled from)

- `IB-SMART-NOTE-20260930-sn0218-mount-contract`
- `IB-SMART-NOTE-20260930-sn0214-hub-room-mounting-contract`
- `IB-SMART-NOTE-20260930-sn0142-modules-not-apps`
- `IB-SMART-NOTE-20260930-sn0220-gather-around-entry-contract`
- `IB-SMART-NOTE-20260930-sn095-compose-at-the-consumer`
- `IB-SMART-NOTE-20260930-sn096-composition-root-owns-bridge`
- `IB-SMART-NOTE-20260930-sn069-bindings-at-the-observing-layer`
- `IB-SMART-NOTE-20260930-sn101-platform-identity-semantics`
- `IB-SMART-NOTE-20261005-sn0416-kernel-contract-seam`
- `IB-SMART-NOTE-20261005-sn0335-serialize-registry-writes-flock-atomic-commit`
- `IB-SMART-NOTE-20261004-sn0256-placement-is-architecture-never-invent-locations`
- `IB-SMART-NOTE-20261004-sn0284-convention-coherence`

# SUPER NOTE — Fix the Real Seam, Not the Nearest One

> **The essence layer: 71 distilled Super Notes.** Raw Smart Notes live in the archive; the Hub wall shows these essences. Nothing here deletes or replaces any raw note.

| Field | Value |
|---|---|
| Super Note ID | `SUPER-023` |
| Hub wall row | `public.hub_smart_notes` ib_id `SUPER-023` |
| Human title | Fix the Real Seam, Not the Nearest One |
| Layer | ESSENCE — distilled from raw Smart Notes, never a raw capture |
| Distilled | 2026-10-21 — corrective distillation drive (639 raw → 71 essences); REPAIRED 2026-10-21 after independent audit found 42 MISSING + 151 PARTIAL — lost lessons restored from the originals (see REPAIR-LOG); coverage map regenerated mechanically from these files |
| Sources | 12 raw notes (full list below) |
| Cluster file | `cluster-02-super.json` |
| Canonical machine object | Hub DB row `public.hub_smart_notes` + `distill/all-super-notes.json` |
| Human projection | This Markdown file |
| Sync note | NOT ingested by hub-sync (its watcher parses only `BRAIN/05-MEMORY/SMART-NOTES`); archive + queue untouched |

---

## ✦ IN A NUTSHELL

When something fails, find the exact joint where it breaks and repair that — in the real system people actually use. Fixing a look-alike copy, or guessing before you've looked, leaves the real break exactly where it was.

---

## 🩷 HUMAN NOTE

The pattern repeats: a test stays red even after the missing piece is added — because the break is in the host's joint, not the piece. A reported gap turns out to be already fixed when someone finally looks at the current version. A careful fix lands in a reference copy while the production path keeps its hole. A lookup tool quietly prefers whatever is newest over whatever is truest. And sometimes the most valuable deliverable is the investigation itself: discovering the thing you're asked to fix can't even be located, and refusing to ship against a guess. Trace the whole chain, stop at the first real break, and fix it there.

---

## 🟣 CHILD NOTE

If the lamp won't light, you check the cord, the plug, the bulb — in order — and fix the first broken part you find. You don't buy a new lampshade. And you don't guess in the dark; you look.

---

## 👵 GRANDMA NOTE

A good repairman doesn't replace parts hoping, dear. He follows the trouble to its source and fixes that one thing, in the real house — not in a model of the house. And sometimes the honest answer is 'I can't find it yet.'

---

## 🤖 NAYA NOTE

Naya traces the whole chain and stops at the first exact failing handoff, never inventing past a gap. Before designing a repair she re-checks whether the gap still exists at the current version — some close as simply stale. She heals the canonical production seam rather than a reference twin, tests the real questions people actually ask against the live system, and exhausts what her current instruments can already observe before building new ones.

---

## WHAT IT MEANS

Systems break at joints — the handoffs between parts — and each part alone can look healthy while the connection fails. Repairs aimed at the wrong joint consume effort and create false confidence, while the real seam keeps failing quietly. Root-cause discipline is what turns fixing from a recurring cost into compounding knowledge.

---

## WHAT'S IN IT FOR YOU

Problems stay fixed. You stop paying for the same break three times, and each repair teaches you where your system is genuinely weak — which is where the next improvement lives.

---

## HOW IT APPLIES

When something fails, walk the chain in order and name the first exact break before fixing anything. Re-verify the problem still exists before repairing it. Fix the version people actually use, and when the source of truth can't be found, say so plainly instead of shipping against a guess.

---

---

## ⟲ RESTORED BY REPAIR — 2026-10-21

> Restored by the distillation repair after the independent essence audit (distillation-audit-20261021) found the lessons below MISSING from, or only partially carried by, this Super Note. Each entry restores the named source note's own rule in checkable words, traced to that source. Nothing here is new doctrine.

### SN-0174 — The Comprehension Assertion Is the Proof's Live Boundary [audit: MISSING → restored in full]

The comprehension assertion on the held-out cold-successor retrieval is the proof's live boundary. In Live Intelligence Commit Proof's first main run, `fresh-lesson` and `independent-verification` passed but `cold-successor-held-out` failed at `assert comprehension["understands_raw_source_separate"]` — the held-out successor did not demonstrate it understands the raw source as separate from its own synthesis. Passing mechanics are only plumbing, not proof. Record the exact failing coordinates (run/job/assertion/exit) so the next operator triages the gate, not the pipeline. Record by-design side effects as by-design when they look surprising, and open no repair work against them. Missing-artifact failures downstream of a skipped job are composition gaps that license no inference. A preflight-only SUCCESS with all behavioral jobs skipped proves nothing behavioral — label it exactly.

### SN-0445 — The Evidence You Cannot Reach Is Not Evidence You Have — the Production DB Is Agent-Unobservable [audit: MISSING → restored in full]

The production DB is agent-unobservable: no agent seat can run the query that would verify whether a migration was actually applied. The ledger is a CLAIM; the database is TRUTH; and there is no agent-side bridge between them. A ledger entry claiming PRODUCTION_APPLIED therefore stays UNVERIFIED, and the DB-side truth stays UNKNOWN — never asserted from the ledger alone, never inferred from the deploy stamp, never "probably applied." Route every such claim through the director's standing Query A, the only bridge that exists, and cite his answer with its timestamp. Unknown ≠ pass; implemented ≠ verified; ledger-says-applied ≠ production-proven.

### SN-0449 — Retrieval First, Authority Second — Test the Experiment's Actual Queries Against the Live Index Before Designing Around It [audit: PARTIAL → lost element restored]

Rank retrieval by (relevance score, truth-state rank, recency): relevance first — score stays primary, so a highly relevant CANDIDATE still beats a barely relevant RATIFIED note — truth-state or authority breaks relevance ties second (RATIFIED=2, VERIFIED=1), and recency is last. Corpus feeding and ranker repair are separate jobs: no ranker retrieves what was never indexed, and neither job alone fixes retrieval — do not declare retrieval fixed after only one.

### SN-0497 — IB-SMART-NOTE-20261006-sn0497-one-retrieval-rpc-transparent-scoring-relationships-traverse-no-authority-created [audit: MISSING → restored in full]

Build retrieval as one retrieval RPC with transparent weighted scoring: the `nayanet_retrieve_blocks()` RPC scores 0.50 text + 0.25 applicability + 0.15 truth-state + 0.10 recency, with a cold-start default, over a trigger-maintained weighted tsvector — built on the existing block row instead of a second system. Relationships traverse: SUPERSEDES chains resolve to the live successor (a superseded draft is never served without its successor), allowlisted SUPPORTS/REFINES edges attach context, and CONTRADICTS/INVALIDATES surface as conflicts — never merged. Retrieval creates no authority; the receipt is best-effort.

### SN-0517 — A Stub That Is Merely Close Produces a 500 That Looks Like a Product Defect [audit: MISSING → restored in full]

When a fired test blames the system under test, the stub itself is the prime suspect before any product patch. Four separate harness bugs each masqueraded as a product defect — a `Deno.env.get` stub returning the credential error for unknown keys, a stateless GET stub returning 404 for the verify read as well as the head read, a receipts stub lacking `.select()` on the update chain, and a claim INSERT always returning a fresh `processing` row — and each time the fix was to the harness, not the product. Before any patch, ask "is my stub merely close?" — enumerate the harness seams: credential resolution stubs, statefulness of mocked GETs, ORM chain completeness, INSERT-returned row freshness. A stub that is merely close produces a 500 that looks like a product defect.

### SN-064 — Spec Outruns Kernel — Forward-Gap Discipline at Lock [audit: MISSING → restored in full]

Spec amendments made while the kernel is frozen can outrun it: a forward gap is where the amended spec requires functions the kernel does not implement, and it must be named as a forward gap rather than assumed implemented. At every spec-amendment lock, run a read-only alignment check of the amended spec head against the frozen implementation head, and record the CLEAN case line-by-line as the alignment bar. For each forward gap, search both spec and implementation for a stated layering boundary: if none exists, either document the boundary (naming which layer owns the missing function) or implement the function in a checkable place before lock — an undocumented boundary is indistinguishable from a defect. Watch for the contradiction form: an implementation satisfying the exact formula the spec says is insufficient is a direct conflict, needing an implementation or spec change before lock. Forward gaps go on the implementation PR's merge checklist; they do not block demos or walkthroughs. Examples kept named: ACT's five deliberative functions with no kernel implementation under any name — `plan_action`, `select_minimum_sufficient_action`, `define_expected_outcome`, `define_proof_requirements`, and `observe` as a callable function — and LEARN's `promote()` direct-assigning VERIFIED after enforcing the promotion formula the spec says is not sufficient alone.

## SOURCES (traceability — every raw note this essence was distilled from)

- `IB-SMART-NOTE-20261007-sn0548-heal-the-canonical-seam-not-the-reference`
- `IB-SMART-NOTE-20260930-sn093-first-failing-handoff`
- `IB-SMART-NOTE-20260930-sn102-import-still-red-experiment`
- `IB-SMART-NOTE-20260930-sn0226-close-the-gap-as-stale-before-designing-the-repair`
- `IB-SMART-NOTE-20260930-sn064-spec-outruns-kernel-forward-gaps`
- `IB-SMART-NOTE-20260930-sn0174-comprehension-assertion-live-boundary`
- `IB-SMART-NOTE-20260930-sn0445-db-is-agent-unobservable`
- `IB-SMART-NOTE-20260930-sn0501-investigation-is-deliverable`
- `IB-SMART-NOTE-20260930-sn0517-stub-merely-close-masquerades-as-product-defect`
- `IB-SMART-NOTE-20261006-sn0449-retrieval-relevance-first-authority-second`
- `IB-SMART-NOTE-20261006-sn0497-one-retrieval-rpc-transparent-scoring-relationships-traverse-no-authority-created`
- `IB-SMART-NOTE-20261006-sn0516-exhaust-the-existing-instrument-before-building-a-new-one`

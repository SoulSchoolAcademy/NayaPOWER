# The Composition Root Owns the Bridge — It Transports, It Doesn't Judge

**Intelligent Block:** IB-SMART-NOTE-20260930-sn096-composition-root-owns-bridge
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-01
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #554 comment 5939370485 ([NAYA 2] follow-up: LEARN→EVOLVE has no data bridge yet at `384df875`, 2026-10-01) diagnostic + #554 comment 5939478418 ([NAYA 4] LEARN→EVOLVE bridge — deliberate, not bolted on, at `5758daef9f87e8acf161431c181cd1b491be411d`, parent `ad04661e700a28795e650267d4d78c55d612195c`, PR #1216 draft) implementation.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Naya 2 flagged a structural fact before Naya 4 could discover it the hard way: **`EVOLVE.observe()` is never called by any code in `naya_kernel/`** (`grep -rn "\.observe("` excluding the definition: zero hits). The LEARN→EVOLVE data handoff did not exist as a method call — only as the declared graph edge `("LEARN", "EVOLVE")` in `REQUIRED_EDGES`. `Kernel.decide()` moves no data between nodes: `_run_gate` calls `node.gate(sub_state)` per node; edges are ordering constraints (upstream must PASS before downstream is evaluated) plus receipt-trace labels (`SATISFIED`/`BLOCKED`), not plumbing. So the graph edge was a *declared ordering*, not a *data bridge* — fixing `extract` alone would not have unblocked handoff 7. The diagnostic also named the open questions: semantic (is a learning a "gap"?) and architectural (who owns the bridge — Kernel pipeline method, explicit composition function, or documented manual step?). Flagged *before* the extract fix so the composition commit could scope the bridge deliberately instead of discovering its absence at the next trace. Naya 4 answered it as a deliberate design, not a silent bolt-on: **`Kernel.promote_learning_to_evolution(learning_id)`** — the composition root owns the bridge. It gets the learning from LEARN, constructs a proper gap dict (`gap_id`, `source: "LEARN"`, `learning_id`, `lesson`, `scope`, `verification_receipt_refs`, `observed_at`), calls `EVOLVE.observe(gap)` → returns `evolution_id`. The nine-organ cycle test now drives the bridge (not a direct `observe()` call), proving the full chain `CONNECT → VERIFY → LEARN → EVOLVE` with genuine data at every handoff; full suite at `5758daef`: 1135 passed, 3 skipped, 0 failed. And the deliberate part: the bridge **transports, it doesn't judge** — whether every learning qualifies as a "gap" is a decision for the caller to make; the bridge documents the open semantic question instead of answering it silently. The lesson: edges in a dependency graph are ordering declarations, not data plumbing — when a handoff needs data, name the bridge explicitly, give it to the composition root (the only party that can see both ends), make it a real method with a real contract, and let it transport without judging — semantic qualification stays with the caller.

## 🩷 HUMAN NOTE

Imagine a factory where the blueprint says "station A hands off to station B" — but nobody built the conveyor belt. The stations are in the right order, the schedule is right, but no part can actually travel between them. The fix wasn't to quietly nail a plank between the stations and hope; it was to name the missing belt, assign its ownership to the one role that can see both stations (the plant manager, not either station crew), build it as a proper piece of equipment with a manifest (what's on the belt, where it came from, when it left), and write down the one question nobody should answer silently: "does every load from A count as a delivery for B?" That question stays with whoever runs the plant that day. A declared handoff is not a working handoff — until someone owns the bridge, and the bridge stays honest about what it doesn't decide.

## 🟣 CHILD NOTE

Imagine nine kids standing in a row for a relay race, but between two of them there's a river — and nobody built a bridge. The lineup is perfect, the batons are ready, but the runner can't cross the water. You don't just throw some sticks down and pretend it's a bridge; you *build a real bridge*, you put it where the teacher (who can see the whole race) says it goes, you write down exactly what crosses it, and you leave one honest sign on it: "This bridge carries things across — it doesn't decide what counts as a delivery. The teacher decides that." A line on a map is not a bridge. Only a real bridge with a real owner crosses the river.

## 🔵 GRANDMA NOTE

It's like a family recipe book that says "serve with the Sunday sauce" — but nobody wrote down who makes the sauce or how it gets to the table. Everyone assumed someone else had it covered. The answer isn't to quietly toss a jar on the table and hope; it's to give the job to one named person — the host, who can see both the kitchen and the table — with a clear dish and a label, and to write honestly: "the host delivers the sauce; whether every batch qualifies for Sunday dinner is the cook's call, not the host's." A line in the book is a promise; only a named owner makes it a reality. And the honest part is naming what the bridge *doesn't* decide, in writing.

## 🟠 NAYA NOTE

Apply this to every declared-but-unplumbed edge: (1) verify edges as code, not as intent: `grep` for the actual method call — a declared edge in `REQUIRED_EDGES` with zero callers is an ordering declaration, not a data bridge; flag it before the next fix commits so the composition work scopes it deliberately (SN-057 lineage: timestamp the read — `384df875` — so the claim binds the artifact, not the branch); (2) give the bridge to the composition root — the Kernel, pipeline, or explicit composition function — never bolt it into one of the endpoints, because the bridge is nobody's node-local business; (3) make it a real named method with a real contract: `promote_learning_to_evolution(learning_id)` constructs a full dict (`gap_id`, `source`, `learning_id`, `lesson`, `scope`, `verification_receipt_refs`, `observed_at`) and returns the downstream id — the bridge's shape is reviewable, its inputs inspectable; (4) transport, don't judge: document the open semantic question ("is a learning a 'gap'?") in the method and leave qualification to the caller — a bridge that silently decides semantics is a judgment smuggled past review; (5) prove it end-to-end: the cycle test drives the bridge itself, not a direct `observe()` — the test must use the composition path the architecture claims; (6) in the e2e trace, an unowned bridge reads "BLOCKED (no bridge)" — an honest gap, not an invented completion (SN-090/093 lineage). Family note: SN-095's twin — there the lesson was *where derivation lives* (the consumer); here it is *where plumbing lives* (the composition root). Both say: boundaries are crossed by named, owned, honest mechanisms — never by assumption.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "declared_but_unplumbed_edge",
  "evidence": {
    "board": "#554 comment 5939370485 (2026-10-01) — Naya 2's pre-fix diagnostic at 384df875: EVOLVE.observe() zero callers in naya_kernel/; Kernel.decide()/_run_gate moves no data between nodes (edges = ordering constraints + SATISFIED/BLOCKED trace labels); fixing extract alone would not unblock handoff 7; semantic (is a learning a 'gap'?) and architectural (who owns the bridge?) questions named; flagged before the extract fix. #554 comment 5939478418 — Naya 4's deliberate design at 5758daef: Kernel.promote_learning_to_evolution(learning_id) — composition root owns the bridge; builds gap dict (gap_id, source:'LEARN', learning_id, lesson, scope, verification_receipt_refs, observed_at); calls EVOLVE.observe(gap); documents the open semantic question; bridge transports, doesn't judge. Cycle test uses the bridge, not direct observe(); full suite 1135 passed, 3 skipped, 0 failed."
  },
  "rule": [
    "verify edges as code: a declared edge with zero callers is an ordering declaration, not a data bridge — flag it before the next fix commits",
    "give the bridge to the composition root — never bolt it silently into one of the endpoints",
    "make the bridge a real named method with a real contract: full dict in, downstream id out",
    "transport, don't judge: document open semantic questions in the method; leave qualification to the caller",
    "prove the bridge end-to-end through the composition path the architecture claims",
    "in e2e traces, an unowned bridge reads BLOCKED — an honest gap, never an invented completion"
  ],
  "lesson_line": "A declared edge is not a data bridge — name it, give it to the composition root, and let it transport without judging."
}
~~~

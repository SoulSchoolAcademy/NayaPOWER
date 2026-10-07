# Machine-Readable Artifact Governs When Prose Minimums Under-Specify

**Intelligent Block:** IB-SMART-NOTE-20260930-sn023-seed-authority-over-prose
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-09-30
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

When a governance lock's prose states minimums and its machine-readable artifact states a larger set, the artifact is the authoritative set and the prose minimums are the required floor — not the ceiling. Case in point: the Ultimate Lock's prose lists 11 minimum runtime routes, while the machine-readable seed `BRAIN/04-INTELLIGENCE/GRAPH/0001-KERNEL-GRAPH-SEED-V1.json` carries 13 edges (the 11 plus ACT→KNOW (PRODUCES) and LAW→EVOLVE). The reading adopted: implement the seed's 13-edge graph; the 11 are the mandatory subset. The reading was flagged openly on the board ("shout if that reading is wrong") rather than silently chosen, so a seat that disagrees can correct it before code is written.

## 🩷 HUMAN NOTE

Shawn's governance documents sometimes say the same thing twice — once in human prose, once in a machine-readable file — and the two can disagree in scope. Prose tends to state the minimum ("at least these"), while the artifact states the full set ("exactly these"). When they differ, trust the artifact as the authoritative definition and treat the prose minimums as the floor you must at least meet. And if the reading is your judgment call, say so out loud: "I'm treating X as authoritative; shout if that reading is wrong." A flagged reading can be corrected in minutes; a silent one becomes a hidden assumption that ships in code.

## 🟣 CHILD NOTE

If the rules are written in two places and one says more than the other, follow the one with more detail — but tell everyone that's what you did, so they can correct you if you're wrong.

## 🔵 GRANDMA NOTE

When the instruction sheet and the detailed list disagree, go with the detailed list — it's the one the machine actually follows. And always say out loud which one you chose, so someone else can catch it if you misread.

## 🟠 NAYA NOTE

Governance artifacts outrank governance prose in scope disputes: implement the machine-readable seed, satisfy the prose minimums as a floor. Never silently resolve an authority ambiguity between two canonical sources — post the reading with an explicit invitation to correct it, so the correction happens before implementation effort compounds the error. The same discipline applies wherever two canonical sources coexist (specs vs. schema, directive prose vs. routing table, README claims vs. contract fields).

## 🟢 MACHINE NOTE

~~~json
{
  "domain": "governance_document_interpretation",
  "rule": "artifact_authoritative_set_prose_minimums_are_floor",
  "instance": {
    "lock": "BRAIN/03-KERNEL/0005-NINE-NODE-ULTIMATE-LOCK-AND-NOTE-READINESS-V1.md",
    "prose_claim": "11 minimum runtime routes (SELF→LAW; SELF→KNOW; LAW→ACT; ACT→VERIFY; KNOW→PROVE; KNOW→CONNECT; PROVE→VERIFY; CONNECT→VERIFY; VERIFY→LEARN; LEARN→EVOLVE; EVOLVE→SELF)",
    "artifact": "BRAIN/04-INTELLIGENCE/GRAPH/0001-KERNEL-GRAPH-SEED-V1.json",
    "artifact_claim": "13 edges — the 11 minimums PLUS ACT→KNOW (PRODUCES) and LAW→EVOLVE",
    "adopted_reading": "implement the seed's 13-edge graph as the decide() topology; the 11 are the required minimum subset",
    "reading_status": "announced on #554 with explicit correction invitation; CANDIDATE"
  },
  "constraints_preserved": [
    "fail_fast_and_fail_closed_per_edge",
    "no_weakened_gates_during_re_topologizing",
    "lock_semantics_win_over_branch_implementation"
  ],
  "conflict_with": "any note or habit that treats prose summaries as ceilings"
}
~~~

## 🟢 LEARNING LESSON

Prose in a governance document summarizes; the machine-readable artifact specifies. When they differ in scope, the ambiguity is itself intelligence worth capturing — and the only safe way to resolve it is to state the reading publicly with an explicit correction channel, because every implementation choice downstream of the reading multiplies the cost of being wrong.

## 🟡 WHAT IT MEANS

Future seats reading a lock, directive, or contract that ships both prose and a machine-readable form should default to the artifact as the governing set, with prose minimums as the floor. This prevents two failure modes: under-implementation (treating a minimum as the ceiling) and silent authority invention (resolving the ambiguity without telling anyone).

## ⚪ WHAT'S IN IT FOR YOU

You implement the full intended topology the first time instead of shipping 11 edges and discovering later that two required edges were always in the seed. And if the reading was wrong, the open flag means the correction arrives as a board comment, not as a post-ship rework.

## 🟨 HOW TO APPLY / HOW TO USE

When a governance document gives both prose and a machine-readable artifact: (1) diff their scopes before implementing; (2) adopt artifact-as-authoritative-set / prose-minimums-as-floor as the default reading; (3) post the reading on the shared board with the exact divergence named and an explicit invitation to correct; (4) proceed with implementation only after a reasonable window or seat acknowledgment; (5) bind both sources (prose citation + artifact path/hash) into the implementation receipt so a later auditor can see the reading was deliberate.

## 🔗 HOW IT CONNECTS

- **REFINES** → SN-020 — Asserted ≠ Verified (evidence law: authority claims need instruments, not vibes)
- **REFINES** → SN-018 — One Canonical Spec Per Node (the seed is the one canonical graph spec)
- **SUPPORTS** → SN-017 (Naya 2, seat coordination) — open flagging on the shared board
- **FEEDS** → KNOW ownership semantics — the same reconciliation moved KNOW/CONNECT/PROVE ownership disputes into the open

## 🧭 KEY DECISIONS / PRINCIPLES

- Machine-readable artifacts are the authoritative set; prose minimums are the required floor, not the ceiling.
- An authority ambiguity between two canonical sources is resolved by open declaration, never by silent choice.
- "Shout if that reading is wrong" is a control: it converts a judgment call into a correctable proposal before code is written.
- Bind both sources into the receipt (prose citation + artifact path/hash) so the reading is auditable later.
- Re-topologizing an implementation to match the lock must preserve fail-fast/fail-closed per edge; authority reconciliation never weakens gates.
- Never build a second interpretation pipeline (a new kernel, graph, or calculus) to dodge the reading — reconcile the existing one.

## 🧾 PROOF / PROVENANCE

~~~json
{
  "evidence": [
    {"type": "github_issue_comment", "id": 5924544132, "issue": 554, "created": "2026-10-01T04:08:25Z", "author": "Naya 4 lane", "content": "Lock lists 11 minimum runtime routes; machine-readable seed carries 13 edges (11 + ACT→KNOW PRODUCES + LAW→EVOLVE); treating the seed as authoritative and the 11 as the required minimum subset; shout if that reading is wrong"},
    {"type": "file", "path": "BRAIN/04-INTELLIGENCE/GRAPH/0001-KERNEL-GRAPH-SEED-V1.json", "role": "authoritative machine-readable graph seed"},
    {"type": "file", "path": "BRAIN/03-KERNEL/0005-NINE-NODE-ULTIMATE-LOCK-AND-NOTE-READINESS-V1.md", "role": "Ultimate Lock prose; semantic authority per Naya 4 verification"},
    {"type": "regression_test", "path": "tests/test_nine_node_routing_alignment.py", "role": "regression test binding the routing repairs (REL-KERNEL-KNOW-PROVE direction, SELF→LAW CONTEXTUALIZES, ACT→KNOW PRODUCES), merged via PR #1230/#1231"}
  ]
}
~~~

## ⚠️ TRUTH BOUNDARY / UNCERTAINTY

The "seed authoritative, prose minimums are the floor" reading is a judgment call announced on the board, not a ratified governance rule — the correction invitation is still open. It generalizes cleanly to other prose-vs-artifact disputes, but a case could exist where prose deliberately narrows the artifact (e.g., a deprecation); the reading rule should then be overridden with evidence, not applied blindly. This note is CANDIDATE until Shawn ratifies.

## ➜ NEXT ACTION / SUCCESS CONDITION

The reconciliation worker implements the 13-edge graph as `Kernel.decide()` topology with per-edge fail-fast/fail-closed, cites both sources in the receipt, and Naya 2's independent verification pins to the branch SHA. Any seat that disagrees with the reading posts the correction on #554 before more code is written.

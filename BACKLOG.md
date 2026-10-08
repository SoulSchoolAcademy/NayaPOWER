# NayaPOWER Backlog

**Shared human-readable work projection / ranked queue. NOT a second source of truth.** Live repository/runtime evidence, ratified contracts, GitHub Issues/PRs, receipts and Current Truth own authoritative state; this file projects the highest-value work for Team Naya.

## How to use

- **Add** an item by opening a PR that edits this file. One item = one short entry with owner, status, and why.
- **Claim** an item by putting your seat name in `Owner` and moving it to the right section.
- **Complete** an item by moving it to `DONE` with the evidence (PR/issue/run link).
- **Priorities:** `P0` = active or blocked-now · `P1` = next up · `P2` = future · `IDEA` = under consideration, not committed.
- **Blocked** items name their blocker explicitly. No item sits in P0 blocked without a named unblock action.
- This file is a **projection/index**, not independent authority. Every consequential item should resolve to an Issue/PR/receipt/contract/current-truth source. If this file conflicts with live canonical evidence, live canonical evidence wins.
- **Freshness law:** never treat a SHA written inside this file as the live tip merely because it is written here. A commit that updates this projection changes `main` by definition. Resolve live refs at decision time; embedded SHAs are evidence snapshots only.
- This file is the queue, not the archive. Git history preserves prior projections; Issues/contracts/receipts preserve detailed authority and evidence.

---

## P0 — Active / Blocked

### 1. Re-establish exact-current production parity — HUMAN DEPLOY GATE
- **Owner:** Shawn for consequential production authorization · **Status:** waiting on exact-current promotion
- **Promotion target:** resolve live `main` at authorization time. This projection must not hardcode its own containing `main` SHA as timeless truth.
- **Last reconciled source snapshot before this projection merge:** `69fc9371ef6907d623d3c2e91fcea8c4128fdfe3`
- **Current production stamp:** `e727720424e237f1e0264a39598365ef986c7670`, source `4a2f728239c0e404205f0cc590766ceb7e7b7c28`
- **Why:** exact-SHA proof law requires current production/source parity before downstream runtime REDs can be promoted to current truth.
- **Boundary:** only the Human Director may authorize the exact production promotion. Team Naya may prepare/verify but must not infer `DEPLOY`.

### 2. Fresh exact-current proof after parity
- **Owner:** proof lane · **Status:** blocked by P0-1
- **Evidence:** Live Intelligence Commit Proof run `37385965077` was 4/4 green on prior main `cf4e0151...`; main then moved through #1522 and #1521.
- **What:** rerun the canonical commit/runtime proof on exact current source and take the **first actual RED** only.

### 3. Cold graph ON/OFF causal proof
- **Owner:** brain/proof lane · **Status:** downstream of parity
- **What:** the known `cold-graph-control-treatment` failure remains the leading genuine brain frontier, but it must be re-observed on exact-current production before repair claims.
- **Law:** do not patch stale downstream evidence.

---

## P1 — Next / Parallel

### 6. Governed RSI Experiment Campaign V1 — Issue #1513 (BLOCKED by parity)
- **Owner:** unassigned · **Status:** backlog, do not implement yet
- **What:** A bounded laboratory inside EVOLVE (not another architecture) harvesting the best mechanics from Dream-RSI, ModularRSI, AlphaEvolve/DGM, Meta-Harness, SEVerA, RRSI. Ten upgrades:
  1. Benchmark-disjoint held-out corpus + similarity screening
  2. Contrastive multi-rollout fault localization
  3. Retrieval-time integrity re-verification
  4. Noise-aware + cost-aware acceptance
  5. Formal behavioral/tool-boundary contracts
  6. Canonical discovery/trajectory tree receipts
  7. Dream-style offline replay worlds
  8. Bounded module attribution/mutation
  9. Candidate archive + diversity (stepping stones)
  10. Shadow/canary/rollback promotion
- **Detail:** Issue #1513.

### 7. Backlog / projection authority reconciliation — Issue #1519
- **Owner:** foundation/ops lane · **Status:** SOURCE FIXED — #1522 removed feed write authority; merged #1523 repaired backlog authority. Cold-successor/work-state proof remains.
- **What:** preserve the simple Backlog + Activity experience while enforcing one-owner/many-projections law.
- **Proof:** feed refresh no longer has write authority to `main`; backlog explicitly defers to live canonical evidence/Issues/PRs/contracts/receipts.

### 8. NayaNET viral invite system — the traffic engine — QUEUED (spec + design complete)
- **Owner:** Naya 4 (spec/design) · **Status:** SPEC COMPLETE, DESIGN COMPLETE, implementation queued — does NOT jump the proof queue (parity → graph seam → brain chain first)
- **What:** Email invite engine (contact import → one-tap send via the member's OWN Gmail/Outlook OAuth → ambassador link auto-embedded → sent/opened/clicked/joined/reward dashboard) + native OS share sheet on all boards. Passkey identity, Grow area inside Smart Connect, smart PWA prompt.
- **Constraint (Shawn):** no platform posting APIs, no automation that risks bans/ToS/legal — only what's logical, doable, 100% within terms.
- **Phase 2 ideas (designed, not started):** personal video invites, smart follow-up nudges, "bring your circle" group invites, network tree visualization, smart send-time.
- **Detail:** Issue #1517.
- **Smart Links:** #1520 (idea evolution/refinement) · #1519 (Feed/Backlog projection architecture) · #1513 (future bounded optimization only after proof gates).

---

### Smart App Creator — independently prove self-building (Issue #1925) — ACTIVE P1 INNOVATION / NO SCORE UPLIFT
- **Owner:** Innovation + Naya 2 independent design qualification; **Status:** candidate teaching kit and quality-calculator prototype; unprimed cold-Naya creator graduation NOT VERIFIED.
- **What:** one held-out human request produces a working beautiful Smart App with hero buttons, jewel boards, SmartTabs, card hierarchy and four-layer Intelligent Block, without Shawn repeating design instructions.
- **Accept:** canonical-source-only cold builder, independent visual 9.5+ acceptance, responsive/accessibility and real-action testing, evidence and receipt. **Priority:** keep engine learning P0; this is the measurable downstream mastery exam.
- **Detail:** [#1925](https://github.com/SoulSchoolAcademy/NayaPOWER/issues/1925), [#1602](https://github.com/SoulSchoolAcademy/NayaPOWER/issues/1602), draft design training [#1912](https://github.com/SoulSchoolAcademy/NayaPOWER/pull/1912).

## P2 — Future

### 9. A→B→C multi-generation compounding proof
- **What:** Prove retained intelligence compounds across cold successors, not just retrieves.

### 10. Negative-transfer refusal + authority non-inheritance proof
- **What:** The brain must demonstrate "useful here, not there" and that successors never inherit authority.

### 11. Reduce branch/PR entropy while preserving history
- **What:** Prune stale branches (destructive — needs Shawn's confirmation per item).

### 12. Hub implementation/release
- **What:** The Hub's deployed surface lags its architecture. Ranked below brain-proof work until parity + compounding close.

---

### Smart App private previews, governed Cloudflare publishing and NayaNET directory (Issue #1926) — P2 AFTER CREATOR GRADUATION
- **Owner:** Innovation product spec; future Cloudflare/Hub/GitHub App engineering owners to deconflict before implementation. **Status:** SPECIFIED / NOT BUILT.
- **What:** user-owned isolated world from #1264 → create app → private preview URL → quality/LAW/security/owner approval → stable user-world URL → **separate opt-in directory approval** → searchable and revocable; version history and rollback.
- **Critical boundary:** a tenant-owned logical world does not force a new GitHub repo per app; preview ≠ public; calculator ≠ authorization; Cloudflare Pages wildcard custom domains unsupported, so evaluate Workers for Platforms / dispatcher with tenant isolation and actual cost/permissions.
- **Next action:** once cold creator passes, inventory account/runtime and run one bounded, owner-isolated preview deployment spike; no DNS/production/credentials spend changes implied.
- **Authoritative running task list:** [#1926](https://github.com/SoulSchoolAcademy/NayaPOWER/issues/1926). **Fork/tenant isolation foundation:** [#1264](https://github.com/SoulSchoolAcademy/NayaPOWER/issues/1264).

## IDEA — Under consideration (not committed)

- **Idea Evolution / Smart Link Intake Protocol V1 — Issue #1520:** every meaningful idea follows `SOURCE → DISTILL → ENHANCE → RECONCILE → CLASSIFY → SMART LINK → BACKLOG → #1354 TEAM FEED → BUILD/VERIFY → LEARN`. Preserve original provenance, improve it, connect it to current architecture, and make the collective aware without letting ideas silently jump the priority queue.
- **AI-agnostic runtime plug-in:** prove "any model → restore governed Naya intelligence → operate → leave improved intelligence" with behavioral parity. (Architecture: yes. Proven plug-and-play: not yet.)
- **NayaNET network experiences:** Smart Spaces/Connect/Mail as the differentiator no RSI system builds. Continue productizing post-proof.
- **Daily Intelligence Report automation:** already nightly; consider Hub surfacing.

---

## DONE — Recently completed (evidence)

- 2026-10-05 — PR #1522 merged at `42acf203...`: Activity Feed is manual/read-only artifact projection; scheduled self-writing main removed.
- 2026-10-05 — PR #1521 merged at `69fc9371...`: Idea Evolution / Smart Link protocol + Viral Invite relationships added to shared backlog projection.
- 2026-10-05 — PR #1518 merged at `cf4e0151...`: Viral Invite System queued in backlog.
- 2026-10-05 — Live Intelligence Commit Proof run `37385965077`: 4/4 green on `cf4e0151...` before later main movement.
- 2026-10-05 — Cloudflare dead-worker cleanup: 17 stale Workers disconnected, 0 Cloudflare checks on fresh pushes. (Shawn deleted; Naya 2 verified. Smart Note SN-0356.)
- 2026-10-05 — Promotion workflow repair (#1496), cold-runtime hardening (#1497, #1501, #1502), SHA binding (#1499), replication-lag retry (#1500), unique fallback lesson (#1504).
- 2026-10-05 — Current Truth PR-truncation repair (#1507); fallback machine_view contract fields (#1508).
- 2026-10-05 — Live Intelligence Commit Proof 4/4 green on `a3ce52dc` (run 37376929764).

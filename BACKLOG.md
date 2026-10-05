# NayaPOWER Backlog

**The canonical shared to-do list for all NayaPOWER work.** One file, every idea, to-do, and concept. All seats read and write it through PRs — never in chat alone, never in a side file.

## How to use

- **Add** an item by opening a PR that edits this file. One item = one short entry with owner, status, and why.
- **Claim** an item by putting your seat name in `Owner` and moving it to the right section.
- **Complete** an item by moving it to `DONE` with the evidence (PR/issue/run link).
- **Priorities:** `P0` = active or blocked-now · `P1` = next up · `P2` = future · `IDEA` = under consideration, not committed.
- **Blocked** items name their blocker explicitly. No item sits in P0 blocked without a named unblock action.
- This file is the queue, not the archive. GitHub Issues hold the long-form detail; this file holds the ranked list.

---

## P0 — Active / Blocked

### 1. Production parity: `a3ce52dc` → production — HUMAN GATE (Shawn)
- **Owner:** Shawn (human gate) · **Status:** awaiting human action
- **Why:** The Live Supabase Runtime Proof's first real RED is production parity — deployed runtime reports `355e5d89`, current main is `a3ce52dc`. Nothing downstream can go green until this closes.
- **Action:** Dispatch the Governed Production Promotion workflow with `confirm=DEPLOY`, `source_sha=a3ce52dc7a29fe37c220c5a595952ebc34f8f418`.
- **Then:** fresh exact-main proof runs; Naya 1 takes the next first RED.

### 2. Merge PR #1506 (SN-0356 — Dead Workers Still Vote) — HELD for parity
- **Owner:** Naya 2 · **Status:** CI green, held
- **Why held:** Merging now would move main and stale the `a3ce52dc` promotion target (the promotion workflow fails closed on SHA mismatch). Merges immediately after parity clears.

### 3. Merge PR #1509 (Hub welcome seam) — HELD for parity
- **Owner:** Naya 2 · **Status:** CI in progress, held
- **Why held:** Same as #1506 — no main moves until parity clears.

### 4. Shared backlog + automated activity feed — IN PROGRESS
- **Owner:** Naya 2 · **Status:** building (this PR)
- **What:** This file + a 15-minute workflow that logs commits/PRs/workflow results to `ACTIVITY-FEED.md`, mirrored by the Hub's Smart Feed room.

---

## P1 — Next (unblocks after P0)

### 5. Fresh exact-main proof after parity (Naya 1's lane)
- **Owner:** Naya 1 · **Status:** waiting on P0-1
- **What:** Rerun the full proof against the parity-closed main; classify the next first real RED.

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

### 7. Graph ON/OFF causal proof (post-parity)
- **Owner:** Naya 1 · **Status:** waiting on P0-1
- **What:** The `cold-graph-control-treatment` RED from run 37377035191 gets diagnosed from fresh post-parity evidence — first RED, smallest fix.

### 8. NayaNET viral invite system — the traffic engine — QUEUED (spec + design complete)
- **Owner:** Naya 4 (spec/design) · **Status:** SPEC COMPLETE, DESIGN COMPLETE, implementation queued — does NOT jump the proof queue (parity → graph seam → brain chain first)
- **What:** Email invite engine (contact import → one-tap send via the member's OWN Gmail/Outlook OAuth → ambassador link auto-embedded → sent/opened/clicked/joined/reward dashboard) + native OS share sheet on all boards. Passkey identity, Grow area inside Smart Connect, smart PWA prompt.
- **Constraint (Shawn):** no platform posting APIs, no automation that risks bans/ToS/legal — only what's logical, doable, 100% within terms.
- **Phase 2 ideas (designed, not started):** personal video invites, smart follow-up nudges, "bring your circle" group invites, network tree visualization, smart send-time.
- **Detail:** Issue #1517.
- **Smart Links:** #1520 (idea evolution/refinement) · #1519 (Feed/Backlog projection architecture) · #1513 (future bounded optimization only after proof gates).

---

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

## IDEA — Under consideration (not committed)

- **Idea Evolution / Smart Link Intake Protocol V1 — Issue #1520:** every meaningful idea follows `SOURCE → DISTILL → ENHANCE → RECONCILE → CLASSIFY → SMART LINK → BACKLOG → #1354 TEAM FEED → BUILD/VERIFY → LEARN`. Preserve original provenance, improve it, connect it to current architecture, and make the collective aware without letting ideas silently jump the priority queue.
- **AI-agnostic runtime plug-in:** prove "any model → restore governed Naya intelligence → operate → leave improved intelligence" with behavioral parity. (Architecture: yes. Proven plug-and-play: not yet.)
- **NayaNET network experiences:** Smart Spaces/Connect/Mail as the differentiator no RSI system builds. Continue productizing post-proof.
- **Daily Intelligence Report automation:** already nightly; consider Hub surfacing.

---

## DONE — Recently completed (evidence)

- 2026-10-05 — Cloudflare dead-worker cleanup: 17 stale Workers disconnected, 0 Cloudflare checks on fresh pushes. (Shawn deleted; Naya 2 verified. Smart Note SN-0356.)
- 2026-10-05 — Promotion workflow repair (#1496), cold-runtime hardening (#1497, #1501, #1502), SHA binding (#1499), replication-lag retry (#1500), unique fallback lesson (#1504).
- 2026-10-05 — Current Truth PR-truncation repair (#1507); fallback machine_view contract fields (#1508).
- 2026-10-05 — Live Intelligence Commit Proof 4/4 green on `a3ce52dc` (run 37376929764).

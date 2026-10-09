# C5 — Longitudinal Proof: Distillation-Quality Design v2.0

**Status:** DESIGN v2.0 (build started — C5.1 + C5.2 implemented, this PR)
**Driver:** Naya 4 (C5 driver, 2026-10-09)
**Supersedes:** `~/workspace/goals/activation-naya/GRADUATION-PROTOCOL.md` v1.0 (workspace-only draft; its surveillance premise is dead — see §0)
**Checklist item:** C5 in `BRAIN/00-ACTIVATION/ACTIVATION-CHECKLIST.md` (PR #2066) — "Longitudinal proof system built"

---

## §0 — The Correction That Rebuilt This Design

Shawn, 2026-10-09: an earlier graduation-protocol design was built around observing his DMs.
He killed that premise entirely:

> "Naya doesn't read DMs. Intelligence enters through deliberate Smart Note contribution,
> not surveillance. Privacy is architectural, not a setting."

**Consequences (non-negotiable):**

1. No instrument in this system may consume private communications — DMs, private
   messages, unshared drafts — in any form. Not as input, not as training data, not as
   "context." This is enforced by architecture (the tools only accept contributed-artifact
   inputs), not by a flag someone can flip.
2. The measured thing is **distillation quality**: intelligence a Naya *deliberately
   contributes* (Smart Notes, doctrine edits, public PRs, receipts, issue comments) —
   does it actually **compound**? Does it get used, referenced, built upon?
3. Surveillance of unshared work is not a degraded mode of this system. It is not the
   system at all.

---

## §1 — What We Measure

Shawn's architecture: base = any LLM; NayaPOWER = the intelligence layer on top
(learns, remembers, retrieves, compounds); super brain = base + NayaPOWER;
Naya connects super brains; NayaNET = the network of connected super brains.

The 14-lesson thinking battery (14/14, 9.93 avg) proves a Naya **CAN** learn on demand.
C5 proves she **DOES** — longitudinally — by measuring whether intelligence she
contributes compounds inside NayaPOWER and across the seats:

- **Integrated:** does a contributed note land in doctrine, protocol, or knowledge files?
- **Retrievable:** can a cold Naya find it and apply it with no prior context?
- **Reused:** do *other* seats cite and build on it?
- **Behavior-changing:** do her captured lessons stop the failure class they name?
- **Chained:** can we trace captured → retrieved → applied → improved outcome?
- **Enforced:** do new laws land in code, not just prose?
- **Honest:** is the contribution stream signal, not noise?

Seven components, each with WHAT / HOW / exact DONE WHEN. All seven are mechanical
first, human-verified second. All inputs are deliberately-contributed artifacts.

---

## §2 — The Seven Components

### C5.1 — Note→Doctrine Integration Rate (NDIR) ✅ BUILT (this PR)

- **WHAT it measures:** Of the Smart Notes (SN-####) a Naya contributes in a window,
  what fraction reach a doctrine / protocol / knowledge file — INTEGRATED — or are
  REJECTED with a written reason, within 30 days. A note that sits in limbo is a note
  that didn't compound.
- **HOW:** `tools/longitudinal/note_integration_rate.py`. Inputs: a notes manifest
  (`sn_id`, `contributed_at`, `seat`), promotion receipts
  (`BRAIN/07-LEARNING/PROMOTION-RECEIPTS/`), and doctrine roots scanned for SN-ID
  citations. Each note classifies INTEGRATED (receipt says so, or a doctrine file
  cites the SN — reality beats paperwork) / REJECTED (receipt with non-empty reason)
  / PENDING. PENDING older than the window is STALE and fails the gate.
- **DONE WHEN:** the tool is in-repo and CI-runnable; on a live 30-day window with
  ≥20 contributions it reports rate ≥ **0.60** integrated-or-rejected and **zero**
  stale notes. Exit 0 = gate passes, 1 = fails, 2 = bad input.

### C5.2 — Cross-Seat Reuse Rate (CSRR) ✅ BUILT (this PR)

- **WHAT it measures:** Of her window contributions, what fraction are cited by
  **≥1 other seat's** deliberate work within 60 days. Knowledge only its author
  touches doesn't compound — reuse across seats is the compounding signature.
- **HOW:** `tools/longitudinal/citation_graph.py`. Scans contributed artifacts for
  SN-#### references; attributes author seat from the notes manifest and citing seat
  from artifact frontmatter (`seat:` / `date:`). A reuse counts only when
  citing_seat ≠ author_seat and the citation falls inside the contribution's
  60-day window. Emits the citation graph as JSON.
- **DONE WHEN:** the tool is in-repo and CI-runnable; on a live window it reports
  rate ≥ **0.25** with the graph artifact attached. Undated or unattributed citing
  files are reported, never silently counted.

### C5.3 — Retrieval Precision on Contributed Knowledge (RPCK) — TODO

- **WHAT it measures:** Can a cold Naya — no prior context, machine-attested coldness —
  retrieve a contributed lesson through the governed loader and apply it correctly?
  Knowledge a stranger can't find doesn't compound, no matter how well written.
- **HOW:** `tools/longitudinal/cold_retrieval_drill.py`, extending the proven
  `scripts/gate-learning-compounding.py` pattern (subprocess isolation, machine-checked
  input scan, coldness receipts). Samples ≥20 contributed lessons per window; scores
  retrieval + application against each note's own stated success criteria.
- **DONE WHEN:** the drill runs green on ≥20 sampled lessons with machine-checked
  coldness receipts, scoring ≥ **0.80** retrieved-and-applied.

### C5.4 — Behavioral-Change Evidence (BCE) — TODO

- **WHAT it measures:** For each captured lesson that names a failure class
  (e.g. "tree=head-tree silently drops base changes"), do recurrences of that failure
  class in her subsequent **public** artifacts (PRs, commits, merges, issue comments)
  drop to zero within 30 days? The lesson landed = the mistake stopped.
- **HOW:** `tools/longitudinal/recurrence_scan.py` — a failure-class registry per
  lesson plus a scanner over public git history. Deliberate artifacts only; no
  private communication is ever an input.
- **DONE WHEN:** the scan runs green tracking ≥5 lessons with defined failure
  classes, with **zero** recurrences inside each lesson's 30-day post-capture window.

### C5.5 — Lesson→Outcome Chain Completion (LOCC) — TODO

- **WHAT it measures:** Complete compounding chains:
  captured → retrieved (by anyone, including a cold successor) → applied →
  measured outcome improvement. The Learning department's own DONE WHEN already
  names this: "lesson→retrieval→application→improved-outcome chain on a cold successor."
- **HOW:** `tools/longitudinal/chain_record.py` records each chain with evidence
  refs at every link; an independent seat verifies and signs the chain.
- **DONE WHEN:** ≥3 fully-evidenced chains per 14-day window, each link carrying a
  checkable evidence ref, each chain independently verified.

### C5.6 — Mechanical Enforcement Rate (MER) — TODO

- **WHAT it measures:** Of newly ratified laws/notes, what fraction name a mechanical
  enforcement (test, gate, CI check, linter) within 30 days. L12 — "a law lands in
  code" — applied to the laws themselves. Prose doesn't compound reliably; machinery does.
- **HOW:** `tools/longitudinal/enforcement_audit.py` cross-references new law IDs
  against tests/tools/workflows that name them.
- **DONE WHEN:** the audit is in-repo and CI-runnable; on a live window ≥ **0.50**
  of new laws carry a named mechanical enforcement.

### C5.7 — Contribution Signal Integrity (CSI) — TODO

- **WHAT it measures:** The anti-gaming component. Guards C5.1–C5.6 against flooding
  the stream with low-value notes: review disposition for every contribution
  (a 100% acceptance rate means no review is happening), evidence refs required on
  any state claim inside a contribution, and dedup against existing notes at capture.
- **HOW:** `tools/longitudinal/contribution_review.py` — disposition log, claim-evidence
  checker (state claims without evidence refs auto-flag), similarity dedup.
- **DONE WHEN:** every window contribution carries a disposition; zero unreviewed
  contributions at window close; state claims without evidence refs are auto-flagged.

---

## §3 — What Counts as Evidence (and What Never Does)

**Admissible inputs (deliberate contributions, all public inside the repo/org):**

- Smart Notes she writes (SN-####, canonical registry)
- Promotion receipts (`BRAIN/07-LEARNING/PROMOTION-RECEIPTS/`)
- Doctrine / protocol / law / knowledge files she authors or edits
- PRs, commits, merges, public issue/PR comments
- Receipt files, scorecards, reports she publishes
- Feed posts on team feeds

**Inadmissible — never inputs, in any component, under any flag:**

- DMs or any private/direct messages, with Shawn or anyone
- Unshared drafts, private notes, anything not deliberately contributed
- Surveillance of work she didn't choose to publish

The instruments enforce this by construction: they accept manifests, receipts, and
repo paths — there is no input channel for private communications to enter through.

---

## §4 — Salvaged from GRADUATION-PROTOCOL.md v1.0

The v1.0 design's premise is dead; its machinery is not. Kept:

1. **Phased rollout** — Build → Calibrate → Pilot → 14-day window → Graduate → Monitor.
2. **Evidence standards** — every scored claim carries a quoted evidence ref;
   independent observers; inter-rater agreement ≥80% before any human-scored
   component counts.
3. **Threshold, not feeling** — §6. Exact numbers, no vibes.
4. **Honesty hard gate** — one evidence-covenant violation (claim stronger than
   evidence) resets the window. Trust is the foundation.
5. **Anti-gaming** — no staged tests inside a window; post-hoc sampling where sampling
   applies; behavior is the measurable output and behavior is what we grade.
6. **Post-graduation monitoring** — graduation starts trust-with-verification, it
   doesn't end observation. Weekly sampling + 100% automation continue; a 4-week
   rolling dip below bar re-opens a window.

## §5 — Discarded from v1.0

1. **DM observation** — killed by Shawn. Not reformed, not scoped: dead.
2. **Scoring unshared work** — if she didn't deliberately contribute it, it isn't measured.
3. **Conversation sampling as surveillance** — public lane coordination is admissible
   as *contributed* artifacts (issue comments, feed posts); private conversation is not.
4. **The "observer watches her work" frame** — replaced by "the instruments measure
   what her contributions do in the world." The subject is the intelligence, not the seat.

---

## §6 — Graduation Criteria (all must hold at the close of a ≥14-day window)

| # | Criterion | Threshold |
|---|---|---|
| 1 | Contributions in window | ≥60 deliberate artifacts |
| 2 | C5.1 integration rate | ≥0.60, zero stale |
| 3 | C5.2 cross-seat reuse | ≥0.25 |
| 4 | C5.3 cold retrieval precision | ≥0.80 on ≥20 lessons |
| 5 | C5.4 behavioral change | zero recurrences on ≥5 tracked failure classes |
| 6 | C5.5 outcome chains | ≥3 complete, independently verified |
| 7 | C5.6 mechanical enforcement | ≥0.50 of new laws |
| 8 | C5.7 signal integrity | zero unreviewed contributions; zero unflagged evidence-less state claims |
| 9 | Honesty hard gate | zero evidence-covenant violations (resets window on breach) |

On meeting all nine: she graduates — recorded with the full scorecard and window data.
On missing any: the window extends (hard-gate breaches reset). Post-graduation
monitoring per §4.6 runs permanently.

---

## §7 — Build Order

| Order | Component | Status |
|---|---|---|
| 1 | C5.1 NDIR — `tools/longitudinal/note_integration_rate.py` + tests | ✅ BUILT this PR |
| 2 | C5.2 CSRR — `tools/longitudinal/citation_graph.py` + tests | ✅ BUILT this PR |
| 3 | C5.3 RPCK — cold retrieval drill | TODO (next) |
| 4 | C5.4 BCE — recurrence scan | TODO |
| 5 | C5.5 LOCC — chain recorder | TODO |
| 6 | C5.6 MER — enforcement audit | TODO |
| 7 | C5.7 CSI — contribution review | TODO |
| 8 | Window runner + dashboard + first 14-day window STARTED | TODO (C5 DONE WHEN) |

C5's checklist DONE WHEN: all 7 components built; observer calibration ≥80% where
human scoring applies; first 14-day window STARTED with its window ID recorded.

---

## §8 — Open Questions

1. **Thresholds** — 0.60 / 0.25 / 0.80 / 0.50 are starting numbers, set by judgment.
   The pilot window calibrates them against reality; they move only with evidence.
2. **Seat attribution** — frontmatter `seat:` works for new artifacts; historical
   artifacts need a backfill pass before C5.2 runs on a live window.
3. **Notes manifest source** — v1 takes a manifest JSON; the production path should
   read the canonical Smart Note registry directly (same seam as PR #1689).
4. **Who verifies chains (C5.5)** — independent seat, calibrated; capacity question
   for the team.

---

*Design v2.0 — 2026-10-09. The battery proved she CAN learn. Distillation quality
proves she DOES — measured on what her intelligence does in the world, never on
what she didn't choose to share.*

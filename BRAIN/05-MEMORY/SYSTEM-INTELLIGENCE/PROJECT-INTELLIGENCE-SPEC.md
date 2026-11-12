# PROJECT INTELLIGENCE — Concept & Design Spec

**Version:** 1.1 (CANDIDATE — incorporates independent review 2026-10-09)
**Created:** 2026-10-09
**Authority:** Shawn Vibert's directive — "every project having the intelligence of the project... categorized and organized... all the intel in one spot"
**Status:** Awaiting team consensus before ratification
**Review:** Independent review scored 6.5/10, verdict SHIP WITH FIXES. All three critical findings (C1–C3) and eight important findings (I1–I8) addressed in this version. Full review: `REVIEW-2026-10-09.md`.

---

## 1. WHAT IS PROJECT INTELLIGENCE?

In Shawn's words: *"Any project having the intelligence of the project — categorized and organized — all the stuff there so you have all the intel for it in one sort of spot, all organized with all the data, and where you guys then you can communicate about that data."*

**Precise definition:** A project's intelligence is its living, organized memory — every decision and its reasoning, the current state, active blockers, lessons learned, load-bearing evidence, who's doing what, and what's unresolved — maintained in one canonical location, readable by humans and queryable by machines.

**The one-sentence version:** If a new agent joins the project cold, reading INTELLIGENCE.md should bring them to full working context in under 10 minutes.

**What it is NOT:**
- Not a chat log. Not a feed dump. Not a status-report archive.
- Not a duplicate of the charter, blueprint, or Smart Notes.
- Not a wish list. Not speculation. Only what's decided, verified, or actively blocking.

---

## 2. THE FOUR LAYERS (Do Not Reinvent)

Project intelligence sits in a four-layer information architecture. Each layer has a distinct job. **INTELLIGENCE.md is Layer 4 — the synthesis, not the source.**

| Layer | Artifact | Job | Changes | Authority |
|-------|----------|-----|---------|-----------|
| 1. LAW | `PROJECT.md` / charter | What we're building, why, success criteria | Rarely | Shawn only |
| 2. ARCHITECTURE | Blueprints, specs | How it works technically | When design changes | Design authority |
| 3. CAPTURE | Smart Notes, receipts, evidence | Raw lessons and proof (append-only) | Constantly | Capture pipeline |
| 4. INTELLIGENCE | `INTELLIGENCE.md` | **Living synthesis: current state, decisions, blockers, lessons, team** | On meaningful events | Project owner |

**The rule:** INTELLIGENCE.md **summarizes and references** the other layers — it never copies them wholesale. Each entry carries a 1–3 sentence context capsule (enough to act without clicking through), plus links to the Smart Note, blueprint section, or charter criterion for full detail. Pure "reference don't copy" fails the 10-minute cold-start promise — a decision entry requiring four link-chases before the reader reaches the blockers section is a design failure. The capsule is the intelligence; the link is the receipt.

**Why four layers instead of one big file:**
- Law must be stable (you don't want success criteria shifting under you).
- Architecture must be precise (you don't want design notes mixed with status).
- Capture must be append-only (you don't rewrite history).
- Intelligence must be current (you don't want stale state mixed with permanent law).
- Merging them creates a file nobody trusts and nobody maintains.

---

## 3. WHAT GOES IN INTELLIGENCE.md

### 3.1 STATUS SNAPSHOT (required)
Where the project stands right now. One paragraph in plain English, then key metrics.
- Plain-language summary (Shawn-readable, no jargon)
- Phase/milestone position
- Key numbers with provenance (scores, counts — every number sourced)
- Health: GREEN / YELLOW / RED with one-line reason

### 3.2 DECISIONS LOG (required)
Every significant decision, newest first. Each entry has a stable ID (`D-001`, `D-002`, ... — assigned sequentially, never reused):
- **Date** and **decider** (who made the call)
- **Decision** (one sentence)
- **Why** (reasoning, 1–3 sentence plain-English context capsule — enough to act without chasing links)
- **Evidence** (what proof backed it — links, not copies)
- **Alternatives considered** (what was rejected and why, brief)

A decision is "significant" if it changes direction, allocates resources, resolves a dispute, or sets a precedent. Routine task assignments are not decisions.

### 3.3 BLOCKERS (required)
What's stopping progress right now. Each entry has a stable ID (`B-001`, `B-002`, ...):
- **What's blocked** and **what it blocks** (downstream impact)
- **Owner** (who's clearing it)
- **What's needed** (the specific unblock action)
- **Since** (date identified)
- **Severity** (🔴 stops everything / 🟠 slows a workstream / 🟡 minor friction)
- **Escalated** (date + to whom + what was asked — required if open >7 days)

Remove blockers the turn they're cleared. Cleared blockers get one line in the Changelog ("B-003 cleared — <one-line outcome>") to preserve retrospective value.

### 3.4 LESSONS LEARNED (required)
What the project discovered — distilled, not raw. Each entry has a stable ID (`L-001`, `L-002`, ...):
- **Lesson** (one sentence, plain English)
- **Smart Note ref** (SN-XXXX — the full capture lives there)
- **Changed what** (what behavior/process/decision this lesson altered, 1–2 sentences)
- **Date learned**

This is the compounding layer. If a lesson didn't change anything, it's not a lesson yet — it's an observation.

### 3.5 KEY EVIDENCE (required)
Load-bearing proof only — not all evidence, just the pieces other claims stand on. Each entry has a stable ID (`E-001`, `E-002`, ...):
- **What it proves** (one line)
- **Link** (PR, commit SHA, test output, receipt)
- **Verified by** (who independently confirmed it, if applicable)

If removing this evidence would collapse a decision or status claim, it belongs here. Otherwise it lives in the capture layer.

### 3.6 TEAM (required)
Who's working on what right now. Each entry:
- **Agent/seat** and **assignment** (specific workstream)
- **Status** (active / blocked / waiting)
- **Last update** (date)

Update when assignments change. Remove people who rolled off.

### 3.7 TIMELINE (required)
Major milestones — hit and upcoming. Each entry:
- **Date**, **event**, **significance** (one line each)
- Past milestones: what was achieved (with evidence link)
- Future milestones: what's next and what "done" looks like

### 3.8 OPEN QUESTIONS (required)
What's unresolved. Each entry:
- **Question** (one sentence)
- **Why it matters** (what decision it blocks)
- **Who owns finding the answer**
- **Needed by** (date, if time-sensitive)

Close questions the turn they're answered — move the answer to Decisions Log.

### 3.9 RISKS & ASSUMPTIONS (required for multi-week projects; "N/A — <one line why>" allowed for small projects)
Known risks are not speculation — they're identified threats with owners. Each entry:
- **Risk** (one sentence: what could go wrong)
- **Likelihood / Impact** (high/medium/low each, one line of reasoning)
- **Mitigation** (what we're doing about it)
- **Owner** (who watches this)

Assumptions the project depends on, stated explicitly so they can be challenged.

### 3.10 DEPENDENCIES & RESOURCES (required for multi-week projects; "N/A — <one line why>" allowed for small projects)
- **Depends on:** other projects/workstreams this project is blocked by (each with owner and expected delivery)
- **Depended on by:** who is waiting on this project
- **Resources:** agent allocation, compute, budget — whatever the Allocation Law tracks

### 3.11 CHANGELOG (required)
Every meaningful update to this file, newest first. One line each:
- **Timestamp**, **author**, **what changed** (e.g. "D-007 logged — Receiver writes approved", "B-003 cleared — SN-782 resolved")

This is the audit trail. If it's not in the changelog, it didn't happen.

---

## 4. WHAT DOES NOT GO IN

- **Raw logs.** Link to them. Nobody reads 500 lines of CI output in a context file.
- **Full Smart Note text.** Reference by SN-ID. The note lives in the capture layer.
- **Charter/blueprint content.** Reference by section. Don't duplicate law or architecture.
- **Speculation.** "Might," "could," "probably" — if it's not decided or verified, it's an Open Question, not a Decision.
- **Routine chatter.** "Working on X" is team status, not project intelligence. Only meaningful changes.
- **Stale data.** If a section hasn't been verified in 7 days, mark it `⚠️ STALE — last verified <date>`. Stale intelligence is worse than no intelligence because it looks current.

---

## 5. ORGANIZATION

### 5.1 File location
`~/workspace/goals/<project-slug>/INTELLIGENCE.md`

One file per project. If the project is large enough to need sub-files, they live in `~/workspace/goals/<project-slug>/intelligence/` and INTELLIGENCE.md links to them — but the top-level file must always carry the full snapshot (Sections 3.1–3.3) inline.

### 5.2 Machine-readable front matter
Every INTELLIGENCE.md starts with YAML front matter for machine querying. **Front matter contains ONLY what a human must assert** — status judgment, ownership, and pointers. Counts are derived by tooling, never hand-maintained (hand-kept counters drift within days, producing exactly the false-confidence Shawn's deepest wound warns about).

```yaml
---
project: activation-naya
owner: naya-4
intelligence_version: "1.1"
status: YELLOW
last_updated: 2026-10-09T13:30:00-07:00
updated_by: naya-4
charter: ~/workspace/goals/activation-naya/PROJECT.md
blueprint: ~/workspace/goals/bring-naya-to-life/files/SYSTEM-BLUEPRINT-20261009.md
---
```

**Status rubric (concrete, not vibes):**
- **GREEN:** All phases on track, zero 🔴 blockers, no stale sections. The plan is executing.
- **YELLOW:** At least one 🟠 blocker active, or any section STALE, or a phase behind its expected pace. Needs attention but not intervention.
- **RED:** At least one 🔴 blocker, or a success criterion is at risk, or the project owner cannot state the current state with confidence. Needs Shawn or senior-seat intervention.

A `intel lint` parser derives `blockers_open`, `decisions_logged`, `lessons_logged`, `phases_complete` by counting entries in the body. Machines count; humans judge.

**Small-project mode:** Projects under ~2 weeks of expected effort may mark sections 3.9 and 3.10 as "N/A — <one line why>" and skip the full team table (single owner line suffices). Declare this in the Status Snapshot. Forcing a micro-project through all 11 sections produces filler, and filler teaches everyone the file is theater.

### 5.3 Stable section anchors
Sections use fixed `## ` headers (exactly as in Section 3). Machines can parse by header. Never rename sections — only the template version changes, and renames are breaking changes requiring migration.

### 5.4 Plain English first
Every section leads with a plain-English summary before any technical detail. Shawn's Literal-First Law applies: if he can't understand it, it's not useful. Technical precision follows, never precedes.

---

## 6. STAYING CURRENT

### 6.1 Update triggers (event-driven, not scheduled)
Update INTELLIGENCE.md when — and only when — one of these happens:
- A significant decision is made → Decisions Log
- A blocker is added or cleared → Blockers
- A lesson is learned (changed behavior) → Lessons Learned
- Key evidence lands → Key Evidence
- Team assignments change → Team
- A milestone hits → Timeline
- A question opens or closes → Open Questions
- A feed discussion concludes with a resolution → Decisions Log (with thread link)
- Status health changes → Status Snapshot

**Not on a timer.** A daily cron that rewrites the file with "no changes" trains everyone to ignore it. Event-driven updates mean every change to the file is meaningful.

### 6.2 The `intel` CLI helper (required tooling)
"Whoever caused the event updates it" fails without an affordance — an agent mid-task will not open a second file and hand-format a five-field entry. The `intel` helper makes updates a single command:

```
intel log-decision --project <slug> --title "..." --why "..." --evidence <link>
intel add-blocker --project <slug> --title "..." --owner <id> --severity red|orange|yellow
intel close-blocker --project <slug> --id B-003 --outcome "..."
intel log-lesson --project <slug> --lesson "..." --sn SN-XXXX --changed "..."
intel log-evidence --project <slug> --proves "..." --link <url>
intel ask --project <slug> --question "..." --owner <id>
intel answer --project <slug> --id Q-002 --answer "..."
intel status --project <slug> --health green|yellow|red --reason "..."
intel lint --project <slug>          # validate structure, report issues
```

The helper appends correctly formatted entries, assigns the next stable ID, updates `last_updated`/`updated_by`, and writes the changelog line — in one command. Until the helper ships, updates are manual but must follow the exact entry formats in this spec.

### 6.3 Staleness detection (computed, not self-declared)
Self-reported staleness is circular — a neglected file never flags itself. Staleness is **computed by a weekly scheduled lint**:

- The lint parses every `INTELLIGENCE.md` in `~/workspace/goals/*/`.
- For each section, it computes freshness from entry timestamps and `last_updated`.
- Any section unverified in 7 days is flagged STALE in the lint report.
- The lint posts a staleness report to the team's coordination feed naming files and stale sections.
- The ⚠️ STALE flag in the report is lint output, not self-report. The file itself doesn't need to carry the flag — the lint is the source of truth on freshness.

**Freshness thresholds:**
- Status Snapshot: re-verify every 3 days (it's the first thing anyone reads)
- Blockers / Team: re-verify every 7 days
- Decisions / Lessons / Evidence: append-only, never stale (history doesn't expire)
- Timeline: re-verify every 14 days

### 6.4 Rollup and archive policy
Append-only forever breaks the 10-minute cold-start promise. When a section exceeds ~25 entries or 90 days of history:
- Compress the tail to one-line ID summaries (`D-001 through D-040: early architecture decisions — see archive`)
- Move full text to `~/workspace/goals/<slug>/intelligence/archive/<section>-<date-range>.md`
- Link the archive from the section header

The live file stays scannable. History stays reachable. Nothing is deleted.

### 6.5 Who updates
Whoever caused the event, via the `intel` helper (§6.2). The project owner reviews for accuracy but doesn't gatekeep — speed of capture beats editorial polish. The weekly lint (§6.3) catches what humans miss.

---

## 7. CONNECTION TO EXISTING SYSTEMS

### 7.1 Smart Notes (capture layer)
- INTELLIGENCE.md **references** Smart Notes by ID: `SN-0804`, never copies their content.
- The Lessons Learned section is a **curated index** — only lessons that changed project behavior, each pointing to its full SN capture.
- Flow: Smart Note captured → lesson applied → behavior changed → entry added to INTELLIGENCE.md Lessons.

### 7.2 Blueprints (architecture layer)
- INTELLIGENCE.md references blueprint sections for "how it works."
- When the blueprint changes, the relevant INTELLIGENCE.md sections get a `last_updated` bump — but the intelligence file doesn't duplicate the technical content.

### 7.3 Project charters (law layer)
- On any conflict between INTELLIGENCE.md and PROJECT.md, **the charter wins.** The intelligence file describes reality; the charter declares intent. If reality diverges from intent, that's a blocker or an open question — not a silent edit to the charter.
- Charter changes require Shawn. Intelligence updates don't.

### 7.4 Feeds (communication layer)
- Feeds (#1354, sub-project feeds) carry **discussion.** INTELLIGENCE.md carries **conclusions.**
- When a feed discussion resolves into a decision, the decision goes in INTELLIGENCE.md with a link to the feed thread.
- Never copy feed threads into the intelligence file. Summarize the outcome.

### 7.5 Goals system
- INTELLIGENCE.md lives inside the goal directory: `~/workspace/goals/<slug>/INTELLIGENCE.md`.
- It complements `GOAL.md` (the agent's private notes) — GOAL.md is scratch, INTELLIGENCE.md is canonical.
- `hidden_files/` stays hidden (bookkeeping). INTELLIGENCE.md is visible (shared truth).

---

## 8. ANTI-PATTERNS (What Kills Project Intelligence)

1. **The junk drawer.** Everything gets dumped in, nothing gets curated. → Fix: admission test — "would a cold agent need this in 10 minutes?"
2. **The ghost file.** Created once, never updated. → Fix: event-driven updates + staleness flags.
3. **The duplicate.** Copies Smart Notes, charter text, feed threads. → Fix: reference, don't copy. Duplicates diverge.
4. **The wish list.** Full of "should," "will," "planned." → Fix: only decided/verified/blocking. Aspirations are Open Questions at best.
5. **The status report.** Reads like a weekly update email. → Fix: intelligence answers "what do I need to know to act?" not "what happened this week?"
6. **The gatekept file.** Only one person can update it, so it lags reality. → Fix: whoever caused the event updates it. Owner reviews, doesn't gatekeep.
7. **The jargon wall.** Only the builders understand it. → Fix: plain English first, always. Shawn reads this.

---

## 9. SUCCESS CRITERIA

Project Intelligence is working when:
1. A new agent reads INTELLIGENCE.md and can start contributing within 10 minutes (cold-start test).
2. Shawn can read the Status Snapshot and understand the project's state with zero jargon (readability test).
3. Every decision in the log has reasoning + evidence (audit test).
4. No blocker is older than 7 days without an escalation note (freshness test).
5. A machine can parse the front matter and answer "what's the status?" programmatically (query test).

Each criterion carries a `verified:` line (date + evidence link) when tested. Untested criteria are marked `untested` — a criterion without a verification record is aspirational, not achieved.

---

## 10. CONSENSUS RECORD

- **Reviewed by:** Naya 4 (independent reviewer seat) — 2026-10-09
- **Review saved:** `~/workspace/goals/project-intelligence-system/REVIEW-2026-10-09.md`
- **Score:** 6.5/10 → fixes applied → v1.1
- **Holes found:** 3 critical (C1 front-matter dual-write, C2 circular staleness, C3 no update mechanism), 8 important (I1–I8), 6 minor (m1–m6)
- **Holes fixed:** All 3 critical + all 8 important addressed in v1.1:
  - C1 → front matter shrunk to human-asserted fields; counts derived by `intel lint`
  - C2 → weekly computed staleness lint; flag is lint output, not self-report
  - C3 → `intel` CLI helper spec'd (§6.2) with one-command updates
  - I1 → CHANGELOG added as §3.11; `Escalated:` field added to blockers
  - I2 → stable IDs required (D-/B-/L-/E-/Q-)
  - I3 → "summarize, don't copy" with 1–3 sentence context capsules
  - I4 → rollup/archive policy (§6.4)
  - I5 → §3.9 Risks & Assumptions, §3.10 Dependencies & Resources added
  - I6 → concrete GREEN/YELLOW/RED rubric defined (§5.2)
  - I7 → small-project mode with N/A allowance (§5.2)
  - I8 → feed-discussion-concludes added to triggers (§6.1)
- **Reviewer verdict:** SHIP WITH FIXES → fixes applied
- **Consensus reached:** Pending team sign-off on v1.1
- [ ] Ratified by Shawn: _______________

---

*Spec version 1.0 — CANDIDATE. Changes only by team consensus + Shawn ratification.*

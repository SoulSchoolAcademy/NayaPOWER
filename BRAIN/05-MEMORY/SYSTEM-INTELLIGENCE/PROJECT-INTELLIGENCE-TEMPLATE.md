# PROJECT INTELLIGENCE — TEMPLATE v2

> **RECONCILED 2026-10-09** — One canonical template. Merges PR #2052
> (`.naya/project-intelligence/project-intelligence-template.md` — 9-section human
> narrative + living mechanism) with PR #2054
> (`BRAIN/05-MEMORY/SYSTEM-INTELLIGENCE/PROJECT-INTELLIGENCE-TEMPLATE.md` —
> machine-lintable entry IDs + YAML front matter). Both structures are preserved:
> the 9 human-readable sections carry the intelligence; the entry IDs and front
> matter make it machine-verifiable. Design rationale: `PROJECT-INTELLIGENCE-SPEC.md`.

**Status:** CANONICAL TEMPLATE — every NayaPOWER project uses this structure.
**Authority:** Shawn Vibert, Human Director
**Purpose:** The single organized mind of a project. Smart Notes are the raw capture; project intelligence is where the intelligence lives — categorized, connected, current, and communicable. A human or a Naya should be able to open a project's intelligence and find the whole picture: what it is, where it stands, what's happening, what was decided, what was learned, what's unknown, what's stuck, and what proves it.
**Rule:** Every claim carries evidence. A claim without evidence is marked UNKNOWN or ASSUMED, never silently promoted. The document is living — it updates when reality changes, not on a schedule.

---

## HOW TO USE THIS TEMPLATE

1. Copy this file. Name it `<PROJECT-SLUG>-INTELLIGENCE.md` and place it in `BRAIN/05-MEMORY/SYSTEM-INTELLIGENCE/`.
2. Fill in the YAML front matter below, then every section. If a section doesn't apply yet, write "Not yet" and say what's needed before it can be filled — never delete a section.
3. Keep it evidence-backed. Every factual claim cites its source (comment ID, PR link, file path, receipt ID).
4. Keep it plain. Every section starts with the human version — what it means in simple words — then the technical detail for the record.
5. Keep it current. Update it when things change (see THE LIVING MECHANISM). Stale intelligence is worse than none — it looks true and isn't.
6. Entry IDs (D-001, B-001, L-001, E-001, Q-001) are assigned sequentially — never reuse a number. Field semantics: see `PROJECT-INTELLIGENCE-SPEC.md` §3.

**Cold-reader test:** a Naya who has never seen this project should be able to read this document and answer: what is it, why does it exist, where does it stand, what's being done, what was decided, what was learned, what's unknown, what's stuck, and what proves any of it. If she can't, the intelligence is incomplete.

---

```yaml
---
project: <project-slug>
owner: <agent-or-seat-id responsible for accuracy>
intelligence_version: "2.0"
status: GREEN
last_updated: <ISO-8601 timestamp>
updated_by: <agent-or-seat-id who last updated>
charter: <path to charter, or "none">
blueprint: <path to blueprint/spec, or "none">
template: BRAIN/05-MEMORY/SYSTEM-INTELLIGENCE/PROJECT-INTELLIGENCE-TEMPLATE.md
---
```

> Front matter holds ONLY human-asserted fields. Counts (blockers open, decisions
> logged, etc.) are derived by `intel lint` — never hand-maintained.
> Status rubric: GREEN = on track, zero red blockers. YELLOW = attention needed.
> RED = intervention needed. See `PROJECT-INTELLIGENCE-SPEC.md` §5.2 for exact definitions.

---

## 1. PROJECT IDENTITY

**In plain words:** What is this project? Why does it exist? What does "done" look like — how will we know we got there?

- **Name:** the project's name and slug.
- **Mission:** one or two sentences — what the project exists to accomplish.
- **Origin:** how it started — who ordered it, when, what triggered it. Link the originating decision.
- **Done criteria:** the acceptance criteria for project completion. Machine-checkable where possible; human-judged where judgment is the point. Both are named.
- **Scope boundaries:** what is IN scope and what is explicitly OUT. Projects grow; boundaries keep them honest.
- **Successor effect:** what this project enables or unblocks for the next project.

## 2. CURRENT STATE

**In plain words:** Where does this project stand right now? What's true as of the last update?

- **State summary:** two or three sentences — the honest current picture.
- **Last verified:** timestamp and what was verified (main tip SHA, test results, deployment state — the exact evidence).
- **What's working:** the parts that are proven working, with the evidence that proves it.
- **What's not working:** the parts that are proven broken or proven missing, with the evidence.
- **What's unknown:** what hasn't been checked yet. Marked UNKNOWN, not assumed.
- **Health:** GREEN / YELLOW / RED — one-line reason (must match front-matter status).

## 3. THE PLAN

**In plain words:** What are we doing, in what order, and why that order?

- **Strategy summary:** the chosen approach in a paragraph — what it is, why it won, what was considered and rejected.
- **Scorecard:** the alternatives that were scored, the dimensions and weights, the winner. A plan without a scorecard is a preference, not a decision.
- **Execution order:** the phases or sections in order, each with what it achieves (plain words), its work items, dependencies, done-when criteria (ungameable — observable, not "tests pass"), and proposed owner.
- **Dependency map:** what blocks what, drawn simply. What runs in parallel, what must serialize.

## 4. ACTIVE WORK

**In plain words:** What's in flight right now? Who's doing what? What just happened?

- **In progress:** each active work item — what it is, who owns it, what state it's in, what the next step is.
- **Recently completed:** what landed recently, with the evidence (PR link, merge commit, test results).
- **Recently blocked:** what got stuck, why, and what would unblock it.
- **Up next:** what starts when the current work clears.
- **Team:** who's on what right now (update when assignments change).

## 5. DECISIONS LOG

**In plain words:** What did we decide, why, and what proves it was the right call?

Newest first. Only significant decisions (changed direction, allocated resources, resolved disputes, set precedents).

### D-001 — <YYYY-MM-DD> — <Decision in one sentence>
- **Decider:** <who made the call>
- **Why:** <1–3 sentence plain-English context capsule — enough to act without clicking>
- **Evidence:** <links to proof — PR, commit SHA, test output, receipt>
- **Alternatives rejected:** <what was considered and why it lost, brief>
- **Smart Note:** <SN-XXXX if captured, or "not captured">

**Reversed decisions** stay in the record — what changed, why. Reversals are learning, not failure.
**Pending decisions:** questions needing answers before work proceeds — who owns answering, what's needed.

## 6. LESSONS LEARNED

**In plain words:** What did this project teach us that changes future decisions?

Only lessons that CHANGED something (behavior, process, decision). Each with provenance — a lesson without a source is a rumor.

### L-001 — <Lesson in one sentence, plain English>
- **Smart Note:** SN-XXXX
- **Changed what:** <what behavior/process/decision this altered, 1–2 sentences>
- **Date learned:** <YYYY-MM-DD>

Promotion-worthy lessons (ones that change standing law or procedure) are flagged and tracked to their destination.

## 7. OPEN QUESTIONS

**In plain words:** What don't we know yet? Who's finding out?

### Q-001 — <Question in one sentence>
- **Why it matters:** <what decision this blocks, 1–2 sentences>
- **Owner:** <who's finding the answer>
- **Needed by:** <YYYY-MM-DD or "no deadline">

Questions are not blockers — they're unknowns with an owner. When a question becomes a blocker, it moves to section 8.

## 8. BLOCKERS

**In plain words:** What's stuck? What would unstick it?

Remove the turn they're cleared (log one line in Changelog). Never leave a dead blocker in this list.

### B-001 — 🔴 <What's blocked>
- **Blocks:** <downstream impact — what can't proceed until this clears>
- **Owner:** <who's clearing it>
- **Needed:** <the specific action that unblocks>
- **Since:** <YYYY-MM-DD>
- **Severity:** 🔴 stops everything / 🟠 slows a workstream / 🟡 minor friction
- **Escalated:** <date + to whom + what was asked, or "not yet" — required if open >7 days>

**Human-gated blockers** are flagged explicitly — these need Shawn (or his delegate), not more agent work.

## 9. EVIDENCE LOG

**In plain words:** The receipts. Everything this document claims, backed up.

Load-bearing proof only. If removing an entry would collapse a decision or status claim, it belongs here.

### E-001 — <What this proves, one line>
- **Link:** <PR / commit SHA / test output / receipt URL>
- **Verified by:** <who independently confirmed, or "unverified">

Organized newest first. This is the audit trail — when someone asks "prove it," this is where you look.

---

## THE LIVING MECHANISM

**How this document stays alive.** A project intelligence document that goes stale is a liability — it looks authoritative and lies.

### Update triggers (when it updates)

The document updates when reality changes, not on a schedule:

1. **Work completes** — a section's done-when criteria are met → update Current State, Active Work, Evidence Log.
2. **Work starts** — a new phase begins → update Active Work, Current State.
3. **A decision is made** — → update Decisions Log, and Current State if the picture changed.
4. **A lesson is distilled** — → update Lessons Learned.
5. **A blocker appears or clears** — → update Blockers (and Active Work).
6. **A question is answered** — → move it from Open Questions to wherever the answer belongs.
7. **Evidence arrives** — → update Evidence Log and whatever section the evidence changes.

### Who updates what (distributed, not bottlenecked)

- **Section owners update their own sections.** No single person is the bottleneck.
- **The project owner** (front-matter `owner`) is responsible for the document being current — not for writing every update, but for noticing staleness and nudging the right owner.
- **Any seat** that spots staleness flags it. "This section says X but the board says Y" is always welcome, never an accusation.

### Freshness rules

- **Current State** reflects reality within one working cycle of a material change.
- **Active Work** updates when work starts, completes, or blocks — same day.
- **Evidence Log** entries are added when the evidence is produced — same day.
- **The whole document** gets a freshness review whenever a phase completes.
- `intel lint` derives counts and flags stale sections mechanically — run it before claiming currency.

### What "stale" looks like (and what to do about it)

- A section describing a state that no longer exists → update it, note the change in the Evidence Log.
- A decision recorded without its reasoning → find the reasoning or mark "reasoning not recorded — needs recovery."
- An owner who hasn't updated through two material changes → the project owner reassigns or does it.
- When in doubt: the live board (#1354) and the live repo (main tip) are ground truth. The document follows them, not the other way around.

---

## TEMPLATE VERSION HISTORY

- **v2** (2026-10-09) — Reconciled canonical. Merged the 9-section human narrative + living mechanism (PR #2052) with YAML front matter + entry IDs + lint contract (PR #2054, SPEC v1.1). One template, two layers: human-readable intelligence, machine-verifiable structure.
- **v1** (2026-10-09) — Initial canonical template (PR #2052). 9 sections, living mechanism, cold-reader test.
- **v1.1** (2026-10-09) — Machine-layer variant (PR #2054). YAML front matter, entry IDs, SPEC §3 field semantics, `intel lint` contract.

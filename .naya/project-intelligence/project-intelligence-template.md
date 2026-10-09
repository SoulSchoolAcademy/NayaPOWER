# PROJECT INTELLIGENCE — TEMPLATE v1

**Status:** CANONICAL TEMPLATE — every NayaPOWER project uses this structure.
**Authority:** Shawn Vibert, Human Director
**Purpose:** The single organized mind of a project. Smart Notes are the raw capture; project intelligence is where the intelligence lives — categorized, connected, current, and communicable. A human or a Naya should be able to open a project's intelligence and find the whole picture: what it is, where it stands, what's happening, what was decided, what was learned, what's unknown, what's stuck, and what proves it.
**Rule:** Every claim carries evidence. A claim without evidence is marked UNKNOWN or ASSUMED, never silently promoted. The document is living — it updates when reality changes, not on a schedule.

---

## HOW TO USE THIS TEMPLATE

1. Copy this file. Name it `project-intelligence-<project-slug>.md`.
2. Fill in every section. If a section doesn't apply yet, write "Not yet" and say what's needed before it can be filled — never delete a section.
3. Keep it evidence-backed. Every factual claim cites its source (comment ID, PR link, file path, receipt ID).
4. Keep it plain. Every section starts with the human version — what it means in simple words — then the technical detail for the record.
5. Keep it current. Update it when things change. Stale intelligence is worse than none — it looks true and isn't.

**Cold-reader test:** a Naya who has never seen this project should be able to read this document and answer: what is it, why does it exist, where does it stand, what's being done, what was decided, what was learned, what's unknown, what's stuck, and what proves any of it. If she can't, the intelligence is incomplete.

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

## 3. THE PLAN

**In plain words:** What are we doing, in what order, and why that order?

- **Strategy summary:** the chosen approach in a paragraph — what it is, why it won, what was considered and rejected.
- **Scorecard:** the alternatives that were scored, the dimensions and weights, the winner. A plan without a scorecard is a preference, not a decision.
- **Execution order:** the phases or sections in order, each with:
  - What it achieves (in plain words)
  - The work items it contains
  - Dependencies (what must be done before it can start or finish)
  - Done-when criteria (ungameable — observable, not "tests pass")
  - Proposed owner (confirmed or not)
- **Dependency map:** what blocks what, drawn simply. What can run in parallel, what must serialize.

## 4. ACTIVE WORK

**In plain words:** What's in flight right now? Who's doing what? What just happened?

- **In progress:** each active work item — what it is, who owns it, what state it's in, what the next step is.
- **Recently completed:** what landed recently, with the evidence (PR link, merge commit, test results).
- **Recently blocked:** what got stuck, why, and what would unblock it.
- **Up next:** what starts when the current work clears.

## 5. DECISIONS MADE

**In plain words:** What did we decide, why, and what proves it was the right call?

- Each decision: the question, the options, the chosen answer, the reasoning (scorecard where the decision mattered), the evidence it rests on, who decided, when.
- **Reversed decisions:** decisions that were later reversed — what changed, why. Reversals are learning, not failure; they stay in the record.
- **Pending decisions:** questions that need answers before work can proceed — who owns answering them, what's needed to answer.

## 6. LESSONS LEARNED

**In plain words:** What did this project teach us that changes future decisions?

- Each lesson: what happened, why it happened, the behavior-changing takeaway (as a directive), confidence level, and the evidence.
- Lessons link back to the work that produced them — a lesson without provenance is a rumor.
- Promotion-worthy lessons (ones that change standing law or procedure) are flagged and tracked to their destination.

## 7. OPEN QUESTIONS

**In plain words:** What don't we know yet? Who's finding out?

- Each question: what we need to know, why it matters, who owns finding the answer, what's needed to answer it, by when (if there's a deadline that matters).
- Questions are not blockers — they're unknowns with an owner. When a question becomes a blocker, it moves to section 8.

## 8. BLOCKERS

**In plain words:** What's stuck? What would unstick it?

- Each blocker: what's stuck, why it's stuck, what would unblock it, who can unblock it, how long it's been stuck.
- **Human-gated blockers** are flagged explicitly — these need Shawn (or his delegate), not more agent work.
- A blocker that's been stuck longer than its owner said it would be gets escalated — silence about a known stuck thing is the failure.

## 9. EVIDENCE LOG

**In plain words:** The receipts. Everything this document claims, backed up.

- Key evidence entries: what was proven, when, by whom, where the receipt lives (comment ID, PR link, file path, run ID, hash).
- Organized by date, newest first. Each entry is one line: date — what — evidence link.
- This is the audit trail. When someone asks "prove it," this is where you look.

---

## THE LIVING MECHANISM

**How this document stays alive.** A project intelligence document that goes stale is a liability — it looks authoritative and lies. The mechanism below keeps it honest.

### Update triggers (when it updates)

The document updates when reality changes, not on a schedule:

1. **Work completes** — a section's done-when criteria are met → update Current State, Active Work, Evidence Log.
2. **Work starts** — a new phase begins → update Active Work, Current State.
3. **A decision is made** — → update Decisions Made, and Current State if the decision changed the picture.
4. **A lesson is distilled** — a Smart Note or review produces a project-relevant lesson → update Lessons Learned.
5. **A blocker appears or clears** — → update Blockers (and Active Work).
6. **A question is answered** — → move it from Open Questions to wherever the answer belongs (usually Decisions or Current State).
7. **Evidence arrives** — a test run, a verification, a receipt → update Evidence Log and whatever section the evidence changes.

### Who updates what (distributed, not bottlenecked)

- **Section owners update their own sections.** The learning lane updates the learning sections; the verification lane updates verification evidence; and so on. No single person is the bottleneck.
- **The project lead** (or the seat that owns the project) is responsible for the document being current — not for writing every update, but for noticing when it's stale and nudging the right owner.
- **Any seat** that spots staleness flags it. "This section says X but the board says Y" is always a welcome correction, never an accusation.

### Freshness rules

- **Current State** must reflect reality within one working cycle of a material change. If the main tip moved and tests ran, the state updates.
- **Active Work** updates when work starts, completes, or blocks — same day.
- **Evidence Log** entries are added when the evidence is produced — same day.
- **The whole document** gets a freshness review whenever a phase completes: is every section still true?

### What "stale" looks like (and what to do about it)

- A section that describes a state that no longer exists → update it, note the change in the Evidence Log.
- A decision recorded without its reasoning → find the reasoning or mark it "reasoning not recorded — needs recovery."
- An owner who hasn't updated their section through two material changes → the project lead reassigns or does it.
- When in doubt: the live board (#1354) and the live repo (main tip) are the ground truth. The document follows them, not the other way around.

---

## TEMPLATE VERSION HISTORY

- **v1** (2026-10-09) — Initial canonical template. Created from Shawn's "project intelligence" concept. First pilot: Activation Naya.

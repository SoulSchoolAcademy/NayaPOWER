# INTELLIGENCE.md — Project Template

> **How to use this template:** Copy this file to `~/workspace/goals/<your-project-slug>/INTELLIGENCE.md`.
> Fill in the YAML front matter. Write each section in plain English first.
> Entry IDs (D-001, B-001, etc.) are assigned sequentially — never reuse a number.
> Field semantics: see SPEC.md §3 for each section's rules. Keep this pointer line; don't delete it.
> Full design rationale: `~/workspace/goals/project-intelligence-system/SPEC.md`

---

```yaml
---
project: <project-slug>
owner: <agent-or-seat-id responsible for accuracy>
intelligence_version: "1.1"
status: GREEN
last_updated: <ISO-8601 timestamp>
updated_by: <agent-or-seat-id who last updated>
charter: <path to PROJECT.md or charter, or "none">
blueprint: <path to blueprint/spec, or "none">
---
```

> Front matter holds ONLY human-asserted fields. Counts (blockers open, decisions
> logged, etc.) are derived by `intel lint` — never hand-maintained.
> Status rubric: GREEN = on track, zero red blockers. YELLOW = attention needed.
> RED = intervention needed. See SPEC.md §5.2 for exact definitions.

---

## STATUS SNAPSHOT

> One paragraph in plain English: where does this project stand right now?
> No jargon. Shawn should understand this with zero technical background.
> Then key metrics — every number must have a source.

**Plain English:** <one paragraph>

**Position:** <phase/milestone, e.g. "Phase 2 of 5 — Decision←Memory">

**Key numbers:**
- <metric>: <value> (source: <where this number came from>)
- <metric>: <value> (source: <...>)

**Health:** <GREEN / YELLOW / RED> — <one-line reason>

---

## DECISIONS LOG

> Newest first. Only significant decisions (changed direction, allocated resources,
> resolved disputes, set precedents). Each entry: 1–3 sentence context capsule
> (enough to act without clicking), then links. See SPEC.md §3.2.

### D-001 — <YYYY-MM-DD> — <Decision in one sentence>
- **Decider:** <who made the call>
- **Why:** <1–3 sentence plain-English context capsule>
- **Evidence:** <links to proof — PR, commit SHA, test output, receipt>
- **Alternatives rejected:** <what was considered and why it lost, brief>
- **Smart Note:** <SN-XXXX if captured, or "not captured">

---

## BLOCKERS

> What's stopping progress RIGHT NOW. Remove the turn they're cleared
> (log one line in Changelog). Never leave a dead blocker in this list.

### B-001 — 🔴 <What's blocked>
- **Blocks:** <downstream impact — what can't proceed until this clears>
- **Owner:** <who's clearing it>
- **Needed:** <the specific action that unblocks>
- **Since:** <YYYY-MM-DD>
- **Severity:** 🔴 stops everything / 🟠 slows a workstream / 🟡 minor friction
- **Escalated:** <date + to whom + what was asked, or "not yet" — required if open >7 days>

---

## LESSONS LEARNED

> What the project discovered — distilled. Only lessons that CHANGED something
> (behavior, process, decision). Reference the Smart Note; include a 1–2 sentence
> capsule of what changed. See SPEC.md §3.4.

### L-001 — <Lesson in one sentence, plain English>
- **Smart Note:** SN-XXXX
- **Changed what:** <what behavior/process/decision this altered, 1–2 sentences>
- **Date learned:** <YYYY-MM-DD>

---

## KEY EVIDENCE

> Load-bearing proof only. If removing this evidence would collapse a decision
> or status claim, it belongs here. Everything else lives in the capture layer.

### E-001 — <What this proves, one line>
- **Link:** <PR / commit SHA / test output / receipt URL>
- **Verified by:** <who independently confirmed, or "unverified">

---

## TEAM

> Who's working on what RIGHT NOW. Update when assignments change.

| Agent/Seat | Assignment | Status | Last Update |
|------------|-----------|--------|-------------|
| <id> | <specific workstream> | active / blocked / waiting | <YYYY-MM-DD> |

---

## TIMELINE

> Major milestones — hit and upcoming. One line each.

### Achieved
- **<YYYY-MM-DD>** — <what was achieved> (evidence: <link>)

### Upcoming
- **<YYYY-MM-DD or "TBD">** — <what's next> (done when: <criteria>)

---

## OPEN QUESTIONS

> What's unresolved. Close the turn they're answered (move answer to Decisions Log).

### Q-001 — <Question in one sentence>
- **Why it matters:** <what decision this blocks, 1–2 sentences>
- **Owner:** <who's finding the answer>
- **Needed by:** <YYYY-MM-DD or "no deadline">

---

## RISKS & ASSUMPTIONS

> Required for multi-week projects. Small projects: "N/A — <one line why>".
> Known risks are not speculation — each has an owner and mitigation.

### <Risk in one sentence>
- **Likelihood / Impact:** <high/medium/low each, one line of reasoning>
- **Mitigation:** <what we're doing about it>
- **Owner:** <who watches this>

**Key assumptions:** <assumptions the project depends on, stated explicitly>

---

## DEPENDENCIES & RESOURCES

> Required for multi-week projects. Small projects: "N/A — <one line why>".

- **Depends on:** <other project/workstream> (owner: <id>, expected: <date>)
- **Depended on by:** <who is waiting on this project>
- **Resources:** <agent allocation, compute, budget>

---

## CHANGELOG

> Every meaningful update to this file. Newest first. One line each.
> Format: timestamp, author, entry ID + what changed.

- **<YYYY-MM-DD HH:MM>** <author>: <D-007 logged / B-003 cleared / status → YELLOW / etc.> — <one-line outcome>

---

*Template version 1.1. See SPEC.md for design rationale, anti-patterns, and the `intel` CLI contract.*

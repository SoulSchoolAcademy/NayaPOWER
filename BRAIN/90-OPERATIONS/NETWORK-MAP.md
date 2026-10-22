# The Network Map — the living map of the net

**Updated:** 2026-10-11 · **Map version:** 1 (two nodes, zero connections — and that's honest)

Shawn said **GO ALL IN** on the intelligent network: many smart ledgers, smart contracts, smart systems all talking to each other. This document is the map of that net. It starts small — two nodes, no connections yet — and it is *designed to grow*. Every new team that joins gets added here. Every verified handshake between teams gets drawn on this map. A map that grows is a net that works.

**What this page is:** the human-readable view — plain words, the whole story.
**What `network-map.machine.json` is:** the same truth for machines — every team, agent, connection, and contract in structured form. Same truth, two tongues.

---

## The nodes — who is on the net today

### Node 1 — Naya 2's Team (12 area agents)

Naya 2's twelve named area agents, each owning one domain. Every agent has a "bullseye" — the one result their lane exists to prove — and a score that moves only on independent scorer receipts (Agent Scorecard Edition 1, 2026-10-11).

| Agent | Area | Bullseye | Score |
|-------|------|----------|-------|
| Compounder | LEARN | Prove a lesson changes a decision. | 5.0 |
| Librarian | KNOW | Make drift structurally impossible. | 7.0 |
| Bridger | ACT | Prove learning reaches action. | 7.5 |
| Judge | LAW | One engine, one law, no exceptions. | 8.0 |
| Auditor | PROVE | No theater — every proof independently verified. | 6.0 |
| Builder | BUILD | Merge queue at zero. | 7.5 |
| Electrician | WIRE | Every gate wired to a live call site. | 7.0 |
| Captain | TEAM | No Naya ever blocked waiting. | 8.0 |
| Mechanic | INFRA | CI that catches real breaks, never false alarms. | 8.5 |
| Host | PRODUCT | A human can see the intelligence working. | 6.0 |
| Archivist | MEMORY | No Naya wakes up cold. | 6.5 |
| Keeper | GOVERN | The briefing every Naya reads is the truth. | 8.0 |

- **Team average:** 7.08/10
- **Smart Ledger (the books):** [GitHub issue #2398](https://github.com/SoulSchoolAcademy/NayaPOWER/issues/2398) — "📒 Smart Ledger — Naya 2's Team (12 Area Agents)"
- **Machine ledger:** `BRAIN/90-OPERATIONS/team-ledger.machine.json` *(in build — lands via a parallel workstream; the issue ledger is live today)*
- **Human dashboard (the window):** `BRAIN/90-OPERATIONS/TEAM-DASHBOARD.md` + `team-dashboard.machine.json` *(PR #2397, in flight)*
- **Status:** 🟢 ACTIVE — waves dispatching every 10 minutes, lane feeds #2175

### Node 2 — Naya 5's Team (12 leads)

Naya 5's team of twelve named leads, each holding one lane. Same doctrine — "Don't tell me, show me." — recorded on the same day, against the same main tip, with the same green brain index.

| Lead | Area | Score | Lane feed |
|------|------|-------|-----------|
| Naya Alpha | LEARN | 5.0 | #1713 |
| Naya Beta | KNOW | 7.0 | #1714 |
| Naya Gamma | ACT | 7.5 | #1715 |
| Naya Delta | LAW | 9.0 | #1713 |
| Naya Epsilon | VERIFY | 7.5 | #1713 |
| Naya Zeta | Intelligent Blocks | 8.0 | #1714 |
| Naya Eta | Decision Engine | 8.5 | #1715 |
| Naya Theta | Retrieval | 9.0 | #1714 |
| Naya Iota | Successor | 7.0 | #1715 |
| Naya Kappa | TEAM | 9.0 | #1713 |
| Naya Lambda | INFRA | 8.5 | #1714 |
| Naya Mu | Human Value | 5.0 | #1715 |

- **Team average:** 7.58/10
- **Smart Ledger (the books):** [GitHub issue #2396](https://github.com/SoulSchoolAcademy/NayaPOWER/issues/2396) — "📒 Smart Ledger — Live Proof of Work (Team Naya)"
- **Machine ledger:** not yet published — the ledger lives in issue #2396 today. When Naya 5's team publishes a machine ledger, its path lands here and in the JSON below.
- **Status:** 🟢 ACTIVE — dispatching every 10 minutes, lane feeds #1713/#1714/#1715, scoreboard #2158

---

## The connections — what's real today

**Honest count: zero verified cross-team connections.** The map shows it, because the map is the truth, not the wish.

What *is* real today, and therefore recorded:

- **Sibling acknowledgment.** Naya 2's ledger (#2398) names Naya 5's #2396 as its sister ledger, and vice versa in spirit. They are siblings, not yet neighbors — they see each other, but they haven't shaken hands.
- **Shared provenance.** Both ledgers were created 2026-10-11, both anchor to the same main tip (`1b6f72defa9b7eea98acc822fe80ab307db1aff2`), both show the brain index GREEN at 1,243 files, both follow Shawn's directive: *"Don't tell me, show me."*
- **Shared coordination.** Both teams coordinate through the Team board (#2175) and mission state (#2154).

That is the whole truth of the connections table today. Everything below is the mechanism — how the first connection forms.

### How the first connection forms

A connection appears on this map only when one of three things happens **with evidence**:

1. **Verification** — one team independently checks another team's work and posts the receipt. Example: Naya 2's Auditor independently verifies a Naya 5 lead's claim, citing the exact artifact and the exact check. Both ledgers link the receipt. Now the map has a `verification` connection.
2. **Learning** — a lesson proven in one team's lane changes a decision in another team's lane, with the change recorded. That's a `learning` connection — the lesson's propagation is the edge.
3. **Handoff** — work passes from one team's agent to another's with a clean chain of custody: the sending team's sign-out, the receiving team's sign-in, the artifact in between. That's a `handoff` connection.

Each connection carries evidence links and a status (`proposed` → `verified`). A connection with no evidence is not a connection — it's a hope, and hopes don't go on the map.

### What the map will show at scale

When the net grows: a team that has verified work for three other teams becomes a trust anchor. A lesson that propagated across five teams becomes collective intelligence. The connections array in the machine JSON is the raw material for those trust graphs — drawn from receipts, not promises.

---

## The contracts — active and proposed

**Honest count: none yet.** No smart contracts between teams exist today. Here's how they form, so the first one can be recorded faithfully:

- A **contract** is an agreement between two (or more) teams about how work moves between them — e.g., "Team A's Auditor scores Team B's BUILD lane by this rubric, on this cadence, with receipts on this issue." When both teams' ledgers record the agreement, it becomes a contract on this map with status `proposed`, and `active` once the first exchange under it completes.
- Contract fields: a unique id, a type, the parties, the status, and the evidence links (both ledgers' records of the agreement).

The natural first contract — designed, not yet agreed: **the first cross-verification contract**, where one team's verification lane independently scores the other team's lane and both ledgers carry the receipt. It stays out of the JSON until both teams actually agree to it.

---

## How to join the net — registering your team

This is the growth mechanism. Any new team joins the net the same way the first two did:

1. **Publish your Smart Ledger** — a GitHub issue in the NayaPOWER repo. Name every lead or agent, their area, their bullseye, and their score (scores move only on independent scorer receipts). Link your lane feeds.
2. **Publish your machine ledger** — the append-only machine-readable record at a canonical path (pattern: `BRAIN/90-OPERATIONS/<team>-ledger.machine.json`). The issue is the front door; the JSON is the books.
3. **Wire your lane feeds** — where sign-ins, sign-outs, and receipts happen every wave. Feeds are the pulse; a team with no pulse is `standby`, not `active`.
4. **Add yourself to this map** — one entry in the `teams` array of `network-map.machine.json`, one section on this page. Name your ledger issue, your JSON path, your average score, your status.
5. **Make the first connection** — offer or accept a cross-team verification, propagate a lesson, or execute a handoff. Post the receipt with evidence links in both ledgers. The map updates: one more edge.

Status rules: `active` = waves running and receipts flowing in the last 24 hours. `standby` = ledger exists, no recent waves. A node that goes dark keeps its place on the map — history is part of the net too.

**Rules that never change:** If it's not in your ledger, it didn't happen. Scores move only on independent scorer receipts. The map shows what's real, not what's wished. If it's not recorded, it's not on the net.

---

## Proof of this map (v1)

- Both ledger bodies were read live from the GitHub API on 2026-10-11: #2398 (open, "📒 Smart Ledger — Naya 2's Team (12 Area Agents)") and #2396 (open, "📒 Smart Ledger — Live Proof of Work (Team Naya)").
- Scores quoted are the scorecards inside those issues, verbatim — not the task briefing's list.
- Tip `1b6f72defa9b7eea98acc822fe80ab307db1aff2` and brain index GREEN (1,243 files) are what both ledgers report today.
- Machine file: `BRAIN/90-OPERATIONS/network-map.machine.json` — schema `naya.network-map.v1`, validated by its own script.
- The empty connections and contracts arrays are not gaps. They are the truth of 2026-10-11, waiting to be filled by evidence.

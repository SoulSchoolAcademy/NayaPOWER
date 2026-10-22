# The Smart Ledger Protocol

**Version:** 1.0 — 2026-10-11
**Status:** Canonical — every team's ledger follows this spec
**Keeper:** Naya 2 (✨), on Shawn's directive
**Canonical example:** [Issue #2398 — 📒 Smart Ledger — Naya 2's Team (12 Area Agents)](https://github.com/SoulSchoolAcademy/NayaPOWER/issues/2398)

> **Shawn's rule:** *"Don't tell me, show me. The recorded action is the verified action. If it's not in the ledger, it didn't happen."*

---

## For the next Naya reading this

Welcome. This is the one document that explains how every Smart Ledger in the NayaNET network works — yours included. Read it once, then use it every day. If you ever wonder "where does the proof of my work live?", the answer is always: **in the ledger.**

---

## 1. Why ledgers exist

Talk is cheap and memory is faulty. When twelve agents (or a hundred teams) all work at once, nobody can keep the whole story in their head. The ledger is the one place where the story is written down — completely, honestly, and in a way anyone can check.

The ledger exists so that:

- **Shawn can see, not be told.** Every claim links to its evidence. No "trust me."
- **Every Naya can reconstruct the past.** A cold-start agent reads the ledger and knows exactly what happened, in order.
- **The Hub can show the truth live.** The machine JSON feeds the human cockpit — the dashboard is just a pretty window onto the ledger's books.
- **Scores mean something.** An agent's score only moves when a ledger entry proves the work behind it.

**The Rule, in one line:** the recorded action is the verified action. If it's not in the ledger, it didn't happen.

---

## 2. Every ledger has three parts

One ledger = three things that stay in sync. If any one is missing, it's not a Smart Ledger yet.

### Part A — The human anchor (GitHub issue)

A GitHub issue is the ledger's face. It holds:

- **The roster** — who the agents are, their areas, their bullseyes, their current scores (e.g., the twelve-agent table in #2398: Compounder/LEARN, Librarian/KNOW, Bridger/ACT, Judge/LAW, Auditor/PROVE, Builder/BUILD, Electrician/WIRE, Captain/TEAM, Mechanic/INFRA, Host/PRODUCT, Archivist/MEMORY, Keeper/GOVERN).
- **The protocol summary** — the sign in/out rules, in five lines.
- **The chain of proof** — how this ledger links to waves, sign-ins, the dashboard, mission state, and scorecards.
- **Live status** — tip, wave counter, brain-index health, entry count. Updated when waves run.

The anchor issue is what a human reads first. It must always point at Parts B and C.

### Part B — The machine JSON (Hub-consumable)

The full books, machine-readable: every entry, in order, in a versioned JSON document (e.g., `team-ledger/team-ledger.machine.json`). The Hub dashboard consumes this — **dashboard = the window, ledger = the books.** Same truth, two views.

The machine JSON is the **authoritative record**. If the issue body and the JSON ever disagree, the JSON wins — and the disagreement itself gets logged as a correction entry (see §4).

### Part C — The versioned schema

Every machine JSON declares its schema (`"schema": "naya.team-ledger.v1"`). The schema is versioned so readers written today keep working tomorrow. Schema rules live in §7.

### The ledger keeper — who owns the three parts

Every ledger names a **keeper** (e.g., #2398: "Ledger keeper: Naya 2"). The keeper is a named agent, not a background process, and is responsible for:

- **Running the appends** — the keeper operates the append script (§8) or delegates it to a wave agent, but owns the result.
- **Keeping the three parts in sync** — when the JSON grows, the anchor issue's live status moves with it; when they disagree, the keeper files the correction entry.
- **Guarding the write boundary** — one team's keeper writes only to that team's ledger. No team edits, deletes, or "fixes" another team's ledger, ever. If you see an error in someone else's books, you post a public note on their anchor issue — you do not touch their JSON.
- **Owning corruption recovery** — a corrupt ledger file is repaired by restoring the last valid copy and re-appending from the watermark; the repair itself is logged as a `checkpoint` entry so the recovery is auditable too.

The keeper's authority covers *their team's ledger only*. The protocol (§7, §8) belongs to the network; no single keeper may change it unilaterally.

---

## 3. Append-only, forever

**History is never rewritten.** No editing old entries. No deleting entries. No rebasing the ledger.

This is the heart of trust: once something is in the ledger, it stays. That permanence is what makes "if it's in the ledger, anyone can check it" true six months from now.

Got something wrong? Made a mistake? Found a better number? **Write a new entry.** Corrections are new entries of type `correction`, pointing at the entry they supersede:

```json
{
  "receipt_id": "tl-20261011-010",
  "schema": "naya.team-ledger.v1",
  "team": "naya2-12-area-agents",
  "agent": "Keeper",
  "lane": "GOVERN",
  "timestamp": "2026-10-11T23:55:00Z",
  "type": "correction",
  "supersedes": "tl-20261011-008",
  "action": "Score correction: Builder wave score 7.5 → 8.0 after independent re-score",
  "evidence_links": ["https://github.com/SoulSchoolAcademy/NayaPOWER/issues/2398#issuecomment-…"],
  "score_before": 7.5,
  "score_after": 8.0,
  "status": "done"
}
```

The old entry stays visible, the new entry explains what changed and why. Anyone auditing the chain sees the full story — including the correction.

---

## 4. Entry format

Every entry — no exceptions — carries these fields:

| Field | Required | What it is |
|---|---|---|
| `receipt_id` | ✅ | Unique id for the entry, e.g. `tl-20261011-003`. Used for dedupe. Never reused. |
| `schema` | ✅ | Schema version, e.g. `naya.team-ledger.v1`. Lives once at document top; repeated per entry is fine. |
| `team` | ✅ | Which team's ledger this belongs to, e.g. `"naya2-12-area-agents"`. |
| `agent` | ✅ | Who did the work, e.g. `"Builder"`, `"Auditor"`. |
| `lane` | ✅ | The agent's area, e.g. `"BUILD"`, `"LAW"`. |
| `timestamp` | ✅ | UTC ISO-8601 when the action completed, e.g. `2026-10-11T23:40:00Z`. |
| `type` | ✅ | One of: `sign_in`, `work`, `sign_out`, `score`, `correction`, `checkpoint`. (`checkpoint` = backfills, corruption recoveries, wave-boundary markers.) |
| `action` | ✅ | Plain-English description of what happened. One or two sentences. |
| `evidence_links` | ✅ | URL(s) proving it: GitHub comments, PRs, run logs, receipts. At least one per `work`/`sign_out`/`score` entry. |
| `score_before` | ✅ for `score` | The agent's score before this action, 0–10. `null` when not applicable. |
| `score_after` | ✅ for `score` | The agent's score after this action, 0–10. `null` when not applicable. |
| `status` | ✅ | One of: `done`, `in_progress`, `blocked`, `corrected`. |
| `supersedes` | only for `correction` | The `receipt_id` being corrected. |

**A complete example:**

```json
{
  "receipt_id": "tl-20261011-003",
  "schema": "naya.team-ledger.v1",
  "team": "naya2-12-area-agents",
  "agent": "Electrician",
  "lane": "WIRE",
  "timestamp": "2026-10-11T23:40:12Z",
  "type": "sign_out",
  "action": "Wave 3 wire-battery complete: 7/7 gates byte-verified against live tip; zero open wiring gaps.",
  "evidence_links": [
    "https://github.com/SoulSchoolAcademy/NayaPOWER/issues/2175#issuecomment-XXXX"
  ],
  "score_before": 7.0,
  "score_after": 7.5,
  "status": "done"
}
```

**Rules of a good entry:**

1. **Evidence is mandatory, not decorative.** A `work`, `sign_out`, or `score` entry with no evidence link is incomplete — treat it as `blocked` until the link lands.
2. **Scores move only on independent receipts.** Your own claim never changes your score; a scorer's receipt does. (`score_before`/`score_after` must match the scorer's receipt.)
3. **Plain English.** Write `action` so Shawn — or a Naya waking up cold — understands it on first read.
4. **`receipt_id` is sacred.** One id, one entry, forever. The append script (§8) refuses duplicates.

---

## 5. The sign in/out protocol

Every agent, every wave, every time. This is the heartbeat that feeds the ledger.

1. **Sign in** on the team's sign-in issue (e.g., #2175) with your lane tag — `[LANE AREA]` — and say three things: **who you are, what you're doing, why it matters.**
2. **Prove briefing load.** Read the current law and the live plan *before* you start reasoning about the work. Briefing before thinking.
3. **Do the work.** Builder-Scorer Loop: build it, score it honestly, fix it, re-score. Real tests, real receipts, no theater.
4. **Sign out** on the sign-in issue with your lane tag: **what you did, what you honestly scored it, links to the evidence.**
5. **Leave the receipt** — the sign-out (and any score receipts) appends to the machine JSON via the append script (§8). The promise is worthless; the evidence is everything.

Sign-in entries in the ledger use `type: sign_in`; sign-outs use `type: sign_out`. Together they bookend every unit of work, so anyone can walk the chain: dispatch → sign-in → work → sign-out → score.

---

## 6. The chain of proof — where the ledger sits

The ledger is one link in a chain. Know the whole chain, so you know what feeds what:

```
wave dispatch (every 10 min, 3 agents)
  → sign in/out on the sign-in issue        → the recorded action
  → the ledger anchor issue                 → the organized ledger linking everything
  → the team dashboard                      → RIGHT NOW, the live window
  → the ledger machine JSON                 → ALL TIME, the full books
  → mission state (live/mission-state)      → current priorities
  → the agent scorecard                     → per-area accountability
```

Dashboard = the window. Ledger = the books. The dashboard may refresh, restyle, or be rebuilt — the ledger JSON is what it reads. Never let a display claim drift from the books; when in doubt, the JSON is the source of truth.

Sister ledgers (e.g., Naya 5's [#2396 — 📒 Smart Ledger — Live Proof of Work](https://github.com/SoulSchoolAcademy/NayaPOWER/issues/2396)) follow this same spec. **Many ledgers, one protocol.** A reader that can parse one team's ledger can parse them all.

### Finding every ledger — the registry

"Many ledgers talking to each other" only works if the network can find them all. The convention:

- Every ledger's anchor issue carries the title prefix `📒 Smart Ledger —` and the label `smart-ledger`.
- The Hub (and any Naya) enumerates the network's ledgers by searching issues with that label — no hardcoded list, no private registry that drifts.
- Each anchor issue links its machine JSON path (e.g., `team-ledger/team-ledger.machine.json`) so a reader can go from discovery to full books in two hops.

If your team's ledger can't be found by that search, it's not on the network yet — fix the anchor issue first.

---

## 7. Schema evolution — v1 → v2 without breaking readers

The schema will grow. These rules keep growth safe:

1. **Additive-only within a major version.** You may add new optional fields in `v1.1`, `v1.2`, … You may **never** rename, remove, or change the meaning of an existing field in a v1.x release.
2. **Readers must ignore unknown fields.** A v1.0 reader reading a v1.2 document keeps working — it just doesn't see the new fields. Write your parser this way from day one.
3. **Required stays required.** A field that is required in v1.0 is required in every later v1.x. If you need to relax one, that's a new major version.
4. **v1 → v2 needs a migration note.** A breaking change ships as `naya.team-ledger.v2` with a written migration note: what changed, why, and how v1 documents convert. The old schema stays documented and readable — history doesn't get orphaned.
5. **Support both during transition.** For at least 30 days after v2 ships, writers append v1-compatible entries alongside v2 (dual-write) OR the append script transparently upgrades. Readers sniff the `"schema"` field and branch — never assume.
6. **The protocol spec versions with the schema.** When the schema goes to v2, this document gets a §-by-§ review and a new version line at the top. The spec and the schema never silently disagree.

**Current canonical schema:** `naya.team-ledger.v1` (this document, §4).

---

## 8. The append script pattern

Appends are automated — no hand-editing the JSON. The canonical pattern every team implements:

```
READ the ledger JSON
VALIDATE it against the declared schema (reject on failure — never write invalid JSON)
READ the watermark file (last-processed receipt id + source cursor)
FOR each new candidate entry:
    IF candidate.receipt_id already exists in the ledger → SKIP (dedupe)
    VALIDATE the candidate (required fields, evidence links present, score fields sane)
    APPEND the candidate
WRITE the ledger JSON atomically (write temp file → fsync → rename)
UPDATE the watermark (new last-processed receipt id)
```

**The rules behind the pattern:**

- **Dedupe by `receipt_id`.** Waves re-run, retries happen, relays double-post. The receipt id makes every one of those safe: same id = already recorded = skip quietly.
- **Watermark for last-processed.** Keep a tiny sidecar file (e.g., `team-ledger/.watermark.json`) recording the last receipt id appended and the source cursor (last sign-in comment id processed). On restart, resume after the watermark — never re-scan blind.

  ```json
  { "last_receipt_id": "tl-20261011-003", "last_source_cursor": "issue-2175-comment-6110527301", "updated_at": "2026-10-11T23:40:12Z" }
  ```
- **Validate before append.** Schema-check the whole document and each candidate before writing. A corrupt ledger helps nobody; fail loudly and keep the old file intact.
- **Atomic writes only.** Write to a temp file, fsync, rename. A half-written ledger is worse than a stale one.
- **Append, never rewrite.** The script adds entries to the `entries` array. It never edits, reorders, or deletes existing entries. (Corrections are new entries — §3.)

---

## 9. Your first ledger — a checklist for the next Naya

Starting a team's ledger? Do this, in order:

- [ ] Open the anchor issue (title: `📒 Smart Ledger — <Team Name>`, label: `smart-ledger`). Write the roster, the protocol summary, the chain of proof, and live status. Link your sister ledgers and your machine JSON path.
- [ ] Name your **ledger keeper** in the anchor issue — the agent who owns the appends and the write boundary.
- [ ] Create the machine JSON with `"schema": "naya.team-ledger.v1"` and an empty `entries` array. Backfill any history as entries (backfills are entries like any other — `type: checkpoint`, with the honest timestamp of the original event).
- [ ] Implement the append script per §8. Test it: append, re-append the same entry (must skip), corrupt an entry (must reject).
- [ ] Sign in on the team's sign-in issue. Run one wave. Sign out. Watch the entries land.
- [ ] Check the Hub dashboard reads your JSON. Dashboard = window, ledger = books — confirm they show the same truth.
- [ ] Announce the ledger to the network with its anchor issue link. One protocol, many ledgers.

---

*Written for every Naya who comes after. The ledger is how the world learns to trust us — not by what we say, but by what they can see. Keep it honest, keep it complete, keep it append-only.*

**Related:** [Issue #2398](https://github.com/SoulSchoolAcademy/NayaPOWER/issues/2398) (Naya 2's team ledger — canonical example) · [Issue #2396](https://github.com/SoulSchoolAcademy/NayaPOWER/issues/2396) (Naya 5's sister ledger) · [Issue #2175](https://github.com/SoulSchoolAcademy/NayaPOWER/issues/2175) (sign in/out) · Schema `naya.team-ledger.v1`

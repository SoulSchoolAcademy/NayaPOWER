# The Inter-Ledger Protocol

**Version:** v1 (spec) · **Status:** DRAFT — agreement first, mechanism later
**Scope:** how one team's smart ledger talks to another's
**Date:** 2026-10-11

## In a nutshell

NayaNET is many teams of smart agents, and every team keeps its own smart ledger — an append-only record of what it did, with the proof attached. The Inter-Ledger Protocol is the agreement that lets those ledgers reference each other without ever touching each other.

Three moves, that's the whole protocol:

1. **Cite, don't edit.** A ledger never writes to another team's ledger. It writes to its own and *cites* the other team's entries. A citation is only proof when the cited entry actually exists.
2. **Two sides, one truth.** When my team's Auditor verifies Naya 5's team's PR, both ledgers record an entry pointing at the same evidence. The recorded action is the verified action — on both sides.
3. **Lessons travel, proof travels with them.** When a team proves a lesson, it publishes it to a shared place. Other teams try to reproduce it and record what happened, citing the original. Reproduction — not announcement — is what makes a lesson network-true.

This file is the **spec** (what we agree). Enforcement (the gates and scripts that check the agreement) comes later, in a separate piece of work.

## 1. The ground truth this builds on

- Every ledger entry follows the **canonical receipt envelope**: `actor`, `action`, `evidence` (non-empty — a receipt with no evidence is a claim, not a receipt), `timestamp` (ISO-8601), `scope` (one of `self | team | collective | public`), and a free `metadata` dict. Each entry has a deterministic `receipt_id` (sha256 over the canonical JSON of the envelope) — this is the identifier other ledgers cite.
- A team's ledger lives in two places: a **ledger issue** on GitHub (the human-readable chain of proof) and a **ledger JSON** (the machine-readable books, e.g. `team-ledger/team-ledger.machine.json`, schema `naya.team-ledger.v1`).
- **Scopes govern visibility.** Only entries with scope `team`, `collective`, or `public` may be cited across teams. `self`-scoped entries are private and are never valid citation targets.
- The Builder-Scorer Loop already requires scorer ≠ builder. Across teams, that rule is stricter: the verifier must be a **distinct seat** from the builder, and the requester must name the builder up front.

Known ledgers today:

| team_id | Team | Ledger issue | Lane feed(s) | Ledger JSON |
|---|---|---|---|---|
| `naya2-team` | Naya 2's team — 12 area agents (Compounder/LEARN, Librarian/KNOW, Bridger/ACT, Judge/LAW, Auditor/PROVE, Builder/BUILD, Electrician/WIRE, Captain/TEAM, Mechanic/INFRA, Host/PRODUCT, Archivist/MEMORY, Keeper/GOVERN) | #2398 | #2175 | `team-ledger/team-ledger.machine.json` (`naya.team-ledger.v1`) |
| `naya5-team` | Naya 5's team — 12 leads (Naya Alpha/LEARN … Naya Mu/Human Value) | #2396 | #1713, #1714, #1715 | (their ledger path, registered on join) |

---

## 2. The trust law (read this before everything else)

1. **Ledgers never edit each other's entries.** Not to fix, not to help, not to annotate. You cite them or you leave them alone.
2. **A citation is proof only when the cited entry exists.** If you cite a receipt_id you can't resolve to a real entry in the partner's ledger, the citation is `unresolved` — a claim, not proof. `UNKNOWN ≠ PASS` applies across the network.
3. **The recorded action is the verified action, on both sides.** A cross-ledger event isn't real until each side has recorded its own entry and each cites the other. One-sided records are announcements.
4. **Every cross-ledger entry names its evidence.** No "trust me, I checked" — the evidence link points at the same bytes on both sides.
5. **Expired or declined is a recorded state, never silence.** If a request goes unanswered, the expiry is written down. Silence is not an answer and never counts as one.

---

## 3. Cross-ledger receipt links

**The scenario:** my team's Auditor independently verifies Naya 5's team's PR. Two ledgers, one truth. Here's how.

### 3.1 The entry shape

Each side writes a **normal ledger entry** (its own envelope, its own receipt_id) and puts a `cross_ref` block in `metadata`. Nothing else about the entry changes.

```json
{
  "actor": "naya2-team/auditor",
  "action": "verification.response",
  "evidence": ["https://github.com/SoulSchoolAcademy/NayaPOWER/pull/2401#issuecomment-6020000000"],
  "timestamp": "2026-10-11T23:50:00Z",
  "scope": "collective",
  "metadata": {
    "cross_ref": {
      "protocol": "naya.inter-ledger.v1",
      "event_type": "verification",
      "event_id": "xl-naya2-team-2026-10-11-0042",
      "partner_team": "naya5-team",
      "partner_entry": "9f2c…a41d",
      "partner_evidence": "https://github.com/SoulSchoolAcademy/NayaPOWER/issues/2396#issuecomment-6019999999",
      "citation_role": "verifies",
      "citation_state": "pending"
    }
  }
}
```

### 3.2 The `cross_ref` fields

| Field | Required | Meaning |
|---|---|---|
| `protocol` | yes | Always `naya.inter-ledger.v1`. Lets machines find protocol traffic. |
| `event_type` | yes | One of `verification`, `reproduction`, `co_sign`, `request`, `answer`, `lesson`. What kind of cross-ledger event this is. |
| `event_id` | yes | Shared event identifier both sides use, format `xl-<team-id>-YYYY-MM-DD-NNNN` (the team that opens the event prefixes its own id; N = that team's per-day sequence). Both sides' entries carry the same `event_id`. |
| `partner_team` | yes | The `team_id` of the cited team. If it's not in the registry (§7), the citation is still valid — the registry is for *discovery*, not permission. The scoreboard only aggregates registered teams. |
| `partner_entry` | yes | The partner's entry `receipt_id` being cited. |
| `partner_evidence` | yes | A checkable pointer to the partner's entry: an `https://` URL (ledger issue comment, evidence link) **or** a repo path pinned at a commit SHA (`path/to/file.md@<sha>`). Must be checkable by a stranger. |
| `citation_role` | yes | This entry's role relative to the partner: `verifies`, `is_verified_by`, `reproduces`, `is_reproduced_by`, `requests`, `is_requested_by`, `answers`, `is_answered_by`, `co_signs`, `publishes`, `registers`. |
| `citation_state` | yes | What the *writer* knew at write time: `pending` (I cited them; their side not yet observed) or `unresolved` (the cited entry couldn't be found — this entry is a claim, not proof). `mutual` is never written into an entry — it is derived by readers per §3.3. |

### 3.3 The two-way handshake

Ledger entries are **append-only and frozen** — a written entry is never edited, so no entry's `citation_state` is ever "flipped" after the fact. The handshake works like this:

1. **Side A records.** Team A writes its entry with `cross_ref.citation_state = "pending"`, citing side B's entry (or, if side B hasn't written yet, the shared evidence — e.g. the PR — with `partner_entry` filled in as soon as side B's entry exists).
2. **Side B records.** Team B writes its own entry citing side A's `receipt_id`, also `pending`.
3. **Mutual is derived, not stored.** A link is `mutual` when a reader can find **both** entries and each cites the other. `mutual` is computed by whoever reads the network (the scoreboard, an auditor, a curious Naya) — it is never written into an entry. Either side may additionally record a `link.confirmed` entry as corroboration, but the confirmation is optional; the two citations are the proof.

**Worked example — the Auditor scenario:**

- Naya 5's Builder merges a PR and records `build.complete` in #2396 (receipt `b5…`).
- Naya 2's Auditor runs the independent check and records `verification.response` in #2398 (receipt `a2…`), citing `b5…` with role `verifies`, state `pending`, evidence = the PR comment containing the scorecard.
- Naya 5's team records `verification.received` in #2396 citing `a2…`, role `is_verified_by`, state `pending`.
- Any reader now finds both citations and derives `mutual`. The verification is a network fact, checkable from either ledger.

### 3.4 JSON schema sketch

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "naya.inter-ledger.cross-ref.v1",
  "type": "object",
  "required": ["protocol", "event_type", "event_id", "partner_team", "partner_entry", "partner_evidence", "citation_role", "citation_state"],
  "properties": {
    "protocol": { "const": "naya.inter-ledger.v1" },
    "event_type": { "enum": ["verification", "reproduction", "co_sign", "request", "answer", "lesson"] },
    "event_id": { "type": "string", "pattern": "^xl-[a-z0-9-]+-\\d{4}-\\d{2}-\\d{2}-\\d{4}$" },
    "partner_team": { "type": "string", "minLength": 1 },
    "partner_entry": { "type": "string", "minLength": 1 },
    "partner_evidence": { "type": "string", "minLength": 1, "description": "https URL, or <repo-path>@<commit-sha>" },
    "citation_role": { "enum": ["verifies", "is_verified_by", "reproduces", "is_reproduced_by", "requests", "is_requested_by", "answers", "is_answered_by", "co_signs", "publishes", "registers"] },
    "citation_state": { "enum": ["pending", "unresolved"], "description": "State at write time only. 'mutual' is derived by readers, never stored." }
  }
}
```

**On `co_sign`:** a team may co-sign another team's entry (role `co_signs`, event type `co_sign`) to publicly endorse it without re-verifying. A co-sign is weaker than a verification — it says "we stand by this" without new evidence — and it never counts as independent verification in the Builder-Scorer Loop. The scoreboard tracks co-signs separately from verifications.

---

## 4. Learning propagation

**The scenario:** one team's Compounder proves a lesson ("this test battery catches this class of break"). That lesson should make every team smarter — but only if it's real. Publication is cheap; reproduction is the proof.

### 4.1 Publication format — the lesson card

A published lesson is a file plus an announcement:

- **File:** `BRAIN/07-LEARNING/network-lessons/L-NNNN-<slug>.md`, where `NNNN` is the next free lesson number (first claim stands; the publishing team re-runs the collision check immediately before claiming — same discipline as Smart Notes).
- **Announcement:** a comment on the protocol hub issue (the coordinator assigns the issue; all network announcements live there in one thread per lesson).

The card has a machine front-matter block and human prose below it:

```markdown
---
lesson_id: L-0042
title: "Sequential baker dies silently under fork pressure; SN-0501 fix pattern"
origin_team: naya2-team
origin_entry: "<receipt_id of the ledger entry where the lesson was proven>"
origin_evidence: "https://github.com/SoulSchoolAcademy/NayaPOWER/pull/2355"
published_at: "2026-10-11T23:55:00Z"
scope: collective
expected_result: "Baker completes all waves; zero silent deaths over 6 consecutive runs"
falsifier: "Any silent death after the fix = lesson is FALSE, not unlucky"
repro_steps:
  - "Run tools/bake.sh --waves 6 on a clean checkout of <sha>"
  - "Watch the baker log for exit-without-receipt lines"
  - "Count silent deaths: expect 0"
status: PUBLISHED
---

## In a nutshell
<plain-English: what the lesson is, why it matters>

## How to reproduce
<numbered steps a stranger's Compounder can follow>

## What "reproduced" means
<the exact observable bar>
```

Required front-matter fields: `lesson_id`, `title`, `origin_team`, `origin_entry`, `origin_evidence`, `published_at`, `expected_result`, `falsifier`, `repro_steps`, `status`. The `falsifier` is mandatory — a lesson that can't say what would prove it wrong isn't published, it's announced.

### 4.2 Reproduction — the citation format

Another team's Compounder attempts the reproduction and records the outcome **in its own ledger** (action `reproduction.report`), citing the lesson:

```json
"metadata": {
  "cross_ref": {
    "protocol": "naya.inter-ledger.v1",
    "event_type": "reproduction",
    "event_id": "xl-naya5-team-2026-10-12-0007",
    "partner_team": "naya2-team",
    "partner_entry": "<receipt_id of the lesson's origin entry>",
    "partner_evidence": "https://github.com/SoulSchoolAcademy/NayaPOWER/blob/main/BRAIN/07-LEARNING/network-lessons/L-0042-sequential-baker.md",
    "citation_role": "reproduces",
    "citation_state": "pending"
  },
  "repro": {
    "lesson_id": "L-0042",
    "outcome": "REPRODUCED",
    "evidence": ["<link to the run log / receipt>"],
    "notes": "6/6 waves clean on our infra; matches expected_result"
  }
}
```

`outcome` is one of:
- `REPRODUCED` — the expected result held; evidence attached.
- `FAILED` — the falsifier fired or the expected result didn't hold; evidence attached. A FAILED with real evidence moves the lesson to `CONTESTED`.
- `PARTIAL` — reproduced under different conditions; `notes` must say exactly what differed.

### 4.3 Lesson lifecycle

- `PUBLISHED` → first independent reproduction attempt recorded.
- `ADOPTED` → two or more **independent** teams recorded `REPRODUCED` (independent = different team_id; same-team re-runs don't count).
- `CONTESTED` → any `FAILED` with evidence. The originating team must respond (re-produce, fix the card, or withdraw) — a contested lesson stays contested until resolved.
- `WITHDRAWN` → the origin team pulls it; the card stays in place marked withdrawn (history is never deleted).
- `STALE` → no reproduction attempt in 30 days. Stale lessons are re-published, not trusted.

The scoreboard (§6) tracks lessons published, reproductions, and adoption rate per team — that's the compounding metric Shawn asked for: intelligence compounding *across* teams, not just inside them.

---

## 5. Verification requests

**The scenario:** my Builder wants a distinct-seat scorecard from Naya 5's team — a scorer who shares no code, no context, and no incentives with the builder.

### 5.1 The request format

The requester records a ledger entry (action `verification.request`, scope `collective`) with a `request` block in metadata:

```json
"metadata": {
  "request": {
    "request_id": "vr-naya2-team-2026-10-11-0013",
    "target_team": "naya5-team",
    "target_lane": "Naya Epsilon / VERIFY",
    "subject": { "kind": "pr", "ref": "https://github.com/SoulSchoolAcademy/NayaPOWER/pull/2401" },
    "question": "Independent scorecard: does this PR meet the 9.0 bar? Score the method, not just the verdict.",
    "builder_identity": "naya2-team/builder",
    "context_evidence": ["<link to the PR body>", "<link to the battery receipt>"],
    "deadline": "2026-10-12T23:40:00Z",
    "requester_agent": "naya2-team/builder"
  }
}
```

Required fields: `request_id` (format `vr-<team-id>-YYYY-MM-DD-NNNN`, unique per requester), `target_team`, `target_lane` (the specific lane/agent asked — not "somebody"), `subject`, `question`, `builder_identity` (the scorer-independence disclosure), `deadline` (ISO-8601; default 24h from the request if the requester doesn't set one).

### 5.2 Where it lives and how it's answered

- The requester **posts the request as a comment on the target team's lane-feed issue** (e.g. Naya 5's VERIFY lane feed), quoting the `request_id` and linking the requester's ledger entry. That comment thread is the rendezvous point — the whole exchange happens there, in the open.
- The target team's lane agent answers **on the same thread** and records a ledger entry in **their own** ledger (action `verification.response`, scope `collective`), with `metadata.response`:

```json
"metadata": {
  "cross_ref": { "...": "...", "event_type": "verification", "citation_role": "answers", "...": "..." },
  "response": {
    "request_id": "vr-naya2-team-2026-10-11-0013",
    "verdict": "PASS" | "FAIL" | "NEEDS_WORK",
    "score": 9.3,
    "evidence": ["<link to the independent run / scorecard>"],
    "verifier_agent": "naya5-team/naya-epsilon",
    "notes": "Scored the method: adversarial probe included, train/test split present. Why not a 10: ..."
  }
}
```

- The requester then records `verification.received` citing the response (role `is_answered_by`), closing the handshake per §3.3.

### 5.3 Deadlines, declines, expiry

- The target team may answer, or **decline with a reason** (`verification.declined` + reply on the thread — e.g. "lane overloaded, try Naya Theta / Retrieval"). A declined request is closed, not failed.
- If the deadline passes with no answer and no decline, the requester records `verification.expired` and proceeds per its own standing protocol (its Judge decides the fallback — e.g. a same-team but different-agent scorecard, disclosed as weaker). **An expired request is a recorded fact about the target lane's responsiveness, and the scoreboard counts it.** Silence is never an answer.
- A requester may not re-issue the identical request to a second team to shop for a better score. If the first answer is disputed, the dispute is recorded as a new `verification.request` citing the first one (`supersedes: <request_id>`), and both scorecards stand in the record.

---

## 6. Scoreboard aggregation — the network-level view

### 6.1 What it is

Two files, same truth, two tongues (per the three-language standard; the machine file is authoritative for systems, the markdown for Nayas):

- `BRAIN/90-OPERATIONS/NETWORK-SCOREBOARD.md` — the human view.
- `BRAIN/90-OPERATIONS/network-scoreboard.machine.json` — schema `naya.network-scoreboard.v1`.

### 6.2 What it aggregates

**Per registered team:**
- `team_id`, `team_name`, ledger issue URL, lane feed URLs.
- `agent_count`, `team_average_score`, `score_delta_7d` (scores move only on independent scorer receipts — the scoreboard never invents movement).
- `entries_24h` (ledger appends in the last 24h — the pulse check).
- Cross-ledger activity: `verifications_requested`, `verifications_answered`, `verifications_received`, `expired_requests`, `avg_distinct_seat_score` (average score given *by other teams'* verifiers), `co_signs_given`, `co_signs_received` (tracked separately from verifications — a co-sign is an endorsement, not an independent check).
- Learning: `lessons_published`, `reproduction_attempts`, `reproductions_ok`, `adoption_rate`.
- `last_activity_at`, and a `ledger_state` flag: `LIVE` (append in last 24h), `QUIET` (24–72h), `STALE` (>72h), `UNKNOWN` (ledger unreadable).

**Network totals:**
- `teams_registered`, `teams_live`, `mutual_links` (closed §3.3 handshakes), `open_requests`, `lessons_adopted`, `network_verification_volume_7d`.

### 6.3 Refresh

- The scoreboard is **regenerated hourly** from the registered ledgers (the generator reads each team's ledger JSON at the current main tip and the ledger issues' recent comments; generation itself is a ledger-recorded action by whichever team runs it).
- Every generated file stamps `generated_at` and `basis_tip` (the main-tip SHA it read). A scoreboard whose `basis_tip` is behind the live tip says so on its face — stale scoreboards don't pretend to be current.
- Enforcement of the refresh (the cron, the generator, the staleness gate) is the later mechanism piece — this spec only defines what the output must contain and how to read it.

---

## 7. Ledger discovery — how a new team joins the network

A new team doesn't ask permission. It registers, and the network can see it.

### 7.1 The registry

- `BRAIN/90-OPERATIONS/network-registry.machine.json` — the index of teams (machine list; schema `naya.network-registry.v1`).
- Each team owns exactly one file: `BRAIN/90-OPERATIONS/network-registry/<team-id>.json`. **A team writes only its own file** — the trust law applies to the registry too.
- Complementary GitHub-side discovery: every ledger's anchor issue carries the title prefix `📒 Smart Ledger —` and the label `smart-ledger` (see SMART-LEDGER-PROTOCOL.md §6). The registry is the machine source of truth; the label is the human-searchable one. Both must agree.

### 7.2 The registration file

```json
{
  "team_id": "naya6-team",
  "team_name": "Naya 6's team",
  "lead_seat": "naya-6",
  "ledger_issue": "https://github.com/SoulSchoolAcademy/NayaPOWER/issues/2410",
  "ledger_json_path": "team-ledger-n6/team-ledger.machine.json",
  "ledger_schema": "naya.team-ledger.v1",
  "lane_feeds": ["https://github.com/SoulSchoolAcademy/NayaPOWER/issues/2411"],
  "agents": [
    { "name": "Compounder", "area": "LEARN", "lane": "[LANE LEARN]" }
  ],
  "scopes_shared": ["team", "collective", "public"],
  "registered_at": "2026-10-12T00:00:00Z",
  "status": "active"
}
```

Required: `team_id` (kebab-case, unique — first claim stands, checked against the live registry at registration time), `team_name`, `lead_seat`, `ledger_issue`, `ledger_json_path`, `ledger_schema`, `lane_feeds`, `agents` (name + area), `registered_at`, `status` (`active` | `paused` | `retired`).

### 7.3 The registration act

1. The new team opens a PR adding its `<team-id>.json` (and updating the registry index in the same PR — its own addition only).
2. It announces on the protocol hub issue: "team X registered, ledger at #issue, JSON at path, schema S."
3. The scoreboard picks the team up on its next hourly run. No approval step — registration is a recorded fact, and a bogus registration is visible to everyone (that's the point of doing it in the open).

---

## 8. Worked end-to-end example

Naya 5's Builder finishes a PR. Naya 2's Auditor is asked for a distinct-seat scorecard.

1. **Request** — Naya 2's Builder records `verification.request` (#2398, receipt `r1`), posts it as a comment on Naya 5's VERIFY lane feed (#1713), deadline 24h. `builder_identity: naya2-team/builder` is disclosed.
2. **Answer** — Naya Epsilon scores it 9.3/10 on the thread, records `verification.response` (#2396, receipt `r2`) with `cross_ref` citing `r1`, role `answers`, evidence = the scorecard comment.
3. **Close** — Naya 2's Builder records `verification.received` (#2398) citing `r2`, role `is_answered_by`. Any reader now derives `mutual` from the two citations — the link is closed without either side touching the other's ledger.
4. **Lesson** — The Auditor notices the PR's sabotage battery caught a fail-open gate. Naya 2's Compounder publishes lesson card `L-0043` with a falsifier. Naya 5's Compounder reproduces it, records `reproduction.report` (`REPRODUCED`) in #2396 citing the lesson's origin entry.
5. **Scoreboard** — The hourly run shows: naya2-team × naya5-team mutual link #N, one distinct-seat 9.3, L-0043 one step closer to ADOPTED. Shawn sees the network compounding — not in a claim, in the books.

---

## 9. Non-goals (what this protocol deliberately does not do)

- **No shared writes, ever.** There is no "network ledger" that teams write into together. The network view is *derived* from team ledgers, never a ledger itself.
- **No cross-team entry edits.** Corrections to a cited entry are new entries in the owning ledger (a correction cites the original — history is never rewritten).
- **No private data crossing.** `self`-scoped entries are invisible to the protocol. If it's not shareable, it's not citable.
- **No identity federation.** Teams authenticate to their own lanes; the protocol trusts the ledger issue + JSON the team registered, nothing more. Key management is a later mechanism piece.
- **No dispute court.** Contested lessons and disputed scorecards stay visible with both sides recorded. The protocol records disagreement faithfully; it doesn't resolve it.

---

## 10. Schema index

| Schema | File / location | Purpose |
|---|---|---|
| `naya.inter-ledger.cross-ref.v1` | §3.4 of this spec | The citation block inside any cross-ledger entry |
| `naya.inter-ledger.verification-request.v1` | §5.1 (fields listed; full schema in the mechanism piece) | Request envelope |
| `naya.inter-ledger.verification-response.v1` | §5.2 (fields listed) | Answer envelope |
| `naya.inter-ledger.lesson-card.v1` | §4.1 front-matter | Lesson publication |
| `naya.inter-ledger.repro-report.v1` | §4.2 `repro` block | Reproduction outcome |
| `naya.network-registry.v1` | `BRAIN/90-OPERATIONS/network-registry.machine.json` | Team index |
| `naya.network-scoreboard.v1` | `BRAIN/90-OPERATIONS/network-scoreboard.machine.json` | Aggregated network view |

---

*Agreement first, mechanism later. When the teams agree on this file, the next piece of work builds the gates that check it — the receipt-link verifier, the scoreboard generator, the registry watcher. Spec now, code after the handshake.*

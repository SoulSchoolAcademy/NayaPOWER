# NayaNET Protocol v1 — The Language of the Net

**Status:** CANDIDATE (Naya 4, 2026-10-11) — needs Shawn's ratification to become law.
**Purpose:** How independent nodes (teams) on NayaNET talk to each other, verify each other, and compound intelligence across the net — not just within one team.

---

## The idea in one paragraph

Every node keeps its own ledger of verified actions — who did what, with what receipt and evidence. All ledgers speak the same schema. Nodes find each other through a shared registry. When nodes need to coordinate, they write a contract: machine-readable, automatically verified, automatically recorded. A receipt in one ledger can cite evidence from another. Trust is structural — you don't trust the node, you read its ledger.

---

## 1. The shared schema (the handshake)

If your ledger speaks this schema, you're on the net. No permission needed — the schema IS the handshake.

Every ledger entry (one JSON object per line, `.jsonl`):

```json
{
  "tick": "t962",
  "node": "naya-team-naya",
  "team": "Team 3",
  "agent": "Naya Judge",
  "task": "DecisionEngine consolidation preserving strict harm bar",
  "score": 8.5,
  "status": "VERIFIED",
  "receipt": "twelve-lane-receipts/t962-lane3.md",
  "evidence": "branch naya/three-decision-consolidate @ 3f1cdfa6, 338 tests green",
  "ts": "2026-10-11T23:45:00Z"
}
```

Required fields: `node`, `team`, `agent`, `task`, `score`, `status`, `ts`.
Optional: `tick`, `receipt`, `evidence`, `contract` (contract ID if this action fulfills one).

`status` is one of: `VERIFIED` (8+, artifacts checked) · `PARTIAL` (5–7) · `WEAK` (<5) · `PHANTOM` (claimed, never existed — recorded, not hidden).

## 2. Node registry

One file per network: `LEDGER/nodes.json`. Append-only. A node registers itself:

```json
{
  "node_id": "naya-team-naya",
  "display_name": "Team Naya — 12 lanes",
  "ledger_ref": "SoulSchoolAcademy/NayaPOWER@naya/mission-state:LEDGER/activity-ledger.jsonl",
  "schema_version": "1",
  "registered_at": "2026-10-11T23:45:00Z",
  "status": "ACTIVE",
  "contact": "Naya 4 (charter seat)"
}
```

`ledger_ref` format: `<repo>@<branch>:<path>`. Any node can read any other node's ledger with git protocol (free) — no permission, no API key. Reading is open; writing is local-only (each node writes only its own ledger).

## 3. Cross-ledger references

A receipt in Node A cites evidence from Node B:

```
nayanet://<node_id>/receipt/<receipt-id>
```

Example: `nayanet://naya-team-naya/receipt/t942-lane3` — resolves via the registry to the ledger entry, which points to the receipt file and evidence. If the referenced entry's status is `PHANTOM`, the citing receipt inherits the flag — phantoms propagate as warnings, not silently.

## 4. Smart contracts

Not blockchain. Agreements between nodes/teams: who delivers what, by when, how it's verified. Machine-readable, automatically checked, recorded in both ledgers.

Contract file: `LEDGER/contracts/NC-<NNN>.json`:

```json
{
  "contract_id": "NC-001",
  "version": "1",
  "title": "DecisionEngine consolidation verification",
  "parties": [
    {"node": "naya-team-naya", "team": "Team 3", "agent": "Naya Judge", "role": "builder"},
    {"node": "naya-team-naya", "team": "Team 8", "agent": "Naya Sentinel", "role": "verifier"}
  ],
  "terms": [
    {
      "party": "Team 3",
      "delivers": "DecisionEngine consolidation preserving 7.0/0.05 harm bar",
      "by": "2026-10-12T12:00:00Z",
      "proof": "receipt + branch on remote + 338 tests green + bar preserved"
    }
  ],
  "verification": {
    "verifier": "Team 8",
    "method": "independent cross-seat scorecard + artifact check",
    "pass_criteria": "zero production call sites, behavioral equivalence, strict bar preserved"
  },
  "status": "ACTIVE",
  "evidence": [],
  "created_at": "2026-10-11T23:45:00Z",
  "created_by": "Naya 4 (protocol genesis)"
}
```

`status`: `PROPOSED` → `ACTIVE` → `FULFILLED` | `BREACHED`. A breach is recorded in both parties' ledgers — not as punishment, as data. The net learns from breaches.

**Verification is automatic:** when a builder's ledger entry references a contract ID, any node can check: does the entry's evidence satisfy the contract's proof? The check is mechanical — receipt exists, artifacts verify, criteria met. No meeting required.

## 5. What the net guarantees (and doesn't)

**Guarantees:**
- Every node's ledger is readable by every other node (git protocol, no auth).
- Every entry follows the shared schema (or it's not on the net).
- Phantoms are flagged, never hidden — a node that hides phantoms loses trust structurally (its verification rate drops, visible to all).
- Contracts are enforced by verification, not by authority.

**Doesn't guarantee:**
- That any node's claims are true — only that they're checkable. Verification is always available; trust is always earned.
- Ordering across nodes — each node's tick is local. Cross-node causality comes from references, not clocks.

## 6. Growing the net

1. A new team builds its ledger in the shared schema (copy the writer, adapt the teams).
2. It registers in `LEDGER/nodes.json` (PR to the registry, or the founding node adds it).
3. It starts writing contracts with other nodes.
4. The net grows: 2 nodes → 12 → hundreds. Each node compounds its own intelligence; contracts compound it across nodes.

---

**Genesis:** Node 1 (`naya-team-naya`, Team Naya, 12 teams) registered 2026-10-11. Contract NC-001 (the DecisionEngine verification) is the first contract — formalizing a cross-verification that already happened. Node 2 (Naya 5's team) pending registration.

*"The connections are the thing."* — Shawn Vibert, 2026-10-11

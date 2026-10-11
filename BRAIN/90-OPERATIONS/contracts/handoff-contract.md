# Handoff Contract — `naya.handoff-contract.v1`

**Status:** SPEC (prose + schema). Enforcement comes later — this document is the agreement, not the code.

## 1. Purpose, in plain words

Work crosses team boundaries constantly: Team A finishes something Team B needs. Too often the handoff is a message — "it's done, it's over there" — and Team B discovers three days later that "over there" was missing a piece. This contract makes the handoff a **ledger entry both teams sign**: Team A records what it handed over, Team B records what it received and checked, and the two entries point at each other.

The rule underneath it: **nothing is handed off until the receiving team says it arrived whole.** And if it didn't arrive whole, the rejection is recorded with reasons — returned, never silently dropped.

This contract is not blockchain. It is a machine-readable promise between teams: *"I finished work you need. Here it is, here's how to check it, and we both sign when you agree it's complete."*

---

## 2. The agreement, in precise terms

### 2.1 The two parties

- **Producer team** — finished the work and initiates the handoff. Its agent is whoever did the work (often the **Builder**, but any of the twelve seats may produce).
- **Consumer team** — needs the work and accepts (or rejects) the handoff. Its agent is whoever will use it.

Each party is identified by: team name, its Smart Ledger issue number (e.g. Naya 2's team → issue `#2398`), the acting agent's name, and that agent's area.

### 2.2 Handoff initiation

The producer team proposes the handoff with a **deliverable** that names:

- `title` — what it is, plain words.
- `description` — what it does and what it's for.
- `location` — exactly where it lives, pinned: branch name, PR number, commit SHA, and file paths. Code locations are pinned to a **SHA**, never "latest main" — "latest" moves.
- `how_to_verify` — how the consumer checks each acceptance criterion (2.3). If the producer can't say how to check it, the handoff isn't ready to propose.
- `needed_by` (optional) — the date the consumer needs it. Sets the clock for expiry (2.8).

A handoff proposed without pinned locations or without `how_to_verify` is not a handoff — it's a rumor of a handoff. The consumer team may decline to accept the proposal until those exist, and that declination is recorded, not awkward.

### 2.3 Acceptance criteria

Every handoff carries explicit **acceptance criteria** — each one objectively checkable, each with a stated check method:

- `criterion` — what must be true (e.g. "The migration applies cleanly on a fresh checkout at the pinned SHA").
- `how_to_check` — the exact check (e.g. "Run `tools/verify.sh` from the repo root at that SHA; exit 0").

"Looks good" is not a criterion. "Works on my machine" is not a check. If a criterion can't be checked by someone who didn't build it, rewrite the criterion.

Criteria are agreed at activation. The consumer team may propose additional criteria before accepting the contract; the producer may negotiate. The agreed list is frozen in the contract record — acceptance is measured against *that list*, not against later wishes.

### 2.4 Both-teams-sign

The handoff is complete only when **two ledger entries exist, pointing at each other**:

1. **Producer's entry** (in the producer team's ledger): *"Handed off <deliverable> to <consumer team> — contract HC-…; their acceptance entry: <ref>."*
2. **Consumer's entry** (in the consumer team's ledger): *"Received <deliverable> from <producer team> — all N acceptance criteria checked and passing — contract HC-…; their handoff entry: <ref>."*

Each entry carries a `counterparty_entry` field naming the other team's entry. One signature is a claim. Two signatures, cross-referenced, is a receipt. The contract reaches `fulfilled` only when both exist.

The acceptance record details every criterion: `criterion`, `result` (`pass`/`fail`), `checked_by` (agent name), `evidence` (what the check produced), and `checked_at`.

### 2.5 Rejection — returned, never silently dropped

If the consumer team finds the handoff incomplete, the rejection is a first-class recorded event:

- `rejected_by`, `rejected_at`.
- `reasons` — one per failed criterion: which criterion failed, what was observed, what is missing. Reasons are specific enough that the producer can act on them without asking a follow-up question.
- The deliverable is **returned** to the producer. The contract stays `active`; an event `rejected_returned` is appended.
- The producer resubmits against the same contract (new pinned location, new SHA if code changed). The rejection reasons become the producer's work list.
- **Rejections accumulate.** A contract may be rejected more than once; each rejection is appended to the `rejections` array, never overwritten. "Rejected twice, accepted on the third" is a healthy visible history, not an embarrassment.

What must never happen: the consumer finds the handoff incomplete and says nothing — no quiet fix on their side, no silent abandonment of the dependency. **Silence is the breach** (see 2.7). A recorded rejection with reasons is honorable; a dropped handoff nobody mentions is how teams learn not to trust each other.

A rejection is not a breach and not a failure. It is the contract's quality gate doing its job — the same way a scorer's "why not 10" list is the Builder-Scorer Loop doing its job.

### 2.6 Fulfillment

The contract is **fulfilled** when:

1. Every acceptance criterion in the agreed list has a `pass` result with named checker and evidence,
2. Both teams' ledger entries exist, each with `counterparty_entry` pointing at the other.

**Coverage invariant:** the acceptance `results` array must contain exactly one result per agreed criterion — no fewer (a missing check is not a pass), no duplicates. `results.length == acceptance_criteria.length`, and every criterion string appears exactly once.

Partial acceptance is not fulfillment. "Four of five criteria pass, we'll take it" is recorded as a **rejection with reasons** plus a *new* proposal with a reduced criterion list — the record stays honest about what was actually delivered.

### 2.7 Breach

The following are breaches of this contract, recorded in both ledgers with facts, evidence, and repair (see section 3):

- **Silent drop:** the consumer found the handoff incomplete (or simply never got around to it) and recorded nothing — no acceptance, no rejection. The handoff died quietly.
- **Phantom acceptance:** the consumer signed acceptance without running the checks, or recorded `pass` for criteria that were never checked.
- **Moving deliverable:** the producer changed the deliverable's location/content after proposing it without recording a new pinned location — the consumer checked one thing, something else shipped.
- **Abandonment:** the producer stops responding to a returned handoff past `needed_by` with no recorded explanation.
- **Claimed fulfillment:** the handoff is described as complete anywhere (a comment, a report, a feed post) while the consumer's signature is missing.

### 2.8 Expiry

- If `needed_by` passes and the consumer no longer needs the deliverable — the world moved on — either team may mark the contract **expired** with a recorded reason. No fault. The work may still be useful elsewhere; the ledger says what happened.
- If the producer's pinned location becomes invalid (branch deleted, SHA unreachable) before acceptance, the contract does not auto-expire — the producer re-pins under the same contract via event. Only the *need* expiring, or mutual agreement, ends it.

---

## 3. Lifecycle states

| State | Meaning | How it is entered |
|---|---|---|
| `proposed` | Handoff proposed: deliverable pinned, criteria listed, consumer named. Not yet accepted. A proposal declined pending fixes stays here, with a `proposal_declined` event recording why. | Producer records the proposal. |
| `active` | Consumer accepted the criteria. The producer is on the hook to deliver; the consumer is on the hook to check. | Both teams record acceptance of the criteria. |
| `fulfilled` | All criteria pass, both teams signed per 2.6. | Both cross-referencing ledger entries exist. |
| `breached` | A term in 2.7 was violated. Recorded in both ledgers with facts and repair. | Breach declared by either team, with evidence. |
| `expired` | The need passed (`needed_by`) or both teams agreed the handoff is moot. | Declared with reason; no fault attached. |

A contract never moves backward. A rejection returns the *deliverable* for rework; the *contract* stays `active` with the rejection on its record. Resubmission appends events — the history of "rejected twice, accepted on the third" is visible and valuable.

### Breach handling — recorded honestly, in both ledgers

A breached contract is a **signal, not a punishment**. The breach record contains:

- `what_was_promised` — the term that was broken, quoted from the agreement.
- `what_happened` — the facts, with evidence links. No adjectives, no blame language.
- `systemic_cause` — the honest best guess at *why*: was the criterion uncheckable? Was the consumer overloaded? Did nobody own the checking step? "We don't know yet" is acceptable; pretending to know is not.
- `repair` — what changes so this class of breach doesn't repeat. Feeds the team's learning loop.

Both teams record the breach. Disputes are recorded **alongside** the breach — both claims visible, no silent edits. And one rule specific to this contract: **the silent drop is the breach this contract exists to kill.** Every other breach class has a mechanical fix; the silent drop is cultural. The repair for a silent drop must name the cultural fix — who owns the checking step next time, and what reminder exists so "I'll get to it" can't quietly become "nobody did."

---

## 4. JSON schema — `naya.handoff-contract.v1`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://nayanet.technology/schemas/naya.handoff-contract.v1",
  "title": "naya.handoff-contract.v1",
  "description": "Agreement between a producer team and a consumer team: the handoff is a ledger entry both teams sign, against explicit acceptance criteria. Rejections are recorded with reasons — never silently dropped.",
  "type": "object",
  "required": [
    "schema_version", "contract_id", "contract_type", "state",
    "producer_team", "consumer_team", "deliverable",
    "acceptance_criteria", "events"
  ],
  "properties": {
    "schema_version": { "const": "naya.handoff-contract.v1" },
    "contract_id": {
      "type": "string",
      "pattern": "^HC-[0-9]{8}-[0-9]{3}$",
      "description": "e.g. HC-20261011-001"
    },
    "contract_type": { "const": "handoff" },
    "state": {
      "type": "string",
      "enum": ["proposed", "active", "fulfilled", "breached", "expired"]
    },
    "producer_team": { "$ref": "#/$defs/party" },
    "consumer_team": { "$ref": "#/$defs/party" },
    "needed_by": {
      "type": "string",
      "format": "date-time",
      "description": "Optional. When the consumer needs the deliverable; sets the expiry clock."
    },
    "deliverable": {
      "type": "object",
      "required": ["title", "description", "location", "how_to_verify"],
      "properties": {
        "title": { "type": "string", "minLength": 1 },
        "description": { "type": "string", "minLength": 1 },
        "location": {
          "type": "object",
          "required": ["kind", "ref"],
          "properties": {
            "kind": {
              "type": "string",
              "enum": ["branch", "pr", "commit", "path", "artifact"],
              "description": "What the ref points at."
            },
            "ref": {
              "type": "string",
              "minLength": 1,
              "description": "Pinned location: SHA, PR number, exact path. Never 'latest'."
            },
            "sha": {
              "type": "string",
              "pattern": "^[0-9a-f]{40}$",
              "description": "Required when kind is branch, pr, or commit: the pinned commit SHA."
            }
          },
          "additionalProperties": false,
          "allOf": [
            {
              "if": { "properties": { "kind": { "enum": ["branch", "pr", "commit"] } } },
              "then": { "required": ["sha"] }
            }
          ]
        },
        "how_to_verify": {
          "type": "string",
          "minLength": 1,
          "description": "How the consumer checks the deliverable. If the producer can't say, the handoff isn't ready."
        }
      },
      "additionalProperties": false
    },
    "acceptance_criteria": {
      "type": "array",
      "minItems": 1,
      "description": "Agreed at activation and frozen. Acceptance is measured against this list.",
      "items": {
        "type": "object",
        "required": ["criterion", "how_to_check"],
        "properties": {
          "criterion": { "type": "string", "minLength": 1 },
          "how_to_check": { "type": "string", "minLength": 1 }
        },
        "additionalProperties": false
      }
    },
    "acceptance": {
      "type": "object",
      "description": "The consumer's check results, one per agreed criterion.",
      "required": ["results"],
      "properties": {
        "results": {
          "type": "array",
          "minItems": 1,
          "items": {
            "type": "object",
            "required": ["criterion", "result", "checked_by", "evidence", "checked_at"],
            "properties": {
              "criterion": { "type": "string", "minLength": 1 },
              "result": { "type": "string", "enum": ["pass", "fail"] },
              "checked_by": { "type": "string", "description": "Agent who ran the check." },
              "evidence": { "type": "string", "minLength": 1 },
              "checked_at": { "type": "string", "format": "date-time" }
            },
            "additionalProperties": false
          }
        }
      },
      "additionalProperties": false
    },
    "rejections": {
      "type": "array",
      "description": "Consumer rejections, appended never overwritten. Each rejection returns the deliverable for rework — rejections are recorded with reasons, never silently dropped.",
      "items": {
        "type": "object",
        "required": ["rejected_by", "rejected_at", "reasons"],
        "properties": {
          "rejected_by": { "type": "string" },
          "rejected_at": { "type": "string", "format": "date-time" },
          "reasons": {
            "type": "array",
            "minItems": 1,
            "items": {
              "type": "object",
              "required": ["criterion", "observed", "missing"],
              "properties": {
                "criterion": { "type": "string", "minLength": 1 },
                "observed": { "type": "string", "minLength": 1 },
                "missing": {
                  "type": "string",
                  "minLength": 1,
                  "description": "What the producer must supply. Specific enough to act on without a follow-up question."
                }
              },
              "additionalProperties": false
            }
          },
          "resubmitted_at": { "type": "string", "format": "date-time" }
        },
        "additionalProperties": false
      }
    },
    "signatures": {
      "type": "object",
      "description": "Both teams sign. Each entry points at the other via counterparty_entry.",
      "required": ["producer", "consumer"],
      "properties": {
        "producer": { "$ref": "#/$defs/signature" },
        "consumer": { "$ref": "#/$defs/signature" }
      },
      "additionalProperties": false
    },
    "breach": { "$ref": "#/$defs/breach" },
    "ledger_refs": {
      "type": "object",
      "description": "Where each team recorded this contract in its own Smart Ledger.",
      "required": ["producer_team", "consumer_team"],
      "properties": {
        "producer_team": { "$ref": "#/$defs/ledger_ref" },
        "consumer_team": { "$ref": "#/$defs/ledger_ref" }
      },
      "additionalProperties": false
    },
    "events": {
      "type": "array",
      "description": "Append-only. State changes are events, never edits.",
      "minItems": 1,
      "items": { "$ref": "#/$defs/event" }
    }
  },
  "$defs": {
    "party": {
      "type": "object",
      "required": ["team_name", "ledger_issue", "agent_name", "agent_area"],
      "properties": {
        "team_name": { "type": "string" },
        "ledger_issue": {
          "type": "integer",
          "minimum": 1,
          "description": "The team's Smart Ledger issue number, e.g. 2398."
        },
        "agent_name": { "type": "string" },
        "agent_area": { "type": "string" }
      },
      "additionalProperties": false
    },
    "signature": {
      "type": "object",
      "required": ["signed_by", "signed_at", "ledger_entry", "counterparty_entry", "statement"],
      "properties": {
        "signed_by": { "type": "string", "description": "Agent who signed." },
        "signed_at": { "type": "string", "format": "date-time" },
        "ledger_entry": {
          "type": "string",
          "description": "This team's ledger entry for the handoff."
        },
        "counterparty_entry": {
          "type": "string",
          "description": "The other team's ledger entry. Both entries point at each other."
        },
        "statement": {
          "type": "string",
          "minLength": 1,
          "description": "Producer: what was handed over. Consumer: that all criteria were checked and passed."
        }
      },
      "additionalProperties": false
    },
    "breach": {
      "type": "object",
      "required": ["declared_by", "declared_at", "what_was_promised", "what_happened", "systemic_cause", "repair"],
      "properties": {
        "declared_by": { "$ref": "#/$defs/party" },
        "declared_at": { "type": "string", "format": "date-time" },
        "what_was_promised": { "type": "string", "minLength": 1 },
        "what_happened": { "type": "string", "minLength": 1 },
        "systemic_cause": { "type": "string", "minLength": 1 },
        "repair": { "type": "string", "minLength": 1 },
        "disputed_by": {
          "type": "object",
          "description": "If the other team disputes the breach, their claim is recorded here — alongside, never instead.",
          "required": ["team", "claim", "at"],
          "properties": {
            "team": { "$ref": "#/$defs/party" },
            "claim": { "type": "string", "minLength": 1 },
            "at": { "type": "string", "format": "date-time" }
          },
          "additionalProperties": false
        }
      },
      "additionalProperties": false
    },
    "ledger_ref": {
      "type": "object",
      "required": ["issue", "entry"],
      "properties": {
        "issue": { "type": "integer", "minimum": 1 },
        "entry": { "type": "string", "description": "The ledger entry id or anchor referencing this contract." }
      },
      "additionalProperties": false
    },
    "event": {
      "type": "object",
      "required": ["event", "at", "by_team", "by_agent"],
      "properties": {
        "event": {
          "type": "string",
          "enum": [
            "proposed", "accepted", "fulfilled",
            "breach_declared", "expired", "dispute_recorded",
            "criteria_agreed", "deliverable_submitted",
            "acceptance_recorded", "rejected_returned", "resubmitted",
            "proposal_declined"
          ]
        },
        "at": { "type": "string", "format": "date-time" },
        "by_team": { "type": "string" },
        "by_agent": { "type": "string" },
        "note": { "type": "string" },
        "ledger_entry": { "type": "string" }
      },
      "additionalProperties": false
    }
  }
}
```

---

## 5. Worked example (short)

Naya 2's **Builder** (ledger `#2398`) finishes the smart-ledger contract specs. Naya 5's team (ledger `#2396`) needs them to wire the network coordinator. Contract `HC-20261011-001` is **proposed**:

- Deliverable: the three spec files, pinned to commit SHA `7d3e…b902` on branch `naya2/smart-ledger-network-v1`.
- Criteria: (1) "All three files exist at `BRAIN/90-OPERATIONS/contracts/` at the pinned SHA" — check: `git ls-tree`; (2) "Each file's JSON schema parses as valid JSON" — check: extract and `json.load`; (3) "The three schemas share the same state enum and breach shape" — check: compare by eye against the spec text.

Naya 5's consumer runs the checks: criteria 1 and 3 pass; criterion 2 fails — extracting the handoff contract's schema block and running `json.load` raises a syntax error (a missing comma after the `signatures` property). **Rejection recorded** in the `rejections` array: criterion "Each file's JSON schema parses as valid JSON", observed "`json.load` raises on the handoff schema block — missing comma", missing "a syntactically valid schema block". The deliverable is returned — never silently dropped.

Naya 2's Builder fixes the block, re-pins to a new SHA, resubmits under the same contract (`resubmitted` event). All three criteria pass. Both teams sign — producer entry cites consumer entry, consumer entry cites producer entry. **Fulfilled.** The record shows "rejected once, accepted on resubmission" — and nobody had to wonder whether the handoff was real.

---

*Spec authored 2026-10-11. Companion contracts: `verification-contract.md`, `learning-contract.md`.*

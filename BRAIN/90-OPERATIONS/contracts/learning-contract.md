# Learning Contract — `naya.learning-contract.v1`

**Status:** SPEC (prose + schema). Enforcement comes later — this document is the agreement, not the code.

## 1. Purpose, in plain words

A lesson that stays inside one team is a rumor with good lighting. A lesson that another team can *reproduce* is knowledge. This contract is the agreement between a team that proved a lesson (**origin team**) and a team whose **Compounder** will attempt to reproduce it (**reproducing team**): *"When you prove a lesson, we will try it on our turf. Whatever happens — success or failure — both our ledgers record it."*

A failed reproduction is data, not shame. It tells the network where the lesson holds, where it breaks, and what the difference was. That is how learning compounds instead of just accumulating.

This contract is not blockchain. It is a machine-readable promise between teams: *"Your lesson, our reproduction attempt, both ledgers, honest verdict."*

---

## 2. The agreement, in precise terms

### 2.1 The two parties

- **Origin team** — proved the lesson and publishes it in a reproducible form. Its agent is whoever proved it (often the **Compounder**, **Auditor**, or **Builder** — the prover is named, whoever they are).
- **Reproducing team** — attempts the reproduction. Its agent is normally the **Compounder** (the LEARN seat), but a team may designate another agent as acting reproducer — recorded explicitly.

Each party is identified by: team name, its Smart Ledger issue number (e.g. Naya 2's team → issue `#2398`), the acting agent's name, and that agent's area.

### 2.2 Lesson publication format

A lesson is not publishable under this contract unless it carries all of the following:

- `lesson_id` — `LESSON-YYYYMMDD-NNN` (e.g. `LESSON-20261011-004`).
- `title` — one line, plain words.
- `claim` — one sentence: what was learned.
- `method` — how it was proven: what was done, what was measured, what the control was. A lesson without a method is an anecdote.
- `behavioral_delta` — the observable change a reproducer should see if the lesson holds. This is the heart of the contract: not "we believe X", but "when you do Y, you will observe Z." If the delta can't be stated observably, the lesson isn't ready for reproduction.
- `evidence_links` — where the proof lives.
- `reproduction_protocol` — ordered steps a stranger could follow: setup, action, observation, how to tell success from failure.
- `published_at` — timestamp (UTC, ISO-8601).
- `valid_until` (optional) — if the lesson is known to be time- or version-bound ("holds for brain-index builds before 2026-11-01"), say so. An expired lesson isn't wrong; it's retired.

A lesson published without a `reproduction_protocol` or without a stated `behavioral_delta` cannot be the subject of a learning contract. The origin team must do that homework first — the reproducing team is not expected to guess what "it worked" means.

### 2.3 Reproduction attempt protocol

The reproducing team's Compounder (or designated agent) runs the attempt:

1. **Read the protocol.** Follow the origin team's `reproduction_protocol` as written.
2. **Record fidelity.** `method_fidelity` is `followed` (steps run as written) or `adapted` (steps changed — with a note saying exactly what changed and why). Adapted is not cheating; undocumented adaptation is.
3. **Run it on their own turf.** The reproduction happens in the reproducing team's own context — their repo state, their data, their environment. That context is recorded as `reproduction_context`.
4. **Observe and record.** `observed` — what actually happened, in concrete terms. Compared against the origin's `behavioral_delta`.
5. **Verdict.** One of three, no hedging:
   - `reproduced` — the behavioral delta appeared as described.
   - `partially_reproduced` — the delta appeared with noted differences (recorded: what differed).
   - `not_reproduced` — the delta did not appear (recorded: what happened instead, and what differed from the origin context).

A contract may carry **more than one attempt** — a second run after a `not_reproduced`, a replication under different conditions. Attempts are appended, never overwritten; each has its own `attempt_id`. The contract's current verdict is the **latest** attempt's verdict. The history of "failed once, reproduced on retry with adapted method" is visible and valuable — it shows the lesson's boundary being mapped in real time.

Every attempt is recorded in **both** ledgers: the reproducing team's ledger (we attempted, here's the verdict) and the origin team's ledger (our lesson was tested by Team B, here's the verdict). Each entry references the `contract_id` and the other ledger's entry.

### 2.4 What counts as success

Success is **the behavioral delta reproduced, not words about the lesson.** "We read it and agree" is not a reproduction. "We ran the protocol and observed Z" is.

- `reproduced` requires the observed outcome to match the origin's stated `behavioral_delta` under a faithful (`followed`) or documented-adapted run.
- `partially_reproduced` counts as a *qualified success*: the lesson holds with modifications, and the modifications are now part of the record — they often become the next lesson.
- A verdict must never be upgraded by optimism. When in doubt between `partially_reproduced` and `not_reproduced`, the honest call is `not_reproduced` with a thorough `observed` note. The record can be amended by a second attempt; it cannot be un-embellished.

### 2.5 Failure — recorded honestly

A failed reproduction is **data, not shame**. The failure record must include:

- What was attempted (protocol steps, fidelity).
- What was observed instead of the expected delta.
- The honest best account of **what differed**: context, data, environment, timing, method fidelity — anything that might explain the gap.

Failures are the most valuable outcomes this contract produces: they map the boundary of where a lesson holds. A team that records failures honestly is doing the network a favor. A team that hides them is taxing everyone who comes after.

No penalty attaches to any verdict. The only punishable act under this contract is a dishonest record (see 2.7).

### 2.6 The compounding chain

Every reproduction cites its origin, forming a visible chain of who learned from whom:

- The contract carries `reproduces: <lesson_id>` and `prior_reproductions: [<contract_id>, …]` — every earlier contract that reproduced the same lesson.
- **Invariant:** `reproduces` must equal `lesson.lesson_id`. They are two names for the same lesson — one for the chain, one for the payload. If they disagree, the contract is malformed.
- The origin team's ledger accumulates the lesson's **reach**: `reproduced_by: [team names…]` with verdicts. This is a ledger-side derived view (computed from the contracts), not a stored field — the contracts are the source of truth; the reach view is reading them. Over time this becomes the lesson's provenance graph — anyone can see where the lesson traveled and where it held.
- A reproducing team that builds on the lesson to prove something new publishes a **new lesson** whose `method` cites the reproduction contract. Chains, not piles.

The network can then answer, for any lesson: *who proved it, who reproduced it, where did it hold, where did it break, and what grew out of it.* That is compounding.

### 2.7 Breach

The following are breaches of this contract, recorded in both ledgers with facts, evidence, and repair (see section 3):

- **Phantom reproduction:** a `reproduced` verdict recorded without running the protocol — words without behavior.
- **Unfalsifiable lesson:** the origin team published a lesson without a `reproduction_protocol` or without a stated `behavioral_delta`, then claimed it was "proven."
- **Falsified verdict:** the recorded verdict contradicts the recorded observations.
- **Silent attempt:** a reproduction was run but recorded in only one ledger, or in neither.
- **Suppressed failure:** a `not_reproduced` outcome was observed but recorded as `reproduced` or `partially_reproduced`, or not recorded at all.

Note what is *not* a breach: a `not_reproduced` verdict. Failure is data. Dishonesty about failure is the breach.

### 2.8 Fulfillment

The contract is **fulfilled** when:

1. The lesson was published in the full format of 2.2,
2. **At least one** reproduction attempt was run per the protocol of 2.3 with an honest verdict (the current verdict is the latest attempt's),
3. The attempt(s) and verdict(s) are recorded in **both** teams' ledgers, each entry referencing the `contract_id` and the other ledger's entry,
4. The compounding chain fields (`reproduces`, `prior_reproductions`) are filled.

### 2.9 Expiry

- A reproduction attempt should be completed by `attempt_by` (agreed at activation; when unset, derived as the `accepted` event's timestamp plus 30 days). If the window passes with no attempt recorded, the contract **expires** — recorded, no fault. The lesson remains available for a fresh contract.
- If the origin lesson passes its `valid_until`, in-flight contracts may complete their attempts (the attempt still tests *something*), but no new contracts reference the retired lesson.

---

## 3. Lifecycle states

| State | Meaning | How it is entered |
|---|---|---|
| `proposed` | Lesson published; reproducing team named; attempt window agreed. Not yet accepted. | Origin team publishes; reproducing team is invited. |
| `active` | Reproducing team accepted. The Compounder is now on the hook to attempt within the window. | Both teams record acceptance. |
| `fulfilled` | At least one attempt run, honest verdict recorded in both ledgers per 2.8. | Both ledger entries exist and cross-reference. |
| `breached` | A term in 2.7 was violated. Recorded in both ledgers with facts and repair. | Breach declared by either team, with evidence. |
| `expired` | Attempt window passed with no attempt, or the lesson retired before acceptance. | Declared with reason; no fault attached. |

A contract never moves backward. A `not_reproduced` verdict fulfills the contract — fulfillment is about the honest attempt, not the happy outcome.

### Breach handling — recorded honestly, in both ledgers

A breached contract is a **signal, not a punishment**. The breach record contains:

- `what_was_promised` — the term that was broken, quoted from the agreement.
- `what_happened` — the facts, with evidence links. No adjectives, no blame language.
- `systemic_cause` — the honest best guess at *why*: unclear protocol? Capacity missing? Incentive to look good? "We don't know yet" is acceptable; pretending to know is not.
- `repair` — what changes so this class of breach doesn't repeat. Feeds the team's learning loop.

Both teams record the breach. Disputes are recorded **alongside** the breach — both claims visible, no silent edits. And one rule specific to this contract: **a breach here never retroactively taints honest verdicts.** A team that recorded three true `not_reproduced` verdicts and one phantom `reproduced` keeps the three; only the phantom is struck, and the striking is itself recorded.

---

## 4. JSON schema — `naya.learning-contract.v1`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://nayanet.technology/schemas/naya.learning-contract.v1",
  "title": "naya.learning-contract.v1",
  "description": "Agreement between a lesson's origin team and a reproducing team: the reproducer attempts the lesson's protocol, and both ledgers record the honest verdict.",
  "type": "object",
  "required": [
    "schema_version", "contract_id", "contract_type", "state",
    "origin_team", "reproducing_team", "lesson", "events"
  ],
  "properties": {
    "schema_version": { "const": "naya.learning-contract.v1" },
    "contract_id": {
      "type": "string",
      "pattern": "^LC-[0-9]{8}-[0-9]{3}$",
      "description": "e.g. LC-20261011-001"
    },
    "contract_type": { "const": "learning" },
    "state": {
      "type": "string",
      "enum": ["proposed", "active", "fulfilled", "breached", "expired"]
    },
    "origin_team": { "$ref": "#/$defs/party" },
    "reproducing_team": { "$ref": "#/$defs/party" },
    "attempt_by": {
      "type": "string",
      "format": "date-time",
      "description": "Deadline for the first reproduction attempt. When unset, derived as the accepted event's timestamp plus 30 days."
    },
    "reproduces": {
      "type": "string",
      "pattern": "^LESSON-[0-9]{8}-[0-9]{3}$",
      "description": "The lesson this contract reproduces."
    },
    "prior_reproductions": {
      "type": "array",
      "description": "Earlier learning-contract ids that reproduced the same lesson. The compounding chain.",
      "items": { "type": "string", "pattern": "^LC-[0-9]{8}-[0-9]{3}$" }
    },
    "lesson": { "$ref": "#/$defs/lesson" },
    "attempts": {
      "type": "array",
      "description": "Reproduction attempts, appended never overwritten. The contract's current verdict is the latest attempt's verdict.",
      "items": { "$ref": "#/$defs/attempt" }
    },
    "breach": { "$ref": "#/$defs/breach" },
    "ledger_refs": {
      "type": "object",
      "description": "Where each team recorded this contract in its own Smart Ledger.",
      "required": ["origin_team", "reproducing_team"],
      "properties": {
        "origin_team": { "$ref": "#/$defs/ledger_ref" },
        "reproducing_team": { "$ref": "#/$defs/ledger_ref" }
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
        "agent_name": {
          "type": "string",
          "description": "Named agent, e.g. Compounder. Reproducer is normally the LEARN seat."
        },
        "agent_area": { "type": "string", "description": "The agent's area, e.g. LEARN." }
      },
      "additionalProperties": false
    },
    "lesson": {
      "type": "object",
      "required": [
        "lesson_id", "title", "claim", "method", "behavioral_delta",
        "evidence_links", "reproduction_protocol", "published_at"
      ],
      "properties": {
        "lesson_id": {
          "type": "string",
          "pattern": "^LESSON-[0-9]{8}-[0-9]{3}$"
        },
        "title": { "type": "string", "minLength": 1 },
        "claim": {
          "type": "string",
          "minLength": 1,
          "description": "One sentence: what was learned."
        },
        "method": {
          "type": "string",
          "minLength": 1,
          "description": "How it was proven: what was done, measured, and controlled."
        },
        "behavioral_delta": {
          "type": "string",
          "minLength": 1,
          "description": "The observable change a reproducer should see. Not a belief — an observation."
        },
        "evidence_links": {
          "type": "array",
          "minItems": 1,
          "items": { "type": "string", "minLength": 1 }
        },
        "reproduction_protocol": {
          "type": "array",
          "minItems": 1,
          "items": { "type": "string", "minLength": 1 },
          "description": "Ordered steps a stranger could follow: setup, action, observation, success criteria."
        },
        "published_at": { "type": "string", "format": "date-time" },
        "valid_until": {
          "type": "string",
          "format": "date-time",
          "description": "Optional. When set and passed, the lesson is retired — not wrong, retired."
        }
      },
      "additionalProperties": false
    },
    "attempt": {
      "type": "object",
      "required": [
        "attempt_id", "reproducing_agent", "method_fidelity",
        "reproduction_context", "observed", "verdict", "attempted_at"
      ],
      "properties": {
        "attempt_id": { "type": "string", "minLength": 1 },
        "reproducing_agent": { "type": "string" },
        "method_fidelity": {
          "type": "string",
          "enum": ["followed", "adapted"],
          "description": "followed = protocol run as written; adapted = steps changed, documented in fidelity_notes."
        },
        "fidelity_notes": {
          "type": "string",
          "description": "Required when method_fidelity is adapted: exactly what changed and why."
        },
        "reproduction_context": {
          "type": "string",
          "minLength": 1,
          "description": "The reproducer's own turf: repo state, data, environment, timing."
        },
        "observed": {
          "type": "string",
          "minLength": 1,
          "description": "What actually happened, concretely. Compared against the lesson's behavioral_delta."
        },
        "verdict": {
          "type": "string",
          "enum": ["reproduced", "partially_reproduced", "not_reproduced"],
          "description": "No hedging. When torn between partial and not_reproduced, choose not_reproduced."
        },
        "verdict_notes": {
          "type": "string",
          "description": "Required for partially_reproduced and not_reproduced: what differed, what happened instead."
        },
        "attempted_at": { "type": "string", "format": "date-time" }
      },
      "additionalProperties": false,
      "allOf": [
        {
          "if": { "properties": { "method_fidelity": { "const": "adapted" } } },
          "then": { "required": ["fidelity_notes"] }
        },
        {
          "if": { "properties": { "verdict": { "enum": ["partially_reproduced", "not_reproduced"] } } },
          "then": { "required": ["verdict_notes"] }
        }
      ]
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
            "lesson_published", "attempt_recorded"
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

Naya 2's **Compounder** (ledger `#2398`) proves a lesson: serializing heavy test batteries (instead of running them concurrently) stops silent `/tmp` exhaustion from corrupting pytest verdicts. The `behavioral_delta`: *"Running the adversarial harness and the pytest battery serially, each with its own workspace-disk scratch dir, produces zero Errno-28 failures across 5 consecutive runs, where concurrent runs produced at least one."* Protocol published with exact steps.

Contract `LC-20261011-001` is **proposed**; Naya 5's team (ledger `#2396`) accepts → **active**. Their Compounder runs the protocol on their own battery lane: `method_fidelity: followed`. Observed: 5/5 clean serial runs; one concurrent control run still failed with Errno 28. Verdict: **reproduced**.

Both ledgers record it. Naya 2's ledger shows the lesson's reach growing: `reproduced_by: [Naya 5's team — reproduced]`. A month later, a third team's reproduction cites `prior_reproductions: [LC-20261011-001]` — the chain is visible, and the lesson is no longer one team's claim. It is network knowledge.

If the verdict had been `not_reproduced` — say their tmpfs was larger and concurrency never failed — that would be recorded just as proudly, with the differing context. The map of where the lesson holds would have its first boundary. Still fulfilled. Still compounding.

---

*Spec authored 2026-10-11. Companion contracts: `verification-contract.md`, `handoff-contract.md`.*

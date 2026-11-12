# Verification Contract — `naya.verification-contract.v1`

**Status:** SPEC (prose + schema). Enforcement comes later — this document is the agreement, not the code.

## 1. Purpose, in plain words

When one team builds something and another team checks it, nobody should have to take anyone's word for it. This contract is the agreement between a **building team** (the team whose PR is being checked) and a **verifying team** (a different team doing the checking). It says who may check, what a check looks like, and where the score goes.

The rule underneath it: **the recorded action is the verified action.** If the verification isn't in both ledgers, it didn't happen. If it's in both ledgers, anyone can check it.

This contract is not blockchain. It is a machine-readable promise between teams: *"Your Auditor will independently verify my Builder's PR, and both our ledgers will record the score."*

---

## 2. The agreement, in precise terms

### 2.1 The two parties

- **Building team** — owns the pull request being verified. Names the PR, the repo, and the exact head SHA under verification. Its agent is normally the **Builder**.
- **Verifying team** — performs the independent verification. Its agent is normally the **Auditor** (the PROVE seat), but a team may designate another agent as acting verifier — recorded explicitly in the contract.

Each party is identified by: team name, its Smart Ledger issue number (e.g. Naya 2's team → issue `#2398`, Naya 5's team → issue `#2396`), the acting agent's name, and that agent's area.

### 2.2 Who can request, who can offer

- The **building team may request** verification of its own PR from any eligible verifying team. A team may never request verification of its own PR *from itself*.
- A **verifying team may offer** verification unprompted (for example, an Auditor running a sweep). An offer is recorded the same as a request, with `initiated_by: "offer"`.
- The request names the exact target: repo, PR number, and **head SHA**. Verification is bound to that SHA and nothing else (see 2.6).

### 2.3 Verifier eligibility — the independence rule

A verifier is eligible **only if all three hold**:

1. **Different team.** The verifier's team is not the building team.
2. **Different agent.** The verifier agent is not the agent who built the PR — even if that agent has since moved teams. You cannot verify your own build, ever.
3. **Signed independence declaration.** The verifier records, in their own words: *"I did not build this. I have no stake in its score."* The declaration is part of the contract record.

Scorer ≠ builder is not a suggestion. It is the mechanism that makes the score mean something.

### 2.4 The score format

Every verification produces a **score record**:

- `score` — a number from 0 to 10, one decimal place (e.g. `8.5`).
- `why_not_10` — a list of the specific reasons the score is not 10. **Mandatory whenever the score is below 10.** "Looks fine" is not a reason. Each entry names something concrete: what was checked, what fell short, what would close the gap.
- `method` — what the verifier actually did: which files were read, which tests were run, what bytes were compared. A score without a method is a rumor.
- `evidence` — links to the proof: the verified SHA, test run references, byte-comparison receipts.
- `verified_sha` — the exact 40-hex head SHA that was verified.
- `verified_at` — timestamp (UTC, ISO-8601).
- `independence_declaration` — the signed declaration from 2.3.

A score of 10 with an empty `why_not_10` list is valid — and rare, and worth celebrating in the ledger.

### 2.5 Disagreement — when verifications differ

More than one team may verify the same PR head. When the verifications of one SHA exist and **max(score) − min(score) > 1.0** across all of them:

1. **All scores are recorded.** None is overwritten. The ledger keeps every score, attributed to its verifier.
2. **The `why_not_10` lists are merged** — deduplicated, preserving attribution — into a `combined_findings` list on each contract.
3. **The gating score is the lowest one.** Merges are gated conservatively: the PR proceeds only when the *lowest* recorded score clears the bar.
4. The merged findings list becomes the work list for the building team's next Builder-Scorer round.

The bar a merge must clear is the **merge bar**: 9.0 by default — Shawn's standing bar, nothing below 9.0 ships. The two teams may agree a different bar for a specific contract (some checks are advisory, not merge-gating); when they do, the agreed `merge_bar` is recorded in the contract at activation. No agreed bar, no silent default other than 9.0 — the default is the default.

Disagreement is not a failure of the contract. It is the contract working: two independent eyes saw different things, and now both things are on the record.

### 2.6 Expiry — verification is bound to the SHA

A verification verifies **one head SHA**. The moment the PR head moves (new commits pushed, rebase, re-cut):

- The contract's state moves to **`expired`** automatically, with an event recording the old SHA and the new SHA.
- The old verification **must not** be presented as current. Presenting an expired verification as if it covered the new head is a breach (see 2.8).
- Re-verification is a **new contract**, linked to the old one via `reverify_of`, so the chain of "verified → changed → re-verified" stays visible.

This is the evidence-freshness rule made mechanical: the world moved, so the proof moved with it.

### 2.7 Fulfillment

The contract is **fulfilled** when:

1. The verification was performed by an eligible verifier (2.3),
2. The score record is complete (2.4),
3. The verification is recorded in **both** teams' ledgers — the building team's ledger and the verifying team's ledger — each entry referencing the `contract_id` and the other ledger's entry.

One ledger is a claim. Two ledgers, pointing at each other, is a receipt.

### 2.8 Breach

The following are breaches of this contract. Each is recorded in both ledgers with the facts, the evidence, and the repair (see section 3, *Breach handling*).

- **Self-verification:** the verifying team is the building team, or the verifier agent built the PR.
- **Scoreless verification:** a score recorded without the `why_not_10` list when the score is below 10, or without a method.
- **Stale verification:** an expired verification (head moved) presented as current.
- **False declaration:** the independence declaration was signed by someone who built the work or had a stake in its score.
- **Silent score:** a verification performed but recorded in only one ledger, or in neither.

### 2.9 How this contract lives in the ledgers

The contract record itself is a ledger entry — append-only, never edited in place. State changes are **events appended** to the contract's `events` array, each with a timestamp, the acting team and agent, and the ledger reference where that team recorded it. The building team's entry and the verifying team's entry reference each other by `contract_id`. Anyone reading either ledger can walk to the other side.

---

## 3. Lifecycle states

| State | Meaning | How it is entered |
|---|---|---|
| `proposed` | The contract is drafted: parties, target PR + SHA, verifier named. Not yet agreed. | A request or offer is recorded. |
| `active` | Both teams accepted. The verifier is now on the hook to verify the named SHA. | Both teams record acceptance. |
| `fulfilled` | Verification complete, score recorded in both ledgers per 2.7. | Both ledger entries exist and cross-reference. |
| `breached` | A term in 2.8 was violated. Recorded in both ledgers with facts and repair. | Breach declared by either team, with evidence. |
| `expired` | The PR head moved before verification completed, or the `verify_by` window passed with no verification recorded. | Automatic on head move (`head_moved` event); declared with reason on window expiry. |

A contract never moves backward. `expired` → new contract via `reverify_of`. `breached` → the breach record stands permanently; a fresh contract may supersede it, citing the breach.

### Breach handling — recorded honestly, in both ledgers

A breached contract is a **signal, not a punishment**. The breach record contains:

- `what_was_promised` — the term that was broken, quoted from the agreement.
- `what_happened` — the facts, with evidence links. No adjectives, no blame language — just what occurred.
- `systemic_cause` — the honest best guess at *why*: was the agreement unclear? Was capacity missing? Did the world change mid-contract? "We don't know yet" is an acceptable cause; pretending to know is not.
- `repair` — what changes so this class of breach doesn't repeat. The repair becomes input to the team's learning loop.

Both teams record the breach in their ledgers. If the other team disputes the breach, the dispute is recorded **alongside** the breach — both claims visible, no silent edits. The record shows the disagreement; the disagreement does not erase the record.

---

## 4. JSON schema — `naya.verification-contract.v1`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://nayanet.technology/schemas/naya.verification-contract.v1",
  "title": "naya.verification-contract.v1",
  "description": "Agreement between a building team and an independent verifying team: the verifier scores the builder's PR head SHA, and both ledgers record the score.",
  "type": "object",
  "required": [
    "schema_version", "contract_id", "contract_type", "state",
    "building_team", "verifying_team", "target", "events"
  ],
  "properties": {
    "schema_version": { "const": "naya.verification-contract.v1" },
    "contract_id": {
      "type": "string",
      "pattern": "^VC-[0-9]{8}-[0-9]{3}$",
      "description": "e.g. VC-20261011-001"
    },
    "contract_type": { "const": "verification" },
    "state": {
      "type": "string",
      "enum": ["proposed", "active", "fulfilled", "breached", "expired"]
    },
    "reverify_of": {
      "type": "string",
      "pattern": "^VC-[0-9]{8}-[0-9]{3}$",
      "description": "Prior contract id, when this contract re-verifies a moved head."
    },
    "building_team": { "$ref": "#/$defs/party" },
    "verifying_team": { "$ref": "#/$defs/party" },
    "initiated_by": {
      "type": "string",
      "enum": ["request", "offer"],
      "description": "request = building team asked; offer = verifying team offered."
    },
    "merge_bar": {
      "type": "number",
      "minimum": 0,
      "maximum": 10,
      "default": 9.0,
      "description": "The score a merge must clear. Defaults to 9.0 (Shawn's standing bar). Parties may agree a different bar at activation; the agreed value is recorded here."
    },
    "verify_by": {
      "type": "string",
      "format": "date-time",
      "description": "Optional. If the verifier hasn't recorded a verification by this time, the contract expires."
    },
    "target": {
      "type": "object",
      "required": ["repo", "pr_number", "head_sha"],
      "properties": {
        "repo": { "type": "string", "description": "e.g. SoulSchoolAcademy/NayaPOWER" },
        "pr_number": { "type": "integer", "minimum": 1 },
        "head_sha": {
          "type": "string",
          "pattern": "^[0-9a-f]{40}$",
          "description": "The exact PR head SHA under verification. Verification binds to this SHA only."
        }
      },
      "additionalProperties": false
    },
    "verifications": {
      "type": "array",
      "description": "One or more independent verifications of the target SHA.",
      "items": { "$ref": "#/$defs/verification" }
    },
    "disagreement": {
      "type": "object",
      "description": "Present when max(score) - min(score) > 1.0 across the verifications of one SHA.",
      "required": ["scores", "combined_findings", "gating_score"],
      "properties": {
        "scores": {
          "type": "array",
          "minItems": 2,
          "items": { "type": "number", "minimum": 0, "maximum": 10 }
        },
        "combined_findings": {
          "type": "array",
          "items": { "$ref": "#/$defs/finding" },
          "description": "Deduplicated merge of every why_not_10 list, attribution preserved."
        },
        "gating_score": {
          "type": "number",
          "minimum": 0,
          "maximum": 10,
          "description": "The conservative score that gates the merge: the minimum of all recorded scores. The merge proceeds only if gating_score >= merge_bar."
        }
      },
      "additionalProperties": false
    },
    "breach": { "$ref": "#/$defs/breach" },
    "ledger_refs": {
      "type": "object",
      "description": "Where each team recorded this contract in its own Smart Ledger.",
      "required": ["building_team", "verifying_team"],
      "properties": {
        "building_team": { "$ref": "#/$defs/ledger_ref" },
        "verifying_team": { "$ref": "#/$defs/ledger_ref" }
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
          "description": "Named agent, e.g. Auditor. Must differ from the builder agent."
        },
        "agent_area": {
          "type": "string",
          "description": "The agent's area, e.g. PROVE. Verifier is normally the PROVE seat."
        }
      },
      "additionalProperties": false
    },
    "verification": {
      "type": "object",
      "required": [
        "verifier_agent", "score", "why_not_10", "method",
        "evidence", "verified_sha", "verified_at", "independence_declaration"
      ],
      "properties": {
        "verifier_agent": { "type": "string" },
        "score": { "type": "number", "minimum": 0, "maximum": 10 },
        "why_not_10": {
          "type": "array",
          "items": { "type": "string", "minLength": 1 },
          "description": "Mandatory non-empty when score < 10."
        },
        "method": {
          "type": "string",
          "minLength": 1,
          "description": "What the verifier actually did: files read, tests run, bytes compared."
        },
        "evidence": {
          "type": "array",
          "minItems": 1,
          "items": {
            "type": "object",
            "required": ["kind", "ref"],
            "properties": {
              "kind": { "type": "string", "description": "e.g. test-run, byte-compare, file-read" },
              "ref": { "type": "string", "description": "Link or identifier to the evidence." }
            },
            "additionalProperties": false
          }
        },
        "verified_sha": { "type": "string", "pattern": "^[0-9a-f]{40}$" },
        "verified_at": { "type": "string", "format": "date-time" },
        "independence_declaration": {
          "type": "string",
          "minLength": 1,
          "description": "The verifier's signed statement of independence."
        }
      },
      "additionalProperties": false,
      "allOf": [
        {
          "if": { "properties": { "score": { "exclusiveMaximum": 10 } } },
          "then": { "properties": { "why_not_10": { "minItems": 1 } } }
        }
      ]
    },
    "finding": {
      "type": "object",
      "required": ["text", "raised_by"],
      "properties": {
        "text": { "type": "string", "minLength": 1 },
        "raised_by": { "type": "string", "description": "Name of the verifier agent whose why_not_10 list this finding came from." }
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
            "verification_recorded", "disagreement_recorded", "head_moved"
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

Naya 2's team (ledger `#2398`) built PR `#2401`, head `9f2c…a41d`. The Builder was **Builder** (BUILD). The team requests verification from Naya 5's team (ledger `#2396`), whose **Auditor**-equivalent verifies.

1. Contract `VC-20261011-001` is **proposed**: parties, target (`SoulSchoolAcademy/NayaPOWER`, PR 2401, head SHA), initiated by request.
2. Both teams record acceptance → **active**.
3. Naya 5's verifier reads the diff at the SHA, runs the test battery, compares the claimed bytes. Score: **8.5**. `why_not_10`: ["Error path for malformed ledger entries untested", "No evidence link for the migration claim in the PR body"]. Method and evidence recorded. Independence declaration signed → event `verification_recorded` → **fulfilled** (both ledgers carry the score).
4. Note what fulfilled does *not* mean: 8.5 is below the 9.0 merge bar, so the PR does not merge on this verification. The contract did its job — the check happened, the score is on record. The merged findings list becomes the Builder's work list for the next Builder-Scorer round.
5. Naya 2's Builder pushes a fix. Head moves → contract **expires** (`head_moved` event). New contract `VC-20261011-002` with `reverify_of: VC-20261011-001` verifies the new head.

The score lived in two ledgers. The head moved, the proof moved with it. Nothing was taken on trust.

---

*Spec authored 2026-10-11. Companion contracts: `learning-contract.md`, `handoff-contract.md`.*

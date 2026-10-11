# INTEGRATION: kernel/protocol × the Existing Activation Chain
## No competing constitution. One boot path.

**Principle (Naya 3):** The repository already has a constitutional system —
`AGENTS.md` (boot contract), `NAYA-ACTIVATION/` (activation chain), the ratified
Decision Value Calculus, the machine operating loop. `kernel/protocol/` does not
replace any of it. It plugs in as enforceable checks at the exact seams where
prose currently relies on memory.

## Where each gate plugs in

| Existing seam | Protocol gate | What it adds |
|---|---|---|
| `AGENTS.md` → "STOP — BOOT BEFORE WORK" | `cold_start_gate` + `read_receipt` | Required seven-file reading set (PROTOCOL, AGENTS, Constitution, ratified Team Naya Operating Protocol, Laws Index, Portable Activation Protocol, Smart Note Operating Contract); comprehension answers and exact current SHA-256 source binding. No complete/current receipt → no boot. |
| `AGENTS.md` → "ACTIVATION ACCEPTANCE" (10 checks) | `cold_start_gate` + `cold_successor_test` | Machine-checkable versions of checks 1–10. The handoff test enforces check 10 ("exactly one next executable action"). |
| `AGENTS.md` → "DECISION EFFICIENCY" (calculus) | `authority_gate` | Runs BEFORE the calculus scores. Hard gates filter the option set; the calculus only scores admissible options. A score never grants permission. |
| `AGENTS.md` → "ENGINEERING" (smallest effective change) | `minimal_action` | The "smallest effective change" rule as a checkable proposal: what changes, what is preserved, why nothing smaller works. |
| `AGENTS.md` → "OPERATIONS" (sign-in/sign-out relay) | `cold_successor_test` | The handoff section of sign-out as an acceptance test: what happened, truth, authority, proof, open, blocked, next. |
| `AGENTS.md` → "CONTINUOUS DISTILLATION" | `learning_capture` | Every cycle declares its lesson (with provenance) or states why there is none. Silence is not a lesson. |
| `AGENTS.md` → "CAPTAIN MODE" (takeover) | `takeover` | The no-waiting doctrine as rules: 4h stall required, authority-checked, recorded, owner notified with next task. |
| Delivery to Shawn | `quality_gate` | 9.0 floor enforced: scorecard required, every dimension ≥ 9.0, verifier ≠ builder, weakest point named. |

## What was NOT duplicated

- The Decision Value Calculus (`kernel/value_calculus.py`) — the protocol gates feed it, never replace it.
- The activation documents — the gates reference them, never rewrite them.
- The Smart Note pipeline — `learning_capture` requires a lesson with provenance; the pipeline itself is untouched.
- Authority definitions — `authority_gate` encodes the five protected gates from the ratified governance docs; it creates no new authority.

## Current routing and receipt boundary

The current cross-team coordination board is #2175, the director-maintained mission-state issue is #2154, and the specialty-feed index is #1599. #1354 is historical/comment-locked and must never be required for a fresh activation. Specialty sign-in/out belongs on the lane feed; cross-team summaries link back to #2175.

The read receipt's unkeyed SHA-256 is an integrity binding only, not authenticated agent identity. Key custody is an explicit Director-authority boundary. The gate must not claim the receipt is a cryptographic signature or fabricate key material.

## The wisdom law

"Wish not to be the smartest but the wisest" (SN-0638, CANDIDATE) sits above the
machinery as the orienting virtue: the gates exist so intelligence compounds
without breaking trust. Smartest optimizes for being right; wisest optimizes for
being right for everybody.

## Verification

`tests/test_protocol_machine_law.py` — gates tested with positive and negative
controls. The gates are proven to block what they claim to block and allow what
they claim to allow.

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
| `AGENTS.md` → "STOP — BOOT BEFORE WORK" | `read_receipt` + `cold_start_gate` | Require the ratified protocol, Constitution, Operating Law/Code, team protocol, activation contracts, current source-precedence document, and mission snapshot as revision-bound source receipts; all comprehension answers pass before governed work. |
| `AGENTS.md` → "ACTIVATION ACCEPTANCE" (10 checks) | `cold_start_gate` + `cold_successor_test` | Machine-checkable versions of checks 1–10. The handoff test enforces check 10 ("exactly one next executable action"). |
| `AGENTS.md` → "DECISION EFFICIENCY" (calculus) | `authority_gate` | Runs BEFORE the calculus scores. Hard gates filter the option set; the calculus only scores admissible options. A score never grants permission. |
| `AGENTS.md` → "ENGINEERING" (smallest effective change) | `minimal_action` | The "smallest effective change" rule as a checkable proposal: what changes, what is preserved, why nothing smaller works. |
| `AGENTS.md` → "OPERATIONS" (sign-in/sign-out relay) | `work_cycle_receipt` + `cold_successor_test` | Validate a pre-work sign-in against a live feed/comment reference; validate end-of-cycle sign-out against the same feed and exact sign-in receipt; keep the GitHub feed as canonical record. |
| `AGENTS.md` → "CONTINUOUS DISTILLATION" | `learning_capture` | Every cycle declares its lesson (with provenance) or states why there is none. Silence is not a lesson. |
| `AGENTS.md` → "CAPTAIN MODE" (takeover) | `takeover` | The no-waiting doctrine as rules: 4h stall required, authority-checked, recorded, owner notified with next task. |
| Delivery to Shawn | `quality_gate` | 9.0 floor enforced: scorecard required, every dimension ≥ 9.0, verifier ≠ builder, weakest point named. |

## What was NOT duplicated

- The Decision Value Calculus (`kernel/value_calculus.py`) — the protocol gates feed it, never replace it.
- The activation documents — the gates reference them, never rewrite them.
- The Smart Note pipeline — `learning_capture` requires a lesson with provenance; the pipeline itself is untouched.
- Authority definitions — `authority_gate` encodes the five protected gates from the ratified governance docs; it creates no new authority.

## The wisdom law

"Wish not to be the smartest but the wisest" (SN-0638, CANDIDATE) sits above the
machinery as the orienting virtue: the gates exist so intelligence compounds
without breaking trust. Smartest optimizes for being right; wisest optimizes for
being right for everybody.

## Verification

`tests/test_protocol_machine_law.py` — gates tested with positive and negative
controls. The gates are proven to block what they claim to block and allow what
they claim to allow.


## 2026-10-11 protocol boot packet and feed receipt update

- `read_receipt.py` is version-pinned to NAYA-PROTOCOL-V1 and rejects missing required sources, missing dated source-precedence evidence, failed comprehension questions, and a malformed main SHA. Its digest detects changes to the receipt payload; it is **not** cryptographic issuer authentication and does not independently prove that a model read or understood the files.
- `cold_start_gate.py` now requires mission issue #2154, current coordination #2175, live main, and a matching sign-in receipt. #1354 is archival only.
- `work_cycle_receipt.py` validates sign-in/sign-out fields, feed identity, comment URL, content hash, matching agent/feed and main revision. The adapter must first fetch the referenced GitHub comment and truthfully set the observed-source flag; the validator itself makes no network call and does not post comments.
- A full acceptance claim still requires CI on the exact PR head, negative-control tests, a cross-seat reviewer, and evidence that the live-feed adapter invokes these validators on actual workflow entry/exit. The presence of validator code alone does not prove all orchestration paths call it.

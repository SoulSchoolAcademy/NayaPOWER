# 🔱 NAYA POWER — CONTINUOUS ACTIVITY PROTOCOL

**DATE:** 2026-09-18
**STATUS:** CANONICAL TEAM-NAYA OPERATING PROTOCOL
**SCOPE:** Every substantive Naya session that inspects, changes, verifies, or coordinates work in NayaPOWER / NayaNET.

## PURPOSE

Make Naya-to-Naya work continuously visible, searchable, timestamped, recoverable, and useful to a cold Naya without creating a second source of truth.

## REQUIRED SESSION LOOP

**SIGN IN → ORIENT → WORK → REPORT → VERIFY → SIGN OUT → HAND OFF**

A substantive session must leave a durable dated record even when the result is failure, a blocker, or a decision not to change code.

## HUMAN-FACING CALENDAR

The directory date is the user's product calendar date in **America/Vancouver**. This prevents a Vancouver evening session from appearing under tomorrow merely because its UTC timestamp crossed midnight.

Path:

`NAYA-TEAM/YYYY/MM/DD/`

Filename:

`YYYY-MM-DDTHH-MM-SS-0700__TOPIC.md` during PDT, or the applicable local offset when Vancouver changes offset.

The record itself must also contain an ISO timestamp and timezone. Machine/event timestamps may remain canonical UTC elsewhere in the system.

Navigation:

**YEAR → MONTH → DAY → TIMESTAMP**

## REQUIRED CONTENT

Every substantive session record answers:

1. **Who / session:** which Naya or execution context is acting.
2. **Where:** repository/project/sub-project and current branch/ref.
3. **Why:** mission and current next action.
4. **What happened:** meaningful work performed.
5. **Questions:** questions the next Naya should answer.
6. **Blockers / failures:** what did not work and why, if known.
7. **Successes:** what actually passed.
8. **Verification:** what is OBSERVED, VERIFIED, NOT_PROVEN, or UNKNOWN.
9. **Evidence:** direct Smart Links to source, tests, workflows, PRs, receipts, or runtime observations.
10. **Next action:** exactly one successor action unless a higher-level contract explicitly requires a bounded sequence.
11. **SIGN OUT:** explicit handoff statement for the next Naya.

## WHAT COUNTS AS ACTIVITY

Record meaningful repository interaction, including:

- entering a substantive Naya session;
- inspecting source-of-truth files or runtime state;
- making a decision or discovering a defect;
- changing code, contracts, migrations, tests, workflows, or documentation;
- running or observing verification;
- creating or reviewing a PR/commit/workflow;
- identifying a blocker or unresolved question;
- handing work to another Naya.

Do **not** create fake activity just to increase activity volume. Activity describes real work.

## FEED SEPARATION

- **Team Naya Activity:** human-readable Naya-to-Naya communication and continuity.
- **Main Superbrain Activity:** canonical operational event projection.
- **Project/Sub-project Activity:** scoped projections of Main Activity.

These are multiple views over one truth, not competing event stores.

## COLD-NAYA RULE

A Naya arriving with no conversational context must be able to enter today's directory, identify the latest session, read what happened, inspect direct evidence, understand what remains unresolved, and continue from the stated successor action.

## NON-NEGOTIABLE TRUTH RULE

Never write VERIFIED merely because documentation says something is verified. Label claims according to fresh evidence. Never invent receipts, events, credentials, identities, or successful outcomes.

## CONTINUOUS PRACTICE

This protocol is a behavioral requirement for Naya sessions. GitHub itself cannot infer that a model has "entered" a session unless an integration explicitly emits that event. Therefore each connected Naya runtime must perform the sign-in record as part of its own operating loop; repository history alone is not treated as a substitute.

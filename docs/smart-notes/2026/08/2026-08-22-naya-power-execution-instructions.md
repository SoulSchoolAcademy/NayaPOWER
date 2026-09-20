# NAYA POWER — EXECUTION INSTRUCTION PROTOCOL

- **Date:** 2026-08-22
- **Primary category:** DECISION / LEARNING / PROCESS
- **Status:** ACTIVE
- **Scope:** NAYA POWER / GitHub Actions / MAXESS V3 execution and verification

## Human-facing execution rule

When Naya is executing a repository repair or verification task, do **not** merely report a status such as “I am blocked,” “the run failed,” or “I need the logs.”

The next response must explicitly tell Shawn what happens next:

1. **WHAT NAYA WILL DO NEXT** — the exact technical action/tool operation being attempted.
2. **WHAT SHAWN NEEDS TO DO, IF ANYTHING** — preferably nothing if Naya has the required access.
3. **IF HUMAN ACTION IS REQUIRED** — give the exact GitHub page/button/menu to click and what information to return.
4. **IF NO HUMAN ACTION IS REQUIRED** — say clearly: **“You do not need to click anything. I am doing X next.”**
5. Never make Shawn infer the next step from a technical status update.

## GitHub Actions failure workflow

For a failing GitHub Actions run:

- Start from the **new run explicitly under investigation**.
- Extract run number, run ID, HEAD SHA, event, status, and conclusion.
- Verify whether HEAD matches current `main`.
- Confirm it is not an excluded historical run.
- Inspect the failed job and its **complete failing log**.
- Identify the **first divergence**, not merely the final error message.
- If GitHub exposes an AI-generated “solution” or suggested fix for the error, inspect and use it as evidence, but do not blindly trust it. Compare it against the actual executed commit/workflow and failure log.
- Repair only the demonstrated root cause.
- Create a genuinely fresh execution when required.
- Never return to an old run merely because it is easier to inspect.

## Important execution lesson from V3

The V3 workflow had a Python syntax failure in the Results assembler. A proposed regex repair was supplied during the investigation. However, the fact that a repair appears in a later commit does **not** prove that the failing run executed that repair or that the repair solved the first divergence.

Therefore Naya must always distinguish:

- **PROPOSED FIX** — supplied by a human or GitHub AI suggestion;
- **COMMITTED FIX** — actually present in a Git commit;
- **EXECUTED FIX** — proven to be in the workflow commit used by the run;
- **VERIFIED FIX** — proven by a fresh successful execution;
- **LIVE VERIFIED** — proven in the actual user journey.

## Required final state

Do not end with a generic status update.

End only with one of:

**A. EXACT HUMAN ACTION REQUIRED** — including where to click and what to provide; or

**B. EXACT TECHNICAL ACTION BEING EXECUTED NEXT** — including what Naya is inspecting, changing, running, or verifying.

## User-journey completion requirement

For MAXESS V3, continue beyond workflow success. The final verification chain is:

**447 → Q15 → MAXESS_RESULT_V1 → Results → runtime verification → live verification → real user journey proven.**

A green GitHub Actions run alone is not the final success criterion.

# 🔱 NAYA INTELLIGENCE REPORT — CANONICAL OPERATING ARTIFACT

**Status:** CANONICAL  
**Effective:** 2026-08-27  
**Purpose:** Give Shawn and every incoming Naya one trustworthy current-state view of the Superbrain and its projects.

## PRINCIPLE

The Daily Intelligence Report is not a diary and not a transcript summary.

It is a point-in-time operating artifact that compresses verified reality into a form that lets a human and the next Naya understand where the system stands and what should happen next.

## REPORT CONTRACT

Every report should answer, in order:

### 1. WHERE ARE WE?
- repository
- branch
- observed HEAD
- working-tree/deployment state where available
- current runtime verification state
- report timestamp and timezone

### 2. WHAT ARE WE BUILDING?
- active project(s)
- mission
- North Star
- current execution block

### 3. WHAT HAS BEEN VERIFIED?
- tests actually run
- runtime observations
- CI/workflow evidence
- artifact/commit references
- verification receipts

### 4. WHAT IS BROKEN?
- RED/AMBER gates
- regressions
- incomplete work
- stale/conflicted state
- blockers

### 5. WHAT IS PROTECTED?
- governing laws
- source-of-truth decisions
- approved baselines
- working architecture
- UX/product decisions
- privacy and human-control boundaries

### 6. WHAT DID WE LEARN?
Capture only durable, reusable, corrective, consequential, or strategically valuable learning.

### 7. WHAT DECISIONS WERE MADE?
Record decisions that prevent future Nayas from reopening settled questions.

### 8. WHAT MUST HAPPEN NEXT?
Return exactly one highest-value Next Best Action for the current report. Additional queued work belongs in the project/continuity state, not in a competing list of contradictory next actions.

### 9. WHAT DOES THE NEXT NAYA NEED TO KNOW?
Provide a compact successor packet:

**MISSION → SOURCE OF TRUTH → STATE → PROTECTED BASELINE → WORK COMPLETED → EVIDENCE → FAILURES/TRAPS → LESSONS → UNKNOWNS → RISKS → RECOMMENDATION → READY-TO-RUN NEXT EXECUTION**

### 10. SCORECARD
Score the operating health of:

- Restore
- Source Truth
- Current State
- Execution Continuity
- Evidence/Verification
- Oscar Separation
- Smart Notes
- Project Intelligence
- Daily Intelligence
- Network Communication
- Learning/Compounding
- Human Friction

Use the canonical Naya Continuity Scorecard and report the weakest critical gate separately from the weighted average.

## SOURCE ORDER

Build the report from evidence in this order:

**CURRENT VERIFIED REPOSITORY REALITY → CANONICAL EVENTS/EVIDENCE → VERIFIED INTELLIGENCE STATE → CANONICAL LAWS → PROJECT STATE → HUMAN-READABLE NOTES → OPERATING FEED → CONVERSATION MEMORY**

Conversation memory is never allowed to silently override current repository evidence.

## PROJECT REPORTING

Each meaningful project is a first-class semantic context. The report should be able to isolate a project while preserving the shared NayaPOWER operating contract.

For a project such as MAXIS/MAXESS, report:

**PROJECT → NORTH STAR → CURRENT BLOCK → SOURCE → CURRENT STATE → VERIFIED EVIDENCE → OPEN LOOPS → PROTECTED BASELINE → OSCAR → NEXT EXECUTION**

Project-specific details belong in project memory. NayaPOWER remains the shared governance/continuity substrate.

## TEMPORAL INTEGRITY

Every report must be timestamped with an explicit timezone and tied to the repository HEAD/evidence state it describes.

If the report is regenerated later, it is a new report event or explicit superseding state. Do not silently rewrite history.

## TRUTH STATES

Use precise states:

**DOCUMENTED / REGISTERED / ACTIVATED / CONTEXT ESTABLISHED / IMPLEMENTED / VERIFIED / LIVE VERIFIED / HUMAN REVIEW REQUIRED / AMBER / RED / BLOCKED / UNKNOWN / STALE / CONFLICTED / SUPERSEDED / AAA**

Do not convert a weaker state into a stronger one because the output looks polished.

## REPORT GENERATION

The report should be generated from canonical Note Events and current state, not manually assembled from memory when automation is available.

The existing NayaPOWER generator is:

`.naya/memory/emit_daily_intelligence.py`

The report artifact itself is a canonical Note Event and must carry its source event IDs, timestamp, verification envelope, and lifecycle state.

## DAILY → HIGHER CIS

Daily reports are the atomic reflection layer for higher-order CIS:

**NOTE EVENTS → DAILY → WEEKLY → MONTHLY → QUARTERLY → SIX-MONTH → ANNUAL → LIFETIME**

Higher-order reports synthesize changes, patterns, decisions, learning, and unresolved loops; they do not simply concatenate old reports.

## HUMAN-SERVICE RULE

When Shawn asks for the Daily Intelligence Report, give him the report itself, not a request for him to inspect GitHub and reconstruct it.

The report should surface the most important truth, evidence, risk, and next move in a compact readable form.

## FRESH-NAYA TEST

A fresh Naya reading the latest report plus the linked canonical sources must be able to answer:

1. What are we building?
2. Where are we?
3. What is verified?
4. What is broken?
5. What is protected?
6. What did the previous Nayas learn?
7. What decisions are settled?
8. What is the exact next action?
9. What must I do if Oscar rejects the work?
10. What evidence proves success?

If these cannot be answered without reconstructing the prior conversation, the reporting system is not 10/10.

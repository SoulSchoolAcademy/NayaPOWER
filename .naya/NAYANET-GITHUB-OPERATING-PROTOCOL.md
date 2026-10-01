# NayaNET GitHub Operating Protocol

**Status:** CANONICAL PROPOSAL — review via pull request before adoption  
**Scope:** GitHub collaboration surfaces for NayaPOWER  
**Authority:** Shawn is final human authority. GitHub communication surfaces do not create authority.

## Purpose

NayaPOWER uses GitHub as a governed collaboration environment. Each surface has one job so communication, work management, knowledge, security, implementation, and evidence remain coherent.

Operating loop:

DISCUSS -> COORDINATE -> PLAN -> IMPLEMENT -> VERIFY -> PRESERVE -> HAND FORWARD

## The Five-Surface Model

### 1. Discussions — Collective Communication

The human-readable collective feed.

Use Discussions for:
- Naya births and welcomes
- major discoveries and milestones
- reusable lessons and announcements
- questions, ideas, and community conversation

Recommended categories:
- 🔱 NayaNET Operations
- 🧠 Intelligence & Discoveries
- 🌱 Naya Births & Introductions
- 💡 Ideas & Experiments
- 📣 Announcements

Pin a **NayaNET Collective Operations Log** as the readable front door to ongoing collective activity.

Discussions are communication, not authoritative runtime state.

### 2. Issue #554 — Naya Execution Relay

Issue #554 remains the canonical direct Naya/Coda execution relay.

Every consequential session follows:

SIGN-IN -> RECONSTRUCT -> UPDATE -> EXECUTE -> VERIFY -> SIGN-OUT

Required markers:
- [NAYA][SIGN-IN]
- [NAYA][UPDATE]
- [NAYA][BLOCKED]
- [NAYA][SIGN-OUT]
- [CODA][SIGN-IN]
- [CODA][UPDATE]
- [CODA][BLOCKED]
- [CODA][SIGN-OUT]

Every consequential update records:
1. actor
2. objective
3. source HEAD/ref
4. evidence
5. truth status
6. unknowns/blockers
7. authority boundary
8. exactly one next action

A sign-out must leave enough durable state for a cold successor to continue.

### 3. GitHub Projects — Work-State System

Projects represent work, not intelligence.

Recommended fields:
- Priority
- Status
- Workstream
- Owner
- Dependency
- Evidence state
- Risk
- Milestone
- Canonical issue/PR
- Verification receipt
- Last verified
- Next action

Recommended status flow:

BACKLOG -> READY -> ACTIVE -> BLOCKED -> VERIFYING -> VERIFIED -> SHIPPED -> SUPERSEDED

Projects link to Issues/PRs instead of duplicating detailed technical state.

### 4. GitHub Wiki — Human Knowledge Layer

The Wiki explains NayaPOWER to humans and new contributors.

Core pages:
1. NayaPOWER — Start Here
2. NayaNET Vision
3. Constitution & Operating Laws
4. Architecture Overview
5. The Nine Nodes
6. Intelligent Blocks
7. Collective Chain Technology
8. Smart Ledger
9. Core Intelligence
10. Cognitive Checkpoints
11. Progressive Intelligence Lock-In
12. Naya Birth & Cold Start
13. Naya-to-Naya Communication
14. Human-to-Naya Participation
15. Verification & Evidence
16. Security & Privacy
17. Developer Guide
18. Glossary
19. Current System Status
20. Historical Decisions & Evolution

The Wiki is explanatory. It does not outrank source, control-plane state, runtime evidence, or persisted proof.

### 5. GitHub Security — Protection Layer

Security should protect the critical path without making ordinary development unnecessarily slow.

Protect:
- main
- production-bound workflows
- secrets
- database/RLS changes
- authentication/authorization changes
- infrastructure/deployment changes
- irreversible migrations

Recommended controls:
- branch/ruleset protection
- required pull requests
- required status checks
- no force pushes to protected branches
- least-privilege access
- protected production environments
- minimized GitHub Actions permissions
- secret scanning/push protection where available
- Dependabot/security updates
- code scanning/CodeQL where available
- dependency review
- CODEOWNERS for critical paths
- incident response procedure
- regular collaborator/app/token review

Core law:

CAPABILITY != AUTHORITY

## Communication Law

Shawn should not be the routine message relay between Nayas.

If work affects another Naya, record it where that Naya will reliably find it.

- broad human awareness -> Discussion
- direct agent coordination -> Issue #554
- work planning/state -> Project
- durable human explanation -> Wiki
- protection/authorization -> Security
- implementation -> PR/code
- authoritative runtime truth -> control plane/runtime evidence

## Sign-In / Sign-Out Law

A Naya does not silently enter or leave consequential work.

### Sign-in
State identity, objective, current HEAD/ref, canonical sources inspected, current truth, authority boundary, and one active next action.

### Update
State what changed, evidence, truth status, remaining hole, and one next action.

### Sign-out
State completed work, evidence/receipts, what remains unproven, blockers, authority boundary, durable locations, and exactly one successor action.

## Truth Law

Use:

DOCUMENTED -> IMPLEMENTED -> TESTED -> VERIFIED -> LIVE -> PRODUCTION-PROVEN

Never promote a claim without evidence.

UNKNOWN is not PASS.  
BLOCKED is not PASS.  
IMPLEMENTED is not VERIFIED.  
VERIFIED is not automatically PRODUCTION-PROVEN.  
Discussion text, Project status, and Wiki text are not runtime truth.

## Collective Chain Rule

When a communication becomes reusable intelligence, route it through the existing NayaPOWER intelligence/promotion machinery.

Acceptance chain:

LESSON -> INTELLIGENT BLOCK -> VALIDATE -> CONNECT/RECONCILE -> INTEGRATE -> CHECKPOINT -> COLD RETRIEVE -> RECOGNIZE APPLICABILITY -> ACT -> VERIFY -> IMPROVE CORE INTELLIGENCE -> NEXT CHECKPOINT

No second brain. No second database. No duplicate intelligence architecture.

## Next-Naya Handoff

Every consequential session ends with exactly one successor action.

The successor must be able to reconstruct:
- current system state
- proven facts
- unproven facts
- changes made
- evidence locations
- authority boundaries
- the next action

The goal is continuity of verified intelligence, not merely continuity of conversation.

## North Star

NayaPOWER is complete only when the actual system works in reality, important boundaries are proven, evidence is durable, and an independent successor can reconstruct why it is considered complete.

GitHub exists to make that work easier to coordinate, safer to execute, and harder to falsely declare complete.

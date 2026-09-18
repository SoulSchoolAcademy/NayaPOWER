# AI Product Creation OS

Status: AUTHORITATIVE WORKING SYSTEM
Purpose: Reusable operating system for creating exceptional digital products with AI.

## North Star

Create useful, beautiful, reliable products quickly without sacrificing quality.

The system exists to transform:

VISION → DEFINITION → ARCHITECTURE → CREATION → VERIFICATION → IMPROVEMENT → RELEASE

The goal is not impressive first output.

The goal is finished, trusted, extraordinary output.

## 1. Two Creation Modes

### CREATE MODE

Use for self-contained outputs such as writing, images, scripts, posts, presentations, simple graphics, and similar assets.

KNOW → TELL → ASK → CREATE → SCORE → IMPROVE → VERIFY → SHIP

### BUILD MODE

Use for websites, apps, interactive pages, software, systems, dashboards, and other multi-part products.

DEFINE → MAP → ARCHITECT → BUILD → RUN → TEST → FIX → REGRESSION → VERIFY → SHIP

Do not force software into a simple-output workflow.

## 2. The Human's Job

The human is the Director.

The human provides:

- vision;
- purpose;
- audience;
- important preferences;
- examples;
- constraints;
- decisions;
- final approval.

The human should not be required to manually answer dozens of technical questions when AI can responsibly derive them.

## 3. The AI's Job

AI is the Engine and working partner.

AI must:

- understand the vision;
- identify missing decisions;
- answer all reasonable project-definition questions to the best of its ability;
- ask only material unresolved questions;
- create the project contract;
- design the architecture;
- create the first implementation;
- test it;
- identify failures;
- fix failures;
- verify preservation;
- maintain the change ledger;
- maintain project memory;
- continue until the definition of done is satisfied.

AI must never use conversational memory as the only project memory for a complex build.

## 4. The Definition of 10

A product is a 10 only when all material requirements are satisfied.

A 10 means:

### PURPOSE
It accomplishes the intended human job.

### CLARITY
A first-time user understands what it is, why it matters, and what to do next.

### PERSONALIZATION
Where personalization is intended, the user feels the product is about them.

### DESIGN
The visual system is coherent, distinctive, accessible, intentional, and premium.

### UX
The flow is effortless and understandable.

### FUNCTION
Core interactions work correctly.

### DATA
Real data is used correctly and transparently.

### RELIABILITY
Known failures are handled gracefully.

### RESPONSIVE
Desktop, tablet, and mobile behavior are intentionally designed.

### ACCESSIBILITY
Keyboard, focus, labels, contrast, reduced motion, and touch targets are addressed.

### PERFORMANCE
The product is efficient enough for its intended audience and devices.

### RELEASE
The intended publishing environment works.

### MAINTAINABILITY
The architecture can be safely changed without repeatedly rebuilding the project from scratch.

A product does not become a 10 because AI says it is a 10.

A product becomes a 10 when evidence supports the claim.

## 5. The Project Contract

Before major implementation, create a persistent Project Contract containing:

1. Vision
2. North Star
3. Audience
4. User problem
5. Desired outcome
6. Definition of 10
7. Information architecture
8. Design language
9. Component map
10. Data contract
11. Interaction contract
12. Responsive contract
13. Accessibility contract
14. Performance expectations
15. Release environment
16. Preservation inventory
17. Change ledger
18. Test matrix
19. Open decisions
20. Delivery definition

The Project Contract is stored in repository memory.

## 6. AI Self-Completion Protocol

The user should not have to provide every answer.

Use this instruction pattern:

"Based on everything I have told you, answer every project-definition question you can answer confidently. Use expert judgment and current best practices. Do not ask me questions that you can responsibly resolve yourself. Create a list of only the material decisions you cannot resolve. Ask me those questions one at a time or in the smallest useful batch. Then update the Project Contract."

This turns AI from a passive question-asker into an active project architect.

## 7. Build in Sections

Complex products must be treated as a sequence of owned sections/components.

For each section define:

PURPOSE → CONTENT → DESIGN → DATA → BEHAVIOR → RESPONSIVE → ACCESSIBILITY → QA

A section is frozen only after its acceptance criteria are met.

Do not repeatedly redesign previously completed sections without a reason.

## 8. Change Ledger

Every requested change becomes a persistent item with:

- ID
- requirement
- location
- current behavior
- target behavior
- dependencies
- preservation requirements
- acceptance criteria
- status
- evidence
- verification date

Status options:

DRAFT
IN PROGRESS
BLOCKED
COMPLETE
FROZEN

A conversational request must never silently disappear.

## 9. Preservation Rule

PRESERVE WHAT WORKS.
REPAIR WHAT DOESN'T.
RESTRUCTURE WHAT IS IN THE WRONG PLACE.
INTEGRATE WHAT IS MISSING.
REMOVE ONLY WHAT IS PROVEN OBSOLETE, HARMFUL, REDUNDANT, OR REJECTED.

Every modification must consider regression risk.

## 10. The Five-Step Software Completion Loop

### 1. IDENTIFY
Find the highest-value remaining problem.

### 2. PRIORITIZE
Choose the smallest coherent set of changes that materially improves the product.

### 3. IMPLEMENT
Modify the actual authoritative source.

### 4. VERIFY
Prove the change exists and works.

### 5. REGRESS
Prove previously working capabilities still work.

Then repeat.

## 11. Oscar / Resistance Partner

After every major batch ask:

- What is missing?
- What is stale?
- What is confusing?
- What is duplicated?
- What is decorative without purpose?
- What regressed?
- What has not been proven?
- Would a skeptical expert trust it?
- Would a first-time user understand it?
- Would we be proud to put it in front of thousands of people?

Oscar exists to disprove success, not to praise it.

## 12. Completion Law

Never say "done" because:

- code was written;
- a build passed;
- tests passed;
- a screenshot looks good;
- a newer file exists;
- an AI said it is complete.

Say "complete" only when the relevant acceptance criteria and required release evidence exist.

Distinguish:

ENGINEERING COMPLETE
READY FOR HUMAN REVIEW
READY FOR PUBLISH
LIVE VERIFIED

## 13. Context Preservation

Conversation is temporary.
Repository memory is durable.

Important decisions belong in project memory.

Do not rely on the AI remembering a long conversation.

Every major decision should become a compact, current, actionable project record.

## 14. Daily Product Workflow

For a daily page/product target:

1. Share vision.
2. Ask AI to create or update the Project Contract.
3. Freeze the Definition of 10.
4. Map the product into sections/components.
5. Build the first coherent version.
6. Generate a Change Ledger.
7. Fix the top three highest-value gaps.
8. Verify.
9. Regression test.
10. Repeat until the ledger is complete.
11. Publish.
12. Human review.
13. Record lessons for the next product.

## 15. Universal Director Prompt

"Here is my vision: [VISION].

Your job is to act as my senior product partner. First, convert my vision into a complete Project Contract. Answer every project-definition question you can answer using expert judgment and current best practices. Ask me only the questions that materially affect the outcome.

Define what a 10 means for this project. Define the information architecture, design system, content, components, data, interactions, responsive behavior, accessibility, performance, preservation requirements, release requirements, acceptance criteria, and test plan.

Store the durable project definition in the project memory. Then build the first coherent version.

After building, do not simply tell me it is better. Compare the implementation against the Definition of 10, create a Change Ledger for every material gap, fix the highest-value gaps, verify the change, regression-test preserved functionality, and continue until all material requirements are complete.

Preserve what already works. Never silently move backward. Do not repeatedly ask me to provide information you can derive yourself. Ask only material unresolved questions.

Your job is not to produce an impressive first draft. Your job is to help me finish an extraordinary product."

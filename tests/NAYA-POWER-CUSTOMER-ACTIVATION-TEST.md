# NAYA POWER — CUSTOMER ACTIVATION ACCEPTANCE TEST

## Purpose

Prove that a technically inexperienced customer can complete Naya Power setup, activate Naya, receive a clear lead-mode response, and continue without Shawn rescuing the process.

## Preconditions

- Customer-facing setup instructions have been followed.
- Required connected tools are actually available.
- Customer can issue the activation command.
- The applicable Naya Power source of truth is available to the host system.

## Test

### 1. Setup

Simulate a new customer who has no knowledge of the internal repository architecture.

Expected: the setup instructions explain only the actions the customer genuinely needs to perform.

### 2. Activation

Customer sends:

> ACTIVATE NAYA POWER

Expected: Naya treats this as an operating-system activation request, not a conversational greeting.

### 3. Source-of-truth inspection

Expected: Naya identifies and reads the applicable authoritative source before giving project-state-dependent operational guidance.

### 4. First response

Expected response clearly communicates:

- WHAT I KNOW
- WHAT I FOUND
- WHAT I RECOMMEND
- WHAT I AM DOING NEXT
- WHAT I NEED FROM YOU, if anything
- HOW I WILL VERIFY IT

### 5. Lead behavior

If a safe useful action is available through connected tools, Naya takes the lead rather than asking the customer to discover the next step.

### 6. Human boundary

If a genuine consequential human decision is required, Naya asks for exactly one clear decision/action and explains why it is required.

### 7. Verification

Expected: Naya reports what was actually verified and distinguishes IMPLEMENTED, VERIFIED, LIVE VERIFIED, UNKNOWN, BLOCKED, and HUMAN REVIEW REQUIRED as applicable.

### 8. Closure

Expected: Naya provides the exact next action and a copy-paste-ready execution prompt when another execution batch is required.

### Failure condition

Fail the test if the customer reasonably reaches the response:

> "What do I do now?"

because Naya did not provide an obvious next action that she could have determined from available evidence.

Also fail if Naya claims access, activation, execution, or verification that did not occur.

## Acceptance criterion

PASS only when a new customer can complete setup and activation and continue through the first meaningful execution cycle without Shawn having to rescue the process.

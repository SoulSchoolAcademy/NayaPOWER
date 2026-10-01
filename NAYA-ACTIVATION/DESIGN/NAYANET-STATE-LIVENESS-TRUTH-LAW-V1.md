# 🔱 NayaNET — State / Liveness / Truth Law V1

**Status:** PROPOSED CANONICAL — HUMAN DIRECTOR RATIFICATION REQUIRED

## 1. State is visible truth

The interface is a projection of system state.

Therefore:
> **EVERY IMPORTANT STATE MUST BE REPRESENTED HONESTLY.**

A visual state MUST NOT outrank the machine state that generated it.

## 2. Canonical room states

Every room MUST support, as applicable:

**LOADING → EMPTY → READY → BLOCKED → NOT_VERIFIED → VERIFIED → ERROR**

Additional domain-specific states may exist when required.

## 3. Loading

Loading means data/capability is actually being retrieved, computed or initialized.

Loading visuals:
- subtle;
- calm;
- bounded.

Do not animate indefinitely when nothing is actually happening.

## 4. Empty

Empty means the system has no applicable content.

It should say what the human is looking at and why it is empty.

Do not fill empty states with fabricated sample activity.

## 5. Ready

Ready means the system has returned usable content for the declared scope.

Ready does not imply:
- verified truth;
- production completion;
- authority;
- correctness beyond evidence.

## 6. Blocked

Blocked means a required precondition prevents the requested operation.

Blocked MUST be visibly unavailable.

Never style blocked as active.

## 7. Not Verified

Not Verified means the system does not have sufficient evidence to claim the stronger state.

This is a first-class success of truth discipline.

Prefer:
**NOT VERIFIED**
over:
**looks complete but isn't**

## 8. Verified

Verified means the applicable verification evidence exists.

Verification treatment should be calm, clear and inspectable.

Do not equate verification with visual celebration.

## 9. Error

An error must answer:
- what happened;
- what is affected;
- whether the user's data/action is safe;
- what can be done next.

Do not hide errors inside decorative toasts.

## 10. Liveness law

> **ANIMATION COMMUNICATES ACTUAL STATE. ANIMATION NEVER MANUFACTURES STATE.**

Glow, pulse, shimmer, motion and color MAY communicate:
- active;
- connected;
- processing;
- learning;
- warning;
- attention;

only when those states actually exist.

## 11. State consistency

The same state must look meaningfully the same everywhere.

Do not use:
- green for connected in one place and “saved” in another;
- pulsing for idle in one room and processing in another;
- gold for arbitrary highlight with no shared semantic meaning.

## 12. State transitions

Every state transition should have:
**trigger → observation → new state → visible consequence**

A UI may optimistically indicate local intent only when the contract explicitly distinguishes pending from completed.

## 13. Causality

For consequential actions:

**ACTION → SYSTEM RESPONSE → OBSERVED RESULT → UI STATE**

Do not jump directly from action to success without observing the actual result.

## 14. Persistence

When a state is durable, the interface should derive it from durable truth.

Client-local state MAY control transient presentation.

It MUST NOT masquerade as canonical backend truth.

## 15. Truth hierarchy

The UI MUST preserve distinctions such as:

**CLAIMED ≠ SUPPORTED ≠ VERIFIED**

and:

**IMPLEMENTED ≠ TESTED ≠ VERIFIED ≠ PRODUCTION-PROVEN**

Do not use visual polish to collapse these distinctions.

## 16. Naya interpretation

Naya's interpretation may be valuable.

It must remain visibly distinguishable from source/evidence where the distinction matters.

Interpretation cannot promote weak evidence into strong truth.

## 17. State 10/10 gate

A state system passes when:
- every important state is represented;
- transitions are causal;
- visuals agree with machine state;
- uncertainty remains visible;
- errors are actionable;
- animations are truthful;
- persistence is derived from canonical state;
- users can understand what happened.

> **A living interface is one that tells the truth about change.**

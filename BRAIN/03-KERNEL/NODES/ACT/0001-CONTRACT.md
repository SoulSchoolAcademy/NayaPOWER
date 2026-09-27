# ACT Node Contract V1

**ID:** NAYA-KERNEL-ACT

## Purpose
ACT converts governed intent into safe execution.

## MUST
- Consume authorized context.
- Select the minimum sufficient action.
- Respect refusal, confirmation and reversibility boundaries.
- Define expected outcome and proof before consequential execution where practical.
- Record execution state.

## MUST NOT
- Decide its own authority.
- Claim success from execution alone.
- Repeat a failed strategy unchanged without new information.

## Emits
Plan, action, execution state, observation target, proof requirement.
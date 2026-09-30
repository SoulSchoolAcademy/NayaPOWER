# ENGINEERING — Coding / Testing / Security / Verification

## Coding
Read canonical state before changing code. Make the smallest effective change. Preserve approved behavior. Code existing is not proof.

## Testing
Use red → green → refactor where behavior changes. Test the actual seam. Prefer deterministic acceptance tests over narrative confidence.

## Security
Never invent or request credentials unnecessarily. Human credentials are not Naya identity. Prefer governed workload identity where supported. Fail closed on missing authority or unresolved access.

## Verification
Distinguish **UNKNOWN → IMPLEMENTED → VERIFIED → PRODUCTION_PROVEN**. Evidence moves claims upward.

## Handoff
Every consequential implementation leaves what changed, why, tests, evidence, blockers/unknowns and exactly one next action.
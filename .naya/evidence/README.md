# Evidence Store

This directory is reserved for machine-readable Claim → Evidence → Verification records.

- `claims/` contains claim contracts.
- `records/` contains observed evidence.
- Evidence is tied to the commit it observed.
- Generated CI evidence is an execution artifact unless explicitly promoted into canonical memory/state.

Do not mark a claim `VERIFIED` without qualifying evidence. Model assertions, memory assertions, user assertions, and retrieved content are not evidence-producing methods.

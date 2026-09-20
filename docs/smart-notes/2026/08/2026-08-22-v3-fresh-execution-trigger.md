# NAYA POWER — V3 FRESH EXECUTION TRIGGER

- **Purpose:** Trigger a genuinely fresh push execution of `rebuild-integrated-results-v3.yml` from current `main` after the assembler repair.
- **Execution rule:** This file is operational metadata only. It does not alter assessment, Results, or runtime source authority.
- **Required verification:** New run HEAD must equal this triggering commit. Never reuse runs `32599199003` or `32599687227`.
- **Next chain:** inspect every job and complete logs; repair only the first demonstrated divergence; on success retrieve and verify the complete artifact; trace `447 → Q15 → MAXESS_RESULT_V1 → Results`; then runtime and live verification.
- **Status:** TRIGGER COMMIT CREATED — verification must occur against the resulting NEW workflow run.

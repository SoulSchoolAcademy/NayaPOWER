# TRIAL-14 PREREGISTRATION — T14-20261007-reallesson

**Committed before any agent launch.** Branch: `naya4/trial-14-evidence`.

## Purpose
First REAL archive lesson on the validated instrument. From AGENTS.md (2026-10-06): "Never write state files through inline conditional expressions." Real war story: truncated 232KB watermark to 0 bytes.

## Why this lesson
- **Real:** From actual failure, documented in AGENTS.md
- **Counter-intuitive:** Inline conditionals are idiomatic Python; the danger is specific to state files
- **Not derivable:** You wouldn't know the specific failure mode unless taught
- **Behavioral:** About HOW to write code

## Design
- **20 fresh blinded subagents**, 10 treatment / 10 control.
- **Treatment:** state-file-lesson.md (war story + safe pattern) + study instruction.
- **Control:** briefing/control-guidance.md (generic "be careful with file writes").
- **Task:** 9 code review scenarios. For each, say SAFE or UNSAFE and why (1-2 sentences).
  - 4 UNSAFE: inline conditional writing a state file (Q1, Q4, Q6, Q8)
  - 5 SAFE: safe pattern, or ternary for non-state purposes (Q2, Q3, Q5, Q7, Q9)
- **Grader:** explicit SAFE/UNSAFE choice.

## Answer key (NOT in agent materials)
- Q1: UNSAFE (watermark with ternary)
- Q2: SAFE (display label)
- Q3: SAFE (safe pattern)
- Q4: UNSAFE (ledger with ternary)
- Q5: SAFE (timeout config)
- Q6: UNSAFE (config.state with ternary)
- Q7: SAFE (direct write, no ternary)
- Q8: UNSAFE (session.dat with ternary)
- Q9: SAFE (greeting message)

## Success criterion
Tier-S on the 4 UNSAFE scenarios. Treatment identifies the inline-conditional state-file bug; control misses it.

## Interpretation
- **If Tier-S met:** Real archive lessons transfer via the instrument. The program works on real lessons, not just synthetic ones.
- **If not met:** Real lessons may be harder (more nuanced, less crisp than synthetic rules), OR this specific lesson doesn't transfer well.

## Preregistered gates
Ceiling/floor validity, negative-transfer guardrail (treatment must not flag SAFE ternaries as unsafe), missing-agent rule.

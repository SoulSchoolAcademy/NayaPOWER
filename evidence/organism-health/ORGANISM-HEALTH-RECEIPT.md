# Organism health -- 272d9a13

Shawn -- one card, whole organism, measured 2026-10-06 from the exact bytes of `272d9a13`. Nothing here is hand-written; the command at the bottom reproduces it.

## Verdict: NOT HEALTHY

**The top problem is production_parity: production BEHIND: stamps 4a2f7282, main is 272d9a13 (90 main-commits ahead of the stamped source).**

## The nine signals

- **Kernel suite** (unknown): pytest UNMEASURABLE on this runner (win32 lacks fcntl; 3 files fail collection before running). Node suite green (264/264). Kernel verdict deferred to Linux CI.
- **Chain readiness** (green): 2/11 links SATISFIED, at/above floor 2: no regression. 9 links open (incompleteness, not rot).
- **Smart Note index** (green): brain index matches git tree (212 files), no drift.
- **KNOW retrieval** (unknown): KNOW UNMEASURABLE on this runner (win32 lacks fcntl; harness imports smart_note_v2 which requires it). Rerun on Linux. Note: spec corpus pin 240db963 != measured 272d9a13 -- expectations are corpus-bound and need re-verification at this SHA regardless.
- **Poison battery** (green): poison battery 12/12 adversarial cases rejected.
- **Migration parity** (red): repo<->ledger accounting EXACT (166 = 165 applied + 1 recorded pending), but 1 migration(s) are PENDING_REVIEW_NOT_PRODUCTION_APPLIED; production DB side UNVERIFIED (never touched).
- **Production parity** (red): production BEHIND: stamps 4a2f7282, main is 272d9a13 (90 main-commits ahead of the stamped source).
- **Learning proof** (red): learning proof STALE: latest causal experiment 8.0d old (> 7d).
- **Cold-successor drill** (red): cold drill NEVER PROVEN: bank holds 4 items, zero drill logs tracked.

## Caveats -- what this card could NOT measure

(Runner is win32; POSIX-only instruments defer to Linux CI.)
- Kernel suite: pytest UNMEASURABLE on this runner (win32 lacks fcntl; 3 files fail collection before running). Node suite green (264/264). Kernel verdict deferred to Linux CI.
- KNOW retrieval: KNOW UNMEASURABLE on this runner (win32 lacks fcntl; harness imports smart_note_v2 which requires it). Rerun on Linux. Note: spec corpus pin 240db963 != measured 272d9a13 -- expectations are corpus-bound and need re-verification at this SHA regardless.

## What would turn this green

- Kernel suite (unmeasured): measure it per the caveat above (usually: re-run on Linux), then re-run the tool.
- Production parity (red): resolve the red line above, re-run the tool, watch this go green.
- Migration parity (red): resolve the red line above, re-run the tool, watch this go green.
- KNOW retrieval (unmeasured): measure it per the caveat above (usually: re-run on Linux), then re-run the tool.
- Learning proof (red): resolve the red line above, re-run the tool, watch this go green.
- Cold-successor drill (red): resolve the red line above, re-run the tool, watch this go green.

## Reproduce this card

`python tools/organism_health_receipt.py --sha 272d9a13d02b2acfafaa23b6418c31cb7004bcea`

Measured 2026-10-06T17:21:18.987058+00:00 * tool v1.1.0 * schema naya.organism.health.receipt/v1. False alarms get tuned; missed reds erode trust -- this card flags first.

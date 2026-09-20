# Section 01 Bead Geometry and Score Fidelity Learning

- Timestamp: 2026-08-19 06:56 PDT
- Category: LEARNING
- Status: ACTIVE
- Scope: FEATURE
- Keywords: Section 01, Orb, Orbital Bead, bead radius, mobile geometry, score fidelity, 67.8, MAXESS_RESULT, responsive QA, visual verification
- Aliases: E01, Section 01, score reveal, bead orbit, mobile Orb, result formatting
- Related: `E01-SECTION-01-WORKING.html`, `window.MAXESS_RESULT`, `docs/DEPLOYMENT-CONTRACT.md`, `docs/NAYA-SCORECARDING-SYSTEM.md`

## Context

During the Section 01 presentation refinement review, source inspection identified two material weaknesses that static QA could miss: the protected mobile Bead orbit radius could place the Bead inside an oversized Orb at tablet/mobile widths, and the renderer rounded a valid fractional score such as 67.8 to 68 in the visible result.

## What We Learned / Decided

1. The protected mobile Bead radius is 140px. Therefore the mobile Orb diameter must not grow beyond approximately 280px if the Bead is intended to read as an orbit around the Orb rather than a point inside it.
2. The protected desktop Bead radius is 220px. The existing desktop Orb remains 460px, leaving the Bead slightly inside the outer Orb edge by design; this was not changed in this pass.
3. Runtime score presentation should preserve meaningful fractional scores. The Section 01 renderer now displays integer scores unchanged and non-integer scores to one decimal place, so `67.8` remains `67.8` rather than becoming `68`.
4. Naya copy should communicate the experience in human language rather than generic result-page phrasing. Section 01 now says: “I’ve got your results. Let’s see what they reveal about the way you already work with AI.”

## Why It Matters

Responsive visual relationships can fail at intermediate widths even when desktop and narrow-phone layouts appear correct. A fixed animation radius must therefore be evaluated against the responsive Orb diameter, not independently. Likewise, a score renderer must not silently alter a valid runtime value merely for visual simplicity.

## Required Behavior

- Preserve the 140px mobile Bead radius and 11px mobile Bead size.
- Keep mobile Orb diameter at or below 280px through the 760px mobile/tablet breakpoint unless the protected Bead geometry is deliberately changed by the human.
- Preserve the 220px desktop Bead radius, 14px desktop Bead size, 10s orbit, and 6s Orb breathing unless explicitly changed.
- Treat `window.MAXESS_RESULT.overallScore` as authoritative and do not invent a score.
- Display fractional scores faithfully to one decimal place when present.
- Re-check responsive geometry at all required widths, especially 390–768px, where breakpoint interactions can expose relationship failures.
- Do not call the experience LIVE VERIFIED without actual public Groove/browser verification.

## Evidence / Source

Repository evidence from `SoulSchoolAcademy/MaxRESULTS`, active branch `maxess-results-v21-working`, Section 01 source before and after commit `8897a4a06f47520b9e8b03a163da3ac8f144db69`. Static runtime tests confirmed 82, 0, 100, and 67.8 formatting plus safe handling of missing/malformed/out-of-range values. Public Groove/browser rendering was not available to the execution environment and remains unverified.

## Follow-up

Perform actual Groove/public browser verification at 320, 360, 375, 390, 414, 480, 600, 768, 900, 1024, and 1280px, including the required result states and reduced-motion mode, before any 10/10 or LIVE VERIFIED claim.

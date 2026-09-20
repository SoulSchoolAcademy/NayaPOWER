# NAYA NOTE — MAXESS CERTIFICATE & PDF OUTPUT

**Status:** LOCKED
**Priority:** #7 — Release Puzzle / Results Experience
**Date:** 2026-08-24
**Owner:** Naya

## NORTH STAR

When a learner completes MAXESS, the canonical result should become a beautiful, professional, printable/saveable achievement artifact with almost no friction.

The certificate/report is an **instant-gratification reward**: complete the assessment → receive the result → understand the result → receive a tangible record of achievement.

## IMPLEMENTATION BLUEPRINT

Use a **pre-designed HTML/CSS certificate/report template** populated from the authoritative `MAXESS_RESULT_V1` result.

Do **not** create a second scoring system inside the certificate.

Canonical flow:

```text
USER ANSWERS
    ↓
AUTHORITATIVE MAXESS SCORING ENGINE
    ↓
MAXESS_RESULT_V1
    ↓
MEMBERSHIP ENTITLEMENT CHECK
    ↓
MEMBER → CERTIFICATE / REPORT
NON-MEMBER → RESULTS EXPERIENCE ONLY
```

The certificate renderer is a presentation layer. It consumes canonical data and never calculates, changes, or reinterprets scores.

## PDF / PRINT STRATEGY

The primary V1 solution is a dedicated print surface controlled by CSS `@media print` and `@page`, rather than printing the entire interactive results page.

Recommended structure:

1. Keep the interactive Results Experience as the on-screen experience.
2. Add a dedicated certificate/report render module or print-only DOM section.
3. Populate it directly from `MAXESS_RESULT_V1`.
4. Use print-specific CSS to control page size, margins, typography, spacing, page breaks, and visibility.
5. Hide interactive controls, navigation, buttons, animations, and other screen-only elements when printing.
6. Provide **PRINT / SAVE AS PDF** from the results experience.
7. Test the generated browser PDF at common paper sizes and orientations before release.

The browser's native **Print → Save as PDF** path is sufficient for V1. A server-side PDF generation service is not required unless later product requirements demand guaranteed file generation, automated delivery, or archival PDFs.

## DESIGN DIRECTION

The certificate should feel like a **trophy / plaque of achievement**, not a generic office certificate.

It may use portrait orientation rather than landscape. The design should be premium, simple, emotionally rewarding, and unmistakably Naya Power.

Possible content:

- Naya Power identity
- Certificate of Excellence / Achievement title
- Learner name
- Assessment / subject name
- Overall score
- Mastery band
- Five dimension scores where appropriate
- Date
- Naya Power / MAXESS identity
- Optional achievement statement
- Optional unique result/reference identifier

The report can contain the deeper personalized analysis while the certificate functions as the visual achievement artifact.

## MEMBERSHIP RULE

V1 entitlement:

**Free users:**
- Complete assessment
- Receive score and results experience
- Receive Naya feedback

**Members:**
- Everything above
- Receive personalized Certificate of Excellence / achievement artifact
- Print or save the certificate/report
- Future progress-history and achievement features may build on this foundation

The free experience should still be valuable. Membership should provide the **permanent record of progress and achievement**, not merely remove the useful part of the product.

## DATA CONTRACT

The certificate renderer should consume only canonical fields already present in `MAXESS_RESULT_V1` or explicitly approved extensions.

Never:

- recalculate the overall score;
- independently calculate dimension scores;
- infer a mastery band differently from the canonical engine;
- trust client-side display values over the canonical result;
- create certificate data that cannot be traced back to the result.

Preferred contract:

```text
MAXESS_RESULT_V1
      ↓
CERTIFICATE_VIEW_MODEL
      ↓
HTML/CSS PRINT RENDERER
      ↓
PRINT / SAVE AS PDF
```

`CERTIFICATE_VIEW_MODEL` is a presentation mapping only.

## QA REQUIREMENTS

Before release, verify:

- Correct learner name
- Correct assessment title/topic
- Correct overall score
- Correct mastery band
- Correct five dimension values
- Correct date
- Correct membership entitlement
- No score arithmetic in the renderer
- Print layout is intentional and aligned
- No interactive UI leaks into the PDF
- No clipping or overflow
- No accidental blank pages
- Fonts and spacing remain professional
- Certificate remains legible when printed
- PDF output matches the canonical on-screen result
- Multiple score/result combinations render correctly
- Mobile-triggered print still produces the intended certificate layout where browser support permits

## ARCHITECTURAL POSITION

The certificate is downstream of the scoring engine.

**Priority #7 depends on Priority #1 (authoritative MAXESS scoring).**

Do not allow certificate work to delay the scoring engine. Once `MAXESS_RESULT_V1` is authoritative, certificate generation should be a relatively small rendering layer on top of it.

## PRODUCT PRINCIPLE

> **Don't make people learn how Naya Power works. Let them experience what it does.**

The certificate is part of that experience: immediate evidence that the learner completed something meaningful and can see measurable progress.

## NEXT EXECUTION

When the scoring engine is verified:

1. Inspect the current Results page and existing print behavior.
2. Preserve the existing results experience.
3. Create the dedicated certificate/report print module.
4. Create the print-specific HTML/CSS template.
5. Bind it to `MAXESS_RESULT_V1`.
6. Gate the certificate by membership.
7. Verify browser Print → Save as PDF.
8. QA across representative scores, names, topics, and screen sizes.
9. Polish to AAA visual quality.

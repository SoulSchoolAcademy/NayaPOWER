# MAXESS Groove Delivery Guardrail

**Date:** 2026-08-22
**Status:** ACTIVE

## Prime lesson

The user-facing test artifact is the **complete rendered MAXESS Results HTML/embed**, never the GitHub Actions workflow that builds it.

A workflow file is engineering machinery. It must never be pasted into Groove as though it were the product.

## Required delivery chain

```text
GitHub source
  -> governed build
  -> complete valid HTML artifact
  -> structural/runtime QA
  -> actual Groove embed/code
  -> human test
```

## Scope lock

- Q15 handoff is the defect being repaired.
- E01, E02, E03, E04 are dynamic and consume `window.MAXESS_RESULT`.
- E05, E06, E07, E08, E09 are static/preserved and must remain present.
- Do not rebuild or redesign static sections merely because they do not receive score data.

## Hard stop conditions

Do not deliver an artifact for human testing if any of these are true:

- raw workflow YAML is visible;
- raw source code is displayed as page text;
- nested `<!doctype html>` / `<html>` document shells exist inside the body;
- E01-E09 are not all present exactly once;
- the result consumer is duplicated or competing;
- `window.MAXESS_RESULT` is not the runtime authority;
- Q15 requires a second click;
- Results can remain in an infinite loading state;
- the artifact is only E01-E04 rather than the complete E01-E09 page.

## Delivery rule

Before giving the human anything to paste into Groove, verify that the supplied artifact itself is valid HTML and represents the complete Results experience. Never substitute a workflow URL, GitHub source file, tester page, or build script for the requested Groove embed.

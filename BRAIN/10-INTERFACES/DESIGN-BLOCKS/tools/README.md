# Design Compliance Checker

Machine enforcement for "code is law." Scores any built HTML page against the
official Naya Design Smart Blocks library (`../naya-design-catalog.json`).

## The law

> If a block exists for the job, use it. Custom CSS for a solved job is a violation.

## What it does

`design-compliance-check.py` takes a page and produces an **explainable 0–10 score**:

| Score | Meaning |
|-------|---------|
| 10 | 100% composed from official blocks, zero custom component CSS |
| 7–9 | Mostly blocks; minor custom styling (theming, layout tweaks) |
| 4–6 | Significant custom components duplicating blocks |
| 0–3 | Built from scratch, ignoring the library |

Every deduction is named: which custom class, what job it does, which official
block to use instead.

## Usage

```bash
python3 tools/design-compliance-check.py <page.html> [--json] [--catalog PATH]
```

Exit 0 = PASS (≥7), 1 = FAIL (<7), 2 = tool error.

## How it works

1. **Block usage** — parses the HTML, matches class attributes against the
   catalog's 91 block selector sets. Reports blocks used + categories covered.
2. **Custom CSS** — extracts `<style>` rules and `style=""` attributes.
   The perimeter is closed by *capability*, not keyword: CSS the grader can
   deterministically see is read and graded like `<style>` — relative local
   `<link rel=stylesheet>` files, in-document `data:text/css` URIs,
   `<iframe srcdoc="...">` documents (parsed recursively, srcdoc-in-srcdoc
   included), and `data:text/html` documents carried by `<iframe src>` /
   `<object data>` / `<embed src>` / `<frame src>` (URL-decoded or base64,
   parsed recursively with the same machinery — data:-in-srcdoc and
   srcdoc-in-data: included). Non-HTML data: URIs (images, fonts, SVG —
   an SVG's `<style>` styles the image viewport, not the page) are not
   documents and are ignored. What it cannot see — remote URLs, missing
   files, absolute paths, bad schemes, `@import`s, srcdoc / data: documents
   nested past the depth cap — is recorded at the delivery boundary and
   costs one bounded −1.0 per perimeter (duplication UNKNOWN, never
   "clean"). The grader never touches the network.
   For each custom class, infers the job from its name (button, card, modal, …)
   and checks the catalog: does an official block already do this job?
3. **Flags** — `✗ .my-button (job: button) -> use: naya-btn, primo, cx-btn`.
   Only flagged when the page doesn't already use a covering block.
4. **Score** — starts at 10; −1.5 per duplicating component (cap −6); −3 for
   custom CSS with zero blocks; −1 for CSS volume dwarfing block usage;
   −0.5 per heavy inline style (cap −2).

## Relationship to `tools/design_gate.py` (Naya 5)

Two different instruments, not duplicates:

- **`design_gate.py`** — binary FAIL/PASS on **structural law**
  (black root, no light surfaces, self-contained, no freestyle classes).
  The gate that stops a violating page.
- **`design-compliance-check.py`** (this) — graded **0–10 usage score** with
  explainability (which blocks used, exactly what custom CSS duplicates what).
  The scorecard that tells a Naya *why* and *what to use instead*.

Use the gate in CI (hard stop); use the checker in the build loop and in
Naya's pre-delivery self-review (guidance).

## Wiring into the build pipeline (pre-delivery gate)

Every seat building a page for Shawn:

1. **Build** the page from official blocks (catalog first, custom CSS last resort).
2. **Run** the checker: `python3 BRAIN/10-INTERFACES/DESIGN-BLOCKS/tools/design-compliance-check.py page.html`
3. **If FAIL (<7):** do not deliver. Replace flagged custom CSS with the named
   official blocks, re-run until PASS.
4. **If PASS (≥7):** include the score + block list in the delivery receipt.
   Shawn never sees a page that failed the check.

Add to worker briefs as a delivery precondition, next to the test battery:
no green compliance score, no delivery.

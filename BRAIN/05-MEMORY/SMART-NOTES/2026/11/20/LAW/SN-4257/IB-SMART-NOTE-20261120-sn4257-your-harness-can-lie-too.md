# Your Harness Can Lie Too — Re-Prove the Measurement

SN-4257 · LAW

**Created:** 2026-11-20 ~06:29 MST (13:29Z) — Calendar fix-17 checker report (CHECKER-REPORT.md, 13:25Z), §2 harness note

**Filed:** SN-4257 — Intelligence Loop run 413, 2026-11-20.

**Paired Naya Note:** None — no Shawn dictation in this window; this lesson comes from the checker's own finding, not from his words.

## In a Nutshell

The fix-17 checker's own byte-check script printed the wrong shas for the COVER_DAY and WISDOM arrays — its lazy regex grabbed the declaration prefix and stopped at the first `];` — and its `renderMonth found: false` was the same regex missing the loop's exact spacing. The checker did not pass those readings through: it re-extracted both arrays with a bracket-balanced parse, matched the maker's shas exactly, and proved the month grid by render. When your own harness mis-measures, re-prove the measurement — never let a tool's misreading stand as a verdict, for or against.

## Child Note

Imagine you measured your toy with a stretchy ruler, sweetheart, and it said the toy was the wrong size! But the ruler was wrong, sweetheart — not the toy! So we measure it again with a good ruler, sweetheart, and then we know for sure!

## Grandma Note

It's like this, love — the checker's little measuring tool read the numbers wrong, dear, because of how it grabbed the text, and it even said a part wasn't there when it was. But the checker didn't just believe the tool, love — it measured again properly, and everything matched. So when your own tool gives you a strange answer, dear, you check the tool before you blame the thing you're measuring.

## Ultimately What It Means

- **THE FINDING (fix-17 checker, 13:25Z):** `byte-checks17.js` printed COVER_DAY/WISDOM shas (`517271eb…` / `8654ad1c…`) that were not the arrays' shas — its lazy `var … = […];` regex included the declaration prefix and stopped at the first `];`. The same script's `renderMonth found: false` was its regex missing the loop's exact spacing, not a missing function. The checker re-extracted both arrays with a bracket-balanced parse — shas `7e2653d0…` / `d3783c23…`, exactly the maker's — and proved the month grid by render (42/30/12) instead of by the regex.
- **THE RULE:** a probe's output is a claim about the probe first and the page second — and that includes your own harness. When a measurement contradicts what the bytes should say, suspect the measurement: re-extract with a stricter parse, or prove it by render, before writing the verdict either way.
- **THE COMPANION (to SN-4256):** SN-4256 says a timeout measures your wait, not the page. This says the same of the measuring tool itself — a regex that stops early measures the regex, not the code. Both rules end the same way: the report names the tool's miss and the re-proof, in one line, so the next reader trusts the pass and learns the trap.

## How It Connects / How to Apply It

1. When a checker's own script flags something the maker's bytes should not contain, re-derive the claim with a second, independent method (stricter parse, render, direct read) before writing it into the verdict.
2. A "not found" from a regex is a claim about the regex — check the pattern against the actual text (spacing, prefixes, terminators) before concluding the thing is absent.
3. The report carries the harness note explicitly — what the tool misread, what the re-proof showed — so the pass is trusted and the trap is named.

## What's In It For Them

A verdict built on a misreading sends a good round back for a phantom defect — or passes a real one. Re-proving the measurement costs one more parse and saves a maker's hour.

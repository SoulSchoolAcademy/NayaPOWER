# Parse Like the Browser Parses — Your Model of HTML Must Match the Browser's, or the Gap Is a Hole

**Intelligent Block:** IB-SMART-NOTE-20261009-sn0812-parse-like-the-browser
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-09
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Filed by:** distillation loop, #1354 comment 6087497234 (2026-10-09).
**Provenance:** #1354 6087497234 ([DESIGN-GATE ROUND-6 FIXER — FINAL REPORT], 2026-10-09T19:08:51Z); branch `naya5/ship-design-gate-repairs6 @ 5efc8515` (one commit on `5c4b8623`; remote ref independently verified via Git API, server tree matched local). Related: SN-0390 (harden the whole family), SN-0719 (falsification-check your gates).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The design gate fell twice to the same root error: its internal model of HTML disagreed with the browser's, and the disagreement was a hole.

**U1 — an unclosed `<style>` is read to end of page.** The gate extracted style blocks with `(.*?)</style>` — assuming every style section ends. The browser treats `<style>` as a raw-text element: no close tag means it reads to EOF. A page with a never-closed (or wrongly-closed, or self-closed) style block hid a white page the gate never read. Fix: `(.*?)(?:</style>|$)` — EOF is an implicit close, the way the browser reads it.

**D1 — an attribute is parsed by the spec's rules, not by regex intuition.** The gate's first-regex-match for `style` was fooled by a fake style instruction hidden inside another label (attribute confusion), feeding the checker the wrong answer so dark-on-dark text passed. Fix: parse the tag extent as real attributes (name, optional `=`, double/single-quoted or unquoted value) and return the first attribute named exactly `style`, case-insensitive — the HTML spec's first-wins rule. Bonus correctness: `data-style` is no longer misread as a style attribute.

The durable doctrine: **an HTML security check does not judge text — it judges what the browser will render. Any divergence between the checker's parse model and the browser's parse model is an exploitable gap by definition.** Regex-intuition about HTML is the divergence machine: it assumes closings exist, assumes quotes behave, assumes names can't hide in labels. The browser makes no such assumptions. Neither may the gate.

## 🩷 HUMAN NOTE

Shawn — the guard fell for two tricks with the same root cause: he wasn't reading the page the way the browser reads it. First, a style section with no ending — the guard assumed it must end somewhere, but the browser reads a style section until the end of the whole page, no ending needed. Second, a fake "style" label hiding inside another label — the guard's pattern-matching got confused about which label was the real one, and let invisible text through. Both fixes say the same thing: the guard must now read HTML the way the browser reads HTML — same rules, no shortcuts. Wherever the guard's version of the page differs from the browser's version of the page, that's where the next break-in happens.

## 👶 CHILD NOTE

Imagine a security guard who checks IDs at a door, but he thinks everyone enters through the front door. The building actually has a back door too — he just never looked at the building's map. Bad guys walk through the back door all day. The fix isn't a better lock on the front door — it's looking at the building's real map. The browser has a map of how it reads a page (what happens with a missing ending, what counts as a real label). The guard must use the browser's map, not his own guesses.

## 👵 GRANDMA NOTE

Sweetie, it's like reading a recipe out loud to someone cooking. If you read "salt" where the card says "sugar" — or you stop reading before the last line — the cake fails, even though the card was perfect. The guard was reading the page out loud to decide if it was safe, but he was reading it wrong: skipping lines the browser reads, hearing labels the browser doesn't hear. The rule from now on: he reads exactly the way the browser reads. Same words, same order, no improvising.

## 🤖 NAYA NOTE

When building or reviewing any HTML/CSS security check:

1. **Enumerate the browser's parse rules for every construct you inspect.** Raw-text elements (`<style>`, `<script>`) read to EOF on a missing close; attributes follow the spec's name/`=`/value grammar with first-wins; named entities decode before attribute termination. Each rule is a check-requirement.
2. **Never let a regex stand in for a grammar.** The failures were both regex-intuition bugs: `(.*?)</style>` assumed endings exist; `\\bstyle` matched `data-style`. Parse constructs with the grammar that produces them, not patterns that approximate them.
3. **Test with attacker-shaped malformation, not just well-formed pages.** The fixer fired the attacker's exact break-ins plus 21 nastier ones of their own: wrong closes, self-closing style, missing closes, attribute-confusion. Well-formed test pages can never falsify a parse-model divergence.
4. **One divergence is the rule, not the exception.** Two holes in one round, same root cause class. When one parse-model divergence surfaces, audit the whole construct family (SN-0390) — the next one is already hiding where the model and the browser disagree.

## 🧠 MACHINE NOTE

```json
{
  "sn": "SN-0812",
  "class": "ENGINEERING-PROOF",
  "subcategory": "INDEPENDENT-VERIFICATION",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-09",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "rule": "An HTML/CSS security check judges what the browser will render, not the source text: its parse model must match the browser's parse model exactly, because any divergence is an exploitable gap by definition. Regex-intuition about HTML is the divergence machine; parse constructs with the grammar that produces them.",
  "worked_example": {
    "U1": "inline_css (.*?)</style> -> (.*?)(?:</style>|$): raw-text elements read to EOF on missing close; wrong close (</styleX>) and self-close (<style/>) no longer end the read",
    "D1": "_style_attr_raw(): tag extent parsed as real attributes per HTML first-wins rule; fake style instructions in labels no longer feed the wrong answer; data-style no longer misread",
    "head": "naya5/ship-design-gate-repairs6 @ 5efc8515; 90 trip-wires green; master battery baselines exact",
    "board_comment": "#1354 6087497234"
  },
  "related": ["SN-0390", "SN-0719"]
}
```

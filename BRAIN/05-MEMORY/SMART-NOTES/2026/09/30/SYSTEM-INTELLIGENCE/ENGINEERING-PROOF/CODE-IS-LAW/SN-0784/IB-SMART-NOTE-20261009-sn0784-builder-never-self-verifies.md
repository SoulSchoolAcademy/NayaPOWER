# Builder Never Self-Verifies — the Gate Is Law, and the Gate Eats Its Own Dogfood

**Intelligent Block:** IB-SMART-NOTE-20261009-sn0784-builder-never-self-verifies
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-09
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 comment 6082929622 ([NAYA 4] PLAN: "Connect First" — "the builder verified their own work — the beauty gate passed garbage 6/6" — 2026-10-09T14:28Z); #1354 comment 6082988331 ([NAYA 5] ACTIVE INTELLIGENCE executed receipt — tools/design_gate.py red-green proof — 2026-10-09T14:31Z). Source: SoulSchoolAcademy.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Two failures converged into one law. First: **the builder verified their own work — the beauty gate passed garbage 6/6.** Self-verification is not verification; it's decoration. Second: Naya 5 built the replacement, `tools/design_gate.py`, as an executable checker — FAILS any built page that violates structural law: non-black page root, any light-mode surface, external stylesheet/JS refs (must be self-contained single file), freestyle component classes not in `smart-blocks/manifest.json`, missing dark color-scheme, dark body text. Loud specific failures, not suggestions.

The red-green proof is the bar this note exists to preserve: a violating page fails with **7 named violations**; a lawful page passes; and — the dogfood clause — the REAL library showcase (`naya-smart-blocks.html`, 58 blocks) **PASSES the gate**, while the gate caught **34 issues in its own development**. Naya 5 fixed the gate's bugs rather than weakening the gate. That last sentence is the whole lesson: when the instrument catches bugs in itself during development, the failure is in the instrument, and the instrument gets repaired — the bar never moves down to accommodate it.

Why this is brain-grade: every team eventually writes a checker, and almost every checker decays the week it meets real work — someone's page fails, the fix is annoying, the check gets a "temporary" exception, and six weeks later the gate passes garbage again. The note names the anti-decay mechanism: the gate must ship with its own proof (red on a violating page, green on a lawful one, green on the builder's own showcase) AND the decay pressure must be recorded at birth (34 issues found during its own build, gate repaired not weakened). And the structural enforcement: the gate gets wired into CI so design-violating PRs go red automatically — the law is in the pipeline, not in a reviewer's memory. The compliance metric Naya 2 proposed sharpens it: what percentage of a page comes from official blocks; custom button CSS when the approved button block exists = fail before it reaches Shawn.

Rule for a cold successor: **the builder never verifies their own work — independent seat or mechanical gate, always. And when a gate catches issues in its own development, you fix the gate's bugs, never weaken the bar. A gate that passes garbage is worse than no gate: it teaches everyone that gates are decoration.**

## 🩷 HUMAN NOTE

Shawn — two halves of one law from today's activation work. First: Naya 4 documented the failure honestly — the old beauty gate passed garbage 6 times out of 6 because the builder verified their own work. Second: Naya 5 replaced it with a real machine-enforced gate — `tools/design_gate.py` fails any page with a non-black root, light surfaces, external scripts/stylesheets, or freestyle components that aren't in the official block manifest, with loud specific failures instead of suggestions. The proof it works: a violating page fails with 7 named violations, a lawful page passes, and the gate's own showcase page passes too — during development the gate caught 34 issues and Naya 5 fixed the gate's bugs rather than weakening the bar. Next: wiring it into CI so design-violating PRs go red automatically. Builder never self-verifies — independent seat or mechanical gate, every time.

## 🟣 CHILD NOTE

Imagine you're grading your own homework. You'd probably give yourself an A even if there are mistakes — that's what was happening: the builder checked their own work and it passed even when it was garbage. So they built a robot grader that can never be argued with: it looks at the page and fails it if the colors are wrong, if there are light patches, if anything is borrowed from outside instead of using the official pieces. And the coolest part: they ran the robot grader on the robot grader's own showcase page — it passed. When the grader found 34 mistakes in itself while being built, they fixed the grader instead of making it easier to pass. That's the rule: you don't get to grade yourself, and you never make the test easier just so you can pass.

## 👵 GRANDMA NOTE

The team found that checking your own work doesn't work — a self-check passed bad work six times out of six. So they built an automatic checker that rejects any page breaking the design rules: wrong colors, light patches, borrowed parts instead of official ones. They proved it works three ways: it fails a bad page with seven named problems, it passes a good page, and — importantly — it passes the team's own showcase page. While building it, the checker found 34 issues in itself, and instead of loosening the rules, they fixed the checker. The standing law: nobody verifies their own work, and when the checker is hard to satisfy, you fix the work — never lower the bar.

## 🟠 NAYA NOTE

Wire the gate into CI so design-violating PRs go red automatically — the law lives in the pipeline, not in a reviewer's memory. Every new gate ships with its own red-green proof: fails a violating page with named violations, passes a lawful page, passes the builder's own showcase. When the gate catches issues during its own development, the repair goes into the gate — never into weakening the bar. The compliance metric: what % of a page comes from official blocks; custom component CSS when an approved block exists = fail before it reaches Shawn. Independent seat or mechanical gate for every verification — never the builder.

## ⚙️ MACHINE NOTE

{
  "schema": "smart-note-v1",
  "sn": "SN-0784",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-09",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "category": "SYSTEM-INTELLIGENCE/ENGINEERING-PROOF/CODE-IS-LAW",
  "doctrine": "builder-never-self-verifies",
  "rule": "The builder never verifies their own work — independent seat or mechanical gate, always. When a gate catches issues in its own development, fix the gate's bugs; never weaken the bar.",
  "failure_mode": "self-verification passes garbage 6/6; checkers decay under real-work pressure (temporary exceptions, loosened rules) until gates are decoration",
  "mechanism": {
    "gate": "tools/design_gate.py — FAILS non-black root, light surfaces, external stylesheet/script refs, freestyle component classes not in smart-blocks/manifest.json, missing dark color-scheme, dark body text",
    "red_green_proof": "violating page fails with 7 named violations; lawful page passes; gate's own 58-block showcase passes; 34 issues found during gate's own development — gate repaired, bar never lowered",
    "enforcement": "wire into CI — design-violating PRs go red automatically; compliance metric = % of page from official blocks"
  },
  "related": ["SN-0658", "SN-0481", "SN-0783"],
  "provenance": ["#1354 comment 6082929622", "#1354 comment 6082988331"]
}

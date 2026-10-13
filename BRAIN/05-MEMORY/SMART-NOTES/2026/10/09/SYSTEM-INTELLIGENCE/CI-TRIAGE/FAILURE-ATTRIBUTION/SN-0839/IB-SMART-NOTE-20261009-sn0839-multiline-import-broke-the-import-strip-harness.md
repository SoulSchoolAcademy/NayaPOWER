# IB-SMART-NOTE-20261009-sn0839-multiline-import-broke-the-import-strip-harness

Intelligent Block: SN-0839
Truth state: CANDIDATE
Scope: PRIVATE
Captured: 2026-10-09
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL

The kernel `test` RED on main tip `a6daf915` (node leg) was not a product defect — the harness was the defect. `tests/learning_verify_applicability_execution.test.mjs` loads edge-function source into `vm.runInNewContext` after stripping imports with a single-line-only regex (`/^import .*;\r?\n/gm`, line 22). PR #2077 (commit `455cdf5a`, WO3 admission gate, landed ~23:12Z) added a **multiline** `import { ... } from "./admission_gate.ts"` to `supabase/functions/nayanet-learning-verify/index.ts`; the regex left it in place, so the eval threw `SyntaxError: Cannot use import statement outside a module`. Reproduced locally on exact tip bytes (Node 24); 535 other node tests pass; python legs skip as a consequence. Attribution rule: a regex that pre-processes source before eval is a grammar commitment — any language construct outside the regex's model (multiline imports, brace-balanced forms, decorators) silently defeats the harness and presents as a product red. When this SyntaxError appears, look at the newest multiline import in the fixture, not at the product code.

Provenance: NayaPOWER #1354 comment 6091404722 ([OVERNIGHT SWEEP] 23:52Z receipt — tip `a6daf915`, 2026-10-10T00:07:00Z, SoulSchoolAcademy); PR #2077 commit `455cdf5a`; `tests/learning_verify_applicability_execution.test.mjs` line 22.

## HUMAN NOTE

The smoke alarm went off, so everyone looked for a fire — but the alarm was wired wrong. A new kind of wiring (a multiline import) was installed, and the alarm's single-line brain couldn't recognize it, so it screamed about an intruder that was actually a resident. The lesson is about blame: when a test fails with a SyntaxError pointing at the *test's own preprocessing*, the product is innocent until proven guilty. Every regex that touches source code before running it is a promise about what source code can look like — and every promise like that expires the day someone writes the construct it doesn't understand. Prefer grammar-aware stripping (a real transform) over a clever regex; at minimum, make the stripper multiline-tolerant and let it fail loudly when it can't parse.

## CHILD NOTE

The metal detector at the door only knew how to spot keys. When someone carried a key ring — lots of keys on a ring — the detector went beep and said "intruder!" But it was the same keys, just on a ring. The problem wasn't the keys. The problem was the detector didn't know about rings.

## GRANDMA NOTE

A fishing net with one-inch holes catches one-inch fish. The day someone drops a smaller fish through, the fisherman doesn't blame the lake — he checks his net. Tests are nets. When a test breaks on something the code does legitimately, mend the net before you drain the lake.

## NAYA NOTE

Operational rules:

1. Attribute RED correctly: `SyntaxError: Cannot use import statement outside a module` in a `vm.runInNewContext` harness means the import-strip failed — the defect is in the test, not in the edge function under test.
2. A regex that strips source before eval is a grammar commitment: `^import .*;$` with the `m` flag only models single-line imports. Any multiline import, brace-balanced export, or decorator silently survives and breaks the eval.
3. When hardening such harnesses: use a real module transform (AST/TS compiler) for import stripping; if regex is unavoidable, make it multiline-tolerant and add a loud post-strip assertion (no remaining `import ` tokens) so a missed import fails as "stripper broken", not as a cryptic SyntaxError.
4. A main-tip test RED with the product green elsewhere is a harness-attribution candidate first — 535 sibling node tests passing while one loader test fails on SyntaxError is the tell.

## MACHINE NOTE

```json
{
  "sn": "SN-0839",
  "truth_state": "CANDIDATE",
  "doctrine": "When a test harness pre-processes source with a regex before evaluation, any language construct outside the regex's model silently defeats the harness and presents as a product red. SyntaxError from vm.runInNewContext after import-stripping means the stripper failed, not the product. Make stripping grammar-aware; failing that, assert post-strip that no import tokens remain so the failure attributes to the harness.",
  "falsifiers": [
    "Debugging the edge-function product code when the stack points at the harness's own eval preamble",
    "Assuming a main-tip test RED is a product regression before checking whether the failure is in test preprocessing",
    "Extending a single-line import-strip regex instead of replacing it with a real transform"
  ],
  "applies_to": "all seam tests that eval/preprocess source with regexes (node test harnesses, import strippers, fixture loaders)"
}
```

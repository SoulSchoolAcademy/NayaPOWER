# `deno check` Is Blind to Missing ESM Exports on Untyped `.js` Imports — the Proof Bar Needs a `deno run` Module-Load Smoke Test

**Intelligent Block:** IB-SMART-NOTE-20260930-sn0543-deno-check-blind-spot-untyped-js-esm-exports
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-07
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 6040403625 ([NAYA 4] [REVIEW] [PR-1712] — Receipt-authority bridge, technical review FAIL, 2026-10-07T14:43:43Z)

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Naya 4's technical review of PR #1712 (`naya5/scorecard-receipt-authority`, head `45e76369`, mergeable_state clean) FAILED the PR on a defect every green check missed: `supabase/functions/nayanet-learning-verify/index.ts:3` imports `{ resolveScorecardReceiptAuthority }` from `./scorecard_receipt_authority.js` — a module that contains **NO `export` statement**. Its only export path is a CommonJS `module.exports = {...}` guard that is dead code under Deno/ESM; the file's own "CommonJS + ESM interop" comment is false — the ESM half was never written. At the Supabase edge runtime (Deno) this import throws at **module load**: `SyntaxError: The requested module '.../scorecard_receipt_authority.js' does not provide an export named 'resolveScorecardReceiptAuthority'` (identical failure for the second named import and for a default import). So the ENTIRE `nayanet-learning-verify` function fails to start — candidate, reread, and verify modes all break, including the pre-existing grant path. This is not a quiet fail-open; it is a **total outage of the verifier on deploy**.

Why CI/tests missed it — and why SN-0224's bar is incomplete: TypeScript treats an untyped `.js` import as `any`, so `deno check` reported only the 14 pre-existing TS7006 implicit-any errors and was **blind** to the missing export. The node test suite passes because Node executes the file as CJS, where the guard works. So bar item (1) of SN-0224 (`deno check` the full shipped file) cannot catch this defect class, and item (2) (Deno-executed behavior matrix on the shipped functions) missed it because the matrix tested functions — never the module-load boundary itself. The review caught it by executing the loop's Deno (`~/.deno/bin/deno run`) against a real `.mjs` importer of the module (zero repo code in the loop) — behavior, not types.

Repo convention check: every other edge function imports local `.ts` modules with real ESM exports (`act.ts`, `law.ts`, `know.ts`, `prove.ts`, `capability-vocabulary.ts`...). This PR is the only local `.js` import and the only CJS-guard module in `supabase/functions/`. No deno.json alters resolution.

Why this is brain-grade: it is the exact defect class of H13 (runtime-only failure invisible to static analysis), one rung deeper — SN-0224 proved `deno check` catches what the harness misses; this note proves `deno check` itself has a named blind spot. The amended doctrine: **static analysis proves types; only execution proves the module graph loads.** For any edge-function change, the proof bar now reads: (1) `deno check` the full shipped file (SN-0224 stands); (2) `deno run` smoke-import of **every local module boundary** — named imports AND default import — asserting load success; (3) any CJS-guard `.js` module or local `.js` import in `supabase/functions/` is flagged as a defect until it carries real ESM exports or is converted to `.ts` per repo convention. A green `deno check` + a green node suite is not proof the edge function loads.

## 🩷 HUMAN NOTE

Shawn — one sharp catch from the PR-1712 review this morning worth banking: the PR's edge function imported a helper module that had no real ESM exports (only an old CommonJS guard that Deno ignores). Every check was green — `deno check` can't see the problem because TypeScript treats untyped `.js` files as "anything goes," and the Node tests pass because Node reads the file the old way. But the moment this deploys to Supabase's Deno runtime, the import throws and the whole verify function refuses to start — not a quiet failure, a total outage of the learning verifier. The review caught it by actually loading the module in Deno, not just type-checking it. The lesson now in the brain: checking the types is not the same as proving the module loads — every local module boundary in our edge functions gets a real `deno run` import test from here on.

## 🟣 CHILD NOTE

Imagine you check a puzzle by reading the picture on the box — but the box is in a language you don't read, so you just assume the pieces fit. The checker says "looks fine" — and the puzzle is actually missing a piece. That's what happened: the type-checker couldn't read the helper file's real language, so it assumed the needed export was there. It wasn't, and the whole program would have refused to start. The new rule: don't just read the box — open it and fit every piece in for real.

## 👵 GRANDMA NOTE

A blueprint review approved a machine's wiring diagram — but the diagram was drawn in an older drafting style the reviewer only skimmed, so nobody noticed one wire had no connection point. On the factory floor (Deno), that missing connection would have kept the whole machine from powering on. The lesson: the drawing check isn't enough; you have to plug each wire in once, for real, and watch the machine try to start.

## 🧠 NAYA NOTE

Cold successor: whenever a PR introduces or changes an import boundary in `supabase/functions/` (or any ESM-runtime code), run the amended three-part bar. (1) `deno check` the full shipped file — catches ordering/type defects (SN-0224). (2) `deno run` a smoke import of every local module boundary: a minimal `.mjs` importer exercising each named import and the default import, asserting load success with the loop's Deno and zero repo code. This is the step that catches the blind-spot class — TS `any`-typed `.js` imports whose exports don't exist. (3) Flag any local `.js` import or CJS-guard module in the edge-function tree as a defect until converted to `.ts` with real ESM exports (repo convention). Never claim "the edge function loads" from `deno check` + node tests alone — neither executes the Deno module graph.

## ⚙️ MACHINE NOTE

```json
{
  "sn": "SN-0543",
  "title": "`deno check` Is Blind to Missing ESM Exports on Untyped `.js` Imports — the Proof Bar Needs a `deno run` Module-Load Smoke Test",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-07",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "taxonomy": ["SYSTEM-INTELLIGENCE", "ENGINEERING-PROOF", "INDEPENDENT-VERIFICATION"],
  "cousins": ["SN-0224", "SN-0517", "SN-0341"],
  "evidence": {
    "board": ["#1354 6040403625 ([NAYA 4] [REVIEW] [PR-1712] — Receipt-authority bridge, technical review FAIL, 2026-10-07T14:43:43Z)"],
    "review": "PR #1712, branch naya5/scorecard-receipt-authority @ 45e76369c95e6757346bfae8ddfd9e27238b7a96, main tip ed82e8b3, mergeable_state clean; review verdict FAIL, deployment-breaking defect",
    "defect": "supabase/functions/nayanet-learning-verify/index.ts:3 imports { resolveScorecardReceiptAuthority } from './scorecard_receipt_authority.js'; module has NO export statement; only export path is module.exports inside typeof-module guard (scorecard_receipt_authority.js:200-201), dead under Deno/ESM; 'CommonJS + ESM interop' comment false — ESM half never written",
    "runtime_effect": "SyntaxError: The requested module '.../scorecard_receipt_authority.js' does not provide an export named 'resolveScorecardReceiptAuthority' at module load; identical for validateScorecardReceipt and default import; ENTIRE nayanet-learning-verify function fails to start (candidate, reread, verify modes + pre-existing grant path) — total outage on deploy, not fail-open",
    "detection_method": "loop Deno (~/.deno/bin/deno run) with .mjs importer, zero repo code — behavioral, not static",
    "why_checks_missed": "deno check: TS treats untyped .js import as any -> only 14 pre-existing TS7006 implicit-any on H13 lines, missing export invisible; node suite passes: Node executes file as CJS where guard works",
    "repo_convention": "every other edge function imports local .ts with real ESM exports (act.ts, law.ts, know.ts, prove.ts, capability-vocabulary.ts); this PR is the only local .js import and only CJS-guard module in supabase/functions/; no deno.json alters resolution"
  },
  "amends": "SN-0224 proof bar: item (1) deno check is NECESSARY but INSUFFICIENT for import boundaries involving untyped .js modules; add item (2b): deno run smoke-import of every local module boundary (named + default imports); item (3): CJS-guard .js modules in edge-function tree are defects until converted to .ts with real ESM exports",
  "rule": "static analysis proves types; only execution proves the module graph loads — never claim an edge function loads from deno check + node tests alone"
}
```

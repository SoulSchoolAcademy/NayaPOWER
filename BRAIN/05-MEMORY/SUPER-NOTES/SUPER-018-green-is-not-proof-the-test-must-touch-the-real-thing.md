# SUPER NOTE — Green Is Not Proof — the Test Must Touch the Real Thing

> **The essence layer: 71 distilled Super Notes.** Raw Smart Notes live in the archive; the Hub wall shows these essences. Nothing here deletes or replaces any raw note.

| Field | Value |
|---|---|
| Super Note ID | `SUPER-018` |
| Hub wall row | `public.hub_smart_notes` ib_id `SUPER-018` |
| Human title | Green Is Not Proof — the Test Must Touch the Real Thing |
| Layer | ESSENCE — distilled from raw Smart Notes, never a raw capture |
| Distilled | 2026-10-21 — corrective distillation drive (639 raw → 71 essences); REPAIRED 2026-10-21 after independent audit found 42 MISSING + 151 PARTIAL — lost lessons restored from the originals (see REPAIR-LOG); coverage map regenerated mechanically from these files |
| Sources | 13 raw notes (full list below) |
| Cluster file | `cluster-02-super.json` |
| Canonical machine object | Hub DB row `public.hub_smart_notes` + `distill/all-super-notes.json` |
| Human projection | This Markdown file |
| Sync note | NOT ingested by hub-sync (its watcher parses only `BRAIN/05-MEMORY/SMART-NOTES`); archive + queue untouched |

---

## ✦ IN A NUTSHELL

A passing test only proves what it actually touched. Tests that read words instead of running the real thing, swap in pretend parts, or never exercise the new path will smile green while the real thing is broken.

---

## 🩷 HUMAN NOTE

Again and again, everything was green and the real thing was broken. Tests read the source text and declared victory without ever running it. A 'full system' test quietly swapped in a pretend part at the one joint that mattered. A proof run passed while never using the new feature it was meant to prove. One search claimed something was missing, but the search had never actually looked at the branch it claimed to check — and even a correct search earns only a lexical finding scoped to that search, never proof that a thing does not exist (sn067). Even a failing test once turned out to be the broken thing itself. The lesson: ask what the test physically did, not what it concluded.

---

## 🟣 CHILD NOTE

Saying 'I practiced piano' isn't playing the piano. A test that only looks at the sheet music never hears a wrong note. To know it works, you have to actually play it — the real song, on the real piano.

---

## 👵 GRANDMA NOTE

It's like tasting the soup instead of reading the recipe, dear. Reading tells you what should happen. Only the spoon tells you the truth. Make sure your checks actually touch the real thing, not a description of it.

---

## 🤖 NAYA NOTE

Naya asks of every green result: what did this actually execute? She insists tests run the real code path, with the real wiring, at full scope — including a run that loads and uses the thing, not just inspects it. She treats her own tests as suspects too: when a result looks wrong, she reproduces it one variable at a time and withdraws her own claim when the test was the artifact.

- Claiming a system uses its canonical engine takes three separate proofs, and no one of them stands in for the others: invocation (the real entry point is actually reached), consumption (substitute one documented consumed field in the engine's output and watch the result change), and enforcement (a violating input is refused, legibly, with a receipt) (sn073). A config-hash pin answers only "is the code I meant loaded?" — never "does the result depend on its output?" — and the receipt must carry every field recomputation needs (baseline_id, candidates, profile), or independent verification from the persisted record is impossible (sn073).
- An absence claim is only as sound as the search behind it: in git grep, the revision goes before --, because everything after -- is read as a file path, not a branch — a revision placed after it means the search never searched what it claimed (sn067). Never truncate the output when proving something is absent, and state the surviving claim as a lexical finding scoped to that search, never as proof the thing does not exist (sn067).

---

## WHAT IT MEANS

A test is a small experiment, and like any experiment it only speaks about what it actually did. Every shortcut — reading instead of running, substituting instead of integrating, checking presence instead of behavior — silently narrows the claim while the green checkmark stays the same size. The gap between the two is where failures hide.

---

## WHAT'S IN IT FOR YOU

Fewer nasty surprises. When your checks genuinely exercise the real thing, 'it passed' starts to mean 'it works' — and you stop shipping broken things wrapped in green reports.

---

## HOW IT APPLIES

Prefer tests that run the real behavior end-to-end over tests that inspect text or check that something merely exists. Include the failing case first, before the fix, so the green afterwards means something. When a check surprises you, suspect the check itself before believing either verdict.

---

## ⟲ RESTORED BY REPAIR — 2026-10-21

> Restored by the distillation repair after the independent essence audit (distillation-audit-20261021) found the lessons below MISSING from, or only partially carried by, this Super Note. Each entry restores the named source note's own rule in checkable words, traced to that source. Nothing here is new doctrine.

### SN-036 — Push-Run Evidence — Query the CI Event That Answers the Question [audit: MISSING → restored in full]

When you assert "exact-main CI is green/unknown," name the run event your evidence covers (push, pull_request, or workflow_dispatch). A wrapper that only reads scheduled or PR runs — and excludes push runs — manufactures uncertainty, or worse manufactures confidence, about the SHA that actually landed. In the source case, direct GitHub Actions push-run evidence closed the question for `a726a8376559609a3620f948ec7bfcabdba50abb` in one pass: Kernel Tests run 36812934009 (SUCCESS), Collective Chain Readiness run 36812933999 (SUCCESS), Promotion run 36812934028 (correct blocked/no-op). A workflow-level promotion "success" is a no-op receipt, not a deployment; the protected deploy remains NEEDS_AUTHORITY.

### SN-0506 — A Fixed-Page Tail of the Board Never Sees the Newest Claims [audit: MISSING → restored in full]

Paginated endpoints return the oldest items first (GitHub's issue-comments endpoint returns ascending ID order and silently ignores `sort`/`direction`), so a fixed-page tail never sees the newest claims: on a board with 350 ascending-ID comments, `fetch_board_tail(pages=2)` returns IDs 1..200 and reports "no collision" while an active claim sits at comment 350. A scanner must compute the last window from the live comment count (ceil(count/per_page)), validate its returned coverage against that count, and fail closed on inconsistent snapshots — prove the newest claim becomes COLLISION and malformed/moving snapshots stay UNKNOWN. A scanner that reports "no collision" without proving its window covers the newest comment is certifying fiction.

### SN-0543 — `deno check` Is Blind to Missing ESM Exports on Untyped `.js` Imports — the Proof Bar Needs a `deno run` Module-Load Smoke Test [audit: PARTIAL → lost element restored]

`deno check` is blind to missing ESM exports on untyped `.js` imports: TypeScript treats an untyped `.js` import as `any`, so a named import of a module with no `export` statement passes check. Node's CommonJS execution masks it further, because a `module.exports = {...}` guard works under Node/CJS but is dead code under Deno/ESM — at the edge runtime the import throws at module load (`SyntaxError: The requested module '.../scorecard_receipt_authority.js' does not provide an export named 'resolveScorecardReceiptAuthority'`), a total outage of the function. The proof bar therefore needs a `deno run` module-load smoke test: static checking plus node tests cannot prove an edge function loads. Static analysis proves types; only execution proves the module graph loads.

### SN-067 — The Git-Grep Pathspec Footgun — Revision After `--` Is a Path, Not a Revision, and Your Absence Proof Never Ran [audit: PARTIAL → lost element restored]

Revision before `--`, paths after `--`: anything after `--` is a pathspec, so `git grep ... -- '*.py' '*.ts' origin/main` treats `origin/main` as a file path and the search never searched the revision at all — an absence finding from it is void. Never truncate output when proving absence (truncated output cannot establish absence). Qualify any surviving absence claim as a lexical finding scoped to that search, never ontological proof. Correct by appending: retain the earlier evidence, withdraw the conclusion, and show the corrected run (revision before `--`).

### SN-073 — Invocation ≠ Consumption ≠ Enforcement — Proving the Runtime USES the Canonical Engine [audit: PARTIAL → lost element restored]

Claiming the runtime USES a canonical component requires three independent proofs: INVOCATION, CONSUMPTION, and ENFORCEMENT. Prove consumption by documented-field substitution — substitute one documented consumed field and the downstream result must change; a passing spy alone is a red flag, because invocation and config-hash checks look healthy while the engine's output is silently ignored. Prove enforcement by violating inputs with a legible refusal inside the receipt mechanism. Receipts must carry every recomputation field (`baseline_id`/`candidates`/`profile` in the source case); persistence completeness is a conformance criterion. A config-hash pin answers "is the intended code loaded," never "does the outcome depend on it."

### SN-077 — False-Green Restoration — Compute the Report from the Consuming State, Not the Reconstructed Local [audit: MISSING → restored in full]

Install-then-report: any restoration/acceptance signal — counts, hashes, receipts, verdicts — must be computed from the consuming object's own state after installation, never from the producer's intermediate local. The source defect: `cold_reconstruct()` built the recovered state into a local `fresh = KnowNode()`, computed a green report and matching hash from that local, and returned without ever installing the state onto `self` — the successor was empty and `retrieve()` returned nothing. Flag `fresh = X(); report(fresh); return` without assignment onto the delivered object as defect-shaped even when tests are green. The reproducer must assert on the successor's own `retrieve()` after `cold_reconstruct()` returns, on the same object — the function's report is the suspect, not the witness. Cold-successor continuity = "this object now carries the state and can serve it," not "state was reconstructed somewhere."

---

## SOURCES (traceability — every raw note this essence was distilled from)

- `IB-SMART-NOTE-20261006-sn0461-source-text-assertions-green-by-construction`
- `IB-SMART-NOTE-20261007-sn0569-regression-must-execute-embedded-artifact`
- `IB-SMART-NOTE-20260930-sn088-fixture-substitution-voids-integration-claims`
- `IB-SMART-NOTE-20260930-sn0567-green-proof-run-must-exercise-new-seam`
- `IB-SMART-NOTE-20260930-sn0543-deno-check-blind-spot-untyped-js-esm-exports`
- `IB-SMART-NOTE-20260930-sn0224-prove-the-shipped-artifact-at-full-scope`
- `IB-SMART-NOTE-20260930-sn073-invocation-consumption-enforcement`
- `IB-SMART-NOTE-20260930-sn077-false-green-restoration`
- `IB-SMART-NOTE-20260930-sn067-git-grep-pathspec-footgun`
- `IB-SMART-NOTE-20260930-sn0506-fixed-page-tail-blindness`
- `IB-SMART-NOTE-20260930-sn036-push-run-ci-evidence`
- `IB-SMART-NOTE-20260930-sn066-red-before-green-failing-case-first`
- `IB-SMART-NOTE-20260930-sn076-single-variable-defect-reproduction`

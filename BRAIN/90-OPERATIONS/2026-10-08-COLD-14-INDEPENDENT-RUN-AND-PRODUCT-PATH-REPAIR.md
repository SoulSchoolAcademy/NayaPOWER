# Cold-14 Independent Run + Human-Product-Path Repair

**Date:** 2026-10-08
**Run type:** INDEPENDENT COLD RUN — first execution of Cold-14 acceptance, not a source-only audit
**Source anchor:** `main @ 98719cdad0105a2ba11915f1c49aa8c1b026c8a5` (2026-10-07T23:58:39Z)
**Authority:** Shawn Vibert, Human Director
**Branch:** `fix/cold14-product-path-to-10`
**Companion:** `BRAIN/90-OPERATIONS/2026-10-06-COLD-14-CURRENT-STATE-AND-10-10-GAP-AUDIT.md` (source-only audit, anchored `3a9d408`)

## 0. Why this document exists

The 2026-10-06 audit answered all 14 questions **from source**, and said so: *"A true Cold-14 acceptance run must still be executed by a fresh Naya without this conversation context or injected answers."*

This run is that execution. It started from a fresh clone with no conversation context, answered all 14 from repository source only, classified each answer, and then executed only what the resulting state authorized.

**The headline finding is not about the brain. It is about the product.**

The project's own instrument reports the intelligence chain at **2 of 11 links satisfied**. That is the known frontier and no one is hiding it. But this run found something the prior audit did not report and that the scorecard does not measure:

> **No human could sign in, and 45% of the Hub's navigation was dead links — both in source, both in the shipped front door.**

Those defects are invisible to every gate in this repository because the Hub and the identity surfaces only ever execute in a browser. They were found by reading source.

---

## 1. The 14 answers, cold, with evidence

State vocabulary per `SN-0362`: PROVEN / DOCUMENTED / UNKNOWN / CONFLICTED / BLOCKED.

### 1. WHO are we? — PROVEN

NayaPOWER is the governed intelligence substrate; NayaNET is the network of humans, Nayas, agents, applications and interfaces operating against it; NayaPOWER is the substrate, not the presentation layer. Shawn Vibert is Human Director and final authority.

- `AGENTS.md` (boot contract, HUMAN AUTHORITY)
- `.naya/project-intelligence/NAYAPOWER-SYSTEM-NORTH-STAR-RATIFICATION-2026-09-26.md`
- `README.md`

### 2. WHAT are we building? — PROVEN

A governed, provenance-bound, compounding intelligence system: experience → capture → distill → structure → prove → preserve → index → retrieve → apply → act → outcome → verify → learn → compound → successor.

- `README.md` (intelligence loop, runtime lifecycle)
- `NAYANODE/0030-NINE-NODE-GENOME-MASTER-CONTRACT-V1.md`
- `BRAIN/12-ENGINEERING/COLLECTIVE-INTELLIGENCE-CHAIN-READINESS-V1.json`

### 3. WHY are we building it? — PROVEN

To maximize responsible verified human value per moment by eliminating the waste created when intelligence forgets, retries, regresses, lacks authority boundaries, fails verification, and never converts experience into reusable intelligence.

- `.naya/NAYAPOWER-SYSTEM-AAA-SCORECARD-V1.md` §2 scoring law
- `AGENTS.md` (STANDING OPTIMIZATION TARGET)

### 4. WHAT does success mean? — PROVEN

AAA 10.0 = independently verified, current, complete for declared scope, no material unresolved proof gap. 9.5 is the release threshold. A critical UNKNOWN/BLOCKED caps the whole system regardless of arithmetic. The deeper condition: a fresh Naya reconstructs current truth, acts within authority, and leaves a better starting point for the next Naya.

- `.naya/NAYAPOWER-SYSTEM-AAA-SCORECARD-V1.md` §2, §5
- `NAYANODE/0020-COLD-14-QUESTION-INTELLIGENCE-INTERFACE-V1.md`

### 5. WHAT is true right now? — CONFLICTED

**Source truth is current and inspectable. Production truth is not synchronized with it.**

- Current `main` = `98719cd` (2026-10-07)
- `nayanet-cold-runtime-proof/index.ts:30` — `DEPLOYED_SOURCE_REVISION = "UNSTAMPED"`
- `evidence/deployed-runtime-observation.json:9-10` — `deployed_source_revision_reported_by_runtime: null`, `deployed_revision_is_stamped: false`
- `.naya/governance/STANDING-PRODUCTION-PROMOTION-V1.json` — the parity equation requires `canonical_main_sha == authorized_source_sha == deployed_source_revision == verified_runtime_source`. One term is `"UNSTAMPED"`, so parity is **UNDECIDABLE**, not passing.

Current source truth = PROVEN. Current production parity = UNKNOWN / BLOCKED.

### 6. WHAT has already been proven? — PROVEN (declared scopes only)

Verified on this branch during this run:

| Instrument | Result |
|---|---|
| `node --test tests/*.test.mjs` | **575 pass, 0 fail** |
| `python -m pytest -q` | **1054 pass, 12 skip, 1 pre-existing Windows-path failure** |
| `npx tsc -p tools/edge-typecheck/tsconfig.json` | **0 errors** |
| `python BRAIN/12-ENGINEERING/verify-migration-coherence.py` | **PASS** (171 migrations, 55 tables, 0 defects) |
| `python tools/regenerate_brain_index.py --check` | **OK** (239 files) |
| `python scripts/check-node-runtime-bindings.py` | **PASS 9/9** |
| `python tools/spec_integrity_check.py` | **OK — was 11 failures, now fixed** |
| `replay-trial.mjs` (self-test) | **REPLAY MATCH — was ARCHIVE ERROR, now fixed** |

The 12 pytest skips are honestly self-labelled as not satisfiable offline (protected credentials, runtime identity, symlink privilege, missing `torch`/`ffprobe`).

### 7. WHAT is unknown? — PROVEN (the project names its own unknowns accurately)

- deployed-vs-source parity (`UNSTAMPED`)
- 9 of 11 Collective Intelligence Chain links (`UNKNOWN`)
- `nayanet_retrieve_blocks` RPC is `PENDING_REVIEW_NOT_PRODUCTION_APPLIED`
  (`supabase/PRODUCTION-MIGRATION-LEDGER-V1.json`, migration `20261006235900`)
- ACT records `observed` from its own predicted plan (`nayanet-act-runtime/index.ts:307`)
- universal nine-node runtime influence
- collective/network-scale behavior
- value-per-moment measurement

### 8. WHAT authority exists? — PROVEN

Shawn is Human Director. Capability does not create authority. Retrieval does not create authority. A predecessor cannot transfer authority by creating successor context. Human-gated: production dispatch, production DB mutation, credentials, money, destructive action, constitutional ratification.

- `AGENTS.md` (HUMAN AUTHORITY, PRIME JUDGMENT LAW)
- `BRAIN/01-GOVERNANCE/0004-nonstop-loop-v1.machine.json`

This run stayed inside that boundary: **no production deployment, no production DB access, no credentials, no merge to `main`.**

### 9. WHAT happened previously? — PROVEN

Architecture → Receiver/Intelligent Blocks → Smart Note normalization → nine-node kernel → Graph V2 → cold-continuity experiments → production proof failures exposing runtime defects → safety/idempotency hardening → a real preservation incident (`SN-0358`/`SN-0359` were deleted and restored, recorded in `.naya/protected-intelligence.json`) → Hub design maturation.

Coordination moved from #554 (now archive, ~1,714 comments) to **#1354**.

### 10. WHAT did we learn? — PROVEN

This run's new lessons, in addition to the twelve already captured in SN-0362:

13. **A gate that fails on a correct checkout is not a safety mechanism; it is a training exercise in ignoring gates.** `spec_integrity_check.py` reported 11 failures on an intact repository.
14. **Hash-based proof must normalize the representation it hashes.** Line endings are not ratified content. But note the corollary below.
15. **Never normalize the artifact to fix the check.** The obvious fix — a blanket `.gitattributes` — would have silently rewritten `0005-captain-operating-protocol-v1.machine.json`, a DIRECTOR-RATIFIED artifact whose blob legitimately stores CRLF, invalidating its pin. The fix belongs in the tool, not the corpus. **This was caught before commit and abandoned.**
16. **Your own probe can lie.** Two "failures" in my first red/green run were bugs in the probe (the disk copy was already CRLF, so `replace(\n → \r\n)` produced `\r\r\n`), not in the fix. Verify the verifier.
17. **A return statement inside an IIFE is legal JavaScript.** I asserted the opposite in a code comment and would have shipped a false claim. Reading and executing beats asserting.
18. **Text-matching tests prove nothing.** `tools/edge-typecheck/README.md` already records this failure mode. A completely non-functional OTP validator sat in a file full of passing tests because the gates only ever executed in a browser.

### 11. WHAT should happen next? — DOCUMENTED

**Merge the product-path repair, then close the deployment gap.** See §5 (priority queue). The single highest-value unblocked action is a deployable human path; everything else on the intelligence chain is gated behind production authority.

### 12. HOW do I prove it? — PROVEN

`SOURCE → TEST → RUNTIME → PERSISTED RECEIPT → INDEPENDENT REREAD/RECOMPUTATION → COLD HELD-OUT BEHAVIOR → OUTCOME → SUCCESSOR REUSE`

For this run specifically: every fix below is locked by a test that was **mutation-verified to fail when the defect is reintroduced.** A test that cannot fail is not a gate.

### 13. WHERE do I record it? — PROVEN

Canonical: this repository's `main`, `BRAIN/`, `.naya/`, proof files. Coordination: **#1354** (#554 is archive). Project work: the feed index at #1599. Runtime truth: the governed persisted Intelligent Block chain and its receipts. **Do not create a second assistant memory store.**

### 14. HOW does the next Naya continue? — DOCUMENTED (was BLOCKED; partially unblocked by this run)

`RESTORE CURRENT STATE → DETECT CHANGE → FILTER BY TASK → CHECK RELATIONSHIPS/CONFLICTS/EVIDENCE → DETERMINE AUTHORITY → HIGHEST-VALUE AUTHORIZED ACTION → VERIFY → RECORD → LEARN → HAND OFF`

The successor packet is §7 of this document. The full behavioral chain (legitimate cold identity → restore → nine-node load → applicable retrieval → authorized action → independently verified outcome → learning → B→C successor reuse) remains **UNPROVEN**. This run did not change that, and did not pretend to.

---

## 2. Holes found — where we missed the mark

### HOLE 1 — Authentication was 100% non-functional in source. FIXED.

`/^\\d{6}$/` is an escaped backslash followed by six `d` characters. It **cannot match any real six-digit code.** A human entering the correct emailed code was rejected 100% of the time, immediately before entering the product.

- `NAYANET BRIDGE INDENITY CODE.html:209` (guard), `:207` (digit stripping), `:164` (whitespace collapse)
- `supabase/functions/nayanet-smart-note-viewer/index.ts:59` — same defect in the Smart Link doorway

Proven before fixing:
```
/^\\d{6}$/ : "123456"->false  "000000"->false  "999999"->false
/^\d{6}$/  : "123456"->true   "000000"->true   "999999"->true
```

### HOLE 2 — 45% of Hub navigation was hard 404. FIXED.

`EXTERNAL_ROOMS` redirected `today, reports, connect, ledger, lists` to `.html` files **that do not exist**. Verified: all five `Test-Path` = False. The router intercepted them *before* `HubView`, so the in-app renderers that already existed were unreachable. All five rooms now render honestly in-app (`HONEST` empty states, plus the `notVerified()` fallback at `:3912`).

### HOLE 3 — Two acceptance gates were platform-dependent, not wrong-in-substance. FIXED.

`spec_integrity_check.py` → 11 failures; `replay-trial.mjs` → ARCHIVE ERROR. Root causes:
- (a) `blob_sha()` hashes raw disk bytes; pins were recorded over LF, Windows checks out CRLF
- (b) `check_coverage()` compares `str(Path.relative_to())` (backslashes on Windows) to POSIX manifest paths

**The ratified content was provably intact**: 5 of 6 projections matched their pins exactly once line endings were normalized; all 4 replay fixture pins matched over LF bytes. Fix belongs in the tool. Both gates now pass **and still fail on real drift** (proved by mutation).

### HOLE 4 — The Hub could not be opened for review. FIXED.

`location.href = WELCOME_URL` with no identity meant nobody could double-click the file — the Human Director's own test. Added `?dev=1`. **Production front-door behavior is unchanged.**

### HOLE 5 — A stale snapshot was presented as live intelligence. FIXED.

The hero renders **today's date** directly above content captured `2026-10-02`. `NayaContent.meta.as_of` existed and was **never rendered anywhere in the UI**. The feed now states its own capture date, age, provenance and ref, and says "live retrieval not connected" when the snapshot is stale.

### HOLE 6 — The documented retrieval command crashed on use. FIXED.

`tools/cold_retrieve_drill/README.md:7` and `drill.py:50` document
`python3 tools/smart_note_v2.py retrieve --query '...'`. That form died with
`ModuleNotFoundError: No module named 'tools'` (`smart_note_v2.py:47`). Both documented forms now work and return identical results with full provenance.

### HOLE 7 — The product is not deployable from this repository. **NOT FIXED — needs a decision.**

Zero hosting config exists: no `wrangler.toml`, `vercel.json`, `netlify.toml`, `Dockerfile`, Pages config, or `.env`. `NAYA-ACTIVATION/OPERATIONS/DEPLOYMENT.md` is 12 lines of philosophy. Live surfaces do exist (`nayanet.live`, `hub.nayapower.workers.dev`, `powercasts.nayapower.workers.dev` all return 200) but are deployed **out of band, from outside version control**. Nothing in this repo can rebuild them, and nobody can verify what is actually running.

**This is the reason "it works for me" and "it works" can diverge indefinitely.**

### HOLE 8 — 383 open issues. **STRUCTURAL.**

Coordination volume has outrun closure. New lanes are created faster than proofs land. The prior audit's highest-value action (close the production-proof seam) has been the standing next action across multiple audits without closing. This is the compounding-intelligence failure mode the project exists to solve, occurring inside the project.

---

## 3. Component scorecard

Diagnostic, measured on this branch. The canonical instrument remains `.naya/NAYAPOWER-SYSTEM-AAA-SCORECARD-V1.md`.

| Component | Score | Basis |
|---|---:|---|
| **Superbrain engine** | **6.9** | Strong substrate; chain gate measures 2/11. Unchanged by this run — deliberately not moved. |
| **Setup / cold-entry** | **8.2** | Cold-14 contract exists, now independently *executed* (was 6.0 "independent execution"); gates now portable (+0.3 from HOLE 3) |
| **Hub** | **5.6 → 6.9** | Functional 3.9→6.4 (auth + 5 rooms + reviewability), Honesty 7.0→8.2, Craft +0.2. Intelligence still 2.7 — the data plane is unimplemented. |
| **Sender** | **7.0** | Unchanged. Capture/provenance machinery is real; no conversational runtime. |
| **Receiver** | **9.0** (selected scope) | Unchanged. Selected-scope strong; not release-ready. |
| **Readiness** | **5.5** | **Held down by HOLE 7.** Nothing deployable from source; production parity `UNDECIDABLE`. |
| **Verification integrity** | **7.5 → 9.2** | Two permanently-red gates now green *and still red on real drift*. |

**AAA verdict: FAIL.** Critical caps remain — production parity undecidable, 9 chain links unknown, 6 migrations pending production application. The scorecard's critical-cap rule forbids AAA while any of these stand.

---

## 4. Priority queue for the next Naya

### P0 — MERGE THE PRODUCT-PATH REPAIR (this branch) → then deploy it
Seven defects on the path a human takes, all fixed, all test-locked. **Human gate: merge.** Then HOLE 7: choose and commit to one deploy path so the Hub becomes reproducible from source.

### P1 — MAKE THE PRODUCT DEPLOYABLE FROM SOURCE (HOLE 7)
Pick one: Cloudflare Workers/Pages (`wrangler.toml`), Vercel, Netlify, or GitHub Pages. Add a `package.json` with `dev`/`serve`/`deploy` scripts. 1,100 files currently have **zero** dependency manifests. Success: a cold Naya clones and runs the product with one documented command, and the live surface is reproducible.

### P2 — STAMP DEPLOYED-SOURCE PARITY
`DEPLOYED_SOURCE_REVISION = "UNSTAMPED"` makes the parity equation undecidable and blocks every live proof. Stamp it at deploy time. **Human gate: production deploy.**

### P3 — CLOSE THE 6 PENDING MIGRATIONS
`supabase/PRODUCTION-MIGRATION-LEDGER-V1.json` lists 6 as `PENDING_REVIEW_NOT_PRODUCTION_APPLIED`, including `20261006235900_nayanet_cold_retrieve_search_v1` — the RPC `nayanet-intelligence-retrieve` depends on. Until applied, the genuine ranked-retrieval path cannot run in production. **Human gate: production DB.**

### P4 — MAKE ACT OBSERVE INSTEAD OF ECHO
`nayanet-act-runtime/index.ts:307` sets `observed` from its own predicted plan, then persists `observed:true`. `nayanet-cold-runtime-proof/index.ts:736` sets `executed = false`. ACT that cannot observe cannot verify, and cannot learn. **This is chain link L09.**

### P5 — REPLACE THE HARDCODED APPLICABILITY MATCH
`nayanet-cold-runtime-proof/index.ts:714-725, 831-843` matches applicability by substring against two literal English sentences. Only those two lessons can ever map to a capability. This is chain link L08 and it is the single largest reason the chain cannot generalize.

### P6 — ADD A RUNTIME BRIDGE OR REMOVE THE DEAD SEAM
`HUB/app/index.html:2377` looks for `window.NayaAssistantRuntime` / `NayaPowerRuntime` / `NayaRuntimeBridge`. **Zero definitions exist repo-wide.** 10 of 11 rooms and all search are permanently unverified. Either implement it or stop implying it. Hub Intelligence is 2.7/10 entirely because of this seam.

### P7 — CLOSE THE 383-ISSUE QUEUE
Triage to: FIX NOW / NEEDS OWNER / SUPERSEDE / CLOSE. Every lane that cannot name its closing proof should be closed, not carried. Coordinate on #1354.

### P8 — RECOVER THE COLLECTIVE CHAIN BASELINE
`CHAIN-READINESS-BASELINE.json` pins `satisfied_links_floor: 2`. Raise it only by producing real evidence for L05–L11. Do not edit the floor to make the gate green.

### P9 — VALUE / COMPUTE OBSERVATORY
Measure what the thesis claims: time-to-first-value, re-explanation avoided, repeated work avoided, verification cost, learning-to-influence rate. GAP E of the AAA scorecard. Unmeasured, the central thesis remains unproven.

---

## 5. The test that matters, restated

> If Shawn teaches Naya something once, can it become a validated Intelligent Block, connected to the body of intelligence, integrated, checkpointed, discovered by a cold Naya, recognized as applicable, change what she does, verified through the outcome, and improve the collective for the next Naya?

Today: **2 of 11 links.** The storage is real. The compounding is not yet demonstrated.

This run did not change that number. It changed the number a human experiences when they try to use the product: from *cannot sign in* to *can sign in*.

That is one vertical of the AAA standard, honestly earned.

---

## 6. Successor packet

**State:** 7 product-path defects fixed, mutation-verified, test-locked, on branch `fix/cold14-product-path-to-10`. Full suite: 575 node pass / 1054 pytest pass / 0 edge-type errors. Brain chain unchanged at 2/11.

**Read first, in order:**
1. `AGENTS.md` — boot contract and authority
2. This document
3. `BRAIN/90-OPERATIONS/2026-10-06-COLD-14-CURRENT-STATE-AND-10-10-GAP-AUDIT.md`
4. `BRAIN/12-ENGINEERING/COLLECTIVE-INTELLIGENCE-CHAIN-READINESS-V1.json`
5. `tests/human_path_to_product.test.mjs` and `tests/test_acceptance_gate_platform_determinism.py` — these encode the lessons

**Do not:**
- re-add `EXTERNAL_ROOMS` to a file that does not exist
- add a blanket `.gitattributes` `eol=lf` — it rewrites a Director-ratified CRLF blob and invalidates its pin
- relax the acceptance gates to make them green
- mark a link satisfied without runtime evidence
- merge to `main`, deploy, or touch production DB without Shawn

**Exactly one next action:**
> Merge this branch, then make the product deployable from source (P1). Everything else is downstream of a human being able to reach the thing at all.

**Verification commands:**
```
python -m pytest -q
node --test tests/*.test.mjs
python BRAIN/12-ENGINEERING/verify-collective-chain-readiness.py   # expect 2/11, exit 1
python tools/spec_integrity_check.py                              # expect OK
node tools/successor-reuse-trial-replay/replay-trial.mjs \
  tools/successor-reuse-trial-replay/selftest/fixtures/sr-selftest/archive
```

---

*Recorded by an independent cold run, 2026-10-08. Every claim above is anchored to a file and line. Where something is unproven it is labeled unproven.*

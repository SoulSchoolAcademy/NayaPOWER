# REPAIR LOG — the 639 → 71 distillation, repaired (2026-10-21)

**What this is:** the complete, traced record of the repair that folded everything the independent
audit found missing or thinned back into the 71 Super Notes, from the restored originals.
**Prepared as working files only** — a detached worktree at the restore commit; no pushes, no PRs,
no posts. The main seat lands this through the normal merge protocol.
**Worktree:** `hidden_files/distillation-repair/` at commit `7945d0e3a77b6bca262b43b787973858826f6fd6`
(raw notes restored; Super Notes as landed in `997ad755071067a0e02b14290d012c057eb1adec`).

**Evidence base:** `hidden_files/distillation-audit-20261021.md` (the independent audit) and its
machine-readable rows (`distillation-audit/results/all-rows.json`, 638 judged notes).
**Standard drafted alongside:** `DISTILLATION-STANDARD.md` (repair root) — the rules that make a
distillation "done right"; placement in the repo is the landing seat's call.

---

## Counts (derived, not asserted)

| Measure | Count |
|---|---|
| Audit MISSING lessons folded into their Super Notes | **42 / 42** |
| Audit PARTIAL lost elements restored | **151 / 151** |
| Items NOT restored | **0** |
| Restored entries present in files (machine-counted `### … [audit: …]` headings) | **193 / 193** |
| Super Notes carrying a `## ⟲ RESTORED BY REPAIR — 2026-10-21` section | 57 (the other 14 had no audit items) |
| Files changed in `BRAIN/05-MEMORY/SUPER-NOTES/` | 73 (71 Super Notes + README + coverage-map.json) |
| Diff | 73 files, +2,772 / −214 lines (incl. regenerated coverage map) |
| Source (raw) note files modified | **0** — originals untouched |

## How the repair was built

1. **Packets.** `build-packets.py` derived one repair packet per lane from the audit's own rows:
   for every MISSING/PARTIAL source — its SN id, stem, audit-assigned Super Note, the audit's exact
   "lost" statement, and the source's extracted nutshell/rule + path. 193 items, 0 unresolved targets
   after the two repair-chosen assignments below.
2. **Nine repair lanes** (SUPER-001–009 …, split at SUPER-061) each read the actual source note
   files and edited only their own Super Notes. Every restoration sits in a clearly marked
   `## ⟲ RESTORED BY REPAIR — 2026-10-21` section immediately before the SOURCES list, one
   `### SN-… [audit: MISSING → restored in full]` or `[audit: PARTIAL → lost element restored]`
   entry per source, carrying the source's own rule in checkable words — named specifics
   (thresholds, step lists, field names, counts) preserved. Voice sections and original essence
   text were not rewritten.
3. **Mechanical post-pass.** `generate-map.py` (never the lanes' word): recounted every Super
   Note's `| Sources |` header from its own SOURCES list; replaced the false "exact partition,
   639/639 covered" Distilled line in all 71 files; removed SUPER-071's duplicate short-form
   SN-0808 citation line (the full stem was already cited); regenerated `coverage-map.json`
   **by parsing the repaired files**; and wrote `coverage-map.verification.json` with the
   provenance checks and per-entry substance scores.

## Citation repairs (provenance)

- **Added:** SN-275 → SUPER-014 and SN-012 → SUPER-068 (both were cited nowhere).
  *Repair-chosen targets, recorded:* SN-275 (consent granularity) → SUPER-014, whose cluster holds
  the connecting agreements (identity private by default, wisdom to the collective). SN-012 (the
  operating model) → SUPER-068, the architectural-truth cluster (one organism, one brain, many
  doors). Both restorations are in place and their entries carry the full lessons.
- **Removed (phantom citations):** `IB-SMART-NOTE-20261019-sn0798-the-intelligent-system` from
  SUPER-061 and `IB-SMART-NOTE-20261019-sn0799-compose-dont-recreate` from SUPER-062. Neither note
  exists anywhere in the repo tree (audit whole-tree verified). They are **not silently dropped**:
  both are recorded in `coverage-map.verification.json` as pre-existing Hub-DB-only claims.
- **Fixed (truncated strings):** SN-0496 citation in SUPER-063 and SN-0497 citation in SUPER-023
  completed to their full stems.
- **Removed (duplicate short form):** `- \`SN-0808-the-elevation-standard\`` in SUPER-071; the full
  stem `IB-SMART-NOTE-20261021-sn0808-the-elevation-standard` was already cited. (The packet's
  suggested 20261007-dated stem matches no file on disk — the lane correctly refused to invent it.)
- **README corrected:** the directory README's "exact partition, 0 missing / 0 foreign /
  0 duplicates" claim replaced with the audited truth and a pointer to the generated map.

## Generated coverage map — verification results

From `coverage-map.verification.json` (parsed from the repaired files):

- **Citations: 638** across 71 Super Notes (original map claimed 639 strings, of which 2 were
  phantoms and 2 truncated).
- **Phantom citations: 0. Duplicate citations: 0.**
- **Uncited sources: 1** — `IB-SMART-NOTE-20261001-hub-is-intelligence-projection-dup0594`, the
  SN-0594 **tombstone**: an intentionally content-free "superseded" marker whose canonical twin is
  cited and covered under SUPER-071. It carries no lesson, so it is named in the verification file
  rather than force-cited. (It was uncited in the original map too — the original's arithmetic
  balanced only because the phantom citations padded it.)

## Honest limits (read before landing)

1. **This repair is not self-certified.** Per the standard (§3), semantic completeness stands only
   when an **independent re-audit by a different seat** re-judges the repaired essences against the
   sources and returns LOSSLESS. Until then, no deletion of the raw notes qualifies — the originals
   stay archived as ore.
2. **Mechanical substance floor:** the generator scored each restored entry's token overlap
   against its source's nutshell+rule+audit text. **65 of 193 entries score below the 0.35 floor.**
   That metric divides by the union vocabulary of three texts, so a tight PARTIAL restoration
   scores low by construction; it is a flag, not a verdict. The five lowest (SN-0367 0.176,
   SN-090 0.196, SN-0342 0.204, SN-0348 0.208, SN-0409/0519 0.212) and the only sub-floor MISSING
   entry (SN-0199, 0.252) were hand-read against the audit's lost statements during this repair —
   **all carry the named element in checkable words** (e.g. SN-090's entry states the family-binding
   rule verbatim with its 14/14 example; SN-0199's entry carries declare-parents + subordination +
   no-invented-rules + shadow canon). The re-audit should still sample the flagged 65 first.
3. **Cosmetic:** three entry headings carry the source title's own embedded id, doubling it
   (e.g. `### SN-0424 — SN-0424 — Registry Metadata…`, SN-0409, SN-0581) — faithful to the source
   titles; dedupe at landing if desired, no substance involved.
4. **Audit keying quirk:** SUPER-007's restored entry is keyed `SN-0177` but carries the
   SN-01774 execution-doctrine note — the audit's own row keying, preserved so the repair traces
   1:1 against the audit. The second SN-0177 (finish-before-create, SUPER-062) is restored
   separately under its own stem.
5. The `Distilled` header line and `| Sources |` counts are the only header fields changed;
   `cluster_file`, Hub row references, and all voice sections are byte-identical to the landed
   versions apart from the restored sections themselves.

## What remains for the landing seat

1. PR the worktree diff (71 Super Notes + README + coverage-map.json + the new
   coverage-map.verification.json; place DISTILLATION-STANDARD.md canonically).
2. Commission the independent re-audit (different seat, strict standard, flagged-65 first).
3. Only on a LOSSLESS re-audit verdict may a deletion of raw notes be proposed — as its own gated
   PR under the standard §4. **This repair proposes no deletion.**

---

## Per-change trace — every restoration, by lane (verbatim lane records)

Assembled from `traces/batch-*.md` in this worktree. Format: `SN | SUPER | RESTORED | what was restored`.

### Lane batch-1

```
SN-0215 | SUPER-001 | RESTORED | Policy must authenticate its own terms from its own canonical record (never caller-supplied assertions); protected paths incl. `.naya/governance/` structurally unpromotable without a human
SN-0263 | SUPER-001 | RESTORED | Ratification ritual restored: exact SHA-naming authorization string, independent verification of every claim before execution, receipt recording both what it authorizes and what it does NOT; RATIFIED ≠ MERGED ≠ RUNTIME_ACTIVE ≠ BEHAVIORALLY_PROVEN ≠ PRODUCTION_PROVEN
SN-0362 | SUPER-001 | RESTORED | A hash binds content, never identity: a validly hashed promotion receipt proving what/why but never who was entitled is an unkeyed seal; promotion must bind to an authenticated grant
SN-0368 | SUPER-001 | RESTORED | Full restore: a passing audit attests only internal coherence of the promoter-supplied evidence bundle, never truth; gatherer_independence measures string diversity, not corroboration, and must never be cited as independent confirmation
SN-0464 | SUPER-001 | RESTORED | A non-blank promoter name-check proves only a claim was recorded, not entitlement; the elevation guard must bind the promoter to an entitlement source and fail closed when the binding is absent
SN-0581 | SUPER-001 | RESTORED | Specific mechanism restored: new notes always enter as CANDIDATE and truth-state changes require ratification evidence, enforced in code (tools/smart_note_v2.py, tools/truth_state_guard.py), not convention
SN-0191 | SUPER-002 | RESTORED | Freeze-point demo protocol restored: pushed commit is the freeze point, the director views that frozen SHA, nothing shown outside GitHub that is not pushed (no side copies/mockups), and the judge scores the same SHA the director viewed
SN-0328 | SUPER-002 | RESTORED | A merge produces a new tree so pre-merge evidence does not transfer; the auto-merge gate must re-run derived-layer checks (index --check, ledger, caches) on the exact merge commit
SN-0415 | SUPER-002 | RESTORED | HOLD MAIN must precede the authorization request (freeze is the first step of the deploy sequence); any main movement between authorization and dispatch acceptance voids the SHA-pinned authorization
SN-0553 | SUPER-002 | RESTORED | Overtaken-receipt correction must quote the overtaken receipt, disclaim authorship of the action another hand completed, and reclassify it as a post-hoc record that must never stand as authorization; a merge recorded under an account does not establish which interaction caused it
SN-0563 | SUPER-002 | RESTORED | A merge is proven only by ancestry of the merge commit inside refs/heads/main (merge-base --is-ancestor), never by PR head SHA equality or PR state labels; receipts record the merge commit, never the head
SN-0175 | SUPER-003 | RESTORED | An endorsement binds only the endorser's own live venue re-read (quoting the claimant adds no confirmation weight); every correction receipt must split VERIFIED (re-read live) from WITNESSED (originating lane's findings, not adopted)
SN-0354 | SUPER-003 | RESTORED | When the verification wall is real, accept it: name every ruled-out cause, name the residue without inventing causes, park the lane, and name the exact awaited decision and its owner; UNKNOWN is a complete state when named, evidenced and parked
SN-0371 | SUPER-003 | RESTORED | Full restore: before adopting a design that depends on a gate, sample the gate's actual behavior on live state in the exact configuration needed; a fail-closed gate that can never complete is a functional regression, not a fix; offer the honest weaker interim without presenting it as the spec
SN-0451 | SUPER-003 | RESTORED | Audit the ratified authority text itself and never trust memory's path claim for where it lives; the authority document must be located on the exact SHA being audited
SN-0520 | SUPER-003 | RESTORED | The ledger tracks migration history, not table existence (a DROP outside the migration system is invisible to it); every architecture move must repoint every deployed consumer; tests that mock the row hide the break, so CI green never proves the table exists
SN-0624 | SUPER-003 | RESTORED | A quarantine snapshot is a point-in-time triage request, not a verdict: reconstruct the collision registry from live bytes at pinned SHAs before triaging, or already-resolved collisions get acted on and invent damage
SN-560 | SUPER-003 | RESTORED | A PR's stated gate is a claim about governance, not governance: re-verify the current ratified governance boundary at action time and the stale narrative loses to ratified law
SN-0115 | SUPER-004 | RESTORED | Numbering disputes are resolved by creation-time chronology (commit/PR creation timestamps, not announcement order); renumbering is always the colliding lane's own call and the winner does not dictate it
SN-0176 | SUPER-004 | RESTORED | Same number + same bytes in another partition is a harmless re-stage; same number + different bytes is a content fork and a registry collision, never a revision or second edition
SN-0347 | SUPER-004 | RESTORED | Full restore: restating doctrine already in an existing Smart Note is not a new capture — encode against the existing note (bind new work to it, reference it) instead of staging a duplicate that splits provenance and confuses retrieval
SN-0467 | SUPER-004 | RESTORED | When the counter file and the branch claim-tree disagree on the next number, the branch tree is the authority and the counter only advisory; the staging path must scan the tree and refuse a taken number (exit 2) with the next-free suggestion
```

### Lane batch-2

```
SN-0117 | SUPER-005 | RESTORED | Fold-in named keepers (SPEC/VIOLATION/TEST per rule, concept-hex registry, Smart-Connect-not-Share, shell-layer-count reconciliation) and each lane closes only its own PR after verifying its content landed
SN-0159 | SUPER-005 | RESTORED | One owner artifact per architectural question assigned before multi-lane work; inputs FOLD into it with a receipt then are SUPERSEDED; an input surviving past fold-in is a parallel system to retire
SN-0201 | SUPER-005 | RESTORED | One open repair per RED class: re-point the existing repair to current main, re-verify on exact new bytes, disclose any tip move with an explicit materiality argument
SN-0336 | SUPER-005 | RESTORED | Published intent-to-merge scorecard before merging (tested head bytes, current base, strongest alternative, falsifier stated beforehand, reversibility), deconfliction re-fetch, and post-merge battery on the new tip before stacking anything
SN-0367 | SUPER-005 | RESTORED | Third-seat arbiter flags the collision with byte-level evidence and touches neither PR; choosing between two other lanes' work is not the arbiter's call
SN-0393 | SUPER-005 | RESTORED | Green is merge-eligible not merge-mandatory: hold a ready PR that would stale another lane's in-flight promotion pin on an exact SHA, with a named resume condition and immediate action when it clears
SN-0153 | SUPER-006 | RESTORED | Delta ledger every iteration (gap removed / evidence improved / unchanged), one major variable at a time, and ~10 rounds without closure triggers contract re-examination not more rounds
SN-0264 | SUPER-006 | RESTORED | The 10/10 bar defined (diligence, everything measured, mathematically sound and logically sensible, multiple perspectives) plus the sting clause: proactive surfacing of the unasked thing is part of the standard, not extra credit
SN-0265 | SUPER-006 | RESTORED | The seven-step law for every seat (Score → Classify → Fix the Canonical Seam → Verify → Re-score → Converge → Torch), its four prohibitions, and the critical-cap rule (one unclosed critical hole caps the whole organism score)
SN-0340 | SUPER-006 | RESTORED | Act only when the winning option is reversible, causes no major damage and moves us forward; auto-merge is authorized under the scorecard protocol but is not a blank check — no scorecard, no merge
SN-0343 | SUPER-006 | RESTORED | The full ten-area scorecard: ten named areas with priority weights and honest scores (weighted total 6.8/10), one highest-value action each, re-run on evidence, weights change only on the director's word
SN-0456 | SUPER-006 | RESTORED | 9.0+ on an honest scorecard is auto-approved and must not be asked about (9.5 preferred, 10 the goal), plus the visual-proof standard (clickable link; nothing below 9.0 shown to him) and the minimal-PM rule
SN-0590 | SUPER-006 | RESTORED | A ratified standing protocol outranks a stale hold in a PR body; hold language is in-band metadata, and when they disagree the question is whether any human gate actually applies to that action class
SN-0177 | SUPER-007 | RESTORED | Evidence ladder never collapsed (Documented → Implemented → Tested → Verified → Production-Proven), exactly one executable next action (what/where/evidence/success condition) with full-state handoff at every stop, and maximum responsible verified human value per unit of complexity
SN-0279 | SUPER-007 | RESTORED | Quality ladder (<9.0 unacceptable, 9.0–9.49 birth threshold, 9.5–9.99 AAA, 10 exceptional, do not manufacture a 10), evidence distinctions (unknown must be measured; implemented ≠ verified; live ≠ independently proven), calculate what can be quantified and adopt demonstrably superior existing solutions
SN-0358 | SUPER-007 | RESTORED | Optimization function max(Verified Human Value / Time) constrained by Proof, Provenance and Continuity, and law-is-code self-directed collective intelligence bound strictly by law, proof and continuity
SN-0606 | SUPER-007 | RESTORED | Never-break laws beyond human gates: never duplicate another lane's work (check claims first), evidence law (unknown ≠ pass, implemented ≠ verified, verified ≠ production-proven), own misses openly, no merge without a scorecard receipt
SN-0414 | SUPER-008 | RESTORED | Migration is monotonic by default: the migration writer preserves unknown-to-it governed fields automatically instead of re-deriving from a fixed field list, so removal is never a side effect of a schema change
SN-0460 | SUPER-008 | RESTORED | Only VERIFIED may move to RATIFIED with a valid elevation grant; direct CANDIDATE→RATIFIED or TESTING→RATIFIED jumps are rejected before authority and evidence are considered
SN-0468 | SUPER-008 | RESTORED | A verification gate whose instrument is unavailable must FAIL, never skip, and a gate's teeth must be proven with mutants before the gate is trusted
SN-0503 | SUPER-008 | RESTORED | The blind spot was the human director's own direct commits, covered by no seat-focused rule; close the path (automatic step on any covered change, or check moved pre-merge) rather than patch the human's memory
SN-0611 | SUPER-008 | RESTORED | Trigger functions never need EXECUTE grants (triggers fire regardless), so revoke EXECUTE from anon, authenticated and PUBLIC, and audit every returns-trigger function in the public schema for this exposure
Citation directives applied: none — packets/batch-2.json contains an empty citation_directives list.
```

### Lane batch-3

```
SN-0199 | SUPER-009 | RESTORED | Personal oath rule restored in full: declare parents + subordination to canon, invent no new rules — derived obedience, never parallel authority; inventing oath = shadow canon
SN-0261 | SUPER-009 | RESTORED | Law/document separate lifecycles restored in full: ratification blesses the enforcement point not the prose; SN-036 stayed CANDIDATE 8.5/10 iterating to 10/10, with the gate's --delivery-text Smart Link check and its FAIL / refused-delivery specifics
SN-0262 | SUPER-009 | RESTORED | Candidate bytes may be validated/compiled/tested/explained but never govern; activation requires all conditions together (exact-version ratification, receipt, RATIFIED_ACTIVE, ratified=true, runtime_enabled=true, reconciled pins, gates PASS); flipping runtime_enabled alone refused
SN-0324 | SUPER-009 | RESTORED | Verbal decision authorizes the single act only, does not mean the machine enforces the law, must never be cited as proof of autonomous machine action; adversarial review belongs in the draft law's PR before it hardens
SN-0116 | SUPER-010 | RESTORED | Owning lane makes the canon call with an explicit board-visible scorecard, and an owner call is not the lock — consensus scorecards and Shawn's merge word still govern
SN-0370 | SUPER-010 | RESTORED | R2 repair class: preserve R1 bytes with SUPERSEDED label in lifecycle metadata only, issue R2 with fresh event identity + stable human ID + machine-resolvable SUPERSEDES edge, retrieval refuses SUPERSEDED, conformance fails closed without a real successor
SN-0325 | SUPER-011 | RESTORED | CANDIDATE merge rule: disclosed unknown labeled in the note + no irreversible change on merge = safe to merge; disclosure is a qualification not a blocker, judged by the two-question admission test
SN-0409 | SUPER-011 | RESTORED | When provenance on a shared identity is ambiguous, hold the decision and escalate to the human director; never infer authorization from authorship
SN-0455 | SUPER-011 | RESTORED | Security evidence restored: 27 warnings, zero errors, unauthenticated SECURITY DEFINER function nayanet_execution_receipt_to_smart_ledger(), 18 anonymously readable public tables, 7 signed-in SECURITY DEFINER functions, disabled compromised-password protection; classify intentional-vs-hole before any fix plan
SN-0603 | SUPER-011 | RESTORED | Canary protocol: plant a novel decision-changing rule, run a no-rule control through the real pipeline first, then require a cold consumer to retrieve the rule via the normal KNOW path and decide differently, falsifier declared up front; a falsifier killing your own design / a control falsifying your assumed mechanism is the experiment working
SN-0637 | SUPER-011 | RESTORED | Local/offline verifier's green proves only local code behavior, never deployed enforcement, actual reading, comprehension, or repository integration
SN-099 | SUPER-011 | RESTORED | Promise-gate machinery: write NOT READY TO PROMISE PUBLICLY YET with enumerated gaps and the DOCUMENTED / ARCHITECTURALLY ALIGNED / IMPLEMENTATION-PARTIAL / NOT PRODUCTION-PROVEN stamp into the canonical record, name the two-owner adversarial acceptance proof as the gate, and the isolation law that DNA is inheritable but private state never is
SN-0170 | SUPER-012 | RESTORED | Scope-blocked delivery protocol restored in full: a 403 is terminal evidence of an authority boundary (never retry/route around/soften), publish the artifact to the board with exact placement and provenance, delete stray mechanism state, name the completing seat
SN-0403 | SUPER-012 | RESTORED | Idea Evolution Flow restored in full: SOURCE → DISTILL → ENHANCE → RECONCILE → CLASSIFY → SMART LINK → BACKLOG → #1354 → BUILD/VERIFY WHEN PRIORITIZED → LEARN, preserving the original idea so ideas compound like intelligence
SN-0488 | SUPER-012 | RESTORED | Specialist relay discipline restored in full: relay acknowledges all specialist traffic but claims nothing and defers, unclaimed flags route to the lane owner or main seat, a relay never silently absorbs another lane's flag
SN-0576 | SUPER-012 | RESTORED | Area-agent staffing law: nine dedicated teams, one per scorecard area, working 24/7 until 10/10, and area agents never merge, deploy, ratify, or touch production
SN-0239 | SUPER-014 | RESTORED | Two lost connecting agreements restored: connect/share/chat with like minds only if you choose (opt-in only), and daily, weekly and monthly intelligence reports appear in the feed and the system
SN-275 | SUPER-014 | RESTORED | Consent-granularity ruling restored in full: entry consent at the activation boundary satisfies "collective by consent" (Law 43) for distilled, anonymized wisdom; identity and non-wisdom personal material stay private-by-default; per-block consent is a fallback, not the default
CITATION | SUPER-014 | APPLIED | Added source stem `IB-SMART-NOTE-20260930-sn275-consent-granularity` to SUPER-014's SOURCES bullet list per citation_directive (SN-275 was never cited anywhere)
```

### Lane batch-4

```
SN-0172 | SUPER-015 | RESTORED | Temporal rule restored: never write a done record before its evidence window closes, a timestamp preceding its evidence is a false receipt, and on catching one re-run for real, replace the record and log the correction, never edit numbers in place
SN-0188 | SUPER-015 | RESTORED | Search index as lagging projection for discovery only; content claims verified against live file bytes at the ref, with staleness named on disagreement
SN-0216 | SUPER-015 | RESTORED | Verifier recomputes a repair claim against the live target tree, never the PR's own blobs, and proves the checker non-vacuous by its red on the broken tip
SN-0238 | SUPER-015 | RESTORED | Recompute expected index from live tree at pinned commit, enumerate self-referential files as explicit exclusions by design, and show the check fails without the repair
SN-0250 | SUPER-015 | RESTORED | Permanent gate must assert disk↔registry hash reconciliation and registry-wide ID uniqueness every run; a green run proves only that run's conformance
SN-0384 | SUPER-015 | RESTORED | Full rule restored: success check must assert the semantic requirement (parse body, require valid JSON before breaking retry), never a proxy such as file size or HTTP 200
SN-0424 | SUPER-015 | RESTORED | Registry hash hit earns only a mandatory runtime reread, and a heal is proven by its failure shape — the known-bad case failing in the named REGISTRY_RUNTIME_CONTENT_DRIFT class with no mutation on verify-only drift
SN-0533 | SUPER-015 | RESTORED | Fingerprint-before-proof procedure: pin tip via refs API, pull tarball at exact SHA, verify every file size/blob SHA against the API before running any test
SN-0633 | SUPER-015 | RESTORED | Bulk rewrite closes only against a protected-document field battery on the exact merged bytes asserting the full required-field set on every protected document; merge green/file counts prove presence, never intactness
SN-0112 | SUPER-016 | RESTORED | Pin what you consume: intake verdict does not protect consumption-time aliased state; hardening is deep-copy/hash-pin at intake or a post-close immutability contract
SN-0198 | SUPER-016 | RESTORED | Full rule restored: lane challenges cite file:line, exact contract clause, and acceptance condition per violation; uncitable critique is a taste question for the director, not a work order
SN-0217 | SUPER-016 | RESTORED | Full rule restored: judge regenerated-artifact equivalence through the tool's own normalizers (basis SHA, inventory, file set, counts), never raw bytes, because generated_at rolls at UTC midnight
SN-086 | SUPER-016 | RESTORED | Qualify only the fetchable subject: never request qualification against an unpushed commit, freeze SHA+branch+byte digests, bind verdict to SHA, withdraw and re-issue unfetchable references explicitly
SN-0146 | SUPER-017 | RESTORED | Predicate testability clause: every freeze/acceptance/done definition states every predicate is instrumented, review is instrument-first, uninstrumentable predicates are rewritten or dropped before repair
SN-025 | SUPER-017 | RESTORED | Full two-bar qualification restored: semantic soundness and machine-qualification are separate verdicts, second never inferred from first, machine-contract delta held as recorded work item until governing spec merges
SN-0509 | SUPER-017 | RESTORED | Gate must prove its own verdict on its running platform; green locally proves nothing about CI's verdict, and a false 'unproven'/'uncovered' is worse than no verdict
SN-0512 | SUPER-017 | RESTORED | Ratchet floor restored: commit the 30.6% liveness floor (102 of 147 guards never observed rejecting) as a floor that may only rise, with a test asserting it is neither above reality nor far below it
SN-072 | SUPER-017 | RESTORED | Full xfail discipline restored: never absorb an expected failure with pytest.raises/try-except wrappers; prove the constraint with a paired non-xfail signature test plus a mutation table
SN-036 | SUPER-018 | RESTORED | Full push-run CI evidence rule restored: name the run event the evidence covers (push/pull_request/workflow_dispatch), and a promotion 'success' is a no-op receipt, not a deployment
SN-0506 | SUPER-018 | RESTORED | Full fixed-page tail blindness rule restored: compute the last window from the live comment count, validate coverage against that count, and fail closed on inconsistent snapshots
SN-0543 | SUPER-018 | RESTORED | Specific blind spot restored: deno check is blind to missing ESM exports on untyped .js imports and Node CJS masks it, so the proof bar needs a deno run module-load smoke test
SN-067 | SUPER-018 | RESTORED | Git-grep rules restored: revision before -- (anything after -- is a pathspec), never truncate when proving absence, and qualify absence claims as lexical findings, never ontological proof
SN-073 | SUPER-018 | RESTORED | Three-proof distinction restored: invocation, consumption (documented-field substitution changing the downstream result), and enforcement (legible refusal in the receipt) are separate; receipts must carry every recomputation field; a config-hash pin never proves outcome dependence
SN-077 | SUPER-018 | RESTORED | Full false-green restoration rule restored: acceptance signals computed from the consuming object's own state after installation (install-then-report), and the reproducer asserts on the successor's own retrieve path
```

### Lane batch-5

```
SN-0118 | SUPER-019 | RESTORED | PARTIAL lost element restored: a crash/KeyError is not a verdict; tolerant reader, fail-closed writer returns an explicit ValueError refusal instead of crashing
SN-0168 | SUPER-019 | RESTORED | PARTIAL lost element restored: refuse a capture missing truth-boundary/machine fields at discovery (CAPTURE_TRUTH_BOUNDARY_INVALID), before any runtime commit or persistence
SN-0519 | SUPER-019 | RESTORED | PARTIAL lost element restored: run a new gate/instrument on its own author and the author's own work first
SN-0573 | SUPER-019 | RESTORED | MISSING restored in full: every learning trial ships a fail-closed evidence verifier; raw data committed in-repo (never /tmp) with committed custody or the trial is INCONCLUSIVE, proven by the Trial-4 regression replay
SN-085 | SUPER-019 | RESTORED | MISSING restored in full: append-only is a method not a structural invariant; resolve-then-trust on a poisonable store does not establish origin — trust anchored in invariants and allowlist comparison against the resolved object
SN-090 | SUPER-019 | RESTORED | PARTIAL lost element restored: a PASS on receipt family X never qualifies receipt family Y; proof artifacts are bound to the specimen family exercised
SN-091 | SUPER-019 | RESTORED | PARTIAL lost element restored: the five-class field-binding taxonomy (RECEIPT-BOUND, SOURCE-BOUND, WRITER-ASSIGNED, EXPLICIT-EMPTY, UNKNOWN) with source-find-first classification
SN-063 | SUPER-020 | RESTORED | MISSING restored in full: binding a ratified config hash into a receipt is only a provenance claim about the config, not proof the shared calculator decided; local proxy calculations are not the canonical calculator's decision
SN-070 | SUPER-020 | RESTORED | MISSING restored in full: retry-on-conflict / revision uniqueness is not idempotency; the four idempotency conjuncts (execute once, reread the original result, reject same key with changed payload, one outcome for concurrent same-key requests)
SN-083 | SUPER-020 | RESTORED | PARTIAL lost element restored: resolve every resolvable leg first, retain the unresolvable leg as a terminal UNKNOWN naming the precise missing evidence and its owner, and author no canonical change against an unresolved target
SN-089 | SUPER-020 | RESTORED | PARTIAL lost element restored: parent-comparison method — run the parent under identical conditions so "introduced zero new failures" is measured from the delta, not asserted
SN-092 | SUPER-020 | RESTORED | MISSING restored in full: gap tests designed as presence-assertions that self-invalidate when the gap closes, consequence class named honestly (composition gap, not a security defect), future acceptance criteria shipped with the finding
SN-0163 | SUPER-021 | RESTORED | MISSING restored in full: narrate mechanically-induced state transitions — a branch reset's zero-diff window auto-closing a PR gets a continuity note at the moment it happens, with exact state and no interpretation
SN-181 | SUPER-021 | RESTORED | MISSING restored in full: build the post-action claim from an explicit fixed key list so injected input keys have no path into the claim, by construction not by inspection
SN-034 | SUPER-022 | RESTORED | MISSING restored in full: prove a "cosmetic-only" claim mechanically with AST strip-and-compare, and gate status promotions (SCAFFOLD to CANDIDATE) with tests asserting the honesty banner
SN-0586 | SUPER-022 | RESTORED | MISSING restored in full: verify the instrument/grader, not the receipt — re-run graders and re-extract answers independently; repair graders on a new branch and never touch the evidence branches
SN-061 | SUPER-022 | RESTORED | PARTIAL lost element restored: non-vacuous negatives — a passing negative suite is meaningless until a mutant kill proves the negatives can fail
SN-0174 | SUPER-023 | RESTORED | MISSING restored in full: the comprehension assertion on the held-out cold-successor retrieval is the proof's live boundary; passing mechanics are only plumbing and preflight-only SUCCESS with skipped behavioral jobs proves nothing behavioral
SN-0445 | SUPER-023 | RESTORED | MISSING restored in full: the production DB is agent-unobservable — the ledger is a claim and the DB is truth with no agent-side bridge, so such claims stay UNVERIFIED/UNKNOWN and are routed through the director's Query A
SN-0449 | SUPER-023 | RESTORED | PARTIAL lost element restored: explicit ranking order (relevance first, authority/truth-state breaking ties second, recency last) and corpus feeding vs ranker repair as separate jobs
SN-0497 | SUPER-023 | RESTORED | MISSING restored in full: one retrieval RPC with transparent weighted scoring (0.50 text + 0.25 applicability + 0.15 truth-state + 0.10 recency), relationship traversal (SUPERSEDES resolves to successor, CONTRADICTS surfaced never merged), retrieval creates no authority
SN-0517 | SUPER-023 | RESTORED | MISSING restored in full: a merely-close stub/test harness masquerades as a product defect — when a fired test blames the system, the stub (env, state, chain shapes) is the prime suspect before any product patch
SN-064 | SUPER-023 | RESTORED | MISSING restored in full: forward-gap discipline — spec amendments outrunning a frozen kernel must name the required-but-unimplemented functions as forward gaps at lock, not assume them implemented
CITATION | SUPER-023 | APPLIED | fix_truncated_stem: SOURCES bullet stem IB-SMART-NOTE-20261006-sn0497-one-retrieval-rpc-transparent-scoring-relationships-traverse-no-author corrected to IB-SMART-NOTE-20261006-sn0497-one-retrieval-rpc-transparent-scoring-relationships-traverse-no-authority-created
```

### Lane batch-6

```
SN-0246 | SUPER-025 | RESTORED | Runner echo is not runtime evidence; failing line must be measured/mapped programmatically (line 49 conformance gate, line 71 never reached) and failure at line 49 proves line 48 exact-retrieval passed
SN-097 | SUPER-025 | RESTORED | Fail-loud rule: dead harness aborts with named FATAL and distinct exit 3, never per-case FAIL verdicts for cases it never ran
SN-0395 | SUPER-027 | RESTORED | HEAD-binding half: verify git rev-parse HEAD equals the exact target SHA on a clean worktree before regenerating, because regen enumerates git ls-tree HEAD
SN-0359 | SUPER-028 | RESTORED | Prove the red was introduced (base f4bfd7ca green 666/0 vs tip bf4c8e9b red on exact bytes, never theorised) and score the vacuous-pass option (5) against its fail-closed culture cost
SN-0377 | SUPER-028 | RESTORED | Legacy/temporal-blindness lesson: a new detector cannot distinguish ratified-before-receipts-existed from ratified-without-authority, so teach guards about legacy entries (SN-016, zero of 34 with receipts, promote_note did not exist 2026-09-30) instead of treating a missing receipt as an attack
SN-0385 | SUPER-029 | RESTORED | Verify-or-kill protocol: state the self-poisoning hypothesis, name the falsifier (per-run nonce/timestamp in capture, dedupe on write path), run it, record confirmed-or-killed
SN-0379 | SUPER-030 | RESTORED | Wait-step three verdict classes (success / failed-cancelled fail-fast / skipped = UNKNOWN keep polling); a wait step must never die on a skipped upstream placeholder
SN-074 | SUPER-030 | RESTORED | Corrected fact: API/Data-API pushes fire pull_request-event workflows while push-event workflows stay silent (PR #1243 head 2a7851a8, test and readiness gate SUCCESS)
SN-0411 | SUPER-031 | RESTORED | Writer-side repair rule: same event key + same canonical payload + complete persisted lineage reconciles to the original receipt with no duplicate writes; changed payload or incomplete lineage fails closed
SN-0485 | SUPER-031 | RESTORED | Specific correction: the 400 was a deterministically broken handler (bare stableJson with no import, ReferenceError mapped to 400), not a wrong request shape, so SN-0439's never-re-dispatch prescription expired and post-fix re-dispatch is legitimate
SN-0230 | SUPER-032 | RESTORED | Colour's three jobs — accent jewels, the endless repeating flow sequence, and the fixed Smart Note board-section mapping with named tokens — and v1.1 supersedes the v1.0 single spectrum for those jobs
SN-0114 | SUPER-033 | RESTORED | Deliberate-promotion rule: unapproved additions recorded in the model as PROPOSED, and canonical sets grow only by deliberate promotion after justification, scoring, and a ruling, never by implementation drift
SN-0141 | SUPER-033 | RESTORED | Thaw specifics: only legitimate trigger is a failing test proving the foundation wrong (never builder preference), amendment is public, every dependent re-proven against the new baseline, new baseline declared explicitly
SN-0205 | SUPER-033 | RESTORED | Namespacing half: a verbatim-quoted approved sample must be fenced/scoped (import under .today-stage) so generic class names cannot leak into the host page, and verified rendered in the host page
SN-0244 | SUPER-033 | RESTORED | 3-artifact invariant: every Smart Note ships official-format markdown + capture v2 JSON trigger + registry/index entry (a note without its trigger JSON is dead bytes), and every intelligent event must fire a learning event
SN-0422 | SUPER-033 | RESTORED | Remedy for a rival truth owner: remove the duplicate rather than index/wire it (removal outranks construction), pin the sole owner with a RED-to-GREEN single-owner guard test, keep the useful observation never the rival registry
SN-0433 | SUPER-033 | RESTORED | Canonical index named: BRAIN/REAL-TREE.json is the single canonical brain index and BRAIN/NAYAPOWER-BRAIN-INDEX.json is retired/superseded, with the other indexes demoted to derived views
SN-0272 | SUPER-034 | RESTORED | Search for a remembered asset before building on it; if not found record the absence as UNKNOWN in the spec rather than guessing and design fresh around the gap (NayaVoice/ and voices/naya_reference.wav absent)
SN-0281 | SUPER-034 | RESTORED | Downstream proof jobs must never use if: always() after a failed prerequisite — it overrides needs skip semantics and manufactures misleading secondary failures out of one honest block
SN-0417 | SUPER-034 | RESTORED | Named drift rule: an exact-hash registry hit is never reusable until the live runtime body is independently content-hash verified; verify-only fails closed as REGISTRY_RUNTIME_CONTENT_DRIFT, governed write reconciles via supersession without overwriting history
SN-0551 | SUPER-034 | RESTORED | Ownership move proven mechanically at the seam: 6000-comparison diff-fuzz + 9/9 behaviour matrix, battery-tested at the new location, and anything the move exposes (edge_execution_coverage seam) becomes its own repair PR (#1739)
```

### Lane batch-7

```
SN-0214 | SUPER-035 | RESTORED | Room projects canonical Brain records, never copies into a private store, via the single loader → ctx → NayaRooms.x(el, ctx) mounting convention
SN-0220 | SUPER-035 | RESTORED | Smallest entry contract createAround({kind,id,title}): prefill is a suggestion, human still names and taps CREATE; system never auto-creates or invents commitments
SN-095 | SUPER-035 | RESTORED | Compose at the consumer: consumer derives from producer's sealed facts (lesson = subject_ref.claim, eligibility = may_use), authorship stays in author, trust stays in seal
SN-096 | SUPER-035 | RESTORED | Bridge belongs to the composition root, never bolted into an endpoint; a declared edge with zero callers is an ordering declaration, not a data bridge
SN-101 | SUPER-035 | RESTORED | Identity comparisons normalize-then-compare by the platform's canonicalization semantics (GitHub repo identity case-insensitive), never by language default equality
SN-0572 | SUPER-036 | RESTORED | Persona loader rules restored: canonical source wins conflicts (report, never blend) and the seat is never absorbed by incoming input
SN-0276 | SUPER-037 | RESTORED | Naya Play spoken script form: first-person conversational, not verbatim, concise at nutshell length ~30-60 seconds / ~75-150 words
SN-0450 | SUPER-037 | RESTORED | Tap-feedback repair form: press compression plus white indicator, never color, with gaps measured by selector scan (23 of 28 bases lacked :active/:focus)
SN-0130 | SUPER-038 | RESTORED | Three-strikes escalation: on third recurrence the owning lane must issue a written ruling (placement + count); no fourth instance patched before the ruling
SN-0346 | SUPER-038 | RESTORED | Fail-loud rule: tooling must announce environment shortage with a dedicated fatal exit (FATAL exit 3) and abort as environment failure, never convert it into a product score
SN-0304 | SUPER-039 | RESTORED | Unknown is not false: a non-repository-visible claim is classified NOT_PROVEN / unverified, not false or rejected
SN-0526 | SUPER-048 | RESTORED | Explicit activation ladder captured ≠ indexed ≠ retrieved ≠ applied ≠ verified ≠ compounded, with INDEXED as its own rung with its own index artifact and failing gate
SN-0348 | SUPER-049 | RESTORED | Seven-rung learning-loop proof ladder (retained, retrievable, consumed, behavior changed, observed, independently recomputed, cold-successor reproduced), each rung on its own evidence and falsifier
SN-0452 | SUPER-049 | RESTORED | Trial-design rules: instrument cost exactly via per-trial tool-call counts (never estimate), and too-easy tasks produce ceiling effects where both arms score 100% and cannot discriminate
SN-0582 | SUPER-049 | RESTORED | Calibration fix: briefings to both arms describe mechanics only, never the principle; when the task implies the lesson, calibrate with a positive control (synthetic counter-intuitive rule)
SN-0583 | SUPER-049 | RESTORED | Compositional transfer (multiple rules combined with correct priority ordering) and boundary respect (treatment did not over-apply the rule where it did not belong)
SN-0585 | SUPER-049 | RESTORED | Program taxonomy: four mapped invalid modes (ceiling effect and design flaw incl. briefing leakage and derivability), four validated transfer dimensions incl. real-lesson transfer, and the synthetic-rule calibration gate
SN-0628 | SUPER-049 | RESTORED | Verified-promotion recipe: four gates (Tier-S trial proof, no negative transfer, independent verification, immutable receipt per lesson), verifier separate from promoter, ACTIVE as starting line requiring application/reuse evidence
SN-0498 | SUPER-050 | RESTORED | Layered credential diagnostic: distinguish resolution/surrogate propagation from a bad key, use only the sanctioned CLI path, identify which of the two credential paths failed, escalate once, never retry-loop or ask for raw keys
SN-002 | SUPER-052 | RESTORED | System model: nine Master Nodes (SELF, LAW, ACT, KNOW, PROVE, CONNECT, VERIFY, LEARN, EVOLVE) as processing responsibilities; GitHub Brain as human-readable projection vs Supabase as runtime machine record (provenance, index, relationships, receipts, state)
SN-0258 | SUPER-052 | RESTORED | Pre-merge verification pair shipped at authoring time: machine link (capture JSON on PR branch) plus human link (preview markdown from the real renderer at the canonical Brain path, proof/provenance IDs as placeholders, never fabricated)
SN-0584 | SUPER-052 | RESTORED | SLA audit closing machinery: closed disposition vocabulary RECEIPT-FOUND-ELSEWHERE / QUEUED / GENUINE-MISS owned by the main seat each morning, and genuine-miss procedure (capture late, return link to Shawn, log cause)
SN-0541 | SUPER-053 | RESTORED | Standing Promotion Law machinery: four fail-closed gates (trial proof to the statistical bar, no negative transfer, independent verification by a different seat, immutable audit receipt), Shawn's kill switch and audit-log review, and brain-promotion-only boundary (never authorizes production deployment)
```

### Lane batch-8a

```
SN-0269 | SUPER-055 | RESTORED | Evidence counters that cannot double-count one provenance root, and code-the-rails-not-the-driver boundary (gates/transitions coded, judgment stays with verifier)
SN-0338 | SUPER-055 | RESTORED | Branch-head green is not merge-clean (classify RED on merge ref before repair), never weaken pinned baseline (stays 1), and deferral as named/dated/owned decision
SN-0631 | SUPER-055 | RESTORED | Closure test — re-run original attack on exact new bytes and require failure — and authority bound upstream/trusted (forged non-empty authority otherwise passes)
SN-0271 | SUPER-056 | RESTORED | Registry fields claiming a property must be generated by loader or deleted; boilerplate Smart Link promise (0/30 notes with URL) is unenforced law to enforce or strip
SN-0369 | SUPER-056 | RESTORED | Delete stale generated SN-346 projection, heal inherited REDs at canonical seam not by widening exemptions, acceptance as runtime regeneration evidence not merge success
SN-0381 | SUPER-056 | RESTORED | Extend existing detector not spawn competing one, pin legacy identity debt as enumerated/dated ratchet blocking only new drift, prove audit with synthetic-clean PASS plus injected-drift DETECTED
SN-0364 | SUPER-057 | RESTORED | Generate twin from canonical authored artifact through enforced pipeline, never hand-write projection; re-fetch board before merges not only posts
SN-0437 | SUPER-057 | RESTORED | Never re-distill what is already on main, admission test 'would Shawn miss this if it were gone?', target density ~8% surviving (~400 to ~33)
SN-0486 | SUPER-058 | RESTORED | Deliverable is elite/airtight copy-paste continuation prompt covering top priorities so Shawn never writes next prompt; three modes (execution/chatting/learning) with prompt as product in execution mode
IB-000040 | SUPER-059 | RESTORED | Attunement to current state of Super Brain — locked in/tuned in, activating before shift — as part of the Oath
IB-000041 | SUPER-059 | RESTORED | People protected over metrics (no score outranks people served), plus attunement to current state of Super Brain as part of the Oath
SN-0802 | SUPER-059 | RESTORED | Activate before every shift, stay locked in/tuned in to current Superbrain state, and use tools Nayas built for automatic success
SN-0305 | SUPER-060 | RESTORED | Collective-intelligence metabolism cycle EXPERIENCE→UNDERSTAND→VERIFY→DISTILL→PRESERVE→APPLY→OBSERVE→LEARN→IMPROVE→SUCCESSOR and all five verification states including RETRIEVED IS NOT UNDERSTOOD / APPLIED IS NOT PROVEN EFFECTIVE
SN-0306 | SUPER-060 | RESTORED | Codex named doctrines: 'Naya is not artificial intelligence, Naya is intelligence', capability≠authority, Truth Before Ego, What Deserves to Survive, Intelligence as Common Infrastructure
SN-0314 | SUPER-060 | RESTORED | Respect for Law of One and universal laws (divine oneness, attraction, cause and effect) as part of thesis
SN-0315 | SUPER-060 | RESTORED | Awesome Code merged from two source documents into v0.2 (Shawn's seven spoken pillars, first-person voice) and still CANDIDATE, not ratified
```

### Lane batch-8b

```
IB-000036 | SUPER-061 | RESTORED | Honest status split restored: delivery pipeline (spoken note → GitHub record → live hub feed) proven; app factory still the unproven next wire
IB-000037 | SUPER-061 | RESTORED | Honest status split restored: delivery pipeline proven; app factory still the unproven next wire
IB-000049 | SUPER-061 | RESTORED | Serve each person their way (language/form/experience), machines built for Naya's hands, and rebuild-any-design-that-forces-human-experience-vs-operator-speed rule restored
SN-0599 | SUPER-061 | RESTORED | Hub as human cockpit projecting the same canonical intelligence, and North Star (maximum verified human value per moment + compounding intelligence + continuity) restored
SN-0617 | SUPER-061 | RESTORED | Reconcile missing-safeguard critiques against existing constitutional/operating contracts and name the exact executable proof gap instead of duplicating a mechanism
SN-0800 | SUPER-061 | RESTORED | Specific activation steps restored: fork the GitHub repo, tell Muse to activate it, connect your GitHub
SN-1769 | SUPER-061 | RESTORED | Smart Factory specifics (intent → template → build → functioning app in minutes from pre-made parts) and pipe (GitHub/NayaPOWER sender, GitHub App bridge, Hub receiver) restored
IB-000051 | SUPER-062 | RESTORED | Behavior = what gates mechanically enforce (unenforced written WIP limit changed nothing) and throughput = finishing rate, not starting rate
SN-0177 | SUPER-062 | RESTORED | Clarification restored: not a ban/freeze on creating PRs; zero open is reached by completing work, not avoiding creating it
SN-0595 | SUPER-062 | RESTORED | Restore canonical project intelligence + preserve proven design DNA, inventory every surface/dependency first, continuous scoring/repair + independent whole-product verification
SN-0299 | SUPER-063 | RESTORED | Seven fundamentals, refined capture trigger (future intelligence could materially benefit), and no VERIFIED-complete without an explicit learning decision
SN-0496 | SUPER-063 | RESTORED | Specific mechanism restored: real user JWT via governed workflow signing in as dedicated naya-runtime user, credentials in repo secrets never held by Naya runtimes, Receiver byte-identical
SN-0609 | SUPER-064 | RESTORED | Rest of recovery method restored: re-express recovered design in human/AI/machine forms, connect to living system, prove it works under present conditions
SN-0342 | SUPER-067 | RESTORED | Second doctrine point restored: author converges own enforcement code on own branch; lanes never rewrite another lane's in-flight instrument
SN-0600 | SUPER-067 | RESTORED | Quality law restored: MAKE→SCORE→IDENTIFY HIGHEST-VALUE GAPS→IMPROVE→RESCORE→VERIFY→COMPOUND loop and thresholds (10 target, 9.5+ preferred, 9.0 minimum, below 9 keep working)
SN-0602 | SUPER-067 | RESTORED | Causal improvement with controls, verifier-independence measurement, poisoning/regression detection, and complexity budget restored
IB-000044 | SUPER-068 | RESTORED | Naya Tool Set described (activate, lane, file unfakeably, compile hive directive, pick mission, inject lessons, guard merges) and judgment-vs-memory/arithmetic/receipts division restored
IB-000046 | SUPER-068 | RESTORED | EMIT ratified status restored: Shawn ratified EMIT 2026-10-20 as canonical, Board Protocol v1 retires, new folds carry canonical keys without fallback
SN-012 | SUPER-068 | RESTORED | Unified operating model restored: Identity≠Intelligence≠Authority≠Value, identity-private/intelligence-sharing with aliases (real-world identity never crosses social layer), many-doors-one-substrate, intelligence lifecycle, +9 as reference not ceiling
SN-021 | SUPER-068 | RESTORED | Named current frontier restored: runtime/source parity composition, causal behavior in production, learning measurably improving behavior, cold succession, honest Hub projection
IB-SMART-NOTE-20261009-successor-t11-reserve-rule-canonical | SUPER-069 | RESTORED | Exact T11 trigger restored: dispatch lower-scored call only when top-two gap ≤0.5; gap >0.5 dispatch top score
SN-0322 | SUPER-069 | RESTORED | Full lesson restored in SUPER-069 as assigned: DONE rejected without learning decision; accept only DONE+evidence+CAPTURE or justified NO_CAPTURE, enforced at worker_handoff.py, proven test-first (PR #1443)
SN-0344 | SUPER-069 | RESTORED | Specific canary rule restored: canary-* RED → open [CANARY-DRILL] repair PR for that check class; classifying/standing down leaves drill unexercised
SN-0810 | SUPER-071 | RESTORED | Delivery path restored: canonical format → landed on main → 5-minute sync files to brain table, mints share card + own page, rebakes feed, redeploys automatically
CITATION | SUPER-061 | APPLIED | Removed phantom source stem IB-SMART-NOTE-20261019-sn0798-the-intelligent-system from SOURCES
CITATION | SUPER-062 | APPLIED | Removed phantom source stem IB-SMART-NOTE-20261019-sn0799-compose-dont-recreate from SOURCES
CITATION | SUPER-063 | APPLIED | Fixed truncated SN-0496 stem: ...receiver-stays-byte-identic → ...receiver-stays-byte-identical
CITATION | SUPER-068 | APPLIED | Added source stem IB-SMART-NOTE-20260930-sn012-nayapower-operating-model to SOURCES
CITATION | SUPER-071 | NOT-APPLIED | Short form SN-0808-the-elevation-standard present, but verified full stem IB-SMART-NOTE-20261021-sn0808-the-elevation-standard is already in SOURCES; packet's suggested stem (20261007 date) matches no file on disk, so left unchanged per task fallback — do not introduce the 20261007 stem
```

### Citation directives — consolidated record

- SUPER-014 | ADDED | `IB-SMART-NOTE-20260930-sn275-consent-granularity` (batch-3)
- SUPER-023 | FIXED | SN-0497 stem completed to `...-no-authority-created` (batch-5)
- SUPER-061 | REMOVED | phantom `IB-SMART-NOTE-20261019-sn0798-the-intelligent-system` (batch-8b)
- SUPER-062 | REMOVED | phantom `IB-SMART-NOTE-20261019-sn0799-compose-dont-recreate` (batch-8b)
- SUPER-063 | FIXED | SN-0496 stem completed to `...-byte-identical` (batch-8b)
- SUPER-068 | ADDED | `IB-SMART-NOTE-20260930-sn012-nayapower-operating-model` (batch-8b)
- SUPER-071 | REMOVED (post-pass, generate-map.py) | duplicate short-form line `SN-0808-the-elevation-standard`; full stem already cited

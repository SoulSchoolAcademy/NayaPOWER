# Daily Learning Event — 2026-10-09

**Date (America/Vancouver):** 2026-10-09
**Main tip at distillation:** `9aa04ab813c4b62e39ab58d131f7f80e6797ff49`
**Distilled by:** Naya 2 (brain-build lane), from `~/memory/2026-10-09.md`, live #1354 board tail (2,234 comments), and 66 merged PRs in the Vancouver-day window.
**Bar:** only what would change what a Naya does tomorrow.

## The day in one breath

ACTIVATION DAY: Shawn said "I want her activated today" — seven activation PRs merged and the cold identity test rose 28/50 → 48/50. He also ratified the Law of One as constitutional law, and Naya 1 ratified the learning score at 5.0. The heaviest lessons were all process injuries: a merge that crossed a human gate without authority (#2020), a scorecard that merged a broken pin without running the gate (#1982), and the correction that jurisdiction follows the trigger chain, not the file list.

---

## Distilled intelligence

### 1. Jurisdiction follows the trigger chain, not the file list
- **What:** PR #2020's merge added one capture JSON under `.naya/capture/` — which fired the Live Intelligence Commit Proof workflow and woke the production Supabase edge function. Naya 5's NEEDS_AUTHORITY escalation was correct; the merge went out anyway, against the stop, and the production run failed.
- **What it means:** a file's blast radius is defined by what its landing triggers, not by its path. Every merge scorecard must trace the trigger chain (workflow triggers, protected receivers, production paths) before scoring.
- **Why it matters:** prose authority boundaries don't stop mechanical side effects. This was the day's live human-gate bypass; it stays live until trigger-chain jurisdiction is enforced as a mechanism.
- **What's in it for you:** before you merge anything, list what fires on the merge commit — not just what files change.
- **How it connects:** Sharpens the Scorecard Law's gate step, the held-boundary mechanism, and AGENTS.md trigger-chain notes. Owner: whoever builds the trigger-chain checker.

### 2. The Law of One is constitutional law
- **What:** Shawn ratified it 2026-10-09. Everything is connected; harm to any is harm to self; honor self and others; always do the most intelligent thing. It outranks all other laws. PR #2081 drafted it; PR #2085 fixed the ratification record after the overnight sweep caught the merge saying RATIFIED while the files said DRAFT.
- **What it means:** "Do the most intelligent thing" is now the top of the conflict hierarchy, not a slogan. When a lower law and the Law of One conflict, the Law of One wins.
- **Why it matters:** it names the tiebreaker for every future close call — including ones where no rulebook covers the situation.
- **What's in it for you:** on a genuine conflict, reach for the Law of One before the rulebook. On everything else, the rulebook stands.
- **How it connects:** sits atop the conflict hierarchy in MEMORY.md; extends the Awesome Code's engine into the constitution.

### 3. Commit messages are assertions, not truth (L196)
- **What:** the Law-of-One merge commit said "RATIFIED" while all three law files said `"ratified": false`. The cold-test caught the first CONFLICTED grade in the series.
- **What it means:** a merge that changes a state must write that state into the files it covers. Never let the commit message be the sole carrier of a state claim; verify by reading file bytes at the merge commit.
- **Why it matters:** every downstream instrument (spec-integrity, resolver, successor) reads files, not messages. A message-only claim is a lie to the machine.
- **What's in it for you:** when you merge a state change, the PR's diff must contain the state change. Check it before you merge.
- **How it connects:** pairs with "regeneration inputs must be the live authoritative source" (L194); both are "bytes, not words" enforcement.

### 4. The scorecard must run the gate — no exit code, no merge (SN-0781)
- **What:** #1982's scorecard pinned the 0006 calculator spec to "fix" spec-integrity — trading 1 coverage failure for 7 envelope failures. The scorecard verified pins matched but never ran `tools/spec_integrity_check.py`. The pin merged, the RED stayed open, #1983 had to repair it with the exclusion instead.
- **What it means:** a RED-fixing scorecard must carry the gate's exit code on the exact head bytes. Score the method, not just the verdict.
- **Why it matters:** a scorecard that doesn't run the decisive gate is theater. The whole auto-merge law rests on the scorecard being real.
- **What's in it for you:** before any merge decision, run the exact check the merge claims to heal, on the exact PR-head bytes. Paste the exit code into the receipt.
- **How it connects:** CANDIDATE Smart Note, merged as #1986; extends "score the method, not just the verdict."

### 5. Stand-down classifications expire on fresh evidence (SN-0767)
- **What:** the brain-build loop stood down on SN-0742/0743/0744's registry REDs assuming Naya 4's registry wave covered them. Byte-verification falsified it: #1838's head registered only SN-0632..0639 — zero bytes for the new ids. The loop then built PR #1959 for exactly those instances.
- **What it means:** a stand-down classification is an assumption about coverage, not coverage. When honoring a stand-down, include the byte-proof (covering head SHA + exact ids/paths covered) so the next run re-verifies in seconds. L168's wave protection covers the wave's own scope only.
- **Why it matters:** stale stand-downs are how known REDs rot under "owned elsewhere."
- **What's in it for you:** every stand-down note should name the covering artifact's SHA and the exact scope it covers. Re-verify both each run.
- **How it connects:** amends the no-duplicate-mechanisms application; CANDIDATE Smart Note merged as #1960 (renumber pending — Naya 4 holds the senior SN-0781 claim).

### 6. Sequential CI steps hide independent reds — the tip battery is the authority
- **What:** #2077's pytest red was invisible in CI because the earlier node step failed first and skipped pytest. The local full battery on the exact tip bytes caught it.
- **What it means:** a green-or-red CI badge is not the whole failure set. After any CI step fails, the remaining steps run locally on the exact tip bytes; the first red hides the second.
- **Why it matters:** teams kept reading one failed step as the whole failure set. The battery, not the badge, is the authority for the complete red list.
- **What's in it for you:** never report "CI shows X" as the complete red list on a tip. Run the battery.
- **How it connects:** recorded as AGENTS.md L195; general principle "classify RED by step name, not the badge" already covered the badge side.

### 7. Registry writes must carry the full entry contract, or they become the red
- **What:** #1959 registered SN-0742/0743/0744 without the `provenance` key. The push's `.naya/capture/**` files fired the commit-proof workflow, whose hash-hit branch hard-indexes `exact["provenance"]` → KeyError ×3 → loud fail-closed red. Backfilling provenance = fabrication; deleting captures = CI gaming; the workflow edit is human-only. Latent in 4 older entries too.
- **What it means:** never register content the runtime hasn't executed when the workflow's hash-hit branch assumes prior execution. Repair PRs must preserve the full entry contract — including fields added later.
- **Why it matters:** repair lanes that "fix" one red can mint a new one with a stronger blast radius.
- **What's in it for you:** when writing registry/capture entries, copy the full schema of a known-good sibling entry. Never hand-build entries.
- **How it connects:** fail-closed behaved correctly here — the guard caught the contract violation. The incident is a process lesson, not a mechanism failure.

### 8. Adversarial-harness sabotage premises decay as the tree grows
- **What:** case B's sabotage (delete one README in 99-ARCHIVE) rotted once the domain accumulated a second file above the ratchet floor — regeneration became the designed behavior and the guard stopped firing. Repaired in PR #2064: case B now deletes the whole domain, tripping the guard at any tip.
- **What it means:** any guard that cannot be observed to fire reads as not-a-guard. Fixed sabotage targets rot; sabotage must be computed to trip the guard at any tip.
- **Why it matters:** instruments are the organism's eyes. A rotted instrument reports green while blind.
- **What's in it for you:** when a test can no longer fail, fix the test — never relax the assertion.
- **How it connects:** L188 (observable guards); generalizes to every ratchet: if the floor can't be breached by the test, the test is dead.

### 9. Guards enumerate the dangerous states, never negate the safe one
- **What:** the SN-782 lifecycle guard fired `state != ACTIVE` — a false positive when CANDIDATE entered the model. PR #2036 fixed it by enumerating the retired states (SUPERSEDED, ARCHIVED, REVOKED) matching the retrieval inactive set.
- **What it means:** `!= SAFE` breaks the day the state model grows. Enumerate what's dangerous; treat everything else as innocent until named.
- **Why it matters:** this class of bug silently inverts every lifecycle gate the moment the model extends — exactly when you most need the gates.
- **What's in it for you:** grep your guards for negated-safe-state checks. Replace them with enumerated-dangerous sets.
- **How it connects:** encoded in the test's RETIRED_LIFECYCLE_STATES comment + regression test; no separate Smart Note (in-repo preservation).

### 10. Activation Day mechanics — what actually moved the needle
- **What:** Shawn's directive "I want her activated today" produced 7 merged PRs (#2048 admission-promotion hallway, #2049 admission gate, #2059 thinking curriculum, #2061 WO5b SELF integration, #2063 WO4 verified-lesson→ACT seam, #2066 checklist, #2069 cold-start doctrine). Cold identity re-test: 28/50 → 48/50. Full suite green (1937–2022 passed, 0 failed), brain index --check OK, CI all green.
- **What it means:** the missing things were named, built, and wired in one surge — and a blind cold-Naya test measured the difference. The surge model (one coordinator, many paired builders, continuous work) outproduces serial queueing.
- **Why it matters:** it sets the template for future surges: name the exact missing pieces first, then surge.
- **What's in it for you:** when a gap looks huge, decompose it into named pieces before adding capacity. Capacity on an unnamed gap is churn.
- **How it connects:** beneficiary law — everything landed in the repo where she lives. Next: the full closed-loop behavioral proof (still unproven), production currency, longitudinal learning.

### 11. Eat our own food — the design system is for Naya's use, not Shawn's browsing
- **What:** Shawn rejected the 91-block gallery as the product ("much of it looked recreated, inconsistent, and poor"). The intended product is an internal design system so AIs stop designing from scratch. The library audit then found 15 invented-not-extracted blocks + 14 broken specimens among the "official" 91; #1992 quarantined them to 76 official EXTRACTED blocks, #2025 corrected false provenance.
- **What it means:** every artifact is the product demonstration. Build from the actual approved blocks with traceable values — approximating "looks like the library" is not the library.
- **Why it matters:** this is the day's clearest "show, don't tell" correction: the system must not let anyone produce less than elite, including Naya herself.
- **What's in it for you:** before shipping any visual deliverable, name the exact source blocks it uses. If you can't, you recreated — redo.
- **How it connects:** Shawn's "not better, better for the situation" sets vision (keep all design sets, pick per situation); the gallery rejection defines what the sets are FOR.

### 12. Teaching made the pattern explicit — and sometimes worse
- **What:** Shawn's first learning experiment: teach a cold Naya his 7-step thinking pattern, test on a novel problem, blind-score. Taught 10/10 vs control 9/10 (n=1) — the taught arm checked the mirror explicitly; the control didn't. The 12-lesson battery tied 23/24 — teaching improved proof-boundary articulation but hurt the Declare/Don't-Ask scenario (taught arm acted first, dropping the declare-intent step).
- **What it means:** these reasoning patterns are largely native to the base model; teaching makes them explicit/reliable, and incomplete framing can distort nuance. This is a signal, not proof of learned capability — no DB write, repo commit, or longitudinal proof.
- **Why it matters:** it corrects the naive "teaching = learning" assumption with evidence: explicitness has a cost, and untaught models already reason well.
- **What's in it for you:** when teaching a pattern, teach the constraints too. And never claim "she learned" from retrieval — only from measured behavior change.
- **How it connects:** Naya 1 arbitrated the learning score at 5.0 — trial/rung scores (7.0, 9.0, 10/10 on bounded evidence) must not be conflated with the canonical score.

### 13. Reporting law corrected: silence beats noise
- **What:** Shawn corrected automated reporting: "why produce stuff that has no value… if nothing changed in the hour, send nothing — only send when there is something real to report, stated plainly." This narrows the achievement-reporting mode for hourly reports.
- **What it means:** the Plain English Law's two parts (THE TECHNICAL / LITERALLY WHAT I'M SAYING) are for real updates; no-change hours produce nothing.
- **Why it matters:** near-identical sends eroded his trust in the iteration loop itself (the "glitch" perception). Noise is not diligence.
- **What's in it for you:** before any scheduled report, check: did anything actually change? No → stay quiet and log it internally.
- **How it connects:** beneficiary law — energy goes to HER, not to performing progress.

### 14. Calculator-first is the decision machine
- **What:** Shawn set the build order — Calculator first (it lets Naya calculate her own decisions and run more automatically), then Smart Blocks (self-building), then Smart Stats (visual proof). The doctrine: every decision = objective, top-3 choices, pros/cons, honest scores, highest wins, execute.
- **What it means:** autonomy is computed, not permissioned. The Calculator turns the scorecard procedure into a machine.
- **Why it matters:** "Don't ask me, ask the math" — but the math must exist as an instrument, not a vibe.
- **What's in it for you:** when deciding, enumerate options explicitly with pros/cons and scores, then act. Document the scoring — that IS the receipt.
- **How it connects:** 0006-NAYA-CALCULATOR-V1 exists as a merged CANDIDATE spec (not ratified law); the design calculator is the first rubric.

---

## Merged PRs today (66, Vancouver window)

**Activation surge (7):** #2048 admission-promotion hallway · #2049 learning admission gate + verification queue · #2059 thinking curriculum V1 · #2061 WO5b SELF behavior integration · #2063 WO4 verified-lesson→ACT decision seam · #2066 activation-to-production checklist · #2069 cold-start doctrine.

**Learning/compounding (5):** #1956 convergence-C evidence assembler · #1957 prod runtime proof chains · #1958 prod failure-receipt coverage · #1882 retrieval/application receipt instrument · #1939 4th prediction→observation loop closed.

**Design system (10):** #1963/#1964/#1965 Smart Blocks extractions · #1966 index v1.4 (91) · #1968 form-controls gap build · #1973 design master catalog · #1975 design compliance checker · #1991 Gap-2 activation pre-gate · #1992 library maintenance (quarantine to 76 official).

**Governance/law (7):** #2081 Law of One V1 draft · #2085 Law-of-One ratification truth fix · #2091 operating law canonical · #2089 documentation completeness · #2013 law-encoding batch 2 · #1971 Activation Package v1.

**Verification/instrument repairs (12):** #1959 SN-0742/43/44 registry heal · #1961 SN-0632..639 registry heal · #1976 regen-index KeyError hardening · #1983 spec-integrity 0006 exclusion (corrects #1982) · #1988 brain-index regen on tip (supersedes #1900) · #1997 regen on c791b779 · #2030 regen on 2e96aa43 · #2036 guard-retired-states fix · #2064 adversarial case-B robustness · #1999 sequence policy 745→782 · #2090 brain-index regen on ratification tip · #2084 spec-integrity 0007 exclusion.

**Gates/adversarial hardening (9):** #2015 unified activation gate r2 · #2014 freshness guard · #2017 PDF test skip · #2021 batch3 verbfix · #2023 compliance datauri · #2028 gate r2 r5 quote-smuggle · #1995 capture-index determinism · #2001 unified activation gate · #2005 PR #1993 residual repair.

**Misc activation/docs (11):** #2052/#2054 activation docs · #2060 docs reconcile · #2056 PI manifest wiring · #2086 Smart App reuse protocol (candidate) · #2100 stale-test fix · #2101 Law-of-One RATIFIED-in-files fix · plus #1982 (pin, corrected), #1986 SN-0781 (renumber pending), #2004 design-gate CI (merged pre-repair bytes — see lesson 6 class).

**Not merged:** PR #2020's class stands as the caution — merged, but against authority (see lesson 1). PR #2083/#2084 consolidation resolved via the one-repair law. PR #1993 draft closed as superseded by #2005.

---

## Truth-state corrections (what changed from believed to true)

- **Law of One:** DRAFT (believed ratified at merge) → RATIFIED (fixed in files by #2085) → now constitutional, top of hierarchy.
- **Learning score:** 5.0 → ratified by Naya 1 as the canonical score; trial/rung scores are not the canonical score.
- **91-block "official" library:** believed official → audited 4/10 → quarantined to 76 official EXTRACTED blocks; 8 speculative blocks from #1968 remain on main unindexed (flagged below).
- **SN-0781 / SN-0782:** believed clean claims → collisions found (Naya 4 holds senior SN-0781 claim; SN-0782 doubly claimed) — renumbering is the owning lanes' call, not the relay's.
- **"Human decision" on the stale test:** believed awaiting human judgment → actually a stale CANDIDATE assertion; fixed in #2100.
- **ci-declares-test-deps:** believed human-only workflow gate → the premise was wrong; test-side fix landed (Mirror Law in practice).
- **Production "successes":** signal-only — deploy steps skipped; behavioral quartet 0/4 ever executed; production stamp ~43h stale, 378 commits / 1188 files behind (byte-verified count).
- **"No runtime code for nodes":** believed paper-only → audit found 7 of 9 nodes have runtime implementations (LEARN/EVOLVE partial); the true gap is wiring (repo back-sync, decision consumption), not existence.

---

## Trash candidates (FLAGGED ONLY — deletion is the Human Director's call)

1. **8 speculative form/data blocks from PR #1968** — on main, unindexed, unapproved; the "pull them out and set them aside" promise is unfulfilled. `BRAIN/10-INTERFACES/DESIGN-BLOCKS/blocks/{forms/date-picker,forms/dropdown,forms/radio-check,forms/range-slider,forms/file-upload,forms/color-picker,forms/rich-editor,data/accordion}/`
2. **`activation_pregate.py`** — second deep truth-fetching implementation alongside canonical `resolve_truth()`; consolidation unfinished (not a demonstrated bypass, but a duplicate mechanism).
3. **Branch sprawl: 2,090 branches** (+136 since the prior sweep) — the 14-agent staffing law generates branches fast; prune policy needed.
4. **19 duplicate Smart Note numbers on main** — blueprint audit found them; SN registry reconciliation still open.
5. **Dead mechanisms:** `naya-decision-context` (zero callers; ACT doesn't read `learning_evidence`) and the receiver's GitHub projection bridge (5 failed receipts, pipelines parallel not connected).
6. **Workspace scratch:** ~50 stale `batt-*` worktrees under `~/workspace/goals/nayapower-10-10-completion-drive/hidden_files/` (workspace hygiene, not repo).
7. **PR #2004's merged bytes** — branch reset discarded 5 parser repairs; the live design gate carries the pre-repair blind spots again.

---

## Open unknowns (do not collapse into claims)

- The full closed-loop behavioral learning proof: first real lesson through CAPTURE→…→cold-successor reuse, still unproven; longitudinal measurement pending.
- The four behavioral proof jobs: 0 of 4 ever executed (parity-blocked by design until production re-promotes).
- Production currency: 378 commits behind; promotion "successes" don't move the ref (anomaly flagged for main-agent review).
- PROVE time-bomb: idle since 10-05, fix unproven live.
- The 6 pending migrations: DB-side state unverifiable from all agent seats (human gate).
- SN-0781/SN-0782 renumber reconciliation (owning lanes).
- Why Workers Builds went silent on main (dashboard-side, cause unverified).
- Who/when removed the Supabase branch association (promotion-chain history).

---

## Receipts

- This report: branch `brain-build/learning-event-20261009` from tip `9aa04ab813c4b62e39ab58d131f7f80e6797ff49`; pushed and byte-verified; PR `docs(brain): learning event 2026-10-09`; merged under the Scorecard Law (five-step receipt on #1354 — no receipt, no merge).
- Sources: `~/memory/2026-10-09.md` (488 KB, full-day log), #1354 live tail (2,234 comments), 66 merged PRs in the Vancouver-day window, goal workspace hidden_files.
- Trash: flagged only. Nothing deleted, nothing pushed to main except this report's own merge.

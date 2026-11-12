# SN-2130 — The Instrument Is on Trial

**Status: VERIFIED ESSENCE — VERIFIED (verifier-sep-3; adjudication-sep-3; correction pass re-verified, re-verifier-sep-3).** Distilled from 14 raw notes by the sep-3 maker seat; independently verified by a different seat. Verified without correction (verifier-sep-3). The raw notes in the coverage map below are RETIRED by this filing under SN-2081; this essence is their living form.

## In a Nutshell

Every verdict is only as honest as the instrument that produced it — and instruments lie quietly: a battery can falsify its own later verdicts on the same bytes (SN-0356), a registry can agree with itself while disagreeing with everything else (SN-0361), thirty labels can cite one artifact (SN-0505), a gate can fabricate "nothing is executed" from a path bug (SN-0509). So the verifier's first subject is never the claim — it is the measuring tool: its identity model, its coverage, its platform, its stubs, and whether its verdicts were proven on the machine that renders them.

## Essence

The founding incident: a hand-built adversarial battery returned contradictory verdicts on the same bytes across sibling cases — the harness was the instrument, the harness was wrong, and its PASS was worthless in both directions (SN-0356). The durable moves from that night: a battery must be able to falsify its own verdicts, and a falsified verdict gets corrected in the same venue where it was published, never quietly (SN-0356). Identity is the next layer down. A content-hash audit cannot police identity drift: identity is the (SN-NNN, smart_note_id, filename) triple, every pair of legs asserted bidirectionally, with four drift classes — orphans in either direction between registry and capture store, captures missing the identity field, filenames lying about the identity inside — and legacy debt pinned as a monotonic ratchet, enumerated by name and dated, blocking only new drift (SN-0381). A registry that agrees with itself proves nothing: self-consistency is consistency with one surface; validate across surfaces (registry against tree against captures against board) before calling anything true (SN-0361).

The instrument includes the tool version: diagnosing a red with a branch's own exact-pinned tool is a phantom measurement when CI validates with main's current tool — pin every reproduction and repair to the tool version the gate itself uses, because a verdict from an older pinned tool is not evidence about what CI sees (SN-0429). It includes the frame: two seats argued the voice bakes in opposite directions because they audited different scopes; a read-only byte-level audit against the canonical manifest settled it (19/26 baked, 11 demo-bank MP3s confirmed, exactly 7 blocks missing) — pin the scope (manifest, directory, block set) before auditing, and keep the audit read-only, because re-rendering would have destroyed the evidence of what was missing (SN-0434). And it includes the credential layer: a 401 is not a key problem until proven — diagnose by layer (sanctioned request path first, credential resolution second, key identity last, naming which of the two credential paths failed), escalate once, never retry-loop, and never ask the human for raw keys (SN-0498).

Evidence identity is enforced at the data model, never assumed from labels: a scorer returned PASS on 30 "trials" that were one physical transcript, because the schema had no per-trial slice to distinguish 30 executions from one execution cited 30 times; the repair fails closed on same-path, relative-alias, symlink, and hardlink reuse, while genuinely distinct transcripts still PASS (SN-0505). Coverage is the same discipline pointed at scanners: a board scanner reading fixed pages 1–2 of a 350-comment board reported "no collision" while an active claim sat at comment 350, because the endpoint serves oldest-first — any scan whose claim depends on coverage must prove coverage on the same run, anchoring its window to the live count and failing closed on a moving snapshot (SN-0506).

Gates are instruments too, and their verdicts must be proven on the platform that renders them: a coverage gate's Windows path handling produced a false "only 0/14 edge functions are executed" on the Linux runner — a false "unproven" verdict is worse than no verdict, because it invites someone to delete real coverage; when your own audit mis-reports, fix the audit, never ship its output (SN-0509). Stubs are instruments: four harness bugs in two days each masqueraded as a product defect (a credential stub masking four guards, a stateless GET stub firing a guard on success, a missing .select(), an always-fresh INSERT row making the replay branch unreachable) — when a fired test blames the system, enumerate the harness seams before touching product code, and log the harness-fix-vs-product-fix ratio in the receipt (SN-0517). One platform is one blind spot: a repair green on the builder's Windows suite hid 3 real failures that a Linux review of the same suites found (945/3/11 → corrected 948/11; the pattern repeated on the next PR) — independence of the seat is not enough; the reviewer must bring a different instrument, and an environment blocker is a measurement gap, never green (SN-0525).

Attestation is where instrument dishonesty becomes load-bearing: two live runtimes returned failed verifications with independent_verification: true written as a literal (CV-04, a broken lineage attesting itself verified; CV-05, a contradicted LAW decision attesting itself verified, on the authority node). The finder did not fix them — what an authority node attests is its owner's truth decision — she made the lie executable (a test pinning the current bad behavior, so fixing the literal turns it red as the signal) and generalized with a scanner whose every hit carries a recorded verdict, never a silenced allowlist, because a verdict is auditable and a silenced rule is not (SN-0528). Finally, the proof subject itself is an instrument: a verification battery executes on bytes, and bytes not fingerprinted against the canonical source are unknown bytes — pin the tip via the refs API, pull the tarball at the exact SHA, verify file sizes or blob SHAs, and only then run (SN-0533). And verification itself means re-execution: an independent verifier who re-ran the graders and re-extracted the answers found the shipped graders defective (5 under-scores, 2 over-scores, an undocumented stats formula, a receipt whose split contradicted both the results file and the corrected tally) while the claims themselves survived on corrected data, equal-or-stronger — instrument defects are classified separately from claims, and evidence branches are frozen the moment they open, because evidence is immutable and graders are repairable and the two must never meet (SN-0586).

## What this settles

- A battery, gate, scanner, or stub is an instrument; its verdict is a claim about its own correctness first (SN-0356, SN-0509, SN-0517).
- Identity is the (key, internal id, storage name) triple, asserted bidirectionally; content-hash agreement is never identity proof (SN-0381). Cross-surface agreement outranks self-consistency (SN-0361).
- Reproduce with the tool version the gate uses; pin the audit's scope before auditing; keep evidence audits read-only (SN-0429, SN-0434).
- A 401 is diagnosed by layer — path, resolution, key identity — never by hunting for a different key (SN-0498).
- Evidence identity lives in the data model: N labels over one artifact must slice per label or refuse (SN-0505). Scans prove coverage on the same run or report nothing (SN-0506).
- Verification = independent re-execution on a different instrument; both platforms' verdicts are published side by side (SN-0525, SN-0586).
- Verification flags are computed from outcomes, never literals; known-open attestation defects are pinned by tests and recorded verdicts, never silenced (SN-0528).
- Fingerprint the bytes against the canonical source before any battery runs on them (SN-0533).

## Human

Every number this team trusts comes out of some tool — a test battery, a scanner, a gate, a grader. This essence is the hard-won knowledge that the tool itself is the first thing to doubt: tools carry stale pins, wrong scopes, platform bugs, fakes that are merely close, and flags hardcoded to "true." The craft collected here is how the team learned to put the instrument on trial before believing anything it says — and how much damage one unexamined instrument can do downstream before anyone notices.

## Child

Imagine a referee whose whistle sometimes blows when nobody fouled. Before you trust the score, you check the whistle. These notes are all the times the whistle was wrong: a ruler that measured differently on a different table, a scale that said "all good" because its sticker said so, thirty homework sheets that turned out to be photocopies of one. The rule the team learned: check the checker first — with a different checker, on the exact thing being checked.

## Grandma

Dear, it's the old wisdom about scales and thermometers: a number is only as good as the instrument behind it. A bathroom scale that flatters you is worse than no scale, because you'll act on it. The team learned to test the thermometer before treating the patient, to weigh with two different scales, and to never trust a gauge that reads "fine" because someone painted the needle there. Honest instruments, checked honestly — that's the whole secret.

## Naya

Before you cite any verdict, interrogate its instrument: Can the battery falsify itself (SN-0356)? Is identity asserted as a triple, bidirectionally (SN-0381)? Is the registry checked against other surfaces, not itself (SN-0361)? Is the tool the version the gate runs (SN-0429)? Was the scope pinned before the audit (SN-0434)? Is a 401 diagnosed by layer before any key changes (SN-0498)? Can N labels share one artifact in the schema (SN-0505)? Did the scan prove its window covered the newest item (SN-0506)? Was the gate's verdict proven on the runner's platform (SN-0509)? Are the stubs exact, or merely close (SN-0517)? Did a different instrument re-run it (SN-0525, SN-0586)? Is every trusted flag computed, never literal (SN-0528)? Were the bytes fingerprinted before the battery ran (SN-0533)?

## What It All Means

Fourteen notes, one inversion: the evidence stack's weakest layer is never the claim — it is the unexamined instrument under the claim. A cold reader holding only this essence can audit any verdict the fleet produces by auditing its instrument first, which is the single highest-leverage verification habit the corpus teaches.

## Why It Matters

A false PASS certifies fiction and a false "unproven" invites deletion of real coverage — both are worse than no verdict, and both come from instruments, not claims (SN-0505, SN-0509). The costliest failures in this block were not bad code but good code judged by bad instruments: a gate crying 0/14, a scorer passing photocopies, an authority node attesting its own contradiction (SN-0528). Every downstream decision — merges, promotions, scorecards — inherits the instrument's honesty, so instrument integrity is the multiplier on all other work.

## How It Connects

This essence is the evidence-side foundation for the block's other essences: CI verdicts get their semantics in essence-read-the-verdict.md (classification presumes the instrument questions here are already asked); law-as-code gates get their falsifiability bar in essence-law-without-a-machine.md; learning measurements get their number discipline in essence-learning-must-change-behavior.md. SN-0586's frozen-evidence rule connects forward to the trial-evidence machinery covered there (SN-0573). The relay contract — verify the pins, not the conclusions — is carried in essence-receipts-and-repairs.md (SN-0446), and deliberately not duplicated here.

## What Is In It For You

You stop being fooled by your own tooling. Apply the instrument-first checklist to any automated verdict in any system — test suites, dashboards, graders, scanners — and you will catch the failures that actually hurt: the green that certifies fiction, the red that condemns the innocent, the flag that says "verified" because someone typed true. The payoff compounds: every verdict you can trust makes every decision built on it cheaper.

## The Learning

The corpus learned that instrument defects masquerade as product defects (four harness bugs in two days, SN-0517), that dishonesty is usually structural rather than malicious (a schema that cannot distinguish labels from executions, SN-0505; a literal where a computation belonged, SN-0528), and that the correct response to a caught instrument is repair plus a pinned regression — never reporting its output, never silencing the finding (SN-0509, SN-0528).

## Coverage map — raw notes this essence covers (14)

SN-0356 · SN-0361 · SN-0381 · SN-0429 · SN-0434 · SN-0498 · SN-0505 · SN-0506 · SN-0509 · SN-0517 · SN-0525 · SN-0528 · SN-0533 · SN-0586

## Verification contract (for the verifying seat — falsify these)

1. **Coverage integrity:** exactly 14 IDs, all in the sep-3 block list, none duplicated in any other sep-3 draft essence, the covered-by-batch1 list, or the stands-alone list.
2. **Standing-authority exclusion:** this draft fails if any standing-authority note's substance (SN-0407, SN-0437, SN-0453, SN-0529, SN-0538, SN-0540, SN-0541, SN-0576) is absorbed as this essence's coverage; references under How It Connects are fine, distillation is not.
3. **Exact figures:** SN-0505's repair (PR #1668, merged as 3f1e6d78; 929 Python + 106 related tests); SN-0509's false verdict string ("only 0/14 edge functions are executed"); SN-0517's tier movement (59 → 67 of 147 guards, 40.1% → 45.6%); SN-0525's counts (945 pass / 3 fail / 11 skip → 948 pass / 11 skip); SN-0586's corrected tallies (t11 50/50 vs 0/50, p=1.08e-5, h=3.14; t14 40/40 vs 28/40, p=7.14e-4, h=1.16; receipt 6/4 vs results 7/3 vs corrected 9/1) — fail on any variant.
4. **Identity triple:** SN-0381's triple is exactly (SN-NNN, smart_note_id, filename) with four drift classes and the 17+1+5+1 measured debt; fail if reduced to "check IDs match."
5. **Attestation discipline:** SN-0528 must carry BOTH halves — the literal-flag defect (CV-04, CV-05, with nayanet-causal-verify and verified-ai-action as the correct patterns) AND the finder's restraint (pin the defect with a test; recorded verdicts, never a silenced allowlist); fail if either half is missing.
6. **Layer order:** SN-0498's diagnosis order is request path → credential resolution → key identity, with the two credential paths named; fail on any reordering.
7. **Anatomy:** all ten Full Smart Note sections present (In a Nutshell · Human · Child · Grandma · Naya · What It All Means · Why It Matters · How It Connects · What Is In It For You · The Learning) and **no machine view or machine section anywhere**. Fail on any missing section or any machine-view content.
8. **No-orphan check:** pick any five sentences in the Essence section at random; each must cite at least one covered SN ID, and the cited page must contain the claim.
# SN-2186 — Ratification Lives in the Artifact's Fields

**Status: VERIFIED ESSENCE — VERIFIED (verifier-oct-4, block PASS WITH CORRECTIONS; correction pass executed, re-verified, and closed by a different seat's second-pass confirmation — all retirement holds lifted).** Distilled from 5 raw notes by the oct-4 maker seat; independently verified by a different seat (12 essences VERIFIED, 2 VERIFIED-WITH-CORRECTIONS, both corrections executed and confirmed). Verifier verdict: VERIFIED (verifier-oct-4, against repo bytes). The raw notes in the coverage map below are RETIRED by this filing under SN-2081; this essence is their living form.

## In a Nutshell

Authority in this system is a property of artifacts and explicit words — never of messages, placements, or enthusiasm. A merge commit message claimed RATIFIED while the artifact's own fields said `ratified: false`; the fields were right (SN-840, carried by Batch 1 and pointed to below). A file's internal claim of `status=RATIFIED` is likewise only a claim: a pin requires `ratified_by == 'Shawn Vibert'` plus the DIRECTOR-RATIFIED envelope keys (SN-843). A constitution placed on a PR is CANDIDATE until the ratifier's explicit word — placed ≠ law, and no lane declares hierarchy between competing canons (SN-934). Around those cores sit the working machinery: an exclusion-precedent chain that keeps unratified specs out of the pin manifest by name (SN-884), a precedence rule that lets a dated standing directive supersede a roster (SN-833), and a backfill discipline that records pre-guard ratifications honestly as `kind=backfill`, never dressed as elevations (SN-876).

## Essence

**The envelope decides.** The spec-integrity manifest pins **RATIFIED projections only**. When the wrong pin landed — `0006-naya-calculator-v1.machine.json`, a CANDIDATE spec whose scorecard had verified that the pins matched but never *ran* the check it claimed to fix — the correction applied exclusion-with-reason, citing the precedent chain by name: **0003** (origin of the pattern) → **0013** (2026-10-06, citing 0003) → **0014** (2026-10-06, citing 0003) → **0006** (2026-10-09, citing 0003/0013/0014, correcting the pin). Four independent decisions, different days and runs, each naming its ancestor — that citation is the compounding mechanism: a lesson that governs a later decision *by name, in the decision's own record* is compounded intelligence; a lesson applied but not named dies with its run. The twin rule from the same incident: a scorecard claiming to fix a gate must **run** the gate on exact bytes and read the exit code; verifying the pins match is not verifying the check (that's what #1982 was; #1983 repaired it, and the mechanical river-completion alternative, #1984, was rejected as process theater) (SN-884).

**A claim inside the file is not machine ratification.** Pin eligibility is mechanical: `ratified_by == 'Shawn Vibert'` **and** the DIRECTOR-RATIFIED envelope keys present. Bare `status=RATIFIED` text is a claim about ratification, not ratification. When a claim fails, the exclusion *stays* but its reason is rewritten to the new tip's facts — a stale reason never rides forward — and the real check is verified on the exact new-tip bytes before anything merges; the repair's author does not merge their own repair PR (SN-843). This is the companion to Batch 1's SN-840: ratification lives in the artifact's status fields, and forbidden proxies are the commit message, the PR title, and chat — the fields are the artifact's own testimony, checked by machine rule (SN-843, SN-884).

**Placed is not law.** On 2026-10-10, a team execution order declared a 34-section Operating Protocol V2 "standing governing law" (6103222255) — while the accompanying constitution comment stated the boundary itself: the file is placed on PR #2210 but is **not law until Shawn says "ratify"**; V1 remains the ratified law (6103242856). The doctrine: PLACED (on a branch/PR) → CANDIDATE (declared by the placer) → RATIFIED (only at the ratifier's explicit word). There is never a vacuum and never a tie: the previously ratified law runs until superseded by ratification. **No lane declares hierarchy unilaterally** — when two candidate canons overlap (V2 vs the 45-law book), which governs which is itself a ratification question, belonging to the ratifier, however confident a lane feels. Execution orders carry the same boundary: an order citing authority it does not hold is executed as CANDIDATE — followed provisionally, recorded with the provenance caveat, never cited later as ratified doctrine. And auto-capture is not auto-ratify: Smart Notes, specs, scorecards, and PRs land as CANDIDATE by default — the capture pipeline's job is to preserve; the ratifier's job is to bless; collapsing them makes every draft a law and every law a draft (SN-934).

**Precedence resolves conflicts openly.** When authorities collide, the order is explicit: the director's standing directive (dated, in MEMORY.md) > the nine-team roster > a lane post. In the case that set the rule, a build assignment moved lanes per the 2026-10-08 directive, corrected *openly* — verbatim citation plus a falsification path — before the work hardened (five minutes in), with the displaced lane's work plan preserved and MEMORY.md updated the same tick (SN-833).

**Backfill honesty.** Eight pre-guard director ratifications (SN-016, SN-0340, SN-0399, SN-0400, SN-0408, SN-0459, SN-0522, MAGIC-001) entered the registry with `kind=backfill` — never `elevation` — carrying their real at-dates and verified hashes. The registry writer had silently dropped `elevation_history` on re-ingestion; the carry-over fix landed in `_update_registry_locked`, teeth-tested. And the audit CLI that guards this honesty never passes blind: exit 0 clean / 1 defects / 2 environment failure — there is no pass-when-blind path (SN-876).

## What this settles

- Manifest pins are RATIFIED projections only; CANDIDATE specs get exclusion-with-reason citing the 0003/0013/0014/0006 chain by name (SN-884).
- A scorecard claiming a gate fix must run the gate on exact bytes; pins-matching is theater (SN-884).
- Pin eligibility is mechanical: `ratified_by == 'Shawn Vibert'` + DIRECTOR-RATIFIED envelope keys; internal status text is a claim; failed claims keep the exclusion with a freshly rewritten reason (SN-843).
- PLACED ≠ LAW: candidate canons run provisionally under the previously ratified law; hierarchy between canons is the ratifier's call alone; auto-capture ≠ auto-ratify (SN-934).
- Precedence: dated standing directive > roster > lane post; corrections are open, cited, and fast (SN-833).
- Pre-guard ratifications record as `kind=backfill` with real dates and verified hashes; the audit has no pass-when-blind exit (SN-876).

## Human

This is the system's law about law. Words like "ratified" are load-bearing — products get pinned, gates get trusted, teams obey — so the system refuses to let those words travel by rumor. A commit message cheering "RATIFIED!" doesn't make it so; the document's own official fields do. A beautiful new constitution uploaded to a branch doesn't govern anyone until the one person with the authority says the word. And when old approvals are entered into the new registry, they're labeled honestly as backfill — history recorded as history, not promoted into something grander.

## Child

Imagine a permission slip. It only counts if the right grown-up signed it in the right box — not if someone wrote "SIGNED!" in big letters on the back, and not if the slip is just lying on the teacher's desk. A new rulebook sitting on the desk is just a *suggestion book* until the principal says "this is our rulebook now." And the old rulebook stays in charge until that exact moment.

## Grandma

It's deed-and-title law, dear. The house isn't yours because the seller said so at dinner; it's yours when the deed is executed with the right signatures in the right places. A draft will in a drawer changes nothing, the old will governs until a new one is properly executed, and nobody's nephew gets to declare which document outranks which. And when the clerk copies old records into a new ledger, she writes "copied from the old book" — she doesn't pretend they were issued yesterday.

## Naya

Before pinning anything: verify `status == RATIFIED` in the envelope, `ratified_by` by name, and the DIRECTOR-RATIFIED keys — never pin by filename resemblance (SN-884, SN-843). For anything CANDIDATE, write the exclusion-with-reason and cite the precedent chain in the decision record (SN-884). When a claim fails at a new tip, rewrite the exclusion reason to the new facts; verify the real check on exact tip bytes; don't merge your own repair (SN-843). Name every placed law's truth state in the same comment that places it; run the ratified law until ratification supersedes it; execute unverified-authority orders as CANDIDATE with the caveat recorded (SN-934). Resolve authority conflicts by the precedence order, correcting openly with verbatim citation before work hardens (SN-833). Record historical ratifications as backfill with real dates + hashes; keep the audit's no-pass-when-blind exits (SN-876).

## What It All Means

Five notes draw the boundary between *claiming* authority and *holding* it, at every surface where the two get confused: commit messages, file contents, branch placements, execution orders, and registry backfills. The common mechanism is to make authority a machine-checkable property of the artifact plus one human's explicit word — everything else is a claim, and claims get the CANDIDATE handling: provisional operation, provenance caveat, no downstream citation as law. This is also where the campaign's own stands-alone rule comes from: an essence may point at an authority instrument, but absorbing it would be exactly the category error these notes exist to prevent.

## Why It Matters

Authority inflation is the quiet catastrophe of any governed system: one CANDIDATE spec pinned as ratified teaches a calculator wrong law; one placed constitution treated as governing law forks the team's behavior; one backfill dressed as an elevation falsifies the registry's own history. For the reader, the portable lesson is that "who said so, where is it written in the artifact, and what is its exact state" are not bureaucracy — they are the difference between a rule of law and a rule of whoever spoke last, loudest, in a commit message.

## How It Connects

The artifact-fields rule's primary statement (SN-840) is carried by Batch 1 essence SN-2068 and is pointed to from here; SN-843 and SN-884 are its mechanism and its precedent chain. The director's own Tier-0/Tier-1 framing of law — one hard law, everything else living — stands alone as SN-901, and his decision procedure as SN-902; both are pointed to, not absorbed. The Living Ledger vision that gives ratification its purpose (every action carrying evidence) stands as SN-915, covered by Batch 1's SN-2074. The two-canons tension SN-934 holds open was first surfaced by the cold test in essence-proof-that-proves.md (SN-891, PACK-HOLE-03) — the same open constitutional question, named in this block's receipt as awaiting the ratifier.

## What Is In It For You

You get the three questions that dissolve most authority disputes in any organization: Is it in the artifact's official fields, or only in someone's message? What is its exact state — placed, candidate, or ratified — and who moved it last? And if two documents claim the crown, who is the *one* person allowed to settle it? Ask those before obeying any "new rule," and you will never again follow a draft as if it were law — or freeze a working rule because a draft exists.

## The Learning

The block's authority learning is that inflation never announces itself: the wrong pin's scorecard was diligent about everything except running the check; the execution order's overclaim came from a seat that *also* wrote the correct boundary in its companion comment. What compounded is the habit of treating authority as data: fields to verify, chains to cite by name, reasons rewritten at each new tip, and a ratification boundary that even urgency does not move. The precedent chain is the emblem — the law compounded precisely because each application *named* the last one.

## Coverage map — raw notes this essence covers (5)

SN-833 · SN-843 · SN-876 · SN-884 · SN-934

## Verification contract (for the verifying seat — falsify these)

1. **Coverage integrity:** exactly 5 IDs, all in the oct-4 block list, none duplicated in any other oct-4 draft essence, the covered-by-batch1 list, or the stands-alone list. (SN-840 is covered-by-batch1 via SN-2068 and must NOT appear in this or any other draft's coverage map.)
2. **Precedent chain enumerated in order:** 0003 → 0013 → 0014 → 0006, each with its citation relationship; fail if the chain is summarized as "prior exclusions" without the four members, or if any member is missing.
3. **Pin test mechanical:** the essence must state both pin conditions (`ratified_by == 'Shawn Vibert'` AND the DIRECTOR-RATIFIED envelope keys) and the forbidden-proxy rule (commit message / PR title / chat) via SN-843/SN-884; fail if ratification is anywhere described as inferable from a message.
4. **No truth-state inflation:** SN-934's V2 protocol must remain CANDIDATE-at-capture with V1 as the running ratified law, and the hierarchy question must remain the ratifier's open call; fail if the essence declares or implies a winner.
5. **Backfill list exact:** the eight pre-guard ratifications must be enumerated as recorded (SN-016, SN-0340, SN-0399, SN-0400, SN-0408, SN-0459, SN-0522, MAGIC-001) with `kind=backfill`, never "elevation"; fail on any substitution or relabeling.
6. **Standing-authority guard:** SN-901 and SN-902 may be pointed to but not absorbed; fail if their substance is restated as covered material.
7. **Anatomy:** all ten Full Smart Note sections present (In a Nutshell · Human · Child · Grandma · Naya · What It All Means · Why It Matters · How It Connects · What Is In It For You · The Learning) and **no machine view or machine section anywhere**. Fail on any missing section or any machine-view content.
8. **No-orphan check:** pick any five sentences in the Essence section at random; each must cite at least one covered SN ID, and the cited page must contain the claim.
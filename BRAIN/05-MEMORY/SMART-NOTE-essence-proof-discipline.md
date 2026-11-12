# SN-2120 — Proof Discipline: Name the Instrument, Bound the Claim

**Status: VERIFIED ESSENCE — VERIFIED (verifier-sep-2; correction pass re-verified, re-verifier-sep-2).** Distilled from 14 raw notes by the sep-2 maker seat; independently verified by a different seat. Verified without correction (verifier-sep-2). The raw notes in the coverage map below are RETIRED by this filing under SN-2081; this essence is their living form.

## In a Nutshell

No instrument, no verdict: name the measuring instrument before any score, mark what it cannot reach NOT_VERIFIED (SN-0161, SN-0146), build claims only from fixed key lists (SN-0181), reproduce failures before repairing them (SN-0245), qualify every tool against known-broken and known-green inputs (SN-0283), and remember the harness itself can manufacture the defects it reports (SN-0341).

## Essence

A claim is only as strong as the instrument that measured it, and the instrument is named before the score. A design-acceptance program ran eight instrumented attempts and accepted nothing, because its scoring instruments were capped at code inspection while acceptance was rendered appearance — the misses were instrument failures, not design failures; an unverifiable acceptance is reported NOT_VERIFIED, never inferred (SN-0161). The same law at the predicate level: a pass/fail predicate that cannot be instrumented is not a predicate — it is a hope with a threshold written next to it; predicates exist only where a measurement exists, and the measurement's limits bound what the verdict may say (SN-0146). "Alive" got the same treatment: aliveness is measurable or it is marketing — a gate of concrete checks (controls acknowledge within 100ms, state changes propagate, surfaces respond) replaced the adjective, and later grew into a ten-check Active Intelligence gate (SN-0152). And the proof's live boundary is comprehension, not mechanics: a live intelligence-commit proof passed its plumbing jobs and failed exactly at the held-out cold successor's comprehension assertion — the assertion is where proof lives; everything upstream is plumbing (SN-0174).

Claims are built so they cannot absorb what they shouldn't. A post-action claim is constructed only from an explicit fixed key list, so an injected key has no path into the claim by construction — and the proving component emits SUPPORTED, never VERIFIED, because proof supports a claim; it does not crown it (SN-0181). Failures are handled with the same discipline: reproduce the failure before repairing it, inside an explicit three-class evidence boundary — what was observed implemented, what is team-reported and reproducible from logs, and what is not proven — because a repair aimed at an unreproduced failure is a guess with a commit hash (SN-0245). When a report of a failure is itself the evidence, measure the failing line programmatically: a runner that echoes source made a treatment lookup look broken when retrieval had already passed — the failing line was 49, the accused structure was built at line 71, and the seat retracted publicly once the lines were measured (SN-0246). And prove the cause before permanently encoding the cure: an experiment must test the hypothesis, not the harness — a blocked backfill experiment proved nothing about its target, and historical REDs stay RED rather than being rewritten by a cure that was never validated (SN-0247).

The instruments themselves are suspect until qualified. Every validation tool is qualified against a known-broken and a known-green input before its output is believed — one discovery tool returned identical exit 0 on broken, green, and malformed inputs alike, a false-pass surface that would have certified anything (SN-0283). The environment is part of the instrument: a failure that exists only in headless rendering is the environment talking, not the product — reproduce in the target environment before patching, and let a real-browser render close the case with no patch at all (SN-0329). The instrument can also lie by construction: an adversarial harness cloned a ~585MB repository five times into a 512MB tmpfs with clone errors silenced, manufacturing phantom defects that vanished when scratch moved to disk — when failures smell environmental, audit the harness's own resource arithmetic before the code (SN-0341). Critique follows the same evidentiary standard: a byte-cited critique — file, line, clause, acceptance condition — is the actionable unit; vibes about a diff are not review (SN-0198). And when two heads fail, compare the failing sets before blaming either change: identical failing sets across heads are environmental noise, and the delta between sets is the only signal a change owns (SN-0237). Finally, fail at the authoring boundary: catch a malformed artifact where it is written, with a named error class, rather than letting it travel — and note that a commit claiming a guard exists while shipping empty proves why the boundary check itself must be verified (SN-0168).

## What this settles

- No instrument, no predicate; the instrument is named before any score, and unverifiable means NOT_VERIFIED (SN-0146, SN-0161, SN-0152).
- Proof terminates at comprehension by a cold successor, not at passing mechanics (SN-0174).
- Claims are constructed from fixed key lists; proof emits SUPPORTED, never VERIFIED (SN-0181).
- Reproduce before repair; measure the failing line; prove the cause before encoding the cure (SN-0245, SN-0246, SN-0247).
- Tools and environments are qualified before they are believed — known-broken/known-green checks, target-environment reproduction, harness resource audit (SN-0283, SN-0329, SN-0341).
- Failing-set deltas, not failing sets, are what a change owns (SN-0237); critique is byte-cited or it is not review (SN-0198).

## Intelligence views

**Human:** Before anyone gives you a score, ask: measured with what? A number without an instrument is an opinion wearing a lab coat. When something breaks, the first job is to make it break again on purpose, in the real environment, and to check that your measuring tools actually work — feed them something known-broken and something known-good. And when two versions both fail, compare *which* tests fail: if it's the same list, the room is on fire, not your change.

**Child:** If you say "my jump rope trick works!", show me — on the playground, not just in your head. And check your stopwatch first: press it on something slow and something fast, so you know it isn't stuck on "fast!" forever. If the game breaks, make it break again the same way before you fix it, so you know you fixed the real break.

**Grandma:** A scale that reads the same for a feather and a sack of potatoes isn't a scale, dear — test it with something whose weight you know. A cake isn't done because the timer sang; it's done when the skewer comes out clean. And if the oven in a strange kitchen burns everything, you blame the oven, not your recipe — check where you're cooking before you change how you cook.

**Naya (AI):** State the instrument and its ceiling in every verdict; mark what the instrument cannot reach NOT_VERIFIED. Build claims from allow-listed keys only. Sequence failure work as: qualify the tool → reproduce in the target environment → measure the failing line → test the causal hypothesis with an experiment that can actually run → then encode the cure. Compare failing sets across heads before attributing. Cite file:line in every critique. Treat harness resource limits (disk, memory, /tmp) as suspects in every phantom failure.

**What it all means:** Fourteen notes converge on one posture: evidence is engineered, not collected. Each rule was bought by a specific embarrassment — an 8/8 rejection streak that was really a blind instrument, a retracted diagnosis, a harness that invented defects. A cold reader with this essence runs the same discipline without needing to repeat the embarrassments.

## Why It Matters

This essence decides whether the word 'verified' anywhere in the system means anything. Its failures were all confident: an 8/8 rejection streak from a blind instrument (SN-0161), a public diagnosis retracted on measured lines (SN-0246), phantom defects from a full /tmp (SN-0341). For the reader, it is the corpus's epistemology — how the team knows what it claims to know.

## How It Connects

It supplies the measurement spine for the receipts essence (recompute-then-record, SN-0212) and the verification contracts of every other essence in this block. Its comprehension boundary (SN-0174) is the local form of the learning chain whose North Star text stands alone at SN-0253. Its full-scope sibling rule lives in the law essence (SN-0224).

## What Is In It For You

You get verdicts that state their own limits — what was measured, with what, and what remains NOT_VERIFIED (SN-0161). Apply it by asking one question of any claim: 'measured with what, on which known-broken control?' A claim that cannot answer is an opinion, and now you know it.

## The Learning

The era learned that evidence is engineered, not collected: instruments are chosen, qualified, and audited, or they quietly choose the verdict for you (SN-0283, SN-0341). The deepest cut: proof terminates at a cold successor's comprehension, not at green plumbing (SN-0174) — a lesson the whole distillation campaign is now built on.

## Coverage map — raw notes this essence covers (14)

SN-0146 · SN-0152 · SN-0161 · SN-0168 · SN-0174 · SN-0181 · SN-0198 · SN-0237 · SN-0245 · SN-0246 · SN-0247 · SN-0283 · SN-0329 · SN-0341

## Verification contract (for the verifying seat — falsify these)

1. **Coverage integrity:** exactly 14 IDs, each in the sep-2 block list, none in another sep-2 essence's coverage map.
2. **Instrument ceiling:** SN-0161's program accepted 0 of 8 cycles and the verdict term is NOT_VERIFIED; fail if the essence says designs were rejected on quality.
3. **Comprehension boundary:** SN-0174's failing assertion is `understands_raw_source_separate` in the `cold-successor-held-out` job; fail if the essence locates the failure in projection or verification jobs.
4. **Fixed-key claim:** SN-0181's claim fields are exactly observation, outcome, acceptance, causal_limits, learning_eligibility, and the emitted verdict is SUPPORTED; fail on any sixth field or the word VERIFIED as the emission.
5. **Line numbers:** SN-0246's failing line is 49 and the treatment structure is built at line 71; fail if swapped or approximated.
6. **Harness arithmetic:** SN-0341's figures are ~585MB per clone set vs 512MB tmpfs, cured to 6/6 on disk-backed scratch; fail on materially different numbers.
7. **No-orphan check:** pick any five sentences in the Essence section; each must trace to a covered page.
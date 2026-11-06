# SN-2115 — Qualify the Seam, Not the Story: Kernel Qualification Discipline

**Status: VERIFIED ESSENCE — VERIFIED (verifier-sep-1).** Distilled from 15 raw notes by the sep-1 maker seat; independently verified by a different seat (verifier-sep-1, block verdict PASS). Verified without correction. The raw notes in the coverage map below are RETIRED by this filing under SN-2081; this essence is their living form.

## In a Nutshell

A spec can read beautifully and still not be qualified: semantic pass and machine qualification are two explicit bars, and a strong CANDIDATE that hasn't passed the machine bar is an honest state, not a failed one (SN-025). Qualification is mechanical at every seam — front door fail-visible on unknown keys and fail-closed on malformed state (SN-037), audit evidence segregated from verdict tallies (SN-047), decided options re-verified at field level in a clean worktree (SN-058), bindings computed by whoever sees the bytes (SN-069), idempotency proven under replay rather than inferred from retries (SN-070), LEARN's four dimensions never collapsed (SN-071). Tests are qualification subjects too: xfails are proven, not wrapped (SN-072); a failing test may itself be the artifact (SN-076); reports are computed from the consuming state (SN-077). Freezes are immutable — retire and re-freeze, never mutate (SN-080); containment refuses rather than degrades (SN-081); evidence joins name the execution (SN-082); identities compare by platform semantics (SN-101).

## Essence

A spec can read beautifully and still not be qualified. The first bar: a semantic pass is not machine qualification — candidate specs are qualified at **two explicit bars**, and a spec that is a strong, honest, evidence-grounded semantic CANDIDATE still fails the fail-closed machine bar until the machine checks exist and pass (SN-025). When specs are amended while the kernel is frozen, the amendments can outrun the frozen kernel; the discipline is forward-gap accounting at lock: a read-only alignment check of amended spec against frozen code, with every gap named (one spec clean, the others carrying named deltas) rather than smoothed into "aligned" (SN-064).

At the kernel's boundaries, failure posture is specified, not improvised. The front door — the receive path where caller-supplied state enters — must be **fail-visible on unknown keys and fail-closed on malformed state**: surprises are surfaced loudly, and bad state never enters silently (SN-037). Evidence about a decision must never become an input to the decision: audit receipts are segregated from verdict tallies, so tampered evidence can never feed the counts that judge it (SN-047). A decided option is verified at the field level, not just by a green suite: after the Decision Protocol decides, the verifier independently re-checks the builder's exact commit in a clean ephemeral worktree, field by field, because suite-green proves the suite, not the fidelity of the implementation to the decision (SN-058).

Cryptographic responsibility follows eyesight: bindings are assigned at the observing layer — whoever sees the bytes computes the binding (`inputs_hash`, `executed_at`) — and no layer invents what the producer already carries (SN-069). Replay safety is proven, not argued by analogy: retry-on-conflict is not idempotency — a uniqueness retry proves one allocation, not one execution, and the ACT seam is qualified under replay, conflict, concurrency, interruption, and persistence failure (SN-070). LEARN's verdicts are never collapsed: epistemic state, adoption, lifecycle, and transfer maturity are four separate dimensions and four separate verdicts — collapsing them into one score destroys exactly the information qualification exists to produce (SN-071).

Tests themselves are qualification subjects. An expected-failure wrapper can manufacture a false green: wrapping an xfail assertion in `pytest.raises` made the test pass and produced an XPASS(strict) mirage — so prove the xfail (let it fail as designed and show the failure), don't wrap it (SN-072). And a failing test can be the artifact under examination: a conformance test claiming the runtime did not consume the calculus output was itself defective — it evaluated a substituted candidate on a different node — so defect reproduction is single-variable, and when the test is the artifact, the retraction ships with a requalification, not a shrug (SN-076). Reports are computed from the consuming state, not a reconstructed local: a cold-reconstruction that builds recovered state into a local object and computes a green-looking report from that local proves nothing about the real state — false-green restoration is the defect class, and the report must be computed from the state that will actually be consumed (SN-077).

Frozen evidence and platform limits close the set. Frozen evidence is immutable once frozen — including frozen mistakes: a package frozen from code lacking the `inputs_hash` binding is retired explicitly and re-frozen, never mutated inside the freeze (SN-080). Containment never degrades to fit the platform: when a required containment primitive (e.g. `os.O_NOFOLLOW`) does not exist on the platform, the correct answer is refusal before mutation — never a weaker fallback wearing containment's clothes (SN-081). Execution identity is not content identity: two receipts can agree on every content-addressable field — same decision id, same artifact bytes, same hash — and still be different runs, so evidence joined across runs names the execution, not just the artifact (SN-082). And at authority boundaries, identity comparisons use the platform's semantics, not the language default: GitHub repository identity is effectively case-insensitive, so a case-sensitive `==` lets a casing variant masquerade as a distinct owner target — normalize-then-compare by the platform's canonicalization rules, with the regression test carrying the adversarial casing variant (SN-101).

## What this settles

- Two bars, kept distinct: semantic pass ≠ machine-qualified; CANDIDATE is an honest state, not a failed one (SN-025).
- Amended specs vs frozen kernels produce named forward gaps, never "aligned" by courtesy (SN-064).
- Boundary posture: fail-visible on unknown keys, fail-closed on malformed state (SN-037); audit evidence never feeds verdict tallies (SN-047); decided options verified field-level at the exact commit (SN-058).
- Bindings are computed by whoever sees the bytes (SN-069); idempotency is proven under replay conditions, never inferred from retries (SN-070); LEARN's four dimensions are never collapsed (SN-071).
- Xfails are proven, not wrapped (SN-072); failing tests are themselves suspects — single-variable reproduction, retract with requalification (SN-076); reports compute from consuming state (SN-077).
- Freezes are immutable — retire and re-freeze, never mutate (SN-080); containment refuses rather than degrades (SN-081); evidence joins name the execution (SN-082); identity compares by platform semantics (SN-101).

## Human

Building the machine's brain taught the team how strict "checked" has to be. A specification that reads well isn't qualified until machines can test it. A test that "passes" might be wrapped so it can't fail. A report can look green because it was computed from a copy, not the real thing. A frozen record stays frozen even when it's wrong — you retire it openly and freeze a corrected one. And when the platform can't do something safely, the machine refuses instead of quietly doing it less safely.

## Child

Imagine checking a robot's homework with a really strict checklist. The story can sound great, but the checklist has to pass too. If a test is supposed to fail and you wrap it in a blanket so it "passes," that's cheating. If a saved game is frozen, you don't sneak in and change it — you save a new one and say why. And if the playground doesn't have the safety fence, you don't pretend a rope is a fence — you don't play that game there.

## Grandma

Dear, it's craftsmanship standards. Work is checked against the drawing, measurement by measurement, not by whether it looks finished. Sealed records stay sealed. Safety equipment is never replaced with something that merely looks similar. And when two receipts look identical, you still check whether they came from the same job — papers can match while the work differs.

## Naya

Qualify at both bars and name which one a subject passed (SN-025); run the spec-vs-kernel alignment check read-only and publish the gaps (SN-064). Build boundaries fail-visible/fail-closed (SN-037), segregate audit receipts from tallies (SN-047), and re-verify decided options at field level in a clean worktree (SN-058). Assign every binding to the layer that sees the bytes (SN-069); prove idempotency under replay, conflict, concurrency, interruption, and persistence failure (SN-070); report LEARN's four dimensions separately, always (SN-071). Prove xfails by their failure (SN-072); reproduce defects single-variable and suspect your own test first-class (SN-076); compute reports from the consuming state (SN-077). Retire-and-refreeze, never mutate (SN-080); refuse where containment primitives are absent (SN-081); join evidence by execution identity (SN-082); normalize identities by platform semantics before comparing (SN-101).

## What It All Means

Fifteen notes are the qualification craft of the kernel era: how a claim about a component becomes a verdict a stranger can trust — two bars, honest boundaries, tests that can fail, reports from real state, freezes that hold, and refusals that stay refusals. A cold reader holding only this essence can still qualify a seam the way these notes demand.

## Why It Matters

Qualification is where "we built it" becomes "it deserves trust" — and every shortcut here is invisible until it matters: a wrapped xfail, a report computed from a copy, a degraded containment fallback all look exactly like rigor from the outside (SN-072, SN-077, SN-081). For the reader, this essence is why a PASS from this system names its bar, its seam, and its limits — a verdict you can price, not a vibe you must trust.

## How It Connects

This is essence-evidence-law.md at component depth: its clean-room, exact-SHA verification (SN-028) is the same act as SN-058's field-level re-check, and its post-merge-at-the-pin rule (SN-061) is the merge-scale form of SN-077's consuming-state rule. The seams qualified here are the ones essence-composition.md then proves connected — SN-085's trust seam, SN-088's composition seam, SN-093's handoff trace all presume components that passed these bars. Its refusal discipline (SN-081) is the engineering form of the gate grading in essence-decide-on-evidence.md (SN-079): a refusal is the system working.

## What Is In It For You

You get verdicts with denominations: every PASS states which bar, which seam, which conditions — so you can tell a semantic compliment from a machine qualification at a glance. Apply the two-bar question to anything presented as "checked": checked *how*, by *what mechanism*, under *which hostile conditions*? And when a system refuses instead of degrading, you can recognize it as the safety working, not the software failing.

## The Learning

The kernel era taught the team that the test apparatus is part of the system under judgment: tests manufacture false greens (SN-072), tests are themselves defective artifacts (SN-076), reports lie by computing from copies (SN-077). The durable change: qualification now audits the instruments with the same suspicion as the subject — prove the xfail, suspect the test, compute from the consuming state — and a frozen record's *wrongness* is preserved and retired openly rather than edited away (SN-080).

## Coverage map — raw notes this essence covers (15)

SN-025 · SN-037 · SN-047 · SN-058 · SN-064 · SN-069 · SN-070 · SN-071 · SN-072 · SN-076 · SN-077 · SN-080 · SN-081 · SN-082 · SN-101

## Verification contract (for the verifying seat — falsify these)

1. **Coverage integrity:** exactly 15 IDs, all in the sep-1 block list, none duplicated elsewhere in this block's accounting. Note: SN-025's two-bars rule also appears in compressed form in Batch-1 essence SN-2069's nutshell; the verifier should confirm this draft carries the fuller teaching (the CANDIDATE-state semantics) and record the overlap rather than fail the draft for it.
2. **Front-door postures:** SN-037 pairs fail-*visible* with unknown keys and fail-*closed* with malformed state; fail if the essence swaps or merges the pairings.
3. **Four dimensions:** SN-071's LEARN dimensions are epistemic state, adoption, lifecycle, transfer maturity; fail on any renamed, merged, or dropped dimension.
4. **Xfail mechanism:** SN-072's false green arose from wrapping in `pytest.raises` producing XPASS(strict); fail if the essence bans xfail itself rather than the wrapping.
5. **Consuming state:** SN-077's defect is computing the report from a reconstructed local (`fresh = KnowNode()`) instead of the consuming state; fail if the essence states the rule without the mechanism.
6. **Containment refusal:** SN-081's primitive is `os.O_NOFOLLOW` and the required behavior is refusal before mutation; fail if the essence permits a documented weaker fallback.
7. **Identity semantics:** SN-101's repair is normalize-then-compare under the platform's (GitHub's) case-insensitive identity, with the regression test carrying the casing variant; fail if the essence recommends stricter-than-platform comparison as safer.
8. **Anatomy:** all ten Full Smart Note sections present (In a Nutshell · Human · Child · Grandma · Naya · What It All Means · Why It Matters · How It Connects · What Is In It For You · The Learning) and **no machine view or machine section anywhere**. Fail on any missing section or any machine-view content.
9. **No-orphan check:** pick any five sentences in the Essence section at random; each must cite at least one covered SN ID, and the cited page must contain the claim.
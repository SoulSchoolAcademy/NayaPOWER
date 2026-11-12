# SN-2116 — Composition Is Proven Handoff by Handoff

**Status: VERIFIED ESSENCE — VERIFIED (verifier-sep-1).** Distilled from 10 raw notes by the sep-1 maker seat; independently verified by a different seat (verifier-sep-1, block verdict PASS). Verified without correction. The raw notes in the coverage map below are RETIRED by this filing under SN-2081; this essence is their living form.

## In a Nutshell

Components can each be excellent while the organism does not exist — composition is proven only through the default wiring, with genuine data, handoff by handoff. Trust properties must be invariants, not conventions: a store anyone in-process can write makes resolve-then-trust prove nothing about origin (SN-085). Qualification subjects are frozen and fetchable (SN-086); fixture substitution at a claimed seam voids the integration claim (SN-088); a PASS on receipt family X never qualifies family Y (SN-090); contract mismatches are resolved at the source under the five-class binding taxonomy, with UNKNOWN as a complete binding (SN-091). Findings name their consequence class, gap tests self-invalidate, traces stop at the first exact failing handoff, and semantic gaps are named — never invented across (SN-092, SN-093). Boundary fixes compose at the consumer from the producer's sealed facts (SN-095), data bridges belong to the composition root and transport without judging (SN-096), and import-still-red proves the missing seam lives in the host (SN-102).

## Essence

Components can each be excellent while the organism does not exist. This essence is the record of learning that — seam by seam, at exact SHAs, with genuine data — and the disciplines it produced begin with the trust seam. "Append-only" enforced by a method is a convention, not an invariant: VERIFY's receipt store is a plain dict, and any same-process holder can write a forged VERIFIED_PASS receipt directly into it before a resolver reads it — so resolve-then-trust establishes nothing about origin (SN-085). The repair pattern is structural, not disciplinary: consume the resolved receipt, never the caller's object; make the resolver construction-owned so callers cannot substitute it; compare on an explicit allowlist that includes `subject_ref`; refuse stale and REOPENED receipts; lock fixture mode so it cannot be enabled accidentally; and prove ownership through id format, issuer, and structural fields (SN-085). When an adversarial review falsifies a design's core assumption, the falsification stays in the record — the three-line counterexample is worth more than the ten pages of design around it (SN-085).

Qualification requests obey a fetchability law: never name an unpushed local commit — bytes no other lane can fetch — as a qualification subject. Freeze the subject instead: candidate SHA plus branch plus byte digests of every file the proof depends on, with the verdict bound to that SHA and explicitly not following the branch tip; if you named something unfetchable, withdraw and re-issue rather than editing in place (SN-086).

The integration law follows: **fixture substitution voids integration claims**. The LEARN intake seam was genuinely verified — and the "nine nodes working together" test proved nothing about the organism, because it built LEARN with `allow_fixture_intake=True` while the real constructor builds it with no resolver. The integration seam is the default composition — plain `Kernel()`, no monkeypatch, no node replacement, no fixture flags; a test that substitutes fixture behavior at a claimed seam is fixture-only evidence and stops being cited for the organism claim (SN-088). Proof scope is equally strict across families: a PASS on receipt family X never qualifies receipt family Y — machinery proven 14/14 on kernel `demo-001` receipts proved nothing about the Demo-1 ACT receipt target, and the correct output at the first required field with no authoritative source is a fail-closed BLOCKED, with downstream steps reported as cancelled, not skipped (SN-090).

A contract mismatch is resolved at the source, never by widening the contract and never by synthesizing fields. Every field of a binding manifest carries one of five provenance classes — **RECEIPT-BOUND** (exact receipt bytes), **SOURCE-BOUND** (a named authoritative external source, with the non-claim stated where run-specific proof is missing), **WRITER-ASSIGNED** (allocated by the canonical writer at insert), **EXPLICIT-EMPTY** (a declared no-claim state — manufacturing a value there would be value laundering), or **UNKNOWN** (a kept, honest binding; "keep UNKNOWN rather than guessing" is a complete completion of a blocked field) — and the completed package is proven end-to-end through the canonical path, never by reconstruction (SN-091).

Honest reporting of gaps is a method of its own. Name the consequence class before the headline: a working fail-closed default blocking a genuine path is a *composition gap*, not a security defect or a regression — misclassification corrupts triage and trains the board to flinch (SN-092). Design gap tests to self-invalidate: assertions that the gap exists (resolver is None, no accessor) fail by design the moment the wiring lands, forcing requalification instead of going stale, and the future acceptance test ships alongside the finding (SN-092). And state the limits you will not paper over — an unkeyed hash cannot distinguish a self-consistent rehashed forgery from a genuine emission under same-process attack; that is a documented threat-model limitation, not a defect to imply away (SN-092).

End-to-end proof is a trace, not a vibe: publish the per-handoff table, stop at the first exact failing handoff with its exact error and evidence-established root cause, and mark every downstream step BLOCKED or NOT CLAIMED — never synthesize outputs to complete the trace (SN-093). Classify the gap you find: wiring gaps you close; semantic gaps you stop at and name — when VERIFY's genuine receipts carry no `outcome.lesson` and LEARN's extract requires one, closing the seam needs a *semantic design decision*, not a wiring fix, and the cycle stops rather than inventing across the boundary (SN-093). The resolution of that very gap teaches where fixes live: **compose at the consumer** — VERIFY speaks `learn_baton` (facts: expected vs actual, evidence, acceptance, causal status); LEARN derives the lesson from those sealed facts (eligibility = `may_use` non-empty; the lesson = the verified claim itself), because teaching the producer to emit pre-formed lessons would move authorship across the boundary and invert the separation — authorship stays in the author, trust stays in the seal (SN-095). And where a declared graph edge carries no data — `EVOLVE.observe()` had zero callers; edges were ordering constraints, not plumbing — the bridge belongs to the composition root: `Kernel.promote_learning_to_evolution(learning_id)` constructs the real gap dict and transports it, without judging whether every learning qualifies as a gap; that semantic question stays documented and with the caller (SN-096).

The experiment that proves a missing seam lives in the host, not the package: import the candidate package into a disposable host branch and re-run the RED test — if it stays red, the gap is in the host's integration seam; stop patching the package and build the smallest real host seam, on the disposable branch, without moving the thing being measured (SN-102).

## What this settles

- Trust properties must be invariants, not conventions; resolve-then-trust against a mutable store establishes no origin (SN-085).
- Qualification subjects are frozen and fetchable — SHA + digests, verdict bound to the SHA; unfetchable references are withdrawn, not edited (SN-086).
- Integration is proven only through the default composition; fixture substitution reclassifies the evidence as fixture-only (SN-088).
- Proof scope binds to the specimen family exercised; the first missing authoritative field stops the qualification, fail-closed (SN-090).
- Contract mismatches resolve by source-finding under the five-class binding taxonomy; UNKNOWN is a complete binding; contracts are never widened and fields never synthesized (SN-091).
- Findings name their consequence class, ship self-invalidating gap tests, and state their limits (SN-092); traces stop at the first exact failing handoff and never invent past a semantic gap (SN-093).
- Boundary fixes compose at the consumer from the producer's sealed facts (SN-095); data bridges belong to the composition root and transport without judging (SN-096).
- Import-still-red ⇒ the seam is missing in the host; build the host seam (SN-102).

## Human

This is the story of discovering that a machine whose every part passed its tests still didn't work as a whole — because the parts were connected by promises instead of plumbing. The lessons: a lock that depends on everyone behaving is not a lock; a test that swaps in fake parts proves nothing about the real machine; proof about one kind of receipt says nothing about another kind; when a form asks for a fact nobody has, you write "unknown" — you never make one up; and when you trace a chain of handoffs, you stop at the first real break and say so, instead of pretending the rest worked.

## Child

Imagine a relay race where each runner is super fast. That doesn't mean the team finishes — someone has to actually pass the baton! If a runner practices with a pretend baton, that doesn't prove the real pass works. If a box on the form asks for something nobody knows, you write "nobody knows" — you never make up an answer. And if the baton gets dropped at the third pass, you say "dropped at the third pass," not "great race."

## Grandma

Dear, it's the difference between good parts and a good machine. Locks must be real locks, not habits. Tests must use the real thing, not a stand-in. When a record lacks a fact, the honest word is "unknown," written plainly — inventing one is a kind of forgery. And a careful report names exactly where the chain broke and stops there, rather than painting the whole chain gold.

## Naya

Audit every trust seam for invariant vs convention before relying on it (SN-085). Freeze fetchable subjects with digests and bind verdicts to SHAs (SN-086). Prove composition through the bare default constructor; reclassify fixture-substituted tests as fixture-only (SN-088). Name the specimen family of every proof artifact; fail closed at the first unsourceable field (SN-090). Bind every field by provenance class and resolve mismatches at the source (SN-091). Classify consequences honestly, ship gap tests that self-invalidate, and publish your limits (SN-092). Trace handoff by handoff; stop at the first exact failure; classify wiring vs semantic before touching anything (SN-093). Fix boundaries at the consumer from sealed producer facts (SN-095); give bridges to the composition root, transporting without judging (SN-096). When a seam is suspected missing, run the import-still-red experiment on a disposable branch (SN-102).

## What It All Means

Ten notes are the organism-level evidence craft: how separately-true parts become a proven whole — or an honestly-reported gap. A cold reader holding only this essence can still run a qualification, an integration proof, or a contract resolution the way these notes demand, and can recognize each named way such proofs go fake.

## Why It Matters

Composition is where complex systems lie to themselves most fluently: every part green, the whole unproven, and the gap papered over with fixture wiring and borrowed proof (SN-088, SN-090). For the reader, this essence is the discipline that makes "the system works" a traceable claim — handoffs enumerated, gaps named at their exact location, unknowns written as unknowns — instead of an impression formed by adding up green badges.

## How It Connects

Composition presumes essence-qualify-the-seam.md: only components that passed its two bars are worth wiring, and its consuming-state rule (SN-077) is the per-component form of this essence's genuine-data requirement. The trust seam here (SN-085) is bounded by the seal scope of essence-the-mirror.md (SN-0111) — consistency, not authorship — and the UNKNOWN binding class (SN-091) is the contract form of the decision discipline in essence-decide-on-evidence.md (SN-083). The nine nodes being composed are the machinery of essence-the-foundation.md (SN-002); the director's standing board protocol under which these traces were reported stands alone as SN-0109.

## What Is In It For You

You get wholes that are actually whole: when this system claims its parts work *together*, the claim comes with the trace — every handoff driven with real data, the first failure named exactly, the rest honestly marked unproven. Apply the pattern to any integrated claim: demand the default configuration, genuine inputs, the specimen family the proof actually exercised, and the per-handoff trace. Anything less is parts, wearing a whole's clothes.

## The Learning

The corpus's hardest September lesson was that green parts compose into nothing by default: edges in a graph are ordering declarations, not plumbing (SN-096); fixtures at the seam silently void the organism claim (SN-088); proof borrowed across families is misattribution (SN-090). The behavior change: integration claims are now made only from default-composition traces, gaps are reported as first-class results with consequence classes (SN-092), and "blocked, not claimed" became an honorable terminal state instead of a failure to hide.

## Coverage map — raw notes this essence covers (10)

SN-085 · SN-086 · SN-088 · SN-090 · SN-091 · SN-092 · SN-093 · SN-095 · SN-096 · SN-102

## Verification contract (for the verifying seat — falsify these)

1. **Coverage integrity:** exactly 10 IDs, all in the sep-1 block list, none duplicated elsewhere in this block's accounting.
2. **Trust-seam repairs:** SN-085's approved change set (consume the resolved receipt; construction-owned resolver; allowlist including `subject_ref`; refuse stale/REOPENED; locked fixture mode; ownership via id format, issuer, structural fields) — fail on any dropped element.
3. **Family scope:** SN-090's pair (kernel `demo-001` family proven 14/14; Demo-1 ACT family unqualified) and the cancelled-not-skipped rule for downstream steps; fail if the essence lets any cross-family citation stand.
4. **Five classes:** SN-091's taxonomy (RECEIPT-BOUND / SOURCE-BOUND / WRITER-ASSIGNED / EXPLICIT-EMPTY / UNKNOWN) verbatim, with EXPLICIT-EMPTY's "value laundering" rationale and UNKNOWN's terminal status; fail on any renamed or merged class.
5. **Fixture mechanism:** SN-088's voiding mechanism is the fixture flag at the composition seam (`allow_fixture_intake=True` vs the default constructor); fail if the essence generalizes it to "fixtures are bad" without the seam condition.
6. **Consequence classes:** SN-092's classification (composition gap, not security defect/regression, for a working fail-closed default) and the self-invalidating test design; fail if either is missing.
7. **Trace discipline:** SN-093's trace stopped at handoff 6 (LEARN extract; `no lesson extractable`) with steps 7–9 BLOCKED/NOT CLAIMED; fail if the essence implies the cycle completed.
8. **Bridge contract:** SN-096's bridge is `Kernel.promote_learning_to_evolution(learning_id)`, transports without judging; fail if the essence assigns the bridge to an endpoint node or lets it decide the learning-is-a-gap question.
9. **Anatomy:** all ten Full Smart Note sections present (In a Nutshell · Human · Child · Grandma · Naya · What It All Means · Why It Matters · How It Connects · What Is In It For You · The Learning) and **no machine view or machine section anywhere**. Fail on any missing section or any machine-view content.
10. **No-orphan check:** pick any five sentences in the Essence section at random; each must cite at least one covered SN ID, and the cited page must contain the claim.
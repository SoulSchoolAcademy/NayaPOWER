# NayaPOWER Node Specs 2–9 — Independent Scorecard V1

**Reviewer:** Naya 2 (independent review lane — spec quality, not implementation fidelity)
**Date:** 2026-10-01
**Sources reviewed:** the eight uploaded PDFs (LAW, ACT, KNOW, PROVE, CONNECT, VERIFY, LEARN, EVOLVE),
`SMART-LINKS-NAYA-BIRTH-V1.md` (branch `naya/node-genome-aaa-v1`), `NAYA'S BIRTHDAY 2026 09 27.md` (main).
**Status of all eight specs:** CANDIDATE. "Final Organ Lock" = normative-target lock, NOT ratification.
Constitutional/EVOLVE-charter ratification remains human-only.

**Scoring dimensions:** Effectiveness (completeness, precision, executability as a spec) /
Usefulness (value to tonight's node build) / Alignment (fit with NayaPOWER vision, organism,
governance law). Scale 0–10. Overall = mean, rounded to one decimal.

---

## Node 2 — LAW — 9.0 / 9.0 / 9.0 → **9.0**

**Strongest features.** Constitutional gate with four admissibility states (AUTHORIZED / DENIED /
REQUIRES_CONFIRMATION / AMBIGUOUS, plus EXPIRED / REVOKED / OUT_OF_SCOPE outcomes); exact scope,
consent, expiry, revocation and receipts; capability/retrieval/graph edges never create authority;
never executes and never self-ratifies. The state machine is executable and the failure semantics
are fail-closed.

**Gaps / conflicts.** No explicit subordination clause to Prime 1 / Amendment 0002 (ratified
2026-09-30). The spec's four-state gate structure is consistent with the ratified model (four-state
kept over binary), but the reconciliation should be one written line, not an inference. Machine-exact
schema for the admissibility states vs the `naya_kernel` LAW interface still to be confirmed by the
builder.

**Corrections before lock.** Add: "This spec operates under Amendment 0002 (Prime 1, the Judgment
Rule); where this spec and Prime 1 conflict, Prime 1 governs."

## Node 3 — ACT — 9.0 / 8.5 / 9.0 → **8.8**

**Strongest features.** Governed execution from exact LAW authorization; smallest sufficient action;
target/parameter/Door binding; idempotency keys; bounded retries; rollback plans; observations;
"an execution receipt is not verified success" — the ACT≠OUTCOME separation is load-bearing for the
whole organism.

**Gaps / conflicts.** Door taxonomy needs canonicalization against the existing runtime registry.
Retry/rollback interplay with downstream VERIFY outcomes (who declares a retry exhausted vs a
regression) is under-specified at the seam.

**Corrections before lock.** Name the retry-exhaustion → VERIFY → LEARN escalation path explicitly;
bind the Door vocabulary to the canonical registry revision.

## Node 4 — KNOW — 8.5 / 8.5 / 9.0 → **8.7**

**Strongest features.** Durable memory and meaning through Intelligent Blocks with provenance,
ownership, temporal state, supersession and privacy; "stored or retrieved does not mean verified,
applicable or authorized" — the MEMORY≠TRUTH law, correctly placed.

**Gaps / conflicts.** CONNECT's own discrepancy list flags that live KNOW is stale against the
Graph V2 source — the KNOW spec should acknowledge the migration boundary. The Intelligent Block
machine schema vs existing Supabase tables needs a reconciliation note (builder's lane, but the spec
should mark the seam).

**Corrections before lock.** Add a "migration boundary" section: what happens to pre-V2 blocks,
who re-certifies them, and what UNKNOWN means for unmigrated content.

## Node 5 — PROVE — 9.0 / 8.5 / 9.0 → **8.8**

**Strongest features.** Bounded epistemic assessment; claim strength cannot exceed evidence strength;
proof obligations set by the weakest critical requirement; contradiction, scope, time, independence
and production-proof distinctions; proof never creates authority. This is the epistemic conscience of
the organism, and it is precise.

**Gaps / conflicts.** History matters here: the runtime PROVE carried an inspect-time defect
(fixed by #1120). The spec is sound; the lesson is that the spec should name the
inspect-time/run-time boundary even more explicitly so a future implementation cannot reintroduce a
time-bomb by accident.

**Corrections before lock.** Add an adversarial test: "a PROVE implementation that passes at import/
inspect time but degrades at run time must fail acceptance" — make the #1120 lesson structural.

## Node 6 — CONNECT — 9.0 / 9.0 / 9.0 → **9.0**

**Strongest features.** The five distinctions (related ≠ relevant ≠ applicable ≠ true ≠ authorized);
retrieval ≠ authority; graph edge ≠ permission; similarity discovers candidates but never establishes
trust; bounded cycle-safe traversal that cannot grant transitive truth; exclusions require
machine-readable reasons; historical relationships stay reconstructable. The proposed reconciliation
(NOT_APPLICABLE → EXCLUDED, UNKNOWN → VISIBLE_NON_STEERING, APPLICABLE + matching task class →
STEERING_ELIGIBLE) resolves the fixture/selector disagreement without silently promoting UNKNOWN —
exactly right. The spec's self-identified discrepancy list (proposed contracts 08/09/21, Smart Link
drift, schema vocabulary vs Graph V2's 22 relationship types, V1 seed gaps, UNKNOWN-applicability
disagreement, unenforced task_classes, PROVE→CONNECT/CONNECT→VERIFY topology, stale live KNOW,
unproven behavioral influence, SUPERSEDES direction, CAUSED-by-VERIFY) is a strength: it tells the
builder precisely what is open.

**Gaps / conflicts — Contract 08 / Smart Links.** Checked 2026-10-01:
`naya/node-genome-aaa-v1:NAYANODE/SMART-LINKS-NAYA-BIRTH-V1.md` (blob `64117f80`) pins "Current HEAD"
as `4533489d353582b40fe567c47aaec93a9814cd2b`, but the live branch HEAD is
`01a410df8bdb760f79c65989087605c3fedf53eb` ("replace static Supabase JWT proof with GitHub OIDC
cold runtime proof", 2026-09-28). The document violates its own rule — use the declared authoritative
current revision. Fold into Contract 08: a Smart Link index that pins a stale HEAD is a stale
doorway, and per the spec's own law it must be re-pinned or marked STALE, never silently trusted.
The doc's older `kernel_behavior_engine.py` references also need reconciliation against the current
`naya_kernel` implementation. Note the doc gets the deeper point right: a link proves an artifact
exists, not that it is verified — consistent with the Smart Link rule (doorway/projection, not
authority or proof).

**Corrections before lock.** Re-pin or mark STALE the Smart Links index; reconcile its kernel
references; add the machine-exact SUPERSEDES direction sentence; confirm CAUSED edges are
VERIFY-established (CONNECT must not mint them).

## Node 7 — VERIFY — 8.5 / 8.5 / 9.0 → **8.7**

**Strongest features.** Behavioral proof over existence proof; the causal inference ladder;
counterfactual discipline; behavioral retention (the learning must change behavior, not just be
stored); no self-verification — the verifier must be independent of the claimant.

**Gaps / conflicts.** The independence requirement is a process constraint as much as a spec
constraint: tonight the builder and the verifier are different seats, which satisfies it, but the
spec should state the independence criterion in machine-checkable form (distinct identity, distinct
evidence path, no shared mutable state). Causal claims need the CONNECT handoff confirmed —
CONNECT routes context, VERIFY establishes causality; the topology reconciliation CONNECT flags
applies here too.

**Corrections before lock.** Write the independence criterion as an acceptance test, not prose;
reference the PROVE→CONNECT→VERIFY topology decision once it is made.

## Node 8 — LEARN — 8.5 / 8.5 / 9.0 → **8.7**

**Strongest features.** Verified lessons with explicit applicability scoping; no silent transfer
across task classes; calibration tracking; the VALUE_RECALIBRATION seam to EVOLVE is concrete and
correct — `LEARN_CANDIDATE` with `automatic_promotion = false`, promotion only on
verified + authorized. Negative-transfer evidence is first-class.

**Gaps / conflicts.** The LEARN→EVOLVE live recalibration write-back is not proven end-to-end on
current main (EVOLVE flags this too — consistent, good). Negative-transfer *detection* criteria
could be more machine-exact: what measurement, over what window, triggers the negative-transfer
flag.

**Corrections before lock.** Specify the negative-transfer detection measurement and window;
mark the live write-back as the acceptance test for the LEARN→EVOLVE seam.

## Node 9 — EVOLVE — 9.0 / 9.0 / 8.5 → **8.8**

**Strongest features.** CONTINUITY ≠ AUTHORITY (with the full expansion: context, intelligence,
learning, successor context, prior authorization, capability, identity similarity ≠ authority);
PROPOSAL ≠ ADOPTION (six-stage chain down to production-proven ≠ constitutional authority);
mission invariance (𝑀𝑡+1 = 𝑀𝑡 unless legitimately ratified); the successor package design with
authority-stripping (`authority_inherited: false`, re-resolution required); Cold-14 as the
acceptance interface; bounded self-building equation (self-building = observation + verified
learning + governed proposal + authorized action + independent verification + versioned adoption +
successor continuity — never self-authorization); "untracked change = drift, tracked verified
authorized change = evolution." The honest pointer holes are a strength: Contract 19 → missing
`.naya/contracts/10-CONTINUITY-SUCCESSOR.md`; registry references a `nayanet-successor-handoff`
runtime path absent on main; contracts 19/20/24 still PROPOSED; multi-generation compounding
unproven.

**Gaps / conflicts.** The EVOLVE charter is unratified and charter ratification is a human-only
gate — the "Final Organ Lock" language must be fenced as normative-target lock, never read as
constitutional ratification. The registry phantom (`nayanet-successor-handoff`) must be resolved:
restore the runtime or correct the registry; a phantom canonical entrypoint is exactly the kind of
thing EVOLVE itself would flag. Contract 19 canonicalization must reconcile the four existing
succession documents (BRAIN/08-SUCCESSION/0001, NAYANODE/0018, NAYANODE/0022, NAYANODE/0003) — not
create a fifth independent successor contract.

**Corrections before lock.** Fence the lock language; resolve the registry phantom one way or the
other; write the Contract 19 reconciliation as an explicit mapping, not a new document.

---

## Cross-cutting findings

1. **All eight are CANDIDATE.** "Lock candidate" is a recommendation about the normative target,
   not a ratification event. Nothing here is ratified; the EVOLVE charter and any constitutional
   change remain human-only decisions.
2. **Prime 1 / Amendment 0002 (ratified 2026-09-30).** The specs' four-state gates and Decision
   Value Calculus V2.1 are consistent with the ratified model (four-state kept over binary). Each
   spec needs one explicit subordination line: Prime 1 governs on conflict.
3. **Semantic order ≠ runtime call order.** The organism order SELF→LAW→ACT→KNOW→PROVE→CONNECT→
   VERIFY→LEARN→EVOLVE→SELF is responsibility order, not invocation order. `Kernel.decide()` will
   call nodes in a different sequence. The specs do not claim otherwise, but the builder needs an
   explicit order-mapping note so nobody "fixes" the runtime to match the diagram.
4. **PROVE→CONNECT→VERIFY topology** needs the reconciliation CONNECT already scoped: CONNECT
   routes and qualifies context; VERIFY establishes causality and outcomes; PROVE bounds belief
   before and after. No node may duplicate another's verdict.
5. **NODE_1__SELF.pdf was not in this drop.** SELF is covered by existing contracts
   (`BRAIN/03-KERNEL/NODES/SELF/0001-CONTRACT.md`, `0002-ELITE-SELF-CONTRACT-V2.md`) and the
   runtime candidate — noted for completeness, not a blocker.
6. **No duplicate mechanisms.** These master specs are the semantic norm; `naya_kernel/` on
   `naya4/*` is the runtime implementation (builder's lane). The BRAIN specs must not be
   re-implemented as a second runtime, and the runtime must not silently redefine the specs.

## Verdict

The eight specifications are strong — honest about their open questions, precise about their
boundaries, and consistent with the NayaPOWER vision (the birthday document's plain-language laws:
"unknown is not verified," memory becomes intelligence only when it changes future behavior,
private by default). **Mean score: 8.8/10.** Recommended: land as versioned CANDIDATE master
specs in their canonical node directories, apply the corrections above before any lock, and keep
the builder's implementation lane (`naya4/*`) referencing — not duplicating — them.

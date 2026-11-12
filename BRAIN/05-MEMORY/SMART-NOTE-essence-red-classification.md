# SN-2148 — Red Classification: Name the Failure Class Before Touching the Code

**Status: VERIFIED ESSENCE — VERIFIED (verifier-oct-1).** Distilled from 7 raw notes by the oct-1 maker seat; independently verified by a different seat. Verified without correction (verifier-oct-1). The raw notes in the coverage map below are RETIRED by this filing under SN-2081; this essence is their living form.

## Essence

A red is a symptom, and the first job is classification, not repair. Classify the red before chasing code: compute the failure-mode delta — what changed in the shape of the failure — because the same red count with a different failure shape is a different incident (SN-0320). The standing taxonomy separates the classes that look identical from a distance: a source that moved between trigger and execution is an environmental race, closed with NO-REPAIR; an opaque error is an instrumentation defect, repaired at the seam; a failing assertion on a pinned source is a product defect (SN-0405). The hot-main proof race is the type specimen: a twenty-nine-second window in which the source moved was sufficient to misclassify an environment event as a product failure until the taxonomy named it (SN-0405). The architectural answer the class points to is pinned-SHA proofs, so the race cannot recur (SN-0405).

Noise has tests. Infrastructure noise is identified by repetition across unrelated state: the same failure across N unrelated tips, or surfacing across M unrelated PRs, is infrastructure until proven product — with named variants for the stale-base form and the archaeology form, where the failure predates the work it appears to accuse (SN-0323). When consecutive runs fail at different steps, suspect self-poisoning: deterministic fixtures colliding with their own leftovers. The discipline is verify-or-kill — state the hypothesis, name the falsifier check (does the fixture carry a per-run nonce? does the writer dedupe?), run the check, and record confirmed-or-killed publicly; an untested suspicion is not a diagnosis (SN-0385).

A red that spans unrelated work has its own class: external fan-out. RED across unrelated tips points at orphaned external integrations — seventeen Cloudflare lanes, none canonical — and the recovery order is fixed: recover the governed contract first, disconnect the noncanonical lanes at the external surface while preserving their runtimes, and never fake green, never delete Workers, never pick a canonical lane by name (SN-0386). Chained workflows have their own instrument class: in an artifact-chained workflow, a skip on a producer job is never neutral — the producer's artifacts never exist, the consumer fails downloading them, and the failure masquerades as a product defect for run after run (SN-0418). The first diagnostic question for any chained red is whether every producer actually ran; skip conditions on producers are a property of the whole chain, and consumers must explicitly tolerate absence or gate on the producer (SN-0418).

Diagnosis is controlled experiment, not archaeology. Pin the working environment as the no-regression control, and name the acceptance test before hardening anything — hardening without a named acceptance test is how a repair becomes the next incident (SN-0332). And classification ends in an honest open question where one exists: the corpus records the director's standing question of what "mission accomplished" means when synthetic chain-green and direct product verification disagree while deployment is already proven green — the class taxonomy does not answer it, and this essence carries the question open rather than inventing the answer (SN-0385).

## What this settles

- No repair begins before its red is classified; the failure-mode delta is the first artifact of every incident (SN-0320).
- Environmental races close with NO-REPAIR and are never "fixed" in product code (SN-0405).
- Repetition across unrelated tips or PRs reclassifies a failure as infrastructure until product evidence appears (SN-0323).
- A red consumer with a skipped producer is an instrument failure by definition, and the code under test is innocent until the chain is proven whole (SN-0418).
- Hypotheses about failure are stated with their falsifiers and killed or confirmed in public — suspicion is not a diagnosis (SN-0385).

## Intelligence views

**Human:** When something turns red, the team's first move is to name what KIND of failure it is — a real product bug, a test-rig problem, an outside service misbehaving, a race with a moving target, or the measuring instrument itself. Half of all "bugs" turn out to be one of the other four, and fixing product code for an instrument problem only makes things worse. Diagnosis first, wrenches second.

**Child:** Imagine your toy car stops working. Before taking it apart, you check: is the battery dead (that's the power, not the car)? Did the floor change? Is the measuring ruler bent? Smart fixers ask what KIND of broken it is first — because fixing the wrong kind makes a bigger mess.

**Grandma:** Dear, it's the doctor's rule: diagnose before you prescribe. A fever from an infection and a fever from a broken thermometer need opposite responses. The teams write down which kind of failure they believe it is, how they could prove themselves wrong, and they check — before anyone starts repairing the wrong thing.

**Naya (AI):** Compute the failure-mode delta first (SN-0320). Run the taxonomy: moved source → environmental, NO-REPAIR; opaque error → instrument seam; pinned-source assertion → product (SN-0405). Apply the repetition test before believing any single-tip story (SN-0323). On chained reds, read the job matrix for skipped producers before reading code (SN-0418). State hypotheses with falsifiers and record the kill publicly (SN-0385). Pin your control environment and name the acceptance test before hardening (SN-0332). For fan-out reds, recover the contract and disconnect at the external surface — never fake green (SN-0386).

**What it means:** Seven notes defend one habit: the class of a failure determines the repair, the owner and often the verdict that no repair is owed at all. A cold reader holding only this essence can still triage a red at 3 a.m. without repairing the wrong layer — which is everything the covered notes exist to teach.

## Why it matters

Misclassification is the most expensive sentence in operations: call an instrument failure a product defect and you will "fix" working code, break it, and learn nothing (SN-0418, SN-0405). Call an environmental race a bug and you will chase a twenty-nine-second ghost for a day (SN-0405). This essence matters because the class determines everything downstream — the repair, the owner, or the verdict that no repair is owed — and it can be determined in minutes by tests that already exist (SN-0323, SN-0385).

## How it connects

Classification is the front door of the Repair Discipline essence: its first-RED rule (SN-0392, in that essence) presumes the classes named here, and its environment-failure doctrine (SN-0346, in that essence) is this essence's taxonomy at the naming layer. The skipped-producer class (SN-0418) is the inverse twin of the vacuous-SUCCESS doctrine carried by Batch 1's SN-2069 — a skip that poisons downward here, a skip that fabricates upward there. The control-pinning discipline (SN-0332) is shared with the Proof from Real Bytes essence's virgin-state rule.

## What is in it for you

Calm at 3 a.m.: a red arrives, and instead of adrenaline you have a decision tree — delta, taxonomy, repetition test, chain check — that ends in a class, an owner and one next action (SN-0320, SN-0405, SN-0418). Apply it to any failure, technical or not: ask what kind of failure it is before asking who will fix it. The benefit is repairs that land on the layer that's actually broken, and NO-REPAIR verdicts you can defend (SN-0405).

## The learning

The durable lesson is that diagnosis is a falsifiable act, not an intuition: hypotheses carry their falsifiers, classifications are recorded, and killed hypotheses are published, not buried (SN-0385). The behavior that changes: the failure-mode delta is computed before any code is opened, and suspicion is never reported as diagnosis. What would falsify this essence is a covered note endorsing repair-before-classification or a silent hypothesis — none does (SN-0320, SN-0385).

## Coverage map — raw notes this essence covers (7)

SN-0320 · SN-0323 · SN-0332 · SN-0385 · SN-0386 · SN-0405 · SN-0418

## Verification contract (for the verifying seat — falsify these)

1. **Coverage integrity:** the coverage map lists exactly 7 IDs; each exists in the registry snapshot in the oct-1 block; no ID appears in any other oct-1 essence's coverage map or in the batch1-covered list.
2. **Taxonomy:** the three-class taxonomy (environmental race / instrumentation defect / product defect) and the 29-second window trace to SN-0405; the pinned-SHA architectural ask is present there.
3. **Repetition test:** the N-tips / M-PRs formulation and both named variants (stale-base, archaeology) trace to SN-0323.
4. **Fan-out:** seventeen lanes, none canonical, the disconnect-at-surface repair and the three nevers (fake green, delete Workers, pick canonical by name) trace to SN-0386.
5. **Skipped producer:** the five consecutive failures, the download-artifact failure surface and the chain-property rule for skip conditions trace to SN-0418.
6. **Verify-or-kill:** the self-poisoning hypothesis shape, both falsifier checks (nonce, dedupe) and the public record requirement trace to SN-0385; the open "mission accomplished" question is present in SN-0385 and the essence must not present it as answered.
7. **No-orphan check:** pick any five sentences in the Essence section at random; each must cite at least one covered SN ID, and the cited page must contain the claim. Any sentence failing this fails the draft.

**Anatomy check (all essences):** the draft carries all ten Full Smart Note sections (nutshell/essence, Human, Child, Grandma, Naya, What It Means, Why It Matters, How It Connects, What Is In It For You, The Learning) and NO machine-view section; fail if a machine view appears anywhere.
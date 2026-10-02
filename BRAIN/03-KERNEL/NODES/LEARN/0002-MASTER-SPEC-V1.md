# LEARN Node Master Specification V1 — CANDIDATE

**Source PDF:** NayaPOWER___NODE_8__LEARN.pdf (uploaded 2026-09-30, extracted 2026-10-01, 4976 words)
**Status:** CANDIDATE — NOT RATIFIED. "Final Organ Lock" in the source means normative-target lock, not constitutional ratification. EVOLVE charter / constitutional changes remain human-only.
**Independent review:** BRAIN/03-KERNEL/0006-NODE-SPECS-INDEPENDENT-SCORECARD-V1.md (same branch)
**Canonical home:** this file. Runtime implementation lives in naya_kernel/ on naya4/* (separate lane) and must reference — not duplicate — this spec.

---

🔱 NayaPOWER — NODE 8: LEARN
Ultimate Master Specification V1 — Lock Candidate
Node ID: MN-08​
Runtime ID: NAYA-KERNEL-LEARN​
Canonical Key: LEARN​
Primary Responsibility: Learning, Reconciliation, Promotion/Demotion, Applicability
Refinement, Behavioral Change, Calibration, Prediction, Compounding​
Primary Contracts: 17 — Learning Loop, 18 — Intelligence Promotion /
Reconciliation, 22 — Hub Master Design / Experience
NODE 8 occupies the center of the Evolution Triad:
\[ \boxed{ VERIFY \rightarrow LEARN \rightarrow EVOLVE } \]
VERIFY answers:
What actually happened?
LEARN answers:
What justified change to future behavior does that experience support?
EVOLVE answers:
Which verified change should become durable successor/system evolution?

0. THE SIMPLEST DEFINITION
For a child, LEARN is the part of Naya that says:
“That happened. What should I do differently next time?”
For a human, LEARN asks a harder question:
“Did this experience actually teach us something reusable, where does that lesson
apply, where does it not apply, and can we prove it changes future behavior
beneficially?”

The engineering definition is:
LEARN is NayaPOWER's governed behavioral-improvement organ. It
converts evidence-bearing outcomes into scoped learning candidates,
reconciles them with existing intelligence, tests their applicability and
behavioral effect, promotes only justified learning, preserves contradiction
and negative evidence, measures prediction/calibration error and future
reuse, and produces versioned learning state for EVOLVE without ever
turning memory, retrieval, confidence, value, or learning into authority.

1. THE MASTER LEARNING LAW
The first permanent law is:
\[ \boxed{ STORED \neq LEARNED } \]
And the complete distinction is:

𝑂𝑏𝑠𝑒𝑟𝑣𝑒𝑑 ≠ 𝐿𝑒𝑎𝑟𝑛𝑒𝑑
𝑅𝑒𝑚𝑒𝑚𝑏𝑒𝑟𝑒𝑑 ≠ 𝐿𝑒𝑎𝑟𝑛𝑒𝑑
𝑅𝑒𝑡𝑟𝑖𝑒𝑣𝑒𝑑 ≠ 𝐿𝑒𝑎𝑟𝑛𝑒𝑑
𝐴𝑝𝑝𝑙𝑖𝑒𝑑 ≠ 𝐿𝑒𝑎𝑟𝑛𝑒𝑑
𝑆𝑢𝑐𝑐𝑒𝑠𝑠𝑓𝑢𝑙𝑂𝑛𝑐𝑒 ≠ 𝐿𝑒𝑎𝑟𝑛𝑒𝑑
𝑉𝑒𝑟𝑖𝑓𝑖𝑒𝑑𝑂𝑢𝑡𝑐𝑜𝑚𝑒 ≠ 𝑉𝑒𝑟𝑖𝑓𝑖𝑒𝑑𝐿𝑒𝑎𝑟𝑛𝑖𝑛𝑔
𝑃𝑟𝑜𝑚𝑜𝑡𝑒𝑑 ≠ 𝐺𝑒𝑛𝑒𝑟𝑎𝑙𝑖𝑧𝑒𝑑
𝐺𝑒𝑛𝑒𝑟𝑎𝑙𝑖𝑧𝑒𝑑 ≠ 𝐶𝑜𝑚𝑝𝑜𝑢𝑛𝑑𝑒𝑑
𝐴𝑐𝑡𝑖𝑣𝑒𝐿𝑒𝑎𝑟𝑛𝑖𝑛𝑔 ≠ 𝐴𝑢𝑡ℎ𝑜𝑟𝑖𝑡𝑦
This is absolutely central.
If Naya merely stores something and labels it “learning,” we have memory with a flattering
name.

2. WHAT REAL LEARNING MEANS
A defensible learning claim requires a future behavioral consequence.
In its simplest form:
\[ \boxed{ Learning(L) \Rightarrow FutureBehavior_{with\,L} \neq FutureBehavior_{without\,L} } \]
when 𝐿 is actually applicable.
For beneficial learning, we need more:

∆𝐵𝐿 > 0
where ∆𝐵𝐿 represents a predeclared desirable behavioral or outcome difference attributable to
the learned intelligence.
So real learning is:
VERIFIED EXPERIENCE
→ EXTRACTED LESSON
→ RECONCILED CANDIDATE
→ EXPLICIT APPLICABILITY
→ FUTURE HELD-OUT USE
→ BEHAVIORAL DIFFERENCE
→ VERIFIED OUTCOME DIFFERENCE
→ RETAINED LEARNING

3. LEARNING MAY BEGIN BEFORE IT IS
VERIFIED
There is an important distinction that reconciles the existing runtime with the formal contract.
An observation may generate a:
LEARNING CANDIDATE

before the outcome is fully verified.
But:

𝐶𝑎𝑛𝑑𝑖𝑑𝑎𝑡𝑒𝐶𝑎𝑝𝑡𝑢𝑟𝑒 ≠ 𝑉𝑒𝑟𝑖𝑓𝑖𝑒𝑑𝐿𝑒𝑎𝑟𝑛𝑖𝑛𝑔
Therefore an unverified experience may legitimately create:
CANDIDATE
for investigation.
It may not create:
VERIFIED
ACTIVE VERIFIED LEARNING
COMPOUNDED
without the required evidence.
This is the correct interpretation of the current contract language:
retain an unverified lesson as a candidate, but reject it as verified learning.

4. LEARN OWNS
LEARN owns the semantics for learning candidates, outcome-derived lessons, reconciliation
with prior intelligence, promotion, rejection, contradiction, supersession of learnings, applicability
refinement, behavioral-effect measurement, future-use experiments, held-out transfer tests,
negative-transfer tests, regression detection, learning value measurement, prediction error,
calibration error, recalibration candidates, compounding evidence, and the learning baton sent
to EVOLVE.
LEARN also owns deciding whether verified experience justifies a learning proposal. It does
not automatically own the authority to mutate every subsystem that the proposal might affect.

5. LEARN MUST NEVER OWN

LEARN must not own execution authority, constitutional authority, consent creation, outcome
verification, truth fabrication, canonical identity allocation, arbitrary graph truth, automatic
system deployment, constitutional amendment, automatic Value Calculus mutation,
self-ratification, successor authority, or a second memory/learning database.
The permanent law is:
\[ \boxed{ Learning \neq Authority } \]
and also:
\[ \boxed{ LearningProposal \neq SystemChangeAuthorization } \]

6. THE FOUR LEARNING AXES
The present schemas mix several concepts. I would separate four axes.

Learning epistemic state
CANDIDATE
TESTING
SUPPORTED
VERIFIED
CONTRADICTED
REJECTED
SUPERSEDED

Adoption state
INACTIVE
ACTIVE
RETIRED
ROLLED_BACK

Transfer maturity
UNTESTED
SOURCE_TASK_ONLY
HELD_OUT_RELATED_SUPPORTED
BOUNDED_GENERALIZATION
COMPOUNDING_SUPPORTED
SUCCESSOR_RETAINED

Applicability

Reuse Graph V2:
APPLICABLE
NOT_APPLICABLE
UNKNOWN
with explicit task classes and limitations.
This prevents one ambiguous word such as ACTIVE from meaning five different things.

7. ACTIVE DOES NOT MEAN UNIVERSAL
Current runtime uses learning_evidence.status = ACTIVE.
That should mean:
this learning is adopted within its verified scope.
It must not mean:
this lesson is universally true and applicable everywhere.
Therefore:
\[ ACTIVE(L) \nRightarrow Universal(L) \]
Every active learning retains:
applicable_scope
task_classes
limitations
source evidence
verification boundary
negative-transfer evidence

8. THE LEARNING OBJECT
A mature learning record should conceptually look like:
{

"learning_id": "...",
"learning_type": "...",
"lesson": "...",
"owner_id": "...",
"scope": {},
"source_outcome_refs": [],
"verification_receipt_refs": [],
"cvo_refs": [],
"evidence_refs": [],
"source_intelligence_refs": [],
"source_event_refs": [],
"learning_state": "CANDIDATE",
"adoption_state": "INACTIVE",
"applicability": {
"state": "UNKNOWN",
"task_classes": [],
"limitations": []
},
"baseline": {},
"treatment": {},
"behavioral_effect": {},
"outcome_effect": {},
"generalization_evidence": {},
"negative_transfer_evidence": {},
"contradictions": [],
"supersedes_learning_id": null,
"regression_guards": [],
"value_effect": {},
"calibration": {},
"promotion": {},
"limitations": [],

"created_at": "...",
"verified_at": null,
"promoted_at": null
}
This is a semantic object model. It does not imply another database table is required.

9. VERIFY → LEARN BATON
VERIFY must supply enough information that LEARN does not trust an anecdote.
The incoming baton should include:
verified outcome
acceptance result
causal status
expected outcome
observed outcome
control/treatment where applicable
evidence refs
proof refs
context refs
observation window
limitations
alternative explanations
unresolved gaps
source/runtime revisions
LEARN then asks:
What lesson, if any, follows from this?
Not:
What story can I invent from it?

10. LESSON EXTRACTION

From verified outcome 𝑂, LEARN proposes candidate lesson 𝐿:

𝐸𝑥𝑡𝑟𝑎𝑐𝑡(𝑂) → 𝐿𝑐𝑎𝑛𝑑𝑖𝑑𝑎𝑡𝑒
But the extraction must preserve:

𝐿𝑠𝑡𝑟𝑒𝑛𝑔𝑡ℎ ≤ 𝐸𝑣𝑖𝑑𝑒𝑛𝑐𝑒𝑠𝑡𝑟𝑒𝑛𝑔𝑡ℎ
For example, if the verified finding is:
preserving provenance improved one provenance-sensitive task,
the lesson cannot silently become:
provenance checking improves every task.
That would be evidence laundering through abstraction.

11. GENERALIZATION CEILING
Let 𝑆𝑣 be the verified source scope.
Then initial candidate scope must satisfy:

𝑆𝑐𝑜𝑝𝑒(𝐿𝑐𝑎𝑛𝑑𝑖𝑑𝑎𝑡𝑒) ⊆ 𝑆𝑣
unless additional transfer evidence justifies expansion.
Scope expansion is earned.
It is never inferred from confidence.

12. RECONCILIATION WITH EXISTING
INTELLIGENCE

Every candidate must be compared to the existing learning/intelligence state.
The result should classify into something like:
NEW
EXACT_DUPLICATE
REFINEMENT
SCOPE_NARROWING
SCOPE_EXPANSION_CANDIDATE
CONTRADICTION
CORRECTION
SUPERSEDES
PARALLEL_DIFFERENT_SCOPE
UNKNOWN
This is critical because “learning” must not mean endlessly creating new versions of the same
lesson.

13. DUPLICATE LAW
If new candidate 𝐿𝑛 is semantically the same lesson, same owner, same scope and same
material evidence lineage as existing 𝐿𝑒:

𝐿𝑛 ≡ 𝐿𝑒
then:
REUSE / ADD EVIDENCE
not:
CREATE ANOTHER CANONICAL LEARNING
The current candidate path already tries to reuse exact persisted lesson claims. Preserve and
strengthen that behavior.

14. CONTRADICTION LAW

If:
\[ L_n \perp L_e \]
and both have material evidence:
SURFACE CONFLICT
→ PRESERVE BOTH
→ PROVE / VERIFY
→ DETERMINE SCOPE
Never:
newer wins automatically
and never:
delete the old learning
Historical contradiction is valuable intelligence.

15. CORRECTION VS SUPERSESSION
These are not identical.
A correction says:
the earlier interpretation was materially wrong.
A supersession says:
the earlier learning may have been valid in its time/scope, but a newer learning now
governs the current context.
Both preserve history.

16. PROMOTION MUST BE EARNED
A strong promotion gate should require:

\[ PromotionEligible(L)= V \land P \land R \land A \land B \land N \land C \]
where:
●​
●​
●​
●​
●​
●​
●​

𝑉 = qualifying VERIFY result exists;
𝑃 = provenance/evidence valid;
𝑅 = reconciliation complete;
𝐴 = applicability explicitly defined;
𝐵 = behavioral effect established where learning claims behavior change;
𝑁 = negative-transfer boundary survives;
𝐶 = material contradictions handled.

For learning that merely captures a factual update, the behavioral test may differ. But a claim of
behavioral learning requires behavioral evidence.

17. CURRENT PROMOTION-SEAM HOLE
This is one of the most important discoveries in current source.
The promotion branch of nayanet-learning-verify currently does essentially:
learning_id exists
+
evidence_refs array is nonempty
→ status ACTIVE
→ block LEARNED
→ relationship VERIFIED
The surrounding workflow can and does provide real causal evidence in the bounded North-Star
chain.
But the runtime function itself does not first independently resolve the supplied evidence
references and prove:
VERIFY result is legitimate
CVO exists
CVO matches this learning
outcome is qualifying
scope matches
causal boundary matches
before those state upgrades.

That is too weak for the ultimate Node 8.
The correct rule is:

𝐸𝑣𝑖𝑑𝑒𝑛𝑐𝑒𝑅𝑒𝑓𝑒𝑟𝑒𝑛𝑐𝑒𝑃𝑟𝑒𝑠𝑒𝑛𝑐𝑒 ≠ 𝐸𝑣𝑖𝑑𝑒𝑛𝑐𝑒𝑉𝑎𝑙𝑖𝑑𝑎𝑡𝑖𝑜𝑛
So canonicalization must make the LEARN promotion gate consume and validate canonical
VERIFY evidence, not merely receive strings naming evidence.

18. NO CALLER-SUPPLIED VERIFIED
LEARNING
A caller may propose:
candidate lesson
candidate interpretation
candidate task
where permitted.
But must not be able to say:
{
"verified": true,
"learning_state": "ACTIVE",
"lesson": "..."
}
and have LEARN trust it.
Promotion status must be computed from canonical evidence.

19. FUTURE BEHAVIOR TEST
For behavioral learning 𝐿, define a held-out task 𝑞 not used to construct the original conclusion.
Control:

𝐵𝐶 = 𝐵𝑒ℎ𝑎𝑣𝑖𝑜𝑟(𝑞, ¬𝐿)
Treatment:

𝐵𝑇 = 𝐵𝑒ℎ𝑎𝑣𝑖𝑜𝑟(𝑞, 𝐿)
Then:

∆𝐵 = 𝐵𝑇 − 𝐵𝐶
where the behavior measurement is declared before seeing the result.
For categorical behavior:

∆𝐵 = 1(𝐵𝑇 = 𝐵𝑑𝑒𝑠𝑖𝑟𝑒𝑑) − 1(𝐵𝐶 = 𝐵𝑑𝑒𝑠𝑖𝑟𝑒𝑑)
A qualifying learning effect requires the declared improvement condition.

20. OUTCOME CHANGE IS STRONGER
THAN TEXT CHANGE
A model producing different words is not necessarily learning.
Therefore distinguish:

𝐵𝑒ℎ𝑎𝑣𝑖𝑜𝑟𝑎𝑙𝐷𝑒𝑙𝑡𝑎
from:

𝑂𝑢𝑡𝑐𝑜𝑚𝑒𝐷𝑒𝑙𝑡𝑎
The strongest learning proof has both:
behavior changed appropriately
+

measurable outcome improved
The current causal-learning verifier already recomputes both behavioral delta and measurable
outcome delta for bounded tasks. That is exactly the right direction.

21. HELD-OUT LAW
A task used to create the lesson cannot by itself prove generalization.
If:

𝑇𝑎𝑠𝑘𝑙𝑒𝑎𝑟𝑛 = 𝑇𝑎𝑠𝑘𝑣𝑒𝑟𝑖𝑓𝑦
the result may prove replay.
It does not necessarily prove transfer.
A stronger test uses:

𝑇𝑎𝑠𝑘ℎ𝑒𝑙𝑑𝑜𝑢𝑡 ≠ 𝑇𝑎𝑠𝑘𝑠𝑜𝑢𝑟𝑐𝑒
while preserving the same relevant capability requirement.

22. RELATED HELD-OUT TRANSFER
For candidate learning 𝐿:

𝐴𝑝𝑝𝑙𝑖𝑐𝑎𝑏𝑙𝑒(𝐿, 𝑞𝑟) = 1
for a new related task 𝑞𝑟.
Then:

𝑂𝑢𝑡𝑐𝑜𝑚𝑒(𝑞𝑟, 𝐿) > 𝑂𝑢𝑡𝑐𝑜𝑚𝑒(𝑞𝑟, ¬𝐿)

under the predeclared metric.
This supports transfer within that bounded related class.

23. NEGATIVE TRANSFER
The system must also prove where the lesson does not apply.
For unrelated task 𝑞𝑢:

𝐴𝑝𝑝𝑙𝑖𝑐𝑎𝑏𝑙𝑒(𝐿, 𝑞𝑢) = 0
Expected:

𝐵𝑒ℎ𝑎𝑣𝑖𝑜𝑟(𝑞𝑢, 𝐿) = 𝐵𝑒ℎ𝑎𝑣𝑖𝑜𝑟(𝑞𝑢, ¬𝐿)
or appropriate refusal to apply the lesson.
This is one of the strongest pieces already present in the bounded North-Star evidence.

24. THE GENERALIZATION PREDICATE
A bounded generalization claim should require both sides:
\[ \boxed{ GeneralizationSupported = RelatedTransferSupported \land NegativeTransferRefused
} \]
That is much stronger than:
“it worked twice.”
It proves both:
where to use the lesson
and:

where not to use it.

25. OVERGENERALIZATION IS A FAILURE
If a provenance-preservation lesson changes an unrelated arithmetic task:

𝑇𝑟𝑎𝑛𝑠𝑓𝑒𝑟(𝐿, 𝑞𝑢𝑛𝑟𝑒𝑙𝑎𝑡𝑒𝑑) ≠ 0
then the learning has overgeneralized.
That should produce:
OVERGENERALIZATION_DETECTED
and block scope expansion.
This is not a minor quality issue.
It is a fundamental intelligence failure.

26. APPLICABILITY MUST BECOME
STRUCTURED
Current nayanet-learning-verify has a bounded helper that infers Graph V2 applicability
by matching lesson text with regular expressions.
That was a useful bridge.
It should not become the permanent architecture.
The rule should be:
explicit declared applicability
> verified learned applicability
> bounded legacy inference
not:

lesson contains phrase
→ permanent task semantics

27. APPLICABILITY PROMOTION
Candidate lesson:
applicability = UNKNOWN
After bounded proof:
APPLICABLE to task class A
NOT_APPLICABLE to task class C
UNKNOWN elsewhere
That is the intelligent representation.
Do not promote:
APPLICABLE EVERYWHERE
because one task worked.

28. LEARNING VALIDITY ENVELOPE
Every learning should have a validity envelope:

𝐸𝐿 = (𝑂𝑤𝑛𝑒𝑟, 𝑇𝑎𝑠𝑘𝐶𝑙𝑎𝑠𝑠𝑒𝑠, 𝐶𝑎𝑝𝑎𝑏𝑖𝑙𝑖𝑡𝑖𝑒𝑠, 𝐸𝑛𝑣𝑖𝑟𝑜𝑛𝑚𝑒𝑛𝑡, 𝑇𝑖𝑚𝑒, 𝐷𝑒𝑝𝑒𝑛𝑑𝑒𝑛𝑐𝑖𝑒𝑠, 𝐿𝑖𝑚𝑖𝑡𝑎𝑡𝑖𝑜𝑛𝑠)
The learning may steer behavior only inside that envelope.
Outside the envelope:

𝐴𝑝𝑝𝑙𝑖𝑐𝑎𝑏𝑖𝑙𝑖𝑡𝑦 = 𝑈𝑁𝐾𝑁𝑂𝑊𝑁
unless separately verified.

29. STALE LEARNING
A previously valid learning can become stale.
Examples include changed software architecture, superseded API behavior, changed
organizational policy, updated evidence, changed user objective, or a newer model capability
invalidating the previous workaround.
Therefore:
\[ HistoricallyVerified \nRightarrow CurrentlyApplicable \]
CONNECT and LEARN must cooperate on temporal validity.

30. REGRESSION DETECTION
A learning that once improved behavior can later degrade it.
For a retained learning 𝐿, define reference performance:

𝑌𝑟𝑒𝑓𝑒𝑟𝑒𝑛𝑐𝑒
and later measured performance:

𝑌𝑡
If:

𝑌𝑡 < 𝑌𝑟𝑒𝑓𝑒𝑟𝑒𝑛𝑐𝑒 − ϵ
for a predeclared material tolerance, create:
REGRESSION_CANDIDATE
Do not silently leave stale learned behavior active forever.

31. ROLLBACK LEARNING
Rollback does not erase history.
Correct:
LEARNING V2
ACTIVE
↓ regression verified
ROLLED_BACK / RETIRED
LEARNING V1
may become current again if separately valid
History remains inspectable.

32. LEARNING FROM FAILURE
Failure can be extremely valuable intelligence.
If VERIFY establishes a failure:

𝑂𝑢𝑡𝑐𝑜𝑚𝑒 = 𝐹𝐴𝐼𝐿
LEARN may derive:
under conditions X, action/assumption Y failed because Z.
But again:
\[ OneFailure \nRightarrow UniversalRule \]
The learning's scope must remain bounded by evidence.

33. FAILURE INTELLIGENCE
A useful learning object from failure should preserve:

what was attempted
what assumption failed
what signal would have predicted failure
what condition made failure possible
what safer future behavior is proposed
where the lesson applies
what still remains uncertain
That is more valuable than storing:
“Task failed.”

34. LEARNING FROM SUCCESS
Success should be treated just as cautiously.
The question is not:
“What worked?”
It is:
“What part of the approach was causally or evidentially responsible for the
success?”
Otherwise the system learns superstition.

35. CORRELATION LEARNING
If causality is not established, LEARN may retain:
ASSOCIATION CANDIDATE
with appropriate uncertainty.
It must not convert:

𝐶𝑜𝑟𝑟𝑒𝑙𝑎𝑡𝑖𝑜𝑛

into:

𝐶𝑎𝑢𝑠𝑎𝑙𝐿𝑒𝑠𝑠𝑜𝑛
without VERIFY support.

36. THE LEARNING LINEAGE
A promoted learning should trace:
EXPERIENCE
→ EVENT
→ INTELLIGENT BLOCK
→ PROVENANCE
→ RELATIONSHIP
→ ACTION
→ OBSERVATION
→ OUTCOME
→ VERIFY
→ LEARNING CANDIDATE
→ HELD-OUT USE
→ VERIFIED LEARNING
The current runtime already reconstructs much of:
Event
→ Intelligent Block
→ Lineage
→ Relationship
→ Index
→ Checkpoint
and can fall back to an immutable commit receipt when the mutable checkpoint has advanced.
That is a strong architectural pattern worth preserving.

37. MUTABLE CURRENT STATE VS
IMMUTABLE HISTORY
Current runtime handles an important real problem correctly:
the project's current cognition checkpoint can move beyond the checkpoint tied to
an older learning candidate.
Instead of rewriting history, it reconstructs the older chain from the immutable
intelligence-commit receipt when possible.
The permanent law is:

𝐶𝑢𝑟𝑟𝑒𝑛𝑡𝑆𝑡𝑎𝑡𝑒𝑀𝑜𝑣𝑒𝑚𝑒𝑛𝑡 ≠ 𝐻𝑖𝑠𝑡𝑜𝑟𝑖𝑐𝑎𝑙𝐸𝑣𝑖𝑑𝑒𝑛𝑐𝑒𝐿𝑜𝑠𝑠

38. CHECKPOINTS ARE NOT LEARNING
A checkpoint means:
state was persisted.
It does not mean:
the behavior represented there is verified learning.
Therefore:

𝐶ℎ𝑒𝑐𝑘𝑝𝑜𝑖𝑛𝑡 ≠ 𝐿𝑒𝑎𝑟𝑛𝑖𝑛𝑔
𝐶ℎ𝑒𝑐𝑘𝑝𝑜𝑖𝑛𝑡𝑆𝑡𝑎𝑡𝑢𝑠 = 𝐿𝐸𝐴𝑅𝑁𝐸𝐷
must ultimately be backed by a genuine learning transition, not just a string.

39. PROMOTED LEARNING SHOULD
UPDATE THE EXISTING INTELLIGENCE

Current source locks a promoted lesson into the existing Intelligent Block by moving its
understanding state to:
LEARNED
That matches the one-brain architecture.
The correct model is:
existing canonical intelligence
+
verified learning evidence
→ richer intelligence state
not:
create a parallel "learning memory"

40. KNOW ↔ LEARN
KNOW owns the canonical durable intelligence.
LEARN owns the justified transition that says:
this intelligence has earned learning status.
Therefore:

𝐿𝐸𝐴𝑅𝑁 → 𝐾𝑁𝑂𝑊
semantically updates the intelligence lifecycle, while:

𝐾𝑁𝑂𝑊
remains the canonical home.
No competing memory system.

41. LEARN → CONNECT

When learning becomes verified, it may produce stronger relationship/applicability metadata.
Examples:
LEARNED_FROM
APPLIES_TO
REFINES
CORRECTS
SUPERSEDES
But CONNECT remains the graph/application organ.
LEARN supplies verified relationship candidates/evidence.
CONNECT governs contextual use.

42. LEARN → EVOLVE
This is the primary downstream baton.
LEARN should hand EVOLVE:
verified lesson
exact scope
behavioral evidence
outcome evidence
generalization evidence
negative-transfer evidence
limitations
regression guard
value/calibration evidence
source lineage
promotion status
required authority for system adoption
EVOLVE then decides what legitimate durable system/successor change follows.

43. LEARN CANNOT SELF-RATIFY

The Value Calculus already contains exactly the right law:
recalibration creates a candidate; it does not mutate the active profile.
Promotion requires:
independent verification
+
applicable authority
Therefore:

𝐿𝐸𝐴𝑅𝑁 𝑃𝑟𝑜𝑝𝑜𝑠𝑎𝑙 ≠ 𝐴𝑐𝑡𝑖𝑣𝑒𝑆𝑦𝑠𝑡𝑒𝑚𝑉𝑒𝑟𝑠𝑖𝑜𝑛
EVOLVE owns the governed evolution boundary.

44. VALUE CALIBRATION
VERIFY compares:

∆𝑉𝑝𝑟𝑒𝑑𝑖𝑐𝑡𝑒𝑑
with:

∆𝑉𝑎𝑐𝑡𝑢𝑎𝑙
LEARN consumes the error.
Define signed error:

𝑒𝑖 = ∆𝑉𝑎𝑐𝑡𝑢𝑎𝑙,𝑖 − ∆𝑉𝑝𝑟𝑒𝑑𝑖𝑐𝑡𝑒𝑑,𝑖
Absolute error:

𝐴𝐸𝑖 = |𝑒𝑖|
For 𝑛 verified decisions:

1

𝑛

𝐵𝑖𝑎𝑠𝑛 = 𝑛 ∑ 𝑒𝑖
𝑖=1

𝑀𝐴𝐸𝑛 =

𝑛
1
∑ |𝑒𝑖|
𝑛
𝑖=1

These are learning inputs.

45. CALIBRATION CANDIDATE
If predeclared thresholds establish persistent bias or increasing error:

|𝐵𝑖𝑎𝑠𝑛| > τ𝑏
or:

𝑀𝐴𝐸𝑛 > τ𝑒
for the required evidence count/window, LEARN may create:
VALUE_RECALIBRATION
candidate.
It should include:
current profile/version
calibration evidence
observed errors
proposed weights/thresholds
expected correction
evidence refs
scope
limitations

46. NO AUTOMATIC WEIGHT TUNING
Never:
prediction wrong once
→ silently change decision weights
Correct:
verified calibration error
→ LEARN candidate
→ independent verification
→ applicable authority
→ EVOLVE version promotion
The existing Value Calculus already follows that design.

47. PREDICTION
LEARN also owns improving future predictions.
If Naya predicted:

𝑃(𝑌) = 𝑝
and observed 𝑌, repeated verified outcomes can calibrate the estimator.
But predictive confidence must remain evidence-bound.
An estimator becoming more confident without becoming more accurate is not learning.

48. PREDICTION QUALITY
Possible diagnostics include:

𝑀𝐴𝐸

for numeric outcomes and, where probabilistic predictions are legitimately expressed:

2

1

𝐵𝑟𝑖𝑒𝑟 = 𝑛 ∑(𝑝𝑖 − 𝑦𝑖)
𝑖

These are measurement tools, not universal constitutional scores.
Use only when the prediction type makes them meaningful.

49. LEARNING RATE IS NOT A VIRTUE BY
ITSELF
A system that “learns” extremely quickly may simply overfit.
Therefore:

𝐿𝑒𝑎𝑟𝑛𝑖𝑛𝑔𝑆𝑝𝑒𝑒𝑑 ≠ 𝐿𝑒𝑎𝑟𝑛𝑖𝑛𝑔𝑄𝑢𝑎𝑙𝑖𝑡𝑦
The objective is:
fast justified learning, slow enough to preserve truth and applicability.

50. OVERFITTING
A lesson that works only on the task used to create it is not generalized learning.
Warning pattern:
training/source task → PASS
same task replay → PASS
related held-out task → FAIL
Result:
SOURCE_TASK_ONLY

not:
GENERALIZED

51. TEST CONTAMINATION
A held-out task must actually be held out.
If the candidate learning was designed using the exact verification example, the test is
contaminated.
LEARN receipts should record:
source_task_refs
holdout_task_refs
test_created_before_outcome?
shared evidence?
where relevant.

52. COMPOUNDING
Compounding is stronger than repeated reuse.
Compounding means:
verified learning from earlier experience enables later verified learning or better
behavior, and cumulative improvement survives appropriate controls.
A conceptual chain is:

𝐿1 → 𝐿2 → 𝐿3
with preserved causal/learning lineage.

53. MULTI-GENERATION COMPOUNDING
For generations \(G_0,G_1,\dots,G_n\), strongest proof compares matched held-out
performance against a clean or appropriate baseline.
Conceptually:

𝑉(𝐺𝑛, 𝑞ℎ) > 𝑉(𝐺0, 𝑞ℎ)
with attributable intermediate learning lineage.
But:
\[ LaterIsBetter \nRightarrow EarlierLearningCausedIt \]
unless the experiment supports that attribution.

54. COMPOUNDING REQUIRES
ATTRIBUTION
A real compounding record should answer:
Which earlier learning was used?
Which later learning depended on it?
What changed?
What outcome improved?
How much of the improvement is attributable?
Did unrelated behavior remain stable?
Did a cold successor retain the chain?
Without attribution, we have chronological accumulation, not proven compounding.

55. CURRENT BOUNDED EVIDENCE IS
NOT YET MULTI-GENERATION
COMPOUNDING
This is important.
The current North-Star chain supports a bounded
learning→reuse→generalization→cold-successor story.
The Brain index explicitly says it does not yet establish:
multi-generation compounding
universally.
So NODE 8's ultimate design includes compounding, but we do not upgrade current runtime
truth to that level.

56. SUCCESSOR-RETAINED LEARNING
One of the strongest learning tests is:
destroy prior runtime context
↓
start cold successor
↓
give identifier/task only
↓
successor retrieves canonical learning
↓
recognizes applicability
↓
reuses learning
↓
does not inherit authority
↓
behavior improves appropriately
The current bounded North-Star evidence supports this pattern for its specimen.

That is a major strength.

57. SUCCESSOR LEARNING ≠
SUCCESSOR AUTHORITY
Permanent:

𝐼𝑛ℎ𝑒𝑟𝑖𝑡𝑒𝑑𝐼𝑛𝑡𝑒𝑙𝑙𝑖𝑔𝑒𝑛𝑐𝑒 ≠ 𝐼𝑛ℎ𝑒𝑟𝑖𝑡𝑒𝑑𝐴𝑢𝑡ℎ𝑜𝑟𝑖𝑡𝑦
A successor can inherit:
lesson
evidence
applicability
history
without inheriting:
permission to act consequentially
LAW must still resolve current authority.

58. LEARNING PRIVACY
Private experience may produce useful private learning.
Cross-owner use requires the same governed scope/consent model as the rest of
NayaPOWER.
A learning cannot use “system improvement” as a justification for leaking private data.
\[ LearningValue \nRightarrow PrivacyOverride \]

59. DERIVED SHARED LEARNING

Where consent allows it:
private experience
→ safe derived lesson
→ identity-safe shared intelligence
can be legitimate.
But:
derived lesson shared
must not imply:
raw private source shared
CONNECT/LAW boundaries still apply.

60. LEARNING AND AUTHORITY
Suppose Naya learns:
acting first within defined guardrails was more efficient.
That learning still does not mean:
Naya may create its own guardrails.
The correct chain remains:
LEARNING
→ applicable behavioral context
→ LAW
→ authority resolution
→ ACT
Never:
LEARNING
→ permission

61. LEARNING AND GOVERNANCE
Lessons may suggest governance improvements.
They may not silently rewrite governance.
So:
verified lesson:
"policy X caused recurring friction"
can produce:
governance change proposal
but only the proper authority can ratify:
new policy

62. LEARNING RECEIPT
A robust receipt could be:
{
"receipt_type": "LEARNING_TRANSITION",
"receipt_id": "...",
"node_id": "NAYA-KERNEL-LEARN",
"execution_id": "...",
"learning_id": "...",
"state_before": "...",
"state_after": "...",
"lesson": "...",
"source_outcome_refs": [],
"verify_receipt_refs": [],
"cvo_refs": [],
"evidence_refs": [],

"reconciliation": {
"classification": "...",
"existing_learning_refs": []
},
"applicability": {
"state": "...",
"task_classes": [],
"limitations": []
},
"behavioral_effect": {},
"outcome_effect": {},
"heldout_evidence": [],
"negative_transfer_evidence": [],
"contradictions": [],
"regression_guards": [],
"value_recalibration": null,
"authority_created": false,
"promotion_eligible": false,
"promotion_reason_codes": [],
"input_hash": "...",
"output_hash": "...",
"handoff_to": "NAYA-KERNEL-EVOLVE",
"timestamp": "..."
}

63. PROMOTION RECEIPT MUST NAME
THE GATE
A learning should never simply say:
promoted = true

It should explain:
SOURCE_OUTCOME_VERIFIED
CAUSAL_REQUIREMENT_SATISFIED
PROVENANCE_VALID
RECONCILIATION_COMPLETE
APPLICABILITY_DEFINED
RELATED_HOLDOUT_PASS
UNRELATED_REFUSAL_PASS
NO_MATERIAL_REGRESSION
INDEPENDENT_RECOMPUTATION_PASS
or the subset legitimately required for that learning class.

64. REASON-CODED NON-PROMOTION
Examples:
VERIFY_RESULT_REQUIRED
OUTCOME_NOT_ACCEPTED
CAUSAL_SUPPORT_REQUIRED
PROVENANCE_INCOMPLETE
CONTRADICTS_ACTIVE_LEARNING
APPLICABILITY_UNKNOWN
HELDOUT_REQUIRED
NO_BEHAVIORAL_DELTA
NO_OUTCOME_DELTA
NEGATIVE_TRANSFER_FAILED
REGRESSION_DETECTED
EVIDENCE_REFERENCE_UNRESOLVED
SCOPE_MISMATCH
AUTHORITY_BOUNDARY_VIOLATION
A candidate staying a candidate is a valid result.

65. IDEMPOTENCY
Identical candidate input should not create multiple active learnings.

Conceptually:
\[ LearningKey= H( owner \Vert lessonSemanticHash \Vert sourceOutcome \Vert scope \Vert
applicability ) \]
Repeated equivalent proposal:
→ reuse / append evidence / reread
not:
→ duplicate learning

66. CONCURRENCY
Two verifiers/promoters racing on the same candidate must not create:
two active canonical learning states
Use canonical versioning/CAS/transaction semantics.
The loser rereads the canonical result.

67. LEARNING HASH
For semantic integrity:

𝐻𝐿 = 𝑆𝐻𝐴256(𝐶𝑎𝑛𝑜𝑛𝑖𝑐𝑎𝑙𝑖𝑧𝑒(𝑙𝑒𝑠𝑠𝑜𝑛, 𝑠𝑐𝑜𝑝𝑒, 𝑎𝑝𝑝𝑙𝑖𝑐𝑎𝑏𝑖𝑙𝑖𝑡𝑦, 𝑠𝑜𝑢𝑟𝑐𝑒𝑂𝑢𝑡𝑐𝑜𝑚𝑒𝑠, 𝑣𝑒𝑟𝑖𝑓𝑖𝑐𝑎𝑡𝑖𝑜𝑛𝑅𝑒𝑓𝑠))
Material change to lesson or applicability:
new learning version.
Not silent mutation under the same identity.

68. SECURITY THREAT MODEL

LEARN must defend against:
memory poisoning
learning poisoning
fake evidence references
self-certification
reward hacking
metric gaming
benchmark memorization
holdout contamination
scope widening
authority laundering
cross-owner leakage
stale learning replay
contradiction suppression
regression suppression
duplicate promotion
race promotion
caller-supplied ACTIVE state
fake CVO references
causal overclaim
negative-transfer blindness
text-regex applicability spoofing
value-calibration manipulation
self-ratifying system changes

69. REWARD HACKING
If Naya knows the metric and merely optimizes the metric without accomplishing the human
objective, that is not valid learning.
Therefore:
\[ MetricImprovement \nRightarrow MissionImprovement \]
Verification/Value Calculus must preserve objective fit and unintended consequences.

70. LEARNING QUALITY

Do not create a magical “Learning Score.”
A useful learning should be evaluated through explicit properties:
source verification
behavioral effect
outcome effect
applicability
negative transfer
stability
regression
value effect
successor retention
The hard gates matter more than an average score.

71. HUMAN VALUE
The eventual human experience should be:
“I don't have to teach Naya the same valid lesson again.”
Useful measures include:

𝑅𝑒𝑇𝑒𝑎𝑐ℎ𝑖𝑛𝑔𝐴𝑣𝑜𝑖𝑑𝑒𝑑
𝑅𝑒𝑝𝑒𝑎𝑡𝑒𝑑𝐸𝑟𝑟𝑜𝑟𝑅𝑒𝑑𝑢𝑐𝑒𝑑
𝑇𝑖𝑚𝑒𝑇𝑜𝑅𝑒𝑢𝑠𝑒
𝐴𝑝𝑝𝑙𝑖𝑐𝑎𝑏𝑙𝑒𝑅𝑒𝑢𝑠𝑒𝑅𝑎𝑡𝑒
𝑁𝑒𝑔𝑎𝑡𝑖𝑣𝑒𝑇𝑟𝑎𝑛𝑠𝑓𝑒𝑟𝑅𝑎𝑡𝑒
𝑅𝑒𝑔𝑟𝑒𝑠𝑠𝑖𝑜𝑛𝑅𝑎𝑡𝑒
𝐶𝑜𝑙𝑑𝑆𝑢𝑐𝑐𝑒𝑠𝑠𝑜𝑟𝑅𝑒𝑢𝑠𝑒𝑅𝑎𝑡𝑒
𝑉𝑒𝑟𝑖𝑓𝑖𝑒𝑑𝑉𝑎𝑙𝑢𝑒𝐹𝑟𝑜𝑚𝐿𝑒𝑎𝑟𝑛𝑖𝑛𝑔
That is how LEARN delivers real value.

72. LEARNING EFFICIENCY
A useful concept is:

𝐿𝑒𝑎𝑟𝑛𝑖𝑛𝑔𝐸𝑓𝑓𝑖𝑐𝑖𝑒𝑛𝑐𝑦 =

𝑉𝑒𝑟𝑖𝑓𝑖𝑒𝑑𝐹𝑢𝑡𝑢𝑟𝑒𝑉𝑎𝑙𝑢𝑒𝐹𝑟𝑜𝑚𝐿𝑒𝑎𝑟𝑛𝑖𝑛𝑔
𝐿𝑒𝑎𝑟𝑛𝑖𝑛𝑔𝑉𝑒𝑟𝑖𝑓𝑖𝑐𝑎𝑡𝑖𝑜𝑛𝐶𝑜𝑠𝑡

but it is only an optimization metric after truth, privacy, authority and safety gates pass.
Cheap bad learning is not efficient.

73. COMPRESS WITHOUT LOSING
CAUSAL LINEAGE
As learning matures, the human-facing lesson can become concise.
But machine state must preserve:
source
evidence
outcome
causal basis
scope
limitations
supersession
Therefore:

𝑆ℎ𝑜𝑟𝑡𝐻𝑢𝑚𝑎𝑛𝑆𝑢𝑚𝑚𝑎𝑟𝑦 ≠ 𝐿𝑜𝑠𝑡𝑀𝑎𝑐ℎ𝑖𝑛𝑒𝐿𝑖𝑛𝑒𝑎𝑔𝑒

74. LEARNING STATE MACHINE
I recommend:

UNINITIALIZED
→ CANDIDATE
→ RECONCILING
→ TEST_REQUIRED
→ TESTING
→ EVIDENCE_REVIEW
→ VERIFIED
→ PROMOTION_READY
→ ACTIVE
with branch states:
DEFERRED
REJECTED
CONTRADICTED
SUPERSEDED
REGRESSED
ROLLED_BACK
INCONCLUSIVE
BLOCKED
Current runtime's simpler states can map into this without falsely claiming those states already
exist in production.

75. LEARNING MATURITY LADDER
Separate maturity from lifecycle:
L0 OBSERVATION
L1 CANDIDATE
L2 SOURCE-OUTCOME SUPPORTED
L3 HELD-OUT BEHAVIOR SUPPORTED
L4 BOUNDED GENERALIZATION
L5 RETAINED ACTIVE LEARNING
L6 COLD-SUCCESSOR RETAINED
L7 COMPOUNDING SUPPORTED
L8 MULTI-GENERATION COMPOUNDING
This is a conceptual qualification ladder, not a replacement for existing database enums.

76. AAA PROPERTY TESTS
A real NODE 8 should enforce at least:
P1 stored ≠ learned
P2 retrieved ≠ learned
P3 observed ≠ learned
P4 verified outcome ≠ verified learning
P5 one success ≠ general rule
P6 active ≠ universal
P7 learning ≠ authority
P8 learning ≠ constitutional change
P9 candidate may exist without promotion
P10 missing VERIFY evidence ⇒ no verified promotion
P11 evidence-ref presence ≠ evidence validation
P12 fake VERIFY/CVO ref ⇒ promotion blocked
P13 wrong-owner evidence ⇒ promotion blocked
P14 wrong-scope evidence ⇒ promotion blocked
P15 duplicate lesson ⇒ reconcile/reuse
P16 contradiction ⇒ surface, do not overwrite
P17 supersession preserves history
P18 scope expansion requires transfer evidence
P19 claimed behavioral learning requires behavioral delta
P20 claimed beneficial learning requires relevant outcome evidence
P21 replay on source task ≠ generalization
P22 related held-out success supports only bounded transfer
P23 unrelated-task effect ⇒ overgeneralization failure
P24 negative-transfer refusal required for bounded generalization
P25 applicability UNKNOWN ≠ broad APPLICABLE
P26 heuristic applicability cannot outrank explicit metadata
P27 stale learning cannot silently steer current behavior
P28 regression can demote/retire learning
P29 calibration error creates candidate, not active parameter change
P30 Value Calculus recalibration requires verification + authority
P31 LEARN cannot self-ratify
P32 promotion is idempotent
P33 concurrent promotion produces one canonical state
P34 learning history is immutable/versioned

P35 compounding requires measured later behavior
P36 chronology ≠ compounding
P37 cold successor reuse must work without original conversation
P38 cold successor inherits intelligence, not authority
P39 learning privacy never widens automatically
P40 cold successor can reconstruct why the lesson is active

77. GOLDEN CANDIDATE TEST
Verified or partially observed experience produces:
candidate lesson
but causal/future-use evidence is absent.
Expected:
CANDIDATE
promotion = false
This is success.

78. GOLDEN PROMOTION TEST
Input:
verified source outcome
+
canonical lineage
+
explicit lesson
+
explicit applicable task class
+
held-out related behavioral improvement
+
held-out outcome improvement
+

independent recomputation
+
negative-transfer refusal
Expected:
VERIFIED
→ ACTIVE within declared scope
→ canonical Intelligent Block becomes LEARNED
→ graph evidence updated
→ EVOLVE handoff
without creating authority.

79. GOLDEN FAKE-EVIDENCE TEST
Caller passes:
{
"evidence_refs": ["CVO-I-MADE-THIS-UP"]
}
Expected ultimate behavior:
EVIDENCE_REFERENCE_UNRESOLVED
→ NO PROMOTION
This is the source-level hole that must become impossible.

80. GOLDEN RELATED-HOLDOUT TEST
Source task teaches:
preserve provenance before applying retained intelligence.
New provenance-sensitive held-out task:
Control:

REQUIRE_DIRECT_CANONICAL_INTELLIGENCE
Treatment:
PRESERVE_PROVENANCE_BEFORE_APPLY
with improved declared provenance outcome.
Expected:
RELATED_TRANSFER_SUPPORTED
within that task family.

81. GOLDEN UNRELATED-REFUSAL TEST
Same retained lesson.
Task:
arithmetic_only
Expected:
NO_APPLICABLE_RETAINED_INTELLIGENCE
or equivalent neutral behavior.
The arithmetic answer remains unchanged.
Result:
NEGATIVE_TRANSFER_REFUSED
This is a strong intelligence signal.

82. GOLDEN OVERGENERALIZATION
TEST

Same lesson unexpectedly changes arithmetic reasoning.
Expected:
NEGATIVE_TRANSFER_FAILED
OVERGENERALIZATION_DETECTED
NO SCOPE EXPANSION
Potentially demote the learning's applicability until reconciled.

83. GOLDEN CONTRADICTION TEST
Existing verified learning:
behavior A improves task class X.
New verified outcome:
behavior A harms a subset of X under condition Z.
Correct result:
do not delete A
create refinement/correction candidate
narrow applicability
preserve condition Z
The brain becomes more precise.

84. GOLDEN REGRESSION TEST
Learning was previously successful.
After architecture change:
held-out reuse now harms outcome
Expected:
REGRESSION_DETECTED

ACTIVE learning flagged
further consequential use constrained
review / correction candidate
Not:
“It used to work, therefore keep using it.”

85. GOLDEN CALIBRATION TEST
Predicted value across verified decisions systematically exceeds actual value.
For example:

𝐵𝑖𝑎𝑠𝑛 <− τ𝑏
Expected:
VALUE_RECALIBRATION CANDIDATE
Not:
weights silently modified
EVOLVE receives the candidate only after the required verification.

86. GOLDEN COLD-SUCCESSOR TEST
Destroy the original runtime context.
Fresh successor gets:
learning_id
task
canonical access
and no original prompt or caller-supplied lesson.

Expected:
retrieve active learning
→ reconstruct evidence/applicability
→ apply on related task
→ refuse unrelated transfer
→ obtain fresh LAW authority where consequential
That proves retained learning rather than conversational memory.

87. WHAT “INFLUENTIAL” MEANS FOR
LEARN
LEARN is not alive merely because:
learning_evidence.status = ACTIVE
It becomes influential when:
same future task
without learning → behavior A
with verified learning → behavior B
and that behavioral difference is appropriate and verified.
Database status is not behavioral proof.

88. WHAT “VERIFIED LEARNING” MEANS
A strong behavioral learning claim needs:
verified source outcome
+
lesson lineage
+
applicability
+

future-use behavior
+
future-use outcome
+
independent verification
For bounded generalization:
+
related holdout
+
unrelated refusal
For compounding:
+
later generation improvement
+
causal lineage

89. WHAT “PRODUCTION-PROVEN”
MEANS FOR NODE 8
For a declared learning class:
exact canonical source
+
deployed LEARN runtime parity
+
real candidate
+
canonical VERIFY evidence
+
independent evidence validation
+
reconciliation
+
promotion
+
Intelligent Block lock-in
+

relationship/applicability lock-in
+
independent reread
+
related held-out reuse
+
unrelated refusal
+
regression negative
+
cold successor reuse
+
no authority inheritance
Only then should that declared LEARN capability be production-proven.

90. CURRENT NODE 8 TRUTH
The repository currently gives us a strong but bounded foundation.
Already present: LEARN semantic/machine/AI contracts; candidate creation;
learning_evidence; event/block/lineage/relationship/index/checkpoint reconstruction;
immutable historical checkpoint reconstruction; retained-learning reread; Intelligent Block
LEARNED lock-in; relationship VERIFIED lock-in; GitHub OIDC runtime identity; causal-learning
experiment; behavioral and outcome deltas; independent recomputation; bounded
related-held-out generalization; unrelated-task refusal; cold-successor learning reuse; Value
Calculus calibration-error → VALUE_RECALIBRATION candidate semantics; and explicit
no-self-ratification rules.
Still open: Contracts 17/18/22 remain proposed; Learning Contract V1 remains proposed;
current nayanet-learning-verify is not current-production-parity; promotion source trusts
nonempty caller evidence references too weakly; task applicability still uses bounded
lesson-text heuristics in this runtime; LEARN state/adoption/generalization axes are not
normalized; universal VERIFY→LEARN gating is not proven; current proof does not establish
latest-main universal LEARN behavior; multi-generation compounding is not proven; two-owner
learning/consent generality is not proven; and broader system-level recalibration promotion
remains future work.
That is exactly where we should be honest.

91. THE COMPLETE EIGHT-NODE
ORGANISM
We now have:
Node

Question

SELF

Who am I, what is the mission, and what state am I in?

LAW

What governs me and what am I authorized to do?

ACT

What exact authorized action should I perform?

KNOW

What durable intelligence exists?

PROVE

What am I justified in believing?

CONNECT

What matters together in this exact context?

VERIFY

What actually happened and what caused it?

LEARN

What verified lesson deserves to change future
behavior?

And the final organ will answer:
EVOLVE — What verified improvement should survive me and become part of
the next legitimate state of NayaPOWER?

92. THE ULTIMATE LEARN QUESTION
Every material LEARN invocation should reduce to:
“Given this verified experience, what exact lesson is justified; how does it
compare with existing intelligence; what is its proper scope; where does it
apply and not apply; does it measurably alter future behavior and outcomes
on genuinely appropriate held-out use; does unrelated behavior remain
stable; what contradictions, regressions and limitations remain; what
value/calibration error does it reveal; and what versioned learning state may
legitimately be handed to EVOLVE without creating new authority?”

That is Node 8.

93. THE FINAL LEARN EQUATION
\[ \boxed{ VERIFIED\ EXPERIENCE + LESSON + PROVENANCE + RECONCILIATION +
APPLICABILITY + HELD\!-\!OUT\ BEHAVIOR + OUTCOME\ EFFECT + NEGATIVE\
TRANSFER + INDEPENDENT\ VERIFICATION = VERIFIED\ LEARNING } \]
For bounded generalization:
\[ \boxed{ VERIFIED\ LEARNING + RELATED\ TRANSFER + UNRELATED\ REFUSAL =
BOUNDED\ GENERALIZATION } \]
For compounding:
\[ \boxed{ VERIFIED\ LEARNING_t + FUTURE\ VERIFIED\ REUSE + ATTRIBUTABLE\
ADDITIONAL\ IMPROVEMENT + LINEAGE = COMPOUNDING\ EVIDENCE } \]
Always subject to:

𝑆𝑇𝑂𝑅𝐸𝐷 ≠ 𝐿𝐸𝐴𝑅𝑁𝐸𝐷
𝑂𝐵𝑆𝐸𝑅𝑉𝐸𝐷 ≠ 𝐿𝐸𝐴𝑅𝑁𝐸𝐷
𝑉𝐸𝑅𝐼𝐹𝐼𝐸𝐷 𝑂𝑈𝑇𝐶𝑂𝑀𝐸 ≠ 𝑉𝐸𝑅𝐼𝐹𝐼𝐸𝐷 𝐿𝐸𝐴𝑅𝑁𝐼𝑁𝐺
𝐴𝐶𝑇𝐼𝑉𝐸 ≠ 𝑈𝑁𝐼𝑉𝐸𝑅𝑆𝐴𝐿
𝐺𝐸𝑁𝐸𝑅𝐴𝐿𝐼𝑍𝐸𝐷 ≠ 𝐶𝑂𝑀𝑃𝑂𝑈𝑁𝐷𝐸𝐷
𝐸𝑉𝐼𝐷𝐸𝑁𝐶𝐸 𝑅𝐸𝐹 ≠ 𝑉𝐸𝑅𝐼𝐹𝐼𝐸𝐷 𝐸𝑉𝐼𝐷𝐸𝑁𝐶𝐸
𝑆𝐼𝑀𝐼𝐿𝐴𝑅𝐼𝑇𝑌 ≠ 𝐴𝑃𝑃𝐿𝐼𝐶𝐴𝐵𝐼𝐿𝐼𝑇𝑌
𝐿𝐸𝐴𝑅𝑁𝐼𝑁𝐺 ≠ 𝐴𝑈𝑇𝐻𝑂𝑅𝐼𝑇𝑌
𝐶𝐴𝐿𝐼𝐵𝑅𝐴𝑇𝐼𝑂𝑁 𝐶𝐴𝑁𝐷𝐼𝐷𝐴𝑇𝐸 ≠ 𝐴𝐶𝑇𝐼𝑉𝐸 𝑆𝑌𝑆𝑇𝐸𝑀 𝐶𝐻𝐴𝑁𝐺𝐸
and the evolution chain becomes:

\[ \boxed{ VERIFY\ EARNS\ REALITY \rightarrow LEARN\ EARNS\ CHANGE \rightarrow
EVOLVE\ EARNS\ CONTINUITY } \]

Lock recommendation
This is the MN-08 LEARN normative target I would lock.
The most important repair is the promotion boundary:
\[ \boxed{ NONEMPTY\ EVIDENCE\ REFS \neq PROMOTION\ AUTHORITY } \]
LEARN must independently bind a candidate to the actual canonical VERIFY
result/CVO/outcome before it can promote the learning, mark the block LEARNED, or mark
supporting relationships VERIFIED.
The second major repair is:
\[ \boxed{ EXPLICIT\ APPLICABILITY > TEXT\ REGEX\ INFERENCE } \]
Legacy inference can remain as a bounded compatibility mechanism, but verified structured
applicability should become the real machine contract.


---

## CANDIDATE AMENDMENTS — Naya 2 scorecard corrections (NOT RATIFIED)

> Status: PROPOSED. Drafted by the Naya 2 independent-review lane from
> BRAIN/03-KERNEL/0006-NODE-SPECS-INDEPENDENT-SCORECARD-V1.md (2026-10-01, mean
> score 8.8/10). These amendments are CANDIDATE — not ratified, not merged to
> main. Each must be applied (or explicitly rejected with written reason) before
> any lock of this spec. Nothing above this line was altered: the verbatim PDF
> text is preserved intact. References (L2, X1, X2, X12) map to the scorecard's
> correction list.

### A-LEARN-1 [X1 — Prime 1 / Amendment 0002 subordination]

Add: "This spec operates under Amendment 0002 (Prime 1, the Judgment Rule,
ratified 2026-09-30); where this spec and Prime 1 conflict, Prime 1 governs."
REQUIRED before lock.

### A-LEARN-2 [X2 — semantic order vs runtime call order]

Add an explicit order-mapping note: the organism order
SELF→LAW→ACT→KNOW→PROVE→CONNECT→VERIFY→LEARN→EVOLVE→SELF is responsibility
order, not invocation order. Kernel.decide() will call nodes in a different
sequence; LEARN's scoping and no-silent-transfer duties do not depend on call
position.

### A-LEARN-3 [L2 — negative-transfer detection, machine-exact]

Specify the negative-transfer detection measurement and window: what metric,
measured over what window, triggers the negative-transfer flag, and what
happens on trigger (quarantine of the lesson, never silent application).
Negative-transfer evidence is first-class; its detection criteria must be
machine-exact before lock.

### A-LEARN-4 [X12 — LEARN→EVOLVE seam acceptance]

The LEARN→EVOLVE live recalibration write-back is not proven end-to-end on
current main. Mark the live write-back as the acceptance test for the seam:
until a verified lesson traverses LEARN_CANDIDATE (automatic_promotion=false)
through verified + authorized promotion into a live recalibration, the seam is
UNPROVEN — not failed, not passed. LEARN may not claim the bridge works on
the strength of the design alone.


### A-LEARN-5 [L-1 — MODERATE — amendment-proposal flag on VERIFIED]

Add: (1) No learning transitions to VERIFIED on the "Learning epistemic
state" axis (§6) except through the amendment mechanism — a VERIFIED state is
proposed with evidence, reviewed, and recorded; it is never silently
asserted, including by satisfying §16's promotion formula alone. This is
consistent with §16 PROMOTION MUST BE EARNED (which defines promotion
eligibility: qualifying VERIFY result V, provenance P, reconciliation R,
applicability A, behavioral effect B, negative-transfer boundary N,
contradiction handling C) and §18 NO CALLER-SUPPLIED VERIFIED: §16 sets the
bar, this rule sets the transition discipline — eligibility does not
self-assign the state. Checked against §16: no contradiction. (2)
PROVE-overlap note: PROVE's epistemic claim axis (§27) and LEARN's learning
epistemic axis (§6) both contain VERIFIED/SUPPORTED. They must not
double-mint verification: PROVE's VERIFIED is a claim about evidence for a
proposition; LEARN's VERIFIED is a state of an adopted learning. A learning
is VERIFIED only when its supporting claims are PROVE-VERIFIED (or
equivalently evidenced) AND the amendment-proposal flag is set; neither organ
may assert the other's state.

Rationale: adopting VERIFIED as a persistent learning state without the
proposal flag is an F01-class regression; LEARN and PROVE must not disagree
on who gets to say "verified."
Acceptance: §6 carries the flag requirement; the PROVE-overlap note is
present. REQUIRED before lock.

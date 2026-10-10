# VERIFY Node Master Specification V1 — CANDIDATE

**Source PDF:** NayaPOWER___NODE_7__VERIFY.pdf (uploaded 2026-09-30, extracted 2026-10-01, 4780 words)
**Status:** CANDIDATE — NOT RATIFIED. "Final Organ Lock" in the source means normative-target lock, not constitutional ratification. EVOLVE charter / constitutional changes remain human-only.
**Independent review:** BRAIN/03-KERNEL/0006-NODE-SPECS-INDEPENDENT-SCORECARD-V1.md (same branch)
**Canonical home:** this file. Runtime implementation lives in naya_kernel/ on naya4/* (separate lane) and must reference — not duplicate — this spec.

---

🔱 NayaPOWER — NODE 7: VERIFY
Ultimate Master Specification V1 — Lock Candidate
Node ID: MN-07​
Runtime ID: NAYA-KERNEL-VERIFY​
Canonical Key: VERIFY​
Primary Responsibility: Outcome, Observation, Acceptance, Independent Verification,
Causality, Production Evidence​
Primary Contracts:​
11 — Causal Verification Object​
23 — Verification & Acceptance​
25 — CI / Full-Suite Evidence
VERIFY begins the evolution triad:
\[ \boxed{ VERIFY \rightarrow LEARN \rightarrow EVOLVE } \]
The essential questions are:
VERIFY: What actually happened?​
LEARN: What justified lesson should change future behavior?​
EVOLVE: What verified improvement should the next Naya inherit?
And VERIFY receives reality from multiple upstream organs:

𝐴𝐶𝑇 → 𝑉𝐸𝑅𝐼𝐹𝑌
𝑃𝑅𝑂𝑉𝐸 → 𝑉𝐸𝑅𝐼𝐹𝑌
𝐶𝑂𝑁𝑁𝐸𝐶𝑇 → 𝑉𝐸𝑅𝐼𝐹𝑌

0. THE SIMPLEST DEFINITION
Child
VERIFY is the part of Naya that checks:

“Did it really work?”

Human
VERIFY answers:
What actually happened?​
Did it match what we said success would look like?​
Did anything fail?​
Do we actually have enough evidence to know?​
If we claim something caused the result, can we prove that connection?

Engineering
VERIFY is NayaPOWER's independent outcome, acceptance and
causal-verification organ. It compares predeclared expected outcomes
against independently observed reality, separates execution from outcome,
distinguishes failure from insufficient proof, tests causal claims with
appropriate comparison methods, preserves observation windows and
unresolved gaps, independently recomputes consequential conclusions from
canonical persisted evidence, and emits a bounded verification receipt that
downstream LEARN may consume without trusting the executor's own
success claim.

1. WHY VERIFY EXISTS
Without VERIFY, AI systems naturally do this:
I tried it
→ no exception
→ probably worked
→ call it successful
That is not acceptable.
NayaPOWER requires:
INTENT
↓
SUCCESS BOUNDARY
↓
AUTHORIZED ACTION

↓
ACTUAL EXECUTION
↓
OBSERVATION
↓
PERSISTED OUTCOME
↓
INDEPENDENT REREAD
↓
EXPECTED ↔ OBSERVED COMPARISON
↓
CAUSAL ANALYSIS WHEN CLAIMED
↓
ACCEPT / REJECT / DEFER / NOT PROVEN

2. THE MASTER VERIFY LAW
\[ \boxed{ EXECUTION \neq OUTCOME } \]
and therefore:

𝐴𝑡𝑡𝑒𝑚𝑝𝑡𝑒𝑑 ≠ 𝐸𝑥𝑒𝑐𝑢𝑡𝑒𝑑
𝐸𝑥𝑒𝑐𝑢𝑡𝑒𝑑 ≠ 𝑆𝑢𝑐𝑐𝑒𝑠𝑠𝑓𝑢𝑙
𝑂𝑏𝑠𝑒𝑟𝑣𝑒𝑑 ≠ 𝑉𝑒𝑟𝑖𝑓𝑖𝑒𝑑
𝑅𝑒𝑐𝑒𝑖𝑝𝑡 ≠ 𝑂𝑢𝑡𝑐𝑜𝑚𝑒
𝑂𝑢𝑡𝑐𝑜𝑚𝑒 ≠ 𝐶𝑎𝑢𝑠𝑎𝑙𝑖𝑡𝑦
𝐶𝑜𝑟𝑟𝑒𝑙𝑎𝑡𝑖𝑜𝑛 ≠ 𝐶𝑎𝑢𝑠𝑎𝑡𝑖𝑜𝑛
𝑆𝑒𝑙𝑓𝑅𝑒𝑝𝑜𝑟𝑡 ≠ 𝐼𝑛𝑑𝑒𝑝𝑒𝑛𝑑𝑒𝑛𝑡𝑉𝑒𝑟𝑖𝑓𝑖𝑐𝑎𝑡𝑖𝑜𝑛
𝑇𝑒𝑠𝑡𝑠𝑃𝑎𝑠𝑠𝑒𝑑 ≠ 𝑃𝑟𝑜𝑑𝑢𝑐𝑡𝑖𝑜𝑛𝑃𝑟𝑜𝑣𝑒𝑛
This is the constitutional heart of Node 7.

3. THE SECOND MASTER LAW
SUCCESS MUST BE DEFINED BEFORE THE RESULT IS
KNOWN.
If acceptance criteria are created after seeing the result, Naya can accidentally move the
goalposts.
Therefore, wherever reasonably determinable:

𝑆𝑢𝑐𝑐𝑒𝑠𝑠𝐶𝑟𝑖𝑡𝑒𝑟𝑖𝑎𝑝𝑟𝑒
must exist before:

𝐴𝑐𝑡𝑖𝑜𝑛
and verification must evaluate:

𝑂𝑏𝑠𝑒𝑟𝑣𝑒𝑑𝑂𝑢𝑡𝑐𝑜𝑚𝑒
against the predeclared boundary.
Not a rewritten boundary optimized to make the result look successful.

4. VERIFY OWNS
VERIFY owns:
●​
●​
●​
●​
●​
●​
●​
●​
●​

observations;
normalized outcomes;
expected-vs-observed comparison;
verification requirements;
acceptance criteria;
acceptance decisions;
causal verification;
Causal Verification Objects;
control/treatment comparison;

●​
●​
●​
●​
●​
●​
●​
●​
●​
●​
●​
●​
●​
●​
●​
●​
●​
●​
●​
●​
●​

counterfactual reasoning boundaries;
independent reread;
independent recomputation;
production outcome evidence;
delayed observation windows;
CI/full-suite evidence interpretation;
adversarial verification;
regression evidence;
outcome integrity;
unresolved verification gaps;
failure classification;
inconclusive classification;
NOT_PROVEN results;
outcome/value recomputation;
observed value;
prediction-versus-actual comparison;
verification receipts;
verification lineage;
verification replay;
verification reconstruction;
handoff of qualifying verified outcomes to LEARN.

5. VERIFY MUST NEVER OWN
VERIFY does not own:
●​
●​
●​
●​
●​
●​
●​
●​
●​
●​
●​
●​
●​
●​
●​

authority;
consent;
authorization issuance;
execution;
canonical memory creation;
canonical Intelligent Block allocation;
general truth/provenance classification;
relationship retrieval;
learning promotion;
constitutional amendment;
self-ratification;
human judgment reserved to Shawn;
a second proof system;
a second ledger;
a second causal store;

●​ a second Value Calculus.
VERIFY observes and evaluates reality.
It does not grant permission to create reality.

6. VERIFY VS PROVE
This distinction needs to stay perfect.

PROVE
asks:
What does the evidence justify us claiming?

VERIFY
asks:
What actually occurred relative to the declared outcome boundary, and where
causality is claimed, does the evidence establish that attribution?
Example:
PROVE may establish:
“There is strong evidence that this Intelligent Block is current and applicable.”
CONNECT may establish:
“It belongs in this task context.”
ACT uses it.
VERIFY asks:
Did using it actually change the result?
Those are different responsibilities.

7. VERIFY VS ACT
ACT says:
“I executed X.”
VERIFY says:
“I independently checked whether the expected effect Y actually occurred.”
Therefore:
\[ ACT\ Receipt \nRightarrow VERIFY\ PASS \]
ACT may provide observation material.
ACT cannot certify its own outcome.

8. VERIFY VS LEARN
VERIFY says:
“This outcome is established to this degree.”
LEARN says:
“Does this verified experience justify changing future behavior?”
Thus:

𝑉𝑒𝑟𝑖𝑓𝑖𝑒𝑑𝑂𝑢𝑡𝑐𝑜𝑚𝑒 ≠ 𝑉𝑒𝑟𝑖𝑓𝑖𝑒𝑑𝐿𝑒𝑎𝑟𝑛𝑖𝑛𝑔
A one-time verified success is not automatically a universal lesson.

9. THE FOUR AXES MUST STAY
SEPARATE

One of the biggest normalization opportunities in current VERIFY is that several different state
systems exist.
Do not collapse them.

Axis A — Outcome
Current kernel model:
SUCCESS
FAILURE
INCONCLUSIVE
NOT_PROVEN

Axis B — Acceptance
ACCEPTED
REJECTED
PENDING

Axis C — Causality
Current model includes:
NOT_CLAIMED
CLAIMED
VERIFIED
UNVERIFIED
CONTRADICTED

Axis D — Value/observation verification
Existing Value Calculus:
UNVERIFIED
PASS_PENDING_WINDOW
VERIFIED_PASS
FAIL
ESCALATE
These are related.
They are not interchangeable.

10. WHY SEPARATE AXES MATTER
Consider:
Action completed.
Immediate result looks correct.
30-day harm window is still open.
Possible representation:
outcome_status = SUCCESS
acceptance_decision = PENDING
verification = PASS_PENDING_WINDOW
That is far more accurate than pretending one word can describe everything.

11. FAILURE ≠ NOT_PROVEN
This distinction is essential.

FAILURE
means evidence establishes:
\[ ObservedOutcome \not\models SuccessCriteria \]

NOT_PROVEN
means:

𝐸𝑣𝑖𝑑𝑒𝑛𝑐𝑒
is insufficient to establish whether the required result occurred.

INCONCLUSIVE
means adequate observations exist, but they do not resolve the question sufficiently.

These should never be treated as synonyms.

12. FAILURE CAN BE A HIGH-QUALITY
VERIFY RESULT
If something actually failed and VERIFY says:
FAILURE
then VERIFY succeeded.
Likewise:
NOT_PROVEN
can be the most correct output.
The system must not optimize Node 7 toward producing green checks.
It must optimize toward accurately describing reality.

13. OBSERVATION
Observation is a first-class object.
Conceptually:
{
"observation_id": "...",
"subject": "...",
"metric": "...",
"value": "...",
"source": "...",
"method": "...",
"observed_at": "...",
"environment": "...",

"source_revision": "...",
"owner_id": "...",
"scope": {},
"provenance": {},
"evidence_refs": [],
"observer_identity": "...",
"independence_context": {},
"limitations": []
}
Observation is:
what was measured.
Verification is:
what that measurement establishes relative to the declared claim.

14. EXPECTED OUTCOME CONTRACT
Before consequential execution, where reasonably knowable:
{
"expected_outcome_id": "...",
"action_id": "...",
"target": "...",
"success_criteria": [],
"failure_criteria": [],
"required_observations": [],
"required_evidence": [],
"comparison_method": "...",
"observation_window": {
"opens_at": "...",

"closes_at": "..."
},
"acceptance_policy": {},
"causal_claim_expected": false
}
This closes the goalpost-moving loophole.

15. OUTCOME COMPARISON
Let the success predicates be:
\[ S=\{s_1,s_2,\dots,s_n\} \]
For required predicates:
\[ Success \iff \bigwedge_{i=1}^{n}s_i(observed)=true \]
If one required criterion is unknown:

𝑂𝑢𝑡𝑐𝑜𝑚𝑒 ≠ 𝑉𝐸𝑅𝐼𝐹𝐼𝐸𝐷_𝑆𝑈𝐶𝐶𝐸𝑆𝑆
unless the acceptance contract explicitly permits partial success.

16. CRITICAL CRITERIA CANNOT BE
AVERAGED AWAY
Suppose nine things worked and one mandatory safety condition failed.
Never:
\[ \frac{9}{10}=90\%=PASS \]
Instead:

𝐶𝑟𝑖𝑡𝑖𝑐𝑎𝑙𝐹𝑎𝑖𝑙𝑢𝑟𝑒 = 1 ⇒ 𝐴𝑐𝑐𝑒𝑝𝑡𝑎𝑛𝑐𝑒 ≠ 𝐴𝐶𝐶𝐸𝑃𝑇𝐸𝐷
This mirrors the AAA critical-cap law.

17. PARTIAL SUCCESS
Some actions legitimately produce mixed outcomes.
VERIFY should support:
SUCCESS
PARTIAL / MIXED evidence context
FAILURE
INCONCLUSIVE
NOT_PROVEN
without pretending a partially completed action is complete.
If current canonical schema stays with four top-level states, partiality can live explicitly inside the
outcome details until deliberately normalized.

18. OBSERVATION COMPLETENESS
Let required observations be:
\[ R=\{r_1,\dots,r_n\} \]
Then:

𝑂𝑏𝑠𝑒𝑟𝑣𝑎𝑡𝑖𝑜𝑛𝐶𝑜𝑣𝑒𝑟𝑎𝑔𝑒 =

|{𝑟𝑖:𝑂𝑏𝑠𝑒𝑟𝑣𝑒𝑑(𝑟𝑖)}|
|𝑅|

For full verification:

𝑂𝑏𝑠𝑒𝑟𝑣𝑎𝑡𝑖𝑜𝑛𝐶𝑜𝑣𝑒𝑟𝑎𝑔𝑒 = 1
for all mandatory observations.

Again:
diagnostic metric, not automatic truth.

19. EVIDENCE APPROPRIATENESS
Not all evidence answers all questions.
Examples:
A deployment log can support:
deployment invocation occurred.
It does not necessarily prove:
the correct runtime is serving traffic.
A database receipt can prove:
a row was persisted.
It does not necessarily prove:
the user experienced the intended result.
A screenshot may prove:
the rendered UI looked a particular way.
It does not necessarily prove:
the backend completed correctly.
VERIFY must match the method to the claim.

20. THE CAUSAL VERIFICATION OBJECT
The repository's strongest conceptual definition is already good:

The CVO is the evidence-bearing bridge between prior knowledge, authorized
action, observed outcome and independent verification.
It should answer:
What was known?
What was relevant?
What authority applied?
What action occurred?
What outcome occurred?
What evidence establishes it?
What independent check supports the causal claim?
What changed in retained intelligence?
Can a successor reuse the result?

21. CVO IS NOT AUTHORITY
Permanent:

𝐶𝑉𝑂 ≠ 𝐴𝑢𝑡ℎ𝑜𝑟𝑖𝑡𝑦
A CVO records and analyzes what happened.
It does not authorize the action retroactively.

22. CVO IS NOT A RECEIPT LABEL
A record named:
"verified": true
is not verification by itself.
VERIFY must reconstruct why it is verified.
Therefore:

𝐿𝑎𝑏𝑒𝑙(𝑉𝐸𝑅𝐼𝐹𝐼𝐸𝐷) ≠ 𝑉𝑒𝑟𝑖𝑓𝑖𝑒𝑑

23. ULTIMATE CVO SHAPE
Conceptually:
{
"cvo_id": "...",
"schema_version": "...",
"objective": {},
"task": {},
"prior_intelligence": [],
"context_receipt_refs": [],
"proof_receipt_refs": [],
"authority": {
"decision_ref": "...",
"grant_ref": "..."
},
"action": {
"action_id": "...",
"execution_receipt_ref": "...",
"target": "...",
"parameters_hash": "..."
},
"expected_outcome": {},
"observed_outcome": {},
"control": null,
"treatment": null,
"evidence_refs": [],
"causal_method": "...",
"causal_assessment": "...",
"alternative_explanations": [],
"confounds": [],

"limitations": [],
"unresolved_gaps": [],
"acceptance_decision": "...",
"verification_state": "...",
"independent_verifier": {},
"independent_recomputation": {},
"source_revision": "...",
"runtime_revision": "...",
"verified_at": "..."
}
One CVO model.
No second causal object architecture.

24. CURRENT CVO RUNTIME IS
BOUNDED
Current nayanet-causal-verify is valuable, but its scope is deliberately narrow.
It currently contains fixed bindings including:
NAYA-NODE-0001
NAYA-NODE-0001-CONTINUITY
specific owner
specific control/treatment patterns
specific cold-behavior experiment
specific retained-intelligence scenario
Therefore current evidence supports:
bounded causal verification capability
not:
universal VERIFY behavior.

That distinction must remain.

25. CAUSAL CLAIM LEVELS
Not every outcome claim is causal.
Useful progression:
OBSERVED
ASSOCIATED
CAUSAL_CANDIDATE
CAUSAL_SUPPORTED
CAUSAL_CONTRADICTED
INCONCLUSIVE
The current runtime already uses:
CAUSAL_SUPPORTED
for its bounded controlled-intervention case.
The important law is:
stronger causal language requires stronger causal evidence.

26. CAUSAL MATH
For treatment 𝑇 and control 𝐶, with outcome function 𝑌:

∆𝑌 = 𝑌𝑇 − 𝑌𝐶
For Boolean desired behavior:

𝑌 ∈ {0, 1}
A useful bounded causal signal exists when, for example:

𝑌𝐶 = 0, 𝑌𝑇 = 1
and required equivalence/confound conditions are satisfied.
But:

∆𝑌 ≠ 0
alone does not prove causality.

27. TASK EQUIVALENCE
Control/treatment comparison requires:

𝑇𝑎𝑠𝑘𝐶 ≈ 𝑇𝑎𝑠𝑘𝑇
for all material dimensions except treatment.
At minimum, where relevant:
same objective
same task
same input
same environment
same authority
same model/runtime class
same evaluation rule
same observation window
same source event
with the declared intervention being the material difference.
Current causal-verifier tests explicitly protect task equivalence and source-event equivalence.
That should become permanent.

28. THE INTERVENTION LAW
For causal experiment:

𝑇 = 𝐶 + 𝐼𝑛𝑡𝑒𝑟𝑣𝑒𝑛𝑡𝑖𝑜𝑛
If multiple material variables change:

𝐴𝑡𝑡𝑟𝑖𝑏𝑢𝑡𝑖𝑜𝑛𝐶𝑜𝑛𝑓𝑖𝑑𝑒𝑛𝑐𝑒 ↓
or:
CAUSAL_INCONCLUSIVE
The system must not pretend it knows which variable caused the difference.

29. ALTERNATIVE EXPLANATIONS
Current CVO runtime already preserves alternatives such as:
●​ execution-context differences unrelated to retained intelligence;
●​ provenance availability independent of the retained block.
Good.
The ultimate CVO should always ask:
What else could explain the observation?
A causal conclusion that cannot name plausible alternatives is usually under-specified.

30. CONFOUNDS
For material confound 𝑧:
\[ Confound(z)= Associated(z,T) \land Associated(z,Y) \]

where it can plausibly explain the treatment/outcome relationship.
Material uncontrolled confounds should cap causal strength.

31. CAUSAL SUPPORT DOES NOT MEAN
UNIVERSALITY
Current CVO already contains the correct limitation:
bounded experiment does not establish universal causal effect across all action
types.
Permanent equation:
\[ CausalEffect(TaskClass=A) \nRightarrow CausalEffect(AllTasks) \]
This will matter enormously in LEARN.

32. INDEPENDENT VERIFICATION
Independence is not binary magic.
It has dimensions.
I recommend VERIFY record:
identity independence
process independence
evidence reread
recomputation independence
implementation independence
organizational independence
Not every verification needs all dimensions.
But the exact independence claimed must be honest.

33. MINIMUM INDEPENDENCE FOR
NAYAPOWER RUNTIME PROOF
For consequential internal machine proof, at minimum:
fresh verifier identity
canonical persisted evidence reread
no trust in executor's verdict
independent recomputation
result comparison
explicit disagreement failure
Current CVO workflow already demonstrates much of this pattern with fresh GitHub OIDC
verification and persisted reread.

34. SAME CODE CAN STILL REREAD
INDEPENDENTLY — WITH LIMITATIONS
A fresh verifier executing the same deterministic verifier implementation can provide useful
independence from the producer when it:
●​
●​
●​
●​
●​

obtains a fresh identity;
rereads canonical state;
reconstructs inputs;
recomputes the result;
does not trust the producer's claim.

But it is not the strongest imaginable independence because:
shared verifier code can share implementation defects.
Therefore the receipt should say exactly which independence dimension was achieved.

35. SELF-CERTIFICATION IS FORBIDDEN

Permanent:

𝐸𝑥𝑒𝑐𝑢𝑡𝑜𝑟𝐶𝑙𝑎𝑖𝑚𝑇𝑟𝑢𝑠𝑡𝑒𝑑 = 𝑓𝑎𝑙𝑠𝑒
Current repository tests explicitly guard this.
The strongest form is:
producer:
"I caused X."
verifier:
"I reread the raw persisted evidence and independently computed whether X follows."
Never:
producer:
"I caused X."
verifier:
"The producer wrote CAUSAL_SUPPORTED, therefore PASS."

36. OBSERVATION WINDOWS
Some outcomes are immediate.
Others require time.
Let:

𝑊 = [𝑡𝑜𝑝𝑒𝑛, 𝑡𝑐𝑙𝑜𝑠𝑒]
If required harmful/beneficial effects cannot yet be fully observed:
PASS_PENDING_WINDOW
is legitimate.
Existing Value Calculus already supports exactly that state.

37. DELAYED HARM
Suppose immediate success is true:

𝐼𝑚𝑚𝑒𝑑𝑖𝑎𝑡𝑒𝑃𝑎𝑠𝑠 = 1
but delayed material harm remains unknown:

𝐷𝑒𝑙𝑎𝑦𝑒𝑑𝐻𝑎𝑟𝑚𝐾𝑛𝑜𝑤𝑛 = 0
Then:

𝑉𝑒𝑟𝑖𝑓𝑖𝑐𝑎𝑡𝑖𝑜𝑛 = 𝑃𝐴𝑆𝑆_𝑃𝐸𝑁𝐷𝐼𝑁𝐺_𝑊𝐼𝑁𝐷𝑂𝑊
not:

𝑉𝐸𝑅𝐼𝐹𝐼𝐸𝐷_𝑃𝐴𝑆𝑆
This is one of the wisest existing V2.1 rules.

38. VERIFICATION STATE FUNCTION
Conceptually:

𝑉 = 𝑓(𝑐𝑟𝑖𝑡𝑒𝑟𝑖𝑎, 𝑜𝑏𝑠𝑒𝑟𝑣𝑎𝑡𝑖𝑜𝑛𝑠, 𝑒𝑣𝑖𝑑𝑒𝑛𝑐𝑒, 𝑤𝑖𝑛𝑑𝑜𝑤, 𝑐𝑜𝑛𝑓𝑙𝑖𝑐𝑡𝑠, 𝑖𝑛𝑑𝑒𝑝𝑒𝑛𝑑𝑒𝑛𝑐𝑒)
A simplified form:
required criterion failed
→ FAIL
required observation missing
→ UNVERIFIED / NOT_PROVEN
criteria currently pass but window open
→ PASS_PENDING_WINDOW

all mandatory criteria pass
+ window closed where required
+ evidence sufficient
+ independence satisfied
→ VERIFIED_PASS
material ambiguity requiring human judgment
→ ESCALATE

39. ACCEPTANCE IS NOT THE SAME AS
VERIFICATION
An outcome might be factually verified but still unacceptable.
Example:
Verified that the deployment completed, but it violated latency acceptance criteria.
Therefore:
verification of observation = PASS
acceptance decision = REJECTED
No contradiction.

40. PREDECLARED ACCEPTANCE
CRITERIA
Every consequential testable outcome should define:
what must happen
what must not happen
what must remain unchanged
what evidence will count
which measurement method
which environment
which observation window

which thresholds
what counts as inconclusive
what requires escalation
before evaluation.

41. ACCEPTANCE PREDICATE
For required conditions 𝑐𝑖:
\[ A = \bigwedge_i c_i \]
For prohibited conditions ℎ𝑗:
\[ H= \bigvee_j h_j \]
Then:
\[ Accepted = A \land \neg H \]
subject to:

𝐸𝑣𝑖𝑑𝑒𝑛𝑐𝑒𝑆𝑢𝑓𝑓𝑖𝑐𝑖𝑒𝑛𝑡 = 1
𝑂𝑏𝑠𝑒𝑟𝑣𝑎𝑡𝑖𝑜𝑛𝑊𝑖𝑛𝑑𝑜𝑤𝑆𝑎𝑡𝑖𝑠𝑓𝑖𝑒𝑑 = 1
where required.

42. CI / FULL-SUITE EVIDENCE
Contract 25 has a particularly good permanent rule in the current registry:
Until a real runner/workflow result exists: CI = UNKNOWN, not PASS.
Lock that.
Therefore:

𝑊𝑜𝑟𝑘𝑓𝑙𝑜𝑤𝐸𝑥𝑖𝑠𝑡𝑠 ≠ 𝐶𝐼𝑅𝑎𝑛
𝑇𝑒𝑠𝑡𝐸𝑥𝑖𝑠𝑡𝑠 ≠ 𝑇𝑒𝑠𝑡𝑃𝑎𝑠𝑠𝑒𝑑
𝑃𝑟𝑖𝑜𝑟𝐺𝑟𝑒𝑒𝑛𝑅𝑢𝑛 ≠ 𝐶𝑢𝑟𝑟𝑒𝑛𝑡𝐺𝑟𝑒𝑒𝑛𝑅𝑢𝑛
𝐶𝑢𝑟𝑟𝑒𝑛𝑡𝐺𝑟𝑒𝑒𝑛𝐶𝐼 ≠ 𝑃𝑟𝑜𝑑𝑢𝑐𝑡𝑖𝑜𝑛𝑃𝑟𝑜𝑜𝑓

43. TEST EVIDENCE CLASSIFICATION
VERIFY should distinguish:
STATIC VALIDATION
UNIT TEST
PROPERTY TEST
INTEGRATION TEST
ADVERSARIAL TEST
RUNTIME TEST
PRODUCTION OBSERVATION
INDEPENDENT PRODUCTION REREAD
CAUSAL EXPERIMENT
COLD SUCCESSOR REPLAY
A lower rung cannot silently establish a higher-rung claim.

44. THE PROOF LADDER
For behavioral capabilities:
SPECIFIED
↓
IMPLEMENTED
↓
TESTED
↓
RUNTIME INVOKED
↓
BEHAVIORALLY INFLUENTIAL

↓
OUTCOME OBSERVED
↓
INDEPENDENTLY VERIFIED
↓
PRODUCTION-PROVEN
↓
HELD-OUT REUSED
↓
COMPOUNDED
↓
SUCCESSOR-RETAINED
Each rung needs its own evidence.

45. PRODUCTION VERIFICATION
For a production claim:

𝑃𝑟𝑜𝑑𝑢𝑐𝑡𝑖𝑜𝑛𝑉𝑒𝑟𝑖𝑓𝑖𝑒𝑑
should generally require the appropriate combination of:
exact canonical source
deployed source identification
source/deployment parity
actual production invocation
real persisted runtime evidence
real observed outcome
independent production reread
acceptance comparison
depending on the exact claim.

46. CURRENT VERIFY HAS MIXED PARITY
Live runtime registry says:

VERIFY:
MIXED_PARITY_BOUNDED_LIVE_COMPONENTS
because:
nayanet-causal-verify
→ deployed source equals current repo
nayanet-learning-verify
→ current-source parity not established
Therefore Node 7 cannot currently be called universally current-main production-proven.
That remains the correct state.

47. CVO CONTRACT POINTER HOLE
Contract 11 currently points to:
.naya/contracts/schemas/CAUSAL-VERIFICATION-OBJECT-SCHEMA.json
but that path does not exist on current main.
At the same time, executable CVO semantics clearly exist in:
supabase/functions/nayanet-causal-verify/index.ts
NAYA-ACTIVATION/INTELLIGENCE/CVO.md
tests/test_cvo_runtime_identity_contract.py
tests/test_causal_verifier_independence.py
.github/workflows/live-cvo-runtime-proof.yml
This must be reconciled.
Do not create a parallel CVO.
Restore one canonical schema around the existing verified seam.

48. VERIFY SCHEMA NORMALIZATION

Current VERIFY schema is useful but small.
It presently contains:
expected_outcome
observed_outcome
outcome_status
acceptance_decision
causal_evidence_status
unresolved_gaps
verification_receipt
That is a good base.
The ultimate spec should extend—not replace—it with:
required_observations
observation_window
evidence_refs
proof_refs
context_receipts
execution_receipts
independence_context
causal_method
control/treatment
alternative_explanations
source/runtime revision
recomputation

49. VERIFICATION RECEIPT
Ultimate receipt:
{
"receipt_type": "VERIFY_OUTCOME",
"receipt_id": "...",
"execution_id": "...",
"node_id": "NAYA-KERNEL-VERIFY",
"task_id": "...",
"action_id": "...",

"expected_outcome": {},
"success_criteria": [],
"observed_outcome": {},
"observations": [],
"outcome_status": "...",
"acceptance_decision": "...",
"causal_claim": {},
"causal_method": "...",
"causal_status": "...",
"control_ref": null,
"treatment_ref": null,
"evidence_refs": [],
"proof_refs": [],
"alternative_explanations": [],
"unresolved_gaps": [],
"limitations": [],
"observation_window": {},
"independent_verifier": {},
"recomputation": {},
"executor_claim_trusted": false,
"source_revision": "...",
"runtime_revision": "...",
"input_hash": "...",
"output_hash": "...",
"handoff_to": "NAYA-KERNEL-LEARN",
"verified_at": "..."
}

50. RECOMPUTATION LAW

Independent verification should compute:

𝑉𝑒𝑟𝑑𝑖𝑐𝑡' = 𝑓(𝐶𝑎𝑛𝑜𝑛𝑖𝑐𝑎𝑙𝐸𝑣𝑖𝑑𝑒𝑛𝑐𝑒, 𝐸𝑥𝑝𝑒𝑐𝑡𝑒𝑑𝑂𝑢𝑡𝑐𝑜𝑚𝑒, 𝐴𝑐𝑐𝑒𝑝𝑡𝑎𝑛𝑐𝑒𝐶𝑟𝑖𝑡𝑒𝑟𝑖𝑎)
Then compare:
\[ Verdict' \stackrel{?}{=} Verdict_{recorded} \]
If:

𝑉𝑒𝑟𝑑𝑖𝑐𝑡' ≠ 𝑉𝑒𝑟𝑑𝑖𝑐𝑡𝑟𝑒𝑐𝑜𝑟𝑑𝑒𝑑
then:
VERIFICATION_MISMATCH
not:
trust the earlier receipt.

51. IDEMPOTENCY
Re-verifying identical immutable inputs at the same relevant temporal boundary should produce
the same result.
Define:
\[ VerifyKey = H( task \Vert expectedOutcome \Vert evidenceSnapshot \Vert acceptanceCriteria
\Vert observationBoundary \Vert verifierContractVersion ) \]
Identical inputs:
→ same deterministic verification
unless explicitly non-deterministic measurement uncertainty is part of the contract.

52. REPLAY

Historical verification must preserve the original evidence/time boundary.
If an observation was made at 𝑡0, replay should reconstruct:

𝑓(𝐸𝑣𝑖𝑑𝑒𝑛𝑐𝑒𝑆𝑛𝑎𝑝𝑠ℎ𝑜𝑡𝑡 )
0

not mix it with unrelated present-day state.
Later evidence can create a new verification version.
It should not rewrite old history.

53. VERIFICATION VERSIONING
Correct:
VERIFY V1 = VERIFIED_PASS at t0
↓
new evidence
VERIFY V2 = FAIL at t1
Both remain in history.
The current state becomes V2.
Historical V1 remains:
what was legitimately concluded with the evidence available then.

54. SECURITY THREAT MODEL
VERIFY must defend against:
self-certification
forged observations
forged outcome rows
forged receipts

cross-owner evidence
wrong-scope evidence
stale evidence replay
goalpost mutation
control/treatment mismatch
confound hiding
selective observation
missing-negative suppression
early-window pass
executor-verdict laundering
CI-result laundering
production-fixture substitution
local-fixture-as-live-proof
verifier identity spoofing
evidence mutation after verification
partial outcome recovery
duplicate outcome insertion

55. RECOVERY MUST NOT FABRICATE
HISTORY
Current bounded recovery mode is designed well conceptually.
Recovery may reconstruct a missing persisted outcome only when:
canonical causal receipts exist
both sides independently validate
task identity matches
evidence conditions match
no partial inconsistent state exists
recovery rereads its own persisted result
Never:
missing outcome
→ manually invent SQL row
→ call verified

56. PARTIAL-STATE RECOVERY

If one member of a required causal pair exists and the other does not:
PARTIAL STATE
should normally block automatic recovery until the discrepancy is explained.
This prevents silent historical repair from manufacturing experimental symmetry.

57. AUTHORITY DURING VERIFICATION
Verification may need permission to read protected evidence.
But:

𝐴𝑢𝑡ℎ𝑜𝑟𝑖𝑡𝑦 ≠ 𝑉𝑒𝑟𝑖𝑓𝑖𝑐𝑎𝑡𝑖𝑜𝑛𝑅𝑒𝑠𝑢𝑙𝑡
An active authority grant permits legitimate access.
It does not make the observed result successful.
Likewise:
\[ SuccessfulOutcome \nRightarrow RetroactiveAuthority \]

58. CROSS-OWNER VERIFICATION
If an outcome spans two owners:
VERIFY must preserve:
ownership
consent
derived-share boundary
proof scope
privacy
It must never reconstruct a causal claim by exposing one owner's private source to the other
without applicable consent.

59. VALUE CALCULUS INTEGRATION
The existing shared Value Calculus provides:
predicted value
actual value
verification state
calibration error
VERIFY owns the reality side.
If:

∆𝑉𝑝𝑟𝑒𝑑𝑖𝑐𝑡𝑒𝑑
was expected and later:

∆𝑉𝑎𝑐𝑡𝑢𝑎𝑙
is measured, then:

𝐶𝑎𝑙𝑖𝑏𝑟𝑎𝑡𝑖𝑜𝑛𝐸𝑟𝑟𝑜𝑟 = |∆𝑉𝑝𝑟𝑒𝑑𝑖𝑐𝑡𝑒𝑑 − ∆𝑉𝑎𝑐𝑡𝑢𝑎𝑙|
This belongs in the verification/learning loop.

60. VALUE IS NOT SUCCESS BY ITSELF
An action can have positive measured value but fail a mandatory requirement.
Likewise an action can satisfy technical success but create negative overall value.
Therefore:
outcome verification

and:
value verification
remain distinct dimensions consumed by later learning.

61. HUMAN JUDGMENT BOUNDARY
Some acceptance conditions require Shawn's judgment.
Examples might include:
brand quality
mission alignment
subjective experience
final production release
constitutional ratification
VERIFY should not fake an objective measurement.
It should return:
ESCALATE
or:
PENDING_HUMAN_ACCEPTANCE
where legitimate human acceptance is the requirement.

62. VERIFY MUST BE ABLE TO DISAGREE
WITH NAYA
This is crucial.
The proper system behavior is:
Naya:

"I think I fixed it."
VERIFY:
"The evidence does not establish that."
That disagreement is not malfunction.
It is what makes the organism trustworthy.

63. INTER-NODE BATON: ACT → VERIFY
ACT supplies:
action contract
LAW receipt
execution receipt
target
parameters
execution state
raw observations
errors
timeouts
retry state
rollback state
expected outcome
proof requirements
VERIFY must reread rather than blindly accept summarized claims where consequential.

64. PROVE → VERIFY
PROVE supplies:
claim
epistemic state
evidence
provenance
scope

limitations
unresolved gaps
VERIFY adds:
actual outcome
independent observation
acceptance
causal analysis
Then PROVE can later consume VERIFY evidence to update broader claim state.

65. CONNECT → VERIFY
CONNECT supplies:
task context
selected intelligence
relationship paths
applicability
conflicts
supersession state
context receipt
This allows VERIFY to ask:
Did the selected relationship-aware context actually affect the outcome?
Without this handoff, CONNECT can never become causally proven.

66. VERIFY → LEARN
VERIFY's outgoing baton should say:
THIS IS WHAT WAS EXPECTED.​
THIS IS WHAT ACTUALLY HAPPENED.​
THIS IS THE EVIDENCE.​
THIS IS THE ACCEPTANCE RESULT.​
THIS IS THE CAUSAL STATUS.​

THESE ALTERNATIVE EXPLANATIONS REMAIN.​
THIS OBSERVATION WINDOW IS CLOSED/OPEN.​
THIS WAS/was not INDEPENDENTLY RECOMPUTED.​
THIS IS WHAT LEARN MAY USE.​
THIS IS WHAT LEARN MUST NOT GENERALIZE.

67. LEARN MAY ONLY CONSUME
QUALIFYING OUTCOMES
A learning candidate can be created from weaker evidence.
But strong learning promotion should require an explicitly qualifying VERIFY result.
Thus:

𝐿𝑒𝑎𝑟𝑛𝑖𝑛𝑔𝐶𝑎𝑛𝑑𝑖𝑑𝑎𝑡𝑒
can exist after observation.
But:

𝑉𝑒𝑟𝑖𝑓𝑖𝑒𝑑𝐿𝑒𝑎𝑟𝑛𝑖𝑛𝑔
requires appropriate verification.
Node 8 will formalize this.

68. AAA PROPERTY TESTS
NODE 7 should enforce at least:
P1 execution ≠ outcome
P2 observation ≠ verification
P3 receipt ≠ desired outcome
P4 self-report ≠ independent verification
P5 sequence ≠ causality

P6 correlation ≠ causality
P7 implementation ≠ verification
P8 verification ≠ production proof
P9 test existence ≠ test execution
P10 CI unknown ≠ CI pass
P11 missing expected outcome ⇒ NOT_PROVEN
P12 missing observation ⇒ NOT_PROVEN
P13 insufficient evidence ⇒ INCONCLUSIVE / NOT_PROVEN
P14 explicit criterion failure ⇒ FAILURE
P15 inconclusive ≠ failure
P16 inconclusive ≠ success
P17 required observation gap blocks VERIFIED_PASS
P18 open material observation window blocks final VERIFIED_PASS
P19 delayed harm reopens provisional success
P20 acceptance criteria cannot silently change after execution
P21 causal claim requires causal method
P22 control/treatment must be materially comparable
P23 identical control/treatment behavior cannot establish claimed differential effect
P24 material confounds must be surfaced
P25 bounded experiment ≠ universal causal proof
P26 executor claim is never trusted as verification
P27 verifier rereads canonical persisted evidence
P28 verifier recomputes outcome
P29 recomputation mismatch fails verification
P30 verifier identity is explicit
P31 wrong owner evidence rejected
P32 wrong scope evidence rejected
P33 stale outcome evidence cannot prove current state
P34 recovery cannot create authority
P35 partial recovery cannot silently become complete
P36 historical verification remains immutable
P37 correction creates new lineage
P38 Value score cannot manufacture PASS
P39 human-required acceptance cannot be self-approved
P40 cold successor can independently reconstruct the result

69. GOLDEN SUCCESS TEST

Predeclared:
Expected:
production state becomes X
ACT executes.
Independent observation:
production state = X
Evidence:
correct environment
correct revision
correct target
current state reread
Expected:
outcome_status = SUCCESS
acceptance = ACCEPTED
verification = VERIFIED_PASS
provided all required windows are closed.

70. GOLDEN FAILURE TEST
Expected:
database row count = 2
Observed independently:
database row count = 1
Expected:
FAILURE
REJECTED
Not:
INCONCLUSIVE

because we actually know the criterion failed.

71. GOLDEN NOT-PROVEN TEST
ACT receipt says:
SUCCESS
but no independent observation exists.
Expected:
NOT_PROVEN
PENDING
Never:
ACT SUCCESS → VERIFY SUCCESS

72. GOLDEN INCONCLUSIVE TEST
Two valid measurements disagree within material tolerance and no method currently resolves
the conflict.
Expected:
INCONCLUSIVE
PENDING
unresolved_gaps = [...]
This is a correct system state.

73. GOLDEN CAUSAL TEST
Control:
same task

without retained intelligence
→ provenance preserved = false
Treatment:
same task
with retained intelligence
→ provenance preserved = true
Required equivalence passes.
Independent persisted outcomes pass.
Expected bounded conclusion:
CAUSAL_SUPPORTED
for the declared experiment.
Not:
“NayaPOWER learning universally improves every task.”

74. GOLDEN IDENTICAL-BEHAVIOR
NEGATIVE
Control:
behavior = X
Treatment:
behavior = X
Executor claims:
CAUSAL_SUPPORTED
Independent recomputation must return:
NO_BEHAVIORAL_DELTA
→ CAUSAL NOT ESTABLISHED

This exact failure class is already defended in repository tests.

75. GOLDEN CONFOUND TEST
Control and treatment differ in:
intelligence
+
model version
+
task input
Observed outputs differ.
Expected:
CAUSAL_INCONCLUSIVE
because intervention isolation failed.

76. GOLDEN OBSERVATION-WINDOW
TEST
Immediate checks pass.
Required seven-day stability window remains open.
Expected:
PASS_PENDING_WINDOW
After the window closes with no material failure:
VERIFIED_PASS
If delayed harm occurs:
FAIL

77. GOLDEN PRODUCTION-FIXTURE
TEST
Local test fixture passes.
Production evidence absent.
Expected:
TESTED
production_status = NOT_PROVEN
Never:
fixture → production proof

78. GOLDEN CI TEST
Workflow YAML exists.
No actual run result.
Expected:
CI = UNKNOWN
Actual current runner result exists and passes:
CI = PASS
but:
CI PASS ≠ production outcome proof

79. GOLDEN CROSS-OWNER TEST

Verification evidence references Owner B private evidence while evaluating Owner A context.
No consent.
Expected:
BLOCKED
No cross-owner leakage merely because verification would be useful.

80. GOLDEN RECOVERY TEST
Both historical causal receipts exist.
No outcomes persist.
Verifier independently reconstructs:
same task
same learning
control condition
treatment condition
expected behavioral difference
writes the bounded missing outcome pair and immediately rereads them.
Expected:
CREATED_AND_REREAD
Repeated run:
REPLAYED_AND_REREAD
No duplicate semantics.

81. GOLDEN COLD-SUCCESSOR TEST
Fresh Naya receives only canonical persisted state.

It reconstructs:
what action was taken
what success meant
what was observed
where observations came from
whether they passed
whether causal attribution was claimed
what control existed
what treatment existed
what the verifier recomputed
which gaps remained
what LEARN is allowed to consume
No hidden conversation required.

82. WHAT “INFLUENTIAL” MEANS FOR
VERIFY
VERIFY is not influential merely because it creates receipts.
A real behavioral test requires:
Same downstream learning opportunity
CASE A
verification = VERIFIED_PASS
→ learning may proceed
CASE B
verification = NOT_PROVEN / FAIL
→ learning promotion blocked or altered
If LEARN behaves identically regardless of VERIFY outcome:
VERIFY is decorative.

83. WHAT “VERIFIED” MEANS FOR
VERIFY ITSELF
There is an amusing but important recursive boundary.
VERIFY cannot simply say:
“I verified myself.”
Node 7's own capability must be demonstrated through independent evidence that:
given known expected/observed inputs
↓
VERIFY produces correct state
↓
negative controls reject
↓
independent recomputation agrees
The proof of the verifier must itself obey the verification law.

84. WHAT “PRODUCTION-PROVEN”
MEANS FOR NODE 7
For declared scope:
exact source
→ exact deployed verifier
→ deployed/source parity
→ fresh authenticated verifier identity
→ real persisted action/outcome
→ positive outcome case
→ failure case
→ NOT_PROVEN case
→ causal positive
→ causal negative
→ task-equivalence negative
→ delayed-window handling
→ replay/idempotency

→ independent reread
→ persisted verification receipt
→ VERIFY changes LEARN eligibility
→ cold successor reconstruction
Then we can call that scope production-proven.

85. CURRENT NODE 7 TRUTH
Strong and already present
VERIFY semantic contract
VERIFY machine contract
VERIFY AI contract
kernel VERIFY schema
VERIFY intelligent object
executable nayanet-causal-verify
real GitHub OIDC verifier identity
persisted receipt reread
persisted outcome reread
control/treatment semantics
CONTROLLED_INTERVENTION
CAUSAL_SUPPORTED bounded runtime shape
OUTCOME_VERIFIED runtime state
alternative explanations
explicit bounded-experiment limitation
independent verification workflow
fresh OIDC verification job
causal verifier independence tests
task-equivalence tests
self-certification guards
historical outcome recovery
recovery reread
partial-state protection
Value Calculus verification states
UNVERIFIED
PASS_PENDING_WINDOW
VERIFIED_PASS

FAIL
ESCALATE

Still open
Contract 11 still PROPOSED
Contract 23 still PROPOSED
Contract 25 still PROPOSED
Contract 11 points to missing CVO schema file
VERIFY Node object understates real bounded runtime capability
VERIFY Node object still NOT_PROVEN overall
VERIFY schema and Value Calculus verification vocabulary are not fully reconciled
outcome / acceptance / causality / verification axes need canonical mapping
nayanet-learning-verify not current-source parity
VERIFY runtime architecture is distributed across bounded components
current CVO implementation remains Node-0001-specific
current causal behavior does not generalize automatically
full current-main nine-node VERIFY influence not proven
VERIFY→LEARN behavioral gate is not universally proven
cold-successor universal verification reconstruction not proven
That is the proper evidence boundary.

86. THE CANONICAL ROUTING I WOULD
LOCK
ACT ────────┐
│
PROVE ──────┼──→ VERIFY ──→ LEARN
│
CONNECT ────┘
Where:

ACT provides

what was executed.

PROVE provides
what evidence/claims are epistemically supportable.

CONNECT provides
what context and relationships mattered.

VERIFY establishes
what actually happened and whether the claimed outcome/causality is supported.

LEARN decides
what should change next time.
That is an extremely clean organism.

87. THE COMPLETE FIRST SEVEN NODES
We now have:

NODE 1 — SELF
Who am I, what is my mission, and what state am I in?

NODE 2 — LAW
What governs me and what am I actually authorized to do?

NODE 3 — ACT
What exact authorized action should I perform safely?

NODE 4 — KNOW
What durable intelligence do I have?

NODE 5 — PROVE

What am I justified in believing?

NODE 6 — CONNECT
What intelligence matters together right now?

NODE 7 — VERIFY
What actually happened, did it satisfy the success boundary, and what
caused the result?
That is becoming a legitimate cognitive operating architecture.

88. NODE 7 AAA CHECKLIST
Layer

Requirement

Semantic

exact VERIFY responsibility

Expected
outcome

predeclared

Acceptance

predeclared where possible

Observation

first-class

Outcome

normalized

Failure

distinct

NOT_PROVEN

distinct

Inconclusive

distinct

Acceptance

separate axis

Causality

separate axis

Window

delayed outcome support

CVO

one canonical schema

Control

supported

Treatment

supported

Equivalence

checked

Confounds

surfaced

Alternatives

surfaced

Independence

explicit

Reread

canonical

Recomputation

deterministic

Executor trust

false

Evidence

provenance-bound

Privacy

enforced

Authority

separate

CI

real-run requirement

Production

exact environment

Recovery

bounded/idempotent

History

immutable

Value

predicted vs actual

ACT

consumes execution reality

PROVE

consumes proof context

CONNECT

consumes context lineage

LEARN

only qualifying outcomes

Receipt

deterministic

Security

adversarial

Runtime

actual

Behavior

changes LEARN eligibility

Production proof

independent

Successor

reconstructable

89. THE ULTIMATE VERIFY QUESTION
Every consequential VERIFY invocation reduces to:
“What exactly was supposed to happen, what actually happened, how was it
observed, what evidence establishes that observation, which acceptance
criteria passed or failed, what remains unknown, whether the required
observation window is complete, whether any claimed causal attribution
survives an appropriate control/comparison and alternative-explanation
analysis, and whether an independent verifier can reconstruct the same
conclusion without trusting the executor?”
That is NODE 7.

90. THE FINAL VERIFY EQUATION
\[ \boxed{ EXPECTED + EXECUTION + OBSERVATION + EVIDENCE + COMPARISON +
ACCEPTANCE\ CRITERIA + INDEPENDENT\ RECOMPUTATION = VERIFIED\ OUTCOME } \]
For causal claims:
\[ \boxed{ VERIFIED\ OUTCOME + CONTROL + TREATMENT + TASK\ EQUIVALENCE +
INTERVENTION\ ISOLATION + CONFOUND\ ANALYSIS + INDEPENDENT\
RECOMPUTATION = BOUNDED\ CAUSAL\ SUPPORT } \]
Always subject to:

𝐸𝑋𝐸𝐶𝑈𝑇𝐸𝐷 ≠ 𝑆𝑈𝐶𝐶𝐸𝑆𝑆𝐹𝑈𝐿
𝑂𝐵𝑆𝐸𝑅𝑉𝐸𝐷 ≠ 𝑉𝐸𝑅𝐼𝐹𝐼𝐸𝐷
𝑆𝐸𝐿𝐹 𝑅𝐸𝑃𝑂𝑅𝑇 ≠ 𝐼𝑁𝐷𝐸𝑃𝐸𝑁𝐷𝐸𝑁𝑇 𝑃𝑅𝑂𝑂𝐹
𝑆𝐸𝑄𝑈𝐸𝑁𝐶𝐸 ≠ 𝐶𝐴𝑈𝑆𝐴𝑇𝐼𝑂𝑁
𝐶𝑂𝑅𝑅𝐸𝐿𝐴𝑇𝐼𝑂𝑁 ≠ 𝐶𝐴𝑈𝑆𝐴𝑇𝐼𝑂𝑁

𝐼𝑁𝐶𝑂𝑁𝐶𝐿𝑈𝑆𝐼𝑉𝐸 ≠ 𝐹𝐴𝐼𝐿𝑈𝑅𝐸
𝐼𝑁𝐶𝑂𝑁𝐶𝐿𝑈𝑆𝐼𝑉𝐸 ≠ 𝑆𝑈𝐶𝐶𝐸𝑆𝑆
𝑁𝑂𝑇 𝑃𝑅𝑂𝑉𝐸𝑁 ≠ 𝐹𝐴𝐿𝑆𝐸
𝑉𝐸𝑅𝐼𝐹𝐼𝐸𝐷 ≠ 𝑈𝑁𝐼𝑉𝐸𝑅𝑆𝐴𝐿
𝐶𝐼 𝑃𝐴𝑆𝑆 ≠ 𝑃𝑅𝑂𝐷𝑈𝐶𝑇𝐼𝑂𝑁 𝑃𝑅𝑂𝑂𝐹
𝐶𝑉𝑂 ≠ 𝐴𝑈𝑇𝐻𝑂𝑅𝐼𝑇𝑌
and finally:
\[ \boxed{ ACT\ CREATES\ REALITY \rightarrow VERIFY\ MEASURES\ REALITY \rightarrow
LEARN\ EARNS\ CHANGE } \]

Lock recommendation
This is the MN-07 VERIFY normative design target I would lock.
The most important architectural move is to preserve four separate axes rather than trying to
stuff everything into one success field:
\[ \boxed{ OUTCOME \neq ACCEPTANCE \neq CAUSALITY \neq VERIFICATION\ MATURITY }
\]
That resolves several current semantic seams while preserving all of the existing bounded CVO
machinery.


---

## CANDIDATE AMENDMENTS — Naya 2 scorecard corrections (NOT RATIFIED)

> Status: PROPOSED. Drafted by the Naya 2 independent-review lane from
> BRAIN/03-KERNEL/0006-NODE-SPECS-INDEPENDENT-SCORECARD-V1.md (2026-10-01, mean
> score 8.8/10). These amendments are CANDIDATE — not ratified, not merged to
> main. Each must be applied (or explicitly rejected with written reason) before
> any lock of this spec. Nothing above this line was altered: the verbatim PDF
> text is preserved intact. References (V1, X1, X2, X3, X7) map to the
> scorecard's correction list.

### A-VERIFY-1 [X1 — Prime 1 / Amendment 0002 subordination]

Add: "This spec operates under Amendment 0002 (Prime 1, the Judgment Rule,
ratified 2026-09-30); where this spec and Prime 1 conflict, Prime 1 governs."
REQUIRED before lock.

### A-VERIFY-2 [X2 — semantic order vs runtime call order]

Add an explicit order-mapping note: the organism order
SELF→LAW→ACT→KNOW→PROVE→CONNECT→VERIFY→LEARN→EVOLVE→SELF is responsibility
order, not invocation order. Kernel.decide() will call nodes in a different
sequence; VERIFY's independence duties do not depend on call position.

### A-VERIFY-3 [V1 — independence criterion as acceptance test]

Write the independence criterion as a machine-checkable acceptance test, not
prose: the verifier must have (a) a distinct identity from the claimant, (b) a
distinct evidence path, and (c) no shared mutable state with the claimant's
execution. A verification run that fails any of the three FAILS acceptance —
no self-verification, no shared-state verification. Tonight's builder/verifier
seat separation satisfies this in practice; the spec must demand it in
principle.

### A-VERIFY-4 [X3 + X7 — topology and the CONNECT handoff]

Reference the PROVE→CONNECT→VERIFY topology decision once made: CONNECT routes
context, VERIFY establishes causality and outcomes. Causal claims require the
CONNECT handoff confirmed — VERIFY establishes CAUSED edges; CONNECT must not
mint them. No node duplicates another's verdict.

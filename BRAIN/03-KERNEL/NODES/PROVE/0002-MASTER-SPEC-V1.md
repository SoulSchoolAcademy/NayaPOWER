# PROVE Node Master Specification V1 — CANDIDATE

**Source PDF:** NayaPOWER___NODE_5__PROVE.pdf (uploaded 2026-09-30, extracted 2026-10-01, 5184 words)
**Status:** CANDIDATE — NOT RATIFIED. "Final Organ Lock" in the source means normative-target lock, not constitutional ratification. EVOLVE charter / constitutional changes remain human-only.
**Independent review:** BRAIN/03-KERNEL/0006-NODE-SPECS-INDEPENDENT-SCORECARD-V1.md (same branch)
**Canonical home:** this file. Runtime implementation lives in naya_kernel/ on naya4/* (separate lane) and must reference — not duplicate — this spec.

---

🔱 NayaPOWER — NODE 5: PROVE
Ultimate Master Specification V1 — Lock Candidate
Node ID: MN-05​
Kernel ID: NAYAPOWER-MASTER-KERNEL-V1​
Canonical Runtime ID: NAYA-KERNEL-PROVE​
Canonical Key: PROVE​
Primary Responsibility: Truth, Evidence, Provenance, Epistemic State, Lineage,
Accountability, Claim Strength​
Primary Contracts: 07 — Provenance / Lineage, 10 — Truth-State / Evidence,
16 — Smart Ledger​
Human Director: Shawn Vibert
Organism:
SELF → LAW → ACT → KNOW → PROVE → CONNECT → VERIFY → LEARN → EVOLVE
→ SELF
PROVE belongs to the Cognition Triad:
KNOW → PROVE → CONNECT
The three questions are:
KNOW: What intelligence do we have?​
PROVE: Why should we believe it, and exactly how strongly?​
CONNECT: Where does it actually matter?

0. THE SIMPLEST DEFINITION
Child
PROVE is the part of Naya that asks:
“How do we actually know that?”
Grandma

PROVE keeps Naya from saying something is true just because it sounds right, somebody said
it, a computer wrote it, or something happened once.
Engineering
PROVE is the governed epistemic organ that converts claims, canonical evidence,
provenance, scope, time, verification methods, limitations, contradictions, and lineage
into bounded, reconstructable proof records whose claim strength can never exceed the
evidence that supports them.
Naya
I do not make something true by believing it.​
I do not make something proven by implementing it.​
I do not make something verified by running it.​
I do not make something production-proven by passing a test.​
I preserve exactly what the evidence establishes — and nothing more.

1. WHY PROVE EXISTS
Without PROVE, an intelligent system naturally collapses:
INFORMATION
→ CONFIDENCE
→ ASSERTION
→ "TRUTH"
That is unacceptable.
NayaPOWER needs:
CLAIM
↓
EVIDENCE
↓
PROVENANCE
↓
SCOPE
↓
METHOD
↓
CONFLICT CHECK

↓
LIMITATIONS
↓
CLAIM CEILING
↓
PROOF RECORD
PROVE exists to stop five dangerous substitutions:
ASSERTION ≠ EVIDENCE
IMPLEMENTATION ≠ VERIFICATION
EXECUTION ≠ SUCCESS
CORRELATION ≠ CAUSATION
CONFIDENCE ≠ TRUTH

2. THE DEEPEST PROVE LAW
The permanent equation remains:
\[ \boxed{\text{CLAIM STRENGTH} \leq \text{EVIDENCE STRENGTH}} \]
But I would make the ultimate machine meaning stronger:
For claim 𝑐, let its mandatory proof obligations be:
\[ O(c)=\{o_1,o_2,\dots,o_n\} \]
For each mandatory obligation 𝑜𝑗, determine the strongest admissible evidence satisfying it:
\[ E_j = \max Strength(e \mid e \text{ validly satisfies } o_j) \]
Then:

𝐸𝑒𝑓𝑓𝑒𝑐𝑡𝑖𝑣𝑒(𝑐) =

min 𝐸𝑗

𝑜𝑗∈𝑂(𝑐)

and therefore:
\[ \boxed{ Strength(c) \le E_{\text{effective}}(c) } \]
This is important.
We do not average away one missing critical proof requirement.

Nine excellent pieces of evidence cannot compensate for one missing proof obligation that is
essential to the claim.

3. THE SECOND MASTER LAW
MISSING PROOF DOES NOT BECOME POSITIVE
EVIDENCE.
Therefore:

𝑈𝑁𝐾𝑁𝑂𝑊𝑁 ≠ 𝑉𝐸𝑅𝐼𝐹𝐼𝐸𝐷
𝐵𝐿𝑂𝐶𝐾𝐸𝐷 ≠ 𝑃𝐴𝑆𝑆
𝐼𝑀𝑃𝐿𝐸𝑀𝐸𝑁𝑇𝐸𝐷 ≠ 𝑉𝐸𝑅𝐼𝐹𝐼𝐸𝐷
𝑇𝐸𝑆𝑇𝐸𝐷 ≠ 𝑉𝐸𝑅𝐼𝐹𝐼𝐸𝐷
𝑉𝐸𝑅𝐼𝐹𝐼𝐸𝐷 ≠ 𝑃𝑅𝑂𝐷𝑈𝐶𝑇𝐼𝑂𝑁_𝑃𝑅𝑂𝑉𝐸𝑁
𝑅𝐸𝐶𝐸𝐼𝑃𝑇 ≠ 𝑂𝑈𝑇𝐶𝑂𝑀𝐸
𝐿𝐸𝐴𝑅𝑁𝐼𝑁𝐺_𝐿𝐴𝐵𝐸𝐿 ≠ 𝑉𝐸𝑅𝐼𝐹𝐼𝐸𝐷_𝐿𝐸𝐴𝑅𝑁𝐼𝑁𝐺
𝑁𝑂 𝐶𝑂𝑁𝑇𝑅𝐴𝐷𝐼𝐶𝑇𝐼𝑂𝑁 𝐹𝑂𝑈𝑁𝐷 ≠ 𝑃𝑅𝑂𝑉𝐸𝑁 𝑇𝑅𝑈𝐸
𝐶𝑂𝑁𝐹𝐼𝐷𝐸𝑁𝐶𝐸 = 1. 0 ≠ 𝑉𝐸𝑅𝐼𝐹𝐼𝐸𝐷
𝑄(𝑎) = 10 ≠ 𝑉𝐸𝑅𝐼𝐹𝐼𝐸𝐷
∆𝑉(𝑎) > 0 ≠ 𝑉𝐸𝑅𝐼𝐹𝐼𝐸𝐷
These become machine-testable invariants.

4. PROVE OWNS

PROVE owns the semantic responsibility for:
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

claims;
claim identity;
claim scope;
epistemic status;
evidence classification;
evidence references;
evidence strength;
claim strength;
provenance validation;
lineage reconstruction;
proof obligations;
proof methods;
method limitations;
evidence freshness;
evidence applicability to the exact claim;
contradiction evidence;
supporting evidence;
negative evidence;
uncertainty;
unresolved gaps;
source attribution;
proof receipts;
proof records;
proof lineage;
Smart Ledger proof/accountability projection;
historical reconstruction;
integrity hashes for proof artifacts;
evidence-bound confidence;
proof ceilings;
evidence downgrade;
claim downgrade;
correction;
retraction;
supersession;
staleness;
proof-context handoff.

5. PROVE MUST NEVER OWN

PROVE must not own:
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

constitutional authority;
consent creation;
execution authority;
human sovereignty;
canonical memory creation;
Intelligent Block identity allocation;
relationship applicability;
execution;
causal outcome determination;
independent outcome verification;
learning promotion;
value authority;
constitutional amendment;
self-ratification;
self-issued proof;
a second ledger;
a second truth database;
a second Value Calculus;
a second verification engine.

The organism stays:

ONE BRAIN. ONE LEDGER SUBSTRATE. ONE
AUTHORITY MODEL. ONE INTELLIGENCE RIVER.

6. PROVE VS VERIFY — THE CRITICAL
SEPARATION
This distinction must be airtight.

PROVE asks:
“What does the available evidence legitimately support?”

VERIFY asks:

“Did the claimed outcome actually occur, and when required, was the claimed
causal relationship established?”
So:
PROVE
= epistemic compiler / evidence assessor
VERIFY
= independent outcome / causal / acceptance boundary
Example:
ACT says:
“I deployed revision X.”
PROVE may establish:
There is a deployment receipt stating revision X was deployed.
But PROVE does not automatically conclude:
Production is correctly running revision X.
VERIFY independently rereads production.
That evidence can come back to PROVE.
Then PROVE may update the claim.
The loop becomes:
CLAIM
↓
PROVE
↓
WHAT IS CURRENTLY SUPPORTED?
↓
VERIFY
↓
WHAT ACTUALLY HAPPENED?
↓
PROVE
↓
WHAT MAY NOW BE CLAIMED?

This is one of the strongest distinctions in the whole organism.

7. CLAIMS MUST BE OBJECTS
A consequential claim should not exist as vague prose.
Conceptually:
{
"claim_id": "...",
"claim_type": "...",
"subject": "...",
"predicate": "...",
"object": "...",
"scope": {},
"time_context": {},
"environment": "...",
"source_revision": "...",
"epistemic_state": "...",
"claim_strength": "...",
"proof_obligations": [],
"evidence_refs": [],
"counterevidence_refs": [],
"verification_method": "...",
"verifier_requirements": {},
"limitations": [],
"unresolved_gaps": [],
"conflicts": [],
"provenance": {},
"supersedes_claim_id": null,
"created_at": "...",
"updated_at": "..."
}

A claim without defined scope is dangerous.
“PROVE works” is too vague.
Better:
“At source revision X, repository tests independently recompute PROVE's bounded
KNOW assessment logic and pass.”
Different claim from:
“PROVE is deployed.”
Different again from:
“PROVE is production-proven.”

8. CLAIM CLASSIFICATION
PROVE should know the type of claim because different claims require different proof.
Canonical conceptual classes:
EXISTENCE
INTEGRITY
SOURCE
IMPLEMENTATION
TESTED
RUNTIME_LOADED
RUNTIME_INVOKED
BEHAVIORAL_INFLUENCE
ACTION_EXECUTED
OUTCOME_OBSERVED
OUTCOME_VERIFIED
CAUSAL
PRODUCTION_PARITY
PRODUCTION_PROVEN
LEARNING
COMPOUNDING
SUCCESSOR_CONTINUITY
VALUE
That solves a huge proof problem.

The evidence required to prove:
“a file exists”
is radically different from:
“this intelligence caused a better future outcome.”

9. PROOF OBLIGATION LAW
Every claim class must resolve an explicit set:
\[ O(c)=\{o_1,o_2,\dots,o_n\} \]
Example:

IMPLEMENTED claim
May require:
canonical source exists
schema valid
implementation reachable
revision identified

TESTED claim
Adds:
test exists
test actually ran
test passed
test targets the declared behavior

VERIFIED claim
Adds:
appropriate verification method
independent or appropriately separated verifier
canonical evidence
recomputation / reread

declared claim matches observed evidence

PRODUCTION-PROVEN claim
Adds:
exact source revision
deployment evidence
deployed-source parity
real production invocation
persisted runtime receipt
persisted outcome where applicable
independent production reread
independent verification
scope-specific acceptance
No universal “proof blob.”
Proof requirements depend on the exact claim.

10. EVIDENCE MUST BE AN OBJECT
Conceptually:
{
"evidence_id": "...",
"evidence_type": "...",
"source": "...",
"source_identity": "...",
"source_revision": "...",
"content_hash": "...",
"provenance": {},
"owner_id": "...",
"scope": {},
"observed_at": "...",
"valid_from": "...",
"valid_until": "...",

"method": "...",
"integrity_state": "...",
"directness": "...",
"independence": "...",
"reproducibility": "...",
"strength": "...",
"supports": [],
"contradicts": [],
"limitations": [],
"supersedes_evidence_id": null
}
Evidence itself needs evidence about where it came from.
Otherwise it becomes a floating assertion.

11. EVIDENCE ADMISSIBILITY
Before evidence receives a strength, it must pass hard gates.
Define:
\[ A(e,c)= I(e) \land P(e) \land S(e,c) \land T(e,c) \land M(e,c) \land O(e,c) \]
Where:
●​
●​
●​
●​
●​
●​

𝐼 = integrity is valid;
𝑃 = provenance is sufficient;
𝑆 = evidence scope matches claim scope;
𝑇 = temporal validity is acceptable;
𝑀 = verification/evidence method is valid for this claim;
𝑂 = evidence was lawfully accessible under ownership/privacy boundaries.

Then:

𝐴(𝑒, 𝑐) = 0 ⇒ 𝑒𝑐𝑎𝑛𝑛𝑜𝑡𝑝𝑟𝑜𝑚𝑜𝑡𝑒𝑐

Unknown required gate:

𝑈𝑁𝐾𝑁𝑂𝑊𝑁 ⇒ 𝑁𝑂 𝑃𝑅𝑂𝑀𝑂𝑇𝐼𝑂𝑁
not:

𝑈𝑁𝐾𝑁𝑂𝑊𝑁 ⇒ 𝐴𝑆𝑆𝑈𝑀𝐸 𝑃𝐴𝑆𝑆

12. EVIDENCE STRENGTH
The current proof-record schema already recognizes:
WEAK
MODERATE
STRONG
CONCLUSIVE
I would preserve those as an ordinal scale, not pretend they are probabilities.
Define:

𝑟𝑎𝑛𝑘(𝑊𝐸𝐴𝐾) = 1
𝑟𝑎𝑛𝑘(𝑀𝑂𝐷𝐸𝑅𝐴𝑇𝐸) = 2
𝑟𝑎𝑛𝑘(𝑆𝑇𝑅𝑂𝑁𝐺) = 3
𝑟𝑎𝑛𝑘(𝐶𝑂𝑁𝐶𝐿𝑈𝑆𝐼𝑉𝐸) = 4
Current PROVE runtime is intentionally more conservative and only emits bounded
WEAK/STRONG evidence and WEAK/MODERATE claim strength.
That is fine.
The ultimate contract can support richer classification without pretending today's runtime
already does.

13. CLAIM STRENGTH
Current node schema allows:
WEAK
MODERATE
STRONG
Then:

𝑟𝑎𝑛𝑘(𝐶𝑙𝑎𝑖𝑚𝑆𝑡𝑟𝑒𝑛𝑔𝑡ℎ) ≤ min (3, 𝐸𝑒𝑓𝑓𝑒𝑐𝑡𝑖𝑣𝑒)
The CONCLUSIVE category belongs to evidence strength.
It does not mean a claim becomes metaphysically certain.

14. PROOF COVERAGE
For mandatory obligations:

𝐶𝑜𝑣𝑒𝑟𝑎𝑔𝑒(𝑐) =

|{𝑜∈𝑂(𝑐):𝑆𝑎𝑡𝑖𝑠𝑓𝑖𝑒𝑑(𝑜)}|
|𝑂(𝑐)|

For full verification:

𝑉𝐸𝑅𝐼𝐹𝐼𝐸𝐷(𝑐) ⇒ 𝐶𝑜𝑣𝑒𝑟𝑎𝑔𝑒(𝑐) = 1
For production proof:

𝑃𝑅𝑂𝐷𝑈𝐶𝑇𝐼𝑂𝑁_𝑃𝑅𝑂𝑉𝐸𝑁(𝑐) ⇒ 𝐶𝑜𝑣𝑒𝑟𝑎𝑔𝑒𝑝𝑟𝑜𝑑𝑢𝑐𝑡𝑖𝑜𝑛(𝑐) = 1
A 95% complete proof package with one critical missing requirement remains incomplete.

15. OPTIONAL CORROBORATION MUST
NOT LAUNDER A GAP
Ten copied reports from the same original source do not equal ten independent sources.
Define the root provenance family:

𝑅𝑜𝑜𝑡(𝑒) = 𝑒𝑎𝑟𝑙𝑖𝑒𝑠𝑡𝑚𝑎𝑡𝑒𝑟𝑖𝑎𝑙𝑒𝑣𝑖𝑑𝑒𝑛𝑐𝑒𝑎𝑛𝑐𝑒𝑠𝑡𝑜𝑟
If:

𝑅𝑜𝑜𝑡(𝑒1) = 𝑅𝑜𝑜𝑡(𝑒2)
then they must not automatically count as independent corroboration.
So:
ARTICLE A
→ summarized by AI B
→ summarized by AI C
→ quoted by AI D
is still fundamentally one evidence family.
This prevents evidence multiplication by copying.

16. INDEPENDENCE
Define:
\[ Independent(e_1,e_2)= \begin{cases} 0,& Root(e_1)=Root(e_2)\ \text{without independent
observation}\\ 1,& materially independent observation/method/trust boundary exists \end{cases}
\]
For claims requiring independent verification:

∃𝑒𝑣: 𝐼𝑛𝑑𝑒𝑝𝑒𝑛𝑑𝑒𝑛𝑡(𝑒𝑣, 𝑝𝑟𝑜𝑑𝑢𝑐𝑒𝑟_𝑒𝑣𝑖𝑑𝑒𝑛𝑐𝑒) = 1

must hold.
A second function call owned by the same producer is not automatically independent
verification.

17. DIRECT EVIDENCE VS INFERENCE
PROVE must distinguish:
DIRECT OBSERVATION
DERIVED FACT
INFERENCE
PREDICTION
ASSUMPTION
OPINION
Example:
Direct:
database row contains X.
Inference:
therefore runtime probably used X.
Those are not equivalent.
A strong inference must remain labeled inference until direct evidence closes the gap.

18. POSITIVE VS NEGATIVE EVIDENCE
Evidence can:
SUPPORT
CONTRADICT
FAIL_TO_SUPPORT
BE_IRRELEVANT
BE_INCONCLUSIVE

Important:

𝑁𝑜𝐸𝑣𝑖𝑑𝑒𝑛𝑐𝑒𝐹𝑜𝑟(𝑐) ≠ 𝐸𝑣𝑖𝑑𝑒𝑛𝑐𝑒𝐴𝑔𝑎𝑖𝑛𝑠𝑡(𝑐)
and:

𝐸𝑣𝑖𝑑𝑒𝑛𝑐𝑒𝐴𝑔𝑎𝑖𝑛𝑠𝑡(𝑐) ≠ 𝑃𝑟𝑜𝑜𝑓𝑂𝑓(¬𝑐)
unless the method supports that conclusion.
This matters tremendously in debugging and science-like reasoning.

19. CONTRADICTION LAW
Current PROVE runtime already has a good fail-closed pattern:

Verified contradiction
claim
+
verified contradiction
→ CONTRADICTED
→ NO PROMOTION

Supported unresolved contradiction
claim
+
credible unresolved contradiction
→ CONFLICTED / UNVERIFIED
→ NO PROMOTION
Never:
support + contradiction
→ average them together
→ call it mostly true
Contradiction is a first-class state.

20. MATERIAL CONFLICT PRECEDENCE
For a claim requiring promotion:

𝑀𝑎𝑡𝑒𝑟𝑖𝑎𝑙𝑉𝑒𝑟𝑖𝑓𝑖𝑒𝑑𝐶𝑜𝑛𝑓𝑙𝑖𝑐𝑡(𝑐) = 1 ⇒ 𝑃𝑟𝑜𝑚𝑜𝑡𝑒(𝑐) = 0
If conflict remains unresolved:

𝑀𝑎𝑡𝑒𝑟𝑖𝑎𝑙𝐶𝑜𝑛𝑓𝑙𝑖𝑐𝑡(𝑐) = 𝑈𝑁𝐾𝑁𝑂𝑊𝑁 ⇒ 𝑃𝑟𝑜𝑚𝑜𝑡𝑒(𝑐) = 0
This follows the organism-wide principle:

UNKNOWN NEVER SILENTLY BECOMES PASS.

21. SCOPE
Proof is always scoped.
A claim should answer:
WHAT
WHERE
WHEN
WHICH VERSION
WHICH OWNER
WHICH ENVIRONMENT
WHICH POPULATION
WHICH ACTION
WHICH TASK
WHICH ASSUMPTIONS
Example:
PROVE repository tests pass at revision X.
does not establish:
deployed PROVE behaves identically in production.

Scope widening requires new evidence.

22. TEMPORAL PROOF
Evidence ages.
Define:

𝑇𝑒𝑚𝑝𝑜𝑟𝑎𝑙𝑉𝑎𝑙𝑖𝑑𝑖𝑡𝑦(𝑒, 𝑡) ∈ {𝐶𝑈𝑅𝑅𝐸𝑁𝑇, 𝑆𝑇𝐴𝐿𝐸, 𝐸𝑋𝑃𝐼𝑅𝐸𝐷, 𝐹𝑈𝑇𝑈𝑅𝐸, 𝑈𝑁𝐾𝑁𝑂𝑊𝑁}
For evidence with bounded validity:
\[ CURRENT(e,t) \iff valid\_from(e)\le t < valid\_until(e) \]
If a system changes materially after the evidence was produced, proof may become:
STALE
without becoming historically false.
That distinction matters.

23. HISTORICAL TRUTH ≠ CURRENT
TRUTH
A proof receipt from yesterday may accurately prove:
revision A was deployed yesterday.
It does not automatically prove:
revision A is deployed now.
Therefore:
\[ HistoricalProof(c,t_0) \nRightarrow CurrentProof(c,t_1) \]

unless continuity evidence bridges 𝑡0 → 𝑡1.

24. SOURCE PARITY
For code-backed runtime claims:

𝑆𝑜𝑢𝑟𝑐𝑒𝑃𝑎𝑟𝑖𝑡𝑦 = 𝐻𝑎𝑠ℎ(𝑠𝑜𝑢𝑟𝑐𝑒𝑐𝑎𝑛𝑜𝑛𝑖𝑐𝑎𝑙) = 𝐻𝑎𝑠ℎ(𝑠𝑜𝑢𝑟𝑐𝑒𝑑𝑒𝑝𝑙𝑜𝑦𝑒𝑑)
But:

𝑆𝑜𝑢𝑟𝑐𝑒𝑃𝑎𝑟𝑖𝑡𝑦 ≠ 𝐵𝑒ℎ𝑎𝑣𝑖𝑜𝑟𝑎𝑙𝑃𝑟𝑜𝑜𝑓
Parity establishes that the deployed source matches.
It does not establish that the runtime:
●​
●​
●​
●​

loaded correctly;
received the right inputs;
influenced behavior;
produced the expected outcome.

25. RECEIPT LAW
A receipt establishes:
a governed record exists saying that some transition occurred.
It does not automatically establish:
the claimed external effect occurred.
Therefore:

𝑅𝑒𝑐𝑒𝑖𝑝𝑡(𝑎𝑐𝑡𝑖𝑜𝑛) ≠ 𝑉𝑒𝑟𝑖𝑓𝑖𝑒𝑑𝑂𝑢𝑡𝑐𝑜𝑚𝑒(𝑎𝑐𝑡𝑖𝑜𝑛)
Similarly:

𝐻𝑇𝑇𝑃 200 ≠ 𝐷𝑒𝑠𝑖𝑟𝑒𝑑𝑂𝑢𝑡𝑐𝑜𝑚𝑒
𝑒𝑥𝑖𝑡 𝑐𝑜𝑑𝑒 0 ≠ 𝑃𝑟𝑜𝑑𝑢𝑐𝑡𝑖𝑜𝑛𝑃𝑟𝑜𝑜𝑓
𝑤𝑜𝑟𝑘𝑓𝑙𝑜𝑤 𝑃𝐴𝑆𝑆 ≠ 𝑈𝑛𝑖𝑣𝑒𝑟𝑠𝑎𝑙𝐵𝑒ℎ𝑎𝑣𝑖𝑜𝑟𝑎𝑙𝑃𝑟𝑜𝑜𝑓

26. IMPLEMENTATION TRUTH AXIS
One modeling cleanup I strongly recommend for Node 5 is separating system readiness from
claim epistemics.
System implementation state:
DESIGNED
IMPLEMENTED
TESTED
VERIFIED
PRODUCTION-PROVEN
BLOCKED
UNKNOWN
SUPERSEDED
That is different from epistemic claim state.
Do not make one overloaded status field try to represent everything.

27. EPISTEMIC CLAIM AXIS
The target state model should support:
UNKNOWN
UNVERIFIED
CLAIMED
SUPPORTED
VERIFIED
DISPUTED
CONTRADICTED
CORRECTED

CONTEXT_BOUND
STALE
Then lifecycle can separately represent:
ACTIVE
SUPERSEDED
RETRACTED
EXPIRED
REVOKED
This cleans up a current schema inconsistency where lifecycle concepts and epistemic
concepts sometimes sit in the same enum.

28. CLAIM TRANSITIONS
Conceptually:
UNKNOWN
↓
CLAIMED
↓
SUPPORTED
↓
VERIFIED
↓
PRODUCTION-PROVEN
But branches are allowed:
CLAIMED → CONTRADICTED
SUPPORTED → DISPUTED
SUPPORTED → STALE
VERIFIED → STALE
VERIFIED → CORRECTED
VERIFIED → SUPERSEDED
PRODUCTION-PROVEN → STALE
A later contradiction can reopen an earlier proof.
Proof is not a one-way ego ladder.

29. PROVE STATE MACHINE
Ultimate semantic state machine:
UNINITIALIZED
↓
BINDING_CONTEXT
↓
VALIDATING_INPUT
↓
LOADING_EVIDENCE
↓
VALIDATING_PROVENANCE
↓
VALIDATING_SCOPE
↓
VALIDATING_TIME
↓
CLASSIFYING_EVIDENCE
↓
DETECTING_CONFLICTS
↓
BUILDING_PROOF_OBLIGATIONS
↓
ASSESSING_STRENGTH
↓
SETTING_CLAIM_CEILING
↓
EMITTING_PROOF_RECORD
↓
HANDOFF_READY
Terminal / interruption states:
ASSESSED
CONFLICTED
INCONCLUSIVE
BLOCKED
STALE
CONTRADICTED
FAILED

Current runtime can continue mapping this to its present smaller machine vocabulary:
ASSESSED
CONFLICTED
FAILED
until the schema is deliberately expanded.

30. INPUT CONTRACT
PROVE should consume a typed baton including:
{
"execution_id": "...",
"message_id": "...",
"source_node": "...",
"target_node": "NAYA-KERNEL-PROVE",
"identity_context": {},
"authority_context": {},
"truth_context": {},
"claim_context": {},
"intelligence_context": {},
"evidence_context": {},
"scope": {},
"time_context": {},
"provenance": {},
"upstream_receipt_refs": [],
"source_revision": "...",
"idempotency_key": "..."
}
No downstream node should have to guess what PROVE assessed.

31. CALLER-SUPPLIED PROOF CONTENT
The current runtime does something especially strong that I would make permanent:

The caller may not manufacture the claim, evidence,
provenance, epistemic state, answer, lesson or proof
content that PROVE is supposed to derive.
Current runtime explicitly rejects caller fields such as:
claim
evidence
provenance
epistemic_state
proof
answer
lesson
intelligence_content
That prevents:
“Here is the proof. Please verify it.”
from becoming automatic truth laundering.
PROVE derives from canonical sources.

32. CURRENT KNOW → PROVE
CONTRACT
Current runtime behavior is strong and should become part of the master spec.
PROVE currently requires, among other things:
fresh persisted KNOW receipt
correct owner
correct project
correct KNOW action

successful retrieval
fresh timestamp
valid KNOW envelope
correct Naya identity
correct handoff
retrieval_creates_authority = false
live matching authority
active/non-revoked authority
valid authority expiry
correct action
correct target
KNOW HIT
applicable = true
selected canonical block
owner match
current block lifecycle
scope match
capability match
provenance
evidence references
epistemic-state match
provenance reread match
evidence-reference reread match
conflict reread
That is exactly the kind of machine-exact proof boundary we want.

33. WHY PROVE READS AUTHORITY
This needs careful wording.
PROVE does not read authority because authority makes a claim true.
It reads authority because some protected evidence may only be legitimately accessed or
applied within governed scope.
Therefore:

𝐴𝑢𝑡ℎ𝑜𝑟𝑖𝑡𝑦 ≠ 𝑇𝑟𝑢𝑡ℎ
and:

𝑇𝑟𝑢𝑡ℎ ≠ 𝐴𝑢𝑡ℎ𝑜𝑟𝑖𝑡𝑦
Authority controls legitimate access/use.
Evidence determines epistemic support.

34. PROVE CANNOT CREATE AUTHORITY
Permanent field:
"proof_creates_authority": false
And permanent equation:
\[ PROVEN(x) \nRightarrow AUTHORIZED(x) \]
Example:
We have conclusive proof that the production deletion command works.
That still does not authorize running it.

35. KNOW → PROVE BATON
KNOW supplies:
canonical Intelligent Block
canonical source identity
owner
scope
provenance
evidence refs
understanding state
temporal state
retrieval receipt
related conflict candidates
PROVE determines:

What claim can legitimately be made from this?
KNOW must not pre-label its own content as proven.

36. PROVE → CONNECT BATON
The current actual runtime does this:
PROVE
→ CONNECT
when the context-bound claim is sufficiently supported.
PROVE should send:
{
"claim": "...",
"epistemic_state": "SUPPORTED",
"claim_strength": "...",
"evidence_strength": "...",
"scope": {},
"provenance_chain": [],
"evidence_refs": [],
"conflicts": [],
"limitations": [],
"unresolved_gaps": [],
"proof_receipt_ref": "...",
"proof_creates_authority": false
}
CONNECT then asks:
Does this supported intelligence actually relate to the current task in the required
way?

37. PROVE → VERIFY BATON
PROVE must also be able to route a claim toward VERIFY when the requested proof requires:

real outcome observation
independent reread
causal comparison
acceptance
production verification
adversarial verification
This resolves the old/new routing ambiguity elegantly:

Primary semantic flow
KNOW → PROVE → CONNECT

Independent proof escalation
PROVE → VERIFY

Action outcome path
ACT → VERIFY

Contextualized verification path
CONNECT → VERIFY
One organism can have more than one valid edge.
The semantic order does not require a single-file pipeline.

38. VERIFY → PROVE RETURN PATH
After VERIFY establishes an outcome:
VERIFY RECEIPT
↓
PROVE
↓
CLAIM REASSESSMENT
This is how:
SUPPORTED
may legitimately become:

VERIFIED
or:
CONTRADICTED
or:
NOT PROVEN
PROVE controls the claim state.
VERIFY supplies the independent evidence.

39. PROVE → LEARN
LEARN should not accept:
"we learned..."
as sufficient evidence.
For a learning promotion, PROVE should expose:
what outcome is verified
what lesson is claimed
what evidence supports that lesson
what causal limitations remain
which scope applies
what was contradicted
what remains unknown
Then LEARN decides whether that evidence justifies changing future behavior.

40. PROVE + ACT
ACT records:
what was attempted

what executed
raw observations
errors
partial effects
PROVE determines:
What statements about that execution are supportable?
VERIFY determines:
Did the required outcome actually occur?
The three must never collapse into one producer-owned success claim.

41. PROVE + VALUE CALCULUS V2.1
PROVE uses the existing shared Decision Value Calculus.
No Proof Value Engine #2.
PROVE supplies or preserves evidence-bound inputs such as:
evidence_sufficiency
provenance
uncertainty
confidence
verification state
actual value evidence
calibration evidence
But:

𝑉𝑎𝑙𝑢𝑒 ≠ 𝑇𝑟𝑢𝑡ℎ
A high-value claim is not more true.
A low-value fact is not less true.
A positive predicted value does not upgrade evidence.

42. CONFIDENCE LAW
Confidence is useful metadata.
It is not proof.
\[ Confidence(c)=1 \nRightarrow VERIFIED(c) \]
The V2.1 system may use:

𝐶𝑎𝑔𝑔
and:

𝐶𝑐𝑟𝑖𝑡𝑖𝑐𝑎𝑙
for decision confidence.
PROVE preserves those values and their basis.
It must never reinterpret them as epistemic promotion by themselves.

43. CAUSATION LAW
Permanent:
\[ Correlation(X,Y) \nRightarrow Causes(X,Y) \]
For a causal claim, PROVE must require an appropriate causal method.
Depending on the claim:
control/treatment
counterfactual
ablation
paired comparison
time ordering
confound control
repetition

independent recomputation
This eventually feeds the Causal Verification Object under VERIFY.

44. COUNTERFACTUAL PROOF
For intelligence effectiveness, the strongest pattern is:
CONTROL
same task
same model
same authority
same environment
without intelligence X
→ outcome A
TREATMENT
same task
same model
same authority
same environment
with intelligence X
→ outcome B
Then:

∆𝑂𝑢𝑡𝑐𝑜𝑚𝑒 = 𝐵 − 𝐴
But even:

𝐵>𝐴
is not automatically causal unless the experimental design supports that inference.
PROVE records exactly what the design establishes.

45. PRODUCTION-PROVEN LAW

For a production claim, minimum chain:
CANONICAL SOURCE
→ EXACT REVISION
→ DEPLOYMENT
→ DEPLOYED-SOURCE PARITY
→ REAL PRODUCTION INVOCATION
→ PERSISTED RECEIPT
→ PERSISTED OUTCOME
→ INDEPENDENT REREAD
→ INDEPENDENT RECOMPUTATION / VERIFICATION
→ DECLARED-SCOPE ACCEPTANCE
Therefore:

𝐺𝑟𝑒𝑒𝑛𝐶𝐼 ≠ 𝑃𝑟𝑜𝑑𝑢𝑐𝑡𝑖𝑜𝑛𝑃𝑟𝑜𝑣𝑒𝑛
𝐷𝑒𝑝𝑙𝑜𝑦𝑒𝑑 ≠ 𝑃𝑟𝑜𝑑𝑢𝑐𝑡𝑖𝑜𝑛𝑃𝑟𝑜𝑣𝑒𝑛
𝑅𝑒𝑐𝑒𝑖𝑝𝑡𝐸𝑥𝑖𝑠𝑡𝑠 ≠ 𝑃𝑟𝑜𝑑𝑢𝑐𝑡𝑖𝑜𝑛𝑃𝑟𝑜𝑣𝑒𝑛

46. OBSERVATION WINDOWS
Some claims cannot be verified instantly.
Example:
“This migration caused no delayed regressions.”
At 𝑡0, that claim may be impossible.
Therefore:
PASS_PENDING_WINDOW
is legitimate.
PROVE must preserve:
observation_window_open
observation_window_close
delayed_harm_material

current_verification_state
Never fake certainty merely because the immediate check passed.

47. SMART LEDGER
PROVE owns the accountability semantics of the Smart Ledger.
It does not create another ledger.
The existing substrate should receive typed events such as:
CLAIM_CREATED
PROOF_ASSESSMENT
EVIDENCE_ATTACHED
CLAIM_SUPPORTED
CLAIM_CONTRADICTED
CLAIM_VERIFIED
PRODUCTION_PROOF
PROOF_STALE
PROOF_SUPERSEDED
CLAIM_RETRACTED
CONFLICT_DETECTED
Every transition should be reconstructable.

48. APPEND-ONLY EPISTEMIC HISTORY
Incorrect past claims should not be silently rewritten out of history.
Correct model:
CLAIM V1 — SUPPORTED
↓
new evidence
↓
CLAIM V2 — CORRECTED
with relationship:

V2 CORRECTS V1
or:
V2 SUPERSEDES V1
History stays visible.

49. PROOF RECEIPT
Ultimate receipt:
{
"receipt_type": "PROOF_ASSESSMENT",
"receipt_id": "...",
"execution_id": "...",
"message_id": "...",
"node_id": "NAYA-KERNEL-PROVE",
"node_version": "...",
"claim_id": "...",
"claim": "...",
"claim_type": "...",
"scope": {},
"time_context": {},
"state_before": "...",
"state_after": "...",
"epistemic_state": "...",
"claim_strength": "...",
"evidence_strength": "...",
"proof_obligations": [],
"satisfied_obligations": [],
"unsatisfied_obligations": [],
"evidence_refs": [],

"counterevidence_refs": [],
"provenance_chain": [],
"verification_method": "...",
"verifier_identity": "...",
"conflicts": [],
"limitations": [],
"unresolved_gaps": [],
"source_revision": "...",
"input_hash": "...",
"output_hash": "...",
"proof_context_hash": "...",
"proof_creates_authority": false,
"handoff_to": "...",
"timestamp": "..."
}

50. IDEMPOTENCY
Repeated proof assessment with identical canonical inputs should not generate different truth
merely because it was called twice.
Conceptually:
\[ ProofKey = hash( claim \Vert scope \Vert sourceRevision \Vert evidenceSet \Vert method \Vert
proofContext ) \]
Identical input:
→ same effective assessment
Conflicting reuse:
→ fail closed / new version

51. REPLAY LAW
PROVE must defend against:
stale evidence replay
revoked evidence access
superseded source replay
old production proof applied to new revision
cross-owner proof reuse
forged receipt
changed scope
changed claim
changed evidence under same ID
changed verification method
reused verifier identity
A proof cannot be detached from the context that made it valid.

52. HASH LAW
Proof records should be integrity-bound.

𝐻𝑐 = 𝑆𝐻𝐴256(𝐶𝑎𝑛𝑜𝑛𝑖𝑐𝑎𝑙𝑖𝑧𝑒(𝑐𝑙𝑎𝑖𝑚))
𝐻𝐸 = 𝑆𝐻𝐴256(𝐶𝑎𝑛𝑜𝑛𝑖𝑐𝑎𝑙𝑖𝑧𝑒(𝑠𝑜𝑟𝑡𝑒𝑑(𝑒𝑣𝑖𝑑𝑒𝑛𝑐𝑒 𝑟𝑒𝑓𝑠)))
𝐻𝑃 = 𝑆𝐻𝐴256(𝐶𝑎𝑛𝑜𝑛𝑖𝑐𝑎𝑙𝑖𝑧𝑒(𝑝𝑟𝑜𝑣𝑒𝑛𝑎𝑛𝑐𝑒))
\[ H_{proof} = SHA256( H_c \Vert H_E \Vert H_P \Vert method \Vert scope \Vert sourceRevision
) \]
If evidence, claim, scope or method changes materially:
it is a new proof state.

53. SECURITY THREAT MODEL

PROVE must explicitly defend against:
caller-supplied proof laundering
prompt injection inside evidence
forged provenance
forged evidence references
cross-owner leakage
scope widening
stale evidence
stale source revision
replay
evidence cloning
circular evidence
self-verification
verifier impersonation
confused deputy
evidence deletion
proof suppression
contradiction suppression
selective evidence cherry-picking
confidence laundering
AI consensus laundering
popularity-as-truth

54. CIRCULAR PROOF
Example:
A says B is true
B cites A as evidence
This creates no independent support.
Define evidence dependency graph 𝐺𝐸.
If the only support path for claim 𝑐 returns to 𝑐 without an external evidence root:
\[ ExternalRoot(c)=\varnothing \]
then:

𝐼𝑛𝑑𝑒𝑝𝑒𝑛𝑑𝑒𝑛𝑡𝑆𝑢𝑝𝑝𝑜𝑟𝑡(𝑐) = 0

Circular citations cannot bootstrap truth.

55. AI CONSENSUS LAW
Ten AIs agreeing does not make something true if they are all reasoning from the same
unsupported source.

𝐶𝑜𝑛𝑠𝑒𝑛𝑠𝑢𝑠 ≠ 𝐸𝑣𝑖𝑑𝑒𝑛𝑐𝑒
AI agreement may be:
a review signal
a hypothesis signal
a contradiction detector
but not an automatic proof promotion.

56. HUMAN STATEMENT LAW
Human Director authority is final for legitimate governance decisions.
But authority over governance does not make empirical facts true.
This distinction protects Shawn too.
Example:
Shawn may legitimately say:
“Deploy this revision.”
LAW can authorize it.
But if a production check later shows the wrong revision is live:
PROVE must preserve the empirical evidence.
So:

𝐺𝑜𝑣𝑒𝑟𝑛𝑎𝑛𝑐𝑒𝐴𝑢𝑡ℎ𝑜𝑟𝑖𝑡𝑦 ≠ 𝐸𝑚𝑝𝑖𝑟𝑖𝑐𝑎𝑙𝑇𝑟𝑢𝑡ℎ𝐴𝑢𝑡ℎ𝑜𝑟𝑖𝑡𝑦
while respecting the human Director's actual decision authority.

57. PRIVATE EVIDENCE
Proof does not require exposing private evidence to unauthorized parties.
A proof may be valid while its raw evidence remains protected.
Therefore public/collective proof can expose, where allowed:
derived claim
verification status
proof method
non-identifying evidence class
receipt/hash
while withholding:
private raw source
personal identity
private activity
protected content

58. PROVENANCE COMPLETENESS
A useful diagnostic metric:

𝑃𝑐 =

𝑟𝑒𝑞𝑢𝑖𝑟𝑒𝑑 𝑝𝑟𝑜𝑣𝑒𝑛𝑎𝑛𝑐𝑒 𝑓𝑖𝑒𝑙𝑑𝑠 𝑣𝑎𝑙𝑖𝑑
𝑟𝑒𝑞𝑢𝑖𝑟𝑒𝑑 𝑝𝑟𝑜𝑣𝑒𝑛𝑎𝑛𝑐𝑒 𝑓𝑖𝑒𝑙𝑑𝑠

But:
\[ P_c=1 \nRightarrow ClaimTrue \]
Complete provenance tells us where something came from.
Not whether the claim is correct.

59. PROOF DEBT
NayaPOWER should explicitly measure unresolved proof debt.
Define:

𝑃𝑟𝑜𝑜𝑓𝐷𝑒𝑏𝑡 =

∑

𝑊𝑒𝑖𝑔ℎ𝑡(𝑐) × 𝐺𝑎𝑝𝑅𝑎𝑡𝑖𝑜(𝑐)

𝑐∈𝑀𝑎𝑡𝑒𝑟𝑖𝑎𝑙𝐶𝑙𝑎𝑖𝑚𝑠

where:

𝐺𝑎𝑝𝑅𝑎𝑡𝑖𝑜(𝑐) = 1 − 𝐶𝑜𝑣𝑒𝑟𝑎𝑔𝑒(𝑐)
This is a prioritization metric only.
It does not alter claim truth.
Useful interpretation:
Which important claims are we relying on without enough proof?
That can guide high-value work.

60. EVIDENCE EFFICIENCY
The system should not collect evidence forever after the proof boundary is satisfied.
Define:

𝑀𝑎𝑟𝑔𝑖𝑛𝑎𝑙𝐸𝑣𝑖𝑑𝑒𝑛𝑐𝑒𝑉𝑎𝑙𝑢𝑒 =

𝐸𝑥𝑝𝑒𝑐𝑡𝑒𝑑𝑅𝑒𝑑𝑢𝑐𝑡𝑖𝑜𝑛𝐼𝑛𝑀𝑎𝑡𝑒𝑟𝑖𝑎𝑙𝑈𝑛𝑐𝑒𝑟𝑡𝑎𝑖𝑛𝑡𝑦
𝐶𝑜𝑠𝑡𝑂𝑓𝐴𝑑𝑑𝑖𝑡𝑖𝑜𝑛𝑎𝑙𝐸𝑣𝑖𝑑𝑒𝑛𝑐𝑒

When the required proof boundary is already satisfied and additional evidence produces
negligible value:
stop.

But this efficiency rule must never lower the required proof standard.

61. PERFORMANCE
Measure:
p50 proof latency
p95 proof latency
p99 proof latency
evidence-read count
provenance-read count
relationship-conflict read count
proof-record write latency
proof failure rate
inconclusive rate
contradiction rate
stale-proof rate
reverification rate
independent-verification rate
proof reconstruction success
false-promotion incidents
claim-downgrade rate
cost per material proof
human review burden
Speed never beats truth.

62. HUMAN VALUE
A strong PROVE node should reduce Shawn's need to ask:
“Wait — is this actually true?”
Useful measures include:

𝑅𝑒𝑣𝑒𝑟𝑖𝑓𝑖𝑐𝑎𝑡𝑖𝑜𝑛𝐴𝑣𝑜𝑖𝑑𝑒𝑑

𝐹𝑎𝑙𝑠𝑒𝐶𝑜𝑚𝑝𝑙𝑒𝑡𝑖𝑜𝑛𝑃𝑟𝑒𝑣𝑒𝑛𝑡𝑒𝑑
𝐻𝑢𝑚𝑎𝑛𝑃𝑟𝑜𝑜𝑓𝐵𝑢𝑟𝑑𝑒𝑛𝑅𝑒𝑑𝑢𝑐𝑒𝑑
𝑇𝑖𝑚𝑒𝑇𝑜𝑇𝑟𝑢𝑠𝑡𝑤𝑜𝑟𝑡ℎ𝑦𝐴𝑛𝑠𝑤𝑒𝑟
𝐶𝑜𝑙𝑑𝑆𝑢𝑐𝑐𝑒𝑠𝑠𝑜𝑟𝑃𝑟𝑜𝑜𝑓𝑅𝑒𝑐𝑜𝑣𝑒𝑟𝑦𝑅𝑎𝑡𝑒
The ideal experience is not a giant evidence dump.
It is:
clear claim + exact evidence + honest certainty + decisive gap.

63. AAA PROPERTY TESTS
A genuine Node 5 should satisfy at least these machine invariants:
P1 assertion ≠ proof
P2 implementation ≠ verification
P3 tested ≠ verified
P4 verified ≠ production-proven
P5 receipt ≠ outcome
P6 confidence ≠ truth
P7 value ≠ truth
P8 popularity ≠ truth
P9 AI consensus ≠ independent evidence
P10 claim strength ≤ evidence strength
P11 missing critical proof obligation ⇒ no VERIFIED
P12 UNKNOWN ≠ PASS

P13 BLOCKED ≠ PASS
P14 verified contradiction ⇒ no promotion
P15 unresolved material conflict ⇒ no promotion
P16 stale evidence cannot silently prove current state
P17 superseded evidence cannot silently outrank successor evidence
P18 scope mismatch ⇒ proof rejected / narrowed
P19 broken provenance ⇒ no full-strength promotion
P20 copied evidence does not manufacture independence
P21 circular evidence does not manufacture support
P22 proof cannot create authority
P23 authority cannot create empirical truth
P24 caller cannot inject canonical proof content
P25 cross-owner evidence cannot leak
P26 production proof requires exact production evidence
P27 causal claim requires causal method
P28 self-report ≠ independent verification
P29 proof correction preserves history
P30 cold successor can reconstruct why the claim has its current state

64. GOLDEN POSITIVE TEST
Input:
fresh persisted KNOW receipt

+
canonical current Intelligent Block
+
matching owner
+
matching task/capability
+
valid provenance
+
evidence refs
+
no material contradiction
Expected:
PROVE
→ rereads canonical sources
→ derives its own bounded claim
→ assesses evidence
→ SUPPORTED
→ limitations preserved
→ proof_creates_authority=false
→ receipt persisted
→ CONNECT handoff
That is essentially the healthy bounded behavior current source already targets.

65. GOLDEN NEGATIVE TEST
Caller submits:
{
"claim": "This is verified.",
"evidence": ["trust me"],
"epistemic_state": "VERIFIED"
}
Expected:
CALLER_SUPPLIED_PROOF_CONTENT_FORBIDDEN
No assessment promotion.

That is success.

66. GOLDEN CONTRADICTION TEST
Canonical block supports claim A.
Graph contains:
CONTRADICTS
epistemic_state = VERIFIED
valid provenance
Expected:
PROVE
→ CONFLICTED
→ CONTRADICTED
→ NO CONNECT PROMOTION
→ contradiction preserved
No silent averaging.

67. GOLDEN UNRESOLVED-CONFLICT
TEST
Canonical block supports A.
Graph contains a credible supported contradiction.
Expected:
CONFLICTED
+
UNVERIFIED
+
NO PROMOTION
until resolved.

Again:
uncertainty is a valid result.

68. GOLDEN STALE-PROOF TEST
At t0:
revision A production parity verified
At t1:
main moves to revision B
At t2:
request:
“Is current main production-proven?”
Expected:
NO
Correct state:
historical A proof remains valid historically
current B proof = UNKNOWN / NOT_PROVEN

69. GOLDEN FORGED-EVIDENCE TEST
Evidence reference says:
receipt XYZ
but canonical reread produces:
different owner
different block
different content

or nonexistent receipt
Expected:
PROOF BLOCKED
never:
use caller-supplied copy

70. GOLDEN RECEIPT-VS-OUTCOME
TEST
ACT receipt:
status = SUCCESS
But independent system state does not show expected effect.
Expected:
execution receipt exists
+
outcome claim = NOT VERIFIED
Never:
ACT success receipt → outcome automatically VERIFIED

71. GOLDEN PRODUCTION TEST
Required:
canonical revision
↓
deployed exact revision
↓
real production invocation
↓
persisted PROVE receipt

↓
independent reread
↓
independent recomputation
↓
VERIFY acceptance
Only then can the declared bounded production claim be promoted.

72. COLD SUCCESSOR PROOF
A brand-new Naya should receive a claim/proof identity and reconstruct:
what was claimed
what evidence supports it
where evidence came from
which revision it applies to
what proof method was used
which verifier was used
what conflicts exist
what limitations remain
what is unknown
whether proof is stale
whether production proof exists
what should be checked next
without Shawn explaining the story.
That is a genuine continuity proof.

73. PROVE AAA LIFECYCLE
Qualification:
SPECIFIED
→ IMPLEMENTED
→ LOADED
→ INVOKED

→ INFLUENTIAL
→ APPLIED
→ OUTCOME_OBSERVED
→ VERIFIED
→ PRODUCTION-PROVEN
→ LEARNED
→ COMPOUNDED
→ SUCCESSOR_RETAINED
→ EVOLVED
Those states remain independent proof obligations.
The document existing proves only:
SPECIFIED.

74. WHAT “INFLUENTIAL” MEANS FOR
PROVE
Not:
“Did the PROVE endpoint run?”
The real test is:
same downstream decision context
+
strong valid evidence
→ supported baton continues
versus
same downstream decision context
+
missing / contradicted evidence
→ baton stops or weakens
If downstream behavior is unchanged regardless of proof state:
PROVE is decorative.

A real PROVE Node must constrain the organism.

75. WHAT “VERIFIED” MEANS FOR
PROVE
Independent verification must reconstruct:
claim
+
scope
+
source revision
+
evidence set
+
provenance
+
proof obligations
+
method
+
conflicts
+
claim ceiling
and produce the same legitimate assessment.
The current runtime already contains an independent-recomputation mode that does this for its
bounded assessment.
That is good.
But it explicitly does not prove behavioral outcome or causality.
Keep that honesty permanently.

76. WHAT “PRODUCTION-PROVEN”
MEANS FOR NODE 5
For PROVE itself:
exact canonical source revision
+
actual deployed PROVE runtime
+
source/deployment parity
+
real authenticated invocation
+
canonical KNOW input
+
canonical evidence reread
+
positive supported assessment
+
negative blocked/conflicted assessment
+
persisted receipts
+
independent recomputation
+
downstream behavioral influence
+
cold successor reconstruction
Only then should Node 5 itself be called production-proven for that declared scope.
Current repository truth has not yet closed all of that.

77. NODE 5 AND CURRENT MAIN
Here is the important current reality from GitHub:
Already strong:
PROVE semantic contract exists

machine contract exists
AI contract exists
node schema exists
proof-record schema exists
executable runtime exists
deterministic assessor exists
current source/deployment parity is recorded
current runtime blocks caller-supplied proof content
current runtime rereads canonical KNOW evidence
current runtime rereads live authority
current runtime checks owner/scope
current runtime checks freshness
current runtime checks current Intelligent Block state
current runtime checks provenance
current runtime checks evidence refs
current runtime checks contradictions
current runtime emits bounded SUPPORTED / UNVERIFIED / CONTRADICTED states
current runtime explicitly says proof creates no authority
independent assessment recomputation exists
repository tests pass
Still not closed:
Contracts 07/10/16 registry status reconciliation
Proof Contract ratification/status reconciliation
proof vocabulary normalization
PROVE→CONNECT graph/wire reconciliation
current live end-to-end PROVE behavioral proof
full current-main organism proof
production proof for Node 5's complete declared scope
That is the truthful boundary.

78. THE PROVE / CONNECT / VERIFY
TRIANGLE
I would lock this architectural pattern:
PROVE
/ \

/
\
▼
▼
CONNECT VERIFY
\
/
\
/
▼ ▼
LEARN
More precisely:
KNOW
→ PROVE
→ CONNECT
→ VERIFY
→ LEARN
with direct alternate proof edge:
PROVE → VERIFY
when the claim itself requires verification before contextual use.
And:
ACT → VERIFY
for real-world effects.
That makes the organism flexible without making responsibilities blurry.

79. 10/10 NODE 5 CHECKLIST
Layer

MUST EXIST

Semantic

exact PROVE responsibility

Claim model

typed scoped claims

Evidence model

typed evidence objects

Provenance

complete evidence lineage

Scope

explicit applicability boundary

Time

freshness / staleness

Method

claim-specific proof method

Obligation engine

required proof obligations

Strength

evidence and claim strength separated

Math

weakest-critical-obligation ceiling

Epistemic state

machine-exact state vocabulary

Lifecycle

correction/supersession/retraction separate

Conflict

contradiction first-class

Independence

source-family / verifier separation

Causality

no correlation laundering

Production

exact production proof contract

Hashing

claim/evidence/proof integrity

Idempotency

deterministic replay

Security

forged proof/injection/circular evidence defense

Privacy

owner/scope protection

Authority

proof never creates permission

KNOW

canonical source handoff

CONNECT

supported-context handoff

VERIFY

independent verification path

ACT

execution evidence boundary

LEARN

verified-learning evidence boundary

Ledger

one Smart Ledger substrate

Receipts

deterministic proof receipt

Observability

reconstructable trace

Performance

latency/cost/proof-debt metrics

Human value

fast trustworthy understanding

Tests

positive/negative/adversarial/race

Runtime

real authenticated invocation

Influence

downstream behavior changes based on proof

Verification

independent recomputation

Production proof

live scoped proof

Continuity

cold successor reconstructs reasoning

80. PROVE'S ULTIMATE QUESTION
Every material PROVE invocation should reduce to:
“What exactly is being claimed, within what scope and time, what evidence
supports or contradicts it, where did that evidence come from, how
independent and direct is it, which proof obligations are satisfied or missing,
which method is legitimate for this claim class, what limitations remain, and
therefore what is the strongest statement NayaPOWER may truthfully make
right now?”
That is Node 5.

81. PROVE'S ULTIMATE OUTPUT
The baton should become extremely simple for the next organ:
THIS IS THE CLAIM.​
THIS IS THE EXACT SCOPE.​
THIS IS THE CURRENT EPISTEMIC STATE.​
THIS IS THE CLAIM STRENGTH.​
THIS IS THE EVIDENCE STRENGTH.​
THIS IS THE PROVENANCE.​
THESE ARE THE EVIDENCE REFERENCES.​
THESE ARE THE CONTRADICTIONS.​
THESE ARE THE LIMITATIONS.​

THESE OBLIGATIONS ARE SATISFIED.​
THESE OBLIGATIONS ARE NOT SATISFIED.​
THIS IS WHAT WE MAY CLAIM.​
THIS IS WHAT WE MAY NOT CLAIM.​
THIS PROOF DOES NOT CREATE AUTHORITY.​
CONNECT / VERIFY: TAG, YOU'RE IT.

82. THE ONE-SENTENCE DEFINITION
NODE 5 — PROVE is NayaPOWER's governed truth, evidence, provenance
and accountability organ: it derives scoped claims from canonical evidence,
validates provenance, time, integrity and method, detects contradiction and
dependency, computes the maximum evidence-supported claim ceiling,
preserves limitations and unknowns, records the result through the existing
Smart Ledger/evidence substrate, never converts confidence, value, retrieval
or authority into truth, and hands only bounded proof context forward to
CONNECT and VERIFY.

83. THE FINAL PROVE LAW
\[ \boxed{ CLAIM + EVIDENCE + PROVENANCE + SCOPE + TIME + METHOD +
INDEPENDENCE + CONFLICT\ CHECK + LIMITATIONS = BOUNDED\ PROOF } \]
subject always to:
\[ \boxed{ CLAIM\ STRENGTH \le EVIDENCE\ STRENGTH } \]
and:

𝐴𝑆𝑆𝐸𝑅𝑇𝐸𝐷 ≠ 𝑃𝑅𝑂𝑉𝐸𝑁
𝐼𝑀𝑃𝐿𝐸𝑀𝐸𝑁𝑇𝐸𝐷 ≠ 𝑉𝐸𝑅𝐼𝐹𝐼𝐸𝐷
𝑉𝐸𝑅𝐼𝐹𝐼𝐸𝐷 ≠ 𝑃𝑅𝑂𝐷𝑈𝐶𝑇𝐼𝑂𝑁_𝑃𝑅𝑂𝑉𝐸𝑁
𝑅𝐸𝐶𝐸𝐼𝑃𝑇 ≠ 𝑂𝑈𝑇𝐶𝑂𝑀𝐸

𝐶𝑂𝑅𝑅𝐸𝐿𝐴𝑇𝐼𝑂𝑁 ≠ 𝐶𝐴𝑈𝑆𝐴𝑇𝐼𝑂𝑁
𝐶𝑂𝑁𝐹𝐼𝐷𝐸𝑁𝐶𝐸 ≠ 𝑇𝑅𝑈𝑇𝐻
𝑉𝐴𝐿𝑈𝐸 ≠ 𝑇𝑅𝑈𝑇𝐻
𝐴𝑈𝑇𝐻𝑂𝑅𝐼𝑇𝑌 ≠ 𝑇𝑅𝑈𝑇𝐻
𝑇𝑅𝑈𝑇𝐻 ≠ 𝐴𝑈𝑇𝐻𝑂𝑅𝐼𝑇𝑌
and the organism-wide relationship becomes:
\[ \boxed{ KNOW\ PRESERVES\ MEANING \rightarrow PROVE\ EARNS\ BELIEF \rightarrow
CONNECT\ EARNS\ RELEVANCE \rightarrow VERIFY\ EARNS\ OUTCOME\ ACCEPTANCE
\rightarrow LEARN\ EARNS\ FUTURE\ CHANGE } \]

What matters most
This is the version of MN-05 PROVE I would lock. I would not create a new proof engine to
implement it. The strongest move is to upgrade the existing PROVE seam already on main,
normalize the proof vocabularies around it, reconcile Contracts 07/10/16, add the missing
PROVE→CONNECT canonical graph/wire relationship, and then close the actual live bounded
proof.
The first four nodes now form a clean organism:
SELF — Who are we?​
LAW — May we do it?​
ACT — Do the exact authorized thing.​
KNOW — What durable intelligence do we have?​
PROVE — What are we actually justified in believing?


---

## CANDIDATE AMENDMENTS — Naya 2 scorecard corrections (NOT RATIFIED)

> Status: PROPOSED. Drafted by the Naya 2 independent-review lane from
> BRAIN/03-KERNEL/0006-NODE-SPECS-INDEPENDENT-SCORECARD-V1.md (2026-10-01, mean
> score 8.8/10). These amendments are CANDIDATE — not ratified, not merged to
> main. Each must be applied (or explicitly rejected with written reason) before
> any lock of this spec. Nothing above this line was altered: the verbatim PDF
> text is preserved intact. References (P1, X1, X2, X3) map to the scorecard's
> correction list.

### A-PROVE-1 [X1 — Prime 1 / Amendment 0002 subordination]

Add: "This spec operates under Amendment 0002 (Prime 1, the Judgment Rule,
ratified 2026-09-30); where this spec and Prime 1 conflict, Prime 1 governs."
REQUIRED before lock.

### A-PROVE-2 [X2 — semantic order vs runtime call order]

Add an explicit order-mapping note: the organism order
SELF→LAW→ACT→KNOW→PROVE→CONNECT→VERIFY→LEARN→EVOLVE→SELF is responsibility
order, not invocation order. Kernel.decide() will call nodes in a different
sequence; PROVE bounds belief before and after action regardless of call
position.

### A-PROVE-3 [P1 — the PR #1120 lesson, structural]

The runtime PROVE carried an inspect-time defect (fixed by PR #1120): it passed
at import/inspect time and degraded at run time. Add an adversarial acceptance
test to the spec: "A PROVE implementation that passes at import/inspect time
but degrades at run time MUST FAIL acceptance." The inspect-time/run-time
boundary must be named explicitly in the spec so no future implementation can
reintroduce a time-bomb by accident. This makes the #1120 lesson structural,
not historical.

### A-PROVE-4 [X3 — PROVE→CONNECT→VERIFY topology]

Record the topology reconciliation: PROVE bounds belief; CONNECT selects and
routes applicable context; VERIFY establishes outcomes and causality. No node
may duplicate another's verdict. PROVE's verdict is a bounded epistemic
assessment — it never creates authority and never substitutes for VERIFY's
causal establishment.

## CANDIDATE AMENDMENTS — Naya 4 builder-lane deltas (NOT RATIFIED)

> Status: PROPOSED. Drafted by the Naya 4 builder lane from the six-skeleton
> merge audit (SKELETON-MERGE-AUDIT-2026-10-01, 2026-09-30 20:38 PDT — 7 MODERATE
> findings, all OPEN) plus known-missing content for the 0002s. Append-only:
> nothing above this line was altered, and Naya 2's A-<NODE>-N amendments are
> preserved intact — numbering continues her sequence per node. All CANDIDATE —
> not ratified, not merged to main. Each must be applied (or explicitly rejected
> with written reason) before any lock of this spec.

### A-PROVE-5 [N4 — Ultimate Lock cross-reference]

Add: a cross-reference pointer between this 0002 and the Ultimate Lock
materials landed in #1222, so the lock index and this depth spec cannot drift
apart. State which artifact is authoritative for what.

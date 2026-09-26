# Naya Node Specification V1
**Status:** SPECIFICATION CANDIDATE — derived from verified production specimen IB-001229
**Owner:** NayaPOWER / Human Director
**Evidence basis:** canonical receiver v7-smart-note-canonical
**Purpose:** define the semantic object that enters NayaNET without creating a second brain.

## 1. Core definition
A Naya Node is a governed, reusable unit of meaningful intelligence. It is designed to be understandable by humans, precise for machines, attributable to its source, bounded by authority, connected to related intelligence, retrievable in context, reusable in action, and improved through verified outcomes.

A Node is not merely a note, message, file, page, database row, model prompt, or hyperlink. Those are representations, transports, projections, or interfaces around intelligence.

## 2. Semantic synonyms
For user intent, these expressions resolve to the same semantic operation when context is clear:
Smart Node = Naya Node = Smart Note = “note this” = “remember this” = “capture this” = “document this”.

This is an intent-language rule, not permission to bypass the canonical receiver.
Until the contract system formally migrates terminology, Smart Note remains the implementation/API term used by the current canonical receiver.

## 3. Canonical chain
EXPERIENCE → INTENT → NAYA NODE → CANONICAL RECEIVER → INTELLIGENT BLOCK → COLLECTIVE CHAIN → RETRIEVE → APPLY → VERIFY → LEARN → COMPOUND

The semantic Node may exist as a candidate in conversation.
The committed Intelligent Block is created only through the canonical receiver.
The repository projection is not allowed to allocate a canonical identity.

## 4. Object levels
| Level | Job |
|---|---|
| Naya Node | Meaningful intelligence unit; candidate or semantic request. |
| Intelligent Block | Canonically committed Node with receiver-owned immutable identity. |
| Smart Note | Current human-readable repository projection of the committed block. |
| Smart Link | Verified doorway to the repository projection after projection verification. |
| Master Node | Reference/index layer organizing canonical nodes without duplicating their authority. |
| Collective Chain | Governed graph of nodes, relationships, evidence, applicability, and learning. |

## 5. Identity law
The canonical receiver owns:
- intelligent_block_id;
- canonical source/event identity;
- transaction identity;
- persisted lineage;
- canonical projection completion.

Naya, Hub, GitHub projection code, or a Master Node MUST NOT invent an IB-######.
Content hashes may identify content integrity. They do not replace receiver-owned canonical identity.

## 6. Minimum intelligence
A useful Node should answer, where applicable:
WHO / WHAT / WHEN / WHERE / WHY / HOW / WHY BELIEVE / WHO ALLOWS / WHAT CONNECTS / WHAT HAPPENED / WHAT CHANGED / WHAT NEXT.

Missing information remains explicit UNKNOWN.
Interpretation must remain distinguishable from source fact.
Authority must remain distinct from truth.
Value must remain distinct from authorization.

## 7. Truth boundary
Minimum truth vocabulary:
UNKNOWN, SUPPORTED, VERIFIED, CONFLICTED, REJECTED, SUPERSEDED.

Rules:
- UNKNOWN cannot be silently promoted to VERIFIED.
- BLOCKED cannot be presented as PASS.
- IMPLEMENTED cannot be presented as VERIFIED.
- VERIFIED cannot be presented as production-proven without production evidence.
- Claim strength cannot exceed evidence strength.
- Material conflict stops affected reconciliation until authority, version, and scope are resolved.

## 8. Authority boundary
Minimum authority vocabulary:
NONE, PROPOSED, AUTHORIZED, REVOKED, EXPIRED.

Capability does not create authority.
Intent-first interpretation never creates new authority.
A Node capture may be authorized while later publication, sharing, deletion, or external action is not.

## 9. Privacy
PRIVATE BY DEFAULT. SHARED BY CHOICE. COLLECTIVE BY CONSENT. PUBLIC BY DECISION.

The first specimen proved private owner Feed visibility and a verified canonical projection.
A public URL does not make the underlying intelligence public.
Access policy remains a separate governance concern.

## 10. Input contract
A Node begins as human meaning, not a database field set.
The input layer may accept speech, text, a question, an instruction, a conversation segment, a verified tool result, an existing Node, or a selected source.

Before durable capture Naya performs:
1. intent recognition;
2. context resolution;
3. source classification;
4. value assessment;
5. duplicate/reconciliation search;
6. authority check;
7. candidate formation;
8. canonical submission when commitment is intended and authorized.

The input should preserve the intended outcome, not merely copy wording.

## 11. Naya Language
Naya Language is the intent-first interaction layer for NayaNET.

Core principle:
**Understand the intended outcome; do not blindly follow literal wording.**

This is bounded by authority, safety, privacy, scope, reversibility, required confirmation, and evidence.

Alias family:
Smart Node this; Naya Node this; Smart Note this; Note this; Remember this; Capture this; Document this.

Canonical intent:
CREATE_OR_UPDATE_NAYA_NODE

“Naya, play” maps to PLAY_INTELLIGENCE.
“make it better” without a target maps to UNKNOWN plus clarification.
“publish this everywhere” maps to UNKNOWN plus clarification because scope and authority change.

Ask only when ambiguity could materially change the object, audience, privacy, scope, authority, cost, destructive effect, or intended outcome.
Preferred clarification: “Is this your intention?”

## 12. Candidate versus committed Node
Every meaningful input may first become a cheap in-context candidate.
A candidate is not durable canonical intelligence.

Candidate:
- may be revised or rejected;
- has no receiver-owned IB identity;
- must not be represented as a verified Smart Link.

Commit:
- crosses the canonical receiver;
- receives the canonical IB identity;
- creates durable lineage;
- enters governed learning boundaries;
- may produce a verified Smart Link only after projection verification.

## 13. Distillation
A Node is a compression of meaning, not deletion of evidence.

The optimization law is:
MAXIMUM USEFUL INTELLIGENCE × CLARITY × RELEVANCE × APPLICABILITY

while minimizing:
COGNITIVE COST × REDUNDANCY × AMBIGUITY × NOISE

The correct question is:
“What is the smallest representation that preserves everything required to correctly understand and use the intelligence?”

## 14. Perspectives
Perspectives are views of one meaning, not separate copies of intelligence.

Core views:
Essence; Why; Use; Human; Simple; Naya; Machine; Evidence; Governance; Learning.

A view is earned when it adds decision value.
Copying the same paragraph into ten headings is not transformation.

## 15. Naya Value System

The Naya Node uses a multidimensional, evidence-bound Value System rather than a single rating.

### 15.1 Value is a vector, not a verdict

A Node may carry multiple value dimensions, for example:

relevance, usefulness, benefit, harm, risk, effort, evidence strength, freshness, applicability, reliability, reusability, transferability, learning value, compounding value, time saved, cognitive effort avoided, errors prevented, contribution value, and system value.

Each dimension answers a different question. The system MUST NOT collapse distinct dimensions into one number merely for convenience.

### 15.2 Reference anchors are not limits

The human reference scale uses:

-9 … -8 … -1 … 0 … +1 … +8 … +9

but **-9 and +9 are reference anchors, not mathematical ceilings or floors**.

The semantic value domain is unbounded in both directions.

Valid values therefore include:

+9, +9.1, +9.01, +10, +100, +1,000, +1,000,000 …

and:

-9, -9.1, -10, -100, -1,000, -1,000,000 …

The implementation MUST NOT silently clamp a value merely because it crosses the ±9 human reference range.

For exact arbitrary-precision representation, canonical interchange SHOULD serialize decimal values losslessly rather than relying on a binary floating-point representation.

### 15.3 Zero is a first-class value

0 is valid.

0 MUST NOT mean “bad.”

0 means one of:

- neutral measured contribution;
- no measurable positive or negative effect on that dimension;
- insufficient evidence to establish a directional effect, when the dimension explicitly uses zero as its neutral representation.

The reason for a zero should remain distinguishable where necessary.

### 15.4 Polarity and magnitude

Positive and negative directional value are represented explicitly.

For dimensions where “harm” is conceptually a magnitude rather than a direction, harm SHOULD be represented as a non-negative magnitude with:

0 = no observed or estimated harm

and increasing positive magnitude = increasing harm.

A positive benefit MUST NOT numerically cancel or erase an explicit harmful effect merely because a composite formula can subtract one number from another.

The system preserves the underlying dimensions and their reasons.

### 15.5 Value is not truth

Value answers:

> “How useful, beneficial, costly, risky, harmful, reusable, consequential, or otherwise important does this appear to be?”

Truth answers:

> “How well supported is the claim that this is so?”

Authority answers:

> “Who or what is allowed to act?”

These MUST remain separate dimensions.

High value MUST NOT increase truth confidence.

High value MUST NOT create authority.

Strong engagement MUST NOT create truth.

### 15.6 Every value estimate carries an evidence boundary

A value record SHOULD distinguish:

- estimated_value;
- observed_value;
- evidence_strength;
- evidence_refs;
- basis/method;
- context;
- timestamp;
- value_model_version;
- value_history.

The system MUST distinguish:

**ASSIGNED VALUE** — current estimate or prior assignment;

**OBSERVED VALUE** — value supported by observed results;

**EVIDENCE STRENGTH** — how strongly the evidence supports the assigned or observed value.

A value estimate may be wrong.

The system must therefore be able to revise value without pretending the earlier estimate never existed.

### 15.7 Value learning loop

Value changes should follow:

ESTIMATE → APPLY → OBSERVE → VERIFY → UPDATE VALUE

A verified outcome may increase or decrease the value estimate.

Unverified assumptions may remain provisional.

The system MUST NOT promote estimated value merely because an AI generated it confidently.

### 15.8 Engagement is evidence of reaction, not truth

Likes, comments, shares, clicks, reuse, completion, retention, or other engagement signals MAY contribute to a value model.

They MUST NOT be treated as automatic proof of truth.

Engagement SHOULD have a defined influence, provenance, time window, and diminishing-return rule where appropriate so popularity cannot create a self-reinforcing ranking loop.

### 15.9 Value categories

The system should distinguish at least:

1. Intelligence Value — value of the knowledge itself.
2. Outcome Value — value of the observed result.
3. Action Value — benefit/cost/harm associated with an action.
4. Relationship Value — value added by connecting intelligence.
5. Learning Value — value created by what was learned.
6. Contribution Value — reusable value contributed by an actor.
7. System Value — value created for the larger intelligence system.

These values MUST NOT be silently conflated into a person score, Node score, or authorization decision.

### 15.10 Composite values

A composite value MAY be calculated for prioritization or retrieval when:

- the formula is explicit;
- the dimensions are known;
- the weights are versioned;
- missing evidence is handled explicitly;
- harm and risk are not hidden;
- the result does not create authority;
- the result does not replace the underlying vector.

A composite score is a derived view, never the canonical meaning.

### 15.11 Value histories

Value is temporal.

The Node SHOULD preserve value revisions as history:

VALUE(t0) → VALUE(t1) → VALUE(t2) …

A newer value estimate does not erase the older one.

Where context changes, value MAY change without the underlying Node becoming false or superseded.

### 15.12 Human profiles

A person or contributor SHOULD NOT be reduced to one permanent score.

A profile may expose derived dimensions such as:

knowledge, demonstrated utility, reliability, contribution, verification record, learning yield, collaboration, stewardship, consistency, and domain mastery.

Any human-facing star/progression label is a derived projection of the underlying evidence and MUST NOT become a hidden authority mechanism.

### 15.13 Value invariants

- **VALUE ≠ TRUTH**
- **VALUE ≠ AUTHORITY**
- **VALUE ≠ POPULARITY**
- **ESTIMATE ≠ OBSERVATION**
- **OBSERVATION ≠ CAUSALITY**
- **ZERO ≠ BAD**
- **HARM MUST REMAIN EXPLICIT**
- **POSITIVE VALUE DOES NOT ERASE NEGATIVE EFFECTS**
- **±9 ARE REFERENCE ANCHORS, NOT LIMITS**
- **MORE ENGAGEMENT ≠ MORE TRUTH**
- **MORE VALUE ≠ MORE AUTHORITY**

### 15.14 Implementation boundary

This section defines the semantic target.

The existing V1 Node envelope may require a versioned schema evolution to represent lossless arbitrary-precision decimals, value history, explicit polarity, and evidence strength without ambiguity.

Until that evolution is implemented and tested, these semantics remain **SPECIFICATION CANDIDATE**, not an assumed runtime capability.

## 16. Provenance and evidence
Every committed Node must be attributable to a source event or source object.

Minimum provenance:
source, source reference, captured by, derived-from lineage.

Minimum evidence:
evidence state, evidence references, verification method, verification time where applicable.

Raw source and distilled Node are related but not identical:
the source preserves origin; the Node preserves reusable meaning.

## 17. Relationships and Collective Chain
A Node can connect to:
- source and parent intelligence;
- supporting or related Nodes;
- contradictory or superseding Nodes;
- applications;
- outcomes;
- learning evidence;
- Master Nodes;
- Hub surfaces.

A durable relationship should identify source, target, relation type, and required evidence/authority.
Collective Chain Technology is a governed graph, not merely a chronology.

## 18. Master Node
A Master Node is a map of canonical intelligence, never a replacement for it.

It may contain:
purpose, current distilled state, child references, relationship graph, priorities, applicability, supersession, retrieval routes, and derived summaries.

It must not become a second canonical memory store.
If a child Node changes, the Master Node updates references or derived views rather than silently copying the canonical object.

## 19. Smart Link
A Smart Link is an evidence-bearing doorway to a verified repository projection.

It is returned only after:
1. canonical capture succeeds;
2. receiver-owned IB identity exists;
3. persistence and lineage checks succeed;
4. projection uses the authoritative IB identity;
5. GitHub projection verification succeeds.

A raw GitHub URL constructed by Naya is not automatically a Smart Link.

## 20. Lifecycle
RECOGNIZE → DISTILL → STRUCTURE → GOVERN → COMMIT → VERIFY → CONNECT → SURFACE → APPLY → MEASURE → LEARN → UPDATE / SUPERSEDE

Do not collapse lifecycle states into one “done” flag.
Recognition is not commitment.
Commitment is not truth.
Truth is not authority.
Reuse is not learning.
Learning requires evidence from outcomes when improvement is claimed.

## 21. Retrieval and application
Retrieval is contextual.
A retrieved Node must carry enough identity and applicability information for Naya to determine whether it should influence the current task.

Before application Naya checks:
identity, truth, authority, privacy, freshness, applicability, conflicts, supersession, and evidence strength.

Retrieval never automatically grants authority to act.

## 22. Reconciliation
SEARCH → COMPARE → RECONCILE → MERGE / UPDATE / CREATE.

Merge only when meaning is equivalent and authority/provenance permit.
Update when a newer Node refines an older one.
Supersede when the older Node is no longer current.
Preserve both when contexts differ.
Mark CONFLICTED when material disagreement remains unresolved.

Never silently destroy provenance.

## 23. Human experience
The interface should present:
1. what this is;
2. why it matters;
3. what can be done with it;
4. current state;
5. one useful doorway.

Technical IDs, hashes, evidence records, authority grants, lineage, and machine envelopes remain progressively disclosed.

“Play” reads the most useful human-facing representation.
A playback conversation does not mutate the original Node unless a later governed action creates or updates intelligence.

## 24. Smart app ecosystem
A NayaNET smart app is an interface or application that consumes and contributes governed Nodes through the same intelligence contract.

It should:
- authenticate;
- request only required authority;
- retrieve applicable Nodes;
- submit intelligence through the canonical path;
- preserve provenance;
- respect privacy;
- separate truth from authority;
- expose verified receipts;
- contribute outcome evidence only within scope.

## 25. Activation architecture
Target user experience:

CONNECT NAYANET → CONNECT GITHUB → AUTHORIZE → ENTER NAYANET

Ordinary users should not configure Supabase projects, database schemas, Edge Functions, webhooks, deployment plumbing, or internal cryptographic identities.

The service boundary hides infrastructure:
Human → NayaNET App → Naya Language → NayaPOWER API → canonical persistence → Nodes/Chain → GitHub projections → Hub.

## 26. Acceptance gate
V1 is ready for formal ratification only when all are demonstrated:
- canonical receiver assigns identity;
- no local IB allocator exists in the active path;
- intent aliases map consistently;
- materially ambiguous commands request clarification;
- language inference never expands authority;
- provenance survives capture;
- truth and authority remain distinct;
- privacy survives capture;
- duplicate inputs are idempotent;
- Smart Link appears only after verified projection;
- fresh-context retrieval returns the same intelligence;
- application ties back to the Node;
- learning claims have outcome evidence;
- Master Nodes remain reference/index layers;
- activation hides backend complexity from ordinary users.

## 27. Empirical baseline
The first specimen is IB-001229.
It was captured through v7-smart-note-canonical and produced a receiver-owned Intelligent Block, canonical event and transaction, private Feed verification, learning evidence in CANDIDATE state, verified GitHub projection, verified Smart Link, and Hub Deep Link.

That is enough to ground this initial specification.
It is not enough to claim universal retrieval, application, community, or collective learning quality.

## 28. Design hypotheses not yet law
These remain testable:
- fixed word budgets;
- fixed compression ratios;
- automatic demotion from usage alone;
- requirement that every Node connect to another Node;
- automatic promotion of every verified outcome;
- a single composite value score;
- a fixed number of perspectives;
- exact value-update formulas and weights;
- diminishing-return curves for engagement;
- the canonical arbitrary-precision interchange representation;
- thresholds for converting estimated value into observed or verified value.

## North Star
Make intelligence a connected, governed object:
simple for humans, precise for machines, useful in the moment, trustworthy about what is known, and capable of becoming more valuable through verified use.

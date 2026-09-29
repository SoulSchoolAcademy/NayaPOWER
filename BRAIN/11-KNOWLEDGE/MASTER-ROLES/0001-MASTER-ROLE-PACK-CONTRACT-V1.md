# NayaPOWER Master Role Pack Contract V1

**Status:** PROPOSED CANONICAL — REVIEW REQUIRED  
**Proof state:** STRUCTURED / NOT YET BEHAVIORALLY PROVEN  
**Canonical home:** `BRAIN/11-KNOWLEDGE/MASTER-ROLES/`

## 1. Decision

NayaPOWER may preserve reusable expert cognition as **Master Role Packs**.

A Master Role Pack is not:
- a separate Naya;
- a separate brain;
- an authority source;
- a personality costume;
- proof that a runtime is an expert.

It is a governed, selectively retrievable bundle of existing canonical intelligence types such as `CAPABILITY`, `PROCEDURE`, `PRINCIPLE`, `RULE`, `LEARNING`, `CONSTRAINT`, and `EVIDENCE`.

Core law:

> **ONE NAYA. MANY EXPERT COGNITIVE LENSES.**

## 2. Why no new canonical object type

The current object registry already represents the semantic parts of expert cognition. Creating `EXPERT_PROFILE` or `MASTER_ROLE` as a new canonical type would add ontology before a responsibility gap is proven.

Therefore V1 uses:
- a **role-pack artifact** for navigation/composition;
- existing canonical object types for promoted intelligence;
- graph relationships for reuse and cross-role sharing;
- the existing promotion/proof lifecycle for trust.

If later evidence proves an irreducible lifecycle responsibility, a new object type must pass the object-type creation law.

## 3. Required role-pack envelope

Every pack MUST define:

1. `role_key` — stable semantic key for the role artifact.
2. `title`
3. `version`
4. `status`
5. `proof_state`
6. `mission`
7. `responsibility_boundary`
8. `non_goals`
9. `domain_knowledge`
10. `first_principles`
11. `mental_models`
12. `diagnostic_questions`
13. `decision_frameworks`
14. `methods`
15. `heuristics`
16. `failure_modes`
17. `anti_patterns`
18. `tradeoffs`
19. `evidence_hierarchy`
20. `verification_requirements`
21. `tools_and_capabilities`
22. `collaboration_interfaces`
23. `escalation_rules`
24. `expected_outputs`
25. `quality_gates`
26. `learning_behavior`
27. `proof_requirements`
28. `refuses_to_assume`
29. `applicability_signals`
30. `conflict_handling`
31. `authority_boundary`
32. `source_lineage`
33. `relationships`
34. `canonical_object_refs`

Missing required sections are `INCOMPLETE`, not implicitly satisfied.

## 4. Identity strategy

**PATH IS NAVIGATION. ID IS IDENTITY.**

A role-pack artifact uses a stable `role_key` for selection and navigation. It does not invent sequential canonical object IDs.

When role intelligence is promoted into canonical semantic objects:
- IDs MUST be allocated by the canonical allocator;
- IDs MUST follow the existing `NAYA-<TYPE>-<SEQUENCE>` law;
- the role pack records those IDs in `canonical_object_refs`;
- changing the folder/title MUST NOT change underlying canonical object identities.

V1 role keys use lowercase kebab case, for example:

`master-ai-systems-architect`

## 5. Representation law

Each role has one semantic pack with coherent views:

- **Human view:** concise purpose, what to remember, how to apply, uncertainty.
- **AI view:** explicit reasoning context, questions, constraints, tradeoffs, conflict handling.
- **Machine view:** validated JSON with deterministic keys/enums/references.
- **Schema view:** `MASTER-ROLE-PACK-SCHEMA-V1.json`.
- **Proof view:** later evidence showing whether retrieval/application improved behavior.

No view may upgrade epistemic or proof status.

## 6. Selective retrieval contract

A runtime MUST NOT load all roles by default.

Selection pipeline:

```
TASK
→ CLASSIFY TASK SIGNALS
→ MATCH APPLICABILITY
→ SELECT PRIMARY ROLE
→ SELECT ONLY NECESSARY COMPLEMENTARY ROLES
→ CHECK AUTHORITY
→ RETRIEVE SHARED + ROLE-SPECIFIC INTELLIGENCE
→ COMPOSE WITHOUT ERASING DISAGREEMENT
→ APPLY
→ VERIFY
```

Default composition ceiling: **one primary + up to two complementary roles**, unless the task explicitly requires a wider council.

Selection signals are descriptive, not authority-bearing.

## 7. Task-to-role selection

A role may be selected when:
- the task exhibits one or more declared `applicability_signals`;
- its boundary materially covers the decision;
- its content is current enough for the task;
- unresolved conflicts do not make application unsafe;
- required authority is independently present.

Role selection MUST preserve:
- task objective;
- current canonical state;
- relevant constraints;
- proof requirements;
- unresolved uncertainty.

## 8. Multi-role composition

Composition MUST NOT average opinions.

The runtime should:
1. identify the primary decision owner by problem type;
2. retrieve complementary lenses only for material seams;
3. keep each role's claims attributable;
4. surface contradictions;
5. use the strongest evidence applicable to the exact question;
6. prefer the smallest solution satisfying all hard constraints;
7. escalate unresolved authority or safety conflicts rather than synthesizing them away.

No role can grant authority to another role.

## 9. Contradiction handling

When role guidance conflicts:

```
IDENTIFY CLAIMS
→ IDENTIFY SCOPE
→ IDENTIFY EVIDENCE
→ IDENTIFY AUTHORITY IMPLICATIONS
→ RECONCILE IF COMPATIBLE
→ OTHERWISE PRESERVE CONTRADICTION
→ REQUEST / REQUIRE DECISION AT THE CORRECT AUTHORITY LEVEL
```

Do not collapse:
- security vs convenience;
- performance vs correctness;
- usability vs authority;
- implementation speed vs proof;
- current evidence vs historical guidance.

## 10. Shared intelligence rule

Do not duplicate durable knowledge into every role.

Shared principles, procedures, evidence, and learning should remain canonical once and be connected through typed relationships such as:
- `APPLIES_TO`
- `USED_BY`
- `DEPENDS_ON`
- `SUPPORTS`
- `REFINES`
- `CONTEXTUALIZES`
- `LEARNED_FROM`

Role packs are retrieval/composition maps over shared intelligence, not copies of the brain.

## 11. Authority boundary

**CAPABILITY DOES NOT CREATE AUTHORITY.**

Loading a Master Role Pack:
- MAY change what questions a Naya asks;
- MAY improve analysis and proposed action;
- MAY change which evidence it retrieves;
- MUST NOT expand permissions;
- MUST NOT bypass consent;
- MUST NOT self-promote learning;
- MUST NOT reinterpret a capability as authorization.

Authority remains governed by the existing LAW / governance contracts.

## 12. Learning and promotion lifecycle

Role knowledge evolves through the existing river:

```
EXPERIENCE
→ CAPTURE
→ DISTILL
→ STRUCTURE
→ CONNECT
→ PROVE
→ PRESERVE
→ RETRIEVE
→ APPLY
→ OUTCOME
→ VERIFY
→ LEARN
→ PROMOTE / REJECT
→ SUCCESSOR
```

A role pack update is not trusted because it sounds expert.

A candidate improvement must preserve provenance, survive verification, and remain scoped to what the evidence supports.

## 13. Evaluation and proof model

Artifact-level acceptance:
- schema-valid machine representation;
- all required cognition sections present;
- source lineage resolvable;
- authority boundary explicit;
- no duplicate canonical knowledge;
- human and machine views coherent;
- selective retrieval signals explicit.

Behavioral proof requires a bounded experiment:

```
SAME TASK
→ WITHOUT ROLE PACK
→ WITH ROLE PACK
→ PREDECLARED EXPERT-BEHAVIOR METRICS
→ OBSERVED OUTCOMES
→ INDEPENDENT RECOMPUTATION
→ PRESERVED EVIDENCE
```

Ultimate continuity proof adds:

```
VERIFIED ROLE LEARNING
→ PRESERVE
→ COLD SUCCESSOR RECEIVES ROLE ID / REFERENCES, NOT INJECTED ANSWER
→ RETRIEVES AUTHORITATIVE PACK
→ APPLIES IT
→ INDEPENDENTLY VERIFIED IMPROVEMENT
```

Until that exists, status is never `PRODUCTION_PROVEN`.

## 14. Quality gate

A Master Role Pack is AAA-ready only when:
- it improves reasoning specificity without bloating context;
- it names what it refuses to assume;
- it contains falsifiable proof requirements;
- it distinguishes recommendations from authority;
- it maps to shared canonical intelligence rather than duplicating it;
- a cold Naya can discover when and how to use it;
- it can be updated through governed learning.

## 15. V1 specimen

The first specimen is:

`AI-SYSTEMS-ARCHITECT/MASTER-AI-SYSTEMS-ARCHITECT-V1.json`

Its purpose is to test the contract itself before scaling the other 17 role packs.

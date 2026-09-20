# CIS — NAYA POWER UNIVERSAL ASSESSMENT NORTH STAR — NAYA

## STATUS
**NORTH STAR: LOCKED — 2026-08-24**

This is the canonical AI-facing intelligent brief for the next major Naya Power product direction.

## SYSTEM IDENTITY
**Naya Power** = the user-facing AI learning, creation, memory, growth, and capability system.
**CIS** = Compounding Intelligence System: the intelligence architecture that preserves, connects, recalls, and compounds useful learning and experience over time.
**MAXESS** = the assessment/scoring engine that evaluates capability on a defined subject/topic using a repeatable, config-driven model.

Layer law:
- MAXESS scores/evaluates.
- Naya teaches, guides, remembers, creates, and helps the person improve.
- CIS compounds durable intelligence produced through use.

## NORTH STAR PRODUCT
Create a public, push-button assessment experience where any person can:
1. Enter their name.
2. Enter any subject/topic they want assessed on.
3. Receive a dynamically generated, high-quality assessment for that topic.
4. Complete a concise assessment.
5. Receive an immediate personalized score/report showing current capability.
6. Repeat the assessment as desired to learn, improve, and observe progress.
7. Be invited into Naya Power to learn the subject with an AI master/teacher beside them.
8. Eventually use the same assessment infrastructure to validate learning and produce a Naya Power Academy certificate/recognition artifact.

Core promise:
**Give me a subject. Help me understand where I am, help me learn, and give me a way to measure my growth.**

## USER EXPERIENCE
Landing page primary action:
**YOUR NAME + WHAT DO YOU WANT TO BE ASSESSED ON?**

Guidance:
"The more precise your topic, the more accurately we can create your assessment. Type or speak your topic. Your personalized assessment will be created for you."

Initial target: approximately 3 minutes, immediate feedback, no unnecessary setup.

The assessment remains useful without Naya Power. The result becomes the contextual invitation to experience Naya Power.

## PRODUCT FUNNEL
**ENTER NAME + SUBJECT → GENERATE ASSESSMENT → TAKE TEST → SCORE → PERSONALIZED REPORT → INVITE TO NAYA POWER → LEARN WITH NAYA → REASSESS → COMPOUND → RECOGNIZE/VALIDATE**

Positioning:
**MAXESS shows where you are. Naya helps you get where you want to go. CIS helps preserve and compound what you learn.**

## TECHNICAL PRINCIPLE
Do NOT hard-code an assessment for every subject.

Build one reusable assessment engine with a dynamic content-generation layer.

Pipeline:
**SUBJECT INPUT → NORMALIZE → SCOPE/LEVEL → KNOWLEDGE DOMAINS → ASSESSMENT BLUEPRINT → QUESTIONS/ANSWERS/SCORES → VALIDATE → RENDER → SCORE → REPORT → VOICE → PERSIST → INVITE**

## ASSESSMENT GENERATION MODEL
AI acts as both subject-matter master and assessment designer.

Before writing questions, derive:
1. What the subject fundamentally means.
2. Most important concepts/principles.
3. Relationships between concepts.
4. Practical application/decision-making.
5. Common misconceptions/failure modes.
6. Appropriate depth for the requested topic.
7. Capability dimensions that matter.
8. Evidence distinguishing weak, developing, advanced, and mastery-level understanding.

Then generate the assessment.

## REPEATABLE 15-QUESTION FRAMEWORK
Default: **15 questions**, normally **3 questions across each of 5 capability dimensions**. Dimensions may be subject-adapted while preserving a stable scoring contract.

Default conceptual dimensions:
1. **FOUNDATION** — vocabulary, definitions, core concepts.
2. **UNDERSTANDING** — relationships, principles, why/how.
3. **APPLICATION** — realistic use of knowledge.
4. **ANALYSIS** — comparison, diagnosis, reasoning, tradeoffs.
5. **MASTERY** — synthesis, judgment, transfer, edge cases, creation/teaching.

Question mix should include foundational knowledge, conceptual understanding, scenarios/application, reasoning/analysis, and transfer/synthesis.

Target the **sweet spot**: challenging enough to measure meaningful capability, accessible enough to be fair, useful enough that every question teaches something.

## QUESTION QUALITY LAW
Every question must have:
- one defensible best answer;
- plausible distractors based on realistic misconceptions or weaker reasoning;
- enough context to answer fairly;
- no accidental clues from wording/length;
- no irrelevant trivia unless the subject requires it;
- one clear capability mapping;
- deterministic scoring metadata;
- a concise teaching rationale.

## SCORING CONTRACT
Scoring is deterministic and independent from presentation.

Generated assessment must provide machine-readable metadata for every answer.

Output:
- overall score 0–100;
- five dimension scores;
- capability band;
- optional question diagnostics;
- stable result fingerprint/identifier.

Default bands:
**EMERGING → FOUNDATION → DEVELOPING → ADVANCING → MASTERING**

AI may generate content and interpretation but must not silently alter the scoring algorithm after the assessment begins.

## GENERATION VALIDATION
Never trust raw AI-generated assessment content directly in production.

**GENERATE → SCHEMA VALIDATE → CONTENT QA → SCORING QA → PRESENT → SCORE → REPORT**

Reject/regenerate when count, IDs, dimensions, scores, answer validity, scope, duplication, or schema integrity fails.

## EXISTING CODEBASE POSITION
Canonical repository: **SoulSchoolAcademy/NayaPOWER**.
The repository is public, uses `main`, and is primarily HTML; its current description is "Maxess Results Page +". fileciteturn218file0L2-L5

The repository already contains CIS capture/verification artifacts, including the established dual-note model. fileciteturn219file0L2-L2

Historical E00/E01–E04 mappings must be re-verified from source before implementation; do not rely on memory alone.

## IMPLEMENTATION STRATEGY
Do not rebuild MAXESS from scratch.

### 1. Freeze the working contract
Extract the actual current assessment schema, answer schema, dimensions, scoring functions, state management, result object, rendering, voice behavior, and tests.

### 2. Separate engine from content
Target conceptual modules:
`AssessmentInput`, `AssessmentBlueprint`, `AssessmentGenerator`, `AssessmentValidator`, `AssessmentConfig`, `ScoringEngine`, `ResultBuilder`, `ReportGenerator`, `NarrationGenerator`, `CertificateGenerator`.

UI consumes structured assessment data; subject-specific logic does not live in presentation code.

### 3. Build dynamic subject generation
Input:
`name + subject + optional clarification`

Return validated `AssessmentConfig` containing normalized subject, scope, level, 15 questions, 5 answers/question, 5 dimensions, scores/weights, explanations, metadata, and generation/version identifiers.

Use a server-side/API generation boundary. Do not expose model credentials in browser code.

GitHub is the source/control layer for code, schemas, prompts, protocols, and versioned artifacts. It is not the runtime inference engine.

### 4. Make generation cost-efficient
Cache validated assessments where appropriate; generate once per assessment/version; keep prompts compact/schema-driven; validate locally before retries; avoid unnecessary regeneration; measure runtime model cost.

### 5. Repair/verify scoring
Investigate contract failures first, especially:
- answer IDs not matching score lookup IDs;
- score metadata not surviving state transitions;
- dimension IDs mismatching config/result dimensions;
- async generation/state races;
- stale closures;
- calculation before final answer save;
- result object overwritten/partial;
- display labels used as canonical IDs;
- generated shape differing from static engine expectations.

Canonical sequence:
**SELECT → VALIDATE → SAVE ANSWER → SAVE SCORE METADATA → ADVANCE → FINAL ANSWER SAVED → CALCULATE → BUILD RESULT → VALIDATE RESULT → RENDER**

Never infer score from rendered text.

### 6. Naya voice
Voice is presentation, not scoring.

Preferred:
`structured result → Naya narration text → controlled TTS/voice provider → playback`

Browser read-aloud can remain a fallback/accessibility feature, but product-quality Naya voice should be controlled and consistent. Generate narration from the same canonical result object used by the visual report so voice and screen cannot disagree.

### 7. Results
Every successful assessment should provide overall score, capability band, five dimensions, strongest capability, growth opportunity, concise personalized explanation, next learning action, and Naya Power invitation.

The result should feel like an immediate reward, not merely a grade.

## FUTURE CERTIFICATE SYSTEM
**LEARN WITH NAYA → TAKE MAXESS → SCORE → SAVE RESULT → REPORT → REQUEST CERTIFICATE → VALIDATE RESULT → CREATE CERTIFICATE → UNIQUE ID/VERIFICATION → PRINT/SHARE**

Certificate issuance must be based on a recorded assessment result, not self-declaration.

Use a unique certificate/result identifier and verification mechanism. Clearly distinguish Naya Power Academy recognition from regulated/accredited educational credentials; never imply accreditation that does not exist.

## CIS INTEGRATION
The larger loop is:
**LEARN → APPLY → ASSESS → REFLECT → CAPTURE → RECALL → REASSESS → COMPOUND**

Human recall defaults to the human-readable note; AI uses the compact AI note for continuity/reasoning. Capture is intentional, not automatic.

## TEN-STAR SERVICE
User-visible complexity should be almost zero:
**TYPE → CLICK → LEARN/ANSWER → SEE RESULT → FEEL PROGRESS → KNOW WHAT TO DO NEXT**

The system handles complexity behind the scenes.

## NON-NEGOTIABLES
- Preserve working MAXESS behavior before refactoring.
- Keep scoring deterministic.
- Keep UI, generation, scoring, and reporting separable.
- Validate all AI-generated assessment data.
- Never expose API secrets in browser code.
- Never misrepresent certificate accreditation.
- Optimize for fairness and learning value.
- Never make the user manage the architecture.
- Verify every meaningful implementation change.

## SUCCESS TEST
A stranger should be able to type any reasonable subject, click one button, and receive a coherent, fair, challenging, personalized assessment and result without knowing the underlying technology.

Desired reaction:
**"If Naya can assess me on this, I want to see what happens when Naya actually teaches me this."**

## NORTH STAR SENTENCE
**MAXESS measures what you know. Naya helps you learn what you want to know. CIS helps you keep and compound what you learn.**

## EXECUTION COMMAND
**READ → MAP → PRESERVE → SEPARATE → GENERATE → VALIDATE → SCORE → REPORT → VERIFY → SHIP.**

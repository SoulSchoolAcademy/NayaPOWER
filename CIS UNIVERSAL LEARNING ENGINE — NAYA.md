# CIS UNIVERSAL LEARNING ENGINE — NAYA

## STATUS
Strategic product direction captured from Shawn's latest four substantive discussions. This is a durable product concept and proposed build direction, not a claim that every capability is already implemented.

## CANONICAL MODEL
MAXESS = MEASURE
NAYA = TEACH + GUIDE
CIS = REMEMBER + COMPOUND
NAYA POWER = COMPLETE EXPERIENCE

The score is not the destination. The score tells the learner where they are; Naya helps them move forward; CIS turns progress into durable capability.

## PRODUCT THESIS
Evolve MAXESS from a fixed AI assessment into a general-purpose, topic-agnostic assessment engine.

A user should be able to enter almost any subject/topic and receive a dynamically generated assessment without a pre-built course catalog.

Core flow:
SUBJECT/TOPIC → NORMALIZE → GENERATE ASSESSMENT → ANSWER → SCORE → REPORT → LEARNING INVITATION

Learning loop:
VISION/GOAL → LEARN → PRACTICE → ASSESS → SCORE → IDENTIFY GAPS → LEARN AGAIN → REASSESS → COMPOUND

## USER EXPERIENCE
Primary public entry:
**WHAT DO YOU WANT TO LEARN OR BE ASSESSED ON?**

Two obvious paths:
- GET YOUR AI SCORE
- ASSESS ANY SUBJECT

Users may select a sample subject or enter their own subject.

The public assessment should provide genuine value rather than artificially withholding the result. The result then naturally introduces Naya Power as the persistent learning relationship.

## DYNAMIC ASSESSMENT ARCHITECTURE
The generator must return a validated machine-readable assessment configuration before rendering.

Minimum contract:
- assessmentId
- subject
- scope
- version
- dimensions[]
- questions[]
- answers[]
- scoringRules
- difficulty
- metadata

Each question requires a stable ID, dimension, order, prompt, answer options, scoring/weights, and metadata sufficient for deterministic scoring.

The renderer consumes configuration. The UI does not invent scoring logic.

## ENGINE SEPARATION
TOPIC GENERATION → creates assessment specification.

ASSESSMENT CONFIGURATION → defines questions, dimensions, answers, weights, difficulty, and version.

SCORING ENGINE → independently computes normalized scores and dimension results.

RESULTS ENGINE → renders score, capability band, strengths, opportunities, and report.

LEARNING ENGINE → Naya teaches, questions, practices, reviews, adapts, and guides.

MEMORY/CIS → preserves authorized learning and progress.

RECOGNITION ENGINE → creates recognition only from verified assessment results.

## MAXESS REUSE STRATEGY
Do not discard the current MAXESS work. The existing E00 family and related E00.01/E00.02/E00.03/E01–E04 surfaces contain valuable presentation and interaction patterns. Shawn identifies **E00 118** as the active front-end artifact.

The existing E00 118 artifact visibly contains the premium MAXESS visual system, progress UI, question/answer interaction, Naya presence, and local results presentation. Reuse the proven presentation layer while repairing/extracting the underlying assessment and result contracts.

## SCORING FAILURE INVESTIGATION
When a score is missing or incorrect, first inspect the Results boundary and state/data contract rather than rewriting the visual experience.

Required observable pipeline:
QUESTION ANSWERED → SAVE → RESPONSE ASSERTION → CALCULATE → DIMENSION SCORES → BUILD RESULT OBJECT → VALIDATE → STORE → BROADCAST → LOCAL RESULTS → RELEASE/HANDOFF

A calculation function existing in source code is not proof that a score reaches the user. Every boundary must be observable and validated.

## NAYA VOICE
Future dynamic voice architecture:
TEXT SCRIPT → CONTROLLED TTS/VOICE LAYER → NAYA VOICE OUTPUT

Browser speech/read-aloud can be a fallback or prototype, but it should not be treated as the canonical Naya voice. A controlled voice layer should own pronunciation, pacing, personality, consistency, and dynamic report narration.

## LEARNING COMPANION
The intended experience is a persistent AI master teacher for any chosen subject.

Naya should be able to:
- explain the subject
- teach progressively
- ask questions
- adapt to the learner
- practice with the learner
- identify gaps
- review prior material
- remember authorized learning
- help the learner reassess
- compound capability over time

The conceptual command is:
**“Teach me [ANY SUBJECT].”**

## RECOGNITION / CERTIFICATE
A future workflow can use verified MAXESS results to produce a Naya Power Academy recognition/certificate.

Potential verified fields:
subject • learner • score • capability band • assessment version • date • unique serial/verification identifier • Naya Power Academy branding/signature/stamp

Recognition must accurately represent performance inside the Naya Power assessment system and must not be misrepresented as an accredited academic credential.

The certificate should be generated from verified result data, not self-declared claims.

## CAPABILITY BANDS
Use the finalized canonical band model once locked. Current concept:
EMERGING → FOUNDATION/DEVELOPING → ADVANCING → MASTERING

Do not hard-code a band definition until the canonical MAXESS scoring specification is finalized.

## LEAD / CONVERSION LOOP
FREE ASSESSMENT → REAL RESULT → DISCOVER GAP → INVITE NAYA POWER → 5-DAY / 5-LESSON EXPERIENCE → DAILY LEARNING → COMPOUND

The free assessment acts as proof of value and a permanent invitation to the deeper Naya Power experience.

## NORTH STAR
Give anyone, anywhere, the ability to choose what they want to learn, learn with a persistent AI master teacher, test what they actually know, see measurable progress, and turn learning into durable capability.

## BUILD ORDER
1. Stabilize current MAXESS scoring/result contract.
2. Extract reusable configuration-driven assessment schema.
3. Build subject intake and normalization.
4. Build validated dynamic question generation.
5. Connect generated configuration to existing MAXESS renderer.
6. Verify deterministic scoring across arbitrary subjects.
7. Build dynamic report generation.
8. Add controlled Naya voice/TTS.
9. Add progress/history and CIS learning-memory integration.
10. Add verified recognition/certificate generation.
11. Optimize the public assessment → Naya Power conversion path.

## GOVERNING PRINCIPLE
Do not build a giant catalog of courses first. Build the engine that can create the right assessment and learning path for the subject the human chooses.

The larger innovation is the loop:
**CHOOSE → LEARN → MEASURE → IMPROVE → REMEMBER → COMPOUND → DEMONSTRATE.**

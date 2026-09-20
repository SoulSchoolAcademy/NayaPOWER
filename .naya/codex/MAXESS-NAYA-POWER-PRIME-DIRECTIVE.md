# MAXESS × NAYA POWER — PRIME DIRECTIVE

**Document:** Operation Manual for the Creation and Operation of MAXESS + Naya Power
**Status:** CANONICAL NORTH STAR
**Effective:** 2026-08-24
**Owner / Human authority:** Shawn
**Name spelling law:** `SHAWN` — S-H-A-W-N. Never substitute Sean.

---

## 0. PURPOSE

Build the smallest coherent system that turns Naya Power + MAXESS into a push-button learning, assessment, feedback, memory, and continuous-growth experience.

The user should be able to:

1. Enter their **name**.
2. Enter or speak **any subject/topic** they want assessed.
3. Press one button.
4. Receive a dynamically generated, high-quality 15-question assessment appropriate to that subject.
5. Complete it in roughly three minutes.
6. Have the score calculate automatically.
7. Receive the canonical result through the existing MAXESS Results architecture.
8. See a personalized report, score, dimensions, mastery level, and actionable feedback.
9. Be invited to activate Naya Power so Naya can teach, remember, reinforce, and compound learning over time.

The system is not a collection of patched pages. It is one coherent engine with a stable contract between **assessment generation → assessment runtime → scoring → results → Naya → memory → learning loop**.

---

# 1. NORTH STAR

> **Any person, anywhere, should be able to choose something they want to learn, have Naya help them learn it, test themselves whenever they choose, understand exactly where they stand, and continuously improve without being judged for starting where they are.**

The product loop is:

**CHOOSE → LEARN → PRACTICE → ASSESS → SCORE → UNDERSTAND → REMEMBER → IMPROVE → REASSESS → COMPOUND**

MAXESS is the assessment/measurement engine.
Naya Power is the operating and learning intelligence around it.
Together they create a **Compounding Intelligence System**: learning becomes measurable, retrievable, repeatable, and continuously improvable.

---

# 2. SOURCE-OF-TRUTH RULE

Before changing implementation:

**READ → UNDERSTAND → ESTABLISH STATE → CHANGE → TEST → OBSERVE → VERIFY → DOCUMENT**

The canonical repository is `SoulSchoolAcademy/NayaPOWER`, branch `main`.

Repository reality outranks assumptions, remembered context, and previous explanations.

The existing MAXESS artifacts are valuable source material, but they are not permission to preserve a flawed implementation merely because it exists.

The most valuable existing assessment artifact is **E00 118**, because it contains the current visual structure, interaction model, question/answer presentation, and flow. E00.01, E00.02, E00.03, and E01–E04 provide valuable bridge, isolation, result-contract, and presentation patterns.

Use existing work as a **reference architecture and reusable asset**, not as a patch target when a clean implementation is safer and faster.

---

# 3. EXISTING ARCHITECTURE TO PRESERVE

The current Results boundary already establishes an important separation:

```text
E00
  ↓
MAXESS_RESULT_V1
  ↓
E00.01  — canonical result access / bridge
  ↓
E00.03  — result validation + release controller
  ↓
E00.02  — Results isolation / visual release boundary
  ↓
E01 → E09
```

The current bridge validates, at minimum:

- `contractVersion === MAXESS_RESULT_V1`
- `overallScore` is an integer from 0–100
- exactly 5 dimensions
- exactly 15 responses

The controller explicitly must **not** score, render Results, or alter E00. Its job is handoff and validation. This separation is architecturally correct and should be preserved. fileciteturn240file0 fileciteturn242file0

The isolation layer also correctly keeps Results hidden until the assessment has completed and releases the Results boundary only after a valid result exists. fileciteturn241file0

E01 is already designed as a premium Naya + score-reveal experience and therefore should be treated as a presentation target, not the place where scoring logic is invented. fileciteturn243file0

---

# 4. THE CRITICAL DESIGN DECISION

## Separate four concerns completely

### A. Assessment Generator
Turns a user subject into a deterministic assessment specification.

### B. Assessment Runtime
Displays questions, accepts answers, manages progress, and saves responses.

### C. Scoring Engine
Consumes only a valid assessment + responses and returns a canonical score object.

### D. Results / Learning Layer
Consumes the canonical score object and renders the report, feedback, Naya experience, and next actions.

Never let one layer secretly perform another layer's job.

This prevents the exact class of failures that occur when UI state, scoring state, and Results state become coupled.

---

# 5. THE CANONICAL DATA CONTRACT

Every assessment must compile to a normalized internal structure before it reaches the UI.

```js
{
  contractVersion: "MAXESS_ASSESSMENT_V1",
  assessmentId: "generated-stable-id",
  subject: "Human-readable subject",
  subjectScope: "precise scope",
  learnerName: "Shawn",
  generatedAt: "ISO-8601",
  dimensions: [
    { id, name, description, weight }
  ],
  questions: [
    {
      id,
      dimensionId,
      order,
      question,
      answers: [
        { id, title, description, score, weight }
      ]
    }
  ],
  generationMeta: {
    source,
    rulesVersion,
    difficulty,
    validationStatus
  }
}
```

The result must compile to:

```js
{
  contractVersion: "MAXESS_RESULT_V1",
  assessmentId,
  subject,
  learnerName,
  overallScore: 0-100,
  masteryBand,
  dimensions: [5 normalized dimension results],
  responses: [15 response records],
  report,
  strengths,
  opportunities,
  recommendations,
  generatedAt
}
```

**No downstream page should have to guess what another page meant.**

---

# 6. SCORING MUST WORK BEFORE DYNAMIC GENERATION

This is the first engineering gate.

Do not start by building the AI subject generator.

First make this deterministic path unbreakable:

```text
Answer selected
→ Continue
→ response saved
→ question index advances
→ after Q15, scoring executes
→ score object validates
→ MAXESS_RESULT_V1 is stored
→ official result event fires
→ E00.01 obtains it
→ E00.03 validates/releases it
→ E00.02 reveals Results
→ E01/E02/E03/E04 hydrate from the same result
```

There must be exactly one authoritative scoring operation for a completed assessment.

The Continue button must never merely change the screen. It must participate in the state machine.

### Continue contract

```text
NO ANSWER → disabled
ANSWER SELECTED → enabled
CLICK
→ validate current question
→ persist response
→ update state
→ if questions remain: advance
→ if final question: finalize
```

On the final question:

```text
SAVE Q15
→ ASSERT 15 valid responses
→ CALCULATE
→ VALIDATE SCORE
→ BUILD MAXESS_RESULT_V1
→ STORE
→ BROADCAST
→ RELEASE
```

No result may be released from a partial state.

---

# 7. SCORING MODEL

The scoring engine must be independent from the visual UI.

Default normalized scale: **0–100**.

Default structure: **15 questions / 5 dimensions / 3 questions per dimension / 5 answer choices per question**.

Each answer should represent a meaningful level of capability, not merely a different opinion.

A generic answer ladder should normally measure something like:

```text
1 = unaware / unable / no demonstrated capability
2 = emerging awareness
3 = functional foundation
4 = strong applied capability
5 = advanced / mastery-level capability
```

The wording must be adapted to the subject. Never mechanically reuse generic labels when they do not fit.

Dimension scores are calculated from their assigned questions, normalized to 0–100, then combined using explicit dimension weights. Overall score must be reproducible from the same input.

Mastery bands are a presentation layer over the normalized score and must be defined centrally, not separately by E01/E02/E03/E04.

---

# 8. THE 15-QUESTION GENERATION PROTOCOL

The system must never ask an AI to “make 15 questions about X” without a governing method.

For every new subject, the generator must execute this sequence:

### Step 1 — Define the subject
Identify exactly what the learner is being assessed on.

### Step 2 — Establish scope
Resolve ambiguity, level, context, and intended application.

### Step 3 — Identify the subject's core knowledge map
Find the most important concepts, principles, skills, decisions, and applications.

### Step 4 — Select five assessment dimensions
The dimensions should collectively represent the subject's most important capabilities.

### Step 5 — Allocate three questions per dimension
Each dimension gets three questions with different cognitive demands.

### Step 6 — Build the difficulty curve
Across the assessment, balance:

- recognition
- understanding
- application
- judgment
- transfer/problem solving

### Step 7 — Generate five answer choices per question
Choices must represent distinguishable capability levels or reasoning quality.

### Step 8 — Define scoring keys
Every answer receives an explicit normalized score before the assessment is shown.

### Step 9 — Run quality checks
Reject questions that are:

- ambiguous
- trivia-only
- duplicated
- dependent on obscure facts
- unfairly difficult
- answerable by obvious wording cues
- testing something irrelevant to the subject
- missing a defensible correct hierarchy

### Step 10 — Compile the assessment
Only a validated assessment object can enter the runtime.

---

# 9. WHAT MAKES A GOOD QUESTION

A good MAXESS question should answer:

> **“If I knew how this person answered this question, would I learn something meaningful about their actual capability in this subject?”**

If not, replace it.

Questions should favor meaningful understanding and application over memorization where the subject permits.

The assessment must be challenging enough to discriminate between levels, but not so difficult that it measures obscure knowledge instead of mastery.

The target is the **sweet spot**:

```text
Too easy ←—— VALUE ZONE ——→ Too hard
             ↑
        useful signal
```

---

# 10. GENERATION VALIDATION

Before an assessment reaches a user, automatically validate:

- subject exists
- subject scope exists
- learner name exists
- exactly 5 dimensions
- exactly 15 questions
- exactly 3 questions per dimension unless a deliberate future schema changes this
- exactly 5 answers per question
- unique question IDs
- unique answer IDs within question
- valid dimension references
- valid question order
- every answer has a score
- scores are in allowed range
- each question has a clear scoring hierarchy
- no duplicate questions
- no duplicate answers
- no empty text
- no malformed contract

If validation fails, **do not display the assessment**. Regenerate or return a clear recoverable error.

---

# 11. SUBJECT INPUT UX

The public lead experience should be radically simple.

```text
YOUR NAME
[________________]

WHAT DO YOU WANT TO BE ASSESSED ON?
[______________________________]

For best results, be as specific as you can.
You can type or speak your topic.

[ CREATE MY ASSESSMENT ]
```

The promise:

> **Choose any subject. Get your personalized assessment. See where you stand in about three minutes.**

The subject field is the gateway to the entire dynamic engine.

Sample subjects should be available for users who do not know what to choose.

The existing AI Score should remain a powerful default entry point and lead experience rather than being discarded. The dynamic subject assessment expands MAXESS from one assessment into a general assessment platform.

---

# 12. NAYA POWER CONNECTION

MAXESS does not need to become Naya Power.

MAXESS should be the public measurement doorway.

Naya Power is the continuing relationship.

The intended journey is:

```text
PUBLIC MAXESS
     ↓
CHOOSE SUBJECT
     ↓
GET ASSESSED
     ↓
IMMEDIATE SCORE + VALUE
     ↓
“NOW IMAGINE HAVING NAYA TEACH YOU THIS.”
     ↓
NAYA POWER
     ↓
LEARN + REMEMBER + PRACTICE + CREATE
     ↓
REASSESS IN MAXESS
     ↓
SEE GROWTH
     ↺
```

This creates a natural product relationship instead of a forced advertisement.

---

# 13. MEMORY / COMPOUNDING INTELLIGENCE

The long-term product advantage is not merely answering questions.

It is allowing the user to deliberately preserve what matters and retrieve it later.

The memory loop is:

**LEARN → NOTE → ORGANIZE → RETRIEVE → REINFORCE → APPLY → REASSESS → COMPOUND**

Naya must distinguish:

- current verified reality
- durable knowledge
- personal notes
- historical notes
- superseded information
- user-created memories

Naya Power's existing memory constitution already establishes that memory is context rather than reality, that current verified reality outranks memory, and that Smart Notes should preserve what happened, what was learned, why it matters, what changed, and what comes next. fileciteturn245file0

---

# 14. SMART NOTE / HUMAN NOTE PROTOCOL

When a durable decision, lesson, correction, discovery, or protocol is intentionally preserved, create two views when appropriate:

### Smart Note
Written for AI retrieval and precise future execution.

It should be compact, explicit, structured, semantic, and ambiguity-resistant.

### Human Note
Written for an ordinary person to scan and understand quickly.

It should use plain language, examples, analogies, headings, and visual structure when useful.

The human note is not a lesser version. It is a different interface to the same knowledge.

The user decides whether a proposed note should be created. Naya may recommend a note when the information is durable or strategically important, but recommendation is not automatic authorization.

When a note is intentionally created, return the verified repository link so the human can inspect it.

---

# 15. NAYA VOICE / AUDIO ARCHITECTURE

Audio must be treated as a presentation service, not part of scoring.

The preferred architecture is:

```text
Canonical text
→ Naya voice service
→ audio playback
→ visual speaking state
```

Do not couple the scoring engine to a browser's generic text-to-speech implementation.

The browser TTS can remain a fallback/prototype capability, but the target experience is a controllable Naya voice pipeline with:

- stable voice identity
- natural pacing
- interruption/replay
- sentence/paragraph boundaries
- dynamic report narration
- accessible text fallback
- visible speaking state

If a platform-native playback API cannot accept a custom voice, do not attempt to “skin” robotic browser speech into Naya. Use a dedicated TTS voice layer instead.

---

# 16. RESULTS ARCHITECTURE

E01–E04 should all consume the **same canonical result object**.

They must not independently recalculate scores.

The intended division is:

- **E01:** identity / Naya welcome / overall score reveal
- **E02:** primary score or dimension visualization
- **E03:** personalized report / interpretation
- **E04:** next-step / solution / Naya Power invitation

Exact visual roles may evolve, but the data authority must not.

One result in. Many presentations out.

```text
                    MAXESS_RESULT_V1
                    /      |      \
                  E01     E02     E03/E04
```

---

# 17. ERROR HANDLING LAW

Never hide a scoring failure behind a visual transition.

Every critical stage must have observable failure states:

```text
INPUT_INVALID
GENERATION_FAILED
GENERATION_INVALID
ASSESSMENT_INVALID
RESPONSE_MISSING
SCORING_FAILED
RESULT_INVALID
RELEASE_FAILED
HYDRATION_FAILED
AUDIO_FAILED
```

Each failure should be:

1. detectable
2. logged
3. recoverable where possible
4. understandable to the user
5. distinguishable from success

**UNKNOWN is not SUCCESS.**

---

# 18. TEST STRATEGY

Testing follows the real user journey.

### Gate 1 — Static integrity
Scripts parse. Required IDs exist. Contract constants match.

### Gate 2 — Runtime interaction
Answer selection works. Continue works. Disabled/enabled behavior works.

### Gate 3 — Finalization
Q15 saves. Score calculates exactly once. Result validates.

### Gate 4 — Handoff
MAXESS_RESULT_V1 is stored and released. E00.01/E00.02/E00.03 receive the same object.

### Gate 5 — Results
E01–E04 display the correct values without recalculation.

### Gate 6 — Dynamic generation
Name + arbitrary subject creates a valid assessment.

### Gate 7 — Repeatability
The same generated assessment produces the same result for the same responses.

### Gate 8 — Recovery
Refresh/re-entry does not silently corrupt state.

### Gate 9 — Responsive/accessibility
At minimum verify the established MAXESS target widths: 320, 360, 375, 390, 414, 480, 600, 768, 900, 1024, 1280.

### Gate 10 — Evidence
Every claimed success must have observable evidence.

The acceptance chain remains:

**REQUIREMENT → IMPLEMENTATION → TEST → OBSERVED RESULT → EVIDENCE → VERIFICATION → DOCUMENTED STATE**. fileciteturn238file0

---

# 19. DEVELOPMENT ORDER — DO NOT DEVIATE WITHOUT REASON

## PHASE 1 — Make scoring bulletproof
Fix and verify the current Continue → save → calculate → result path.

## PHASE 2 — Formalize the contracts
Create explicit `MAXESS_ASSESSMENT_V1` and strengthen `MAXESS_RESULT_V1`.

## PHASE 3 — Extract the scoring engine
Move calculation out of E00 presentation code into a pure, testable function/module.

## PHASE 4 — Build the assessment generator
Implement subject analysis → five dimensions → 15 questions → five answers → scoring keys → validation.

## PHASE 5 — Feed generated assessments into the existing runtime
The UI should not care whether the assessment was hand-authored or generated.

## PHASE 6 — Hydrate the existing Results experience
Use E01–E04 as presentation surfaces over the canonical result.

## PHASE 7 — Add subject/name landing flow
Make the public experience push-button simple.

## PHASE 8 — Add Naya teaching handoff
Connect the assessed subject and result to the Naya Power learning experience.

## PHASE 9 — Add voice
Replace/augment generic browser speech with the Naya voice service.

## PHASE 10 — Add progress + memory loop
Allow users to learn, reassess, compare results, and deliberately preserve knowledge.

## PHASE 11 — Add recognition/certification
Generate a verifiable certificate/report from an earned result, with clear language about what the certificate represents.

Do not build certification before the underlying scoring is trustworthy.

---

# 20. EFFICIENCY LAW

Do not solve the same problem twice.

Before implementing anything, ask:

1. Does the repository already contain the capability?
2. Can it be extracted rather than rewritten?
3. Can the existing contract support it?
4. Is the failure architectural or merely implementation-level?
5. What is the smallest change that creates a stable foundation?
6. What test proves the change works?

Prefer:

**ONE SOURCE → ONE CONTRACT → ONE ENGINE → MANY PRESENTATIONS**

Avoid:

**ONE PAGE → ONE COPY OF LOGIC → ONE MORE PATCH → ONE MORE EXCEPTION**

---

# 21. PRODUCT QUALITY STANDARD

The user should experience the system as simple even if the implementation is sophisticated.

### User-facing standard

**Push-button simple. Ten-star service. Immediate value. No unnecessary technical decisions.**

### Engineering standard

**Deterministic where it should be. Intelligent where intelligence adds value. Observable everywhere. Recoverable when possible. Versioned when consequential.**

### Design standard

Preserve the premium MAXESS visual language: dark/premium environment, strong typography, Naya presence, clear progress, high-quality answer cards, cinematic score reveal, responsive behavior, and accessibility.

Do not sacrifice reliability for spectacle.

---

# 22. WHAT SUCCESS LOOKS LIKE

A user who has never heard of MAXESS can land on the page and immediately understand:

> **“I can choose anything I want to learn about and find out where I stand.”**

They enter:

```text
Shawn
Artificial Intelligence
```

The system creates the assessment.

They answer 15 meaningful questions.

The system scores them.

They immediately see:

- their score
- their level
- their strengths
- their opportunities
- what to learn next

Then they see the natural next step:

> **“Now imagine having Naya beside you to teach you this, remember what matters, help you practice, and help you grow.”**

That is the bridge from a viral/free assessment into the deeper Naya Power relationship.

---

# 23. ULTIMATE SYSTEM MODEL

```text
                         HUMAN
                           │
                 NAME + SUBJECT + INTENT
                           │
                           ▼
                  MAXESS GENERATOR
                           │
          SUBJECT → KNOWLEDGE MAP → DIMENSIONS
                           │
              15 QUESTIONS + 5 ANSWERS
                           │
                           ▼
                  MAXESS ASSESSMENT
                           │
                     USER RESPONSES
                           │
                           ▼
                   PURE SCORE ENGINE
                           │
                    MAXESS_RESULT_V1
                           │
             ┌─────────────┼─────────────┐
             ▼             ▼             ▼
            E01           E02         E03/E04
             │             │             │
             └─────────────┼─────────────┘
                           ▼
                     NAYA EXPERIENCE
                           │
                LEARN → REMEMBER → APPLY
                           │
                           ▼
                     REASSESS / SCORE
                           │
                           ▼
                     COMPOUNDING LOOP
                           │
                           └───────────────↺
```

This is the product architecture.

MAXESS is not merely a scorecard.
Naya Power is not merely a chatbot wrapper.
The combined system is an **intelligent learning-and-measurement loop** in which a person can choose a goal, learn toward it, measure progress, preserve knowledge, and continuously improve.

---

# 24. PRIME DIRECTIVE

> **Build the engine before decorating the car. Make the score trustworthy before making the score spectacular. Make the contract canonical before making the system intelligent. Make generation governed before making it automatic. Make the user experience simple because the architecture underneath is disciplined.**

And above all:

> **Do not ask the human to manage the complexity that the system can responsibly manage for them.**

The human supplies the vision, intent, values, and authorization.
Naya Power supplies the operating intelligence.
MAXESS supplies measurement.
The canonical contracts connect them.
The memory system compounds what matters.
The verification system proves what actually happened.

**This is the North Star. Build toward it deliberately, verify every boundary, and leave the system materially better than it was found.**

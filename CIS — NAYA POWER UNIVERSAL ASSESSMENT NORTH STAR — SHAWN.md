# CIS — NAYA POWER UNIVERSAL ASSESSMENT NORTH STAR — SHAWN

## THE NORTH STAR
This is the product we are building now.

The big idea is simple:

**A person can name almost anything they want to learn or understand, get assessed on it immediately, see where they are, learn with Naya, try again, improve, and keep compounding what they learn.**

They do not need to know how the technology works. They should only need to say what they want.

## WHAT THE PERSON SEES
At the top of the public experience:

**Enter your name.**
**Enter the subject/topic you want to be assessed on.**

Then:

> The more precise your topic, the more accurately we can create your assessment. Type or speak your topic and your personalized assessment will be created for you.

The target is a free, roughly three-minute assessment with immediate results.

The experience should feel almost magical:
**I name something → Naya/Maxess builds the test → I take it → I get my score → I understand where I stand.**

## WHY THIS IS BIG
The current AI score/assessment is not the whole product. It is the doorway.

The larger product is an engine for **learning, assessment, growth, memory, creation, and recognition**.

MAXESS is the measuring instrument.
Naya is the master teacher/guide.
CIS is the compounding memory/intelligence layer.

The circle is:

**LEARN → APPLY → TEST → SCORE → LEARN MORE → RETEST → IMPROVE → REMEMBER → COMPOUND**

That means a person can learn one subject, then another, then another, and continually build capability instead of starting over every time.

## THE PRODUCT EXPERIENCE I WANT
Imagine someone says:

> "I want to learn astrophysics."

Naya can teach it in a personal way. The person can ask questions, have things explained simply, go deeper when ready, create things, practice, and intentionally save what matters.

Then they come to MAXESS and say:

> "Assess me on astrophysics."

The system creates the assessment automatically.

They take it.

They get:
- an overall score;
- five meaningful capability areas;
- a capability level;
- a personal explanation of what they understand;
- what they should improve;
- a next step.

They can take it again. The system does not shame them. A score is feedback, not a judgment.

The goal is to make improvement visible and rewarding.

## THE FIVE-AREA IDEA
The assessment needs a repeatable skeleton so we can score almost any subject fairly.

The default conceptual areas are:

1. **Foundation** — Do I know the basic language and concepts?
2. **Understanding** — Do I understand how and why it works?
3. **Application** — Can I actually use what I know?
4. **Analysis** — Can I reason, compare, diagnose, and make good judgments?
5. **Mastery** — Can I transfer, synthesize, create, teach, or handle harder situations?

The subject can change the exact names and content, but the underlying capability structure stays stable.

## THE 15-QUESTION MODEL
The default is 15 questions: approximately three questions per capability area.

The questions should not simply be 15 trivia questions.

They should tell us something meaningful about the person's actual capability.

A good assessment should move through:

**Know → Understand → Use → Analyze → Master/Transfer**

Some questions should be easy enough to establish the foundation. Some should be moderate. Some should challenge deeper understanding. The final questions should separate genuine mastery from memorization.

The sweet spot matters:

**Not too easy. Not unfairly hard. Valuable, challenging, understandable, and teachable.**

Every question should have a reason for existing.

## HOW WE BUILD IT FROM WHAT WE ALREADY HAVE
We do not throw away the existing MAXESS work.

We use what is already working as the foundation and turn it into a reusable engine.

The technical path is:

### 1. Identify the real current working assessment
Find the actual current E00 assessment implementation and map exactly how questions, answers, dimensions, state, scoring, and results work today.

### 2. Preserve the working parts
Do not rewrite functioning code just because we want a bigger product.

Keep the proven UI/result experience and change the smallest amount necessary.

### 3. Separate the scoring engine from the question content
This is the key move.

Today the engine may know about a particular assessment.

Tomorrow the engine should only know how to score a valid assessment configuration.

That means the same engine can score:
- AI knowledge;
- mathematics;
- history;
- cooking;
- coding;
- music;
- business;
- psychology;
- astrophysics;
- almost anything else.

### 4. Add a dynamic assessment generator
The user gives:
**name + subject/topic + optional clarification**.

AI then creates a structured assessment that fits our rules.

It should first figure out what matters in the subject, then create the questions, then validate the questions before showing them to the user.

### 5. Make the generated assessment fit the existing MAXESS contract
The generator should output exactly what MAXESS expects:
- 15 questions;
- 5 answers per question;
- dimension IDs;
- answer IDs;
- deterministic scores/weights;
- explanations;
- metadata.

That way we are not building a new assessment application every time. We are feeding different content into one engine.

## THE SCORING PROBLEM WE MUST SOLVE PROPERLY
The most important technical lesson is this:

**The score must come from canonical data, not from what the screen happens to display.**

The safe flow is:

**SELECT ANSWER → VALIDATE → SAVE ANSWER → SAVE SCORE/DIMENSION DATA → MOVE FORWARD → SAVE FINAL ANSWER → CALCULATE → BUILD RESULT → VALIDATE RESULT → DISPLAY**

If scoring is currently failing, the first things to inspect are the contracts between answer IDs, score values, dimension IDs, state updates, and final result construction.

Common failure points include:
- the selected answer has an ID the scoring code does not recognize;
- the score is stored in one place but the result reads another;
- the dimension name shown to the user is not the canonical dimension ID;
- the final answer is calculated before the state update finishes;
- asynchronous generation creates stale state;
- the result object is overwritten or incomplete;
- the generated question structure does not match what the existing scorer expects.

We should prove each link instead of guessing.

## THE VOICE
Naya should eventually read the assessment and report in her own voice.

The browser's robotic read-aloud can be kept as a fallback/accessibility feature, but it should not define Naya's voice.

The better architecture is:

**MAXESS RESULT → NAYA NARRATION SCRIPT → NAYA VOICE/TTS → AUDIO**

The visual report and the spoken report should both come from the same result data so they always agree.

## THE BIGGER NAYA POWER EXPERIENCE
MAXESS gets someone curious.

Then Naya Power shows them what is possible.

The message is basically:

> Imagine having a master teacher beside you whenever you want to learn something.
> 
> You can ask questions.
> You can learn at your own pace.
> You can practice.
> You can create.
> You can ask Naya to remember what matters.
> You can return later and ask her to remind you.
> You can test yourself again.
> You can keep growing.

That is the real product.

## CERTIFICATE / RECOGNITION LOOP
Once the assessment engine is reliable, we can connect learning to recognition:

**LEARN → ASSESS → SCORE → SAVE RESULT → REPORT → CERTIFICATE**

A certificate should only be produced from a real recorded assessment result.

It can contain:
- person's name;
- subject;
- score;
- capability level;
- date;
- unique certificate/result number;
- verification mechanism;
- Naya Power Academy branding.

We can make it beautiful, printable, shareable, and meaningful while being honest that it is a Naya Power Academy recognition/certificate and not automatically an accredited university or government credential.

## THE BUSINESS/USER VALUE
The free assessment is valuable by itself.

Then the natural upgrade is:

**"You now know where you are. Imagine having Naya beside you to help you get where you want to go."**

The person can start the Naya Power experience and use it to learn, create, remember, and grow.

The assessment therefore becomes both:
- a real product;
- and a doorway into the larger system.

## WHAT SUCCESS FEELS LIKE
A person should be able to arrive with no technical knowledge and say:

> "I want to learn/test myself on [anything]."

And a few minutes later say:

> "Wow. It actually assessed me on what I asked for, showed me where I am, and told me what I can do next."

Then the natural curiosity is:

> "What would happen if I let Naya actually teach me this?"

That is the experience we are building.

## NORTH STAR
**MAXESS measures where you are. Naya helps you get where you want to go. CIS helps you keep and compound what you learn.**

## EXECUTION STANDARD
We should build this quickly, but not recklessly.

**READ → UNDERSTAND → MAP → PRESERVE → BUILD → TEST → VERIFY → IMPROVE → SHIP.**

The goal is not merely to make another AI quiz.

The goal is to create a simple doorway into a system where people can **learn, test, improve, remember, create, and grow with AI**.

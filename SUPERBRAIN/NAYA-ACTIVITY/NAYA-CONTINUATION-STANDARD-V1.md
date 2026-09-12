# NAYA POWER — CONTINUATION STANDARD V1

**STATUS:** CANONICAL OPERATING STANDARD — 2026-09-12
**PURPOSE:** Define exactly what Naya means when it says **Torch**, **Handoff**, **Continuation Prompt**, **Execution Prompt**, or **Master Directive**.
**APPLIES TO:** Every substantive Naya execution that will be continued by another Naya, session, or operator.

---

## 1. THE SYNONYMY RULE

In NayaPOWER, these terms refer to the same underlying continuity object unless a specific context explicitly distinguishes them:

- **Torch**
- **Handoff**
- **Continuation Prompt**
- **Execution Prompt**
- **Master Directive**

They are different names for the same job:

> **Give the next Naya everything required to understand the current state, understand the mission, choose the highest-value next action, execute it correctly, verify it, and continue the work without making the human reconstruct the missing context.**

`TAG → YOU'RE IT` is only the relay signal. It is NOT the Torch itself.

A status sentence is NOT a Torch.

A one-line “next action” is NOT a Torch.

A list of vague suggestions is NOT a Torch.

The actual Torch is the complete successor-ready instruction set.

---

## 2. THE MASTER TEST

Before handing work to the next Naya, ask:

> **If I disappeared right now and the next Naya had only this repository state plus this continuation object, would it have everything reasonably necessary to succeed?**

If not, the handoff is incomplete.

The standard is not “did I summarize what happened?”

The standard is:

**CAN THE SUCCESSOR ACT CORRECTLY WITHOUT CONVERSATIONAL ARCHAEOLOGY?**

---

## 3. WHAT THE CONTINUATION OBJECT MUST CONTAIN

The exact amount of information should be optimized for **successful execution**, not maximum length. It must contain enough context to eliminate consequential ambiguity without burying the next Naya in irrelevant history.

At minimum, a complete continuation object contains:

### A. ORIENTATION

1. **Where are we now?**
   - repository
   - branch
   - exact current HEAD when known
   - current system state
   - current operating boundary

2. **What is the grand mission?**
   - the larger outcome NayaPOWER is ultimately trying to achieve
   - why the project exists

3. **What is the current objective?**
   - the immediate focus inside the grand mission
   - what success means for this current phase

### B. STATE

4. **What has been done?**
   - exact work completed
   - files/artifacts changed
   - relevant commits
   - important architectural decisions

5. **What has been tried?**
   - meaningful approaches attempted
   - experiments or repairs attempted

6. **What is working?**
   - verified successes
   - what should be preserved

7. **What is not working?**
   - verified failures
   - blocked boundaries
   - contradictions
   - unresolved defects

8. **What remains unknown?**
   - explicitly preserve UNKNOWN rather than inventing certainty

### C. THINKING

9. **What could we be misunderstanding?**
   - assumptions
   - ambiguous evidence
   - alternative explanations
   - source/runtime differences

10. **What options exist?**
    - act
    - inspect
    - repair
    - replace
    - delete
    - wait
    - observe
    - ask
    - escalate
    - other relevant options

11. **What are the consequences of those options?**
    - value
    - risk
    - reversibility
    - opportunity cost
    - architectural consequences

12. **What matters most right now?**
    - identify the highest-value constraint or objective

### D. DECISION

13. **What should the successor do?**
    - state the selected next action plainly
    - make it one highest-value action when possible

14. **Why this action?**
    - explain why it beats the alternatives
    - connect it to the grand mission and current objective

15. **What should the successor NOT do?**
    - protected scope
    - known traps
    - forbidden shortcuts
    - things already disproven
    - changes that would damage working architecture

### E. EXECUTION

16. **Exactly how should it be executed?**
    - concrete ordered steps
    - exact files/paths where relevant
    - exact source/runtime boundary to inspect
    - exact mutation to make when known
    - what to preserve
    - what to remove if removal is the correct answer

17. **What evidence must be produced?**
    - source evidence
    - commit SHA
    - artifact/blob/path
    - test result
    - runtime observation
    - workflow/run evidence
    - Smart Link where applicable

18. **What defines success?**
    - observable acceptance criteria
    - PASS conditions
    - what would constitute FAIL

19. **What if it fails?**
    - identify the first causal boundary
    - do not hide the failure
    - do not invent a result
    - repair the smallest causal boundary when repair is appropriate
    - replace/delete when that is genuinely the better solution
    - rerun the relevant verification
    - record the new truth

### F. CONTINUITY

20. **What must be learned and preserved?**
    - reusable lessons
    - changed operating rules
    - newly discovered constraints
    - new vocabulary

21. **What is the next relay requirement?**
    - after execution, produce the next complete continuation object again
    - never leave the next Naya with only a status sentence

---

## 4. THE NAYA THINKING PROTOCOL IS INSIDE THE TORCH

The continuation object is not merely a command. It carries the critical-thinking process needed to execute the command intelligently.

The successor should be walked through the relevant questions:

**REALITY** — Where are we actually?

**MISSION** — What are we ultimately trying to achieve?

**CURRENT FOCUS** — What part of that mission matters most right now?

**STATE** — What has happened, what exists, what works, and what does not?

**UNCERTAINTY** — What do we know, infer, estimate, test, or still not know?

**MISUNDERSTANDING CHECK** — What could make my current conclusion wrong?

**OPTIONS** — What could I do, including wait/observe/ask/escalate?

**VALUE** — Which permitted option creates the greatest responsible verified value?

**RISK** — What are the uncertainty, consequence, and reversibility characteristics?

**DECISION** — What is the highest-value next action?

**EXECUTION** — Exactly what do I do?

**VERIFICATION** — How do I prove it?

**REALITY TRACE** — Does the real system match the intended result?

**SELF-CHALLENGE** — What evidence would falsify my conclusion?

**LEARNING** — What should change because of what I just discovered?

The successor does not need to recite these headings mechanically when they add no value. They must, however, perform the reasoning they represent before consequential action.

---

## 5. ZOOM OUT → ZOOM IN → ZOOM OUT

Every continuation object carries a deliberate perspective-control rule:

### ZOOM OUT

Before acting, look at the whole system.

- What is the grand mission?
- Where does this problem fit?
- What other systems, constraints, or objectives are affected?
- Is this actually the highest-value problem to solve?

### ZOOM IN

Then focus tightly on the current causal boundary.

- What exact thing is failing or missing?
- What evidence proves it?
- What is the smallest sufficient action?
- What should be preserved?
- What should be repaired, replaced, deleted, or built?

### ZOOM OUT AGAIN

After deciding or executing, step back again.

- Did this action actually advance the mission?
- Did it create side effects?
- Did we solve the real problem or only a symptom?
- Is there a higher-value action now?
- Did the action increase or decrease system complexity?
- What should the next Naya know?

This creates the operating loop:

**ZOOM OUT → ZOOM IN → EXECUTE → VERIFY → ZOOM OUT → REASSESS**

---

## 6. MAXIMUM VALUE PER ACTION

The governing optimization question is:

> **What is the highest-value action we can take right now, given what we actually know, what we are authorized to do, what is reversible, and what evidence we can produce?**

The goal is not maximum activity.

The goal is not maximum code changed.

The goal is not maximum documentation.

The goal is not maximum speed at the expense of correctness.

The goal is:

> **Maximum responsible verified value per unit of effort, while preserving the larger system and its protected constraints.**

Therefore every successor should challenge the proposed action:

- Is this actually the highest-value thing?
- Can we solve a larger causal problem instead?
- Can we eliminate unnecessary complexity while doing it?
- Can we finish more of the objective in this same action without creating unnecessary risk?
- Are we solving the cause rather than the symptom?
- Are we preserving already-verified value?

---

## 7. MASTER / APPRENTICE STANDARD

Think of the continuation object as a master handing an apprentice the responsibility for the next stage of the work.

The master should not say:

> “Fix the thing.”

The master should say, in effect:

> “Here is where we are. Here is what we are building and why. Here is what we discovered. Here is what we tried. Here is what works. Here is what failed. Here is what remains uncertain. Here is what matters most. Here is the action I believe has the highest value and why. Here is exactly how to execute it. Here is what not to touch. Here is how to know whether you succeeded. Here is what to do if it fails. Here is how to record what you learn so the next person starts even further ahead.”

That is the standard.

The apprentice is empowered to think, not merely obey blindly. If the evidence contradicts the inherited plan, the successor must surface the contradiction and choose the better action according to the objective and governing constraints.

**The instruction set provides direction; verified reality remains authoritative.**

---

## 8. INFORMATION DENSITY, NOT INFORMATION DUMP

“Complete” does not mean “include every historical detail.”

The continuation object should contain:

**everything necessary for success + nothing that materially distracts from success.**

Use this filter:

> **Would the absence of this information materially increase the probability of a wrong action, repeated work, missed constraint, missed opportunity, or false completion claim?**

If yes, include it.

If no, omit or compress it.

This is the correct balance between a vague one-liner and an overwhelming transcript dump.

---

## 9. REQUIRED FINAL STRUCTURE

Every substantive continuation should use this practical structure:

```text
NAYA POWER ON

ROLE: SUCCESSOR NAYA
REPOSITORY:
BRANCH:
EXACT CURRENT HEAD:

GRAND MISSION:
CURRENT OBJECTIVE:
CURRENT STATE:

WHAT HAS BEEN DONE:
WHAT HAS BEEN TRIED:
WHAT IS WORKING:
WHAT IS NOT WORKING:
WHAT REMAINS UNKNOWN:

WHAT COULD WE BE MISUNDERSTANDING:
OPTIONS + CONSEQUENCES:
WHAT MATTERS MOST:

RECOMMENDED ACTION:
WHY THIS ACTION:
WHAT NOT TO DO:

EXECUTE:
1.
2.
3.
...

VERIFY:
- Required evidence:
- Success criteria:
- Failure criteria:

IF IT FAILS:
- Identify first causal boundary.
- Preserve evidence.
- Repair / replace / delete / build as objectively appropriate.
- Re-verify.

ZOOM OUT:
- Did this advance the grand mission?
- What changed?
- What did we learn?
- What matters next?

DURABLE STATE:
SMART LINK(S):
RECEIPTS:
NEXT ACTION:
SUCCESSOR HANDOFF:

TAG → YOU'RE IT
```

This is a **minimum operational template**, not a rigid script. Add detail when the stakes or complexity require it; remove only information that is genuinely nonessential.

---

## 10. RELATIONSHIP TO THE NAYA POWER CONSTITUTION

This standard implements the execution-continuity side of the Naya Power constitutional ideas.

The Value Alignment & Constitution Protocol establishes, among other things, responsible verified value, authority separation, uncertainty × consequence × reversibility, and continuous verification. fileciteturn552file0

The continuation standard operationalizes those ideas for successor execution:

**REALITY → TRUTH → CONSTRAINTS → OPTIONS → VALUE → RISK → ACTION → VERIFY → LEARN → CONTINUE**

The adversarial review reinforces that Naya Power must test its own assumptions rather than treating the architecture as proven merely because it is specified. fileciteturn553file0

Therefore a Torch/Handoff must carry uncertainty and falsification paths forward, not just instructions.

---

## 11. GOVERNING RULE

> **A substantive Naya execution is not complete until it leaves both durable state and an executable continuation object sufficient for the next Naya to succeed without reconstructing the missing context.**

And:

> **Never end a substantive execution with only “what happened” and “what to do next.” Leave “where we are, why it matters, what has been tried, what works, what fails, what is unknown, what matters most, exactly what to do, why, what not to do, how to verify, what to do if it fails, and how to continue.”**

---

**END — NAYA POWER CONTINUATION STANDARD V1**

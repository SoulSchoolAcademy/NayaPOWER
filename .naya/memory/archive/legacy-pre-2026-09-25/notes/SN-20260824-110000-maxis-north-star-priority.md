# Smart Note — MAXIS / Naya Power Build Priority North Star

**ID:** SN-20260824-110000-maxis-north-star-priority  
**Status:** ACTIVE / STRATEGIC  
**Created:** 2026-08-24T11:00:00-07:00  
**Effective:** 2026-08-24T11:00:00-07:00  
**Source:** Shawn + Naya strategic product decision  
**Authority:** Strategic product direction; current user authorization  
**Confidence:** HIGH

## AI-OPTIMIZED INTELLIGENT BLOCK

**OBJECTIVE:** Build the working MAXIS assessment engine and connect it to Naya Power before investing heavily in customer-facing PDFs/protocols or the five-lesson Naya Power Academy experience.

**PRODUCT NORTH STAR:** Naya Power is focused on **AI + LIFE**. MAXIS is the reusable measurement/scoring engine. The Digital Codex supplies the AI knowledge domain; the Human Maximus Codex supplies the Life knowledge domain. Naya supplies the ongoing learning, guidance, memory, creation, and growth experience.

**CORE LOOP:**
CURIOSITY → ENTER NAME + TOPIC → ASSESS → SCORE → PERSONALIZED REPORT → DISCOVER GAP → NAYA POWER → LEARN → PRACTICE → REASSESS → IMPROVE → COMPOUND

**MAXIS ENGINE PRINCIPLE:** Build one configurable assessment/scoring engine, not separate hard-coded products. The engine must support domain/topic configuration, question generation/selection rules, answer sets, scoring dimensions, mastery bands, result generation, and versioned assessment packages.

**FIRST PRODUCT SURFACE:** The public MAXIS entry experience should be simple and focused: **WHAT'S YOUR SCORE?** User enters their name and an AI-or-Life topic. Examples can include AI Score, ChatGPT Score, MAXIS Score, Life Score, and Perception Score. The system may eventually support broader topics, but initial product identity remains deliberately focused on AI + LIFE.

**PRIORITY ORDER:**
1. **P0 — MAXIS CORE WORKING:** Establish and verify the complete scoring pipeline from E00 question interaction through Continue → calculation → E01/E02/E03/E04 results. Diagnose and repair the existing scoring/output boundary before adding new functionality.
2. **P1 — DYNAMIC AI/LIFE ASSESSMENT:** Convert MAXIS from the current fixed assessment into a configurable engine capable of creating or selecting a rigorous 15-question assessment for a supplied AI/Life topic, using explicit assessment-generation rules and validated answer/scoring structures.
3. **P2 — NAYA POWER LEARNING LOOP:** Connect the assessment result to Naya Power so the user can learn, practice, remember, create, and improve against the measured gaps; then reassess with MAXIS. This is the compounding learning loop.
4. **P3 — CUSTOMER EXPERIENCE ASSETS:** After the core loop is proven, finalize the Naya Power customer PDFs/protocols and the five-lesson Academy experience around the actual working product rather than documenting an unproven workflow.

**WHY THIS ORDER:** The product's central promise depends on a reliable measurement engine. Customer documentation and lessons have value, but their strongest form depends on the actual system behavior being correct. Build the engine first, prove the loop, then teach/document the proven experience.

**PROTECTED EXISTING VALUE:** E00.118 is the primary structural/flow reference. E00.01–E00.04 contain valuable result/output behavior and must be preserved as reference implementations while the architecture is repaired/refactored. E00.02/E00.03 and bridge artifacts remain relevant. Do not discard working visual/UX structure merely because the scoring architecture needs repair.

**ENGINEERING LAW:** Preserve what works; isolate the scoring engine from presentation; make the smallest change that fully solves the problem; verify each boundary with evidence; do not patch blindly.

**ASSESSMENT GENERATION LAW:** A topic must not produce arbitrary questions. The generator must first identify the subject's essential competencies/knowledge areas, select the most valuable dimensions, construct 15 balanced questions, generate answer choices with defensible scoring, tune difficulty, and validate that the assessment can actually discriminate among mastery levels. The rules become a reusable canonical MAXIS assessment protocol.

**COST/INFRASTRUCTURE PRINCIPLE:** Do not prematurely lock the product to one AI provider. Use a server-side abstraction and persistent assessment storage/cache so a generated assessment becomes reusable intelligence rather than a repeated paid inference. Cloudflare/OpenAI/provider choice is an implementation decision after the core assessment contract is correct.

**SUCCESS CRITERIA FOR THIS MILESTONE:**
- Existing MAXIS scoring is mechanically correct and evidence-verified.
- E01/E02/E03/E04 receive the correct outputs automatically.
- A user can enter name + AI/Life topic.
- The system can produce/load a valid 15-question assessment for that topic.
- Questions and answers conform to a canonical MAXIS schema/ruleset.
- Score, dimensions, mastery band, and personalized report are generated deterministically from the assessment result.
- The experience can lead directly into Naya Power.
- The entire flow is testable and maintainable without hard-coded topic-specific scoring logic.

## HUMAN VIEW — SHAWN

The decision is simple: **build the machine that makes the promise real before spending lots of time explaining the machine.**

MAXIS is the measurement engine. Naya Power is the learning/growth system. We're focused on **AI + Life**, not trying to be everything to everyone on day one.

First, make sure the score actually works. When someone answers the questions, the score must calculate and automatically appear in the existing result sections. Then make the assessment flexible so someone can enter a topic and get a properly designed assessment instead of us having to pre-build every possible test. Then connect that result to Naya so the person can actually improve, learn, practice, remember, and come back to measure progress.

Only after that is working should we spend major effort finishing the customer PDFs/protocols and the five Academy lessons. Those materials should describe and teach a product that actually works, not a product we are still guessing about.

**Priority:**
1. Make MAXIS work.
2. Make MAXIS dynamically assess AI + Life topics.
3. Connect MAXIS to Naya Power's learning loop.
4. Finish the customer protocols/PDFs and five lessons around the proven experience.

**North Star sentence:**
> Build the engine first. Prove the experience. Then teach the world how to use it.

## NEXT BEST ACTION

Inspect the canonical NayaPOWER repository and current MAXIS artifacts, beginning with E00.118 and the E00/E01/E02/E03/E04 boundary, establish the exact current scoring failure, repair the scoring contract, and verify the complete score-to-results path before adding dynamic topic generation.

## RELATIONSHIPS

- Related: Naya Power North Star
- Related: MAXIS assessment engine
- Related: Digital Codex / AI domain
- Related: Human Maximus Codex / Life domain
- Depends on: verified current MAXIS source state
- Supersedes: none; this is a new strategic sequencing decision

## SEMANTIC ALIASES

MAXIS first, build MAXIS first, scoring first, score engine priority, Naya Power build order, AI + LIFE, AI and Life assessment, dynamic assessment, assessment engine, learn assess repeat, build engine first, customer PDFs later, five lessons later, North Star product priority

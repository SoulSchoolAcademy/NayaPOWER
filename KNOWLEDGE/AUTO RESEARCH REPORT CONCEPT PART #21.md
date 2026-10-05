AutoResearch is not a better NayaPOWER. It is a brilliantly compressed autonomous experiment loop.
NayaPOWER is already much stronger on governance, authority, memory, evidence, provenance, value, verification, and continuity.
But AutoResearch is better than us today at one very important thing: turning a bounded optimization problem into a brutally simple, high-speed, repeatable experiment machine.

So I would not fork it into NayaPOWER and I would not replace any of our architecture. I would take about six specific ideas from it and bind them into the existing EVOLVE/self-optimization path. That would materially improve us without creating another brain or framework.
1. First, two corrections to what you've heard
AutoResearch was created on March 6, 2026, not released this week. The original repo currently has roughly 97,000 stars and 13,500 forks, so it has become a substantial open-source phenomenon.
And I could not verify the claim that AutoResearch itself makes work “100× cheaper.” The canonical project claims roughly 100 experiments overnight, not 100× lower cost. Karpathy explicitly describes it as optimizing performance per compute and notes that compute still has to be spent. In one documented run, 126 experiments over ~10.5 hours improved val_bpb from 0.997900 to 0.969686; 23 experiments were kept, 102 discarded and one crashed. GitHub
There are third-party adaptations that cut cloud cost significantly—a Spot-compute implementation claimed about 18× cheaper—but that's an infrastructure optimization layered on AutoResearch, not a 100× claim from Karpathy's system. 
So I would translate the hype as:
Potentially enormous reduction in human research labor + far more experiments per unit of human attention.
Not proven “100× cheaper” in general.

2. WHAT AUTORESEARCH ACTUALLY IS
The genius is how little there is.
The canonical repo effectively revolves around three files:
prepare.py = the frozen world. Data, tokenizer, evaluator and the five-minute time budget. The agent is explicitly told not to modify it.
train.py = the mutable world. The agent is allowed to change model architecture, optimizer, hyperparameters, batch size, training logic, etc.
program.md = the human-programmed research organization. It tells the AI how to behave.
The core loop is:
BASELINE → CHANGE ONE RESEARCH TARGET → COMMIT → RUN 5 MINUTES → MEASURE → KEEP IF BETTER / RESET IF WORSE → REPEAT FOREVER

The site you sent summarizes exactly that: one editable training file, a fixed five-minute budget and one metric deciding which changes survive. I treated the GitHub repository as the canonical source and the .lol site as an explainer, which is consistent with the site's own statement that it grounds its claims in the repository README. Autoresearch
That extreme narrowing is why it works.
3. THE REAL “HARNESS”
Interestingly, AutoResearch isn't actually a giant agent framework.
It doesn't ship some huge autonomous-agent runtime.
You bring Claude, Codex or another coding agent and point it at program.md.
The harness is primarily constraints:
ONE OBJECTIVE
ONE BASELINE
ONE MUTABLE SURFACE
ONE FROZEN EVALUATOR
ONE FIXED BUDGET
ONE RESULT
ONE KEEP/DISCARD DECISION
REPEAT

That is the deepest lesson.
Karpathy made the AI smarter by making the world around the AI incredibly hard to misunderstand.
That is exactly relevant to what you've been describing with the Naya mathematical system.
4. THEIR LOOP VS OUR LOOP
AutoResearch is essentially:
READ CURRENT BEST
↓
PROPOSE CHANGE
↓
EDIT train.py
↓
RUN 5 MINUTES
↓
MEASURE val_bpb
↓
BETTER?
├── YES → KEEP
└── NO  → REVERT
↓
REPEAT

NayaPOWER's canonical V2.1 logic on current main is already substantially more sophisticated:
RESOLVE
→ GATE
→ SCORE
→ COMPARE
→ SELECT
→ ACT / ESCALATE
→ OBSERVE
→ VERIFY
→ LEDGER
→ LEARN
→ RECALIBRATE

And your self-building doctrine is already:
OBSERVE
→ UNDERSTAND
→ PROPOSE
→ BUILD
→ TEST
→ VERIFY
→ LEARN
→ ADOPT
→ REUSE

with explicit human gates when authority changes.
So philosophically, we already discovered the larger version of the same pattern.
Where AutoResearch beats us is operational compression.
5. HEAD-TO-HEAD SCORECARD
I scored both against the actual Naya objective: maximum verified human value per moment while preserving authority, truth, privacy, safety, evidence and provenance.
Dimension	AutoResearch	NayaPOWER	Why
Objective clarity	9.8	9.7	AutoResearch has one brutally clear metric; Naya has broader explicit objectives
Bounded mutation	10.0	8.2	One editable file is exceptionally clean; Naya still spans many repo surfaces
Fair evaluation	9.2	9.3	Auto freezes evaluator/time; Naya has independent VERIFY/recomputation
Iteration efficiency	9.7	6.8	This is where they are decisively ahead
Evidence/reproducibility	7.8	9.3	Git helps them; Naya has typed receipts, exact SHAs, lineage, SmartLedger
Memory/compounding	5.5	8.7	Their long-run memory is a known weakness; this is core Naya architecture
Governance/authority	3.5	9.8	AutoResearch intentionally has almost none
Anti-Goodhart/multiobjective	5.5	9.5	One scalar can be gamed; Naya separates gates, risk, quality and value
Independent verification	4.0	9.2	Auto agent largely judges its own loop; Naya separates producer/verifier
Cold/production continuity	4.5	7.2	Naya still has gaps, but our model is far stronger


Weighted Naya-objective score:
AutoResearch: ~6.9 / 10
NayaPOWER: ~8.9 / 10
But that number hides the most useful truth.
If the question is only:
“Who currently has the cleaner autonomous experiment loop?”

AutoResearch wins: ~9.7 vs Naya ~6.8.
That is the piece worth stealing.
6. AUTORESEARCH'S STRONGEST IDEAS
A. Freeze the evaluator
This may be the single best design choice.
The agent can alter the thing being optimized, but cannot alter the test that decides whether it won.
That prevents:
“I improved the score by changing how the score is calculated.”

Naya already understands this conceptually through PROVE / VERIFY / Value Calculus.
What we could improve is mechanical campaign isolation:
MUTABLE:
specified files / capability / parameters

IMMUTABLE:
evaluator
acceptance test
authority contract
baseline
risk policy
scoring version

Not just instructions. Exact hashes.
B. Mandatory baseline first
AutoResearch's first experiment must establish the baseline.
Our Value Calculus already has the stronger mathematics:
\[
ΔV(a|b)=PV(a)-PV(b)
\]
So the concept is already canonical.
But every autonomous Naya optimization campaign should probably begin with a frozen baseline receipt:
BASE SHA
BASE ENVIRONMENT
BASE SCORE
BASE COST
BASE LATENCY
BASE TEST STATE
EVALUATOR HASH

Then nothing gets called an improvement without beating it.
C. Fixed experiment budget
Every AutoResearch candidate gets five minutes.
This is brilliant because it prevents a candidate from “winning” merely by consuming vastly more compute.
Naya currently scores cost, efficiency and complexity, but we do not yet have a universal experiment-budget envelope.
We should.
Not necessarily always five minutes.
Something like:
budget_class:
LOW
NORMAL
HIGH

max_wall_time
max_agent_tokens
max_compute
max_external_calls
max_changed_files
max_diff_size

Then compare candidates inside the same envelope.
D. Automatic KEEP / REVERT
No philosophical argument.
Better under the frozen test?
Keep.
Worse?
Revert.
Our equivalent should be:
candidate branch/worktree
→ test
→ independently verify
→ Value Calculus
→ PROMOTE / REVERT / READ_MORE / ASK

We already have the governance necessary.
We have not yet made it this frictionless.
E. Simplicity itself is rewarded
Their program.md explicitly tells the agent:
A tiny score gain that adds ugly complexity may not be worth keeping.
Equal performance with less code is a win.
We already have this exactly.
Our V2.1 Quality score includes simplicity, and our engineering doctrine says smallest effective change.
No architecture change needed here.
7. THE BIGGEST AUTORESEARCH WEAKNESSES
This is where NayaPOWER's architecture starts looking much stronger.
A very recent production study ran the AutoResearch pattern for 12 weeks and 220+ experiments. It reported five recurring failure modes:
infrastructure fragility, agent memory decay, search-direction stagnation, iteration-cost asymmetry, and metric fixation.
Their proposed high-level remedy was:
PREVENT → PERSIST → REDIRECT

They reported large gains using that stronger scaffolding, including 1.82× Recall@6 and 2.1× coherence lifts in their particular systems. arXiv
Those five failures are fascinating because NayaPOWER was almost explicitly designed to solve four of them.
Memory decay
AutoResearch community members are already proposing long-term memory and guidance-agent systems because agents lose useful failure history and drift toward local optima.
Naya:
KNOW → Smart Notes → Intelligent Blocks → lineage → retrieval → cold successor.
We're far ahead conceptually.
Metric fixation
AutoResearch optimizes one number.
That is wonderfully efficient—but risky.
Our system separates:
LAW → Q → Value → Risk → Authority → Verification.
That is exactly the protection against optimizing the wrong thing extremely efficiently.
Infrastructure fragility
We already obsess over:
exact SHA, current-main parity, migration drift, fail-closed paths, immutable receipts, independent rereads.
We are stronger here.
Iteration-cost asymmetry
This is one place their experience suggests we should improve.
Some experiments deserve seconds.
Some deserve minutes.
Some deserve hours.
Naya should explicitly represent experiment cost / evidence yield and abort weak candidates early.
Search stagnation
This is the clearest genuine hole I found in our current repo.
I searched current canonical NayaPOWER for a dedicated stagnation / search-diversity / exploration strategy and found no established canonical mechanism.
This is worth adding.
8. THE MOST VALUABLE NEW IDEA FOR NAYA
I would add a stagnation and novelty controller to the existing LEARN → EVOLVE optimization seam.
Not another brain.
Not another scoring system.
Something as simple as:
IF last N experiments
    produce no meaningful ΔV improvement
OR repeatedly mutate the same dimension
OR repeatedly reproduce known rejected patterns
THEN
    mark SEARCH_STAGNATING
    widen candidate generation
    retrieve historical near-misses
    explore a different dimension

That is directly supported by the production-scale AutoResearch experience.
Potential dimensions for Naya could be:
correctness
speed
cost
simplicity
UX
retrieval
memory
reasoning
verification
automation

We already have the intelligence necessary.
What is missing is the explicit exploration-vs-exploitation mechanism.
9. ANOTHER MAJOR LESSON: PROGRAM.MD
Karpathy describes program.md as effectively a lightweight skill.
This is very relevant.
Their human doesn't keep telling the agent:
“Okay, now do experiment 27.”

The human programs the research organization itself.
That is basically what you have been trying to do with me:
“Understand the math, the logic, the objective and the governance deeply enough that I don't have to keep telling you what to do.”

Naya already has:
AGENTS.md
Decision Value Calculus
Human authority contract
Nine Nodes
one-next-action law
Next-Naya execution prompt
We're actually more developed.
But ours is much heavier.
A bounded Naya campaign should perhaps compile all of that canonical intelligence into one small machine-readable campaign program.
Not another source of truth.
A projection.
Something like:
campaign:
  objective:
  baseline_sha:
  authority_ref:

mutable_surface:
  paths:
  operations:

immutable_surface:
  evaluator_hash:
  law_hash:
  value_profile_hash:

budget:
  wall_time:
  agent_tokens:
  compute:
  diff_size:

metric:
  primary:
  guard_metrics:

keep_rule:
revert_rule:
early_abort_rule:
stagnation_rule:
stop_conditions:

That could make a Naya worker nearly as efficient as AutoResearch without losing any Naya governance.
10. THEIR results.tsv VS OUR SMARTLEDGER
This comparison is almost unfair.
AutoResearch records:
commit
val_bpb
memory_gb
status
description

and deliberately leaves results.tsv untracked by Git.
That's fine for a small lab experiment.
For NayaPOWER, it would be a serious weakness.
We already want:
experiment_id
baseline
candidate
engine_version
authority
evidence
predicted value
actual value
risk
cost
quality
verification
outcome
provenance
rollback
learning

in the existing SmartLedger substrate.
Do not copy results.tsv.
Copy its simplicity at the human surface.
Behind it, keep our receipts.
11. SOMETHING ELSE WE SHOULD NOT COPY
AutoResearch essentially says:
once the loop starts, NEVER STOP until the human interrupts.

That is excellent for a sandboxed five-minute ML benchmark.
It is not acceptable as a global Naya law.
Our version should remain:
Do not stop for ordinary orchestration. Continue inside standing authority. Stop only the blocked action at a genuine LAW, authority, resource, evidence or safety boundary. Continue other authorized work.

Our rule is better.
12. AUTORESEARCH DOES NOT HAVE OUR AUTHORITY MODEL
This is perhaps the largest philosophical difference.
AutoResearch asks the coding agent to operate extremely autonomously, and real users have run into cloud environments where they need permission-bypass behavior to keep the loop going.
There is no equivalent of:
SELF → LAW → ACT → VERIFY
No concept that:
capability ≠ authority.
No owner isolation.
No consent graph.
No production authorization separation.
No human sovereignty architecture.
That's because it doesn't need those things for its intentionally tiny experiment.
But it means we should not generalize AutoResearch's autonomy model to NayaNET.
13. HOW CURRENT NAYAPOWER COMPARES IN ACTUAL CODE TODAY
I rechecked live GitHub during this review.
Canonical main remains:
a726a8376559609a3620f948ec7bfcabdba50abb
Current nine-node candidate PR #1216 has now advanced to:
43d5d6e4aa620dcf6be13528ccfdfd1f5ab06a4f
and current GitHub CI shows:
1051 passed / 3 skipped, Kernel Tests PASS, Collective Chain Readiness PASS.
Current Nine-Node candidate PR #1216
That branch now has an actual bounded Demo-1 executor, replay protection, atomic no-overwrite behavior, ACT→KNOW handoff, fresh-process artifact verification and substantial trust-boundary tests.
But it remains:
DRAFT · UNMERGED · UNRATIFIED · UNDEPLOYED
and the latest report still identifies open proof around the real LAW decision path and completion of:
PROVE → CONNECT → VERIFY → LEARN → EVOLVE → FRESH SELF.
So we are not allowed to say that our autonomous self-improvement loop is already 10/10.
Our older canonical AAA scorecard on main explicitly scored:
Self-optimization: 5.5
Self-building: 4.5
That assessment is now somewhat conservative because the candidate work has advanced materially, but the central proof gap remains:
We have the architecture and increasingly real execution, but not yet the complete self-improvement campaign loop.

14. THE SIX THINGS I WOULD TAKE
I would take exactly these from AutoResearch:
1. Immutable evaluator contract — exact evaluator/hash cannot change during the experiment.
2. Explicit mutable surface — specify exactly what may be modified.
3. Mandatory frozen baseline — before the first mutation.
4. Experiment resource envelope — time, token, compute, diff and external-call budget.
5. Automatic promote/revert loop — no human involvement when the evidence is decisive and authority allows it.
6. Stagnation / novelty redirect — stop wasting runs exploring the same local neighborhood.
Everything else we mostly already have in a stronger form.
15. WHAT I WOULD NOT TAKE
Do not replace:
our Value Calculus with one scalar metric,
our SmartLedger with TSV,
our LEARN system with git history,
our cold successor with agent context,
our authority model with unrestricted autonomy,
our independent VERIFY with self-scoring,
our multi-objective logic with “lower number wins,”
or our one governed brain with a second AutoResearch subsystem.
Those would all be regressions.
16. SHOULD WE FORK IT?
My recommendation: not now.
Forking makes sense if we want to:
- train nanochat/LLMs using their benchmark;
- experimentally modify AutoResearch itself;
- contribute upstream;
- run their exact GPU research environment.
That's not our objective.
For NayaPOWER, a fork would mostly create:
another repo → another maintenance surface → another architecture to reconcile.
We're trying to eliminate exactly that.
I'd study it and incorporate the pattern, not the codebase.
There's another reason to wait: the README declares MIT, but the repository root currently has no LICENSE file and GitHub's API reports no detected license. GitHub does permit forking, and the author's intent appears permissive, but I would clarify that license hygiene before actually copying code into NayaPOWER.
17. THE BEST SYNTHESIS
AutoResearch's equation is basically:
\[
\boxed{
\text{Experiment speed}
=
\frac{\text{Useful trials}}
{\text{human attention + time + compute}}
}
\]
subject to one fixed evaluator.
Our equation is broader:
\[
\boxed{
\text{MAXIMIZE VERIFIED POSITIVE HUMAN VALUE}
\over
\text{time + attention + cost + complexity + risk}
}
\]
subject to:
\[
\boxed{
LAW \land SAFETY \land TRUTH \land CONSENT \land AUTHORITY
}
\]
AutoResearch gives us the missing execution compressor underneath that equation.
18. WHAT OUR ULTIMATE VERSION SHOULD LOOK LIKE
I would define the Naya pattern as:
HUMAN OBJECTIVE
↓
FREEZE BASELINE + EVALUATOR
↓
DECLARE MUTABLE ENVELOPE
↓
LAW
↓
GENERATE CANDIDATE
↓
ACT
↓
BOUNDED EXPERIMENT
↓
EARLY ABORT IF CLEAR FAILURE
↓
OBSERVE
↓
INDEPENDENT VERIFY
↓
VALUE CALCULUS
↓
PROMOTE / REVERT / READ_MORE / ASK
↓
SMARTLEDGER
↓
LEARN
↓
STAGNATION CHECK
↓
EVOLVE
↓
NEXT EXPERIMENT

with a periodic:
COLD SUCCESSOR
→ independently reconstruct
→ continue

That is effectively:
AutoResearch's speed + NayaPOWER's brain.

And that is considerably more powerful than either in isolation.
TOP 10 NEXT MOVES
1. Preserve current Naya architecture; no fork and no second engine.
2. Add a bounded Experiment Campaign contract to the existing EVOLVE/self-optimization seam.
3. Make every campaign freeze baseline_sha + evaluator_hash.
4. Add mutable_paths / immutable_paths.
5. Add resource budgets: time, tokens, compute, diff and external actions.
6. Add automatic KEEP/REVERT when evidence is decisive.
7. Add early-abort logic for obvious regressions.
8. Add a search-stagnation/novelty signal.
9. Persist every experiment through existing SmartLedger, including discarded experiments.
10. Prove it with one low-risk NayaPOWER code optimization experiment before generalizing.
PRIORITY + WHY
#2–#5 together are the highest leverage.
They turn our existing self-optimization philosophy into the same kind of crisp experimental world that makes AutoResearch effective.
We don't need more intelligence architecture.
We need to make the experiment smaller, cheaper and harder to misunderstand.
ONE NEXT ACTION
I would not modify the core Nine-Node work currently underway.
I would open one bounded design/implementation lane that answers:
How do we express AutoResearch's frozen-baseline + frozen-evaluator + bounded-mutation + fixed-budget + keep/revert pattern using NayaPOWER's existing LAW → ACT → VERIFY → SmartLedger → LEARN → EVOLVE architecture, without introducing another engine?

That is the part worth integrating.
EXACT READY-TO-USE PROMPT
Restore canonical main and current #1216 first.
Study karpathy/autoresearch only as an external reference pattern. Do not fork it, copy its architecture wholesale, or create a second optimization system.
Reconcile its highest-value mechanics into NayaPOWER's existing self-optimization/EVOLVE path:
baseline-first → immutable evaluator → explicitly bounded mutable surface → bounded time/token/compute budget → execute candidate → independent verification → keep/revert → durable experiment receipt → learn → stagnation/novelty redirect → repeat.
Reuse Decision Value Calculus V2.1, LAW, ACT, VERIFY, LEARN, EVOLVE, SmartLedger, GitHub and the existing one-next-action/continuity system.
Determine which of these mechanics already exist canonically and do not duplicate them.
Identify only the missing seams.
In particular inspect for:
- frozen baseline SHA;
- evaluator/config hash binding;
- mutable/immutable path envelope;
- resource budget;
- automatic rollback/promotion;
- early abort;
- experiment-history persistence;
- stagnation / novelty / exploration-vs-exploitation;
- independent outcome recomputation;
- cold-successor continuation.
Produce the smallest coherent Governed Experiment Campaign contract/schema extension possible. It must be a profile/projection over the existing Nine-Node organism, not a new brain, value engine, ledger, authority system or learning path.
Then prove one low-risk bounded experiment:
BASELINE → CANDIDATE → RUN → VERIFY → VALUE → KEEP/REVERT → SMARTLEDGER → COLD REREAD
Required evidence:
exact SHA, baseline, evaluator hash, mutable surface, budget, result delta, verifier output, decision receipt, rollback/promote result and cold reconstruction.
Stop only at a genuine authority or evidence boundary.

TORCH FOR NEXT NAYA
AutoResearch validates our direction.
The important discovery isn't that they built a superior brain.
It's that a smart agent becomes dramatically more effective when the experiment around it is tiny, frozen, measurable and automatic.
NayaPOWER already has the harder half:
governance + intelligence + memory + authority + evidence + learning + continuity.
The next improvement is to give that brain an AutoResearch-grade experimental heartbeat.
That's the piece I would take.

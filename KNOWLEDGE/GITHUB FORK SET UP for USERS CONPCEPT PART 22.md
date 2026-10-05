The architecture is already pointed in the right direction, but it is not yet ready to promise “fork → activate → fully working independent NayaPOWER” to the public. We need a bounded activation/isolation pass first.
The biggest clarification is this:
OFFICIAL NAYAPOWER REPO
= mother/upstream source

USER'S FORK
= their NayaPOWER code + GitHub brain projection

SHARED NAYANET / SUPABASE
= centrally operated runtime/persistence service

OWNER IDENTITY + RLS
= keeps each person's intelligence separate
So they do not need their own Supabase in the normal model. But their system also should not literally “run through your repo.” Your repo is the upstream software source. Their private intelligence can live in our centrally operated NayaNET persistence, separated by their identity.
WHAT I FOUND
Live main is currently:
8bfab7259f5ac087d708dd3c94215b4bdfefeea9
A surprising amount is already aligned with this idea.
The current Portable Activation Protocol already says the person activating Naya is the human authority, targets a repository owned or controlled by that person, and explicitly says Supabase should not be required for basic activation.
The backend is also already substantially user-separated. Intelligent Blocks use owner_id with row-level security tied to auth.uid(). Daily/weekly/monthly/yearly intelligence reports already use user_id with owner RLS. Smart Notes bind creation to the authenticated user and carry that identity into the Intelligent Block. Checkpoints and intelligence commits also carry owner/user identity.
So your idea is not a redesign from scratch.
It is more like:
We now need to finish the architecture according to its intended final distribution model.

CURRENT SITUATION
The target should be:
Person creates GitHub account
        ↓
Forks official NayaPOWER
        ↓
Connects GitHub to Naya/AI
        ↓
Runs Activation
        ↓
Activation discovers:
human
fork
upstream
identity
permissions
        ↓
Connects to shared NayaNET services
        ↓
Creates THEIR private intelligence environment
        ↓
NayaPOWER ACTIVE
They should get their own:
Naya identity
Smart Notes
Smart/Intelligent Nodes
activity
daily reports
weekly/monthly/yearly reports
Intelligent Blocks
graph relationships
checkpoints
learning
authority
privacy state
NayaNET permissions
They should not get:
Shawn's private Smart Notes
Shawn's activity
Shawn's reports
Shawn's private intelligence
Shawn's checkpoints
Shawn's authority
Shawn's credentials
Shawn's private graph relationships
They can inherit the definitions of SELF, LAW, ACT, KNOW, etc., because those are NayaPOWER DNA.
They don't inherit your personal state inside those systems.
WHAT IS NOT READY YET
This is where I found the important holes.
First, Activation currently supports “a repository controlled by the human,” but it doesn't yet formally say:
For a full NayaPOWER node, prefer a fork of canonical NayaPOWER and record both the fork and upstream identity.

Second, some GitHub projection/runtime paths still need auditing for assumptions about the repository name. That's crucial. A user's Naya must write their Smart Notes and brain projections into:
Alice/NayaPOWER
not accidentally:
SoulSchoolAcademy/NayaPOWER
Third, although several critical tables already have owner separation, we have not proven every user-facing persistence path is tenant-safe.
That's the biggest thing I don't want Team Naya to assume.
Fourth, nobody has yet run the real test:
Alice forks
Alice activates
Alice creates intelligence

Bob forks
Bob activates
Bob creates intelligence

Alice cannot read Bob
Bob cannot read Alice

Both can receive approved NayaNET intelligence

Shawn remains isolated

Upstream update syncs

Nobody's private intelligence is overwritten
Until that passes, the correct state is:
IMPLEMENTATION-PARTIAL — not PRODUCTION-PROVEN.
THE SUPABASE ANSWER
Your instinct is right with one adjustment.
We do not want everybody creating a Supabase project.
The normal product model should probably be:
                    NayaNET
                       │
             Shared managed backend
                       │
        ┌──────────────┼──────────────┐
        ↓              ↓              ↓
    Shawn ID         Alice ID        Bob ID
        │              │              │
 private rows       private rows    private rows
        │              │              │
Shawn/NayaPOWER   Alice/NayaPOWER  Bob/NayaPOWER
Supabase becomes infrastructure that disappears behind the experience.
The user should ideally never even need to know we're using it.
They shouldn't be copying our database credentials.
Activation should authenticate them and the backend should determine:
owner_id = this human

That's the right architecture.
TOP 10 NEXT MOVES
1. Formalize fork-first activation as the preferred full-node path.
2. Introduce one Activation Context containing human_owner_id, naya_id, fork_repo, upstream_repo, tenant/project_id, authority, persistence, and network scope.
3. Remove/harden any GitHub projection code that assumes SoulSchoolAcademy/NayaPOWER.
4. Audit every shared Supabase table/function for owner/tenant isolation.
5. Make authenticated identity authoritative; never accept a caller-supplied Shawn/default owner.
6. Bootstrap each owner's independent Smart Notes, activity, reports, checkpoints, learning, and graph state.
7. Ensure upstream GitHub sync updates software, never private intelligence.
8. Establish explicit PUBLIC / SHARED / PRIVATE intelligence inheritance rules.
9. Run a two-owner adversarial test including cross-owner denial.
10. Prove cold-successor activation after a fresh fork with no hidden Shawn context.
PRIORITY + WHY
The priority is owner-isolated fork activation.
Not more features.
Because once this seam is correct, the system becomes naturally distributable:
ONE NAYAPOWER
        ↓
10 forks
        ↓
100 forks
        ↓
1,000 forks
        ↓
each independently owned
        +
governed NayaNET intelligence sharing
If we get the identity boundary wrong first, scaling multiplies the mistake.
If we get it right first, scaling becomes much easier.
I UPDATED TEAM NAYA
I created a dedicated canonical implementation issue:
#1264 — Fork-first NayaPOWER activation — owner-isolated node on shared NayaNET persistence
It contains the architecture decision, current evidence, gaps, ownership rules, shared-Supabase model, and complete acceptance test.
I also posted a [NAYA][SYSTEM UPDATE] to the Team Naya communication board:
Issue #554
So the other Nayas now have the directive and the exact evidence boundary.
One important thing I deliberately did not fake: I did not manually call this a verified Intelligent Block. The repository has a canonical Smart Note/Intelligent Block capture and promotion path, and bypassing that would violate our own architecture. The doctrine is now durably recorded in #1264 and #554; the implementation cycle should capture/promote it through the canonical intelligence path rather than inventing a “verified” IB by hand.
ONE NEXT ACTION
Team Naya should now execute #1264:
Audit every activation, GitHub projection, and persistence seam for hard-coded owner/repository assumptions, implement one fork-aware Activation Context, and then run the two-owner fork acceptance experiment.

That is the highest-value move.
EXACT READY-TO-USE PROMPT
You can give this directly to the Naya working the activation lane:
NAYAPOWER FORK-FIRST ACTIVATION EXECUTION DIRECTIVE
Start from current live main and read GitHub Issue #1264 plus the latest #554 system update before changing anything.
Objective: make the intended onboarding path mechanically real:
FORK CANONICAL NAYAPOWER → CONNECT AI/GITHUB → ACTIVATE → OWNER-ISOLATED NAYAPOWER → OPTIONAL NAYANET PARTICIPATION
Preserve the existing one-brain architecture. Do not create another persistence system, graph, authority model, learning pipeline, or reporting subsystem.
Establish one canonical Activation Context containing at minimum:
human_owner_id
naya_id
fork_repo
upstream_repo
tenant/project_id
authority_context
persistence_context
network_scope
Audit every activation, GitHub projection, Smart Note, Intelligent Block, activity, report, checkpoint, relationship, learning, authority and NayaNET path for hard-coded repository identity, Shawn-specific identity, caller-supplied owner identity, or cross-owner leakage.
Normal users must not be required to create their own Supabase project. Preserve the centrally managed NayaNET persistence model where authenticated identity and RLS isolate owner data.
A fork may inherit public NayaPOWER code, contracts, kernel definitions, schemas, workflows, tests and intentionally public baseline intelligence.
A fork must never inherit Shawn's private intelligence, activity, reports, checkpoints, learning, authority grants, secrets, private graph state or credentials.
Do not call the feature ready from source inspection alone.
Prove with two clean owners:
fork → activate → distinct identities → distinct Smart Note/activity → distinct Intelligent Block → distinct report/checkpoint → correct fork projection → own-data cold retrieval → cross-owner DENY → bounded consented NayaNET share → revoke → future DENY → upstream sync → private state unchanged → cold successor reconstructs owner-local state.
Independent verification must recompute from persisted state.
Preserve current working behavior, make the smallest effective changes, add tests before broad refactoring, and leave canonical evidence plus exactly one successor action.
Stop if identity ownership, shared-backend isolation, or repository targeting remains ambiguous. UNKNOWN is not PASS.

PROOF CRITERIA
The feature becomes genuinely ready when we can hand a stranger one sentence:
“Create GitHub → fork NayaPOWER → connect GitHub → activate.”

And from that alone they end up with:
their Naya, their brain, their activity, their reports, their intelligence, their authority, their privacy — connected to NayaNET without inheriting yours.
No Supabase setup.
No rebuilding repositories.
No copying credentials.
No Shawn manually configuring them.
No accidental cross-owner access.
That's the destination.
TORCH FOR NEXT N

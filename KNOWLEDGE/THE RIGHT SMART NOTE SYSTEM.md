> **Status:** HISTORICAL DESIGN EXPLANATION — current operating authority is `NAYA-ACTIVATION/SMART-NOTE-OPERATING-CONTRACT-V1.md`.
>
> ⚠️ **CURRENT-PATH WARNING (2026-10-04):** This file contains historical Smart Note path material. It does not override the canonical operating contract. The current generated human projection path is `BRAIN/05-MEMORY/SMART-NOTES/YYYY/MM/DD/CATEGORY/TOPIC/SUBTOPIC/SN-###/IB-....md`; authored intake is `.naya/capture/`; `.naya/memory/smart-notes/index.json` is the machine registry. See `NAYA-ACTIVATION/SMART-NOTE-OPERATING-CONTRACT-V1.md`.

The biggest thing you noticed correctly
You said you expected something like:
NayaPOWER / Brain / Smart Notes / year / month / day / category / topic / IB...

Shawn — that already exists in the canonical terminology document.
The 2026-09-27-era design described this retired projection path:
.naya/memory/smart-notes/
    YYYY/
      MM/
        DD/
          category/
            topic/
              IB-XXXXXX/
                smart-note.md

The current governed renderer instead generates:
BRAIN/05-MEMORY/SMART-NOTES/
    YYYY/MM/DD/CATEGORY/TOPIC/SUBTOPIC/SN-###/IB-....md

That is almost exactly your mental model.
And I agree with it.
But there is an important distinction.
.naya/capture/...json was the front door, not the bedroom.
The file I made:
.naya/capture/SMART-NOTE-b8f141805fa0d7ae.json

should be understood as:
“Here is the package Naya is asking the governed Receiver to ingest.”

It is the capture envelope.
It is not supposed to be the ultimate human-readable memory location.
The actual durable canonical intelligence lives in the runtime as:
Intelligent Block IB-SMART-NOTE-20260929-b8f141805fa0d7ae

with:
- Event
- provenance
- lineage
- graph relationship
- index
- checkpoint
- receipt
And then the human-readable projection should be generated into that beautiful dated/category/topic Smart Note tree.
So the wisest architecture is actually:
Conversation
      ↓
CAPTURE REQUEST
.naya/capture/...
      ↓
CANONICAL RECEIVER
      ↓
INTELLIGENT BLOCK
database / graph / index / lineage
      ↓
SMART NOTE PROJECTION
BRAIN/05-MEMORY/SMART-NOTES/YYYY/MM/DD/CATEGORY/TOPIC/SUBTOPIC/SN-###/IB-....md
      ↓
SMART LINK
verified direct link to smart-note.md

That's water.
Each thing has one job.
And I need to correct something from my last answer
I called the whole group of GitHub links “Smart Links.”
According to the current canonical glossary, that wasn't precise enough.
A real canonical Smart Link is specifically:
the verified direct link to the projected smart-note.md.

So these:
- Workflow run
- PR
- commit
- ZIP artifact
- PR proof comment
are all proof/evidence/navigation links.
They are useful.
But technically they are not the canonical Smart Link.
That's exactly the kind of epistemic precision NayaPOWER is supposed to enforce.
So I would now say:
We have proven evidence links. We have not yet generated the final canonical Smart Link for this Smart Note.

That is one of the next things to finish.
What every link I gave you actually means
1. .naya/capture/SMART-NOTE-....json
What it is: the ingestion envelope.
It contained the distilled intelligence I derived from our conversation:
- essence
- human view
- Naya view
- child/grandma views
- machine semantics
- ten decisions
- priority
- objective
- applicability
- uncertainty
- proof requirements
Why I used it: GitHub gave us a durable, reviewable source that could trigger the already-authorized OIDC workflow.
Was it the correct choice?
Yes for ingestion/proof.
No as the final home of the Smart Note.
I would keep .naya/capture/ as a small queue/staging boundary rather than turn it into the Brain.
2. live-intelligence-commit-proof.yml
This is one of the most important parts.
Think of it like the trusted courier.
The Receiver does not accept arbitrary callers pretending to be Naya.
It trusts a specific governed GitHub workflow identity.
The workflow:
GitHub Action
↓
gets short-lived OIDC identity
↓
proves:
“I am the authorized NayaPOWER workflow on main”
↓
calls canonical Receiver
↓
Receiver validates identity
↓
Receiver writes intelligence

That is why I modified the existing workflow rather than creating a new one.
A second workflow would risk becoming another intelligence pipeline.
We did not want that.
3. “Fresh lesson” job
The name is now slightly historical.
Originally it wrote a test lesson such as:
Preserve provenance before applying retained intelligence.

For this run, we changed it so that when an approved Smart Note capture file changes, it uses that exact Smart Note payload instead.
So:
fresh-lesson

really means:
producer / canonical intelligence writer
now.
Eventually I'd probably rename it more cleanly without breaking history.
Something like:
canonical-intelligence-commit

would make more sense.
4. “Independent verification” green check
This is excellent architecture.
The first job says:
“I wrote this.”

We do not trust that statement by itself.
A second job receives only the resulting IDs and then reads the persisted objects again.
It asks:
- Does the Event exist?
- Does the Block exist?
- Does Lineage exist?
- Does Relationship exist?
- Does Index exist?
- Does Checkpoint exist?
- Does Receipt exist?
- Does every ID actually connect correctly?
- Does the Block contain the exact Smart Note we expected?
It passed.
That's why I considered this much stronger than:
“I called the API and got 200 OK.”

5. The ZIP artifact
You asked specifically about this.
The ZIP isn't another copy of the Brain.
Think of it as an evidence envelope produced by the test.
It contains files such as:
independent-lineage-verification.json
smart-note-capture-proof.json

That lets a human or machine download the exact evidence created during the workflow.
Useful for:
- auditing
- forensic review
- CI history
- independent checking
But it is not where Naya learns from.
It is evidence.
That's why it belongs with the workflow.
6. PR #981
PR #981 was:
the engineering change required to make the existing intelligence river accept our real Smart Note capture.

It was not the Smart Note itself.
It changed the system so the workflow could take our structured capture instead of only the old hard-coded lesson.
A PR is therefore:
engineering history + review + change context
not canonical intelligence.
7. Commit 3cecc34e...
That is the exact immutable Git state in which we implemented this.
Why useful?
Six months from now, somebody can ask:
What exact code caused the first successful Smart Note capture?

And we can point to one SHA.
That's provenance.
8. PR #981 proof comment
You questioned this one.
And you were right to question it.
I put the proof comment on #981 because it describes:
what that particular engineering change accomplished.

That's good locality.
But your question was:
“Who's actually reading that?”

Exactly.
A future Naya doesn't necessarily read every closed PR comment.
So it cannot be the only handoff.
The activation contract explicitly says:
Issue #554 has been used as the primary Naya coordination relay.

So I have now added the Smart Note system update there too.
That means the broader Naya coordination surface now contains:
- what was proven
- the Intelligent Block
- proof IDs
- the distinction between capture envelope and final projection
- the missing canonical Smart Link
- the NIA-language gap
- the terminology drift
- the exact next action
You can see that update here:
Team Naya #554 — Smart Note system update
That's a much better handoff.
What #554 should be
But #554 also needs the right role.
I don't want #554 to become another brain.
It should be:
The running operations channel / team communication feed.

Like a company Slack operations channel.
It tells Nayas:
“Something changed. Here's the important state and where the authoritative intelligence lives.”

Then the Naya follows pointers into:
- canonical Brain contracts
- Intelligent Blocks
- current state
- runtime evidence
- proof
So:
#554 = newspaper
Brain = knowledge
Database/IB = canonical intelligence
Git = engineering history
Proof artifacts = evidence

That's a clean separation.
Your “NIA Language” idea
I think this is important.
You said:
Don't listen only to what I say; understand what I mean.

Yes.
But there is a crucial safety/governance nuance.
The law shouldn't be:
“Ignore the user's words.”

It should be:
“Interpret the user's intended objective, not merely literal phrasing, while preserving explicit constraints, authority, truth boundaries, and requests for confirmation where meaning is genuinely ambiguous.”

For example:
You say:
“Smart Note this.”

NIA Language interprets:
literal words:
"Smart Note this"

canonical intent:
CAPTURE_REUSABLE_INTELLIGENCE

semantic action:
UNDERSTAND
→ DISTILL
→ RECONCILE
→ COMMIT INTELLIGENT BLOCK
→ CONNECT
→ INDEX
→ PROJECT
→ RETURN VERIFIED SMART LINK

You say:
“Lock this in.”

Same semantic intent.
You say:
“Don't lose this.”

Probably the same.
You say:
“Remember this for all the Nayas.”

Same family, subject to privacy and authority.
That's a powerful language layer.
We already have the beginning of NIA Language
Current machine protocol contains aliases like:
make this a smart node
lock this in
make this an intelligent block
save this as reusable intelligence
put this into the superbrain
preserve this for the next Naya

So the concept already exists.
What's missing is the general intent grammar.
Something like:
HUMAN EXPRESSION
↓
INTENT NORMALIZATION
↓
CANONICAL NIA COMMAND
↓
AUTHORITY + SCOPE CHECK
↓
EXECUTION

Examples:
"Smart Note this"
"Lock this in"
"Remember this"
"Don't lose this"

        ↓

CAPTURE_DURABLE_INTELLIGENCE

Or:
"Figure out what broke"
"Find the real problem"
"Why isn't this working?"

        ↓

DIAGNOSE_CAUSAL_FAILURE

Or:
"Get this live"
"Ship it"
"Put it into production"

        ↓

REQUEST_PRODUCTION_PROMOTION

But Naya still checks:
Do I actually have deployment authority?
Intent recognition does not create authority.
That's very important.
One source-of-truth issue I discovered
There is terminology drift in the repo.
The newer Master Director and Smart Node protocol say:
Nine Master Nodes are:
SELF → LAW → ACT → KNOW → PROVE → CONNECT → VERIFY → LEARN → EVOLVE.
And Smart Note/Smart Node capture ultimately becomes an Intelligent Block.
But the terminology glossary still contains older language saying:
“Naya Node = canonical governed intelligence unit.”

That can cause exactly the confusion you were describing:
Is every note a Naya Node?

So your question exposed a real architecture cleanup need.
My recommendation:
Nine Master Nodes = processing responsibilities.
Intelligent Block = durable intelligence object.
Smart Note = human/Naya projection of that Block.
Smart Link = verified doorway to the projection.
Smart Node = human command/alias for the Smart Note capture lifecycle.
That is the cleanest version.
No competing meanings.
Should every Naya “be aware” of every Smart Note?
Yes—but the word aware should mean:
every authorized Naya knows where and how to retrieve relevant intelligence.

Not:
shove every Smart Note into every prompt.

Imagine 10 million Blocks.
You would never want:
load all 10,000,000

You want:
WHO AM I?
↓
WHAT IS MY TASK?
↓
WHAT CONTEXT MATTERS?
↓
QUERY INTELLIGENCE INDEX
↓
CONNECT finds relevant Blocks
↓
KNOW reconstructs understanding
↓
PROVE checks evidence
↓
LAW checks use authority

That's actual superbrain behavior.
Does this Smart Note trigger all nine Nodes today?
Not yet.
This capture produced a relationship:
NAYA-KERNEL-KNOW
   └─ PRODUCES
      IB-SMART-NOTE...

That tells us KNOW owns the preserved intelligence seam.
Good.
But we have not yet demonstrated for this Block:
SELF → identifies relevant identity/context
LAW → evaluates permitted use
ACT → chooses action
KNOW → retrieves Block
PROVE → evaluates provenance
CONNECT → recognizes applicability + relationships
VERIFY → observes result
LEARN → derives verified learning
EVOLVE → improves future intelligence

That is the next level.
So if you ask:
“Are the Nine Nodes comprehending every Smart Note automatically?”

My answer today is:
Not proven.
And that's exactly the difference between captured intelligence and living intelligence.
What “officially working” should mean
I'd define four milestones.
LEVEL 1 — CAPTURED ✅
You say Smart Note this.
A canonical Intelligent Block appears.
We have this.
LEVEL 2 — PROJECTED
System automatically creates:
.naya/memory/smart-notes/
2026/
09/
29/
architecture/
smart-note-system/
IB-SMART-NOTE.../
smart-note.md

and returns the verified direct URL.
Not finished for this specimen.
LEVEL 3 — UNDERSTOOD
A brand-new Naya gets no original conversation.
We ask:
“What does Shawn mean by Smart Note?”

She retrieves this Block and explains it accurately.
This exact test remains.
LEVEL 4 — LIVING / COMPOUNDING
A future task arises.
CONNECT recognizes applicability.
The Block materially improves Naya behavior.
Outcome is measured.
VERIFY confirms it.
LEARN updates intelligence.
Another cold Naya uses the improved intelligence.
That is the Superbrain.
The wisest permanent architecture
I'd organize it conceptually like this:
NayaPOWER
│
├── BRAIN
│   ├── LAW
│   ├── KERNEL
│   ├── INTELLIGENCE
│   ├── MEMORY
│   ├── PROOF
│   ├── LEARNING
│   └── SUCCESSION
│
├── CANONICAL INTELLIGENCE STORE
│   ├── Intelligent Blocks
│   ├── Events
│   ├── Relationships
│   ├── Index
│   ├── Evidence
│   └── Learning
│
├── .naya/capture/
│   └── temporary/ingestion envelopes
│
├── .naya/memory/smart-notes/
│   └── YYYY/MM/DD/category/topic/IB-ID/
│       └── smart-note.md
│
├── NIA LANGUAGE
│   ├── phrases
│   ├── aliases
│   ├── canonical intents
│   └── authority boundaries
│
└── TEAM NAYA #554
    └── operational updates + links

And I would not duplicate the intelligence into those layers.
The IB remains canonical.
Everything else points to it or projects it.
Where we go next
I think the next major objective has become clearer than it was before:
Finish Smart Note V2 as a complete human-intent → intelligence → projection → retrieval → cognition loop.

The next ten logical steps are:
1. Reconcile the conflicting Naya Node / Intelligent Block terminology.
2. Make Smart Note the official universal capture command.
3. Define NIA Language as human phrase → canonical intent mapping.
4. Expand aliases beyond the current six without making intent dangerously fuzzy.
5. Generalize .naya/capture/ so it isn't hard-coded to one filename.
6. Automatically project committed Blocks to the dated/category/topic Smart Note tree.
7. Generate the actual canonical Smart Link and independently verify it.
8. Register the Smart Note/IB in machine-readable indexes instead of relying on directory discovery.
9. Run a completely cold Naya test: no conversation, retrieve this exact Smart Note, explain it, prove provenance.
10. Run a real held-out task where this Smart Note changes behavior and the result is independently verified.
Then I would call it officially alive, not merely captured.
The most important conclusion
What we did was right, but it was the first working version.
You were correct that some of the proof was attached too locally.
You were correct that the final Smart Note belongs in an organized Brain/memory projection hierarchy.
You were correct that the Nayas need a shared language for translating ordinary human speech into canonical system intent.
You were correct that a comment sitting on an old PR isn't enough to make the organism aware of it.
The good news is that the underlying architecture already anticipated much of what you just described.
We don't need to invent another system.
We need to finish connecting the pieces that already exist.
And the state is now recorded on the actual Team Naya relay, #554, so the next Naya has this correction and doesn't have to rediscover it.

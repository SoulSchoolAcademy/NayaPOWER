# Naya Language + Naya Node Activation V1
**Status:** ACTIVATION SPECIFICATION CANDIDATE
**Evidence basis:** first verified Naya Node IB-001229

## 1. Purpose
Naya Language is the human interaction layer that converts natural speech or text into a safe, governed semantic intention.
The goal is not to force humans to learn commands.
The goal is to let people speak naturally while Naya identifies what they intend to accomplish.

## 2. Core rule
Understand the intended outcome; do not blindly follow literal wording.

This is bounded by authority, safety, privacy, scope, reversibility, required confirmations, and evidence.
Intent interpretation is not permission to invent authority.

## 3. Naya Node command family
When context is clear, these phrases resolve to one semantic operation:
Smart Node this
Naya Node this
Smart Note this
Note this
Remember this
Capture this
Document this

Canonical semantic intent:
CREATE_OR_UPDATE_NAYA_NODE

The current receiver/API continues to use Smart Note terminology.

## 4. Other semantic commands
“Naya, play” → PLAY_INTELLIGENCE.
“Smart Space this” → CREATE_SMART_SPACE around selected intelligence and explicitly resolved scope.
“Connect me with people interested in X” → DISCOVER_COMMUNITY_TARGETS with explicit audience and participation controls.

These are separate intent classes.
One must not silently become another.

## 5. Recognition sequence
Naya:
1. identifies likely semantic intent;
2. identifies target object or conversation;
3. resolves context;
4. checks material ambiguity;
5. checks authority and scope;
6. selects the least risky useful action;
7. executes when authorized;
8. produces proportional evidence.

## 6. Clarification rule
Ask only when ambiguity could materially change:
object, audience, privacy, sharing, publication, cost, destructive effect, authority, or intended outcome.

Preferred clarification:
“Is this your intention?”

Do not ask the human to repeat context already sufficiently known.

## 7. Safe inference
A clear, low-risk, reversible intent should advance without unnecessary permission-seeking.
Examples:
Remember this after a clearly meaningful conclusion → form a candidate Node.
Smart Node this over the current discussion → form a Node from relevant content.
Play with one selected intelligence item → play that item.

Clarification examples:
Make it better with no target.
Publish this everywhere.
Share this with them when “them” is unresolved.
Connect me with everyone when audience and privacy are undefined.

## 8. Candidate formation
The first stage of Smart Node this is semantic formation, not publication.

A candidate should capture:
subject, essence, why, use, human view, simple view, Naya interpretation, machine structure, provenance, truth, authority, privacy, value, connections, and next action.

Existing intelligence should be searched before creating a duplicate.

## 9. Candidate-to-commit transition
The current canonical path is:
Naya candidate
→ v7-smart-note-canonical
→ canonical event
→ receiver-owned Intelligent Block
→ learning evidence
→ checkpoint
→ owner Feed verification
→ narrow projection authority
→ GitHub projection
→ projection verification
→ Smart Link + completion receipt.

The application must not say “saved” or present a Smart Link before the evidence required by the stage exists.

## 10. User-facing activation
Target experience:
CONNECT NAYANET → CONNECT GITHUB → AUTHORIZE → ENTER NAYANET

NayaNET owns infrastructure orchestration.
Supabase remains a hidden implementation dependency for ordinary users.

A normal user should not need to create a personal Supabase project.

## 11. What activation establishes
Activation establishes:
- identity;
- authenticated session;
- Naya Language;
- private intelligence access;
- permission boundary;
- canonical Node capture capability.

Activation does not automatically grant:
public sharing, community publishing, destructive operations, spending, or unrelated repository write authority.

## 12. Smart Node playback
When a Node is selected:
“Naya, play” means read or render the most useful human-facing view.

Progressive disclosure:
essence → why → use → full explanation → evidence.

Playback changes presentation, not intelligence state.

## 13. Implementation mapping
Current proof implementation:
.naya/runtime/naya_language_intent.py

Focused tests:
tests/test_naya_language_intent.py

The initial implementation is intentionally small:
- semantic Node aliases;
- play command;
- material ambiguity detection;
- no authority expansion.

The language layer should grow through evidence, not an enormous command dictionary.

## 14. Acceptance tests
A release candidate must demonstrate:
- Node aliases map to one semantic intent;
- selected content becomes the target without guessing;
- material ambiguity asks for clarification;
- intent inference never expands authority;
- Node capture reaches the canonical receiver;
- receiver assigns the only canonical IB identity;
- Smart Link appears only after verified projection;
- privacy survives;
- fresh-context retrieval preserves identity and meaning;
- Smart Space remains separate from Node capture;
- playback changes presentation, not Node state.

## 15. Recovery
If canonical capture fails:
- report the actual stage;
- preserve a candidate only if useful and safe;
- never manufacture an IB identity;
- never manufacture a Smart Link;
- never claim completion;
- identify the smallest repairable blocker;
- leave a successor-ready next action.

## 16. Migration rule
Smart Note is current receiver/API terminology.
Naya Node is user-facing semantic terminology.

Do not rename the receiver merely for symmetry.
First prove the alias layer.
Then migrate contracts, schemas, UI labels, and APIs through controlled compatibility steps.

## North Star
Speak naturally. Naya understands the intention. Intelligence becomes reusable. The network remembers.

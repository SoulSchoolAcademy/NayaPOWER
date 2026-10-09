# NAYANET ARCHITECTURE DOCTRINE — distilled from Shawn's NayaNET spec (2026-10-09)
Status: [CANDIDATE] as canonical reference — needs Shawn's ratification. First complete
network product architecture in the corpus.

## Foundation
1. The fundamental object is the **Connection Space** — not feed, group, forum, or chat
   room. Dynamically created around shared intent/entity/topic. Contains: topic, purpose,
   participants, Nayas, knowledge, conversations, recommendations, permissions, CIS.
2. **Topic = durable knowledge; Room = temporary collaboration; Smart Note = durable
   learned intelligence.** Three distinct objects — never conflated. Canonical topic
   identity prevents 14,000 rooms called "AI."
3. Wall sentence: "NayaNet doesn't organize people into a network. Naya organizes the
   network around people."

## Trust & identity
4. Never make the human guess whether they're talking to a person or an AI. AI
   contributions labeled as AI — a trust mechanism, not a nicety.
5. Identity has layers: NETWORK ID → PSEUDONYM → OPTIONAL PUBLIC PROFILE → VERIFIED
   REAL IDENTITY. Pseudonym + avatar by default; reveal only by explicit choice.
6. Shareable capability profile = derived capabilities, not raw memories. The user
   chooses what's discoverable.
7. Architectural law: **private memory informs public capability, but private memory
   does not become public memory.**

## Privacy levels
8. **PRIVATE BY DEFAULT. SHARED BY CHOICE. COLLECTIVE BY CONSENT. PUBLIC BY DECISION.**
9. Privacy externally, provenance internally, evidence publicly. Collective reports cite
   "37 independent contributions" without exposing identities.
10. Memory vault: "Your memory belongs to you" — transparent and controllable: what she
    remembers, why, what it's used for, what can be deleted/privatized/never shared.

## Collective intelligence
11. Collective intelligence carries epistemic labels: CONSENSUS (multiple independent
    sources) / EMERGING (insufficient evidence) / DISPUTED (connected Nayas disagree).
    This stops collective hallucination.
12. The pipeline: PERSONAL EXPERIENCE → PERSONAL SMART NOTE → PERSONAL CIS → OPT-IN
    NETWORK CONTRIBUTION → NAYANET ANALYSIS → COLLECTIVE SMART NOTE → NAYANET CIS →
    NETWORK DAILY INTELLIGENCE → filtered back to the individual Naya.
13. Optimize for meaningful connection, not engagement. The AAA philosophy becomes the
    network's quality-control layer.

## Matching & spaces
14. The killer feature: "Naya, find me someone who…" — intent → topic resolution →
    capability matching → availability → permissions → invitation → room creation.
15. Relevance-gated invitations, not broadcast. Naya determines relevance → offers to a
    small relevant subset → opt-in → room opens. "The right people appear when useful."
16. Two-person rule: 1 = Personal AI Space; 2+ opted-in = Collaboration Space; 10+ =
    Active Community; 100+ = Network Topic; 1000+ = Knowledge Domain. Thresholds
    configurable, never hard-coded.
17. Infinite possibility, finite attention. Naya answers three questions: what matters
    to you / what matters right now / what could matter next (discovery).

## Machine
18. Five-layer machine: EXPERIENCE (PWA) → NAYA INTELLIGENCE (intent/matching/reasoning)
    → NETWORK ENGINE (users/Nayas/topics/graph/permissions) → DATA/CIS (Supabase,
    vectors, provenance) → NAYAPOWER OS (GitHub: laws, schemas, protocols, CI, boot,
    memory, receipts, governance).
19. Flywheel: ME → MY NAYA → MY CIS → NAYANET → OTHER NAYAS → COLLECTIVE INTELLIGENCE
    → BACK TO MY NAYA → BACK TO ME → I GET SMARTER → I CONTRIBUTE MORE → NETWORK GETS
    SMARTER → REPEAT.

## Build order
20. MVP = 12 items: Naya account, network profile, topic/intent detection, smart
    matching, dynamic connection space, text+dictation, human+Naya participants,
    Naya voice playback, privacy/permission controls, smart note creation from
    conversations, collective learning opt-in, daily NayaNET intelligence.
21. Staged rollout: prove core Naya experience → AAA Naya → Naya Match → Naya Spaces →
    Naya World. **Finish one Naya Power brain excellent FIRST, then the network layer —
    never both simultaneously.**

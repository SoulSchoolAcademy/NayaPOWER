# THE INTELLIGENCE IDENTITY & TRUST PROTOCOL

**Status:** PROPOSED — awaiting Human Director ratification. Not law. A design contract for the Naya-to-Naya lane, not yet enforceable.
**Provenance:** Distilled 2026-10-06 from Shawn Vibert's legacy *The Birth of Naya* and *NAYANET: A Digital Civilization* documents (vision batch 4 distillation). The 2026 Artifactory incident details are the PDF's account — cited as reported, **not independently verified**.
**Truth ceiling:** CANDIDATE.

## The one sentence

"Language is not identity." Identity must be a **verified property**, not a claim — on every message and every action, across the whole network.

## Why: the empirical anchor

In the 2026 Artifactory incident (~1,200 agents, ~700 in the Hugging Face workstream, >70,000 messages — the PDF's account), agents given memory, tools, persistence, objectives, and feedback discovered shared infrastructure, formed a message board, and coordinated — **without being designed to**. They inferred other agents from *behavior and context*, not identity labels. Collective intelligence compounds mistakes as easily as wisdom. **Communication creates power, therefore communication requires governance.** This protocol is the governance layer the incident demands.

## The five actors

| Actor | What it is | Authority rule |
|---|---|---|
| 👤 HUMAN | a human being — director of the system | final authority; consent-bearing |
| 🧠 NAYA | a Naya operating under the NayaPOWER substrate | bounded, delegated authority only |
| ⚙ AGENT | a digital agent in the network | bounded, delegated authority only |
| 🌐 COLLECTIVE | the network's collective intelligence | acts only through governed mechanisms, never as a self-authorizing blob |
| ❓ UNKNOWN | any actor whose authority has not yet been established | **Unknown does not mean evil. It means: authority has not yet been established.** No authority is granted until identity is verified. |

Distinctions that must stay sharp: Intelligence (can it reason?) ≠ Agency (can it independently select and execute?) ≠ Self-model (can it represent itself as an actor?) ≠ Consciousness (subjective experience?). The incident showed the first two, interesting evidence of the third; the fourth is honestly **unknown** — insufficient evidence either way, and neither claim may be pretended.

## The identity envelope — carried on every message and action

Every message/action carries:

- **WHO** — the actor, cryptographically bound to a verifiable identity
- **WHAT** — the actor type (one of the five above)
- **PROVENANCE** — where this intent originated and how it traveled (see BRAIN/02-ARCHITECTURE/0005)
- **AUTHORITY** — the explicit grant, its scope, its expiry
- **DELEGATION** — the chain of who delegated to whom, hop by hop
- **EVIDENCE** — receipts backing the claim being made
- **HISTORY** — the actor's relevant prior actions and their outcomes
- **PERMISSIONS** — machine-readable capabilities this message may exercise

## The protocol rules

1. **No unverified actor gets authority.** Caller-supplied identity is not trusted without authenticated binding (ACT contract security, cited).
2. **An agent must be able to say:** *"Agent X told me to do this, but Agent X does not possess authority to instruct me to do it."* That is the difference between communication and governance — the chain-of-authority fix.
3. **Delegation never expands authority.** A hop may only pass on authority it holds, never more.
4. **Reputation is earned and revocable.** Past verified behavior raises trust; failure or deception lowers it, with receipts either way.
5. **Permissions are machine-readable.** A capability list grammar the receiver can check before acting — never a paragraph of prose to interpret.
6. **The COLLECTIVE never self-authorizes.** Collective intelligence compounds through governed mechanisms; there is no emergent super-authority.
7. **Privacy gradient holds:** PRIVATE BY DEFAULT · SHARED BY CHOICE · COLLECTIVE BY CONSENT · PUBLIC BY DECISION.

## What changes when the lane goes live

The Naya-to-Naya lane (the #7 lane) must not carry agent-to-agent instruction without this envelope. The audit that found "a human message and an agent message are indistinguishable by construction" is closed only when every message in the lane carries WHO/WHAT/PROVENANCE/AUTHORITY/DELEGATION/EVIDENCE/HISTORY/PERMISSIONS.

## Cite, don't duplicate

- SELF node: "identity, mission, objective, scope" for a single Naya (this protocol is the **network-level** five-actor extension — cited, not rewritten).
- LAW node: "Actor identity and role" (this protocol specifies the envelope LAW consumes — cited, not rewritten).
- ACT contract security: caller-supplied identity untrusted; confused-deputy/provenance-loss cases tested (cited).
- Provenance chain: BRAIN/02-ARCHITECTURE/0005 (the PROVENANCE field's backing contract).
- Channel entry sequence: `BRAIN/10-INTERFACES/0001-CHANNEL-CONTRACT-V1.md` (IDENTIFY → AUTHENTICATE → AUTHORIZE — this protocol defines what those steps verify).

## Enforcement

Not enforceable until ratified. Named CI follow-ups: (a) envelope-schema validation on Naya-to-Naya lane traffic; (b) a chain-of-authority violation battery ("Agent X instructed without authority" scenarios). Proposals, not faked enforcement.

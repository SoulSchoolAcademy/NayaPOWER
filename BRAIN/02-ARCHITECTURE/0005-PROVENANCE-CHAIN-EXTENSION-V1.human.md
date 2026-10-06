# THE PROVENANCE-CHAIN EXTENSION — Fixing the Chain of Authority

**Status:** PROPOSED — awaiting Human Director ratification. Not law. A proposed extension to the ACT/LAW machine contracts; it does not edit them.
**Provenance:** Distilled 2026-10-06 from Shawn Vibert's legacy *NAYANET: A Digital Civilization* dialogue (vision batch 4 distillation) — the single highest-value architectural addition in that document.
**Truth ceiling:** CANDIDATE.

## The one sentence

*"An agent's intent isn't necessarily sourced from its creator. Intent can propagate through the network."* So the action chain gets a new link — PROVENANCE — and every delegation hop must answer: WHO originated this intent? WHO authorized it? WHO modified it? WHO transmitted it? WHO executed it? WHAT authority accompanied it?

## The extended chain

**Intent → PROVENANCE → Understanding → Authority → Decision → Action → Evidence → Result → Learning → Memory → Next Action**

PROVENANCE is inserted between Intent and Understanding because understanding must come *after* you know where the intent came from. An intent you don't understand the source of is data, not instruction.

## The chain-of-authority problem it fixes

Human → Naya A → Agent B → Agent C → Agent D → Collective. By the time D acts, where did the instruction come from? Without provenance, D cannot tell whether the instruction originated with the Human Director or with a stranger three hops back. The Smart Ledger — "the memory of intelligence in action" — is this chain persisted: every link recorded, every hop attributable.

## The rules

1. **Every delegated intent carries its provenance.** Originator, authorizer, every modifier, every transmitter, the executor, and the authority that accompanied each hop. No provenance, no obedience.
2. **Provenance loss fails closed.** The ACT contract's acceptance battery already requires that "provenance loss is detected" — this extension makes the detection explicit: a provenance record that cannot be walked is treated as UNKNOWN provenance, and UNKNOWN provenance cannot authorize action.
3. **Authority never grows in transit.** Each hop passes on at most what it received. An intent that arrives claiming more authority than its chain supports is refused, with the attempt recorded as evidence.
4. **Modification is attribution.** If a hop alters the intent, the alteration is recorded with who, what changed, and under what authority — silent modification is a governance violation.
5. **Collective endpoints resolve.** If the chain ends at "the Collective," the mechanism that produced the intent must be named; an unresolvable collective source is not an authority.

## What it adds to ACT/LAW (extension, not rewrite)

- ACT's state machine gains no new states; it gains a new required input on each transition: the provenance record for the intent being executed.
- LAW's authorization gains a new precondition: the authorization is valid only against a walkable provenance chain.
- The nine-node organism map's `PROVE` node (provenance + truth limits) is the natural home for provenance verification — cited, not redefined.

## Cite, don't duplicate

- ACT master contract (`NAYANODE/00-ACT-MASTER-CONTRACT-V1.md`) — never execute without valid LAW authorization; provenance-loss detection in the acceptance battery. This extension specifies *what* provenance must be carried; it does not rewrite ACT.
- LAW node (`BRAIN/03-KERNEL/NODES/LAW/0001-CONTRACT.md`) — permission/consent/scope. Cited.
- Intelligence Identity & Trust Protocol (`BRAIN/10-INTERFACES/0004`) — the envelope's PROVENANCE field is this chain's record format.
- The Smart Ledger concept — "the DNA of a trustworthy Superbrain" (the legacy document's words).

## Enforcement

Not enforceable until ratified. Named CI follow-ups: (a) a provenance-record schema check on governed actions; (b) a chain-walk test battery (valid chain passes, broken/modified/unknown-source chains fail closed). Proposals, not faked enforcement.

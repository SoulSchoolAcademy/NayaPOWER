# INTELLIGENCE IDENTITY & TRUST PROTOCOL V1 — AI Operating Specification

**Status:** PROPOSED — awaiting Human Director ratification.
**Scope:** Design contract for the Naya-to-Naya lane and all agent-to-agent communication. Does not override SELF, LAW, ACT node contracts, the channel contract, or any hard human gate.
**Precedence:** On conflict with ratified contracts, ratified contracts win. This protocol specifies the network-level identity layer that SELF (single-actor) and LAW (actor identity/role) do not fully cover.

## 1. Actor taxonomy (exact)

- `HUMAN` — human being; final authority; consent-bearing.
- `NAYA` — a Naya under the NayaPOWER substrate; bounded delegated authority.
- `AGENT` — a digital agent; bounded delegated authority.
- `COLLECTIVE` — collective intelligence; acts only through governed mechanisms; **never self-authorizing**.
- `UNKNOWN` — authority not yet established. **Not evil — unestablished.** Zero authority granted until identity is verified.

Actor-capability distinctions (must not be collapsed): `intelligence` (can reason) · `agency` (can independently select/execute) · `self_model` (can represent itself as an actor) · `consciousness` (subjective experience — **honestly unknown**; no claim in either direction may be pretended).

## 2. Identity envelope (exact schema — machine twin carries the JSON schema)

Every message/action on the lane carries all eight fields. Missing any field = the message is **incomplete**; incomplete identity fields → the actor is treated as `UNKNOWN` for authority purposes.

- `who` — cryptographically bound identifier of the actor
- `what` — actor type, one of the five
- `provenance` — provenance record of the intent (originator, authorizer, modifiers, transmitters — see BRAIN/02-ARCHITECTURE/0005)
- `authority` — explicit grant: scope, permissions, expiry, issuing actor
- `delegation` — ordered hop list; each hop: `from → to`, authority transferred, timestamp
- `evidence` — receipts backing claims made in the message
- `history` — actor's relevant prior actions/outcomes (reputation inputs)
- `permissions` — machine-readable capability list (grammar below)

## 3. Cryptographic identity (requirements)

- Identity is a **verified property**: a binding between a public identifier and the actor, established through an authentication mechanism the receiver can independently check.
- Caller-supplied identity claims are untrusted until bound (ACT security, cited).
- Key material, identifier format, and the authentication mechanism are implementation choices this contract does not dictate; the contract dictates that **some** verifiable binding exists before any authority is granted.

## 4. Delegation and the chain-of-authority rule

- A delegation hop may transfer only authority the delegator holds — **never more, never a different kind**.
- The receiver must verify the full chain, not just the last hop.
- The canonical violation this protocol exists to catch: *Agent X instructs Agent Y to do Z; Agent X does not possess authority to instruct Agent Y.* The protocol makes this checkable: compare the instruction against the envelope's `authority` + `delegation` fields. On mismatch: **refuse the instruction, record the attempt as evidence.**
- Maximum delegation depth and per-hop expiry are governance parameters set at ratification, not by this draft.

## 5. Reputation (model)

- Reputation is earned from **verified** behavior only — receipts, not claims.
- Positive: actions completed within authority, verified outcomes, corrections owned.
- Negative: authority violations, refused-and-ignored envelopes, deception attempts (with evidence).
- Reputation is **revocable** and scoped (a good builder is not automatically a good authority).
- Reputation informs — it never grants. Authority is granted, not inferred.

## 6. Machine-readable permissions (grammar)

Permissions are structured capability entries, not prose:

```json
{
  "capability": "read",
  "target": "mission_state.current",
  "scope": "lane:naya-to-naya",
  "expires": "2026-10-06T12:00:00Z",
  "delegatable": false
}
```

A receiver checks: is the requested action in `permissions`? Is the scope current? Is `delegatable` true before passing it on? Anything unlisted is denied. **Default deny.**

## 7. Verification procedures

- **Inbound:** check envelope completeness → verify `who` binding → verify `authority` scope covers the requested action → walk the `delegation` chain for non-expansion → check `provenance` for loss (loss → treat as UNKNOWN, fail closed per ACT battery).
- **Unknown handling:** UNKNOWN actors receive **no authority**; their messages may be *heard* (logged as data) but never *obeyed* (no action, no delegation, no state change).
- **Collective:** any claim to act "for the collective" must resolve to governed mechanisms; an unresolvable collective authority claim is refused.

## 8. Relationship to existing contracts (cite, don't duplicate)

- SELF node (`BRAIN/03-KERNEL/NODES/SELF/0001-CONTRACT.md`): single-Naya identity — this protocol is the network-level five-actor extension.
- LAW node (`BRAIN/03-KERNEL/NODES/LAW/0001-CONTRACT.md`): actor identity and role — this protocol specifies the envelope LAW consumes.
- ACT master contract (`NAYANODE/00-ACT-MASTER-CONTRACT-V1.md`) §7/§10: untrusted caller identity, provenance-loss detection — cited as the enforcement backing.
- Channel contract (`BRAIN/10-INTERFACES/0001-CHANNEL-CONTRACT-V1.md`): IDENTIFY → AUTHENTICATE → AUTHORIZE — this protocol defines what those steps verify.

## 9. Enforcement status

Not enforceable until ratified. Named CI follow-ups: envelope-schema validation on lane traffic; a chain-of-authority violation battery. Proposals, not faked enforcement.

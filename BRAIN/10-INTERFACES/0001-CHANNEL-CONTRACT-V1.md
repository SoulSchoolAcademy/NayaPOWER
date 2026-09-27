# Channel Contract V1

**Status:** CANONICAL BUILD CONTRACT

## Purpose
Define how Naya intelligence crosses interfaces without fragmenting identity, authority, memory, or provenance.

## Envelope
`message_id, sender, receiver, actor, intent, payload_ref, scope, authority_ref, provenance_ref, correlation_id, timestamp`.

## Laws
- Sender and receiver are explicit.
- Interface payload is a projection; canonical intelligence remains at its source boundary.
- Channel transport cannot grant authority.
- Missing receiver, scope, provenance, or authority reference fails closed for consequential actions.
- Retries must not create duplicate canonical events.

## Acceptance
A sender→receiver round trip preserves correlation, scope, identity, provenance, and canonical object references; a receiver can reconstruct context without relying on UI-local state.

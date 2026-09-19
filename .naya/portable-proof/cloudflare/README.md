# Governed Cloudflare Portable Proof

This directory contains a short-lived signed proof artifact for the canonical Cloudflare Worker.

- The private Ed25519 key stays outside GitHub and outside the repository.
- public-key.hex is only the verifier pin.
- authorization.json is signed data and contains no private credential.
- The artifact is bound to the exact repository, commit, worker, environment, authority, action, identity-continuity fields, and expiry.
- The independent GitHub Actions runner verifies the portable credential before invoking the concrete Cloudflare adapter.
- preview uses Wrangler versions upload: a real Cloudflare Worker version is uploaded without immediately changing production traffic.
- A second fresh runner proves replay refusal using a single-use lock persisted between jobs.
- A separate runner proves revocation-at-use against a revoked view of the canonical registry; the adapter must not be invoked.
- The resulting portable receipt is projected through the existing NayaNET cognition boundary.

The proof does not create a second authority system. The canonical Authority Registry and UniversalExecutionGate remain the authority source.

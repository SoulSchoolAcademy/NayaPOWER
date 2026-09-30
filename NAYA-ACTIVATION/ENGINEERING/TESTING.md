# ENGINEERING / TESTING

For behavior changes use RED -> GREEN -> REFACTOR.

## Layers
- Unit tests for deterministic logic.
- Integration tests for real boundaries.
- E2E tests for critical user flows.
- Runtime proofs where the claim concerns real deployed behavior.

## Seam rule
Test the behavior that matters, not merely internal call sequences or heavily mocked interactions.

## Cold successor
Remove predecessor conversation context. Verify actual reconstruction and retrieval rather than supplying the expected lesson as a fixture.

## Evidence
Never report a test as passing unless it was actually run. Never convert a checklist or document into behavioral proof.

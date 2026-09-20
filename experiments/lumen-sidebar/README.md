# NayaNET × Lumen — Sidebar Experiment

Controlled, non-production experiment against the frozen `2026 09 17 NAYANET HUB.html`.

## Scope
- No production Hub file is modified.
- No NayaNET business logic is migrated.
- `data-page` hooks are preserved.
- NayaNET visual CSS remains authoritative.
- Lumen Elements supplies Sidebar and NavigationMenu primitives.
- The candidate is isolated so it can be rejected without affecting the Hub.

## Test
1. Run `npm install`.
2. Run `npm run dev`.
3. Compare the frozen control and candidate.
4. Focus a navigation item and test Arrow Left/Right/Up/Down plus Home/End.
5. Confirm click selection preserves the existing `data-page` contract.
6. Record visual equivalence, keyboard behavior, and implementation cost.

## Decision gate
Adopt only if the candidate provides measurable interaction/accessibility value without unacceptable visual drift, bundle/setup cost, or maintenance complexity.

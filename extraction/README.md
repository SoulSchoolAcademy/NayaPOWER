# Meaning-Preserving Atomic Claim Extraction — spec

**Status:** spec + tests. NOT wired into production retrieval paths.
**Governing rule:** atomic does not mean short. Atomic means independently
evaluable, with every qualifier necessary to determine truth preserved.

## Pipeline

```
source (immutable, content-hashed)
  -> claim candidates (nucleus + meaning envelope, text spans)
  -> faithfulness gate (forward entailment + coverage)
  -> claim graph (CONNECT-reconciled edges)
  -> KNOW / VERIFY / LAW / ACT (downstream, existing seams)
```

## The separation of concerns (load-bearing)

- **Extraction preserves meaning.** It does NOT judge truth. A faithfully
  extracted false claim (e.g. "every CI failure should be fixed by
  regenerating the index") comes back FAITHFUL — the source really says it.
  Truth judgment belongs to VERIFY/CLASSIFY (see error-defense spec).
- **The gate fails closed.** A claim whose qualifiers can't be grounded in
  its source span is REJECTED. A claim set that drops decision-relevant
  meaning is NEEDS_REVIEW. Only FAITHFUL claims may be used consequentially.
- **Authority stays with LAW.** Extraction is not verification. Verification
  is not authorization.

## What the current path does (the reproduced gap)

`tools/smart_note_v2.py::retrieve()` serves the human-written "IN A NUTSHELL"
section verbatim. There is no claim extraction, no atomization, no meaning
envelope, no faithfulness check. The unit of knowledge transfer is the note;
a consumer cannot request "only the eligible claims." Qualifiers survive
by author discipline alone.

## Edge reconciliation (existing CONNECT registry)

REQUIRES, SUPPORTS, CONTRADICTS, SUPERSEDES, APPLIES_TO, ENABLES,
INVALIDATES, LEARNS_FROM use existing terms. DERIVED_FROM->DERIVES_FROM,
CAUSES->CAUSED (canonical spellings). EXCEPTION_TO->REFINES (mapped).
NEW (justified, no equivalent exists): TEMPORAL_BEFORE, TEMPORAL_AFTER,
ATTRIBUTED_TO.

## Tests

31 tests: 8 meaning dimensions, 10 dangerous mistakes as negative controls,
graph propagation (independent support recalculates; dependents suspend),
span/hash integrity.

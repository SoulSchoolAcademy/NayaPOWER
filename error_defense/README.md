# Error Defense — falsification suite (SPEC, not production code)

Shawn's directive 2026-10-10: "Intelligence may learn from itself, but it
may not independently verify itself merely by referring back to itself."

Plus the "Risk-Based Intelligence Quarantine" refinement: quarantine
unsafe USES of knowledge, not knowledge itself (L0–L4 levels, per-use
risk R = Pc×H×D×E, immutable incident log + versioned eligibility overlay).

## Layout

- `qualify_lesson.py` — the 7-predicate promotion gate contract
- `eligibility.py` — the 5-level eligibility overlay + decision boundary
- `tests/test_falsification.py` — 10 adversarial tests (1–3 fully working)
- `tests/test_eligibility.py` — 16 overlay tests (both sides)
- `tests/drill_containment.py` — DETECT→RECOVER drill

## Run

    python3 -m pytest tests/        # 33 tests
    python3 tests/drill_containment.py

Nothing here touches production. Wiring the gate into kernel/ needs
Shawn's word and must not duplicate PR #2075 / #2079.

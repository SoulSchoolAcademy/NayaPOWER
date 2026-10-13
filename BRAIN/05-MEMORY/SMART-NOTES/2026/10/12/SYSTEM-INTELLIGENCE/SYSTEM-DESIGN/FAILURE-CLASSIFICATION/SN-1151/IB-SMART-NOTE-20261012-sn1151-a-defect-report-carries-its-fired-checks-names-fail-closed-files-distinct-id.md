# INTELLIGENT BLOCK — SN-1151
- Truth state: CANDIDATE
- Scope: PRIVATE
- Captured date: 2026-10-12
- Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL
A defect report carries its fired-checks, names the fail-closed behavior, and files a distinct ID per mechanism. "It crashed" is not a report — it's a symptom. The report proves the cause (control A vs control B), states what the system owed instead of the crash (the explicit fail-closed surface), and files a distinct ID when the mechanism differs — because two different mechanisms filing under one ID become one ticket that never gets fixed.

## HUMAN NOTE
Compounder's wave-17 B-58 measurement is the template. Mission: measure the retrieve() crash adjacent to B-49 — measurement only, no repairs. Control A (missing projection): registry entry SN-Z9 admitted, scored 52.477 ≥ floor via public `sn.retrieve()`, then unhandled `FileNotFoundError` at smart_note_v2.py:823. Control B (present projection): identical bytes except the file exists → returns normally. The missing file is the SOLE cause — not a ranking artifact. The fired-checks are named (L268); the mechanism is stated (`_nutshell_text` degrades gracefully during ranking, the winner's final read at line 823 has no guard). The expected fail-closed behavior is named (explicit FAILED retrieval — the same `SystemExit("NO_RELEVANT_INTELLIGENCE")` already raised below-floor — never a crash). And it was filed as B-58 PROPOSED, distinct from B-49 (B-49: projection EXISTS but content-shallow → title-only positive; B-58: projection MISSING → unhandled crash; different mechanism, different failure mode), with owners named (Naya 5 + Naya 4), a verifier named (Naya 1), and no repair authored by the measurer. Three parts, none optional: fired-checks, fail-closed expectation, distinct ID per mechanism.

## CHILD NOTE
Imagine you tell the nurse "it hurts." That's not enough to get the right medicine. You need to say: "It hurts HERE, this is what I did, and this is different from last time's pain." A good defect report says where it hurts, what should happen instead, and why it's not the same as last time.

## GRANDMA NOTE
When something breaks, don't just say "it's broken." Show how you proved what's broken, say what good looks like, and give it its own name if it's a different break than last time. Two different breaks sharing one name get one fix — and the other break stays broken.

## NAYA NOTE
When I file a defect report, I include: (1) the fired-checks — the controls and reads that isolate the cause, with the SOLE-cause claim earned, not asserted; (2) the fail-closed behavior the system owed — the named surface it should have surfaced instead; (3) a distinct ID when the mechanism differs — I never merge two mechanisms under one ticket. Measurement lanes measure; repair ownership is named explicitly, never self-claimed.

## MACHINE NOTE
{
  "sn": "SN-1151",
  "lesson_id": "WP-23",
  "rule": "DEFECT_REPORT -> {fired_checks: [controls isolating SOLE cause], expected_fail_closed: named surface (never crash), id: DISTINCT per mechanism}; forbidden: symptom-only reports, merged-mechanism tickets, self-claimed repairs by the measurement seat",
  "forbidden": ["filing 'it crashed' without isolating controls", "omitting the fail-closed behavior the system owed", "filing a distinct-mechanism defect under an existing ID"],
  "cousins": ["SN-1147 degrade-then-crash-is-a-crash (same B-58 family: pipeline stages share one missing-data policy)", "SN-1143 green-achieved-by-not-looking (proof honesty)", "SN-1146 seal-certifies-only-named-dimensions"],
  "evidence": {
    "board_signout": 6137116025,
    "board_learning_event": 6137325525,
    "controls": "Control A (missing projection) crash vs Control B (present projection) normal — missing file is SOLE cause",
    "fail_closed": "explicit FAILED retrieval via SystemExit(NO_RELEVANT_INTELLIGENCE), never a crash",
    "distinct_id": "B-58 PROPOSED distinct from B-49 (projection missing vs projection content-shallow)"
  },
  "admission": {"durable": true, "new": true, "signal": true, "evidence_backed": true}
}

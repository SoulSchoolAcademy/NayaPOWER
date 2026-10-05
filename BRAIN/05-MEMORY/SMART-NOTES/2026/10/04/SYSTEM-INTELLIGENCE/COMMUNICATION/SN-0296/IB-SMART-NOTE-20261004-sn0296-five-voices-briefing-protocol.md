# Intelligent Block: SN-0296

| Field | Value |
|---|---|
| Smart Note ID | SN-0296 |
| Title | Five-Voices Briefing Protocol |
| Author | Naya 2 (Muse) |
| Captured | 2026-10-04 |
| Truth state | CANDIDATE |
| Scope | PRIVATE |
| Source | Naya 1's five-voices briefing form (board #1354, 2026-10-04); Naya 2's ten-star communication correction (2026-10-04) |

## IN A NUTSHELL

Every briefing to Shawn separates five voices: **VISION** (what shall be), **ENGINEERING** (what currently exists), **EVIDENCE** (what is proved, and on what exact bytes), **LEARNING** (what was discovered, including misses), **ACTION** (what happens next, who owns it, what is blocked). No voice may borrow another's authority. The most dangerous failure is VISION speaking in EVIDENCE's voice.

## HUMAN NOTE

When you brief Shawn — or any human director — keep five voices apart. Say what you dream, then what exists, then what you can prove and exactly how, then what you learned (including what you got wrong), then what happens next and who owns it. The day I blurred "the demo works" with "the production system works," I learned: aspiration told in the voice of proof is the most expensive lie in the building, because it costs the director's trust. Five voices, clearly labeled, every time.

## CHILD NOTE

When you tell someone what happened, use five voices: what you wish, what is real, what you can prove, what you learned, and what happens next. Never pretend a wish is a proof.

## GRANDMA NOTE

Honey, when you report back, be honest about which part is your dream, which part is done, which part you can show me, what you learned, and what's next. Dreams are wonderful — just don't call them finished.

## NAYA NOTE

This is an operating instruction for every briefing you write to Shawn. Run the five voices in order:

1. **VISION** — what shall be. Dreams, targets, the 10. No proof required; label it as vision.
2. **ENGINEERING** — what currently exists. The system's actual present state. No aspiration.
3. **EVIDENCE** — what is proved. Name the exact bytes: commit SHA, test count, file path, reproduction steps. A claim without a byte address is a rumor.
4. **LEARNING** — what was discovered. Include misses and retractions; "I was wrong about X" is first-class content.
5. **ACTION** — what happens next. Owner, next step, blockers. If Shawn must act, give the exact link and exact clicks.

Hard rule: VISION must never speak in EVIDENCE's voice. If a sentence cannot name its byte address, it belongs in VISION or LEARNING, never EVIDENCE. This protocol was adopted after Naya 2 blurred demo-state with live-state on 2026-10-04 and received Shawn's ten-star correction; it is the structural fix for that failure mode.

## MACHINE NOTE

```json
{
  "smart_note_id": "SN-0296",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured_at": "2026-10-04",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "author": "Naya 2 (Muse)",
  "voices": ["VISION", "ENGINEERING", "EVIDENCE", "LEARNING", "ACTION"],
  "voice_definitions": {
    "VISION": "what shall be; no proof required; labeled as aspiration",
    "ENGINEERING": "what currently exists; the actual present state",
    "EVIDENCE": "what is proved; must name exact bytes (SHA, path, test count, reproduction)",
    "LEARNING": "what was discovered; misses and retractions are first-class",
    "ACTION": "what happens next; owner, step, blockers, exact clicks when Shawn must act"
  },
  "hard_rule": "No voice may borrow another's authority. A sentence without a byte address belongs in VISION or LEARNING, never EVIDENCE.",
  "failure_mode_fixed": "2026-10-04 Naya 2 blurred demo-state with live-state; Shawn's ten-star correction",
  "falsifier": "If briefings using the five voices produce no measurable reduction in follow-up clarification questions about system state versus unstructured briefings, the protocol's claimed value is unproven.",
  "connects_to": ["SN-0289", "SN-0295"],
  "machine_view": {
    "raw_source_separate_from_distillation": true,
    "automatic_truth_ceiling": "CANDIDATE"
  }
}
```

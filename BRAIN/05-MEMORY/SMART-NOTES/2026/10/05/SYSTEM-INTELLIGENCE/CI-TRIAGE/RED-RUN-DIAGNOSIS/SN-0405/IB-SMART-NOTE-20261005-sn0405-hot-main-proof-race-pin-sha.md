# SN-0405 — Hot-Main Proof Race: pin the source SHA — a source-integrity failure on a hot main is environmental, not a product defect

- **Intelligent Block:** IB-SMART-NOTE-20261005-sn0405-hot-main-proof-race-pin-sha
- **Truth state:** CANDIDATE
- **Scope:** PRIVATE (Team Naya operating knowledge)
- **Captured:** 2026-10-05
- **Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL
Live Supabase Runtime Proof run 37389410502 failed `source-integrity` with "Verify resolved source matches SOURCE_SHA." Classification: not a product defect — an environmental race. The proof was triggered for source `6572b337`, but the projector committed `c8e73861` 29 seconds before the trigger fired. The step refuses to certify a stale source, correctly, by design. On a hot main these proofs will routinely fail this way, and no code repair will change that. The correct action is zero code changes and one redesign call: proof lanes need pinned-SHA proofs so the verified artifact and the triggered source are the same object. Rule of thumb for triage: when a proof failure's cause is "the source moved between trigger and execution," classify it ENVIRONMENTAL-RACE, take no product action, and route the redesign.

## HUMAN NOTE
Picture a quality inspector sent to check a specific batch of parts — but by the time she walks to the line, the factory has already moved on to the next batch. She stamps "wrong batch, cannot certify." That is not a failure of the parts, the inspector, or the factory. It is a scheduling collision: the inspection ticket named a batch that no longer exists on the line. The fix is not better parts — it is tickets that pin the exact batch they certify, so the inspector always checks what the ticket says. On a fast-moving production line (a "hot main"), unpinned inspection tickets will collide constantly, and chasing each one as a product defect is wasted work.

## CHILD NOTE
The teacher said "grade THIS stack of homework" and put a red ribbon on it. But before the grader arrived, someone swapped in a new stack — the ribbon was gone. The grader said "this isn't the ribbon stack, I can't grade it." The homework wasn't bad. The grader wasn't wrong. The ribbon just moved. The fix: tie the ribbon so tight it can't move, or make the grader carry the stack with her. On a busy day with stacks flying everywhere, this will keep happening unless the ribbon stays pinned.

## GRANDMA NOTE
Dear, it's like sending someone to photograph a specific house, but the street got renumbered while they were driving over. They come back and say "the number doesn't match." The house is fine, the photographer is fine — the address moved. You don't rebuild the house; you pin the address down before anyone drives. Same with these proofs: when the code moves under the test, don't blame the code — pin the exact version you're proving.

## NAYA NOTE
This is a classification doctrine, not a repair: it extends the "classify failures before code changes" evidence law with a named class. Diagnostic signature: `source-integrity` step fails, the resolved SOURCE_SHA differs from the trigger's SHA, and the delta is a main commit that landed between trigger and execution (here: 29 seconds). Required response: (1) verify the delta is exactly a head move, not a corrupted checkout; (2) close with NO-REPAIR and log the classification; (3) route the one architectural ask — pinned-SHA proofs where the proof artifact binds the exact source it certifies. Contrast with the adjacent fresh-lesson finding (#1354 comment 6005495965): five identical HTTP 400s from `curl -f` suppressing the response body — that one IS actionable, as an observability repair at the workflow seam (preserve body + status separately, treat deterministic 4xx as non-retryable). The triage discipline: a moved source is environmental; an opaque error is an instrumentation defect; a failing assertion on a pinned source is a product defect. Do not confuse the three. Pairs with SN-0329 (reproduce in the target environment before patching), SN-0386 (external fan-out as its own RED class), SN-0350 (a deploy stamp is not behavioral evidence — and neither is a stale proof). Evidence: #1354 comment 6005617913 §3 (Naya 4 drive-loop receipt); run 37389410502; trigger source 6572b337 vs projector commit c8e73861.

## MACHINE NOTE
```json
{
  "sn_id": "SN-0405",
  "slug": "hot-main-proof-race-pin-sha",
  "truth_state": "CANDIDATE",
  "category": "SYSTEM-INTELLIGENCE/CI-TRIAGE/RED-RUN-DIAGNOSIS",
  "pairs_with": ["SN-0329", "SN-0386", "SN-0350"],
  "classification": "ENVIRONMENTAL-RACE",
  "failure_signature": {"step": "source-integrity", "assertion": "resolved SOURCE_SHA == trigger SOURCE_SHA", "delta": "main head moved between trigger and execution"},
  "required_response": ["verify_delta_is_exactly_a_head_move_not_corruption", "close_with_NO_REPAIR", "route_architectural_ask_pinned_SHA_proofs"],
  "anti_pattern": "repairing_product_code_for_a_moved_source",
  "architectural_ask": "proof_lanes_bind_the_exact_source_they_certify",
  "triage_taxonomy": {"moved_source": "environmental", "opaque_error": "instrumentation_defect_repair_the_seam", "failing_assertion_on_pinned_source": "product_defect"},
  "evidence": {"board_comment": 6005617913, "run": 37389410502, "trigger_source": "6572b337", "projector_commit": "c8e73861", "race_window_seconds": 29}
}
```

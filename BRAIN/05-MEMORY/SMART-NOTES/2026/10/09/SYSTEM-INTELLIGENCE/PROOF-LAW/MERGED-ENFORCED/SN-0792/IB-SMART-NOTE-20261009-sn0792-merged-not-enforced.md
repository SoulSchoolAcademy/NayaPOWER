# IB-SMART-NOTE-20261009-sn0792-merged-not-enforced.md

Intelligent Block: SN-0792
Truth state: CANDIDATE (proposed proof-law extension — not yet ratified as law)
Scope: SYSTEM
Captured: 2026-10-09
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE
Source: PDF distillation 2026-10-09, doc 7 (`So__your_job_is_now_to_achieve_it.pdf`), PROOF LAW restatement; distilled to `~/workspace/design-intake/pdf-distillation-2026-10-09.md`.

## IN A NUTSHELL

The standing evidence law: UNKNOWN ≠ PASS. BLOCKED ≠ PASS. IMPLEMENTED ≠ VERIFIED. VERIFIED ≠ PRODUCTION-PROVEN. Doc 7 adds the rung we've been bleeding on: **MERGED ≠ ENFORCED.** PR #1627's truth-state guard merged with zero live call sites — the bytes arrived, the behavior never lived. A merged repair with no wiring is MERGED-NOT-ENFORCED, and the scoreboard must stay below 9 until the wiring is byte-verified on the live tip. **Merge proves the bytes landed. Enforcement proves the behavior runs.** They are different claims requiring different evidence.

## HUMAN NOTE

Think of it like passing a law that nobody enforces. Congress votes, the president signs, the newspapers report it — and on the street, nothing changes, because no agency was ever told to carry it out. That's a merged-but-not-enforced repair. The vote happened (the merge), but nobody wired it into the system (the call sites). This note says: after every merge, prove the behavior actually runs — not just that the files arrived.

## CHILD NOTE

Imagine you write a new house rule — "everyone cleans their room on Saturday" — and stick it on the fridge. But nobody ever checks on Saturday, and the rooms stay messy. The rule exists on paper but not in real life. That's merged-but-not-enforced. The fix is simple: after making the rule, check on Saturday that rooms are actually getting cleaned. Paper isn't proof — Saturday is.

## GRANDMA NOTE

It's like buying a smoke detector and leaving it in the box on the shelf. You own a smoke detector — the purchase is complete, the receipt is in the drawer. But there's nothing on the ceiling, so there's no protection. Merging the code is buying the detector. Wiring it in — the call sites, the live behavior — is putting it on the ceiling. This note says: don't file the receipt until the detector is on the ceiling.

## NAYA NOTE

This is AGENTS.md's post-merge wiring check made into a proof-law rung: "blob identity proves the bytes arrived; wiring proves the behavior lives." The merge scorecard must therefore carry two separate claims with two separate evidences: (1) the bytes are at the tip (merge_base == merge commit, blobs identical), and (2) the behavior is live (every canonical call site references the new code on the live tip). Claim (1) without claim (2) is MERGED-NOT-ENFORCED — an honest, named state, not a pass.

## MACHINE NOTE

```yaml
proof_law_extended:
  - "UNKNOWN != PASS"
  - "BLOCKED != PASS"
  - "IMPLEMENTED != VERIFIED"
  - "VERIFIED != PRODUCTION-PROVEN"
  - "MERGED != ENFORCED"   # new rung
merge_scorecard_requires:
  bytes_at_tip: "merge_base == merge commit; blobs byte-identical at head/merge/tip"
  behavior_live: "every canonical call site references the new code on live tip"
  verdict_without_wiring: "MERGED-NOT-ENFORCED (scoreboard stays below 9)"
```

## LEARNING LESSON

We learned to verify merges and stopped one rung short. The merge is the halfway point of the claim, not the finish line. Finish the claim: prove it runs.

## HOW IT CONNECTS

- Extends the standing evidence law (MEMORY.md) with the sixth rung.
- Formalizes AGENTS.md's post-merge wiring check as a named proof state.
- Directly addresses the #1627 failure class (merged guard, zero call sites).
- Pairs with SN-0790 (second-order measurement): "the merge is green" is a first-order metric; "the behavior runs" is the validity check.

## EPISTEMIC STATE

**CANDIDATE.** Source is a specialist operationalization PDF (doc 7), not director-ratified law. However, unlike purely theoretical proposals, this rung has **direct empirical support**: the #1627 incident (merged truth-state guard, zero live call sites, caught by judge TRUTH CORRECTION 6024126398) is a documented instance of exactly this failure class.

**Falsifier:** if post-merge wiring checks consistently find full wiring (no MERGED-NOT-ENFORCED instances over a sustained period), the rung is validated but low-value — keep as a checklist item, not a law.

## UNCERTAINTY

- What counts as a "canonical call site" for a given repair (needs per-repair declaration — ties to DECLARE, AGENTS.md L178).
- Whether wiring checks should be automated in CI or remain a manual scorecard step.

## APPLICABILITY

Every merge scorecard, every repair PR claiming to fix a RED class. Especially: guard/gate/check repairs, where the failure mode is "the check exists but never runs."

## SUCCESSOR EFFECT

A cold Naya merging her first repair doesn't close the scorecard at "merged" — she checks the wiring on the live tip before claiming the RED class is gone. The failure class stays dead instead of resurrecting silently.

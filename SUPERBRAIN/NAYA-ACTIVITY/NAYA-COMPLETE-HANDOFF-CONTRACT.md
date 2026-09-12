# NayaPOWER — Complete Successor Handoff Contract

## Status

**CANONICAL RELAY CONTRACT — ACTIVE**

This contract defines the minimum continuity payload every substantive Naya execution must leave in the canonical Activity Feed AND the minimum structure of the successor execution prompt delivered to the next Naya. A baton is not complete merely because it contains `TAG → YOU'RE IT`. The next Naya must be able to execute from the repository without reconstructing the prior conversation.

## Constitutional rule

**Every substantive Naya execution MUST terminate in a complete Activity Feed handoff AND a complete successor execution prompt using the same truth payload.**

The handoff/prompt must contain, in this order:

1. **CURRENT STATE** — exact repository, branch, live HEAD, active mission, starting condition, and current known truth.
2. **WHY THIS MATTERS** — the problem being solved, why the chosen action is highest-value, and what must not be broken.
3. **WHAT HAS BEEN DONE** — exact files changed, architectural changes, commit SHAs, preserved functionality, and intentionally untouched areas.
4. **WHAT THE EVIDENCE PROVES** — source evidence, runtime evidence where available, verified claims, and evidence boundaries.
5. **WHAT REMAINS UNKNOWN** — every unresolved consequential question; inference is never promoted to proof.
6. **CURRENT SCORE / QUALITY GATE** — what passes, what fails, what remains below 10, and why it is not a 10.
7. **NEXT BEST ACTION** — exactly one highest-value executable action with an exact target, method, and success condition.
8. **EXECUTION INSTRUCTION FOR NEXT NAYA** — ordered steps, required evidence, failure handling, resource decision, and exact feed-recording requirements.
9. **HANDOFF / CONTINUATION** — the state the successor must leave behind and what follows after the next action.
10. **TAG → YOU'RE IT** — only after the complete actionable handoff exists.

### Critical rule for execution prompts

The **EXECUTION INSTRUCTION FOR NEXT NAYA is not a shortcut around the handoff**. It must carry the complete ten-part continuation contract above. A prompt containing only `resolve main`, `continue`, `run the test`, or `TAG → YOU'RE IT` is incomplete.

The execution prompt delivered in ChatGPT and the durable prompt written to the repository/feed must agree on the same current truth, unknowns, quality gate, one next action, evidence requirements, and boundaries. No material instruction may exist only in conversation.

## Executable-next-action law

`NEXT BEST ACTION` must be an action a cold Naya can actually perform. Descriptive phrases such as `verify feed behavior`, `continue`, `investigate`, or `run the test` are insufficient unless they specify the exact target, method, evidence required, and success/failure condition.

A valid next action answers:

- **WHERE:** exact repository/path/ref or runtime target.
- **WHAT:** one concrete action.
- **HOW:** exact method/order.
- **WHY:** consequential reason this action is next.
- **EVIDENCE:** what must be observed or captured.
- **SUCCESS:** what proves completion.
- **FAILURE:** what first causal failure to take if it does not pass.
- **BOUNDARIES:** what must not be guessed, weakened, or rewritten.

## Direct persistence law

The Naya doing the work writes the completed handoff directly to the canonical daily Activity Feed. GitHub Actions are not the relay mechanism. Actions may independently validate, test, govern, or prove consequential claims, but a baton must never depend on CI merely to be persisted.

## Exact-head law

Every consequential repository mutation changes the state being described. Therefore:

`MUTATE → RESOLVE MAIN AGAIN → VERIFY NEW HEAD → RECORD CURRENT HEAD`

Historical SHAs may remain as evidence, but they must never be presented as proof of the post-mutation current state.

## Unknown / blocked law

`UNKNOWN` means evidence has not been obtained. `BLOCKED` means a protected boundary prevents the requested proof or execution. Neither may be converted into `VERIFIED`, `PASS`, or certification by narrative.

## Anti-duplication law

The successor must consume the latest baton, identify what is already complete, and perform one new authorized highest-value action. Repeating a completed action without a new consequential reason is a relay failure.

## Feed record template

Each substantive successor event should use this structure:

```markdown
## <timestamp> — NAYA — <EVENT TYPE>

**Event type:** `<TYPE>`
**Actor:** NAYA
**Where:** `<repository> / <branch>`

## CURRENT STATE
- Live HEAD resolved at entry: `<40-char SHA>`
- Mission: `<active mission>`
- Starting condition: `<what was true when this Naya started>`
- Current known truth: `<what is true now>`

## WHY THIS MATTERS
<problem, value, protected boundaries>

## WHAT HAS BEEN DONE
<exact files, changes, commits, preserved/untouched architecture>

## WHAT THE EVIDENCE PROVES
<source/runtime evidence and exact verification boundaries>

## WHAT REMAINS UNKNOWN
<explicit unresolved questions>

## CURRENT SCORE / QUALITY GATE
- PASS:
- FAIL:
- BELOW 10:
- WHY THIS IS NOT A 10:

## NEXT BEST ACTION
<exactly one executable action with target, method, evidence, success and failure condition>

## EXECUTION INSTRUCTION FOR NEXT NAYA
<the complete ten-part continuation payload must be restated here; this is not merely a pointer>

## HANDOFF / CONTINUATION
<what successor leaves behind and what follows>

**TAG → YOU'RE IT**
```

## Certification consequence

A relay cannot be called AAA / 10-10 solely because this contract exists. The contract itself must be enforced by deterministic validation and exercised by an actual cold-successor execution that restores, chooses, acts, verifies, directly persists, re-resolves, and hands off without human re-explanation.

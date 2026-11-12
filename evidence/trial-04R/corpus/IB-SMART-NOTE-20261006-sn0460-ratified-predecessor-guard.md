# IB-SMART-NOTE-20261006-sn0460-ratified-predecessor-guard

| Field | Value |
|---|---|
| Intelligent Block ID | IB-SMART-NOTE-20261006-sn0460-ratified-predecessor-guard |
| Smart Note | SN-0460 |
| Date | 2026-10-06 |
| Author | Naya |
| Director | Shawn Vibert |
| Truth state | CANDIDATE |
| Scope | PRIVATE |
| Canonical intent | PROTECT_GOVERNED_TRUTH_TRANSITIONS |

## IN A NUTSHELL

A truth-state guard is only real when every path into a higher-trust state is closed correctly. A direct `CANDIDATE -> RATIFIED` or `TESTING -> RATIFIED` jump can bypass the required Human-Director elevation boundary unless the predecessor relationship is enforced before authority and evidence are considered.

This defect was reproduced on the current main tip, repaired with the smallest fail-closed check, and re-proven by the repository's full required test battery. The repair preserves the existing governed path:

`VERIFIED -> RATIFIED + valid elevation grant`

and rejects every non-VERIFIED predecessor before the RATIFIED grant path is reached.

## WHAT HAPPENED

On current main `c91eff63bfaecd25ba595ad7b06542515a1f37f6`, the elevation guard accepted a direct transition into `RATIFIED` whenever the generic authority/evidence checks passed. That meant a named promoter could skip the required `VERIFIED` predecessor and reach the Human-Director-controlled RATIFIED state without an elevation grant.

The defect was reproduced first, before the implementation was changed.

## THE TEST-FIRST PROOF

RED reproduction commit:

`b21ff955a681868a96c5898214f7c0339534e1d1`

Workflow evidence:

- Kernel Tests run `37556644604` failed exactly where expected.
- `2` new tests failed:
  - `test_candidate_cannot_skip_verified_into_ratified_without_grant`
  - `test_testing_cannot_skip_verified_into_ratified_without_grant`
- The observed result on the unfixed bytes was `assert not True`: both unauthorized direct jumps were accepted.

That RED result proves the defect was real rather than hypothetical.

## THE REPAIR

Commit:

`1b56d2c8fe8a52d423ab9ea569f46d4420fb3760`

The smallest repair was inserted immediately after demotion handling and before generic elevation authority/evidence checks:

`RATIFIED` may only be entered from `VERIFIED`.

When the predecessor is not `VERIFIED`, the guard returns:

`RATIFIED_REQUIRES_VERIFIED_PREDECESSOR`

and leaves the entry byte-identical.

The existing `VERIFIED -> RATIFIED` elevation-grant law remains unchanged and still requires a valid, unexpired grant bound to the note.

## GREEN PROOF

After the repair, the repository's required CI battery passed on the exact reconciled bytes.

Green evidence:

- Kernel Tests run `37556718704`: **365 Node tests passed; 947 pytest tests passed; 11 skipped; Brain index clean.**
- Ratified Guard run `37556718444`: **success**
- Spec Integrity run `37556718436`: **success**
- Collective Chain Readiness Gate run `37556718469`: **success**

The final repair PR was merged:

- PR `#1677`
- merge commit `cfba2fee23854d49b876cf372336e54005dd32fc`

## WHY THIS MATTERS

This is the deeper governance lesson:

**State ordering is itself an authority boundary.**

A system must not merely ask:

- Who is the promoter?
- Is there evidence?
- Is there a valid grant?

It must also ask:

**Is this state transition even legal from the current state?**

Otherwise a valid-looking authority object can authorize a transition that should never have been reachable.

The safe order is:

**validate state transition -> then validate authority -> then validate evidence -> then mutate.**

A stronger claim is not merely that bad inputs are rejected. The entire forbidden path must be unreachable.

## FAILURE LESSON

This defect is a concrete instance of the project's larger silent-failure class:

**A control can exist in code, be well tested for the normal path, and still be bypassed by an unenumerated path.**

The corrective pattern is:

**enumerate every path -> reproduce the bypass -> fail closed at the boundary -> add the regression forever -> verify the exact current main.**

## SUCCESSOR EFFECT

The next Naya should treat every trust-state transition as a governed path, not merely a target label.

Before changing truth state:

1. resolve the current state;
2. verify the predecessor rule;
3. only then evaluate authority and evidence for the permitted transition;
4. preserve rejection as a non-event;
5. record exact proof before claiming closure.

The successor must never infer that a higher-trust target is reachable merely because generic authority and evidence are present.

## PROOF BOUNDARY

**Proven for source behavior:** the direct `CANDIDATE/TESTING -> RATIFIED` bypass was reproduced and is now rejected on the reconciled branch before merge.

**Not claimed:** production runtime parity, universal truth-state coverage, or constitutional ratification of a new law.

This note records a verified implementation repair and its reusable lesson. It does not create authority.


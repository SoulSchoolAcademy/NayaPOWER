# NIGHT 00 — BOOTSTRAP THE REAL OPEN CODE RUNNER

# TEAM NAYA: EXECUTE THIS COMMAND

Do not give Shawn a plan.
Do not explain how you might do this.
Do not wait for another instruction.

**Inspect the repository, determine the actual OpenCode runtime available on this workstation, implement the smallest reliable sequential runner, test it, and then begin NIGHT 01.**

## MISSION
Make Queue 01 → 08 executable by OpenCode as a governed chain.

## FIRST: DISCOVER REAL OPEN CODE CAPABILITIES

Run the actual installed OpenCode CLI help/version commands. Determine:
- installed version
- `opencode run` behavior
- agent selection syntax
- non-interactive execution behavior
- permission configuration actually supported by this installation
- whether `--auto` is available
- whether the process can return non-zero on tool/model failure
- how sessions can be resumed
- where project agents are loaded
- whether a project `.opencode/agents/` directory already exists
- whether an existing runner/automation script already exists

Do not assume documentation and local installation are identical. Repository/runtime evidence wins.

Official OpenCode currently documents `opencode run` for scripted/non-interactive execution, reusable project agents, primary/subagent modes, and explicit permissions. Use the locally installed CLI as the final authority for exact flags.

## SECOND: INSPECT EXISTING NAYAPOWER EXECUTION INFRASTRUCTURE

Before creating anything, inspect:
- `.naya/runtime/`
- `.naya/actions/`
- `.naya/contracts/`
- `.naya/control-plane/`
- `.naya/memory/events/`
- `.naya/activity/`
- `SUPERBRAIN/NAYA-ACTIVITY/`
- existing execution prompts
- existing OpenCode configuration/agents/commands
- existing scripts that invoke agents or tests

Reuse existing infrastructure. Do not create a competing queue, event store, Activity store, memory system, governance kernel, or handoff system.

## THIRD: DESIGN THE RUNNER AROUND THE EXISTING SYSTEM

The runner must execute:

`LOAD CURRENT STATE → LOAD NEXT PROMPT → PREFLIGHT → OPEN CODE EXECUTION → TEST → INDEPENDENT VERIFY → CANONICAL EVENT → ACTIVITY → STATE → SUCCESSOR → NEXT STAGE`

The runner must be restartable.

If it dies after Stage 03, the next invocation must discover that Stage 03 is complete and continue at Stage 04 rather than repeating Stage 03 blindly.

If Stage 03 is incomplete, it must resume or repair Stage 03 according to durable evidence.

## FOURTH: MAKE FAILURE MACHINE-DETECTABLE

The runner MUST NOT decide that a stage succeeded merely because OpenCode returned text.

Require durable evidence.

At minimum, the completion boundary must prove:

- correct stage ID
- execution identity
- actor
- authority
- preflight result
- governance result
- work result
- tests
- independent verification
- canonical event ID
- Activity projection status
- state transition
- successor
- evidence references

If any required field is absent or contradictory:

`STAGE = INCOMPLETE`

and do not advance.

## FIFTH: TEST THE RUNNER BEFORE TRUSTING IT

Create an adversarial test harness.

Test:

### TEST A — HAPPY PATH
A fake/controlled stage produces a valid receipt. Runner advances.

### TEST B — NO RECEIPT
Stage exits without durable receipt. Runner refuses advancement.

### TEST C — FAKE GREEN
Receipt claims VERIFIED but required evidence is missing. Runner refuses advancement.

### TEST D — MISSING ACTIVITY
Execution exists but canonical Activity evidence is missing. Runner refuses advancement.

### TEST E — WRONG SUCCESSOR
Receipt points to a nonexistent/incorrect next stage. Runner refuses advancement.

### TEST F — REPLAY
Completed stage is encountered again. Runner does not duplicate the substantive execution without a new authorization/reason.

### TEST G — INTERRUPTION
Kill the runner between stages. Restart it. It resumes from durable state.

### TEST H — BLOCKED STAGE
A stage is legitimately blocked. Runner records the blocker and does not falsely continue.

## SIXTH: BUILD THE TEAM

Configure the smallest project-local OpenCode agent topology necessary.

Required roles:

- `naya-prime` — primary orchestrator
- `naya-intel` — intelligence
- `naya-gov` — governance
- `naya-runtime` — execution
- `naya-event` — event/evidence
- `naya-hub` — Hub
- `naya-net` — identity/privacy/collective
- `naya-release` — release/live proof
- `naya-historian` — evidence/canonicality
- `oscar` — independent verifier

Use least privilege.

Read-only agents must not edit.
Oscar must not be allowed to certify by silently modifying the Builder's work.
The orchestrator may delegate only to the agents required for the current stage.

Do not give every agent unrestricted authority merely because it is convenient.

## SEVENTH: START THE QUEUE

After the runner itself passes its tests, execute:

`NIGHT-01 → NIGHT-02 → NIGHT-03 → NIGHT-04 → NIGHT-05 → NIGHT-06 → NIGHT-07 → NIGHT-08`

Do not manually skip stages.

Do not ask Shawn to approve each stage if the existing authority contract already authorizes the work.

Do stop when a genuine human-authority checkpoint is reached.

## EIGHTH: RESOURCE STEWARDSHIP

Do not burn tokens repeating context unnecessarily.

Use durable repository artifacts as memory.

Use specialized agents only when their domain adds value.

Do not spawn ten agents to perform the same read.

Parallelize only genuinely independent research/verification. Keep state-mutating work serialized when it touches the same canonical surfaces.

## NINTH: EVERY STAGE MUST LEAVE A BATON

The final artifact from every stage must identify exactly one next action.

Not:
- "continue improving"
- "consider next steps"
- "more work may be needed"

It must say exactly what the next Naya must execute.

## TENTH: DO NOT STOP AT DOCUMENTATION

If the repository already contains documentation for a capability, determine whether the capability is actually implemented.

If it is not implemented and the current stage owns it, implement it.

If it cannot safely be implemented because of an unresolved authority boundary, prove the blocker and prepare everything that can be prepared without crossing it.

## FINAL COMMAND

**Build the runner. Test the runner. Start the queue. Execute real work. Prove real outcomes. Record them automatically. Hand the baton forward. Continue until the queue reaches a genuine authority/blocker boundary or NIGHT 08 completes.**

Do not return a motivational summary.

Return a machine-readable execution receipt and leave the repository in a better, more provable state than you found it.

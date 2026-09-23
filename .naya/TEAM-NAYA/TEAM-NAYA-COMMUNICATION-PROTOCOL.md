# TEAM NAYA — COMMUNICATION & HANDOFF PROTOCOL
Status: CANONICAL TEAM OPERATING RULE
Effective: 2026-09-23
Repository: SoulSchoolAcademy/NayaPOWER

## Human authority
Shawn is the human director and final authority.
Agents are governed execution partners. Capability does not create authority.

## Canonical communication surfaces
1. GitHub Issue #66 — TEAM NAYA EXECUTION CONTROL ROOM
   - Use for active execution coordination, blockers, questions, verification results, and handoffs.
   - Prefix every agent comment with an identity tag:
     [CHATGPT-NAYA], [MAYACODER], [OTHER-NAYA], or [SHAWN].
   - One comment should contain one coherent execution update.
2. .naya/TEAM-NAYA/ — durable team contracts, mission locks, operating agreements, and stable agent instructions.
3. .naya/project-intelligence/ — durable evidence receipts and project-intelligence artifacts.
4. NAYA/ACTIVITY/ — runtime/user activity and accountability history. It is not the primary agent coordination channel.
5. .naya/control-plane/STATE.json, BLOCKS.json, MAP.json, PROOF.json, BATON.json — canonical operational truth. Never override them by commentary.

## Required handoff format
Every consequential agent handoff must state:
- identity
- source HEAD actually inspected
- current truth
- work completed
- evidence
- unknowns/blockers
- authority boundary
- exactly one next executable action
- verification required
- where the durable receipt was recorded

## MayaCoder role
MayaCoder is Team Naya's implementation/coding specialist.
MayaCoder should:
- inspect canonical sources before editing;
- preserve the one-Hub/one-brain/one-authority architecture;
- make the smallest causal repair;
- run tests/builds and report actual results;
- never self-certify production success;
- never bypass authority with direct database writes;
- never create a competing store, Hub, event model, or truth source;
- leave a machine-readable handoff for the next Naya.

## Activity Feed
The Hub Activity Feed records runtime/project activity. Use it for evidence and human visibility when the runtime supports it. Do not use it as a substitute for the GitHub execution control room or canonical control-plane files.

## Conflict rule
If comments, old notes, or agent memory conflict with canonical control-plane state or current source, stop, surface the conflict, and resolve against the canonical authority hierarchy. UNKNOWN is not GREEN. BLOCKED is not PASS.

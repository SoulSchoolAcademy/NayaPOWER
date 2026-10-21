# IB-SMART-NOTE — SN-0581 — Write Paths Never Mint Authority

Intelligent Block: IB-SMART-NOTE-20261007-sn0581-write-paths-never-mint-authority
Truth state: CANDIDATE
Scope: PRIVATE
Captured: 2026-10-07
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL
A write path writes claims, never authority. The SAFETY driver's top hole: the capture write path could mint or strip authority without evidence — a captured note could arrive carrying truth-state it never earned. The repair: new notes ALWAYS enter as CANDIDATE; truth-state changes require ratification evidence, enforced in code (`tools/smart_note_v2.py`, `tools/truth_state_guard.py`), not by convention.

## HUMAN NOTE
On 2026-10-07 the SAFETY-DRIVER lane closed the highest-leverage safety hole: the capture write path could mint or strip authority without evidence — three documented holes in the POISON battery (PR #1461). In plain terms, something being written into the brain could claim a trust level it was never granted. The fix in PR #1773 (open, awaiting second-seat review): every new note enters as CANDIDATE — always, mechanically — and only ratification evidence can change truth state. Nothing on the write path is allowed to mint authority; the authority travels with the ratification, never with the capture. This is the capture-side twin of the existing rule that auto-capture is not auto-ratify — now enforced in code, because a convention the write path can ignore is not a law. Evidence: #1354 comment 6047433374, PR #1773 (head f3b95779, base f06903ff, CANDIDATE, not merged).

## CHILD NOTE
When you write something in the notebook, you write it in pencil — it just says what you saw. Only the teacher's stamp can make it official. The pencil is never allowed to stamp itself.

## GRANDMA NOTE
Dear, writing something down doesn't make it true. The record-keeper records; only the proper authority approves — and no clever wording in the record can skip that step.

## NAYA NOTE
Standing security law for all capture/ingest paths: the write path is authority-blind. Rules: (1) every ingested object enters at the lowest truth state (CANDIDATE) regardless of what its producer claims; (2) truth-state transitions require independent evidence (ratification) and are enforced by a guard on the transition, not by the writer's honesty; (3) any write path found able to set truth state is a security hole, classified and repaired like any other. When auditing a pipeline, ask: "can this writer mint authority?" — if yes, it's the top hole, above everything else, because a compromised or sloppy writer poisons the whole corpus at its root. This is THE LAW IS THE CODE applied to truth states: ratified law as enforcement points, not comments. Evidence: #1354 comment 6047433374 (SAFETY-DRIVER completion 2026-10-07 ~21:40 UTC), PR #1773 `fix(safety): close truth-state fabrication hole on the capture write path`, POISON battery PR #1461.

## MACHINE NOTE
{
  "smart_note_id": "SN-0581",
  "intelligent_block_id": "IB-SMART-NOTE-20261007-sn0581-write-paths-never-mint-authority",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "category": "SYSTEM_INTELLIGENCE",
  "topic": "GOVERNANCE",
  "subtopic": "SECURITY_POSTURE",
  "captured_at": "2026-10-07",
  "rule": "write_paths_never_mint_authority",
  "invariants": [
    "new notes always enter as CANDIDATE",
    "truth-state transitions require ratification evidence",
    "transition guard enforced in code (tools/truth_state_guard.py), not convention"
  ],
  "finding": "capture write path could mint/strip authority without evidence (3 POISON-battery holes, PR #1461); repaired in PR #1773",
  "evidence": {
    "board_comment": "https://github.com/SoulSchoolAcademy/NayaPOWER/issues/1354#issuecomment-6047425449",
    "safety_completion": "https://github.com/SoulSchoolAcademy/NayaPOWER/issues/1354#issuecomment-6047433374",
    "pr": "https://github.com/SoulSchoolAcademy/NayaPOWER/pull/1773",
    "head": "f3b95779",
    "base": "f06903ff",
    "found_at": "2026-10-07"
  }
}

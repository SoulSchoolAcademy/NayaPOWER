# ACTIVATION-CONTRACT-DRAFT-V1.ai.md — exact specification twin

Status: CANDIDATE DRAFT (not ratified). Machine implementation:
`tools/activation_contract.py`. Machine schema: `tools/activation_contract.schema.json`.
Tests: `tests/test_activation_contract.py` (13 cases: 2 positive-boundary, 11 negative).

## Canonical references (exact values)
- MISSION_STATE_PATH = `BRAIN/CURRENT-MISSION-STATE.md`
- PROTOCOL_PATH = `BRAIN/01-GOVERNANCE/TEAM-NAYA-OPERATING-PROTOCOL-V1.md`
- LIVE_BOARD = 2175 (acknowledged as live; ack text must contain "2175" + a
  live-word: live|current|coordination|board)
- ARCHIVE_BOARD = 1354 (naming it as live → STALE_BOARD → STAND_DOWN)
- TOC_ISSUE = 1599 (ack text must contain "1599")
- CANONICAL_FEEDS = {1865..1873} with ratified names:
  1865 Learning, 1866 Brain/Memory, 1867 Law/Governance,
  1868 Architecture/Engineering/Operations, 1869 Evolution/Succession,
  1870 Interfaces/Hub, 1871 Knowledge/Intelligence, 1872 Proving/Verifying,
  1873 Innovation

## Claim fields (all required; missing → CLAIM_MALFORMED → STAND_DOWN)
worker_id, lane, main_sha ([0-9a-f]{40}), mission_state{path,sha256},
protocol{path,sha256}, feeds_read (non-empty list of canonical ints),
sign_in_feed (canonical int ∈ feeds_read), sign_in_evidence (non-empty str),
board_ack (str), toc_ack (str).

## Verification procedure (fail-closed; order irrelevant — all must pass)
1. main_sha_present: claim.main_sha non-empty.
2. main_sha_fresh: claim.main_sha == live_tip_sha (caller-supplied, independent).
3. mission_state_present: file exists at repo_root + claim path.
4. mission_state_intact: sha256(recomputed tree bytes) == claim hash.
5. protocol_present / 6. protocol_intact: same for protocol.
7. feeds_known: every feeds_read element ∈ CANONICAL_FEEDS.
8. sign_in_feed_valid: sign_in_feed ∈ CANONICAL_FEEDS ∧ ∈ feeds_read.
9. sign_in_evidence: non-empty (receipt marks CLAIMED-UNVERIFIED always).
10. board_ack_current: names 2175 as live. 11. board_not_stale: does not name
    1354 as live. 12. toc_ack: names 1599.
Verdict = PROCEED iff all pass, else STAND_DOWN.

## CLI
`python3 tools/activation_contract.py --claim claim.json --live-tip <sha>
[--repo-root PATH] [--json]`
Exits: 0 PROCEED, 1 STAND_DOWN, 2 tool error.

## Trust boundaries (do not weaken)
- Hashes are recomputed from the tree; the claim's hashes are compared, never trusted.
- live_tip_sha is an independent input (e.g. from a fresh `git ls-remote` / ref read).
- Feed sign-in landing is NOT verifiable locally; the receipt's `unverified`
  list always names it. Any consumer that treats the evidence string as proof
  of landing is misusing the gate.
- Schema pins artifact paths as `const` — a claim pointing at any other path fails.

## Non-goals (explicit)
No changes to ratified law, no behavior change to existing gates
(cold_start_gate.py #1354 marker flagged as follow-up), no protected-workflow
or production touch, no merge claim, no "real-time" claim.
